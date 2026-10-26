#!/usr/bin/env python3
"""Report time decay in this tree against GitHub's public metadata (regime-cutover U81).

uv run --no-project --with pyyaml python -I scripts/drift-watch.py [--root DIR] [--now ISO] [--upstream FIXTURE.json]
prints one Markdown report on stdout, the body .github/workflows/drift-watch.yml writes into its tracking issue, and
exits 0 when it found no drift, 3 when it found drift, 4 when an upstream read failed (the report lists the failures
beside whatever it found; a failed read is never read as "current"). Any other status is a crash with no report.

The watch reads api.github.com only, and only these four things:
- runner-image: every open actions/runner-images announcement whose title mentions a runner label the workflows use
  (`runs-on` and strategy.matrix values in .github/workflows), as "announcement mentions <label>, review". A title
  mentions a label when it contains the label itself (`macos-14`) or its OS name and version (`macOS 14`, `Ubuntu
  24.04` or `Ubuntu 24`, `Windows Server 2025`), each as a whole token. The watch does not decide whether the
  announcement retires the image: a tool or SDK deprecation that mentions a used label is reported on purpose. These
  false positives are intended; the finding asks a human to read the announcement.
- mise-pin and manifest-pin: every exact version in home/dot_mise/config.toml and every `pin` and `fallback.pin` in
  home/dot_agents/agent-config.yaml assets that lives on GitHub, against the newest stable GitHub release at least
  minimum_release_age old (the window home/dot_mise/config.toml sets, 72h today).
- plugin-pin: every Claude and Codex plugin pin in that manifest against each version its marketplace serves now:
  the catalog entry's `version` when it has one and, always, its plugin.json (a marketplace serves its default
  branch, so no release window applies); only an entry with `strict: false` whose directory listing holds no
  manifest directory has no plugin.json, and then its catalog version alone is read. A content pin (`sha256:...`, a Claude plugin with no version, U91) is
  compared with the content hash (scripts/pin_records.py content_digest, the definition make update and make doctor
  use) of the plugin's catalog entry and its directory as the marketplace serves them now: its git tree (recursive, never truncated) and
  each blob, read by the SHA this script took from that tree and checked against the blob's own git SHA-1.
- retired-term: the retired-term lint (RETIRED_TERM_LINT, owned by U72) when this tree has it; each line it prints is
  a finding.
A `pin: unknown` is a finding (unrecorded). Every other pin (npm, PyPI, nodejs.org, python.org, gcloud, git commits,
installer scripts, vendored code) and the retired-term lint while it is absent are listed under "Not watched", with
the reason. Every payload goes through a strict parser for its endpoint, and one that is not exactly the expected
shape, any non-2xx response, and any error while a body is read are read failures. A list endpoint (releases,
announcements) is read page by page from URLs this script builds (`&page=1`, `&page=2`, ... at PER_PAGE items) until a
page holds fewer than PER_PAGE items; no URL the server supplies is followed (the Link header is not read), and a list
still full after MAX_PAGES pages is a read failure, never a cut list. An unexpected exception inside a check is a read
failure of that check, so a report is always written. --upstream replaces the network with a JSON object mapping each
URL to its decoded response (a URL missing from it is a read failure); --now fixes the clock. GITHUB_TOKEN, when set,
is sent to api.github.com and never follows a redirect.
"""

