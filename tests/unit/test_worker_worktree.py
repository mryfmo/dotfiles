"""Exercise scripts/orchestrator/worker-worktree.sh against a scratch origin (regime-cutover U123).

Each test builds a bare `origin` and a main checkout pushed to it, and runs the lever from that checkout with
`DOTFILES_WT` under the scratch root. A `git` wrapper on PATH records every argv and fails the calls named by
`FAKE_GIT_FAIL` (one or more substrings of the argv, newline-separated; `FAKE_GIT_FAIL_STATUS` the exit status of each,
the last repeating), so a test can inject a failure into one read or write, before or after `git init`, and assert
what is left; it holds the call named by `FAKE_GIT_WAIT_ON` until the fifo `FAKE_GIT_WAIT_FIFO` is opened for writing
(touching `FAKE_GIT_WAITING` first), so two runs can be ordered around one step; and it runs the shell command
`FAKE_GIT_AFTER` after the call named by `FAKE_GIT_AFTER_ON`, so a directory git made can be made read-only before the
lever writes into it. The steps that are not git (`mkdir`, `chmod`, `rm`, `uname`, `stat`) are failed by PATH shims
(`shim`). Nothing reads the real `~/.local/bin` or writes outside the scratch root.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/worker-worktree.sh"
PUSHURL = "refused://never-push-from-a-worker-worktree"
HOOK_MESSAGE = "standing order 29: the coordinator pushes"

GIT_WRAPPER = """#!/usr/bin/env python3
import json, os, subprocess, sys
with open(os.environ["FAKE_GIT_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\\n")
argv = " ".join(sys.argv[1:])
patterns = [p for p in os.environ.get("FAKE_GIT_FAIL", "").split("\\n") if p]
statuses = [s for s in os.environ.get("FAKE_GIT_FAIL_STATUS", "").split("\\n") if s] or ["1"]
for index, pattern in enumerate(patterns):
    if pattern in argv:
        print(f"fake-git: failing {pattern!r} as asked", file=sys.stderr)
        sys.exit(int(statuses[min(index, len(statuses) - 1)]))
wait_on = os.environ.get("FAKE_GIT_WAIT_ON")
if wait_on and wait_on in argv:
    open(os.environ["FAKE_GIT_WAITING"], "w").close()
    with open(os.environ["FAKE_GIT_WAIT_FIFO"]) as release:  # blocks until the test opens the fifo for writing
        release.read()
after_on = os.environ.get("FAKE_GIT_AFTER_ON")
if after_on and after_on in argv:
    status = subprocess.call([os.environ["REAL_GIT"], *sys.argv[1:]])
    subprocess.call(["sh", "-c", os.environ["FAKE_GIT_AFTER"]])
    sys.exit(status)
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

    def listing(self, path):
        """Every path under PATH, relative and sorted: what a run could have added to or removed from a directory."""
        return sorted(
            str(Path(directory, name).relative_to(path))
            for directory, dirs, files in os.walk(path)
            for name in dirs + files
        )

    def start_lever(self, *args, **env):
        """Start the lever from the checkout with ENV over the scratch env and return the Popen without waiting, for
        a run the test orders against another one."""
        merged = {key: value for key, value in {**self.env, **env}.items() if value is not None}
        return subprocess.Popen(
            [str(LEVER), *args],
            cwd=self.checkout,
            env=merged,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def shim(self, name, pattern, action):
        """The PATH to run under so that the external tool NAME is a shim in a directory of its own: a call whose
        arguments hold PATTERN runs ACTION (sh, the arguments in `$@`, the real tool in `$real`), every other call
        execs the real tool."""
        real = shutil.which(name, path=os.defpath)
        shims = Path(tempfile.mkdtemp(prefix=f"shim-{name}-", dir=self.root))
        (shims / name).write_text(
            f'#!/bin/sh\nreal={real}\ncase "$*" in\n*{pattern}*) {action} ;;\nesac\nexec "$real" "$@"\n'
        )
        (shims / name).chmod(0o755)
        return f"{shims}:{self.env['PATH']}"

    def make_writable(self, path):
        """Every directory under PATH owner-writable again, so the scratch root can be removed whatever a row left."""
        for directory, _, _ in os.walk(path):
            os.chmod(directory, 0o755)

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
            (f"branch.{branch}.pushRemote", "origin"),
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
        """Standing order 21: a git step that fails after the reservation is exit 2 naming it, and the repository
        this run made is removed again, so no tree without the refusals is left and the checkout is byte-identical:
        the init itself, the git-directory read, each config write, the fetch, the checkout, each readback and the
        head (twenty rows). The same run without the injected failure then succeeds."""
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
            (failing("config branch.feat/u7.pushRemote origin", status=1), "cannot set branch.feat/u7.pushRemote"),
            (failing("config --get-all remote.origin.pushurl"), f"remote.origin.pushurl is not set in {path}"),
            (failing("config --get core.hooksPath"), "core.hooksPath is not set"),
            (failing("config --get branch.feat/u7.remote"), "branch.feat/u7.remote is not set"),
            (failing("config --get branch.feat/u7.merge"), "branch.feat/u7.merge is not set"),
            (failing("config --get branch.feat/u7.pushRemote"), "branch.feat/u7.pushRemote is not set"),
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
        `GIT_COMMON_DIR` would point every command at another repository: the lever runs git with every `GIT_*` name
        removed, so the scratch file is unchanged, the checkout and the origin are untouched, and the fresh
        repository's own config carries the refusals."""
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

    def test_two_runs_for_one_unit_leave_exactly_one_repository_and_it_is_intact(self):
        """The target is reserved atomically (the verdict on e1f3b4cf, P1 :235): `mkdir <root>/<unit>` without `-p`
        is the reservation, so of two runs started together for one unit the one whose mkdir succeeded owns the
        directory and the other refuses having touched nothing. The first run is held in its `git init` by the PATH
        `git` waiting on a fifo (after the mkdir); the second runs to its end meanwhile; the first is then released:
        exactly one exits 0, the other exits 2 naming the existing path, and the winner's repository is intact
        afterwards (the old lever's second run passed the absence check and made the repository, and the released
        first run's cleanup then removed it)."""
        fifo = self.root / "release"
        os.mkfifo(fifo)
        waiting = self.root / "waiting"
        path = self.root / "wt/U7"
        before = self.checkout_state()
        first = self.start_lever(
            "U7",
            "feat/u7",
            "origin/main",
            FAKE_GIT_WAIT_ON="init --quiet --template=",
            FAKE_GIT_WAIT_FIFO=str(fifo),
            FAKE_GIT_WAITING=str(waiting),
        )
        try:
            deadline = time.monotonic() + 60
            while not waiting.exists():
                if first.poll() is not None:
                    self.fail(f"the first run ended before its git init: {first.communicate()[1]}")
                self.assertLess(time.monotonic(), deadline, "the first run did not reach its git init")
                time.sleep(0.05)
            second = self.run_lever("U7", "feat/u7", "origin/main")
            with fifo.open("w"):  # the reader is waiting, so this returns at once; closing releases it
                pass
            first_out, first_err = first.communicate(timeout=120)
        finally:
            if first.poll() is None:
                first.kill()
        runs = {
            "first, released after its mkdir": (first.returncode, first_out, first_err),
            "second, run meanwhile": (second.returncode, second.stdout, second.stderr),
        }
        self.assertEqual(sorted(status for status, _, _ in runs.values()), [0, 2], runs)
        loser = next(err for status, _, err in runs.values() if status == 2)
        self.assertIn(f"worker-worktree.sh: refused: {path} exists; an existing directory is never touched", loser)
        self.assertNotIn("removed again", loser)
        winner = next(out for status, out, _ in runs.values() if status == 0)
        self.assertIn(f"worktree={path}\nbranch=feat/u7\nhead={self.main}\n", winner)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main)
        self.assertEqual((path / "README").read_text(), "main\n")
        self.assert_refusals_in_place(path, "feat/u7")
        self.assertEqual(self.checkout_state(), before)

    def test_an_index_file_or_object_directory_of_the_caller_does_not_reach_the_lever_s_git(self):
        """`GIT_INDEX_FILE` and `GIT_OBJECT_DIRECTORY` in the caller's environment (the verdict on e1f3b4cf, P2 :176:
        the first sent the tree's index elsewhere, into the checkout when it named a path there, and left the tree
        without an index or a README; the second named another objects directory for the alternates) are two of the
        `GIT_*` names the lever subtracts by prefix instead of listing six: the run is exit 0, neither path is
        written, the checkout gains no file, and the worker has its own index, its README and the checkout's objects
        in its alternates."""
        for unit, index in (("U7", self.root / "elsewhere-index"), ("U8", self.checkout / ".git/index-elsewhere")):
            with self.subTest(index=index):
                objects = self.root / f"elsewhere-objects-{unit}"
                objects.mkdir()
                before = (self.checkout_state(), self.listing(self.checkout))
                run = self.run_lever(
                    unit, "feat/u7", "origin/main", GIT_INDEX_FILE=str(index), GIT_OBJECT_DIRECTORY=str(objects)
                )
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
                self.assertFalse(index.exists(), index)
                self.assertEqual(list(objects.iterdir()), [])
                self.assertEqual((self.checkout_state(), self.listing(self.checkout)), before)
                path = self.root / "wt" / unit
                self.assertTrue((path / ".git/index").is_file(), "the worker has its own index")
                self.assertEqual((path / "README").read_text(), "main\n")
                self.assertEqual(self.git("ls-files", cwd=path), "README")
                self.assert_refusals_in_place(path, "feat/u7")

    def test_a_root_inside_the_checkout_or_a_path_holding_a_newline_is_refused_before_anything_is_made(self):
        """`DOTFILES_WT` naming the checkout's hooks directory, the checkout, a directory under it that does not exist
        yet, a symlink into its git directory, or a path whose `..` component would land there (the verdict on
        e1f3b4cf, P2 :219: the old lever made U7 inside `.git/hooks` with exit 0), and a root or a checkout path
        holding a newline (P3 :239: written as two alternates lines) are each refused with exit 2 before anything is
        made: no `git init`, the hooks directory and the checkout as they were, nothing under the scratch root."""
        hooks = self.checkout / ".git/hooks"
        git_dir = self.checkout / ".git"
        link = self.root / "link"
        link.symlink_to(git_dir)
        before = (self.checkout_state(), self.listing(self.checkout))
        inside = f"lies inside the checkout {self.checkout} or its git directory {git_dir}"
        for root, message in (
            (str(hooks), f"DOTFILES_WT {hooks} {inside}"),
            (str(self.checkout), f"DOTFILES_WT {self.checkout} {inside}"),
            (str(self.checkout / "trees/absent"), f"DOTFILES_WT {self.checkout / 'trees/absent'} {inside}"),
            (str(link / "hooks"), f"DOTFILES_WT {hooks} {inside}"),
            (
                f"{self.root}/absent/../checkout/.git/hooks",
                f"DOTFILES_WT {self.root}/absent/../checkout/.git/hooks has a . or .. component; give the resolved path",
            ),
            (
                f"{self.root}/wt\nx",
                f"DOTFILES_WT {self.root}/wt\\nx holds a newline; the alternates file is one path per line",
            ),
        ):
            with self.subTest(root=root):
                run = self.run_lever("U7", "feat/u7", "origin/main", DOTFILES_WT=root)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"worker-worktree.sh: refused: {message}", run.stderr)
                self.assertNotIn("removed again", run.stderr)
                self.assertEqual((self.checkout_state(), self.listing(self.checkout)), before)
                self.assertEqual(sorted(entry.name for entry in self.root.iterdir() if entry.name.startswith("wt")), [])
        checkout = self.root / "check\nout"
        git_clone(self.origin, checkout, env=self.env, cwd=self.root)
        run = self.run_lever("U7", "feat/u7", "origin/main", cwd=checkout)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"refused: the checkout path {self.root}/check\\nout holds a newline", run.stderr)
        self.assertFalse((self.root / "wt").exists())
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")

    def test_a_case_alias_of_the_checkout_path_is_refused_by_identity(self):
        """On a case-insensitive volume `<CHECKOUT>/.git/hooks`, the checkout's hooks directory with the case of the
        checkout's name swapped, resolves to a string that is no prefix match of the checkout's path, and round 5's
        string comparison let it through: the verdict on ee3145aa (P2 :254) made U7 inside the checkout's hooks
        directory with exit 0. Containment is decided by the device and inode of the resolved root's longest existing
        directory and of each directory above it, so the alias, and an absent directory under it, are refused with
        exit 2 before anything is made, the hooks directory and the checkout as they were. Skipped where the scratch
        volume is case-sensitive: no alias names the checkout there."""
        alias = self.checkout.with_name(self.checkout.name.swapcase())
        hooks = alias / ".git/hooks"
        if not hooks.is_dir() or not os.path.samefile(hooks, self.checkout / ".git/hooks"):
            self.skipTest(f"{self.root} is on a case-sensitive volume: {hooks} names no directory of the checkout")
        before = (self.checkout_state(), self.listing(self.checkout))
        inside = f"lies inside the checkout {self.checkout} or its git directory {self.checkout / '.git'}"
        for root in (str(hooks), str(alias / "trees/absent")):
            with self.subTest(root=root):
                run = self.run_lever("U7", "feat/u7", "origin/main", DOTFILES_WT=root)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("worker-worktree.sh: refused: DOTFILES_WT ", run.stderr)
                self.assertIn(inside, run.stderr)
                self.assertNotIn("removed again", run.stderr)
                self.assertEqual((self.checkout_state(), self.listing(self.checkout)), before)
                self.assertFalse((self.checkout / ".git/hooks/U7").exists())
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")

    def test_a_symlink_to_a_directory_whose_name_holds_a_newline_is_refused_after_resolution(self):
        """`DOTFILES_WT` naming a symlink whose own name holds no newline, pointing at a directory whose name holds
        one (the verdict on ee3145aa, P3 :251: exit 0 and a `worktree=` receipt split across two lines), is refused
        with exit 2 after the resolution, naming the resolved path with the newline escaped, before anything is made:
        nothing under the target, no `git init`, the checkout as it was. The same for an absent directory under the
        link."""
        target = self.root / "trees\nx"
        target.mkdir()
        link = self.root / "trees-link"
        link.symlink_to(target)
        before = self.checkout_state()
        for root, resolved in ((str(link), f"{self.root}/trees\\nx"), (str(link / "wt"), f"{self.root}/trees\\nx/wt")):
            with self.subTest(root=root):
                run = self.run_lever("U7", "feat/u7", "origin/main", DOTFILES_WT=root)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"worker-worktree.sh: refused: DOTFILES_WT resolves to {resolved}, which holds a newline; "
                    "the alternates file is one path per line",
                    run.stderr,
                )
                self.assertNotIn("removed again", run.stderr)
                self.assertEqual(self.listing(target), [])
                self.assertEqual(self.checkout_state(), before)
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")

    def test_a_symlink_to_a_directory_whose_name_ends_in_a_newline_is_not_read_as_its_sibling(self):
        """`DOTFILES_WT` naming a newline-free symlink to a directory named `trees<LF>`, with a newline-free sibling
        `trees` present (the verdict on bb87a69a and Codex thread 4427932954, P2 :209): `$(cd … && pwd -P)` strips a
        trailing newline, so the newline check and the identity walk ran on the sibling and the tree was made under
        it with exit 0. The resolution keeps the newline, so the link, and an absent directory under it, are refused
        with exit 2 naming the resolved path, before anything is made: the sibling and the target stay empty, no
        `git init`, the checkout as it was. The same for a checkout whose own name ends in a newline with a sibling
        present: the checkout path is refused, not read as the sibling."""
        target = self.root / "trees\n"
        target.mkdir()
        sibling = self.root / "trees"
        sibling.mkdir()
        link = self.root / "trees-link"
        link.symlink_to(target)
        before = self.checkout_state()
        for root, resolved in ((str(link), f"{self.root}/trees\\n"), (str(link / "wt"), f"{self.root}/trees\\n/wt")):
            with self.subTest(root=root):
                run = self.run_lever("U7", "feat/u7", "origin/main", DOTFILES_WT=root)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"worker-worktree.sh: refused: DOTFILES_WT resolves to {resolved}, which holds a newline; "
                    "the alternates file is one path per line",
                    run.stderr,
                )
                self.assertNotIn("removed again", run.stderr)
                self.assertEqual((self.listing(sibling), self.listing(target)), ([], []))
                self.assertEqual(self.checkout_state(), before)
        checkout = self.root / "co\n"
        git_clone(self.origin, checkout, env=self.env, cwd=self.root)
        (self.root / "co").mkdir()
        run = self.run_lever("U7", "feat/u7", "origin/main", cwd=checkout)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"worker-worktree.sh: refused: the checkout path {self.root}/co\\n holds a newline", run.stderr)
        self.assertEqual(self.listing(self.root / "co"), [])
        self.assertFalse((self.root / "wt").exists())
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")

    def test_a_failing_resolver_or_identity_read_is_a_refusal_that_makes_nothing(self):
        """Standing order 21 for the reads that place the root (the verdict on ee3145aa, P2 test :686): the resolver's
        `cd` into a directory without permissions, the `uname -s` that chooses `stat`'s format flag (failing, or naming
        a system the lever knows no flag for), and `stat` on the checkout, on its git directory and on a directory the
        root lies under (failing, or printing something that is no device and inode) each refuse with exit 2 naming
        the read, before anything is made: no root directory, no `git init`, the checkout byte-identical."""
        before = self.checkout_state()
        failing_tool = 'echo "fake-$0: failing $* as asked" >&2; exit 1'
        identity = "cannot read the identity (device and inode) of"
        rows = [
            ({"PATH": self.shim("uname", "-s", failing_tool)}, "cannot read the operating system name (uname -s)"),
            (
                {"PATH": self.shim("uname", "-s", "echo Plan9; exit 0")},
                "no identity read for the system Plan9; stat's format flag is known for Darwin and Linux",
            ),
            ({"PATH": self.shim("stat", str(self.checkout), failing_tool)}, f"{identity} the checkout {self.checkout}"),
            (
                {"PATH": self.shim("stat", str(self.checkout), "echo not-an-identity; exit 0")},
                f"{identity} the checkout {self.checkout}",
            ),
            (
                {"PATH": self.shim("stat", f"{self.checkout}/.git", failing_tool)},
                f"{identity} the git directory {self.checkout}/.git",
            ),
            (
                # the path is the last argument; the shim's own pattern cannot anchor the end, so the action tests it
                {"PATH": self.shim("stat", "", f'case "$4" in {self.root}) {failing_tool} ;; esac')},
                f"{identity} {self.root}, which DOTFILES_WT {self.root}/wt lies under",
            ),
        ]
        if os.geteuid() != 0:  # root enters a directory without permissions
            locked = self.root / "locked"
            locked.mkdir()
            locked.chmod(0)
            self.addCleanup(locked.chmod, 0o755)
            rows.append(
                (
                    {"DOTFILES_WT": str(locked / "wt")},
                    f"cannot resolve DOTFILES_WT {locked}/wt; its longest existing directory cannot be entered",
                )
            )
        for env, message in rows:
            with self.subTest(message=message):
                run = self.run_lever("U7", "feat/u7", "origin/main", **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"worker-worktree.sh: refused: {message}", run.stderr)
                self.assertNotIn("removed again", run.stderr)
                self.assertFalse((self.root / "wt").exists())
                self.assertEqual(self.checkout_state(), before)
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assert_refusals_in_place(self.root / "wt/U7", "feat/u7")

    def test_a_relative_origin_url_is_refused_before_anything_is_made(self):
        """A relative `remote.origin.url` (`../origin.git`; the verdict on e1f3b4cf, P2 :247) resolves from the
        repository git runs in: `git fetch origin` works in the checkout, and the same value copied into the fresh
        repository names another place. The lever refuses it naming the value, before anything is made; an absolute
        URL of any form (a scheme, the scp-like `user@host:path`, a `/`-rooted path) is copied as it is."""
        self.git("remote", "set-url", "origin", "../origin.git")
        self.git("fetch", "-q", "origin")
        before = self.checkout_state()
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"worker-worktree.sh: refused: the origin URL ../origin.git of {self.checkout} is not absolute", run.stderr
        )
        self.assertFalse((self.root / "wt").exists())
        self.assertEqual(self.checkout_state(), before)
        self.assertNotIn('"init"', self.lever_calls, "no refusal ran git init")
        for unit, url in (
            ("U7", "https://example.invalid/origin.git"),
            ("U8", "git@example.invalid:origin.git"),
            ("U9", str(self.origin)),
        ):
            with self.subTest(url=url):
                self.git("remote", "set-url", "origin", url)
                run = self.run_lever(unit, "feat/u7", "origin/main")
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
                path = self.root / "wt" / unit
                self.assertEqual(self.git("config", "--get", "remote.origin.url", cwd=path), url)
                self.assertIn(f" push {url} FETCH_HEAD:refs/heads/feat/u7\n", run.stdout)

    def test_a_global_branch_push_remote_does_not_reopen_the_push_path(self):
        """git resolves a bare push's remote as `branch.<name>.pushRemote`, then `remote.pushDefault`, then
        `branch.<name>.remote` (git-push(1)): a global `branch.<branch>.pushRemote=upstream` with a global
        `remote.upstream.url` stood before the tree's `remote.pushDefault=origin` (the verdict on e1f3b4cf, P2 :251:
        the bare push reached upstream and was stopped by the hook, not by the refused scheme). The tree sets all
        three locally, so the bare push fails on the refused scheme before any remote is contacted, the hook never
        runs, and nothing reaches the origin."""
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stderr)
        path = self.root / "wt/U7"
        with self.gitconfig.open("a") as gitconfig:
            gitconfig.write(
                f'[branch "feat/u7"]\n\tpushRemote = upstream\n[remote "upstream"]\n\turl = {self.origin}\n'
            )
        self.assertEqual(self.git("config", "--get", "remote.upstream.url", cwd=path), str(self.origin))
        self.assertEqual(self.git("config", "--get", "branch.feat/u7.pushRemote", cwd=path), "origin")
        self.commit_work(path)
        status, _, err = self.git_status("push", cwd=path)
        self.assertNotEqual(status, 0)
        self.assertIn("remote helper 'refused'", err)
        self.assertNotIn(HOOK_MESSAGE, err)
        self.assertIsNone(self.origin_branch("feat/u7"), err)

    def test_a_failing_write_or_removal_after_the_reservation_is_named_and_leaves_nothing_of_this_run(self):
        """Standing order 21 for the steps that are not git (the verdict on e1f3b4cf, P2 test :304): the alternates
        write (`objects/info` made read-only by the PATH `git` after the init), the hooks-directory creation (a
        `mkdir` shim that fails), the hook write (a `mkdir` shim that makes the directory read-only) and the `chmod`
        (a shim that fails) each refuse with exit 2 naming the step, the reserved directory is removed again and the
        scratch root holds nothing of the run, with the checkout byte-identical; the cleanup's own `rm` failing (a
        shim, under an injected fetch failure) is said on stderr with the directory left for the operator, exit 2
        still. The plain run then succeeds."""
        self.addCleanup(self.make_writable, self.root / "wt")
        before = self.checkout_state()
        path = self.root / "wt/U7"
        failing_tool = 'echo "fake-$0: failing $* as asked" >&2; exit 1'
        for env, message in (
            (
                {
                    "FAKE_GIT_AFTER_ON": "init --quiet --template=",
                    "FAKE_GIT_AFTER": f"chmod 555 {path}/.git/objects/info",
                },
                f"cannot write {path}/.git/objects/info/alternates",
            ),
            ({"PATH": self.shim("mkdir", "hooks-lever", failing_tool)}, f"cannot make {path}/.git/hooks-lever"),
            (
                {"PATH": self.shim("mkdir", "hooks-lever", '"$real" "$@" && chmod 555 "$@"; exit $?')},
                f"cannot write {path}/.git/hooks-lever/pre-push",
            ),
            (
                {"PATH": self.shim("chmod", "pre-push", failing_tool)},
                f"cannot make {path}/.git/hooks-lever/pre-push executable",
            ),
        ):
            with self.subTest(message=message):
                run = self.run_lever("U7", "feat/u7", "origin/main", **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(
                    f"worker-worktree.sh: refused: {message}; the repository {path} this run made is removed again",
                    run.stderr,
                )
                self.assertNotIn("remove it by hand", run.stderr)
                self.assertEqual(self.listing(self.root / "wt"), [], "nothing of this run remains")
                self.assertEqual(self.checkout_state(), before)
        run = self.run_lever(
            "U7",
            "feat/u7",
            "origin/main",
            PATH=self.shim("rm", "-rf", failing_tool),
            **failing("fetch --quiet", status=1),
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"worker-worktree.sh: refused: git fetch {self.main} from {self.checkout} exited 1; "
            f"the repository {path} this run made is removed again",
            run.stderr,
        )
        self.assertIn(f"worker-worktree.sh: rm -rf {path} failed; remove it by hand", run.stderr)
        self.assertTrue((path / ".git/hooks-lever/pre-push").is_file(), "left for the operator, as stderr says")
        self.assertEqual(self.checkout_state(), before)
        shutil.rmtree(path)
        run = self.run_lever("U7", "feat/u7", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assert_refusals_in_place(path, "feat/u7")
        self.assertEqual(self.checkout_state(), before)


if __name__ == "__main__":
    unittest.main()
