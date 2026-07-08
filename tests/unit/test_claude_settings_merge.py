#!/usr/bin/env python3
"""Exercise Claude settings modify-script merge behavior."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MERGE_SCRIPT = ROOT / "home/dot_claude/modify_private_settings.json"


class ClaudeSettingsMergeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="claude-settings-merge-test-")
        self.source_dir = Path(self.temp_dir.name)
        (self.source_dir / ".chezmoitemplates").mkdir()
        self.baseline_path = self.source_dir / ".chezmoitemplates/claude-settings-managed.json"
        self.home_dir = self.source_dir / "target-home"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def merge(self, managed: dict[str, Any], current: str) -> str:
        self.baseline_path.write_text(json.dumps(managed, indent=2) + "\n")
        env = os.environ.copy()
        env["CHEZMOI_SOURCE_DIR"] = str(self.source_dir)
        env["CHEZMOI_HOME_DIR"] = str(self.home_dir)
        result = subprocess.run(
            ["uv", "run", "python", str(MERGE_SCRIPT)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=True,
        )
        json.loads(result.stdout)
        return result.stdout

    def test_managed_wins_for_managed_key(self) -> None:
        output = self.merge(
            {"model": "managed", "enabledPlugins": {}},
            json.dumps({"model": "runtime", "enabledPlugins": {}}),
        )

        self.assertEqual(json.loads(output)["model"], "managed")

    def test_enabled_plugins_are_preserved_from_current(self) -> None:
        output = self.merge(
            {"model": "managed", "enabledPlugins": {}},
            json.dumps({"model": "runtime", "enabledPlugins": {"crit@crit": True}}),
        )

        self.assertEqual(json.loads(output)["enabledPlugins"], {"crit@crit": True})

    def test_current_only_key_is_preserved(self) -> None:
        output = self.merge(
            {"model": "managed", "enabledPlugins": {}},
            json.dumps({"model": "runtime", "runtimeOnly": {"kept": True}}),
        )

        self.assertEqual(json.loads(output)["runtimeOnly"], {"kept": True})

    def test_empty_stdin_outputs_managed(self) -> None:
        managed = {"model": "managed", "enabledPlugins": {}}
        output = self.merge(managed, "   \n")

        self.assertEqual(json.loads(output), managed)

    def test_invalid_json_outputs_managed(self) -> None:
        managed = {"model": "managed", "enabledPlugins": {}}
        output = self.merge(managed, "{not json")

        self.assertEqual(json.loads(output), managed)

    def test_merge_is_idempotent(self) -> None:
        managed = {"model": "managed", "effortLevel": "high", "enabledPlugins": {}}
        current = json.dumps({"enabledPlugins": {"crit@crit": True}, "model": "runtime", "localState": 1}, indent=2) + "\n"

        once = self.merge(managed, current)
        twice = self.merge(managed, once)

        self.assertEqual(twice, once)

    def test_desired_current_output_is_byte_identical(self) -> None:
        managed = {"model": "managed", "effortLevel": "high", "enabledPlugins": {}}
        current = (
            json.dumps(
                {
                    "enabledPlugins": {"crit@crit": True},
                    "model": "managed",
                    "localState": 1,
                    "effortLevel": "high",
                },
                indent=2,
            )
            + "\n"
        )

        self.assertEqual(self.merge(managed, current), current)

    def test_reordered_but_equal_current_is_byte_identical(self) -> None:
        managed = {"model": "managed", "effortLevel": "high", "enabledPlugins": {}}
        current = '{"enabledPlugins":{"crit@crit":true},"effortLevel":"high","model":"managed"}'

        self.assertEqual(self.merge(managed, current), current)

    def test_real_value_change_is_redumped(self) -> None:
        managed = {"model": "managed", "effortLevel": "high", "enabledPlugins": {}}
        current = '{"enabledPlugins":{"crit@crit":true},"effortLevel":"low","model":"managed"}'

        output = self.merge(managed, current)

        self.assertNotEqual(output, current)
        self.assertEqual(json.loads(output)["effortLevel"], "high")
        self.assertTrue(output.endswith("\n"))

    def test_trailing_newline(self) -> None:
        output = self.merge({"model": "managed", "enabledPlugins": {}}, "")

        self.assertTrue(output.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
