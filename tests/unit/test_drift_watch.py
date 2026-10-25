"""scripts/drift-watch.py (regime-cutover U81) on a fixture tree with recorded upstream responses.

A tree whose every pin is current reports nothing even though upstream has newer prereleases, drafts, yanked or
deprecated versions and releases younger than the 72h window; the same tree with a retiring runner image and old pins
reports each one; a failed or malformed upstream read is reported as a failure, never as "current"; the GitHub token
reaches api.github.com only. The watch runs as a subprocess (`python -I`), except for the token checks.
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
BREW_PIN = "a" * 40
RUNNER_ISSUES = f"{GH}/actions/runner-images/issues?labels=Announcement&state=all&per_page=100"
BREW_COMPARE = f"{GH}/Homebrew/install/compare/{BREW_PIN}...main"


def release(tag, published, prerelease=False, draft=False):
    return {"tag_name": tag, "published_at": published, "prerelease": prerelease, "draft": draft}


def workflow(oses):
    return {
        "name": "ci",
        "on": "push",
        "jobs": {"test": {"strategy": {"matrix": {"os": oses}}, "runs-on": "${{ matrix.os }}"}},
    }


CURRENT_MISE = """[tools]
python = "3.15.1"
node = "26.12.1"
jq = "latest"
"npm:ccusage" = "20.0.40"

[tools."http:bats"]
version = "1.14.0"
url = "https://github.com/bats-core/bats-core/archive/refs/tags/v1.14.0.tar.gz"

