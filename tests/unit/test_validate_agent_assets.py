#!/usr/bin/env python3
"""Exercise focused checks in validate-agent-assets.py."""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from tests.unit.test_generate_agent_configs import MANAGED_ALLOW, load_manifest_fixture

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate-agent-assets.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_agent_assets", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


class ValidateAgentAssetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_validator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="validate-agent-assets-test-"))
        self.module.ROOT = self.temp_dir
        self.codex_writable_roots = ["{{ .chezmoi.homeDir }}/.cache/codex-root"]
        (self.temp_dir / "home/dot_codex").mkdir(parents=True)
        (self.temp_dir / "home/.chezmoitemplates").mkdir(parents=True)

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def write_levers(self, *names: str) -> Path:
        """Executable shebang scripts under the temp ROOT, standing in for the levers the allow rules name, each with
        the byte-identical installed copy the generator renders under home/dot_local/bin/common."""
        levers = self.temp_dir / "scripts/orchestrator"
        installed = self.temp_dir / "home/dot_local/bin/common"
        levers.mkdir(parents=True, exist_ok=True)
        installed.mkdir(parents=True, exist_ok=True)
        for name in names:
            (levers / name).write_text("#!/usr/bin/env bash\nexit 0\n")
            (levers / name).chmod(0o755)
            (installed / f"executable_{name}").write_text("#!/usr/bin/env bash\nexit 0\n")
        return levers

    def test_home_paths_normalise_to_tilde_and_repository_paths_stay(self) -> None:
        with mock.patch.dict(os.environ, {"HOME": "/srv/operator"}):
            for text, expected in (
                ("cd /srv/operator/Workspace/dotfiles", "cd ~/Workspace/dotfiles"),
                ("`/home/alice/.agents/skills/x`", "`~/.agents/skills/x`"),
                ('"/Users/bob/Library/x"', '"~/Library/x"'),
                ("file:/home/carol", "file:~"),
                ("worker-c/home/dot_codex/x and (repo)/home/dot_codex/y", None),
                ("/home/.chezmoitemplates/x", None),
                ("/home/... and /home/<user> and ~/.codex", None),
                ("/srv/operatorX/x", None),
                ("file:///home/alice/x and file:///Users/bob/y", "file://~/x and file://~/y"),
                ("/proc/self/root/srv/operator/.git and ..F/srv/operator/a", "/proc/self/root~/.git and ..F~/a"),
                ("/tmp/test-x/home/worker/.config", None),
                (
                    "/proc/self/root/home/alice/.ssh/id and /proc/42/root/Users/bob/x",
                    "/proc/self/root~/.ssh/id and /proc/42/root~/x",
                ),
                ("cat /root/.ssh/id_ed25519", "cat ~/.ssh/id_ed25519"),
                ("HOME=/root;", "HOME=~;"),
                ("cat /var/root/.ssh/id_ed25519", "cat ~/.ssh/id_ed25519"),
                ("cat /private/var/root/.ssh/id and /home/_build/.ssh/id", "cat ~/.ssh/id and ~/.ssh/id"),
                (
                    "/proc/1/root/root/.ssh/id and /proc/1/root/var/root/.ssh/id",
                    "/proc/1/root~/.ssh/id and /proc/1/root~/.ssh/id",
                ),
                ("/var/root/Library/Keychains/login.keychain-db", "~/Library/Keychains/login.keychain-db"),
                (
                    "/private/var/root/Library/x and /proc/1/root/var/root/Library/x",
                    "~/Library/x and /proc/1/root~/Library/x",
                ),
                ("/home/éclair/.ssh/id and /Users/ユーザー/x", "~/.ssh/id and ~/x"),
                ("/var/home/alice/x and /export/home/bob/y", "~/x and ~/y"),
                ("agent /root/t97_evidence_review and /proc/self/root/etc", None),
            ):
                with self.subTest(text=text):
                    masked, count = self.module.mask_home_paths(text)
                    self.assertEqual(masked, expected or text)
                    self.assertEqual(count, 0 if expected is None else expected.count("~") - text.count("~"))
                    self.assertIsNone(self.module.home_path_pattern().search(masked))

    def test_runner_homes_match_anywhere(self) -> None:
        with mock.patch.dict(os.environ, {"HOME": "/home/alice"}):
            for text, expected in (
                ("..F/home/runner/.ssh/id", "..F~/.ssh/id"),
                ("x/Users/runner/y", "x~/y"),
                ("/home/runner-up/x and /home/runners/y", "~/x and ~/y"),
                ("a/home/runner-up/x and a/home/runners/y", None),
            ):
                with self.subTest(text=text):
                    masked, _ = self.module.mask_home_paths(text)
                    self.assertEqual(masked, expected or text)
                    self.assertEqual(self.module.home_path_pattern().search(text) is not None, expected is not None)

    def test_a_root_home_keeps_sub_agent_identifiers(self) -> None:
        with mock.patch.dict(os.environ, {"HOME": "/root"}):
            masked, count = self.module.mask_home_paths("agent /root/t97_evidence_review read /root/.ssh/id")
        self.assertEqual(masked, "agent /root/t97_evidence_review read ~/.ssh/id")
        self.assertEqual(count, 1)

    def test_secret_scan_flags_the_running_users_home_as_a_backstop(self) -> None:
        self.write_text_file(".orchestration/validation/T1.md", "$ cat /srv/operator/.ssh/id_ed25519\n")
        self.module.validate_no_obvious_secrets()
        with mock.patch.dict(os.environ, {"HOME": "/srv/operator"}):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                self.module.validate_no_obvious_secrets()
        self.assertIn(".orchestration/validation/T1.md names a home directory", stderr.getvalue())

    def test_a_one_segment_home_keeps_namespace_roots_intact(self) -> None:
        with mock.patch.dict(os.environ, {"HOME": "/root"}):
            masked, count = self.module.mask_home_paths(
                "cd /root/.cache; ls /proc/self/root/home/alice/.ssh /proc/self/root/etc"
            )
        self.assertEqual(masked, "cd ~/.cache; ls /proc/self/root~/.ssh /proc/self/root/etc")
        self.assertEqual(count, 2)
        self.assertIsNone(self.module.home_path_pattern().search(masked))
        self.assertIsNotNone(self.module.home_path_pattern().search("/proc/self/root/home/alice/.ssh"))

    def test_secret_scan_rejects_home_paths_in_orchestration_evidence_only(self) -> None:
        self.write_text_file("docs/notes.md", "see /home/alice/x\n")
        self.module.validate_no_obvious_secrets()
        evidence = self.write_text_file(".orchestration/validation/T1.md", "$ ls /home/alice/x\n")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn(".orchestration/validation/T1.md names a home directory", stderr.getvalue())
        evidence.write_text(self.module.mask_secret_matches(evidence.read_text())[0])
        self.assertEqual(evidence.read_text(), "$ ls ~/x\n")
        self.module.validate_no_obvious_secrets()
        escaped = self.write_text_file(
            ".orchestration/validation/T1-crit.json", '{"path": "\\/home\\/alice\\/.ssh\\/id"}\n'
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn("T1-crit.json names a home directory", stderr.getvalue())
        escaped.unlink()

    def test_recursive_scans_skip_gitignored_local_state(self) -> None:
        git = ["git", "-C", str(self.temp_dir), "-c", "user.name=t", "-c", "user.email=t@example.invalid"]
        subprocess.run([*git, "init", "-q"], check=True)
        self.write_text_file(".gitignore", ".claude/contextdb/state/*\n")
        ledger_text = "high-impact" + "-journal-publishing " + "ghp_" + "x" * 25 + " /home/alice/x\n"
        self.write_text_file(".claude/contextdb/state/context.db", ledger_text)
        # A non-UTF-8 ignored file name must not abort the scans; APFS refuses such a name outright.
        with contextlib.suppress(OSError):
            (self.temp_dir / os.fsdecode(b".claude/contextdb/state/raw-\xff")).write_text(ledger_text)
        for scan_name in ("validate_no_removed_claude_skill", "validate_no_obvious_secrets"):
            with self.subTest(scan=scan_name):
                getattr(self.module, scan_name)()
        self.write_text_file("tracked.txt", ledger_text)
        for scan_name in ("validate_no_removed_claude_skill", "validate_no_obvious_secrets"):
            with self.subTest(scan=scan_name, ignored=False):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    getattr(self.module, scan_name)()
                self.assertIn("tracked.txt", stderr.getvalue())

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
        data = json.loads(self.module.render_template_text(path))
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
                "omp": {"model": "claude-bridge/claude-model"},
            }
            for name in ("express", "standard", "review", "deep", "security", "audit")
        }
        profiles["security"]["codex"]["model"] = "gpt-6-astra"
        profiles["audit"]["codex"].update(model="gpt-6-astra", model_reasoning_effort="xhigh", sandbox_mode="read-only")
        profiles["standard"]["claude"]["advisor"] = "fable"
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

    def test_agent_manifest_accepts_exact_security_profile_set(self) -> None:
        self.write_valid_agent_manifest()

        self.module.validate_agent_manifest()

    def test_agent_manifest_accepts_the_four_omp_providers_and_rejects_others(self) -> None:
        accepted = (
            "claude-bridge/claude-model",
            "openai-siwc/gpt-model",
            "anthropic/claude-model",
            "openai-codex/gpt-model",
        )
        for value in accepted:
            with self.subTest(value=value):
                manifest = self.write_valid_agent_manifest()
                manifest["model_profiles"]["audit"]["omp"]["model"] = value
                self.module.validate_agent_manifest()
        for value in ("foo/bar", "claude-bridge/claude model", "claude-model", None):
            with self.subTest(value=value):
                manifest = self.write_valid_agent_manifest()
                if value is None:
                    del manifest["model_profiles"]["audit"]["omp"]
                else:
                    manifest["model_profiles"]["audit"]["omp"]["model"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn("model profile audit.omp.model must match", stderr.getvalue())

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

    def asset_manifest(self) -> dict:
        return {
            "assets": {
                "mise": {
                    "source": "github-release",
                    "upstream": "jdx/mise",
                    "pin": "v1",
                    "verify": "release-shasums",
                    "reason": "fixture: a pinned release",
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
                    "reason": "fixture: the publisher signs nothing",
                    "install_path": "/opt/homebrew",
                    "installer": "install/macos/common/brew.sh",
                },
                "aws": {
                    "source": "https-download",
                    "upstream": "https://awscli.amazonaws.com",
                    "pin": "2",
                    "verify": "gpg",
                    "gpg_fingerprint": "FB5D",
                    "reason": "fixture: a pinned archive",
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

    def rolling_asset_manifest(self) -> dict:
        """The fixture with mise and aws rolling: release: latest and no pin, sha256 or reason."""
        manifest = self.asset_manifest()
        mise = manifest["assets"]["mise"]
        for key in ("pin", "reason", "render"):
            mise.pop(key)
        mise.update(
            release="latest",
            attestation="when-gh-authenticated",
            fallback={"pin": "v1", "sha256": {"linux-x64": "abc"}, "reason": "fixture: no gh on a fresh host"},
        )
        aws = manifest["assets"]["aws"]
        for key in ("pin", "reason"):
            aws.pop(key)
        aws.update(
            release="latest",
            render={
                "file": "install/ubuntu/common/aws_cli.sh",
                "constants": {"AWS_CLI_FINGERPRINT": "gpg_fingerprint"},
            },
        )
        return manifest

    def test_assets_accept_rolling_releases_without_pins(self) -> None:
        self.write_text_file("install/ubuntu/common/aws_cli.sh", 'readonly AWS_CLI_FINGERPRINT="FB5D"\n')

        self.module.validate_assets(self.rolling_asset_manifest())

    def test_assets_reject_invalid_rolling_and_pinned_declarations(self) -> None:
        self.write_text_file("install/ubuntu/common/aws_cli.sh", 'readonly AWS_CLI_FINGERPRINT="FB5D"\n')
        cases = {
            "release other than latest": (lambda a: a["mise"].update(release="v1"), "release must be 'latest'"),
            "release on a git-commit source": (
                lambda a: a["brew"].update(release="latest", pin=None) or a["brew"].pop("pin"),
                "release must be 'latest'",
            ),
            "rolling with a pin": (lambda a: a["mise"].update(pin="v1"), "must not record ['pin']"),
            "rolling with a sha256": (lambda a: a["mise"].update(sha256="abc"), "must not record ['sha256']"),
            "rolling with a reason": (
                lambda a: a["mise"].update(reason="x"),
                "a reason belongs only to a pinned asset",
            ),
            "rolling renders a version": (
                lambda a: a["aws"]["render"]["constants"].update(AWS_CLI_VERSION="pin"),
                "must not render AWS_CLI_VERSION from pin",
            ),
            "pinned release without a reason": (lambda a: a["brew"].pop("reason"), "must give the reason"),
            "unknown attestation": (lambda a: a["mise"].update(attestation="always"), "attestation must be"),
            # An attestation-gated rolling asset needs a reviewed fallback for a host without gh (Amendment 8).
            "attestation without a fallback": (lambda a: a["mise"].pop("fallback"), "must record fallback.pin"),
            "fallback without a reason": (lambda a: a["mise"]["fallback"].pop("reason"), "must record fallback.pin"),
            "fallback without sha256": (lambda a: a["mise"]["fallback"].update(sha256={}), "must record fallback.pin"),
            "fallback on a pinned asset": (
                lambda a: a["brew"].update(fallback={"pin": "v1", "sha256": {"x": "y"}, "reason": "r"}),
                "fallback belongs only to",
            ),
            "float fallback pin": (lambda a: a["mise"]["fallback"].update(pin=1.1), "fallback.pin must be a string"),
            # A same-release checksum file alone is not an independent check (Amendment 7).
            "rolling on a same-release checksum only": (
                lambda a: a["mise"].pop("attestation"),
                "checks only a file from the same release",
            ),
            "rolling on a sha256 sidecar only": (
                lambda a: a["mise"].pop("attestation") and a["mise"].update(verify="release-sha256"),
                "checks only a file from the same release",
            ),
            "attestation off GitHub": (
                lambda a: a["aws"].update(attestation="when-gh-authenticated"),
                "attestation must be",
            ),
        }
        for name, (breaks, message) in cases.items():
            with self.subTest(case=name):
                manifest = self.rolling_asset_manifest()
                breaks(manifest["assets"])
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_assets(manifest)
                self.assertIn(message, stderr.getvalue())

    def test_assets_report_an_unrendered_declare_r_version(self) -> None:
        relative = "install/ubuntu/common/tool.sh"
        path = self.write_text_file(relative, 'declare -r X_VERSION="1"\n')
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_assets(self.asset_manifest())
        self.assertIn(f"{relative} hard-codes X_VERSION", stderr.getvalue())

        manifest = self.asset_manifest()
        manifest["assets"]["mise"]["render"] = [
            manifest["assets"]["mise"]["render"],
            {"file": relative, "constants": {"X_VERSION": "pin"}},
        ]
        self.write_text_file("install/common/mise.sh", 'readonly MISE_VERSION="v1"\n')
        self.module.validate_assets(manifest)
        path.unlink()

    def test_claude_mcp_config_accepts_an_empty_map_and_rejects_a_non_mapping(self) -> None:
        path = self.write_text_file(
            "home/dot_claude/private_mcp.json.tmpl", '{{/* generated */}}\n{"mcpServers": {}}\n'
        )
        self.assertEqual(self.module.validate_claude_mcp_config(), {"mcpServers": {}})
        self.module.validate_mcp_parity({"mcp_servers": {}}, {"mcpServers": {}}, {"mcp_servers": {}})

        for text in ('{"mcpServers": []}', "{}"):
            with self.subTest(text=text):
                path.write_text(text)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_claude_mcp_config()
                self.assertIn("must define mcpServers as a mapping", stderr.getvalue())

    def test_assets_scan_setup_sh_for_unrendered_versions(self) -> None:
        self.write_text_file("setup.sh", 'declare -r CHEZMOI_VERSION="2.70.4"\n')
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_assets(self.asset_manifest())
        self.assertIn("setup.sh hard-codes CHEZMOI_VERSION", stderr.getvalue())

        manifest = self.asset_manifest()
        manifest["assets"]["mise"]["render"] = [
            manifest["assets"]["mise"]["render"],
            {"file": "setup.sh", "constants": {"CHEZMOI_VERSION": "pin"}},
        ]
        self.write_text_file("install/common/mise.sh", 'readonly MISE_VERSION="v1"\n')
        self.module.validate_assets(manifest)

    def test_assets_reject_a_malformed_render_entry(self) -> None:
        for render in (
            ["install/common/mise.sh"],
            [{"file": "install/common/mise.sh", "constants": {}}],
            [{"file": 1, "constants": {"MISE_VERSION": "pin"}}],
            {"file": "install/common/mise.sh", "constants": {"MISE_VERSION": 1}},
            [{"file": "install/../install/common/mise.sh", "constants": {"MISE_VERSION": "pin"}}],
            [{"file": "./install/common/mise.sh", "constants": {"MISE_VERSION": "pin"}}],
            [{"file": "/etc/mise.sh", "constants": {"MISE_VERSION": "pin"}}],
            [{"file": "../outside.sh", "constants": {"MISE_VERSION": "pin"}}],
        ):
            with self.subTest(render=render):
                manifest = self.asset_manifest()
                manifest["assets"]["mise"]["render"] = render
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_assets(manifest)
                self.assertIn("assets.mise.render entries must each be a mapping", stderr.getvalue())

    def test_assets_reject_one_assignment_rendered_from_two_fields(self) -> None:
        manifest = self.asset_manifest()
        mise = manifest["assets"]["mise"]
        mise["sha256"] = "abc"
        mise["render"] = [
            mise["render"],
            {"file": "install/common/mise.sh", "constants": {"MISE_VERSION": "sha256"}},
        ]
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_assets(manifest)
        self.assertIn(
            "install/common/mise.sh MISE_VERSION is rendered from both assets.mise.pin "
            "(via install/common/mise.sh) and assets.mise.sha256",
            stderr.getvalue(),
        )

        mise["render"] = [mise["render"][0], dict(mise["render"][0])]
        self.write_text_file("install/common/mise.sh", 'readonly MISE_VERSION="v1"\n')
        self.module.validate_assets(manifest)

    def test_assets_reject_one_assignment_rendered_through_a_symlink_alias(self) -> None:
        target = self.write_text_file("install/common/mise.sh", 'readonly MISE_VERSION="v1"\n')
        alias = target.parent / "alias.sh"
        alias.symlink_to(target.name)
        manifest = self.asset_manifest()
        mise = manifest["assets"]["mise"]
        mise["sha256"] = "abc"
        mise["render"] = [
            mise["render"],
            {"file": "install/common/alias.sh", "constants": {"MISE_VERSION": "sha256"}},
        ]
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_assets(manifest)
        self.assertIn(
            "install/common/alias.sh MISE_VERSION is rendered from both assets.mise.pin "
            "(via install/common/mise.sh) and assets.mise.sha256",
            stderr.getvalue(),
        )

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

    def test_agent_manifest_rejects_the_retired_adh_profile(self) -> None:
        manifest = self.write_valid_agent_manifest()
        manifest["model_profiles"]["adh"] = manifest["model_profiles"]["deep"]

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()
        self.assertIn("must define the six base profiles and no others", stderr.getvalue())

    def test_agent_manifest_pins_the_audit_codex_profile(self) -> None:
        for key, wrong in (
            ("model", "gpt-5.6-sol"),
            ("model", "gpt-6.1-sol"),
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
            "filesystem": {
                "allowWrite": list(self.codex_writable_roots),
                "denyRead": ["~/**/.env", "~/**/.env.*"],
            },
            "credentials": {"files": [{"path": "~/.ssh", "mode": "deny"}]},
            "network": {
                "allowedDomains": ["github.com", "api.github.com"],
                "allowUnixSockets": ["~/.config/herdr/herdr.sock", "/run/user/1000/x.sock"],
            },
        }

    def test_claude_sandbox_accepts_manifest_symmetric_settings(self) -> None:
        self.module.validate_claude_sandbox(self.valid_claude_sandbox(), self.codex_writable_roots, "sandbox")

    def test_claude_sandbox_validator_refuses_each_forbidden_form(self) -> None:
        spec = importlib.util.spec_from_file_location(
            "generate_agent_configs", ROOT / "scripts/generate-agent-configs.py"
        )
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        manifest = load_manifest_fixture(self.temp_dir)
        self.write_levers("hcom-seat", "hcom-dispatch", "bus-history.sh", "worktree-gc.sh", "regime-init")
        self.write_text_file("home/dot_config/claude/rules/crit-review.md", "/crit\n")
        cases = [
            ("macOS gh exclusion", lambda sandbox: sandbox["excludedCommands"].append("gh *"), "macOS.*gh"),
            (
                "Linux extra exclusion",
                lambda sandbox: sandbox["linux_excluded_commands"].append("bash *"),
                "Linux.*excludedCommands",
            ),
            (
                "Mach allowlist",
                lambda sandbox: sandbox["network"].update(allowMachLookup=["com.apple.sysmond"]),
                "Mach",
            ),
            (
                "all Unix sockets",
                lambda sandbox: sandbox["network"].update(allowAllUnixSockets=True),
                "allowAllUnixSockets",
            ),
        ]
        for domain in (
            "cafe.github.com",
            "datadoghq.com",
            "api.datadoghq.com",
            "checkpoint-api.hashicorp.com",
            "api.anthropic.com",
        ):
            cases.append(
                (domain, lambda sandbox, domain=domain: sandbox["network"]["allowedDomains"].append(domain), "domain")
            )
        for name, mutate, message in cases:
            with self.subTest(form=name):
                candidate = copy.deepcopy(manifest)
                mutate(candidate["claude"]["sandbox"])
                self.write_text_file(
                    "home/.chezmoitemplates/claude-settings-managed.json", generator.render_claude_settings(candidate)
                )
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_claude_settings(candidate)
                self.assertRegex(stderr.getvalue(), message)

        template = generator.render_claude_settings(manifest)
        prefix, linux = template.rsplit("{{ else }}", 1)  # the last OS conditional is the sandbox block
        linux = linux.replace('"allowedDomains": [', '"allowedDomains": ["cafe.github.com",', 1)
        self.write_text_file("home/.chezmoitemplates/claude-settings-managed.json", prefix + "{{ else }}" + linux)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_claude_settings(manifest)
        self.assertIn("linux sandbox", stderr.getvalue())

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
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")

    def test_claude_permissions_allow_must_list_non_empty_rules(self) -> None:
        for allow in ("Bash(hcom list *)", [""], [3]):
            with (
                self.subTest(rejects=allow),
                contextlib.redirect_stderr(io.StringIO()) as stderr,
                self.assertRaises(SystemExit),
            ):
                self.module.validate_claude_permissions_allow({"allow": allow}, "permissions")
            self.assertIn("permissions.allow must be a list", stderr.getvalue())

    def test_claude_permissions_allow_accepts_the_fixed_rules_and_the_executable_levers(self) -> None:
        self.write_levers("hcom-seat", "hcom-dispatch", "bus-history.sh", "worktree-gc.sh", "regime-init")
        for permissions in ({}, {"allow": []}, {"allow": ["Bash(hcom list *)"]}, {"allow": MANAGED_ALLOW}):
            with self.subTest(accepts=permissions):
                self.module.validate_claude_permissions_allow(permissions, "permissions")
        pinned = {
            "hcom-seat": "0" * 64,
            "hcom-dispatch": "0" * 64,
            "bus-history.sh": "0" * 64,
            "worktree-gc.sh": "0" * 64,
            "regime-init": "0" * 64,
        }
        self.module.validate_claude_permissions_allow({"allow": MANAGED_ALLOW}, "permissions", pinned)

    def test_claude_permissions_allow_refuses_every_other_rule(self) -> None:
        levers = self.write_levers("hcom-seat", "python3", "node.js", "drifted")
        (self.temp_dir / "home/dot_local/bin/common/executable_drifted").write_text("#!/usr/bin/env bash\nexit 1\n")
        (levers / "notes.md").write_text("#!/usr/bin/env bash\n")
        (levers / "binary").write_bytes(b"\xcf\xfa\xed\xfe")
        (levers / "binary").chmod(0o755)
        (levers / "link").symlink_to(levers / "hcom-seat")
        (levers / "dir").mkdir()
        (levers / "uninstalled").write_text("#!/usr/bin/env bash\n")
        (levers / "uninstalled").chmod(0o755)
        installed = "Bash(~/.local/bin/common/{} *)".format
        cases = {
            "Bash(*)": "is not Bash\\(hcom list \\*\\) or",
            "Bash": "is not Bash\\(hcom list \\*\\) or",
            "Bash(hcom *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(hcom list)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(git worktree remove *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(git *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(python3 *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(bash ~/.local/bin/common/hcom-seat *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(/Users/x/.local/bin/common/hcom-seat *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(~/.local/bin/common/hcom-seat)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(~/.local/bin/common/hcom-seat:*)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(~/.local/bin/common/../../bin/sh *)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(~/.local/bin/common/*)": "is not Bash\\(hcom list \\*\\) or",
            "Read(**)": "is not Bash\\(hcom list \\*\\) or",
            "Bash(scripts/orchestrator/hcom-seat *)": "names a lever inside the rewritable checkout",
            "Bash(./scripts/orchestrator/hcom-seat *)": "names a lever inside the rewritable checkout",
            "Bash(scripts/orchestrator/hcom-seat:*)": "names a lever inside the rewritable checkout",
            installed("absent"): "absent is not a regular file",
            installed("dir"): "dir is not a regular file",
            installed("link"): "link is not a regular file",
            installed("notes.md"): "notes.md is not executable",
            installed("python3"): "python3 is named as an interpreter",
            installed("node.js"): "node.js is named as an interpreter",
            installed("binary"): "binary is not a script with a shebang line",
            installed("uninstalled"): "has no byte-identical installed copy",
            installed("drifted"): "has no byte-identical installed copy",
        }
        for rule, message in cases.items():
            with self.subTest(rejects=rule):
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_permissions_allow({"allow": ["Bash(hcom list *)", rule]}, "permissions")
                self.assertRegex(stderr.getvalue(), message)
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_claude_permissions_allow({"allow": [installed("hcom-seat")]}, "permissions", {})
        self.assertIn("no claude.levers.sha256 pin for hcom-seat", stderr.getvalue())

    def test_the_managed_allow_rules_name_the_installed_levers_on_every_os(self) -> None:
        """The rules name ~/.local/bin/common on darwin and linux; a checkout-path rule fails either (U31)."""
        self.module.ROOT = ROOT
        manifest = load_manifest_fixture(self.temp_dir)
        self.assertEqual(MANAGED_ALLOW, manifest["claude"]["permissions"]["allow"])
        self.assertNotIn("darwin_allow", manifest["claude"]["permissions"])
        pinned = manifest["claude"]["levers"]["sha256"]
        self.module.validate_claude_permissions_allow(manifest["claude"]["permissions"], "manifest permissions", pinned)

        spec = importlib.util.spec_from_file_location(
            "generate_agent_configs", ROOT / "scripts/generate-agent-configs.py"
        )
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        self.module.ROOT = self.temp_dir
        self.write_text_file("home/dot_config/claude/rules/crit-review.md", "/crit\n")
        self.write_levers("hcom-seat", "hcom-dispatch", "bus-history.sh", "worktree-gc.sh", "regime-init")
        checkout = copy.deepcopy(manifest)
        checkout["claude"]["permissions"]["allow"][1] = "Bash(scripts/orchestrator/hcom-seat *)"
        for os_name in ("darwin", "linux"):
            with self.subTest(os=os_name):
                self.write_text_file(
                    "home/.chezmoitemplates/claude-settings-managed.json", generator.render_claude_settings(checkout)
                )
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_settings(checkout, os_name)
                self.assertIn("names a lever inside the rewritable checkout", stderr.getvalue())
                self.write_text_file(
                    "home/.chezmoitemplates/claude-settings-managed.json", generator.render_claude_settings(manifest)
                )
                self.module.validate_claude_settings(manifest, os_name)

    def test_claude_sandbox_requires_the_ssh_credential_deny_and_home_or_absolute_deny_read(self) -> None:
        cases = {
            "no credentials": (lambda sandbox: sandbox.pop("credentials"), "credentials.files must contain"),
            "ssh allowed": (
                lambda sandbox: sandbox["credentials"].update(files=[{"path": "~/.ssh", "mode": "allow"}]),
                "credentials.files must contain",
            ),
            "other directory only": (
                lambda sandbox: sandbox["credentials"].update(files=[{"path": "~/.gnupg", "mode": "deny"}]),
                "credentials.files must contain",
            ),
            "no denyRead": (lambda sandbox: sandbox["filesystem"].pop("denyRead"), "denyRead must be a non-empty"),
            "empty denyRead": (
                lambda sandbox: sandbox["filesystem"].update(denyRead=[]),
                "denyRead must be a non-empty",
            ),
            "relative denyRead": (
                lambda sandbox: sandbox["filesystem"]["denyRead"].append("**/.env"),
                "globs are allowed here, unlike allowWrite",
            ),
        }
        for name, (breaks, message) in cases.items():
            with self.subTest(rule=name):
                sandbox = self.valid_claude_sandbox()
                breaks(sandbox)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
                self.assertIn(message, stderr.getvalue())
        sandbox = self.valid_claude_sandbox()
        sandbox["filesystem"]["denyRead"].append("/srv/secrets/**")
        self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")

    def test_claude_deny_rules_refuse_a_glob_last_segment_except_the_env_pair(self) -> None:
        accepted = [
            "Bash(sudo:*)",
            "Bash(curl * | sh)",
            "Read(.env)",
            "Read(.env.*)",
            "Edit(.env*)",
            "Read(~/.ssh/**)",
            "Read(secrets/**)",
            "Read(config/credentials.json)",
        ]
        self.module.validate_claude_permissions_deny({"deny": accepted}, "permissions")
        for rule in (
            "Read(id_rsa*)",
            "Read(id_ed25519*)",
            "Read(~/.ssh/id_*)",
            "Edit(.env.*)",
            "Read(.env*)",
            "Read(secret?.json)",
            "Edit(config/[ab].json)",
            "Read(secrets/*.pem/**)",
        ):
            with self.subTest(rejects=rule):
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_permissions_deny({"deny": [*accepted, rule]}, "permissions")
                self.assertIn("which the Linux sandbox ignores", stderr.getvalue())
                self.assertIn("covered for subprocesses by sandbox.filesystem.denyRead", stderr.getvalue())

    def test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs(self) -> None:
        sandbox = self.valid_claude_sandbox()
        sandbox["filesystem"]["allowWrite"].append("~/.cache/uv")
        self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
        for path in ("relative/cache", "~cache", "/tmp/*", 7):
            with self.subTest(path=path):
                sandbox = self.valid_claude_sandbox()
                sandbox["filesystem"]["allowWrite"].append(path)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
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
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
                self.assertIn("allowUnixSockets entries must be absolute or ~/ paths", stderr.getvalue())

    def test_claude_sandbox_requires_extra_codex_writable_roots(self) -> None:
        roots = [*self.codex_writable_roots, "/extra/codex/root"]
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
                    "writable_roots": self.codex_writable_roots,
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
        self.write_codex_config(f"network_access = false\nwritable_roots = {json.dumps(self.codex_writable_roots)}")
        manifest = {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
            "interactive_profile": "standard",
            "codex": {
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": self.codex_writable_roots,
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

    def test_codex_command_hooks_accept_the_declared_tables(self) -> None:
        self.module.validate_codex_command_hooks(
            {"command_hooks": COMMAND_HOOKS}, tomllib.loads(COMMAND_HOOKS_TOML)["hooks"], Path("codex.toml")
        )
        self.module.validate_codex_command_hooks({}, {}, Path("codex.toml"))

    def test_codex_command_hooks_reject_bad_entries_and_stray_tables(self) -> None:
        rendered = tomllib.loads(COMMAND_HOOKS_TOML)["hooks"]
        stray = tomllib.loads(COMMAND_HOOKS_TOML + COMMAND_HOOKS_TOML.split("[[hooks.PostCompact]]")[0])["hooks"]
        for name, hooks, tables, message in (
            ("unknown event", [{**COMMAND_HOOKS[0], "event": "Notification"}], rendered, "is not a Codex hook event"),
            ("missing command", [{**COMMAND_HOOKS[0], "command": ""}], rendered, "must set a non-empty command"),
            ("string timeout", [{**COMMAND_HOOKS[0], "timeout": "30"}], rendered, "timeout must be a positive integer"),
            (
                "boolean timeout",
                [{**COMMAND_HOOKS[0], "timeout": True}],
                rendered,
                "timeout must be a positive integer",
            ),
            ("stray hand-edited table", COMMAND_HOOKS, stray, "must hold exactly the manifest's Codex hook tables"),
            ("undeclared rendered table", [], rendered, "must hold exactly the manifest's Codex hook tables"),
            (
                "SessionEnd over 3 seconds",
                [{**COMMAND_HOOKS[2], "timeout": 4}],
                rendered,
                "at most 3 seconds for SessionEnd",
            ),
            ("mapping instead of a list", {}, {}, "codex.hooks.command_hooks must be a list"),
            ("false instead of a list", False, {}, "codex.hooks.command_hooks must be a list"),
            ("null instead of a list", None, {}, "codex.hooks.command_hooks must be a list"),
        ):
            with self.subTest(case=name):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_codex_command_hooks({"command_hooks": hooks}, tables, Path("codex.toml"))
                self.assertIn(message, stderr.getvalue())

    def codex_config_manifest(self, projects: dict) -> dict:
        return {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
            "interactive_profile": "standard",
            "codex": {
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": self.codex_writable_roots,
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
            f"network_access = false\nwritable_roots = {json.dumps(self.codex_writable_roots)}",
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

    def test_secret_scan_fails_a_nul_in_orchestration_text_and_skips_other_binaries(self) -> None:
        binary = self.temp_dir / "home/dot_local/share/blob.bin"
        binary.parent.mkdir(parents=True, exist_ok=True)
        binary.write_bytes(b"\x00\x01ghp_" + b"x" * 25)
        self.module.validate_no_obvious_secrets()

        evidence = self.temp_dir / ".orchestration/validation/t-a01.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b"heading\x00ghp_" + b"x" * 25)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn(".orchestration/validation/t-a01.md holds a NUL byte at offset 7", stderr.getvalue())

    def test_secret_scan_rejects_utf16_orchestration_text_with_the_nul_offset(self) -> None:
        evidence = self.temp_dir / ".orchestration/validation/t-utf16.md"
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(("ghp_" + "f" * 25 + "\n").encode("utf-16"))
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn(".orchestration/validation/t-utf16.md holds a NUL byte at offset 3", stderr.getvalue())

        evidence.write_bytes("\u3042\u3044".encode("utf-16"))  # UTF-16 with no NUL byte
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn(".orchestration/validation/t-utf16.md is UTF-16; evidence must be UTF-8 text", stderr.getvalue())

    def test_secret_scan_reads_json_per_key_and_string_value(self) -> None:
        key = "ghp_" + "d" * 25
        path = self.temp_dir / ".orchestration/validation/t-pr-feedback.json"
        path.parent.mkdir(parents=True)
        across_fields = json.dumps({"items": [{"body": f"ends with {FIELD} = ", "url": "https://x/1"}]}, indent=2)
        path.write_text(across_fields)
        self.module.validate_no_obvious_secrets()

        for name, text in (
            ("key-shaped object key", json.dumps({key: "value"})),
            ("duplicate key's earlier value", '{"m": "' + key + '", "m": "later"}'),
            ("escaped quoted assignment", json.dumps({"body": f"{FIELD} = " + '"abc"'})),
            ("not JSON, text scan", across_fields[:-1]),
        ):
            with self.subTest(case=name):
                path.write_text(text)
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.validate_no_obvious_secrets()

    def test_compactiondb_project_copy_must_match_the_vendor_tree(self) -> None:
        files = {"contextdb/contextdb/storage.py": "store\n", "hooks/contextdb_cli.py": "cli\n"}
        for relative, text in files.items():
            self.write_text_file(f"vendor/compactiondb/.claude/{relative}", text)
            self.write_text_file(f".claude/{relative}", text)
        self.module.validate_compactiondb_project_copy()

        for name, path, text in (
            ("edited project file", ".claude/contextdb/contextdb/storage.py", "edited\n"),
            ("missing project hook", ".claude/hooks/contextdb_cli.py", None),
            ("project-only file", ".claude/contextdb/contextdb/extra.py", "extra\n"),
        ):
            with self.subTest(case=name):
                target = self.temp_dir / path
                original = target.read_bytes() if target.exists() else None
                if text is None:
                    target.unlink()
                else:
                    target.write_text(text)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_compactiondb_project_copy()
                self.assertIn(f"{path} differs from vendor/compactiondb/{path}", stderr.getvalue())
                if original is None:
                    target.unlink()
                else:
                    target.write_bytes(original)

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

    def test_normalises_home_paths_in_text_and_json_evidence(self) -> None:
        home = str(Path.home())
        evidence = self.temp_dir / "T1-audit-abcdef1.md"
        evidence.write_text(f"$ cat {home}/.agents/skills/a/SKILL.md\n/home/runner/work/x\nVerdict: correct\n")
        feedback = self.temp_dir / "T1-pr-feedback.json"
        feedback.write_text(json.dumps({"items": [{"body": f"see {home}/x", "path": "home/dot_config/a"}]}) + "\n")

        result = self.run_mask(evidence, feedback)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(evidence.read_text(), "$ cat ~/.agents/skills/a/SKILL.md\n~/work/x\nVerdict: correct\n")
        self.assertEqual(json.loads(feedback.read_text())["items"], [{"body": "see ~/x", "path": "home/dot_config/a"}])
        self.assertIn(f"masked 2 match(es) in {evidence}", result.stdout)

    def test_masks_json_content_whatever_the_suffix(self) -> None:
        evidence = self.temp_dir / "T1-crit.md"
        evidence.write_text('{"path":"\\/home\\/alice\\/.ssh\\/id"}\n')
        prose = self.temp_dir / "T1.md"
        prose.write_text("see /home/alice/x\n")

        result = self.run_mask(evidence, prose)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(evidence.read_text()), {"path": "~/.ssh/id"})
        self.assertEqual(prose.read_text(), "see ~/x\n")
        module = load_validator()
        for path in (evidence, prose):
            text = path.read_text()
            with self.subTest(path=path.name):
                strings = module.json_strings(text) or [text]
                self.assertFalse(any(module.home_path_pattern().search(s) for s in (text, *strings)))

    def test_keeps_carriage_returns_and_every_unmasked_byte(self) -> None:
        evidence = self.temp_dir / "T1.md"
        evidence.write_bytes(b"progress 10%\rprogress 100%\r\nline\r\n/home/alice/x\n")

        result = self.run_mask(evidence)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(evidence.read_bytes(), b"progress 10%\rprogress 100%\r\nline\r\n~/x\n")

    def test_leaves_allowed_placeholders_the_scan_accepts(self) -> None:
        evidence = self.temp_dir / "audit.md"
        placeholder = "GITHUB_PERSONAL_ACCESS_" + FIELD.upper()
        original = f'{placeholder}: "${{{placeholder}}}"\n'
        evidence.write_text(original)

        result = self.run_mask(evidence)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, f"masked 0 match(es) in {evidence}\n")
        self.assertEqual(evidence.read_text(), original)

    def test_masks_json_string_values_and_keeps_the_document_parseable(self) -> None:
        evidence = self.temp_dir / "t-pr-feedback.json"
        key = "ghp_" + "b" * 25
        items = [
            {"body": f"ends with {FIELD} = ", "url": "https://x/1"},
            {"body": f"line\n{key}\nset {FIELD} = " + '"abc"', "url": "https://x/2"},
            {key: "a key-shaped member name"},
        ]
        evidence.write_text(json.dumps({"items": items}, indent=2) + "\n")

        result = self.run_mask(evidence)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, f"masked 3 match(es) in {evidence}\n")
        saved = json.loads(evidence.read_text())["items"]
        module = load_validator()
        self.assertEqual([item.get("url") for item in saved[:2]], ["https://x/1", "https://x/2"])
        self.assertEqual(
            [item["body"] for item in saved[:2]], [module.mask_secret_matches(i["body"])[0] for i in items[:2]]
        )
        self.assertEqual(saved[2], {module.SECRET_MASK: "a key-shaped member name"})
        self.assertNotIn(key, evidence.read_text())

    def test_masks_an_earlier_duplicate_member_so_the_scan_passes(self) -> None:
        evidence = self.temp_dir / "t-pr-feedback.json"
        key = "ghp_" + "e" * 25
        evidence.write_text('{"items": [{"body": "' + key + '", "body": "safe replacement"}]}\n')

        result = self.run_mask(evidence)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, f"masked 1 match(es) in {evidence}\n")
        self.assertEqual(json.loads(evidence.read_text()), {"items": [{"body": "safe replacement"}]})
        module = load_validator()
        strings = module.json_strings(evidence.read_text())
        self.assertFalse(any(module.SECRET_PATTERN.search(s) for s in strings))

    def test_a_masked_key_collision_fails_and_leaves_the_file_unchanged(self) -> None:
        evidence = self.temp_dir / "t-pr-feedback.json"
        first, second = "ghp_" + "g" * 25, "ghp_" + "h" * 25
        original = json.dumps({"items": [{first: "one", second: "two"}]}) + "\n"
        evidence.write_text(original)

        result = self.run_mask(evidence)

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(str(evidence), result.stderr)
        self.assertIn(repr(first), result.stderr)
        self.assertIn(repr(second), result.stderr)
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
