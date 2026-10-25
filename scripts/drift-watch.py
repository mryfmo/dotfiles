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
  a git-commit pin is drift when the default branch has commits past it older than the window, and absent when the
  compare endpoint answers 404 after the repository itself was read (the only read where 404 means "absent"; any
  other failed read, a repository 404 included, is a read failure).
- plugin-pin: every Claude and Codex plugin pin in that manifest against each version its marketplace serves now: the
  catalog entry's `version` when it has one and, always, the plugin.json its source points at (a relative path or a
  `local` source is read in the marketplace's own repository; a marketplace serves its default branch, so there is
  no release date to apply the window to).
- unrecorded: a `pin: unknown`.
- retired-term: the retired-term lint (RETIRED_TERM_LINT, owned by U72) when this tree has it; each line it prints
  is a finding.
A pin whose upstream the watch cannot read, and the retired-term lint while it is absent, are listed under "Not
watched": they are known gaps, not findings. Every upstream payload goes through its source's parse function, and one
that is not exactly the expected shape is a read failure. --upstream replaces the network with a JSON object mapping
each URL to its decoded response (a URL missing from it is a read failure); --now fixes the clock. The GitHub token in
GITHUB_TOKEN, when set, is sent to api.github.com only.
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


class ReadError(Exception):
    """An upstream read that returned no usable answer."""

    def __init__(self, url: str, reason: str, status: int | None = None) -> None:
        super().__init__(f"{url}: {reason}")
        self.status = status


MISSING = object()
# Every upstream timestamp: date, time, optional fraction, and a zone (Z or +hh:mm).
ISO_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})")


class Shape:
    """Checks one upstream payload against the shape its parser expects; any mismatch is a ReadError for its URL."""

    def __init__(self, url: str) -> None:
        self.url = url

    def fail(self, what: str) -> ReadError:
        return ReadError(self.url, f"unexpected response: {what}")

    def of(self, value, kind, what: str):
        if not isinstance(value, kind) or (isinstance(value, bool) and kind is int):
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
        """The one timestamp parser of every source: a non-empty ISO 8601 date-time with a time zone, and a real one
        (2026-02-30 is refused); anything else is a read failure."""
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
            if url not in self.fixture:  # lint-comparisons: allow fixture keys are the exact URLs this script builds
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
                # Strict UTF-8, as JSON on the wire must be: json.loads(bytes) would also accept UTF-16 and UTF-32,
                # and a str that starts with a byte-order mark is refused by json.loads.
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            raise ReadError(url, f"HTTP {error.code}", error.code) from None
        # OSError covers URLError, timeouts and a connection reset while the body is read; HTTPException covers
        # IncompleteRead; ValueError covers a body that is no UTF-8 JSON.
        except (OSError, http.client.HTTPException, ValueError) as error:
            raise ReadError(url, f"{type(error).__name__}: {error}") from None


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


def release_url(kind: str, name: str) -> str:
    return {
        "github": f"{GITHUB_API}/repos/{name}/releases?per_page=100",
        "npm": f"https://registry.npmjs.org/{urllib.parse.quote(name, safe='@')}",
        "pypi": f"https://pypi.org/pypi/{name}/json",
        "python": "https://www.python.org/api/v2/downloads/release/?is_published=true",
        "node": "https://nodejs.org/dist/index.json",
        "gcloud": "https://dl.google.com/dl/cloudsdk/channels/rapid/components-2.json",
    }[kind]


def parse_github_releases(doc, shape: Shape) -> list[Release]:
    releases = []
    for item in shape.of(doc, list, "the release list"):
        published = shape.key(item, "published_at", (str, type(None)), "a release")
        stable = not shape.key(item, "draft", bool, "a release") and not shape.key(
            item, "prerelease", bool, "a release"
        )
        releases.append(
            Release(
                shape.key(item, "tag_name", str, "a release"),
                # null is GitHub's value for a draft; any string, the empty one included, must be a real time.
                None if published is None else shape.time(published, "published_at"),
                stable,
            )
        )
    return releases


def parse_npm(doc, shape: Shape) -> list[Release]:
    times = shape.key(doc, "time", dict)
    releases = []
    for version, meta in shape.key(doc, "versions", dict).items():
        deprecated = shape.key(meta, "deprecated", (str, bool), f"versions.{version}", default=False)
        published = shape.time(shape.key(times, version, str, "time"), f"time.{version}")
        releases.append(Release(version, published, not deprecated))
    return releases


