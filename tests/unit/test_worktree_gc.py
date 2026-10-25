"""Exercise scripts/orchestrator/worktree-gc.sh in a scratch repository.

Each test builds a bare `origin` and a checkout under a temporary directory, with worktrees under
`.claude/worktrees/` in every state the lever tells apart. A fake `gh` written into the scratch PATH answers the two
`gh pr list --state merged` queries from a JSON table and records its argv; a `git` wrapper records every argv and
execs the real git, so the tests can assert that no git call carries `--force` or runs `git worktree prune`. The real `gh` is never called and the
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
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in " ".join(sys.argv[1:]):
    sys.exit("fake-git: failing as asked")
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
        """Add `.claude/worktrees/<name>` from origin/main, on `branch` or detached, with one commit past main.

        The commit adds `<name>.txt`, so its content is not in main either.
        """
        path = self.trees / name
        self.git("worktree", "add", *(["-b", branch] if branch else ["--detach"]), str(path), "origin/main")
        if commit:
            self.commit_file(path, f"{name}.txt", f"{name}\n")
        return path, self.git("rev-parse", "HEAD", cwd=path)

    def commit_file(self, cwd, name, content, message=None):
        (cwd / name).write_text(content)
        self.git("add", name, cwd=cwd)
        self.git("commit", "-m", message or name, cwd=cwd)

    def land_on_main(self, name, content):
        """Commit `name` on main and push it, as a squash merge of a branch that added the same file would.

        The message differs from the branch's, so within the same second the commit is not the branch head itself.
        """
        self.commit_file(self.checkout, name, content, message=f"squash: {name}")
        self.git("push", "origin", "main")

    def build_states(self):
        """Every state the lever tells apart; returns the expected verdict per worktree name."""
        landed, landed_sha = self.add_tree("landed-branch", "feat/landed")
        self.add_tree("in-main", "feat/in-main", commit=False)
        untracked, _ = self.add_tree("untracked", "feat/untracked")
        (untracked / "notes.txt").write_text("work in progress\n")
        modified, _ = self.add_tree("modified", "feat/modified")
        (modified / "README").write_text("edited\n")
        self.add_tree("open-pr", "feat/open")
        self.add_tree("reused-name", "feat/reused")
        _, detached_sha = self.add_tree("detached-landed")
        _, other_sha = self.add_tree("detached-other")
        locked, _ = self.add_tree("locked", "feat/locked")
        self.git("worktree", "lock", str(locked))
        self.git("worktree", "add", "-b", "feat/outside", str(self.root / "outside"), "origin/main")
        self.merged.write_text(
            json.dumps(
                {
                    "head": {
                        "feat/landed": [{"number": 11, "headRefOid": landed_sha}],
                        "feat/untracked": [{"number": 12, "headRefOid": "1" * 40}],
                        "feat/modified": [{"number": 13, "headRefOid": "2" * 40}],
                        "feat/locked": [{"number": 14, "headRefOid": "3" * 40}],
                        # A merged PR with this branch name (another fork's, or the head before later commits).
                        "feat/reused": [{"number": 15, "headRefOid": "4" * 40}],
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
            "landed-branch": ("gc", "is the head of merged PR #11"),
            "in-main": ("gc", "is in origin/main"),
            "untracked": ("keep", "dirty or untracked files"),
            "modified": ("keep", "dirty or untracked files"),
            "open-pr": ("keep", "neither in origin/main nor the head of a merged PR"),
            "reused-name": ("keep", "neither in origin/main nor the head of a merged PR"),
            "detached-landed": ("gc", "is the head of merged PR #7"),
            "detached-other": ("keep", "neither in origin/main nor the head of a merged PR"),
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
        self.assertIn("3 qualify, 6 kept; dry run", rows[-1][1])
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
        git_calls = self.calls(self.git_calls)
        self.assertEqual(
            sorted(Path(argv[-1]).name for argv in git_calls if argv[-3:-1] == ["worktree", "remove"]), landed
        )
        for argv in git_calls:
            self.assertNotIn("--force", argv)
            self.assertNotIn("prune", argv)
            if "remove" in argv:
                self.assertEqual(argv, ["-C", str(self.checkout), "worktree", "remove", argv[-1]])
        self.assertIn("feat/landed", self.git("branch", "--list", "feat/landed"), "the branch ref stays")

    def test_the_gh_queries_are_the_documented_ones(self):
        self.build_states()
        self.run_gc()
        gh_calls = self.calls(self.gh_calls)
        self.assertIn(
            [
                "pr",
                "list",
                "--state",
                "merged",
                "--head",
                "feat/landed",
                "--json",
                "number,headRefOid",
                "--limit",
                "100",
            ],
            gh_calls,
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

    def test_a_newline_in_a_path_cannot_forge_a_landed_record(self):
        """A path `a<LF>worktree <victim>` must not lend its landed head to the victim (audit row 679, U16c)."""
        victim, victim_head = self.add_tree("victim")
        forged = self.trees / f"a\nworktree {victim}"
        self.git("worktree", "add", "--detach", str(forged), "origin/main")
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 1, result.stdout)
        rows = self.rows(result.stdout)
        self.assertIn(["error", str(forged).replace("\n", "\\n")], [row[:2] for row in rows])
        self.assertIn("path contains a newline", {row[3] for row in rows if row[0] == "error"})
        victim_rows = [row for row in rows if row[1] == str(victim)]
        self.assertEqual([row[0] for row in victim_rows], ["keep"], "the victim is listed once, from its own record")
        self.assertIn("nothing removed", rows[-1][1])
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=victim), victim_head)
        self.assertTrue(forged.is_dir())
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv or "prune" in argv], [])

    def test_a_failing_worktree_listing_exits_1_and_removes_nothing(self):
        expected = self.build_states()
        result = self.run_gc("--apply", FAKE_GIT_FAIL="worktree list")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("git worktree list failed", result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.remaining(), sorted(expected))

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
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "removed", "summary"])
        self.assertNotIn("in-main", self.remaining())
        self.assertIn("landed-branch", self.remaining())

    def test_nothing_to_collect_exits_0(self):
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows(result.stdout), [["summary", "0 removed, 0 failed, 0 kept"]])
        self.assertEqual(self.calls(self.gh_calls), [])

    def test_an_ignored_file_keeps_the_tree(self):
        """`git worktree remove` deletes ignored files with exit 0, so a tree holding an ignored `.env` is kept."""
        self.land_on_main(".gitignore", ".env\n")
        path, _ = self.add_tree("with-env", "feat/with-env", commit=False)
        (path / ".env").write_text("TOKEN=secret\n")
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual(rows[0][:2], ["keep", str(path)])
        self.assertIn("ignored files", rows[0][3])
        self.assertEqual(rows[-1], ["summary", "0 removed, 0 failed, 1 kept"])
        self.assertEqual((path / ".env").read_text(), "TOKEN=secret\n")

    def test_a_squash_merged_branch_is_landed_until_it_gets_a_later_commit(self):
        path, _ = self.add_tree("squashed", "feat/squashed")
        self.land_on_main("squashed.txt", "squashed\n")
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        result = self.run_gc()
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self.rows(result.stdout)[0]
        self.assertEqual(row[0], "gc", row)
        self.assertIn("into origin/main changes nothing", row[3])
        self.assertEqual(self.calls(self.gh_calls), [], "content already in main needs no gh call")

        self.commit_file(path, "later.txt", "after the squash\n")
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self.rows(result.stdout)[0]
        self.assertEqual(row[0], "keep", row)
        self.assertIn("neither in origin/main nor the head of a merged PR", row[3])
        self.assertTrue((path / "later.txt").is_file())

    def test_a_merged_pr_with_the_branch_name_but_another_head_does_not_land_the_tree(self):
        path, head = self.add_tree("same-name", "feat/same-name")
        self.merged.write_text(json.dumps({"head": {"feat/same-name": [{"number": 21, "headRefOid": "5" * 40}]}}))
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows(result.stdout)[0][0], "keep")
        self.assertTrue(path.is_dir())

        self.merged.write_text(json.dumps({"head": {"feat/same-name": [{"number": 21, "headRefOid": head}]}}))
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "removed", "summary"])
        self.assertFalse(path.exists())

    def test_the_admin_data_of_a_sibling_worktree_whose_directory_is_missing_survives(self):
        """An unlocked seat worktree outside `.claude/worktrees/` whose directory is gone keeps its admin data."""
        seat = self.root / "seat"
        self.git("worktree", "add", "-b", "seat", str(seat), "origin/main")
        shutil.rmtree(seat)
        self.add_tree("in-main", "feat/in-main", commit=False)
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "removed", "summary"])
        listing = self.git("worktree", "list", "--porcelain")
        self.assertIn(f"worktree {seat}", listing)


if __name__ == "__main__":
    unittest.main()
