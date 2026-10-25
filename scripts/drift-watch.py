#!/usr/bin/env python3
"""Report time decay in this tree against public upstream metadata (regime-cutover U81).

uv run --no-project --with pyyaml python -I scripts/drift-watch.py [--root DIR] [--now ISO] [--upstream FIXTURE.json]
prints one Markdown report on stdout, the body .github/workflows/drift-watch.yml writes into its tracking issue, and
exits 0 when it found no drift, 3 when it found drift, 4 when an upstream read failed (the report lists the failures
beside whatever it found; a failed read is never read as "current"). Any other status is a crash with no report.

The checks, all pure reads (no installs, no host state):
- runner-image: every runner label in .github/workflows (`runs-on` and strategy.matrix values) against the
  actions/runner-images announcements whose title announces a deprecation, retirement or removal of that image (by
  OS and major version, e.g. "macOS 14" for macos-14-large) or names the label itself.
- mise-pin: every exact (non-"latest") version in home/dot_mise/config.toml against the newest stable upstream
  release at least minimum_release_age old (the window the same file sets, 72h today).
- manifest-pin: every `pin` and `fallback.pin` in home/dot_agents/agent-config.yaml assets, with the same window;
  a git-commit pin is drift when the default branch has commits past it older than the window.
- plugin-pin: every Claude and Codex plugin pin in that manifest against the plugin.json version its marketplace
  serves now (a marketplace serves its default branch, so there is no release date to apply the window to).
- unrecorded: a `pin: unknown`.
- retired-term: the retired-term lint (RETIRED_TERM_LINT, owned by U72) when this tree has it; each line it prints
  is a finding.
A pin whose upstream the watch cannot read, and the retired-term lint while it is absent, are listed under "Not
watched": they are known gaps, not findings. --upstream replaces the network with a JSON object mapping each URL to
its decoded response (a URL missing from it is a read failure); --now fixes the clock. The GitHub token in
GITHUB_TOKEN, when set, is sent to api.github.com only.
"""

import argparse
import datetime
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
# An announcement counts when its title retires something and that something is an image (not a tool on one, such
# as "Deprecation of simulator runtimes ... on macOS 15"), or when it names the label itself.
RETIREMENT = re.compile(r"deprecat|retir|unsupported|end of life", re.IGNORECASE)
IMAGE_WORD = re.compile(r"\bimages?\b", re.IGNORECASE)
# The only hosts the watch reads; the token goes to the first one only.
HOSTS = ("api.github.com", "registry.npmjs.org", "pypi.org", "www.python.org", "nodejs.org", "dl.google.com")
# mise core tools with an exact pin, and the upstream each one installs from.
MISE_CORE = {
    "node": ("node", ""),
    "python": ("python", ""),
    "fd": ("github", "sharkdp/fd"),
    "uv": ("github", "astral-sh/uv"),
}
RUNNER_LABEL = re.compile(r"(?:ubuntu|macos|windows)-[a-z0-9.]+(?:-[a-z0-9]+)*")
TITLE_IMAGE = re.compile(r"\b(macos|ubuntu|windows)(?:\s+server)?\s+(\d+)", re.IGNORECASE)
PLUGIN_FILES = {
    "claude-plugin": (".claude-plugin/marketplace.json", ".claude-plugin/plugin.json"),
    "codex-plugin": (".agents/plugins/marketplace.json", ".codex-plugin/plugin.json"),
}
# What a response of an unexpected shape raises while it is read: a read failure, never "no drift".
SHAPE_ERRORS = (KeyError, TypeError, ValueError, AttributeError)


class ReadError(Exception):
    """An upstream read that returned no usable answer."""

    def __init__(self, url: str, reason: str, status: int | None = None) -> None:
        super().__init__(f"{url}: {reason}")
        self.status = status


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
    return parts.scheme == "https" and parts.hostname in HOSTS


class AllowedRedirects(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only to HOSTS; the token never follows one (it is an unredirected header)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req, fp, code, msg, headers, newurl) if allowed(newurl) else None


OPENER = urllib.request.build_opener(AllowedRedirects)


class Upstream:
    """Reads JSON from HOSTS, or from a fixture mapping URL to the decoded response."""

    def __init__(self, fixture: dict | None, token: str) -> None:
        self.fixture = fixture
        self.token = token

    def get(self, url: str, raw: bool = False):
        if not allowed(url):
            raise ReadError(url, "not an allowed upstream host")
        if self.fixture is not None:
            if url not in self.fixture:
                raise ReadError(url, "not in the fixture")
            entry = self.fixture[url]
            if isinstance(entry, dict) and set(entry) == {"http_status"}:
                raise ReadError(url, f"HTTP {entry['http_status']}", entry["http_status"])
            return entry
        request = urllib.request.Request(url, headers={"User-Agent": "mryfmo-dotfiles-drift-watch"})
        if urllib.parse.urlsplit(url).hostname == "api.github.com":
            request.add_header("Accept", "application/vnd.github.raw+json" if raw else "application/vnd.github+json")
            request.add_header("X-GitHub-Api-Version", "2022-11-28")
            if self.token:
                request.add_unredirected_header("Authorization", f"Bearer {self.token}")
        try:
            with OPENER.open(request, timeout=30) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            raise ReadError(url, f"HTTP {error.code}", error.code) from None
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            raise ReadError(url, str(error)) from None


