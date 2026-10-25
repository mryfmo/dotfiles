#!/usr/bin/env python3
"""Report time decay in this tree against GitHub's public metadata (regime-cutover U81).

uv run --no-project --with pyyaml python -I scripts/drift-watch.py [--root DIR] [--now ISO] [--upstream FIXTURE.json]
prints one Markdown report on stdout, the body .github/workflows/drift-watch.yml writes into its tracking issue, and
exits 0 when it found no drift, 3 when it found drift, 4 when an upstream read failed (the report lists the failures
beside whatever it found; a failed read is never read as "current"). Any other status is a crash with no report.

The watch reads api.github.com only, and only these four things:
- runner-image: every runner label in .github/workflows (`runs-on` and strategy.matrix values) against the
  actions/runner-images announcements whose title retires an image of that OS and major version (e.g. "macOS 14"
  for macos-14-large) or names the label itself.
- mise-pin and manifest-pin: every exact version in home/dot_mise/config.toml and every `pin` and `fallback.pin` in
  home/dot_agents/agent-config.yaml assets that lives on GitHub, against the newest stable GitHub release at least
  minimum_release_age old (the window home/dot_mise/config.toml sets, 72h today).
- plugin-pin: every Claude and Codex plugin pin in that manifest against each version its marketplace serves now:
  the catalog entry's `version` when it has one and, always, its plugin.json (a marketplace serves its default
  branch, so no release window applies).
- retired-term: the retired-term lint (RETIRED_TERM_LINT, owned by U72) when this tree has it; each line it prints is
  a finding.
A `pin: unknown` is a finding (unrecorded). Every other pin (npm, PyPI, nodejs.org, python.org, gcloud, git commits,
installer scripts, vendored code) and the retired-term lint while it is absent are listed under "Not watched", with
the reason. Every payload goes through a strict parser for its endpoint, and one that is not exactly the expected
shape, any non-2xx response, and any error while a body is read are read failures. --upstream replaces the network
with a JSON object mapping each URL to its decoded response (a URL missing from it is a read failure); --now fixes
the clock. GITHUB_TOKEN, when set, is sent to api.github.com and never follows a redirect.
"""

import argparse
import datetime
import http.client
import json
import os
import posixpath
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
GITHUB_API = "https://api.github.com"
RUNNER_IMAGES = "actions/runner-images"
RETIRED_TERM_LINT = "scripts/lint-retired-terms.py"
MISE_CONFIG = "home/dot_mise/config.toml"
MANIFEST = "home/dot_agents/agent-config.yaml"
WORKFLOWS = ".github/workflows"
OUT_OF_SCOPE = "no strict upstream parser in scope"
# An announcement counts when its title retires something and that something is an image (not a tool on one, such
# as "Deprecation of simulator runtimes ... on macOS 15"), or when it names the label itself.
RETIREMENT = re.compile(r"deprecat|retir|unsupported|end of life", re.IGNORECASE)
IMAGE_WORD = re.compile(r"\bimages?\b", re.IGNORECASE)
RUNNER_LABEL = re.compile(r"(?:ubuntu|macos|windows)-[a-z0-9.]+(?:-[a-z0-9]+)*")
TITLE_IMAGE = re.compile(r"\b(macos|ubuntu|windows)(?:\s+server)?\s+(\d+)", re.IGNORECASE)
# mise core tools with an exact pin whose releases are on GitHub; every other core tool is not watched.
MISE_CORE_GITHUB = {"fd": "sharkdp/fd", "uv": "astral-sh/uv"}
PLUGIN_FILES = {
    "claude-plugin": (".claude-plugin/marketplace.json", ".claude-plugin/plugin.json"),
    "codex-plugin": (".agents/plugins/marketplace.json", ".codex-plugin/plugin.json"),
}
# Every upstream timestamp: date, time, optional fraction, and a zone (Z or +hh:mm).
ISO_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})")
REPO_PART = re.compile(r"[A-Za-z0-9_.-]+")
GIT_REF = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*")
MISSING = object()


