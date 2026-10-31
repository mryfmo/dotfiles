#!/usr/bin/env python3
"""Exercise focused checks in validate-agent-assets.py."""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
import unittest
from pathlib import Path
from unittest import mock

from tests.unit.test_generate_agent_configs import MANAGED_ALLOW, load_manifest_fixture, render_claude_template

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init  # noqa: E402

sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate-agent-assets.py"

# Built at runtime so this test file never holds a literal rule match: the generic rules' key words are split, and a
# planted provider token is split at its prefix.
FIELD = "tok" + "en"
SECRET_KEY = "sec" + "ret"
PASSWORD_KEY = "pass" + "word"
API_KEY = "api_" + "key"
# A quoted value above the generic rules' entropy threshold (20 distinct characters, 4.32 bits) and one below it.
HIGH_ENTROPY_VALUE = "Qz7vR2mK9pL4wX8nJ3fT"
LOW_ENTROPY_VALUE = "real-secret"
# 160 characters at 2 bits whose every 20-character window is 2 bits: beside a secret on its line it brought the
# whole line under the threshold (round 7 finding on 38a83e45).
LOW_ENTROPY_PADDING = "low-" * 40


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
        # An allowlisted spelling (validate-agent-assets.py SANDBOX_WRITE_ROOTS), so fixtures pass the write-root check.
        self.codex_writable_roots = ["~/.local/state/hcom"]
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
        git_init(self.temp_dir)
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

    def test_rendered_skill_entries_that_drift_from_the_audience_are_refused(self) -> None:
        """validate_skill_audience parses the rendered Codex, omp and Claude files and refuses each kind of drift."""
        # The manifest and the omp configs parsed by chezmoi's fromYaml: `make unit-test` gives the test process no
        # PyYAML (as in test_the_omp_writing_seats_allow_only_the_merge_and_installed_levers).
        manifest = load_manifest_fixture(self.temp_dir)
        rendered = [
            manifest["codex"]["config_path"],
            "home/.chezmoitemplates/omp-config-managed.yml",
            *(f"home/dot_agents/omp/profiles/{role}.yml.tmpl" for role in manifest["omp"]["roles"]),
        ]
        for rel in rendered:
            (self.temp_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, self.temp_dir / rel)
        shutil.copytree(ROOT / "home/dot_claude/skills", self.temp_dir / "home/dot_claude/skills")
        paths = self.module.rendered_omp_skill_configs(manifest)
        texts = {consumer: path.read_text() for consumer, path in paths.items()}

        def parsed(edits: dict[str, tuple[str, str]]) -> dict:
            configs = {}
            for consumer, text in texts.items():
                if consumer in edits:
                    old, new = edits[consumer]
                    self.assertIn(old, text)
                    text = text.replace(old, new, 1)
                text = text.replace("{{ .chezmoi.homeDir }}", self.module.SKILL_CONFIG_HOME)
                configs[consumer] = render_claude_template(
                    "{{ fromYaml " + json.dumps(text) + " | toJson }}", self.temp_dir
                )
            return configs

        self.module.validate_skill_audience(manifest, parsed({}))
        if self.module.yaml is None:
            with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                self.module.validate_skill_audience(manifest)
            self.assertIn("PyYAML is required", stderr.getvalue())
        else:
            self.module.validate_skill_audience(manifest)

        cases = {
            "worker no longer ignores a seat skill": (
                "omp-worker",
                ("    - hcom-orchestration\n", ""),
                "for omp-worker",
            ),
            "audit given skills": ("omp-audit", ("  enabled: false\n", "  enabled: true\n"), "for omp-audit"),
            "plain launch loses enabled": ("omp", ("  enabled: true\n", ""), "for omp:"),
        }
        for label, (consumer, edit, message) in cases.items():
            with self.subTest(case=label):
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_skill_audience(manifest, parsed({consumer: edit}))
                self.assertIn(message, stderr.getvalue())
        configs = parsed({})
        codex = self.temp_dir / manifest["codex"]["config_path"]
        original = codex.read_text()
        self.assertIn("hcom-worker/SKILL.md", original)
        codex.write_text(original.replace("hcom-worker/SKILL.md", "kept-for-codex/SKILL.md", 1))
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_skill_audience(manifest, configs)
        self.assertIn("[[skills.config]]", stderr.getvalue())
        codex.write_text(original)
        link = self.temp_dir / "home/dot_claude/skills/hcom-worker/symlink_SKILL.md.tmpl"
        link.parent.mkdir()
        link.write_text("{{ .chezmoi.sourceDir }}/dot_agents/skills/hcom-worker/SKILL.md\n")
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_skill_audience(manifest, configs)
        self.assertIn("audience leaves out claude: ['hcom-worker']", stderr.getvalue())

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

    def git_config_failure(self, template: str) -> str | None:
        """Run validate_git_config on a template beside the real setup-gh; return its error or None."""
        self.write_text_file("home/dot_config/git/config.tmpl", template)
        setup_gh = "home/dot_local/bin/common/executable_setup-gh"
        self.write_text_file(setup_gh, (ROOT / setup_gh).read_text())
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr):
                self.module.validate_git_config()
        except SystemExit:
            return stderr.getvalue()
        return None

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_git_config_accepts_the_managed_template_rendered_with_and_without_the_key(self) -> None:
        self.assertIsNone(self.git_config_failure((ROOT / "home/dot_config/git/config.tmpl").read_text()))

    @unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is not installed")
    def test_git_config_refuses_templates_that_render_the_wrong_signing(self) -> None:
        managed = (ROOT / "home/dot_config/git/config.tmpl").read_text()
        guard = '{{- $signing := stat (joinPath .chezmoi.homeDir ".ssh/id_ed25519.pub") }}\n'
        if_line = "{{- if $signing }}\n"
        self.assertIn(guard, managed)
        self.assertEqual(2, managed.count(if_line))
        mutations = {
            # Audit of 52e28100: an else right after each guard signs only when the key is absent.
            "else after the guard": (
                managed.replace(if_line, if_line + "{{- else }}\n"),
                "rendered with the signing key present",
            ),
            "unconditional signing": (
                managed.replace(guard, "{{- $signing := true }}\n"),
                "rendered without the signing key",
            ),
            "gpgsign outside the guard": (
                managed.replace(
                    "{{- if $signing }}\n[commit]\n\tgpgsign = true\n",
                    "[commit]\n\tgpgsign = true\n{{- if $signing }}\n",
                ),
                "without the signing key must not set commit.gpgsign",
            ),
            "format dropped": (managed.replace("\tformat = ssh\n", ""), "must set gpg.format exactly once"),
            "guard dropped": (managed.replace(guard, ""), "could not render"),
            # Audit of 551f3439: git reads [Commit] as [commit], so an unconditional one signs without the key.
            "unconditional [Commit]": (managed + "[Commit]\n\tgpgsign = true\n", "commit.gpgsign"),
            "mixed-case section and key": (managed + "[COMMIT]\n\tGpgSign = true\n", "commit.gpgsign"),
            "mixed-case format outside the guard": (managed + "[GPG]\n\tFormat = ssh\n", "gpg.format"),
            "gpgsign false beside the guarded one": (
                managed.replace("[pull]\n", "[Commit]\n\tgpgsign = false\n[pull]\n"),
                "commit.gpgsign",
            ),
            "include directive": (managed + "[include]\n\tpath = ~/.gitconfig.local\n", "[include] or [includeIf]"),
            "includeIf directive": (
                managed + '[IncludeIf "gitdir:~/work/"]\n\tpath = ~/.gitconfig.work\n',
                "[include] or [includeIf]",
            ),
            "include hidden from the text check": (
                managed + '{{ "[" }}include]\n\tpath = ~/.gitconfig.local\n',
                "must not include other config: include.path",
            ),
        }
        for name, (template, message) in mutations.items():
            with self.subTest(mutation=name):
                self.assertNotEqual(managed, template)
                self.assertIn(message, self.git_config_failure(template) or "")

    def test_git_config_names_a_missing_chezmoi(self) -> None:
        self.write_text_file("home/dot_config/git/config.tmpl", "[user]\n")
        old_path = os.environ.get("PATH", "")
        old_override = os.environ.pop("DOTFILES_CHEZMOI", None)
        os.environ["PATH"] = str(self.temp_dir / "no-bin")
        stderr = io.StringIO()
        try:
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                self.module.validate_git_config()
        finally:
            os.environ["PATH"] = old_path
            if old_override is not None:
                os.environ["DOTFILES_CHEZMOI"] = old_override
        self.assertIn("chezmoi is required", stderr.getvalue())

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
                "omp": {"model": "claude-bridge/claude-model", "effort": "high"},
            }
            for name in ("express", "standard", "review", "deep", "security", "audit")
        }
        profiles["security"]["codex"].update(model="gpt-6-astra", sandbox_mode="read-only")
        profiles["audit"]["codex"].update(model="gpt-6-astra", model_reasoning_effort="xhigh", sandbox_mode="read-only")
        profiles["standard"]["claude"]["advisor"] = "fable"
        bridge = "~/.local/lib/omp-extensions/pi-claude-bridge"
        siwc = "~/.agents/omp/extensions/openai-siwc"
        manifest = {
            "schema_version": 1,
            "model_profiles": profiles,
            "interactive_profile": "deep",
            "omp": {
                "extensions": [bridge],
                "extension_providers": {"claude-bridge": bridge, "openai-siwc": siwc},
            },
            "claude": {"levers": {"extensions": [bridge, siwc]}},
            "codex": {"plugins": {"crit@mryfmo-personal-plugins": {"enabled": True}}},
            "mcp_servers": {},
        }
        self.module.load_yaml = lambda _path: manifest
        return manifest

    def test_agent_manifest_accepts_exact_security_profile_set(self) -> None:
        self.write_valid_agent_manifest()

        self.module.validate_agent_manifest()

    def test_agent_manifest_accepts_the_three_omp_providers_and_rejects_others(self) -> None:
        accepted = (
            "claude-bridge/claude-model",
            "openai-siwc/gpt-model",
            "anthropic/claude-model",
        )
        for value in accepted:
            with self.subTest(value=value):
                manifest = self.write_valid_agent_manifest()
                manifest["model_profiles"]["audit"]["omp"]["model"] = value
                self.module.validate_agent_manifest()
        for value in ("foo/bar", "claude-bridge/claude model", "claude-model", "openai-codex/gpt-model", None):
            with self.subTest(value=value):
                manifest = self.write_valid_agent_manifest()
                if value is None:
                    del manifest["model_profiles"]["audit"]["omp"]
                else:
                    manifest["model_profiles"]["audit"]["omp"]["model"] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn("model profile audit", stderr.getvalue())

    def test_agent_manifest_applies_the_generators_profile_rules(self) -> None:
        """F169: the validator refuses exactly what the generator refuses, through the generator's own check."""
        manifest = self.write_valid_agent_manifest()
        manifest["model_profiles"]["audit"]["omp"]["effort"] = "auto"
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agent_manifest()
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.generator().model_profiles(manifest)

    def test_agent_manifest_requires_the_extension_that_registers_the_interactive_omp_provider(self) -> None:
        bridge = "~/.local/lib/omp-extensions/pi-claude-bridge"
        siwc = "~/.agents/omp/extensions/openai-siwc"
        for model, extensions, needed in (
            ("claude-bridge/claude-model", [], bridge),
            ("claude-bridge/claude-model", [siwc], bridge),
            ("openai-siwc/gpt-model", [bridge], siwc),
        ):
            with self.subTest(model=model, extensions=extensions):
                manifest = self.write_valid_agent_manifest()
                manifest["model_profiles"]["deep"]["omp"]["model"] = model
                manifest["omp"]["extensions"] = extensions
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn(
                    f"interactive_profile omp model {model} needs {needed} in omp.extensions", stderr.getvalue()
                )
        for model, extensions in (
            ("claude-bridge/claude-model", [bridge]),
            ("openai-siwc/gpt-model", [siwc]),
            ("anthropic/claude-model", []),
        ):
            with self.subTest(model=model, extensions=extensions):
                manifest = self.write_valid_agent_manifest()
                manifest["model_profiles"]["deep"]["omp"]["model"] = model
                manifest["omp"]["extensions"] = extensions
                self.module.validate_agent_manifest()
        # Only the interactive profile reaches a plain launch; a seat profile's route needs no entry here.
        manifest = self.write_valid_agent_manifest()
        manifest["model_profiles"]["audit"]["omp"]["model"] = "openai-siwc/gpt-model"
        self.module.validate_agent_manifest()

    def test_the_default_model_provider_stays_loadable_when_its_mapping_is_removed(self) -> None:
        """A plain omp launch must load the default model's provider: dropping its extension_providers entry, with or
        without emptying omp.extensions, is refused, as is an entry for a route omp provides or does not know."""
        for name, mutate in (
            (
                "bridge entry removed, extensions emptied",
                lambda m: (m["omp"]["extension_providers"].pop("claude-bridge"), m["omp"].update(extensions=[])),
            ),
            ("bridge entry removed", lambda m: m["omp"]["extension_providers"].pop("claude-bridge")),
            (
                "builtin route mapped",
                lambda m: m["omp"]["extension_providers"].update({"anthropic": "~/.agents/omp/extensions/openai-siwc"}),
            ),
            (
                "unknown route mapped",
                lambda m: m["omp"]["extension_providers"].update({"other": "~/.agents/omp/extensions/openai-siwc"}),
            ),
        ):
            with self.subTest(name=name):
                manifest = self.write_valid_agent_manifest()
                mutate(manifest)
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
        manifest = self.write_valid_agent_manifest()
        manifest["model_profiles"]["deep"]["omp"]["model"] = "anthropic/claude-model"
        manifest["omp"]["extensions"] = []
        self.module.validate_agent_manifest()

    def test_agent_manifest_keeps_every_omp_extension_directory_among_the_seat_extensions(self) -> None:
        """F162: omp.extensions and omp.extension_providers name only claude.levers.extensions directories."""
        for mutate in (
            lambda manifest: manifest["omp"]["extension_providers"].update({"openai-siwc": "~/elsewhere/siwc"}),
            lambda manifest: manifest["omp"]["extensions"].append("~/elsewhere/ext"),
            lambda manifest: manifest["claude"]["levers"]["extensions"].remove("~/.agents/omp/extensions/openai-siwc"),
            lambda manifest: manifest["omp"].pop("extension_providers"),
        ):
            with self.subTest(mutate=mutate):
                manifest = self.write_valid_agent_manifest()
                mutate(manifest)
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()

    def test_agent_manifest_requires_review_to_match_deep_claude_model_and_effort(self) -> None:
        """F164 (INV-7): the review profile's Claude model and effort are deep's."""
        for key, value in (("model", "other-model"), ("effort", "low")):
            with self.subTest(key=key):
                manifest = self.write_valid_agent_manifest()
                manifest["model_profiles"]["review"]["claude"][key] = value
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_agent_manifest()
                self.assertIn("INV-7", stderr.getvalue())

    def test_agent_manifest_requires_fable_advisor_on_the_standard_profile(self) -> None:
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
                    "installer": "install/common/aws_cli.sh",
                },
                "plugins": {
                    "source": "claude-plugin",
                    "upstream": "marketplaces",
                    "pin": "per-plugin",
                    "verify": "installed-version",
                    "plugins": {"crit@crit": {"marketplace": "tomasz-tomczyk/crit", "pin": "1.8.10"}},
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
            "float plugin pin": lambda assets: assets["plugins"]["plugins"]["crit@crit"].update(pin=1.1),
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
                "file": "install/common/aws_cli.sh",
                "constants": {"AWS_CLI_FINGERPRINT": "gpg_fingerprint"},
            },
        )
        return manifest

    def test_assets_accept_rolling_releases_without_pins(self) -> None:
        self.write_text_file("install/common/aws_cli.sh", 'readonly AWS_CLI_FINGERPRINT="FB5D"\n')

        self.module.validate_assets(self.rolling_asset_manifest())

    def test_assets_reject_invalid_rolling_and_pinned_declarations(self) -> None:
        self.write_text_file("install/common/aws_cli.sh", 'readonly AWS_CLI_FINGERPRINT="FB5D"\n')
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

    def test_mcp_parity_compares_the_manifest_with_codex_only(self) -> None:
        self.module.validate_mcp_parity({"mcp_servers": {}}, {"mcp_servers": {}})
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_mcp_parity({"mcp_servers": {}}, {"mcp_servers": {"x": {}}})
        self.assertIn("MCP server names differ", stderr.getvalue())

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
            ("sandbox_mode", "workspace-write"),
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

    def valid_claude_sandbox(self, os_name: str = "darwin") -> dict:
        return {
            "enabled": True,
            "failIfUnavailable": True,
            "allowUnsandboxedCommands": False,
            "autoAllowBashIfSandboxed": True,
            "excludedCommands": list(self.module.SANDBOX_EXCLUSIONS),
            "filesystem": {
                "allowWrite": list(self.codex_writable_roots),
                "denyRead": ["~/**/.env", "~/**/.env.*"],
            },
            "credentials": {
                "files": [{"path": path, "mode": "deny"} for path in self.module.SANDBOX_CREDENTIAL_DENIES],
                "envVars": [{"name": "CLAUDE_CODE_OAUTH_TOKEN", "mode": "deny"}],
            },
            "network": {"allowedDomains": ["github.com", "api.github.com"]},
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
        self.write_levers(
            "hcom-seat", "hcom-dispatch", "bus-history.sh", "worktree-gc.sh", "worker-worktree.sh", "regime-init"
        )
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

        # U68 round 2: Claude Code 2.1.310 reads `Bash(dangerouslyDisableSandbox:true)` as a literal command and keeps
        # an allow on the retry, so the boundary is strict mode plus a prompted exclusion, never that rule.
        def without_push_ask(candidate: dict) -> None:
            candidate["claude"]["permissions"]["ask"].remove("Bash(git push *)")

        def without_gh_ask(candidate: dict) -> None:
            candidate["claude"]["permissions"]["ask"].remove("Bash(gh *)")

        def with_retry(candidate: dict) -> None:
            candidate["claude"]["sandbox"]["allowUnsandboxedCommands"] = True

        def with_dead_rule(candidate: dict) -> None:
            candidate["claude"]["permissions"]["ask"].append("Bash(dangerouslyDisableSandbox:true)")

        def with_lever_excluded(candidate: dict) -> None:
            candidate["claude"]["sandbox"]["excludedCommands"].append("~/.local/bin/common/hcom-seat *")

        def with_gh_hosts_masked(candidate: dict) -> None:
            # Round 6: a mask lets the proxy write the real token into a body api.github.com echoes back (/markdown).
            for entry in candidate["claude"]["sandbox"]["credentials"]["files"]:
                if entry["path"] == "~/.config/gh/hosts.yml":  # lint-comparisons: allow settings text
                    entry.update(mode="mask", extract="oauth_token:\\s*(\\S+)", injectHosts=["api.github.com"])

        def with_tls_termination(candidate: dict) -> None:
            candidate["claude"]["sandbox"]["network"]["tlsTerminate"] = {}

        for name, mutate, message in (
            ("unprompted git push exclusion", without_push_ask, "Bash(<pattern>) for each excluded command"),
            ("unprompted gh exclusion", without_gh_ask, "Bash(<pattern>) for each excluded command"),
            ("unsandboxed retry", with_retry, "allowUnsandboxedCommands must be false"),
            ("literal retry rule", with_dead_rule, "must not name dangerouslyDisableSandbox"),
            ("allowed lever excluded", with_lever_excluded, "excludedCommands must be exactly"),
            ("gh hosts file masked", with_gh_hosts_masked, "must all be exactly path and deny (no mask)"),
            ("TLS termination", with_tls_termination, "tlsTerminate must not be set"),
        ):
            with self.subTest(form=name):
                candidate = copy.deepcopy(manifest)
                mutate(candidate)
                self.write_text_file(
                    "home/.chezmoitemplates/claude-settings-managed.json", generator.render_claude_settings(candidate)
                )
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_claude_settings(candidate)
                self.assertIn(message, stderr.getvalue())

        template = generator.render_claude_settings(manifest)
        widened = template.replace(
            '"defaultMode": "auto",', '"defaultMode": "auto", "additionalDirectories": ["~/"],', 1
        )
        self.assertNotEqual(template, widened)
        self.write_text_file("home/.chezmoitemplates/claude-settings-managed.json", widened)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_claude_settings(manifest)
        self.assertIn("permissions.additionalDirectories entries must be exactly one of", stderr.getvalue())

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
        self.write_levers(
            "hcom-seat", "hcom-dispatch", "bus-history.sh", "worktree-gc.sh", "worker-worktree.sh", "regime-init"
        )
        for permissions in ({}, {"allow": []}, {"allow": ["Bash(hcom list *)"]}, {"allow": MANAGED_ALLOW}):
            with self.subTest(accepts=permissions):
                self.module.validate_claude_permissions_allow(permissions, "permissions")
        pinned = {
            "hcom-seat": "0" * 64,
            "hcom-dispatch": "0" * 64,
            "bus-history.sh": "0" * 64,
            "worktree-gc.sh": "0" * 64,
            "worker-worktree.sh": "0" * 64,
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
        self.write_levers(
            "hcom-seat", "hcom-dispatch", "bus-history.sh", "worktree-gc.sh", "worker-worktree.sh", "regime-init"
        )
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

    def test_the_omp_writing_seats_allow_only_the_merge_and_installed_levers(self) -> None:
        """U28: the committed orchestrator.yml and worker.yml pass; every other allow form is refused."""
        self.module.ROOT = ROOT
        manifest = load_manifest_fixture(self.temp_dir)
        # The overlays parsed by chezmoi's fromYaml, as load_manifest_fixture parses the manifest: `make unit-test`
        # gives the test process no PyYAML, and without it validate_omp_policies refuses to read the files.
        policies = {
            role: render_claude_template(
                "{{ fromYaml "
                + json.dumps((ROOT / f"home/dot_agents/omp/policies/{role}.yml").read_text())
                + " | toJson }}",
                self.temp_dir,
            )
            for role in self.module.omp_policy_roles()
        }
        self.assertEqual(["audit", "orchestrator", "worker"], sorted(policies))
        self.module.validate_omp_policies(manifest, policies)
        # U71 audit rounds 3, 8 and 9: in every policy file an allow row that reaches GitHub must be on its role's
        # allowlist; merge spellings are not enumerated, so the GraphQL mutation and any gh write are refused too.
        allowed = self.module.OMP_GITHUB_ALLOWLIST
        self.assertEqual(sorted(allowed), sorted(policies))
        for role, policy in policies.items():
            reaching = [
                rule["match"]
                for rule in policy["bash"]["patterns"]
                if rule["approval"] == "allow" and self.module.OMP_GITHUB_REACH.search(rule["match"])
            ]
            self.assertEqual(sorted(reaching), sorted(allowed[role]), role)
        for role in sorted(policies):
            for row in (
                "gh pr merge 541 --squash --match-head-commit *",
                "gh api repos/o/r/pulls/541/merge *",
                "gh api repos/o/r/merges *",
                "curl -X POST https://api.github.com/repos/o/r/merges *",
                "gh api graphql -f query='mutation { mergePullRequest(input: {pullRequestId: \"x\"}) { clientMutationId } }'",
                "gh api graphql *",
                "gh issue create *",
                "gh pr view 1 --json body && gh pr close 1",
                "GH_TOKEN=x gh api user",
                "wget -qO- https://example.com",
                "gh api repos/* ",
            ):
                with self.subTest(role=role, row=row):
                    injected = json.loads(json.dumps(policies))
                    injected[role]["bash"]["patterns"].insert(0, {"match": row, "approval": "allow"})
                    with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                        self.module.validate_omp_policies(manifest, injected)
                    self.assertIn(f"reaches GitHub and is not on the {role} allowlist", stderr.getvalue())
        # each allowlisted row passes in its own role, and only there
        for role, rows in allowed.items():
            for row in rows:
                for other in sorted(policies):
                    with self.subTest(row=row, into=other):
                        injected = json.loads(json.dumps(policies))
                        patterns = injected[other]["bash"]["patterns"]
                        patterns[:] = [rule for rule in patterns if rule["match"] != row]
                        patterns.append({"match": row, "approval": "allow"})
                        if other == role:
                            self.module.validate_omp_policies(manifest, injected)
                        else:
                            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                                self.module.validate_omp_policies(manifest, injected)
        if self.module.yaml is None:
            with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                self.module.validate_omp_policies(manifest)
            self.assertIn("PyYAML is required", stderr.getvalue())
        self.module.ROOT = self.temp_dir
        self.write_levers("pr-close.sh", "python3")
        pinned = {"pr-close.sh": "0" * 64, "python3": "0" * 64}

        def policy(*matches: str) -> dict:
            return {"bash": {"patterns": [{"match": match, "approval": "allow"} for match in matches]}}

        merge = "gh pr merge * --squash --match-head-commit *"
        installed = "~/.local/bin/common/pr-close.sh --from-table *"
        self.module.validate_omp_policy_allow(policy(installed), "orchestrator.yml", pinned)
        self.module.validate_omp_policy_allow(policy("~/.local/bin/common/pr-close.sh *"), "worker.yml", pinned)
        # U28b F3: the exact bare form of a lever that acts without arguments.
        self.module.validate_omp_policy_allow(policy("~/.local/bin/common/pr-close.sh"), "orchestrator.yml", pinned)
        cases = {
            merge: "is not ~/.local/bin/common/<lever>",  # U71: no raw merge allow, even for the orchestrator
            "gh pr close *": "is not ~/.local/bin/common/<lever>",
            "gh api *": "is not ~/.local/bin/common/<lever>",
            "*": "is not ~/.local/bin/common/<lever>",
            "bash *": "is not ~/.local/bin/common/<lever>",
            "~/.local/bin/common/pr-close.sh x": "is not ~/.local/bin/common/<lever>",
            "~/.local/bin/common/pr-close.sh*": "is not ~/.local/bin/common/<lever>",
            "~/.local/bin/common/pr-close.sh --from-table x *": "is not ~/.local/bin/common/<lever>",
            "~/.local/bin/common/pr-close.sh * && *": "is not ~/.local/bin/common/<lever>",
            "/Users/x/.local/bin/common/pr-close.sh *": "is not ~/.local/bin/common/<lever>",
            "scripts/orchestrator/pr-close.sh *": "names a lever inside the rewritable checkout",
            "./scripts/orchestrator/pr-close.sh --from-table *": "names a lever inside the rewritable checkout",
            "*scripts/orchestrator/pr-close.sh *": "names a lever inside the rewritable checkout",
            "~/.local/bin/common/absent.sh *": "absent.sh is not a regular file",
            "~/.local/bin/common/python3 *": "python3 is named as an interpreter",
        }
        for match, message in cases.items():
            with self.subTest(rejects=match):
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_omp_policy_allow(policy(match), "seat.yml", pinned)
                self.assertIn(message, stderr.getvalue())
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_omp_policy_allow(policy(installed), "seat.yml", {})
        self.assertIn("no claude.levers.sha256 pin for pr-close.sh", stderr.getvalue())
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_omp_policy_allow({"bash": {"patterns": "x"}}, "seat.yml", pinned)
        self.assertIn("bash.patterns must be a list of rules", stderr.getvalue())

    def test_the_worker_push_allows_are_accepted_only_in_worker_yml_and_only_before_their_catch_rows(self) -> None:
        """U76 rounds 5 and 6: the worker's three exact push lines are the one non-lever allow in a writing seat, and
        only directly before the catch-all push denies; a wildcard push allow is refused."""
        module = self.module
        self.assertFalse([match for match in module.OMP_WORKER_PUSH_ALLOW if "*" in match])
        rows = [
            *({"match": m, "approval": "allow"} for m in module.OMP_WORKER_PUSH_ALLOW),
            *({"match": m, "approval": "deny"} for m in module.OMP_WORKER_PUSH_CATCH),
        ]
        module.validate_omp_policy_allow({"bash": {"patterns": rows}}, "worker.yml", {}, "worker")
        broken = {
            "orchestrator role": (rows, "orchestrator"),
            "catch-all dropped": (rows[:-1], "worker"),
            "an allow dropped": (rows[1:], "worker"),
            "catch before the allows": (rows[3:] + rows[:3], "worker"),
            "the round-5 wildcard allow": (rows + [{"match": "git push origin *", "approval": "allow"}], "worker"),
        }
        for name, (patterns, role) in broken.items():
            with (
                self.subTest(broken=name),
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                module.validate_omp_policy_allow({"bash": {"patterns": patterns}}, "worker.yml", {}, role)

    def test_claude_sandbox_requires_the_ssh_credential_deny_and_home_or_absolute_deny_read(self) -> None:
        cases = {
            "no credentials": (lambda sandbox: sandbox.pop("credentials"), "credentials.files must contain"),
            "ssh allowed": (
                lambda sandbox: sandbox["credentials"].update(files=[{"path": "~/.ssh", "mode": "allow"}]),
                "credentials.files entries must all be exactly path and deny",
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

    def test_claude_sandbox_refuses_each_way_out_of_the_boundary(self) -> None:
        """U68: credential stores denied, no write reaching PATH or mise trust state, no socket, fail closed."""

        def without_file(path: str):
            def mutate(sandbox: dict) -> None:
                files = sandbox["credentials"]["files"]
                files[:] = [e for e in files if e["path"] != path]  # lint-comparisons: allow settings text

            return mutate

        def hosts(**change):
            def mutate(sandbox: dict) -> None:
                for entry in sandbox["credentials"]["files"]:
                    if entry["path"] == "~/.config/gh/hosts.yml":  # lint-comparisons: allow settings text
                        entry.update(change)

            return mutate

        cases = {
            "fails open": (lambda sandbox: sandbox.update(failIfUnavailable=False), "failIfUnavailable must be true"),
            "uv tools writable": (
                lambda sandbox: sandbox["filesystem"]["allowWrite"].append("~/.local/share/uv"),
                "must be exactly one of",
            ),
            "mise trust writable": (
                lambda sandbox: sandbox["filesystem"]["allowWrite"].append("~/.local/state/mise"),
                "must be exactly one of",
            ),
            "a parent of PATH writable": (
                lambda sandbox: sandbox["filesystem"]["allowWrite"].append("~/.local"),
                "must be exactly one of",
            ),
            "uv python writable": (
                lambda sandbox: sandbox["filesystem"]["allowWrite"].append("~/.local/share/uv/python"),
                "must be exactly one of",
            ),
            "age key readable": (without_file("~/.config/age/key.txt"), "deny entry for each credential store"),
            "codex login readable": (without_file("~/.codex/auth.json"), "deny entry for each credential store"),
            "gh hosts unlisted": (without_file("~/.config/gh/hosts.yml"), "~/.config/gh/hosts.yml"),
            # Round 6: no mask of any kind, on any OS: the proxy would write the real token into an echoed body.
            "gh hosts masked": (
                hosts(mode="mask", extract="oauth_token:\\s*(\\S+)", injectHosts=["api.github.com"]),
                "must all be exactly path and deny (no mask)",
            ),
            "gh hosts allowed": (hosts(mode="allow"), "must all be exactly path and deny (no mask)"),
            "deny with mask fields": (hosts(injectHosts=["api.github.com"]), "must all be exactly path and deny"),
            "another file masked": (
                lambda sandbox: sandbox["credentials"]["files"].append({"path": "~/.netrc", "mode": "mask"}),
                "must all be exactly path and deny (no mask)",
            ),
            "a variable masked": (
                lambda sandbox: sandbox["credentials"]["envVars"].append({"name": "GH_TOKEN", "mode": "mask"}),
                "envVars entries must all be exactly name and deny",
            ),
            "plaintext injection": (
                lambda sandbox: sandbox["credentials"].update(allowPlaintextInject=True),
                "allowPlaintextInject must not be set",
            ),
            "TLS termination": (
                lambda sandbox: sandbox["network"].update(tlsTerminate={}),
                "tlsTerminate must not be set",
            ),
            # Round 5: every entry is checked and no path or variable may appear twice (Claude keeps the later).
            "a path listed twice": (
                lambda sandbox: sandbox["credentials"]["files"].append({"path": "~/.codex/auth.json", "mode": "deny"}),
                "must name each path once",
            ),
            "a variable listed twice": (
                lambda sandbox: sandbox["credentials"]["envVars"].append(
                    {"name": "CLAUDE_CODE_OAUTH_TOKEN", "mode": "deny"}
                ),
                "must name each variable once",
            ),
            "token env passed": (
                lambda sandbox: sandbox["credentials"].update(envVars=[]),
                "envVars must deny",
            ),
            "herdr socket": (
                lambda sandbox: sandbox["network"].update(allowUnixSockets=["~/.config/herdr/herdr.sock"]),
                "allowUnixSockets must not list a socket",
            ),
        }
        for name, (breaks, message) in cases.items():
            with self.subTest(rule=name):
                sandbox = self.valid_claude_sandbox()
                breaks(sandbox)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
                self.assertIn(message, stderr.getvalue())
        linux_cases = {
            "Linux TLS termination": (
                lambda sandbox: sandbox["network"].update(tlsTerminate={}),
                "tlsTerminate must not be set",
            ),
            "Linux socket list": (
                lambda sandbox: sandbox["network"].update(allowUnixSockets=[]),
                "allowUnixSockets must not list a socket",
            ),
        }
        for name, (breaks, message) in linux_cases.items():
            with self.subTest(rule=name):
                sandbox = self.valid_claude_sandbox("linux")
                breaks(sandbox)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox", "linux")
                self.assertIn(message, stderr.getvalue())
        self.module.validate_claude_sandbox(self.valid_claude_sandbox("linux"), self.codex_writable_roots, "s", "linux")
        sandbox = self.valid_claude_sandbox()
        sandbox["network"]["allowUnixSockets"] = []
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

    def test_claude_sandbox_allow_write_refuses_any_form_off_the_allowlist(self) -> None:
        sandbox = self.valid_claude_sandbox()
        sandbox["filesystem"]["allowWrite"].append("~/.cache/uv")
        self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
        for path in ("relative/cache", "~cache", "/tmp/*", 7, None):
            with self.subTest(path=path):
                sandbox = self.valid_claude_sandbox()
                sandbox["filesystem"]["allowWrite"].append(path)
                with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                    self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
                self.assertIn("allowWrite entries must be exactly one of", stderr.getvalue())

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
                "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
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
                "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
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

    def test_codex_config_with_a_key_codex_removed_is_refused(self) -> None:
        """`personality` and `features.plugin_hooks` set nothing on Codex 0.163.0; the validator refuses them (U79)."""
        self.write_codex_config(f"network_access = false\nwritable_roots = {json.dumps(self.codex_writable_roots)}")
        config = self.temp_dir / "home/.chezmoitemplates/codex-config-managed.toml"
        valid = config.read_text()
        manifest = {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
            "interactive_profile": "standard",
            "codex": {
                "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
                "sandbox_workspace_write": {"network_access": False, "writable_roots": self.codex_writable_roots},
                "shell_environment_policy": {
                    "inherit": "core",
                    "set": {"PATH": "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin"},
                },
            },
        }
        for removed in (
            valid.replace(
                'sandbox_mode = "workspace-write"', 'sandbox_mode = "workspace-write"\npersonality = "pragmatic"'
            ),
            valid.replace("hooks = true", "hooks = true\nplugin_hooks = true"),
        ):
            with self.subTest(removed=removed):
                config.write_text(removed)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_codex_config(manifest)
                self.assertIn("which Codex 0.163.0 removed", stderr.getvalue())

    def test_every_write_root_list_accepts_only_the_exact_allowlisted_spellings(self) -> None:
        """U68 audits 1-3: an exact allowlist on Claude allowWrite, Codex roots and additionalDirectories."""
        unlisted = [
            # Round 3: case folding, a `/root` traversal, and the parent of a nonstandard home.
            "~/.LOCAL/share/uv",
            "~/.Cache/uv",
            "~/../home/bob/.local/share/uv",
            "/srv",
            # Round 2: `..` routes into another home or above one.
            f"~/../{Path.home().name}/.local/share/uv",
            "~/../someone/.local/bin",
            "$HOME/../someone/.local/state/mise",
            "{{ .chezmoi.homeDir }}/../someone/.local/share/mise",
            "~/..",
            "~/../..",
            "~/../../Users/someone/.local/bin",
            "/Users/someone/../someone/.local/share/uv",
            "/home/someone/../someone/.local/bin",
            "/home/someone/../../Users/other/.local/share/mise",
            # Round 1: roots, homes, ancestors and descendants of PATH directories and mise trust state.
            "/",
            "//",
            "~",
            "~/",
            "~/.local",
            "~/.local/",
            "~/.local/share/uv",
            "~/.local/share/uv/",
            "~/.local/share/uv/tools/hcom",
            "~/.cache/../.local/bin",
            "~/./.local/state//mise",
            "$HOME/.local/bin",
            "{{ .chezmoi.homeDir }}/.local/share/mise",
            "{{ .chezmoi.homeDir }}",
            "/Users",
            "/Users/someone/.local/bin",
            "/home/someone",
            "/home/someone/.local/state/mise/trusted-configs",
            str(Path.home() / ".local/share/uv"),
            # Other spellings of allowlisted roots are refused too: only the listed bytes pass.
            "~/.cache/uv/",
            "$HOME/.cache/uv",
            "{{ .chezmoi.homeDir }}/.cache/uv",
            str(Path.home() / ".cache/uv"),
            " ~/.cache/uv",
            "~/.local/statex",
            "/tmp/build",
            "relative/root",
            "../escape",
            "~/.cache/*",
        ]
        with mock.patch.dict(os.environ, {"HOME": "/srv/operator"}):
            for root in unlisted:
                with self.subTest(list="claude allowWrite", root=root):
                    sandbox = self.valid_claude_sandbox()
                    sandbox["filesystem"]["allowWrite"].append(root)
                    with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                        self.module.validate_claude_sandbox(sandbox, self.codex_writable_roots, "sandbox")
                    self.assertIn("must be exactly one of", stderr.getvalue())
                with self.subTest(list="shared Codex root via the Claude sandbox", root=root):
                    roots = [*self.codex_writable_roots, root]
                    sandbox = self.valid_claude_sandbox()
                    sandbox["filesystem"]["allowWrite"] = list(roots)
                    with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
                        self.module.validate_claude_sandbox(sandbox, roots, "sandbox")
                    self.assertIn("must be exactly one of", stderr.getvalue())
        for os_name in ("darwin", "linux"):
            with self.subTest(accepts_all_on=os_name):
                permitted = list(self.module.SANDBOX_WRITE_ROOTS)
                if os_name == "darwin":
                    permitted += self.module.DARWIN_SANDBOX_WRITE_ROOTS
                self.module.validate_write_roots(permitted, "roots", os_name)
                sandbox = self.valid_claude_sandbox(os_name)
                sandbox["filesystem"]["allowWrite"] = permitted
                self.module.validate_claude_sandbox(sandbox, [], "sandbox", os_name)
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_write_roots(["~/Library/Caches/mise"], "roots", "linux")
        self.assertIn("must be exactly one of", stderr.getvalue())

        roots = ["{{ .chezmoi.homeDir }}/.local/share/uv"]
        self.write_codex_config(f"network_access = false\nwritable_roots = {json.dumps(roots)}")
        manifest = {
            "model_profiles": {"standard": {"codex": {"model": "gpt-5.5", "model_reasoning_effort": "high"}}},
            "interactive_profile": "standard",
            "codex": {
                "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
                "sandbox_workspace_write": {"network_access": False, "writable_roots": roots},
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
        with contextlib.redirect_stderr(io.StringIO()) as stderr, self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)
        self.assertIn("sandbox_workspace_write.writable_roots entries must be exactly one of", stderr.getvalue())

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
                "config_path": "home/.chezmoitemplates/codex-config-managed.toml",
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
            f'{API_KEY} = "{HIGH_ENTROPY_VALUE}"\n',
        )
        path.chmod(0o755)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()

    def test_secret_scan_checks_docs_paths(self) -> None:
        self.write_text_file("docs/reference/leaky.md", f'{FIELD} = "{HIGH_ENTROPY_VALUE}"\n')

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

    def test_secret_scan_reports_every_finding_in_one_run(self) -> None:
        first = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        second = "ghp_" + "Z9y8X7w6V5u4T3s2R1q0P9o8N7m6L5k4J3i2"
        self.write_text_file("docs/a.md", f"one\n{first}\n")
        self.write_text_file("scripts/b.sh", f"two\n\n{second}\n")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            self.module.validate_no_obvious_secrets()

        self.assertEqual(raised.exception.code, 1)
        report = stderr.getvalue()
        self.assertIn("2 finding(s) in the committed-secret scan", report)
        self.assertIn("possible committed secret docs/a.md:github-pat:2 ghp_... (GitHub personal access token)", report)
        self.assertIn("possible committed secret scripts/b.sh:github-pat:3 ghp_...", report)
        for token in (first, second):
            self.assertNotIn(token[4:], report, "the report shows a secret's first four characters only")

    def test_secret_scan_judges_a_quoted_assignment_by_its_entropy(self) -> None:
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        path = self.write_text_file("docs/notes.md", "")
        for text in (
            f'{FIELD} = "{LOW_ENTROPY_VALUE}"\n',
            f"{PASSWORD_KEY} = 'password123'\n",
            f'{API_KEY}: "{LOW_ENTROPY_VALUE}"\n',
        ):
            with self.subTest(text=text):
                path.write_text(text)
                self.module.validate_no_obvious_secrets()
        for text, rule in (
            (f'{FIELD} = "{HIGH_ENTROPY_VALUE}"\n', "generic-token"),
            (f"{SECRET_KEY}: '{HIGH_ENTROPY_VALUE}'\n", "generic-secret"),
            (f'{PASSWORD_KEY} = "{HIGH_ENTROPY_VALUE}"\n', "generic-password"),
            (f'{API_KEY.replace("_", "-")} = "{HIGH_ENTROPY_VALUE}"\n', "generic-api-key"),
            (f'{FIELD} = "{planted}"\n', "github-pat"),
            # A split literal: the provider rule sees no token body, but the token's characters are on the line and
            # the generic rule measures the whole rest of the line, so the split token is reported under it.
            (f'{FIELD} = "ghp_" + "{planted[4:]}"\n', "generic-token"),
        ):
            with self.subTest(text=text):
                path.write_text(text)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_no_obvious_secrets()
                self.assertIn(f"docs/notes.md:{rule}:1 ", stderr.getvalue())

    def test_a_masked_quoted_assignment_is_clean_and_a_value_beside_the_marker_is_reported(self) -> None:
        """The masker's own marker is not evidence: a generic rule measures a quoted value's entropy with every
        SECRET_MASK removed, so the masker's output passes the scan, while a value beside the marker is judged on its
        own and a provider token beside it is a finding (round 3 verdict on ce36a3a5: the masked assignment crossed the
        threshold and --scan-identifiers refused cleaned evidence)."""
        module = self.module
        mask = module.SECRET_MASK
        planted = "ghp_" + "a" * 25
        masked, count = module.mask_secret_matches(f'{FIELD} = "prefix {planted}"\n')
        self.assertEqual((masked, count), (f'{FIELD} = "prefix {mask}"\n', 1))
        self.assertEqual(module.secret_findings(masked), [])
        path = self.write_text_file(".orchestration/validation/t-a01.md", "")
        for text in (
            masked,
            f'{FIELD} = "{mask}"\n',
            f'{FIELD} = "{mask}{mask}"\n',
            f'{SECRET_KEY}: "{mask} and {mask}"\n',
            f'{PASSWORD_KEY} = "{mask} {LOW_ENTROPY_VALUE}"\n',
        ):
            with self.subTest(text=text):
                path.write_text(text)
                module.validate_no_obvious_secrets()
        for text, rule in (
            (f'{FIELD} = "{mask} {HIGH_ENTROPY_VALUE}"\n', "generic-token"),
            (f'{PASSWORD_KEY} = "{HIGH_ENTROPY_VALUE}{mask}"\n', "generic-password"),
            (f'{API_KEY}: "{mask}{HIGH_ENTROPY_VALUE}{mask}"\n', "generic-api-key"),
            (f'{FIELD} = "{mask} {planted}"\n', "github-pat"),
        ):
            with self.subTest(text=text):
                path.write_text(text)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    module.validate_no_obvious_secrets()
                self.assertIn(f".orchestration/validation/t-a01.md:{rule}:1 ", stderr.getvalue())

    def test_a_quoted_value_with_the_other_quote_inside_is_measured_whole_and_reported(self) -> None:
        """Round 4 verdict on 43fe25f3: the quoted-value capture stopped at either quote, so `"x'Qz7v..."` was
        measured as `x` and a 4.46-bit value passed both scans. The secret is now the whole rest of the field from the
        opening quote, so no quote inside the value can end it."""
        module = self.module
        apostrophe = "x'" + HIGH_ENTROPY_VALUE
        double_quote = 'it"s' + HIGH_ENTROPY_VALUE
        self.assertEqual(
            [(f.rule.id, f.secret) for f in module.secret_findings(f'{PASSWORD_KEY} = "{apostrophe}"\n')],
            [("generic-password", f'"{apostrophe}"')],
        )
        self.assertEqual(
            [(f.rule.id, f.secret) for f in module.secret_findings(f"{FIELD} = '{double_quote}'\n")],
            [("generic-token", f"'{double_quote}'")],
        )
        path = self.write_text_file("docs/notes.md", f'{PASSWORD_KEY} = "{apostrophe}"\n')
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn("docs/notes.md:generic-password:1 \"x'Q... (a quoted password assignment)", stderr.getvalue())
        self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
        # A word with an apostrophe is still a word.
        path.write_text(f'{PASSWORD_KEY} = "don\'t tell"\n')
        module.validate_no_obvious_secrets()
        # The second literal of a split assignment is on the line, so it is measured with the first: over-capture
        # errs on the refusing side, and a legitimate line is absorbed by a fingerprint row.
        path.write_text(f'{FIELD} = "{LOW_ENTROPY_VALUE}" + "{HIGH_ENTROPY_VALUE}"\n')
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn('docs/notes.md:generic-token:1 "rea... (a quoted token assignment)', stderr.getvalue())

    def test_a_generic_rule_measures_the_whole_rest_of_the_assignment_line(self) -> None:
        """Round 5 verdict on a7b060cd: the quote-matched capture stopped at an escaped quote, so `"x\\"Qz7v..."` was
        measured as `x\\` and a 4.46-bit value passed scanning and masking. A generic rule's secret is now the whole
        rest of the field from the opening quote (to the next tab, line feed or carriage return), trimmed, measured
        with the quotes and backslashes removed, so no quoting decides where the value ends: the three values the
        audits used are reported with the whole text as the secret and masked whole, a trailing comment is captured
        with the value, and the trailing whitespace is not."""
        module = self.module
        mask = module.SECRET_MASK
        escaped = 'x\\"' + HIGH_ENTROPY_VALUE
        planted = "ghp_" + "a" * 60
        for text, expected in (
            (f'{PASSWORD_KEY} = "x\'{HIGH_ENTROPY_VALUE}"\n', [("generic-password", f'"x\'{HIGH_ENTROPY_VALUE}"')]),
            (f'{PASSWORD_KEY} = "{escaped}"\n', [("generic-password", f'"{escaped}"')]),
            # The densest window of the value is the 20-character value itself, so the generic rule reports the line
            # beside the provider rule (round 6 measured the whole value, mostly `a`, under the threshold).
            (
                f'{FIELD} = "{HIGH_ENTROPY_VALUE} {planted}"\n',
                [("generic-token", f'"{HIGH_ENTROPY_VALUE} {planted}"'), ("github-pat", planted)],
            ),
            (
                f'{FIELD} = "{HIGH_ENTROPY_VALUE}"  # rotated\n',
                [("generic-token", f'"{HIGH_ENTROPY_VALUE}"  # rotated')],
            ),
            (f"{SECRET_KEY}: '{HIGH_ENTROPY_VALUE}'\r\n", [("generic-secret", f"'{HIGH_ENTROPY_VALUE}'")]),
        ):
            with self.subTest(text=text):
                self.assertEqual([(f.rule.id, f.secret) for f in module.secret_findings(text)], expected)
                masked, _ = module.mask_secret_matches(text)
                self.assertEqual(masked, f"{mask}{text[len(text.rstrip()) :]}")
                self.assertEqual(module.secret_findings(masked), [])
        trailing = f'{FIELD} = "{HIGH_ENTROPY_VALUE}"   \n'
        self.assertEqual([f.secret for f in module.secret_findings(trailing)], [f'"{HIGH_ENTROPY_VALUE}"'])
        self.assertEqual(module.mask_secret_matches(trailing), (f"{mask}   \n", 1))
        path = self.write_text_file("docs/notes.md", f'{PASSWORD_KEY} = "{escaped}"\n')
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn('docs/notes.md:generic-password:1 "x\\"... (a quoted password assignment)', stderr.getvalue())
        self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
        # The measure removes the writer's syntax, not the value's characters.
        self.assertEqual(module.measured_text(f'"{escaped}"'), "x" + HIGH_ENTROPY_VALUE)
        self.assertEqual(module.measured_text(f'"{mask}"\\'), "")

    def test_a_low_entropy_quoted_word_is_not_a_finding_whatever_its_quoting(self) -> None:
        """The whole-line measure keeps the threshold's other side: a word with an escaped quote, an apostrophe or
        the masker's marker, and a word followed by a comment, are not findings (passes on a7b060cd too)."""
        module = self.module
        path = self.write_text_file("docs/notes.md", "")
        for text in (
            f'{PASSWORD_KEY} = "it\\"s fine"\n',
            f'{PASSWORD_KEY} = "don\'t tell"\n',
            f'{FIELD} = "{module.SECRET_MASK}"\n',
            f'{FIELD} = "{LOW_ENTROPY_VALUE}"  # a name\n',
        ):
            with self.subTest(text=text):
                path.write_text(text)
                self.assertEqual(module.secret_findings(text), [])
                module.validate_no_obvious_secrets()

    def test_a_json_member_with_an_escaped_quote_is_reported_on_the_line_of_its_literal(self) -> None:
        """Round 5 verdict on a7b060cd, in JSON: a decoded string holding a `<key> = "x\\"Qz7v..."` assignment passed
        the per-string scan. It is a finding placed on its literal's line (line 4 of the document), and the masker
        clears it."""
        module = self.module
        escaped = 'x\\"' + HIGH_ENTROPY_VALUE
        document = json.dumps({"items": [{"note": f'{PASSWORD_KEY} = "{escaped}"'}]}, indent=2) + "\n"
        self.assertIn('\\\\"', document)
        path = self.write_text_file("fixtures/evidence.json", document)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn('fixtures/evidence.json:generic-password:4 "x\\"...', stderr.getvalue())
        self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
        masked, count = module.mask_json_strings(json.loads(document))
        self.assertEqual((masked, count), ({"items": [{"note": module.SECRET_MASK}]}, 1))
        path.write_text(json.dumps(masked, indent=2) + "\n")
        module.validate_no_obvious_secrets()

    def test_a_secret_beside_padding_on_its_line_is_found_by_its_densest_window(self) -> None:
        """Round 7 finding on 38a83e45: a line holding two assignments, 160 characters of padding and then a 4.32-bit
        value, was one capture whose entropy over the whole line was under the threshold, so the tree scan and both
        CLIs accepted it in plain text and in JSON. A secret is found by its densest window, not by the average of
        its line: the line is reported under its rule and masked whole, in either order of the two assignments."""
        module = self.module
        mask = module.SECRET_MASK
        padded = f'{FIELD} = "{LOW_ENTROPY_PADDING}" {FIELD} = "{HIGH_ENTROPY_VALUE}"\n'
        secret_first = f'{PASSWORD_KEY} = "{HIGH_ENTROPY_VALUE}" {PASSWORD_KEY} = "{LOW_ENTROPY_PADDING}"\n'
        for text, rule in ((padded, "generic-token"), (secret_first, "generic-password")):
            with self.subTest(text=text):
                secret = text.split(" = ", 1)[1].rstrip()
                self.assertEqual([(f.rule.id, f.secret) for f in module.secret_findings(text)], [(rule, secret)])
                self.assertEqual(module.mask_secret_matches(text), (f"{mask}\n", 1))
                path = self.write_text_file("docs/notes.md", text)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    module.validate_no_obvious_secrets()
                self.assertIn(f"docs/notes.md:{rule}:1 {secret[:4]}...", stderr.getvalue())
                self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
                path.write_text(f"{mask}\n")
                module.validate_no_obvious_secrets()
        # The same line inside a JSON string: reported on its literal's line (line 4 of the document) and masked.
        document = json.dumps({"items": [{"note": padded.rstrip("\n")}]}, indent=2) + "\n"
        path = self.write_text_file("fixtures/evidence.json", document)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn('fixtures/evidence.json:generic-token:4 "low...', stderr.getvalue())
        self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
        masked, count = module.mask_json_strings(json.loads(document))
        self.assertEqual((masked, count), ({"items": [{"note": mask}]}, 1))
        path.write_text(json.dumps(masked, indent=2) + "\n")
        module.validate_no_obvious_secrets()
        # The whole rest of the line is under the threshold; its densest window is the value alone.
        captured = module.measured_text(padded.split(" = ", 1)[1].rstrip())
        self.assertLess(module.shannon_entropy(captured), module.GENERIC_SECRET_ENTROPY)
        self.assertGreaterEqual(module.densest_window_entropy(captured), module.GENERIC_SECRET_ENTROPY)

    def test_a_long_low_entropy_value_alone_is_not_a_finding(self) -> None:
        """The windowed measure keeps the threshold's other side: 160 characters of padding alone, beside the
        masker's marker, beside a word, before a comment, or inside a JSON string has no window over the threshold
        (passes on 38a83e45 too)."""
        module = self.module
        path = self.write_text_file("docs/notes.md", "")
        for text in (
            f'{FIELD} = "{LOW_ENTROPY_PADDING}"\n',
            f'{FIELD} = "{LOW_ENTROPY_PADDING} {module.SECRET_MASK}"\n',
            f'{SECRET_KEY}: "{LOW_ENTROPY_PADDING} {LOW_ENTROPY_VALUE}"\n',
            f'{PASSWORD_KEY} = "{LOW_ENTROPY_PADDING}"  # a name\n',
            json.dumps({"note": f'{FIELD} = "{LOW_ENTROPY_PADDING}"'}, indent=2) + "\n",
        ):
            with self.subTest(text=text):
                path.write_text(text)
                self.assertEqual(module.secret_findings(text), [])
                self.assertEqual(module.mask_secret_matches(text), (text, 0))
                module.validate_no_obvious_secrets()

    def test_a_carriage_return_before_text_ends_the_capture_and_the_value_before_it_is_reported(self) -> None:
        """Round 7 verdict on 1632d807: the capture stopped at a CR and ended with a lookahead for whitespace before the
        LF, so `<key> = "Qz7v..."` followed by a bare CR and text matched nothing and a 4.32-bit value passed the tree
        scan and both CLIs in text and in JSON while origin/main reported it. The capture ends at the CR with no
        lookahead (U107b: a tab, a line feed or a carriage return ends the field): the value before the CR is
        reported and masked, the text after it stays, and a trailing CR is outside the capture."""
        module = self.module
        mask = module.SECRET_MASK
        tail = "\rprogress complete"
        text = f'{FIELD} = "{HIGH_ENTROPY_VALUE}"{tail}\n'
        secret = f'"{HIGH_ENTROPY_VALUE}"'
        self.assertEqual([(f.rule.id, f.secret) for f in module.secret_findings(text)], [("generic-token", secret)])
        self.assertEqual(module.measured_text(secret), HIGH_ENTROPY_VALUE)
        self.assertEqual(module.mask_secret_matches(text), (f"{mask}{tail}\n", 1))
        # A CR between the operator and the quote is whitespace before the value; one before the LF is outside the
        # capture, and the mask leaves the CRLF line ending in place.
        crlf = f'{FIELD} =\r"{HIGH_ENTROPY_VALUE}"\r\n'
        self.assertEqual([f.secret for f in module.secret_findings(crlf)], [f'"{HIGH_ENTROPY_VALUE}"'])
        self.assertEqual(module.mask_secret_matches(crlf), (f"{mask}\r\n", 1))
        path = self.write_text_file("docs/notes.md", text)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn('docs/notes.md:generic-token:1 "Qz7...', stderr.getvalue())
        self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
        path.write_text(f"{mask}{tail}\n")
        module.validate_no_obvious_secrets()
        # The same line inside a JSON string, where the CR is the escape `\r`: reported on its literal's line (line 4
        # of the document) and masked up to the CR.
        document = json.dumps({"items": [{"note": text.rstrip("\n")}]}, indent=2) + "\n"
        self.assertIn("\\r", document)
        path = self.write_text_file("fixtures/evidence.json", document)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn('fixtures/evidence.json:generic-token:4 "Qz7...', stderr.getvalue())
        self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
        masked, count = module.mask_json_strings(json.loads(document))
        self.assertEqual((masked, count), ({"items": [{"note": f"{mask}{tail}"}]}, 1))
        path.write_text(json.dumps(masked, indent=2) + "\n")
        module.validate_no_obvious_secrets()
        # The threshold's other side: a word before a CR and a short word has no window over it (passes on 1632d807
        # too, where the line matched nothing).
        low = f'{FIELD} = "{LOW_ENTROPY_VALUE}"\rok\n'
        self.write_text_file("docs/notes.md", low)
        self.assertEqual(module.secret_findings(low), [])
        self.assertEqual(module.mask_secret_matches(low), (low, 0))
        module.validate_no_obvious_secrets()

    def test_a_generic_rule_scans_a_padded_line_in_linear_time(self) -> None:
        """Round 7 verdict on 1632d807: the lazy capture's lookahead rescanned the rest of the line at every step, so a
        quoted value behind 2,000, 8,000 and 32,000 spaces took 0.018, 0.264 and 4.191 s against 0.0001 s on
        origin/main, and a small padded file could stall validation. The capture is one greedy class to the LF and
        the trailing whitespace is trimmed in code, so the scan is linear in the line.

        The rule: the line is scanned and masked at 2,000, 8,000 and 32,000 padding characters in this process (the
        least of three runs each), the 8,000-to-32,000 step may grow the time by less than 8x, and one loose absolute
        cap of 2 s on any single run still fails a hang. Round 8 bounded every run at 0.5 s, which measured the
        runner's speed, not the scanner's complexity: CI on 1bd17d87 (run 40826819351, the ubuntu-26.04 client row)
        took 0.648 and 0.676 s for 32,000 low-entropy characters, a linear scan on a slow shared runner. Round 9 also
        bounded the 2,000-to-8,000 step, where the 2 to 3 ms fixed cost of a run dominates the 2,000 run: CI on
        17d2d99b (run 40830602891, the macos-15 and ubuntu-26.04 client rows) measured 8.1x there (0.0022 to 0.0179 s,
        0.0032 to 0.0258 s) on the linear scan, so only the step whose runs are tens of milliseconds is judged. The
        value behind the padding is still reported, with the whole rest of the line as the secret."""
        module = self.module
        mask = module.SECRET_MASK
        lengths = (2_000, 8_000, 32_000)
        # 8x per 4x step: a linear scan grows about 4x (the densest-window measure visits one window per character),
        # a quadratic one 16x (the round-7 lookahead grew 14.7x and 16.1x); 8x is the midpoint with headroom for the
        # jitter of a slow shared runner. Judged on the 8,000-to-32,000 step only: at 2,000 characters a run is a few
        # milliseconds and its fixed cost pushed a linear scan to 8.1x on CI.
        growth_bound = 8
        judged_step = (8_000, 32_000)
        hang_bound = 2.0

        def least_of_three(scan) -> float:
            times = []
            for _ in range(3):
                started = time.perf_counter()
                scan()
                times.append(time.perf_counter() - started)
            return min(times)

        for padding_kind, unit in (("spaces", " "), ("low-entropy characters", "low-")):
            for kind in ("inside the quotes", "after the value", "in a JSON string"):
                times = []
                for length in lengths:
                    padding = unit * (length // len(unit))
                    if kind == "after the value":
                        text = f'{FIELD} = "{HIGH_ENTROPY_VALUE}"{padding}\n'
                    else:
                        text = f'{FIELD} = "{padding}{HIGH_ENTROPY_VALUE}"\n'
                    with self.subTest(length=length, padding=padding_kind, kind=kind):
                        if kind == "in a JSON string":
                            # The padded line as a JSON member, masked per decoded string as the JSON masker does.
                            document = {"note": text.rstrip("\n")}
                            elapsed = least_of_three(lambda: module.mask_json_strings(document))
                        else:
                            elapsed = least_of_three(
                                lambda: (module.secret_findings(text), module.mask_secret_matches(text))
                            )
                        # Recorded before any assertion, so the step below is judged even when a run fails the cap.
                        times.append(elapsed)
                        self.assertLess(elapsed, hang_bound, f"{length:,} {padding_kind} {kind} took {elapsed:.3f} s")
                        if kind == "in a JSON string":
                            self.assertEqual(module.mask_json_strings(document), ({"note": mask}, 1))
                        else:
                            secret = text.split(" = ", 1)[1].rstrip()
                            findings = [(f.rule.id, f.secret) for f in module.secret_findings(text)]
                            self.assertEqual(findings, [("generic-token", secret)])
                            self.assertEqual(
                                module.mask_secret_matches(text), (f"{mask}{text[len(text.rstrip()) :]}", 1)
                            )
                shorter, longer = judged_step
                before, after = times[lengths.index(shorter)], times[lengths.index(longer)]
                with self.subTest(step=f"{shorter:,} to {longer:,}", padding=padding_kind, kind=kind):
                    self.assertLess(
                        after / before,
                        growth_bound,
                        f"{padding_kind} {kind}: {before:.4f} s at {shorter:,} to {after:.4f} s at {longer:,}, "
                        f"{after / before:.1f}x per 4x step",
                    )

    def test_a_finding_is_placed_on_its_line_by_the_file_index(self) -> None:
        """A finding's line comes from line_starts, the per-file index of line starts, bisected at the finding's
        offset (or its JSON literal's): the same line the count of line feeds before the offset named, on line 1, on
        the last line, with and without a final line feed, and after a blank line, in text and through the scan."""
        module = self.module
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        lines = [f"first {planted}", "plain", "", f"after a blank line {planted}", "plain", f"last {planted}"]
        for text in ("\n".join(lines) + "\n", "\n".join(lines)):
            with self.subTest(final_line_feed=text.endswith("\n")):
                starts = module.line_starts(text)
                self.assertEqual(starts[0], 0)
                self.assertEqual(starts[1:], [i + 1 for i, char in enumerate(text) if char == "\n"])
                findings = module.secret_findings(text)
                placed = [module.finding_line(starts, finding, None) for finding in findings]
                self.assertEqual(placed, [1, 4, 6])
                self.assertEqual(placed, [text.count("\n", 0, finding.start) + 1 for finding in findings])
                # A finding's offset is 1-based line N wherever it sits on the line: the key, the token or the line feed.
                for offset, line in ((0, 1), (len(lines[0]), 1), (len(lines[0]) + 1, 2), (len(text) - 1, 6)):
                    probe = findings[0]._replace(start=offset)
                    self.assertEqual(module.finding_line(starts, probe, None), line, offset)
        # A finding in a decoded JSON string is placed on its literal's line, from the same index of the document.
        escaped = "\\u0067hp\\u005f" + planted[4:]
        document = "\n".join(
            (
                "{",
                '  "items": [',
                "    {",
                '      "url": "https://x/1",',
                f'      "body": "{escaped}"',
                "    }",
                "  ]",
                "}",
                "",
            )
        )
        starts = module.line_starts(document)
        literals = module.json_strings(document)
        placed = [
            (module.finding_line(starts, finding, literal), document.count("\n", 0, literal.offset) + 1)
            for literal in literals
            for finding in module.secret_findings(literal.text)
        ]
        self.assertEqual(placed, [(5, 5)])
        self.write_text_file("fixtures/planted.md", "\n".join(lines) + "\n")
        self.write_text_file("fixtures/planted.json", document)
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn("4 finding(s)", stderr.getvalue())
        for fingerprint in (
            "planted.md:github-pat:1",
            "planted.md:github-pat:4",
            "planted.md:github-pat:6",
            "planted.json:github-pat:5",
        ):
            self.assertIn(f"possible committed secret fixtures/{fingerprint} ghp_...", stderr.getvalue())

    def test_the_report_of_many_findings_in_one_file_is_linear_in_the_findings(self) -> None:
        """Round 10 verdict on cd56bd93: finding_line counted the line feeds from the start of the text for every
        finding, so a file with N findings cost N scans of its text: a tree scan over 32,000, 64,000 and 128,000
        planted provider tokens took 1.85, 7.23 and 28.71 s (0.96, 1.92 and 3.84 MB), and PR-controlled text could
        stall validation. The line starts are indexed once per file and each finding bisects the index.

        The rule, in the shape of the padded-line test: a file of 8,000 and then 32,000 planted provider tokens, one
        per line, is scanned by the tree scan in this process (secret_findings, the line placement and the allowlist
        of every finding, the least of three runs each); the 8,000-to-32,000 step may grow the time by less than 8x
        (linear is about 4x; the count grew 14.7x on cd56bd93 on this host, 0.513 to 7.524 s, against 0.029 to
        0.120 s on this head) and one loose cap of 2 s on any run still fails a hang. Every finding is reported on
        its own line, the first on line 1 and the last on line N."""
        module = self.module
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        counts = (8_000, 32_000)
        growth_bound = 8
        hang_bound = 2.0
        path = self.write_text_file("fixtures/planted.md", "")

        def least_of_three(scan) -> float:
            times = []
            for _ in range(3):
                started = time.perf_counter()
                scan()
                times.append(time.perf_counter() - started)
            return min(times)

        times = []
        for count in counts:
            text = "".join(f"line {number} holds {planted}\n" for number in range(1, count + 1))
            path.write_text(text)
            report = io.StringIO()

            def scan() -> None:
                report.seek(0)
                report.truncate()
                with contextlib.redirect_stderr(report), self.assertRaises(SystemExit):
                    module.validate_no_obvious_secrets()

            with self.subTest(count=count):
                elapsed = least_of_three(scan)
                # Recorded before any assertion, so the step below is judged even when a run fails the cap.
                times.append(elapsed)
                self.assertLess(elapsed, hang_bound, f"{count:,} findings reported in {elapsed:.3f} s")
                self.assertEqual(len(module.secret_findings(text)), count)
                self.assertIn(f"{count} finding(s)", report.getvalue())
                self.assertIn(f"possible committed secret fixtures/planted.md:github-pat:1 ghp_...", report.getvalue())
                self.assertIn(
                    f"possible committed secret fixtures/planted.md:github-pat:{count} ghp_...", report.getvalue()
                )
                self.assertEqual(report.getvalue().count("possible committed secret "), count)
        shorter, longer = counts
        before, after = times
        with self.subTest(step=f"{shorter:,} to {longer:,}"):
            self.assertLess(
                after / before,
                growth_bound,
                f"{before:.4f} s at {shorter:,} findings to {after:.4f} s at {longer:,}, {after / before:.1f}x per 4x step",
            )

    def test_a_key_spelled_with_a_letter_the_regex_folds_is_reported_and_masked(self) -> None:
        """Round 8 verdict on 1bd17d87: the keyword filter looked for a keyword in the lower-cased text while the
        rules' `(?i)` regexes fold by Unicode simple case folding, and str.lower keeps U+017F LATIN SMALL LETTER LONG
        S, so a `ſecret` key with a quoted 4.32-bit value never reached its rule and passed the tree scan and both CLIs
        in text and in JSON while origin/main reported it. The filter is now a `(?i)` regex over the keywords, so a key
        spelled with a long s, a Kelvin sign (U+212A) or a dotted or dotless i (U+0130, U+0131) is reported under
        its rule and masked whole, in text and in a JSON string, and the ASCII spellings stay reported."""
        module = self.module
        mask = module.SECRET_MASK
        long_s, kelvin, dotted_i, dotless_i = "\u017f", "\u212a", "\u0130", "\u0131"
        spellings = (
            (f"{long_s}ecret", "generic-secret"),
            (f"{long_s}ECRET", "generic-secret"),
            (f"pa{long_s}{long_s}word", "generic-password"),
            (f"to{kelvin}en", "generic-token"),
            (f"api_{kelvin}ey", "generic-api-key"),
            (f"ap{dotted_i}_key", "generic-api-key"),
            (f"ap{dotless_i}-key", "generic-api-key"),
            # The spellings reported before this round stay reported.
            (SECRET_KEY, "generic-secret"),
            (FIELD.upper(), "generic-token"),
            (API_KEY, "generic-api-key"),
        )
        text_path = self.write_text_file("docs/notes.md", "")
        json_path = self.write_text_file("fixtures/evidence.json", "{}\n")
        for key, rule in spellings:
            text = f'{key} = "{HIGH_ENTROPY_VALUE}"\n'
            with self.subTest(key=key):
                findings = [(f.rule.id, f.secret) for f in module.secret_findings(text)]
                self.assertEqual(findings, [(rule, f'"{HIGH_ENTROPY_VALUE}"')])
                self.assertEqual(module.mask_secret_matches(text), (f"{mask}\n", 1))
                text_path.write_text(text)
                json_path.write_text("{}\n")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    module.validate_no_obvious_secrets()
                self.assertIn(f'docs/notes.md:{rule}:1 "Qz7...', stderr.getvalue())
                self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
                text_path.write_text(f"{mask}\n")
                module.validate_no_obvious_secrets()
                # The same line in a JSON string whose literal escapes the letter (`\\u017f`): the decoded string is
                # reported on its literal's line (line 4 of the document) and masked.
                document = json.dumps({"items": [{"note": text.rstrip("\n")}]}, indent=2) + "\n"
                self.assertEqual("\\u" in document, not key.isascii())
                json_path.write_text(document)
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    module.validate_no_obvious_secrets()
                self.assertIn(f'fixtures/evidence.json:{rule}:4 "Qz7...', stderr.getvalue())
                self.assertNotIn(HIGH_ENTROPY_VALUE, stderr.getvalue())
                masked, count = module.mask_json_strings(json.loads(document))
                self.assertEqual((masked, count), ({"items": [{"note": mask}]}, 1))
                json_path.write_text(json.dumps(masked, indent=2) + "\n")
                module.validate_no_obvious_secrets()
        # The threshold still applies to a folded spelling: a word is not a finding under any of them.
        for key, _ in spellings:
            low = f'{key} = "{LOW_ENTROPY_VALUE}"\n'
            with self.subTest(key=key, value="low"):
                self.assertEqual(module.secret_findings(low), [])
                self.assertEqual(module.mask_secret_matches(low), (low, 0))
                text_path.write_text(low)
                module.validate_no_obvious_secrets()

    def test_the_keyword_filter_agrees_with_the_rule_regex_on_every_letter_it_folds(self) -> None:
        """The filter before a rule's regex folds a text as the regex folds it, so it never skips a text the regex
        would match (round 8 verdict on 1bd17d87, where a filter over the lower-cased text skipped the long s). The
        letters Python's `(?i)` folds onto a keyword letter beyond ASCII are enumerated here over the whole code
        space: exactly the four the re module documents, and str.lower and str.casefold each miss some of them. Every
        keyword of every rule spelled with each of them is passed by the filter and reported by the rule; a letter the
        regex does not fold (a Cyrillic es or ka) is passed by neither, so the filter is no wider than the regex."""
        module = self.module
        letters = sorted(
            {c for rule in module.SECRET_RULES for keyword in rule.keywords for c in keyword if c.isalpha()}
        )
        beyond_ascii = "".join(map(chr, range(0x80, sys.maxunicode + 1)))
        folded = re.compile("(?i)[" + "".join(letters) + "]").findall(beyond_ascii)
        self.assertEqual(folded, ["\u0130", "\u0131", "\u017f", "\u212a"])
        self.assertEqual([c.lower() for c in folded], ["i\u0307", "\u0131", "\u017f", "k"])
        self.assertEqual([c.casefold() for c in folded], ["i\u0307", "\u0131", "s", "k"])
        folds = {c: [letter for letter in letters if re.fullmatch(f"(?i){letter}", c)] for c in folded}
        self.assertEqual(folds, {"\u0130": ["i"], "\u0131": ["i"], "\u017f": ["s"], "\u212a": ["k"]})
        body = "A1b2C3d4E5f6G7h8I9j0K1l2M"
        for rule in module.SECRET_RULES:
            for keyword in rule.keywords:
                spellings = [
                    keyword[:index] + char + keyword[index + 1 :]
                    for index, letter in enumerate(keyword)
                    for char, targets in folds.items()
                    if letter in targets
                ]
                for spelling in spellings:
                    text = (
                        f'{spelling} = "{HIGH_ENTROPY_VALUE}"\n' if rule.entropy is not None else f"{spelling}{body}\n"
                    )
                    secret = f'"{HIGH_ENTROPY_VALUE}"' if rule.entropy is not None else f"{spelling}{body}"
                    with self.subTest(rule=rule.id, spelling=spelling):
                        self.assertEqual(
                            [(f.rule.id, f.secret) for f in module.secret_findings(text)], [(rule.id, secret)]
                        )
                        self.assertEqual(module.mask_secret_matches(text), (f"{module.SECRET_MASK}\n", 1))
                        self.assertIsNotNone(rule.keyword_regex.search(text))
                        self.assertIsNotNone(rule.regex.search(text))
        # Letters the regex does not fold: U+0455 CYRILLIC SMALL LETTER DZE for s, U+043A CYRILLIC SMALL LETTER KA for k.
        for text in (
            f'\u0455ecret = "{HIGH_ENTROPY_VALUE}"\n',
            f'to\u043aen = "{HIGH_ENTROPY_VALUE}"\n',
            f"\u0455k-{body}\n",
        ):
            with self.subTest(text=text):
                self.assertEqual(module.secret_findings(text), [])
                for rule in module.SECRET_RULES:
                    self.assertIsNone(rule.keyword_regex.search(text), rule.id)
                    self.assertIsNone(rule.regex.search(text), rule.id)

    def test_masking_repeats_until_the_text_passes_the_scan(self) -> None:
        """Round 4 verdict on 43fe25f3: for a quoted assignment whose value is a word and a provider token, the masker
        removed the token and left a remainder above the generic threshold, so --mask-secrets exited 0 and
        --scan-identifiers exited 1 on its output. The masker now repeats until a pass masks nothing, so its output is
        the scan's fixpoint. Since round 7 the densest window finds the round-4 value beside its token in the first
        pass; the remainder that needs a second pass is two short words a token (or a home path) kept apart."""
        module = self.module
        mask = module.SECRET_MASK
        planted = "ghp_" + "a" * 60
        # One pass sees the provider token alone: every window of the value, mostly `a`, is below the generic
        # threshold; the two words it kept apart make one window above it once the marker is removed.
        apart = f'{FIELD} = "abcdefghi {planted} jklmnopqr"\n'
        self.assertEqual([(f.rule.id, f.secret) for f in module.secret_findings(apart)], [("github-pat", planted)])
        self.assertEqual(module.mask_secret_matches(apart), (f"{mask}\n", 2))
        # A home path inside the value: the `~` written in its place joins the words the same way.
        home = f'{FIELD} = "/home/{"a" * 40}/abcde fghij"\n'
        self.assertEqual(module.secret_findings(home), [])
        self.assertEqual(module.mask_secret_matches(home), (f"{mask}\n", 2))
        # The round-4 value beside its token is found by its own window in the first pass: one mask over the line.
        two_part = f'{FIELD} = "{HIGH_ENTROPY_VALUE} {planted}"\n'
        self.assertEqual(module.mask_secret_matches(two_part), (f"{mask}\n", 1))
        for text in (apart, home, two_part, f'{FIELD} = "prefix {planted}"\n', f"{HIGH_ENTROPY_VALUE} {planted}\n"):
            with self.subTest(text=text):
                masked, _ = module.mask_secret_matches(text)
                self.assertEqual(module.secret_findings(masked), [])
                self.assertIsNone(module.home_path_pattern().search(masked))
        # A pass that finds nothing writes nothing, so a one-pass result and a clean text are unchanged.
        self.assertEqual(
            module.mask_secret_matches(f'{FIELD} = "prefix {planted}"\n'), (f'{FIELD} = "prefix {mask}"\n', 1)
        )
        self.assertEqual(module.mask_secret_matches("prose\nVerdict: correct\n"), ("prose\nVerdict: correct\n", 0))

    def test_a_path_ending_in_a_newline_matches_no_allowlist_row(self) -> None:
        """A path regex anchored with `$` also matches before a trailing newline, so a file named `validate.py` plus
        a newline under the CompactionDB row's directory was suppressed like the real one (round 4 live run on
        43fe25f3). Every path row ends in `\\Z`, and a `$`-anchored path row is refused when the table loads."""
        module = self.module
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        allowed = "vendor/compactiondb/validate.py"
        self.write_text_file(allowed, f"{planted}\n")
        module.validate_no_obvious_secrets()
        self.write_text_file(allowed + "\n", f"{planted}\n")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            module.validate_no_obvious_secrets()
        self.assertIn("1 finding(s)", stderr.getvalue())
        self.assertIn(f"possible committed secret {allowed}\n:github-pat:1 ghp_...", stderr.getvalue())
        self.assertIsNotNone(module.secret_allowance("github-pat", planted, allowed, f"{allowed}:github-pat:1"))
        self.assertIsNone(module.secret_allowance("github-pat", planted, allowed + "\n", f"{allowed}\n:github-pat:1"))

        for row in module.SECRET_ALLOWLIST:
            if row.path_regex is not None:
                self.assertIsNone(module.UNESCAPED_DOLLAR.search(row.path_regex.pattern), row.reason)
        row = module.SecretAllowance
        with self.assertRaisesRegex(ValueError, r"anchors its path regex with `\$`; use `\\Z`"):
            module.checked_allowlist((row("*", "a row ending in $", path_regex=re.compile(r"^fixtures/a\.md$")),))
        with self.assertRaisesRegex(ValueError, r"anchors its path regex with `\$`"):
            module.checked_allowlist((row("*", "a $ in the middle", path_regex=re.compile(r"^fixtures/(a$|b\Z)")),))
        # An escaped `$` is a character of the path, not an anchor.
        module.checked_allowlist((row("*", "a literal dollar", path_regex=re.compile(r"^fixtures/\$a\.md\Z")),))

    def test_a_nul_orchestration_file_and_a_later_token_are_both_reported_in_one_run(self) -> None:
        """Round 3 verdict on ce36a3a5: read_scannable_text() exited at the first NUL orchestration file, dropping the
        findings collected before it and skipping every file after it. A NUL or UTF-16 evidence file is now one
        finding of the scan, reported in the one failure with every token elsewhere in the tree."""
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        self.write_text_file("docs/a.md", f"{planted}\n")
        nul = self.temp_dir / ".orchestration/validation/t-a01.md"
        nul.parent.mkdir(parents=True)
        nul.write_bytes(b"heading\x00" + planted.encode())
        (nul.parent / "t-utf16.md").write_bytes("\u3042\u3044".encode("utf-16"))
        self.write_text_file(".orchestration/validation/t-z99.md", f"{planted}\n")
        self.write_text_file("scripts/z.sh", f"\n{planted}\n")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            self.module.validate_no_obvious_secrets()

        self.assertEqual(raised.exception.code, 1)
        report = stderr.getvalue()
        self.assertIn("5 finding(s) in the committed-secret scan", report)
        for line in (
            "  .orchestration/validation/t-a01.md holds a NUL byte at offset 7; evidence must be UTF-8 text",
            "  .orchestration/validation/t-utf16.md is UTF-16; evidence must be UTF-8 text",
            "  possible committed secret .orchestration/validation/t-z99.md:github-pat:1 ghp_...",
            "  possible committed secret docs/a.md:github-pat:1 ghp_...",
            "  possible committed secret scripts/z.sh:github-pat:2 ghp_...",
        ):
            self.assertIn(line, report)
        self.assertNotIn(planted[4:], report, "the report shows a secret's first four characters only")

    def test_an_allowlist_row_suppresses_by_path_or_by_one_fingerprint(self) -> None:
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        self.write_text_file("fixtures/planted.md", f"{planted}\n\n{planted}\n")
        row = self.module.SecretAllowance
        by_path = row("github-pat", "fixture", path_regex=re.compile(r"^fixtures/"))
        with mock.patch.object(self.module, "SECRET_ALLOWLIST", (by_path,)):
            self.module.validate_no_obvious_secrets()

        other_rule = row("openai-api-key", "another rule's fixture", path_regex=re.compile(r"^fixtures/"))
        with mock.patch.object(self.module, "SECRET_ALLOWLIST", (other_rule,)):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                self.module.validate_no_obvious_secrets()

        line_one = row("*", "the first line only", fingerprint="fixtures/planted.md:github-pat:1")
        with mock.patch.object(self.module, "SECRET_ALLOWLIST", (line_one,)):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                self.module.validate_no_obvious_secrets()
        self.assertIn("1 finding(s)", stderr.getvalue())
        self.assertIn("fixtures/planted.md:github-pat:3 ", stderr.getvalue())
        self.assertNotIn("fixtures/planted.md:github-pat:1 ", stderr.getvalue())

        with self.assertRaises(ValueError):
            self.module.checked_allowlist((row("*", "a row with no condition"),))

    def test_identical_json_secrets_on_two_lines_get_two_fingerprints_and_a_row_suppresses_one(self) -> None:
        """Each finding in a JSON document is placed on the line of its own string literal, so two copies of one
        secret get two fingerprints and a fingerprint row names one of them (Codex P2 on PR #582)."""
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        text = json.dumps({"items": [{"body": planted, "url": "https://x/1"}, {"body": planted}]}, indent=2)
        self.write_text_file("fixtures/planted.json", text + "\n")
        lines = [number for number, line in enumerate(text.splitlines(), 1) if planted in line]
        self.assertEqual(len(lines), 2)
        first, second = (f"fixtures/planted.json:github-pat:{number}" for number in lines)

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn("2 finding(s)", stderr.getvalue())
        self.assertIn(f"possible committed secret {first} ghp_...", stderr.getvalue())
        self.assertIn(f"possible committed secret {second} ghp_...", stderr.getvalue())

        line_one = self.module.SecretAllowance("*", "the first copy only", fingerprint=first)
        with mock.patch.object(self.module, "SECRET_ALLOWLIST", (line_one,)):
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                self.module.validate_no_obvious_secrets()
        self.assertIn("1 finding(s)", stderr.getvalue())
        self.assertIn(f"{second} ", stderr.getvalue())
        self.assertNotIn(f"{first} ", stderr.getvalue())

    def test_an_escaped_json_secret_is_placed_on_the_line_of_its_literal(self) -> None:
        """A writer's escaping (`\\u0067hp_`, `\\u005f`) hides the raw token from the text; the finding is still
        placed on its literal's line, never on line 0, and the whole token is the secret the rule reports."""
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        escaped = "\\u0067hp\\u005f" + planted[4:]
        self.assertEqual(json.loads(f'"{escaped}"'), planted)
        # The escaped literal sits on line 5 of the document.
        lines = ["{", '  "items": [', "    {", '      "url": "https://x/1",', f'      "body": "see {escaped}"', "    }"]
        text = "\n".join((*lines, "  ]", "}", ""))
        self.assertNotIn(planted, text)
        path = self.write_text_file("fixtures/escaped.json", text)

        literals = self.module.json_strings(text)
        expected = ["items", "url", "https://x/1", "body", f"see {planted}"]
        self.assertEqual([literal.text for literal in literals], expected)
        self.assertTrue(all(text[literal.offset] == '"' for literal in literals))

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
            self.module.validate_no_obvious_secrets()
        self.assertIn("1 finding(s)", stderr.getvalue())
        self.assertIn("possible committed secret fixtures/escaped.json:github-pat:5 ghp_...", stderr.getvalue())
        self.assertNotIn(":github-pat:0 ", stderr.getvalue())

        row = self.module.SecretAllowance("github-pat", "fixture", fingerprint="fixtures/escaped.json:github-pat:5")
        with mock.patch.object(self.module, "SECRET_ALLOWLIST", (row,)):
            self.module.validate_no_obvious_secrets()
        path.unlink()

    def test_json_strings_refuses_when_the_literals_do_not_match_the_parsed_document(self) -> None:
        """The literals found in the text are compared with the parsed document's strings; a difference is refused
        rather than placing a finding on another literal's line, and the tree scan reports the file."""
        text = json.dumps({"a": "one", "b": ["two", "three"]}, indent=2) + "\n"
        literals = self.module.json_strings(text)
        self.assertEqual([literal.text for literal in literals], ["a", "one", "b", "two", "three"])
        self.assertEqual([text[literal.offset] for literal in literals], ['"'] * 5)
        self.assertIsNone(self.module.json_strings("not json\n"))
        self.assertEqual(self.module.json_strings("42\n"), [])

        self.write_text_file("fixtures/mismatch.json", text)
        with mock.patch.object(self.module, "decoded_json_strings", return_value=["a", "one", "b", "two"]):
            with self.assertRaises(self.module.JsonStringMismatch):
                self.module.json_strings(text)
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                self.module.validate_no_obvious_secrets()
        self.assertIn("1 finding(s)", stderr.getvalue())
        self.assertIn(
            "fixtures/mismatch.json cannot be scanned per JSON string: 5 JSON string literal(s) in the text do not "
            "match the 4 string(s) of the parsed document",
            stderr.getvalue(),
        )
        for value in ("one", "two", "three"):
            self.assertNotIn(f'"{value}"', stderr.getvalue(), "the refusal quotes no string")

    def test_a_provider_token_in_a_unit_test_file_is_reported(self) -> None:
        """No SECRET_ALLOWLIST row names a test file: the planted fixtures are split literals, and a real token pasted
        into either file is a finding like anywhere else. Each file's committed text is scanned as a scratch copy."""
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        for row in self.module.SECRET_ALLOWLIST:
            if row.path_regex is not None:
                self.assertIsNone(row.path_regex.search("tests/unit/test_validate_agent_assets.py"), row.reason)
                self.assertIsNone(row.path_regex.search("tests/unit/test_pr_levers.py"), row.reason)
        for name in ("test_validate_agent_assets.py", "test_pr_levers.py"):
            with self.subTest(file=name):
                source = (ROOT / "tests/unit" / name).read_text()
                copy = self.write_text_file(f"tests/unit/{name}", source)
                self.module.validate_no_obvious_secrets()  # the committed text is clean on its own

                copy.write_text(f"{source}\n{planted}\n")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    self.module.validate_no_obvious_secrets()
                self.assertIn("1 finding(s)", stderr.getvalue())
                self.assertIn(f"tests/unit/{name}:github-pat:{source.count(chr(10)) + 2} ghp_...", stderr.getvalue())
                copy.unlink()

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
            ("escaped quoted assignment", json.dumps({"body": f'{FIELD} = "{HIGH_ENTROPY_VALUE}"'})),
            ("not JSON, text scan", across_fields[:-1] + f'\n{FIELD} = "{HIGH_ENTROPY_VALUE}"'),
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
        path.write_bytes(f'{FIELD} = "{HIGH_ENTROPY_VALUE}"\n'.encode("utf-16"))

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


class SecretRuleBoundaryTest(unittest.TestCase):
    """Key prefixes match only at a word boundary, so hyphenated slugs stay clean."""

    def setUp(self) -> None:
        self.module = load_validator()

    def found(self, text: str) -> bool:
        return bool(self.module.secret_findings(text))

    def test_a_key_prefix_inside_a_hyphenated_word_is_clean(self) -> None:
        for text in (
            "dotfiles-T67-audit-task-level-a01-review-receipt.md",
            "the dotfiles-T75-shell-dead-code-a01 report",
        ):
            with self.subTest(text=text):
                self.assertFalse(self.found(text))

    def test_a_real_key_prefix_is_still_flagged(self) -> None:
        openai, github = "s" + "k-" + "a1" * 12, "gh" + "p_" + "a1" * 12
        for text in (f"x {openai}", f'"{openai}"', openai, f"KEY={openai}", f"x {github}"):
            with self.subTest(text=text):
                self.assertTrue(self.found(text))

    def test_a_key_after_json_escaped_whitespace_is_flagged(self) -> None:
        # Audit evidence holds JSON-encoded transcripts: the character before the
        # key is then the n/r/t of an escape sequence, a word character.
        keys = ("s" + "k-" + "a1" * 12, "gh" + "p_" + "a1" * 12, "github" + "_pat_" + "a1" * 12)
        for key in keys:
            for text in (json.dumps({"m": "\n" + key}), json.dumps({"m": "\t" + key}), json.dumps({"m": "\r" + key})):
                with self.subTest(text=text):
                    self.assertTrue(self.found(text))
            # Any escape sequence (a backslash, then up to nine letters or digits)
            # right before the key: JSON \uXXXX, \b, \f, TOML \UXXXXXXXX, YAML \x, \0.
            escapes = ("\\u000a", "\\u000d", "\\u0009", "\\u0020", "\\b", "\\f", "\\U0000000A", "\\x0a", "\\0")
            for escape in escapes:
                text = '{"m": "' + escape + key + '"}'
                with self.subTest(text=text):
                    self.assertTrue(self.found(text))

    def test_an_sk_key_body_needs_a_hyphen_free_run(self) -> None:
        bare, project = "s" + "k-" + "a1" * 12, "s" + "k-" + "proj-" + "a1" * 12
        for text in (f"x {bare}", f"x {project}", json.dumps({"m": "\n" + project})):
            with self.subTest(text=text):
                self.assertTrue(self.found(text))
        slug = "dotfiles-T91-secret-scan-" + "s" + "k-boundary-a01"
        for text in (f"{slug}-audit-1845139e.md", f"{slug}-pr-feedback.json", f"{slug}-review-receipt.md"):
            with self.subTest(text=text):
                self.assertFalse(self.found(text))

    def test_a_long_hyphenated_run_scans_in_linear_time(self) -> None:
        text = "-s" + "k-a" * 1 + ("-s" + "k-a") * (64 * 1024 // 5)
        started = time.monotonic()
        self.assertFalse(self.found(text))
        self.assertLess(time.monotonic() - started, 1.0)

    def test_masking_keeps_the_escape_before_the_key(self) -> None:
        module = self.module
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
    """`--mask-secrets` rewrites the committed-secret scan's findings in place (audit evidence)."""

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
            f'schema:\n  design_{FIELD}: "{HIGH_ENTROPY_VALUE}"\n  applies_{FIELD}: "{HIGH_ENTROPY_VALUE}"\n'
            "prose line stays\nVerdict: correct\n"
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
        self.assertEqual(module.secret_findings(text), [])

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
                strings = [literal.text for literal in module.json_strings(text) or ()] or [text]
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
            {"body": f'line\n{key}\nset {FIELD} = "{HIGH_ENTROPY_VALUE}"', "url": "https://x/2"},
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
        literals = module.json_strings(evidence.read_text())
        self.assertFalse(any(module.secret_findings(literal.text) for literal in literals))

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


class MaskerProviderRuleParityTest(unittest.TestCase):
    """For every provider-rule match, the masker writes the bytes origin/main's masker wrote (U107)."""

    def setUp(self) -> None:
        before = subprocess.run(
            ["git", "-C", str(ROOT), "show", "origin/main:scripts/validate-agent-assets.py"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(before.returncode, 0, before.stderr)
        temp_dir = Path(tempfile.mkdtemp(prefix="masker-before-"))
        self.addCleanup(shutil.rmtree, temp_dir)
        path = temp_dir / "validate-agent-assets.py"
        path.write_text(before.stdout)
        spec = importlib.util.spec_from_file_location("validate_agent_assets_before", path)
        assert spec and spec.loader
        self.before = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.before)
        # Both maskers read the repository's home/ entry names from ROOT for the home-path pass.
        self.before.ROOT = ROOT
        self.after = load_validator()

    def test_every_provider_match_masks_to_the_same_bytes(self) -> None:
        github = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        fine_grained = "github_" + "pat_" + "11AAAAAAA0bcdefghijklmnopqrstuvwxyz"
        openai, project = "s" + "k-" + "a1" * 12, "s" + "k-" + "proj-" + "a1" * 12
        samples = (
            f"{FIELD} {github}\n",
            f'"{github}"',
            github,
            github.upper(),
            f"KEY={openai}",
            f"{github} and {openai} on one line\n",
            f"{github}\n{fine_grained}\n{project}\n",
            f"{github}{openai}",
            json.dumps({"m": "\n" + github}),
            json.dumps({"m": "\t" + fine_grained}),
            '{"m": "\\u000a' + openai + '"}',
            '{"m": "\\U0000000A' + project + '"}',
            f"see /home/alice/x and {github}\n",
            f"dotfiles-T91-secret-scan-s" + f"k-boundary-a01-review-receipt.md {github}",
            "progress 10%\rprogress 100%\r\n" + github + "\r\n",
        )
        for text in samples:
            with self.subTest(text=text):
                masked, count = self.after.mask_secret_matches(text)
                self.assertGreaterEqual(count, 1)
                self.assertEqual((masked, count), self.before.mask_secret_matches(text))


class ScanIdentifiersModeTest(unittest.TestCase):
    """`--scan-identifiers` refuses a secret, a home path or a redact word, and never quotes what it found (U101)."""

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="scan-identifiers-test-"))
        self.addCleanup(shutil.rmtree, self.temp_dir)
        self.words = self.temp_dir / "redact-words.txt"
        self.words.write_text("# host and user names\nmbp-kana\n\nOperator1\n")

    def scan(self, *paths: Path, words: bool = True) -> "subprocess.CompletedProcess[str]":
        args = ["--redact-words", str(self.words)] if words else []
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--scan-identifiers", *args, "--", *map(str, paths)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_each_kind_is_a_finding_and_a_clean_file_passes(self) -> None:
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        # The words sit on physical lines 2 and 4 of the file (a comment and a blank line around them).
        cases = (
            ("a secret pattern", f"token {planted}\n"),
            ("a home directory path", "ran in /Users/someone/x\n"),
            ("redact word on line 2", "seen on MBP-KANA\n"),
            ("redact word on line 4", '{"host": "operator1"}\n'),
            # U101 audit P2: a KELVIN SIGN (U+212A) is no ASCII letter, so it bounds the word; inside the word it
            # folds to k, as the word's case-insensitive match allows.
            ("redact word on line 4", "\u212aoperator1-test\n"),
            ("redact word on line 2", "mbp-\u212aana\n"),
        )
        for finding, text in cases:
            with self.subTest(finding=finding, text=text):
                path = self.temp_dir / "evidence.md"
                path.write_text(text)
                result = self.scan(path)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({path}): {finding}\n")
                self.assertNotIn(planted, result.stderr)
        clean = self.temp_dir / "clean.md"
        clean.write_text("mbp-kanax and xoperator1 are other words; ~/x is masked\n")
        result = self.scan(clean)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

    def test_a_redact_word_in_the_path_is_a_finding_that_never_prints_the_path(self) -> None:
        # U101 audit P2: the finding printed the raw path, and so the word in it; the file is now named by its place.
        clean = self.temp_dir / "clean.md"
        clean.write_text("clean\n")
        path = self.temp_dir / "notes-operator1.md"
        path.write_text("clean\n")
        result = self.scan(clean, path)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "--scan-identifiers: file 2: redact word on line 4 in the path\n")
        self.assertNotIn("operator1", (result.stdout + result.stderr).lower())
        self.assertEqual(self.scan(path, words=False).returncode, 0)

    def test_every_content_test_also_applies_to_the_path(self) -> None:
        # U101 round 5: the secret and home-path tests read the content only, so a clean file named after a token
        # published it. Each kind is a finding of the path; no output line names the path or what was found.
        planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
        cases = (
            ("a secret pattern", Path(f"{planted}.md")),
            ("a home directory path", Path("store/home/runner/notes.md")),  # the same glued forms as content
            ("redact word on line 2", Path("MBP-Kana/notes.md")),
        )
        for reason, relative in cases:
            with self.subTest(reason):
                path = self.temp_dir / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("clean\n")
                result = subprocess.run(
                    [sys.executable, str(VALIDATOR), "--scan-identifiers", "--redact-words", str(self.words), "--"]
                    + [str(relative)],
                    cwd=self.temp_dir,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(result.stderr, f"--scan-identifiers: file 1: {reason} in the path\n")
                for found in (planted.lower(), "runner", "kana"):
                    self.assertNotIn(found, (result.stdout + result.stderr).lower())

    def test_usage_and_unreadable_files_exit_2(self) -> None:
        present = self.temp_dir / "present.md"
        present.write_text("clean\n")
        self.assertEqual(self.scan(self.temp_dir / "missing.md").returncode, 2)
        self.assertEqual(self.scan().returncode, 2)
        self.words.unlink()
        self.assertEqual(self.scan(present).returncode, 2)

    def test_masked_evidence_passes_and_a_value_beside_the_marker_is_refused(self) -> None:
        """Round 3 verdict on ce36a3a5: the masker's output for a quoted assignment holding a provider token crossed
        the generic entropy threshold, so records-sync.sh refused cleaned evidence. The masked file exits 0; a real
        value beside the marker still exits 1."""
        module = load_validator()
        evidence = self.temp_dir / "audit.md"
        planted = "ghp_" + "a" * 25
        evidence.write_text(f'{FIELD} = "prefix {planted}"\nVerdict: correct\n')
        masked = subprocess.run(
            [sys.executable, str(VALIDATOR), "--mask-secrets", str(evidence)], text=True, capture_output=True
        )
        self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
        self.assertEqual(evidence.read_text(), f'{FIELD} = "prefix {module.SECRET_MASK}"\nVerdict: correct\n')

        result = self.scan(evidence)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

        evidence.write_text(f'{FIELD} = "{module.SECRET_MASK} {HIGH_ENTROPY_VALUE}"\n')
        result = self.scan(evidence)
        self.assertEqual(result.returncode, 1)
        self.assertIn(f"file 1 ({evidence}): a secret pattern", result.stderr)

    def test_a_token_inside_a_longer_quoted_value_masks_to_text_the_scan_accepts(self) -> None:
        """Round 4 verdict on 43fe25f3, through the two CLIs records-sync.sh runs: masking only the provider token
        out of a quoted assignment whose value is a word and the token left a value above the generic threshold, so
        --mask-secrets exited 0 and --scan-identifiers exited 1 on its output. The masker now repeats until its
        output passes the scan: two words a token kept apart need the second pass, and the round-4 value beside its
        token is found by its own window in the first pass (round 7)."""
        module = load_validator()
        planted = "ghp_" + "a" * 60
        for value, masks in ((f"abcdefghi {planted} jklmnopqr", 2), (f"{HIGH_ENTROPY_VALUE} {planted}", 1)):
            with self.subTest(value=value):
                evidence = self.temp_dir / "audit.md"
                evidence.write_text(f'{FIELD} = "{value}"\nVerdict: correct\n')
                masked = subprocess.run(
                    [sys.executable, str(VALIDATOR), "--mask-secrets", str(evidence)], text=True, capture_output=True
                )
                self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
                self.assertEqual(masked.stdout, f"masked {masks} match(es) in {evidence}\n")
                self.assertEqual(evidence.read_text(), f"{module.SECRET_MASK}\nVerdict: correct\n")

                result = self.scan(evidence)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
                self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

    def test_a_quoted_value_with_an_apostrophe_is_refused_whole(self) -> None:
        """Round 4 verdict on 43fe25f3: a double-quoted value with an apostrophe after its first character was
        measured as that character, so the scan accepted it."""
        evidence = self.temp_dir / "audit.md"
        evidence.write_text(f'{PASSWORD_KEY} = "x\'{HIGH_ENTROPY_VALUE}"\n')
        result = self.scan(evidence)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({evidence}): a secret pattern\n")
        self.assertNotIn(HIGH_ENTROPY_VALUE, result.stdout + result.stderr)

    def test_a_quoted_value_with_an_escaped_quote_is_refused_and_masked_whole(self) -> None:
        """Round 5 verdict on a7b060cd, through the two CLIs records-sync.sh runs: a double-quoted value with an
        escaped quote after its first character exited 0 from --scan-identifiers, and --mask-secrets left it as it
        was. The value is refused, and the masker writes one marker over the whole line."""
        module = load_validator()
        evidence = self.temp_dir / "audit.md"
        evidence.write_text(f'{PASSWORD_KEY} = "x\\"{HIGH_ENTROPY_VALUE}"\nVerdict: correct\n')
        result = self.scan(evidence)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({evidence}): a secret pattern\n")
        self.assertNotIn(HIGH_ENTROPY_VALUE, result.stdout + result.stderr)

        masked = subprocess.run(
            [sys.executable, str(VALIDATOR), "--mask-secrets", str(evidence)], text=True, capture_output=True
        )
        self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
        self.assertEqual(masked.stdout, f"masked 1 match(es) in {evidence}\n")
        self.assertEqual(evidence.read_text(), f"{module.SECRET_MASK}\nVerdict: correct\n")
        result = self.scan(evidence)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

    def test_a_secret_beside_padding_on_its_line_is_refused_and_masked_whole(self) -> None:
        """Round 7 finding on 38a83e45, through the two CLIs records-sync.sh runs: a line holding two assignments,
        160 characters of padding and then a 4.32-bit value, exited 0 from --scan-identifiers and --mask-secrets left
        it as it was. The line is refused, the masker writes one marker over all of it, and the padding alone still
        passes."""
        module = load_validator()
        evidence = self.temp_dir / "audit.md"
        padded = f'{FIELD} = "{LOW_ENTROPY_PADDING}" {FIELD} = "{HIGH_ENTROPY_VALUE}"'
        evidence.write_text(f"{padded}\nVerdict: correct\n")
        result = self.scan(evidence)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({evidence}): a secret pattern\n")
        self.assertNotIn(HIGH_ENTROPY_VALUE, result.stdout + result.stderr)

        masked = subprocess.run(
            [sys.executable, str(VALIDATOR), "--mask-secrets", str(evidence)], text=True, capture_output=True
        )
        self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
        self.assertEqual(masked.stdout, f"masked 1 match(es) in {evidence}\n")
        self.assertEqual(evidence.read_text(), f"{module.SECRET_MASK}\nVerdict: correct\n")
        result = self.scan(evidence)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

        evidence.write_text(f'{FIELD} = "{LOW_ENTROPY_PADDING}"\nVerdict: correct\n')
        result = self.scan(evidence)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

    def test_a_line_with_a_carriage_return_before_text_is_refused_and_masked_up_to_it(self) -> None:
        """Round 7 verdict on 1632d807, through the two CLIs records-sync.sh runs: a quoted 4.32-bit value followed on
        its line by a bare CR and text exited 0 from --scan-identifiers and --mask-secrets reported zero masks and
        kept it, in text and in a JSON string. The line is refused and the masker writes one marker over the value up
        to the CR (U107b: the CR ends the field, the text after it stays); the CRLF evidence the masker already
        handles keeps its line endings."""
        module = load_validator()
        tail = "\rprogress complete"
        line = f'{FIELD} = "{HIGH_ENTROPY_VALUE}"{tail}'
        evidence = self.temp_dir / "audit.md"
        evidence.write_bytes(f"{line}\nVerdict: correct\n".encode())
        member = self.temp_dir / "member.json"
        member.write_bytes((json.dumps({"items": [{"note": line}]}, indent=2) + "\n").encode())
        self.assertIn(b"\\r", member.read_bytes())
        for path, masked_text in (
            (evidence, f"{module.SECRET_MASK}{tail}\nVerdict: correct\n"),
            (member, json.dumps({"items": [{"note": f"{module.SECRET_MASK}{tail}"}]}, indent=2) + "\n"),
        ):
            with self.subTest(path=path.name):
                result = self.scan(path)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({path}): a secret pattern\n")
                self.assertNotIn(HIGH_ENTROPY_VALUE, result.stdout + result.stderr)

                masked = subprocess.run(
                    [sys.executable, str(VALIDATOR), "--mask-secrets", str(path)], text=True, capture_output=True
                )
                self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
                self.assertEqual(masked.stdout, f"masked 1 match(es) in {path}\n")
                self.assertEqual(path.read_bytes().decode(), masked_text)
                result = self.scan(path)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
                self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

        crlf = self.temp_dir / "crlf.md"
        crlf.write_bytes(f'{FIELD} = "{HIGH_ENTROPY_VALUE}"\r\nVerdict: correct\r\n'.encode())
        self.assertEqual(self.scan(crlf).returncode, 1)
        masked = subprocess.run(
            [sys.executable, str(VALIDATOR), "--mask-secrets", str(crlf)], text=True, capture_output=True
        )
        self.assertEqual(masked.stdout, f"masked 1 match(es) in {crlf}\n")
        self.assertEqual(crlf.read_bytes(), f"{module.SECRET_MASK}\r\nVerdict: correct\r\n".encode())
        self.assertEqual(self.scan(crlf).returncode, 0)

    def test_a_key_spelled_with_a_long_s_or_a_kelvin_sign_is_refused_and_masked(self) -> None:
        """Round 8 verdict on 1bd17d87, through the two CLIs records-sync.sh runs: a `ſecret` key (U+017F) with a quoted
        4.32-bit value exited 0 from --scan-identifiers and --mask-secrets masked nothing, in text and in a JSON string
        whose literal holds `\\u017f`, because the keyword filter lower-cased the text and str.lower keeps the long s.
        Each spelling the rule regex folds is refused and masked whole; the Kelvin sign (U+212A), which str.lower did
        fold, stays so."""
        module = load_validator()
        long_s, kelvin = "\u017f", "\u212a"
        evidence = self.temp_dir / "audit.md"
        evidence.write_bytes(f'{long_s}ecret = "{HIGH_ENTROPY_VALUE}"\nVerdict: correct\n'.encode())
        member = self.temp_dir / "member.json"
        line = f'pa{long_s}{long_s}word = "{HIGH_ENTROPY_VALUE}"'
        member.write_bytes((json.dumps({"items": [{"note": line}]}, indent=2) + "\n").encode())
        self.assertIn(b"\\u017f", member.read_bytes())
        kelvin_file = self.temp_dir / "kelvin.md"
        kelvin_file.write_bytes(f'to{kelvin}en: "{HIGH_ENTROPY_VALUE}"\nVerdict: correct\n'.encode())
        for path, masked_text in (
            (evidence, f"{module.SECRET_MASK}\nVerdict: correct\n"),
            (member, json.dumps({"items": [{"note": module.SECRET_MASK}]}, indent=2) + "\n"),
            (kelvin_file, f"{module.SECRET_MASK}\nVerdict: correct\n"),
        ):
            with self.subTest(path=path.name):
                result = self.scan(path)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({path}): a secret pattern\n")
                self.assertNotIn(HIGH_ENTROPY_VALUE, result.stdout + result.stderr)

                masked = subprocess.run(
                    [sys.executable, str(VALIDATOR), "--mask-secrets", str(path)], text=True, capture_output=True
                )
                self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
                self.assertEqual(masked.stdout, f"masked 1 match(es) in {path}\n")
                self.assertEqual(path.read_bytes().decode(), masked_text)
                result = self.scan(path)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
                self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

    def test_a_masked_value_in_a_tsv_column_stays_inside_its_field(self) -> None:
        """U107b (2026-10-31), through the two CLIs records-sync.sh runs on the store's copies: the generic capture
        ran to the line feed, so the ledger row whose evidence column quotes the round-5 finding was masked from its
        key through two tabs to the end of the row, the masked copy had 5 columns instead of 7 and rounds-check.py
        refused it. A tab ends the capture: the row keeps its 7 columns, the marker sits inside the fifth, the masked
        copy passes the scan, and a value followed by a tab is masked up to the tab, with an escaped quote or an
        apostrophe inside it (the rounds 4 and 5 cases) as without."""
        module = load_validator()
        mask = module.SECRET_MASK
        prefix = (
            "incorrect (round 5, findings=1 P2: validate-agent-assets.py:103 the quoted-value capture stops at an "
            "escaped quote, so "
        )
        quoted = f'{PASSWORD_KEY} = "x\\"Qz7vTq9mLw2Kp\\"..." is measured as x\\ and passes scanning and masking; reproduced)'
        columns = [
            "2026-10-28T14:06:18Z",
            "U107",
            "582",
            "a7b060cdfb61692cf382305da2af775bd550fec1",
            prefix + quoted,
            "pr-audit.sh (U71b lever) run by the coordinator",
            "verdicts/U107-a7b060cd.md",
        ]
        ledger = self.temp_dir / "ledger.tsv"
        ledger.write_text("\t".join(columns) + "\n")
        result = self.scan(ledger)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(result.stderr, f"--scan-identifiers: file 1 ({ledger}): a secret pattern\n")
        masked = subprocess.run(
            [sys.executable, str(VALIDATOR), "--mask-secrets", str(ledger)], text=True, capture_output=True
        )
        self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
        self.assertEqual(masked.stdout, f"masked 1 match(es) in {ledger}\n")
        row = ledger.read_text()
        masked_columns = row.rstrip("\n").split("\t")
        self.assertEqual(len(masked_columns), 7, f"{len(masked_columns)} columns after masking: {row!r}")
        self.assertEqual(masked_columns, columns[:4] + [prefix + mask] + columns[5:])
        result = self.scan(ledger)
        self.assertEqual((result.returncode, result.stderr), (0, ""))
        self.assertEqual(result.stdout, "scanned 1 file(s): 0 finding(s), 2 redact word(s)\n")

        for value in (f'x\\"{HIGH_ENTROPY_VALUE}', f"x'{HIGH_ENTROPY_VALUE}", HIGH_ENTROPY_VALUE):
            with self.subTest(value=value):
                text = f'{PASSWORD_KEY} = "{value}"\tVerdict: correct\n'
                self.assertEqual(
                    [(f.rule.id, f.secret) for f in module.secret_findings(text)], [("generic-password", f'"{value}"')]
                )
                self.assertEqual(module.mask_secret_matches(text), (f"{mask}\tVerdict: correct\n", 1))
                evidence = self.temp_dir / "audit.md"
                evidence.write_text(text)
                result = self.scan(evidence)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertNotIn(HIGH_ENTROPY_VALUE, result.stdout + result.stderr)
                masked = subprocess.run(
                    [sys.executable, str(VALIDATOR), "--mask-secrets", str(evidence)], text=True, capture_output=True
                )
                self.assertEqual(masked.stdout, f"masked 1 match(es) in {evidence}\n")
                self.assertEqual(evidence.read_text(), f"{mask}\tVerdict: correct\n")
                self.assertEqual(self.scan(evidence).returncode, 0)


if __name__ == "__main__":
    unittest.main()
