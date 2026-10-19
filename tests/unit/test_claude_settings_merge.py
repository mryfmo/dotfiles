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

from tests.unit.test_generate_agent_configs import all_hooks

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
        """Order is preserved; a stale bare herdr-agents command still migrates."""
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
        commands = [h["command"] for e in session_hooks for h in e["hooks"]]
        self.assertEqual(len(session_hooks), 2)
        self.assertTrue(
            commands[0].startswith('/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME"')
            and commands[0].endswith('"$HOME/.claude/hooks/orchestrator-only.sh" herdr-agents'),
            f"attach hook must migrate to the installed guard, got {commands[0]!r}",
        )
        self.assertEqual(session_hooks[1], state_hook)

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
        self.assertTrue(
            commands[0].endswith("herdr-agent-state.sh' session"),
            f"state hook must stay first, got {commands}",
        )
        self.assertIn('orchestrator-only.sh" herdr-agents', commands[1])
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
                        [
                            "agmsg-dispatch *",
                            "herdr-agents *",
                            f"{self.home_dir}/.agents/skills/agmsg/scripts/actas-claim.sh *",
                        ],
                        settings["sandbox"]["excludedCommands"],
                    )
                    if "sandbox" in json.loads(current):
                        self.assertEqual(result.stdout, current)
                    current = result.stdout

    def test_trailing_newline(self) -> None:
        output = self.merge({"model": "managed", "enabledPlugins": {}}, "")

        self.assertTrue(output.endswith("\n"))

    def test_prefixed_guarded_managed_hooks_replace_legacy_hooks_idempotently(self):
        prefix = '/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}" '
        guard = '"$HOME/.claude/hooks/orchestrator-only.sh" '

        def entry(commands):
            return {
                "matcher": "*",
                "hooks": [{"type": "command", "command": c, "onFailure": "block"} for c in commands],
            }

        state = prefix + guard + 'herdr-agent-state.sh "${HERDR_PANE_ID}"'
        formatting = prefix + guard + "format-edited-files.py"
        mapping = prefix + guard + "project-map-reload.sh"
        attachment = (
            prefix
            + 'HERDR_ENV="${HERDR_ENV}" HERDR_PANE_ID="${HERDR_PANE_ID}" HERDR_WORKSPACE_ID="${HERDR_WORKSPACE_ID}" '
            + guard
            + "herdr-agents"
        )
        staleness = prefix + guard + "agent-session-staleness"
        legacy_staleness = f"{self.home_dir}/.local/bin/common/agent-session-staleness hook"
        custom = "custom-wrapper format-edited-files.py"
        foreign = [
            prefix + "'$HOME/.claude/hooks/orchestrator-only.sh' format-edited-files.py",
            prefix + '"/foreign/orchestrator-only.sh" format-edited-files.py',
            prefix + guard + "format-edited-files.py extra",
            prefix.replace("PATH=/usr/bin:/bin", "PATH=/tmp") + guard + "format-edited-files.py",
            "wrapper " + prefix + guard + "herdr-agent-state.sh",
            prefix + guard + "herdr-agent-state.sh extra",
            "echo herdr-agents",
        ]
        managed = {
            "hooks": {
                "SessionStart": [entry([state]), entry([staleness])],
                "PostToolUse": [entry([formatting, mapping])],
            }
        }
        current = {
            "hooks": {
                "SessionStart": [
                    entry(["bash '/old-home/.claude/hooks/herdr-agent-state.sh' session"]),
                    entry([legacy_staleness]),
                    entry(
                        [
                            f'{self.home_dir}/.local/bin/common/herdr-agents --attach 2>> "$HOME/.config/herdr/herdr-agents.log" || true'
                        ]
                    ),
                    *[entry([c]) for c in foreign],
                ],
                "PostToolUse": [
                    entry(["~/.claude/hooks/format-edited-files.py", custom]),
                    *[entry([c]) for c in foreign],
                ],
            }
        }
        once = self.merge(managed, json.dumps(current))
        self.assertEqual(once, self.merge(managed, once))
        events = json.loads(once)["hooks"]
        self.assertEqual(events["SessionStart"][0], entry([state]))
        self.assertEqual(events["PostToolUse"][0], entry([custom]))
        for event in events.values():
            commands = [h["command"] for e in event for h in e["hooks"]]
            self.assertTrue(all(c in commands for c in foreign))
        commands = [h["command"] for e in events["SessionStart"] for h in e["hooks"]]
        self.assertEqual(commands.count(attachment), 1)
        self.assertEqual(commands.count(staleness), 1)
        self.assertNotIn(legacy_staleness, commands)
        self.assertNotIn("/old-home", once)
        self.assertEqual(events["PostToolUse"][-1], entry([formatting, mapping]))
        absolute = prefix + f'"{self.home_dir}/.claude/hooks/orchestrator-only.sh" format-edited-files.py'
        upgraded = self.merge(managed, json.dumps({"hooks": {"PostToolUse": [entry([absolute])]}}))
        self.assertEqual(json.loads(upgraded)["hooks"]["PostToolUse"], [entry([formatting, mapping])])

    def test_orchestrator_settings_keep_existing_policy(self):
        from tests.unit.test_generate_agent_configs import load_generator, load_manifest_fixture, render_claude_template

        module = load_generator()
        manifest = load_manifest_fixture(self.source_dir)
        policy = render_claude_template(module.render_claude_settings(manifest), self.source_dir)
        before = {
            "alwaysThinkingEnabled": True,
            "autoUpdates": False,
            "autoUpdatesChannel": "stable",
            "plansDirectory": "./.agents/worklog/claude",
            "disableSkillShellExecution": True,
            "includeGitInstructions": True,
            "statusLine": {"type": "command", "command": "ccstatusline"},
        }
        self.assertEqual({key: policy[key] for key in before}, before)
        self.assertEqual(policy["permissions"], manifest["claude"]["permissions"])
        self.assertEqual(policy["env"], manifest["claude"]["env"])
        self.assertTrue(policy["sandbox"]["failIfUnavailable"])
        self.assertIn("~/.cache/uv", policy["sandbox"]["filesystem"]["allowWrite"])
        for hook in all_hooks(policy):
            self.assertEqual(hook["onFailure"], "block")
            if hook["command"] != "~/.local/bin/common/permgate claude":
                self.assertTrue(hook["command"].startswith("/usr/bin/env -i PATH="))
        first = self.merge(policy, json.dumps({"unrelated": 1}))
        self.assertEqual(self.merge(policy, first), first)
        merged = json.loads(first)
        self.assertEqual(merged["unrelated"], 1)
        appended = [
            h
            for g in merged["hooks"]["SessionStart"]
            for h in g["hooks"]
            if h["command"].endswith('orchestrator-only.sh" herdr-agents')
        ]
        self.assertEqual(len(appended), 1)
        self.assertEqual(appended[0]["onFailure"], "block")


if __name__ == "__main__":
    unittest.main()