class ReadError(Exception):
    """An upstream read that returned no usable answer."""

    def __init__(self, url: str, reason: str) -> None:
        super().__init__(f"{url}: {reason}")


class Shape:
    """Checks one upstream payload against the shape its parser expects; any mismatch is a ReadError for its URL."""

    def __init__(self, url: str) -> None:
        self.url = url

    def fail(self, what: str) -> ReadError:
        return ReadError(self.url, f"unexpected response: {what}")

    def of(self, value, kind, what: str):
        kinds = kind if isinstance(kind, tuple) else (kind,)
        # bool is an int subclass: true or false is never an accepted int.
        if not isinstance(value, kinds) or (isinstance(value, bool) and bool not in kinds):
            raise self.fail(f"{what} is {type(value).__name__}")
        return value

    def key(self, obj, name: str, kind, what: str = "the response", default=MISSING):
        obj = self.of(obj, dict, what)
        if name not in obj:
            if default is not MISSING:
                return default
            raise self.fail(f"{what} has no {name}")
        return self.of(obj[name], kind, f"{what}.{name}")

    def time(self, text, what: str) -> datetime.datetime:
        """The one timestamp parser: a non-empty ISO 8601 date-time with a zone that exists on the calendar."""
        if not isinstance(text, str) or not ISO_TIME.fullmatch(text):
            raise self.fail(f"{what} {text!r} is no ISO date-time with a time zone")
        try:
            return datetime.datetime.fromisoformat(text)
        except ValueError:
            raise self.fail(f"{what} {text!r} is no real date-time") from None


@dataclass(frozen=True)
class Finding:
    check: str
    subject: str
    recorded: str
    upstream: str
    where: str


@dataclass(frozen=True)
class Release:
    version: str
    published: datetime.datetime | None
    stable: bool


def allowed(url: str) -> bool:
    parts = urllib.parse.urlsplit(url)
    return parts.scheme == "https" and parts.hostname == "api.github.com" and parts.port is None


class AllowedRedirects(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only within api.github.com; the token never follows one (it is an unredirected header)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req, fp, code, msg, headers, newurl) if allowed(newurl) else None


OPENER = urllib.request.build_opener(AllowedRedirects)


