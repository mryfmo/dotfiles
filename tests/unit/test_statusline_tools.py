#!/usr/bin/env python3
"""Verify statusline tools are declared in mise and execute without network installers."""

from __future__ import annotations

import json
import os
import runpy
import shutil
import subprocess
import tempfile
import textwrap
import time
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MISE_CONFIG = ROOT / "home/dot_mise/config.toml"
CCUSAGE_SETTINGS = ROOT / "home/dot_ccstatusline/settings.json"
CLAUDE_SETTINGS = ROOT / "home/.chezmoitemplates/claude-settings-managed.json"
CI_WORKFLOW = ROOT / ".github/workflows/test.yaml"
INTEGRATION_SMOKE = ROOT / "scripts/check-statusline-tools.py"
# The tools are declared once, in home/dot_mise/config.toml.
EXPECTED_TOOLS = {
    tool: tomllib.loads(MISE_CONFIG.read_text())["tools"][tool] for tool in ("npm:ccusage", "npm:ccstatusline")
}
SKEW_CHECK = ROOT / "scripts/ci/npm-cooldown-skew-check.sh"
# Registry answers recorded on 2026-10-29 with `npm view --json` against registry.npmjs.org. The fake npm below
# serves them, so the frozen-clock cases replay the 2026-10-24 failure (run 40087404553) without the network.
CCUSAGE_20_0_38_OPTIONAL_DEPENDENCIES = {
    "@ccusage/ccusage-linux-x64": "20.0.38",
    "@ccusage/ccusage-win32-x64": "20.0.38",
    "@ccusage/ccusage-darwin-x64": "20.0.38",
    "@ccusage/ccusage-linux-arm64": "20.0.38",
    "@ccusage/ccusage-win32-arm64": "20.0.38",
    "@ccusage/ccusage-darwin-arm64": "20.0.38",
}
CCUSAGE_PLATFORM_PACKAGES = {
    "@ccusage/ccusage-linux-x64": {"os": ["linux"], "cpu": ["x64"]},
    "@ccusage/ccusage-win32-x64": {"os": ["win32"], "cpu": ["x64"]},
    "@ccusage/ccusage-darwin-x64": {"os": ["darwin"], "cpu": ["x64"]},
    "@ccusage/ccusage-linux-arm64": {"os": ["linux"], "cpu": ["arm64"]},
    "@ccusage/ccusage-win32-arm64": {"os": ["win32"], "cpu": ["arm64"]},
    "@ccusage/ccusage-darwin-arm64": {"os": ["darwin"], "cpu": ["arm64"]},
}
CCUSAGE_TIME = {
    "created": "2025-05-29T19:25:18.575Z",
    "modified": "2026-10-26T20:27:27.185Z",
    "20.0.37": "2026-10-19T20:02:04.451Z",
    "20.0.38": "2026-10-21T10:49:51.361Z",
}
CCUSAGE_LINUX_X64_TIME = {
    "created": "2026-05-19T22:50:27.380Z",
    "modified": "2026-10-26T20:22:55.412Z",
    "20.0.37": "2026-10-19T20:01:25.157Z",
    "20.0.38": "2026-10-21T10:54:25.259Z",
}
CCSTATUSLINE_TIME = {
    "created": "2025-08-08T11:08:09.986Z",
    "modified": "2026-10-09T18:53:58.258Z",
    "2.2.32": "2026-10-09T18:53:57.953Z",
}
# The config's requests, as the fake `mise tool --json` reports them to the check.
FAKE_REQUESTS = {"npm:ccusage": "20.0.38", "npm:ccstatusline": "2.2.32"}
# 2026-10-24T10:49:49Z, the start of the failing "Install statusline tools" step; then 10:52:00Z, 10:54:26Z (one
# second past the linux-x64 package's 72 h, inside the 60 s margin) and 10:55:26Z (past the margin).
STEP_START, IN_THE_SKEW, WINDOW_END, PAST_THE_MARGIN = "1792838989", "1792839120", "1792839266", "1792839326"
META_REFUSAL = "refuse: ccusage@20.0.38: 20.0.38 was published 2026-10-21T10:49:51.361000Z"
LINUX_X64_REFUSAL = "refuse: @ccusage/ccusage-linux-x64@20.0.38: 20.0.38 was published 2026-10-21T10:54:25.259000Z"
OPTIONAL_READ = "view --json ccusage@20.0.38 optionalDependencies"
LINUX_X64_READ = "view --json @ccusage/ccusage-linux-x64@20.0.38 os cpu"


