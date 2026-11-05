"""Exercise the worktree sweep of home/dot_local/bin/common/executable_disk-gc in scratch repositories.

Each test builds a bare `origin` and a checkout under a temporary directory, points `DISK_GC_REPOS` at the checkout,
and runs the lever with a PATH that holds a `git` wrapper (it records every argv and execs the real git) and symlinks
to the tools the lever needs, and nothing else: no `docker`, `uv` or `npm`, so the docker and package-cache steps skip
and the host's daemon and caches are never touched. HOME and XDG_DATA_HOME are under the scratch root. The tests assert
what is on disk after a run and the lever's log lines. The lever needs GNU find's `-files0-from` and `date -d`;
setUpModule probes both and skips the module with the reason when either is missing.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env

ROOT = Path(__file__).resolve().parents[2]
GC = ROOT / "home/dot_local/bin/common/executable_disk-gc"
TOOLS = (
    "bash",
    "find",
    "date",
    "tar",
    "gzip",
    "awk",
    "du",
    "wc",
    "tr",
    "basename",
    "mktemp",
    "df",
    "grep",
    "rm",
    "mkdir",
)
ABSENT = ("docker", "uv", "npm")

GIT_WRAPPER = """#!/usr/bin/env python3
import json, os, sys
argv = sys.argv[1:]
with open(os.environ["FAKE_GIT_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(argv) + "\\n")
joined = " ".join(argv)
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in joined:
    sys.exit("fake-git: failing as asked")
if os.environ.get("FAKE_GIT_SWAP") and "worktree remove" in joined:
    # The worktree directory is swapped for a symlink while git fails to remove it, after the lever's check.
    path, target = os.environ["FAKE_GIT_SWAP"].split(os.pathsep)
    os.rename(path, path + ".moved")
    os.symlink(target, path)
    sys.exit("fake-git: remove failed after the swap")
os.execv(os.environ["REAL_GIT"], ["git", *argv])
"""

tools_dir = None
skip_reason = None


def setUpModule():
    global tools_dir, skip_reason
    tools_dir = Path(tempfile.mkdtemp(prefix="disk-gc-tools-"))
    for tool in TOOLS:
        real = shutil.which(tool)
        if real:
            (tools_dir / tool).symlink_to(real)
    (tools_dir / "python3").symlink_to(sys.executable)  # the git wrapper's shebang; the narrow PATH has no other
    for tool in ("bash", "find", "date", "tar", "awk"):
        if not (tools_dir / tool).exists():
            skip_reason = f"no {tool} on PATH"
            return
    env = {"PATH": str(tools_dir)}
    probe = subprocess.run(
        ["find", "-files0-from", "-", "-maxdepth", "0", "-print"],
        input=f"{tools_dir}\0",
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        skip_reason = "find does not take -files0-from (GNU findutils needed)"
        return
    probe = subprocess.run(["date", "-d", "1 days ago", "+%s"], env=env, capture_output=True, text=True, check=False)
    if probe.returncode != 0:
        skip_reason = "date does not take -d (GNU coreutils needed)"


def tearDownModule():
    if tools_dir is not None:
        shutil.rmtree(tools_dir, ignore_errors=True)


class DiskGcTest(unittest.TestCase):
    def setUp(self):
        if skip_reason:
            self.skipTest(skip_reason)
        self.temp = tempfile.TemporaryDirectory(prefix="disk-gc-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        bindir = self.root / "bin"
        bindir.mkdir()
        (bindir / "git").write_text(GIT_WRAPPER)
        (bindir / "git").chmod(0o755)
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = gc test\n\temail = gc@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.git_calls = self.root / "git-calls"
        self.workspace = self.root / "ws"
        self.workspace.mkdir()
        self.checkout = self.workspace / "repo"
        self.env = quiet_git_env(
            {
                "PATH": f"{bindir}:{tools_dir}",
                "HOME": str(self.root / "home"),
                "XDG_DATA_HOME": str(self.root / "xdg"),
                "TMPDIR": str(self.root / "tmp"),
                "REAL_GIT": shutil.which("git"),
                "GIT_CONFIG_GLOBAL": str(gitconfig),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CEILING_DIRECTORIES": str(self.root),
                "FAKE_GIT_CALLS": str(self.git_calls),
                "DISK_GC_REPOS": str(self.checkout),
                "DISK_GC_WORKSPACE": str(self.workspace),
                "DISK_GC_WORKTREE_DAYS": "1",
            }
        )
        for name in ("home", "xdg", "tmp"):
            (self.root / name).mkdir()
        for tool in ABSENT:
            self.assertIsNone(shutil.which(tool, path=self.env["PATH"]), f"{tool} must be absent from the lever's PATH")
        git_init(self.root / "origin.git", "--bare", env=self.env)
        git_clone(self.root / "origin.git", self.checkout, env=self.env)
        (self.checkout / "README").write_text("scratch\n")
        self.git("add", "README")
        self.git("commit", "-q", "-m", "initial")
        self.git("push", "-q", "origin", "main")

    def git(self, *args, cwd=None):
        return subprocess.run(
            ["git", *args], cwd=cwd or self.checkout, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def age(self, path):
        """Set every file under PATH (the tree's `.git` aside) three days back, so the tree counts as idle."""
        stamp = time.time() - 3 * 86400
        for parent, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d != ".git"]
            for name in files:
                os.utime(Path(parent, name), (stamp, stamp))

    def add_tree(self, path):
        """A detached worktree at PATH on origin/main, idle: merged into the base by construction."""
        self.git("worktree", "add", "-q", "--detach", str(path), "origin/main")
        self.age(path)
        return path

    def run_gc(self, *args, **overrides):
        if self.git_calls.exists():
            self.git_calls.unlink()
        result = subprocess.run(
            [str(GC), *args],
            cwd=self.root,
            env={**self.env, **overrides},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        return result

    def calls(self):
        return [json.loads(line) for line in self.git_calls.read_text().splitlines()] if self.git_calls.exists() else []

    def removals(self):
        return [argv for argv in self.calls() if "remove" in argv]

    def space_and_prefix(self):
        """`<ws>/My Tree`, a merged idle worktree, beside `<ws>/My`, a clone holding an untracked marker.

        The sibling is a clone, not a plain directory, because that is the shape the sweep named: a path at the cut
        prefix whose HEAD is merged and whose tree is clean passes every check of the old reader.
        """
        tree = self.add_tree(self.workspace / "My Tree")
        prefix = git_clone(self.root / "origin.git", self.workspace / "My", env=self.env)
        marker = prefix / "marker.txt"
        marker.write_text("precious\n")
        self.age(prefix)
        return tree, prefix, marker

    def test_a_path_with_a_space_is_removed_whole_and_its_prefix_is_untouched(self):
        tree, prefix, marker = self.space_and_prefix()
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(marker.is_file(), f"the marker under My was removed: {result.stdout}")
        self.assertEqual(marker.read_text(), "precious\n")
        self.assertFalse(tree.exists(), result.stdout)
        self.assertTrue((prefix / "README").is_file())
        self.assertIn("disk-gc: remove My Tree: merged into origin/main", result.stdout)
        self.assertNotIn(str(prefix), result.stdout.replace(str(tree), ""), "the prefix is never named")
        for argv in self.calls():
            self.assertNotIn(str(prefix), argv, "no git call received the truncated path")
        self.assertEqual([argv[-1] for argv in self.removals()], [str(tree)])

    def test_a_path_with_a_newline_is_removed_whole_and_nothing_else(self):
        tree = self.workspace / "new\nline"
        try:
            tree.mkdir()
        except OSError as error:
            self.skipTest(f"the filesystem refuses a newline in a name: {error}")
        tree.rmdir()
        self.add_tree(tree)
        sibling = self.workspace / "new"
        sibling.mkdir()
        (sibling / "marker.txt").write_text("precious\n")
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(tree.exists(), result.stdout)
        self.assertEqual((sibling / "marker.txt").read_text(), "precious\n")
        self.assertIn("disk-gc: remove new\nline: merged into origin/main", result.stdout)
        self.assertEqual([argv[-1] for argv in self.removals()], [str(tree)])
        self.assertEqual(sorted(p.name for p in self.workspace.iterdir()), ["new", "repo"])

    def test_the_lock_is_read_from_each_tree_s_own_admin_directory(self):
        first = self.add_tree(self.workspace / "one" / "tree")
        second = self.add_tree(self.workspace / "two" / "tree")
        self.git("worktree", "lock", "--reason", f"claude agent test (pid {os.getpid()} start 1)", str(first))
        admin = {
            path: Path(self.git("rev-parse", "--path-format=absolute", "--git-dir", cwd=path))
            for path in (first, second)
        }
        self.assertEqual(admin[first].name, "tree")
        self.assertEqual(admin[second].name, "tree1", "git names the second admin directory by a suffix")
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(second.exists(), result.stdout)
        self.assertTrue((first / "README").is_file(), result.stdout)
        self.assertEqual(result.stdout.count("disk-gc: keep tree: locked by a live process"), 1, result.stdout)
        self.assertEqual(result.stdout.count("disk-gc: remove tree: merged into origin/main"), 1, result.stdout)
        self.assertEqual([argv[-1] for argv in self.removals()], [str(second)])
        self.assertIn(f"worktree {first}", self.git("worktree", "list", "--porcelain"))

    def test_a_listed_path_that_is_no_longer_a_worktree_root_is_kept(self):
        tree = self.add_tree(self.workspace / "plain")
        shutil.rmtree(tree)
        tree.mkdir()
        (tree / "keep.txt").write_text("not a worktree\n")
        self.assertIn(f"worktree {tree}", self.git("worktree", "list", "--porcelain"), "still listed")
        result = self.run_gc("--apply")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((tree / "keep.txt").read_text(), "not a worktree\n")
        self.assertIn(f"disk-gc: keep plain: not a worktree root of {self.checkout} (no toplevel)", result.stdout)
        self.assertEqual(self.removals(), [])

    def test_the_report_mode_removes_nothing_and_names_the_whole_path(self):
        tree, prefix, marker = self.space_and_prefix()
        result = self.run_gc()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            f"disk-gc: would run: git -C {self.checkout} worktree remove --force --force {tree}", result.stdout
        )
        self.assertTrue((tree / "README").is_file())
        self.assertEqual(marker.read_text(), "precious\n")
        self.assertEqual(self.removals(), [])
        for argv in self.calls():
            self.assertNotIn(str(prefix), argv)

    def test_a_failed_listing_skips_the_repository_and_removes_nothing(self):
        tree = self.add_tree(self.workspace / "merged")
        result = self.run_gc("--apply", FAKE_GIT_FAIL="worktree list")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"disk-gc: cannot list the worktrees of {self.checkout}; skipping its worktrees", result.stdout)
        self.assertNotIn("remove", result.stdout)
        self.assertTrue((tree / "README").is_file())
        self.assertEqual(self.removals(), [])
        self.assertIn("disk-gc: docker not installed; skipping", result.stdout)

    def test_a_directory_swapped_after_the_check_is_not_removed(self):
        tree = self.add_tree(self.workspace / "swapped")
        victim = self.root / "victim"
        victim.mkdir()
        (victim / "marker.txt").write_text("precious\n")
        result = self.run_gc("--apply", FAKE_GIT_SWAP=f"{tree}{os.pathsep}{victim}")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("disk-gc: worktree remove failed for swapped", result.stdout)
        self.assertIn("disk-gc: keep swapped: no longer the directory checked before removal", result.stdout)
        self.assertTrue(tree.is_symlink(), "the planted link stays")
        self.assertEqual((victim / "marker.txt").read_text(), "precious\n")
        self.assertTrue((tree.parent / "swapped.moved" / "README").is_file(), "the moved tree stays")


if __name__ == "__main__":
    unittest.main()
