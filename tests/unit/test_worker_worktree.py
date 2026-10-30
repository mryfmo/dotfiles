"""Exercise scripts/orchestrator/worker-worktree.sh against a scratch origin (regime-cutover U123).

Each test builds a bare `origin` and a main checkout pushed to it, and runs the lever from that checkout with
`DOTFILES_WT` under the scratch root. A `git` wrapper on PATH records every argv and fails the calls named by
`FAKE_GIT_FAIL` (one or more substrings of the argv, newline-separated; `FAKE_GIT_FAIL_STATUS` the exit status of each,
the last repeating), so a test can inject a failure into one read or write, before or after `git init`, and assert
what is left. Nothing reads the real `~/.local/bin` or writes outside the scratch root.
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
argv = " ".join(sys.argv[1:])
patterns = [p for p in os.environ.get("FAKE_GIT_FAIL", "").split("\\n") if p]
statuses = [s for s in os.environ.get("FAKE_GIT_FAIL_STATUS", "").split("\\n") if s] or ["1"]
for index, pattern in enumerate(patterns):
    if pattern in argv:
        print(f"fake-git: failing {pattern!r} as asked", file=sys.stderr)
        sys.exit(int(statuses[min(index, len(statuses) - 1)]))
os.execv(os.environ["REAL_GIT"], ["git", *sys.argv[1:]])
"""


def failing(*patterns: str, status: int = 128) -> dict[str, str]:
    """The env that makes the PATH `git` exit STATUS on each call whose argv holds one of PATTERNS (128 is git's own
    status for a read that could not run, which no decision may read as an absence)."""
    return {"FAKE_GIT_FAIL": "\n".join(patterns), "FAKE_GIT_FAIL_STATUS": str(status)}


class WorkerWorktreeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        bindir = self.root / "bin"
        bindir.mkdir()
        (bindir / "git").write_text(GIT_WRAPPER)
        (bindir / "git").chmod(0o755)
        self.gitconfig = self.root / "gitconfig"
        self.gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        (self.root / "home").mkdir()
        self.git_calls = self.root / "git-calls"
        self.lever_calls = ""
        self.env = quiet_git_env(
            {
                "PATH": f"{bindir}:{os.environ['PATH']}",
                "HOME": str(self.root / "home"),
                "LC_ALL": "C",
                "REAL_GIT": shutil.which("git"),
                "GIT_CONFIG_GLOBAL": str(self.gitconfig),
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
        """Run the lever from CWD (default the checkout) with ENV over the scratch env; a None value unsets the name.
        The git calls of every lever run accumulate in `self.lever_calls`, apart from the test's own."""
        merged = {key: value for key, value in {**self.env, **env}.items() if value is not None}
        self.git_calls.write_text("")
        run = subprocess.run(
            [str(LEVER), *args],
            cwd=cwd or self.checkout,
            env=merged,
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.lever_calls += self.git_calls.read_text()
        return run

    def worktrees(self):
        return self.git("worktree", "list", "--porcelain")

    def checkout_state(self):
        """Everything of the checkout a lever run could have touched: its refs, its config bytes, its hooks and its
        worktree list. The lever must leave each byte-identical."""
        hooks = self.checkout / ".git/hooks"
        return (
            self.git("for-each-ref"),
            (self.checkout / ".git/config").read_bytes(),
            sorted(hook.name for hook in hooks.iterdir()) if hooks.exists() else None,
            self.worktrees(),
        )

    def origin_branch(self, branch):
        """The sha `origin` holds for BRANCH, or None."""
        status, sha, _ = self.git_status("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", cwd=self.origin)
        return sha if status == 0 else None

    def git_dir(self, path):
        return Path(self.git("rev-parse", "--path-format=absolute", "--git-dir", cwd=path))

    def assert_refusals_in_place(self, path, branch):
        """The worker tree is a repository of its own whose config holds the refusals and the push shape, with the
        lever's hooks directory holding the one `pre-push` hook, and whose objects are the checkout's."""
        git_dir = self.git_dir(path)
        self.assertEqual(git_dir, path / ".git")
        self.assertEqual(
            (git_dir / "objects/info/alternates").read_text(),
            f"{self.git('rev-parse', '--path-format=absolute', '--git-path', 'objects')}\n",
        )
        for key, value in (
            ("remote.origin.url", str(self.origin)),
            ("remote.origin.fetch", "+refs/heads/*:refs/remotes/origin/*"),
            ("remote.origin.pushurl", PUSHURL),
            ("credential.helper", ""),
            ("core.hooksPath", str(git_dir / "hooks-lever")),
            ("remote.pushDefault", "origin"),
            ("push.default", "current"),
            (f"branch.{branch}.remote", "origin"),
            (f"branch.{branch}.merge", f"refs/heads/{branch}"),
        ):
            with self.subTest(key=key):
                # the empty helper value leaves nothing after the tab, which strip() removes: partition, not split;
                # the origin is the path git opened, `.git/config` relative to the tree
                origin, _, got = self.git("config", "--show-origin", "--get-all", key, cwd=path).partition("\t")
                self.assertEqual(
                    ((path / origin.removeprefix("file:")).resolve(), got), (git_dir / "config", value), key
                )
        hook = git_dir / "hooks-lever/pre-push"
        self.assertEqual([entry.name for entry in hook.parent.iterdir()], ["pre-push"])
        self.assertTrue(os.access(hook, os.X_OK), hook)
        self.assertIn(HOOK_MESSAGE, hook.read_text())
        self.assertNotIn(str(path), self.worktrees(), "git worktree list of the checkout does not list a worker tree")

    def commit_work(self, path):
        (path / "work.txt").write_text("work\n")
        self.git("add", "work.txt", cwd=path)
        self.git("commit", "-q", "-m", "work", cwd=path)
        return self.git("rev-parse", "HEAD", cwd=path)

    def test_a_worker_tree_cannot_push_and_the_coordinator_pushes_its_head_from_the_main_checkout(self):
        """Standing order 29 as a refusal of the tool: the worker tree is a fresh repository borrowing the checkout's
        objects, its own config holds the refused pushurl, the empty credential helper, a hooks directory with the
        pre-push hook and the push shape (`remote.pushDefault`, `push.default`, the branch's upstream); a plain
        `git push` fails on the pushurl's scheme before any remote is contacted, a push that spells the URL is refused
        by the hook, `git fetch origin` works, and the main checkout, which the lever never writes, fetches the
        worker's head by path and pushes it."""
        before = self.checkout_state()
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        path = self.root / "wt/U7"
        self.assertEqual(
            run.stdout,
            f"worktree={path}\nbranch=feat/u7\nhead={self.main}\n"
            f"push=git -C {self.checkout} fetch {path} feat/u7 && "
            f"git -C {self.checkout} push {self.origin} FETCH_HEAD:refs/heads/feat/u7\n",
        )
        self.assertEqual(self.checkout_state(), before)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD", cwd=path), "feat/u7")
        self.assertEqual(self.git("rev-parse", "origin/main", cwd=path), self.main)
        self.assertEqual((path / "README").read_text(), "main\n")
        self.assert_refusals_in_place(path, "feat/u7")
        for key in ("remote.origin.pushurl", "credential.helper", "core.hooksPath", "branch.feat/u7.remote"):
            self.assertEqual(self.git_status("config", "--get", key)[:2], (1, ""), "the main checkout keeps its config")
        # the worker's tests fetch main: origin is the checkout's origin, and origin/main moves with it
        (self.checkout / "README").write_text("main two\n")
        self.git("commit", "-q", "-am", "main two")
        self.git("push", "-q", "origin", "main")
        moved = self.git("rev-parse", "HEAD")
        self.git("fetch", "-q", "origin", cwd=path)
        self.assertEqual(self.git("rev-parse", "origin/main", cwd=path), moved)
        # the worker's push forms: every one fails, nothing reaches origin
        head = self.commit_work(path)
        for argv, message in (
            # the pushurl's scheme has no remote helper: refused before any remote is contacted, so the hook is not
            # reached; the bare push goes to origin through remote.pushDefault and push.default=current
            (("push",), "refused"),
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
        # the coordinator's line, as printed: fetched by path into the checkout, pushed from there
        command = next(line for line in run.stdout.splitlines() if line.startswith("push=")).removeprefix("push=")
        pushed = subprocess.run(["bash", "-c", command], env=self.env, capture_output=True, text=True, timeout=120)
        self.assertEqual(pushed.returncode, 0, pushed.stderr)
        self.assertEqual(self.origin_branch("feat/u7"), head)
        # the lever ran no worktree command and removed nothing: the cleanup runs only after a failed step
        self.assertNotIn('"worktree"', self.lever_calls)
        self.assertNotIn('"-D"', self.lever_calls)

    def test_refusals_make_nothing(self):
        """Every input is checked before anything is made: exit 2, no `git init`, no root directory, and the
        checkout byte-identical. A name with a character the shell would read (`;`) is refused, and a read that
        fails (exit 128 from the PATH shim: the git directory, the common directory, the objects directory and the
        origin URL reads) is a refusal naming the read, never an absence and never exit 1."""
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "origin/main")
        before = self.checkout_state()
        held = self.root / "held/U9"
        held.mkdir(parents=True)
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
            (
                ("U7", "feat/u7", "origin/main"),
                None,
                failing("rev-parse --path-format=absolute --git-dir"),
                "cannot read the git directory of",
            ),
            (
                ("U7", "feat/u7", "origin/main"),
                None,
                failing("rev-parse --path-format=absolute --git-common-dir"),
                "cannot read the git common directory of",
            ),
            (
                ("U7", "feat/u7", "origin/main"),
                None,
                failing("rev-parse --path-format=absolute --git-path objects"),
                "cannot read the objects directory of",
            ),
            (
                ("U7", "feat/u7", "origin/main"),
                None,
                failing("config --get remote.origin.url"),
                "cannot read remote.origin.url from the checkout's config",
            ),
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
                self.assertNotIn("removed again", run.stderr)
                self.assertFalse((self.root / "wt").exists())
                self.assertEqual(self.checkout_state(), before)
        self.git("remote", "remove", "origin")
        run = self.run_lever("U7", "feat/u7", "main")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"refused: no origin remote in {self.checkout}", run.stderr)
        self.assertFalse((self.root / "wt").exists())
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")

    def test_a_failing_step_after_the_init_leaves_no_repository_and_the_checkout_unchanged(self):
        """Standing order 21: a git step that fails after `git init` is exit 2 naming it, and the repository this
        run made is removed again, so no tree without the refusals is left and the checkout is byte-identical: the
        init itself, the git-directory read, each config write, the fetch, the checkout, each readback and the head.
        The same run without the injected failure then succeeds."""
        before = self.checkout_state()
        path = self.root / "wt/U7"
        for env, message in (
            (failing("init --quiet --template=", status=1), f"git init {path} exited 1"),
            (
                failing(f"-C {path} rev-parse --path-format=absolute --git-dir"),
                f"cannot read the git directory of {path}",
            ),
            (failing("config core.hooksPath", status=1), "cannot set core.hooksPath"),
            (failing("config remote.origin.url", status=1), "cannot set remote.origin.url"),
            (failing("config remote.origin.fetch", status=1), "cannot set remote.origin.fetch"),
            (failing("config remote.origin.pushurl", status=1), "cannot set remote.origin.pushurl"),
            (failing("config credential.helper", status=1), "cannot set credential.helper"),
            (failing("config remote.pushDefault", status=1), "cannot set remote.pushDefault"),
            (failing("config push.default", status=1), "cannot set push.default"),
            (failing("fetch --quiet", status=1), f"git fetch {self.main} from {self.checkout} exited 1"),
            (failing("checkout --quiet --no-track -b feat/u7", status=1), "git checkout -b feat/u7 origin/main"),
            (failing("config branch.feat/u7.remote origin", status=1), "cannot set branch.feat/u7.remote"),
            (failing("config branch.feat/u7.merge refs/heads/feat/u7", status=1), "cannot set branch.feat/u7.merge"),
            (failing("config --get-all remote.origin.pushurl"), f"remote.origin.pushurl is not set in {path}"),
            (failing("config --get core.hooksPath"), "core.hooksPath is not set"),
            (failing("config --get branch.feat/u7.remote"), "branch.feat/u7.remote is not set"),
            (failing("config --get branch.feat/u7.merge"), "branch.feat/u7.merge is not set"),
            (failing(f"-C {path} rev-parse --verify HEAD"), "cannot read the head of"),
        ):
            with self.subTest(failing=env["FAKE_GIT_FAIL"]):
                run = self.run_lever("U7", "feat/u7", "origin/main", **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"worker-worktree.sh: refused: {message}", run.stderr)
                self.assertIn(f"the repository {path} this run made is removed again", run.stderr)
                self.assertFalse(path.exists())
                self.assertFalse(path.is_symlink())
                self.assertEqual(self.checkout_state(), before)
        # the same run without the injected failure then succeeds: nothing of the failed runs stands in its way
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assert_refusals_in_place(path, "feat/u7")
        self.assertEqual(self.checkout_state(), before)

    def test_no_hook_of_the_checkout_runs_while_the_tree_is_made(self):
        """The worker tree is a repository of its own, made under a closed global configuration with the lever's own
        hooks directory in its config before the fetch and the checkout: a `hook.<name>.event` post-checkout hook of
        the checkout (git 2.56) that locks the tree, writes a marker and exits 1, and the `core.hooksPath` hooks of
        the checkout (a post-checkout that does the same, a reference-transaction that writes a marker) all stay
        silent, the run is exit 0 with the refusals in place, and the checkout keeps its hooks and config."""
        marker = self.root / "hook-ran"
        locker = self.root / "locker.sh"
        locker.write_text(
            f'#!/bin/sh\ngit worktree lock "$PWD" 2> /dev/null\necho config-hook >> {marker}\n'
            "echo 'config-hook: refused' >&2\nexit 1\n"
        )
        locker.chmod(0o755)
        self.git("config", "hook.locker.command", str(locker))
        self.git("config", "hook.locker.event", "post-checkout")
        hooks = self.root / "checkout-hooks"
        hooks.mkdir()
        (hooks / "post-checkout").write_text(
            f'#!/bin/sh\ngit worktree lock "$PWD" 2> /dev/null\necho post-checkout >> {marker}\n'
            "echo 'post-checkout: refused' >&2\nexit 1\n"
        )
        (hooks / "reference-transaction").write_text(f"#!/bin/sh\necho reference-transaction >> {marker}\nexit 0\n")
        for hook in ("post-checkout", "reference-transaction"):
            (hooks / hook).chmod(0o755)
        self.git("config", "core.hooksPath", str(hooks))
        before = self.checkout_state()
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
        self.assertNotIn("locked", self.worktrees())
        self.assertEqual(self.checkout_state(), before)
        path = self.root / "wt/U7"
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assert_refusals_in_place(path, "feat/u7")
        self.assertEqual(self.git_status("config", "--get", "hook.locker.event", cwd=path)[:2], (1, ""))
        self.commit_work(path)
        status, _, err = self.git_status("push", "origin", "HEAD", cwd=path)
        self.assertNotEqual(status, 0)
        self.assertIn("refused", err)
        self.assertIsNone(self.origin_branch("feat/u7"), err)

    def test_a_required_smudge_filter_of_the_checkout_does_not_run_while_the_tree_is_made(self):
        """A `.gitattributes` of the tree names a filter the checkout's config makes required and failing: the fresh
        repository has no filter config, so creation succeeds with the blob checked out as it is, the filter's
        command never runs, and the checkout keeps its config (observed on git 2.56: creation succeeds)."""
        marker = self.root / "smudge-ran"
        (self.checkout / ".gitattributes").write_text("* filter=fail\n")
        self.git("add", ".gitattributes")
        self.git("commit", "-q", "-m", "attributes")
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")
        base = self.git("rev-parse", "origin/main")
        self.git("config", "filter.fail.smudge", f"sh -c 'echo smudge >> {marker}; exit 1'")
        self.git("config", "filter.fail.required", "true")
        self.assertEqual(self.git("check-attr", "filter", "README"), "README: filter: fail")
        before = self.checkout_state()
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertFalse(marker.exists())
        path = self.root / "wt/U7"
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), base)
        self.assertEqual((path / "README").read_text(), "main\n")
        self.assertEqual(self.git_status("config", "--get", "filter.fail.smudge", cwd=path)[:2], (1, ""))
        self.assert_refusals_in_place(path, "feat/u7")
        self.assertEqual(self.checkout_state(), before)

    def test_the_checkout_s_configuration_does_not_reach_the_worker_tree(self):
        """A pushurl, `core.worktree` and a push shape the checkout's config holds (rounds 2 and 3 refused the first
        two; round 4 removes the premise) are not read by the fresh repository: creation succeeds, the worker tree
        reads one pushurl, the refusal, and a plain push fails on its scheme before any remote is contacted."""
        self.git("config", "remote.origin.pushurl", str(self.origin))
        self.git("config", "core.worktree", str(self.checkout))
        self.git("config", "remote.pushDefault", "upstream")
        self.git("config", "push.default", "nothing")
        before = self.checkout_state()
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(self.checkout_state(), before)
        path = self.root / "wt/U7"
        self.assertEqual(self.git("config", "--get-all", "remote.origin.pushurl", cwd=path), PUSHURL)
        self.assertEqual(self.git_status("config", "--get", "core.worktree", cwd=path)[:2], (1, ""))
        self.assert_refusals_in_place(path, "feat/u7")
        self.commit_work(path)
        for argv in (("push",), ("push", "origin", "HEAD")):
            with self.subTest(argv=argv):
                status, _, err = self.git_status(*argv, cwd=path)
                self.assertNotEqual(status, 0)
                self.assertIn("refused", err)
                self.assertNotIn(HOOK_MESSAGE, err)
                self.assertIsNone(self.origin_branch("feat/u7"), err)

    def test_the_worker_s_own_push_configuration_does_not_reopen_the_push_path(self):
        """A worker's global config with `remote.pushDefault=upstream` and `push.default=nothing` (the verdict on
        5183f849, P2 and P3: inherited, these sent a bare push to the real remote or made it fail on a configuration
        error): the fresh repository's own `remote.pushDefault=origin` and `push.default=current` win, so a bare
        `git push` fails on the refused scheme before any remote is contacted and the hook never runs, and a push
        that spells the URL is refused by the hook."""
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        path = self.root / "wt/U7"
        with self.gitconfig.open("a") as gitconfig:
            gitconfig.write("[remote]\n\tpushDefault = upstream\n[push]\n\tdefault = nothing\n")
        self.git("remote", "add", "upstream", str(self.origin), cwd=path)
        self.assertEqual(self.git("config", "--get", "remote.pushDefault", cwd=path), "origin")
        self.assertEqual(self.git("config", "--get", "push.default", cwd=path), "current")
        self.commit_work(path)
        for argv in (("push",), ("push", "origin", "HEAD"), ("push", "-u", "origin", "feat/u7")):
            with self.subTest(argv=argv):
                status, _, err = self.git_status(*argv, cwd=path)
                self.assertNotEqual(status, 0)
                self.assertIn("remote helper 'refused'", err)
                self.assertNotIn(HOOK_MESSAGE, err)
                self.assertIsNone(self.origin_branch("feat/u7"), err)
        status, _, err = self.git_status("push", str(self.origin), "HEAD:refs/heads/feat/u7", cwd=path)
        self.assertNotEqual(status, 0)
        self.assertIn(HOOK_MESSAGE, err)
        self.assertIsNone(self.origin_branch("feat/u7"), err)

    def test_a_branch_the_checkout_holds_is_no_conflict_and_the_name_is_the_normalized_one(self):
        """The branch is made in the fresh repository, so a branch of the same name in the checkout is no longer
        refused and is never touched; the name made is the one `check-ref-format --branch` prints, so `@{-1}` names
        the checkout's previous branch."""
        self.git("branch", "taken", "origin/main")
        self.git("checkout", "-q", "taken")
        (self.checkout / "taken.txt").write_text("taken\n")
        self.git("add", "taken.txt")
        self.git("commit", "-q", "-m", "taken")
        self.git("checkout", "-q", "main")
        before = self.checkout_state()
        for unit, branch in (("U7", "taken"), ("U8", "@{-1}")):
            with self.subTest(branch=branch):
                run = self.run_lever(unit, branch, "origin/main")
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
                path = self.root / "wt" / unit
                self.assertIn(f"worktree={path}\nbranch=taken\nhead={self.main}\n", run.stdout)
                self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD", cwd=path), "taken")
                self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
                self.assert_refusals_in_place(path, "taken")
                self.assertEqual(self.checkout_state(), before)

    def test_the_environment_of_the_caller_does_not_redirect_the_lever_s_git(self):
        """`GIT_CONFIG` would send a config write into another file, `GIT_CONFIG_PARAMETERS` and a `GIT_CONFIG_COUNT`
        entry would add a pushurl and a `core.worktree` every read sees, and `GIT_DIR`, `GIT_WORK_TREE` and
        `GIT_COMMON_DIR` would point every command at another repository: the lever runs git with each removed, so
        the scratch file is unchanged, the checkout and the origin are untouched, and the fresh repository's own
        config carries the refusals."""
        scratch = self.root / "elsewhere.gitconfig"
        scratch.write_text("[elsewhere]\n\tkey = value\n")
        count = int(self.env["GIT_CONFIG_COUNT"])
        before = self.checkout_state()
        run = self.run_lever(
            "U7",
            "feat/u7",
            "origin/main",
            GIT_CONFIG=str(scratch),
            GIT_CONFIG_PARAMETERS="'remote.origin.pushurl=https://example.invalid/elsewhere'",
            **{f"GIT_CONFIG_KEY_{count}": "core.worktree", f"GIT_CONFIG_VALUE_{count}": "/x/elsewhere"},
            GIT_CONFIG_COUNT=str(count + 1),
            GIT_DIR=str(self.origin),
            GIT_WORK_TREE=str(self.root / "home"),
            GIT_COMMON_DIR=str(self.origin),
        )
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        self.assertEqual(scratch.read_text(), "[elsewhere]\n\tkey = value\n")
        self.assertEqual(self.checkout_state(), before)
        self.assertIsNone(self.origin_branch("feat/u7"))
        path = self.root / "wt/U7"
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assert_refusals_in_place(path, "feat/u7")

    def test_the_default_root_is_dotfiles_wt_under_tmpdir(self):
        """With `DOTFILES_WT` unset the root is `dotfiles-wt` under `TMPDIR`, the value the lever's `@env` line, the
        README row and the PR body's Contract state: under a scratch `TMPDIR` the repository is made there."""
        tmpdir = self.root / "scratch-tmp"
        tmpdir.mkdir()
        run = self.run_lever("U7", "feat/u7", "origin/main", DOTFILES_WT=None, TMPDIR=str(tmpdir))
        self.assertEqual(run.returncode, 0, run.stderr)
        path = tmpdir / "dotfiles-wt/U7"
        self.assertIn(f"worktree={path}\n", run.stdout)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assertEqual(self.git("config", "--get", "remote.origin.pushurl", cwd=path), PUSHURL)
        self.assertFalse((self.root / "wt").exists())

    def test_the_printed_push_line_round_trips_through_the_shell_for_a_spaced_checkout(self):
        """The coordinator pastes the push line into a shell: a checkout path, a worker tree path and an origin URL
        holding a space are quoted, so `eval` of the line fetches the worker's head by path into the main checkout
        and pushes it from there."""
        origin = self.root / "origin two.git"
        checkout = self.root / "check out"
        git_clone(self.origin, origin, "--bare", env=self.env, cwd=self.root)
        git_clone(origin, checkout, env=self.env, cwd=self.root)
        root = self.root / "wt two"
        run = self.run_lever("U7", "feat/u7", "origin/main", cwd=checkout, DOTFILES_WT=str(root))
        self.assertEqual(run.returncode, 0, run.stderr)
        line = next(line for line in run.stdout.splitlines() if line.startswith("push="))
        self.assertEqual(
            line,
            f"push=git -C {self.root}/check\\ out fetch {self.root}/wt\\ two/U7 feat/u7 && "
            f"git -C {self.root}/check\\ out push {self.root}/origin\\ two.git FETCH_HEAD:refs/heads/feat/u7",
        )
        path = root / "U7"
        head = self.commit_work(path)
        run = subprocess.run(
            ["bash", "-c", 'eval "$1"', "_", line.removeprefix("push=")],
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