def parse_pypi(doc, shape: Shape) -> list[Release]:
    # A yanked file is no release: a version's age is its earliest non-yanked upload, and a version whose files are
    # all yanked (or that has none) is skipped.
    releases = []
    for version, files in shape.key(doc, "releases", dict).items():
        uploads = []
        for file in shape.of(files, list, f"releases.{version}"):
            uploaded = shape.key(file, "upload_time_iso_8601", str, f"a {version} file")
            if not shape.key(file, "yanked", bool, f"a {version} file"):
                uploads.append(shape.time(uploaded, "upload_time_iso_8601"))
        if uploads:
            releases.append(Release(version, min(uploads), True))
    return releases


def parse_python(doc, shape: Shape) -> list[Release]:
    # The feed also lists other products ("Python install manager 26.4"); CPython's are "Python X.Y.Z".
    releases = []
    for item in shape.of(doc, list, "the release list"):
        name = shape.key(item, "name", str, "a release")
        if match := re.fullmatch(r"Python (\d+\.\d+\.\d+\S*)", name):
            published = shape.time(shape.key(item, "release_date", str, name), "release_date")
            releases.append(Release(match[1], published, not shape.key(item, "pre_release", bool, name)))
    return releases


def parse_node(doc, shape: Shape) -> list[Release]:
    # index.json dates a release by day only; the end of that day never makes a release look older than it is.
    releases = []
    for item in shape.of(doc, list, "index.json"):
        date = shape.key(item, "date", str, "a release")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            raise shape.fail(f"date {date!r} is no YYYY-MM-DD")
        published = shape.time(f"{date}T23:59:59Z", "date")
        releases.append(Release(shape.key(item, "version", str, "a release"), published, True))
    return releases


def parse_gcloud(doc, shape: Shape) -> list[Release]:
    revision = str(shape.key(doc, "revision", int))
    try:
        published = datetime.datetime.strptime(revision, "%Y%m%d%H%M%S").replace(tzinfo=datetime.UTC)
    except ValueError:
        raise shape.fail(f"revision {revision} is no timestamp") from None
    return [Release(shape.key(doc, "version", str), published, True)]


RELEASE_PARSERS = {
    "github": parse_github_releases,
    "npm": parse_npm,
    "pypi": parse_pypi,
    "python": parse_python,
    "node": parse_node,
    "gcloud": parse_gcloud,
}


def releases_of(upstream: Upstream, kind: str, name: str) -> list[Release]:
    url = release_url(kind, name)
    return RELEASE_PARSERS[kind](upstream.get(url), Shape(url))


def parse_announcements(doc, shape: Shape) -> list[tuple[int, str, str]]:
    announcements = []
    for item in shape.of(doc, list, "the issue list"):
        if "pull_request" not in shape.of(item, dict, "an issue"):
            number = shape.key(item, "number", int, "an issue")
            announcements.append(
                (number, shape.key(item, "state", str, "an issue"), shape.key(item, "title", str, "an issue"))
            )
    return announcements