class Upstream:
    """Reads JSON from api.github.com, or from a fixture mapping URL to the decoded response."""

    def __init__(self, fixture: dict | None, token: str) -> None:
        self.fixture = fixture
        self.token = token

    def get(self, url: str, raw: bool = False):
        if not allowed(url):
            raise ReadError(url, "not an allowed upstream host")
        if self.fixture is not None:
            if url not in self.fixture:  # lint-comparisons: allow fixture keys are the exact URLs this script builds
                raise ReadError(url, "not in the fixture")
            entry = self.fixture[url]
            if isinstance(entry, dict) and set(entry) == {"http_status"}:
                raise ReadError(url, f"HTTP {entry['http_status']}")
            return entry
        request = urllib.request.Request(url, headers={"User-Agent": "mryfmo-dotfiles-drift-watch"})
        request.add_header("Accept", "application/vnd.github.raw+json" if raw else "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if self.token:
            request.add_unredirected_header("Authorization", f"Bearer {self.token}")
        try:
            with OPENER.open(request, timeout=30) as response:
                # Strict UTF-8, as JSON on the wire must be: json.loads(bytes) would also accept UTF-16 and UTF-32,
                # and a str that starts with a byte-order mark is refused by json.loads.
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise ReadError(url, f"HTTP {error.code}") from None
        # OSError covers URLError, timeouts and a connection reset while the body is read; HTTPException covers
        # IncompleteRead; ValueError covers a body that is no strict UTF-8 JSON.
        except (OSError, http.client.HTTPException, ValueError) as error:
            raise ReadError(url, f"{type(error).__name__}: {error}") from None


def cli_time(text: str) -> datetime.datetime:
    value = datetime.datetime.fromisoformat(text)
    if value.tzinfo is None:
        raise argparse.ArgumentTypeError(f"{text!r} has no time zone")
    return value


def version_key(text: str) -> tuple[tuple[int, ...], bool] | None:
    """The numeric core of a version or tag, and whether anything (a prerelease suffix) follows it."""
    match = re.search(r"(\d+(?:\.\d+)*)(.*)$", text)
    if not match:
        return None
    return tuple(int(part) for part in match[1].split(".")), bool(match[2])


def newer(candidate: str, pin: str) -> bool:
    ours, theirs = version_key(pin), version_key(candidate)
    return ours is not None and theirs is not None and theirs[0] > ours[0]


def newest_eligible(releases: list[Release], cutoff: datetime.datetime) -> Release | None:
    eligible = []
    for release in releases:
        key = version_key(release.version)
        if release.stable and key and not key[1] and release.published and release.published <= cutoff:
            eligible.append((key[0], release))
    return max(eligible, key=lambda pair: pair[0])[1] if eligible else None


def github_repo(text: str) -> str | None:
    """owner/repo from `owner/repo` or a https://github.com URL, each part a plain name (never `.` or `..`)."""
    match = re.fullmatch(r"(?:https://github\.com/)?([^/]+)/([^/]+?)(?:\.git)?/?", text)
    if not match:
        return None
    parts = match.groups()
    if all(REPO_PART.fullmatch(part) and part.strip(".") for part in parts):
        return "/".join(parts)
    return None


def repo_path(text: str, shape: Shape, what: str) -> list[str]:
    """The components of a path relative to a repository's root. An absolute path, `..`, `?`, `#`, `%`, a backslash
    or a control character is a read failure, so no catalog text can change the URL it is read from."""
    if posixpath.isabs(text) or any(char in text for char in "?#%\\") or any(ord(char) < 0x20 for char in text):
        raise shape.fail(f"{what} {text!r} is no plain relative path")
    parts = [part for part in text.split("/") if part not in ("", ".")]
    if ".." in parts:
        raise shape.fail(f"{what} {text!r} leaves the repository")
    return parts


def contents_url(repo: str, parts: list[str], ref: str = "") -> str:
    url = f"{GITHUB_API}/repos/{repo}/contents/{urllib.parse.quote('/'.join(parts), safe='/')}"
    return url + (f"?ref={urllib.parse.quote(ref, safe='')}" if ref else "")


def parse_github_releases(doc, shape: Shape) -> list[Release]:
    releases = []
    for item in shape.of(doc, list, "the release list"):
        tag = shape.key(item, "tag_name", str, "a release")
        draft = shape.key(item, "draft", bool, f"release {tag}")
        prerelease = shape.key(item, "prerelease", bool, f"release {tag}")
        published = shape.key(item, "published_at", (str, type(None)), f"release {tag}")
        if published is None and not draft:
            # Only a draft is unpublished; a published release without a date is a broken answer.
            raise shape.fail(f"release {tag} is no draft and has no published_at")
        when = None if published is None else shape.time(published, f"release {tag} published_at")
        releases.append(Release(tag, when, not draft and not prerelease))
    return releases


def parse_announcements(doc, shape: Shape) -> list[tuple[int, str, str]]:
    announcements = []
    for item in shape.of(doc, list, "the issue list"):
        if "pull_request" not in shape.of(item, dict, "an issue"):
            number = shape.key(item, "number", int, "an issue")
            announcements.append(
                (number, shape.key(item, "state", str, "an issue"), shape.key(item, "title", str, "an issue"))
            )
    return announcements


def line_of(root: Path, path: str, pattern: str, after: str = "") -> str:
    """`path:line` of the first line matching pattern (after the first line matching `after`), else `path`."""
    lines = (root / path).read_text().splitlines()
    start = next((n for n, line in enumerate(lines) if re.search(after, line)), 0) if after else 0
    for number in range(start, len(lines)):
        if re.search(pattern, lines[number]):
            return f"{path}:{number + 1}"
    return path


def scalars(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from scalars(item)
    elif isinstance(value, list):
        for item in value:
            yield from scalars(item)
    else:
        yield value


def mise_repo(name: str, spec) -> str | None:
    """The GitHub repository a mise tool's releases come from, or None when they come from anywhere else."""
    backend, _, rest = name.partition(":")
    if not rest:
        return MISE_CORE_GITHUB.get(name)
    if backend in ("github", "aqua"):
        return github_repo(rest)
    if backend == "http" and isinstance(spec, dict) and isinstance(spec.get("url"), str):
        parts = urllib.parse.urlsplit(spec["url"])
        if (parts.scheme, parts.hostname) == ("https", "github.com"):
            return github_repo("/".join(parts.path.split("/")[1:3]))
    return None


class Watch:
    def __init__(self, root: Path, upstream: Upstream, now: datetime.datetime) -> None:
        self.root = root
        self.upstream = upstream
        self.now = now
        self.findings: list[Finding] = []
        self.unwatched: list[str] = []
        self.failures: list[str] = []
        self.window = self.release_window()
        self.cutoff = now - self.window

    def release_window(self) -> datetime.timedelta:
        settings = tomllib.loads((self.root / MISE_CONFIG).read_text()).get("settings", {})
        match = re.fullmatch(r"(\d+)([hd])", str(settings.get("minimum_release_age", "")))
        if not match:
            raise SystemExit(f"{MISE_CONFIG}: [settings] minimum_release_age is not a whole number of hours or days")
        return datetime.timedelta(**{"hours" if match[2] == "h" else "days": int(match[1])})

    def compare_release(self, check: str, subject: str, pin: str, repo: str, where: str) -> None:
        if version_key(pin) is None:
            self.unwatched.append(f"{check} {subject} {pin} ({where}): the pin carries no version number")
            return
        url = f"{GITHUB_API}/repos/{repo}/releases?per_page=100"
        try:
            releases = parse_github_releases(self.upstream.get(url), Shape(url))
        except ReadError as error:
            self.failures.append(f"{check} {subject}: {error}")
            return
        if not releases:
            self.unwatched.append(f"{check} {subject} {pin} ({where}): {repo} lists no GitHub release")
            return
        newest = newest_eligible(releases, self.cutoff)
        if newest and newer(newest.version, pin):
            published = newest.published.strftime("%Y-%m-%d")
            self.findings.append(Finding(check, subject, pin, f"{newest.version} ({published})", where))

    def runner_images(self) -> None:
        used: dict[str, set[str]] = {}
        for path in sorted((self.root / WORKFLOWS).glob("*.y*ml")):
            for job in (yaml.safe_load(path.read_text()).get("jobs") or {}).values():
                for value in scalars([job.get("runs-on"), (job.get("strategy") or {}).get("matrix")]):
                    if isinstance(value, str) and RUNNER_LABEL.fullmatch(value):
                        used.setdefault(value, set()).add(path.name)
        if not used:
            return
        url = f"{GITHUB_API}/repos/{RUNNER_IMAGES}/issues?labels=Announcement&state=all&per_page=100"
        try:
            announcements = parse_announcements(self.upstream.get(url), Shape(url))
        except ReadError as error:
            self.failures.append(f"runner-image: {error}")
            return
        for label, files in sorted(used.items()):
            image = re.match(r"(ubuntu|macos|windows)-(\d+)", label)
            for number, state, title in announcements:
                if not RETIREMENT.search(title):
                    continue
                named = re.search(rf"(?<![\w.-]){re.escape(label)}(?![\w.-])", title)
                retired = (
                    image
                    and IMAGE_WORD.search(title)
                    and any(
                        (os_name.lower(), int(major)) == (image[1], int(image[2]))
                        for os_name, major in TITLE_IMAGE.findall(title)
                    )
                )
                if named or retired:
                    recorded = ", ".join(sorted(files))
                    notice = f"{RUNNER_IMAGES}#{number} ({state}): {title}"
                    self.findings.append(Finding("runner-image", label, recorded, notice, f"{WORKFLOWS}/"))

    def mise_pins(self) -> None:
        for name, spec in tomllib.loads((self.root / MISE_CONFIG).read_text()).get("tools", {}).items():
            version = spec if isinstance(spec, str) else spec.get("version")
            if not version or version == "latest":
                continue
            where = line_of(self.root, MISE_CONFIG, rf'^(\[tools\.)?"?{re.escape(name)}"?[\] =]')
            repo = mise_repo(name, spec)
            if repo is None:
                self.unwatched.append(f"mise-pin {name} {version} ({where}): {OUT_OF_SCOPE}")
                continue
            self.compare_release("mise-pin", name, str(version), repo, where)

    def manifest_pins(self) -> None:
        assets = (yaml.safe_load((self.root / MANIFEST).read_text()) or {}).get("assets") or {}
        for name, asset in assets.items():
            if asset.get("source") in PLUGIN_FILES:  # lint-comparisons: allow a manifest source kind, not a path
                self.plugin_pins(name, asset)
                continue
            fallback = asset.get("fallback") or {}
            for field, pin in (("pin", asset.get("pin")), ("fallback.pin", fallback.get("pin"))):
                if not pin:
                    continue
                subject = f"{name}.{field}"
                where = line_of(
                    self.root, MANIFEST, rf"^\s+pin: {re.escape(str(pin))}\s*$", rf"^  {re.escape(name)}:\s*$"
                )
                if pin == "unknown":
                    self.findings.append(Finding("unrecorded", subject, "unknown", "-", where))
                    continue
                repo = github_repo(str(asset.get("upstream", "")))
                if asset.get("source") not in ("github-release", "gh-extension") or repo is None:
                    self.unwatched.append(
                        f"manifest-pin {subject} {pin} ({where}): {asset.get('source')}: {OUT_OF_SCOPE}"
                    )
                    continue
                self.compare_release("manifest-pin", subject, str(pin), repo, where)

    def plugin_pins(self, asset_name: str, asset: dict) -> None:
        marketplace_file, manifest_file = PLUGIN_FILES[asset["source"]]
        for key, entry in (asset.get("plugins") or {}).items():
            plugin, pin = key.split("@", 1)[0], str(entry.get("pin"))
            subject = f"{asset_name}.{key}"
            where = line_of(self.root, MANIFEST, rf"^\s+{re.escape(key)}:", rf"^  {re.escape(asset_name)}:\s*$")
            if pin == "unknown":
                self.findings.append(Finding("unrecorded", subject, "unknown", "-", where))
                continue
            repo = github_repo(str(entry.get("marketplace", "")))
            if repo is None:
                self.unwatched.append(f"plugin-pin {subject} {pin} ({where}): marketplace is no GitHub repository")
                continue
            try:
                served, unreadable = self.plugin_versions(repo, plugin, marketplace_file, manifest_file)
            except ReadError as error:
                self.failures.append(f"plugin-pin {subject}: {error}")
                continue
            if unreadable:
                self.unwatched.append(f"plugin-pin {subject} {pin} ({where}): {unreadable}")
            differing = [f"{version} ({place})" for place, version in served if version != pin]
            if differing:
                self.findings.append(Finding("plugin-pin", subject, pin, ", ".join(differing), where))

    def plugin_versions(
        self, repo: str, plugin: str, marketplace_file: str, manifest_file: str
    ) -> tuple[list[tuple[str, str]], str]:
        """Every version the marketplace serves for plugin (its catalog entry's and its plugin.json's, each with where
        it was read), and why the plugin.json could not be read ("" when it was). A catalog version never stands in
        for plugin.json."""
        url = contents_url(repo, marketplace_file.split("/"))
        shape = Shape(url)
        items = shape.key(self.upstream.get(url, raw=True), "plugins", list)
        item = next((p for p in items if shape.key(p, "name", str, "a plugin") == plugin), None)
        if item is None:
            return [(f"{repo}/{marketplace_file}", "absent")], ""
        served = []
        if (version := shape.key(item, "version", str, plugin, default=None)) is not None:
            served.append((f"{repo}/{marketplace_file}", version))
        source, ref = shape.key(item, "source", (str, dict), plugin), ""
        if isinstance(source, dict):
            kind = shape.key(source, "source", str, f"{plugin}.source")
            if kind == "local":
                # A local source (the shape generate-agent-configs.py emits) is a directory of the marketplace's own
                # repository, so its plugin.json is read there.
                source = shape.key(source, "path", str, f"{plugin}.source")
            elif kind in ("url", "github"):
                location = shape.key(source, "url" if kind == "url" else "repo", str, f"{plugin}.source")
                repo = github_repo(location)
                if repo is None:
                    return served, f"source {kind} is no GitHub repository"
                ref = shape.key(source, "sha", str, f"{plugin}.source", default="") or shape.key(
                    source, "ref", str, f"{plugin}.source", default=""
                )
                if ref and not GIT_REF.fullmatch(ref):
                    raise shape.fail(f"{plugin}.source ref {ref!r} is no plain git ref")
                source = ""
            else:
                return served, f"source kind {kind}: {OUT_OF_SCOPE}"
        parts = repo_path(source, shape, f"{plugin}.source") + manifest_file.split("/")
        manifest_url = contents_url(repo, parts, ref)
        version = Shape(manifest_url).key(self.upstream.get(manifest_url, raw=True), "version", str)
        served.append((f"{repo}/{'/'.join(parts)}", version))
        return served, ""

    def retired_terms(self) -> None:
        lint = self.root / RETIRED_TERM_LINT
        if not lint.is_file():
            self.unwatched.append(f"retired-term lint: {RETIRED_TERM_LINT} is not in this tree (U72)")
            return
        run = subprocess.run(
            [sys.executable, "-I", str(lint)], cwd=self.root, capture_output=True, text=True, check=False
        )
        if run.returncode not in (0, 1):
            self.failures.append(
                f"retired-term: {RETIRED_TERM_LINT} exited {run.returncode}: {run.stderr.strip()[:200]}"
            )
            return
        for line in run.stdout.splitlines():
            if line.strip():
                location, _, text = line.partition(": ")
                self.findings.append(Finding("retired-term", text or line, "-", "-", location))
        if run.returncode == 1 and not run.stdout.strip():
            self.failures.append(f"retired-term: {RETIRED_TERM_LINT} exited 1 and printed no hit")

    def run(self) -> None:
        self.runner_images()
        self.mise_pins()
        self.manifest_pins()
        self.retired_terms()


def cell(text: str) -> str:
    """Upstream text as an inline code span: no Markdown, links, mentions or table breaks survive in it."""
    flat = re.sub(r"[`|\r\n]+", " ", str(text)).strip()[:400]
    return f"`{flat}`" if flat else "-"


def report(watch: Watch) -> str:
    lines = [
        "# Drift watch",
        "",
        (
            f"Checked {watch.now.strftime('%Y-%m-%dT%H:%MZ')} by `scripts/drift-watch.py` (`make drift`). Release "
            f"window: {watch.window.total_seconds() / 3600:g}h (`{MISE_CONFIG}` minimum_release_age)."
        ),
        "",
    ]
    if watch.findings:
        lines += [
            f"## Findings ({len(watch.findings)})",
            "",
            "| check | subject | recorded | upstream | where |",
            "| --- | --- | --- | --- | --- |",
        ]
        lines += [
            f"| {f.check} | {cell(f.subject)} | {cell(f.recorded)} | {cell(f.upstream)} | {cell(f.where)} |"
            for f in watch.findings
        ]
    else:
        lines.append("No drift found.")
    if watch.failures:
        lines += ["", f"## Read failures ({len(watch.failures)})", ""] + [f"- {cell(f)}" for f in watch.failures]
    if watch.unwatched:
        lines += ["", f"## Not watched ({len(watch.unwatched)})", ""] + [f"- {cell(u)}" for u in watch.unwatched]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--now", type=cli_time, default=None)
    parser.add_argument("--upstream", type=Path, default=None, help="fixture: JSON object mapping URL to response")
    args = parser.parse_args(argv)
    fixture = json.loads(args.upstream.read_text()) if args.upstream else None
    now = args.now or datetime.datetime.now(datetime.UTC)
    watch = Watch(args.root.resolve(), Upstream(fixture, os.environ.get("GITHUB_TOKEN", "")), now)
    watch.run()
    sys.stdout.write(report(watch))
    return 4 if watch.failures else 3 if watch.findings else 0


if __name__ == "__main__":
    sys.exit(main())
