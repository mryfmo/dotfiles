"""Exercise scripts/orchestrator/worktree-gc.sh in a scratch repository.

Each test builds a bare `origin` and a checkout under a temporary directory, with worktrees under
`.claude/worktrees/` in every state the lever tells apart. A fake `gh` written into the scratch PATH answers the two
`gh pr list --state merged` queries from a JSON table and records its argv; a `git` wrapper records every argv and
execs the real git, so the tests can assert that no git call carries `--force`. The real `gh` is never called and the
real worktrees of this repository are never read.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GC = ROOT / "scripts/orchestrator/worktree-gc.sh"

FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
argv = sys.argv[1:]
with open(os.environ["FAKE_GH_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(argv) + "\\n")
if os.environ.get("FAKE_GH_FAIL"):
    sys.exit("fake-gh: HTTP 502")
if argv[:4] != ["pr", "list", "--state", "merged"]:
    sys.exit(f"fake-gh: unexpected call {argv}")
table = json.load(open(os.environ["FAKE_GH_MERGED"], encoding="utf-8"))
flag, value = argv[4], argv[5]
print(json.dumps(table["head" if flag == "--head" else "search"].get(value, [])))
"""

GIT_WRAPPER = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAKE_GIT_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\\n")
os.execv(os.environ["REAL_GIT"], ["git", *sys.argv[1:]])
"""


class WorktreeGcTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        bindir = self.root / "bin"
        bindir.mkdir()
        for name, body in (("gh", FAKE_GH), ("git", GIT_WRAPPER)):
            (bindir / name).write_text(body)
            (bindir / name).chmod(0o755)
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = gc test\n\temail = gc@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.gh_calls = self.root / "gh-calls"
        self.git_calls = self.root / "git-calls"
        self.merged = self.root / "merged.json"
        self.env = {
            **os.environ,
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "REAL_GIT": shutil.which("git"),
            "GIT_CONFIG_GLOBAL": str(gitconfig),
            "GIT_CONFIG_NOSYSTEM": "1",
            "FAKE_GH_CALLS": str(self.gh_calls),
            "FAKE_GIT_CALLS": str(self.git_calls),
            "FAKE_GH_MERGED": str(self.merged),
        }
        self.checkout = self.root / "checkout"
        self.git("init", "--bare", str(self.root / "origin.git"), cwd=self.root)
        self.git("clone", str(self.root / "origin.git"), str(self.checkout), cwd=self.root)
        (self.checkout / "README").write_text("scratch\n")
        self.git("add", "README")
        self.git("commit", "-m", "initial")
        self.git("push", "origin", "main")
        self.trees = self.checkout / ".claude/worktrees"

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.checkout, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def add_tree(self, name, branch=None, commit=True):
        """Add `.claude/worktrees/<name>` from origin/main, on `branch` or detached, with one commit past main."""
        path = self.trees / name
        self.git("worktree", "add", *(["-b", branch] if branch else ["--detach"]), str(path), "origin/main")
        if commit:
            self.git("commit", "--allow-empty", "-m", name, cwd=path)
        return path, self.git("rev-parse", "HEAD", cwd=path)

    def build_states(self):
        """Every state the lever tells apart; returns the expected verdict per worktree name."""
        landed, _ = self.add_tree("landed-branch", "feat/landed")
        self.add_tree("in-main", "feat/in-main", commit=False)
        untracked, _ = self.add_tree("untracked", "feat/untracked")
        (untracked / "notes.txt").write_text("work in progress\n")
        modified, _ = self.add_tree("modified", "feat/modified")
        (modified / "README").write_text("edited\n")
        self.add_tree("open-pr", "feat/open")
        _, detached_sha = self.add_tree("detached-landed")
        _, other_sha = self.add_tree("detached-other")
        locked, _ = self.add_tree("locked", "feat/locked")
        self.git("worktree", "lock", str(locked))
        self.git("worktree", "add", "-b", "feat/outside", str(self.root / "outside"), "origin/main")
        self.merged.write_text(
            json.dumps(
                {
                    "head": {
                        branch: [{"number": number}]
                        for branch, number in (
                            ("feat/landed", 11),
                            ("feat/untracked", 12),
                            ("feat/modified", 13),
                            ("feat/locked", 14),
                        )
                    },
                    "search": {
                        detached_sha: [{"number": 7, "headRefOid": detached_sha}],
                        other_sha: [{"number": 8, "headRefOid": "0" * 40}],
                    },
                }
            )
        )
        self.assertTrue(landed.is_dir())
        return {
            "landed-branch": ("gc", "branch PR #11 merged"),
            "in-main": ("gc", "is in origin/main"),
            "untracked": ("keep", "dirty or untracked files"),
            "modified": ("keep", "dirty or untracked files"),
            "open-pr": ("keep", "no merged PR for the branch"),
            "detached-landed": ("gc", "detached at the head of merged PR #7"),
            "detached-other": ("keep", "detached at no merged PR head"),
            "locked": ("keep", "locked"),
        }

    def run_gc(self, *args, **overrides):
        return subprocess.run(
            [str(GC), *args],
            cwd=self.checkout,
            env={**self.env, **overrides},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def rows(self, stdout):
        return [line.split("\t") for line in stdout.splitlines()]

    def calls(self, path):
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def remaining(self):
        return sorted(path.name for path in self.trees.iterdir())

    def test_the_dry_run_prints_one_row_per_worktree_and_removes_nothing(self):
        expected = self.build_states()
        result = self.run_gc()
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        verdicts = {Path(row[1]).name: (row[0], row[3]) for row in rows if row[0] in ("gc", "keep")}
        self.assertEqual(set(verdicts), set(expected), "the outside worktree and the main checkout are not listed")
        for name, (verdict, reason) in expected.items():
            with self.subTest(worktree=name):
                self.assertEqual(verdicts[name][0], verdict)
                self.assertIn(reason, verdicts[name][1])
        self.assertEqual(rows[-1][0], "summary")
        self.assertIn("3 qualify, 5 kept; dry run", rows[-1][1])
        self.assertEqual(self.remaining(), sorted(expected))
        self.assertTrue((self.root / "outside").is_dir())
        removals = [argv for argv in self.calls(self.git_calls) if "remove" in argv or "prune" in argv]
        self.assertEqual(removals, [])

    def test_apply_removes_only_the_clean_landed_worktrees_and_never_forces(self):
        expected = self.build_states()
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        landed = sorted(name for name, (verdict, _) in expected.items() if verdict == "gc")
        self.assertEqual(landed, ["detached-landed", "in-main", "landed-branch"])
        self.assertEqual(self.remaining(), sorted(set(expected) - set(landed)))
        self.assertTrue((self.root / "outside").is_dir())
        removed = [row[1] for row in self.rows(result.stdout) if row[0] == "removed"]
        self.assertEqual(sorted(Path(path).name for path in removed), landed)
        self.assertIn(["pruned", "git worktree prune"], self.rows(result.stdout))
        git_calls = self.calls(self.git_calls)
        self.assertEqual(
            sorted(Path(argv[-1]).name for argv in git_calls if argv[-3:-1] == ["worktree", "remove"]), landed
        )
        self.assertIn(["-C", str(self.checkout), "worktree", "prune"], git_calls)
        for argv in git_calls:
            self.assertNotIn("--force", argv)
            if "remove" in argv:
                self.assertEqual(argv, ["-C", str(self.checkout), "worktree", "remove", argv[-1]])
        self.assertIn("feat/landed", self.git("branch", "--list", "feat/landed"), "the branch ref stays")

    def test_the_gh_queries_are_the_documented_ones(self):
        self.build_states()
        self.run_gc()
        gh_calls = self.calls(self.gh_calls)
        self.assertIn(
            ["pr", "list", "--state", "merged", "--head", "feat/landed", "--json", "number", "--limit", "1"], gh_calls
        )
        detached = self.git("rev-parse", "HEAD", cwd=self.trees / "detached-landed")
        self.assertIn(
            ["pr", "list", "--state", "merged", "--search", detached, "--json", "number,headRefOid"], gh_calls
        )
        queried = {argv[5] for argv in gh_calls}
        self.assertNotIn("feat/in-main", queried, "a head already in origin/main needs no gh call")
        self.assertNotIn("feat/untracked", queried, "a dirty tree is kept before gh is asked")

    def test_a_gh_failure_removes_nothing_and_exits_1(self):
        expected = self.build_states()
        result = self.run_gc("--apply", FAKE_GH_FAIL="1")
        self.assertEqual(result.returncode, 1, result.stdout)
        rows = self.rows(result.stdout)
        self.assertIn("error", [row[0] for row in rows])
        self.assertIn("nothing removed", rows[-1][1])
        self.assertEqual(self.remaining(), sorted(expected))
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv], [])

    def test_a_path_outside_claude_worktrees_is_refused(self):
        expected = self.build_states()
        for path in (self.root / "outside", self.checkout, Path("/tmp")):
            with self.subTest(path=path):
                result = self.run_gc("--apply", str(path))
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("refused", result.stderr)
                self.assertEqual(result.stdout, "")
        self.assertTrue((self.root / "outside").is_dir())
        self.assertEqual(self.remaining(), sorted(expected))

    def test_a_path_argument_narrows_the_run_to_that_worktree(self):
        self.build_states()
        result = self.run_gc("--apply", str(self.trees / "in-main"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "removed", "pruned", "summary"])
        self.assertNotIn("in-main", self.remaining())
        self.assertIn("landed-branch", self.remaining())

    def test_nothing_to_collect_exits_0(self):
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.rows(result.stdout), [["pruned", "git worktree prune"], ["summary", "0 removed, 0 failed, 0 kept"]]
        )
        self.assertEqual(self.calls(self.gh_calls), [])


if __name__ == "__main__":
    unittest.main()
