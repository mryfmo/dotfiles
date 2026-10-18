"""Permission-surface decisions are bound to a canonical diff, without executing revision code."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

GUARD = Path(__file__).resolve().parents[2] / "scripts/permission-guard.py"


class PermissionGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(
            os.environ,
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
            GIT_AUTHOR_NAME="fixture",
            GIT_AUTHOR_EMAIL="fixture@example.test",
            GIT_COMMITTER_NAME="fixture",
            GIT_COMMITTER_EMAIL="fixture@example.test",
        )
        self.manifest = {
            "claude": {
                "permissions": {"ask": [], "allow": [], "defaultMode": "auto"},
                "sandbox": {"enabled": True},
                "hooks": {},
            },
            "codex": {"approval_policy": "on-request", "sandbox_workspace_write": {"network_access": False}},
        }
        self.write("home/dot_agents/agent-config.yaml", json.dumps(self.manifest))
        self.write("home/.chezmoitemplates/claude-settings-managed.json", '{"permissions":{},"sandbox":{},"hooks":{}}')
        self.write(
            "home/.chezmoitemplates/codex-config-managed.toml",
            'approval_policy="on-request"\n[sandbox_workspace_write]\nnetwork_access=false\n',
        )
        self.git("init", "-q")
        self.base = self.commit()

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=self.root, env=self.env, text=True).strip()

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self) -> str:
        self.git("add", ".")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def run_guard(self, *extra: str) -> subprocess.CompletedProcess[str]:
        command = ["uv", "run", "--no-project", "--with", "pyyaml", "python", "-I", str(GUARD)]
        return subprocess.run(
            command + ["--base", self.base, "--head", "HEAD", *extra],
            cwd=self.root,
            env=self.env,
            text=True,
            capture_output=True,
        )

    def change_permission(self) -> None:
        self.manifest["claude"]["permissions"]["allow"] = ["Bash(gh pr merge:*)"]
        self.write("home/dot_agents/agent-config.yaml", json.dumps(self.manifest))
        self.commit()

    def test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes(self) -> None:
        self.change_permission()
        red = self.run_guard()
        self.assertEqual(1, red.returncode, red.stderr)
        digest = re.search(r"permission diff sha256: ([0-9a-f]{64})", red.stdout)[1]
        self.assertIn("claude.permissions.allow", red.stdout)
        for tags in (
            f"scope=permission approved_by=user-other diff_sha256={digest}",
            f"scope=permission approved_by=user diff_sha256={digest}0",
        ):
            self.write(".orchestration/decisions.tsv", "id\twhat\tbasis\nD-test\t\t" + tags + "\n")
            self.assertEqual(1, self.run_guard().returncode)
        self.write(
            ".orchestration/decisions.tsv",
            "id\twhat\tbasis\nD-test\t\tscope=permission approved_by=user diff_sha256=" + digest + "\n",
        )
        green = self.run_guard()
        self.assertEqual(0, green.returncode, green.stderr)
        self.assertIn("D-test", green.stdout)
        self.assertIn(digest, green.stdout)

    def test_unchanged_surface_and_non_permission_changes_pass(self) -> None:
        self.assertIn("permission surface: unchanged", self.run_guard().stdout)
        self.manifest["claude"]["model"] = "different-model"
        self.write("home/dot_agents/agent-config.yaml", json.dumps(self.manifest))
        self.commit()
        self.assertEqual(0, self.run_guard().returncode)

    def test_rendered_file_only_changes_and_sandbox_changes_fail(self) -> None:
        for path, text in (
            ("home/dot_agents/agent-config.yaml", json.dumps({**self.manifest, "orchestrator_checkout": "~/other"})),
            ("home/.chezmoitemplates/claude-settings-managed.json", '{"permissions":{"allow":["Bash(*)"]}}'),
            ("home/.chezmoitemplates/codex-config-managed.toml", 'approval_policy="never"\n'),
            (
                "home/dot_agents/agent-config.yaml",
                json.dumps({**self.manifest, "claude": {"sandbox": {"enabled": False}}}),
            ),
        ):
            with self.subTest(path=path):
                self.write(path, text)
                self.commit()
                self.assertEqual(1, self.run_guard().returncode)

    def test_bad_refs_and_malformed_data_fail_without_executing_input(self) -> None:
        self.assertNotEqual(0, self.run_guard("--head=--output=unexpected").returncode)
        self.assertFalse((self.root / "unexpected").exists())
        self.write("home/.chezmoitemplates/claude-settings-managed.json", "{")
        self.commit()
        self.assertEqual(1, self.run_guard().returncode)
