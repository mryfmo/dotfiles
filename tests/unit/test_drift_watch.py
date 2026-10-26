"""scripts/drift-watch.py (regime-cutover U81) on a fixture tree with recorded GitHub responses.

A tree whose every watched pin is current reports nothing even though upstream has newer prereleases, drafts and
releases younger than the 72h window; the same tree with a retiring runner image and old pins reports each one; pins
outside the watched sources are listed as not watched; a failed or misshapen read is a failure, never "current"; no
catalog text changes the URL a plugin.json is read from; the GitHub token reaches api.github.com only. The watch runs
as a subprocess (`python -I`), except for the request-level checks. The script needs PyYAML, and the macOS unit run has
none: a test that runs the script or reads the workflow skips without it; the request-level tests run everywhere.
Fake tokens are built from parts at run time, so the committed-secret scan has no credential-shaped literal to flag.
"""

import base64
import copy
import hashlib
import http.client
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

NO_YAML = "PyYAML is not installed: the script and the workflow parse need it"

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes


def setUpModule() -> None:
    # The watch now loads scripts/pin_records.py (content pins), one of the scripts that resolve agent homes.
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


def fake_token(fill: str) -> str:
    """A token-shaped test value, assembled so no literal in this file looks like a credential."""
    return "_".join(("ghs", fill * 36))


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/drift-watch.py"
NOW = "2026-10-25T00:00:00Z"
GH = "https://api.github.com/repos"
# The first page of each list endpoint the script reads; it builds `&page=N` itself.
RUNNER_ISSUES = f"{GH}/actions/runner-images/issues?labels=Announcement&state=open&per_page=100&page=1"
FD = f"{GH}/sharkdp/fd/releases?per_page=100&page=1"
BATS = f"{GH}/bats-core/bats-core/releases?per_page=100&page=1"
STARSHIP = f"{GH}/starship/starship/releases?per_page=100&page=1"
SHELLCHECK = f"{GH}/koalaman/shellcheck/releases?per_page=100&page=1"
SHELLCHECK_ASSET = "https://github.com/koalaman/shellcheck/releases/download/v0.11.0/shellcheck-v0.11.0"


def page(first: str, number: int) -> str:
    """The URL of page `number` of the list whose first page is `first`."""
    return f"{first.removesuffix('&page=1')}&page={number}"


PONYTAIL = f"{GH}/DietrichGebert/ponytail/contents"
CLAUDE_CATALOG = f"{PONYTAIL}/.claude-plugin/marketplace.json"
CODEX_CATALOG = f"{PONYTAIL}/.agents/plugins/marketplace.json"
OUT_OF_SCOPE = "no strict upstream parser in scope"


def release(tag, published, prerelease=False, draft=False):
    return {"tag_name": tag, "published_at": published, "prerelease": prerelease, "draft": draft}


def workflow(oses):
    return {
        "name": "ci",
        "on": "push",
        "jobs": {"test": {"strategy": {"matrix": {"os": oses}}, "runs-on": "${{ matrix.os }}"}},
    }


CURRENT_MISE = """[tools]
fd = "10.5.0"
jq = "latest"
python = "3.15.1"
"npm:ccusage" = "20.0.40"

[tools."http:bats"]
version = "1.14.0"
url = "https://github.com/bats-core/bats-core/archive/refs/tags/v1.14.0.tar.gz"

[tools."http:gcloud"]
version = "590.0.1"

[tools."http:shellcheck"]
version = "0.11.0"

[tools."http:shellcheck".platforms]
linux-x64 = { url = "{SHELLCHECK_ASSET}.linux.x86_64.tar.xz", checksum = "sha256:00" }
macos-arm64 = { url = "{SHELLCHECK_ASSET}.darwin.aarch64.tar.xz", checksum = "sha256:00" }

[settings]
minimum_release_age = "72h"
""".replace("{SHELLCHECK_ASSET}", SHELLCHECK_ASSET)
CURRENT_MANIFEST = {
    "assets": {
        "starship": {"source": "github-release", "upstream": "starship/starship", "pin": "v1.27.0"},
        "homebrew-installer": {"source": "git-commit", "upstream": "Homebrew/install", "pin": "a" * 40},
        "omp": {
            "source": "https-download",
            "upstream": "https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-18.12.6.tgz",
            "pin": "18.12.6",
        },
        "hcom": {
            "source": "https-download",
            "upstream": "https://pypi.org/project/hcom/0.7.31/#files",
            "pin": "0.7.31",
        },
        "claude-plugins": {
            "source": "claude-plugin",
            "pin": "per-plugin",
            "plugins": {
                "ponytail@ponytail": {"marketplace": "DietrichGebert/ponytail", "pin": "5.3.2"},
                "superpowers": {"marketplace": "anthropics/claude-plugins-official", "pin": "7.0.0"},
            },
        },
        "codex-plugins": {
            "source": "codex-plugin",
            "pin": "per-plugin",
            "plugins": {"ponytail": {"marketplace": "https://github.com/DietrichGebert/ponytail.git", "pin": "5.3.2"}},
        },
    }
}
# The pins of CURRENT_MISE and CURRENT_MANIFEST that no watched source covers.
NOT_WATCHED = (
    "mise-pin python 3.15.1",
    "mise-pin npm:ccusage 20.0.40",
    "mise-pin http:gcloud 590.0.1",
    "manifest-pin homebrew-installer.pin",
    "manifest-pin omp.pin 18.12.6",
    "manifest-pin hcom.pin 0.7.31",
)
SUPERPOWERS_JSON = f"{GH}/obra/superpowers/contents/.claude-plugin/plugin.json?ref={'c' * 40}"
CURRENT_UPSTREAM = {
    RUNNER_ISSUES: [
        {
            "number": 13518,
            "state": "open",
            "title": "[macOS] The macOS 14 Sonoma based runner images will begin deprecation on July 6th",
        },
        # Closed announcements are not reported, even when they mention a used label.
        {"number": 12520, "state": "closed", "title": "[macOS] `macos-latest` YAML-label will use `macos-15` in 2025"},
        {
            "number": 13570,
            "state": "closed",
            "title": "[macOS] Deprecation of simulator runtimes for Xcode 26 on macOS 15",
        },
        # A title naming only an unused label or version is no finding.
        {"number": 14856, "state": "open", "title": "[macOS] OpenSSL will be updated from 3 to 4 on macOS 26"},
        {"number": 7, "state": "open", "title": "macos-15 is retired", "pull_request": {}},
    ],
    FD: [
        release("v10.6.0", "2026-10-24T06:00:00Z"),
        release("v10.5.0", "2026-08-26T00:00:00Z"),
    ],
    BATS: [
        release("v1.15.0", None, draft=True),
        release("v1.15.0-rc1", "2026-09-01T00:00:00Z", prerelease=True),
        release("v1.14.0", "2026-07-21T00:00:00Z"),
    ],
    STARSHIP: [
        release("v1.28.0", "2026-10-24T06:00:00Z"),
        release("v1.27.0", "2026-10-17T00:00:00Z"),
    ],
    SHELLCHECK: [release("v0.11.0", "2025-08-04T00:27:19Z"), release("v0.10.0", "2024-03-08T02:37:35Z")],
    CLAUDE_CATALOG: {"plugins": [{"name": "ponytail", "source": "./"}]},
    f"{PONYTAIL}/.claude-plugin/plugin.json": {"version": "5.3.2"},
    f"{GH}/anthropics/claude-plugins-official/contents/.claude-plugin/marketplace.json": {
        "plugins": [
            {
                "name": "superpowers",
                "source": {"source": "url", "url": "https://github.com/obra/superpowers.git", "sha": "c" * 40},
            }
        ]
    },
    SUPERPOWERS_JSON: {"version": "7.0.0"},
    CODEX_CATALOG: {
        "plugins": [
            {
                "name": "ponytail",
                "source": {"source": "url", "url": "https://github.com/DietrichGebert/ponytail.git", "ref": "main"},
            }
        ]
    },
    f"{PONYTAIL}/.codex-plugin/plugin.json?ref=main": {"version": "5.3.2"},
}


