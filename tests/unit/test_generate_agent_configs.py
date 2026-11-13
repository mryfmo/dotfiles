#!/usr/bin/env python3
"""Exercise focused checks in generate-agent-configs.py."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
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
CHEZMOI = shutil.which("chezmoi") or str(Path.home() / ".local/share/mise/installs/chezmoi/latest/chezmoi")
NODE = shutil.which("node") or str(Path.home() / ".local/share/mise/installs/node/latest/bin/node")
JQ = shutil.which("jq") or str(Path.home() / ".local/share/mise/installs/jq/latest/jq")
# `claude doctor` for the Linux glob check (regime-cutover U17): CI's ubuntu-24.04 leg installs Claude Code through
# mise and exports CLAUDE_DOCTOR_BIN; elsewhere the test runs when `claude` is on PATH and skips otherwise.
CLAUDE_DOCTOR_BIN = os.environ.get("CLAUDE_DOCTOR_BIN") or shutil.which("claude")
LINUX_GLOB_WARNING = "Glob patterns in sandbox permission rules are not fully supported on Linux"
LINUX_GLOB_FOUND = re.compile(r"Found (\d+) pattern\(s\): (.+?)(?: \((\d+) more\))?\. On Linux")
# A project path that exists on every test host, so the profile merge keeps its trust.
EXISTING_PROJECT = "/tmp"
# The same fixture as test_codex_config_merge: a profile table whose multiline strings hold header-like lines, with and without a trailing comment.
MULTILINE_PROFILE = (
    "[agents.reviewer]\n"
    'developer_instructions = """\n'
    "Examples:\n"
    '[hooks.state."custom-hook"] # example\n'
    '[projects."/x"]\n'
    'An escaped \\""" stays inside.\n'
    '"""\n'
    "notes = '''\n"
    "[[mcp_servers.example]] # literal\n"
    "[tui]\n"
    "'''\n"
    'one_line = """[a] # b"""\n'
)


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
                "omp": {"model": "openai-siwc/gpt-5.6-luna", "effort": "low"},
            },
            "standard": {
                "claude": {"model": "sonnet", "effort": "high"},
                "codex": {"model": "gpt-6.1-sol", "model_reasoning_effort": "high"},
                "omp": {"model": "anthropic/sonnet", "effort": "high"},
            },
        },
        "interactive_profile": "standard",
        "omp": {"skills_directories": ["~/.agents/skills"], "roles": {"worker": "standard"}, "check_update": False},
        "skills": {
            "audience": {"example": ["claude", "codex", "omp", "omp-worker"]},
            "pstack": {"audience": ["omp", "omp-worker"], "exclude": []},
        },
        "codex": {
            "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
            "audit": {
                "model_profile": "standard",
                "filesystem": {
                    ":root": "deny",
                    ":minimal": "read",
                    "$AUDIT_TREE": "read",
                    ":tmpdir": "write",
                    "/opt/homebrew": "read",
                    "$CODEX_LOGIN_HOME": "deny",
                    "$CODEX_HOME": "deny",
                    "~/.ssh": "deny",
                },
            },
            "model_reasoning_summary": "concise",
            "model_verbosity": "low",
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
            "schema": "https://json.schemastore.org/claude-code-settings.json",
            "plansDirectory": "./.agents/worklog/claude",
            "permissions": {"deny": [], "defaultMode": "plan", "ask": []},
            "hooks": {
                "enforce_uv_hook": "~/.claude/hooks/enforce-uv.sh",
                "format_edited_files_hook": "~/.claude/hooks/format-edited-files.py",
                "project_map_reload_hook": "~/.claude/hooks/project-map-reload.sh",
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
        "command_policy": [
            {
                "id": "sudo",
                "patterns": [["sudo"]],
                "claude": "deny",
                "codex": "forbidden",
                "reason": "Agents never escalate privileges.",
                "examples": ["sudo true"],
            }
        ],
        "mcp_servers": {},
    }


COMMAND_HOOKS = [
    {"event": "PreCompact", "command": "contextdb hook pre-compact", "timeout": 30, "status_message": "Saving context"},
    {
        "event": "PostCompact",
        "command": "contextdb hook post-compact",
        "timeout": 30,
        "status_message": "Restoring context",
    },
    {
        "event": "SessionEnd",
        "command": "contextdb hook session-end",
        "timeout": 3,
        "status_message": "Closing session",
    },
]
COMMAND_HOOKS_TOML = """
[[hooks.PreCompact]]
matcher = "*"

[[hooks.PreCompact.hooks]]
type = "command"
command = "contextdb hook pre-compact"
timeout = 30
statusMessage = "Saving context"

[[hooks.PostCompact]]
matcher = "*"

[[hooks.PostCompact.hooks]]
type = "command"
command = "contextdb hook post-compact"
timeout = 30
statusMessage = "Restoring context"

[[hooks.SessionEnd]]
matcher = "*"

[[hooks.SessionEnd.hooks]]
type = "command"
command = "contextdb hook session-end"
timeout = 3
statusMessage = "Closing session"
"""


def render_claude_template(text: str, temp_dir: Path, os_name: str = "darwin") -> dict:
    return json.loads(execute_chezmoi_template(text, temp_dir, os_name))


def execute_chezmoi_template(text: str, temp_dir: Path, os_name: str = "darwin") -> str:
    result = subprocess.run(
        [
            CHEZMOI,
            "--config",
            str(temp_dir / "chezmoi.toml"),
            "--source",
            str(temp_dir),
            "--cache",
            str(temp_dir / "cache"),
            "--persistent-state",
            str(temp_dir / "state"),
            "execute-template",
            "--init",
            "--override-data",
            json.dumps({"chezmoi": {"os": os_name, "homeDir": "/render-home"}}),
        ],
        input=text,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout


# The managed allow rules: the coordinator levers (regime-cutover U16), each lever rule naming the copy chezmoi
# installs under ~/.local/bin/common (U31), and the read-only `hcom list`.
MANAGED_ALLOW = [
    "Bash(~/.local/bin/common/hcom-seat *)",
    "Bash(~/.local/bin/common/hcom-dispatch *)",
    "Bash(~/.local/bin/common/bus-history.sh *)",
    "Bash(~/.local/bin/common/worktree-gc.sh *)",
    "Bash(~/.local/bin/common/worker-worktree.sh *)",
    "Bash(~/.local/bin/common/regime-init *)",
    "Bash(~/.local/bin/common/checkout-guard.sh *)",
    "Bash(hcom list *)",
]
LEVERS = (
    "acp-broker",
    "acp-record-place.py",
    "acp-relay.py",
    "acp-seat",
    "brief-check.py",
    "bus-history.sh",
    "checkout-guard.sh",
    "claude-keyed",
    "git-isolated.sh",
    "hcom-dispatch",
    "hcom-seat",
    "intake-observe.py",
    "ledger-row.py",
    "ledger.py",
    "omp-run.sh",
    "pr-audit.sh",
    "pr-body-edit.sh",
    "pr-close.sh",
    "pr-merge.sh",
    "pr-thread-reply.sh",
    "pr-thread-resolve.sh",
    "pr-threads-check.sh",
    "pr-update-branch.sh",
    "profile-config-place.py",
    "read-lib.sh",
    "records-sync.sh",
    "regime-env",
    "regime-init",
    "regime-start",
    "regime-stop",
    "regime-store-move",
    "router-gh",
    "router-settings-apply",
    "router-settings-apply.py",
    "seat-login-preflight",
    "seat-settings-render.sh",
    "worker-worktree.sh",
    "worktree-gc.sh",
)


def load_manifest_fixture(temp_dir: Path) -> dict:
    text = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
    return render_claude_template("{{ fromYaml " + json.dumps(text) + " | toJson }}", temp_dir)


class GenerateAgentConfigsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_generator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="generate-agent-configs-test-"))
        self.module.ROOT = self.temp_dir

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def render_claude_template(self, text: str, os_name: str = "darwin") -> dict:
        return render_claude_template(text, self.temp_dir, os_name)

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
                "plain-asset": {"pin": "snapshot"},
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
        self.module.load_manifest = lambda _text=None: manifest
        self.module.expected_outputs = self.module.render_asset_constants
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
        "  deepseek-harness:\n"
        "    pin: dsh-v0.0.1\n"
        f"    ref_commit: {'ab' * 20}\n"
    )
    COMMIT = "b830ec950faba0a46dda564be3e2d854afed94f1"

    def test_set_asset_field_rewrites_only_the_named_scalar(self) -> None:
        text = self.module.set_asset_field(self.MANIFEST_TEXT, "crit", "pin", "v0.20.3")
        text = self.module.set_asset_field(text, "crit", "sha256.linux-amd64", "d3a3")

        self.assertEqual(
            text,
            self.MANIFEST_TEXT.replace("pin: v0.0.1", "pin: v0.20.3").replace("linux-amd64: old", "linux-amd64: d3a3"),
        )
        self.assertIn("  # Pins live here.\n", text)
        self.assertIn("    pin: v0.0.2\n", text)

    def test_set_asset_field_rewrites_the_ref_commit_alone(self) -> None:
        text = self.module.set_asset_field(self.MANIFEST_TEXT, "deepseek-harness", "ref_commit", self.COMMIT)

        self.assertEqual(text, self.MANIFEST_TEXT.replace(f"ref_commit: {'ab' * 20}", f"ref_commit: {self.COMMIT}"))

    def test_set_asset_field_refuses_a_ref_commit_that_is_not_40_lowercase_hex(self) -> None:
        for value in (self.COMMIT[:-1], self.COMMIT.upper(), "dsh-v0.2.1-rc.5", f"{self.COMMIT}0", "g" * 40):
            with self.subTest(value=value):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.set_asset_field(self.MANIFEST_TEXT, "deepseek-harness", "ref_commit", value)
                self.assertIn(
                    f"assets.deepseek-harness.ref_commit must be a commit of 40 lowercase hex characters: {value!r}",
                    stderr.getvalue(),
                )

    def test_set_asset_field_refuses_a_ref_commit_under_fallback(self) -> None:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.set_asset_field(self.MANIFEST_TEXT, "deepseek-harness", "fallback.ref_commit", self.COMMIT)
        self.assertIn(
            "may change only pin, sha256, sha256.<arch> (optionally under fallback.) or ref_commit", stderr.getvalue()
        )

    def test_set_asset_field_reaches_the_fallback_pin_and_its_checksums(self) -> None:
        manifest = self.MANIFEST_TEXT + (
            "  mise:\n    release: latest\n    fallback:\n      pin: v1\n      sha256:\n        linux-x64: old\n"
        )
        text = self.module.set_asset_field(manifest, "mise", "fallback.pin", "v2026.10.3")
        text = self.module.set_asset_field(text, "mise", "fallback.sha256.linux-x64", "0414")

        self.assertEqual(
            text, manifest.replace("pin: v1\n", "pin: v2026.10.3\n").replace("linux-x64: old", "linux-x64: 0414")
        )

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

    def test_set_asset_moves_the_ref_commit_and_renders_dsh_commit(self) -> None:
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(self.MANIFEST_TEXT)
        pins = self.temp_dir / "scripts/lib/installer-pins.sh"
        pins.parent.mkdir(parents=True)
        pins.write_text(f'DSH_PIN_TAG="dsh-v0.0.1"\nDSH_COMMIT="{"ab" * 20}"\n')
        self.module.parse_manifest = self.parse_indented_mapping
        real_render = self.module.render_asset_constants

        def render(manifest: dict) -> dict:
            # The fixture parser reads no flow mapping, so the render entries are set here.
            manifest["assets"]["crit"].pop("render")
            manifest["assets"]["deepseek-harness"]["render"] = {
                "file": "scripts/lib/installer-pins.sh",
                "constants": {"DSH_PIN_TAG": "pin", "DSH_COMMIT": "ref_commit"},
            }
            return real_render(manifest)

        self.module.render_asset_constants = render
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        sys.argv = ["generate-agent-configs.py", "--set-asset", f"deepseek-harness.ref_commit={self.COMMIT}"]
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self.module.main()

        self.assertIn("asset pins updated: deepseek-harness.ref_commit", stdout.getvalue())
        self.assertEqual(
            manifest_path.read_text(),
            self.MANIFEST_TEXT.replace(f"ref_commit: {'ab' * 20}", f"ref_commit: {self.COMMIT}"),
        )
        self.assertEqual(pins.read_text(), f'DSH_PIN_TAG="dsh-v0.0.1"\nDSH_COMMIT="{self.COMMIT}"\n')

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
                self.assertIn(
                    "may change only pin, sha256, sha256.<arch> (optionally under fallback.) or ref_commit",
                    stderr.getvalue(),
                )

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
        source = self.temp_dir / "home/dot_agents/skills/example/scripts/executable_send.sh"
        source.parent.mkdir(parents=True)
        source.write_text("#!/bin/sh\n")

        outputs = self.module.claude_skill_symlink_outputs(sample_manifest())

        target = self.temp_dir / "home/dot_claude/skills/example/scripts/symlink_send.sh.tmpl"
        self.assertEqual(
            outputs[target],
            "{{ .chezmoi.sourceDir }}/dot_agents/skills/example/scripts/executable_send.sh\n",
        )
        self.assertNotIn(
            self.temp_dir / "home/dot_claude/skills/example/scripts/symlink_executable_send.sh.tmpl",
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
        self.assertNotIn("personality", outputs[codex_path])
        self.assertIn("check_for_update_on_startup = false", outputs[codex_path])
        self.assertNotIn(self.temp_dir / "home/dot_codex/private_config.toml.tmpl", outputs)

    def test_profile_modify_scripts_preserve_runtime_state(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())

        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.assertIn(standard_profile, outputs)
        self.module.write_outputs(outputs)
        self.assertTrue(standard_profile.stat().st_mode & 0o111)

        result = subprocess.run(
            [sys.executable, str(standard_profile)],
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
            "omp": {"model": "openai-siwc/gpt-6-astra", "effort": "high"},
        }
        outputs = self.module.expected_outputs(manifest)
        security_profile = self.temp_dir / "home/dot_codex/modify_private_security.config.toml"
        self.module.write_outputs(outputs)

        home = self.temp_dir / "target-home"
        result = subprocess.run(
            [sys.executable, str(security_profile)],
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
        self.assertNotIn("denyWrite", extended["filesystem"], "no hcom root granted, so no denyWrite key")

    def test_claude_sandbox_deny_write_renders_the_hcom_launch_inputs_per_os(self) -> None:
        filesystem = {
            "extra_allow_write": ["~/.local/state/hcom-regime", "~/.local/state/hcom", "~/.local/state/omp-seats"],
            "hcom_store_roots": {"~/.local/state/hcom-regime": "store", "~/.local/state/hcom": "parent"},
            "deny_write_under_hcom_stores": {"env": "file", "scripts": "dir", ".tmp/launch": "dir"},
            "seats_root": "~/.local/state/omp-seats",
            "deny_write_seat_sandboxes": ["*/.sandbox"],
        }
        manifest = {
            "claude": {
                "sandbox": {
                    "enabled": True,
                    "failIfUnavailable": True,
                    "autoAllowBashIfSandboxed": True,
                    "allowUnsandboxedCommands": False,
                    "excludedCommands": [],
                    "filesystem": filesystem,
                    "network": {"allowedDomains": ["github.com"]},
                }
            },
            "codex": {"sandbox_workspace_write": {"writable_roots": ["/root-a"]}},
        }
        # macOS: every denied path as written under the store, under each slug of the parent, and every seat sandbox,
        # sorted and unique, and no pin of the directories between a root and a denied path (`~/.local/state/hcom/*`,
        # `~/.local/state/hcom-regime/.tmp`, `~/.local/state/omp-seats/*`): measured, such an entry denies the
        # directory's contents, so a pin would deny every seat worktree write (U195b).
        self.assertEqual(
            [
                "~/.local/state/hcom-regime/.tmp/launch",
                "~/.local/state/hcom-regime/env",
                "~/.local/state/hcom-regime/scripts",
                "~/.local/state/hcom/*/.tmp/launch",
                "~/.local/state/hcom/*/env",
                "~/.local/state/hcom/*/scripts",
                "~/.local/state/omp-seats/*/.sandbox",
            ],
            self.module.render_claude_sandbox(manifest)["filesystem"]["denyWrite"],
        )
        # Linux: the static store alone, a file literal, a directory as <dir>/**, the directory between the root and
        # `.tmp/launch` pinned whole; nothing holding an interior `*` (the per-slug stores, the seat sandboxes), which
        # the Linux sandbox discards.
        self.assertEqual(
            [
                "~/.local/state/hcom-regime/.tmp/**",
                "~/.local/state/hcom-regime/.tmp/launch/**",
                "~/.local/state/hcom-regime/env",
                "~/.local/state/hcom-regime/scripts/**",
            ],
            self.module.render_claude_sandbox(manifest, "linux")["filesystem"]["denyWrite"],
        )
        # The derivation, not a list: a deeper name yields every directory strictly between the root and the name as a
        # pin on Linux and the name alone on macOS (the seat sandbox stays, from its own list).
        filesystem["deny_write_under_hcom_stores"] = {"hooks/pre/run.sh": "file"}
        self.assertEqual(
            [
                "~/.local/state/hcom-regime/hooks/pre/run.sh",
                "~/.local/state/hcom/*/hooks/pre/run.sh",
                "~/.local/state/omp-seats/*/.sandbox",
            ],
            self.module.render_claude_sandbox(manifest)["filesystem"]["denyWrite"],
        )
        self.assertEqual(
            [
                "~/.local/state/hcom-regime/hooks/**",
                "~/.local/state/hcom-regime/hooks/pre/**",
                "~/.local/state/hcom-regime/hooks/pre/run.sh",
            ],
            self.module.render_claude_sandbox(manifest, "linux")["filesystem"]["denyWrite"],
        )
        filesystem["deny_write_under_hcom_stores"] = {"env": "file", "scripts": "dir", ".tmp/launch": "dir"}
        # A root allowWrite does not grant gets no deny; with no hcom root, or on Linux with only globbed roots, the
        # key is absent.
        filesystem["extra_allow_write"] = ["~/.local/state/hcom"]
        self.assertEqual(
            ["~/.local/state/hcom/*/.tmp/launch", "~/.local/state/hcom/*/env", "~/.local/state/hcom/*/scripts"],
            self.module.render_claude_sandbox(manifest)["filesystem"]["denyWrite"],
        )
        self.assertNotIn("denyWrite", self.module.render_claude_sandbox(manifest, "linux")["filesystem"])
        filesystem["extra_allow_write"] = []
        self.assertNotIn("denyWrite", self.module.render_claude_sandbox(manifest)["filesystem"])
        filesystem["deny_write_under_hcom_stores"] = {"env": "link"}
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.render_claude_sandbox(manifest)
        self.assertIn("deny_write_under_hcom_stores values dir or file", stderr.getvalue())

    def test_claude_sandbox_renders_per_os_from_the_manifest(self) -> None:
        manifest = load_manifest_fixture(self.temp_dir)
        # The hand-written rules, then one rule per command_policy expansion (U76).
        expected_ask = ["Bash(git push *)", "Bash(gh *)", *self.module.claude_command_rules(manifest, "ask")]
        for rule in ("Bash(gh api *)", "Bash(gh pr merge *)", "Bash(gh secret set *)", "Bash(gh run rerun *)"):
            self.assertIn(rule, expected_ask)
        template = self.module.render_claude_settings(manifest)
        for os_name in ("darwin", "linux"):
            with self.subTest(os=os_name):
                settings = self.render_claude_template(template, os_name)
                sandbox = settings["sandbox"]
                self.assertEqual(
                    ["com.apple.trustd.agent"] if os_name == "darwin" else [],
                    sandbox["network"].get("allowMachLookup", []),
                )
                roots = [
                    path.replace("{{ .chezmoi.homeDir }}", "/render-home")
                    for path in manifest["codex"]["sandbox_workspace_write"]["writable_roots"]
                ]
                # Cache and state only: no uv tool tree (the hcom binary) and no mise trust state (U68).
                extras = [
                    "~/.cache/uv",
                    "~/.local/state/hcom-regime",
                    "~/.local/state/hcom",
                    "~/.local/state/omp-seats",
                ]
                self.assertEqual(
                    roots + extras + (["~/Library/Caches/mise"] if os_name == "darwin" else []),
                    sandbox["filesystem"]["allowWrite"],
                )
                self.assertEqual(
                    [
                        "github.com",
                        "api.github.com",
                        "uploads.github.com",
                        "objects.githubusercontent.com",
                        "release-assets.githubusercontent.com",
                        "codeload.github.com",
                        "pypi.org",
                        "files.pythonhosted.org",
                    ],
                    sandbox["network"]["allowedDomains"],
                )
                # Strict sandbox mode: no retry, and the two excluded commands prompt (U68).
                self.assertIs(False, sandbox["allowUnsandboxedCommands"])
                self.assertEqual(["git push *", "gh *"], sandbox["excludedCommands"])
                ask = settings["permissions"]["ask"]
                self.assertTrue(all(f"Bash({entry})" in ask for entry in sandbox["excludedCommands"]))
                self.assertFalse(any("dangerouslyDisableSandbox" in rule for rule in ask))
                self.assertEqual(expected_ask, settings["permissions"]["ask"])
                expected_deny = [
                    *manifest["claude"]["permissions"]["deny"],
                    *self.module.claude_command_rules(manifest, "deny"),
                ]
                self.assertEqual(expected_deny, settings["permissions"]["deny"])
                self.assertEqual(
                    {
                        "GH_TELEMETRY": "false",
                        "DO_NOT_TRACK": "1",
                        "CHECKPOINT_DISABLE": "1",
                        "AWS_EC2_METADATA_DISABLED": "true",
                        # Claude Code's own updater stays off for a claude started outside a login shell too.
                        "DISABLE_AUTOUPDATER": "1",
                        "DISABLE_UPDATES": "1",
                    },
                    settings["env"],
                )
                self.assertFalse(sandbox["network"].get("allowAllUnixSockets", False))
                self.assertNotIn("allowUnixSockets", sandbox["network"])
                self.assertNotIn("tlsTerminate", sandbox["network"])
                self.assertTrue(sandbox["failIfUnavailable"])
                # Round 6: every credential entry is a plain deny, the gh hosts file included; no mask on any OS.
                self.assertEqual(
                    [
                        {"path": path, "mode": "deny"}
                        for path in (
                            "~/.ssh",
                            "~/.config/gh/hosts.yml",
                            "~/.claude/.credentials.json",
                            "~/.config/claude-code/oauth-token",
                            "~/.codex/auth.json",
                            "~/.omp/agent/agent.db*",
                            "~/.omp/profiles/*/agent/agent.db*",
                            "~/.config/age/key.txt",
                        )
                    ],
                    sandbox["credentials"]["files"],
                )
                self.assertEqual(
                    [{"name": "CLAUDE_CODE_OAUTH_TOKEN", "mode": "deny"}], sandbox["credentials"]["envVars"]
                )
                tmp = ["/tmp/**/.env", "/tmp/**/.env.*"]
                darwin_tmp = ["/private/tmp/**/.env", "/private/tmp/**/.env.*"] if os_name == "darwin" else []
                self.assertEqual(["~/**/.env", "~/**/.env.*", *tmp, *darwin_tmp], sandbox["filesystem"]["denyRead"])
                # U195: the inputs the next seat launch runs unsandboxed, taken back from each hcom root, and every
                # seat sandbox; the list hcom-seat denies its seats. macOS holds every path as written and no pin;
                # Linux holds the static store alone (file literal, <dir>/**, `.tmp/**` pinned) and no interior glob.
                names = ("config.toml", "env", "config.env", ".tmp/launch", "scripts", "integrations", "shell_env.json")
                self.assertEqual(
                    [
                        "~/.local/state/hcom-regime/.tmp/launch",
                        "~/.local/state/hcom-regime/config.env",
                        "~/.local/state/hcom-regime/config.toml",
                        "~/.local/state/hcom-regime/env",
                        "~/.local/state/hcom-regime/integrations",
                        "~/.local/state/hcom-regime/scripts",
                        "~/.local/state/hcom-regime/shell_env.json",
                        "~/.local/state/hcom/*/.tmp/launch",
                        "~/.local/state/hcom/*/config.env",
                        "~/.local/state/hcom/*/config.toml",
                        "~/.local/state/hcom/*/env",
                        "~/.local/state/hcom/*/integrations",
                        "~/.local/state/hcom/*/scripts",
                        "~/.local/state/hcom/*/shell_env.json",
                        "~/.local/state/omp-seats/*/.sandbox",
                    ]
                    if os_name == "darwin"
                    else [
                        "~/.local/state/hcom-regime/.tmp/**",
                        "~/.local/state/hcom-regime/.tmp/launch/**",
                        "~/.local/state/hcom-regime/config.env",
                        "~/.local/state/hcom-regime/config.toml",
                        "~/.local/state/hcom-regime/env",
                        "~/.local/state/hcom-regime/integrations/**",
                        "~/.local/state/hcom-regime/scripts/**",
                        "~/.local/state/hcom-regime/shell_env.json",
                    ],
                    sandbox["filesystem"]["denyWrite"],
                )
                # The manifest keeps hcom-seat's seven names in hcom-seat's order (chezmoi's fromYaml sorts keys, so
                # the order is read from the YAML text).
                manifest_text = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
                block = manifest_text.split("deny_write_under_hcom_stores:\n", 1)[1].splitlines()[:7]
                self.assertEqual(list(names), [line.strip().split(":")[0] for line in block])
                deny = settings["permissions"]["deny"]
                self.assertIn("Read(.env)", deny)
                self.assertIn("Read(~/.ssh/**)", deny)
                self.assertNotIn("Read(id_rsa*)", deny)
                self.assertNotIn("Read(id_ed25519*)", deny)

    def test_linux_sandbox_confines_the_top_level_herdr_agents_invocation(self) -> None:
        manifest = load_manifest_fixture(self.temp_dir)
        settings = self.render_claude_template(self.module.render_claude_settings(manifest), "linux")
        self.assertEqual(["git push *", "gh *"], settings["sandbox"]["excludedCommands"])
        # No lever is excluded, so a lever's allow rule only ever approves a sandboxed run (U68).
        self.assertFalse(any(rule.startswith("Bash(git") for rule in MANAGED_ALLOW))
        self.assertEqual(MANAGED_ALLOW, settings["permissions"]["allow"])
        darwin = self.render_claude_template(self.module.render_claude_settings(manifest), "darwin")
        self.assertEqual(MANAGED_ALLOW, darwin["permissions"]["allow"])

    def test_darwin_allow_renders_into_the_darwin_variant_only(self) -> None:
        """`claude.permissions.darwin_allow` stays available for a macOS-only rule (U31 part 1 mechanism)."""
        manifest = load_manifest_fixture(self.temp_dir)
        manifest["claude"]["permissions"]["darwin_allow"] = ["Bash(hcom list *)"]
        manifest["claude"]["permissions"]["allow"] = []
        template = self.module.render_claude_settings(manifest)
        self.assertEqual(["Bash(hcom list *)"], self.render_claude_template(template, "darwin")["permissions"]["allow"])
        # With no shared rule (U26 removed the last one), the linux variant renders no allow rule.
        self.assertEqual([], self.render_claude_template(template, "linux")["permissions"]["allow"])

    def test_the_levers_install_byte_identical_and_pinned(self) -> None:
        """The generator renders each lever's chezmoi copy and pins its sha256 in the manifest (regime-cutover U31)."""
        self.module.ROOT = ROOT
        manifest = load_manifest_fixture(self.temp_dir)
        self.assertEqual(list(LEVERS), self.module.lever_names(manifest))
        installs = self.module.render_lever_installs(manifest)
        text = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        for name in LEVERS:
            with self.subTest(lever=name):
                source = (ROOT / "scripts/orchestrator" / name).read_bytes()
                install_name = self.module.lever_install_name(name)
                installed = ROOT / "home/dot_local/bin/common" / install_name
                self.assertEqual(installs[installed], source.decode())
                self.assertEqual(installed.read_bytes(), source)
                # A module another lever imports is installed under its bare name and never executable (U418).
                self.assertEqual(os.access(installed, os.X_OK), install_name.startswith("executable_"))
                pin = hashlib.sha256(source).hexdigest()
                self.assertEqual(manifest["claude"]["levers"]["sha256"][name], pin)
                self.assertIn(f"\n      {name}: {pin}\n", text)
        self.assertEqual(self.module.refresh_lever_pins(text), text, "the committed pins are current")
        stale = text.replace(manifest["claude"]["levers"]["sha256"]["hcom-seat"], "0" * 64)
        self.assertEqual(self.module.refresh_lever_pins(stale), text, "a stale pin is refreshed and nothing else moves")

    def test_the_ledger_reader_installs_beside_the_row_writer_under_its_bare_name_and_pinned(self) -> None:
        """`ledger-row.py` imports `ledger.py` from its own directory, so the deployed writer needs the reader deployed
        beside it (regime-cutover U418: every run of `~/.local/bin/common/ledger-row.py` refused, `no ledger.py beside
        the lever`). The copy is byte-identical to the checkout's reader, pinned like every lever, and carries no
        `executable_` prefix: chezmoi installs it at mode 0644, a module that is imported and never run."""
        self.module.ROOT = ROOT
        source = ROOT / "scripts/orchestrator/ledger.py"
        installed = ROOT / "home/dot_local/bin/common/ledger.py"
        self.assertTrue(
            installed.is_file(), f"{installed.relative_to(ROOT)} is missing: the deployed row writer imports it"
        )
        self.assertEqual(installed.read_bytes(), source.read_bytes())
        self.assertFalse((ROOT / "home/dot_local/bin/common/executable_ledger.py").exists())
        self.assertFalse(os.access(installed, os.X_OK), "the reader is imported, never run")
        manifest = load_manifest_fixture(self.temp_dir)
        pin = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual(manifest["claude"]["levers"]["sha256"].get("ledger.py"), pin)
        self.assertIn(f"\n      ledger.py: {pin}\n", (ROOT / "home/dot_agents/agent-config.yaml").read_text())
        self.assertEqual(installed, next(path for path in self.module.lever_pins(manifest) if path.name == "ledger.py"))

    def write_claude_bridge_modify_script(self) -> Path:
        """The worker role's rendered claude-bridge modify script, written executable under the scratch directory."""
        self.module.ROOT = ROOT
        manifest = load_manifest_fixture(self.temp_dir)
        rendered = self.module.render_claude_bridge_modify(manifest)
        script = self.temp_dir / "modify_claude-bridge.json"
        script.write_text(rendered[ROOT / self.module.CLAUDE_BRIDGE_MODIFY_PATH.format(role="worker")])
        script.chmod(0o755)
        return script

    def run_modify(
        self, script: Path, current: str | bytes, home: Path, path: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        """Run the modify script as chezmoi does, the live file on stdin (bytes when the case is about the bytes);
        `path` replaces PATH for the fixture runs."""
        env = os.environ | {"HOME": str(home)}
        if path is not None:
            env["PATH"] = path
        run = subprocess.run(
            [str(script)],
            input=current.encode() if isinstance(current, str) else current,
            capture_output=True,
            env=env,
            timeout=180,
            check=False,
        )
        return subprocess.CompletedProcess(
            run.args, run.returncode, run.stdout.decode("utf-8", "replace"), run.stderr.decode("utf-8", "replace")
        )

    def write_fixture_path(self, name: str, *tools: str) -> str:
        """A PATH of one directory holding symlinks to the named tools alone, so a run sees nothing else."""
        bin_dir = self.temp_dir / name
        bin_dir.mkdir()
        for tool in tools:
            source = shutil.which(tool) if tool != "python3" else (shutil.which("python3") or sys.executable)
            self.assertIsNotNone(source, f"{tool} is needed on PATH to build the fixture")
            (bin_dir / tool).symlink_to(source)
        return str(bin_dir)

    def test_the_claude_bridge_modify_scripts_render_for_the_bridge_routed_roles_only(self) -> None:
        """regime-cutover U510: `provider.pathToClaudeCodeExecutable` of every role on the claude-bridge route (a seat
        role whose omp model route is claude-bridge, and every gateway role, whose child the bridge serves) is the
        installed `claude-keyed`, placed by the chezmoi modify script `home/dot_omp/private_profiles/private_<role>/
        private_agent/modify_claude-bridge.json` (the private_ attributes keep hcom-seat's 0700 profile directories);
        a role on another route gets none. The committed files are the renderer's bytes, executable, and the output
        index deploys each as a modify entry on `~/.omp/profiles/<role>/agent/claude-bridge.json`."""
        self.module.ROOT = ROOT
        manifest = load_manifest_fixture(self.temp_dir)
        outputs = self.module.expected_outputs(manifest)
        rendered = self.module.render_claude_bridge_modify(manifest)
        self.assertEqual(
            sorted(path.relative_to(ROOT).as_posix() for path in rendered),
            [self.module.CLAUDE_BRIDGE_MODIFY_PATH.format(role=role) for role in ("dsh", "orchestrator", "worker")],
        )
        index = json.loads((ROOT / "scripts/generated-agent-outputs.json").read_text())
        entries = {entry["source"]: entry for entry in index["outputs"]}
        for path, text in rendered.items():
            rel = path.relative_to(ROOT).as_posix()
            with self.subTest(source=rel):
                self.assertEqual(outputs[path], text)
                self.assertEqual(path.read_bytes(), text.encode(), "the committed file is the renderer's bytes")
                self.assertTrue(os.access(path, os.X_OK))
                self.assertTrue(text.startswith("#!/bin/sh\n"))
                self.assertIn(self.module.CLAUDE_KEYED_INSTALL_PATH, text)
                role = rel.split("/")[3].removeprefix("private_")
                self.assertEqual(
                    entries[rel],
                    {
                        "source": rel,
                        "target": f".omp/profiles/{role}/agent/claude-bridge.json",
                        "kind": "modify",
                        "executable": False,
                    },
                )
        self.assertNotIn(ROOT / self.module.CLAUDE_BRIDGE_MODIFY_PATH.format(role="audit"), outputs)
        # A seat role moved off the bridge route loses its script; one moved onto it gets one.
        moved = json.loads(json.dumps(manifest))
        moved["model_profiles"]["standard"]["omp"]["model"] = "openai-siwc/gpt-6-astra"
        moved["model_profiles"]["audit"]["omp"]["model"] = "claude-bridge/claude-fable-5-1"
        self.assertEqual(
            sorted(path.relative_to(ROOT).as_posix() for path in self.module.render_claude_bridge_modify(moved)),
            [self.module.CLAUDE_BRIDGE_MODIFY_PATH.format(role=role) for role in ("audit", "dsh", "orchestrator")],
        )

    def test_the_claude_bridge_modify_script_keeps_the_bridges_own_keys_and_is_idempotent(self) -> None:
        """The merge sets the one managed key and keeps every other key the bridge wrote (config.ts:29 records
        `startupNoticeShown` with `{...existing}`) in its order, as `json.dumps(indent=2)` and a newline, so a second
        run on its own output returns the same bytes and chezmoi apply and the output index's modify comparison see no
        change. It runs on the system python3 alone (U510b): a PATH holding python3 and cat and nothing else, no uv,
        is enough."""
        script = self.write_claude_bridge_modify_script()
        home = self.temp_dir / "target-home"
        home.mkdir()
        current = (
            json.dumps(
                {
                    "startupNoticeShown": "2026-11-13",
                    "provider": {"plan": "max", "pathToClaudeCodeExecutable": "/old/claude"},
                    "askClaude": {"enabled": True},
                },
                indent=2,
            )
            + "\n"
        )
        run = self.run_modify(script, current, home, path=self.write_fixture_path("python3-only", "python3", "cat"))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        merged = json.loads(run.stdout)
        self.assertEqual(
            merged["provider"], {"plan": "max", "pathToClaudeCodeExecutable": f"{home}/.local/bin/common/claude-keyed"}
        )
        self.assertEqual(merged["startupNoticeShown"], "2026-11-13")
        self.assertEqual(merged["askClaude"], {"enabled": True})
        self.assertEqual(list(merged), ["startupNoticeShown", "provider", "askClaude"], "the key order stays")
        self.assertEqual(run.stdout, json.dumps(merged, indent=2) + "\n")
        again = self.run_modify(script, run.stdout, home)
        self.assertEqual((again.returncode, again.stderr, again.stdout), (0, "", run.stdout))

    def test_the_claude_bridge_modify_script_prints_the_managed_object_with_a_warning_on_empty_or_invalid_input(
        self,
    ) -> None:
        """chezmoi apply never clobbers: an input the merge cannot read yields the managed object alone, one stderr
        warning naming the file, exit 0 (the bridge rewrites the file whole on its next notice anyway)."""
        script = self.write_claude_bridge_modify_script()
        home = self.temp_dir / "target-home"
        home.mkdir()
        managed = (
            json.dumps({"provider": {"pathToClaudeCodeExecutable": f"{home}/.local/bin/common/claude-keyed"}}, indent=2)
            + "\n"
        )
        cases = (
            ("empty", ""),
            ("invalid JSON", "{not json\n"),
            ("a JSON list", "[1, 2]\n"),
            ("a provider that is no object", '{"provider": 3}\n'),
        )
        for label, current in cases:
            with self.subTest(input=label):
                run = self.run_modify(script, current, home)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(run.stdout, managed)
                self.assertEqual(len(run.stderr.splitlines()), 1, run.stderr)
                self.assertIn("claude-bridge.json", run.stderr)

    def test_the_claude_bridge_modify_script_routes_every_odd_input_into_its_warn_branch(self) -> None:
        """U510d (the review of 5594f0e7, findings 1 and 8): the live file sits in the seat's own write root, so its
        content is an input of the seat's choosing. A NaN or an Infinity (json.loads admits them and json.dumps
        re-emits them, so the file became non-JSON, the bridge's tryParseJson read `{}` and the SDK fell back to its
        bundled binary on the login, silently), a lone surrogate escape (an encode error at the write), nesting past
        the recursion limit (a traceback and exit 1), a byte order mark and bytes that are not UTF-8 each yield the
        managed object alone, strict JSON, one stderr warning naming the file, exit 0: the warn branch and nothing
        else, never a traceback, never a file the bridge cannot parse."""
        script = self.write_claude_bridge_modify_script()
        home = self.temp_dir / "target-home"
        home.mkdir()
        managed = (
            json.dumps({"provider": {"pathToClaudeCodeExecutable": f"{home}/.local/bin/common/claude-keyed"}}, indent=2)
            + "\n"
        )

        def refuse_constant(token: str) -> None:
            raise AssertionError(f"the output holds {token}, which is no JSON")

        cases = (
            ("a NaN", '{"startupNoticeShown": "2026-11-13", "provider": {"plan": NaN}}\n'),
            ("an Infinity", '{"provider": {"plan": -Infinity}}\n'),
            ("a lone surrogate escape", '{"startupNoticeShown": "\\ud800", "provider": {"plan": "max"}}\n'),
            ("nesting past the recursion limit", '{"a":' * 100000 + "1" + "}" * 100000 + "\n"),
            ("a byte order mark", "\ufeff" + json.dumps({"startupNoticeShown": "2026-11-13"}) + "\n"),
            ("bytes that are not UTF-8", b'\xff\xfe{"startupNoticeShown": "2026-11-13"}\n'),
        )
        for label, current in cases:
            with self.subTest(input=label):
                run = self.run_modify(script, current, home)
                self.assertEqual(run.returncode, 0, (run.stdout, run.stderr))
                self.assertEqual(run.stdout, managed)
                self.assertEqual(json.loads(run.stdout, parse_constant=refuse_constant), json.loads(managed))
                self.assertEqual(len(run.stderr.splitlines()), 1, run.stderr)
                self.assertIn("claude-bridge.json", run.stderr)
                self.assertNotIn("Traceback", run.stderr)
        text = script.read_text()
        self.assertIn("parse_constant", text, "a NaN or an Infinity is refused at the parse")
        self.assertIn("allow_nan=False", text, "and never written")

    def test_the_claude_bridge_modify_script_claims_idempotence_of_its_own_output_not_the_bridges_bytes(self) -> None:
        """U510e (verdict U510-88ae09c6 P2 :2546): json.dumps writes a float as 1e-07 where the bridge's
        JSON.stringify writes 1e-7, so the script cannot promise byte equality with the bridge's rewrite and claims
        none: its contract is idempotence of its own output and the provider row's presence. A float the bridge
        wrote survives two runs unchanged in value, the second run's bytes equal the first's, and the header states
        the contract and the float form it does not match."""
        script = self.write_claude_bridge_modify_script()
        home = self.temp_dir / "target-home"
        home.mkdir()
        bridge_form = '{\n  "startupNoticeShown": "2026-11-13",\n  "provider": {\n    "plan": "max",\n    "timeout": 1e-7,\n    "ratio": 0.1,\n    "big": 1e+21\n  }\n}\n'
        first = self.run_modify(script, bridge_form, home)
        self.assertEqual((first.returncode, first.stderr), (0, ""), first.stderr)
        merged = json.loads(first.stdout)
        self.assertEqual(merged["provider"]["timeout"], 1e-7)
        self.assertEqual(merged["provider"]["ratio"], 0.1)
        self.assertEqual(merged["provider"]["big"], 1e21)
        self.assertEqual(merged["provider"]["pathToClaudeCodeExecutable"], f"{home}/.local/bin/common/claude-keyed")
        self.assertIn('"timeout": 1e-07,', first.stdout, "json.dumps's float form, not the bridge's 1e-7")
        second = self.run_modify(script, first.stdout, home)
        self.assertEqual((second.returncode, second.stderr, second.stdout), (0, "", first.stdout))
        self.assertEqual(json.loads(second.stdout), merged)
        header = script.read_text().split("set -eu", 1)[0]
        self.assertIn("idempotence of its own output", header)
        self.assertIn("1e-07", header)
        self.assertNotIn("so a second apply changes nothing", header, "no byte-stability claim against the bridge")

    def test_the_claude_bridge_modify_script_warns_once_when_two_conditions_apply(self) -> None:
        """U510e (verdict U510-88ae09c6 P3 :2565): a live file whose provider is no object and which also holds a
        lone surrogate met two warn branches and printed two lines; the script prints one warning per run, the first
        condition met naming the reason, with the managed object alone on stdout and exit 0."""
        script = self.write_claude_bridge_modify_script()
        home = self.temp_dir / "target-home"
        home.mkdir()
        managed = (
            json.dumps({"provider": {"pathToClaudeCodeExecutable": f"{home}/.local/bin/common/claude-keyed"}}, indent=2)
            + "\n"
        )
        run = self.run_modify(script, '{"startupNoticeShown": "\\ud800", "provider": 3}\n', home)
        self.assertEqual(run.returncode, 0, (run.stdout, run.stderr))
        self.assertEqual(run.stdout, managed)
        self.assertEqual(len(run.stderr.splitlines()), 1, run.stderr)
        self.assertIn("claude-bridge.json: provider is not a JSON object", run.stderr)
        self.assertNotIn("surrogate", run.stderr, "the first condition met names the reason")

    def test_the_claude_bridge_modify_script_needs_no_uv_and_fails_the_apply_without_python3(self) -> None:
        """regime-cutover U510b: the apply container (Dockerfile) has python3 and no uv, and the first form's
        `exec cat` without uv echoed the empty stdin, so chezmoi apply wrote nothing, exit 0, and the doctor found
        the three bridge files missing: the login route left in place by silence. The script holds no `uv`, runs the
        merge under `python3 -I -c` (the kit's baseline), and without python3 exits 1 with one stderr line naming
        claude-bridge.json and python3 and nothing on stdout, so chezmoi fails the apply naming the file."""
        script = self.write_claude_bridge_modify_script()
        text = script.read_text()
        self.assertTrue(text.startswith("#!/bin/sh\n"), text.splitlines()[0])
        self.assertNotIn("uv", text)
        self.assertIn("if ! command -v python3 > /dev/null 2>&1; then\n", text)
        self.assertIn('exec python3 -I -c "$merge"\n', text)
        self.assertIn("fail", text.split("set -eu", 1)[0].lower(), "the header states the fail-closed rule")
        home = self.temp_dir / "target-home"
        home.mkdir()
        no_python3 = self.write_fixture_path("no-python3", "cat")
        live = json.dumps({"startupNoticeShown": "2026-10-23"}, indent=2) + "\n"
        for label, current in (("an absent file", ""), ("the bridge's live file", live)):
            with self.subTest(input=label):
                run = self.run_modify(script, current, home, path=no_python3)
                self.assertEqual(run.returncode, 1, (run.stdout, run.stderr))
                self.assertEqual(run.stdout, "", "nothing on stdout: chezmoi gets no content to write")
                self.assertEqual(len(run.stderr.splitlines()), 1, run.stderr)
                self.assertIn("claude-bridge.json", run.stderr)
                self.assertIn("python3", run.stderr)

    def test_check_reports_a_stale_lever_pin_and_a_run_refreshes_it(self) -> None:
        (self.temp_dir / "scripts/orchestrator").mkdir(parents=True)
        (self.temp_dir / "home/dot_agents").mkdir(parents=True)
        (self.temp_dir / "scripts/orchestrator/hcom-seat").write_text("#!/usr/bin/env bash\nexit 0\n")
        pin = hashlib.sha256(b"#!/usr/bin/env bash\nexit 0\n").hexdigest()
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        stale = "schema_version: 1\nclaude:\n  levers:\n    sha256:\n      hcom-seat: " + "0" * 64 + "\n"
        manifest_path.write_text(stale)
        self.module.load_manifest = lambda _text=None: {"claude": {}}
        self.module.expected_outputs = lambda _manifest: {}
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)

        sys.argv = ["generate-agent-configs.py", "--check"]
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.main()
        self.assertIn("home/dot_agents/agent-config.yaml", stderr.getvalue())
        self.assertEqual(manifest_path.read_text(), stale, "--check writes nothing")
        sys.argv = ["generate-agent-configs.py"]
        with contextlib.redirect_stdout(io.StringIO()):
            self.module.main()
        self.assertEqual(manifest_path.read_text(), stale.replace("0" * 64, pin))

    def test_check_refuses_a_crlf_lever_copy_and_a_copy_off_its_pin(self) -> None:
        """F156: freshness compares bytes, and each lever copy must hash to its claude.levers.sha256 pin."""
        body = b"#!/usr/bin/env bash\nexit 0\n"
        source = self.temp_dir / "scripts/orchestrator/omp-run.sh"
        copy = self.temp_dir / "home/dot_local/bin/common/executable_omp-run.sh"
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        for path in (source, copy, manifest_path):
            path.parent.mkdir(parents=True, exist_ok=True)
        pin = hashlib.sha256(body).hexdigest()
        manifest_path.write_text(f"schema_version: 1\nclaude:\n  levers:\n    sha256:\n      omp-run.sh: {pin}\n")
        manifest = {"claude": {"levers": {"sha256": {"omp-run.sh": pin}}}}
        self.module.load_manifest = lambda _text=None: manifest
        self.module.expected_outputs = self.module.render_lever_installs
        self.addCleanup(setattr, sys, "argv", sys.argv)
        sys.argv = ["generate-agent-configs.py", "--check"]

        def check() -> str:
            with contextlib.redirect_stderr(io.StringIO()) as stderr, contextlib.redirect_stdout(io.StringIO()):
                try:
                    self.module.main()
                except SystemExit:
                    pass
            return stderr.getvalue()

        source.write_bytes(body)
        copy.write_bytes(body)
        self.assertEqual("", check())
        copy.write_bytes(body.replace(b"\n", b"\r\n"))
        self.assertIn("home/dot_local/bin/common/executable_omp-run.sh", check())
        # A source and a copy corrupted alike still differ from the pin.
        source.write_bytes(body.replace(b"\n", b"\r\n"))
        self.assertEqual(
            ["home/dot_local/bin/common/executable_omp-run.sh (does not hash to its claude.levers.sha256 pin)"],
            self.module.lever_pin_drift(manifest),
        )
        self.assertIn("does not hash to its claude.levers.sha256 pin", check())

    def test_check_lists_every_orphan_in_a_generated_directory_and_a_run_deletes_it(self) -> None:
        """F056: a file in a generated directory that the expected output set does not hold fails --check."""
        expected = self.temp_dir / "home/dot_agents/omp/profiles/worker.yml.tmpl"
        orphans = [
            "home/dot_agents/omp/profiles/retired.yml.tmpl",
            "home/dot_agents/plugins/old/.codex-plugin/plugin.json",
            "home/dot_claude/agents/old.md",
            "home/dot_claude/skills/gone/references/symlink_removed.md.tmpl",
            "home/dot_codex/modify_private_retired.config.toml",
            "home/dot_codex/retired.config.toml",
            "home/dot_local/bin/common/executable_unpinned",
        ]
        keepers = ["home/dot_codex/symlink_AGENTS.md.tmpl", "home/dot_local/bin/common/executable_tool"]
        for rel in [*orphans, *keepers, "scripts/orchestrator/unpinned"]:
            (self.temp_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.temp_dir / rel).write_text("x\n")
        expected.write_text("current\n")
        self.module.load_manifest = lambda _text=None: {}
        self.module.expected_outputs = lambda _manifest: {expected: "current\n"}
        self.addCleanup(setattr, sys, "argv", sys.argv)

        sys.argv = ["generate-agent-configs.py", "--check"]
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.main()
        for rel in orphans:
            self.assertIn(f"{rel} (orphan", stderr.getvalue())
        for rel in [*keepers, "home/dot_agents/omp/profiles/worker.yml.tmpl"]:
            self.assertNotIn(rel, stderr.getvalue())
        self.assertTrue(all((self.temp_dir / rel).exists() for rel in orphans), "--check deletes nothing")

        sys.argv = ["generate-agent-configs.py"]
        with contextlib.redirect_stdout(io.StringIO()):
            self.module.main()
        self.assertEqual([rel for rel in orphans if (self.temp_dir / rel).exists()], [])
        self.assertTrue(all((self.temp_dir / rel).exists() for rel in keepers))
        self.assertFalse((self.temp_dir / "home/dot_claude/skills/gone").exists())
        sys.argv = ["generate-agent-configs.py", "--check"]
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            self.module.main()
        self.assertIn("up to date", stdout.getvalue())

    def test_a_generated_file_chezmoi_ignores_is_refused(self) -> None:
        """F054: chezmoi skips a dot-prefixed source name, so a file generated under one never deploys."""
        hidden = self.temp_dir / "home/dot_agents/plugins/p/.codex-plugin/plugin.json"
        self.assertIsNone(self.module.chezmoi_target(hidden))
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.render_output_index({hidden: "{}\n"})
        self.assertIn("never deploys", stderr.getvalue())
        shown = self.temp_dir / "home/dot_agents/plugins/p/dot_codex-plugin/plugin.json"
        self.assertEqual(
            {"target": ".agents/plugins/p/.codex-plugin/plugin.json", "kind": "file", "executable": False},
            self.module.chezmoi_target(shown),
        )

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_every_indexed_target_is_what_chezmoi_deploys(self) -> None:
        """The output index's targets are exactly the entries chezmoi manages for the generated sources."""
        self.module.ROOT = ROOT
        index = json.loads((ROOT / "scripts/generated-agent-outputs.json").read_text())
        deployed = [entry for entry in index["outputs"] if entry["target"]]
        source, home = self.temp_dir / "source", self.temp_dir / "home"
        for entry in deployed:
            path = source / Path(entry["source"]).relative_to("home")
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / entry["source"], path)
        home.mkdir()
        (self.temp_dir / "chezmoi.toml").write_text("")
        run = subprocess.run(
            [
                *("chezmoi", "managed", "--include=files,symlinks", "--no-tty"),
                *("--source", str(source), "--destination", str(home), "--config", str(self.temp_dir / "chezmoi.toml")),
                *("--cache", str(self.temp_dir / "cache"), "--persistent-state", str(self.temp_dir / "state.boltdb")),
            ],
            env=os.environ | {"HOME": str(home)},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(0, run.returncode, run.stderr)
        self.assertEqual(sorted(entry["target"] for entry in deployed), sorted(run.stdout.split()))

    def test_sandbox_exclusions_render_only_git_push_and_gh_for_all_os(self) -> None:
        manifest = load_manifest_fixture(self.temp_dir)
        for os_name in ("darwin", "linux"):
            with self.subTest(os=os_name):
                self.assertEqual(
                    ["git push *", "gh *"], self.module.render_claude_sandbox(manifest, os_name)["excludedCommands"]
                )

    def test_managed_sandbox_exclusions_are_only_git_push_and_gh_for_all_os(self) -> None:
        template = (ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()
        for os_name in ("darwin", "linux"):
            with self.subTest(os=os_name):
                sandbox = self.render_claude_template(template, os_name)["sandbox"]
                self.assertEqual(["git push *", "gh *"], sandbox["excludedCommands"])
                self.assertIs(False, sandbox["allowUnsandboxedCommands"])

    def test_sandbox_validator_requires_strict_mode_and_the_allowlisted_exclusions(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "validate_agent_assets", ROOT / "scripts/validate-agent-assets.py"
        )
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        manifest = load_manifest_fixture(self.temp_dir)
        cases = [
            ({"excludedCommands": ["git push *", "gh *"]}, True),
            ({"excludedCommands": ["gh *", "git push *"]}, True),
        ]
        patterns = ["git *", "git push", "gh", "herdr *", "herdr-agents *", "actas-claim.sh *", "arbitrary *"]
        levers = ["~/.local/bin/common/hcom-seat *", "hcom *"]
        legacy = ["gh *", "herdr-agents *"]
        cases += [
            ({"excludedCommands": value}, False)
            for value in (
                None,
                False,
                0,
                "",
                {},
                (),
                [],
                [None],
                [""],
                ["git push *"],
                ["gh *"],
                ["git push *", "gh *", "gh *"],
                legacy,
                *(["git push *", "gh *", p] for p in patterns + levers),
            )
        ]
        cases += [({"allowUnsandboxedCommands": value}, False) for value in (True, None, "false", 0)]
        for os_name in ("darwin", "linux"):
            for patch, expected in cases:
                with self.subTest(os=os_name, patch=patch), contextlib.redirect_stderr(io.StringIO()):
                    sandbox = self.module.render_claude_sandbox(manifest, os_name)
                    sandbox.update(patch)
                    try:
                        validator.validate_claude_sandbox(
                            sandbox, manifest["codex"]["sandbox_workspace_write"]["writable_roots"], "sandbox", os_name
                        )
                    except SystemExit:
                        accepted = False
                    else:
                        accepted = True
                    self.assertEqual(expected, accepted)

    def test_audit_profile_renders_read_only_sandbox_override(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["audit"] = {
            "claude": {"model": "claude-fable-5-1", "effort": "high"},
            "codex": {
                "model": "gpt-6-astra",
                "model_reasoning_effort": "high",
                "sandbox_mode": "read-only",
            },
            "omp": {"model": "openai-siwc/gpt-6-astra", "effort": "xhigh"},
        }
        outputs = self.module.expected_outputs(manifest)
        self.module.write_outputs(outputs)

        def render(name: str) -> dict:
            path = self.temp_dir / f"home/dot_codex/modify_private_{name}.config.toml"
            result = subprocess.run(
                [sys.executable, str(path)],
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

    def test_model_profiles_reject_invalid_sandbox_mode(self) -> None:
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["codex"]["sandbox_mode"] = "readonly"

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.model_profiles(manifest)
        self.assertIn("standard.codex.sandbox_mode must be one of", stderr.getvalue())

    def test_model_profiles_reject_a_null_dsh_entry(self) -> None:
        # U172 round 3: a present `dsh: null` is a malformed entry, not an absent one (the renderer raised on it).
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["dsh"] = None

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.model_profiles(manifest)
        self.assertIn("standard.dsh must be a mapping of exactly model and route", stderr.getvalue())

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
            [sys.executable, str(standard_profile)],
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
            [sys.executable, str(standard_profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(self.temp_dir / "target-home")},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, current)

        agent_path = self.temp_dir / "home/dot_claude/agents/express-explorer.md"
        self.assertIn("model: haiku", outputs[agent_path])
        self.assertIn("effort: low", outputs[agent_path])

        project_map_path = self.temp_dir / "home/dot_claude/agents/project-map.md"
        self.assertIn("model: sonnet", outputs[project_map_path])
        self.assertIn("effort: high", outputs[project_map_path])
        self.assertIn("  - project-map\n", outputs[project_map_path])

        self.assertFalse([path for path in outputs if path.name == "ccgate.jsonnet"])

    def hook_trust_namespace(self, manifest: dict) -> dict:
        namespace = {"sys": sys, "Path": Path, "HOOK_TRUST": self.module.codex_hook_trust(manifest)}
        exec(self.module.HOOK_TRUST_CODE, namespace)
        return namespace

    def test_hook_trust_hash_reproduces_codex_current_hashes(self) -> None:
        # Values Codex 0.160.0 reported as current_hash (app-server hooks/list) on the operator's host.
        codex_hook_hash = self.hook_trust_namespace(sample_manifest())["codex_hook_hash"]
        notify = "/home/moriya/.local/bin/common/contextdb-codex-notify"
        for event, matcher, handler, expected in (
            (
                "permission_request",
                "*",
                {
                    "type": "command",
                    "command": "/home/moriya/.local/bin/common/permgate codex",
                    "timeout": 10,
                    "statusMessage": "Evaluating permission request",
                },
                "sha256:64d9851fb629f7cd5608706436fb5b8588dc60abf355893ebe3eaca401a9ff65",
            ),
            (
                "pre_compact",
                "*",
                {"type": "command", "command": notify, "timeout": 10, "statusMessage": "Recording to CompactionDB"},
                "sha256:daa1e215632e85e1b578f07ff0647c8f650d6d73f454c1089a74a6d354736edc",
            ),
            (
                "session_end",
                "*",
                {"type": "command", "command": notify, "timeout": 3, "statusMessage": "Recording to CompactionDB"},
                "sha256:14a8144bdb3ac2bfa907e5415009fe1e359bc5ce9f6a46300e9a249b31fffc05",
            ),
            # Codex drops a Stop hook's matcher before hashing.
            (
                "stop",
                "ignored",
                {
                    "type": "command",
                    "command": "crit plan-hook --mode codex",
                    "timeout": 345600,
                    "statusMessage": "Reviewing proposed plan with Crit",
                },
                "sha256:bf6ad428ae7902810fa2d68d8db42228377af118aa18508ad0eccf73a95ed1f8",
            ),
        ):
            with self.subTest(event=event):
                self.assertEqual(codex_hook_hash(event, matcher, handler), expected)

    def hook_trust_manifest(self) -> dict:
        manifest = sample_manifest()
        manifest["codex"]["hooks"]["state"] = {
            "{{ .chezmoi.homeDir }}/.codex/config.toml:permission_request:0:0": {"enabled": True},
            "demo@market:hooks/hooks.json:stop:0:0": {"trusted_hash": "sha256:pinned", "enabled": True},
        }
        return manifest

    def run_profile(self, manifest: dict, home: Path, current: str) -> subprocess.CompletedProcess:
        self.module.write_outputs(self.module.expected_outputs(manifest))
        return subprocess.run(
            [sys.executable, str(self.temp_dir / "home/dot_codex/modify_private_standard.config.toml")],
            input=current,
            text=True,
            capture_output=True,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

    def test_profile_modify_scripts_replace_declared_hook_trust_and_keep_undeclared(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        expected = self.hook_trust_namespace(manifest)["codex_hook_hash"](
            "permission_request",
            "*",
            {
                "type": "command",
                "command": "permgate codex",
                "timeout": 10,
                "statusMessage": "Evaluating permission request",
            },
        )
        operator_hooks = self.temp_dir / "elsewhere/hooks.json"
        operator_hooks.parent.mkdir()
        operator_hooks.write_text("{}")
        current = (
            f'[hooks.state]\n\n[hooks.state."{key}"]\ntrusted_hash = "sha256:stale"\n\n'
            f'[hooks.state."{operator_hooks}:stop:0:0"]\ntrusted_hash = "sha256:operator"\n'
        )

        result = self.run_profile(manifest, home, current)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f'[hooks.state."{key}"]\ntrusted_hash = "{expected}"\nenabled = true', result.stdout)
        self.assertNotIn("sha256:stale", result.stdout)
        self.assertIn('trusted_hash = "sha256:operator"', result.stdout)
        self.assertIn(f"replacing sha256:stale with {expected}", result.stderr)
        # A second apply is quiet and byte-identical.
        again = self.run_profile(manifest, home, result.stdout)
        self.assertEqual(again.stdout, result.stdout)
        self.assertNotIn("divergence", again.stderr)

    def test_profile_modify_scripts_trust_a_plugin_hook_only_at_its_pin(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = '[hooks.state."demo@market:hooks/hooks.json:stop:0:0"]'

        missing = self.run_profile(manifest, home, "")

        self.assertEqual(missing.returncode, 0, missing.stderr)
        self.assertIn(f'{key}\ntrusted_hash = "sha256:pinned"', missing.stdout)
        self.assertIn(
            "warning: cannot compute hook trust for demo@market:hooks/hooks.json:stop:0:0 (no installed copy",
            missing.stderr,
        )
        handler = {"type": "command", "command": "demo stop", "timeout": 5}
        plugin = home / ".codex/plugins/cache/market/demo/1.0/hooks/hooks.json"
        plugin.parent.mkdir(parents=True)
        plugin.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [handler]}]}}))
        installed = self.hook_trust_namespace(manifest)["codex_hook_hash"]("stop", None, handler)

        # The installed hook is not the pinned one: it stays untrusted, even over an entry that trusted it.
        changed = self.run_profile(manifest, home, f'[hooks.state]\n\n{key}\ntrusted_hash = "{installed}"\n')

        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertIn(f"{key}\nenabled = true\n", changed.stdout)
        self.assertNotIn(f'trusted_hash = "{installed}"', changed.stdout)
        self.assertIn(installed, changed.stderr)
        self.assertIn("sha256:pinned", changed.stderr)

        # Once the reviewed hash is the pin, the same hook is trusted.
        manifest["codex"]["hooks"]["state"]["demo@market:hooks/hooks.json:stop:0:0"]["trusted_hash"] = installed
        reviewed = self.run_profile(manifest, home, changed.stdout)

        self.assertEqual(reviewed.returncode, 0, reviewed.stderr)
        self.assertIn(f'{key}\ntrusted_hash = "{installed}"', reviewed.stdout)

    def test_plugin_hook_state_without_a_pin_is_refused(self) -> None:
        manifest = self.hook_trust_manifest()
        manifest["codex"]["hooks"]["state"]["demo@market:hooks/hooks.json:stop:0:0"] = {"enabled": True}

        with self.assertRaises(SystemExit):
            self.module.codex_hook_trust(manifest)

    def test_profile_modify_scripts_hash_the_plugin_version_codex_loads(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        codex_hook_hash = self.hook_trust_namespace(manifest)["codex_hook_hash"]
        root = home / ".codex/plugins/cache/market/demo"
        for version in ("1.9.0", "1.12.0", "1.12.0-rc.1"):
            plugin = root / version / "hooks/hooks.json"
            plugin.parent.mkdir(parents=True)
            plugin.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": version}]}]}}))
        key = '[hooks.state."demo@market:hooks/hooks.json:stop:0:0"]'
        state = manifest["codex"]["hooks"]["state"]["demo@market:hooks/hooks.json:stop:0:0"]
        for active in ("1.12.0", "local"):
            if active == "local":
                # Codex prefers a `local` copy over any released version.
                plugin = root / "local/hooks/hooks.json"
                plugin.parent.mkdir(parents=True)
                plugin.write_text(
                    json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "local"}]}]}})
                )
            with self.subTest(active=active):
                # Pinned to the copy Codex loads, the hook is trusted; any other copy would leave it untrusted.
                state["trusted_hash"] = codex_hook_hash("stop", None, {"type": "command", "command": active})
                result = self.run_profile(manifest, home, "")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(f'{key}\ntrusted_hash = "{state["trusted_hash"]}"', result.stdout)
                self.assertNotIn("demo@market", result.stderr)

    def test_active_plugin_version_matches_codex_on_symlinks_and_invalid_semver(self) -> None:
        namespace = self.hook_trust_namespace(sample_manifest())
        active_plugin_version = namespace["active_plugin_version"]
        root = self.temp_dir / "cache/market/demo"
        (root / "4.12.0").mkdir(parents=True)
        # Codex skips a symlinked version entry, so the real 4.12.0 stays active.
        (root / "local").symlink_to(root / "4.12.0")
        self.assertEqual(active_plugin_version(root), "4.12.0")
        # `1.10.0-01` is not semver (leading zero in a numeric pre-release identifier), so Codex
        # compares it lexically and 1.9.0 wins; a build identifier may keep its leading zero.
        compare = namespace["compare_plugin_versions"]
        self.assertGreater(compare("1.9.0", "1.10.0-01"), 0)
        self.assertGreater(compare("1.10.0+01", "1.9.0"), 0)
        other = self.temp_dir / "cache/market/other"
        for version in ("1.9.0", "1.10.0-01"):
            (other / version).mkdir(parents=True)
        self.assertEqual(active_plugin_version(other), "1.9.0")

    def test_plugin_versions_order_build_metadata_like_the_semver_crate(self) -> None:
        namespace = self.hook_trust_namespace(sample_manifest())
        compare = namespace["compare_plugin_versions"]
        # semver 1.0.27 BuildMetadata: empty < non-empty; numeric by stripped length, value, then length.
        self.assertGreater(compare("1.0.0+123", "1.0.0"), 0)
        self.assertGreater(compare("1.0.0+01", "1.0.0+1"), 0)
        self.assertLess(compare("1.0.0+0", "1.0.0+00"), 0)
        self.assertGreater(compare("1.0.0+a", "1.0.0+1"), 0)
        self.assertEqual(compare("1.0.0+1", "1.0.0+1"), 0)
        root = self.temp_dir / "cache/market/build"
        for version in ("1.0.0", "1.0.0+123"):
            (root / version).mkdir(parents=True)
        self.assertEqual(namespace["active_plugin_version"](root), "1.0.0+123")

    def test_profile_modify_scripts_replace_a_single_quoted_declared_entry(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        current = f"[hooks.state]\n\n[hooks.state.'{key}']\ntrusted_hash = \"sha256:stale\"\n"

        result = self.run_profile(manifest, home, current)

        self.assertEqual(result.returncode, 0, result.stderr)
        state = tomllib.loads(result.stdout)["hooks"]["state"]
        self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
        self.assertEqual(result.stdout.count(key), 1)
        self.assertIn("replacing sha256:stale with", result.stderr)

    def test_profile_modify_scripts_handle_table_headers_with_trailing_comments(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        others = (
            '[hooks.state."custom-hook"] # mine\ntrusted_hash = "sha256:custom"\n\n'
            f'[projects."{EXISTING_PROJECT}"]  # trusted\ntrust_level = "trusted"\n'
        )
        # A commented declared header, then an uncommented one followed by commented unrelated tables.
        for declared in (f'[hooks.state."{key}"] # declared', f'[hooks.state."{key}"]'):
            with self.subTest(declared=declared):
                current = f'[hooks.state]\n\n{declared}\ntrusted_hash = "sha256:stale"\n\n' + others

                result = self.run_profile(manifest, home, current)

                self.assertEqual(result.returncode, 0, result.stderr)
                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertEqual(result.stdout.count(key), 1)
                self.assertEqual(state["custom-hook"], {"trusted_hash": "sha256:custom"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertIn("replacing sha256:stale with", result.stderr)

    def test_profile_modify_scripts_keep_header_like_lines_inside_multiline_strings(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        current = '[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n\n' + MULTILINE_PROFILE

        result = self.run_profile(manifest, home, current)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(MULTILINE_PROFILE, result.stdout)
        merged = tomllib.loads(result.stdout)
        self.assertEqual(merged["agents"], tomllib.loads(MULTILINE_PROFILE)["agents"])
        self.assertEqual(merged["hooks"]["state"]["custom-hook"], {"enabled": True})

    def test_profile_modify_scripts_replace_inline_table_and_dotted_forms(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        for entry in (
            f'"{key}" = {{ trusted_hash = "sha256:stale", enabled = false }}\n',
            f'"{key}".trusted_hash = "sha256:stale"\n"{key}" . enabled = false\n',
        ):
            with self.subTest(entry=entry):
                current = (
                    f'[hooks.state]\n{entry}"other" = {{ trusted_hash = "sha256:other" }}\n\n'
                    f'[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
                )

                result = self.run_profile(manifest, home, current)

                self.assertEqual(result.returncode, 0, result.stderr)
                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertIs(state[key]["enabled"], True)
                self.assertEqual(state["other"], {"trusted_hash": "sha256:other"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertEqual(result.stderr.count("replacing sha256:stale with"), 1)
                self.assertNotIn("WARN", result.stderr)

    def test_profile_modify_scripts_treat_equivalent_hook_state_spellings_as_one_table(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        others = f'\n[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
        currents = [
            f'{parent}\n"{key}" = {{ trusted_hash = "sha256:stale", enabled = false }}\n'
            f'"other" = {{ trusted_hash = "sha256:other" }}\n' + others
            for parent in ("[hooks . state]", '["hooks"."state"]')
        ]
        currents.append(
            f'[hooks.state]\n"other" = {{ trusted_hash = "sha256:other" }}\n\n'
            f'[ hooks . state . "{key}" ]\ntrusted_hash = "sha256:stale"\n' + others
        )
        for current in currents:
            with self.subTest(current=current.splitlines()[0]):
                result = self.run_profile(manifest, home, current)

                self.assertEqual(result.returncode, 0, result.stderr)
                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertIs(state[key]["enabled"], True)
                self.assertEqual(state["other"], {"trusted_hash": "sha256:other"})
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertEqual(result.stdout.count(key), 1)
                self.assertEqual(result.stderr.count("replacing sha256:stale with"), 1)
                self.assertNotIn("WARN", result.stderr)

    def test_profile_modify_scripts_replace_declared_dotted_keys_under_hooks_and_at_the_root(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        key = f"{home}/.codex/config.toml:permission_request:0:0"
        others = f'\n[projects."{EXISTING_PROJECT}"]\ntrust_level = "trusted"\n'
        for current in (
            f'[hooks]\nstate."{key}".trusted_hash = "sha256:stale"\nstate . "{key}" . enabled = false\n' + others,
            f'hooks.state."{key}".trusted_hash = "sha256:stale"\n"hooks".state."{key}".enabled = false\n' + others,
        ):
            with self.subTest(current=current.splitlines()[0]):
                result = self.run_profile(manifest, home, current)

                self.assertEqual(result.returncode, 0, result.stderr)
                data = tomllib.loads(result.stdout)
                state = data["hooks"]["state"]
                self.assertNotEqual(state[key]["trusted_hash"], "sha256:stale")
                self.assertIs(state[key]["enabled"], True)
                self.assertEqual(data["projects"][EXISTING_PROJECT], {"trust_level": "trusted"})
                self.assertEqual(result.stdout.count(key), 1)
                self.assertEqual(result.stderr.count("replacing sha256:stale with"), 1)
                self.assertNotIn("WARN", result.stderr)

    def test_profile_modify_scripts_refuse_an_invalid_merge(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        self.module.write_outputs(self.module.expected_outputs(manifest))
        profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        # A splitter that emits every chunk twice stands in for any representation the merge mishandles.
        source = profile.read_text()
        broken = source.replace(
            "\nsys.stdout.write(merge_config(sys.stdin.read()))",
            "\n_split_chunks = split_chunks\nsplit_chunks = lambda text: _split_chunks(text) * 2\n"
            "sys.stdout.write(merge_config(sys.stdin.read()))",
        )
        self.assertNotEqual(broken, source)
        profile.write_text(broken)
        current = '[hooks.state]\n\n[hooks.state."custom-hook"]\nenabled = true\n\n[projects."/work"]\ntrust_level = "trusted"\n'

        result = subprocess.run(
            [sys.executable, str(profile)],
            input=current,
            text=True,
            capture_output=True,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("ERROR: codex config merge: the merged config is not valid TOML", result.stderr)

    def test_profile_modify_scripts_revoke_an_unpinned_plugin_hook_in_inline_and_dotted_forms(self) -> None:
        manifest = self.hook_trust_manifest()
        home = self.temp_dir / "target-home"
        handler = {"type": "command", "command": "demo stop", "timeout": 5}
        plugin = home / ".codex/plugins/cache/market/demo/1.0/hooks/hooks.json"
        plugin.parent.mkdir(parents=True)
        plugin.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [handler]}]}}))
        installed = self.hook_trust_namespace(manifest)["codex_hook_hash"]("stop", None, handler)
        key = "demo@market:hooks/hooks.json:stop:0:0"
        entry = f'"{key}" = {{ trusted_hash = "{installed}", enabled = true }}'
        for form, current in (
            ("inline table under [hooks]", f"[hooks]\nstate = {{ {entry} }}\n"),
            ("inline table at the root", f"hooks.state = {{ {entry} }}\n"),
            ("dotted keys under [hooks]", f'[hooks]\nstate."{key}".trusted_hash = "{installed}"\n'),
        ):
            with self.subTest(form=form):
                result = self.run_profile(manifest, home, current)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(tomllib.loads(result.stdout)["hooks"]["state"][key], {"enabled": True})
                self.assertNotIn(installed, result.stdout)

    def test_profile_modify_scripts_seed_base_hook_trust(self) -> None:
        outputs = self.module.expected_outputs(sample_manifest())
        standard_profile = self.temp_dir / "home/dot_codex/modify_private_standard.config.toml"
        self.module.write_outputs(outputs)
        home = self.temp_dir / "target-home"
        base = home / ".codex/config.toml"
        base.parent.mkdir(parents=True)
        hooks_file = home / ".codex/hooks.json"
        hooks_file.write_text("{}")
        base.write_text(f'[hooks.state]\n\n[hooks.state."{hooks_file}:stop:0:0"]\ntrusted_hash = "sha256:base"\n')

        result = subprocess.run(
            [sys.executable, str(standard_profile)],
            input=(
                f'[hooks.state]\n\n[hooks.state."{hooks_file}:session_start:0:0"]\ntrusted_hash = "sha256:profile"\n'
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
            [sys.executable, str(profile)],
            input=current,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "HOME": str(home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            "warning: hook trust divergence for hooks.state.hook: profile=sha256:profile base=sha256:base",
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
            [sys.executable, str(profile)],
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

    def test_an_empty_mcp_server_map_renders_no_tables(self) -> None:
        manifest = sample_manifest()
        self.assertEqual(manifest["mcp_servers"], {})

        self.assertNotIn("[mcp_servers.", self.module.render_codex(manifest))
        self.assertNotIn("enabledPlugins", json.loads(self.module.render_claude_settings(manifest)))

    def test_codex_command_hooks_render_after_permission_request_in_manifest_order(self) -> None:
        manifest = sample_manifest()
        manifest["codex"]["hooks"]["command_hooks"] = COMMAND_HOOKS

        config = self.module.render_codex(manifest)

        self.assertIn(COMMAND_HOOKS_TOML, config)
        self.assertLess(config.index("[[hooks.PermissionRequest]]"), config.index("[[hooks.PreCompact]]"))
        if "[hooks.state]" in config:
            self.assertLess(config.index("[[hooks.SessionEnd.hooks]]"), config.index("[hooks.state]"))
        tomllib.loads(config)

    def test_empty_or_missing_codex_command_hooks_render_no_table(self) -> None:
        baseline = self.module.render_codex(sample_manifest())
        manifest = sample_manifest()
        manifest["codex"]["hooks"]["command_hooks"] = []

        self.assertEqual(self.module.render_codex(manifest), baseline)
        self.assertEqual(baseline.count("[[hooks."), 2)  # PermissionRequest and its handler only.

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
        claude = self.render_claude_template((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text())
        manifest = load_manifest_fixture(self.temp_dir)
        command = manifest["claude"]["hooks"]["permission_request"]["command"]
        expected = self.render_claude_template(json.dumps({"command": command}))["command"]
        (group,) = claude["hooks"]["PermissionRequest"]
        (hook,) = group["hooks"]

        self.assertIn("{{ .chezmoi.homeDir }}/.local/bin/common/permgate codex", codex)
        self.assertEqual(hook["command"], expected)
        executable, argument = hook["command"].rsplit(" ", 1)
        self.assertEqual(Path(executable).name, "permgate")
        self.assertEqual(argument, "claude")

    def test_managed_codex_config_routes_compaction_and_session_end_to_compactiondb(self) -> None:
        hooks = tomllib.loads((ROOT / "home/.chezmoitemplates/codex-config-managed.toml").read_text())["hooks"]

        for event, timeout in (("PreCompact", 10), ("PostCompact", 10), ("SessionEnd", 3)):
            with self.subTest(event=event):
                (table,) = hooks[event]
                (handler,) = table["hooks"]
                self.assertEqual(table["matcher"], "*")
                self.assertEqual(handler["command"], "{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify")
                self.assertEqual(handler["timeout"], timeout)

    def test_managed_claude_settings_name_no_update_channel(self) -> None:
        """mise is the only version channel: no release channel and no dead `autoUpdates` key (regime-cutover U18)."""
        claude = self.render_claude_template((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text())
        self.assertNotIn("autoUpdatesChannel", claude)
        self.assertNotIn("autoUpdates", claude)

    def test_login_environments_block_every_claude_update_path(self) -> None:
        """Sourcing each managed login file exports DISABLE_UPDATES and DISABLE_AUTOUPDATER (regime-cutover U18)."""
        home = self.temp_dir / "home"
        home.mkdir()
        env = {"PATH": os.environ["PATH"], "HOME": str(home)}
        probe = 'printf "%s %s" "${DISABLE_UPDATES:-unset}" "${DISABLE_AUTOUPDATER:-unset}"'
        for shell, source in (
            ("zsh", ROOT / "home/dot_zshenv"),  # every zsh, client login shell and server bashrc's exec zsh
            ("bash", ROOT / "home/dot_profile"),  # ~/.profile, read by the server's bash login shell
        ):
            if not shutil.which(shell):
                self.fail(f"{shell} is required to source {source}")
            with self.subTest(file=source.name):
                result = subprocess.run(
                    [shell, "-c", f'. "{source}" > /dev/null 2>&1; {probe}'],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                self.assertEqual(result.stdout, "1 1", result.stderr)

    def test_managed_claude_settings_render_the_levers_and_the_regime_env(self) -> None:
        claude = self.render_claude_template((ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text())

        self.assertEqual(["git push *", "gh *"], claude["sandbox"]["excludedCommands"])
        self.assertEqual(MANAGED_ALLOW, claude["permissions"]["allow"])
        self.assertEqual("auto", claude["permissions"]["defaultMode"])
        # No session-wide bus: the store and team are per repository, derived by the levers (regime-cutover U33).
        self.assertNotIn("HCOM_DIR", claude["env"])
        self.assertNotIn("HCOM_TEAM", claude["env"])
        self.assertIn("~/.local/state/hcom-regime", claude["sandbox"]["filesystem"]["allowWrite"])
        self.assertIn("~/.local/state/omp-seats", claude["sandbox"]["filesystem"]["allowWrite"])
        manifest = load_manifest_fixture(self.temp_dir)
        self.assertEqual(
            [*manifest["claude"]["permissions"]["ask"], *self.module.claude_command_rules(manifest, "ask")],
            claude["permissions"]["ask"],
        )
        deny = claude["permissions"]["deny"]
        for rule in ("Bash(gh release *)", "Bash(pnpm publish *)", "Bash(terraform destroy *)", "Bash(/bin/rm -rf *)"):
            self.assertIn(rule, deny)

    def test_managed_codex_path_includes_installed_common_bin(self) -> None:
        codex = tomllib.loads((ROOT / "home/.chezmoitemplates/codex-config-managed.toml").read_text())

        path = codex["shell_environment_policy"]["set"]["PATH"].split(":")
        self.assertIn("{{ .chezmoi.homeDir }}/.local/bin/common", path)
        self.assertLess(
            path.index("{{ .chezmoi.homeDir }}/.local/bin"),
            path.index("{{ .chezmoi.homeDir }}/.local/bin/common"),
        )

    def test_the_herdr_agents_worker_era_keys_are_gone(self) -> None:
        # U40: nothing reads worker_kind, orchestrator_kind, worker_profile, worker_worktree or worker_cap since
        # U26 removed herdr-agents' worker modes, so the manifest drops them; U142 retired the launch fragment
        # (model-profiles.env) that once carried them, so the generator renders no HERDR_AGENTS_ line anywhere.
        keys = ("worker_kind", "orchestrator_kind", "worker_profile", "worker_worktree", "worker_cap")
        # The keys were top-level; read as text, as make unit-test has no PyYAML.
        text = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        for key in keys:
            with self.subTest(key=key):
                self.assertIsNone(re.search(rf"^{re.escape(key)}:", text, re.MULTILINE))
        self.assertFalse((ROOT / "home/dot_agents/model-profiles.env").exists())
        stale = sample_manifest() | {key: "x" for key in keys}
        for manifest in (sample_manifest(), stale):
            outputs = self.module.expected_outputs(manifest)
            self.assertNotIn(self.temp_dir / "home/dot_agents/model-profiles.env", outputs)
            for path, rendered in outputs.items():
                with self.subTest(path=str(path)):
                    self.assertNotIn("HERDR_AGENTS_", rendered)

    def test_unknown_interactive_profile_fails(self) -> None:
        manifest = sample_manifest()
        manifest["interactive_profile"] = "missing"

        with self.assertRaises(SystemExit):
            self.module.interactive_profile(manifest)

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

    def test_model_profiles_require_an_omp_model_from_the_provider_allowlist(self) -> None:
        refused = (
            "model profile standard.omp.model must be <provider>/<id> "
            "with provider claude-bridge, openai-siwc or anthropic"
        )
        retired = (
            "model profile standard.omp.model names the retired openai-codex route; "
            "use claude-bridge, openai-siwc or anthropic"
        )
        for value, message in (
            (None, "model profile standard is missing omp"),
            ("foo/bar", refused),
            ("openai/gpt-x", refused),
            ("anthropic/claude x", refused),
            ("anthropic/claude-x\n", refused),
            ("openai-codex/gpt-x", retired),
        ):
            with self.subTest(value=value):
                manifest = sample_manifest()
                if value is None:
                    del manifest["model_profiles"]["standard"]["omp"]
                else:
                    manifest["model_profiles"]["standard"]["omp"]["model"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.model_profiles(manifest)
                self.assertIn(message, stderr.getvalue())

        for value in ("claude-bridge/claude-x", "openai-siwc/gpt-x", "anthropic/claude-x"):
            with self.subTest(value=value):
                manifest = sample_manifest()
                manifest["model_profiles"]["standard"]["omp"]["model"] = value
                self.assertEqual(
                    self.module.model_profiles(manifest)["standard"]["omp"], {"model": value, "effort": "high"}
                )

    def test_model_profiles_require_an_omp_thinking_level_omp_accepts(self) -> None:
        for value in (None, "auto", "off", "XHIGH", "ultra", 3):
            with self.subTest(value=value):
                manifest = sample_manifest()
                if value is None:
                    del manifest["model_profiles"]["standard"]["omp"]["effort"]
                else:
                    manifest["model_profiles"]["standard"]["omp"]["effort"] = value
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.model_profiles(manifest)

    def test_omp_config_renders_the_interactive_profile_as_the_default_role(self) -> None:
        manifest = sample_manifest()
        path = self.temp_dir / "home/.chezmoitemplates/omp-config-managed.yml"
        header = f"# {self.module.GENERATED_HEADER}\n"
        skills = "skills:\n  enabled: true\n  customDirectories:\n    - ~/.agents/skills\n"
        pstack = "    - ~/.agents/pstack/skills\n  ignoredSkills: []\n"

        self.assertEqual(
            self.module.expected_outputs(manifest)[path],
            header
            + "modelRoles:\n  default: anthropic/sonnet\n"
            + skills
            + pstack
            + "extensions: []\ndisabledProviders: []\n"
            + "startup:\n  checkUpdate: false\n",
        )
        manifest["interactive_profile"] = "express"
        manifest["omp"]["skills_directories"] = ["~/.agents/skills", "/srv/skills"]
        manifest["omp"]["extensions"] = ["~/.agents/omp/extensions/openai-siwc", "/srv/omp-ext"]
        manifest["omp"]["disabled_providers"] = ["agent-plugins", "openai-codex"]
        text = self.module.expected_outputs(manifest)[path]
        self.assertEqual(
            text,
            header
            + "modelRoles:\n  default: openai-siwc/gpt-5.6-luna\n"
            + skills
            + "    - /srv/skills\n"
            + pstack
            + "extensions:\n  - ~/.agents/omp/extensions/openai-siwc\n  - /srv/omp-ext\n"
            + "disabledProviders:\n  - agent-plugins\n  - openai-codex\n"
            + "startup:\n  checkUpdate: false\n",
        )
        self.assertNotIn("ANTHROPIC", text)
        self.assertNotIn("OAUTH", text)

    def test_omp_update_check_follows_the_manifest_in_the_plain_config_and_every_overlay(self) -> None:
        """U94: omp's self-update refuses this install, so the startup nudge to run it is the manifest's to switch off."""
        profiles = self.temp_dir / "home/dot_agents/omp/profiles"
        plain = self.temp_dir / "home/.chezmoitemplates/omp-config-managed.yml"
        for value in (False, True):
            with self.subTest(check_update=value):
                manifest = sample_manifest()
                manifest["omp"]["check_update"] = value
                outputs = self.module.expected_outputs(manifest)
                line = f"  checkUpdate: {str(value).lower()}\n"
                self.assertIn(f"startup:\n{line}", outputs[plain])
                self.assertIn(f"startup:\n  setupWizard: false\n{line}", outputs[profiles / "worker.yml.tmpl"])
        for value in (None, "false", 0):
            with self.subTest(value=value):
                manifest = sample_manifest()
                if value is None:
                    del manifest["omp"]["check_update"]
                else:
                    manifest["omp"]["check_update"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.render_omp_config(manifest)
                self.assertIn("omp.check_update must be true or false", stderr.getvalue())

    def test_the_repository_manifest_switches_omps_update_check_off(self) -> None:
        # The committed manifest decides the deployed config: the pin is omp's only update path (U94).
        manifest = load_manifest_fixture(self.temp_dir)
        self.assertIs(False, manifest["omp"]["check_update"])

    def test_omp_extensions_must_be_a_list_of_home_or_absolute_paths(self) -> None:
        for value, message in (
            ("~/ext", "omp.extensions must be a list of extension directories"),
            ({"claude-bridge": "~/ext"}, "omp.extensions must be a list of extension directories"),
            (["ext"], "omp.extensions entries must be ~/ or absolute paths: 'ext'"),
            (["~/x; rm -rf"], "omp.extensions entries must be ~/ or absolute paths"),
            ([3], "omp.extensions entries must be ~/ or absolute paths: 3"),
        ):
            with self.subTest(value=value):
                manifest = sample_manifest()
                manifest["omp"]["extensions"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.render_omp_config(manifest)
                self.assertIn(message, stderr.getvalue())

    def test_skill_audience_refuses_unknown_empty_repeated_and_undeclared(self) -> None:
        (self.temp_dir / "home/dot_agents/skills/example").mkdir(parents=True)
        cases = (
            ({"example": ["claude", "cursor"]}, None, "skill example names unknown audience ['cursor']"),
            ({"example": []}, None, "skill example needs a non-empty audience list without repeats"),
            ({"example": ["codex", "codex"]}, None, "skill example needs a non-empty audience list without repeats"),
            ({"example": ["omp-audit"]}, None, "skill example names unknown audience ['omp-audit']"),
            ({"other": ["claude"]}, None, "not declared in skills.audience: ['example']"),
            ({"example": ["claude"]}, {"audience": ["codex"]}, "skills.pstack cannot name ['codex']"),
            ({"example": ["claude"]}, {"audience": ["omp"], "exclude": ["example"]}, "skills.audience declares"),
            ({"example": ["claude"]}, {"audience": []}, "skills.pstack needs a non-empty audience list"),
        )
        for audience, pstack, message in cases:
            with self.subTest(audience=audience, pstack=pstack):
                manifest = sample_manifest()
                manifest["skills"]["audience"] = audience
                if pstack is not None:
                    manifest["skills"]["pstack"] = pstack
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.expected_outputs(manifest)
                self.assertIn(message, stderr.getvalue())

    def test_each_agent_gets_only_the_skills_its_audience_names(self) -> None:
        for name in ("shared", "seat-only", "claude-only"):
            skill = self.temp_dir / f"home/dot_agents/skills/{name}/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(f"---\nname: {name}\ndescription: d\n---\n")
        manifest = sample_manifest()
        manifest["omp"]["roles"] = {"worker": "standard", "audit": "express"}
        manifest["skills"] = {
            "audience": {
                "shared": ["claude", "codex", "omp", "omp-worker"],
                "seat-only": ["omp-worker"],
                "claude-only": ["claude"],
                "installer-owned": ["omp"],
            },
            "pstack": {"audience": ["omp-worker"], "exclude": ["setup-pstack"]},
        }
        outputs = self.module.expected_outputs(manifest)

        codex = tomllib.loads(outputs[self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml"])
        self.assertEqual(
            [
                {"path": f"{{{{ .chezmoi.homeDir }}}}/.agents/skills/{name}/SKILL.md", "enabled": False}
                for name in ("claude-only", "installer-owned", "seat-only")
            ],
            codex["skills"]["config"],
        )
        plain = outputs[self.temp_dir / "home/.chezmoitemplates/omp-config-managed.yml"]
        self.assertIn(
            "skills:\n  enabled: true\n  customDirectories:\n    - ~/.agents/skills\n  ignoredSkills:\n    - claude-only\n    - seat-only\n",
            plain,
        )
        worker = outputs[self.temp_dir / "home/dot_agents/omp/profiles/worker.yml.tmpl"]
        self.assertIn(
            "    - {{ .chezmoi.homeDir }}/.agents/pstack/skills\n"
            "  ignoredSkills:\n    - claude-only\n    - installer-owned\n    - setup-pstack\n",
            worker,
        )
        audit = outputs[self.temp_dir / "home/dot_agents/omp/profiles/audit.yml.tmpl"]
        self.assertIn("skills:\n  enabled: false\n", audit)
        links = sorted(
            {
                path.relative_to(self.temp_dir / "home/dot_claude/skills").parts[0]
                for path in outputs
                if self.temp_dir / "home/dot_claude/skills" in path.parents
            }
        )
        self.assertEqual(["claude-only", "shared"], links)
        removals = outputs[self.temp_dir / "home/.chezmoiremove"]
        self.assertIn(
            self.module.SKILL_REMOVALS_BEGIN + ".claude/skills/seat-only\n" + self.module.SKILL_REMOVALS_END, removals
        )
        index = json.loads(outputs[self.temp_dir / "scripts/generated-agent-outputs.json"])["skills"]
        self.assertEqual(["claude-only", "installer-owned", "seat-only"], index["codex_disabled"])
        self.assertEqual({"enabled": False, "pstack": False, "ignored": []}, index["omp"]["omp-audit"])
        self.assertEqual(
            {"enabled": True, "pstack": True, "ignored": ["claude-only", "installer-owned", "setup-pstack"]},
            index["omp"]["omp-worker"],
        )

        # A skill given back to Claude Code leaves the removal block; one that loses it enters.
        self.module.write_exact(self.temp_dir / "home/.chezmoiremove", removals)
        manifest["skills"]["audience"]["seat-only"] = ["claude", "omp-worker"]
        manifest["skills"]["audience"]["shared"] = ["codex"]
        removals = self.module.expected_outputs(manifest)[self.temp_dir / "home/.chezmoiremove"]
        self.assertIn(
            self.module.SKILL_REMOVALS_BEGIN + ".claude/skills/shared\n" + self.module.SKILL_REMOVALS_END, removals
        )

    def test_omp_skills_directories_must_be_home_or_absolute_paths(self) -> None:
        for value in (None, [], "~/.agents/skills", ["skills"], ["~"], ["~other/skills"], ["/"], ["~/x; rm -rf"], [3]):
            with self.subTest(value=value):
                manifest = sample_manifest()
                if value is None:
                    del manifest["omp"]
                else:
                    manifest["omp"]["skills_directories"] = value
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.render_omp_config(manifest)

    def test_omp_role_overlays_render_one_file_per_role_from_the_mapped_profile(self) -> None:
        manifest = sample_manifest()
        manifest["omp"]["roles"] = {"worker": "standard", "audit": "express"}
        manifest["omp"]["skills_directories"] = ["~/.agents/skills", "/srv/skills"]
        profiles = self.temp_dir / "home/dot_agents/omp/profiles"
        header = f"# {self.module.GENERATED_HEADER}\n"
        skills = (
            "skills:\n  enabled: true\n  customDirectories:\n    - {{ .chezmoi.homeDir }}/.agents/skills\n    - /srv/skills\n"
            "    - {{ .chezmoi.homeDir }}/.agents/pstack/skills\n  ignoredSkills: []\n"
        )
        wizard = "setupVersion: 2\nstartup:\n  setupWizard: false\n  checkUpdate: false\n"

        overlays = {
            path.name: text for path, text in self.module.expected_outputs(manifest).items() if path.parent == profiles
        }

        self.assertEqual(sorted(overlays), ["audit.yml.tmpl", "worker.yml.tmpl"])
        self.assertEqual(
            overlays["worker.yml.tmpl"],
            header + "modelRoles:\n  default: anthropic/sonnet\n" + skills + "defaultThinkingLevel: high\n" + wizard,
        )
        # No skill names omp-audit, so the audit role's overlay loads none at all.
        self.assertEqual(
            overlays["audit.yml.tmpl"],
            header
            + "modelRoles:\n  default: openai-siwc/gpt-5.6-luna\n"
            + "skills:\n  enabled: false\n"
            + "defaultThinkingLevel: low\n"
            + wizard,
        )
        self.assertEqual(
            execute_chezmoi_template(overlays["worker.yml.tmpl"], self.temp_dir),
            header
            + "modelRoles:\n  default: anthropic/sonnet\n"
            + skills.replace("{{ .chezmoi.homeDir }}", "/render-home")
            + "defaultThinkingLevel: high\n"
            + wizard,
        )

    def test_omp_role_overlays_switch_off_the_disabled_providers(self) -> None:
        manifest = sample_manifest()
        manifest["omp"]["disabled_providers"] = ["agent-plugins"]
        overlay = self.module.expected_outputs(manifest)[self.temp_dir / "home/dot_agents/omp/profiles/worker.yml.tmpl"]

        self.assertEqual(
            overlay,
            f"# {self.module.GENERATED_HEADER}\n"
            "modelRoles:\n  default: anthropic/sonnet\n"
            "skills:\n  enabled: true\n  customDirectories:\n    - {{ .chezmoi.homeDir }}/.agents/skills\n"
            "    - {{ .chezmoi.homeDir }}/.agents/pstack/skills\n  ignoredSkills: []\n"
            "defaultThinkingLevel: high\n"
            "disabledProviders:\n  - agent-plugins\n"
            "setupVersion: 2\nstartup:\n  setupWizard: false\n  checkUpdate: false\n",
        )

    def test_only_the_seat_overlays_switch_off_the_seat_providers(self) -> None:
        """U66 F005: seat_disabled_providers reach every role overlay after the shared list, never the plain config."""
        manifest = sample_manifest()
        manifest["omp"]["disabled_providers"] = ["agent-plugins"]
        manifest["omp"]["seat_disabled_providers"] = ["native", "agent-plugins", "mcp-json"]
        outputs = self.module.expected_outputs(manifest)

        for role in manifest["omp"]["roles"]:
            with self.subTest(role=role):
                overlay = outputs[self.temp_dir / f"home/dot_agents/omp/profiles/{role}.yml.tmpl"]
                self.assertIn("disabledProviders:\n  - agent-plugins\n  - native\n  - mcp-json\nsetupVersion", overlay)
        plain = outputs[self.temp_dir / "home/.chezmoitemplates/omp-config-managed.yml"]
        self.assertIn("disabledProviders:\n  - agent-plugins\n", plain)
        self.assertNotIn("native", plain)
        manifest["omp"]["seat_disabled_providers"] = ["claude-bridge"]
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.expected_outputs(manifest)
        self.assertIn("omp.seat_disabled_providers must not name the model route claude-bridge", stderr.getvalue())

    def test_omp_disabled_providers_refuse_non_ids_and_model_routes(self) -> None:
        for value, message in (
            ("agent-plugins", "omp.disabled_providers must be a list of omp provider ids"),
            ([3], "omp.disabled_providers entries must be omp provider ids: 3"),
            (["Agent Plugins"], "omp.disabled_providers entries must be omp provider ids: 'Agent Plugins'"),
            (["claude-bridge"], "must not name the model route claude-bridge; disabledProviders turns it off"),
            (["openai-siwc"], "must not name the model route openai-siwc; disabledProviders turns it off"),
            (["anthropic"], "must not name the model route anthropic; disabledProviders turns it off"),
        ):
            with self.subTest(value=value):
                manifest = sample_manifest()
                manifest["omp"]["disabled_providers"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.expected_outputs(manifest)
                self.assertIn(message, stderr.getvalue())

    def test_the_model_route_set_is_the_route_regex_alternation(self) -> None:
        alternation = re.fullmatch(r"\^\(([a-z|-]+)\)/.*", self.module.OMP_MODEL_RE.pattern)

        self.assertIsNotNone(alternation, self.module.OMP_MODEL_RE.pattern)
        self.assertEqual(sorted(alternation.group(1).split("|")), sorted(self.module.OMP_MODEL_ROUTES))

    def test_omp_roles_must_map_launcher_safe_roles_to_model_profiles(self) -> None:
        for value in (None, {}, "worker", ["worker"], {"worker": "nope"}, {"Worker-1": "standard"}, {"worker": 3}):
            with self.subTest(value=value):
                manifest = sample_manifest()
                if value is None:
                    del manifest["omp"]["roles"]
                else:
                    manifest["omp"]["roles"] = value
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.expected_outputs(manifest)

    def test_every_seat_policy_role_has_a_committed_omp_overlay(self) -> None:
        roles = load_manifest_fixture(self.temp_dir)["omp"]["roles"]
        policies = {path.stem for path in (ROOT / "home/dot_agents/omp/policies").glob("*.yml")}

        self.assertTrue(policies)
        self.assertLessEqual(policies, set(roles))
        for role in roles:
            self.assertTrue((ROOT / "home/dot_agents/omp/profiles" / f"{role}.yml.tmpl").is_file(), role)

    def test_omp_gateway_role_overlay_carries_the_bridge_route_the_extension_and_the_seat_providers_off(self) -> None:
        """U310: the dsh role's profile config, placed by hcom-seat as `~/.omp/profiles/dsh/agent/config.yml`, names the
        gateway route of the profile's dsh model, the bridge extension directory of omp.extension_providers (the home
        through the chezmoi template, as the seat overlays carry it), the seat providers off, skills off and the seat
        overlays' wizard and update rows; a key that is a seat role too, a profile without a dsh entry and a missing
        extension_providers row each refuse."""
        manifest = sample_manifest()
        manifest["model_profiles"]["standard"]["dsh"] = {"model": "claude-opus-5-5", "route": "omp-gateway"}
        manifest["omp"]["gateway_roles"] = {"dsh": "standard"}
        manifest["omp"]["extension_providers"] = {"claude-bridge": "~/.local/lib/omp-extensions/pi-claude-bridge"}
        manifest["omp"]["disabled_providers"] = ["agent-plugins"]
        manifest["omp"]["seat_disabled_providers"] = ["native", "mcp-json"]
        overlay = self.module.render_omp_gateway_overlay(manifest, "dsh")

        self.assertEqual(
            overlay,
            f"# {self.module.GENERATED_HEADER}\n"
            "modelRoles:\n  default: claude-bridge/claude-opus-5-5\n"
            "skills:\n  enabled: false\n"
            "extensions:\n  - {{ .chezmoi.homeDir }}/.local/lib/omp-extensions/pi-claude-bridge\n"
            "disabledProviders:\n  - agent-plugins\n  - native\n  - mcp-json\n"
            "setupVersion: 2\nstartup:\n  setupWizard: false\n  checkUpdate: false\n",
        )
        self.assertIn(
            "extensions:\n  - /render-home/.local/lib/omp-extensions/pi-claude-bridge\n",
            execute_chezmoi_template(overlay, self.temp_dir),
        )
        for change, message in (
            ({"roles": {"dsh": "standard"}}, "omp.gateway_roles.dsh is a seat role too"),
            ({"gateway_roles": {"dsh": "express"}}, "names 'express', which carries no dsh entry"),
            ({"gateway_roles": {"Dsh": "standard"}}, "omp.gateway_roles key is not launcher-safe: 'Dsh'"),
            ({"gateway_roles": {"dsh": "nope"}}, "omp.gateway_roles.dsh must name a model profile: 'nope'"),
            ({"gateway_roles": ["dsh"]}, "omp.gateway_roles must be a mapping"),
            ({"extension_providers": {"openai-siwc": "~/x"}}, "must name the extension directory of claude-bridge"),
            ({"extension_providers": {"claude-bridge": "relative/dir"}}, "must name the extension directory"),
        ):
            with self.subTest(change=change):
                broken = sample_manifest()
                broken["model_profiles"]["standard"]["dsh"] = {"model": "claude-opus-5-5", "route": "omp-gateway"}
                broken["omp"]["gateway_roles"] = {"dsh": "standard"}
                broken["omp"]["extension_providers"] = {"claude-bridge": "~/.local/lib/omp-extensions/pi-claude-bridge"}
                broken["omp"].update(change)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.render_omp_gateway_overlay(broken, "dsh")
                self.assertIn(message, stderr.getvalue())

    def test_the_manifest_renders_the_dsh_gateway_overlay_with_the_allow_listed_bridge(self) -> None:
        """U310: the committed manifest's gateway role is dsh, its overlay is a committed output, its route is the
        gateway provider on the interactive profile's dsh model (the thak profile's agent-default-model, so the child
        answers the model the harness asks for), and its one extension entry is the bridge row of the lever's
        allow-list claude.levers.extensions, which hcom-seat holds the placed entry to."""
        manifest = load_manifest_fixture(self.temp_dir)
        self.module.ROOT = ROOT
        roles = self.module.omp_gateway_roles(manifest)
        self.assertEqual(roles, {"dsh": "deep"})
        self.assertEqual(roles["dsh"], manifest["interactive_profile"])
        expected = self.module.expected_outputs(manifest)
        path = ROOT / "home/dot_agents/omp/profiles/dsh.yml.tmpl"
        self.assertIn(path, expected)
        self.assertEqual(path.read_text(), expected[path])
        text = expected[path]
        dsh_model = manifest["model_profiles"][manifest["interactive_profile"]]["dsh"]["model"]
        header = f"# {self.module.GENERATED_HEADER}\nmodelRoles:\n  default: claude-bridge/{dsh_model}\n"
        self.assertTrue(text.startswith(header + "skills:\n  enabled: false\nextensions:\n"), text)
        allow_list = manifest["claude"]["levers"]["extensions"]
        bridge = manifest["omp"]["extension_providers"]["claude-bridge"]
        self.assertIn(bridge, allow_list)
        self.assertIn(
            f"extensions:\n  - {bridge.replace('~', '{{ .chezmoi.homeDir }}', 1)}\ndisabledProviders:\n", text
        )
        disabled = "".join(f"  - {provider}\n" for provider in self.module.omp_seat_disabled_providers(manifest))
        tail = f"disabledProviders:\n{disabled}setupVersion: 2\nstartup:\n  setupWizard: false\n  checkUpdate: false\n"
        self.assertTrue(text.endswith(tail), text)
        # The seat overlays are what they were: the gateway row adds a file and changes none of theirs.
        for role in manifest["omp"]["roles"]:
            self.assertNotIn("extensions:", expected[ROOT / "home/dot_agents/omp/profiles" / f"{role}.yml.tmpl"])

    def test_the_router_profile_runs_its_subagents_through_acp_seat_and_the_thak_profile_does_not(self) -> None:
        """U434 (M-22 Part B, table row s21): the rendered router patch inserts `subagent-acp`, the pinned tree's
        out-of-process ACP backend, whose command is the installed `acp-seat` (the broker's thin client, run inside
        the Router's sandbox by its absolute path under HOME) with exactly four args: the launch's socket read from
        `ACP_BROKER_SOCK` (hcom-seat's router row sets it) and the fixed name `router`; `tool-subagent` is repointed
        to that provider as a row of the list, before the insert. The thak patch holds neither row."""
        manifest = load_manifest_fixture(self.temp_dir)
        self.module.ROOT = ROOT
        router = self.module.render_dsh_router_profile(manifest)[ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"]
        thak = self.module.render_dsh_profile_patch(manifest)[ROOT / "home/dot_dsh/profiles/thak/cordis.patch.yml"]
        self.assertIn(
            "    - id: subagent-acp\n"
            "      name: '@deepseek-ai/dsh-subagent-acp'\n"
            "      config:\n"
            "        providerName: acp\n"
            "        command: !!js process.env.HOME + '/.local/bin/common/acp-seat'\n"
            "        args:\n"
            "          - --socket\n"
            "          - !!js process.env.ACP_BROKER_SOCK\n"
            "          - --name\n"
            "          - router\n"
            "        permission: allow\n"
            "        env: {}\n",
            router,
        )
        self.assertEqual(1, router.count("- id: subagent-acp\n"))
        block = re.search(r"    - id: subagent-acp\n(?:      .*\n)+", router)
        self.assertIsNotNone(block)
        args = re.search(r"        args:\n((?:          - .*\n)+)", block[0])
        self.assertIsNotNone(args)
        self.assertEqual(
            ["--socket", "!!js process.env.ACP_BROKER_SOCK", "--name", "router"],
            [line.strip().removeprefix("- ") for line in args[1].splitlines()],
        )
        self.assertIn(
            "- id: tool-subagent\n"
            "  disabled: false\n"
            "  config:\n"
            "    provider: acp\n"
            "    toolName: subagent\n"
            "    maxDepth: provider-managed\n",
            router,
        )
        # One top-level row; U466 adds the worker preset's nested `tool-subagent` row (ten spaces in), the same keys.
        self.assertEqual(1, len(re.findall(r"^- id: tool-subagent\n", router, re.MULTILINE)))
        self.assertEqual(1, len(re.findall(r"^          - id: tool-subagent\n", router, re.MULTILINE)))
        self.assertLess(router.index("- id: tool-subagent\n"), router.index("- insert:\n"))
        self.assertNotIn("subagent-acp", thak)
        self.assertNotIn("tool-subagent", thak)
        self.assertNotIn("ACP_BROKER_SOCK", thak)
        # The rows render from constants beside the gateway's, and the client they name is an installed, pinned lever.
        self.assertEqual("@deepseek-ai/dsh-subagent-acp", self.module.DSH_SUBAGENT_ACP_PLUGIN)
        self.assertEqual("~/.local/bin/common/acp-seat", self.module.DSH_ACP_SEAT_PATH)
        self.assertEqual("ACP_BROKER_SOCK", self.module.DSH_ACP_BROKER_SOCK_ENV)
        self.assertIn("acp-seat", manifest["claude"]["levers"]["sha256"])

    def test_the_router_patch_enables_the_subagent_tool_the_web_app_bundle_disables_and_the_thak_patch_has_no_row(
        self,
    ) -> None:
        """U434c (round 3 of U434; verdicts/U434-1faa81f1 P1 [f5 s8]): the web-app bundle ships the top-level
        `tool-subagent` row `disabled: true` (the round-1 dump), and the patch algorithm merges a row's keys other
        than `config`, so the rendered router row carries `disabled: false` directly under the row beside its ACP
        config; the round-1 real run needed an overlay for that one key. The thak patch has no `tool-subagent` row."""
        manifest = load_manifest_fixture(self.temp_dir)
        self.module.ROOT = ROOT
        router = self.module.render_dsh_router_profile(manifest)[ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"]
        thak = self.module.render_dsh_profile_patch(manifest)[ROOT / "home/dot_dsh/profiles/thak/cordis.patch.yml"]
        row = re.search(r"^- id: tool-subagent\n((?:  .*\n)+)", router, re.MULTILINE)
        self.assertIsNotNone(row, router)
        keys = [line[2:] for line in row[1].splitlines() if not line.startswith("    ")]
        self.assertEqual(["disabled: false", "config:"], keys, "the row's own keys, the enable beside the config")
        self.assertIn("    provider: acp\n", row[1])
        self.assertEqual(1, len(re.findall(r"^  disabled: false\n", router, re.MULTILINE)), router)
        self.assertNotIn("tool-subagent", thak)

    def test_the_router_patch_puts_the_worker_presets_subagent_tool_on_the_acp_provider_and_the_thak_patch_does_not(
        self,
    ) -> None:
        """U466 (U437's work, table row i8): the Executor Session's preset `dsh-superagent-worker` carries its own nested
        `tool-subagent` row with `provider: spawn` in the pinned plugin's bundle layer, and the include plugin's patch
        algorithm indexes rows by id at the top level and inside `group: true` rows alone (vendor/include/src/index.ts
        `buildMap`), so no patch reaches the nested row by id (measured, /tmp/u466/prototype.txt: `entry ... not found`,
        `is not a group`). The kit's form is its own row set for the preset row `dsh-superagent-worker-preset`: the
        rendered router patch carries that one preset row, whose `delegation` group's `tool-subagent` config is exactly
        the three keys the base agent's row carries (one constant), no `provider: spawn` stands anywhere in the router
        patch, the router preset is not restated, and the thak patch carries no preset row."""
        manifest = load_manifest_fixture(self.temp_dir)
        self.module.ROOT = ROOT
        router = self.module.render_dsh_router_profile(manifest)[ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"]
        thak = self.module.render_dsh_profile_patch(manifest)[ROOT / "home/dot_dsh/profiles/thak/cordis.patch.yml"]
        preset = re.search(r"^- id: dsh-superagent-worker-preset\n((?:  .*\n)+)", router, re.MULTILINE)
        self.assertIsNotNone(preset, router)
        self.assertEqual(1, router.count("- id: dsh-superagent-worker-preset\n"))
        keys = [line[2:] for line in preset[1].splitlines() if not line.startswith("    ")]
        self.assertEqual(["config:"], keys, "the preset row's own keys: the config alone (replaced whole by the patch)")
        self.assertIn("    id: dsh-superagent-worker\n", preset[1])
        delegation = re.search(r"^      - id: delegation\n((?:        .*\n)+)", preset[1], re.MULTILINE)
        self.assertIsNotNone(delegation, preset[1])
        nested = re.search(
            r"^          - id: tool-subagent\n            name: '@deepseek-ai/dsh-tool-subagent'\n            config:\n"
            r"((?:              .*\n)+)",
            delegation[1],
            re.MULTILINE,
        )
        self.assertIsNotNone(nested, delegation[1])
        three = ["provider: acp", "toolName: subagent", "maxDepth: provider-managed"]
        self.assertEqual(three, [line.strip() for line in nested[1].splitlines()])
        base = re.search(r"^- id: tool-subagent\n  disabled: false\n  config:\n((?:    .*\n)+)", router, re.MULTILINE)
        self.assertIsNotNone(base, router)
        self.assertEqual(three, [line.strip() for line in base[1].splitlines()], "one source for both rows")
        self.assertEqual(three, [f"{key}: {value}" for key, value in self.module.DSH_SUBAGENT_TOOL_CONFIG])
        self.assertNotIn("provider: spawn", router)
        self.assertNotIn("agentPreset:", router)
        self.assertNotIn("dsh-superagent-router-preset", router)
        self.assertNotIn("'@deepseek-ai/dsh-agent-preset'", router, "the row is addressed by id; no plugin name")
        self.assertLess(router.index("- id: tool-subagent\n"), router.index("- id: dsh-superagent-worker-preset\n"))
        self.assertLess(router.index("- id: dsh-superagent-worker-preset\n"), router.index("- insert:\n"))
        self.assertNotIn("preset", thak)
        self.assertNotIn("tool-subagent", thak)

    def test_the_router_profile_declares_the_acp_plugin_as_a_link_dependency_and_the_thak_profile_does_not(
        self,
    ) -> None:
        """U434b (round 2 of U434; verdicts/U434-8c3cfec2 P1 [f8 s6]): the package the `subagent-acp` insert names is
        a `link:` dependency of the rendered router package.json, the path from `$DSH_HOME/profiles/router` through
        the `dsh/current` link to the pinned tree's built package, so the updater's profile install resolves it on a
        deploy without a hand-made link; the insert's name and the dependency's name are one constant beside the
        gateway's; the thak package.json declares no such row."""
        manifest = load_manifest_fixture(self.temp_dir)
        self.module.ROOT = ROOT
        router = self.module.render_dsh_router_profile(manifest)
        package = json.loads(router[ROOT / "home/dot_dsh/profiles/router/package.json"])
        link = "link:../../dsh/current/packages/subagent/subagent-acp"
        self.assertEqual(
            {
                "dsh-superagent": "link:../../plugins/dsh-superagent",
                "dsh-omp-gateway": "link:../../plugins/omp-gateway",
                "@deepseek-ai/dsh-subagent-acp": link,
            },
            package["dependencies"],
        )
        insert = re.search(
            r"    - id: subagent-acp\n      name: '([^']+)'\n",
            router[ROOT / "home/dot_dsh/profiles/router/cordis.patch.yml"],
        )
        self.assertIsNotNone(insert)
        self.assertIn(insert[1], package["dependencies"], "the insert names a package the profile declares")
        self.assertEqual(self.module.DSH_SUBAGENT_ACP_PLUGIN, insert[1])
        self.assertEqual(link, self.module.DSH_SUBAGENT_ACP_LINK)
        self.assertEqual(link, package["dependencies"][self.module.DSH_SUBAGENT_ACP_PLUGIN])
        thak = json.loads(
            self.module.render_dsh_profile_patch(manifest)[ROOT / "home/dot_dsh/profiles/thak/package.json"]
        )
        self.assertNotIn("@deepseek-ai/dsh-subagent-acp", thak["dependencies"])
        self.assertNotIn("subagent-acp", json.dumps(thak))

    def test_manifest_adds_one_allowlisted_omp_model_per_profile_and_nothing_else(self) -> None:
        manifest = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        profiles: dict[str, list[str]] = {}
        current = None
        in_profiles = False
        for line in manifest.splitlines():
            if not line.startswith(" "):
                in_profiles = line == "model_profiles:"
                continue
            if in_profiles and (header := re.fullmatch(r"  ([a-z][a-z0-9_]*):", line)):
                current = header[1]
                profiles[current] = []
            elif in_profiles and line.startswith("    omp:"):
                profiles[current].append(line)

        self.assertEqual(sorted(profiles), ["audit", "deep", "express", "review", "security", "standard"])
        for name, lines in profiles.items():
            with self.subTest(profile=name):
                self.assertEqual(len(lines), 1)
                value = re.fullmatch(r'    omp: \{ model: "([^"]+)", effort: ([a-z]+) \}', lines[0])
                self.assertIsNotNone(value)
                self.assertIsNotNone(self.module.OMP_MODEL_RE.fullmatch(value[1]))
                self.assertIn(value[2], self.module.OMP_THINKING_LEVELS)

        base = subprocess.run(
            ["git", "-C", str(ROOT), "show", "origin/main:home/dot_agents/agent-config.yaml"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(base.returncode, 0, base.stderr)
        if sum(line.startswith("    omp:") for line in base.stdout.splitlines()) == 6:
            self.skipTest("origin/main already carries the six omp mappings")
        stripped = "".join(line for line in manifest.splitlines(keepends=True) if not line.startswith("    omp:"))
        self.assertEqual(stripped, base.stdout)

    def test_claude_settings_render_the_format_hook_from_its_path(self) -> None:
        settings = self.module.json.loads(self.module.render_claude_settings(sample_manifest()))
        self.assertEqual(
            settings["hooks"]["PostToolUse"],
            [
                {
                    "matcher": "Write|Edit",
                    "hooks": [
                        {"type": "command", "command": "~/.claude/hooks/format-edited-files.py"},
                        {"type": "command", "command": "~/.claude/hooks/project-map-reload.sh"},
                    ],
                }
            ],
        )

        manifest = sample_manifest()
        del manifest["claude"]["hooks"]["format_edited_files_hook"]
        del manifest["claude"]["hooks"]["project_map_reload_hook"]
        settings = self.module.json.loads(self.module.render_claude_settings(manifest))
        self.assertEqual(settings["hooks"]["PostToolUse"], [{"matcher": "Write|Edit", "hooks": []}])

    def test_project_map_reload_hook_renders_into_post_tool_use(self) -> None:
        manifest = sample_manifest()
        settings = json.loads(self.module.render_claude_settings(manifest))
        self.assertEqual(
            settings["hooks"]["PostToolUse"],
            [
                {
                    "matcher": "Write|Edit",
                    "hooks": [
                        {"type": "command", "command": "~/.claude/hooks/format-edited-files.py"},
                        {"type": "command", "command": "~/.claude/hooks/project-map-reload.sh"},
                    ],
                }
            ],
        )
        del manifest["claude"]["hooks"]["project_map_reload_hook"]
        settings = json.loads(self.module.render_claude_settings(manifest))
        self.assertEqual(
            settings["hooks"]["PostToolUse"],
            [
                {
                    "matcher": "Write|Edit",
                    "hooks": [
                        {"type": "command", "command": "~/.claude/hooks/format-edited-files.py"},
                    ],
                }
            ],
        )

    def test_project_map_reload_hook_acts_only_on_the_map_and_never_fails(self) -> None:
        hook = ROOT / "home/dot_claude/hooks/executable_project-map-reload.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            browser_calls = root / "browser-calls"
            agent_calls = root / "agent-calls"
            listing_file = root / "listing.json"
            browser = root / "terminal-browser"
            browser.write_text(
                "#!/bin/bash\n"
                'printf \'%s\\n\' "$*" >> "$BROWSER_CALLS"\n'
                'if [[ "$LIST_FAIL" == 1 ]]; then echo "listing failed" >&2; exit 1; fi\n'
                '/bin/cat "$LISTING"\n'
            )
            browser.chmod(0o755)
            agent = root / "agent-browser"
            agent.write_text(
                "#!/bin/bash\n"
                'printf \'%s\\n\' "$@" >> "$AGENT_CALLS"\n'
                'if [[ "$5" == "$AGENT_FAIL_ON" || "$6" == "$AGENT_FAIL_ON" ]]; then echo "agent failed" >&2; exit 1; fi\n'
                'echo "agent output"\n'
            )
            agent.chmod(0o755)
            jq = JQ
            self.assertIsNotNone(jq)
            (root / "jq").symlink_to(jq)
            (root / "python3").symlink_to(sys.executable)
            jq_only = root / "jq-only"
            jq_only.mkdir()
            (jq_only / "jq").symlink_to(jq)
            (jq_only / "python3").symlink_to(sys.executable)
            map_path = str(root / ".project-map/index.html")
            map_tab = {
                "id": 7,
                "url": "file://" + map_path,
                "active": False,
                "targetId": "4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3",
            }
            other_tab = {"id": 1, "url": "https://example.com/", "active": True, "targetId": "OTHER-TARGET"}
            listing = {
                "self": None,
                "browsers": [
                    {"key": "other-browser", "cdpPort": 1111, "tabs": [other_tab]},
                    {"key": "map-browser", "cdpPort": 9222, "tabs": [other_tab, map_tab]},
                ],
            }
            tab_call = [
                "--cdp",
                "9222",
                "--session",
                "project-map-reload",
                "--pin-tab",
                "tab",
                "4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3",
            ]
            eval_call = [
                "--cdp",
                "9222",
                "--session",
                "project-map-reload",
                "--pin-tab",
                "eval",
                f"if (location.href === new URL({json.dumps('file://' + map_path)}).href) location.reload()",
            ]
            cases = [
                ("Write", {"file_path": map_path}, listing, {}, 2, True),
                ("Edit", {"file_path": map_path}, listing, {}, 2, True),
                ("missing file_path", {}, listing, {}, 0, False),
                ("other path", {"file_path": str(root / "other.html")}, listing, {}, 0, False),
                ("missing jq", {"file_path": map_path}, listing, {"PATH": ""}, 0, False),
                ("missing terminal-browser", {"file_path": map_path}, listing, {"PATH": str(jq_only)}, 0, False),
                ("listing failure", {"file_path": map_path}, listing, {"LIST_FAIL": "1"}, 0, True),
                ("no browser", {"file_path": map_path}, {"browsers": []}, {}, 0, True),
                ("no map tab", {"file_path": map_path}, {"browsers": [listing["browsers"][0]]}, {}, 0, True),
                (
                    "null target",
                    {"file_path": map_path},
                    {"browsers": [{"cdpPort": 9222, "tabs": [dict(map_tab, targetId=None)]}]},
                    {},
                    0,
                    True,
                ),
                (
                    "missing agent",
                    {"file_path": map_path},
                    listing,
                    {"TERMINAL_BROWSER_AGENT": str(root / "missing")},
                    0,
                    True,
                ),
                ("tab failure", {"file_path": map_path}, listing, {"AGENT_FAIL_ON": "tab"}, 1, True),
                ("eval failure", {"file_path": map_path}, listing, {"AGENT_FAIL_ON": "eval"}, 2, True),
            ]
            for port in (None, "9222", 0, 65536, 1.5):
                cases.append(
                    (
                        "invalid port",
                        {"file_path": map_path},
                        {"browsers": [{"cdpPort": port, "tabs": [map_tab]}]},
                        {},
                        0,
                        True,
                    )
                )
            cases.append(
                (
                    "invalid target",
                    {"file_path": map_path},
                    {"browsers": [{"cdpPort": 9222, "tabs": [dict(map_tab, targetId="--all")]}]},
                    {},
                    0,
                    True,
                )
            )
            for name, tool_input, browser_listing, overrides, call_count, listed in cases:
                with self.subTest(case=name, listing=browser_listing):
                    browser_calls.unlink(missing_ok=True)
                    agent_calls.unlink(missing_ok=True)
                    listing_file.write_text(json.dumps(browser_listing))
                    result = subprocess.run(
                        ["/bin/bash", str(hook)],
                        input=json.dumps({"tool_name": name, "tool_input": tool_input}),
                        text=True,
                        capture_output=True,
                        env={
                            **os.environ,
                            "PATH": str(root),
                            "BROWSER_CALLS": str(browser_calls),
                            "AGENT_CALLS": str(agent_calls),
                            "LISTING": str(listing_file),
                            "TERMINAL_BROWSER_AGENT": str(agent),
                            "LIST_FAIL": "0",
                            "AGENT_FAIL_ON": "",
                            **overrides,
                        },
                        check=False,
                    )
                    self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
                    expected_browser_calls = ["ls --all --json"] if listed else []
                    if name in {"no browser", "no map tab", "null target", "invalid port", "invalid target"}:
                        expected_browser_calls.append(f"open {map_path} --split right --size 0.5 --no-merge")
                    self.assertEqual(
                        browser_calls.read_text().splitlines() if browser_calls.exists() else [],
                        expected_browser_calls,
                    )
                    self.assertEqual(
                        agent_calls.read_text().splitlines() if agent_calls.exists() else [],
                        tab_call[: call_count * len(tab_call)] + (eval_call if call_count == 2 else []),
                    )

    def test_project_map_reload_hook_opens_the_pane_when_no_browser_shows_the_map(self) -> None:
        hook = ROOT / "home/dot_claude/hooks/executable_project-map-reload.sh"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            browser_calls = root / "browser-calls"
            agent_calls = root / "agent-calls"
            browser = root / "terminal-browser"
            browser.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                "with open(os.environ['BROWSER_CALLS'], 'a') as out:\n"
                "    out.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if sys.argv[1:] == ['ls', '--all', '--json']:\n"
                "    print(os.environ['BROWSER_LISTING'])\n"
                "else:\n"
                "    print('open stdout')\n"
                "    print('open stderr', file=sys.stderr)\n"
                "    sys.exit(int(os.environ['OPEN_EXIT']))\n"
            )
            browser.chmod(0o755)
            agent = root / "agent-browser"
            agent.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                "with open(os.environ['AGENT_CALLS'], 'a') as out:\n"
                "    out.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            )
            agent.chmod(0o755)
            jq = JQ
            self.assertIsNotNone(jq)
            (root / "jq").symlink_to(jq)
            (root / "python3").symlink_to(sys.executable)
            map_path = str(root / "map with spaces/.project-map/index.html")
            no_map = {
                "self": {},
                "browsers": [
                    {
                        "cdpPort": 9222,
                        "tabs": [
                            {"url": "https://example.com/", "targetId": "OTHER-TARGET"},
                        ],
                    }
                ],
            }
            map_listing = {
                "self": {},
                "browsers": [
                    {
                        "cdpPort": 9222,
                        "tabs": [
                            {"url": "file://" + map_path, "targetId": "4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3"},
                        ],
                    }
                ],
            }
            cases = [
                ("no map", json.dumps(no_map), "0", True, False),
                ("open failure", json.dumps(no_map), "1", True, False),
                ("map tab", json.dumps(map_listing), "0", False, True),
                ("no browser", json.dumps({"self": {}, "browsers": []}), "0", True, False),
                ("malformed listing", "{", "0", False, False),
            ]
            for name, listing, open_exit, opened, reloaded in cases:
                with self.subTest(case=name):
                    browser_calls.unlink(missing_ok=True)
                    agent_calls.unlink(missing_ok=True)
                    result = subprocess.run(
                        ["/bin/bash", str(hook)],
                        input=json.dumps({"tool_name": "Write", "tool_input": {"file_path": map_path}}),
                        text=True,
                        capture_output=True,
                        env={
                            **os.environ,
                            "PATH": str(root),
                            "BROWSER_CALLS": str(browser_calls),
                            "AGENT_CALLS": str(agent_calls),
                            "BROWSER_LISTING": listing,
                            "OPEN_EXIT": open_exit,
                            "TERMINAL_BROWSER_AGENT": str(agent),
                        },
                        check=False,
                    )
                    self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
                    expected_browser = [["ls", "--all", "--json"]]
                    if opened:
                        expected_browser.append(["open", map_path, "--split", "right", "--size", "0.5", "--no-merge"])
                    self.assertEqual(
                        [json.loads(line) for line in browser_calls.read_text().splitlines()], expected_browser
                    )
                    self.assertEqual(
                        [json.loads(line) for line in agent_calls.read_text().splitlines()]
                        if agent_calls.exists()
                        else [],
                        [
                            [
                                "--cdp",
                                "9222",
                                "--session",
                                "project-map-reload",
                                "--pin-tab",
                                "tab",
                                "4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3",
                            ],
                            [
                                "--cdp",
                                "9222",
                                "--session",
                                "project-map-reload",
                                "--pin-tab",
                                "eval",
                                f"if (location.href === new URL({json.dumps('file://' + map_path)}).href) location.reload()",
                            ],
                        ]
                        if reloaded
                        else [],
                    )

    def _run_project_map_reload_listing(
        self, map_path: str, listing: dict, *, cwd: Path | None = None, home: Path | None = None
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            browser = root / "terminal-browser"
            browser.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                "with open(os.environ['BROWSER_CALLS'], 'a') as out:\n"
                "    out.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if sys.argv[1:] == ['ls', '--all', '--json']:\n"
                "    print(os.environ['BROWSER_LISTING'])\n"
            )
            browser.chmod(0o755)
            agent = root / "agent-browser"
            agent.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                "with open(os.environ['AGENT_CALLS'], 'a') as out:\n"
                "    out.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            )
            agent.chmod(0o755)
            (root / "jq").symlink_to(JQ)
            (root / "python3").symlink_to(sys.executable)
            result = subprocess.run(
                ["/bin/bash", str(ROOT / "home/dot_claude/hooks/executable_project-map-reload.sh")],
                input=json.dumps({"tool_input": {"file_path": map_path}}),
                text=True,
                capture_output=True,
                cwd=cwd,
                env={
                    **os.environ,
                    **({"PWD": str(cwd)} if cwd is not None else {}),
                    **({"HOME": str(home)} if home is not None else {}),
                    "PATH": str(root),
                    "BROWSER_LISTING": json.dumps(listing),
                    "BROWSER_CALLS": str(root / "browser-calls"),
                    "AGENT_CALLS": str(root / "agent-calls"),
                    "TERMINAL_BROWSER_AGENT": str(agent),
                },
                check=False,
            )
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
            return tuple(
                [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
                for path in (root / "browser-calls", root / "agent-calls")
            )

    def test_project_map_reload_hook_selects_the_event_map_among_two_repositories(self) -> None:
        target_id = "4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3"
        for map_path in (
            "/repo/.project-map/index.html",
            "/repo with spaces/./.project-map/index.html",
            "/repo/unused/../.project-map/index.html",
            "/repo_日本%#?'x/.project-map/index.html",
        ):
            with self.subTest(map_path=map_path):
                browser, agent = self._run_project_map_reload_listing(
                    map_path,
                    {
                        "browsers": [
                            {
                                "cdpPort": 9222,
                                "tabs": [{"url": "file:///other/.project-map/index.html", "targetId": "A" * 32}],
                            },
                            {
                                "cdpPort": 9333,
                                "tabs": [{"url": Path(os.path.normpath(map_path)).as_uri(), "targetId": target_id}],
                            },
                        ]
                    },
                )
                self.assertEqual(browser, [["ls", "--all", "--json"]])
                self.assertEqual(len(agent), 2)
                self.assertEqual(
                    agent[0], ["--cdp", "9333", "--session", "project-map-reload", "--pin-tab", "tab", target_id]
                )
                self.assertEqual(agent[1][:-1], agent[0][:-2] + ["eval"])

    def test_project_map_reload_hook_opens_event_map_when_only_another_repository_is_open(self) -> None:
        map_path = "/repo/.project-map/index.html"
        browser, agent = self._run_project_map_reload_listing(
            map_path,
            {
                "browsers": [
                    {
                        "cdpPort": 9222,
                        "tabs": [{"url": "file:///repo-other/.project-map/index.html", "targetId": "A" * 32}],
                    }
                ]
            },
        )
        self.assertEqual(
            browser,
            [["ls", "--all", "--json"], ["open", map_path, "--split", "right", "--size", "0.5", "--no-merge"]],
        )
        self.assertEqual(agent, [])

    def test_project_map_reload_hook_matches_percent_encoded_tilde(self) -> None:
        for directory, url_directory in (
            ("repo~name", "repo%7Ename"),
            ("repo~name", "repo%7ename"),
            ("repo~name", "repo~name"),
            ("repo%7Ename", "repo%257Ename"),
        ):
            with self.subTest(directory=directory, url_directory=url_directory):
                browser, agent = self._run_project_map_reload_listing(
                    f"/{directory}/.project-map/index.html",
                    {
                        "browsers": [
                            {
                                "cdpPort": 9222,
                                "tabs": [
                                    {"url": f"file:///{url_directory}/.project-map/index.html", "targetId": "A" * 32}
                                ],
                            }
                        ]
                    },
                )
                self.assertEqual(browser, [["ls", "--all", "--json"]])
                self.assertEqual(len(agent), 2)
                self.assertEqual(agent[0][-2:], ["tab", "A" * 32])

    def test_project_map_reload_hook_resolves_relative_paths_from_physical_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            physical = root / "physical repo"
            physical.mkdir()
            logical = root / "logical repo"
            logical.symlink_to(physical, target_is_directory=True)
            browser, agent = self._run_project_map_reload_listing(
                "./.project-map/index.html",
                {
                    "browsers": [
                        {
                            "cdpPort": 9222,
                            "tabs": [{"url": (physical / ".project-map/index.html").as_uri(), "targetId": "A" * 32}],
                        }
                    ]
                },
                cwd=logical,
            )
            self.assertEqual(browser, [["ls", "--all", "--json"]])
            self.assertEqual(len(agent), 2)
            self.assertEqual(agent[0][-2:], ["tab", "A" * 32])

    def test_project_map_reload_hook_compares_canonical_paths_for_every_path_form(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            home = root / "home"
            repo = home / "repo"
            map_path = repo / ".project-map/index.html"
            map_path.parent.mkdir(parents=True)
            map_path.write_text("map")
            (repo / "unused").mkdir()
            tilde_map = home / "repo~name/.project-map/index.html"
            tilde_map.parent.mkdir(parents=True)
            tilde_map.write_text("map")
            logical = root / "logical repo"
            logical.symlink_to(repo, target_is_directory=True)
            encoded_tilde = tilde_map.as_uri().replace("~", "%7E")
            for form, event, url, cwd in (
                ("home", "~/repo/.project-map/index.html", map_path.as_uri(), root),
                ("encoded tab URL", str(tilde_map), encoded_tilde, root),
                ("encoded event URL", encoded_tilde, tilde_map.as_uri(), root),
                ("symlinked cwd", "./.project-map/index.html", map_path.as_uri(), logical),
                (
                    "dot and parent segments",
                    str(repo) + "/./unused/../.project-map/index.html",
                    repo.as_uri() + "/./unused/../.project-map/index.html",
                    root,
                ),
                ("event trailing slash", str(map_path) + "/", map_path.as_uri(), root),
                ("tab trailing slash", str(map_path), map_path.as_uri() + "/", root),
                ("event symlink", str(logical / ".project-map/index.html"), map_path.as_uri(), root),
                ("tab symlink", str(map_path), (logical / ".project-map/index.html").as_uri(), root),
                (
                    "quoted URL query",
                    str(map_path),
                    map_path.as_uri() + '?q=";globalThis.injected=true;//\u2028',
                    root,
                ),
            ):
                with self.subTest(form=form):
                    browser, agent = self._run_project_map_reload_listing(
                        event,
                        {
                            "browsers": [
                                {
                                    "cdpPort": 9222,
                                    "tabs": [{"url": url, "targetId": "A" * 32}],
                                }
                            ]
                        },
                        cwd=cwd,
                        home=home,
                    )
                    self.assertEqual(browser, [["ls", "--all", "--json"]])
                    self.assertEqual(len(agent), 2)
                    self.assertEqual(agent[0][-2:], ["tab", "A" * 32])
                    result = subprocess.run(
                        [
                            NODE,
                            "-e",
                            (
                                "const assert = require('node:assert/strict'); let reloads = 0; "
                                f"const location = new URL({json.dumps(url)}); "
                                "location.reload = () => reloads++; "
                                f"{agent[1][-1]}; assert.equal(reloads, 1); "
                                "assert.equal(globalThis.injected, undefined);"
                            ),
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""), result.stderr)

    def test_project_map_reload_hook_rejects_percent_encoded_path_separators(self) -> None:
        map_path = "/repo/.project-map/index.html"
        valid = {"url": "file://" + map_path, "targetId": "B" * 32}
        for encoded in ("%2F", "%2f"):
            invalid_url = f"file:///repo{encoded}.project-map/index.html"
            for fallback in (False, True):
                with self.subTest(encoded=encoded, fallback=fallback):
                    tabs = [{"url": invalid_url, "targetId": "A" * 32}] + ([valid] if fallback else [])
                    browser, agent = self._run_project_map_reload_listing(
                        map_path, {"browsers": [{"cdpPort": 9222, "tabs": tabs}]}
                    )
                    self.assertEqual(
                        browser,
                        [["ls", "--all", "--json"]]
                        + ([] if fallback else [["open", map_path, "--split", "right", "--size", "0.5", "--no-merge"]]),
                    )
                    if fallback:
                        self.assertEqual(len(agent), 2)
                        self.assertEqual(agent[0][-2:], ["tab", "B" * 32])
                    else:
                        self.assertEqual(agent, [])
            with self.subTest(encoded_event=encoded):
                self.assertEqual(
                    self._run_project_map_reload_listing(
                        invalid_url, {"browsers": [{"cdpPort": 9222, "tabs": [valid]}]}
                    ),
                    ([], []),
                )
        for path, url in (
            ("/repo%2Fname/.project-map/index.html", "file:///repo%252Fname/.project-map/index.html"),
            ("/repo%2fname/.project-map/index.html", "file:///repo%252fname/.project-map/index.html"),
            (map_path, "file://" + map_path + "?q=%2F"),
        ):
            with self.subTest(literal_percent_or_query=url):
                browser, agent = self._run_project_map_reload_listing(
                    path,
                    {"browsers": [{"cdpPort": 9222, "tabs": [{"url": url, "targetId": "A" * 32}]}]},
                )
                self.assertEqual(browser, [["ls", "--all", "--json"]])
                self.assertEqual(len(agent), 2)
                self.assertEqual(agent[0][-2:], ["tab", "A" * 32])

    def _run_project_map_reload_case(self, target_id: str, *, tab_gone: bool = False, map_path: str | None = None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            browser = root / "terminal-browser"
            browser.write_text(f"#!{sys.executable}\nimport os\nprint(os.environ['BROWSER_LISTING'])\n")
            browser.chmod(0o755)
            agent = root / "agent-browser"
            agent.write_text(
                f"#!{sys.executable}\n"
                "import json, os, sys\n"
                "from pathlib import Path\n"
                "with open(os.environ['AGENT_CALLS'], 'a') as out:\n"
                "    out.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if sys.argv[-2] == 'tab':\n"
                "    Path(os.environ['PIN_STATE']).write_text(str('--pin-tab' in sys.argv))\n"
                "if sys.argv[-2] == 'eval' and os.environ['TAB_GONE'] == '1':\n"
                "    if Path(os.environ['PIN_STATE']).read_text() == 'True': sys.exit(1)\n"
                "    Path(os.environ['WRONG_TAB_RELOADED']).touch()\n"
            )
            agent.chmod(0o755)
            (root / "jq").symlink_to(JQ)
            (root / "python3").symlink_to(sys.executable)
            map_path = map_path or str(root / ".project-map/index.html")
            result = subprocess.run(
                ["/bin/bash", str(ROOT / "home/dot_claude/hooks/executable_project-map-reload.sh")],
                input=json.dumps({"tool_input": {"file_path": map_path}}),
                text=True,
                capture_output=True,
                env={
                    **os.environ,
                    "PATH": str(root),
                    "BROWSER_LISTING": json.dumps(
                        {
                            "browsers": [
                                {"cdpPort": 9222, "tabs": [{"url": "file://" + map_path, "targetId": target_id}]}
                            ]
                        }
                    ),
                    "TERMINAL_BROWSER_AGENT": str(agent),
                    "AGENT_CALLS": str(root / "agent-calls"),
                    "TAB_GONE": str(int(tab_gone)),
                    "PIN_STATE": str(root / "pin-state"),
                    "WRONG_TAB_RELOADED": str(root / "wrong-tab-reloaded"),
                },
                check=False,
            )
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
            calls = root / "agent-calls"
            return (
                [json.loads(line) for line in calls.read_text().splitlines()] if calls.exists() else [],
                (root / "wrong-tab-reloaded").exists(),
            )

    def test_project_map_reload_hook_guards_against_a_tab_navigating_away(self) -> None:
        calls, _ = self._run_project_map_reload_case(
            "4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3", map_path="/repo/.project-map/index.html"
        )
        self.assertEqual(len(calls), 2)
        script = calls[-1][-1]
        for url, expected in (
            ("file:///repo/.project-map/index.html", 1),
            ("file:///unsaved-form", 0),
            ("file:///other/.project-map/index.html", 0),
        ):
            with self.subTest(url=url):
                result = subprocess.run(
                    [
                        NODE,
                        "-e",
                        (
                            "const assert = require('node:assert/strict'); let reloads = 0; "
                            f"const location = new URL({json.dumps(url)}); location.reload = () => reloads++; "
                            f"{script}; assert.equal(reloads, {expected});"
                        ),
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_project_map_reload_hook_pins_the_bound_tab_when_it_closes(self) -> None:
        calls, wrong_tab_reloaded = self._run_project_map_reload_case("4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3", tab_gone=True)
        self.assertEqual(len(calls), 2)
        self.assertIn("--pin-tab", calls[0])
        self.assertIn("--pin-tab", calls[-1])
        self.assertFalse(wrong_tab_reloaded)

    def test_project_map_reload_hook_accepts_only_cdp_target_ids(self) -> None:
        for target in (
            "list",
            "new",
            "close",
            "MAP-CDP-TARGET",
            "--all",
            "A" * 31,
            "A" * 33,
            "G" * 32,
            "A" * 31 + "\n",
            "A" * 32 + "\n",
        ):
            with self.subTest(rejected=target):
                self.assertEqual(self._run_project_map_reload_case(target), ([], False))
        for target in ("4A0B7C4E1F2D3A4B5C6D7E8F90A1B2C3", "0123456789abcdef0123456789ABCDEF"):
            with self.subTest(accepted=target):
                calls, _ = self._run_project_map_reload_case(target)
                self.assertEqual(len(calls), 2)
                self.assertEqual(calls[0][-2:], ["tab", target])

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
        self.assertIn("- Read(.env)\n", manifest)
        self.assertNotIn("- Read(id_rsa*)", manifest)
        self.assertNotIn("- Write(.env*)", manifest)

    def test_manifest_keeps_model_ids_only_in_profiles(self) -> None:
        manifest = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        profiles_block = manifest.split("model_profiles:")[1].split("\ncodex:")[0]

        self.assertIn("interactive_profile:", profiles_block)
        for line in manifest.splitlines():
            if line.startswith(("  model:", "  effortLevel:", "  model_reasoning_effort:")):
                self.fail(f"model settings must live in model_profiles only: {line.strip()}")


def linux_glob_patterns(output: str) -> tuple[int, list[str]] | None:
    """The count and the named patterns of doctor's Linux glob warning, or None when it prints none."""
    lines = output.splitlines()
    for index, line in enumerate(lines):
        if LINUX_GLOB_WARNING in line:
            found = LINUX_GLOB_FOUND.search(" ".join(lines[index : index + 4]))
            if found is None:
                raise ValueError(f"the glob warning is not in the measured form:\n{output}")
            return int(found.group(1)), found.group(2).split(", ")
    return None


class LinuxGlobWarningParserTest(unittest.TestCase):
    def test_the_parser_reads_the_measured_doctor_form(self) -> None:
        # The operator's paste from a Linux host, Claude Code 2.1.309, 2026-10-24 (brief F2 context 1).
        measured = (
            "Warning: Glob patterns in sandbox permission rules are not fully supported on Linux\n"
            "Fix: Found 4 pattern(s): Read(.env.*), Read(id_rsa*), Read(id_ed25519*) (1 more). "
            "On Linux, glob patterns in Edit/Read rules will be ignored.\n"
        )
        self.assertEqual(linux_glob_patterns(measured), (4, ["Read(.env.*)", "Read(id_rsa*)", "Read(id_ed25519*)"]))
        pair = measured.replace(
            "4 pattern(s): Read(.env.*), Read(id_rsa*), Read(id_ed25519*) (1 more)",
            "2 pattern(s): Read(.env.*), Edit(.env*)",
        )
        self.assertEqual(linux_glob_patterns(pair), (2, ["Read(.env.*)", "Edit(.env*)"]))
        self.assertIsNone(linux_glob_patterns("Claude Code doctor\n1 warning found\n"))
        with self.assertRaises(ValueError):
            linux_glob_patterns(measured.replace("Found 4 pattern(s)", "Found four patterns"))


class ClaudeDoctorLinuxGlobTest(unittest.TestCase):
    """`claude doctor` names exactly the `.env` glob pair on Linux (regime-cutover U17).

    The rendered settings load from a scratch CLAUDE_CONFIG_DIR under a scratch HOME, never the real ~/.claude. A
    control copy with `Read(id_rsa*)` and `Read(id_ed25519*)` added back shows that the instrument sees the warning it
    checks; should a later Claude Code stop emitting the warning, both runs carry none and the test passes.

    Linux only: on macOS `claude doctor` under a scratch HOME asks the login keychain for its credentials
    (`security find-generic-password -a unknown`, then `security -i`), and with no keychain search list in that HOME
    macOS raises a "keychain unknown cannot be found" dialog on every run. The glob warning is Linux-only anyway.
    """

    def setUp(self) -> None:
        if not sys.platform.startswith("linux"):
            self.skipTest("Linux only: macOS claude doctor under a scratch HOME raises a keychain dialog")
        if os.environ.get("CLAUDE_DOCTOR_BIN") and not os.access(os.environ["CLAUDE_DOCTOR_BIN"], os.X_OK):
            self.fail(f"CLAUDE_DOCTOR_BIN is not executable: {os.environ['CLAUDE_DOCTOR_BIN']}")
        if not CLAUDE_DOCTOR_BIN:
            self.skipTest("claude is not on PATH (CI installs it on the ubuntu-24.04 leg)")
        self.temp_dir = Path(tempfile.mkdtemp(prefix="claude-doctor-test-"))
        self.addCleanup(shutil.rmtree, self.temp_dir)

    def doctor(self, settings: dict, name: str) -> str:
        config, home = self.temp_dir / name / "config", self.temp_dir / name / "home"
        config.mkdir(parents=True)
        home.mkdir(parents=True)
        (config / "settings.json").write_text(json.dumps(settings))
        env = {
            "PATH": os.environ["PATH"],
            "HOME": str(home),
            "CLAUDE_CONFIG_DIR": str(config),
            "NO_COLOR": "1",
            "TERM": "dumb",
            "DISABLE_AUTOUPDATER": "1",
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
        }
        result = subprocess.run(
            [CLAUDE_DOCTOR_BIN, "doctor"],
            cwd=home,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn("Invalid settings", output, "the rendered settings must load without a schema error")
        return output

    def test_doctor_names_only_the_env_glob_pair_on_linux(self) -> None:
        template = (ROOT / "home/.chezmoitemplates/claude-settings-managed.json").read_text()
        settings = json.loads(execute_chezmoi_template(template, self.temp_dir, "linux"))
        control = json.loads(json.dumps(settings))
        control["permissions"]["deny"] += ["Read(id_rsa*)", "Read(id_ed25519*)"]
        managed = linux_glob_patterns(self.doctor(settings, "managed"))
        seen = linux_glob_patterns(self.doctor(control, "control"))
        if seen is None:
            self.assertIsNone(managed, "no glob warning at all once Claude Code stops emitting it")
            self.skipTest("this Claude Code prints no Linux glob warning even for the control; nothing to hold")
        self.assertIsNotNone(managed, "the .env pair keeps its glob, so Linux doctor still warns about it")
        self.assertEqual(seen[0], managed[0] + 2, f"the control adds the two key globs: {seen} against {managed}")
        self.assertEqual((managed[0], sorted(managed[1])), (2, sorted(["Read(.env.*)", "Edit(.env*)"])))


class StandingRulesTest(unittest.TestCase):
    """Each agent gets exactly the standing rules its audience names, rendered from one source (regime-cutover U75)."""

    SHARED = "## Shared\n\n- Applies to every audience.\n"
    CLAUDE_ONLY = "---\npaths: '**/*.py'\n---\n\n## Claude only\n"
    CODEX_ONLY = "## Codex only\n\n- `{{ not a template }}` stays literal.\n"

    def setUp(self) -> None:
        self.module = load_generator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="standing-rules-test-"))
        self.module.ROOT = self.temp_dir
        (self.temp_dir / ".chezmoiroot").write_text("home\n")
        self.rules = self.temp_dir / "home/rules"
        self.rules.mkdir(parents=True)
        (self.rules / "shared.md").write_text(self.SHARED)
        (self.rules / "claude-only.md").write_text(self.CLAUDE_ONLY)
        (self.rules / "codex-only.md").write_text(self.CODEX_ONLY)
        self.manifest = sample_manifest()
        self.manifest["omp"]["roles"] = {"orchestrator": "standard", "worker": "standard", "audit": "standard"}
        self.manifest["standing_rules"] = {
            "source_dir": "home/rules",
            "rules": {
                "codex-only": ["codex"],
                "shared": ["claude", "codex", "omp-worker"],
                "claude-only": ["claude"],
            },
        }

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def rendered(self) -> dict[str, str]:
        """Each output's home-relative path and the text chezmoi renders from it, with the source state in place."""
        outputs = self.module.render_standing_rules(self.manifest)
        self.module.write_outputs(outputs)
        return {
            str(path.relative_to(self.temp_dir / "home")): execute_chezmoi_template(text, self.temp_dir)
            for path, text in outputs.items()
        }

    def refused(self) -> str:
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.render_standing_rules(self.manifest)
        return stderr.getvalue()

    def test_each_agent_gets_exactly_the_rules_its_audience_names(self) -> None:
        self.assertEqual(
            self.rendered(),
            {
                "dot_claude/rules/shared.md.tmpl": self.SHARED,
                "dot_claude/rules/claude-only.md.tmpl": self.CLAUDE_ONLY,
                "dot_codex/AGENTS.md.tmpl": self.CODEX_ONLY + "\n" + self.SHARED,
                "dot_agents/omp/rules/worker.md.tmpl": self.SHARED,
            },
        )

    def test_a_rule_that_could_reach_an_agent_it_is_not_for_is_refused(self) -> None:
        rules = self.manifest["standing_rules"]["rules"]
        cases = {
            "front matter outside claude": ("claude-only", ["claude", "codex"], "front matter"),
            "the audit run": ("shared", ["claude", "omp-audit"], "origin/main AGENTS.md"),
            "an unknown audience": ("shared", ["claude", "cursor"], "unknown audience"),
            "an empty audience": ("shared", [], "non-empty audience"),
        }
        for label, (name, audience, message) in cases.items():
            with self.subTest(label):
                saved = rules[name]
                rules[name] = audience
                self.assertIn(message, self.refused())
                rules[name] = saved
        del rules["codex-only"]
        self.assertIn("not declared in standing_rules.rules: ['codex-only']", self.refused())
        rules["missing"] = ["claude"]
        rules["codex-only"] = ["codex"]
        self.assertIn("no source file home/rules/missing.md", self.refused())

    def test_a_rule_file_left_from_an_old_audience_is_stale_and_removed(self) -> None:
        outputs = self.module.render_standing_rules(self.manifest)
        self.module.write_outputs(outputs)
        old_link = self.temp_dir / "home/dot_claude/rules/retired.md.tmpl"
        old_seat = self.temp_dir / "home/dot_omp/private_profiles/private_orchestrator/private_agent/AGENTS.md.tmpl"
        for path in (old_link, old_seat):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("old\n")
        self.assertEqual(self.module.stale_standing_rule_outputs(outputs), [old_link, old_seat])
        self.module.remove_stale_generated_outputs(outputs)
        self.assertFalse(old_link.exists())
        self.assertFalse(old_seat.parent.parent.exists())
        self.assertEqual(self.module.stale_standing_rule_outputs(outputs), [])

    def test_a_refused_run_leaves_every_file_byte_identical_even_with_a_stale_lever_pin(self) -> None:
        # Audit round 6 on 509a9895: the lever-pin refresh wrote the manifest before the unknown-file refusal ran.
        lever = b"#!/usr/bin/env bash\nexit 0\n"
        (self.temp_dir / "scripts/orchestrator").mkdir(parents=True)
        (self.temp_dir / "scripts/orchestrator/hcom-seat").write_bytes(lever)
        manifest_path = self.temp_dir / "home/dot_agents/agent-config.yaml"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(
            "schema_version: 1\nclaude:\n  levers:\n    sha256:\n      hcom-seat: " + "a" * 64 + "\n"
            + "".join(f"{key}: {json.dumps(self.manifest[key])}\n" for key in ("standing_rules", "omp", "model_profiles"))
        )  # fmt: skip
        parsed: list[str | None] = []

        def load(text: str | None = None) -> dict:  # records the text main parses; no PyYAML in make unit-test
            parsed.append(text)
            return self.manifest

        self.module.load_manifest = load
        self.module.expected_outputs = self.module.render_standing_rule_outputs
        self.module.stale_profile_outputs = lambda _manifest: []
        self.module.write_outputs(self.module.render_standing_rule_outputs(self.manifest))
        planted = self.temp_dir / "home/dot_claude/rules/readonly_retired.md.tmpl"
        planted.write_text("old\n")

        def snapshot() -> dict[Path, bytes]:
            return {path: path.read_bytes() for path in sorted(self.temp_dir.rglob("*")) if path.is_file()}

        before = snapshot()
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        for argv in ([], ["--check"]):
            with self.subTest(argv=argv):
                sys.argv = ["generate-agent-configs.py", *argv]
                stderr = io.StringIO()
                quiet = contextlib.redirect_stdout(io.StringIO())
                with contextlib.redirect_stderr(stderr), quiet, self.assertRaises(SystemExit):
                    self.module.main()
                self.assertIn("not generated by scripts/generate-agent-configs.py", stderr.getvalue())
                self.assertEqual(before, snapshot())
                self.assertIn(
                    f"hcom-seat: {hashlib.sha256(lever).hexdigest()}", parsed[-1], "the refreshed text renders"
                )
        planted.unlink()
        sys.argv = ["generate-agent-configs.py"]
        with contextlib.redirect_stdout(io.StringIO()):
            self.module.main()
        self.assertIn(f"hcom-seat: {hashlib.sha256(lever).hexdigest()}", manifest_path.read_text())

    def test_a_rule_root_file_the_generator_does_not_emit_is_refused_not_guessed(self) -> None:
        # Audit round 4 on bc439b02: a chezmoi attribute (readonly_, empty_) changes the target, so no removal is
        # derived from such a name; the run fails, check or not, before anything is written or removed.
        outputs = self.module.render_standing_rule_outputs(self.manifest)
        self.module.write_outputs(outputs)
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        self.module.load_manifest = lambda _text=None: self.manifest
        self.module.expected_outputs = self.module.render_standing_rule_outputs
        self.module.stale_profile_outputs = lambda _manifest: []
        for name in (
            "dot_claude/rules/readonly_retired.md.tmpl",
            "dot_claude/rules/empty_retired.md.tmpl",
            "dot_omp/private_profiles/private_worker/readonly_agent/AGENTS.md.tmpl",
        ):
            with self.subTest(name=name):
                planted = self.temp_dir / "home" / name
                planted.parent.mkdir(parents=True, exist_ok=True)
                planted.write_text("old\n")
                before = (self.temp_dir / "home/.chezmoiremove").read_text()
                for argv in (["--check"], []):
                    sys.argv = ["generate-agent-configs.py", *argv]
                    stderr = io.StringIO()
                    quiet = contextlib.redirect_stdout(io.StringIO())
                    with contextlib.redirect_stderr(stderr), quiet, self.assertRaises(SystemExit):
                        self.module.main()
                    self.assertIn(
                        f"not generated by scripts/generate-agent-configs.py; remove or rename by hand: home/{name}",
                        stderr.getvalue(),
                    )
                self.assertTrue(planted.exists())
                self.assertEqual(before, (self.temp_dir / "home/.chezmoiremove").read_text())
                planted.unlink()

    def generate(self) -> dict[Path, str]:
        """One generate run over the fixture: write the standing-rule outputs, then sweep the stale ones."""
        outputs = self.module.render_standing_rule_outputs(self.manifest)
        self.module.write_outputs(outputs)
        self.module.remove_stale_generated_outputs(outputs)
        return outputs

    def removals(self) -> set[str]:
        return self.module.removal_block_entries((self.temp_dir / "home/.chezmoiremove").read_text())

    def test_a_target_that_leaves_an_audience_is_removed_from_the_host_on_apply(self) -> None:
        remove = self.temp_dir / "home/.chezmoiremove"
        remove.write_text(".hand/written\n")
        self.generate()
        self.assertIn(".hand/written\n", remove.read_text())
        self.assertNotIn(".claude/rules/shared.md", self.removals())
        self.assertIn(".omp/profiles/audit/agent/AGENTS.md", self.removals())
        dest = self.temp_dir / "dest"
        dest.mkdir()
        apply = [
            CHEZMOI,
            *("--source", str(self.temp_dir), "--destination", str(dest), "--no-tty"),
            *("--config", str(self.temp_dir / "chezmoi.toml"), "--persistent-state", str(self.temp_dir / "state")),
            "apply",
        ]
        subprocess.run(apply, check=True, capture_output=True)
        self.assertTrue((dest / ".claude/rules/shared.md").is_file())
        self.assertTrue((dest / ".agents/omp/rules/worker.md").is_file())

        self.manifest["standing_rules"]["rules"]["shared"] = ["codex"]
        stale = self.module.render_standing_rule_outputs(self.manifest)
        self.assertNotEqual(stale[remove], remove.read_text(), "--check must report the missing removal")
        self.generate()
        self.assertLessEqual({".claude/rules/shared.md", ".agents/omp/rules/worker.md"}, self.removals())
        subprocess.run(apply, check=True, capture_output=True)
        self.assertFalse((dest / ".claude/rules/shared.md").exists())
        self.assertFalse((dest / ".agents/omp/rules/worker.md").exists())
        self.assertTrue((dest / ".codex/AGENTS.md").is_file())

        del self.manifest["standing_rules"]["rules"]["claude-only"]
        (self.rules / "claude-only.md").unlink()
        self.generate()
        self.assertIn(".claude/rules/claude-only.md", self.removals(), "a deleted rule keeps its removal")
        self.manifest["standing_rules"]["rules"]["shared"] = ["claude"]
        del self.manifest["standing_rules"]["rules"]["codex-only"]
        (self.rules / "codex-only.md").unlink()
        self.generate()
        self.assertNotIn(".claude/rules/shared.md", self.removals(), "a target rendered again leaves the block")
        self.assertIn(".codex/AGENTS.md", self.removals(), "Codex with no rule left loses its AGENTS.md")
        self.assertFalse((self.temp_dir / "home/dot_codex/AGENTS.md.tmpl").exists())
        subprocess.run(apply, check=True, capture_output=True)
        self.assertFalse((dest / ".codex/AGENTS.md").exists())
        self.assertTrue((dest / ".claude/rules/shared.md").is_file())

    def test_check_fails_while_a_codex_rules_file_no_rule_renders_is_present(self) -> None:
        # PR #544 thread 4370227867: with no codex audience left, the old Codex AGENTS.md template must fail --check.
        self.module.write_outputs(self.module.render_standing_rules(self.manifest))
        codex = self.temp_dir / "home/dot_codex/AGENTS.md.tmpl"
        self.assertTrue(codex.is_file())
        rules = self.manifest["standing_rules"]["rules"]
        del rules["codex-only"]
        (self.rules / "codex-only.md").unlink()
        rules["shared"] = ["claude", "omp-worker"]
        self.module.load_manifest = lambda _text=None: self.manifest
        self.module.expected_outputs = self.module.render_standing_rules
        self.module.stale_profile_outputs = lambda _manifest: []
        old_argv = sys.argv
        self.addCleanup(setattr, sys, "argv", old_argv)
        sys.argv = ["generate-agent-configs.py", "--check"]
        stderr = io.StringIO()
        quiet = contextlib.redirect_stdout(io.StringIO())
        with contextlib.redirect_stderr(stderr), quiet, self.assertRaises(SystemExit):
            self.module.main()
        self.assertIn("home/dot_codex/AGENTS.md.tmpl", stderr.getvalue())

    def test_pstack_models_render_from_the_model_profiles_they_name(self) -> None:
        self.manifest["standing_rules"]["pstack_models"] = {
            "budget": "medium (high)",
            "roles": {"bug-fix": "inherit-parent", "arena runners": ["standard", "auto"], "how explainer": "express"},
        }
        lines = self.module.render_pstack_models(self.manifest).splitlines()
        self.assertIn("# budget: medium (high)", lines)
        self.assertEqual(
            [line for line in lines if line and not line.startswith("#")],
            ["bug-fix: inherit-parent", "arena runners: sonnet high, auto", "how explainer: haiku low"],
        )
        self.manifest["model_profiles"]["standard"]["claude"]["model"] = "claude-opus-5-5"
        self.assertIn("arena runners: opus high, auto", self.module.render_pstack_models(self.manifest))
        for value, message in (("nope", "names no model_profiles entry"), (3, "must be a profile name")):
            with self.subTest(value=value):
                self.manifest["standing_rules"]["pstack_models"]["roles"]["bug-fix"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.render_pstack_models(self.manifest)
                self.assertIn(message, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
