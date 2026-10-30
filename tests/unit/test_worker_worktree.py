"""Exercise scripts/orchestrator/worker-worktree.sh against a scratch origin (regime-cutover U123).

Each test builds a bare `origin` and a main checkout pushed to it, and runs the lever from that checkout with
`DOTFILES_WT` under the scratch root. A `git` wrapper on PATH records every argv and fails one named call on request,
so a test can inject a failure after `git worktree add` and assert that nothing is left. Nothing reads the real
`~/.local/bin` or writes outside the scratch root.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/worker-worktree.sh"
PUSHURL = "refused://never-push-from-a-worker-worktree"
HOOK_MESSAGE = "standing order 29: the coordinator pushes"

GIT_WRAPPER = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["FAKE_GIT_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\\n")
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in " ".join(sys.argv[1:]):
    print("fake-git: failing as asked", file=sys.stderr)
    sys.exit(int(os.environ.get("FAKE_GIT_FAIL_STATUS") or 1))
os.execv(os.environ["REAL_GIT"], ["git", *sys.argv[1:]])
"""


class WorkerWorktreeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        bindir = self.root / "bin"
        bindir.mkdir()
        (bindir / "git").write_text(GIT_WRAPPER)
        (bindir / "git").chmod(0o755)
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        (self.root / "home").mkdir()
        self.git_calls = self.root / "git-calls"
        self.env = quiet_git_env(
            {
                "PATH": f"{bindir}:{os.environ['PATH']}",
                "HOME": str(self.root / "home"),
                "LC_ALL": "C",
                "REAL_GIT": shutil.which("git"),
                "GIT_CONFIG_GLOBAL": str(gitconfig),
                "GIT_CONFIG_NOSYSTEM": "1",
                "FAKE_GIT_CALLS": str(self.git_calls),
                "DOTFILES_WT": str(self.root / "wt"),
            }
        )
        self.origin = self.root / "origin.git"
        self.checkout = self.root / "checkout"
        git_init(self.origin, "--bare", env=self.env, cwd=self.root)
        git_init(self.checkout, env=self.env, cwd=self.root)
        (self.checkout / "README").write_text("main\n")
        self.git("add", "README")
        self.git("commit", "-q", "-m", "main")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")
        self.main = self.git("rev-parse", "origin/main")

    def git(self, *args, cwd=None):
        run = subprocess.run(["git", *args], cwd=cwd or self.checkout, env=self.env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout.strip()

    def git_status(self, *args, cwd=None):
        """(exit status, stdout, stderr) of a git command that may fail."""
        run = subprocess.run(["git", *args], cwd=cwd or self.checkout, env=self.env, capture_output=True, text=True)
        return run.returncode, run.stdout.strip(), run.stderr

    def run_lever(self, *args, cwd=None, **env):
        return subprocess.run(
            [str(LEVER), *args],
            cwd=cwd or self.checkout,
            env={**self.env, **env},
            capture_output=True,
            text=True,
            timeout=120,
        )

    def worktrees(self):
        return self.git("worktree", "list", "--porcelain")

    def origin_branch(self, branch):
        """The sha `origin` holds for BRANCH, or None."""
        status, sha, _ = self.git_status("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", cwd=self.origin)
        return sha if status == 0 else None

    def test_a_worker_worktree_cannot_push_and_the_coordinator_pushes_its_head_from_the_main_checkout(self):
        """Standing order 29 as a refusal of the tool: the worktree's own config holds the refused pushurl, the empty
        credential helper and a hooks directory under its git directory with the pre-push hook; a plain `git push`
        fails on the pushurl's scheme before any ref is read, a push that spells the URL is refused by the hook, and
        the main checkout, whose config is untouched, pushes the worker's head."""
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual(run.returncode, 0, run.stderr)
        path = self.root / "wt/U7"
        self.assertEqual(
            run.stdout,
            f"worktree={path}\nbranch=feat/u7\nhead={self.main}\n"
            f"push=git -C {self.checkout} push {self.origin} <head>:refs/heads/feat/u7\n",
        )
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD", cwd=path), "feat/u7")
        self.assertIn(f"worktree {path}\n", self.worktrees())
        # the three refusals live in the worktree's own config.worktree and git directory
        wt_git = Path(self.git("rev-parse", "--path-format=absolute", "--git-dir", cwd=path))
        self.assertEqual(wt_git.parent.parent, self.checkout / ".git")
        for key, value in (
            ("remote.origin.pushurl", PUSHURL),
            ("credential.helper", ""),
            ("core.hooksPath", str(wt_git / "hooks")),
        ):
            with self.subTest(key=key):
                # the empty helper value leaves nothing after the tab, which strip() removes: partition, not split
                origin, _, got = self.git("config", "--show-origin", "--get", key, cwd=path).partition("\t")
                self.assertEqual((origin, got), (f"file:{wt_git}/config.worktree", value))
                self.assertEqual(
                    self.git_status("config", "--get", key)[:2], (1, ""), "the main checkout keeps its config"
                )
        hook = wt_git / "hooks/pre-push"
        self.assertTrue(os.access(hook, os.X_OK), hook)
        self.assertIn(HOOK_MESSAGE, hook.read_text())
        self.assertEqual(self.git("config", "--get", "extensions.worktreeConfig"), "true")
        # the worker's push forms: every one fails, nothing reaches origin
        (path / "work.txt").write_text("work\n")
        self.git("add", "work.txt", cwd=path)
        self.git("commit", "-q", "-m", "work", cwd=path)
        head = self.git("rev-parse", "HEAD", cwd=path)
        for argv, message in (
            # the pushurl's scheme has no remote helper: refused before any ref is read, so the hook is not reached
            (("push", "origin", "HEAD"), "refused"),
            (("push", "-u", "origin", "feat/u7"), "refused"),
            # a push that spells the URL reads the remote's refs and is then refused by the hook
            (("push", str(self.origin), "HEAD:refs/heads/feat/u7"), HOOK_MESSAGE),
            (("push", f"file://{self.origin}", "HEAD:refs/heads/feat/u7"), HOOK_MESSAGE),
            # spelling the helper too: the hook fires first (an https push without a credential would then fail)
            (("-c", "credential.helper=", "push", str(self.origin), "HEAD:refs/heads/feat/u7"), HOOK_MESSAGE),
        ):
            with self.subTest(argv=argv):
                status, out, err = self.git_status(*argv, cwd=path)
                self.assertNotEqual(status, 0, out)
                self.assertIn(message, err)
                self.assertIsNone(self.origin_branch("feat/u7"), err)
        # the coordinator's line: from the main checkout, which shares the objects
        self.git("push", str(self.origin), f"{head}:refs/heads/feat/u7")
        self.assertEqual(self.origin_branch("feat/u7"), head)
        # the lever removed nothing: the cleanup runs only after a failed step
        calls = self.git_calls.read_text()
        self.assertNotIn('"remove"', calls)
        self.assertNotIn('"-D"', calls)

    def test_refusals_make_nothing(self):
        """Every input is checked before anything is made: exit 2, no worktree, no branch, no root directory, and
        `extensions.worktreeConfig` not yet set in the checkout. The branch is the normalized name
        `check-ref-format --branch` prints (`@{-1}` names the previous branch, here one that exists), a name with a
        character the shell would read (`;`) is refused, and a `show-ref` that fails (exit 128 from the PATH shim)
        is a refusal naming the read, never an absent branch."""
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "origin/main")
        self.git("branch", "taken", "origin/main")
        self.git("checkout", "-q", "taken")
        self.git("checkout", "-q", "main")
        before = self.worktrees()
        held = self.root / "held/U9"
        held.mkdir(parents=True)
        read_failed = {"FAKE_GIT_FAIL": "show-ref", "FAKE_GIT_FAIL_STATUS": "128"}
        for argv, cwd, env, message in (
            ((), None, {}, "usage: worker-worktree.sh <unit> <branch> <base>"),
            (("U7", "feat/u7"), None, {}, "usage:"),
            (("U7", "feat/u7", "origin/main", "extra"), None, {}, "usage:"),
            (("u7", "feat/u7", "origin/main"), None, {}, "the unit u7 is not U<n> or U<n><letter>"),
            (("U7/x", "feat/u7", "origin/main"), None, {}, "the unit U7/x is not U<n>"),
            (("U7", "", "origin/main"), None, {}, "the branch is empty"),
            (("U7", "feat..u7", "origin/main"), None, {}, "the branch feat..u7 is not a name git accepts"),
            (("U7", "feat/u7;true", "origin/main"), None, {}, "the branch feat/u7;true has a character outside"),
            (("U7", "feat/u7", ""), None, {}, "the base is empty"),
            (("U7", "feat/u7", "nowhere"), None, {}, "the base nowhere names no commit"),
            (("U7", "taken", "origin/main"), None, {}, "the branch taken exists"),
            (("U7", "@{-1}", "origin/main"), None, {}, "the branch taken exists"),
            (("U7", "feat/u7", "origin/main"), None, read_failed, "cannot read refs/heads/feat/u7 in"),
            (("U9", "feat/u9", "origin/main"), None, {"DOTFILES_WT": str(held.parent)}, f"{held} exists"),
            (("U7", "feat/u7", "origin/main"), None, {"DOTFILES_WT": "wt"}, "DOTFILES_WT wt is not an absolute path"),
            (("U7", "feat/u7", "origin/main"), linked, {}, "is a linked worktree"),
            (("U7", "feat/u7", "origin/main"), self.root / "home", {}, "run from the main checkout"),
        ):
            with self.subTest(argv=argv, cwd=cwd, env=env):
                run = self.run_lever(*argv, cwd=cwd, **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("worker-worktree.sh: refused: ", run.stderr)
                self.assertIn(message, run.stderr)
                self.assertFalse((self.root / "wt").exists())
                self.assertEqual(self.worktrees(), before)
                self.assertEqual(self.git_status("show-ref", "--verify", "--quiet", "refs/heads/feat/u7")[0], 1)
        self.git("config", "core.worktree", str(self.checkout))
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("refused: core.worktree is set in the checkout's config", run.stderr)
        self.git("config", "--unset", "core.worktree")
        self.git("remote", "remove", "origin")
        run = self.run_lever("U7", "feat/u7", "main")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"refused: no origin remote in {self.checkout}", run.stderr)
        self.assertFalse((self.root / "wt").exists())
        self.assertEqual(self.worktrees(), before)
        self.assertEqual(self.git_status("config", "--get", "extensions.worktreeConfig")[0], 1)

    def test_a_failing_step_after_the_add_leaves_no_half_made_worktree(self):
        """Standing order 21: a git step that fails after `git worktree add` is exit 1 naming it, and the tree and
        branch this run made are removed again, so no worktree without the refusals is left; a failed add or a failed
        `extensions.worktreeConfig` write makes nothing."""
        before = self.worktrees()
        for failing, message in (
            ("config --worktree remote.origin.pushurl", "cannot set remote.origin.pushurl"),
            ("config --worktree credential.helper", "cannot set credential.helper"),
            ("config --worktree core.hooksPath", "cannot set core.hooksPath"),
        ):
            with self.subTest(failing=failing):
                run = self.run_lever("U7", "feat/u7", "origin/main", FAKE_GIT_FAIL=failing)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
                self.assertIn(f"worker-worktree.sh: {message}", run.stderr)
                self.assertIn(
                    f"removing the half-made worktree {self.root / 'wt/U7'} and the branch feat/u7", run.stderr
                )
                self.assertFalse((self.root / "wt/U7").exists())
                self.assertEqual(self.worktrees(), before)
                self.assertEqual(self.git_status("show-ref", "--verify", "--quiet", "refs/heads/feat/u7")[0], 1)
        for failing, message in (
            ("worktree add", "git worktree add"),
            ("config extensions.worktreeConfig", "cannot set extensions.worktreeConfig"),
        ):
            with self.subTest(failing=failing):
                run = self.run_lever("U7", "feat/u7", "origin/main", FAKE_GIT_FAIL=failing)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertNotIn("removing", run.stderr)
                self.assertFalse((self.root / "wt/U7").exists())
                self.assertEqual(self.worktrees(), before)
                self.assertEqual(self.git_status("show-ref", "--verify", "--quiet", "refs/heads/feat/u7")[0], 1)
        # the same run without the injected failure then succeeds: nothing of the failed runs stands in its way
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=self.root / "wt/U7"), self.main)

    def test_a_worktree_add_that_fails_after_making_its_tree_leaves_nothing(self):
        """A post-checkout hook that exits 1 makes `git worktree add` exit non-zero after the tree and the branch
        exist (measured on git 2.56). The run is exit 1 naming the add, and the tree and the branch are removed
        again: a failed add leaves no worktree without the refusals behind either."""
        before = self.worktrees()
        hooks = self.checkout / ".git/hooks"
        hooks.mkdir(exist_ok=True)
        (hooks / "post-checkout").write_text("#!/bin/sh\necho 'post-checkout: refused' >&2\nexit 1\n")
        (hooks / "post-checkout").chmod(0o755)
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertIn("worker-worktree.sh: git worktree add", run.stderr)
        self.assertIn(f"removing the half-made worktree {self.root / 'wt/U7'} and the branch feat/u7", run.stderr)
        self.assertFalse((self.root / "wt/U7").exists())
        self.assertFalse((self.checkout / ".git/worktrees/U7").exists())
        self.assertEqual(self.worktrees(), before)
        self.assertEqual(self.git_status("show-ref", "--verify", "--quiet", "refs/heads/feat/u7")[0], 1)

    def test_a_pushurl_the_checkout_already_holds_is_refused_before_anything_is_made(self):
        """git pushes to every pushurl of a remote, and a worktree's own scope cannot shadow one set in the
        checkout's config (measured on git 2.56: `git push origin` reached the origin before the refusal URL
        failed), so such a checkout is refused before anything is made. A worktree the lever made reads exactly one
        pushurl, the refusal, and a plain push fails on its scheme before the remote's refs are read: the hook, which
        runs after that read, never runs."""
        before = self.worktrees()
        self.git("config", "remote.origin.pushurl", str(self.origin))
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"refused: remote.origin.pushurl is set in the checkout's config ({self.origin})", run.stderr)
        self.assertFalse((self.root / "wt").exists())
        self.assertEqual(self.worktrees(), before)
        self.assertEqual(self.git_status("show-ref", "--verify", "--quiet", "refs/heads/feat/u7")[0], 1)
        self.git("config", "--unset", "remote.origin.pushurl")
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual(run.returncode, 0, run.stderr)
        path = self.root / "wt/U7"
        self.assertEqual(self.git("config", "--get-all", "remote.origin.pushurl", cwd=path), PUSHURL)
        (path / "work.txt").write_text("work\n")
        self.git("add", "work.txt", cwd=path)
        self.git("commit", "-q", "-m", "work", cwd=path)
        status, _, err = self.git_status("push", "origin", "HEAD", cwd=path)
        self.assertNotEqual(status, 0)
        self.assertIn("refused", err)
        self.assertNotIn(HOOK_MESSAGE, err)
        self.assertIsNone(self.origin_branch("feat/u7"), err)

    def test_the_printed_push_line_round_trips_through_the_shell_for_a_spaced_checkout(self):
        """The coordinator pastes the push line into a shell: a checkout path and an origin URL holding a space are
        quoted, so `eval` of the line with `<head>` replaced pushes the worker's head from the main checkout."""
        origin = self.root / "origin two.git"
        checkout = self.root / "check out"
        git_clone(self.origin, origin, "--bare", env=self.env, cwd=self.root)
        git_clone(origin, checkout, env=self.env, cwd=self.root)
        root = self.root / "wt two"
        run = self.run_lever("U7", "feat/u7", "origin/main", cwd=checkout, DOTFILES_WT=str(root))
        self.assertEqual(run.returncode, 0, run.stderr)
        line = next(line for line in run.stdout.splitlines() if line.startswith("push="))
        self.assertEqual(
            line, f"push=git -C {self.root}/check\\ out push {self.root}/origin\\ two.git <head>:refs/heads/feat/u7"
        )
        path = root / "U7"
        (path / "work.txt").write_text("work\n")
        self.git("add", "work.txt", cwd=path)
        self.git("commit", "-q", "-m", "work", cwd=path)
        head = self.git("rev-parse", "HEAD", cwd=path)
        command = line.removeprefix("push=").replace("<head>", head)
        run = subprocess.run(
            ["bash", "-c", 'eval "$1"', "_", command],
            cwd=self.root / "home",
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.git("rev-parse", "--verify", "refs/heads/feat/u7", cwd=origin), head)


if __name__ == "__main__":
    unittest.main()