class StatuslineToolsTest(unittest.TestCase):
    def commands(self) -> tuple[str, str]:
        ccusage = json.loads(CCUSAGE_SETTINGS.read_text())["lines"][0][0]["commandPath"]
        render = runpy.run_path(str(ROOT / "home/dot_claude/modify_private_settings.json"))["render_managed_template"]
        ccstatusline = json.loads(render(CLAUDE_SETTINGS.read_text()))["statusLine"]["command"]
        return ccusage, ccstatusline

    def test_mise_config_holds_the_statusline_tools_at_exact_versions(self) -> None:
        # U114: ccusage's platform packages publish minutes after its meta package, so a job inside that skew installs
        # 20.0.38 without the binary; both smoke tools hold exact pins, and a drift back to "latest" or a range fails.
        config = tomllib.loads(MISE_CONFIG.read_text())
        self.assertEqual({"npm:ccusage": "20.0.37", "npm:ccstatusline": "2.2.32"}, EXPECTED_TOOLS)
        self.assertEqual("72h", config["settings"]["minimum_release_age"])

    def test_generated_commands_are_direct_and_static(self) -> None:
        commands = self.commands()
        self.assertEqual(commands, ("ccusage statusline", "ccstatusline"))
        for command in commands:
            for forbidden in ("npx", "@latest", " --yes", " -y"):
                self.assertNotIn(forbidden, command)

    def test_direct_commands_use_offline_path_binaries(self) -> None:
        with tempfile.TemporaryDirectory() as bin_dir:
            bin_path = Path(bin_dir)
            log = bin_path / "calls"
            for name in ("ccusage", "ccstatusline"):
                executable = bin_path / name
                executable.write_text(f'#!/bin/sh\nprintf "{name}%s\\n" "${{*:+ $*}}" >> "{log}"\n')
                executable.chmod(0o755)

            env = os.environ | {
                "PATH": bin_dir,
                "HTTP_PROXY": "http://127.0.0.1:1",
                "HTTPS_PROXY": "http://127.0.0.1:1",
                "NO_PROXY": "",
            }
            for command in self.commands():
                subprocess.run(command.split(), env=env, check=True, timeout=1)

            self.assertEqual(
                log.read_text().splitlines(),
                ["ccusage statusline", "ccstatusline"],
            )

    def test_missing_binary_fails_immediately(self) -> None:
        for command in self.commands():
            started = time.monotonic()
            result = subprocess.run(
                command,
                shell=True,
                executable="/bin/sh",
                env=os.environ | {"PATH": ""},
                text=True,
                capture_output=True,
                timeout=1,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertLess(time.monotonic() - started, 1)
            self.assertRegex(result.stderr, r"not found|No such file")

    def test_ci_smokes_statusline_tools_with_network_denied(self) -> None:
        workflow = CI_WORKFLOW.read_text()
        smoke = INTEGRATION_SMOKE.read_text()
        node_install = 'mise -C "${RUNNER_TEMP}/statusline-mise" install node'
        skew_check = (
            'scripts/ci/npm-cooldown-skew-check.sh "${RUNNER_TEMP}/statusline-mise" npm:ccstatusline npm:ccusage'
        )
        tools_install = 'mise -C "${RUNNER_TEMP}/statusline-mise" install npm:ccstatusline npm:ccusage'

        for token in (
            node_install,
            skew_check,
            tools_install,
            'where npm:ccstatusline)"',
            'where npm:ccusage)"',
            'mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"',
            "sudo unshare --net",
            "/usr/bin/sandbox-exec",
            "ip route show",
            's.bind(("127.0.0.1", 0))',
            "scripts/check-statusline-tools.py",
        ):
            self.assertIn(token, workflow)
        # The check runs between the node install and the tools install, so a young platform package stops the step.
        self.assertLess(workflow.index(node_install), workflow.index(skew_check))
        self.assertLess(workflow.index(skew_check), workflow.index(tools_install))
        # A failing smoke names the pins to bump, on both platforms.
        self.assertIn("bump the exact pins in home/dot_mise/config.toml", workflow)
        self.assertEqual(2, workflow.count('"${smoke[@]}" || smoke_failed'))
        # The versions come from the copied config; the workflow carries no literal.
        for literal in ("ccstatusline@", "ccusage@"):
            self.assertNotIn(literal, workflow)
        for token in (
            '"display_name": "Claude"',
            '"session_id": "offline-test"',
            "timeout=5",
            'run([str(args.ccusage), "statusline"]',
        ):
            self.assertIn(token, smoke)


class NpmCooldownSkewCheckTest(unittest.TestCase):
    """scripts/ci/npm-cooldown-skew-check.sh against a fake mise and npm that serve the recorded registry answers."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="npm-cooldown-skew-"))
        self.addCleanup(shutil.rmtree, self.temp, ignore_errors=True)
        self.config_dir = self.temp / "statusline-mise"
        self.config_dir.mkdir()
        bin_dir = self.temp / "bin"
        self.executable(
            bin_dir / "mise",
            """
            # The reads the check makes. FAKE_REQUESTS maps a tool to the config's request (`mise tool --json`),
            # FAKE_TOOL_JSON replaces that answer whole, FAKE_LATEST replaces `mise latest`'s (the request otherwise),
            # FAKE_WINDOW is minimum_release_age ("fail" fails the read), FAKE_PLATFORM and FAKE_ARCH are node's
            # answers, and `exec node -- npm ...` runs the fake npm on PATH.
            [ "$1" = -C ] && [ -d "$2" ] || exit 1
            shift 2
            case "$*" in
                "tool --json "*)
                    if [ -n "${FAKE_TOOL_JSON+set}" ]; then
                        printf '%s\\n' "$FAKE_TOOL_JSON"
                    else
                        python3 -I -c 'import json, sys; r = json.loads(sys.argv[1]).get(sys.argv[2]); print(json.dumps({"requested_versions": [r] if r else []}))' "$FAKE_REQUESTS" "$3"
                    fi
                    ;;
                "latest npm:"*) printf '%s\\n' "${FAKE_LATEST-${2##*@}}" ;;
                "settings get minimum_release_age")
                    [ "${FAKE_WINDOW-72h}" != fail ] || exit 1
                    printf '%s\\n' "${FAKE_WINDOW-72h}"
                    ;;
                "exec node -- node -p process.platform") printf '%s\\n' "${FAKE_PLATFORM-linux}" ;;
                "exec node -- node -p process.arch") printf '%s\\n' "${FAKE_ARCH-x64}" ;;
                "exec node -- npm "*)
                    shift 3
                    exec "$@"
                    ;;
                *) exit 1 ;;
            esac
            """,
        )
        self.executable(
            bin_dir / "npm",
            """
            # Answers `npm view --json <spec> <field>...` from FAKE_REGISTRY, a JSON object of "view --json <spec>
            # <field>..." to the text npm printed on 2026-10-29; a null or missing entry is a failed npm view.
            python3 -I -c 'import json, sys; a = json.load(open(sys.argv[1])).get(sys.argv[2]); sys.exit(1) if a is None else sys.stdout.write(a)' "$FAKE_REGISTRY" "$*"
            """,
        )

    def executable(self, path: Path, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/bash\n" + textwrap.dedent(body))
        path.chmod(0o755)

    def registry(self) -> dict[str, str | None]:
        """The recorded answers, keyed as the fake npm sees them."""
        recorded: dict[str, str | None] = {
            "view --json ccusage time": json.dumps(CCUSAGE_TIME),
            OPTIONAL_READ: json.dumps(CCUSAGE_20_0_38_OPTIONAL_DEPENDENCIES),
            "view --json @ccusage/ccusage-linux-x64 time": json.dumps(CCUSAGE_LINUX_X64_TIME),
            "view --json ccstatusline time": json.dumps(CCSTATUSLINE_TIME),
            "view --json ccstatusline@2.2.32 optionalDependencies": "",
        }
        for package, shape in CCUSAGE_PLATFORM_PACKAGES.items():
            recorded[f"view --json {package}@20.0.38 os cpu"] = json.dumps(shape)
        return recorded

    def run_check(
        self, *tools: str, now: str, registry: dict[str, str | None] | None = None, **fakes: str
    ) -> subprocess.CompletedProcess[str]:
        registry_file = self.temp / "registry.json"
        registry_file.write_text(json.dumps(self.registry() | (registry or {})))
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "FAKE_REGISTRY": str(registry_file),
            "FAKE_REQUESTS": json.dumps(FAKE_REQUESTS),
            **fakes,
        }
        return subprocess.run(
            [str(SKEW_CHECK), "--now", now, str(self.config_dir), *tools],
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )

    @staticmethod
    def refusals(result: subprocess.CompletedProcess[str]) -> list[str]:
        return [line for line in result.stdout.splitlines() if line.startswith("refuse: ")]

    def test_the_2026_10_24_install_is_refused_until_the_platform_package_clears_the_window_and_the_margin(
        self,
    ) -> None:
        # The job started at 10:49:49Z: the meta package turned 72 h old 2.4 s later, its linux-x64 package 4 min
        # 36 s later, and npm installed without the binary. The check names both, then the skew alone, then nothing.
        for name, now, tool, expected in (
            ("the step's start", STEP_START, "npm:ccusage", [META_REFUSAL, LINUX_X64_REFUSAL]),
            ("inside the skew", IN_THE_SKEW, "npm:ccusage@20.0.38", [LINUX_X64_REFUSAL]),
            ("one second past the window, inside the margin", WINDOW_END, "npm:ccusage@20.0.38", [LINUX_X64_REFUSAL]),
            ("past the margin", PAST_THE_MARGIN, "npm:ccusage@20.0.38", []),
        ):
            with self.subTest(name):
                result = self.run_check(tool, now=now)
                output = result.stdout + result.stderr
                refusals = self.refusals(result)
                self.assertEqual(1 if expected else 0, result.returncode, output)
                self.assertEqual(len(expected), len(refusals), output)
                for prefix in expected:
                    self.assertTrue(any(line.startswith(prefix) for line in refusals), output)
                if LINUX_X64_REFUSAL in expected:
                    self.assertIn("it can be rebuilt from 2026-10-24T10:55:25.259000Z", output)
                if META_REFUSAL in expected:
                    self.assertIn("it can be rebuilt from 2026-10-24T10:50:51.361000Z", output)
                if expected:
                    self.assertNotIn("pass:", output)
                else:
                    self.assertEqual(
                        [
                            "pass: npm:ccusage@20.0.38: ccusage@20.0.38 (published 2026-10-21T10:49:51.361Z),"
                            " @ccusage/ccusage-linux-x64@20.0.38 (published 2026-10-21T10:54:25.259Z),"
                            " at least 72h and 60 s old"
                        ],
                        result.stdout.splitlines(),
                    )

    def test_a_tool_without_optional_dependencies_passes_on_its_own_publish_time(self) -> None:
        result = self.run_check("npm:ccstatusline", now=STEP_START)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            [
                "ccstatusline@2.2.32: no optional dependencies",
                "pass: npm:ccstatusline: ccstatusline@2.2.32 (published 2026-10-09T18:53:57.953Z), at least 72h and 60 s old",
            ],
            result.stdout.splitlines(),
        )

    def test_the_window_is_mise_s_setting_in_hours_or_days(self) -> None:
        for window, now, expected in (("3d", WINDOW_END, 1), ("3d", PAST_THE_MARGIN, 0), ("1h", IN_THE_SKEW, 0)):
            with self.subTest(window=window, now=now):
                result = self.run_check("npm:ccusage", now=now, FAKE_WINDOW=window)
                self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
                if expected == 0:
                    self.assertIn(f"at least {window} and 60 s old", result.stdout)

    def test_a_runner_with_no_platform_package_is_refused_naming_it(self) -> None:
        linux_only = {
            name: version for name, version in CCUSAGE_20_0_38_OPTIONAL_DEPENDENCIES.items() if "linux" in name
        }
        result = self.run_check(
            "npm:ccusage",
            now=PAST_THE_MARGIN,
            registry={OPTIONAL_READ: json.dumps(linux_only)},
            FAKE_PLATFORM="darwin",
            FAKE_ARCH="arm64",
        )
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            ["refuse: ccusage@20.0.38: none of its optional dependencies is built for darwin/arm64"],
            result.stdout.splitlines(),
        )

    def test_an_answer_that_cannot_be_read_fails_closed_naming_it(self) -> None:
        # Fail closed: every read the verdict rests on has a failure injected here, and none is read as "old enough"
        # (the clock is past the margin, so a swallowed failure would print the pass line).
        two_requests = '{"requested_versions": ["20.0.37", "20.0.38"]}'
        cases = [
            (
                "npm view fails",
                {OPTIONAL_READ: None},
                {},
                "npm view --json ccusage@20.0.38 optionalDependencies failed",
            ),
            ("npm view prints no JSON", {OPTIONAL_READ: "not json"}, {}, "optionalDependencies printed no JSON"),
            ("npm view prints a list", {OPTIONAL_READ: "[]"}, {}, "not an object of package name to version"),
            (
                "a dependency on a range",
                {OPTIONAL_READ: '{"@ccusage/ccusage-linux-x64": "^20.0.0"}'},
                {},
                "not an object of package name to version",
            ),
            ("os missing", {LINUX_X64_READ: '{"cpu": ["x64"]}'}, {}, "os and cpu are lists of strings"),
            ("a negated os entry", {LINUX_X64_READ: '{"os": ["!linux"], "cpu": ["x64"]}'}, {}, "negated os or cpu"),
            (
                "the platform package's publish time fails",
                {"view --json @ccusage/ccusage-linux-x64 time": None},
                {},
                "npm view --json @ccusage/ccusage-linux-x64 time failed",
            ),
            ("mise latest prints two lines", {}, {"FAKE_LATEST": "20.0.38\n20.0.39"}, "not one exact version"),
            ("mise latest prints a tag", {}, {"FAKE_LATEST": "latest"}, "not one exact version"),
            ("mise settings get prints 72", {}, {"FAKE_WINDOW": "72"}, "printed '72', not <N>h or <N>d"),
            ("mise settings get fails", {}, {"FAKE_WINDOW": "fail"}, "settings get minimum_release_age failed"),
            ("mise tool --json lists two requests", {}, {"FAKE_TOOL_JSON": two_requests}, "not one version request"),
            ("the config requests no version", {}, {"FAKE_REQUESTS": "{}"}, "not one version request"),
            ("the config directory is missing", {}, {"MISSING_DIR": "1"}, "is not a directory"),
        ]
        for name, registry, fakes, message in cases:
            with self.subTest(name):
                if fakes.pop("MISSING_DIR", None):
                    shutil.rmtree(self.config_dir)
                result = self.run_check("npm:ccusage", now=PAST_THE_MARGIN, registry=registry, **fakes)
                output = result.stdout + result.stderr
                self.assertEqual(2, result.returncode, output)
                self.assertIn(message, output)
                self.assertNotIn("pass:", result.stdout)


if __name__ == "__main__":
    unittest.main()
