#!/usr/bin/env python3
"""Verify statusline tools are declared in mise and execute without network installers."""

from __future__ import annotations

import json
import os
import re
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
META_TIME_READ = "view --json ccusage time"
LINUX_X64_TIME_READ = "view --json @ccusage/ccusage-linux-x64 time"
# The commands the check runs, as its source spells them after `mise -C "${config_dir}"`, and the npm reads it makes
# through npm_view. FAILURES below injects each one's failed command and an answer of another shape, and the census
# test derives this set from the source again, so a read added without its injection fails there.
SETTINGS_READ = "settings get minimum_release_age"
PLATFORM_READ = "exec node -- node -p process.platform"
ARCH_READ = "exec node -- node -p process.arch"
TOOL_READ = "tool --json"
LATEST_READ = "latest"
NPM_VIEW = "exec node -- npm view --json"
TIME_FIELD, OPTIONAL_FIELD, OS_CPU_FIELD = "npm view time", "npm view optionalDependencies", "npm view os cpu"


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
        self.npm_log = self.temp / "npm-reads.log"
        bin_dir = self.temp / "bin"
        self.executable(
            bin_dir / "mise",
            """
            # The reads the check makes. FAKE_REQUESTS maps a tool to the config's request (`mise tool --json`),
            # FAKE_TOOL_JSON replaces that answer whole, FAKE_LATEST replaces `mise latest`'s (the request otherwise),
            # FAKE_WINDOW is minimum_release_age, FAKE_PLATFORM and FAKE_ARCH are node's answers, and
            # `exec node -- npm ...` runs the fake npm on PATH. FAKE_FAIL names, space-separated, the reads that
            # exit 1 without an answer instead: tool, latest, settings, platform, arch.
            [ "$1" = -C ] && [ -d "$2" ] || exit 1
            shift 2
            fails() { case " ${FAKE_FAIL-} " in *" $1 "*) exit 1 ;; esac; }
            case "$*" in
                "tool --json "*)
                    fails tool
                    if [ -n "${FAKE_TOOL_JSON+set}" ]; then
                        printf '%s\\n' "$FAKE_TOOL_JSON"
                    else
                        python3 -I -c 'import json, sys; r = json.loads(sys.argv[1]).get(sys.argv[2]); print(json.dumps({"requested_versions": [r] if r else []}))' "$FAKE_REQUESTS" "$3"
                    fi
                    ;;
                "latest npm:"*)
                    fails latest
                    printf '%s\\n' "${FAKE_LATEST-${2##*@}}"
                    ;;
                "settings get minimum_release_age")
                    fails settings
                    printf '%s\\n' "${FAKE_WINDOW-72h}"
                    ;;
                "exec node -- node -p process.platform")
                    fails platform
                    printf '%s\\n' "${FAKE_PLATFORM-linux}"
                    ;;
                "exec node -- node -p process.arch")
                    fails arch
                    printf '%s\\n' "${FAKE_ARCH-x64}"
                    ;;
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
            # <field>..." to the text npm printed on 2026-10-29; a null or missing entry is a failed npm view. Every
            # read is appended to FAKE_NPM_LOG first, so a test can see which reads a refusal came before.
            printf '%s\\n' "$*" >> "$FAKE_NPM_LOG"
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
            META_TIME_READ: json.dumps(CCUSAGE_TIME),
            OPTIONAL_READ: json.dumps(CCUSAGE_20_0_38_OPTIONAL_DEPENDENCIES),
            LINUX_X64_TIME_READ: json.dumps(CCUSAGE_LINUX_X64_TIME),
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
        self.npm_log.unlink(missing_ok=True)
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "FAKE_REGISTRY": str(registry_file),
            "FAKE_REQUESTS": json.dumps(FAKE_REQUESTS),
            "FAKE_NPM_LOG": str(self.npm_log),
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

    def npm_reads(self) -> list[str]:
        """Every `npm view` the last run made, in order."""
        return self.npm_log.read_text().splitlines() if self.npm_log.exists() else []

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
                # The meta package's time, the dependencies, then os and cpu of each one in name order, and the time
                # of the one built for this runner right after its own os and cpu; no other package's time.
                reads = self.npm_reads()
                self.assertEqual([META_TIME_READ, OPTIONAL_READ], reads[:2])
                self.assertEqual(
                    sorted(f"view --json {package}@20.0.38 os cpu" for package in CCUSAGE_PLATFORM_PACKAGES),
                    [read for read in reads if read.endswith(" os cpu")],
                )
                self.assertEqual(reads.index(LINUX_X64_READ) + 1, reads.index(LINUX_X64_TIME_READ))
                self.assertEqual(
                    [META_TIME_READ, LINUX_X64_TIME_READ], [read for read in reads if read.endswith(" time")]
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

    def test_a_dependency_on_a_tag_or_a_range_is_refused_before_any_platform_read(self) -> None:
        # npm would resolve a tag or a range to a version this check never saw, so the object is refused whole, before
        # the `os cpu` read of any package in it, however the other entries look. A prerelease is one exact version.
        for name, listed in (
            ("a tag", {"@ccusage/ccusage-linux-x64": "latest"}),
            ("a caret range", {"@ccusage/ccusage-linux-x64": "^20.0.0"}),
            ("a tilde range", {"@ccusage/ccusage-linux-x64": "~20.0.38"}),
            ("an x-range", {"@ccusage/ccusage-linux-x64": "20.x"}),
            ("a bounded range", {"@ccusage/ccusage-linux-x64": ">=20.0.0 <21"}),
            ("build metadata", {"@ccusage/ccusage-linux-x64": "20.0.38+build.1"}),
            (
                "a range on another runner's package",
                {**CCUSAGE_20_0_38_OPTIONAL_DEPENDENCIES, "@ccusage/ccusage-win32-arm64": "20.x"},
            ),
        ):
            with self.subTest(name):
                result = self.run_check(
                    "npm:ccusage", now=PAST_THE_MARGIN, registry={OPTIONAL_READ: json.dumps(listed)}
                )
                output = result.stdout + result.stderr
                self.assertEqual(2, result.returncode, output)
                self.assertIn(f"npm view --json ccusage@20.0.38 optionalDependencies printed {listed!r}", output)
                self.assertIn("not an object of package name to one exact version", output)
                self.assertNotIn("pass:", result.stdout)
                self.assertEqual([META_TIME_READ, OPTIONAL_READ], self.npm_reads())
        with self.subTest("a prerelease is one exact version"):
            prerelease = {"@ccusage/ccusage-linux-x64": "20.0.38-beta.1"}
            prerelease_read = "view --json @ccusage/ccusage-linux-x64@20.0.38-beta.1 os cpu"
            result = self.run_check(
                "npm:ccusage",
                now=PAST_THE_MARGIN,
                registry={
                    OPTIONAL_READ: json.dumps(prerelease),
                    prerelease_read: json.dumps({"os": ["linux"], "cpu": ["x64"]}),
                },
            )
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("npm view lists no publish time for 20.0.38-beta.1", result.stderr)
            self.assertEqual([META_TIME_READ, OPTIONAL_READ, prerelease_read, LINUX_X64_TIME_READ], self.npm_reads())

    def test_the_runner_s_platform_and_architecture_are_one_word_each_on_every_run(self) -> None:
        # Read once before any tool, so a malformed answer is exit 2 even when no tool has an optional dependency to
        # match it against (ccstatusline), and before any registry read.
        for name, fakes, message in (
            ("an empty platform", {"FAKE_PLATFORM": ""}, "process.platform printed '', not one word"),
            (
                "a platform of two lines",
                {"FAKE_PLATFORM": "linux\nx64"},
                "process.platform printed 'linux\\nx64', not one word",
            ),
            (
                "a platform of two words",
                {"FAKE_PLATFORM": "linux x64"},
                "process.platform printed 'linux x64', not one word",
            ),
            ("a negated platform", {"FAKE_PLATFORM": "!linux"}, "process.platform printed '!linux', not one word"),
            ("an empty architecture", {"FAKE_ARCH": ""}, "process.arch printed '', not one word"),
            (
                "an architecture of two lines",
                {"FAKE_ARCH": "x64\narm64"},
                "process.arch printed 'x64\\narm64', not one word",
            ),
        ):
            for tool in ("npm:ccstatusline", "npm:ccusage"):
                with self.subTest(name, tool=tool):
                    result = self.run_check(tool, now=PAST_THE_MARGIN, **fakes)
                    output = result.stdout + result.stderr
                    self.assertEqual(2, result.returncode, output)
                    self.assertIn(f"mise -C {self.config_dir} exec node -- node -p {message}", result.stderr)
                    self.assertEqual("", result.stdout)
                    self.assertEqual([], self.npm_reads())

    def test_the_version_mise_resolves_is_one_exact_version_before_any_registry_read(self) -> None:
        # `mise latest` answers before any npm view; a tag, a range, two lines or nothing is exit 2 there, so no
        # registry read is made for a version this check cannot name.
        for name, latest in (
            ("a tag", "latest"),
            ("two lines", "20.0.38\n20.0.39"),
            ("a range", "^20.0.0"),
            ("build metadata", "20.0.38+build"),
            ("nothing", ""),
        ):
            with self.subTest(name):
                result = self.run_check("npm:ccusage", now=PAST_THE_MARGIN, FAKE_LATEST=latest)
                output = result.stdout + result.stderr
                self.assertEqual(2, result.returncode, output)
                self.assertIn(
                    f"mise -C {self.config_dir} latest npm:ccusage@20.0.38 printed {latest!r}, not one exact version",
                    result.stderr,
                )
                self.assertEqual("", result.stdout)
                self.assertEqual([], self.npm_reads())
        with self.subTest("a prerelease is one exact version"):
            result = self.run_check("npm:ccusage", now=PAST_THE_MARGIN, FAKE_LATEST="20.0.38-beta.1")
            self.assertEqual(2, result.returncode, result.stdout + result.stderr)
            self.assertIn("npm view lists no publish time for 20.0.38-beta.1", result.stderr)
            self.assertEqual([META_TIME_READ], self.npm_reads())

    # Fail closed: every read the verdict rests on has its command failing and an answer of another shape injected
    # here, and none is read as "old enough" (the clock is past the margin, so a swallowed failure would print the
    # pass line). Each row: the case, the registry answers replaced, the fake's variables, the message, the read.
    TWO_REQUESTS = '{"requested_versions": ["20.0.37", "20.0.38"]}'
    FAILURES: tuple[tuple[str, dict[str, str | None], dict[str, str], str, str | None], ...] = (
        (
            "mise settings get fails",
            {},
            {"FAKE_FAIL": "settings"},
            "settings get minimum_release_age failed",
            SETTINGS_READ,
        ),
        ("mise settings get prints 72", {}, {"FAKE_WINDOW": "72"}, "printed '72', not <N>h or <N>d", SETTINGS_READ),
        (
            "mise settings get prints 3 days",
            {},
            {"FAKE_WINDOW": "3 days"},
            "printed '3 days', not <N>h or <N>d",
            SETTINGS_READ,
        ),
        (
            "node -p process.platform fails",
            {},
            {"FAKE_FAIL": "platform"},
            "node -p process.platform failed",
            PLATFORM_READ,
        ),
        (
            "node -p process.platform prints two words",
            {},
            {"FAKE_PLATFORM": "linux x64"},
            "printed 'linux x64', not one word",
            PLATFORM_READ,
        ),
        ("node -p process.arch fails", {}, {"FAKE_FAIL": "arch"}, "node -p process.arch failed", ARCH_READ),
        (
            "node -p process.arch prints nothing",
            {},
            {"FAKE_ARCH": ""},
            "process.arch printed '', not one word",
            ARCH_READ,
        ),
        ("mise tool --json fails", {}, {"FAKE_FAIL": "tool"}, "tool --json npm:ccusage failed", TOOL_READ),
        (
            "mise tool --json prints no JSON",
            {},
            {"FAKE_TOOL_JSON": "not json"},
            "tool --json npm:ccusage printed no JSON",
            TOOL_READ,
        ),
        ("mise tool --json prints a list", {}, {"FAKE_TOOL_JSON": "[]"}, "not one version request", TOOL_READ),
        (
            "mise tool --json lists two requests",
            {},
            {"FAKE_TOOL_JSON": TWO_REQUESTS},
            "not one version request",
            TOOL_READ,
        ),
        ("the config requests no version", {}, {"FAKE_REQUESTS": "{}"}, "not one version request", TOOL_READ),
        ("mise latest fails", {}, {"FAKE_FAIL": "latest"}, "latest npm:ccusage@20.0.38 failed", LATEST_READ),
        ("mise latest prints two lines", {}, {"FAKE_LATEST": "20.0.38\n20.0.39"}, "not one exact version", LATEST_READ),
        ("mise latest prints a tag", {}, {"FAKE_LATEST": "latest"}, "not one exact version", LATEST_READ),
        ("npm view time fails", {META_TIME_READ: None}, {}, "npm view --json ccusage time failed", TIME_FIELD),
        (
            "npm view time prints no JSON",
            {META_TIME_READ: "not json"},
            {},
            "npm view printed no JSON publish times",
            TIME_FIELD,
        ),
        (
            "npm view time prints a list",
            {META_TIME_READ: "[]"},
            {},
            "npm view lists no publish time for 20.0.38",
            TIME_FIELD,
        ),
        (
            "npm view time lacks the version",
            {META_TIME_READ: json.dumps({"20.0.37": CCUSAGE_TIME["20.0.37"]})},
            {},
            "npm view lists no publish time for 20.0.38",
            TIME_FIELD,
        ),
        (
            "npm view optionalDependencies fails",
            {OPTIONAL_READ: None},
            {},
            "npm view --json ccusage@20.0.38 optionalDependencies failed",
            OPTIONAL_FIELD,
        ),
        (
            "npm view optionalDependencies prints no JSON",
            {OPTIONAL_READ: "not json"},
            {},
            "optionalDependencies printed no JSON",
            OPTIONAL_FIELD,
        ),
        (
            "npm view optionalDependencies prints a list",
            {OPTIONAL_READ: "[]"},
            {},
            "not an object of package name to one exact version",
            OPTIONAL_FIELD,
        ),
        (
            "a dependency on a range",
            {OPTIONAL_READ: '{"@ccusage/ccusage-linux-x64": "^20.0.0"}'},
            {},
            "not an object of package name to one exact version",
            OPTIONAL_FIELD,
        ),
        (
            "a dependency on a tag",
            {OPTIONAL_READ: '{"@ccusage/ccusage-linux-x64": "latest"}'},
            {},
            "not an object of package name to one exact version",
            OPTIONAL_FIELD,
        ),
        (
            "npm view os cpu fails",
            {LINUX_X64_READ: None},
            {},
            "npm view --json @ccusage/ccusage-linux-x64@20.0.38 os cpu failed",
            OS_CPU_FIELD,
        ),
        ("npm view os cpu prints no JSON", {LINUX_X64_READ: "not json"}, {}, "os cpu printed no JSON", OS_CPU_FIELD),
        ("npm view os cpu prints a list", {LINUX_X64_READ: "[]"}, {}, "os and cpu are lists of strings", OS_CPU_FIELD),
        ("os missing", {LINUX_X64_READ: '{"cpu": ["x64"]}'}, {}, "os and cpu are lists of strings", OS_CPU_FIELD),
        (
            "a cpu entry that is not a string",
            {LINUX_X64_READ: '{"os": ["linux"], "cpu": [64]}'},
            {},
            "os and cpu are lists of strings",
            OS_CPU_FIELD,
        ),
        (
            "a negated os entry",
            {LINUX_X64_READ: '{"os": ["!linux"], "cpu": ["x64"]}'},
            {},
            "negated os or cpu",
            OS_CPU_FIELD,
        ),
        (
            "the platform package's publish time fails",
            {LINUX_X64_TIME_READ: None},
            {},
            "npm view --json @ccusage/ccusage-linux-x64 time failed",
            TIME_FIELD,
        ),
        (
            "the platform package's time lacks the version",
            {LINUX_X64_TIME_READ: json.dumps({"20.0.37": CCUSAGE_LINUX_X64_TIME["20.0.37"]})},
            {},
            "npm view lists no publish time for 20.0.38",
            TIME_FIELD,
        ),
        (
            "the frozen clock is not a number",
            {},
            {"NOW": "soon"},
            "the given time ['soon'] is not one number of Unix seconds",
            None,
        ),
        ("the tool is not an npm: tool", {}, {"TOOL": "pipx:ccusage"}, "pipx:ccusage is not an npm: tool", None),
        ("no tool is named", {}, {"TOOL": ""}, "usage: npm-cooldown-skew-check.sh", None),
        ("the config directory is missing", {}, {"MISSING_DIR": "1"}, "is not a directory", None),
    )

    def test_an_answer_that_cannot_be_read_fails_closed_naming_it(self) -> None:
        for name, registry, fakes, message, _ in self.FAILURES:
            with self.subTest(name):
                fakes = dict(fakes)
                if fakes.pop("MISSING_DIR", None):
                    shutil.rmtree(self.config_dir)
                now = fakes.pop("NOW", PAST_THE_MARGIN)
                tools = [tool for tool in (fakes.pop("TOOL", "npm:ccusage"),) if tool]
                result = self.run_check(*tools, now=now, registry=registry, **fakes)
                output = result.stdout + result.stderr
                self.assertEqual(2, result.returncode, output)
                self.assertIn(message, result.stderr)
                self.assertNotIn("pass:", result.stdout)

    def test_every_command_the_check_runs_has_a_failed_run_and_another_shape_injected(self) -> None:
        # The census: the mise commands and npm reads are read from the source, so a read added later without both
        # injections in FAILURES fails here, and a FAILURES row naming a read the source no longer makes fails too.
        source = SKEW_CHECK.read_text()
        mise_reads = set(re.findall(r'mise -C "\$\{config_dir\}" ((?:[^"$\s)]+ )*[^"$\s)]+)', source))
        self.assertIn(NPM_VIEW, mise_reads, "npm_view runs the config's npm through mise")
        npm_fields = set(re.findall(r'npm_view "[^"]*" ([^)]+)\)', source))
        reads = (mise_reads - {NPM_VIEW}) | {f"npm view {field}" for field in npm_fields}
        self.assertEqual(
            {SETTINGS_READ, PLATFORM_READ, ARCH_READ, TOOL_READ, LATEST_READ, TIME_FIELD, OPTIONAL_FIELD, OS_CPU_FIELD},
            reads,
        )
        injected: dict[str, set[str]] = {read: set() for read in reads}
        for name, _, _, _, read in self.FAILURES:
            if read is not None:
                self.assertIn(read, reads, name)
                injected[read].add("failed run" if name.endswith(" fails") else "another shape")
        for read, kinds in injected.items():
            self.assertEqual({"failed run", "another shape"}, kinds, read)


if __name__ == "__main__":
    unittest.main()
