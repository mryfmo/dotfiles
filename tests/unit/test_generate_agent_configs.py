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


def sample_manifest() -> dict:
    return {
        "model_profiles": {
            "express": {
                "claude": {"model": "haiku", "effort": "low"},
                "codex": {"model": "gpt-5.6-luna", "model_reasoning_effort": "low"},
            },
            "standard": {
                "claude": {"model": "sonnet", "effort": "high"},
                "codex": {"model": "gpt-5.6-terra", "model_reasoning_effort": "medium"},
            },
        },
        "interactive_profile": "standard",
        "codex": {
            "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
            "model_reasoning_summary": "concise",
            "model_verbosity": "low",
            "personality": "pragmatic",
            "approval_policy": "on-request",
            "sandbox_mode": "workspace-write",
            "web_search": "cached",
            "check_for_update_on_startup": False,
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
            "schema": "https://json.schemastore.org/claude-code-settings.json",
            "alwaysThinkingEnabled": True,
            "autoUpdates": False,
            "autoUpdatesChannel": "stable",
            "plansDirectory": "./.agents/worklog/claude",
            "permissions": {"deny": [], "defaultMode": "plan", "ask": []},
            "hooks": {
                "enforce_uv_hook": "~/.claude/hooks/enforce-uv.sh",
                "format_edited_files_hook": "~/.claude/hooks/format-edited-files.py",
            },
            "statusLine": {},
            "disableSkillShellExecution": True,
            "includeGitInstructions": True,
            "enabledPlugins": {},
        },
        "plugins": {
            "marketplace_path": "home/dot_agents/plugins/marketplace.json",
            "marketplace": {"displayName": "Local", "name": "local"},
        },
        "mcp_servers": {},
    }


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
        source = (
            self.temp_dir / "home/dot_agents/skills/agmsg/scripts/executable_send.sh"
        )
        source.parent.mkdir(parents=True)
        source.write_text("#!/bin/sh\n")

        outputs = self.module.claude_skill_symlink_outputs()

        target = (
            self.temp_dir / "home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl"
        )
        self.assertEqual(
            outputs[target],
            "{{ .chezmoi.sourceDir }}/dot_agents/skills/agmsg/scripts/executable_send.sh\n",
        )
        self.assertNotIn(
            self.temp_dir
            / "home/dot_claude/skills/agmsg/scripts/symlink_executable_send.sh.tmpl",
            outputs,
        )

    def test_expected_outputs_uses_codex_baseline_path(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())

        codex_path = self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml"
        self.assertIn(codex_path, outputs)
        self.assertIn('model = "gpt-5.6-terra"', outputs[codex_path])
        self.assertIn('model_reasoning_effort = "medium"', outputs[codex_path])
        self.assertIn('model_reasoning_summary = "concise"', outputs[codex_path])
        self.assertIn('model_verbosity = "low"', outputs[codex_path])
        self.assertIn('personality = "pragmatic"', outputs[codex_path])
        self.assertIn("check_for_update_on_startup = false", outputs[codex_path])
        self.assertNotIn(
            self.temp_dir / "home/dot_codex/private_config.toml.tmpl", outputs
        )

    def test_expected_outputs_render_profile_artifacts(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())

        express_profile = self.temp_dir / "home/dot_codex/express.config.toml"
        self.assertIn('model = "gpt-5.6-luna"', outputs[express_profile])
        self.assertIn('model_reasoning_effort = "low"', outputs[express_profile])

        env_path = self.temp_dir / "home/dot_agents/model-profiles.env"
        self.assertIn('MODEL_PROFILE_INTERACTIVE="standard"', outputs[env_path])
        self.assertIn(
            'MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"', outputs[env_path]
        )
        self.assertIn(
            'MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"',
            outputs[env_path],
        )

        agent_path = self.temp_dir / "home/dot_claude/agents/express-explorer.md"
        self.assertIn("model: haiku", outputs[agent_path])
        self.assertIn("effort: low", outputs[agent_path])

        self.assertFalse([path for path in outputs if path.name == "ccgate.jsonnet"])

    def test_claude_settings_use_interactive_profile_without_permission_gate(
        self,
    ) -> None:
        settings = self.module.json.loads(
            self.module.render_claude_settings(sample_manifest())
        )

        self.assertEqual("sonnet", settings["model"])
        self.assertEqual("high", settings["effortLevel"])
        self.assertNotIn("[1m]", settings["model"])
        self.assertNotIn("PermissionRequest", settings["hooks"])

    def test_unknown_interactive_profile_fails(self) -> None:
        manifest = sample_manifest()
        manifest["interactive_profile"] = "missing"

        with self.assertRaises(SystemExit):
            self.module.interactive_profile(manifest)

    def test_model_profiles_reject_incomplete_or_unsafe_entries(self) -> None:
        missing_agent = sample_manifest()
        del missing_agent["model_profiles"]["standard"]["codex"]
        with self.assertRaises(SystemExit):
            self.module.model_profiles(missing_agent)

        unsafe_value = sample_manifest()
        unsafe_value["model_profiles"]["standard"]["claude"]["model"] = (
            "sonnet 5; rm -rf"
        )
        with self.assertRaises(SystemExit):
            self.module.model_profiles(unsafe_value)

        missing_express = sample_manifest()
        del missing_express["model_profiles"]["express"]
        with self.assertRaises(SystemExit):
            self.module.model_profiles(missing_express)

    def test_claude_settings_renders_session_start_hooks(self) -> None:
        manifest = sample_manifest()
        manifest["claude"]["hooks"]["session_start"] = [
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
        ]

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

    def test_claude_deny_rules_use_edit_for_file_mutations(self) -> None:
        manifest = (ROOT / "home/dot_agents/agent-config.yaml").read_text()

        self.assertIn("- Edit(.env*)", manifest)
        self.assertNotIn("- Write(.env*)", manifest)

    def test_manifest_keeps_model_ids_only_in_profiles(self) -> None:
        manifest = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        profiles_block = manifest.split("model_profiles:")[1].split("\ncodex:")[0]

        self.assertIn("interactive_profile:", profiles_block)
        for line in manifest.splitlines():
            if line.startswith(
                ("  model:", "  effortLevel:", "  model_reasoning_effort:")
            ):
                self.fail(
                    f"model settings must live in model_profiles only: {line.strip()}"
                )


if __name__ == "__main__":
    unittest.main()
