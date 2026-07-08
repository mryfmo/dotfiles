#!/usr/bin/env python3
"""Exercise focused checks in generate-agent-configs.py."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts/generate-agent-configs.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_agent_configs", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GenerateAgentConfigsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_generator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="generate-agent-configs-test-"))
        self.module.ROOT = self.temp_dir

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def test_claude_skill_symlink_outputs_strip_executable_target_prefix(self) -> None:
        source = self.temp_dir / "home/dot_agents/skills/agmsg/scripts/executable_send.sh"
        source.parent.mkdir(parents=True)
        source.write_text("#!/bin/sh\n")

        outputs = self.module.claude_skill_symlink_outputs()

        target = self.temp_dir / "home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl"
        self.assertEqual(
            outputs[target],
            "{{ .chezmoi.sourceDir }}/dot_agents/skills/agmsg/scripts/executable_send.sh\n",
        )
        self.assertNotIn(
            self.temp_dir / "home/dot_claude/skills/agmsg/scripts/symlink_executable_send.sh.tmpl",
            outputs,
        )

    def test_expected_outputs_uses_codex_baseline_path(self) -> None:
        manifest = {
            "codex": {
                "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
                "ccgate_config_path": "home/dot_codex/ccgate.jsonnet",
                "model": "gpt-5.5",
                "model_reasoning_effort": "high",
                "approval_policy": "on-request",
                "sandbox_mode": "workspace-write",
                "web_search": "cached",
                "project_doc_max_bytes": 65536,
                "project_doc_fallback_filenames": ["CLAUDE.md"],
                "tui": {},
                "sandbox_workspace_write": {"network_access": False},
                "shell_environment_policy": {},
                "features": {},
                "plugins": {},
                "marketplaces": {},
                "hooks": {},
                "projects": {},
            },
            "claude": {
                "settings_path": "home/.chezmoitemplates/claude-settings-managed.json",
                "mcp_config_path": "home/dot_claude/private_mcp.json.tmpl",
                "ccgate_config_path": "home/dot_claude/ccgate.jsonnet",
                "schema": "https://json.schemastore.org/claude-code-settings.json",
                "model": "claude-fable-5[1m]",
                "effortLevel": "high",
                "alwaysThinkingEnabled": True,
                "autoUpdates": False,
                "autoUpdatesChannel": "stable",
                "plansDirectory": "./.agents/worklog/claude",
                "permissions": {"deny": [], "defaultMode": "plan", "ask": []},
                "hooks": {
                    "ccgate_permission_request_hook": "ccgate claude",
                    "enforce_uv_hook": "~/.claude/hooks/enforce-uv.sh",
                    "format_edited_files_hook": "~/.claude/hooks/format-edited-files.py",
                },
                "statusLine": {},
                "disableSkillShellExecution": True,
                "includeGitInstructions": True,
                "enabledPlugins": {},
            },
            "plugins": {"marketplace_path": "home/dot_agents/plugins/marketplace.json", "marketplace": {"displayName": "Local", "name": "local"}},
            "mcp_servers": {},
        }

        outputs = self.module.expected_outputs(manifest)

        self.assertIn(self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml", outputs)
        self.assertNotIn(self.temp_dir / "home/dot_codex/private_config.toml.tmpl", outputs)

    def test_claude_settings_renders_session_start_hooks(self) -> None:
        manifest = {
            "claude": {
                "schema": "https://json.schemastore.org/claude-code-settings.json",
                "model": "claude-fable-5[1m]",
                "effortLevel": "high",
                "alwaysThinkingEnabled": True,
                "autoUpdates": False,
                "autoUpdatesChannel": "stable",
                "plansDirectory": "./.agents/worklog/claude",
                "permissions": {"deny": [], "defaultMode": "plan", "ask": []},
                "hooks": {
                    "ccgate_permission_request_hook": "ccgate claude",
                    "enforce_uv_hook": "~/.claude/hooks/enforce-uv.sh",
                    "format_edited_files_hook": "~/.claude/hooks/format-edited-files.py",
                    "session_start": [
                        {
                            "matcher": "*",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "bash '/Users/mryfmo/.claude/hooks/herdr-agent-state.sh' session",
                                    "timeout": 10,
                                }
                            ],
                        }
                    ],
                },
                "statusLine": {},
                "disableSkillShellExecution": True,
                "includeGitInstructions": True,
                "enabledPlugins": {},
            }
        }

        settings = self.module.json.loads(self.module.render_claude_settings(manifest))

        self.assertEqual(
            settings["hooks"]["SessionStart"],
            [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "bash '/Users/mryfmo/.claude/hooks/herdr-agent-state.sh' session",
                            "timeout": 10,
                        }
                    ],
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
