#!/usr/bin/env python3
"""Verify statusline tools are pinned and execute without network installers."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MISE_CONFIG = ROOT / "home/dot_mise/config.toml"
MISE_LOCK = ROOT / "home/dot_mise/mise.lock"
CCUSAGE_SETTINGS = ROOT / "home/dot_ccstatusline/settings.json"
CLAUDE_SETTINGS = ROOT / "home/.chezmoitemplates/claude-settings-managed.json"
CI_WORKFLOW = ROOT / ".github/workflows/test.yaml"
INTEGRATION_SMOKE = ROOT / "scripts/check-statusline-tools.py"
EXPECTED_TOOLS = {
    "npm:ccusage": "20.0.17",
    "npm:ccstatusline": "2.2.23",
}


class StatuslineToolsTest(unittest.TestCase):
    def commands(self) -> tuple[str, str]:
        ccusage = json.loads(CCUSAGE_SETTINGS.read_text())["lines"][0][0]["commandPath"]
        ccstatusline = json.loads(CLAUDE_SETTINGS.read_text())["statusLine"]["command"]
        return ccusage, ccstatusline

    def test_mise_config_and_lock_pin_exact_npm_versions(self) -> None:
        config = tomllib.loads(MISE_CONFIG.read_text())
        self.assertEqual(config["tools"] | EXPECTED_TOOLS, config["tools"])
        self.assertEqual(
            config["settings"]["lockfile_platforms"],
            ["linux-x64", "linux-arm64", "macos-x64", "macos-arm64"],
        )

        lock = tomllib.loads(MISE_LOCK.read_text())
        for tool, version in EXPECTED_TOOLS.items():
            self.assertEqual(lock["tools"][tool][0]["version"], version)
            self.assertEqual(lock["tools"][tool][0]["backend"], tool)

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
                executable.write_text(
                    f'#!/bin/sh\nprintf "{name}%s\\n" "${{*:+ $*}}" >> "{log}"\n'
                )
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

    def test_ci_smokes_exact_tools_with_network_denied(self) -> None:
        workflow = CI_WORKFLOW.read_text()
        smoke = INTEGRATION_SMOKE.read_text()

        for token in (
            "npm:ccstatusline@2.2.23",
            "npm:ccusage@20.0.17",
            'mise trust --yes "${RUNNER_TEMP}/statusline-mise/mise.toml"',
            "sudo unshare --net",
            "/usr/bin/sandbox-exec",
            "ip route show",
            's.bind(("127.0.0.1", 0))',
            "scripts/check-statusline-tools.py",
        ):
            self.assertIn(token, workflow)
        for token in (
            '"display_name": "Claude"',
            '"session_id": "offline-test"',
            "timeout=5",
            'run([str(args.ccusage), "statusline"]',
        ):
            self.assertIn(token, smoke)


if __name__ == "__main__":
    unittest.main()
