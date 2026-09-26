#!/usr/bin/env python3
"""Exercise the orchestrator-guardrails PreToolUse hook (G1-G6)."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "home/dot_claude/hooks/executable_orchestrator-guardrails.py"


def bash_payload(command: str, cwd: str = "/tmp/repo") -> dict:
    return {
        "session_id": "test-session",
        "cwd": cwd,
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }


class OrchestratorGuardrailsTest(unittest.TestCase):
    def run_hook(
        self, payload: dict | str, *, role: str | None = None, allow: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        if role is None:
            env.pop("HERDR_AGENTS_ROLE", None)
        else:
            env["HERDR_AGENTS_ROLE"] = role
        if allow is None:
            env.pop("GUARDRAILS_ALLOW", None)
        else:
            env["GUARDRAILS_ALLOW"] = allow
        stdin = payload if isinstance(payload, str) else json.dumps(payload)
        return subprocess.run(
            [sys.executable, str(HOOK)],
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )

    def test_g1_denies_status_inference_for_orchestrator_only(self) -> None:
        payload = bash_payload("herdr agent list")
        result = self.run_hook(payload, role="orchestrator")
        self.assertEqual(result.returncode, 2)
        self.assertIn("G1 no-status-inference", result.stderr)

        result = self.run_hook(payload, role="worker")
        self.assertEqual(result.returncode, 0)

        result = self.run_hook(bash_payload("git status"), role="orchestrator")
        self.assertEqual(result.returncode, 0)

    def test_g2_denies_bare_send_allows_dispatch(self) -> None:
        deny = self.run_hook(
            bash_payload("bash .agents/skills/agmsg/scripts/send.sh team a b msg"),
            role="orchestrator",
        )
        self.assertEqual(deny.returncode, 2)
        self.assertIn("G2 no-bare-send", deny.stderr)

        allow = self.run_hook(
            bash_payload("agmsg-dispatch dotfiles worker-pane 'AGMSG-TASK ...'"),
            role="orchestrator",
        )
        self.assertEqual(allow.returncode, 0)

    def test_g3_denies_writes_into_worker_worktree_allows_reads_and_review_tree(
        self,
    ) -> None:
        deny = self.run_hook(
            bash_payload("rm .claude/worktrees/worker-c/file.txt"), role="orchestrator"
        )
        self.assertEqual(deny.returncode, 2)
        self.assertIn("G3 worker-tree-isolation", deny.stderr)

        allow_read = self.run_hook(
            bash_payload("git show HEAD:.claude/worktrees/worker-c/file.txt"),
            role="orchestrator",
        )
        self.assertEqual(allow_read.returncode, 0)

        allow_review = self.run_hook(
            bash_payload("cp a.txt .claude/worktrees/orchestrator-review/a.txt"),
            role="orchestrator",
        )
        self.assertEqual(allow_review.returncode, 0)

    def test_g4_requires_explicit_pr_number(self) -> None:
        result = self.run_hook(
            bash_payload("gh pr merge --squash"), role="orchestrator"
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit PR number", result.stderr)

    def test_g4_denies_without_feedback_and_receipt_allows_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deny = self.run_hook(
                bash_payload("gh pr merge 42", cwd=str(root)), role="orchestrator"
            )
            self.assertEqual(deny.returncode, 2)
            self.assertIn("G4 merge-gate", deny.stderr)

            validation_dir = root / ".orchestration" / "validation"
            validation_dir.mkdir(parents=True)
            (validation_dir / "T1-pr-feedback.json").write_text(
                '{"items": [{"number": 42}]}'
            )
            receipt_dir = root / ".agents" / "worklog" / "claude" / "crit"
            receipt_dir.mkdir(parents=True)
            (receipt_dir / "pr-42-receipt.md").write_text("reviewed\n")

            allow = self.run_hook(
                bash_payload("gh pr merge 42", cwd=str(root)), role="orchestrator"
            )
            self.assertEqual(allow.returncode, 0, allow.stderr)

    def test_g4_delete_branch_denied_when_worktree_still_checked_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            validation_dir = root / ".orchestration" / "validation"
            validation_dir.mkdir(parents=True)
            (validation_dir / "T1-pr-feedback.json").write_text(
                '{"items": [{"number": 42}]}'
            )
            receipt_dir = root / ".agents" / "worklog" / "claude" / "crit"
            receipt_dir.mkdir(parents=True)
            (receipt_dir / "pr-42-receipt.md").write_text("reviewed\n")

            bin_dir = root / "bin"
            bin_dir.mkdir()
            self._write_fake_gh(bin_dir, head_branch="feat/still-open")
            self._write_fake_git_worktree_list(
                bin_dir,
                porcelain=(
                    "worktree /repos/dotfiles/.claude/worktrees/worker-c\n"
                    "HEAD abc123\n"
                    "branch refs/heads/feat/still-open\n"
                    "\n"
                    "worktree /repos/dotfiles\n"
                    "HEAD def456\n"
                    "branch refs/heads/main\n"
                ),
            )

            env = os.environ.copy()
            env["HERDR_AGENTS_ROLE"] = "orchestrator"
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            result = subprocess.run(
                [sys.executable, str(HOOK)],
                input=json.dumps(
                    bash_payload("gh pr merge 42 --delete-branch", cwd=str(root))
                ),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("still checked out at worktree", result.stderr)

    def _write_fake_gh(self, bin_dir: Path, *, head_branch: str) -> None:
        script = bin_dir / "gh"
        script.write_text(f"#!{sys.executable}\nprint({head_branch!r})\n")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)

    def _write_fake_git_worktree_list(self, bin_dir: Path, *, porcelain: str) -> None:
        script = bin_dir / "git"
        script.write_text(f"#!{sys.executable}\nprint({porcelain!r}, end='')\n")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)

    def test_g5_denies_make_upgrade_for_worker_only(self) -> None:
        payload = bash_payload("make upgrade")
        deny = self.run_hook(payload, role="worker")
        self.assertEqual(deny.returncode, 2)
        self.assertIn("G5 no-make-upgrade-in-tasks", deny.stderr)

        allow = self.run_hook(payload, role="orchestrator")
        self.assertEqual(allow.returncode, 0)

    def test_g6_warns_but_allows_broad_search(self) -> None:
        result = self.run_hook(bash_payload("grep -r TODO ."), role="orchestrator")
        self.assertEqual(result.returncode, 0)
        decision = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "allow")
        self.assertIn("G6 no-self-exploration", decision["permissionDecisionReason"])

        scoped = self.run_hook(
            bash_payload("grep -r TODO .orchestration"), role="orchestrator"
        )
        self.assertEqual(scoped.returncode, 0)
        self.assertEqual(scoped.stdout, "")

    def test_role_missing_enforces_nothing(self) -> None:
        for command in ("herdr agent list", "make upgrade"):
            with self.subTest(command=command):
                result = self.run_hook(bash_payload(command), role=None)
                self.assertEqual(result.returncode, 0)

    def test_guardrails_allow_override_skips_rule_and_logs(self) -> None:
        result = self.run_hook(
            bash_payload("herdr agent list"), role="orchestrator", allow="G1"
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("GUARDRAILS_ALLOW override used for G1", result.stderr)

    def test_malformed_json_fails_open(self) -> None:
        result = self.run_hook("not-json", role="orchestrator")
        self.assertEqual(result.returncode, 0)
        self.assertIn("failed to parse", result.stderr)


if __name__ == "__main__":
    unittest.main()
