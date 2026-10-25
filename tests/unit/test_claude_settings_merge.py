#!/usr/bin/env python3
"""Exercise Claude settings modify-script merge behavior."""

from __future__ import annotations

import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

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

    def test_runtime_enabled_plugins_survive_a_managed_file_without_the_key(self) -> None:
        output = self.merge(
            {"model": "managed"},
            json.dumps({"model": "runtime", "enabledPlugins": {"crit@crit": True}}),
        )

        self.assertEqual(json.loads(output)["enabledPlugins"], {"crit@crit": True})

    def test_current_only_key_is_preserved(self) -> None:
        output = self.merge(
            {"model": "managed", "enabledPlugins": {}},
            json.dumps({"model": "runtime", "runtimeOnly": {"kept": True}}),
        )

        self.assertEqual(json.loads(output)["runtimeOnly"], {"kept": True})

    def test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win(self) -> None:
        managed = {
            "env": {
                "GH_TELEMETRY": "false",
                "DO_NOT_TRACK": "1",
                "CHECKPOINT_DISABLE": "1",
                "AWS_EC2_METADATA_DISABLED": "true",
            }
        }
        existing = {
            "CUSTOM_RUNTIME_MARKER": "keep-me",
            "ANTHROPIC_BASE_URL": "https://provider.invalid",
            "HTTPS_PROXY": "https://proxy.invalid",
            "GH_TELEMETRY": "true",
        }
        once = self.merge(managed, json.dumps({"env": existing}))
        self.assertEqual(existing | managed["env"], json.loads(once)["env"])
        self.assertEqual(once, self.merge(managed, once))

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
        current = (
            json.dumps(
                {
                    "enabledPlugins": {"crit@crit": True},
                    "model": "runtime",
                    "localState": 1,
                },
                indent=2,
            )
            + "\n"
        )

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
        """Order is preserved; a stale herdr-agents --attach hook leaves, as the managed attach hook did (U26)."""
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
        stale_attach_hook = {
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
        current = (
            json.dumps(
                {
                    "enabledPlugins": {},
                    "hooks": {"SessionStart": [stale_attach_hook, state_hook]},
                },
                indent=2,
            )
            + "\n"
        )

        output = self.merge(managed, current)

        session_hooks = json.loads(output)["hooks"]["SessionStart"]
        self.assertEqual(session_hooks, [state_hook])

    def test_session_start_hook_that_only_mentions_a_managed_script_survives(self) -> None:
        """Only the invoked executable (or the script an interpreter runs) makes a hook managed, never an argument."""
        managed_hook = {
            "matcher": "*",
            "hooks": [
                {"type": "command", "command": f"{self.home_dir}/.local/bin/common/agent-session-staleness hook"},
                {"type": "command", "command": f"bash '{self.home_dir}/.claude/hooks/herdr-agent-state.sh' session"},
            ],
        }
        mentions = [
            "logger -t agent-session-staleness started",
            "echo herdr-agent-state.sh",
            "logger herdr-agents",
            "bash ~/bin/wrap.sh agent-session-staleness",
        ]
        for command in mentions:
            unrelated = {"matcher": "*", "hooks": [{"type": "command", "command": command}]}
            with self.subTest(command=command):
                output = self.merge(
                    {"hooks": {"SessionStart": [managed_hook]}},
                    json.dumps({"hooks": {"SessionStart": [unrelated]}}),
                )
                commands = [h["command"] for e in json.loads(output)["hooks"]["SessionStart"] for h in e["hooks"]]
                self.assertIn(command, commands)

        invocations = [
            "/Users/someone-else/.local/bin/common/agent-session-staleness hook",
            "FOO=1 /Users/someone-else/.local/bin/common/agent-session-staleness hook",
            "sh '/Users/someone-else/.claude/hooks/herdr-agent-state.sh' session",
            'herdr-agents --attach >> "$HOME/.config/herdr/herdr-agents.log" 2>&1 || true',
        ]
        for command in invocations:
            stale = {"matcher": "*", "hooks": [{"type": "command", "command": command, "async": True}]}
            with self.subTest(command=command):
                output = self.merge(
                    {"hooks": {"SessionStart": [managed_hook]}},
                    json.dumps({"hooks": {"SessionStart": [stale]}}),
                )
                self.assertEqual(json.loads(output)["hooks"]["SessionStart"], [managed_hook])

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

        commands = [h["command"] for e in json.loads(output)["hooks"]["SessionStart"] for h in e["hooks"]]
        self.assertEqual(len(commands), 1, f"the stale attach hook leaves (U26), got {commands}")
        self.assertTrue(
            commands[0].endswith("herdr-agent-state.sh' session"),
            f"state hook must stay first, got {commands}",
        )
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

    def test_managed_post_tool_use_replaces_stale_format_only_entry(self) -> None:
        format_hook = {"type": "command", "command": "~/.claude/hooks/format-edited-files.py"}
        reload_hook = {"type": "command", "command": "~/.claude/hooks/project-map-reload.sh"}
        custom_hook = {"type": "command", "command": "~/bin/my-hook.sh"}
        managed_entry = {"matcher": "Write|Edit|MultiEdit", "hooks": [format_hook, reload_hook]}
        stale_entry = {"matcher": "Write|Edit|MultiEdit", "hooks": [format_hook]}
        mixed_entry = {"matcher": "Write|Edit|MultiEdit", "hooks": [format_hook, custom_hook]}
        wrapper_entry = {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [{"type": "command", "command": "~/bin/log-hook.sh ~/.claude/hooks/format-edited-files.py"}],
        }
        chained_entry = {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [{"type": "command", "command": "~/.claude/hooks/format-edited-files.py && ~/bin/audit-edit.sh"}],
        }
        same_basename_entry = {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [{"type": "command", "command": "/opt/team/format-edited-files.py"}],
        }
        compact_chain_entry = {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [{"type": "command", "command": "~/bin/audit-edit.sh;~/.claude/hooks/format-edited-files.py"}],
        }
        absolute_entry = {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [{"type": "command", "command": str(self.home_dir / ".claude/hooks/format-edited-files.py")}],
        }
        project_local_entry = {
            "matcher": "Write|Edit|MultiEdit",
            "hooks": [{"type": "command", "command": "/workspace/team/.claude/hooks/format-edited-files.py"}],
        }
        cases = [
            ("stale and managed", [stale_entry, managed_entry], [managed_entry]),
            ("stale alone", [stale_entry], [managed_entry]),
            (
                "mixed custom command",
                [mixed_entry],
                [{"matcher": "Write|Edit|MultiEdit", "hooks": [custom_hook]}, managed_entry],
            ),
            ("absent key", None, [managed_entry]),
            ("wrapper argument", [wrapper_entry, stale_entry], [wrapper_entry, managed_entry]),
            ("chained user command", [chained_entry, stale_entry], [chained_entry, managed_entry]),
            ("same basename", [same_basename_entry, stale_entry], [same_basename_entry, managed_entry]),
            ("compact chain", [compact_chain_entry, stale_entry], [compact_chain_entry, managed_entry]),
            ("absolute managed path", [absolute_entry], [managed_entry]),
            ("project-local path", [project_local_entry, stale_entry], [project_local_entry, managed_entry]),
        ]
        for interpreter in ("python3", "python", "bash", "sh"):
            interpreted = {
                "matcher": "Write|Edit|MultiEdit",
                "hooks": [
                    {"type": "command", "command": f"/usr/bin/{interpreter} ~/.claude/hooks/format-edited-files.py"}
                ],
            }
            cases.append(("unmanaged interpreter", [interpreted], [interpreted, managed_entry]))
        for command in (
            "~/bin/my-hook.sh",
            "'unterminated",
            None,
            "",
            "python3",
            "bash",
            "~/.claude/hooks/format-edited-files.py --custom",
            "python3 ~/.claude/hooks/format-edited-files.py --custom",
            "python3 /opt/team/format-edited-files.py",
            "python3 /workspace/team/.claude/hooks/format-edited-files.py",
            "~/bin/audit-edit.sh;/usr/bin/python3 ~/.claude/hooks/format-edited-files.py",
            "/former-home/.claude/hooks/format-edited-files.py",
            "bash ~/.claude/hooks/project-map-reload.sh && ~/bin/audit-edit.sh",
        ):
            unmanaged = {"matcher": "Bash", "hooks": [{"type": "command", "command": command}]}
            cases.append(("unmanaged command", [unmanaged, stale_entry], [unmanaged, managed_entry]))
        for name, current_entries, expected in cases:
            with self.subTest(case=name, entries=current_entries):
                current_hooks = {} if current_entries is None else {"PostToolUse": current_entries}
                output = self.merge(
                    {"hooks": {"PostToolUse": [managed_entry]}},
                    json.dumps({"hooks": current_hooks}),
                )
                self.assertEqual(json.loads(output)["hooks"]["PostToolUse"], expected)

    def test_managed_post_tool_use_keeps_a_quoted_or_escaped_tilde_path(self) -> None:
        # audit:ca892e4:1: a quoted or escaped ~ names a literal ~ directory in the shell, not the managed home path.
        format_hook = {"type": "command", "command": "~/.claude/hooks/format-edited-files.py"}
        reload_hook = {"type": "command", "command": "~/.claude/hooks/project-map-reload.sh"}
        managed_entry = {"matcher": "Write|Edit|MultiEdit", "hooks": [format_hook, reload_hook]}
        for command in ("'~/.claude/hooks/format-edited-files.py'", "\\~/.claude/hooks/format-edited-files.py"):
            literal = {"matcher": "Write|Edit|MultiEdit", "hooks": [{"type": "command", "command": command}]}
            with self.subTest(command=command):
                output = self.merge(
                    {"hooks": {"PostToolUse": [managed_entry]}},
                    json.dumps({"hooks": {"PostToolUse": [literal]}}),
                )
                self.assertEqual(json.loads(output)["hooks"]["PostToolUse"], [literal, managed_entry])

    def test_managed_pre_tool_use_is_not_duplicated_next_to_an_unmanaged_hook(self) -> None:
        enforce = {"type": "command", "command": "~/.claude/hooks/enforce-uv.sh"}
        audit = {"type": "command", "command": "~/bin/audit-bash.sh"}
        managed_entry = {"matcher": "Bash", "hooks": [enforce]}
        current = json.dumps({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [enforce, audit]}]}})
        output = self.merge({"hooks": {"PreToolUse": [managed_entry]}}, current)
        expected = [{"matcher": "Bash", "hooks": [audit]}, managed_entry]
        self.assertEqual(json.loads(output)["hooks"]["PreToolUse"], expected)
        # A second apply is a fixed point: enforce-uv.sh still runs once.
        self.assertEqual(self.merge({"hooks": {"PreToolUse": [managed_entry]}}, output), output)

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

    def test_real_template_preserves_herdr_matcher_and_converges(self) -> None:
        render = runpy.run_path(str(MERGE_SCRIPT))["render_managed_template"]
        with mock.patch.dict(os.environ, {"CHEZMOI_HOME_DIR": str(self.home_dir)}):
            managed = json.loads(render((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()))
        canonical_matcher = "^(startup|resume|clear|compact|fork)$"
        current = json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {
                            "matcher": canonical_matcher,
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": f"bash '{self.home_dir}/.claude/hooks/herdr-agent-state.sh' session",
                                    "timeout": 10,
                                }
                            ],
                        }
                    ]
                },
            }
        )

        once = self.merge(managed, current)
        state_entries = [
            entry
            for entry in json.loads(once)["hooks"]["SessionStart"]
            if any("herdr-agent-state.sh" in hook["command"] for hook in entry["hooks"])
        ]
        self.assertEqual(len(state_entries), 1)
        self.assertEqual(state_entries[0]["matcher"], canonical_matcher)
        self.assertEqual(self.merge(managed, once), once)

    def test_installed_async_staleness_hook_is_replaced_by_the_synchronous_one(self) -> None:
        render = runpy.run_path(str(MERGE_SCRIPT))["render_managed_template"]
        with mock.patch.dict(os.environ, {"CHEZMOI_HOME_DIR": str(self.home_dir)}):
            managed = json.loads(render((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()))
        command = f"{self.home_dir}/.local/bin/common/agent-session-staleness hook"
        installed = {"type": "command", "command": command, "async": True, "timeout": 5}
        current = json.dumps({"hooks": {"SessionStart": [{"matcher": "*", "hooks": [installed]}]}})

        once = self.merge(managed, current)
        staleness = [
            hook
            for entry in json.loads(once)["hooks"]["SessionStart"]
            for hook in entry["hooks"]
            if "agent-session-staleness" in hook["command"]
        ]
        self.assertEqual(len(staleness), 1, staleness)
        self.assertNotIn("async", staleness[0])
        self.assertEqual(self.merge(managed, once), once)

    def test_retired_update_keys_leave_settings_the_old_template_installed(self) -> None:
        """The former managed defaults go; every other installed key stays; a second run is a no-op (U18, D-024-150)."""
        render = runpy.run_path(str(MERGE_SCRIPT))["render_managed_template"]
        with mock.patch.dict(os.environ, {"CHEZMOI_HOME_DIR": str(self.home_dir)}):
            managed = json.loads(render((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()))
        self.assertNotIn("autoUpdatesChannel", managed, "the current template names no release channel")
        old_template = {}
        for key, value in managed.items():
            old_template[key] = value
            if key == "alwaysThinkingEnabled":
                old_template |= {"autoUpdates": False, "autoUpdatesChannel": "stable"}
        installed = json.loads(self.merge(old_template, ""))
        self.assertEqual((installed["autoUpdates"], installed["autoUpdatesChannel"]), (False, "stable"))
        installed |= {"operatorOnly": {"kept": True}, "enabledPlugins": {"crit@crit": True}}

        after = self.merge(managed, json.dumps(installed))
        merged = json.loads(after)
        self.assertNotIn("autoUpdates", merged)
        self.assertNotIn("autoUpdatesChannel", merged)
        expected = {key: value for key, value in installed.items() if key not in ("autoUpdates", "autoUpdatesChannel")}
        self.assertEqual(merged, expected, "only the two retired keys change")
        self.assertEqual(self.merge(managed, after), after)

    def test_installed_checkout_path_lever_rules_are_replaced_by_the_installed_path_rules(self) -> None:
        """`make update` moves an installed settings file off the checkout-path lever rules (regime-cutover U31)."""
        render = runpy.run_path(str(MERGE_SCRIPT))["render_managed_template"]
        with mock.patch.dict(os.environ, {"CHEZMOI_HOME_DIR": str(self.home_dir)}):
            managed = json.loads(render((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()))
        installed = json.loads(self.merge(managed, ""))
        installed["permissions"]["allow"] = [
            "Bash(agmsg-dispatch:*)",
            *(f"Bash(scripts/orchestrator/{name} *)" for name in ("hcom-seat", "hcom-dispatch", "bus-history.sh")),
            "Bash(scripts/orchestrator/worktree-gc.sh *)",
            "Bash(hcom list *)",
        ]
        installed |= {"operatorOnly": {"kept": True}, "enabledPlugins": {"crit@crit": True}}

        after = self.merge(managed, json.dumps(installed))
        merged = json.loads(after)
        self.assertEqual(merged["permissions"]["allow"], managed["permissions"]["allow"])
        self.assertNotIn("scripts/orchestrator/", json.dumps(merged["permissions"]))
        levers = merged["permissions"]["allow"][:-1]
        self.assertTrue(all("~/.local/bin/common/" in rule for rule in levers))  # lint-comparisons: allow rule-text
        self.assertEqual((merged["operatorOnly"], merged["enabledPlugins"]), ({"kept": True}, {"crit@crit": True}))
        self.assertEqual(self.merge(managed, after), after)

    def test_the_retired_session_bus_env_leaves_installed_settings(self) -> None:
        """U16's HCOM_DIR/HCOM_TEAM go while they hold the old managed values; overrides stay (regime-cutover U33b)."""
        render = runpy.run_path(str(MERGE_SCRIPT))["render_managed_template"]
        with mock.patch.dict(os.environ, {"CHEZMOI_HOME_DIR": str(self.home_dir)}):
            managed = json.loads(render((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()))
        self.assertNotIn("HCOM_DIR", managed["env"], "the current template sets no session-wide bus")
        installed = json.loads(self.merge(managed, ""))
        installed["env"] |= {
            "HCOM_DIR": f"{self.home_dir}/.local/state/hcom-regime",
            "HCOM_TEAM": "regime",
            "OPERATOR_VAR": "kept",
        }
        installed["operatorOnly"] = {"kept": True}

        after = self.merge(managed, json.dumps(installed))
        merged = json.loads(after)
        self.assertNotIn("HCOM_DIR", merged["env"])
        self.assertNotIn("HCOM_TEAM", merged["env"])
        self.assertEqual(merged["env"]["OPERATOR_VAR"], "kept")
        self.assertEqual({k: v for k, v in merged["env"].items() if k != "OPERATOR_VAR"}, managed["env"])
        self.assertEqual(merged["operatorOnly"], {"kept": True})
        self.assertEqual(self.merge(managed, after), after)

    def test_a_session_bus_env_the_operator_set_differently_is_kept(self) -> None:
        managed = {"env": {"DO_NOT_TRACK": "1"}}
        for name, value in (("HCOM_DIR", "/elsewhere/store"), ("HCOM_TEAM", "mine")):
            with self.subTest(name=name):
                output = json.loads(self.merge(managed, json.dumps({"env": {name: value}})))
                self.assertEqual(output["env"], {name: value, "DO_NOT_TRACK": "1"})
        output = json.loads(self.merge({"env": {"HCOM_TEAM": "managed"}}, json.dumps({"env": {"HCOM_TEAM": "regime"}})))
        self.assertEqual(output["env"], {"HCOM_TEAM": "managed"}, "a key the template manages again still wins")

    def test_an_update_value_the_operator_set_differently_is_kept(self) -> None:
        for key, value in (("autoUpdatesChannel", "latest"), ("autoUpdates", True), ("autoUpdates", 0)):
            with self.subTest(key=key, value=value):
                output = self.merge({"model": "managed"}, json.dumps({"model": "runtime", key: value}))
                self.assertEqual(json.loads(output), {"model": "managed", key: value})

    def test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging(self) -> None:
        self.baseline_path.write_text((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text())
        command = "import platform,runpy,sys; platform.system=lambda:sys.argv[1]; runpy.run_path(sys.argv[2],run_name='__main__')"
        env = os.environ | {"CHEZMOI_SOURCE_DIR": str(self.source_dir), "CHEZMOI_HOME_DIR": str(self.home_dir)}
        for os_name in ("Darwin", "Linux"):
            with self.subTest(os=os_name):
                current = json.dumps(
                    {
                        "runtimeOnly": {"kept": True},
                        "enabledPlugins": {"custom@local": True},
                        "env": {"ANTHROPIC_BASE_URL": "https://provider.invalid", "GH_TELEMETRY": "true"},
                    }
                )
                for _ in range(2):
                    result = subprocess.run(
                        [sys.executable, "-c", command, os_name, str(MERGE_SCRIPT)],
                        input=current,
                        text=True,
                        capture_output=True,
                        env=env,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    settings = json.loads(result.stdout)
                    self.assertEqual({"kept": True}, settings["runtimeOnly"])
                    self.assertEqual({"custom@local": True}, settings["enabledPlugins"])
                    self.assertEqual("https://provider.invalid", settings["env"]["ANTHROPIC_BASE_URL"])
                    self.assertEqual("false", settings["env"]["GH_TELEMETRY"])
                    self.assertEqual(
                        ["com.apple.trustd.agent"] if os_name == "Darwin" else [],
                        settings["sandbox"]["network"].get("allowMachLookup", []),
                    )
                    self.assertEqual(
                        [],
                        settings["sandbox"]["excludedCommands"],
                    )
                    if "sandbox" in json.loads(current):
                        self.assertEqual(result.stdout, current)
                    current = result.stdout

    def test_trailing_newline(self) -> None:
        output = self.merge({"model": "managed", "enabledPlugins": {}}, "")

        self.assertTrue(output.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
