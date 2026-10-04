"""Exercise the agmsg seat Stop gate against a fixture repository and fake agmsg scripts."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/agent-stop-gate.sh"
# identities.sh answers from per-seat files and insists on resolution off.
IDENTITIES_SH = """#!/usr/bin/env bash
[[ ${AGMSG_RESOLVE_PROJECT:-} == 0 && ! -e $HOME/ids-fail ]] || exit 9
case "$1" in
*/.claude/worktrees/*) cat "$HOME/ids-worker" ;;
*) cat "$HOME/ids-main" ;;
esac
"""
# Stand-in for the agmsg storage facade: team-wide history only, from JSONL files.
STORAGE_SH = """
agmsg_storage_load() { :; }
storage_store_exists() { [[ -f $HOME/history-$1.jsonl ]]; }
storage_history() {
    [[ $# == 1 && ! -e $HOME/store-down ]] || return 9
    cat "$HOME/history-$1.jsonl"
}
"""


def row(sender, recipient, body):
    return {"from": sender, "to": recipient, "body": body, "at": "2026-10-04T00:00:00Z"}


class AgentStopGateTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name) / "home"
        scripts = self.home / ".agents/skills/agmsg/scripts"
        scripts.mkdir(parents=True)
        (scripts / "lib").mkdir()
        (scripts / "lib/storage.sh").write_text(STORAGE_SH)
        (scripts / "identities.sh").write_text(IDENTITIES_SH)
        (scripts / "identities.sh").chmod(0o755)
        (self.home / "ids-main").write_text("dotfiles\tworker-a001\ndotfiles\torch\n")
        (self.home / "ids-worker").write_text("dotfiles\tworker-a001\n")
        # A quote and a backslash in the path exercise JSON-escaped cwd values.
        self.main = Path(temp.name) / 're"po\\x'
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

    def history(self, *rows, team="dotfiles"):
        (self.home / f"history-{team}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))

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

    def test_staged_rename_out_of_orchestration_blocks(self):
        (self.main / ".orchestration").mkdir()
        (self.main / ".orchestration/note.md").write_text("x")
        self.git("add", ".orchestration/note.md")
        self.git("commit", "-q", "-m", "note")
        self.git("mv", ".orchestration/note.md", "moved.md")
        self.assertIn("moved.md (from .orchestration/note.md)", self.assert_gate(self.main, 2))
        self.git("mv", "moved.md", ".orchestration/kept.md")
        self.assert_gate(self.main, 0)

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

    def test_worker_alive_pong_keeps_the_task_open(self):
        self.history(
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T2 repo=/r"),
            row("worker-a001", "orch", "AGMSG-PONG v1 task_id=T2 status=alive note=working"),
        )
        self.assertIn("task_id=T2", self.assert_gate(self.worker, 2))

    def test_worker_blocked_pong_closes_the_task(self):
        self.history(
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T2 repo=/r"),
            row("worker-a001", "orch", "AGMSG-PONG v1 task_id=T2 status=blocked note=boundary"),
        )
        self.assert_gate(self.worker, 0)

    def test_worker_revise_acceptance_reopens_the_task(self):
        self.history(
            row("orch", "worker-a001", "AGMSG-TASK v1 task_id=T2 repo=/r"),
            row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T2 status=ready_for_review"),
            row("orch", "worker-a001", "AGMSG-ACCEPTANCE v1 task_id=T2 status=revise next_action=fix"),
        )
        self.assertIn("task_id=T2", self.assert_gate(self.worker, 2))

    def test_solo_unsuffixed_worker_is_gated(self):
        (self.home / "ids-worker").write_text("dotfiles\tsolo-worker\n")
        self.history(row("orch", "solo-worker", "AGMSG-TASK v1 task_id=T3 repo=/r"))
        self.assertIn("task_id=T3", self.assert_gate(self.worker, 2))

    def test_every_team_of_the_identity_is_checked(self):
        (self.home / "ids-main").write_text("dotfiles\torch\nother\torch\n")
        self.history()
        self.history(row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T9 status=ready_for_review"), team="other")
        self.assertIn("task_id=T9 in team other", self.assert_gate(self.main, 2))

    def test_unreadable_store_blocks_once(self):
        self.history()
        (self.home / "store-down").write_text("")
        self.assertIn("unreadable", self.assert_gate(self.main, 2))
        self.assert_gate(self.main, 0, active=True)

    def test_failing_identity_lookup_blocks_once(self):
        self.history(row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"))
        (self.home / "ids-fail").write_text("")
        self.assertIn("identity lookup failed", self.assert_gate(self.main, 2))
        self.assert_gate(self.main, 0, active=True)

    def test_missing_agmsg_install_passes(self):
        (self.main / "junk.txt").write_text("x")
        (self.home / ".agents/skills/agmsg/scripts/identities.sh").unlink()
        self.assert_gate(self.main, 0)

    def test_json_escaped_cwd_resolves(self):
        self.assertIn('"', str(self.main))
        self.assertIn("\\", str(self.main))
        self.history(row("worker-a001", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"))
        self.assertIn("task_id=T1", self.assert_gate(self.main, 2))

    def test_checkout_outside_any_seat_passes(self):
        self.assert_gate(self.home, 0)


if __name__ == "__main__":
    unittest.main()