[settings]
minimum_release_age = "72h"
"""
CURRENT_MANIFEST = {
    "assets": {
        "starship": {"source": "github-release", "upstream": "starship/starship", "pin": "v1.27.0"},
        "homebrew-installer": {"source": "git-commit", "upstream": "Homebrew/install", "pin": BREW_PIN},
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
CURRENT_UPSTREAM = {
    RUNNER_ISSUES: [
        {
            "number": 13518,
            "state": "open",
            "title": "[macOS] The macOS 14 Sonoma based runner images will begin deprecation on July 6th",
        },
        # Naming a label in use without retiring anything is no drift either.
        {
            "number": 12520,
            "state": "closed",
            "title": "[macOS] `macos-latest` YAML-label will use `macos-15` in August 2025",
        },
        # A tool deprecation on an image in use is not the image's retirement.
        {
            "number": 13570,
            "state": "closed",
            "title": "[macOS] Deprecation of simulator runtimes for Xcode 26 on macOS 15",
        },
        {"number": 7, "state": "open", "title": "macos-15 is retired", "pull_request": {}},
    ],
    "https://nodejs.org/dist/index.json": [
        {"version": "v27.0.0", "date": "2026-10-24"},
        {"version": "v26.12.1", "date": "2026-10-21"},
    ],
    "https://www.python.org/api/v2/downloads/release/?is_published=true": [
        {"name": "Python 3.15.1", "release_date": "2026-10-21T09:59:50Z", "pre_release": False},
        {"name": "Python 3.15.2", "release_date": "2026-10-24T12:00:00Z", "pre_release": False},
        {"name": "Python 3.16.0a1", "release_date": "2026-10-13T19:02:12Z", "pre_release": True},
        {"name": "Python install manager 26.4", "release_date": "2026-10-09T00:00:00Z", "pre_release": False},
    ],
    "https://registry.npmjs.org/ccusage": {
        "time": {
            "created": "2025-01-01T00:00:00Z",
            "20.0.40": "2026-10-21T00:00:00Z",
            "20.0.41": "2026-10-24T20:00:00Z",
            "20.0.99": "2026-10-01T00:00:00Z",
            "21.0.0-beta.1": "2026-10-01T00:00:00Z",
        },
        "versions": {"20.0.40": {}, "20.0.41": {}, "20.0.99": {"deprecated": "broken"}, "21.0.0-beta.1": {}},
    },
    f"{GH}/bats-core/bats-core/releases?per_page=100": [
        release("v1.15.0", None, draft=True),
        release("v1.15.0-rc1", "2026-09-01T00:00:00Z", prerelease=True),
        release("v1.14.0", "2026-07-21T00:00:00Z"),
    ],
    f"{GH}/starship/starship/releases?per_page=100": [
        release("v1.28.0", "2026-10-24T06:00:00Z"),
        release("v1.27.0", "2026-10-17T00:00:00Z"),
    ],
    f"{GH}/Homebrew/install": {"default_branch": "main"},
    BREW_COMPARE: {
        "status": "ahead",
        "ahead_by": 1,
        "commits": [{"sha": "b" * 40, "commit": {"committer": {"date": "2026-10-24T08:00:00Z"}}}],
    },
    "https://registry.npmjs.org/@oh-my-pi%2Fpi-coding-agent": {
        "time": {"18.12.6": "2026-10-21T00:00:00Z", "18.12.7": "2026-10-24T00:00:00Z"},
        "versions": {"18.12.6": {}, "18.12.7": {}},
    },
    "https://pypi.org/pypi/hcom/json": {
        "releases": {
            "0.7.31": [{"upload_time_iso_8601": "2026-10-21T03:56:00.000000Z", "yanked": False}],
            "0.7.32": [{"upload_time_iso_8601": "2026-10-20T00:00:00.000000Z", "yanked": True}],
            "0.8.0rc1": [{"upload_time_iso_8601": "2026-10-01T00:00:00.000000Z", "yanked": False}],
            "0.9.0": [],
        }
    },
    f"{GH}/DietrichGebert/ponytail/contents/.claude-plugin/marketplace.json": {
        "plugins": [{"name": "ponytail", "source": "./"}]
    },
    f"{GH}/DietrichGebert/ponytail/contents/.claude-plugin/plugin.json": {"version": "5.3.2"},
    f"{GH}/anthropics/claude-plugins-official/contents/.claude-plugin/marketplace.json": {
        "plugins": [
            {
                "name": "superpowers",
                "source": {"source": "url", "url": "https://github.com/obra/superpowers.git", "sha": "c" * 40},
            }
        ]
    },
    f"{GH}/obra/superpowers/contents/.claude-plugin/plugin.json?ref={'c' * 40}": {"version": "7.0.0"},
    f"{GH}/DietrichGebert/ponytail/contents/.agents/plugins/marketplace.json": {
        "plugins": [
            {
                "name": "ponytail",
                "source": {"source": "url", "url": "https://github.com/DietrichGebert/ponytail.git", "ref": "main"},
            }
        ]
    },
    f"{GH}/DietrichGebert/ponytail/contents/.codex-plugin/plugin.json?ref=main": {"version": "5.3.2"},
}


def stale_tree():
    """The current tree aged: a retiring runner image in the matrix and every pin one release or more behind."""
    mise = (
        CURRENT_MISE.replace('python = "3.15.1"', 'python = "3.15.0"')
        .replace('"20.0.40"', '"20.0.37"')
        .replace('version = "1.14.0"', 'version = "1.13.0"')
    )
    manifest = copy.deepcopy(CURRENT_MANIFEST)
    assets = manifest["assets"]
    assets["starship"]["pin"] = "v1.26.0"
    assets["omp"]["pin"] = "18.11.3"
    assets["hcom"]["pin"] = "0.7.30"
    assets["claude-plugins"]["plugins"]["ponytail@ponytail"]["pin"] = "4.10.0"
    assets["codex-plugins"]["plugins"]["ponytail"]["pin"] = "4.10.0"
    assets["gh-extensions"] = {
        "source": "gh-extension",
        "upstream": "https://github.com/seachicken/gh-poi",
        "pin": "unknown",
    }
    upstream = copy.deepcopy(CURRENT_UPSTREAM)
    upstream[BREW_COMPARE]["ahead_by"] = 2
    upstream[BREW_COMPARE]["commits"].insert(
        0, {"sha": "d" * 40, "commit": {"committer": {"date": "2026-10-01T00:00:00Z"}}}
    )
    return ["ubuntu-24.04", "macos-14", "macos-15"], mise, manifest, upstream


STALE = {
    ("runner-image", "macos-14"),
    ("mise-pin", "python"),
    ("mise-pin", "npm:ccusage"),
    ("mise-pin", "http:bats"),
    ("manifest-pin", "starship.pin"),
    ("manifest-pin", "homebrew-installer.pin"),
    ("manifest-pin", "omp.pin"),
    ("manifest-pin", "hcom.pin"),
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
    def watch(self, oses, mise, manifest, upstream, lint=None):
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
            run = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--now",
                    NOW,
                    "--upstream",
                    str(root / "upstream.json"),
                ],
                capture_output=True,
                text=True,
                env=env,
                check=False,
            )
        self.assertEqual("", run.stderr)
        return run.returncode, run.stdout

    @staticmethod
    def findings(report):
        rows = [
            line for line in report.splitlines() if line.startswith("| ") and not line.startswith(("| check", "| ---"))
        ]
        return {tuple(cell.strip().strip("`") for cell in row.strip("|").split(" | ")[:2]) for row in rows}

    def test_a_tree_with_every_pin_current_reports_no_drift(self):
        status, report = self.watch(["ubuntu-24.04", "macos-15"], CURRENT_MISE, CURRENT_MANIFEST, CURRENT_UPSTREAM)
        self.assertEqual(0, status, report)
        self.assertIn("No drift found.", report)
        self.assertEqual(set(), self.findings(report))
        self.assertNotIn("Read failures", report)

    def test_a_retiring_runner_image_and_each_stale_pin_are_reported(self):
        oses, mise, manifest, upstream = stale_tree()
        status, report = self.watch(oses, mise, manifest, upstream)
        self.assertEqual(3, status, report)
        self.assertEqual(STALE, self.findings(report))
        self.assertIn("`3.15.1 (2026-10-21)`", report, "the newest release past the window, not the fresh 3.15.2")
        self.assertIn("actions/runner-images#13518 (open)", report)

    def test_a_failed_or_malformed_upstream_read_is_a_failure_not_current(self):
        for name, change in (
            ("missing", lambda upstream: upstream.pop(f"{GH}/starship/starship/releases?per_page=100")),
            ("http error", lambda upstream: upstream.update({RUNNER_ISSUES: {"http_status": 403}})),
            ("malformed", lambda upstream: upstream.update({"https://pypi.org/pypi/hcom/json": {"info": {}}})),
            (
                "plugin",
                lambda upstream: upstream.update(
                    {f"{GH}/obra/superpowers/contents/.claude-plugin/plugin.json?ref={'c' * 40}": []}
                ),
            ),
        ):
            with self.subTest(name):
                upstream = copy.deepcopy(CURRENT_UPSTREAM)
                change(upstream)
                status, report = self.watch(["ubuntu-24.04", "macos-15"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
                self.assertEqual(4, status, report)
                self.assertIn("## Read failures (1)", report)

    def test_a_payload_that_is_not_exactly_the_expected_shape_is_a_read_failure(self):
        starship = f"{GH}/starship/starship/releases?per_page=100"
        bats = f"{GH}/bats-core/bats-core/releases?per_page=100"
        python = "https://www.python.org/api/v2/downloads/release/?is_published=true"
        catalog = f"{GH}/DietrichGebert/ponytail/contents/.claude-plugin/marketplace.json"
        node = "https://nodejs.org/dist/index.json"
        pypi = "https://pypi.org/pypi/hcom/json"
        for name, change in (
            ("a release list that is an object", lambda upstream: upstream.update({starship: {}})),
            ("a draft flag that is a string", lambda upstream: upstream[bats][2].update({"draft": "no"})),
            (
                "an issue number that is a string",
                lambda upstream: upstream[RUNNER_ISSUES][0].update({"number": "13518"}),
            ),
            (
                "an npm version without a time",
                lambda upstream: upstream["https://registry.npmjs.org/ccusage"]["versions"].update({"20.0.50": {}}),
            ),
            (
                "a release date that is no time",
                lambda upstream: upstream[python][0].update({"release_date": "yesterday"}),
            ),
            ("an empty published_at", lambda upstream: upstream[starship][0].update({"published_at": ""})),
            ("an impossible Node date", lambda upstream: upstream[node][1].update({"date": "2026-02-30"})),
            (
                "an impossible python.org date",
                lambda upstream: upstream[python][0].update({"release_date": "2026-02-30T00:00:00Z"}),
            ),
            (
                "a PyPI upload time without a zone",
                lambda upstream: upstream[pypi]["releases"]["0.7.31"][0].update(
                    {"upload_time_iso_8601": "2026-10-21T03:56:00"}
                ),
            ),
            (
                "an empty npm time",
                lambda upstream: upstream["https://registry.npmjs.org/ccusage"]["time"].update({"20.0.40": ""}),
            ),
            (
                "repository metadata that is 404",
                lambda upstream: upstream.update({f"{GH}/Homebrew/install": {"http_status": 404}}),
            ),
            ("compare commits that are no list", lambda upstream: upstream[BREW_COMPARE].update({"commits": {}})),
            (
                "a catalog version that is a number",
                lambda upstream: upstream[catalog]["plugins"][0].update({"version": 5}),
            ),
        ):
            with self.subTest(name):
                upstream = copy.deepcopy(CURRENT_UPSTREAM)
                change(upstream)
                status, report = self.watch(["ubuntu-24.04", "macos-15"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
                self.assertEqual(4, status, report)
                self.assertIn("## Read failures (1)", report)
                self.assertRegex(report, "unexpected response|HTTP 404")

    def test_a_catalog_version_never_hides_an_advanced_plugin_json(self):
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[f"{GH}/DietrichGebert/ponytail/contents/.claude-plugin/marketplace.json"]["plugins"][0]["version"] = (
            "5.3.2"
        )
        upstream[f"{GH}/DietrichGebert/ponytail/contents/.claude-plugin/plugin.json"] = {"version": "5.4.0"}
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(3, status, report)
        self.assertEqual({("plugin-pin", "claude-plugins.ponytail@ponytail")}, self.findings(report))
        self.assertIn("5.4.0 (DietrichGebert/ponytail/.claude-plugin/plugin.json)", report)

    def test_a_yanked_file_does_not_age_a_pypi_release(self):
        # 0.7.33's only installable file is 12 hours old; its old yanked file must not put it past the window.
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream["https://pypi.org/pypi/hcom/json"]["releases"]["0.7.33"] = [
            {"upload_time_iso_8601": "2026-10-01T00:00:00.000000Z", "yanked": True},
            {"upload_time_iso_8601": "2026-10-24T12:00:00.000000Z", "yanked": False},
        ]
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(0, status, report)
        self.assertEqual(set(), self.findings(report))

    def test_a_codex_plugin_with_a_local_source_is_read_from_its_marketplace_repository(self):
        codex = f"{GH}/DietrichGebert/ponytail/contents/.agents/plugins/marketplace.json"
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[codex]["plugins"][0]["source"] = {"source": "local", "path": "./plugins/ponytail"}
        upstream[f"{GH}/DietrichGebert/ponytail/contents/plugins/ponytail/.codex-plugin/plugin.json"] = {
            "version": "5.4.0"
        }
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(3, status, report)
        self.assertEqual({("plugin-pin", "codex-plugins.ponytail")}, self.findings(report))
        self.assertIn("5.4.0 (DietrichGebert/ponytail/plugins/ponytail/.codex-plugin/plugin.json)", report)
        # A local path that leaves the repository is a read failure; a source kind the watch cannot read is listed.
        upstream[codex]["plugins"][0]["source"] = {"source": "local", "path": "../elsewhere"}
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(4, status, report)
        upstream[codex]["plugins"][0]["source"] = {"source": "npm", "package": "ponytail"}
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(0, status, report)
        self.assertIn("codex-plugins.ponytail 5.3.2", report.split("## Not watched", 1)[1])

    def test_a_commit_pin_upstream_no_longer_has_is_drift(self):
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[BREW_COMPARE] = {"http_status": 404}
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(3, status, report)
        self.assertEqual({("manifest-pin", "homebrew-installer.pin")}, self.findings(report))

    def test_an_upstream_with_no_release_is_listed_as_not_watched_not_current(self):
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        upstream[f"{GH}/starship/starship/releases?per_page=100"] = []
        status, report = self.watch(["ubuntu-24.04"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(0, status, report)
        self.assertIn("manifest-pin starship.pin v1.27.0", report.split("## Not watched", 1)[1])

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
        upstream = copy.deepcopy(CURRENT_UPSTREAM)
        title = "macos-15 retired | `x` @someone [link](https://e.invalid)\n## injected"
        upstream[RUNNER_ISSUES].append({"number": 9, "state": "open", "title": title})
        status, report = self.watch(["macos-15"], CURRENT_MISE, CURRENT_MANIFEST, upstream)
        self.assertEqual(3, status, report)
        row = next(line for line in report.splitlines() if "#9" in line)
        upstream_cell = row.strip("|").split(" | ")[3]
        self.assertEqual(6, row.count("|"), row)
        self.assertTrue(upstream_cell.startswith("`") and upstream_cell.endswith("`"), upstream_cell)
        self.assertEqual(2, upstream_cell.count("`"), upstream_cell)
        self.assertNotIn("\n## injected", report)


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

    def test_the_token_goes_to_api_github_com_only_and_never_follows_a_redirect(self):
        upstream = self.module.Upstream(None, "token-value")
        upstream.get("https://api.github.com/repos/o/r/releases?per_page=100")
        upstream.get("https://registry.npmjs.org/ccusage")
        github, npm = self.requests
        self.assertEqual("Bearer token-value", github.unredirected_hdrs.get("Authorization"))
        self.assertNotIn("Authorization", github.headers)
        self.assertNotIn("Authorization", npm.headers)
        self.assertNotIn("Authorization", npm.unredirected_hdrs)

    def test_no_request_leaves_the_allowed_hosts(self):
        upstream = self.module.Upstream(None, "token-value")
        for url in (
            "https://evil.invalid/x",
            "http://api.github.com/repos/o/r",
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

    def test_an_http_error_is_a_read_failure(self):
        error = urllib.error.HTTPError("https://api.github.com/x", 500, "boom", {}, None)
        with (
            mock.patch.object(self.module.OPENER, "open", side_effect=error),
            self.assertRaises(self.module.ReadError) as raised,
        ):
            self.module.Upstream(None, "").get("https://api.github.com/x")
        self.assertEqual(500, raised.exception.status)

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
# A stub gh: logs its argv, and answers `issue list` by running the step's own --jq filter over GH_LIST_JSON.
GH_STUB = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$GH_LOG"
if [ "$1 $2" = "issue list" ]; then
    [ -z "${GH_LIST_FAIL:-}" ] || exit 1
    while [ $# -gt 0 ]; do [ "$1" != --jq ] || filter="$2"; shift; done
    printf '%s' "$GH_LIST_JSON" | jq -r "$filter"
fi
"""
BOT = {"login": "app/github-actions", "is_bot": True}