def stale_tree():
    """The current tree aged: a retiring runner image in the matrix and every watched pin a release behind."""
    mise = CURRENT_MISE.replace('fd = "10.5.0"', 'fd = "10.3.0"').replace('version = "1.14.0"', 'version = "1.13.0"')
    mise = mise.replace('version = "0.11.0"', 'version = "0.10.0"')
    manifest = copy.deepcopy(CURRENT_MANIFEST)
    assets = manifest["assets"]
    assets["starship"]["pin"] = "v1.26.0"
    assets["claude-plugins"]["plugins"]["ponytail@ponytail"]["pin"] = "4.10.0"
    assets["codex-plugins"]["plugins"]["ponytail"]["pin"] = "4.10.0"
    assets["gh-extensions"] = {
        "source": "gh-extension",
        "upstream": "https://github.com/seachicken/gh-poi",
        "pin": "unknown",
    }
    return ["ubuntu-24.04", "macos-14", "macos-15"], mise, manifest, copy.deepcopy(CURRENT_UPSTREAM)


STALE = {
    ("runner-image", "macos-14"),
    ("mise-pin", "fd"),
    ("mise-pin", "http:bats"),
    ("mise-pin", "http:shellcheck"),
    ("manifest-pin", "starship.pin"),
    ("plugin-pin", "claude-plugins.ponytail@ponytail"),
    ("plugin-pin", "codex-plugins.ponytail"),
    ("unrecorded", "gh-extensions.pin"),
}


