"""Exercise the review-side chain scripts (plan 021 step 6.3) in a temporary git repository.

Each script runs as a subprocess from this checkout with the temporary repository as its working directory, so the
repository root it resolves is the temporary one. git is the real one. A stub review binary appends its argv, its
working directory, the HEAD there, PATH and its stdin to `<calls>/<name>.log`, prints `<calls>/transcript` and exits with
`<calls>/status` (0 when absent).
"""

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2] / "scripts/orchestrator"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
STUB = (
    "#!/usr/bin/env bash\n"
    '{{ printf "argv:"; printf " %s" "$@"; printf "\\ncwd: %s\\nhead: %s\\npath: %s\\nstdin: %s\\n" '
    '"$(pwd -P)" "$(git rev-parse HEAD)" "$PATH" "$(cat)"; }} >> "$CALLS/{name}.log"\n'
    'cat "$CALLS/transcript"\nexit "$(cat "$CALLS/status" 2> /dev/null || echo 0)"\n'
)
ARGV = "argv: --profile review -s read-only review --base main"
SCAN_HIT = "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"


class ChainReviewScriptsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        self.git("init", "-q", "-b", "main", str(self.repo), cwd=self.temp)
        self.write("a.txt", "a\n")
        self.git("add", "a.txt")
        self.git("commit", "-q", "-m", "main")
        self.env = {**os.environ, **GIT_ENV, "CALLS": str(self.calls), "TMPDIR": str(self.temp)}
        for name in ("CODEX_BIN", "ORCH_REVIEW_WORKTREE"):
            self.env.pop(name, None)

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cwd or self.repo,
            env={**os.environ, **GIT_ENV},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def write(self, rel, text, root=None):
        path = (root or self.repo) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def stub(self, path, name):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(STUB.format(name=name))
        path.chmod(0o755)

    def log(self, name):
        path = self.calls / f"{name}.log"
        return path.read_text() if path.exists() else ""

    def run_tool(self, name, *args, code=0, env=None, cwd=None):
        # The review binary must not read what the caller's stdin holds.
        result = subprocess.run(
            ["bash", str(TOOLS / name), *map(str, args)],
            capture_output=True,
            text=True,
            input="caller stdin\n",
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout

    def test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file(self):
        review = self.temp / "review"
        self.git("worktree", "add", "-q", "--detach", str(review), "main")
        # The head commit, made in the review worktree, carries a decoy bin/codex; the main working tree never does.
        self.stub(review / "bin/codex", "decoy")
        self.write("b.txt", "b\n", root=review)
        self.git("add", "bin/codex", "b.txt", cwd=review)
        self.git("commit", "-q", "-m", "head", cwd=review)
        head, base = self.git("rev-parse", "HEAD", cwd=review), self.git("rev-parse", "main")
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        self.stub(self.temp / "bin/codex", "codex")
        (self.repo / ".orchestration/validation").mkdir(parents=True)
        path = f"./bin{os.pathsep}{self.temp / 'bin'}{os.pathsep}{os.environ['PATH']}"
        env = {"ORCH_REVIEW_WORKTREE": str(review), "PATH": path}
        # An earlier marker's message is not the final one; the worktree prefix is stripped; a repeated line counts once.
        final = f"One finding.\n- [P2] {review}/b.txt:1 b is new\n- [P2] {review}/b.txt:1 b is new\n"
        (self.calls / "transcript").write_text(f"codex\n- [P1] {review}/a.txt:1 superseded\ncodex\n{final}")
        finding = "- [P2] b.txt:1 b is new"
        call = f"{ARGV}\ncwd: {review}\nhead: {head}\npath: {path}\nstdin: \n"

        def out(task):
            return self.repo / f".orchestration/validation/{task}-local-review-{head[:7]}.md"

        with self.subTest("a review worktree path without its own .git entry exits 2"):
            # First, while the main working tree is clean: the dirty check alone would pass it.
            (self.repo / "plain").mkdir()
            plain = {**env, "ORCH_REVIEW_WORKTREE": str(self.repo / "plain")}
            self.assertIn("is not a worktree root", self.run_tool("local-review.sh", "t-p", head, 9, code=2, env=plain))
            self.assertEqual("", self.log("codex"))
            self.assertEqual(base, self.git("rev-parse", "HEAD"))
        with self.subTest("CODEX_BIN unset: codex resolved in the root before the checkout"):
            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
            self.assertEqual(f"{finding}\nlocal-review: 1 findings ({out('t-a')})\n", stdout)
            self.assertEqual(call, self.log("codex"))
            self.assertEqual("", self.log("decoy"))
            self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=review))
            status = self.git("status", "--porcelain", "--untracked-files=all")
            self.assertEqual(f"?? .orchestration/validation/t-a-local-review-{head[:7]}.md", status)
            text = out("t-a").read_text()
            front = f"---\ntask: t-a\nhead: {head}\npr: 9\nbase: {base}\nstarted: .+\nfinished: .+\nfindings: 1\n"
            self.assertRegex(text, "^" + re.escape(front).replace(r"\.\+", ".+"))
            self.assertIn("engine: codex review --base main (profile review, read-only)\n---\n", text)
            self.assertIn(f"\n{finding}\n\n```text\nOne finding.\n{finding}\n{finding}\n```\n", text)
            self.assertNotIn("superseded", text)
            self.assertEqual([], list(self.temp.glob("local-review.*")))
        self.git("checkout", "-q", "--detach", "main", cwd=review)
        with self.subTest("CODEX_BIN set: that binary runs, a relative path resolved in the root"):
            self.stub(self.repo / "seam/review-binary", "seam")
            seam = {**env, "CODEX_BIN": "seam/review-binary"}
            self.run_tool("local-review.sh", "t-b", head, 9, code=3, env=seam, cwd=self.repo / ".orchestration")
            self.assertEqual(call, self.log("seam"))
            self.assertEqual(call, self.log("codex"))
        with self.subTest("one review per head: the file is reused"):
            stdout = self.run_tool("local-review.sh", "t-a", head, 9, code=3, env=env)
            self.assertEqual(f"{finding}\nlocal-review: 1 findings (existing {out('t-a')})\n", stdout)
            self.assertEqual(call, self.log("codex"))
        (self.calls / "transcript").write_text("codex\nNo findings.\n")
        (self.calls / "status").write_text("5")
        with self.subTest("no finding exits 0, also when the binary fails"):
            stdout = self.run_tool("local-review.sh", "t-c", head, 9, env=env)
            file = out("t-c")
            self.assertEqual(
                f"local-review: codex exited 5 (see {file})\n\nlocal-review: 0 findings ({file})\n", stdout
            )
            self.assertIn("findings: 0\n", out("t-c").read_text())
        missing = {**env, "CODEX_BIN": "seam/missing"}
        self.assertIn("no review binary", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=missing))
        self.write("dirty.txt", "x\n", root=review)
        with self.subTest("a dirty review worktree or an unknown head exits 2 and runs nothing"):
            self.assertIn("is not clean", self.run_tool("local-review.sh", "t-d", head, 9, code=2, env=env))
            unknown = "0" * 40
            self.assertIn("is not a local commit", self.run_tool("local-review.sh", "t-d", unknown, 9, code=2, env=env))
            self.assertEqual(2, self.log("codex").count(ARGV))
            self.assertFalse(out("t-d").exists())

    def test_local_advisory_records_p2_rows_and_stops_on_p0_p1(self):
        head, owner = "abcdef0" + "1" * 33, "t-followup-a01"
        record = self.write(".orchestration/acceptance/t-a01.md", "# record\n")
        heading = f"## Owned by {owner} (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n"
        # Numbered in sort order; the second is cut to 120 characters, then loses its backticks.
        first, long = "- [P2] `a.sh:1` first", "- [P2] `b.sh:3` " + "y" * 130

        def review(*findings):
            front = f"---\ntask: t-a01\nfindings: {len(findings)}\n---\n\n"
            # Each finding appears twice, in the list and in the transcript, as the local review writes it.
            text = "\n".join(findings)
            self.write(f".orchestration/validation/t-a01-local-review-{head[:7]}.md", f"{front}{text}\n\n{text}\n")

        def line(n, finding):
            text = finding[:120].replace("`", "")
            return (
                f"local-finding: abcdef0:{n} not-applicable:advisory P2 owned by {owner} ({text}); "
                f"evidence=git show origin/main:.orchestration/tasks/{owner}.md | grep -n 'item 1'\n"
            )

        review(long, first)
        for _ in range(2):
            stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner)
        self.assertEqual(
            f"local review of abcdef0: 2 finding(s) recorded as advisory under 'Owned by {owner}' in .orchestration/acceptance/t-a01.md\n",
            stdout,
        )
        rows = "local:abcdef0:1\tadvisory-p2\n" + line(1, first)
        rows += "local:abcdef0:2\tadvisory-p2\n" + line(2, long)
        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
        record.write_text("# record\n")
        review("- [P1] a.sh:1 blocks", "- [P2] b.sh:2 second")
        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P1] a.sh:1 blocks\n", stdout)
        rows = "local:abcdef0:2\tadvisory-p2\n" + line(2, "- [P2] b.sh:2 second")
        self.assertEqual(f"# record\n\n{heading}\n{rows}", record.read_text())
        record.write_text("# record\n")
        review("- [P0] c.sh:1 breaks")
        stdout = self.run_tool("local-advisory.sh", "t-a01", head, owner, code=3)
        self.assertIn("STOP: local finding 1 of abcdef0 is P0/P1: - [P0] c.sh:1 breaks\n", stdout)
        self.assertEqual(f"# record\n\n{heading}\n", record.read_text())
        record.write_text("# record\n")
        review()
        self.assertEqual(
            "local review of abcdef0: no findings\n", self.run_tool("local-advisory.sh", "t-a01", head, owner)
        )
        self.assertEqual("# record\n", record.read_text())
        self.assertIn("no local review file", self.run_tool("local-advisory.sh", "t-b01", head, owner, code=2))

    def test_sandbox_scan_prints_the_unsandboxed_mutation_calls(self):
        sandboxes = ".orchestration/sandboxes"
        hit = "| 2 | dangerouslyDisableSandbox: git commit -m wip |"
        self.write(
            f"{sandboxes}/t-a01.md", f"# sandbox\n{hit}\n- The unsandboxed table Counts every git commit > log.\n"
        )
        self.assertEqual(f"2:{hit}\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-a01"))
        # A trailing -fixtures is stripped, and the match ignores case.
        self.write(f"{sandboxes}/t-b01.md", "Outside The Sandbox: GIT ADD x\n")
        self.assertEqual(
            f"1:Outside The Sandbox: GIT ADD x\n{SCAN_HIT}\n", self.run_tool("sandbox-scan.sh", "t-b01-fixtures")
        )
        reads = (
            "| 1 | gh pr view 9 > pr.json (outside the sandbox; reads) |\n| 2 | unsandboxed tee log, lists the PRs |\n"
        )
        self.write(f"{sandboxes}/t-c01.md", reads)
        none = f"sandbox scan: no unsandboxed mutation call in {sandboxes}/t-c01.md\n"
        self.assertEqual(none, self.run_tool("sandbox-scan.sh", "t-c01"))
        self.assertEqual("", self.run_tool("sandbox-scan.sh", "t-d01"))


if __name__ == "__main__":
    unittest.main()