class TrackingIssueStepTest(unittest.TestCase):
    """The workflow's issue step, run with a stub gh: which issue it writes, and that a failed lookup writes none."""

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
                "GH_LIST_JSON": json.dumps(issues),
                "RUNNER_TEMP": str(temp),
                "STATUS": status,
                "RUN_URL": "https://github.com/o/r/actions/runs/1",
            }
            if list_fails:
                env["GH_LIST_FAIL"] = "1"
            run = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True, check=False)
            calls = (temp / "gh.log").read_text().splitlines()
        return run.returncode, [call for call in calls if not call.startswith("issue list")]

    def test_the_workflow_runs_only_on_schedule_and_by_hand(self):
        doc = yaml.safe_load(WORKFLOW.read_text())
        self.assertEqual({"schedule", "workflow_dispatch"}, set(doc[True]))

    def test_drift_opens_one_issue_and_never_rewrites_an_issue_someone_else_opened(self):
        human = {"number": 5, "title": "Drift watch", "author": {"login": "someone", "is_bot": False}}
        self.assertEqual(
            (0, ["issue create --title Drift watch --body-file " + "{}"]), self.normalised(self.step("3", [human]))
        )
        bot = {"number": 7, "title": "Drift watch", "author": BOT}
        self.assertEqual((0, ["issue edit 7 --body-file {}"]), self.normalised(self.step("4", [human, bot])))

    def test_a_clean_run_closes_the_open_issue_and_otherwise_writes_nothing(self):
        bot = {"number": 7, "title": "Drift watch", "author": BOT}
        status, calls = self.normalised(self.step("0", [bot]))
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

    @staticmethod
    def normalised(result):
        status, calls = result
        return status, [
            " ".join("{}" if word.endswith("/drift.md") else word for word in call.split(" ")) for call in calls
        ]


if __name__ == "__main__":
    unittest.main()