def parse_time(text: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(text)


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
    """owner/repo from `owner/repo` or a github.com URL."""
    match = re.fullmatch(r"(?:https://github\.com/)?([\w.-]+/[\w.-]+?)(?:\.git)?/?", text)
    return match[1] if match else None


def releases_of(upstream: Upstream, kind: str, name: str) -> list[Release]:
    if kind == "github":
        items = upstream.get(f"{GITHUB_API}/repos/{name}/releases?per_page=100")
        return [
            Release(
                i["tag_name"],
                i["published_at"] and parse_time(i["published_at"]),
                not i["draft"] and not i["prerelease"],
            )
            for i in items
        ]
    if kind == "npm":
        doc = upstream.get(f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='@')}")
        times = doc["time"]
        return [
            Release(v, parse_time(times[v]), not meta.get("deprecated"))
            for v, meta in doc["versions"].items()
            if v in times
        ]
    if kind == "pypi":
        doc = upstream.get(f"https://pypi.org/pypi/{name}/json")
        found = []
        for version, files in doc["releases"].items():
            if files:
                published = min(parse_time(f["upload_time_iso_8601"]) for f in files)
                found.append(Release(version, published, not all(f["yanked"] for f in files)))
        return found
    if kind == "python":
        # The feed also lists other products ("Python install manager 26.4"); CPython's are "Python X.Y.Z".
        items = upstream.get("https://www.python.org/api/v2/downloads/release/?is_published=true")
        return [
            Release(match[1], parse_time(i["release_date"]), not i["pre_release"])
            for i in items
            if (match := re.fullmatch(r"Python (\d+\.\d+\.\d+\S*)", i["name"]))
        ]
    if kind == "node":
        # index.json dates a release by day only; the end of that day never makes a release look older than it is.
        items = upstream.get("https://nodejs.org/dist/index.json")
        return [Release(i["version"], parse_time(f"{i['date']}T23:59:59Z"), True) for i in items]
    if kind == "gcloud":
        doc = upstream.get("https://dl.google.com/dl/cloudsdk/channels/rapid/components-2.json")
        revision = datetime.datetime.strptime(str(doc["revision"]), "%Y%m%d%H%M%S").replace(tzinfo=datetime.UTC)
        return [Release(doc["version"], revision, True)]
    raise ValueError(kind)


