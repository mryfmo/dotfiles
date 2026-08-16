#!/usr/bin/env python3
"""Exercise focused checks in validate-agent-assets.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate-agent-assets.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_agent_assets", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateAgentAssetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_validator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="validate-agent-assets-test-"))
        self.module.ROOT = self.temp_dir
        self.required_agmsg_writable_roots = sorted(self.module.REQUIRED_AGMSG_WRITABLE_ROOTS)
        (self.temp_dir / "home/dot_codex").mkdir(parents=True)
        (self.temp_dir / "home/.chezmoitemplates").mkdir(parents=True)

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def write_codex_config(self, sandbox_workspace_write: str) -> None:
        (self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml").write_text(
            "\n".join(
                [
                    "#:schema https://developers.openai.com/codex/config-schema.json",
                    'model = "gpt-5.5"',
                    'model_reasoning_effort = "high"',
                    'sandbox_mode = "workspace-write"',
                    "",
                    "[sandbox_workspace_write]",
                    sandbox_workspace_write,
                    "",
                    "[features]",
                    "plugins = true",
                    "hooks = true",
                    "plugin_hooks = true",
                    "",
                    "[shell_environment_policy]",
                    'inherit = "core"',
                    'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
                    "",
                ]
            )
        )

    def test_codex_modify_script_requires_executable_source(self) -> None:
        path = self.temp_dir / "home/dot_codex/modify_private_config.toml"
        path.write_text("RUNTIME_PREFIXES = ('hooks.state', 'marketplaces', 'tui.model_availability_nux', 'projects')\n")
        path.chmod(0o644)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_modify_script()

        path.chmod(0o755)
        self.module.validate_codex_modify_script()

    def write_agmsg_script(self, relative_path: str, executable: bool = True) -> None:
        path = self.temp_dir / "home/dot_agents/skills/agmsg/scripts" / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\n")
        path.chmod(0o755 if executable else 0o644)

    def write_text_file(self, relative_path: str, content: str) -> Path:
        path = self.temp_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def copy_managed_hook_sources(self) -> None:
        for relative_path, _file_type in self.module.HOOK_COMPOSITION_SOURCES.values():
            self.write_text_file(str(relative_path), (ROOT / relative_path).read_text())

    def update_json_hook_source(self, relative_path: str, event: str, groups: list[dict]) -> None:
        path = self.temp_dir / relative_path
        data = json.loads(path.read_text())
        data["hooks"][event] = groups
        path.write_text(json.dumps(data))

    def assert_hook_composition_fails(self, finding: str) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_hook_composition()
        self.assertIn(finding, stderr.getvalue())

    def write_valid_agent_manifest(self) -> dict:
        profiles = {
            name: {
                "claude": {"model": "claude-model", "effort": "high"},
                "codex": {"model": "codex-model", "model_reasoning_effort": "high"},
            }
            for name in ("express", "standard", "review", "deep", "security")
        }
        profiles["security"]["codex"]["model"] = "gpt-daybreak-blue-latest"
        manifest = {
            "schema_version": 1,
            "target_agents": ["codex", "claude"],
            "skills": {"canonical_dir": "~/.agents/skills"},
            "model_profiles": profiles,
            "interactive_profile": "deep",
            "claude": {},
            "codex": {"plugins": {"crit@mryfmo-personal-plugins": {"enabled": True}}},
            "mcp_servers": {},
        }
        self.module.load_yaml = lambda _path: manifest
        return manifest

    def write_pi_assets(
        self, *, trust: str | None = "never", version: str = "0.84.1"
    ) -> None:
        settings = {} if trust is None else {"defaultProjectTrust": trust}
        self.write_text_file(
            "home/dot_pi/agent/settings.json", json.dumps(settings)
        )
        (self.temp_dir / "home/dot_pi/agent/extensions").mkdir(parents=True)
        extension_source = ROOT / "home/dot_pi/agent/extensions/permgate.ts"
        if extension_source.exists():
            shutil.copy2(
                extension_source,
                self.temp_dir / "home/dot_pi/agent/extensions/permgate.ts",
            )
        self.write_text_file(
            "home/dot_mise/config.toml",
            '[tools]\n"npm:@earendil-works/pi-coding-agent" = '
            f'"{version}"\n',
        )

    def test_pi_assets_accept_deny_trust_and_exact_pin(self) -> None:
        self.write_pi_assets()

        self.module.validate_pi_assets()

    def test_pi_assets_reject_missing_default_project_trust(self) -> None:
        self.write_pi_assets(trust=None)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_pi_assets()

    def test_pi_assets_reject_version_range(self) -> None:
        self.write_text_file(
            "home/dot_mise/config.toml",
            '[tools]\n"npm:@earendil-works/pi-coding-agent" = "^0.84.1"\n',
        )

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_pi_assets()

    def test_pi_assets_reject_newer_exact_pin_during_cooldown(self) -> None:
        self.write_pi_assets(version="0.84.2")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_pi_assets()

    def test_pi_assets_accept_absent_deferred_pin(self) -> None:
        self.write_text_file("home/dot_mise/config.toml", "[tools]\n")

        self.module.validate_pi_assets()

    def test_pi_assets_accept_matching_permgate_extension_hash(self) -> None:
        self.write_pi_assets()
        extension_path = self.temp_dir / "home/dot_pi/agent/extensions/permgate.ts"
        self.assertTrue(extension_path.exists())

        self.module.validate_pi_assets()

    def test_pi_assets_reject_tampered_permgate_extension(self) -> None:
        self.write_pi_assets()
        extension_path = self.temp_dir / "home/dot_pi/agent/extensions/permgate.ts"
        self.assertTrue(extension_path.exists())
        extension_path.write_text(extension_path.read_text() + "// tampered\n")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_pi_assets()

    def test_agent_manifest_accepts_exact_security_profile_set(self) -> None:
        self.write_valid_agent_manifest()

        self.module.validate_agent_manifest()

    def test_agent_manifest_rejects_missing_security_profile(self) -> None:
        manifest = self.write_valid_agent_manifest()
        del manifest["model_profiles"]["security"]

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()

    def test_agent_manifest_rejects_wrong_security_codex_model(self) -> None:
        manifest = self.write_valid_agent_manifest()
        manifest["model_profiles"]["security"]["codex"]["model"] = "gpt-5.6-sol"

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()

    def test_hook_composition_accepts_managed_source_fixture(self) -> None:
        self.copy_managed_hook_sources()

        self.module.validate_hook_composition()

    def test_hook_composition_rejects_duplicate_command(self) -> None:
        self.copy_managed_hook_sources()
        duplicate = {"type": "command", "command": "audit-hook", "timeout": 5}
        self.update_json_hook_source(
            "home/.chezmoitemplates/claude-settings-managed.json",
            "Stop",
            [{"hooks": [duplicate, duplicate]}],
        )

        self.assert_hook_composition_fails("duplicate-command source=claude event=Stop")

    def test_hook_composition_requires_permgate_first(self) -> None:
        self.copy_managed_hook_sources()
        self.update_json_hook_source(
            "home/.chezmoitemplates/claude-settings-managed.json",
            "PermissionRequest",
            [
                {
                    "hooks": [
                        {"type": "command", "command": "audit-hook", "timeout": 5},
                        {"type": "command", "command": "permgate claude", "timeout": 10},
                    ]
                }
            ],
        )

        self.assert_hook_composition_fails("permgate-first source=claude event=PermissionRequest")

    def test_hook_composition_rejects_sync_timeout_over_budget(self) -> None:
        self.copy_managed_hook_sources()
        self.update_json_hook_source(
            "home/.chezmoitemplates/claude-settings-managed.json",
            "Stop",
            [
                {
                    "hooks": [
                        {"type": "command", "command": "first", "timeout": 20},
                        {"type": "command", "command": "second", "timeout": 11},
                    ]
                }
            ],
        )

        self.assert_hook_composition_fails("sync-timeout-budget source=claude event=Stop total=31s limit=30s")

    def test_hook_composition_pins_sessionstart_order(self) -> None:
        self.copy_managed_hook_sources()
        path = self.temp_dir / "vendor/compactiondb/.claude/settings.fragment.json"
        data = json.loads(path.read_text())
        data["hooks"]["SessionStart"].reverse()
        path.write_text(json.dumps(data))

        self.assert_hook_composition_fails("sessionstart-order source=compactiondb")

    def test_codex_sandbox_workspace_write_must_match_manifest(self) -> None:
        self.write_codex_config("network_access = false")
        manifest = {
            "model_profiles": {
                "standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}
            },
            "interactive_profile": "standard",
            "codex": {
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": self.required_agmsg_writable_roots,
                },
                "shell_environment_policy": {
                    "inherit": "core",
                    "set": {"PATH": "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin"},
                },
                "tui": {},
                "plugins": {},
                "marketplaces": {},
                "hooks": {},
                "projects": {},
            }
        }

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def test_codex_sandbox_workspace_write_accepts_matching_manifest(self) -> None:
        self.write_codex_config(
            "network_access = false\nwritable_roots = "
            f"{json.dumps(self.required_agmsg_writable_roots)}"
        )
        manifest = {
            "model_profiles": {
                "standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}
            },
            "interactive_profile": "standard",
            "codex": {
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": self.required_agmsg_writable_roots,
                },
                "shell_environment_policy": {
                    "inherit": "core",
                    "set": {"PATH": "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin"},
                },
                "tui": {},
                "plugins": {},
                "marketplaces": {},
                "hooks": {},
                "projects": {},
            }
        }

        self.module.validate_codex_config(manifest)

    def test_codex_sandbox_workspace_write_requires_all_agmsg_roots(self) -> None:
        roots = ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db"]
        self.write_codex_config("network_access = false\nwritable_roots = " + json.dumps(roots))
        manifest = {
            "model_profiles": {
                "standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}
            },
            "interactive_profile": "standard",
            "codex": {
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": roots,
                },
                "shell_environment_policy": {
                    "inherit": "core",
                    "set": {"PATH": "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin"},
                },
                "tui": {},
                "plugins": {},
                "marketplaces": {},
                "hooks": {},
                "projects": {},
            }
        }

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def test_agmsg_script_modes_accept_prefixed_entrypoints_and_lib_helpers(self) -> None:
        self.write_agmsg_script("executable_send.sh")
        self.write_agmsg_script("release/executable_sync-version.sh")
        self.write_agmsg_script("lib/storage.sh", executable=False)

        self.module.validate_agmsg_script_modes()

    def test_agmsg_script_modes_reject_unprefixed_direct_entrypoint(self) -> None:
        self.write_agmsg_script("send.sh")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agmsg_script_modes()

    def test_agmsg_script_modes_reject_non_executable_prefixed_entrypoint(self) -> None:
        self.write_agmsg_script("executable_send.sh", executable=False)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agmsg_script_modes()

    def test_secret_scan_checks_extensionless_executables(self) -> None:
        path = self.write_text_file("home/dot_local/bin/common/executable_leaky", "api_" + 'key = "real-secret"\n')
        path.chmod(0o755)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()

    def test_secret_scan_checks_docs_paths(self) -> None:
        self.write_text_file("docs/reference/leaky.md", "to" + 'ken = "real-secret"\n')

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()

    def test_secret_scan_allows_exact_placeholder_tokens(self) -> None:
        self.write_text_file(
            "docs/reference/placeholders.md",
            "to" + 'ken = "GITHUB_PERSONAL_ACCESS_TOKEN"\n'
            "to" + 'ken = "FIGMA_OAUTH_TOKEN"\n',
        )

        self.module.validate_no_obvious_secrets()

    def test_secret_scan_rejects_placeholder_with_suffix(self) -> None:
        self.write_text_file(
            "docs/reference/leaky-placeholder.md",
            "to" + 'ken = "GITHUB_PERSONAL_ACCESS_TOKEN' + '_REAL"\n',
        )

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()

    def test_secret_scan_checks_utf16_bom_text(self) -> None:
        path = self.temp_dir / "docs/reference/leaky-utf16.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(("to" + 'ken = "real-secret"\n').encode("utf-16"))

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()


    def write_manifest(self, hook_command: str) -> None:
        path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"claude:\n  hooks:\n    session_start: {hook_command}\n")

    def test_manifest_home_paths_reject_hard_coded_home(self) -> None:
        self.write_manifest("bash '/Users/mryfmo/.claude/hooks/state.sh' session")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_reject_hard_coded_linux_home(self) -> None:
        self.write_manifest("bash '/home/mryfmo/.claude/hooks/state.sh' session")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_allow_chezmoi_home_dir(self) -> None:
        self.write_manifest(
            "bash '{{ .chezmoi.homeDir }}/.claude/hooks/state.sh' session"
        )

        self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_allow_flow_style_projects(self) -> None:
        path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            'codex:\n  projects: {"/Users/mryfmo/Workspace/dotfiles": {"trust_level": "trusted"}}\n'
        )

        self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_exempt_runtime_owned_projects(self) -> None:
        path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "codex:\n"
            "  projects:\n"
            "    /Users/mryfmo/Workspace/dotfiles:\n"
            "      trust_level: trusted\n"
            "claude:\n"
            '  hooks:\n    session_start: bash "$HOME/.claude/hooks/state.sh" session\n'
        )

        self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_only_exempt_the_projects_subtree(self) -> None:
        path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "codex:\n"
            "  projects:\n"
            "    /Users/mryfmo/Workspace/dotfiles:\n"
            "      trust_level: trusted\n"
            "claude:\n"
            "  hooks:\n"
            "    session_start: bash '/Users/mryfmo/.claude/hooks/state.sh' session\n"
        )

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_reject_non_codex_projects_mapping(self) -> None:
        path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "claude:\n"
            "  projects:\n"
            "    /Users/mryfmo/Workspace/dotfiles:\n"
            "      trust_level: trusted\n"
        )

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_manifest_home_paths()

    AGMSG_COMMAND_TARGET = "dot_agents/skills/agmsg/templates/cmd.claude-code.md"

    def write_agmsg_command_symlink(
        self, target: str, create_target: bool = True
    ) -> None:
        path = self.temp_dir / "home/dot_claude/commands/symlink_agmsg.md.tmpl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(target)
        if create_target:
            template = self.temp_dir / "home" / self.AGMSG_COMMAND_TARGET
            template.parent.mkdir(parents=True, exist_ok=True)
            template.write_text("shared command template\n")

    def test_claude_command_parity_rejects_dangling_target(self) -> None:
        self.write_agmsg_command_symlink(
            "{{ .chezmoi.sourceDir }}/" + self.AGMSG_COMMAND_TARGET + "\n",
            create_target=False,
        )

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_claude_command_parity()

    def test_claude_command_parity_rejects_wrong_target(self) -> None:
        self.write_agmsg_command_symlink(
            "{{ .chezmoi.sourceDir }}/dot_claude/elsewhere.md\n"
        )

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_claude_command_parity()

    def test_claude_command_parity_rejects_restored_duplicate(self) -> None:
        self.write_agmsg_command_symlink(
            "{{ .chezmoi.sourceDir }}/dot_agents/skills/agmsg/templates/cmd.claude-code.md\n"
        )
        (self.temp_dir / "home/dot_claude/commands/agmsg.md").write_text("duplicate\n")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_claude_command_parity()

    def test_claude_command_parity_accepts_symlink_only(self) -> None:
        self.write_agmsg_command_symlink(
            "{{ .chezmoi.sourceDir }}/dot_agents/skills/agmsg/templates/cmd.claude-code.md\n"
        )

        self.module.validate_claude_command_parity()


if __name__ == "__main__":
    unittest.main()
