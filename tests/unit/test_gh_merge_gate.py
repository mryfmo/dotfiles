#!/usr/bin/env python3
"""Exercise the gh-merge-gate PreToolUse hook against a stub gh, without touching GitHub."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


HOOK = Path(__file__).resolve().parents[2] / "home/dot_claude/hooks/executable_gh-merge-gate.sh"
SHA = "3498973bd057ea4fb405823de718e9da6e40e548"
STUB = r"""#!/usr/bin/env bash
state=${GATE_STUB_DIR}
case "$*" in
  "repo view --json nameWithOwner --jq .nameWithOwner") echo o/r ;;
  "repo view o/r --json defaultBranchRef --jq .defaultBranchRef.name") echo main ;;
  "pr view 7 --json headRefOid,baseRefName,state,isDraft") cat "${state}/pr.json" ;;
  api\ repos/o/r/rules/branches/main*) cat "${state}/required.txt" ;;
  api\ --paginate\ repos/o/r/commits/*/check-runs*) cat "${state}/runs.txt" ;;
  api\ repos/o/r/commits/*/status*) : ;;
  "api repos/o/r/branches/task/ok --jq .commit.sha"|"api repos/o/r/branches/orchestration/b --jq .commit.sha") echo "${GATE_HEAD_SHA}" ;;
  api\ repos/o/r/branches/*) exit 1 ;;
  "pr list --repo o/r --head stack/parent --state open --json number --jq length") echo 1 ;;
  "pr list --repo o/r --head "*) echo 0 ;;
  api\ repos/o/r/compare/*) cat "${state}/compare.txt" ;;
  *) echo "unexpected gh $*" >&2; exit 9 ;;
esac
"""


class GhMergeGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        (self.bin / "gh").write_text(STUB)
        (self.bin / "gh").chmod(0o755)
        self.repo = self.tmp / "repo"
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".orchestration/acceptance").mkdir(parents=True)
        (self.repo / ".orchestration/validation").mkdir(parents=True)
        self.write_record(SHA, "accepted")
        (self.repo / f".orchestration/validation/t-audit-{SHA[:7]}.md").write_text("audit\n")
        self.write_pr(SHA)
        (self.tmp / "required.txt").write_text("validate\ntest\n")
        (self.tmp / "runs.txt").write_text("validate\ntest\nCodeRabbit\n")

    def write_record(self, head: str, *statuses: str) -> None:
        lines = "".join(f"- AGMSG-ACCEPTANCE v1 task_id=t status={status} reason=r\n" for status in statuses)
        (self.repo / ".orchestration/acceptance/t.md").write_text(f'{{\n  "head": "{head}"\n}}\n---\n{lines}')

    def write_pr(self, head: str, base: str = "main", state: str = "OPEN") -> None:
        pr = {"headRefOid": head, "baseRefName": base, "state": state, "isDraft": False}
        (self.tmp / "pr.json").write_text(json.dumps(pr))

    def decide(self, command: str, cwd: Path | None = None) -> tuple[str, str]:
        env = {
            **os.environ,
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "GATE_STUB_DIR": str(self.tmp),
            "XDG_STATE_HOME": str(self.tmp / "state"),
            "GATE_HEAD_SHA": SHA,
        }
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd or self.repo)})
        result = subprocess.run(
            ["bash", str(HOOK)], input=payload, capture_output=True, text=True, env=env, check=False
        )
        self.assertEqual(0, result.returncode, result.stderr)
        if not result.stdout:
            return "", ""
        decision = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual("PreToolUse", decision["hookEventName"])
        return decision["permissionDecision"], decision["permissionDecisionReason"]

    def pinned(self, extra: str = "") -> str:
        return f"gh pr merge 7 --squash --match-head-commit {SHA}{extra}"

    def test_unrelated_commands_get_no_decision(self) -> None:
        for command in ("gh pr view 7", "git merge main", "gh pr checks 7", "echo merged"):
            with self.subTest(command=command):
                self.assertEqual(("", ""), self.decide(command))

    def test_pinned_accepted_green_head_is_allowed(self) -> None:
        self.assertEqual("allow", self.decide(self.pinned())[0])
        log = (self.tmp / "state/claude/gh-merge-gate.log").read_text().splitlines()
        self.assertEqual("allow", log[-1].split("\t")[1])
        self.assertEqual("allow", self.decide(f"gh pr merge --match-head-commit={SHA} -s 7")[0])

    def test_update_branch_is_allowed(self) -> None:
        self.assertEqual("allow", self.decide("gh pr update-branch 7")[0])
        self.assertEqual("allow", self.decide("gh pr update-branch 7 --repo o/r")[0])
        self.assertEqual("ask", self.decide("gh pr update-branch 7 --rebase")[0])

    def test_bypass_and_unpinned_forms_ask(self) -> None:
        for command in (
            "gh pr merge 7 --squash",
            "gh pr merge 7 --merge --match-head-commit " + SHA,
            f"gh pr merge 7 --squash --match-head-commit {SHA[:12]}",
            self.pinned(" --admin"),
            self.pinned(" --auto"),
            self.pinned(" --delete-branch"),
            self.pinned(" --body x"),
            self.pinned("; gh pr merge 8 --admin"),
            self.pinned(" && true"),
            self.pinned(" $(true)"),
            f"env gh pr merge 7 --squash --match-head-commit {SHA}",
            "gh api -X PUT repos/o/r/pulls/7/merge",
            "gh api repos/o/r/pulls/7/merge -X PUT",
        ):
            with self.subTest(command=command):
                self.assertEqual("ask", self.decide(command)[0])

    def test_head_base_checks_and_acceptance_are_enforced(self) -> None:
        self.write_pr("f" * 40)
        self.assertIn("head is not", self.decide(self.pinned())[1])
        self.write_pr(SHA, base="tools/x")
        self.assertIn("does not target", self.decide(self.pinned())[1])
        self.write_pr(SHA, state="MERGED")
        self.assertIn("not open", self.decide(self.pinned())[1])
        self.write_pr(SHA)
        (self.tmp / "runs.txt").write_text("validate\n")
        self.assertIn("required check test", self.decide(self.pinned())[1])
        (self.tmp / "runs.txt").write_text("validate\ntest\n")
        (self.tmp / "required.txt").write_text("")
        self.assertIn("requires no status checks", self.decide(self.pinned())[1])
        (self.tmp / "required.txt").write_text("validate\ntest\n")
        (self.repo / f".orchestration/validation/t-audit-{SHA[:7]}.md").unlink()
        self.assertIn("no audit", self.decide(self.pinned())[1])
        (self.repo / f".orchestration/validation/t-audit-{SHA[:7]}.md").write_text("audit\n")
        self.write_record(SHA, "accepted", "revise")
        self.assertIn("is revise not accepted", self.decide(self.pinned())[1])
        self.write_record(SHA)
        self.assertIn("is missing not accepted", self.decide(self.pinned())[1])
        self.write_record(SHA, "revise", "accepted")
        self.assertEqual("allow", self.decide(self.pinned())[0])
        self.write_record("e" * 40, "accepted")
        self.assertIn("no acceptance record", self.decide(self.pinned())[1])

    def test_linked_worktree_asks(self) -> None:
        subprocess.run(
            ["git", "-C", str(self.repo), "commit", "-q", "--allow-empty", "-m", "i"],
            check=True,
            env={
                **os.environ,
                "GIT_AUTHOR_NAME": "t",
                "GIT_AUTHOR_EMAIL": "t@t",
                "GIT_COMMITTER_NAME": "t",
                "GIT_COMMITTER_EMAIL": "t@t",
                "GIT_CONFIG_GLOBAL": "/dev/null",
            },
        )
        worktree = self.tmp / "wt"
        subprocess.run(["git", "-C", str(self.repo), "worktree", "add", "-q", str(worktree)], check=True)
        self.assertIn("main checkout", self.decide(self.pinned(), cwd=worktree)[1])
        self.assertIn("no existing working directory", self.decide(self.pinned(), cwd=self.tmp / "gone")[1])

    def test_create_draft_of_a_pushed_task_branch_is_allowed(self) -> None:
        for command in (
            "gh pr create --draft --base main --head task/ok --title 'feat: x; y' --body-file /tmp/b.md",
            "gh pr create -d -B stack/parent -H task/ok --fill",
        ):
            with self.subTest(command=command):
                self.assertEqual("allow", self.decide(command, cwd=self.tmp)[0])

    def test_create_ready_needs_acceptance_or_records_only(self) -> None:
        ready = "gh pr create --base main --head task/ok --title t --body b"
        self.assertEqual("allow", self.decide(ready)[0])
        self.write_record(SHA, "accepted", "revise")
        self.assertIn("not accepted", self.decide(ready)[1])
        self.assertIn("not in a git checkout", self.decide(ready, cwd=self.tmp)[1])
        records = "gh pr create --base main --head orchestration/b --fill"
        (self.tmp / "compare.txt").write_text("2\n.orchestration/a.md\n.orchestration/b.tsv\n")
        self.assertEqual("allow", self.decide(records)[0])
        (self.tmp / "compare.txt").write_text("2\n.orchestration/a.md\nscripts/x.sh\n")
        self.assertIn("outside .orchestration", self.decide(records)[1])

    def test_create_other_forms_ask(self) -> None:
        for command in (
            "gh pr create --draft --head task/ok --fill",
            "gh pr create --draft --base main --fill",
            "gh pr create --draft --base other --head task/ok --fill",
            "gh pr create --draft --base main --head task/missing --fill",
            "gh pr create --draft --base main --head main --fill",
            "gh pr create --draft --base main --head task/ok --fill --reviewer x",
            "gh pr create --draft --base main --head task/ok --fill --web",
            'gh pr create --draft --base main --head task/ok --title "$(id)"',
            "gh pr create --draft --base main --head task/ok --fill; echo x",
            "gh pr create --draft --base main --head task/ok --fill | cat",
            "gh pr create --draft --base main --head task/ok --title 'unterminated",
            "cd /tmp && gh pr create --draft --base main --head task/ok --fill",
        ):
            with self.subTest(command=command):
                self.assertEqual("ask", self.decide(command)[0])


if __name__ == "__main__":
    unittest.main()