def line_of(root: Path, path: str, pattern: str, after: str = "") -> str:
    """`path:line` of the first line matching pattern (after the first line matching `after`), else `path`."""
    lines = (root / path).read_text().splitlines()
    start = next((n for n, line in enumerate(lines) if re.search(after, line)), 0) if after else 0
    for number in range(start, len(lines)):
        if re.search(pattern, lines[number]):
            return f"{path}:{number + 1}"
    return path


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

    def compare_release(self, check: str, subject: str, pin: str, kind: str, name: str, where: str) -> None:
        try:
            newest = newest_eligible(releases_of(self.upstream, kind, name), self.cutoff)
        except ReadError as error:
            self.failures.append(f"{check} {subject}: {error}")
            return
        except SHAPE_ERRORS as error:
            self.failures.append(f"{check} {subject}: unexpected {kind} response ({error!r})")
            return
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
            announcements = [
                (int(i["number"]), str(i["state"]), str(i["title"]))
                for i in self.upstream.get(url)
                if "pull_request" not in i
            ]
        except ReadError as error:
            self.failures.append(f"runner-image: {error}")
            return
        except SHAPE_ERRORS as error:
            self.failures.append(f"runner-image: unexpected issues response ({error!r})")
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
            source = mise_source(name, spec)
            if source is None:
                self.unwatched.append(f"mise {name} {version} ({where}): no upstream source the watch can read")
                continue
            self.compare_release("mise-pin", name, version, *source, where)

    def manifest_pins(self) -> None:
        assets = (yaml.safe_load((self.root / MANIFEST).read_text()) or {}).get("assets") or {}
        for name, asset in assets.items():
            if asset.get("source") in PLUGIN_FILES:
                self.plugin_pins(name, asset)
                continue
            pins = [
                (field, value)
                for field, value in (
                    ("pin", asset.get("pin")),
                    ("fallback.pin", (asset.get("fallback") or {}).get("pin")),
                )
                if value
            ]
            for field, pin in pins:
                subject = f"{name}.{field}"
                where = line_of(
                    self.root, MANIFEST, rf"^\s+pin: {re.escape(str(pin))}\s*$", rf"^  {re.escape(name)}:\s*$"
                )
                if pin == "unknown":
                    self.findings.append(Finding("unrecorded", subject, "unknown", "-", where))
                    continue
                source = manifest_source(asset)
                if source is None:
                    self.unwatched.append(f"manifest {subject} {pin} ({where}): no upstream source the watch can read")
                elif source[0] == "commit":
                    self.compare_commit(subject, str(pin), source[1], where)
                else:
                    self.compare_release("manifest-pin", subject, str(pin), *source, where)

    def compare_commit(self, subject: str, pin: str, repo: str, where: str) -> None:
        try:
            branch = self.upstream.get(f"{GITHUB_API}/repos/{repo}")["default_branch"]
            compare = self.upstream.get(f"{GITHUB_API}/repos/{repo}/compare/{pin}...{branch}")
            status, ahead = str(compare["status"]), int(compare["ahead_by"])
            dated = [(c["sha"], c["commit"]["committer"]["date"]) for c in compare["commits"]]
            eligible = [(sha, date) for sha, date in dated if parse_time(date) <= self.cutoff]
        except ReadError as error:
            if error.status == 404:
                self.findings.append(
                    Finding("manifest-pin", subject, pin[:12], f"not found in {repo} (HTTP 404)", where)
                )
            else:
                self.failures.append(f"manifest-pin {subject}: {error}")
            return
        except SHAPE_ERRORS as error:
            self.failures.append(f"manifest-pin {subject}: unexpected compare response ({error!r})")
            return
        if status in ("diverged", "behind"):
            self.findings.append(
                Finding("manifest-pin", subject, pin[:12], f"not on {repo}@{branch} ({status})", where)
            )
        elif eligible:
            sha, date = eligible[-1]
            upstream = f"{branch} is {ahead} commits ahead; newest past the window {sha[:12]} ({date[:10]})"
            self.findings.append(Finding("manifest-pin", subject, pin[:12], upstream, where))

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
                self.unwatched.append(
                    f"{subject} {pin} ({where}): marketplace {entry.get('marketplace')} is no GitHub repository"
                )
                continue
            try:
                version = self.plugin_version(repo, plugin, marketplace_file, manifest_file)
            except ReadError as error:
                self.failures.append(f"plugin-pin {subject}: {error}")
                continue
            except SHAPE_ERRORS as error:
                self.failures.append(f"plugin-pin {subject}: unexpected marketplace response ({error!r})")
                continue
            if version is None:
                self.unwatched.append(f"{subject} {pin} ({where}): {repo} lists no readable source for {plugin}")
            elif version != pin:
                self.findings.append(Finding("plugin-pin", subject, pin, f"{version} (marketplace {repo})", where))

    def plugin_version(self, repo: str, plugin: str, marketplace_file: str, manifest_file: str) -> str | None:
        catalog = self.upstream.get(f"{GITHUB_API}/repos/{repo}/contents/{marketplace_file}", raw=True)
        item = next((p for p in catalog.get("plugins", []) if p.get("name") == plugin), None)
        if item is None:
            return f"absent from {marketplace_file}"
        if item.get("version"):
            return str(item["version"])
        source, ref = item.get("source"), ""
        if isinstance(source, str):
            path = posixpath.normpath(posixpath.join(source, manifest_file))
        elif isinstance(source, dict) and source.get("source") in ("url", "github"):
            repo = github_repo(str(source.get("url") or source.get("repo") or ""))
            path, ref = manifest_file, str(source.get("sha") or source.get("ref") or "")
            if repo is None:
                return None
        else:
            return None
        query = f"?ref={urllib.parse.quote(ref)}" if ref else ""
        return str(self.upstream.get(f"{GITHUB_API}/repos/{repo}/contents/{path}{query}", raw=True)["version"])

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


def scalars(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from scalars(item)
    elif isinstance(value, list):
        for item in value:
            yield from scalars(item)
    else:
        yield value


def mise_source(name: str, spec) -> tuple[str, str] | None:
    backend, _, rest = name.partition(":")
    if not rest:
        return MISE_CORE.get(name)
    if backend == "npm":
        return "npm", rest
    if backend in ("github", "aqua"):
        return "github", rest
    if backend == "http" and isinstance(spec, dict):
        urls = [spec.get("url", "")] + [p.get("url", "") for p in (spec.get("platforms") or {}).values()]
        for url in urls:
            if match := re.match(r"https://github\.com/([\w.-]+/[\w.-]+)/", url):
                return "github", match[1]
            if url.startswith("https://storage.googleapis.com/cloud-sdk-release/"):
                return "gcloud", ""
    return None


def manifest_source(asset: dict) -> tuple[str, str] | None:
    source, upstream = asset.get("source"), str(asset.get("upstream", ""))
    if source == "git-commit" and github_repo(upstream):
        return "commit", github_repo(upstream)
    if source in ("github-release", "gh-extension") and github_repo(upstream):
        return "github", github_repo(upstream)
    if source == "https-download":
        if match := re.match(r"https://registry\.npmjs\.org/((?:@[\w.-]+/)?[\w.-]+)/-/", upstream):
            return "npm", match[1]
        if match := re.match(r"https://pypi\.org/project/([\w.-]+)/", upstream):
            return "pypi", match[1]
    return None


def cell(text: str) -> str:
    """Upstream text as an inline code span: no Markdown, links, mentions or table breaks survive in it."""
    flat = re.sub(r"[`|\r\n]+", " ", str(text)).strip()[:160]
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
    parser.add_argument("--now", type=parse_time, default=None)
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
