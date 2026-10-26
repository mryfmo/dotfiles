"""Exercise scripts/orchestrator/worktree-gc.sh in a scratch repository.

Each test builds a bare `origin` and a checkout under a temporary directory, with worktrees under
`.claude/worktrees/` in every state the lever tells apart. A fake `gh` written into the scratch PATH answers the two
`gh pr list --state merged` queries from a JSON table and records its argv; a `git` wrapper records every argv and
execs the real git, so the tests can assert that no git call carries `--force` or runs `git worktree prune`, and that
`--apply` only moves trees into `.claude/worktrees/.gc-quarantine/` while `--purge` alone removes. The real `gh` is
never called and the real worktrees of this repository are never read.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git  # noqa: E402

quiet_git()  # U100: no git command in this module's scratch repositories starts background maintenance

ROOT = Path(__file__).resolve().parents[2]
GC = ROOT / "scripts/orchestrator/worktree-gc.sh"

FAKE_GH = """#!/usr/bin/env python3
import json, os, subprocess, sys
argv = sys.argv[1:]
with open(os.environ["FAKE_GH_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(argv) + "\\n")
if os.environ.get("FAKE_GH_FAIL"):
    sys.exit("fake-gh: HTTP 502")
if argv[:4] != ["pr", "list", "--state", "merged"]:
    sys.exit(f"fake-gh: unexpected call {argv}")
if os.environ.get("FAKE_GH_TOUCH"):
    # A file written into a worktree while the lever waits on gh, after that tree's clean check.
    with open(os.environ["FAKE_GH_TOUCH"], "w", encoding="utf-8") as late:
        late.write("TOKEN=late\\n")
if os.environ.get("FAKE_GH_COMMIT"):
    # A commit made in a worktree while the lever waits on gh, after that tree's head was read.
    subprocess.run(["git", "-C", os.environ["FAKE_GH_COMMIT"], "commit", "-q", "--allow-empty", "-m", "late"], check=True)
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
        git_init(self.root / "origin.git", "--bare", env=self.env)
        git_clone(self.root / "origin.git", self.checkout, env=self.env)
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
        return sorted(path.name for path in self.trees.iterdir() if path.name != ".gc-quarantine")

    def quarantined(self):
        """The quarantined trees by name, each in its own `.gc-quarantine/<random>/` directory."""
        return sorted(path.name for path in (self.trees / ".gc-quarantine").glob("*/*"))

    def marker(self, path):
        return Path(self.git("rev-parse", "--absolute-git-dir", cwd=path)) / "gc-quarantined-at"

    def apply_one(self, name, **overrides):
        """`--apply` on a tree landed in origin/main; returns its quarantine path and the run's rows."""
        path, _ = self.add_tree(name, f"feat/{name}", commit=False)
        result = self.run_gc("--apply", **overrides)
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        moved = [row for row in rows if row[0] == "quarantined"]
        self.assertEqual([row[1] for row in moved], [str(path)], rows)
        return Path(moved[0][2]), rows

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
        self.assertIn("3 qualify, 6 kept, 0 in quarantine; dry run", rows[-1][1])
        self.assertEqual(self.remaining(), sorted(expected))
        self.assertTrue((self.root / "outside").is_dir())
        removals = [argv for argv in self.calls(self.git_calls) if "remove" in argv or "prune" in argv]
        self.assertEqual(removals, [])

    def test_apply_quarantines_only_the_clean_landed_worktrees_and_deletes_nothing(self):
        expected = self.build_states()
        files = {name: sorted(p.name for p in (self.trees / name).iterdir()) for name in expected}
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        landed = sorted(name for name, (verdict, _) in expected.items() if verdict == "gc")
        self.assertEqual(landed, ["detached-landed", "in-main", "landed-branch"])
        self.assertEqual(self.remaining(), sorted(set(expected) - set(landed)))
        self.assertEqual(self.quarantined(), landed)
        self.assertTrue((self.root / "outside").is_dir())
        rows = self.rows(result.stdout)
        moved = {Path(row[1]).name: Path(row[2]) for row in rows if row[0] == "quarantined"}
        self.assertEqual(sorted(moved), landed)
        self.assertEqual(rows[-1], ["summary", "3 quarantined, 0 held, 0 failed, 6 kept"])
        for name, dest in moved.items():
            with self.subTest(worktree=name):
                self.assertEqual(dest.parent.parent, self.trees / ".gc-quarantine")
                self.assertEqual(sorted(p.name for p in dest.iterdir()), files[name], "the tree moved whole")
                stamp, head = self.marker(dest).read_text().split()
                self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=dest))
                self.assertTrue(stamp.isdigit())
        git_calls = self.calls(self.git_calls)
        self.assertEqual(sorted(Path(argv[-2]).name for argv in git_calls if argv[2:4] == ["worktree", "move"]), landed)
        for argv in git_calls:
            self.assertNotIn("--force", argv)
            self.assertNotIn("prune", argv)
            self.assertNotIn("remove", argv, "--apply deletes nothing")
            if "move" in argv:
                self.assertEqual(argv[:4], ["-C", str(self.checkout), "worktree", "move"])
                self.assertEqual(len(argv), 6)
        self.assertIn("feat/landed", self.git("branch", "--list", "feat/landed"), "the branch ref stays")
        self.assertTrue((self.trees / "locked").is_dir(), "a locked tree is not moved")

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
        self.assertIn("nothing moved", rows[-1][1])
        self.assertEqual(self.remaining(), sorted(expected))
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv or "move" in argv], [])

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
        self.assertIn("nothing moved", rows[-1][1])
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
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "quarantined", "summary"])
        self.assertNotIn("in-main", self.remaining())
        self.assertIn("landed-branch", self.remaining())

    def test_nothing_to_collect_exits_0(self):
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows(result.stdout), [["summary", "0 quarantined, 0 held, 0 failed, 0 kept"]])
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
        self.assertEqual(rows[-1], ["summary", "0 quarantined, 0 held, 0 failed, 1 kept"])
        self.assertEqual((path / ".env").read_text(), "TOKEN=secret\n")

    def test_a_squash_merged_branch_is_landed_until_it_gets_a_later_commit(self):
        path, _ = self.add_tree("squashed", "feat/squashed")
        self.land_on_main("squashed.txt", "squashed\n")
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        result = self.run_gc()
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self.rows(result.stdout)[0]
        self.assertEqual(row[0], "gc", row)
        self.assertIn("changed holds the same entry in origin/main", row[3])
        self.assertEqual(self.calls(self.gh_calls), [], "content already in main needs no gh call")

        self.commit_file(path, "later.txt", "after the squash\n")
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        row = self.rows(result.stdout)[0]
        self.assertEqual(row[0], "keep", row)
        self.assertIn("neither in origin/main nor the head of a merged PR", row[3])
        self.assertTrue((path / "later.txt").is_file())

    def keep_ours_conflict(self, name):
        """A branch and main both change README; returns the tree path once main's change is pushed."""
        path, _ = self.add_tree(name, f"feat/{name}", commit=False)
        self.commit_file(path, "README", "branch work\n")
        self.land_on_main("README", "main work\n")
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        return path

    def assert_kept_although_a_merge_would_change_nothing(self, path):
        head = self.git("rev-parse", "HEAD", cwd=path)
        merged = self.git("merge-tree", "--write-tree", "origin/main", head).splitlines()[0]
        self.assertEqual(merged, self.git("rev-parse", "origin/main^{tree}"), "the driver hides the conflict")
        self.git_calls.unlink()
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual(rows[0][:2], ["keep", str(path)], rows)
        self.assertIn("neither in origin/main nor the head of a merged PR", rows[0][3])
        self.assertEqual((path / "README").read_text(), "branch work\n")
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "merge-tree" in argv], [], "no merge runs")

    def test_a_keep_ours_merge_default_does_not_land_a_conflicting_change(self):
        """`merge.default=ours` with a no-op driver resolves the conflict to main's tree with exit 0 (U56b F1)."""
        self.git("config", "merge.default", "ours")
        self.git("config", "merge.ours.driver", "true")
        self.assert_kept_although_a_merge_would_change_nothing(self.keep_ours_conflict("keep-ours-config"))

    def test_a_keep_ours_merge_attribute_does_not_land_a_conflicting_change(self):
        self.git("config", "merge.ours.driver", "true")
        attributes = self.checkout / ".git/info/attributes"
        attributes.parent.mkdir(exist_ok=True)
        attributes.write_text("* merge=ours\n")
        self.assert_kept_although_a_merge_would_change_nothing(self.keep_ours_conflict("keep-ours-attribute"))

    def test_a_rename_and_a_deletion_land_only_once_main_holds_both(self):
        self.land_on_main("old.txt", "old\n")
        self.land_on_main("gone.txt", "gone\n")
        path, _ = self.add_tree("moved", "feat/moved", commit=False)
        self.git("mv", "old.txt", "new.txt", cwd=path)
        self.git("rm", "-q", "gone.txt", cwd=path)
        self.git("commit", "-m", "move and delete", cwd=path)
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        verdicts = []
        for step in ("unlanded", "deletion only", "rename too"):
            if step == "deletion only":
                self.git("rm", "-q", "gone.txt")
                self.git("commit", "-m", "squash: delete")
                self.git("push", "origin", "main")
            elif step == "rename too":
                self.git("mv", "old.txt", "new.txt")
                self.git("commit", "-m", "squash: move")
                self.git("push", "origin", "main")
            result = self.run_gc()
            self.assertEqual(result.returncode, 0, result.stderr)
            verdicts.append(self.rows(result.stdout)[0][0])
        self.assertEqual(verdicts, ["keep", "keep", "gc"])
        result = self.run_gc("--apply")
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "quarantined", "summary"])
        self.assertFalse(path.exists())

    def test_a_mode_change_alone_is_not_landed_by_the_same_blob(self):
        path, _ = self.add_tree("mode", "feat/mode", commit=False)
        (path / "README").chmod(0o755)
        self.git("commit", "-am", "make README executable", cwd=path)
        self.merged.write_text(json.dumps({"head": {}, "search": {}}))
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows(result.stdout)[0][0], "keep")
        self.assertTrue(path.is_dir())

    def test_a_content_comparison_failure_is_an_error_and_removes_nothing(self):
        path, _ = self.add_tree("squashed", "feat/squashed")
        self.land_on_main("squashed.txt", "squashed\n")
        result = self.run_gc("--apply", FAKE_GIT_FAIL="ls-tree")
        self.assertEqual(result.returncode, 1, result.stdout)
        rows = self.rows(result.stdout)
        self.assertEqual(rows[0][0], "error", rows)
        self.assertIn("with origin/main failed", rows[0][3])
        self.assertIn("nothing moved", rows[-1][1])
        self.assertTrue(path.is_dir())

    def test_an_ignored_file_written_after_the_check_is_held_in_quarantine(self):
        """The tree is moved, then checked again (U56c); gh writes `.env` mid-run, so it is held with the file."""
        self.land_on_main(".gitignore", ".env\n")
        path, head = self.add_tree("late-env", "feat/late-env")
        self.merged.write_text(json.dumps({"head": {"feat/late-env": [{"number": 31, "headRefOid": head}]}}))
        result = self.run_gc("--apply", FAKE_GH_TOUCH=str(path / ".env"))
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual([row[0] for row in rows], ["gc", "held", "summary"], rows)
        self.assertEqual(rows[1][:2], ["held", str(path)])
        self.assertIn("ignored files", rows[1][3])
        self.assertEqual(rows[-1], ["summary", "0 quarantined, 1 held, 0 failed, 0 kept"])
        held = Path(rows[1][2])
        self.assertEqual((held / ".env").read_text(), "TOKEN=late\n")
        self.assertFalse(path.exists(), "a held tree is never moved back")
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv], [])

    def test_a_commit_made_after_the_check_is_held_in_quarantine(self):
        """A detached tree whose head moves after its classification (U56c F1) is held with its new commit."""
        path, head = self.add_tree("late-commit")
        self.merged.write_text(json.dumps({"head": {}, "search": {head: [{"number": 41, "headRefOid": head}]}}))
        result = self.run_gc("--apply", FAKE_GH_COMMIT=str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual([row[0] for row in rows], ["gc", "held", "summary"], rows)
        self.assertIn(f"head moved from {head[:12]}", rows[1][3])
        held = Path(rows[1][2])
        new_head = self.git("rev-parse", "HEAD", cwd=held)
        self.assertNotEqual(new_head, head)
        self.assertEqual(self.git("log", "-1", "--format=%s", new_head, cwd=held), "late")
        self.assertEqual(self.git("rev-parse", "HEAD^", cwd=held), head)
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv], [])

    def test_purge_removes_a_quarantined_tree_that_still_qualifies(self):
        dest, _ = self.apply_one("done")
        result = self.run_gc("--purge", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual(rows[0][0], "keep", rows)
        self.assertIn("younger than 1 days", rows[0][3])
        self.assertTrue(dest.is_dir())

        result = self.run_gc("--purge", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual([row[0] for row in rows], ["gc", "removed", "summary"], rows)
        self.assertEqual(rows[1], ["removed", str(dest)])
        self.assertEqual(rows[-1], ["summary", "1 removed, 0 failed, 0 kept"])
        self.assertFalse(dest.exists())
        self.assertFalse(dest.parent.exists(), "the empty quarantine slot goes too")
        self.assertIn("feat/done", self.git("branch", "--list", "feat/done"), "the branch ref stays")
        removals = [argv for argv in self.calls(self.git_calls) if "remove" in argv]
        self.assertEqual(removals, [["-C", str(self.checkout), "worktree", "remove", str(dest)]])

    def test_purge_keeps_a_quarantined_tree_that_gained_an_ignored_file(self):
        self.land_on_main(".gitignore", ".env\n")
        dest, _ = self.apply_one("gained-env")
        (dest / ".env").write_text("TOKEN=written-in-quarantine\n")
        result = self.run_gc("--purge", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual(rows[0][:2], ["keep", str(dest)], rows)
        self.assertIn("ignored files", rows[0][3])
        self.assertEqual(rows[-1], ["summary", "0 removed, 0 failed, 1 kept"])
        self.assertEqual((dest / ".env").read_text(), "TOKEN=written-in-quarantine\n")
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv], [])

    def test_purge_keeps_a_locked_or_unmarked_quarantined_tree(self):
        dest, _ = self.apply_one("locked-later")
        self.git("worktree", "lock", str(dest))
        other, _ = self.apply_one("unmarked")
        self.marker(other).unlink()
        result = self.run_gc("--purge", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        reasons = {Path(row[1]).name: (row[0], row[3]) for row in self.rows(result.stdout) if row[0] != "summary"}
        self.assertEqual(reasons["locked-later"], ("keep", "locked"))
        self.assertEqual(reasons["unmarked"][0], "keep")
        self.assertIn("no gc-quarantined-at marker", reasons["unmarked"][1])
        self.assertTrue(dest.is_dir() and other.is_dir())
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv], [])

    def test_a_symlink_planted_at_the_marker_name_is_replaced_not_written_through(self):
        """`--apply` renames a fresh file onto `gc-quarantined-at` (U56d F1), so the link's target is untouched."""
        path, _ = self.add_tree("linked", "feat/linked", commit=False)
        outside = self.root / "victim.txt"
        outside.write_text("precious\n")
        link = self.marker(path)
        link.symlink_to(outside)
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual([row[0] for row in rows], ["gc", "quarantined", "summary"], rows)
        self.assertEqual(outside.read_text(), "precious\n")
        marker = self.marker(Path(rows[1][2]))
        self.assertFalse(marker.is_symlink())
        self.assertRegex(marker.read_text(), r"^[0-9]+ [0-9a-f]{40}\n$")
        self.assertEqual(sorted(p.name for p in marker.parent.glob("gc-quarantined-at*")), ["gc-quarantined-at"])

    def test_a_symlink_at_the_marker_name_to_a_directory_holds_the_tree(self):
        path, _ = self.add_tree("dir-linked", "feat/dir-linked", commit=False)
        outside = self.root / "victim-dir"
        outside.mkdir()
        self.marker(path).symlink_to(outside)
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual([row[0] for row in rows], ["gc", "held", "summary"], rows)
        self.assertIn("cannot write gc-quarantined-at", rows[1][3])
        self.assertEqual(list(outside.iterdir()), [])

    def test_an_edit_hidden_by_an_index_flag_keeps_the_tree_through_apply_and_purge(self):
        """`assume-unchanged` and `skip-worktree` hide an edit from `git status` (U56d F2); the tree is kept."""
        flags = ("--assume-unchanged", "--skip-worktree")
        hidden = {}
        for flag in flags:
            path, _ = self.add_tree(flag.strip("-"), f"feat/{flag.strip('-')}", commit=False)
            (path / "README").write_text("hidden edit\n")
            self.git("update-index", flag, "README", cwd=path)
            self.assertEqual(self.git("status", "--porcelain", "--ignored", cwd=path), "")
            hidden[str(path)] = path
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual(sorted(row[1] for row in rows if row[0] == "keep"), sorted(hidden), rows)
        for row in rows[:-1]:
            self.assertIn("assume-unchanged or skip-worktree", row[3])
        self.assertEqual(rows[-1], ["summary", "0 quarantined, 0 held, 0 failed, 2 kept"])
        for path in hidden.values():
            self.assertEqual((path / "README").read_text(), "hidden edit\n")

        quarantined = {}
        for flag in flags:
            dest, _ = self.apply_one(f"{flag.strip('-')}-later")
            (dest / "README").write_text("hidden in quarantine\n")
            self.git("update-index", flag, "README", cwd=dest)
            quarantined[str(dest)] = dest
        result = self.run_gc("--purge", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual(sorted(row[1] for row in rows if row[0] == "keep"), sorted(quarantined), rows)
        for row in rows[:-1]:
            self.assertIn("assume-unchanged or skip-worktree", row[3])
        self.assertEqual(rows[-1], ["summary", "0 removed, 0 failed, 2 kept"])
        for dest in quarantined.values():
            self.assertEqual((dest / "README").read_text(), "hidden in quarantine\n")
        self.assertEqual([argv for argv in self.calls(self.git_calls) if "remove" in argv], [])

    def test_the_quarantine_is_never_a_candidate(self):
        dest, _ = self.apply_one("parked")
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows(result.stdout)
        self.assertEqual([row[0] for row in rows], ["quarantine", "summary"], rows)
        self.assertEqual(rows[0][1], str(dest))
        self.assertRegex(rows[0][3], r"^quarantined 0d 0h ago$")
        self.assertEqual(rows[-1], ["summary", "0 quarantined, 0 held, 0 failed, 0 kept"])
        self.assertEqual(self.quarantined(), ["parked"])
        result = self.run_gc()
        self.assertEqual(
            self.rows(result.stdout)[-1][1],
            "0 qualify, 0 kept, 1 in quarantine; dry run, rerun with --apply to quarantine",
        )
        for path in (dest, dest.parent, self.trees / ".gc-quarantine"):
            with self.subTest(path=path):
                result = self.run_gc("--apply", str(path))
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("in the quarantine", result.stderr)
        self.assertTrue(dest.is_dir())

    def test_purge_takes_a_day_count_and_nothing_else(self):
        for args in (
            ["--purge"],
            ["--purge", "x"],
            ["--purge", "-1"],
            ["--purge", "1", "--apply"],
            ["--purge", "1", str(self.trees)],
        ):
            with self.subTest(args=args):
                result = self.run_gc(*args)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertIn("usage", result.stderr)

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
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "quarantined", "summary"])
        self.assertFalse(path.exists())

    def test_the_admin_data_of_a_sibling_worktree_whose_directory_is_missing_survives(self):
        """An unlocked seat worktree outside `.claude/worktrees/` whose directory is gone keeps its admin data."""
        seat = self.root / "seat"
        self.git("worktree", "add", "-b", "seat", str(seat), "origin/main")
        shutil.rmtree(seat)
        self.add_tree("in-main", "feat/in-main", commit=False)
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row[0] for row in self.rows(result.stdout)], ["gc", "quarantined", "summary"])
        listing = self.git("worktree", "list", "--porcelain")
        self.assertIn(f"worktree {seat}", listing)


if __name__ == "__main__":
    unittest.main()
