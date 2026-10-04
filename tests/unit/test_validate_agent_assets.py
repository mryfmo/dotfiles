#!/usr/bin/env python3
"""Exercise focused checks in validate-agent-assets.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import time
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

    def test_recursive_scans_skip_nested_git_trees_only(self) -> None:
        (self.temp_dir / ".git").mkdir()
        cases = (
            ("validate_no_removed_claude_skill", "high-impact" + "-journal-publishing"),
            ("validate_no_obvious_secrets", "ghp_" + "x" * 25),
        )
        for marker_kind in ("file", "directory"):
            for scan_name, token in cases:
                with self.subTest(marker_kind=marker_kind, scan=scan_name):
                    nested = self.temp_dir / marker_kind / scan_name
                    nested.mkdir(parents=True)
                    marker = nested / ".git"
                    if marker_kind == "file":
                        marker.write_text("gitdir: /unused/worktree-metadata\n")
                    else:
                        marker.mkdir()
                    deep_file = nested / "deep" / "nested.txt"
                    deep_file.parent.mkdir()
                    deep_file.write_text(token)
                    scan = getattr(self.module, scan_name)
                    with contextlib.redirect_stderr(io.StringIO()):
                        scan()
                    top_file = self.temp_dir / "top.txt"
                    top_file.write_text(token)
                    try:
                        stderr = io.StringIO()
                        with (
                            contextlib.redirect_stderr(stderr),
                            self.assertRaises(SystemExit),
                        ):
                            scan()
                        self.assertIn("top.txt", stderr.getvalue())
                        self.assertNotIn("nested.txt", stderr.getvalue())
                    finally:
                        top_file.unlink()

    def write_codex_config(self, sandbox_workspace_write: str, projects_toml: str = "") -> None:
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
                    projects_toml,
                ]
            )
        )

    def write_repo_claude_settings(self, command: str) -> None:
        (self.temp_dir / ".claude").mkdir(parents=True, exist_ok=True)
        (self.temp_dir / ".claude/settings.json").write_text(
            json.dumps(
                {
                    "hooks": {
                        "SessionEnd": [
                            {
                                "matcher": "*",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": command,
                                        "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"],
                                    }
                                ],
                            }
                        ]
                    }
                }
            )
        )

    def test_repo_claude_settings_reject_machine_specific_interpreter(self) -> None:
        self.write_repo_claude_settings("/Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14")
        with self.assertRaises(SystemExit):
            self.module.validate_repo_claude_settings_portable()

    def test_repo_claude_settings_accept_portable_interpreter(self) -> None:
        self.write_repo_claude_settings("python3")
        self.module.validate_repo_claude_settings_portable()

    def test_codex_modify_script_requires_executable_source(self) -> None:
        path = self.temp_dir / "home/dot_codex/modify_private_config.toml"
        path.write_text(
            "RUNTIME_PREFIXES = ('hooks.state', 'marketplaces', 'tui.model_availability_nux', 'projects')\n"
        )
        path.chmod(0o644)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_modify_script()

        path.chmod(0o755)
        self.module.validate_codex_modify_script()

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
            for name in ("express", "standard", "review", "deep", "security", "audit")
        }
        profiles["security"]["codex"]["model"] = "gpt-6-astra"
        profiles["audit"]["codex"].update(model="gpt-6.1-sol", model_reasoning_effort="xhigh", sandbox_mode="read-only")
        profiles["standard"]["claude"]["advisor"] = "fable"
        manifest = {
            "schema_version": 1,
            "target_agents": ["codex", "claude"],
            "skills": {"canonical_dir": "~/.agents/skills"},
            "model_profiles": profiles,
            "interactive_profile": "deep",
            "worker_kind": "claude",
            "worker_profile": "standard",
            "claude": {},
            "codex": {"plugins": {"crit@mryfmo-personal-plugins": {"enabled": True}}},
            "mcp_servers": {},
        }
        self.module.load_yaml = lambda _path: manifest
        self.write_text_file(
            "README.md",
            "worker kind (currently `claude`; codex)\nherdr-agents --restart-worker\n",
        )
        return manifest

    def test_agent_manifest_accepts_exact_security_profile_set(self) -> None:
        self.write_valid_agent_manifest()

        self.module.validate_agent_manifest()

    def test_agent_manifest_rejects_invalid_or_missing_worker_kind(self) -> None:
        for value in ("banana", None):
            with self.subTest(worker_kind=value):
                manifest = self.write_valid_agent_manifest()
                manifest["worker_kind"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn("worker_kind must be codex or claude", stderr.getvalue())

    def test_agent_manifest_accepts_a_worker_worktree_under_claude_worktrees(self) -> None:
        manifest = self.write_valid_agent_manifest()
        manifest["worker_worktree"] = ".claude/worktrees/worker-c"

        self.module.validate_agent_manifest()

    def test_agent_manifest_rejects_a_worker_worktree_outside_claude_worktrees(self) -> None:
        for value in ("worker-c", "/abs/.claude/worktrees/x", ".claude/worktrees/..", ".claude/worktrees/a/b", 3):
            with self.subTest(worker_worktree=value):
                manifest = self.write_valid_agent_manifest()
                manifest["worker_worktree"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn("worker_worktree must be a relative path under .claude/worktrees/", stderr.getvalue())

    def test_agent_manifest_rejects_unknown_worker_profile(self) -> None:
        manifest = self.write_valid_agent_manifest()
        manifest["worker_profile"] = "banana"
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()
        self.assertIn(
            "worker_profile must name a defined model profile: 'banana'",
            stderr.getvalue(),
        )

    def test_agent_manifest_requires_fable_advisor_on_the_worker_profile(self) -> None:
        for advisor in (None, "opus"):
            with self.subTest(advisor=advisor):
                manifest = self.write_valid_agent_manifest()
                claude = manifest["model_profiles"]["standard"]["claude"]
                if advisor is None:
                    del claude["advisor"]
                else:
                    claude["advisor"] = advisor
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn(
                    "worker profile 'standard' must set claude.advisor: fable",
                    stderr.getvalue(),
                )

    def test_agent_manifest_requires_readme_to_state_the_worker_kind(self) -> None:
        manifest = self.write_valid_agent_manifest()
        manifest["worker_kind"] = "codex"
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()
        self.assertIn("(currently `codex`;", stderr.getvalue())

    def test_agent_manifest_requires_readme_to_document_restart_worker(self) -> None:
        self.write_valid_agent_manifest()
        self.write_text_file("README.md", "worker kind (currently `claude`; codex)\n")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()
        self.assertIn("README.md must document herdr-agents --restart-worker", stderr.getvalue())

    def asset_manifest(self) -> dict:
        return {
            "assets": {
                "mise": {
                    "source": "github-release",
                    "upstream": "jdx/mise",
                    "pin": "v1",
                    "verify": "release-shasums",
                    "install_path": "~/.local/bin/mise",
                    "installer": "install/common/mise.sh",
                    "render": {
                        "file": "install/common/mise.sh",
                        "constants": {"MISE_VERSION": "pin"},
                    },
                },
                "brew": {
                    "source": "git-commit",
                    "upstream": "Homebrew/install",
                    "pin": "abc",
                    "verify": "sha256",
                    "sha256": "def",
                    "install_path": "/opt/homebrew",
                    "installer": "install/macos/common/brew.sh",
                },
                "aws": {
                    "source": "https-download",
                    "upstream": "https://awscli.amazonaws.com",
                    "pin": "2",
                    "verify": "gpg",
                    "gpg_fingerprint": "FB5D",
                    "install_path": "~/.local/share/aws-cli",
                    "installer": "install/ubuntu/common/aws_cli.sh",
                },
                "plugins": {
                    "source": "claude-plugin",
                    "upstream": "marketplaces",
                    "pin": "per-plugin",
                    "verify": "none",
                    "plugins": {"crit": {"marketplace": "tomasz-tomczyk/crit", "pin": "1.8.10"}},
                },
                "agmsg": {
                    "source": "agmsg-installer",
                    "upstream": "https://github.com/fujibee/agmsg",
                    "pin": "1.5.0",
                    "ref": "v1.5.0",
                    "ref_commit": "c487be269c1973aeb01ca831806eb3f65ff3366d",
                    "verify": "sha256",
                    "sha256": "9201cb5ff23ddd9ddaa19ff821dce0d0f2d58c6c292aade252a8d824b3dfc059",
                    "bootstrap_integrity": "sha512-n6057L93AE+tnItTkBnClv3QvgsOlI6AO1SwodvKFJvqqTJqITHg/2O6jjHZZfh0nKbq49VKQv6F3t2d/62gyg==",
                    "install_path": "~/.agents/skills/agmsg",
                    "installer": "scripts/update-agent-assets.sh#update_agmsg",
                },
            }
        }

    def test_assets_accept_complete_declarations_and_rendered_versions(self) -> None:
        self.write_text_file("install/common/mise.sh", 'readonly MISE_VERSION="v1"\n')

        self.module.validate_assets(self.asset_manifest())

    def test_assets_reject_each_incomplete_declaration(self) -> None:
        cases = {
            "missing pin": lambda assets: assets["mise"].pop("pin"),
            "unknown source": lambda assets: assets["mise"].update(source="ftp"),
            "verify not valid for source": lambda assets: assets["brew"].update(verify="gpg"),
            "missing sha256": lambda assets: assets["brew"].pop("sha256"),
            "missing gpg fingerprint": lambda assets: assets["aws"].pop("gpg_fingerprint"),
            "missing install_path": lambda assets: assets["brew"].pop("install_path"),
            "missing installer": lambda assets: assets["aws"].pop("installer"),
            "float pin": lambda assets: assets["aws"].update(pin=1.1),
            "float plugin pin": lambda assets: assets["plugins"]["plugins"]["crit"].update(pin=1.1),
            "agmsg missing installer": lambda assets: assets["agmsg"].pop("installer"),
        }
        for name, breaks in cases.items():
            with self.subTest(case=name):
                manifest = self.asset_manifest()
                breaks(manifest["assets"])
                with (
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit),
                ):
                    self.module.validate_assets(manifest)

    def assert_agmsg_asset_rejected(self, **changes: object) -> str:
        manifest = self.asset_manifest()
        for key, value in changes.items():
            if value is None:
                manifest["assets"]["agmsg"].pop(key)
            else:
                manifest["assets"]["agmsg"][key] = value
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_assets(manifest)
        return stderr.getvalue()

    def test_agmsg_installer_requires_a_release_pin_and_its_tag(self) -> None:
        for changes, message in (
            ({"pin": "c487be269c1973aeb01ca831806eb3f65ff3366d"}, "must be an upstream release"),
            ({"ref": None}, "must be the release tag v1.5.0"),
            ({"ref": "v1.4.2"}, "must be the release tag v1.5.0"),
        ):
            with self.subTest(changes=changes):
                self.assertIn(message, self.assert_agmsg_asset_rejected(**changes))

    def test_agmsg_installer_requires_the_full_tag_commit(self) -> None:
        for changes in ({"ref_commit": None}, {"ref_commit": "c487be2"}):
            with self.subTest(changes=changes):
                self.assertIn("ref_commit", self.assert_agmsg_asset_rejected(**changes))

    def test_agmsg_installer_requires_the_npm_bootstrap_integrity(self) -> None:
        for changes in (
            {"bootstrap_integrity": None},
            {"bootstrap_integrity": "sha256-not-an-npm-integrity-string"},
        ):
            with self.subTest(changes=changes):
                self.assertIn("bootstrap_integrity", self.assert_agmsg_asset_rejected(**changes))

    def write_agmsg_installer_layout(self) -> None:
        self.write_text_file("home/.chezmoiremove", ".claude/skills/agmsg/**\n")

    def assert_agmsg_ownership_rejected(self, message: str) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_agmsg_is_installer_owned()
        self.assertIn(message, stderr.getvalue())

    def test_agmsg_ownership_accepts_the_installer_layout(self) -> None:
        self.write_agmsg_installer_layout()
        self.write_text_file("home/dot_claude/commands/other.md", "other\n")

        self.module.validate_agmsg_is_installer_owned()

    def test_agmsg_ownership_rejects_a_vendored_skill_copy(self) -> None:
        for vendored in (
            "home/dot_agents/skills/agmsg",
            "home/dot_claude/skills/agmsg",
            "home/private_dot_agents/skills/exact_agmsg",
        ):
            with self.subTest(vendored=vendored):
                self.write_agmsg_installer_layout()
                self.write_text_file(f"{vendored}/SKILL.md", "vendored\n")
                self.assert_agmsg_ownership_rejected(f"{vendored} must not exist")
                shutil.rmtree(self.temp_dir / vendored)

    def test_agmsg_ownership_rejects_a_managed_claude_command(self) -> None:
        for name in ("symlink_agmsg.md.tmpl", "agmsg.md"):
            with self.subTest(name=name):
                self.write_agmsg_installer_layout()
                path = f"home/dot_claude/commands/{name}"
                self.write_text_file(path, "managed\n")
                self.assert_agmsg_ownership_rejected(f"{path} must not exist")
                (self.temp_dir / path).unlink()

    def test_agmsg_ownership_requires_retiring_the_symlink_farm(self) -> None:
        self.write_text_file("home/.chezmoiremove", ".codex/ccgate.jsonnet\n")

        self.assert_agmsg_ownership_rejected("must retire .claude/skills/agmsg/**")

    def test_agmsg_ownership_rejects_removing_installer_owned_paths(self) -> None:
        for pattern in (
            ".agents/skills/agmsg",
            ".agents/skills/agmsg/**",
            ".agents/skills/agmsg/.agmsg",
            ".agents/skills/agmsg/VERSION",
            ".claude/commands/agmsg.md",
        ):
            with self.subTest(pattern=pattern):
                self.write_text_file("home/.chezmoiremove", f".claude/skills/agmsg/**\n{pattern}\n")
                self.assert_agmsg_ownership_rejected(f"entry {pattern!r} would remove")

    def test_assets_reject_unrendered_literal_versions_anywhere_in_install_or_scripts(
        self,
    ) -> None:
        cases = (
            (
                "install/ubuntu/common/tool.sh",
                'readonly TOOL_VERSION="1.2.3"\n',
                "TOOL_VERSION",
            ),
            (
                "install/ubuntu/common/copy.sh",
                'readonly MISE_VERSION="v0"\n',
                "MISE_VERSION",
            ),
            ("scripts/lib/other.sh", 'OTHER_VERSION="2"\n', "OTHER_VERSION"),
            ("scripts/tool.sh", '    local version="3.0"\n', "version"),
            (
                "install/ubuntu/common/bare.sh",
                "readonly TOOL_VERSION=1.2.3\n",
                "TOOL_VERSION",
            ),
            (
                "install/ubuntu/common/single.sh",
                "TOOL_VERSION='1.2.3'; export TOOL_VERSION\n",
                "TOOL_VERSION",
            ),
        )
        for relative, content, constant in cases:
            with self.subTest(file=relative):
                path = self.write_text_file(relative, content)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_assets(self.asset_manifest())
                self.assertIn(f"{relative} hard-codes {constant}", stderr.getvalue())
                path.unlink()

        for derived in (
            'readonly TOOL_VERSION="${MISE_VERSION}"\n',
            "TOOL_VERSION=${MISE_VERSION}\n",
            'version="$(tool --version)"\n',
            "local version\n",
        ):
            self.write_text_file("install/ubuntu/common/tool.sh", derived)
            self.module.validate_assets(self.asset_manifest())

    def test_permgate_policy_requires_a_schema_3_object(self) -> None:
        policy_path = self.temp_dir / "permgate-policy.yaml"
        policy_path.write_text('{"schema_version": 3, "allow_patterns": [], "deny_patterns": []}\n')
        self.module.validate_permgate_policy(policy_path)

        for label, text, message in (
            ("array", '["schema_version", "allow_patterns", "deny_patterns"]', "must be a JSON object"),
            ("old schema", '{"schema_version": 2, "allow_patterns": [], "deny_patterns": []}', "schema_version 3"),
            (
                "extra key",
                '{"schema_version": 3, "allow_patterns": [], "deny_patterns": [], "providers": {}}',
                "must hold only",
            ),
            (
                "null allow entry",
                '{"schema_version": 3, "allow_patterns": [null], "deny_patterns": []}',
                "allow_patterns must be a list of objects",
            ),
            (
                "deny not a list",
                '{"schema_version": 3, "allow_patterns": [], "deny_patterns": {}}',
                "deny_patterns must be a list of objects",
            ),
        ):
            with self.subTest(label):
                policy_path.write_text(text + "\n")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_permgate_policy(policy_path)
                self.assertIn(str(policy_path), stderr.getvalue())
                self.assertIn(message, stderr.getvalue())

    def test_agent_manifest_rejects_missing_security_profile(self) -> None:
        manifest = self.write_valid_agent_manifest()
        del manifest["model_profiles"]["security"]

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()

    def test_agent_manifest_rejects_wrong_security_codex_model(self) -> None:
        for key, value in (
            ("model", "gpt-5.6-sol"),
            ("model", "gpt-daybreak-blue-latest"),
            ("model_reasoning_effort", "medium"),
        ):
            with self.subTest(key=key, value=value):
                manifest = self.write_valid_agent_manifest()
                manifest["model_profiles"]["security"]["codex"][key] = value

                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn(f"security profile must set codex.{key}", stderr.getvalue())

    def test_agent_manifest_rejects_missing_audit_profile(self) -> None:
        manifest = self.write_valid_agent_manifest()
        del manifest["model_profiles"]["audit"]

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()
        self.assertIn("must define the six base profiles", stderr.getvalue())

    def test_agent_manifest_pins_the_audit_codex_profile(self) -> None:
        for key, wrong in (
            ("model", "gpt-5.6-sol"),
            ("model", "gpt-6-astra"),
            ("model", "gpt-6-sol"),
            ("model_reasoning_effort", "medium"),
            ("model_reasoning_effort", "high"),
            ("sandbox_mode", "workspace-write"),
            ("sandbox_mode", None),
        ):
            with self.subTest(key=key, value=wrong):
                manifest = self.write_valid_agent_manifest()
                codex = manifest["model_profiles"]["audit"]["codex"]
                if wrong is None:
                    del codex[key]
                else:
                    codex[key] = wrong
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn(f"audit profile must set codex.{key}:", stderr.getvalue())

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
                        {
                            "type": "command",
                            "command": "permgate claude",
                            "timeout": 10,
                        },
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

    def valid_claude_sandbox(self) -> dict:
        return {
            "enabled": True,
            "failIfUnavailable": False,
            "autoAllowBashIfSandboxed": True,
            "filesystem": {"allowWrite": list(self.required_agmsg_writable_roots)},
            "network": {
                "allowedDomains": ["github.com", "api.github.com"],
                "allowUnixSockets": ["~/.config/herdr/herdr.sock", "/run/user/1000/x.sock"],
            },
        }

    def test_claude_sandbox_accepts_manifest_symmetric_settings(self) -> None:
        self.module.validate_claude_sandbox(self.valid_claude_sandbox(), self.required_agmsg_writable_roots, "sandbox")

    def test_claude_sandbox_rejects_each_broken_rule(self) -> None:
        def disabled(sandbox: dict, key: str) -> None:
            sandbox[key] = False

        cases = {
            "enabled": lambda sandbox: disabled(sandbox, "enabled"),
            "failIfUnavailable": lambda sandbox: sandbox.pop("failIfUnavailable"),
            "autoAllowBashIfSandboxed": lambda sandbox: disabled(sandbox, "autoAllowBashIfSandboxed"),
            "missing Codex writable root": lambda sandbox: sandbox["filesystem"]["allowWrite"].pop(),
            "empty allowedDomains": lambda sandbox: sandbox["network"].update(allowedDomains=[]),
            "scheme in allowedDomains": lambda sandbox: sandbox["network"]["allowedDomains"].append(
                "https://github.com"
            ),
            "path in allowedDomains": lambda sandbox: sandbox["network"]["allowedDomains"].append("github.com/mryfmo"),
        }
        for name, breaks in cases.items():
            with self.subTest(rule=name):
                sandbox = self.valid_claude_sandbox()
                breaks(sandbox)
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.required_agmsg_writable_roots, "sandbox")

    def test_claude_permissions_allow_must_list_non_empty_rules(self) -> None:
        for permissions in ({}, {"allow": []}, {"allow": ["Bash(agmsg-dispatch:*)"]}):
            with self.subTest(accepts=permissions):
                self.module.validate_claude_permissions_allow(permissions, "permissions")
        for allow in ("Bash(agmsg-dispatch:*)", [""], [3]):
            with (
                self.subTest(rejects=allow),
                contextlib.redirect_stderr(io.StringIO()) as stderr,
                self.assertRaises(SystemExit),
            ):
                self.module.validate_claude_permissions_allow({"allow": allow}, "permissions")
            self.assertIn("permissions.allow must be a list", stderr.getvalue())

    def test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs(self) -> None:
        sandbox = self.valid_claude_sandbox()
        sandbox["filesystem"]["allowWrite"].append("~/.cache/uv")
        self.module.validate_claude_sandbox(sandbox, self.required_agmsg_writable_roots, "sandbox")
        for path in ("relative/cache", "~cache", "/tmp/*", 7):
            with self.subTest(path=path):
                sandbox = self.valid_claude_sandbox()
                sandbox["filesystem"]["allowWrite"].append(path)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.required_agmsg_writable_roots, "sandbox")
                self.assertIn("allowWrite extra entries must be absolute or ~/ paths", stderr.getvalue())

    def test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs(self) -> None:
        for socket in (
            "relative/herdr.sock",
            "./herdr.sock",
            "~herdr.sock",
            "/run/user/*/cc.sock",
            "~/.config/herdr/{a,b}.sock",
            7,
        ):
            with self.subTest(socket=socket):
                sandbox = self.valid_claude_sandbox()
                sandbox["network"]["allowUnixSockets"].append(socket)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.required_agmsg_writable_roots, "sandbox")
                self.assertIn("allowUnixSockets entries must be absolute or ~/ paths", stderr.getvalue())

    def test_claude_sandbox_requires_extra_codex_writable_roots(self) -> None:
        roots = [*self.required_agmsg_writable_roots, "/extra/codex/root"]
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_claude_sandbox(self.valid_claude_sandbox(), roots, "sandbox")

    def test_codex_sandbox_workspace_write_must_match_manifest(self) -> None:
        self.write_codex_config("network_access = false")
        manifest = {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
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
            },
        }

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def test_codex_sandbox_workspace_write_accepts_matching_manifest(self) -> None:
        self.write_codex_config(
            f"network_access = false\nwritable_roots = {json.dumps(self.required_agmsg_writable_roots)}"
        )
        manifest = {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
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
            },
        }

        self.module.validate_codex_config(manifest)

    def test_codex_sandbox_workspace_write_requires_all_agmsg_roots(self) -> None:
        roots = ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db"]
        self.write_codex_config("network_access = false\nwritable_roots = " + json.dumps(roots))
        manifest = {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
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
            },
        }

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def codex_config_manifest(self, projects: dict) -> dict:
        return {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
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
                "projects": projects,
            },
        }

    def write_codex_config_with_projects(self, projects_toml: str) -> None:
        self.write_codex_config(
            f"network_access = false\nwritable_roots = {json.dumps(self.required_agmsg_writable_roots)}",
            projects_toml=projects_toml,
        )

    def test_codex_projects_reject_hard_coded_macos_home(self) -> None:
        self.write_codex_config_with_projects(
            '[projects."/Users/mryfmo/Workspace/dotfiles"]\ntrust_level = "trusted"\n'
        )
        manifest = self.codex_config_manifest({"/Users/mryfmo/Workspace/dotfiles": {"trust_level": "trusted"}})

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def test_codex_projects_reject_missing_working_tree_placeholder(self) -> None:
        self.write_codex_config_with_projects('[projects."/repo"]\ntrust_level = "trusted"\n')
        manifest = self.codex_config_manifest({"/repo": {"trust_level": "trusted"}})

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def test_codex_projects_accept_working_tree_placeholder(self) -> None:
        self.write_codex_config_with_projects('[projects."{{ .chezmoi.workingTree }}"]\ntrust_level = "trusted"\n')
        manifest = self.codex_config_manifest({"{{ .chezmoi.workingTree }}": {"trust_level": "trusted"}})

        self.module.validate_codex_config(manifest)

    def test_secret_scan_checks_extensionless_executables(self) -> None:
        path = self.write_text_file(
            "home/dot_local/bin/common/executable_leaky",
            "api_" + 'key = "real-secret"\n',
        )
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
            "to" + 'ken = "GITHUB_PERSONAL_ACCESS_TOKEN"\nto' + 'ken = "FIGMA_OAUTH_TOKEN"\n',
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
        self.write_manifest("bash '{{ .chezmoi.homeDir }}/.claude/hooks/state.sh' session")

        self.module.validate_manifest_home_paths()

    def test_manifest_home_paths_allow_flow_style_projects(self) -> None:
        path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('codex:\n  projects: {"/Users/mryfmo/Workspace/dotfiles": {"trust_level": "trusted"}}\n')

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
        path.write_text("claude:\n  projects:\n    /Users/mryfmo/Workspace/dotfiles:\n      trust_level: trusted\n")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_manifest_home_paths()


# Built at runtime so this test file never contains a literal SECRET_PATTERN match.
FIELD = "tok" + "en"


class SecretPatternBoundaryTest(unittest.TestCase):
    """Key prefixes match only at a word boundary, so hyphenated slugs stay clean."""

    def test_a_key_prefix_inside_a_hyphenated_word_is_clean(self) -> None:
        pattern = load_validator().SECRET_PATTERN
        for text in (
            "dotfiles-T67-audit-task-level-a01-review-receipt.md",
            "the dotfiles-T75-shell-dead-code-a01 report",
        ):
            with self.subTest(text=text):
                self.assertIsNone(pattern.search(text))

    def test_a_real_key_prefix_is_still_flagged(self) -> None:
        pattern = load_validator().SECRET_PATTERN
        openai, github = "s" + "k-" + "a1" * 12, "gh" + "p_" + "a1" * 12
        for text in (f"x {openai}", f'"{openai}"', openai, f"KEY={openai}", f"x {github}"):
            with self.subTest(text=text):
                self.assertIsNotNone(pattern.search(text))

    def test_a_key_after_json_escaped_whitespace_is_flagged(self) -> None:
        # Audit evidence holds JSON-encoded transcripts: the character before the
        # key is then the n/r/t of an escape sequence, a word character.
        pattern = load_validator().SECRET_PATTERN
        keys = ("s" + "k-" + "a1" * 12, "gh" + "p_" + "a1" * 12, "github" + "_pat_" + "a1" * 12)
        for key in keys:
            for text in (json.dumps({"m": "\n" + key}), json.dumps({"m": "\t" + key}), json.dumps({"m": "\r" + key})):
                with self.subTest(text=text):
                    self.assertIsNotNone(pattern.search(text))
            # Any escape sequence (a backslash, then up to nine letters or digits)
            # right before the key: JSON \uXXXX, \b, \f, TOML \UXXXXXXXX, YAML \x, \0.
            escapes = ("\\u000a", "\\u000d", "\\u0009", "\\u0020", "\\b", "\\f", "\\U0000000A", "\\x0a", "\\0")
            for escape in escapes:
                text = '{"m": "' + escape + key + '"}'
                with self.subTest(text=text):
                    self.assertIsNotNone(pattern.search(text))

    def test_an_sk_key_body_needs_a_hyphen_free_run(self) -> None:
        pattern = load_validator().SECRET_PATTERN
        bare, project = "s" + "k-" + "a1" * 12, "s" + "k-" + "proj-" + "a1" * 12
        for text in (f"x {bare}", f"x {project}", json.dumps({"m": "\n" + project})):
            with self.subTest(text=text):
                self.assertIsNotNone(pattern.search(text))
        slug = "dotfiles-T91-secret-scan-" + "s" + "k-boundary-a01"
        for text in (f"{slug}-audit-1845139e.md", f"{slug}-pr-feedback.json", f"{slug}-review-receipt.md"):
            with self.subTest(text=text):
                self.assertIsNone(pattern.search(text))

    def test_a_long_hyphenated_run_scans_in_linear_time(self) -> None:
        pattern = load_validator().SECRET_PATTERN
        text = "-s" + "k-a" * 1 + ("-s" + "k-a") * (64 * 1024 // 5)
        started = time.monotonic()
        self.assertIsNone(pattern.search(text))
        self.assertLess(time.monotonic() - started, 1.0)

    def test_masking_keeps_the_escape_before_the_key(self) -> None:
        module = load_validator()
        key = "s" + "k-" + "a1" * 12
        for escape in ("\\n", "\\u000a", "\\U0000000A"):
            text = '{"m": "x' + escape + key + '"}'
            with self.subTest(escape=escape):
                masked, count = module.mask_secret_matches(text)
                self.assertEqual(count, 1)
                self.assertEqual(masked, '{"m": "x' + escape + module.SECRET_MASK + '"}')
                self.assertNotIn(key, masked)
                if escape != "\\U0000000A":  # \U is a TOML escape, not JSON.
                    json.loads(masked)


class MaskSecretsModeTest(unittest.TestCase):
    """`--mask-secrets` rewrites SECRET_PATTERN matches in place (audit evidence)."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="mask-secrets-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def run_mask(self, *paths: Path) -> "subprocess.CompletedProcess[str]":
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--mask-secrets", *map(str, paths)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_masks_every_match_in_place_and_reports_counts(self) -> None:
        evidence = self.temp_dir / "audit.md"
        evidence.write_text(
            f'schema:\n  design_{FIELD}: "abcdefgh"\n  applies_{FIELD}: "xyz"\nprose line stays\nVerdict: correct\n'
        )
        last = self.temp_dir / "audit.md.last.md"
        last.write_text("No findings.\nVerdict: correct\n")

        result = self.run_mask(evidence, last)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            result.stdout,
            f"masked 2 match(es) in {evidence}\nmasked 0 match(es) in {last}\n",
        )
        text = evidence.read_text()
        self.assertEqual(
            text,
            "schema:\n  design_<redacted:secret-pattern>\n  applies_<redacted:secret-pattern>\n"
            "prose line stays\n"
            "Verdict: correct\n",
        )
        self.assertEqual(last.read_text(), "No findings.\nVerdict: correct\n")
        module = load_validator()
        self.assertIsNone(module.SECRET_PATTERN.search(text))

    def test_leaves_allowed_placeholders_the_scan_accepts(self) -> None:
        evidence = self.temp_dir / "audit.md"
        placeholder = "GITHUB_PERSONAL_ACCESS_" + FIELD.upper()
        original = f'{placeholder}: "${{{placeholder}}}"\n'
        evidence.write_text(original)

        result = self.run_mask(evidence)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, f"masked 0 match(es) in {evidence}\n")
        self.assertEqual(evidence.read_text(), original)

    def test_missing_file_exits_2_without_touching_others(self) -> None:
        evidence = self.temp_dir / "audit.md"
        evidence.write_text(f'{FIELD}: "abc"\n')

        result = self.run_mask(evidence, self.temp_dir / "missing.md")

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("missing.md", result.stderr)
        self.assertEqual(evidence.read_text(), f'{FIELD}: "abc"\n')


if __name__ == "__main__":
    unittest.main()
