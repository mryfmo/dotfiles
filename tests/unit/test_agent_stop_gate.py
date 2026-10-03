"""Exercise the agmsg seat Stop gate against a fixture repository and fake agmsg scripts."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/agent-stop-gate.sh"
# identities.sh answers the unsuffixed orchestrator at the main checkout and an
# -aNNN worker at any .claude/worktrees path, and insists on resolution off.
IDENTITIES_SH = """#!/usr/bin/env bash
[[ ${AGMSG_RESOLVE_PROJECT:-} == 0 ]] || exit 9
case "$1" in
*/.claude/worktrees/*) printf 'dotfiles\\tworker-a001\\n' ;;
*) printf 'dotfiles\\tworker-a001\\ndotfiles\\torch\\n' ;;
esac
"""
# history.sh must be the team-wide read: an agent argument would self-name a pane.
HISTORY_SH = """#!/usr/bin/env bash
[[ $1 == dotfiles && -z $2 ]] || exit 9
cat "$HOME/history.txt" 2>/dev/null || echo "No message history."
"""


def row(sender, recipient, body):
    return f"  ○ [2026-10-04T00:00:00Z] {sender} → {recipient}: {body}"


class AgentStopGateTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name) / "home"
        scripts = self.home / ".agents/skills/agmsg/scripts"
        scripts.mkdir(parents=True)
        for name, text in (("identities.sh", IDENTITIES_SH), ("history.sh", HISTORY_SH)):
            (scripts / name).write_text(text)
            (scripts / name).chmod(0o755)
        self.main = Path(temp.name) / "repo"
        self.main.mkdir()
        self.git("init", "-q", "-b", "main")
        (self.main / ".gitignore").write_text(".claude/worktrees/\n")
        self.git("add", ".gitignore")
        self.git("commit", "-q", "-m", "init")
        self.worker = self.main / ".claude/worktrees/x"
        self.git("worktree", "add", "-q", "-b", "x", str(self.worker))

    def git(self, *args):
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
            cwd=self.main,
            check=True,
            env={**os.environ, "HOME": str(self.home)},
        )

    def history(self, *rows):
        (self.home / "history.txt").write_text("".join(f"{r}\n" for r in rows))

    def run_gate(self, cwd, active=False):
        return subprocess.run(
            ["bash", str(SCRIPT)],
            input=json.dumps({"stop_hook_active": active, "cwd": str(cwd), "session_id": "s"}),
            capture_output=True,
            check=False,
            text=True,
            env={**os.environ, "HOME": str(self.home)},
            timeout=10,
        )

    def assert_gate(self, cwd, code, active=False):
        result = self.run_gate(cwd, active)
        self.assertEqual(result.returncode, code, result.stderr)
        return result.stderr

    def test_clean_orchestrator_passes(self):
        (self.main / ".orchestration").mkdir()
        (self.main / ".orchestration/note.md").write_text("x")
        self.assertEqual(self.assert_gate(self.main, 0), "")

    def test_untracked_file_outside_orchestration_blocks(self):
        (self.main / "junk.txt").write_text("x")
        self.assertIn("junk.txt", self.assert_gate(self.main, 2))

    def test_result_without_acceptance_blocks(self):
        self.history(
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T1 repo=/r"),
            row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
        )
        self.assertIn("task_id=T1", self.assert_gate(self.main, 2))

    def test_result_then_acceptance_passes(self):
        self.history(
            row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
            row("orch", "worker-a001", "AGMSG-ACCEPTANCE v1 task_id=T1 status=accepted"),
        )
        self.assert_gate(self.main, 0)

    def test_result_then_revision_task_passes(self):
        self.history(
            row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T1 revision=2 repo=/r"),
        )
        self.assert_gate(self.main, 0)

    def test_worker_task_newer_than_result_blocks(self):
        self.history(
            row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T2 repo=/r"),
        )
        stderr = self.assert_gate(self.worker, 2)
        self.assertIn("task_id=T2", stderr)
        self.assertNotIn("task_id=T1", stderr)

    def test_worker_after_result_passes(self):
        self.history(
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T2 repo=/r"),
            row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T2 status=ready_for_review"),
        )
        self.assert_gate(self.worker, 0)

    def test_stop_hook_active_skips_only_the_dirty_tree_check(self):
        (self.main / "junk.txt").write_text("x")
        self.assert_gate(self.main, 0, active=True)
        self.history(row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"))
        stderr = self.assert_gate(self.main, 2, active=True)
        self.assertIn("task_id=T1", stderr)
        self.assertNotIn("junk.txt", stderr)

    def test_checkout_outside_any_seat_passes(self):
        self.assert_gate(self.home, 0)


if __name__ == "__main__":
    unittest.main()
