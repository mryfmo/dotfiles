#!/usr/bin/env python3
"""Exercise focused checks in generate-agent-configs.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
import types
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
                "codex": {"model": "gpt-6.1-sol", "model_reasoning_effort": "high"},
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
            "hooks": {
                "permission_request": {
                    "command": "permgate codex",
                    "timeout": 10,
                    "status_message": "Evaluating permission request",
                }
            },
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
                "permission_request": {
                    "command": "permgate claude",
                    "timeout": 10,
                    "status_message": "Evaluating permission request",
                },
            },
            "statusLine": {},
            "disableSkillShellExecution": True,
            "includeGitInstructions": True,
        },
        "plugins": {
            "marketplace_path": "home/dot_agents/plugins/create_marketplace.json",
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

    def write_asset_fixture(self) -> dict:
        pins = self.temp_dir / "scripts/lib/installer-pins.sh"
        pins.parent.mkdir(parents=True)
        pins.write_text('#!/usr/bin/env bash\nCRIT_PIN_VERSION="v0.0.1"\nCRIT_LINUX_AMD64_SHA256="old"\n')
        installer = self.temp_dir / "install/common/mise.sh"
        installer.parent.mkdir(parents=True)
        installer.write_text('#!/usr/bin/env bash\nreadonly MISE_VERSION="v0.0.1"\necho "${MISE_VERSION}"\n')
        return {
            "assets": {
                "mise": {
                    "pin": "v2026.9.12",
                    "render": {
                        "file": "install/common/mise.sh",
                        "constants": {"MISE_VERSION": "pin"},
                    },
                },
                "crit": {
                    "pin": "v0.20.3",
                    "sha256": {"linux-amd64": "d3a3"},
                    "render": {
                        "file": "scripts/lib/installer-pins.sh",
                        "constants": {
                            "CRIT_PIN_VERSION": "pin",
                            "CRIT_LINUX_AMD64_SHA256": "sha256.linux-amd64",
                        },
                    },
                },
                "agmsg": {"pin": "snapshot"},
            }
        }

    def test_asset_constants_render_into_their_files(self) -> None:
        outputs = self.module.render_asset_constants(self.write_asset_fixture())

        self.assertEqual(
            outputs[self.temp_dir / "install/common/mise.sh"],
            '#!/usr/bin/env bash\nreadonly MISE_VERSION="v2026.9.12"\necho "${MISE_VERSION}"\n',
        )
        self.assertEqual(
            outputs[self.temp_dir / "scripts/lib/installer-pins.sh"],
            '#!/usr/bin/env bash\nCRIT_PIN_VERSION="v0.20.3"\nCRIT_LINUX_AMD64_SHA256="d3a3"\n',
        )
        self.assertEqual(len(outputs), 2)

    def test_a_list_render_writes_one_pin_into_several_files_and_declare_r(self) -> None:
        manifest = self.write_asset_fixture()
        bootstrap = self.temp_dir / "setup.sh"
        bootstrap.write_text('#!/usr/bin/env bash\ndeclare -r MISE_VERSION="v0.0.1"\n')
        mise = manifest["assets"]["mise"]
        mise["render"] = [mise["render"], {"file": "setup.sh", "constants": {"MISE_VERSION": "pin"}}]

        outputs = self.module.render_asset_constants(manifest)

        self.assertEqual(
            outputs[self.temp_dir / "install/common/mise.sh"],
            '#!/usr/bin/env bash\nreadonly MISE_VERSION="v2026.9.12"\necho "${MISE_VERSION}"\n',
        )
        self.assertEqual(outputs[bootstrap], '#!/usr/bin/env bash\ndeclare -r MISE_VERSION="v2026.9.12"\n')
        self.assertEqual(len(outputs), 3)

    def test_bootstrap_pins_render_into_setup_and_their_installers(self) -> None:
        manifest = self.write_asset_fixture()
        bootstrap = self.temp_dir / "setup.sh"
        bootstrap.write_text(
            "#!/usr/bin/env bash\n"
            'declare -r HOMEBREW_INSTALL_COMMIT="old"\n'
            'declare -r HOMEBREW_INSTALL_SHA256="old"\n'
            'declare -r CHEZMOI_VERSION="2.70.5"\n'
        )
        brew = self.temp_dir / "install/macos/common/brew.sh"
        brew.parent.mkdir(parents=True)
        brew.write_text('readonly HOMEBREW_INSTALL_COMMIT="old"\nreadonly HOMEBREW_INSTALL_SHA256="old"\n')
        pins = self.temp_dir / "scripts/lib/installer-pins.sh"
        pins.write_text(pins.read_text() + 'CHEZMOI_BOOTSTRAP_PIN_VERSION="2.70.5"\n')
        homebrew = {"HOMEBREW_INSTALL_COMMIT": "pin", "HOMEBREW_INSTALL_SHA256": "sha256"}
        manifest["assets"]["homebrew-installer"] = {
            "pin": "c795",
            "sha256": "9928",
            "render": [
                {"file": "install/macos/common/brew.sh", "constants": homebrew},
                {"file": "setup.sh", "constants": homebrew},
            ],
        }
        manifest["assets"]["chezmoi-bootstrap"] = {
            "pin": "2.70.4",
            "render": [
                {"file": "setup.sh", "constants": {"CHEZMOI_VERSION": "pin"}},
                {"file": "scripts/lib/installer-pins.sh", "constants": {"CHEZMOI_BOOTSTRAP_PIN_VERSION": "pin"}},
            ],
        }

        outputs = self.module.render_asset_constants(manifest)

        self.assertEqual(
            outputs[bootstrap],
            "#!/usr/bin/env bash\n"
            'declare -r HOMEBREW_INSTALL_COMMIT="c795"\n'
            'declare -r HOMEBREW_INSTALL_SHA256="9928"\n'
            'declare -r CHEZMOI_VERSION="2.70.4"\n',
        )
        self.assertEqual(
            outputs[brew], 'readonly HOMEBREW_INSTALL_COMMIT="c795"\nreadonly HOMEBREW_INSTALL_SHA256="9928"\n'
        )
        self.assertIn('CHEZMOI_BOOTSTRAP_PIN_VERSION="2.70.4"\n', outputs[pins])

    def test_entries_reaching_one_file_through_a_symlink_edit_one_snapshot(self) -> None:
        manifest = self.write_asset_fixture()
        pins = self.temp_dir / "scripts/lib/installer-pins.sh"
        (pins.parent / "alias.sh").symlink_to(pins.name)
        manifest["assets"]["crit"]["render"] = [
            {
                "file": "scripts/lib/alias.sh",
                "constants": {"CRIT_PIN_VERSION": "pin", "CRIT_LINUX_AMD64_SHA256": "sha256.linux-amd64"},
            },
            {"file": "scripts/lib/installer-pins.sh", "constants": {"CRIT_PIN_VERSION": "pin"}},
        ]

        outputs = self.module.render_asset_constants(manifest)

        crit_outputs = [path for path in outputs if path.resolve() == pins.resolve()]
        self.assertEqual(len(crit_outputs), 1, outputs)
        self.assertEqual(
            outputs[crit_outputs[0]],
            '#!/usr/bin/env bash\nCRIT_PIN_VERSION="v0.20.3"\nCRIT_LINUX_AMD64_SHA256="d3a3"\n',
        )
        self.module.write_outputs(outputs)
        self.assertEqual(pins.read_text(), outputs[crit_outputs[0]])

    def test_a_declare_r_assignment_must_appear_exactly_once(self) -> None:
        manifest = self.write_asset_fixture()
        bootstrap = self.temp_dir / "setup.sh"
        mise = manifest["assets"]["mise"]
        mise["render"] = [mise["render"], {"file": "setup.sh", "constants": {"MISE_VERSION": "pin"}}]
        for body in ('declare -r MISE_VERSION="a"\ndeclare -r MISE_VERSION="b"\n', "echo no assignment\n"):
            with self.subTest(body=body):
                bootstrap.write_text(body)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.render_asset_constants(manifest)
                self.assertIn("setup.sh must assign MISE_VERSION exactly once for assets.mise", stderr.getvalue())

    def test_asset_constant_must_be_assigned_exactly_once(self) -> None:
        manifest = self.write_asset_fixture()
        manifest["assets"]["mise"]["render"]["constants"] = {"MISSING_VERSION": "pin"}

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.render_asset_constants(manifest)

    def test_asset_pin_must_be_a_plain_value(self) -> None:
        manifest = self.write_asset_fixture()
        manifest["assets"]["mise"]["pin"] = "v1$(touch /tmp/x)"

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.render_asset_constants(manifest)

    def test_check_reports_asset_render_drift(self) -> None:
        manifest = self.write_asset_fixture()
        self.module.load_manifest = lambda: manifest
        self.module.expected_outputs = self.module.render_asset_constants
        self.module.stale_profile_outputs = lambda _manifest: []
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)

        sys.argv = ["generate-agent-configs.py", "--check"]
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.main()
        self.assertIn("install/common/mise.sh", stderr.getvalue())
        self.assertIn("scripts/lib/installer-pins.sh", stderr.getvalue())

        sys.argv = ["generate-agent-configs.py"]
        with contextlib.redirect_stdout(io.StringIO()):
            self.module.main()
        sys.argv = ["generate-agent-configs.py", "--check"]
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.module.main()
        self.assertIn("up to date", stdout.getvalue())

    MANIFEST_TEXT = (
        "schema_version: 1\n"
        "assets:\n"
        "  # Pins live here.\n"
        "  crit:\n"
        "    pin: v0.0.1\n"
        "    sha256:\n"
        "      linux-amd64: old\n"
        "    render:\n"
        "      file: scripts/lib/installer-pins.sh\n"
        "  zed:\n"
        "    pin: v0.0.2\n"
    )

    def test_set_asset_field_rewrites_only_the_named_scalar(self) -> None:
        text = self.module.set_asset_field(self.MANIFEST_TEXT, "crit", "pin", "v0.20.3")
        text = self.module.set_asset_field(text, "crit", "sha256.linux-amd64", "d3a3")

        self.assertEqual(
            text,
            self.MANIFEST_TEXT.replace("pin: v0.0.1", "pin: v0.20.3").replace("linux-amd64: old", "linux-amd64: d3a3"),
        )
        self.assertIn("  # Pins live here.\n", text)
        self.assertIn("    pin: v0.0.2\n", text)

    def test_set_asset_field_rejects_unknown_targets_and_unsafe_values(self) -> None:
        cases = (
            ("nosuch", "pin", "v1"),
            ("crit", "nosuch", "v1"),
            ("crit", "sha256.linux-arm64", "v1"),
            ("zed", "sha256", "v1"),
            ("crit", "pin", "v1$(id)"),
        )
        for name, path, value in cases:
            with self.subTest(target=f"{name}.{path}", value=value):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.set_asset_field(self.MANIFEST_TEXT, name, path, value)

    @staticmethod
    def parse_indented_mapping(text: str) -> dict:
        """Parse the fixture's nested key: value lines without PyYAML."""
        root: dict = {}
        stack = [(-1, root)]
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            key, _, value = line.strip().partition(":")
            while stack[-1][0] >= indent:
                stack.pop()
            if value.strip():
                stack[-1][1][key] = value.strip()
            else:
                stack[-1][1][key] = {}
                stack.append((indent, stack[-1][1][key]))
        return root

    def test_set_asset_updates_the_manifest_and_renders_its_pins(self) -> None:
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(self.MANIFEST_TEXT)
        pins = self.temp_dir / "scripts/lib/installer-pins.sh"
        pins.parent.mkdir(parents=True)
        pins.write_text('CRIT_PIN_VERSION="v0.0.1"\nCRIT_LINUX_AMD64_SHA256="old"\n')
        self.module.parse_manifest = self.parse_indented_mapping
        real_render = self.module.render_asset_constants

        def render(manifest: dict) -> dict:
            manifest["assets"]["crit"]["render"]["constants"] = {
                "CRIT_PIN_VERSION": "pin",
                "CRIT_LINUX_AMD64_SHA256": "sha256.linux-amd64",
            }
            return real_render(manifest)

        self.module.render_asset_constants = render
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        sys.argv = [
            "generate-agent-configs.py",
            "--set-asset",
            "crit.pin=v0.20.3",
            "--set-asset",
            "crit.sha256.linux-amd64=d3a3",
        ]
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.module.main()

        self.assertIn("asset pins updated: crit.pin, crit.sha256.linux-amd64", stdout.getvalue())
        self.assertIn("    pin: v0.20.3\n", manifest_path.read_text())
        self.assertEqual(pins.read_text(), 'CRIT_PIN_VERSION="v0.20.3"\nCRIT_LINUX_AMD64_SHA256="d3a3"\n')

    def test_set_asset_leaves_files_untouched_when_an_assignment_is_invalid(self) -> None:
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(self.MANIFEST_TEXT)
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        sys.argv = [
            "generate-agent-configs.py",
            "--set-asset",
            "crit.pin=v0.20.3",
            "--set-asset",
            "crit.nosuch=1",
        ]
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.main()
        self.assertEqual(manifest_path.read_text(), self.MANIFEST_TEXT)

    def test_set_asset_refuses_fields_other_than_pins_and_checksums(self) -> None:
        for path in ("render.file", "upstream", "sha256.linux-amd64.extra"):
            with self.subTest(path=path):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.set_asset_field(self.MANIFEST_TEXT, "crit", path, "v1")
                self.assertIn("may change only pin, sha256, or sha256.<arch>", stderr.getvalue())

    def run_set_asset_with_parser(self, parser) -> str:
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(self.MANIFEST_TEXT)
        self.module.parse_manifest = parser
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        sys.argv = ["generate-agent-configs.py", "--set-asset", "crit.sha256.linux-amd64=1234"]
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.main()
        self.assertEqual(manifest_path.read_text(), self.MANIFEST_TEXT)
        return stderr.getvalue()

    def test_set_asset_rejects_a_value_that_does_not_parse_back_as_a_string(self) -> None:
        def parse_digits_as_int(text: str) -> dict:
            manifest = self.parse_indented_mapping(text)
            sha256 = manifest["assets"]["crit"]["sha256"]
            sha256["linux-amd64"] = int(sha256["linux-amd64"])
            return manifest

        stderr = self.run_set_asset_with_parser(parse_digits_as_int)

        self.assertIn("did not update to the string '1234': 1234", stderr)

    def test_set_asset_reports_an_unparsable_manifest_without_a_traceback(self) -> None:
        class YAMLError(Exception):
            pass

        self.module.yaml = types.SimpleNamespace(YAMLError=YAMLError)

        def broken(_text: str) -> dict:
            raise YAMLError("mapping values are not allowed here")

        stderr = self.run_set_asset_with_parser(broken)

        self.assertIn("--set-asset produced an unparsable manifest: mapping values", stderr)
        self.assertNotIn("Traceback", stderr)

    def test_repository_marketplace_is_a_runtime_owned_seed(self) -> None:
        manifest = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        seed = ROOT / "home/dot_agents/plugins/create_marketplace.json"
        managed = ROOT / "home/dot_agents/plugins/marketplace.json"
        ignore = (ROOT / "home/.chezmoiignore").read_text()

        self.assertIn(
            "marketplace_path: home/dot_agents/plugins/create_marketplace.json",
            manifest,
        )
        self.assertTrue(seed.is_file())
        self.assertFalse(managed.exists())
        self.assertIn(
            'stat (joinPath .chezmoi.homeDir ".agents/plugins/marketplace.json")',
            ignore,
        )
        self.assertIn(".agents/plugins/marketplace.json", ignore)

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
        outputs = self.module.expected_outputs(sample_manifest())

        codex_path = self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml"
        self.assertIn(codex_path, outputs)
        self.assertIn('model = "gpt-6.1-sol"', outputs[codex_path])
        self.assertIn('model_reasoning_effort = "high"', outputs[codex_path])
        self.assertIn('model_reasoning_summary = "concise"', outputs[codex_path])
        self.assertIn('model_verbosity = "low"', outputs[codex_path])
        self.assertIn('personality = "pragmatic"', outputs[codex_path])
        self.assertIn("check_for_update_on_startup = false", outputs[codex_path])
        self.assertNotIn(self.temp_dir / "home/dot_codex/private_config.toml.tmpl", outputs)

    def test_profile_modify_scripts_preserve_runtime_state(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())

        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.assertIn(standard_profile, outputs)
        self.module.write_outputs(outputs)
        self.assertTrue(standard_profile.stat().st_mode & 0o111)

        result = subprocess.run(
            [str(standard_profile)],
            input='model = "runtime"\nmodel_reasoning_effort = "high"\n\n[hooks.state]\ntrusted = true\n',
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={
                **os.environ,
                "HOME": str(self.temp_dir / "target-home"),
                "CHEZMOI_SOURCE_DIR": str(self.temp_dir / "home"),
                "CHEZMOI_HOME_DIR": str(self.temp_dir / "target-home"),
            },
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('model = "gpt-6.1-sol"', result.stdout)
        self.assertIn('model_reasoning_effort = "high"', result.stdout)
        self.assertIn("[hooks.state]", result.stdout)
        self.assertIn("trusted = true", result.stdout)
        self.assertNotIn(self.temp_dir / "home/dot_codex/standard.config.toml", outputs)

    def test_security_profile_renders_launcher_and_expanded_notify(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["security"] = {
            "claude": {"model": "claude-fable-5", "effort": "high"},
            "codex": {
                "model": "gpt-6-astra",
                "model_reasoning_effort": "high",
                "notify": ["{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify"],
            },
        }
        outputs = self.module.expected_outputs(manifest)
        security_profile = self.temp_dir / "home/dot_codex/modify_private_security.config.toml"
        self.module.write_outputs(outputs)

        home = self.temp_dir / "target-home"
        result = subprocess.run(
            [str(security_profile)],
            input="",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('model = "gpt-6-astra"', result.stdout)
        self.assertIn('model_reasoning_effort = "high"', result.stdout)
        self.assertIn(
            f'notify = ["{home}/.local/bin/common/contextdb-codex-notify"]',
            result.stdout,
        )
        self.assertNotIn("{{", result.stdout)
        env = outputs[self.temp_dir / "home/dot_agents/model-profiles.env"]
        self.assertIn(
            'MODEL_PROFILE_SECURITY_CLAUDE_ARGS="--model claude-fable-5 --effort high"',
            env,
        )
        self.assertIn('MODEL_PROFILE_SECURITY_CODEX_ARGS="--profile security"', env)

    def test_claude_sandbox_renders_optional_socket_and_extra_write_keys(self) -> None:
        manifest = {
            "claude": {
                "sandbox": {
                    "enabled": True,
                    "failIfUnavailable": False,
                    "autoAllowBashIfSandboxed": True,
                    "allowUnsandboxedCommands": True,
                    "excludedCommands": [],
                    "network": {"allowedDomains": ["github.com"], "allowUnixSockets": []},
                }
            },
            "codex": {"sandbox_workspace_write": {"writable_roots": ["/root-a"]}},
        }
        plain = self.module.render_claude_sandbox(manifest)
        self.assertEqual(["/root-a"], plain["filesystem"]["allowWrite"])

        manifest["claude"]["sandbox"]["filesystem"] = {"extra_allow_write": ["~/.cache/uv"]}
        extended = self.module.render_claude_sandbox(manifest)
        self.assertEqual(["/root-a", "~/.cache/uv"], extended["filesystem"]["allowWrite"])

    def test_audit_profile_renders_read_only_sandbox_override(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["audit"] = {
            "claude": {"model": "claude-fable-5-1", "effort": "high"},
            "codex": {
                "model": "gpt-6-astra",
                "model_reasoning_effort": "high",
                "sandbox_mode": "read-only",
            },
        }
        outputs = self.module.expected_outputs(manifest)
        self.module.write_outputs(outputs)

        def render(name: str) -> dict:
            path = self.temp_dir / f"home/dot_codex/modify_private_{name}.config.toml"
            result = subprocess.run(
                [str(path)],
                input="",
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return tomllib.loads(result.stdout)

        self.assertEqual(render("audit")["sandbox_mode"], "read-only")
        self.assertNotIn("sandbox_mode", render("standard"))
        self.assertIn(
            'sandbox_mode = "workspace-write"',
            outputs[self.temp_dir / manifest["codex"]["config_path"]],
        )
        env = outputs[self.temp_dir / "home/dot_agents/model-profiles.env"]
        self.assertIn('MODEL_PROFILE_AUDIT_CODEX_ARGS="--profile audit"', env)

    def test_model_profiles_reject_invalid_sandbox_mode(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["codex"]["sandbox_mode"] = "readonly"

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.model_profiles(manifest)
        self.assertIn("standard.codex.sandbox_mode must be one of", stderr.getvalue())

    def test_profile_modify_scripts_are_byte_idempotent_with_runtime_state(
        self,
    ) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        current = (
            '# Codex model profile "standard"; launch with: codex --profile standard\n'
            f"# {self.module.GENERATED_HEADER}\n"
            "\n"
            'model = "gpt-6.1-sol"\n'
            'model_reasoning_effort = "high"\n'
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "[hooks.state]\n"
            "trusted = true\n"
        )
        result = subprocess.run(
            [str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

    def test_profile_modify_scripts_preserve_repeated_runtime_tables(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        current = (
            '# Codex model profile "standard"; launch with: codex --profile standard\n'
            f"# {self.module.GENERATED_HEADER}\n"
            "\n"
            'model = "gpt-6.1-sol"\n'
            'model_reasoning_effort = "high"\n'
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "[hooks.state]\n"
            "\n"
            "[[hooks.state.sub]]\n"
            'name = "first"\n'
            "\n"
            "[[hooks.state.sub]]\n"
            'name = "second"\n'
        )
        result = subprocess.run(
            [str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

        env_path = self.temp_dir / "home/dot_agents/model-profiles.env"
        self.assertIn('MODEL_PROFILE_INTERACTIVE="standard"', outputs[env_path])
        self.assertIn('MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"', outputs[env_path])
        self.assertIn(
            'MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"',
            outputs[env_path],
        )

        agent_path = self.temp_dir / "home/dot_claude/agents/express-explorer.md"
        self.assertIn("model: haiku", outputs[agent_path])
        self.assertIn("effort: low", outputs[agent_path])

        self.assertFalse([path for path in outputs if path.name == "ccgate.jsonnet"])

    def test_profile_modify_scripts_seed_base_hook_trust(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        home = self.temp_dir / "target-home"
        base = home / ".codex/config.toml"
        base.parent.mkdir(parents=True)
        base.write_text(
            '[hooks.state]\n\n[hooks.state."/workspace/.codex/hooks.json:stop:0:0"]\ntrusted_hash = "sha256:base"\n'
        )

        result = subprocess.run(
            [str(standard_profile)],
            input=(
                "[hooks.state]\n\n"
                '[hooks.state."/home/.codex/config.toml:permission_request:0:0"]\n'
                'trusted_hash = "sha256:profile"\n'
            ),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[features]\nhooks = true", result.stdout)
        self.assertIn('trusted_hash = "sha256:profile"', result.stdout)
        self.assertIn('trusted_hash = "sha256:base"', result.stdout)

    def test_profile_modify_scripts_warn_on_hook_trust_divergence(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        home = self.temp_dir / "target-home"
        base = home / ".codex/config.toml"
        base.parent.mkdir(parents=True)
        base.write_text('[hooks.state."hook"]\ntrusted_hash = "sha256:base"\n')
        current = '[hooks.state."hook"]\ntrusted_hash = "sha256:profile"\n'

        result = subprocess.run(
            [str(profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            'warning: hook trust divergence for hooks.state."hook": profile=sha256:profile base=sha256:base',
            result.stderr,
        )
        self.assertIn('trusted_hash = "sha256:profile"', result.stdout)

    def test_profile_modify_scripts_are_quiet_for_matching_hook_trust(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        home = self.temp_dir / "target-home"
        base = home / ".codex/config.toml"
        base.parent.mkdir(parents=True)
        base.write_text('[hooks.state."hook"]\ntrusted_hash = "sha256:same"\n')
        current = '[hooks.state."hook"]\ntrusted_hash = "sha256:same"\n'

        result = subprocess.run(
            [str(profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual("", result.stderr)

    def test_claude_settings_use_interactive_profile_with_permgate(
        self,
    ) -> None:
        settings = self.module.json.loads(self.module.render_claude_settings(sample_manifest()))

        self.assertEqual("sonnet", settings["model"])
        self.assertEqual("high", settings["effortLevel"])
        self.assertNotIn("[1m]", settings["model"])
        self.assertEqual(
            settings["hooks"]["PermissionRequest"],
            [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "permgate claude",
                            "timeout": 10,
                            "statusMessage": "Evaluating permission request",
                        }
                    ],
                }
            ],
        )

    def test_an_empty_mcp_server_map_renders_no_tables_and_an_empty_claude_map(self) -> None:
        manifest = sample_manifest()
        self.assertEqual(manifest["mcp_servers"], {})

        self.assertNotIn("[mcp_servers.", self.module.render_codex(manifest))
        claude_mcp = self.module.render_claude_mcp(manifest).split("*/}}", 1)[-1]
        self.assertEqual(json.loads(claude_mcp), {"mcpServers": {}})
        self.assertNotIn("enabledPlugins", json.loads(self.module.render_claude_settings(manifest)))

    def test_codex_config_renders_permgate_permission_request(self) -> None:
        config = self.module.render_codex(sample_manifest())

        self.assertIn("[[hooks.PermissionRequest]]", config)
        self.assertIn("[[hooks.PermissionRequest.hooks]]", config)
        self.assertIn('command = "permgate codex"', config)
        self.assertNotIn("ccgate", config)

    def test_codex_config_renders_working_tree_project_key(self) -> None:
        manifest = sample_manifest()
        manifest["codex"]["projects"] = {"{{ .chezmoi.workingTree }}": {"trust_level": "trusted"}}

        config = self.module.render_codex(manifest)

        self.assertIn('[projects."{{ .chezmoi.workingTree }}"]', config)
        self.assertNotIn("/Users/mryfmo/", config)

    def test_managed_hooks_use_installed_permgate_paths(self) -> None:
        codex = (ROOT / "home/.chezmoitemplates/codex-config-managed.toml").read_text()
        claude = (ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()

        self.assertIn("{{ .chezmoi.homeDir }}/.local/bin/common/permgate codex", codex)
        self.assertIn("~/.local/bin/common/permgate claude", claude)

    def test_managed_claude_sandbox_excludes_agmsg_dispatch(self) -> None:
        claude = json.loads((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text())

        self.assertIn("agmsg-dispatch", claude["sandbox"]["excludedCommands"])
        self.assertEqual(["Bash(agmsg-dispatch:*)"], claude["permissions"]["allow"])
        self.assertEqual("auto", claude["permissions"]["defaultMode"])
        self.assertEqual([], claude["permissions"]["ask"])
        self.assertEqual(
            [
                "Bash(gh release:*)",
                "Bash(npm publish:*)",
                "Bash(uv publish:*)",
                "Bash(terraform apply:*)",
                "Bash(kubectl apply:*)",
            ],
            claude["permissions"]["deny"][-5:],
        )

    def test_managed_codex_path_includes_installed_common_bin(self) -> None:
        codex = tomllib.loads((ROOT / "home/.chezmoitemplates/codex-config-managed.toml").read_text())

        path = codex["shell_environment_policy"]["set"]["PATH"].split(":")
        self.assertIn("{{ .chezmoi.homeDir }}/.local/bin/common", path)
        self.assertLess(
            path.index("{{ .chezmoi.homeDir }}/.local/bin"),
            path.index("{{ .chezmoi.homeDir }}/.local/bin/common"),
        )

    def test_model_profiles_env_renders_worker_kind(self) -> None:
        manifest = sample_manifest()
        manifest["worker_kind"] = "claude"

        env = self.module.render_model_profiles_env(manifest)

        self.assertIn('HERDR_AGENTS_WORKER_KIND="claude"', env)

    def test_worker_kind_defaults_to_codex(self) -> None:
        env = self.module.render_model_profiles_env(sample_manifest())

        self.assertIn('HERDR_AGENTS_WORKER_KIND="codex"', env)

    def test_unknown_worker_kind_fails(self) -> None:
        manifest = sample_manifest()
        manifest["worker_kind"] = "banana"

        with self.assertRaises(SystemExit):
            self.module.render_model_profiles_env(manifest)

    def test_model_profiles_env_renders_worker_profile(self) -> None:
        manifest = sample_manifest()
        manifest["worker_profile"] = "express"

        env = self.module.render_model_profiles_env(manifest)

        self.assertIn('HERDR_AGENTS_WORKER_PROFILE="express"', env)

    def test_absent_worker_profile_renders_no_env_line(self) -> None:
        env = self.module.render_model_profiles_env(sample_manifest())

        self.assertNotIn("HERDR_AGENTS_WORKER_PROFILE", env)

    def test_model_profiles_env_renders_worker_worktree(self) -> None:
        manifest = sample_manifest()
        manifest["worker_worktree"] = ".claude/worktrees/worker-c"

        env = self.module.render_model_profiles_env(manifest)

        self.assertIn('HERDR_AGENTS_WORKER_WORKTREE=".claude/worktrees/worker-c"', env)

    def test_absent_worker_worktree_renders_no_env_line(self) -> None:
        env = self.module.render_model_profiles_env(sample_manifest())

        self.assertNotIn("HERDR_AGENTS_WORKER_WORKTREE", env)

    def test_worker_worktree_outside_claude_worktrees_fails(self) -> None:
        for path in (
            "worker-c",
            "/abs/.claude/worktrees/x",
            ".claude/worktrees/..",
            ".claude/worktrees/a/b",
            ".claude/worktrees/$(x)",
        ):
            with self.subTest(path=path):
                manifest = sample_manifest()
                manifest["worker_worktree"] = path
                with self.assertRaises(SystemExit):
                    self.module.render_model_profiles_env(manifest)

    def test_unknown_worker_profile_fails(self) -> None:
        manifest = sample_manifest()
        manifest["worker_profile"] = "missing"

        with self.assertRaises(SystemExit):
            self.module.render_model_profiles_env(manifest)

    def test_unknown_interactive_profile_fails(self) -> None:
        manifest = sample_manifest()
        manifest["interactive_profile"] = "missing"

        with self.assertRaises(SystemExit):
            self.module.interactive_profile(manifest)

    def test_model_profiles_env_renders_claude_advisor_only_when_set(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["claude"]["advisor"] = "fable"

        env = self.module.render_model_profiles_env(manifest)

        self.assertIn(
            'MODEL_PROFILE_STANDARD_CLAUDE_ARGS="--model sonnet --effort high --advisor fable"',
            env,
        )
        self.assertIn('MODEL_PROFILE_EXPRESS_CLAUDE_ARGS="--model haiku --effort low"', env)
        self.assertEqual(env.count("--advisor"), 1)

    def test_model_profiles_reject_unsafe_advisor(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["claude"]["advisor"] = "fable; rm -rf"

        with self.assertRaises(SystemExit):
            self.module.model_profiles(manifest)

    def test_claude_settings_render_interactive_advisor_only_when_set(self) -> None:
        manifest = sample_manifest()
        self.assertNotIn("advisorModel", json.loads(self.module.render_claude_settings(manifest)))

        manifest["model_profiles"]["standard"]["claude"]["advisor"] = "fable"
        settings = json.loads(self.module.render_claude_settings(manifest))

        self.assertEqual(settings["advisorModel"], "fable")

    def test_model_profiles_reject_incomplete_or_unsafe_entries(self) -> None:
        missing_agent = sample_manifest()
        del missing_agent["model_profiles"]["standard"]["codex"]
        with self.assertRaises(SystemExit):
            self.module.model_profiles(missing_agent)

        unsafe_value = sample_manifest()
        unsafe_value["model_profiles"]["standard"]["claude"]["model"] = "sonnet 5; rm -rf"
        with self.assertRaises(SystemExit):
            self.module.model_profiles(unsafe_value)

        missing_express = sample_manifest()
        del missing_express["model_profiles"]["express"]
        with self.assertRaises(SystemExit):
            self.module.model_profiles(missing_express)

    def test_claude_settings_render_the_format_hook_from_its_path(self) -> None:
        settings = self.module.json.loads(self.module.render_claude_settings(sample_manifest()))
        self.assertEqual(
            settings["hooks"]["PostToolUse"],
            [
                {
                    "matcher": "Write|Edit|MultiEdit",
                    "hooks": [{"type": "command", "command": "~/.claude/hooks/format-edited-files.py"}],
                }
            ],
        )

        manifest = sample_manifest()
        del manifest["claude"]["hooks"]["format_edited_files_hook"]
        settings = self.module.json.loads(self.module.render_claude_settings(manifest))
        self.assertEqual(settings["hooks"]["PostToolUse"], [{"matcher": "Write|Edit|MultiEdit", "hooks": []}])

    def test_claude_settings_renders_session_start_hooks(self) -> None:
        manifest = sample_manifest()
        manifest["claude"]["hooks"]["session_start"] = [
            {
                "matcher": "*",
                "hooks": [
                    {
                        "type": "command",
                        "command": "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session",
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
                            "command": "bash '{{ .chezmoi.homeDir }}/.claude/hooks/herdr-agent-state.sh' session",
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
            if line.startswith(("  model:", "  effortLevel:", "  model_reasoning_effort:")):
                self.fail(f"model settings must live in model_profiles only: {line.strip()}")


if __name__ == "__main__":
    unittest.main()
