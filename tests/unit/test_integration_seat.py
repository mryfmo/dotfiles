"""Plan 023 F4 items 1 and 2: integrate-seat.sh and result-precheck.sh against stub gh, uv, agmsg and scripts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEAT = ROOT / "scripts/orchestrator/integrate-seat.sh"
PRECHECK = ROOT / "scripts/orchestrator/result-precheck.sh"
TASK, OWNER, ORCH, ME, TEAM = (
    "dotfiles-T129-x-a01",
    "dotfiles-T129-x-followup-a01",
    "claude-deep-x",
    "claude-x-a009",
    "t",
)
GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@t",
    "GIT_CONFIG_COUNT": "2",
    "GIT_CONFIG_KEY_0": "commit.gpgsign",
    "GIT_CONFIG_VALUE_0": "false",
    "GIT_CONFIG_KEY_1": "init.defaultBranch",
    "GIT_CONFIG_VALUE_1": "main",
}
STUB = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$CALLS/{name}.log"
echo {name} >> "$CALLS/order.log"
exit "$(cat "$CALLS/{name}.status" 2> /dev/null || echo 0)"
"""
SCRIPTS = {
    "pr-feedback.py": "pr-feedback",
    "orchestrator/local-review.sh": "local-review",
    "orchestrator/local-advisory.sh": "local-advisory",
    "orchestrator/resolve-threads.sh": "resolve-threads",
    "orchestrator/fill_sweep.py": "fill_sweep",
    "orchestrator/acceptance-front-matter.py": "acceptance-front-matter",
}
# gh colours its output whenever CLICOLOR_FORCE is set to anything but 0, as the real one does (C-62).
GH = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$CALLS/gh.log"
paint() { if [ "${CLICOLOR_FORCE:-0}" != 0 ]; then sed $'s/.*/\\e[32m&\\e[0m/'; else cat; fi; }
jq=; prev=; path=; for a; do [ "$prev" != --jq ] || jq=$a; prev=$a; case $a in repos/*) path=$a ;; esac; done
case "$1 $2" in
"pr view") paint < "$CALLS/head" ;;
"pr checks") exit "$(cat "$CALLS/checks.status" 2> /dev/null || echo 0)" ;;
"pr merge") echo merge >> "$CALLS/order.log" ;;
"api user") echo orch | paint ;;
"api "*)
    case $path in *reviews) f=$CALLS/reviews.json ;; */issues/*) f=$CALLS/issues.json ;; *) f=$CALLS/comments.json ;; esac
    if [ -n "$jq" ]; then JQ -rc "$jq" "$f"; else cat "$f"; fi | paint ;;
esac
"""
UV = """#!/usr/bin/env bash
while [ "$1" != python ]; do shift; done
shift 2
exec "$@"
"""
BOT = {"login": "chatgpt-codex-connector[bot]"}


class IntegrationSeatTest(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.calls, self.bin, agmsg = self.temp / "calls", self.temp / "bin", self.temp / "agmsg"
        for d in (self.calls, self.bin, agmsg, self.temp / "home"):
            d.mkdir()
        self.env = {
            **GIT_ENV,
            "CALLS": str(self.calls),
            "HOME": str(self.temp / "home"),
            "TMPDIR": str(self.temp),
            "AGMSG_SCRIPTS": str(agmsg),
            "PATH": f"{self.bin}{os.pathsep}/usr/bin{os.pathsep}/bin",
        }
        origin, seed = self.temp / "origin.git", self.temp / "seed"
        self.git("init", "-q", "--bare", str(origin), cwd=self.temp)
        self.git("clone", "-q", str(origin), str(seed), cwd=self.temp)
        for rel, name in SCRIPTS.items():
            self.executable(seed / "scripts" / rel, STUB.format(name=name))
        self.commit(seed, "base")
        self.git("push", "-q", "origin", "HEAD:main", cwd=seed)
        self.executable(seed / "scripts/orchestrator/new.sh", "#!/bin/sh\necho new\n")
        self.commit(seed, "the PR")
        self.git("push", "-q", "origin", "HEAD:refs/pull/7/head", cwd=seed)
        self.head, self.seed = self.git("rev-parse", "HEAD", cwd=seed), seed
        self.main = self.temp / "main"
        self.git("clone", "-q", str(origin), str(self.main), cwd=self.temp)
        self.seat = self.main / ".claude/worktrees/seat"
        self.git("worktree", "add", "-q", "--detach", str(self.seat), "origin/main", cwd=self.main)
        (self.main / ".orchestration/acceptance").mkdir(parents=True)
        (self.main / f".orchestration/acceptance/{TASK}.md").write_text("---\n{}\n---\n\n# Record\n")
        self.executable(self.bin / "gh", GH.replace("JQ", shutil.which("jq") or "jq"))
        self.executable(self.bin / "uv", UV)
        (self.bin / "jq").symlink_to(shutil.which("jq") or "/usr/bin/jq")
        self.executable(self.bin / "agmsg-dispatch", '#!/bin/sh\nprintf \'%s\\n\' "$*" >> "$CALLS/dispatch.log"\n')
        self.executable(
            agmsg / "whoami.sh",
            f'#!/bin/sh\n[ "$2" = claude-code ] && echo "agent={ME} teams={TEAM} type=claude-code project=$1"\n',
        )
        self.executable(agmsg / "history.sh", '#!/bin/sh\ncat "$CALLS/history.txt"\n')
        team = json.dumps([{"member": ORCH, "pane": f"{self.temp}/herdr.sock:wA:p1"}])
        self.executable(agmsg / "team.sh", f"#!/bin/sh\necho '{team}'\n")
        (self.calls / "head").write_text(self.head + "\n")
        (self.calls / "reviews.json").write_text(json.dumps([{"id": 9, "user": BOT, "commit_id": self.head}]))
        (self.calls / "issues.json").write_text("[]")
        comments = [
            {"id": 4300000001, "in_reply_to_id": None, "user": BOT, "body": "**![P1 Badge](x)** a"},
            {"id": 4300000002, "in_reply_to_id": None, "user": BOT, "body": "**![P2 Badge](x)** b"},
        ]
        (self.calls / "comments.json").write_text(json.dumps(comments))
        self.bus("4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory)")

    def git(self, *args: str, cwd: Path) -> str:
        return subprocess.run(
            ["git", *args], cwd=cwd, env={**os.environ, **GIT_ENV}, capture_output=True, text=True, check=True
        ).stdout.strip()

    def commit(self, repo: Path, message: str) -> None:
        self.git("add", "-A", cwd=repo)
        self.git("commit", "-q", "--allow-empty", "-m", message, cwd=repo)

    def executable(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(0o755)

    def bus(self, threads: str, task_sha: str = "0" * 64) -> None:
        (self.calls / "history.txt").write_text(
            f"  ○ [2026-10-17T10:00:00Z] {ORCH} → claude-x-a001: AGMSG-TASK v1 task_id={TASK} round=1 task_sha256={task_sha}\n"
            f"  ○ [2026-10-17T11:00:00Z] claude-x-a001 → {ORCH}: AGMSG-RESULT v1 task_id={TASK} status=done threads={threads}\n"
        )

    def run_script(self, script: Path, *args: str, cwd: Path, code: int, env: dict | None = None):
        result = subprocess.run(
            ["bash", str(script), *args],
            cwd=cwd,
            env={**self.env, **(env or {})},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result

    def logged(self, name: str) -> list[str]:
        path = self.calls / f"{name}.log"
        return path.read_text().splitlines() if path.exists() else []

    def reset_calls(self) -> None:
        for path in self.calls.glob("*.log"):
            path.unlink()

    # integrate-seat.sh (item 1)

    def test_integrate_seat_runs_the_steps_in_order_stops_at_the_first_failure_and_never_merges(self) -> None:
        h7, v = self.head[:7], self.seat / ".orchestration/validation"
        self.run_script(SEAT, TASK, "7", "--owner", OWNER, cwd=self.seat, code=0)
        order = [
            "pr-feedback",
            "local-review",
            "resolve-threads",
            "pr-feedback",
            "fill_sweep",
            "acceptance-front-matter",
        ]
        self.assertEqual(order, self.logged("order"))
        record = f".orchestration/validation/{TASK}-integration-{h7}.md"
        self.assertEqual(
            [
                f"{TEAM} {ME} {ORCH} wA:p1 AGMSG-RESULT v1 task_id={TASK} kind=integration status=ready_for_audit head={self.head} record={record}"
            ],
            self.logged("dispatch"),
        )
        self.assertEqual(
            f"4300000001\tfixed:abcdef1\n4300000002\tnot-applicable:advisory P2 owned by {OWNER}; "
            "evidence=gh api repos/{owner}/{repo}/pulls/comments/4300000002\n",
            (v / f"{TASK}-dispositions-{h7}.tsv").read_text(),
        )
        text = (self.seat / record).read_text()
        for name in ("base", "pr-view", "checks", "sweep", "local-review", "resolve-threads", "fill-sweep", "record"):
            self.assertIn(f"## {name} rc=0\n", text)
        self.assertIn(f"- final head: {self.head}\n", text)
        self.assertIn("---\n{}\n---\n\n# Record\n", (self.seat / f".orchestration/acceptance/{TASK}.md").read_text())
        receipt = (v / f"{TASK}-review-receipt.md").read_text()
        self.assertIn("review_surface: crit-data\nreviewer: claude-code\n", receipt)
        self.assertIn(f"head: {self.head}\npr: 7\n", receipt)
        # Never past the audit: no merge call, and no audit, gate or merge command in the script at all.
        self.assertNotIn("merge", self.logged("order"))
        self.assertIsNone(
            re.search(r"pr merge|orch-audit|orch-gate|require-crit-review|herdr-agents --audit", SEAT.read_text())
        )
        # The first failing step ends the chain with a blocked RESULT naming it.
        for label, setup, step in (
            ("CI", lambda: (self.calls / "checks.status").write_text("1"), "checks rc=1"),
            ("threads", lambda: (self.calls / "resolve-threads.status").write_text("3"), "resolve-threads rc=3"),
            ("an unfixed P1", lambda: self.bus("4300000003:P1:open:4300000003"), "thread-4300000003-P1-not-fixed rc=1"),
        ):
            with self.subTest(label):
                self.reset_calls()
                setup()
                self.run_script(SEAT, TASK, "7", "--owner", OWNER, cwd=self.seat, code=1)
                [line] = self.logged("dispatch")
                self.assertIn(f"kind=integration status=blocked step={step} head={self.head}", line)
                self.assertNotIn("acceptance-front-matter", self.logged("order"))
                for path in self.calls.glob("*.status"):
                    path.unlink()
                self.bus("4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory)")
        # Refused before anything runs: malformed arguments, no RESULT on the bus, a seat not at origin/main.
        self.reset_calls()
        for args, message in ((("a/b", "7"), "invalid id"), ((TASK, "x"), "invalid PR number")):
            self.assertIn(message, self.run_script(SEAT, *args, cwd=self.seat, code=2).stderr)
        (self.calls / "history.txt").write_text("")
        self.assertIn("no AGMSG-TASK", self.run_script(SEAT, TASK, "7", cwd=self.seat, code=2).stderr)
        self.assertEqual([], self.logged("order") + self.logged("dispatch"))

    def test_integrate_seat_reads_plain_gh_output_under_clicolor_force(self) -> None:
        # Amendment 1 (C-62): with CLICOLOR_FORCE=1 inherited, gh's JSON would arrive coloured; the script's export
        # keeps every gh call plain, so the head check and the comments the sweep fill reads still parse.
        self.run_script(SEAT, TASK, "7", "--owner", OWNER, cwd=self.seat, code=0, env={"CLICOLOR_FORCE": "1"})
        comments = json.loads((self.seat / f".orchestration/validation/{TASK}-pr-comments.json").read_text())
        self.assertEqual([4300000001, 4300000002], [c["id"] for c in comments])
        [line] = self.logged("dispatch")
        self.assertIn("status=ready_for_audit", line)

    # result-precheck.sh (item 2)

    def precheck_ready(self, cap: int = 10) -> Path:
        """The PR head carries the task copy, a validation file with the Check's commands and a report."""
        d = self.seed / f".orchestration/{TASK}"
        d.mkdir(parents=True, exist_ok=True)
        check = (
            "`uv run python -m unittest tests/unit/test_x.py -v` green, `shellcheck scripts/orchestrator/new.sh` "
            f"clean, with `git diff --numstat origin/main...HEAD`: at most {cap} changed lines (added plus deleted) "
            "outside `tests/` and `.orchestration/`, excluding `docs/x.md` (text), and 100 added lines under `tests/`."
        )
        allowed = (
            "allowed_files:\n  - scripts/orchestrator/new.sh\n  - .orchestration/dotfiles-T129-x-a01/**\nafter: []\n"
        )
        (d / "task.md").write_text(
            f"---\ntask_id: {TASK}\n{allowed}---\n\n# Task\n\n## Check\n\n{check}\n\n## Completion\n\nx\n"
        )
        (d / "validation.md").write_text(
            "$ uv run python -m unittest tests/unit/test_x.py -v\nOK\n$ shellcheck scripts/orchestrator/new.sh\n"
            "$ git diff --numstat origin/main...HEAD\n"
        )
        (d / "report.md").write_text("threads=4300000001:P1:fixed:abcdef1;4300000002:P2:proposed(advisory)\n")
        self.commit(self.seed, "evidence")
        self.git("push", "-q", "-f", "origin", "HEAD:refs/pull/7/head", cwd=self.seed)
        self.head = self.git("rev-parse", "HEAD", cwd=self.seed)
        (self.calls / "head").write_text(self.head + "\n")
        (self.calls / "reviews.json").write_text(json.dumps([{"id": 9, "user": BOT, "commit_id": self.head}]))
        self.bus("-", hashlib.sha256((d / "task.md").read_bytes()).hexdigest())
        return d

    def precheck(self, code: int, *args: str) -> tuple[str, str]:
        result = self.run_script(PRECHECK, "run", TASK, "7", *(args or (self.head,)), cwd=self.seed, code=code)
        return result.stdout, (self.seed / f".orchestration/{TASK}/precheck-{self.head[:7]}.md").read_text()

    def test_result_precheck_refuses_each_missing_condition_and_verify_refuses_a_result_without_a_matching_receipt(
        self,
    ) -> None:
        d = self.precheck_ready()
        out, receipt = self.precheck(0)
        self.assertEqual(9, len(re.findall(r"^- [a-i] ok: ", receipt, re.MULTILINE)), receipt)
        self.assertIn("local-review: unavailable", receipt)
        self.assertIn("audit-dry-run: unavailable", receipt)
        [(digest, path)] = re.findall(r"^precheck=([0-9a-f]{64}) (\S+)$", out, re.MULTILINE)
        self.assertEqual(hashlib.sha256((self.seed / path).read_bytes()).hexdigest(), digest)
        # verify: the receipt committed after the head (a records-only commit) is found by its sha256.
        self.commit(self.seed, "the receipt")
        good = self.git("rev-parse", "HEAD", cwd=self.seed)
        verify = lambda line, code: self.run_script(PRECHECK, "verify", TASK, line, cwd=self.seed, code=code).stdout
        self.assertEqual("", verify(f"AGMSG-RESULT v1 task_id={TASK} head={good[:8]} precheck={digest}", 0))
        refusal = f"AGMSG-ACCEPTANCE v1 task_id={TASK} status=revise reason=precheck:"
        self.assertIn(f"{refusal}receipt next_action=", verify(f"head={good} precheck={'0' * 64}", 1))
        (self.seed / "scripts/orchestrator/new.sh").write_text("#!/bin/sh\necho changed after the receipt\n")
        self.commit(self.seed, "code after the receipt")
        later = self.git("rev-parse", "HEAD", cwd=self.seed)
        self.assertIn(f"{refusal}code-after-receipt next_action=", verify(f"head={later} precheck={digest}", 1))
        self.git("reset", "-q", "--hard", good, cwd=self.seed)
        # Each condition, broken alone, is named missing and exits 1.
        cases = {
            "a": lambda: (d / "task.md").write_text((d / "task.md").read_text() + "edited\n"),
            "c": lambda: (d / "task.md").write_text((d / "task.md").read_text().replace("at most 10", "at most 1")),
            "d": lambda: (d / "validation.md").write_text("$ uv run python -m unittest tests/unit/test_x.py -v\n"),
            "e": lambda: (self.calls / "checks.status").write_text("1"),
            "f": lambda: (self.calls / "reviews.json").write_text("[]"),
            "g": lambda: (d / "report.md").write_text("threads=4300000001:P1:proposed(x);4300000002:P2:proposed(x)\n"),
            "h": lambda: self.executable(
                self.seed / f".orchestration/validation/{TASK}-local-review-{self.head[:7]}.md",
                "- [P1] high a.sh:1 x\n",
            ),
        }
        for letter, broken in cases.items():
            with self.subTest(letter):
                self.git("reset", "-q", "--hard", self.head, cwd=self.seed)
                self.git("clean", "-q", "-fd", cwd=self.seed)
                (self.calls / "checks.status").unlink(missing_ok=True)
                (self.calls / "reviews.json").write_text(json.dumps([{"id": 9, "user": BOT, "commit_id": self.head}]))
                self.bus("-", hashlib.sha256((d / "task.md").read_bytes()).hexdigest())
                broken()
                if letter == "c":  # the edited task copy is the dispatched one in this case, so only (c) breaks
                    self.bus("-", hashlib.sha256((d / "task.md").read_bytes()).hexdigest())
                out, receipt = self.precheck(1)
                self.assertIn(f"- {letter} missing: ", receipt)
                self.assertIn(f"missing: {letter} ", out)
                self.assertEqual(8, len(re.findall(r"^- [a-i] ok: ", receipt, re.MULTILINE)), receipt)
        # (b): a changed file outside allowed_files.
        self.git("reset", "-q", "--hard", self.head, cwd=self.seed)
        self.git("clean", "-q", "-fd", cwd=self.seed)
        (self.seed / "other.txt").write_text("outside\n")
        self.commit(self.seed, "outside allowed_files")
        self.head = self.git("rev-parse", "HEAD", cwd=self.seed)
        (self.calls / "head").write_text(self.head + "\n")
        (self.calls / "reviews.json").write_text(json.dumps([{"id": 9, "user": BOT, "commit_id": self.head}]))
        out, receipt = self.precheck(1)
        self.assertIn("- b missing: ", receipt)
        self.assertIn("no other.txt", receipt)
        # A receipt naming a missing check is refused by verify.
        self.commit(self.seed, "the failing receipt")
        sha = hashlib.sha256(receipt.encode()).hexdigest()
        self.assertIn(
            f"{refusal}b next_action=", verify(f"head={self.git('rev-parse', 'HEAD', cwd=self.seed)} precheck={sha}", 1)
        )
        # Malformed arguments are refused before anything is read.
        for args in (
            ("run", "a/b", "7", self.head),
            ("run", TASK, "x", self.head),
            ("run", TASK, "7", "abc"),
            ("verify", TASK, "no fields"),
        ):
            self.run_script(PRECHECK, *args, cwd=self.seed, code=2)


if __name__ == "__main__":
    unittest.main()
