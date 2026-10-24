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
        self.tmp = Path(self.temp.name).resolve()
        self.root = self.tmp / "anchor"
        self.root.mkdir()
        self.anchor = self.root
        self.env = dict(
            os.environ,
            HOME=str(self.tmp),
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
        self.git("remote", "add", "origin", "https://github.com/o/r.git")
        self.base = self.commit()
        self.root = self.tmp / "pr"
        subprocess.run(
            ["git", "-C", str(self.anchor), "worktree", "add", "-q", str(self.root)], env=self.env, check=True
        )
        self.deployed = self.tmp / ".agents/agent-config.yaml"
        self.deployed.parent.mkdir()
        self.deployed.write_text("orchestrator_checkout: ~/anchor\n")
        self.ledger = self.anchor / ".orchestration/decisions.tsv"
        self.ledger.parent.mkdir()
        tools = self.tmp / ".local/bin"
        tools.mkdir(parents=True)
        (tools / "gh").write_text("#!/bin/sh\nprintf 'o/r\\n'\n")
        (tools / "gh").chmod(0o755)
        self.env["PATH"] = str(tools) + os.pathsep + self.env["PATH"]

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

    def run_guard(self, *extra: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        command = ["uv", "run", "--no-project", "--with", "pyyaml", "python", "-I", str(GUARD)]
        return subprocess.run(
            command + ["--base", self.base, "--head", self.git("rev-parse", "HEAD"), *extra],
            cwd=cwd or self.anchor,
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
            self.ledger.write_text("id\twhat\tbasis\nD-test\t\t" + tags + "\n")
            self.assertEqual(1, self.run_guard().returncode)
        self.ledger.write_text(
            "id\twhat\tbasis\nD-test\t\tscope=permission approved_by=user diff_sha256=" + digest + "\n",
        )
        green = self.run_guard()
        self.assertEqual(0, green.returncode, green.stderr)
        self.assertIn("D-test", green.stdout)
        self.assertIn(digest, green.stdout)

    def test_guard_reads_the_ledger_from_the_anchored_checkout_never_the_pr_tree(self) -> None:
        self.change_permission()
        red = self.run_guard()
        digest = re.search(r"permission diff sha256: ([0-9a-f]{64})", red.stdout)[1]
        row = "id\twhat\tbasis\nD-test\t\tscope=permission approved_by=user diff_sha256=" + digest + "\n"
        self.write(".orchestration/decisions.tsv", row)
        forged = self.root / ".orchestration/decisions.tsv"
        alias = self.tmp / "ledger-alias"
        alias.symlink_to(forged)
        for cwd, extra in (
            (self.root, ()),
            (self.anchor, ()),
            (self.anchor, ("--decisions", str(forged))),
            (self.anchor, ("--decisions", str(alias))),
        ):
            with self.subTest(cwd=cwd, extra=extra):
                self.assertEqual(1, self.run_guard(*extra, cwd=cwd).returncode)
        external = self.tmp / "external.tsv"
        external.write_text(row)
        original = self.deployed.read_text()
        for text in ("", "orchestrator_checkout: ~/missing\n", original + original):
            with self.subTest(anchor=text):
                self.deployed.write_text(text)
                self.assertEqual(1, self.run_guard("--decisions", str(external)).returncode)
        self.deployed.write_text(original)
        other = self.tmp / "other"
        subprocess.run(["git", "clone", "-q", str(self.anchor), str(other)], env=self.env, check=True)
        with self.subTest(unrelated_checkout=True):
            self.assertEqual(1, self.run_guard("--decisions", str(external), cwd=other).returncode)
        self.git("remote", "set-url", "origin", "https://github.com/wrong/repo.git")
        with self.subTest(origin_mismatch=True):
            self.assertEqual(1, self.run_guard("--decisions", str(external)).returncode)
        self.git("remote", "set-url", "origin", "https://github.com/o/r.git")
        self.ledger.write_text(row)
        self.assertEqual(0, self.run_guard().returncode)
        self.assertEqual(0, self.run_guard("--decisions", str(external)).returncode)

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