def load_module():
    spec = importlib.util.spec_from_file_location("drift_watch", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MiseRepoTest(unittest.TestCase):
    def test_an_http_tool_is_watched_only_when_every_url_names_one_github_repository(self):
        mise_repo = load_module().mise_repo
        asset = "https://github.com/koalaman/shellcheck/releases/download/v1/s"
        for name, spec, repo in (
            ("one url", {"url": "https://github.com/bats-core/bats-core/archive/v1.tar.gz"}, "bats-core/bats-core"),
            (
                "platforms",
                {"platforms": {"a": {"url": f"{asset}.a"}, "b": {"url": f"{asset}.b"}}},
                "koalaman/shellcheck",
            ),
            (
                "a platform elsewhere",
                {"platforms": {"a": {"url": f"{asset}.a"}, "b": {"url": "https://e.invalid/b"}}},
                None,
            ),
            (
                "two repositories",
                {"platforms": {"a": {"url": f"{asset}.a"}, "b": {"url": "https://github.com/o/r/b"}}},
                None,
            ),
            ("a platform without a url", {"platforms": {"a": {"url": f"{asset}.a"}, "b": {}}}, None),
            ("no url at all", {"version": "1"}, None),
            ("plain http", {"platforms": {"a": {"url": "http://github.com/o/r/a"}}}, None),
        ):
            with self.subTest(name):
                self.assertEqual(repo, mise_repo("http:tool", {"version": "1", **spec}))


class DriftWatchTest(unittest.TestCase):
    def watch(self, oses, mise, manifest, upstream, lint=None, token=None, stderr=""):
        if yaml is None:
            self.skipTest(NO_YAML)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github/workflows").mkdir(parents=True)
            # JSON is YAML, so the fixture tree needs no YAML writer.
            (root / ".github/workflows/ci.yml").write_text(json.dumps(workflow(oses)))
            (root / "home/dot_mise").mkdir(parents=True)
            (root / "home/dot_mise/config.toml").write_text(mise)
            (root / "home/dot_agents").mkdir(parents=True)
            (root / "home/dot_agents/agent-config.yaml").write_text(json.dumps(manifest))
            if lint is not None:
                (root / "scripts").mkdir()
                (root / "scripts/lint-retired-terms.py").write_text(lint)
            (root / "upstream.json").write_text(json.dumps(upstream))
            env = {key: value for key, value in os.environ.items() if key != "GITHUB_TOKEN"}
            if token is not None:
                env["GITHUB_TOKEN"] = token
            command = [sys.executable, "-I", str(SCRIPT), "--root", str(root), "--now", NOW]
            run = subprocess.run(
                [*command, "--upstream", str(root / "upstream.json")],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )
        if token:
            self.assertNotIn(token.strip(), run.stdout + run.stderr)
        self.assertEqual(stderr, run.stderr)
        return run.returncode, run.stdout

    def current(self, change=None, oses=("ubuntu-24.04", "macos-15"), manifest=None):
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        if change:
            change(upstream)
        return self.watch(list(oses), CURRENT_MISE, manifest or CURRENT_MANIFEST, upstream)

    @staticmethod
    def findings(report):
        rows = [
            line for line in report.splitlines() if line.startswith("| ") and not line.startswith(("| check", "| ---"))
        ]
        return {tuple(cell.strip().strip("`") for cell in row.strip("|").split(" | ")[:2]) for row in rows}

    @staticmethod
    def not_watched(report):
        return report.split("## Not watched", 1)[1] if "## Not watched" in report else ""

    def assert_read_failure(self, status, report):
        self.assertEqual(4, status, report)
        self.assertIn("## Read failures (1)", report)

    def test_a_tree_with_every_watched_pin_current_reports_no_drift(self):
        status, report = self.current()
        self.assertEqual(0, status, report)
        self.assertIn("No drift found.", report)
        self.assertEqual(set(), self.findings(report))
        self.assertNotIn("Read failures", report)

    def test_pins_outside_the_watched_sources_are_listed_as_not_watched_with_the_reason(self):
        _, report = self.current()
        listed = self.not_watched(report)
        for entry in NOT_WATCHED:
            with self.subTest(entry):
                line = next(line for line in listed.splitlines() if entry in line)
                self.assertIn(OUT_OF_SCOPE, line)

    def test_a_retiring_runner_image_and_each_stale_pin_are_reported(self):
        status, report = self.watch(*stale_tree())
        self.assertEqual(3, status, report)
        self.assertEqual(STALE, self.findings(report))
        self.assertIn("`v10.5.0 (2026-08-26)`", report, "the newest release past the window, not the fresh v10.6.0")
        self.assertIn("announcement mentions macos-14, review: actions/runner-images#13518", report)

    def test_a_failed_read_is_a_failure_not_current(self):
        for name, change in (
            ("missing", lambda upstream: upstream.pop(STARSHIP)),
            ("http error", lambda upstream: upstream.update({RUNNER_ISSUES: {"http_status": 403}})),
            ("plugin.json 404", lambda upstream: upstream.update({SUPERPOWERS_JSON: {"http_status": 404}})),
        ):
            with self.subTest(name):
                self.assert_read_failure(*self.current(change))

    def test_every_404_is_a_read_failure_and_never_a_missing_pin(self):
        # Codex bot thread on 5a646261: a repository lookup 404 was read as a missing commit pin. The watch now has
        # no 404 that means "absent": a deleted, renamed or private repository is a read failure (exit 4).
        for name, url in (
            ("a release repository", STARSHIP),
            ("a runner announcement list", RUNNER_ISSUES),
            ("a marketplace catalog", CLAUDE_CATALOG),
            ("a plugin.json", SUPERPOWERS_JSON),
        ):
            with self.subTest(name):
                status, report = self.current(lambda upstream, url=url: upstream.update({url: {"http_status": 404}}))
                self.assert_read_failure(status, report)
                self.assertIn("HTTP 404", report)
                self.assertEqual(set(), self.findings(report))

    def test_a_pypi_pin_is_never_read_so_a_yanked_file_cannot_age_it(self):
        # Codex bot thread on 5a646261: a yanked PyPI file made a fresh release look past the window. PyPI is out of
        # scope: the fixture has no pypi.org entry, so any read of it would be a read failure, and none happens.
        old_yanked_then_fresh = {
            "https://pypi.org/pypi/hcom/json": {
                "releases": {
                    "0.7.32": [
                        {"upload_time_iso_8601": "2026-10-01T00:00:00Z", "yanked": True},
                        {"upload_time_iso_8601": "2026-10-24T12:00:00Z", "yanked": False},
                    ]
                }
            }
        }
        status, report = self.current(lambda upstream: upstream.update(old_yanked_then_fresh))
        self.assertEqual(0, status, report)
        self.assertEqual(set(), self.findings(report))
        self.assertIn("manifest-pin hcom.pin 0.7.31 (home/dot_agents/agent-config.yaml", self.not_watched(report))

    def test_a_payload_that_is_not_exactly_the_expected_shape_is_a_read_failure(self):
        for name, change in (
            ("a release list that is an object", lambda upstream: upstream.update({STARSHIP: {}})),
            ("a draft flag that is a string", lambda upstream: upstream[BATS][2].update({"draft": "no"})),
            (
                "a published release with a null date",
                lambda upstream: upstream[STARSHIP][0].update({"published_at": None}),
            ),
            ("an empty published_at", lambda upstream: upstream[STARSHIP][0].update({"published_at": ""})),
            ("an impossible date", lambda upstream: upstream[FD][1].update({"published_at": "2026-02-30T00:00:00Z"})),
            ("a date without a zone", lambda upstream: upstream[FD][1].update({"published_at": "2026-08-26T00:00:00"})),
            (
                "an offset minute of 60",
                lambda upstream: upstream[FD][1].update({"published_at": "2026-08-26T00:00:00+00:60"}),
            ),
            (
                "an offset hour of 24",
                lambda upstream: upstream[FD][1].update({"published_at": "2026-08-26T00:00:00+24:00"}),
            ),
            ("an hour of 25", lambda upstream: upstream[FD][1].update({"published_at": "2026-08-26T25:00:00Z"})),
            ("a second of 60", lambda upstream: upstream[FD][1].update({"published_at": "2026-08-26T00:00:60Z"})),
            ("a month of 13", lambda upstream: upstream[FD][1].update({"published_at": "2026-13-26T00:00:00Z"})),
            ("a draft with an invalid date", lambda upstream: upstream[BATS][0].update({"published_at": "soon"})),
            ("an issue number that is a string", lambda upstream: upstream[RUNNER_ISSUES][0].update({"number": "1"})),
            ("an issue number that is a boolean", lambda upstream: upstream[RUNNER_ISSUES][0].update({"number": True})),
            (
                "a catalog version that is a number",
                lambda upstream: upstream[CLAUDE_CATALOG]["plugins"][0].update({"version": 5}),
            ),
            (
                "a plugin.json version that is a number",
                lambda upstream: upstream[SUPERPOWERS_JSON].update({"version": 7}),
            ),
            ("a catalog without plugins", lambda upstream: upstream.update({CODEX_CATALOG: {}})),
        ):
            with self.subTest(name):
                status, report = self.current(change)
                self.assert_read_failure(status, report)
                self.assertIn("unexpected response", report)

    def test_a_catalog_version_never_hides_an_advanced_plugin_json(self):
        def change(upstream):
            upstream[CLAUDE_CATALOG]["plugins"][0]["version"] = "5.3.2"
            upstream[f"{PONYTAIL}/.claude-plugin/plugin.json"] = {"version": "5.4.0"}

        status, report = self.current(change)
        self.assertEqual(3, status, report)
        self.assertEqual({("plugin-pin", "claude-plugins.ponytail@ponytail")}, self.findings(report))
        self.assertIn("5.4.0 (DietrichGebert/ponytail/.claude-plugin/plugin.json)", report)

    def test_a_codex_plugin_with_a_local_source_is_read_from_its_marketplace_repository(self):
        def local(upstream):
            upstream[CODEX_CATALOG]["plugins"][0]["source"] = {"source": "local", "path": "./plugins/ponytail"}
            upstream[f"{PONYTAIL}/plugins/ponytail/.codex-plugin/plugin.json"] = {"version": "5.4.0"}

        status, report = self.current(local)
        self.assertEqual(3, status, report)
        self.assertEqual({("plugin-pin", "codex-plugins.ponytail")}, self.findings(report))
        self.assertIn("5.4.0 (DietrichGebert/ponytail/plugins/ponytail/.codex-plugin/plugin.json)", report)

        def other(upstream):
            upstream[CODEX_CATALOG]["plugins"][0]["source"] = {"source": "npm", "package": "ponytail"}

        status, report = self.current(other)
        self.assertEqual(0, status, report)
        self.assertIn("codex-plugins.ponytail 5.3.2 (home/dot_agents/agent-config.yaml", self.not_watched(report))
        self.assertIn(f"source kind npm: {OUT_OF_SCOPE}", self.not_watched(report))

    def test_no_catalog_text_changes_the_url_a_plugin_json_is_read_from(self):
        # Each source would, if it reached a URL unchecked, read the fixture's stale-free entry and pass; refused,
        # it is a read failure. The injected URLs are in the fixture with the pinned version to prove it.
        injected = {
            "a query": "./.claude-plugin/plugin.json?ref=old-pin#",
            "a fragment": "./x#",
            "a percent escape": "./%2e%2e/x",
            "a parent directory": "./a/../../x",
            "an absolute path": "/etc",
            "a backslash": ".\\x",
            "a DEL (U+007F)": "./x\x7f",
            "a next line (U+0085)": "./x\x85",
            "a zero-width space (U+200B)": "./x\u200b",
            "a right-to-left override (U+202E)": "./x\u202e",
            "a byte-order mark (U+FEFF)": "./\ufeffx",
        }
        for name, source in injected.items():
            with self.subTest(name):

                def change(upstream, source=source):
                    upstream[CLAUDE_CATALOG]["plugins"][0]["source"] = source
                    upstream[f"{PONYTAIL}/.claude-plugin/plugin.json"] = {"version": "5.4.0"}
                    upstream[f"{PONYTAIL}/.claude-plugin/plugin.json?ref=old-pin#/.claude-plugin/plugin.json"] = {
                        "version": "5.3.2"
                    }

                status, report = self.current(change)
                self.assert_read_failure(status, report)
                self.assertIn("unexpected response", report)

    def test_a_ref_that_is_no_plain_git_ref_is_a_read_failure(self):
        def change(upstream):
            upstream[CODEX_CATALOG]["plugins"][0]["source"]["ref"] = "main&ref=old"
            upstream[f"{PONYTAIL}/.codex-plugin/plugin.json?ref=main&ref=old"] = {"version": "5.3.2"}

        status, report = self.current(change)
        self.assert_read_failure(status, report)

    def test_a_two_page_list_is_read_in_full(self):
        # A full page of 100 means another page may follow; the script asks for page 2 itself.
        older = [{"number": 20000 + n, "state": "open", "title": f"Announcement {n}"} for n in range(100)]
        retiring = {"number": 13518, "state": "open", "title": "The macOS 14 Sonoma runner images will be retired"}

        def runner(upstream):
            upstream[RUNNER_ISSUES] = older
            upstream[page(RUNNER_ISSUES, 2)] = [retiring]

        status, report = self.current(runner, oses=["macos-14"])
        self.assertEqual(3, status, report)
        self.assertEqual({("runner-image", "macos-14")}, self.findings(report))

        def releases(upstream):
            drafts = [release(f"v11.0.{n}", None, draft=True) for n in range(100 - len(upstream[FD]))]
            upstream[FD] = upstream[FD] + drafts
            upstream[page(FD, 2)] = [release("v10.9.0", "2026-09-01T00:00:00Z")]

        status, report = self.current(releases)
        self.assertEqual(3, status, report)
        self.assertIn("`v10.9.0 (2026-09-01)`", report)

        def exactly_full(upstream):
            upstream[RUNNER_ISSUES] = older
            upstream[page(RUNNER_ISSUES, 2)] = []

        self.assertEqual(0, self.current(exactly_full)[0])

    def test_a_list_still_full_after_twenty_pages_is_a_read_failure(self):
        def endless(upstream):
            for number in range(1, 22):
                drafts = [release(f"v99.{number}.{n}", None, draft=True) for n in range(100)]
                upstream[page(FD, number)] = drafts

        status, report = self.current(endless)
        self.assert_read_failure(status, report)
        self.assertIn("more than 20 pages of 100", report)
        status, report = self.current(lambda upstream: upstream.update({FD: {}}))
        self.assert_read_failure(status, report)
        self.assertIn("a page of the list is dict", report)

    def test_an_unexpected_error_in_a_check_is_a_read_failure_and_the_report_is_written(self):
        mise = CURRENT_MISE.replace('jq = "latest"', '"npm:odd" = 5')
        status, report = self.watch(["ubuntu-24.04"], mise, CURRENT_MANIFEST, CURRENT_UPSTREAM)
        self.assert_read_failure(status, report)
        self.assertIn("mise-pin: the check stopped on an unexpected AttributeError", report)
        self.assertIn("# Drift watch", report)

    def test_an_upstream_with_no_release_is_listed_as_not_watched_not_current(self):
        status, report = self.current(lambda upstream: upstream.update({STARSHIP: []}))
        self.assertEqual(0, status, report)
        self.assertIn("manifest-pin starship.pin v1.27.0", self.not_watched(report))

    def test_the_retired_term_lint_is_run_when_the_tree_has_it(self):
        current = (["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, CURRENT_UPSTREAM)
        status, report = self.watch(*current)
        self.assertEqual(0, status, report)
        self.assertIn("scripts/lint-retired-terms.py is not in this tree (U72)", report)
        status, report = self.watch(*current, lint="print('AGENTS.md:3: retired term agmsg')\nraise SystemExit(1)\n")
        self.assertEqual(3, status, report)
        self.assertEqual({("retired-term", "retired term agmsg")}, self.findings(report))
        status, report = self.watch(*current, lint="raise SystemExit(0)\n")
        self.assertEqual(0, status, report)
        status, report = self.watch(*current, lint="raise SystemExit(2)\n")
        self.assertEqual(4, status, report)

    def test_upstream_text_cannot_break_out_of_its_table_cell(self):
        title = "macos-15 will be retired | `x` @someone [link](https://e.invalid)\n## injected"
        status, report = self.current(
            lambda upstream: upstream[RUNNER_ISSUES].append({"number": 9, "state": "open", "title": title}),
            oses=["macos-15"],
        )
        self.assertEqual(3, status, report)
        row = next(line for line in report.splitlines() if "#9" in line)
        upstream_cell = row.strip("|").split(" | ")[3]
        self.assertEqual(6, row.count("|"), row)
        self.assertTrue(upstream_cell.startswith("`") and upstream_cell.endswith("`"), upstream_cell)
        self.assertEqual(2, upstream_cell.count("`"), upstream_cell)
        self.assertNotIn("\n## injected", report)

    def test_a_token_with_a_newline_is_refused_with_a_fixed_message_and_no_report(self):
        refused = "GITHUB_TOKEN contains whitespace or a control character; refusing to use it\n"
        current = (["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, CURRENT_UPSTREAM)
        newline = fake_token("n") + "\n"
        status, report = self.watch(*current, token=newline, stderr=refused)
        self.assertEqual((2, ""), (status, report))

    def test_a_token_that_upstream_text_repeats_is_redacted_from_the_report(self):
        secret = fake_token("t")
        title = f"macos-15 will be retired {secret}"
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[RUNNER_ISSUES].append({"number": 9, "state": "open", "title": title})
        status, report = self.watch(["macos-15"], CURRENT_MISE, CURRENT_MANIFEST, upstream, token=secret)
        self.assertEqual(3, status, report)
        self.assertIn("macos-15 will be retired [redacted]", report)

    def test_an_open_announcement_that_mentions_a_used_label_is_reported_for_review(self):
        # The titles of audit rounds 4 and 5 plus the live retirement title: whether each retires the image or
        # deprecates a tool on it, it mentions the label, so it is reported for a human to read.
        mentioning = [
            ("Deprecation of Python 3.9 on macOS 15 runner images", "macos-15"),
            ("The macOS 15 SDK in runner images will be removed", "macos-15"),
            ("The macOS 15 runner images will be retired from the macOS runner fleet", "macos-15"),
            ("Deprecated packages on macos-15 will be removed", "macos-15"),
            ("[macOS] The macOS 14 Sonoma based runner images will begin deprecation on July 6th", "macos-14"),
            ("[macOS] The macOS 14 Sonoma based runner images will begin deprecation", "macos-14-large"),
            ("[Ubuntu] The Ubuntu 22 based runner images will begin deprecation on September 17th", "ubuntu-22.04"),
            ("[Ubuntu] `ubuntu-latest` label will use Ubuntu 26.04 in November 2026", "ubuntu-26.04"),
            ("The Windows Server 2025 image will be updated", "windows-2025"),
        ]
        # Each names another label or version than the one in use, or the used one only inside a longer token.
        unused = [
            ("The macOS 14 Sonoma based runner images will begin deprecation", "macos-15"),
            ("[macOS] Xcode 16 is removed from macOS 150 images", "macos-15"),
            ("Deprecation on macOS 15.5 point images", "macos-15"),
            ("macos-15-large will be retired", "macos-15"),
            ("[Ubuntu] `ubuntu-latest` label will use Ubuntu 26.04 in November 2026", "ubuntu-24.04"),
            ("Ubuntu 24.10 images are in preview", "ubuntu-24.04"),
            ("[Windows] MySQL will be updated from 8.0 to 8.4", "windows-2025"),
        ]
        for expected, cases in ((True, mentioning), (False, unused)):
            for title, label in cases:
                with self.subTest(title=title, label=label):
                    issue = [{"number": 1, "state": "open", "title": title}]
                    status, report = self.current(
                        lambda upstream, issue=issue: upstream.update({RUNNER_ISSUES: issue}), oses=[label]
                    )
                    self.assertEqual(3 if expected else 0, status, report)
                    self.assertEqual(expected, f"announcement mentions {label}, review" in report, report)

    def test_a_closed_announcement_is_not_reported(self):
        issue = [{"number": 1, "state": "closed", "title": "The macOS 15 runner images will be retired"}]
        status, report = self.current(lambda upstream: upstream.update({RUNNER_ISSUES: issue}), oses=["macos-15"])
        self.assertEqual(0, status, report)

    def test_make_drift_names_the_script_status(self):
        # make turns a failing recipe into its own status 2; the recipe prints the script's status first.
        with tempfile.TemporaryDirectory() as directory:
            stub = Path(directory) / "uv"
            stub.write_text('#!/usr/bin/env bash\n[ "${*: -2}" = "-c import yaml" ] && exit 0\nexit "$RUN_RC"\n')
            stub.chmod(0o755)
            for script_status, make_status in (("0", 0), ("3", 2), ("4", 2)):
                with self.subTest(script_status):
                    env = {**os.environ, "PATH": f"{directory}:{os.environ['PATH']}", "RUN_RC": script_status}
                    env.pop("MAKEFLAGS", None)
                    run = subprocess.run(
                        ["make", "--no-print-directory", "-C", str(ROOT), "drift"],
                        env=env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(make_status, run.returncode, run.stderr)
                    named = f"drift-watch.py exited {script_status} (3: drift, 4: an upstream read failed)"
                    self.assertEqual(script_status != "0", named in run.stderr, run.stderr)

    # U91: a Claude plugin with no version is pinned by content (sha256:..., scripts/pin_records.py content_digest);
    # a strict: false entry may have no plugin.json at all.
    OFFICIAL = f"{GH}/anthropics/claude-plugins-official"
    TREE_SHA = "d" * 40

    @staticmethod
    def git_blob_sha(data: bytes) -> str:
        return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()

    def content_upstream(self, files: dict, extra_nodes=(), truncated=False):
        """CURRENT_UPSTREAM plus frontend-design served as FILES {relative path: bytes} (and pyright-lsp, a strict:
        false entry with a version and no plugin.json), read through the tree and blob endpoints."""
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"]["plugins"] += [
            self.reviewed_entry(),
            {"name": "pyright-lsp", "source": "./plugins/pyright-lsp", "version": "1.0.0", "strict": False},
        ]
        upstream[f"{self.OFFICIAL}/contents/plugins"] = [
            {"name": "frontend-design", "type": "dir", "sha": self.TREE_SHA}
        ]
        upstream[f"{self.OFFICIAL}/contents/plugins/pyright-lsp"] = [{"name": "LICENSE"}, {"name": "README.md"}]
        nodes = []
        for path, data in files.items():
            sha = self.git_blob_sha(data)
            nodes.append({"path": path, "mode": "100644", "type": "blob", "sha": sha})
            upstream[f"{self.OFFICIAL}/git/blobs/{sha}"] = {
                "encoding": "base64",
                "content": base64.encodebytes(data).decode(),
                "sha": sha,
            }
        tree = [{"path": "skills", "mode": "040000", "type": "tree", "sha": "e" * 40}, *nodes, *extra_nodes]
        upstream[f"{self.OFFICIAL}/git/trees/{self.TREE_SHA}?recursive=1"] = {"tree": tree, "truncated": truncated}
        return upstream

    @staticmethod
    def reviewed_files() -> dict:
        reviewed = ROOT / "tests/fixtures/claude-plugins/frontend-design"
        return {str(p.relative_to(reviewed)): p.read_bytes() for p in sorted(reviewed.rglob("*")) if p.is_file()}

    def content_manifest(self, pin: str):
        manifest = copy.deepcopy(CURRENT_MANIFEST)
        manifest["assets"]["claude-plugins"]["plugins"].update(
            {
                "frontend-design@claude-plugins-official": {
                    "marketplace": "anthropics/claude-plugins-official",
                    "pin": pin,
                },
                "pyright-lsp@claude-plugins-official": {
                    "marketplace": "anthropics/claude-plugins-official",
                    "pin": "1.0.0",
                },
            }
        )
        return manifest

    def content_watch(self, upstream, pin=None):
        pin = (
            pin
            or json.loads((ROOT / "scripts/plugin-pins.json").read_text())["claude"][
                "frontend-design@claude-plugins-official"
            ]["pin"]
        )
        return self.watch(["ubuntu-24.04", "macos-15"], CURRENT_MISE, self.content_manifest(pin), upstream)

    def test_a_content_pin_is_compared_with_the_upstream_directory_content(self):
        # The reviewed tree served upstream hashes to the recorded pin: the same definition as make update's.
        status, report = self.content_watch(self.content_upstream(self.reviewed_files()))
        self.assertEqual(0, status, report)
        self.assertNotIn("Read failures", report)
        self.assertEqual(set(), self.findings(report))
        # One changed byte upstream is a plugin-pin finding with the hash served now.
        changed = {**self.reviewed_files(), "README.md": self.reviewed_files()["README.md"] + b"!"}
        status, report = self.content_watch(self.content_upstream(changed))
        self.assertEqual(3, status, report)
        self.assertEqual(
            {("plugin-pin", "claude-plugins.frontend-design@claude-plugins-official")}, self.findings(report)
        )
        self.assertIn("(anthropics/claude-plugins-official/plugins/frontend-design)", report)
        # A symlink in the served tree is no reviewable content: a finding, never a pass.
        link = {"path": "skills/link", "mode": "120000", "type": "blob", "sha": "f" * 40}
        status, report = self.content_watch(self.content_upstream(self.reviewed_files(), [link]))
        self.assertEqual(3, status, report)
        self.assertIn("skills/link is not a regular file (git mode 120000)", report)
        # Round-8 audit: the catalog entry is part of what Claude Code loads, so an entry that adds an LSP server
        # (strict: false) over the same files is a finding, never current.
        upstream = self.content_upstream(self.reviewed_files())
        upstream[f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"]["plugins"][-2].update(
            strict=False, lspServers={"x": {"command": "x"}}
        )
        status, report = self.content_watch(upstream)
        self.assertEqual(3, status, report)
        self.assertEqual(
            {("plugin-pin", "claude-plugins.frontend-design@claude-plugins-official")}, self.findings(report)
        )

    @staticmethod
    def reviewed_entry() -> dict:
        """frontend-design's reviewed catalog entry (tests/fixtures/claude-plugins/marketplaces), part of its pin."""
        clone = ROOT / "tests/fixtures/claude-plugins/marketplaces/claude-plugins-official/.claude-plugin"
        return json.loads((clone / "marketplace.json").read_text())["plugins"][0]

    def test_a_content_read_that_cannot_be_trusted_is_a_read_failure(self):
        files = self.reviewed_files()

        def forged(upstream):
            blob = next(url for url in upstream if "/git/blobs/" in url)  # lint-comparisons: allow a fixture key
            upstream[blob]["content"] = base64.encodebytes(b"other bytes").decode()

        def no_listing(upstream):
            upstream[f"{self.OFFICIAL}/contents/plugins"] = {"http_status": 404}

        for name, upstream in (
            ("a truncated tree", self.content_upstream(files, truncated=True)),
            ("blob bytes that are not its git SHA", self.content_upstream(files)),
            ("the parent listing 404", self.content_upstream(files)),
        ):
            with self.subTest(case=name):
                if name.startswith("blob"):
                    forged(upstream)
                elif name.startswith("the parent"):
                    no_listing(upstream)
                status, report = self.content_watch(upstream)
                self.assert_read_failure(status, report)
                self.assertIn("frontend-design", report.split("## Read failures", 1)[1])

    def test_a_strict_false_entry_without_a_plugin_json_reads_its_catalog_version(self):
        # pyright-lsp: the catalog entry is the whole definition and the directory has no .claude-plugin.
        upstream = self.content_upstream(self.reviewed_files())
        status, report = self.content_watch(upstream)
        self.assertEqual(0, status, report)
        upstream[f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"]["plugins"][-1]["version"] = "1.1.0"
        status, report = self.content_watch(upstream)
        self.assertEqual(3, status, report)
        self.assertIn("1.1.0 (anthropics/claude-plugins-official/.claude-plugin/marketplace.json)", report)
        # A manifest directory in the listing means a plugin.json is read, and one not served is a read failure.
        upstream[f"{self.OFFICIAL}/contents/plugins/pyright-lsp"].append({"name": ".claude-plugin"})
        status, report = self.content_watch(upstream)
        self.assert_read_failure(status, report)
        self.assertIn("pyright-lsp/.claude-plugin/plugin.json: not in the fixture", report)

    def test_a_pinned_plugin_with_no_upstream_value_is_a_read_failure_never_not_watched(self):
        # Round-5 audit: a value that cannot be determined was listed as not watched and the run said "No drift".
        def no_version(upstream):
            entry = upstream[f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"]["plugins"][-1]
            del entry["version"]  # pyright-lsp: strict: false, no catalog version, no plugin.json

        def root_source(upstream):
            upstream[f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"]["plugins"][-2]["source"] = "./"

        def npm_source(upstream):
            entry = upstream[f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"]["plugins"][-2]
            entry["source"] = {"source": "npm", "package": "frontend-design"}

        for name, change, plugin in (
            ("strict: false with no version anywhere", no_version, "pyright-lsp"),
            ("a content pin at the repository root", root_source, "frontend-design"),
            ("a content pin from an npm source", npm_source, "frontend-design"),
        ):
            with self.subTest(case=name):
                upstream = self.content_upstream(self.reviewed_files())
                change(upstream)
                status, report = self.content_watch(upstream)
                self.assert_read_failure(status, report)
                self.assertNotIn("No drift found", report)
                self.assertIn(plugin, report.split("## Read failures", 1)[1])
                self.assertNotIn(plugin, self.not_watched(report))

    def test_a_catalog_or_tree_naming_an_entry_twice_is_a_read_failure(self):
        # Round-9 audit: the first of two catalog entries was taken, while make update and make doctor refuse the
        # catalog. Both sides read it with pin_records.parse_catalog_entry; listings and trees get the same rule.
        catalog = f"{self.OFFICIAL}/contents/.claude-plugin/marketplace.json"

        def duplicate_entry(upstream):
            plugins = upstream[catalog]["plugins"]
            plugins.append({**plugins[-2], "lspServers": {"x": {"command": "x"}}, "strict": False})

        def duplicate_key(upstream):
            text = json.dumps(upstream[catalog])
            upstream[catalog] = text.replace('"name": "frontend-design"', '"name": "frontend-design", "name": "x"', 1)

        def duplicate_listing(upstream):
            listing = upstream[f"{self.OFFICIAL}/contents/plugins"]
            listing.append({**listing[0], "sha": "f" * 40})

        def duplicate_tree_path(upstream):
            tree = upstream[f"{self.OFFICIAL}/git/trees/{self.TREE_SHA}?recursive=1"]["tree"]
            tree.append(dict(tree[-1]))

        for name, change, where in (
            ("the plugin listed twice", duplicate_entry, "listed 2 times, not once"),
            ("a duplicate key in the catalog", duplicate_key, "not strict JSON"),
            ("the plugin directory listed twice", duplicate_listing, "appears more than once"),
            ("a path twice in the tree", duplicate_tree_path, "appears more than once"),
        ):
            with self.subTest(case=name):
                upstream = self.content_upstream(self.reviewed_files())
                change(upstream)
                status, report = self.content_watch(upstream)
                # A catalog that is no strict JSON is refused for every plugin it lists, so count is not checked.
                self.assertEqual(4, status, report)
                self.assertNotIn("No drift found", report)
                failures = report.split("## Read failures", 1)[1]
                self.assertIn("frontend-design", failures)
                self.assertIn(where, failures)

    def test_every_tree_entry_is_validated(self):
        # Round-6 audit: directory entries skipped mode and SHA checks, so a malformed tree read as current.
        tree_path = f"/repos/anthropics/claude-plugins-official/git/trees/{self.TREE_SHA}"
        findings = {
            "a symlink typed as a tree": {"path": "skills/l", "mode": "120000", "type": "tree", "sha": "a" * 40},
            "a submodule": {"path": "skills/m", "mode": "160000", "type": "commit", "sha": "b" * 40},
        }
        for name, node in findings.items():
            with self.subTest(case=name):
                upstream = self.content_upstream(self.reviewed_files(), [node])
                status, report = self.content_watch(upstream)
                self.assertEqual(3, status, report)
                self.assertIn(f"{node['path']} is not a regular file (git mode {node['mode']})", report)
        failures = {
            "a directory with no sha": {"path": "skills/d", "mode": "040000", "type": "tree"},
            "a directory with a short sha": {"path": "skills/d", "mode": "040000", "type": "tree", "sha": "abc"},
            "a directory with a blob mode": {"path": "skills/d", "mode": "100644", "type": "tree", "sha": "c" * 40},
            "an unknown mode": {"path": "skills/x", "mode": "100600", "type": "blob", "sha": "c" * 40},
        }
        for name, node in failures.items():
            with self.subTest(case=name):
                upstream = self.content_upstream(self.reviewed_files(), [node])
                status, report = self.content_watch(upstream)
                self.assert_read_failure(status, report)
                self.assertIn(tree_path, report.split("## Read failures", 1)[1])


class UpstreamTokenTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.requests = []

        def fake_open(request, timeout):
            self.requests.append(request)
            response = mock.MagicMock()
            response.__enter__.return_value.read.return_value = b"{}"
            return response

        patcher = mock.patch.object(self.module.OPENER, "open", side_effect=fake_open)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_the_token_is_an_unredirected_header(self):
        self.module.Upstream(None, "token-value").get("https://api.github.com/repos/o/r/releases?per_page=100")
        (github,) = self.requests
        self.assertEqual("Bearer token-value", github.unredirected_hdrs.get("Authorization"))
        self.assertNotIn("Authorization", github.headers)

    def test_no_request_leaves_api_github_com(self):
        upstream = self.module.Upstream(None, "token-value")
        for url in (
            "https://registry.npmjs.org/ccusage",
            "https://pypi.org/pypi/hcom/json",
            "https://evil.invalid/x",
            "http://api.github.com/repos/o/r",
            "https://api.github.com:8443/repos/o/r",
            "https://api.github.com@evil.invalid/x",
            "https://api.github.com.evil.invalid/x",
        ):
            with self.subTest(url), self.assertRaises(self.module.ReadError):
                upstream.get(url)
        self.assertEqual([], self.requests)
        handler = self.module.AllowedRedirects()
        request = self.module.urllib.request.Request("https://api.github.com/repos/o/r")
        self.assertIsNone(handler.redirect_request(request, None, 302, "Found", {}, "https://evil.invalid/x"))
        self.assertIsNotNone(
            handler.redirect_request(request, None, 302, "Found", {}, "https://api.github.com/repositories/1")
        )

    def test_exception_text_never_reaches_a_read_failure(self):
        # http.client quotes the whole header, token included, when it refuses one.
        error = ValueError("Invalid header value b'Bearer ghs_secret\\n'")
        with (
            mock.patch.object(self.module.OPENER, "open", side_effect=error),
            self.assertRaises(self.module.ReadError) as raised,
        ):
            self.module.Upstream(None, "ghs_secret").get("https://api.github.com/repos/o/r/releases?per_page=100")
        self.assertEqual("/repos/o/r/releases?per_page=100: read failed (ValueError)", str(raised.exception))

    def test_a_token_with_whitespace_or_a_control_character_is_refused(self):
        for token in ("ghs_secret\n", "ghs_secret\nInjected: 1", "ghs secret", "ghs_\tsecret", "ghs_secret\x00"):
            with self.subTest(repr(token)), self.assertRaises(ValueError):
                self.module.Upstream(None, token)
        self.assertEqual([], self.requests)

    def test_the_report_never_contains_the_token(self):
        token = fake_token("s")
        watch = mock.Mock(
            now=self.module.datetime.datetime(2026, 10, 25), window=self.module.datetime.timedelta(hours=72)
        )
        watch.upstream.token = token
        watch.findings = [self.module.Finding("runner-image", token, "x", f"title {token}", "y")]
        watch.failures = [f"/x: {'p' * 395}{token}"]
        watch.unwatched = []
        report = self.module.report(watch)
        self.assertNotIn(token, report)
        self.assertNotIn(token[:8], report, "no cut-off part of the token survives truncation")
        self.assertIn("[redacted]", report)

    def test_an_http_error_is_a_read_failure(self):
        error = urllib.error.HTTPError("https://api.github.com/x", 500, "boom", {}, None)
        with (
            mock.patch.object(self.module.OPENER, "open", side_effect=error),
            self.assertRaises(self.module.ReadError) as raised,
        ):
            self.module.Upstream(None, "").get("https://api.github.com/x")
        self.assertIn("HTTP 500", str(raised.exception))

    def test_pages_come_from_urls_this_script_builds_and_the_link_header_is_ignored(self):
        base = "https://api.github.com/repos/o/r/releases?per_page=100"
        bodies = {f"{base}&page=1": json.dumps([{"n": n} for n in range(100)]).encode(), f"{base}&page=2": b"[]"}
        requested = []

        def open_page(request, timeout):
            requested.append(request.full_url)
            response = mock.MagicMock()
            response.__enter__.return_value.read.return_value = bodies[request.full_url]
            # A server-supplied next link, to another host and with extra parameters: never read.
            response.__enter__.return_value.headers = {"Link": '<https://evil.invalid/p2>; rel="next"; type="x"'}
            return response

        with mock.patch.object(self.module.OPENER, "open", side_effect=open_page):
            items = self.module.Upstream(None, "").get_list(base)
        self.assertEqual(100, len(items))
        self.assertEqual([f"{base}&page=1", f"{base}&page=2"], requested)

    def test_a_url_that_does_not_parse_is_refused_without_an_exception(self):
        upstream = self.module.Upstream(None, "")
        for url in ("https://api.github.com:bad/x", "https://[api.github.com/x"):
            with self.subTest(url):
                self.assertFalse(self.module.allowed(url))
                with self.assertRaises(self.module.ReadError):
                    upstream.get(url)
        handler = self.module.AllowedRedirects()
        request = self.module.urllib.request.Request("https://api.github.com/repos/o/r")
        self.assertIsNone(handler.redirect_request(request, None, 302, "Found", {}, "https://api.github.com:bad/x"))
        self.assertEqual([], self.requests)

    def test_an_error_while_the_body_is_read_is_a_read_failure(self):
        for name, read in (
            ("connection reset", mock.Mock(side_effect=ConnectionResetError(54, "Connection reset by peer"))),
            ("incomplete read", mock.Mock(side_effect=http.client.IncompleteRead(b"{", 10))),
            ("timeout", mock.Mock(side_effect=TimeoutError("timed out"))),
            ("truncated JSON", mock.Mock(return_value=b'{"tag_name": ')),
            ("not UTF-8", mock.Mock(return_value=b"\xff\xfe")),
            ("a UTF-8 byte-order mark", mock.Mock(return_value=b'\xef\xbb\xbf{"a": 1}')),
            ("UTF-16 with a byte-order mark", mock.Mock(return_value='{"a": 1}'.encode("utf-16"))),
            ("UTF-16-LE without one", mock.Mock(return_value='{"a": 1}'.encode("utf-16-le"))),
            ("UTF-32", mock.Mock(return_value='{"a": 1}'.encode("utf-32"))),
        ):
            response = mock.MagicMock()
            response.__enter__.return_value.read = read
            with (
                self.subTest(name),
                mock.patch.object(self.module.OPENER, "open", return_value=response),
                self.assertRaises(self.module.ReadError),
            ):
                self.module.Upstream(None, "").get("https://api.github.com/x")


WORKFLOW = ROOT / ".github/workflows/drift-watch.yml"
# A stub gh. `gh api [--paginate] <issues URL> --jq <filter>` serves GH_ISSUES as the REST issues endpoint does: it
# filters by the URL's state, labels and creator, splits the result into pages of per_page, and runs the step's own jq
# filter over each page, every page only with --paginate. Every other call is logged and succeeds.
GH_STUB = """#!/usr/bin/env python3
import json, os, subprocess, sys, urllib.parse
args = sys.argv[1:]
with open(os.environ["GH_LOG"], "a") as log:
    log.write(" ".join(arg.replace("\\n", " ") for arg in args) + "\\n")
if args[:1] == ["api"]:
    if os.environ.get("GH_LIST_FAIL"):
        sys.exit(1)
    url = next(a for a in args[1:] if a.startswith("repos/"))
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
    wanted = set(query.get("labels", "").split(",")) - {""}
    issues = [
        i for i in json.loads(os.environ["GH_ISSUES"])
        if i["state"] == query.get("state", "open")
        and wanted <= {label["name"] for label in i["labels"]}
        and i["user"]["login"] == query.get("creator", i["user"]["login"])
    ]
    size = int(query.get("per_page", "30"))
    pages = [issues[n:n + size] for n in range(0, len(issues), size)] or [[]]
    for page in pages if "--paginate" in args else pages[:1]:
        jq = args[args.index("--jq") + 1]
        sys.stdout.write(subprocess.run(["jq", "-r", jq], input=json.dumps(page), capture_output=True, text=True,
                                        check=True).stdout)
"""
BOT = "github-actions[bot]"
CREATE = [
    "label create drift-watch --color BFD4F2 --description Tracking issue of the weekly drift watch --force",
    "issue create --title Drift watch --label drift-watch --body-file {}",
]


def issue(number, title="Drift watch", login=BOT, labels=("drift-watch",), state="open"):
    return {
        "number": number,
        "title": title,
        "state": state,
        "user": {"login": login},
        "labels": [{"name": name} for name in labels],
    }


class TrackingIssueStepTest(unittest.TestCase):
    """The workflow's issue step, run with a stub gh: which issue it writes, and that an unclear lookup writes none."""

    def step(self, status, issues, list_fails=False):
        if yaml is None:
            self.skipTest(NO_YAML)
        doc = yaml.safe_load(WORKFLOW.read_text())
        script = next(
            s["run"] for s in doc["jobs"]["drift"]["steps"] if s.get("name") == "Keep the tracking issue current"
        )
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            (temp / "bin").mkdir()
            (temp / "bin/gh").write_text(GH_STUB)
            (temp / "bin/gh").chmod(0o755)
            (temp / "drift.md").write_text("# Drift watch\n")
            env = {
                "PATH": f"{temp / 'bin'}:{os.environ['PATH']}",
                "GH_LOG": str(temp / "gh.log"),
                "GH_ISSUES": json.dumps(issues),
                "GH_REPO": "o/r",
                "RUNNER_TEMP": str(temp),
                "STATUS": status,
                "RUN_URL": "https://github.com/o/r/actions/runs/1",
            }
            if list_fails:
                env["GH_LIST_FAIL"] = "1"
            run = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True, check=False)
            calls = (temp / "gh.log").read_text().splitlines()
        writes = [" ".join("{}" if w.endswith("/drift.md") else w for w in c.split(" ")) for c in calls]
        return run.returncode, [call for call in writes if not call.startswith("api ")]

    def test_the_workflow_runs_only_on_schedule_and_by_hand(self):
        if yaml is None:
            self.skipTest(NO_YAML)
        doc = yaml.safe_load(WORKFLOW.read_text())
        self.assertEqual({"schedule", "workflow_dispatch"}, set(doc[True]))

    def test_drift_opens_one_labelled_issue_and_never_rewrites_an_issue_someone_else_opened(self):
        human = issue(5, login="someone")
        self.assertEqual((0, CREATE), self.step("3", [human]))
        self.assertEqual((0, ["issue edit 7 --body-file {}"]), self.step("4", [human, issue(7)]))

    def test_the_tracking_issue_is_found_behind_more_than_a_hundred_other_bot_issues(self):
        unlabelled = [issue(1000 + n, title=f"Bot issue {n}", labels=()) for n in range(150)]
        # Labelled bot issues with another title fill the first page, so only reading every page finds it.
        labelled = [issue(2000 + n, title=f"Other {n}") for n in range(150)]
        for name, others in (("unlabelled", unlabelled), ("labelled, other titles", labelled)):
            with self.subTest(name):
                self.assertEqual((0, ["issue edit 7 --body-file {}"]), self.step("3", [*others, issue(7)]))

    def test_more_than_one_tracking_issue_fails_the_step_and_writes_nothing(self):
        status, calls = self.step("3", [issue(7), issue(8)])
        self.assertNotEqual(0, status)
        self.assertEqual([], calls)

    def test_a_clean_run_closes_the_open_issue_and_otherwise_writes_nothing(self):
        status, calls = self.step("0", [issue(7), issue(9, state="closed")])
        self.assertEqual(0, status)
        self.assertEqual(
            [
                "issue edit 7 --body-file {}",
                "issue close 7 --comment No drift found: https://github.com/o/r/actions/runs/1",
            ],
            calls,
        )
        self.assertEqual((0, []), self.step("0", []))

    def test_a_failed_issue_lookup_fails_the_step_and_writes_no_issue(self):
        status, calls = self.step("3", [], list_fails=True)
        self.assertNotEqual(0, status)
        self.assertEqual([], calls)


if __name__ == "__main__":
    unittest.main()