import argparse
import base64
import datetime
import hashlib
import http.client
import importlib.util
import json
import os
import posixpath
import re
import subprocess
import sys
import tomllib
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # main() refuses with a fixed message; importing the module stays possible without it
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
GITHUB_API = "https://api.github.com"
RUNNER_IMAGES = "actions/runner-images"
RETIRED_TERM_LINT = "scripts/lint-retired-terms.py"
MISE_CONFIG = "home/dot_mise/config.toml"
MANIFEST = "home/dot_agents/agent-config.yaml"
WORKFLOWS = ".github/workflows"
OUT_OF_SCOPE = "no strict upstream parser in scope"
# The title words for each runner OS; the version follows them as a whole token.
RUNNER_OS_WORDS = {"macos": r"macOS", "ubuntu": r"Ubuntu", "windows": r"Windows(?:\s+Server)?"}
# A whole token ends where no word character, hyphen, or `.` plus a digit follows (so `macOS 14` is not in
# `macOS 14.5`, and `macos-14` is not in `macos-14-large`).
TOKEN_END = r"(?![\w-]|\.\d)"
TOKEN_START = r"(?<![\w.-])"
RUNNER_LABEL = re.compile(r"(?:ubuntu|macos|windows)-[a-z0-9.]+(?:-[a-z0-9]+)*")
# mise core tools with an exact pin whose releases are on GitHub; every other core tool is not watched.
MISE_CORE_GITHUB = {"fd": "sharkdp/fd", "uv": "astral-sh/uv"}
PLUGIN_FILES = {
    "claude-plugin": (".claude-plugin/marketplace.json", ".claude-plugin/plugin.json"),
    "codex-plugin": (".agents/plugins/marketplace.json", ".codex-plugin/plugin.json"),
}
# Every upstream timestamp, RFC 3339 with the fields range-checked: YYYY-MM-DDTHH:MM:SS, an optional fraction, and
# Z or an offset of at most 23:59. fromisoformat then refuses a day the month does not have (2026-02-30); it is never
# trusted with the rest, since it normalises an offset such as +00:60.
ISO_TIME = re.compile(
    r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d{1,6})?"
    r"(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)"
)
REPO_PART = re.compile(r"[A-Za-z0-9_.-]+")
GIT_REF = re.compile(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*")
MISSING = object()
GIT_SHA = re.compile(r"[0-9a-f]{40}")
# The git modes of a regular file; a symlink (120000) or a submodule (160000) is no reviewable content.
REGULAR_MODES = ("100644", "100755")
TREE_MODE = "040000"
# A symlink and a submodule (gitlink): reported as a finding, since neither is reviewable content.
NOT_CONTENT_MODES = ("120000", "160000")


def load_pin_records():
    """scripts/pin_records.py next to this script: the one definition of a content pin (content_digest)."""
    spec = importlib.util.spec_from_file_location("pin_records", Path(__file__).resolve().parent / "pin_records.py")
    if spec is None or spec.loader is None:
        raise ImportError("cannot load scripts/pin_records.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["pin_records"] = module
    spec.loader.exec_module(module)
    return module


pin_records = load_pin_records()


class ReadError(Exception):
    """An upstream read that returned no usable answer. Its text is a fixed reason and the path of a URL this script
    built; no exception text ever reaches it, since an exception can quote a request header (the token)."""

    def __init__(self, url: str, reason: str) -> None:
        try:
            parts = urllib.parse.urlsplit(url)
            where = f"{parts.path}{'?' + parts.query if parts.query else ''}"
        except ValueError:
            where = "(a URL that does not parse)"
        super().__init__(f"{where}: {reason}")


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
    try:
        parts = urllib.parse.urlsplit(url)
        return parts.scheme == "https" and parts.hostname == "api.github.com" and parts.port is None
    except ValueError:
        # urlsplit or .port refuses the URL (a port such as `api.github.com:bad`): not an allowed URL.
        return False


class AllowedRedirects(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only within api.github.com; the token never follows one (it is an unredirected header)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return super().redirect_request(req, fp, code, msg, headers, newurl) if allowed(newurl) else None


OPENER = urllib.request.build_opener(AllowedRedirects)


# A GitHub token is printable ASCII without spaces; anything else is refused before any request is built, since
# http.client quotes an invalid header value, token included, in its error.
TOKEN_CHARS = re.compile(r"[\x21-\x7e]+")
TOKEN_REFUSED = "GITHUB_TOKEN contains whitespace or a control character; refusing to use it"
# List endpoints are read PER_PAGE items a page; a list still full after MAX_PAGES pages is a read failure.
PER_PAGE = 100
MAX_PAGES = 20


class Upstream:
    """Reads JSON from api.github.com, or from a fixture mapping URL to the decoded response."""

    def __init__(self, fixture: dict | None, token: str) -> None:
        if token and not TOKEN_CHARS.fullmatch(token):
            raise ValueError(TOKEN_REFUSED)
        self.fixture = fixture
        self.token = token

    def get_list(self, base: str) -> list:
        """Every item of a list endpoint. base ends in `per_page=PER_PAGE`; this script appends `&page=N` itself
        (N = 1, 2, ...) and stops at the first page with fewer than PER_PAGE items. Every page must be a JSON list.
        No server-supplied URL (Link header) is read. A list whose MAX_PAGES-th page is still full is a read failure;
        a list is never silently cut."""
        items: list = []
        for number in range(1, MAX_PAGES + 1):
            url = f"{base}&page={number}"
            page = self.get(url)
            if not isinstance(page, list):
                raise ReadError(url, f"unexpected response: a page of the list is {type(page).__name__}")
            items += page
            if len(page) < PER_PAGE:
                return items
        raise ReadError(base, f"more than {MAX_PAGES} pages of {PER_PAGE}")

    def get(self, url: str, raw: bool = False):
        """One response's decoded JSON body."""
        if self.fixture is not None:
            return self.fixture_entry(url)
        body = self.get_bytes(url, raw)
        try:
            # Strict UTF-8, as JSON on the wire must be: json.loads(bytes) would also accept UTF-16 and UTF-32,
            # and a str that starts with a byte-order mark is refused by json.loads.
            return json.loads(body.decode("utf-8"))
        except ValueError as error:
            raise ReadError(url, f"read failed ({type(error).__name__})") from None

    def fixture_entry(self, url: str):
        if not allowed(url):
            raise ReadError(url, "not an allowed upstream host")
        if url not in self.fixture:  # lint-comparisons: allow fixture keys are the exact URLs this script builds
            raise ReadError(url, "not in the fixture")
        entry = self.fixture[url]
        if isinstance(entry, dict) and set(entry) == {"http_status"}:
            raise ReadError(url, f"HTTP {entry['http_status']}")
        return entry

    def get_bytes(self, url: str, raw: bool = False) -> bytes:
        """One response's body as bytes, for a parser that reads the JSON itself (pin_records.parse_catalog_entry).
        In a fixture, a string entry is the body's text and any other entry is serialised as JSON."""
        if self.fixture is not None:
            entry = self.fixture_entry(url)
            return entry.encode() if isinstance(entry, str) else json.dumps(entry).encode()
        if not allowed(url):
            raise ReadError(url, "not an allowed upstream host")
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "mryfmo-dotfiles-drift-watch"})
            request.add_header("Accept", "application/vnd.github.raw+json" if raw else "application/vnd.github+json")
            request.add_header("X-GitHub-Api-Version", "2022-11-28")
            if self.token:
                request.add_unredirected_header("Authorization", f"Bearer {self.token}")
            with OPENER.open(request, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            raise ReadError(url, f"HTTP {int(error.code)}") from None
        # OSError covers URLError, timeouts and a connection reset while the body is read; HTTPException covers
        # IncompleteRead and InvalidURL; ValueError covers a body that is no strict UTF-8 JSON and a URL the request
        # refuses. Only the class name is kept.
        except (OSError, http.client.HTTPException, ValueError) as error:
            raise ReadError(url, f"read failed ({type(error).__name__})") from None


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
    if posixpath.isabs(text) or any(char in text for char in "?#%\\") or any(not_printable(char) for char in text):
        raise shape.fail(f"{what} {text!r} is no plain relative path")
    parts = [part for part in text.split("/") if part not in ("", ".")]
    if ".." in parts:
        raise shape.fail(f"{what} {text!r} leaves the repository")
    return parts


def unique_names(shape: Shape, entries: list, key: str = "name") -> list[str]:
    """Each entry's KEY, in order; an entry named twice is a read failure, so no lookup takes the first of two."""
    names = [shape.key(entry, key, str, "an entry") for entry in entries]
    if len(set(names)) != len(names):
        raise shape.fail(f"an entry {key} appears more than once")
    return names


def not_printable(char: str) -> bool:
    """A Unicode control (Cc: C0, DEL and C1 such as U+0085) or format (Cf: U+200B, U+202E, U+FEFF...) character."""
    return char == "\x7f" or unicodedata.category(char) in ("Cc", "Cf")


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


def mention_pattern(label: str) -> re.Pattern:
    """The whole-token forms in which an announcement title names a runner label: the label, and its OS name and
    version (a dotted version also by its major alone)."""
    forms = [re.escape(label)]
    if match := re.fullmatch(r"(macos|ubuntu|windows)-(\d+)(?:\.(\d+))?(?:-[a-z0-9]+)*", label):
        versions = [re.escape(f"{match[2]}.{match[3]}"), match[2]] if match[3] else [match[2]]
        forms.append(rf"{RUNNER_OS_WORDS[match[1]]}\s+(?:{'|'.join(versions)})")
    # Every interpolated part is re.escape()d, a run of digits from the fullmatch above, or a module constant.
    pattern = rf"{TOKEN_START}(?:{'|'.join(forms)}){TOKEN_END}"
    return re.compile(pattern, re.IGNORECASE)  # lint-comparisons: allow each part is escaped or digits-only


def mise_repo(name: str, spec) -> str | None:
    """The GitHub repository a mise tool's releases come from, or None when they come from anywhere else."""
    backend, _, rest = name.partition(":")
    if not rest:
        return MISE_CORE_GITHUB.get(name)
    if backend in ("github", "aqua"):
        return github_repo(rest)
    if backend != "http" or not isinstance(spec, dict):
        return None
    # An http tool's url, or, when it has none, the url of every platform: one GitHub repository for all of them.
    if isinstance(spec.get("url"), str):
        urls = [spec["url"]]
    else:
        platforms = spec.get("platforms")
        entries = list(platforms.values()) if isinstance(platforms, dict) else []
        urls = [entry.get("url") if isinstance(entry, dict) else None for entry in entries]
    repos = set()
    for url in urls:
        if not isinstance(url, str):
            return None
        parts = urllib.parse.urlsplit(url)
        if (parts.scheme, parts.hostname) != ("https", "github.com"):
            return None
        repos.add(github_repo("/".join(parts.path.split("/")[1:3])))
    return repos.pop() if len(repos) == 1 else None


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
            releases = parse_github_releases(self.upstream.get_list(url), Shape(url))
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
        url = f"{GITHUB_API}/repos/{RUNNER_IMAGES}/issues?labels=Announcement&state=open&per_page=100"
        try:
            announcements = parse_announcements(self.upstream.get_list(url), Shape(url))
        except ReadError as error:
            self.failures.append(f"runner-image: {error}")
            return
        for label, files in sorted(used.items()):
            mentions = mention_pattern(label)
            for number, state, title in announcements:
                if state == "open" and mentions.search(title):
                    recorded = ", ".join(sorted(files))
                    notice = f"announcement mentions {label}, review: {RUNNER_IMAGES}#{number}: {title}"
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
            content = asset["source"] == "claude-plugin" and pin_records.CONTENT_PIN.fullmatch(pin)
            try:
                if content:
                    served, unreadable = self.plugin_content(repo, plugin, marketplace_file)
                else:
                    served, unreadable = self.plugin_versions(repo, plugin, marketplace_file, manifest_file)
            except ReadError as error:
                self.failures.append(f"plugin-pin {subject}: {error}")
                continue
            if unreadable:
                self.unwatched.append(f"plugin-pin {subject} {pin} ({where}): {unreadable}")
            differing = [f"{version} ({place})" for place, version in served if version != pin]
            if differing:
                self.findings.append(Finding("plugin-pin", subject, pin, ", ".join(differing), where))

    def catalog_item(self, repo: str, plugin: str, marketplace_file: str):
        """The plugin's catalog entry in the marketplace (None when the catalog does not list it) and its Shape."""
        url = contents_url(repo, marketplace_file.split("/"))
        shape = Shape(url)
        # The one catalog parser make update and make doctor read the installed clone with: strict JSON, and a
        # plugin listed more than once is refused rather than its first entry taken.
        try:
            return pin_records.parse_catalog_entry(
                self.upstream.get_bytes(url, raw=True), marketplace_file, plugin
            ), shape
        except pin_records.RecordError as error:
            raise shape.fail(str(error)) from None

    @staticmethod
    def plugin_source(item, repo: str, plugin: str, shape: Shape) -> tuple[str, list[str], str, str]:
        """Where a catalog entry's plugin directory lives: (repository, path components, ref, why it cannot be read
        or "")."""
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
                    return "", [], "", f"source {kind} is no GitHub repository"
                ref = shape.key(source, "sha", str, f"{plugin}.source", default="") or shape.key(
                    source, "ref", str, f"{plugin}.source", default=""
                )
                if ref and not GIT_REF.fullmatch(ref):
                    raise shape.fail(f"{plugin}.source ref {ref!r} is no plain git ref")
                source = ""
            else:
                return "", [], "", f"source kind {kind}: {OUT_OF_SCOPE}"
        return repo, repo_path(source, shape, f"{plugin}.source"), ref, ""

    def plugin_versions(
        self, repo: str, plugin: str, marketplace_file: str, manifest_file: str
    ) -> tuple[list[tuple[str, str]], str]:
        """Every version the marketplace serves for plugin (its catalog entry's and its plugin.json's, each with where
        it was read), and why the plugin.json could not be read ("" when it was). A catalog version never stands in
        for plugin.json. Only a catalog entry with `strict: false` (the entry is the plugin's whole definition) may
        have no plugin.json, and only a listing of the plugin's directory with no manifest directory in it proves
        that; a plugin.json that is not served there is still a read failure."""
        item, shape = self.catalog_item(repo, plugin, marketplace_file)
        if item is None:
            return [(f"{repo}/{marketplace_file}", "absent")], ""
        served = []
        if (version := shape.key(item, "version", str, plugin, default=None)) is not None:
            served.append((f"{repo}/{marketplace_file}", version))
        source_repo, parts, ref, unreadable = self.plugin_source(item, repo, plugin, shape)
        if unreadable:
            return served, unreadable
        manifest_dir, manifest_name = manifest_file.split("/")
        if shape.key(item, "strict", bool, plugin, default=True) is False:
            listing_url = contents_url(source_repo, parts, ref)
            listing = Shape(listing_url)
            entries = listing.of(self.upstream.get(listing_url), list, "the directory listing")
            names = unique_names(listing, entries)
            if manifest_dir not in names:  # lint-comparisons: allow entry names, not paths
                if not served:
                    # No value to compare the pin with is a read failure, never "not watched" and never current.
                    raise listing.fail(
                        f"neither the strict: false catalog entry of {plugin} nor a plugin.json sets a version"
                    )
                return served, ""
        parts = [*parts, manifest_dir, manifest_name]
        manifest_url = contents_url(source_repo, parts, ref)
        version = Shape(manifest_url).key(self.upstream.get(manifest_url, raw=True), "version", str)
        served.append((f"{source_repo}/{'/'.join(parts)}", version))
        return served, ""

    def plugin_content(self, repo: str, plugin: str, marketplace_file: str) -> tuple[list[tuple[str, str]], str]:
        """The content pin the marketplace serves for plugin now (pin_records.content_digest over its directory), with
        where it was read. Every URL is built here: the directory's tree SHA comes from its parent's contents listing,
        each blob's from that tree, and a blob whose bytes do not hash to its git SHA-1 is a read failure. A symlink
        or submodule in the tree is reported as the upstream value. A content that cannot be determined (a source
        outside GitHub or of another kind, a plugin at its repository's root) is a read failure, never "not
        watched"."""
        item, shape = self.catalog_item(repo, plugin, marketplace_file)
        if item is None:
            return [(f"{repo}/{marketplace_file}", "absent")], ""
        source_repo, parts, ref, unreadable = self.plugin_source(item, repo, plugin, shape)
        if unreadable:
            raise shape.fail(f"the content of {plugin} cannot be read: {unreadable}")
        if not parts:
            raise shape.fail(f"{plugin} sits at its repository's root: no directory tree to hash for its content pin")
        place = f"{source_repo}/{'/'.join(parts)}"
        listing_url = contents_url(source_repo, parts[:-1], ref)
        listing = Shape(listing_url)
        entries = listing.of(self.upstream.get(listing_url), list, "the directory listing")
        entry = dict(zip(unique_names(listing, entries), entries)).get(parts[-1])
        if entry is None:
            return [(place, "absent")], ""
        if listing.key(entry, "type", str, parts[-1]) != "dir":
            return [(place, "not a directory")], ""
        tree_sha = listing.key(entry, "sha", str, parts[-1])
        if not GIT_SHA.fullmatch(tree_sha):
            raise listing.fail(f"{parts[-1]}.sha {tree_sha!r} is no git SHA")
        tree_url = f"{GITHUB_API}/repos/{source_repo}/git/trees/{tree_sha}?recursive=1"
        tree = Shape(tree_url)
        doc = self.upstream.get(tree_url)
        if tree.key(doc, "truncated", bool):
            raise tree.fail("the tree is truncated")
        files = []
        nodes = tree.key(doc, "tree", list)
        unique_names(tree, nodes, "path")
        for node in nodes:
            path = tree.key(node, "path", str, "a tree entry")
            kind, mode = tree.key(node, "type", str, path), tree.key(node, "mode", str, path)
            repo_path(path, tree, "a tree path")
            # Every entry, a directory included, carries its git object SHA and a mode git defines for its type.
            sha = tree.key(node, "sha", str, path)
            if not GIT_SHA.fullmatch(sha):
                raise tree.fail(f"{path}.sha {sha!r} is no git SHA")
            if mode in NOT_CONTENT_MODES:
                # A symlink or a submodule is no reviewable content: reported as the value served, never current.
                return [(place, f"{path} is not a regular file (git mode {mode})")], ""
            if (kind, mode) == ("tree", TREE_MODE):
                continue
            if kind != "blob" or mode not in REGULAR_MODES:
                raise tree.fail(f"{path} has type {kind!r} with mode {mode!r}, no git tree entry shape")
            files.append((path.encode(), self.blob(source_repo, sha)))
        # The catalog entry is part of what Claude Code loads (strict: false can define servers or hooks in it).
        return [(place, pin_records.content_digest(files, item))], ""

    def blob(self, repo: str, sha: str) -> bytes:
        """A git blob's bytes, proven by its own git SHA-1."""
        url = f"{GITHUB_API}/repos/{repo}/git/blobs/{sha}"
        shape = Shape(url)
        doc = self.upstream.get(url)
        if shape.key(doc, "encoding", str) != "base64":
            raise shape.fail("the blob is not base64")
        try:
            data = base64.b64decode(shape.key(doc, "content", str).replace("\n", ""), validate=True)
        except ValueError:
            raise shape.fail("the blob content is no base64") from None
        if hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest() != sha:  # git's own object id, not a security hash
            raise shape.fail("the blob bytes do not hash to its git SHA")
        return data

    def retired_terms(self) -> None:
        lint = self.root / RETIRED_TERM_LINT
        if not lint.is_file():
            self.unwatched.append(f"retired-term lint: {RETIRED_TERM_LINT} is not in this tree (U72)")
            return
        run = subprocess.run(
            [sys.executable, "-I", str(lint)], cwd=self.root, capture_output=True, text=True, check=False
        )
        if run.returncode not in (0, 1):
            # Only the status: the lint's stderr is not copied into a report that goes into a public issue.
            self.failures.append(f"retired-term: {RETIRED_TERM_LINT} exited {run.returncode}")
            return
        for line in run.stdout.splitlines():
            if line.strip():
                location, _, text = line.partition(": ")
                self.findings.append(Finding("retired-term", text or line, "-", "-", location))
        if run.returncode == 1 and not run.stdout.strip():
            self.failures.append(f"retired-term: {RETIRED_TERM_LINT} exited 1 and printed no hit")

    def run(self) -> None:
        for name, check in (
            ("runner-image", self.runner_images),
            ("mise-pin", self.mise_pins),
            ("manifest-pin", self.manifest_pins),
            ("retired-term", self.retired_terms),
        ):
            try:
                check()
            except Exception as error:  # noqa: BLE001 - any escape still ends in a report, as a read failure
                # The class name only: exception text can quote a request header, the token included.
                self.failures.append(f"{name}: the check stopped on an unexpected {type(error).__name__}")


def code_span(text: str) -> str:
    """Upstream text as an inline code span: no Markdown, links, mentions or table breaks survive in it."""
    flat = re.sub(r"[`|\r\n]+", " ", str(text)).strip()[:400]
    return f"`{flat}`" if flat else "-"


def redact(text: str, token: str) -> str:
    """text with every occurrence of the token replaced, the last guard before anything is written."""
    return text.replace(token, "[redacted]") if token else text


def report(watch: Watch) -> str:
    token = watch.upstream.token

    def cell(text) -> str:
        # Redacted before the cell flattens and truncates it, so no part of the token survives a cut.
        return code_span(redact(str(text), token))

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
    elif watch.failures:
        # Some pins have no upstream value to compare: the run is not clean, so it never says so.
        lines.append("Not clean: the read failures below are unchecked; the pins that were read show no drift.")
    else:
        lines.append("No drift found.")
    if watch.failures:
        lines += ["", f"## Read failures ({len(watch.failures)})", ""] + [f"- {cell(f)}" for f in watch.failures]
    if watch.unwatched:
        lines += ["", f"## Not watched ({len(watch.unwatched)})", ""] + [f"- {cell(u)}" for u in watch.unwatched]
    return redact("\n".join(lines) + "\n", token)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--now", type=cli_time, default=None)
    parser.add_argument("--upstream", type=Path, default=None, help="fixture: JSON object mapping URL to response")
    args = parser.parse_args(argv)
    if yaml is None:
        print("PyYAML is required: uv run --no-project --with pyyaml python -I scripts/drift-watch.py", file=sys.stderr)
        return 2
    fixture = json.loads(args.upstream.read_text()) if args.upstream else None
    now = args.now or datetime.datetime.now(datetime.UTC)
    try:
        upstream = Upstream(fixture, os.environ.get("GITHUB_TOKEN", ""))
    except ValueError:
        print(TOKEN_REFUSED, file=sys.stderr)
        return 2
    watch = Watch(args.root.resolve(), upstream, now)
    watch.run()
    sys.stdout.write(report(watch))
    return 4 if watch.failures else 3 if watch.findings else 0


if __name__ == "__main__":
    sys.exit(main())
