"""scripts/drift-watch.py (regime-cutover U81) on a fixture tree with recorded GitHub responses.

A tree whose every watched pin is current reports nothing even though upstream has newer prereleases, drafts and
releases younger than the 72h window; the same tree with a retiring runner image and old pins reports each one; pins
outside the watched sources are listed as not watched; a failed or misshapen read is a failure, never "current"; no
catalog text changes the URL a plugin.json is read from; the GitHub token reaches api.github.com only. The watch runs
as a subprocess (`python -I`), except for the request-level checks.
"""

import copy
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

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/drift-watch.py"
NOW = "2026-10-25T00:00:00Z"
GH = "https://api.github.com/repos"
RUNNER_ISSUES = f"{GH}/actions/runner-images/issues?labels=Announcement&state=open&per_page=100"
FD = f"{GH}/sharkdp/fd/releases?per_page=100"
BATS = f"{GH}/bats-core/bats-core/releases?per_page=100"
STARSHIP = f"{GH}/starship/starship/releases?per_page=100"
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

[settings]
minimum_release_age = "72h"
"""
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


class DriftWatchTest(unittest.TestCase):
    def watch(self, oses, mise, manifest, upstream, lint=None, token=None, stderr=""):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text(yaml.safe_dump(workflow(oses)))
            (root / "home/dot_mise").mkdir(parents=True)
            (root / "home/dot_mise/config.toml").write_text(mise)
            (root / "home/dot_agents").mkdir(parents=True)
            (root / "home/dot_agents/agent-config.yaml").write_text(yaml.safe_dump(manifest))
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

    def test_every_page_of_a_list_endpoint_is_read(self):
        older = [{"number": 20000 + n, "state": "open", "title": f"Announcement {n}"} for n in range(100)]
        retiring = {"number": 13518, "state": "open", "title": "The macOS 14 Sonoma runner images will be retired"}
        page_two = f"{RUNNER_ISSUES}&page=2"

        def runner(upstream):
            upstream[RUNNER_ISSUES] = {"body": older, "link_next": page_two}
            upstream[page_two] = [retiring]

        status, report = self.current(runner, oses=["macos-14"])
        self.assertEqual(3, status, report)
        self.assertEqual({("runner-image", "macos-14")}, self.findings(report))

        fd_two = f"{FD}&page=2"

        def releases(upstream):
            upstream[FD] = {"body": upstream[FD], "link_next": fd_two}
            upstream[fd_two] = [release("v10.9.0", "2026-09-01T00:00:00Z")]

        status, report = self.current(releases)
        self.assertEqual(3, status, report)
        self.assertIn("`v10.9.0 (2026-09-01)`", report)

    def test_a_list_that_does_not_end_or_leaves_api_github_com_is_a_read_failure(self):
        def endless(upstream):
            for page in range(1, 22):
                url = FD if page == 1 else f"{FD}&page={page}"
                upstream[url] = {"body": [], "link_next": f"{FD}&page={page + 1}"}

        status, report = self.current(endless)
        self.assert_read_failure(status, report)
        self.assertIn("more than 20 pages", report)
        status, report = self.current(
            lambda upstream: upstream.update({FD: {"body": [], "link_next": "https://evil.invalid/page2"}})
        )
        self.assert_read_failure(status, report)
        self.assertIn("the next page is not on api.github.com", report)
        status, report = self.current(
            lambda upstream: upstream.update({FD: {"body": [], "link_next": f"{FD}&page=2"}, f"{FD}&page=2": {}})
        )
        self.assert_read_failure(status, report)
        self.assertIn("a page of the list is dict", report)

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
        status, report = self.watch(*current, token="ghs_secretvalue123\n", stderr=refused)
        self.assertEqual((2, ""), (status, report))

    def test_a_token_that_upstream_text_repeats_is_redacted_from_the_report(self):
        token = "ghs_" + "t" * 36
        title = f"macos-15 will be retired {token}"
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[RUNNER_ISSUES].append({"number": 9, "state": "open", "title": title})
        status, report = self.watch(["macos-15"], CURRENT_MISE, CURRENT_MANIFEST, upstream, token=token)
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
        token = "ghs_" + "s" * 36
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

    def test_the_link_header_next_page_is_followed(self):
        pages = {
            "https://api.github.com/repos/o/r/releases?per_page=100": (
                b'[{"n": 1}]',
                (
                    '<https://api.github.com/repositories/1/releases?per_page=100&page=2>; rel="next", '
                    '<https://api.github.com/repositories/1/releases?per_page=100&page=2>; rel="last"'
                ),
            ),
            "https://api.github.com/repositories/1/releases?per_page=100&page=2": (
                b'[{"n": 2}]',
                '<https://api.github.com/repositories/1/releases?per_page=100&page=1>; rel="first"',
            ),
        }

        def open_page(request, timeout):
            body, link = pages[request.full_url]
            response = mock.MagicMock()
            response.__enter__.return_value.read.return_value = body
            response.__enter__.return_value.headers = {"Link": link}
            return response

        with mock.patch.object(self.module.OPENER, "open", side_effect=open_page):
            items = self.module.Upstream(None, "").get_list("https://api.github.com/repos/o/r/releases?per_page=100")
        self.assertEqual([{"n": 1}, {"n": 2}], items)

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
