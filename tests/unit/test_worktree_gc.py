"""Exercise scripts/orchestrator/worktree-gc.sh in a scratch repository with a fake `gh`.

The repository, its `origin` and every worktree live under a temporary directory; `gh` is
tests/fixtures/worktree-gc/fake-tool.py answering from `FAKE_GH_MERGED`, and `git` is the same fake logging argv
before it runs the real git. Nothing reads the real checkout's worktrees or GitHub.
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
TREES = ("landed", "dirty", "open", "past", "locked", "detached", "atmain")
FAKE = ROOT / "tests/fixtures/worktree-gc/fake-tool.py"
GIT_IDENTITY = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
}


class WorktreeGcTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        bindir = root / "bin"
        bindir.mkdir()
        for tool in ("gh", "git"):
            (bindir / tool).symlink_to(FAKE)
        self.calls = root / "calls"
        self.calls.mkdir()
        self.repo = root / "repo"
        self.repo.mkdir()
        self.trees = self.repo / ".claude/worktrees"
        self.env = {
            **os.environ,
            **GIT_IDENTITY,
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "FAKE_CALLS": str(self.calls),
            "FAKE_REAL_GIT": shutil.which("git"),
        }
        self.git("init", "-q", "-b", "main")
        (self.repo / ".gitignore").write_text("/.claude/worktrees/\n")
        self.git("add", ".gitignore")
        self.git("commit", "-q", "-m", "init")
        self.git("init", "-q", "--bare", str(root / "origin"))
        self.git("remote", "add", "origin", str(root / "origin"))
        self.git("push", "-q", "origin", "main")
        self.heads = {}
        for name in ("landed", "dirty", "open", "past", "locked"):
            self.git("worktree", "add", "-q", "-b", f"feat/{name}", str(self.trees / name), "main")
            self.heads[name] = self.commit(name, "work")
        self.heads["past-merged"] = self.heads["past"]
        self.heads["past"] = self.commit("past", "more")
        (self.trees / "dirty" / "untracked.txt").write_text("not committed\n")
        self.git("worktree", "lock", str(self.trees / "locked"))
        self.git("worktree", "add", "-q", "--detach", str(self.trees / "detached"), "main")
        self.heads["detached"] = self.commit("detached", "work")
        self.git("worktree", "add", "-q", "--detach", str(self.trees / "atmain"), "main")
        self.git("worktree", "add", "-q", "--detach", str(root / "elsewhere"), "main")
        self.env["FAKE_GH_MERGED"] = ",".join(
            (
                f"11:feat/landed:{self.heads['landed']}",
                f"12:feat/dirty:{self.heads['dirty']}",
                f"13::{self.heads['detached']}",
                f"14:feat/past:{self.heads['past-merged']}",
            )
        )
        for tool in ("gh", "git"):
            (self.calls / tool).unlink(missing_ok=True)

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.repo, env=self.env, capture_output=True, text=True, check=True
        ).stdout.strip()

    def commit(self, tree, name):
        (self.trees / tree / f"{name}.txt").write_text(f"{name}\n")
        self.git("add", f"{name}.txt", cwd=self.trees / tree)
        self.git("commit", "-q", "-m", name, cwd=self.trees / tree)
        return self.git("rev-parse", "HEAD", cwd=self.trees / tree)

    def gc(self, *args, cwd=None, **overrides):
        return subprocess.run(
            [str(GC), *args],
            cwd=cwd or self.repo,
            env={**self.env, **overrides},
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )

    def calls_of(self, tool):
        path = self.calls / tool
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def rows(self, run):
        self.assertEqual(run.returncode, 0, run.stderr)
        return sorted(line.split("\t") for line in run.stdout.splitlines())

    def expected_rows(self):
        short = {name: f"detached@{sha[:12]}" for name, sha in self.heads.items()}
        main = f"detached@{self.git('rev-parse', 'origin/main')[:12]}"
        return sorted(
            [
                ["keep", str(self.trees / "dirty"), "feat/dirty", "dirty"],
                ["keep", str(self.trees / "locked"), "feat/locked", "locked"],
                ["keep", str(self.trees / "open"), "feat/open", "not-landed"],
                ["keep", str(self.trees / "past"), "feat/past", "not-landed"],
                ["remove", str(self.trees / "atmain"), main, "reachable-from-origin/main"],
                ["remove", str(self.trees / "detached"), short["detached"], "pr-merged #13"],
                ["remove", str(self.trees / "landed"), "feat/landed", "pr-merged #11"],
            ]
        )

    def test_the_dry_run_judges_each_tree_in_order_and_removes_nothing(self):
        self.assertEqual(self.rows(self.gc()), self.expected_rows())
        self.assertEqual(self.rows(self.gc("--dry-run", cwd=self.trees / "open")), self.expected_rows())
        self.assertTrue(all((self.trees / name).is_dir() for name in TREES))
        self.assertFalse(
            [argv for argv in self.calls_of("git") if argv[:2] in (["worktree", "remove"], ["worktree", "prune"])]
        )
        queried = [argv[6:] for argv in self.calls_of("gh")]
        self.assertNotIn(["--head", "feat/dirty"], queried, "the dirty check runs before any gh call")
        self.assertNotIn(["--head", "feat/locked"], queried)
        self.assertEqual(
            sorted(map(tuple, set(map(tuple, queried)))),
            sorted(
                [
                    ("--head", "feat/landed"),
                    ("--head", "feat/open"),
                    ("--head", "feat/past"),
                    ("--search", self.heads["detached"]),
                ]
            ),
        )

    def test_apply_removes_the_landed_trees_without_force_and_is_idempotent(self):
        applied = self.gc("--apply")
        self.assertEqual(applied.returncode, 0, applied.stderr)
        removed = [line.split("\t")[1] for line in applied.stdout.splitlines() if line.startswith("removed\t")]
        self.assertEqual(sorted(removed), sorted(str(self.trees / name) for name in ("atmain", "detached", "landed")))
        for name in ("atmain", "detached", "landed"):
            self.assertFalse((self.trees / name).exists(), name)
        for name in ("dirty", "locked", "open", "past"):
            self.assertTrue((self.trees / name / "work.txt").is_file(), name)
        listed = self.git("worktree", "list", "--porcelain")
        self.assertNotIn(str(self.trees / "landed"), listed)
        self.assertIn(str(self.trees / "dirty"), listed)
        git_calls = self.calls_of("git")
        self.assertIn(["worktree", "remove", str(self.trees / "landed")], git_calls)
        self.assertIn(["worktree", "prune"], git_calls)
        self.assertFalse([argv for argv in git_calls + self.calls_of("gh") if "--force" in argv or "-f" in argv])
        again = self.gc("--apply")
        self.assertEqual((again.returncode, "removed\t" in again.stdout), (0, False), again.stderr)
        self.assertEqual(self.rows(again), [row for row in self.expected_rows() if row[0] == "keep"])

    def test_a_path_outside_the_worktrees_directory_is_refused_and_one_inside_narrows_the_scan(self):
        for outside in (str(Path(self.temp.name) / "elsewhere"), str(self.repo), "."):
            with self.subTest(path=outside):
                refused = self.gc("--apply", outside)
                self.assertEqual((refused.returncode, refused.stdout), (2, ""), refused.stderr)
                self.assertIn("is outside", refused.stderr)
        self.assertEqual(self.calls_of("gh"), [])
        self.assertTrue((Path(self.temp.name) / "elsewhere").is_dir())
        one = self.gc("--dry-run", str(self.trees / "landed"))
        self.assertEqual(self.rows(one), [["remove", str(self.trees / "landed"), "feat/landed", "pr-merged #11"]])
        self.assertTrue((self.trees / "landed").is_dir())

    def test_a_failed_gh_call_ends_the_run_before_any_removal(self):
        failed = self.gc("--apply", FAKE_GH_FAIL="1")
        self.assertEqual(failed.returncode, 2, failed.stderr)
        self.assertIn("gh pr list --state merged", failed.stderr)
        self.assertTrue(all((self.trees / name).is_dir() for name in TREES))
        self.assertNotIn(["worktree", "prune"], self.calls_of("git"))


if __name__ == "__main__":
    unittest.main()