def parse_compare(doc, shape: Shape) -> tuple[str, int, list[tuple[str, datetime.datetime]]]:
    commits = []
    for item in shape.key(doc, "commits", list):
        committer = shape.key(shape.key(item, "commit", dict, "a commit"), "committer", dict, "commit")
        date = shape.time(shape.key(committer, "date", str, "committer"), "committer.date")
        commits.append((shape.key(item, "sha", str, "a commit"), date))
    return shape.key(doc, "status", str), shape.key(doc, "ahead_by", int), commits


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
        if version_key(pin) is None:
            self.unwatched.append(f"{check} {subject} {pin} ({where}): the pin carries no version number")
            return
        try:
            releases = releases_of(self.upstream, kind, name)
            newest = newest_eligible(releases, self.cutoff)
        except ReadError as error:
            self.failures.append(f"{check} {subject}: {error}")
            return
        if not releases:
            self.unwatched.append(f"{check} {subject} {pin} ({where}): {kind} {name} lists no release")
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
            source = mise_source(name, spec)
            if source is None:
                self.unwatched.append(f"mise {name} {version} ({where}): no upstream source the watch can read")
                continue
            self.compare_release("mise-pin", name, version, *source, where)

    def manifest_pins(self) -> None:
        assets = (yaml.safe_load((self.root / MANIFEST).read_text()) or {}).get("assets") or {}
        for name, asset in assets.items():
            if asset.get("source") in PLUGIN_FILES:  # lint-comparisons: allow a manifest source kind, not a path
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
        repo_url = f"{GITHUB_API}/repos/{repo}"
        try:
            branch = Shape(repo_url).key(self.upstream.get(repo_url), "default_branch", str)
        except ReadError as error:
            # Any failed repository read, a 404 included, is a read failure: it says nothing about the pin.
            self.failures.append(f"manifest-pin {subject}: {error}")
            return
        compare_url = f"{GITHUB_API}/repos/{repo}/compare/{pin}...{branch}"
        try:
            status, ahead, commits = parse_compare(self.upstream.get(compare_url), Shape(compare_url))
        except ReadError as error:
            # Only here does 404 mean "absent": the repository and its default branch were just read, so the compare
            # endpoint's 404 means the pinned commit is not in the repository.
            if error.status == 404:
                self.findings.append(
                    Finding("manifest-pin", subject, pin[:12], f"not found in {repo} (HTTP 404)", where)
                )
            else:
                self.failures.append(f"manifest-pin {subject}: {error}")
            return
        eligible = [(sha, date) for sha, date in commits if date <= self.cutoff]
        if status in ("diverged", "behind"):
            self.findings.append(
                Finding("manifest-pin", subject, pin[:12], f"not on {repo}@{branch} ({status})", where)
            )
        elif eligible:
            sha, date = eligible[-1]
            upstream = f"{branch} is {ahead} commits ahead; newest past the window {sha[:12]} ({date:%Y-%m-%d})"
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
                served, readable = self.plugin_versions(repo, plugin, marketplace_file, manifest_file)
            except ReadError as error:
                self.failures.append(f"plugin-pin {subject}: {error}")
                continue
            if not readable:
                self.unwatched.append(
                    f"{subject} {pin} ({where}): {repo} serves {plugin} from a source the watch cannot read"
                )
            differing = [f"{version} ({place})" for place, version in served if version != pin]
            if differing:
                self.findings.append(Finding("plugin-pin", subject, pin, ", ".join(differing), where))

    def plugin_versions(
        self, repo: str, plugin: str, marketplace_file: str, manifest_file: str
    ) -> tuple[list[tuple[str, str]], bool]:
        """Every version the marketplace serves for plugin (its catalog entry's and its plugin.json's, each with where
        it was read), and whether the plugin.json was readable. A catalog version never stands in for plugin.json."""
        url = f"{GITHUB_API}/repos/{repo}/contents/{marketplace_file}"
        shape = Shape(url)
        items = shape.key(self.upstream.get(url, raw=True), "plugins", list)
        item = next((p for p in items if shape.key(p, "name", str, "a plugin") == plugin), None)
        if item is None:
            return [(f"{repo}/{marketplace_file}", "absent")], True
        served = []
        if (version := shape.key(item, "version", str, plugin, default=None)) is not None:
            served.append((f"{repo}/{marketplace_file}", version))
        source, ref = shape.key(item, "source", (str, dict), plugin), ""
        if isinstance(source, dict) and shape.key(source, "source", str, f"{plugin}.source") == "local":
            # A local source (the shape generate-agent-configs.py emits) is a directory of the marketplace's own
            # repository, so its plugin.json is read there.
            source = shape.key(source, "path", str, f"{plugin}.source")
        if isinstance(source, str):
            path = posixpath.normpath(posixpath.join(source, manifest_file))
            # The first component of the normalised path: ".." leaves the repository, "" is an absolute path.
            if posixpath.normpath(path).split("/", 1)[0] in ("..", ""):
                raise shape.fail(f"{plugin}.source {source!r} leaves the marketplace repository")
        else:
            kind = shape.key(source, "source", str, f"{plugin}.source")
            location = shape.key(source, "url" if kind == "url" else "repo", str, f"{plugin}.source", default="")
            repo = github_repo(location) if kind in ("url", "github") else None
            if repo is None:
                return served, False
            path = manifest_file
            ref = shape.key(source, "sha", str, f"{plugin}.source", default="") or shape.key(
                source, "ref", str, f"{plugin}.source", default=""
            )
        manifest_url = f"{GITHUB_API}/repos/{repo}/contents/{path}" + (f"?ref={urllib.parse.quote(ref)}" if ref else "")
        served.append(
            (f"{repo}/{path}", Shape(manifest_url).key(self.upstream.get(manifest_url, raw=True), "version", str))
        )
        return served, True

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
            parts = urllib.parse.urlsplit(url)
            if (parts.hostname, parts.path.split("/")[1:2]) == ("storage.googleapis.com", ["cloud-sdk-release"]):
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
