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

    def test_current_session_start_order_is_preserved(self) -> None:
        state_hook = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": "herdr-agent-state",
                    "timeout": 10,
                }
            ],
        }
        attach_hook = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": 'herdr-agents --attach >> "$HOME/.config/herdr/herdr-agents.log" 2>&1 || true',
                    "timeout": 10,
                }
            ],
        }
        managed = {
            "enabledPlugins": {},
            "hooks": {"SessionStart": [state_hook]},
        }
        current = json.dumps(
            {
                "enabledPlugins": {},
                "hooks": {"SessionStart": [attach_hook, state_hook]},
            },
            indent=2,
        ) + "\n"

        output = self.merge(managed, current)

        self.assertEqual(json.loads(output), json.loads(current))
        self.assertEqual(
            json.loads(output)["hooks"]["SessionStart"],
            [attach_hook, state_hook],
        )

    def test_managed_permgate_replaces_stale_current_ccgate_hook(self) -> None:
        managed_hook = {
            "matcher": "*",
            "hooks": [{"type": "command", "command": "permgate claude"}],
        }
        stale_hook = {
            "matcher": "*",
            "hooks": [{"type": "command", "command": "ccgate claude"}],
        }
        output = self.merge(
            {
                "enabledPlugins": {},
                "hooks": {"PermissionRequest": [managed_hook]},
            },
            json.dumps(
                {
                    "enabledPlugins": {},
                    "hooks": {"PermissionRequest": [stale_hook]},
                }
            ),
        )

        permission_hooks = json.loads(output)["hooks"]["PermissionRequest"]
        self.assertEqual(permission_hooks, [managed_hook])
        self.assertNotIn("ccgate", json.dumps(permission_hooks))

    def test_managed_session_start_replaces_stale_hard_coded_home_hook(self) -> None:
        """Upgrade path: a machine that received the old hard-coded managed hook."""
        managed_hook = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session",
                    "timeout": 10,
                }
            ],
        }
        stale_hook = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": "bash '/Users/someone-else/.claude/hooks/herdr-agent-state.sh' session",
                    "timeout": 10,
                }
            ],
        }
        unrelated_hook = {
            "matcher": "*",
            "hooks": [{"type": "command", "command": "custom-session-hook"}],
        }

        output = self.merge(
            {"enabledPlugins": {}, "hooks": {"SessionStart": [managed_hook]}},
            json.dumps(
                {
                    "enabledPlugins": {},
                    "hooks": {"SessionStart": [unrelated_hook, stale_hook]},
                }
            ),
        )

        session_hooks = json.loads(output)["hooks"]["SessionStart"]
        commands = [h["command"] for e in session_hooks for h in e["hooks"]]
        self.assertNotIn("/Users/someone-else", json.dumps(session_hooks))
        self.assertEqual(
            sum(1 for c in commands if "herdr-agent-state.sh" in c),
            1,
            "the managed session-start hook must not be duplicated",
        )
        self.assertIn("custom-session-hook", commands)

    def test_managed_session_start_replacement_keeps_hook_order(self) -> None:
        """Replacing a managed entry must not reorder SessionStart."""
        state_hook = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": "bash '/Users/someone-else/.claude/hooks/herdr-agent-state.sh' session",
                    "timeout": 10,
                }
            ],
        }
        attach_hook = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": 'herdr-agents --attach >> "$HOME/.config/herdr/herdr-agents.log" 2>&1 || true',
                    "timeout": 10,
                }
            ],
        }
        managed_state = {
            "matcher": "*",
            "hooks": [
                {
                    "type": "command",
                    "command": "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session",
                    "timeout": 10,
                }
            ],
        }

        output = self.merge(
            {"enabledPlugins": {}, "hooks": {"SessionStart": [managed_state]}},
            json.dumps(
                {
                    "enabledPlugins": {},
                    "hooks": {"SessionStart": [state_hook, attach_hook]},
                }
            ),
        )

        commands = [
            h["command"]
            for e in json.loads(output)["hooks"]["SessionStart"]
            for h in e["hooks"]
        ]
        self.assertTrue(
            commands[0].endswith("herdr-agent-state.sh' session"),
            f"state hook must stay first, got {commands}",
        )
        self.assertIn("herdr-agents --attach", commands[1])
        self.assertNotIn("/Users/someone-else", json.dumps(commands))

    def test_permission_merge_preserves_unrelated_current_hooks(self) -> None:
        managed_hook = {
            "matcher": "*",
            "hooks": [{"type": "command", "command": "permgate claude"}],
        }
        stale_hook = {
            "matcher": "*",
            "hooks": [{"type": "command", "command": "ccgate claude"}],
        }
        custom_hook = {
            "matcher": "Bash",
            "hooks": [{"type": "command", "command": "custom-audit-hook"}],
        }

        output = self.merge(
            {
                "enabledPlugins": {},
                "hooks": {"PermissionRequest": [managed_hook]},
            },
            json.dumps(
                {
                    "enabledPlugins": {},
                    "hooks": {"PermissionRequest": [custom_hook, stale_hook]},
                }
            ),
        )

        permission_hooks = json.loads(output)["hooks"]["PermissionRequest"]
        self.assertEqual(permission_hooks, [custom_hook, managed_hook])

    def test_permission_merge_preserves_custom_hook_in_mixed_entry(self) -> None:
        managed_hook = {
            "matcher": "*",
            "hooks": [{"type": "command", "command": "permgate claude"}],
        }
        mixed_hook = {
            "matcher": "*",
            "hooks": [
                {"type": "command", "command": "/opt/homebrew/bin/ccgate claude"},
                {"type": "command", "command": "custom-audit-hook"},
            ],
        }

        output = self.merge(
            {
                "enabledPlugins": {},
                "hooks": {"PermissionRequest": [managed_hook]},
            },
            json.dumps(
                {
                    "enabledPlugins": {},
                    "hooks": {"PermissionRequest": [mixed_hook]},
                }
            ),
        )

        permission_hooks = json.loads(output)["hooks"]["PermissionRequest"]
        self.assertEqual(
            permission_hooks,
            [
                {
                    "matcher": "*",
                    "hooks": [{"type": "command", "command": "custom-audit-hook"}],
                },
                managed_hook,
            ],
        )

    def test_managed_hook_object_key_order_is_preserved(self) -> None:
        managed = {
            "enabledPlugins": {},
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [
                            {
                                "type": "command",
                                "command": "managed-command",
                            }
                        ],
                    }
                ]
            },
        }
        current = (
            '{"enabledPlugins":{},"hooks":{"PreToolUse":[{"matcher":"Bash",'
            '"hooks":[{"command":"managed-command","type":"command"}]}]}}'
        )

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
