"""Exercise scripts/orchestrator/worker-worktree.sh against a scratch origin (regime-cutover U123).

Each test builds a bare `origin` and a main checkout pushed to it, and runs the lever from that checkout with
`DOTFILES_WT` under the scratch root. A `git` wrapper on PATH records every argv and fails the calls named by
`FAKE_GIT_FAIL` (one or more substrings of the argv, newline-separated; `FAKE_GIT_FAIL_STATUS` the exit status of each,
the last repeating), so a test can inject a failure into one read or write, before or after `git init`, and assert
what is left; it holds the call named by `FAKE_GIT_WAIT_ON` until the fifo `FAKE_GIT_WAIT_FIFO` is opened for writing
(touching `FAKE_GIT_WAITING` first), so two runs can be ordered around one step; and it runs the shell command
`FAKE_GIT_AFTER` after the call named by `FAKE_GIT_AFTER_ON`, so a directory git made can be made read-only before the
lever writes into it. The steps that are not git (`mkdir`, `chmod`, `rm`, `uname`, `stat`) are failed by PATH shims
(`shim`). The owner-record tests (U509, U509e) run the lever's `claim` and `release`, which run the pinned program
`worker-worktree-owner.py` beside it under one lock; two runs are raced by holding each at its record read (`hold`),
and a failed write is injected with a file-size limit of 0 on the run. A release names the claim time its claim
printed (U509f), so a same-name successor's record is never removed by its predecessor; the program's read, pin and
hash refusals run against the installed layout built under the scratch HOME from the checkout's bytes
(`install_lever`). The dispatch-text and return-check tests (U573) run `task` and `verify` against seat checkouts under
regime-env's seats root for the scratch checkout (`~/.local/state/omp-seats/checkout` under the scratch HOME) and plant
linked worktrees of the checkout under the roots `verify` judges, the `/private/tmp/dotfiles-wt` one as the
`.git/worktrees` entry `git worktree add` records, so the test writes nothing there; the round-2 tests (verdict
U573-32986760) plant the reads the audit found passing as absences: a caller's `GIT_DIR` and `GIT_TRACE`, a mode-000
parent of the seats root, a seat's `core.fsmonitor`, a tag named like the branch, a worktree path holding a newline
and a unit holding one; the round-3 tests (verdict U573-5f983ea2 and the Codex threads on the round-2 pull request)
plant a link and a file above the seats root, a git read failing inside regime-env alone (`FAKE_GIT_FAIL_SKIP` lets
the lever's own read pass), a seat's clean filter, a case alias of the root and an entry spelled through a link, a
seat and a HOME holding a newline, a worktree path holding a carriage return, and a branch the checkout held before
the tree was made; the round-4 tests (verdict U573-5a5aa7fa) plant a stray worktree whose branch holds an unmerged
commit and a seat with a staged version cancelled by an unstaged edit beside a binary file (no finding names a
destructive command), a seats root component longer than the system allows and a link chain deeper than the kernel
follows, an unreadable directory inside a seat, a seat holding a submodule, a root and a brief holding a carriage
return, a failing `uname`, and a file both staged and changed again. Nothing reads the real `~/.local/bin` or writes
outside the scratch root.
"""

import errno
import importlib.util
import json
import os
import re
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/worker-worktree.sh"
PUSHURL = "refused://never-push-from-a-worker-worktree"
HOOK_MESSAGE = "standing order 29: the coordinator pushes"
OWNER_RECORD = ".git/regime-owner"
OWNER_LOCK = ".git/regime-owner.lock"
STAMP = "%Y-%m-%dT%H:%M:%SZ"
# A claim time in the grammar, for a release whose refusal or `no claim` comes before the record is compared.
ANY_STAMP = "2026-11-13T05:00:00Z"
# The record's two exact lines, as the program matches them over the file's bytes.
RECORD = re.compile(
    rb"owner=([A-Za-z0-9._-]{1,64})\nclaimed=([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z)\n"
)

GIT_WRAPPER = """#!/usr/bin/env python3
import json, os, subprocess, sys
with open(os.environ["FAKE_GIT_CALLS"], "a", encoding="utf-8") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\\n")
argv = " ".join(sys.argv[1:])
patterns = [p for p in os.environ.get("FAKE_GIT_FAIL", "").split("\\n") if p]
statuses = [s for s in os.environ.get("FAKE_GIT_FAIL_STATUS", "").split("\\n") if s] or ["1"]
skip = int(os.environ.get("FAKE_GIT_FAIL_SKIP", "0"))
for index, pattern in enumerate(patterns):
    if pattern in argv:
        if skip:  # the first SKIP matching calls of the run pass; the call just recorded counts
            with open(os.environ["FAKE_GIT_CALLS"], encoding="utf-8") as calls:
                seen = sum(1 for line in calls if pattern in " ".join(json.loads(line)))
            if seen <= skip:
                continue
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

    def run_lever(self, *args, cwd=None, preexec_fn=None, lever=LEVER, **env):
        """Run the lever (the checkout's, or the installed copy LEVER names) from CWD (default the checkout) with ENV
        over the scratch env; a None value unsets the name; PREEXEC_FN runs in the child before the lever (a resource
        limit or an umask on the run). The git calls of every lever run accumulate in `self.lever_calls`, apart from
        the test's own."""
        merged = {key: value for key, value in {**self.env, **env}.items() if value is not None}
        self.git_calls.write_text("")
        run = subprocess.run(
            [str(lever), *args],
            cwd=cwd or self.checkout,
            env=merged,
            capture_output=True,
            text=True,
            timeout=120,
            preexec_fn=preexec_fn,
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

    # The tree's owner record (regime-cutover U509, U509e, U509f): `claim <unit> <owner> [--stale <minutes>]` writes
    # `<tree>/.git/regime-owner` and refuses while a live owner holds it, printing the claim time; `release <unit>
    # <owner> <claimed>` removes it when the record holds that owner and that claim time, and nothing else. Every
    # record operation runs in `worker-worktree-owner.py` beside the lever under one lock on `regime-owner.lock`,
    # which stays beside the record. The program reads the real clock, so a claim's stamp is read back and must lie
    # within the run, and a hand-written record is given its age with a 30 s margin, so its age in whole minutes is
    # exact while the test runs.

    def now(self):
        return datetime.now(timezone.utc).replace(microsecond=0)

    def write_record(self, path, owner, minutes):
        """A record written by hand in the exact form, claimed MINUTES ago and 30 s more (so its age in whole minutes
        is MINUTES for the next 30 s; a negative count is a record from the future); the stamp written."""
        stamp = (self.now() - timedelta(minutes=minutes, seconds=30)).strftime(STAMP)
        (path / OWNER_RECORD).write_bytes(f"owner={owner}\nclaimed={stamp}\n".encode())
        return stamp

    def assert_record(self, path, owner, since):
        """The record is a regular file of mode 0600 holding the two exact lines, naming OWNER with a claim time
        between SINCE and now; the stamp it holds."""
        record = path / OWNER_RECORD
        self.assertFalse(record.is_symlink())
        self.assertTrue(record.is_file())
        self.assertEqual(stat.S_IMODE(record.lstat().st_mode), 0o600)
        content = record.read_bytes()
        match = RECORD.fullmatch(content)
        self.assertIsNotNone(match, content)
        self.assertEqual(match.group(1).decode(), owner)
        stamp = match.group(2).decode()
        claimed = datetime.strptime(stamp, STAMP).replace(tzinfo=timezone.utc)
        self.assertLessEqual(since, claimed)
        self.assertLessEqual(claimed, self.now())
        return stamp

    def verb_args(self, verb, unit, owner, stamp=ANY_STAMP):
        """The lever's arguments for VERB on UNIT by OWNER: a release names the claim time it releases (U509f)."""
        return (verb, unit, owner) if verb == "claim" else (verb, unit, owner, stamp)

    def install_lever(self):
        """The installed layout under the scratch HOME from the checkout's own bytes, as `test_lever_self_check`
        builds it: the lever and its program under `~/.local/bin/common`, the manifest at
        `~/.agents/agent-config.yaml`; the installed lever's path, which reads that manifest and that program."""
        bindir = self.root / "home/.local/bin/common"
        bindir.mkdir(parents=True)
        (self.root / "home/.agents").mkdir()
        shutil.copy2(ROOT / "home/dot_agents/agent-config.yaml", self.root / "home/.agents/agent-config.yaml")
        for name in ("worker-worktree.sh", "worker-worktree-owner.py"):
            shutil.copy2(ROOT / "home/dot_local/bin/common" / f"executable_{name}", bindir / name)
        return bindir / "worker-worktree.sh"

    def owner_entries(self, path):
        """The entries of the tree's `.git` that belong to the owner record: the record, its lock, any temporary."""
        return sorted(entry.name for entry in (path / ".git").iterdir() if "regime-owner" in entry.name)

    def make_tree(self, unit="U7"):
        """A worker tree the creation subcommand made under the scratch root; it carries no owner record."""
        run = self.run_lever(unit, f"feat/{unit.lower()}", "origin/main")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        path = self.root / "wt" / unit
        self.assertEqual(self.owner_entries(path), [], "the creation subcommand does not claim")
        return path

    def working_tree(self, path):
        """Every path under PATH outside its `.git`, relative and sorted: what a worker's status or commit can see."""
        return [entry for entry in self.listing(path) if entry != ".git" and not entry.startswith(".git/")]

    class Hold:
        """A PATH whose tools hold a lever run at its record read until `release`: the program's interpreter
        `python3` before it starts (so held runs reach the lock together), and the round-1 shell's `cat` of the
        record after it has printed (so held runs have read the same owner). Each holder writes its pid under
        `waiting` and blocks opening the fifo for reading; `release` opens it for writing and keeps it open, so a
        holder that arrives later passes too."""

        def __init__(self, case, once):
            self.case = case
            scratch = Path(tempfile.mkdtemp(prefix="hold-", dir=case.root))
            self.fifo = scratch / "fifo"
            os.mkfifo(self.fifo)
            self.waiting = scratch / "waiting"
            self.waiting.mkdir()
            shims = scratch / "bin"
            shims.mkdir()
            hold = f'hold() {{ : > "{self.waiting}/$$"; : < "{self.fifo}"; }}\n'
            for name, after in (("python3", False), ("cat", True)):
                real = shutil.which(name, path=case.env["PATH"])
                guard = (
                    f'if [ ! -e "{scratch}/once-{name}" ]; then : > "{scratch}/once-{name}"; hold; fi'
                    if once
                    else "hold"
                )
                if after:
                    body = f'case "$*" in\n*regime-owner*) "$real" "$@"; status=$?; {guard}; exit $status ;;\nesac\n'
                else:
                    body = f"{guard}\n"
                (shims / name).write_text(f'#!/bin/sh\nreal={real}\n{hold}{body}exec "$real" "$@"\n')
                (shims / name).chmod(0o755)
            self.path = f"{shims}:{case.env['PATH']}"
            self.writer = None

        def wait_for(self, count, runs):
            """Until COUNT holders are waiting; a run that ends first fails the test with its stderr."""
            deadline = time.monotonic() + 60
            while len(os.listdir(self.waiting)) < count:
                for run in runs:
                    if run.poll() is not None:
                        self.case.fail(f"a run ended before its record read: {run.communicate()[1]}")
                self.case.assertLess(time.monotonic(), deadline, "the runs did not reach their record read")
                time.sleep(0.02)

        def release(self):
            deadline = time.monotonic() + 60
            while self.writer is None:
                try:
                    self.writer = os.open(self.fifo, os.O_WRONLY | os.O_NONBLOCK)
                except OSError as error:  # ENXIO: no reader has opened the fifo yet
                    self.case.assertLess(time.monotonic(), deadline, f"no holder opened the fifo: {error}")
                    time.sleep(0.02)
            self.case.addCleanup(os.close, self.writer)

    def hold(self, once=False):
        return self.Hold(self, once)

    @staticmethod
    def no_file_may_grow():
        """For `preexec_fn`: no regular file of the run may hold a byte (RLIMIT_FSIZE 0), and SIGXFSZ is ignored so
        a write past the limit is EFBIG from `write`, the error a program handles, not a death by signal (the
        disposition is inherited across exec, so bash and the program both see the error)."""
        signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
        resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))

    def test_claim_writes_the_owner_record_under_the_tree_s_git_directory(self):
        """A fresh claim writes `<tree>/.git/regime-owner` as the two lines `owner=<name>` and `claimed=<ISO UTC>`,
        the claim time within the run, mode 0600, a regular file, with the lock file `regime-owner.lock` (0600)
        beside it and nothing else, and prints `claimed <unit> owner=<name> claimed=<stamp>` (the claim time a release
        names, U509f); the record lives under `.git`, so the
        tree's `git status` (untracked and ignored files included) and its working tree are as they were, the main
        checkout is byte-identical, and the subcommand runs no git at all."""
        path = self.make_tree()
        before = self.checkout_state()
        tree_before = self.working_tree(path)
        self.lever_calls = ""
        since = self.now()
        run = self.run_lever("claim", "U7", "U7Worker")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "U7Worker", since)
        self.assertEqual(run.stdout, f"claimed U7 owner=U7Worker claimed={stamp}\n", "the claim time a release names")
        self.assertEqual((path / OWNER_RECORD).read_bytes(), f"owner=U7Worker\nclaimed={stamp}\n".encode())
        self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"])
        self.assertEqual(stat.S_IMODE((path / OWNER_LOCK).lstat().st_mode), 0o600)
        self.assertEqual(self.git("status", "--porcelain", "--untracked-files=all", "--ignored", cwd=path), "")
        self.assertEqual(self.working_tree(path), tree_before)
        self.assertEqual(self.checkout_state(), before)
        self.assertEqual(self.lever_calls, "", "claim and release run no git")
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main, "the tree is still the worker's")
        # the default root: with `DOTFILES_WT` unset the tree is looked up under `TMPDIR/dotfiles-wt`
        tmpdir = self.root / "scratch-tmp"
        tmpdir.mkdir()
        run = self.run_lever("U8", "feat/u8", "origin/main", DOTFILES_WT=None, TMPDIR=str(tmpdir))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        run = self.run_lever("claim", "U8", "W8", DOTFILES_WT=None, TMPDIR=str(tmpdir))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(tmpdir / "dotfiles-wt/U8", "W8", since)
        self.assertEqual(run.stdout, f"claimed U8 owner=W8 claimed={stamp}\n")

    def test_a_second_claim_within_stale_is_refused_with_exit_3_naming_the_owner_and_the_age(self):
        """While the record is younger than `--stale` minutes (default 20), a claim by anyone, the same name
        included, is refused with exit 3 (a code of its own, so the coordinator's dispatch step tells a live owner
        from a malformed call) and one stderr line naming the owner, the claim time and the age; the record is
        untouched. The claim that follows a fresh one is refused at age 0; hand-written records at 5, 19, 0 and 59
        minutes (`--stale 60`), one by the same name at 1 minute, and one from the future (a clock set back), which
        is live at age 0."""
        path = self.make_tree()
        since = self.now()
        run = self.run_lever("claim", "U7", "W1")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W1", since)
        refused = f"worker-worktree.sh: refused: the tree {path} is owned by W1 (claimed %s, %d min ago); release it or wait past --stale\n"
        run = self.run_lever("claim", "U7", "W2")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (3, "", refused % (stamp, 0)))
        for owner, minutes, args in (
            ("W2", 5, ()),
            ("W2", 19, ()),
            ("W2", 0, ()),
            ("W2", 59, ("--stale", "60")),
            ("W1", 1, ()),
            ("W2", -10, ()),
        ):
            with self.subTest(owner=owner, minutes=minutes, args=args):
                stamp = self.write_record(path, "W1", minutes)
                record = (path / OWNER_RECORD).read_bytes()
                run = self.run_lever("claim", "U7", owner, *args)
                self.assertEqual((run.returncode, run.stdout, run.stderr), (3, "", refused % (stamp, max(minutes, 0))))
                self.assertEqual((path / OWNER_RECORD).read_bytes(), record)

    def test_a_claim_past_stale_takes_over_and_the_record_names_the_new_owner(self):
        """A record at least `--stale` minutes old is taken over: exit 0, one stdout line naming the stale owner and
        the age, and the record rewritten by rename (mode 0600, no temporary left) with the new owner and the new
        time. `--stale 0` takes over any record; a record written by hand in the exact form is read by its own time;
        `--stale N` refuses at N-1 minutes and takes over at N."""
        path = self.make_tree()
        before = self.checkout_state()
        self.write_record(path, "W1", 20)
        since = self.now()
        run = self.run_lever("claim", "U7", "W2")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W2", since)
        self.assertEqual(run.stdout, f"taken over U7 from=W1 age=20m owner=W2 claimed={stamp}\n")
        self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"], "no temporary left")
        self.write_record(path, "W2", 1)
        run = self.run_lever("claim", "U7", "W3", "--stale", "0")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W3", since)
        self.assertEqual(run.stdout, f"taken over U7 from=W2 age=1m owner=W3 claimed={stamp}\n")
        self.write_record(path, "Old.worker-1", 60)
        run = self.run_lever("claim", "U7", "W4")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W4", since)
        self.assertEqual(run.stdout, f"taken over U7 from=Old.worker-1 age=60m owner=W4 claimed={stamp}\n")
        stamp = self.write_record(path, "W4", 2)
        run = self.run_lever("claim", "U7", "W5", "--stale", "3")
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertIn(f"is owned by W4 (claimed {stamp}, 2 min ago)", run.stderr)
        self.write_record(path, "W4", 3)
        run = self.run_lever("claim", "U7", "W5", "--stale", "3")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W5", since)
        self.assertEqual(run.stdout, f"taken over U7 from=W4 age=3m owner=W5 claimed={stamp}\n")
        self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"], "no temporary left")
        self.assertEqual(self.git("status", "--porcelain", "--untracked-files=all", "--ignored", cwd=path), "")
        self.assertEqual(self.checkout_state(), before)

    def test_release_by_the_owner_removes_the_record_and_release_with_no_record_is_no_claim(self):
        """`release <unit> <owner> <claimed>` by the record's owner, naming the claim time its claim printed, removes
        the record and prints `released <unit> owner=<name>`; with no record it prints `no claim <unit>` and exits 0
        whatever claim time it names, so a release after a kill or a crash is idempotent; nothing else under `.git`
        is touched (the lock file stays), and the next claim is a fresh one, not a takeover."""
        path = self.make_tree()
        run = self.run_lever("release", "U7", "W1", ANY_STAMP)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "no claim U7\n", ""))
        self.assertEqual(self.owner_entries(path), ["regime-owner.lock"])
        listing = self.listing(path)
        since = self.now()
        run = self.run_lever("claim", "U7", "W1")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W1", since)
        self.assertEqual(run.stdout, f"claimed U7 owner=W1 claimed={stamp}\n")
        run = self.run_lever("release", "U7", "W1", stamp)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "released U7 owner=W1\n", ""))
        self.assertFalse((path / OWNER_RECORD).exists())
        self.assertEqual(self.listing(path), listing, "the release removed the record and nothing else")
        run = self.run_lever("release", "U7", "W1", stamp)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "no claim U7\n", ""))
        since = self.now()
        run = self.run_lever("claim", "U7", "W2")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W2", since)
        self.assertEqual(run.stdout, f"claimed U7 owner=W2 claimed={stamp}\n")

    def test_release_by_another_owner_is_refused_with_exit_3_and_keeps_the_record(self):
        """A release naming an owner other than the record's is refused with exit 3 and one stderr line, whatever
        the record's age: release has no staleness rule, a stale record is taken over by `claim` instead."""
        path = self.make_tree()
        for minutes in (1, 60):
            with self.subTest(minutes=minutes):
                stamp = self.write_record(path, "W1", minutes)
                record = (path / OWNER_RECORD).read_bytes()
                run = self.run_lever("release", "U7", "W2", stamp)
                self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
                self.assertEqual(
                    run.stderr,
                    f"worker-worktree.sh: refused: the tree {path} is owned by W1, not W2; only the owner releases "
                    "it\n",
                )
                self.assertEqual((path / OWNER_RECORD).read_bytes(), record)

    def test_a_claim_or_release_outside_the_grammar_or_on_no_worker_tree_is_refused_with_exit_2(self):
        """A name outside `[A-Za-z0-9._-]{1,64}`, a unit outside `U<n>` or `U<n><letter>`, a `--stale` that is no
        count, a release without its claim time or with one outside `YYYY-MM-DDTHH:MM:SSZ`, a wrong argument count,
        a tree that does not exist or is no repository (no `.git` directory, a
        `.git` file), a `.git` that is a symbolic link, a root outside the creation subcommand's shape rules, and a
        record outside the two exact lines (read by shape, never as an owner or an absence) each refuse with exit 2
        and one stderr line; no record or lock is written anywhere and a malformed record is left for the
        operator."""
        path = self.make_tree()
        record = path / OWNER_RECORD
        (self.root / "wt/U8").mkdir()
        (self.root / "wt/U9").mkdir()
        (self.root / "wt/U9/.git").symlink_to(path / ".git")
        (self.root / "wt/U10").mkdir()
        (self.root / "wt/U10/.git").write_text(f"gitdir: {path / '.git'}\n")
        cases = (
            (("claim", "U7", "bad name"), "the owner bad name is not a name over [A-Za-z0-9._-]{1,64}"),
            (("claim", "U7", "a;b"), "the owner a;b is not a name over"),
            (("claim", "U7", "x" * 65), "is not a name over [A-Za-z0-9._-]{1,64}"),
            (("claim", "U7", ""), "is not a name over [A-Za-z0-9._-]{1,64}"),
            (("release", "U7", "a/b", ANY_STAMP), "the owner a/b is not a name over"),
            (("claim", "7", "W1"), "the unit 7 is not U<n> or U<n><letter>"),
            (("claim", "U7bb", "W1"), "the unit U7bb is not U<n> or U<n><letter>"),
            (("release", "u7", "W1", ANY_STAMP), "the unit u7 is not U<n> or U<n><letter>"),
            (("claim", "U7", "W1", "--stale", "x"), "--stale x is not a count of minutes"),
            (("claim", "U7", "W1", "--stale", "-1"), "--stale -1 is not a count of minutes"),
            (("claim", "U7", "W1", "--stale"), "--stale needs a count of minutes"),
            (("claim", "U7", "W1", "--later"), "usage:"),
            (("claim", "U7"), "usage:"),
            (("claim",), "usage:"),
            (("release", "U7", "W1", "--stale", "5"), "usage:"),
            (("release", "U7", "W1", "extra"), "the claim time extra is not YYYY-MM-DDTHH:MM:SSZ"),
            (("release", "U7", "W1", "2026-11-13 05:00:00"), "the claim time 2026-11-13 05:00:00 is not"),
            (("release", "U7", "W1"), "release names the claim it releases: release <unit> <owner> <claimed>"),
            (("claim", "U11", "W1"), f"the tree {self.root}/wt/U11 does not exist"),
            (("release", "U11", "W1", ANY_STAMP), f"the tree {self.root}/wt/U11 does not exist"),
            (
                ("claim", "U8", "W1"),
                f"{self.root}/wt/U8 is no worker repository: {self.root}/wt/U8/.git is not a directory",
            ),
            (
                ("claim", "U10", "W1"),
                f"{self.root}/wt/U10 is no worker repository: {self.root}/wt/U10/.git is not a directory",
            ),
            (
                ("claim", "U9", "W1"),
                f"{self.root}/wt/U9/.git is a symbolic link; a worker tree's .git is the directory the lever made",
            ),
            (("release", "U9", "W1", ANY_STAMP), f"{self.root}/wt/U9/.git is a symbolic link"),
            (("release", "U8", "W1", ANY_STAMP), "is no worker repository"),
        )
        for argv, message in cases:
            with self.subTest(argv=argv):
                run = self.run_lever(*argv)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("worker-worktree.sh: refused: "), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(
                    self.owner_entries(path), [], "nothing under the real tree, through the symlink included"
                )
                for unit in ("U8", "U9", "U10", "U11"):
                    self.assertFalse((self.root / "wt" / unit / OWNER_RECORD).is_file())
                    self.assertFalse((self.root / "wt" / unit / OWNER_LOCK).is_file())
        for env, message in (
            ({"DOTFILES_WT": "relative/wt"}, "DOTFILES_WT relative/wt is not an absolute path"),
            ({"DOTFILES_WT": f"{self.root}/wt/../wt"}, "has a . or .. component"),
            ({"DOTFILES_WT": f"{self.root}/wt\nx"}, "holds a newline"),
        ):
            with self.subTest(env=env):
                run = self.run_lever("claim", "U7", "W1", **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(self.owner_entries(path), [])
        for body in (
            b"owner=W1\n",
            b"owner=W1\nclaimed=2026-11-13T05:00:00Z\n\n",
            b"owner=bad name\nclaimed=2026-11-13T05:00:00Z\n",
            b"owner=W1\nclaimed=yesterday\n",
            b"owner=W1\nclaimed=2026-13-40T05:00:00Z\n",
            b"claimed=2026-11-13T05:00:00Z\nowner=W1\n",
            b"owner=W1\nclaimed=2026-11-13T05:00:00Z",
            b"",
        ):
            record.write_bytes(body)
            for verb in ("claim", "release"):
                with self.subTest(body=body, verb=verb):
                    run = self.run_lever(*self.verb_args(verb, "U7", "W2"))
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                    self.assertIn(f"the owner record {path}/.git/regime-owner is not the two lines", run.stderr)
                    self.assertEqual(record.read_bytes(), body, "left for the operator, as stderr says")
        record.unlink()
        (path / ".git/regime-owner").symlink_to(path / ".git/HEAD")
        for verb in ("claim", "release"):
            with self.subTest(verb=verb, record="a symbolic link"):
                run = self.run_lever(*self.verb_args(verb, "U7", "W2"))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the owner record {path}/.git/regime-owner is a symbolic link", run.stderr)
                self.assertTrue(record.is_symlink())
                self.assertEqual(self.git("rev-parse", "HEAD", cwd=path), self.main, "HEAD was not written through it")
        record.unlink()
        os.mkfifo(record)
        for verb in ("claim", "release"):
            with self.subTest(verb=verb, record="a fifo"):
                run = self.run_lever(*self.verb_args(verb, "U7", "W2"))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"the owner record {path}/.git/regime-owner is not a regular file", run.stderr)
                self.assertTrue(stat.S_ISFIFO(record.lstat().st_mode))

    # Round 1 (verdicts/U509-e343a569.md): the eight findings, each a test red at e343a569 where the old behaviour
    # was the defect (six) and a coverage test where it was the missing test (the `.git` link, the unreadable record).

    def test_two_claimers_on_one_stale_record_leave_exactly_one_owner(self):
        """The round-1 P1 (:484): the record's read and the takeover were two steps with nothing held between them,
        so two claimers that both read a stale record both wrote and both exited 0. Two real runs race the takeover
        of a record 25 minutes old, each held at its record read (the program's interpreter before it starts, so
        both reach the one lock together; round 1's `cat` after it printed, so both held the stale owner) and both
        released at once: exactly one exits 0 and prints `taken over`, the other exits 3 naming the winner at age 0,
        and the record names the winner alone, with no temporary beside it. The race is run three times on the tree,
        the lock removed before each round so its first creation is raced too: the round-4 P2 (:269, U509g) was the
        loser of that creation exiting 2 with ENOENT instead of 3 under the lock, once in three gate runs; the
        creation itself is raced deterministically by the next test."""
        path = self.make_tree()
        for round_number in range(3):
            with self.subTest(round=round_number):
                self.write_record(path, "W1", 25)
                (path / OWNER_LOCK).unlink(missing_ok=True)
                since = self.now()
                hold = self.hold()
                runs = {owner: self.start_lever("claim", "U7", owner, PATH=hold.path) for owner in ("W2", "W3")}
                try:
                    hold.wait_for(2, runs.values())
                    hold.release()
                    results = {owner: (*run.communicate(timeout=120), run.returncode) for owner, run in runs.items()}
                finally:
                    for run in runs.values():
                        if run.poll() is None:
                            run.kill()
                self.assertEqual(sorted(status for _, _, status in results.values()), [0, 3], results)
                winner = next(owner for owner, (_, _, status) in results.items() if status == 0)
                loser = next(owner for owner, (_, _, status) in results.items() if status == 3)
                stamp = self.assert_record(path, winner, since)
                self.assertEqual(
                    results[winner][:2], (f"taken over U7 from=W1 age=25m owner={winner} claimed={stamp}\n", "")
                )
                self.assertEqual(
                    results[loser][:2],
                    (
                        "",
                        f"worker-worktree.sh: refused: the tree {path} is owned by {winner} (claimed {stamp}, 0 min ago); "
                        "release it or wait past --stale\n",
                    ),
                )
                self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"])

    def test_the_lock_s_first_creation_raced_through_the_descriptor_is_opened_by_every_run_after_a_retry(self):
        """The round-4 P2 (verdicts/U509f-f21a9f7f.md :269, U509g): on macOS an `O_CREAT` open through a directory
        descriptor of a name another process is creating at the same instant fails with ENOENT for the loser (a probe
        of 300 synchronized pairs failed 299 losers; by absolute path, or with `O_EXCL` first, none; one retry
        recovered every one), so two claimers that reached the lock's first creation together exited 0 and 2 for 0 and
        3, and the race above flaked once in three gate runs. The program's `take_lock`, loaded from the checkout's
        file, runs in eight forked children released by one barrier against a directory holding no lock, ten times:
        every child gets the lock in turn (a refusal is reported with its line and status), and one regular lock file
        of mode 0600 is all that is left. Red at a7e4f042: the open without the retry refused the losers with ENOENT."""
        spec = importlib.util.spec_from_file_location(
            "worker_worktree_owner", ROOT / "scripts/orchestrator/worker-worktree-owner.py"
        )
        program = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(program)
        for round_number in range(10):
            git_dir = self.root / f"lock-race-{round_number}"
            git_dir.mkdir()
            dfd = os.open(git_dir, os.O_RDONLY | os.O_DIRECTORY)
            children = []
            try:
                barrier_read, barrier_write = os.pipe()
                for _ in range(8):
                    report_read, report_write = os.pipe()
                    pid = os.fork()
                    if pid == 0:  # the child: wait at the barrier, take the lock once, report and leave at once
                        try:
                            os.close(report_read)
                            os.close(barrier_write)
                            os.read(barrier_read, 1)
                            try:
                                program.take_lock(dfd, str(git_dir))
                            except program.Refusal as refusal:
                                os.write(report_write, refusal.reason.encode())
                                os._exit(refusal.status)
                            os._exit(0)
                        except BaseException:
                            os._exit(99)
                    os.close(report_write)
                    children.append((pid, report_read))
                os.close(barrier_read)
                time.sleep(0.01)
                os.close(barrier_write)  # the EOF releases every child at once
                outcomes = []
                for pid, report_read in children:
                    _, status = os.waitpid(pid, 0)
                    outcomes.append((os.waitstatus_to_exitcode(status), os.read(report_read, 4096).decode()))
                    os.close(report_read)
            finally:
                os.close(dfd)
            self.assertEqual(outcomes, [(0, "")] * 8, f"round {round_number}: every run opens the lock")
            self.assertEqual(sorted(entry.name for entry in git_dir.iterdir()), ["regime-owner.lock"])
            self.assertTrue(stat.S_ISREG((git_dir / "regime-owner.lock").lstat().st_mode))
            self.assertEqual(stat.S_IMODE((git_dir / "regime-owner.lock").lstat().st_mode), 0o600)

    def test_a_release_delayed_past_a_successor_s_claim_is_refused_and_the_successor_s_record_stands(self):
        """The round-1 P1's second half (:484): a release that had read its owner before a successor's claim went on
        to remove the successor's record. The old owner's release is held at its record read (the first call alone),
        the successor takes the tree over meanwhile, and the release is let go: it exits 3 naming the successor,
        and the successor's record is byte-identical afterwards. Under the lock the release reads and removes in
        one step, so nothing can land between its read and its removal; the delay a kill path shows is before it."""
        path = self.make_tree()
        first = self.write_record(path, "W1", 25)
        hold = self.hold(once=True)
        late = self.start_lever("release", "U7", "W1", first, PATH=hold.path)
        try:
            hold.wait_for(1, (late,))
            since = self.now()
            run = self.run_lever("claim", "U7", "W2", "--stale", "0", PATH=hold.path)
            self.assertEqual((run.returncode, run.stderr), (0, ""))
            stamp = self.assert_record(path, "W2", since)
            self.assertEqual(run.stdout, f"taken over U7 from=W1 age=25m owner=W2 claimed={stamp}\n")
            hold.release()
            out, err = late.communicate(timeout=120)
        finally:
            if late.poll() is None:
                late.kill()
        self.assertEqual(
            (late.returncode, out, err),
            (
                3,
                "",
                f"worker-worktree.sh: refused: the tree {path} is owned by W2, not W1; only the owner releases it\n",
            ),
        )
        self.assertEqual((path / OWNER_RECORD).read_bytes(), f"owner=W2\nclaimed={stamp}\n".encode())
        self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"])

    def test_a_git_directory_or_a_tree_that_is_a_link_is_refused_by_the_open_and_the_target_gets_nothing(self):
        """The round-1 P2 (:377): the shell checked `.git` and then entered it by path, so a link planted between the
        check and the `cd` sent the claim into the link's target. The program opens the tree and its `.git` with
        `O_NOFOLLOW` and works through that descriptor, so the open is the check: a `.git` that is a link to another
        tree's real `.git`, and a tree that is a link to another tree, each refuse both verbs with exit 2 naming the
        link, and the target gains no record, no lock and no temporary. (Neither form has a step a test can hold
        between a check and the open; the refusal and the untouched target are what this test pins.)"""
        target = self.make_tree()
        (self.root / "wt/U9").mkdir()
        (self.root / "wt/U9/.git").symlink_to(target / ".git")
        (self.root / "wt/U10").symlink_to(target)
        git_link = f"{self.root}/wt/U9/.git is a symbolic link; a worker tree's .git is the directory the lever made"
        tree_link = f"the tree {self.root}/wt/U10 is a symbolic link; a worker tree is the directory the lever made"
        for verb, unit, message in (
            ("claim", "U9", git_link),
            ("release", "U9", git_link),
            ("claim", "U10", tree_link),
            ("release", "U10", tree_link),
        ):
            with self.subTest(verb=verb, unit=unit):
                run = self.run_lever(*self.verb_args(verb, unit, "W1"))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr, f"worker-worktree.sh: refused: {message}\n")
                self.assertEqual(self.owner_entries(target), [], "nothing reached the link's target")

    def test_a_record_holding_a_nul_byte_is_malformed_for_both_verbs_and_left_in_place(self):
        """The round-1 P2 (:399): `$(…)` drops a NUL, so `owner=W<NUL>1` read as `W1`, a claim was refused in W1's
        name and a release by W1 removed the record. The program matches the record's bytes whole, so a NUL anywhere
        in it is malformed: both verbs exit 2 with one stderr line naming the two-line shape, and the bytes are left
        for the operator."""
        path = self.make_tree()
        stamp = self.write_record(path, "W1", 1)
        record = path / OWNER_RECORD
        for body in (
            f"owner=W\x001\nclaimed={stamp}\n".encode(),
            f"owner=W1\x00\nclaimed={stamp}\n".encode(),
            f"\x00owner=W1\nclaimed={stamp}\n".encode(),
            f"owner=W1\nclaimed={stamp}\n\x00".encode(),
            f"owner=W1\nclaimed={stamp}\x00\n".encode(),
        ):
            record.write_bytes(body)
            for verb, owner in (("claim", "W2"), ("release", "W1")):
                with self.subTest(body=body, verb=verb):
                    run = self.run_lever(*self.verb_args(verb, "U7", owner, stamp))
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                    self.assertIn(
                        f"the owner record {path}/.git/regime-owner is not the two lines owner=<name> and "
                        "claimed=<YYYY-MM-DDTHH:MM:SSZ>; remove it by hand",
                        run.stderr,
                    )
                    self.assertEqual(record.read_bytes(), body, "left for the operator, as stderr says")

    def test_an_impossible_date_in_the_record_is_malformed_and_a_leap_day_is_a_date(self):
        """The round-1 P2 (:336): the shell accepted any day up to 31 and any second up to 60, so `2026-02-31` was
        read as a time and released. The stamp is parsed with `strptime` and must print back to itself: February 31,
        April 31, February 29 of a common year, hour 24 and second 60 are each malformed for both verbs (exit 2,
        one line, the bytes left), and a real leap day is read, so its owner releases it."""
        path = self.make_tree()
        record = path / OWNER_RECORD
        for stamp in (
            "2026-02-31T05:00:00Z",
            "2026-04-31T05:00:00Z",
            "2027-02-29T05:00:00Z",
            "2026-11-13T24:00:00Z",
            "2026-11-13T05:00:60Z",
        ):
            body = f"owner=W1\nclaimed={stamp}\n".encode()
            record.write_bytes(body)
            for verb, owner in (("claim", "W2"), ("release", "W1")):
                with self.subTest(stamp=stamp, verb=verb):
                    run = self.run_lever(*self.verb_args(verb, "U7", owner, stamp))
                    self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                    self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                    self.assertIn(f"the owner record {path}/.git/regime-owner is not the two lines", run.stderr)
                    self.assertEqual(record.read_bytes(), body, "left for the operator, as stderr says")
        record.write_bytes(b"owner=W1\nclaimed=2028-02-29T05:00:00Z\n")
        run = self.run_lever("release", "U7", "W1", "2028-02-29T05:00:00Z")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "released U7 owner=W1\n", ""))
        self.assertFalse(record.exists())

    def test_a_stale_count_outside_1_to_6_digits_is_refused_before_anything_is_read(self):
        """The round-1 P2 (:459): `$((10#n))` overflowed, so `--stale 9223372036854775808` went negative and took
        over a claim of age 0. `--stale` is 1 to 6 decimal digits: the overflowing count, a seventh digit, a sign, an
        exponent, a space and an empty value each refuse with exit 2 and one line naming the value, the live record
        untouched and no lock written; `999999` is a count and refuses the live claim with exit 3; `000000` is 0 and
        takes over."""
        path = self.make_tree()
        stamp = self.write_record(path, "W1", 0)
        record = (path / OWNER_RECORD).read_bytes()
        for value in ("9223372036854775808", "1000000", "0000000", "+5", "1e3", "-1", " 5", "", "٥"):
            with self.subTest(stale=value):
                run = self.run_lever("claim", "U7", "W2", "--stale", value)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(f"--stale {value} is not a count of minutes", run.stderr)
                self.assertEqual((path / OWNER_RECORD).read_bytes(), record)
                self.assertEqual(self.owner_entries(path), ["regime-owner"], "refused before the tree is opened")
        run = self.run_lever("claim", "U7", "W2", "--stale", "999999")
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertIn(f"is owned by W1 (claimed {stamp}, 0 min ago)", run.stderr)
        self.assertEqual((path / OWNER_RECORD).read_bytes(), record)
        since = self.now()
        run = self.run_lever("claim", "U7", "W2", "--stale", "000000")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W2", since)
        self.assertEqual(run.stdout, f"taken over U7 from=W1 age=0m owner=W2 claimed={stamp}\n")

    def test_a_failed_write_after_the_exclusive_create_leaves_no_empty_record_and_no_temporary(self):
        """The round-1 P2 (:415): a write that failed after the exclusive create left an empty record and exit 3, and
        the takeover's temporary leaked. Under a file-size limit of 0 (`RLIMIT_FSIZE`, so the create succeeds and the
        first `write` is EFBIG) a fresh claim exits 1 with one stderr line naming the record and the error, no record
        and no temporary are left (the lock file alone), and a takeover exits 1 the same way with the stale record
        byte-identical and no temporary; the plain claim then succeeds."""
        path = self.make_tree()
        run = self.run_lever("claim", "U7", "W1", preexec_fn=self.no_file_may_grow)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(
            run.stderr.startswith(
                f"worker-worktree.sh: failed: cannot write the owner record {path}/.git/regime-owner: "
            ),
            run.stderr,
        )
        self.assertIn("(EFBIG)", run.stderr)
        self.assertIn("removed", run.stderr)
        self.assertEqual(self.owner_entries(path), ["regime-owner.lock"], "no empty record, no temporary")
        self.write_record(path, "W1", 25)
        record = (path / OWNER_RECORD).read_bytes()
        run = self.run_lever("claim", "U7", "W2", preexec_fn=self.no_file_may_grow)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertIn(f"cannot write the owner record {path}/.git/regime-owner: ", run.stderr)
        self.assertEqual((path / OWNER_RECORD).read_bytes(), record, "the stale record stands")
        self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"], "no temporary left")
        since = self.now()
        run = self.run_lever("claim", "U7", "W2")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W2", since)
        self.assertEqual(run.stdout, f"taken over U7 from=W1 age=25m owner=W2 claimed={stamp}\n")

    def test_a_record_that_cannot_be_read_refuses_both_verbs_in_one_line_and_is_left(self):
        """Standing order 21 for the record read (the round-1 P2 on the tests, :1212: neither verb had a committed
        failing-read test): a record of mode 000 cannot be opened, and both verbs refuse with exit 2 and one stderr
        line naming the record and the error, never an absence (no fresh claim, no `no claim`); the bytes are as
        they were. Root reads a mode 000 file, so the refusal cannot be forced there and the test skips."""
        if os.geteuid() == 0:
            self.skipTest("root reads a mode 000 record, so the unreadable-record refusal cannot be forced")
        path = self.make_tree()
        stamp = self.write_record(path, "W1", 1)
        record = path / OWNER_RECORD
        record.chmod(0)
        self.addCleanup(record.chmod, 0o600)
        for verb, owner in (("claim", "W2"), ("release", "W1")):
            with self.subTest(verb=verb):
                run = self.run_lever(*self.verb_args(verb, "U7", owner, stamp))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertTrue(
                    run.stderr.startswith(
                        f"worker-worktree.sh: refused: cannot read the owner record {path}/.git/regime-owner"
                    ),
                    run.stderr,
                )
                self.assertEqual(stat.S_IMODE(record.lstat().st_mode), 0)
        record.chmod(0o600)
        self.assertEqual(record.read_bytes(), f"owner=W1\nclaimed={stamp}\n".encode())

    # Round 3 (verdicts/U509e-d8529b25.md, U509f): the release's identity, the grammars matched whole, the lock's mode
    # under the umask, the program's read, pin and hash refusals, and the one-line refusal.

    def test_a_release_presents_the_claim_it_releases_so_a_same_name_successor_s_record_stands(self):
        """The round-2 P1 (:351): the release compared the owner's name alone, so a successor that reused the name
        (the documented `<unit>Worker` form, so every round's worker is `U7Worker`) could have its fresh claim
        deleted by the previous worker's delayed release. A release presents the claim it releases, `release <unit>
        <owner> <claimed>`, the claim time the claim printed: W1's stale claim is taken over by a second W1 (the
        line prints the new claim time), the first W1's release, delayed past that takeover (held at its record
        read) and also run afterwards, is refused with exit 3 naming the record's claim and the one presented, and
        the successor's record is byte-identical; the old form without a claim time and a claim time outside the
        grammar are refused by shape (exit 2) with the record untouched; the successor's own release removes it."""
        path = self.make_tree()
        first = self.write_record(path, "W1", 25)
        hold = self.hold(once=True)
        late = self.start_lever("release", "U7", "W1", first, PATH=hold.path)
        try:
            hold.wait_for(1, (late,))
            since = self.now()
            run = self.run_lever("claim", "U7", "W1", PATH=hold.path)
            self.assertEqual((run.returncode, run.stderr), (0, ""))
            second = self.assert_record(path, "W1", since)
            self.assertEqual(run.stdout, f"taken over U7 from=W1 age=25m owner=W1 claimed={second}\n")
            self.assertNotEqual(first, second)
            record = (path / OWNER_RECORD).read_bytes()
            hold.release()
            out, err = late.communicate(timeout=120)
        finally:
            if late.poll() is None:
                late.kill()
        refused = (
            f"worker-worktree.sh: refused: the tree {path} is owned by W1 since {second}, not the claim of {first} "
            "this release presents; a later claim by the same name stands\n"
        )
        self.assertEqual((late.returncode, out, err), (3, "", refused))
        self.assertEqual((path / OWNER_RECORD).read_bytes(), record, "the successor's record stands")
        run = self.run_lever("release", "U7", "W1", first)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (3, "", refused), "and after the takeover too")
        self.assertEqual((path / OWNER_RECORD).read_bytes(), record)
        for argv, message in (
            (("release", "U7", "W1"), "release names the claim it releases: release <unit> <owner> <claimed>"),
            (("release", "U7", "W1", "yesterday"), "the claim time yesterday is not YYYY-MM-DDTHH:MM:SSZ"),
        ):
            with self.subTest(argv=argv):
                run = self.run_lever(*argv)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual((path / OWNER_RECORD).read_bytes(), record)
        run = self.run_lever("release", "U7", "W1", second)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "released U7 owner=W1\n", ""))
        self.assertEqual(self.owner_entries(path), ["regime-owner.lock"])

    def test_an_argument_ending_in_a_newline_is_outside_its_grammar(self):
        """The round-2 P2 (:153): Python's `$` admits a final newline, so an owner `W1<LF>` passed the grammar, exit
        0, and the record written held three lines, which no later run could read; the unit and `--stale` grammars
        shared the gap. Every grammar is matched whole: an owner, a unit, a `--stale` count and a release's claim
        time ending in a newline each refuse with exit 2 and one stderr line naming the value with the newline
        escaped, and nothing is written (no record, no lock, no tree of the newline name)."""
        path = self.make_tree()
        for argv, message in (
            (("claim", "U7", "W1\n"), "the owner W1\\n is not a name over [A-Za-z0-9._-]{1,64}"),
            (("claim", "U7\n", "W1"), "the unit U7\\n is not U<n> or U<n><letter>"),
            (("claim", "U7", "W1", "--stale", "5\n"), "--stale 5\\n is not a count of minutes of 1 to 6 digits"),
            (("release", "U7", "W1\n", ANY_STAMP), "the owner W1\\n is not a name over"),
            (("release", "U7", "W1", ANY_STAMP + "\n"), f"the claim time {ANY_STAMP}\\n is not YYYY-MM-DDTHH:MM:SSZ"),
        ):
            with self.subTest(argv=argv):
                run = self.run_lever(*argv)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("worker-worktree.sh: refused: "), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(self.owner_entries(path), [], "nothing written: no record, no lock")
                self.assertEqual(sorted(entry.name for entry in (self.root / "wt").iterdir()), ["U7"])

    def test_a_rejected_value_holding_a_newline_is_refused_in_one_line(self):
        """The round-2 P3 (:154): a rejected owner holding a newline was printed verbatim, so the one-line refusal
        ran over two stderr lines. Every refusal passes the one-line sink: a newline, a carriage return, a tab and a
        backslash in a rejected owner, unit or `--stale` value print as `\\n`, `\\r`, `\\t` and `\\\\`, one line,
        exit 2, nothing written."""
        path = self.make_tree()
        for argv, message in (
            (("claim", "U7", "W\n1"), "the owner W\\n1 is not a name over [A-Za-z0-9._-]{1,64}"),
            (("claim", "U7", "W\r1"), "the owner W\\r1 is not a name over"),
            (("claim", "U7", "W\t1"), "the owner W\\t1 is not a name over"),
            (("claim", "U7", "a\\nb"), "the owner a\\\\nb is not a name over"),
            (("claim", "U7", "W\x011"), "the owner W\\x011 is not a name over"),
            (("claim", "U\n7", "W1"), "the unit U\\n7 is not U<n> or U<n><letter>"),
            (("claim", "U7", "W1", "--stale", "5\n5"), "--stale 5\\n5 is not a count of minutes"),
            (("release", "U7", "W1", "2026\n-11-13T05:00:00Z"), "the claim time 2026\\n-11-13T05:00:00Z is not"),
        ):
            with self.subTest(argv=argv):
                run = self.run_lever(*argv)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("worker-worktree.sh: refused: "), run.stderr)
                self.assertTrue(run.stderr.endswith("\n"), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(self.owner_entries(path), [])

    def test_a_claim_under_a_closed_umask_leaves_a_lock_and_a_record_of_mode_0600(self):
        """The round-2 P2 (:217): the lock was created with mode 0600 reduced by the umask and never corrected, so
        under umask 0777 the first claim passed and left a mode-000 lock, and every later claim and release refused
        with EACCES. The lock and the record's temporary are `fchmod`ed after their open: a fresh claim, a release
        and a takeover under umask 0777 each pass, the lock and the record are 0600 afterwards, and a run under the
        caller's own umask follows them."""
        path = self.make_tree()

        def closed():
            os.umask(0o777)

        since = self.now()
        run = self.run_lever("claim", "U7", "W1", preexec_fn=closed)
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W1", since)
        self.assertEqual(stat.S_IMODE((path / OWNER_LOCK).lstat().st_mode), 0o600, "the lock's mode, umask or not")
        run = self.run_lever("release", "U7", "W1", stamp, preexec_fn=closed)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "released U7 owner=W1\n", ""))
        self.write_record(path, "W1", 25)
        since = self.now()
        run = self.run_lever("claim", "U7", "W2", preexec_fn=closed)
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W2", since)
        self.assertEqual(run.stdout, f"taken over U7 from=W1 age=25m owner=W2 claimed={stamp}\n")
        self.assertEqual(self.owner_entries(path), ["regime-owner", "regime-owner.lock"])
        self.assertEqual(stat.S_IMODE((path / OWNER_LOCK).lstat().st_mode), 0o600)
        run = self.run_lever("release", "U7", "W2", stamp)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "released U7 owner=W2\n", ""))
        run = self.run_lever("claim", "U7", "W3")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assert_record(path, "W3", since)

    def test_an_unreadable_program_a_missing_pin_or_a_differing_hash_refuses_the_owner_subcommands_with_nothing_written(
        self,
    ):
        """The round-2 P2 on the tests (:344): the lever's read of its program, the pin's presence and the hash
        comparison had no committed failure-injection test. Through the installed layout (the lever, the program and
        the manifest under the scratch HOME, the checkout's bytes), the program of mode 000, the manifest without
        the program's pin line and the program with one appended line each refuse both verbs with exit 2, one
        stderr line naming the file, nothing on stdout (the appended line never runs) and no claim: no record, no
        lock. The intact layout claims and releases through the installed copy. Root reads a mode 000 file, so that
        case is skipped there."""
        path = self.make_tree()
        lever = self.install_lever()
        program = lever.parent / "worker-worktree-owner.py"
        manifest = self.root / "home/.agents/agent-config.yaml"
        original = program.read_bytes()
        text = manifest.read_text()
        pin_line = next(line for line in text.splitlines() if line.startswith("      worker-worktree-owner.py: "))
        cases = [
            (
                "a missing pin",
                lambda: manifest.write_text(text.replace(pin_line + "\n", "")),
                lambda: manifest.write_text(text),
                f"no single sha256 pin for worker-worktree-owner.py in {manifest}",
            ),
            (
                "a differing hash",
                lambda: program.write_bytes(original + b'print("rewritten")\n'),
                lambda: program.write_bytes(original),
                f"of {program} differs from the pin in {manifest}; the program is not the pinned one",
            ),
        ]
        if os.geteuid() != 0:
            cases.insert(
                0,
                (
                    "an unreadable program",
                    lambda: program.chmod(0),
                    lambda: program.chmod(0o755),
                    f"cannot read {program}",
                ),
            )
        for label, inject, restore, message in cases:
            inject()
            try:
                for verb in ("claim", "release"):
                    with self.subTest(case=label, verb=verb):
                        run = self.run_lever(*self.verb_args(verb, "U7", "W1"), lever=lever)
                        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                        self.assertTrue(run.stderr.startswith("worker-worktree.sh: refused: "), run.stderr)
                        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                        self.assertIn(message, run.stderr)
                        self.assertNotIn("rewritten", run.stdout + run.stderr)
                        self.assertEqual(self.owner_entries(path), [], "no claim: no record, no lock")
            finally:
                restore()
        self.assertEqual(program.read_bytes(), original)
        since = self.now()
        run = self.run_lever("claim", "U7", "W1", lever=lever)
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        stamp = self.assert_record(path, "W1", since)
        self.assertEqual(run.stdout, f"claimed U7 owner=W1 claimed={stamp}\n")
        run = self.run_lever("release", "U7", "W1", stamp, lever=lever)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "released U7 owner=W1\n", ""))

    # The dispatch text and the return check (regime-cutover U573): `task` and `verify`, the two subcommands the
    # coordinator runs around every dispatch. Each test is red at a113750c0, where both verbs are unknown (`task U7
    # <brief>` is three arguments read as the unit `task`, `verify U7` two arguments: each a refusal, exit 2).

    def seats_root(self):
        """regime-env's seats root for the scratch checkout: `~/.local/state/omp-seats/<slug>` under the scratch
        HOME, the slug the checkout's basename."""
        return self.root / "home/.local/state/omp-seats/checkout"

    def make_seat(self, name, root=None):
        """A seat checkout NAME under the seats root ROOT (default regime-env's): a clone of the origin, clean."""
        path = (root or self.seats_root()) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        git_clone(self.origin, path, env=self.env, cwd=self.root)
        return path

    def fabricate_worktree(self, name, path):
        """The `.git/worktrees/<name>` entry of the checkout that `git worktree add PATH` records, written by hand
        so nothing at PATH is touched: `git worktree list` lists it (prunable), so a root outside the scratch tree
        (`/private/tmp/dotfiles-wt`) is judged without a write there."""
        entry = self.checkout / ".git/worktrees" / name
        entry.mkdir(parents=True)
        (entry / "gitdir").write_text(f"{path}/.git\n")
        (entry / "HEAD").write_text("ref: refs/heads/main\n")
        (entry / "commondir").write_text("../..\n")
        return entry

    def task_line_1(self, path):
        """The first line of the task text for the tree PATH, the brief's words: the tree and the first command."""
        return (
            f"Tree: {path} (every command runs here; your first command is `cd {path} && pwd -P`, "
            "and the report's first line is its output)"
        )

    def assert_refused(self, run, message):
        """RUN was refused: exit 2, nothing on stdout, one stderr line in the lever's form holding MESSAGE."""
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertTrue(run.stderr.startswith("worker-worktree.sh: refused: "), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertIn(message, run.stderr)

    def dirty_line(self, seat, paths):
        """The finding for the seat checkout SEAT with PATHS changed, deleted, untracked or staged (in the lever's
        order, `sort -u` under LC_ALL=C): the seat, the count, every path and the step, which names no command."""
        return (
            f"dirty seat checkout {seat} ({len(paths)} paths changed, deleted, untracked or staged: {', '.join(paths)}): "
            "a worker writes in its own tree alone; move the work out by hand, then restore the seat checkout to its head"
        )

    def clearing_commands(self, line):
        """The commands a foreign-worktree finding LINE ends with: the `worktree remove`, and the `branch -d` of the
        branch that worktree was on, or None when it was detached or on the checkout's own branch."""
        tail = line.split("; move any work out by hand, then ", 1)[1]
        remove = tail.split(" (git -C ", 1)[0]
        delete = None
        if "), then " in tail:
            delete = tail.split("), then ", 1)[1].split(", the branch that worktree was on", 1)[0]
        return remove, delete

    def test_task_renders_the_tree_the_brief_the_branch_the_base_and_the_forbidden_paths_in_their_places(self):
        """`task <unit> <brief> [--round <text>]` prints the text the coordinator pastes into the worker's Task
        call: line 1 names the tree and the first command `cd <tree> && pwd -P` in the brief's words, then the
        brief, the branch the tree is on with the base it was made from (the creation, not where `origin/main` or
        the head is now), the no-push rule, the forbidden paths (the main checkout and every seat checkout under
        regime-env's seats root by name, the `.`-directories left out, an absent root holding none) and the round
        text only when given; an explicit `REGIME_SEATS_ROOT` wins over the derived one; nothing is written in the
        checkout, the tree or the seats."""
        path = self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        sweep = self.make_seat("sweep-3")
        audit = self.make_seat("audit")
        (self.seats_root() / ".state").mkdir()
        (self.seats_root() / ".sandbox").mkdir()
        before = (self.checkout_state(), self.listing(path), self.listing(self.seats_root()))
        run = self.run_lever("task", "U7", str(brief))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        lines = run.stdout.splitlines()
        self.assertEqual(lines[0], self.task_line_1(path))
        self.assertTrue(lines[1].startswith(f"Brief: {brief} ("), lines[1])
        self.assertTrue(
            lines[2].startswith(f"Branch: feat/u7, which the tree is on, made by worker-worktree.sh from {self.main} "),
            lines[2],
        )
        self.assertIn("`git worktree list` in any checkout cannot show it", lines[2])
        self.assertTrue(
            lines[3].startswith(f"No push: the tree has no push path (remote.origin.pushurl {PUSHURL}"), lines[3]
        )
        self.assertIn("the coordinator fetches it by path and pushes", lines[3])
        self.assertEqual(
            lines[4],
            "Forbidden paths (standing order 27; never run git or edit files there): "
            f"the main checkout {self.checkout}; the seat checkouts under {self.seats_root()}: {audit}, {sweep}.",
        )
        self.assertEqual(len(lines), 5, "no Round line without --round")
        self.assertNotIn(".state", run.stdout)
        self.assertNotIn(".sandbox", run.stdout)
        self.assertEqual((self.checkout_state(), self.listing(path), self.listing(self.seats_root())), before)
        run = self.run_lever("task", "U7", str(brief), "--round", "round 2: the verdict's P2 at :12")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertEqual(run.stdout.splitlines(), [*lines, "Round: round 2: the verdict's P2 at :12"])
        # the base is the one the tree was made from: origin/main moves in the checkout and in the tree, the worker
        # commits, and the text still names the creation base
        (self.checkout / "README").write_text("main two\n")
        self.git("commit", "-q", "-am", "main two")
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin", cwd=path)
        self.commit_work(path)
        run = self.run_lever("task", "U7", str(brief))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertIn(f"made by worker-worktree.sh from {self.main} ", run.stdout)
        other = self.root / "other-seats"
        other.mkdir()
        seat = self.make_seat("worker-2", root=other)
        run = self.run_lever("task", "U7", str(brief), REGIME_SEATS_ROOT=str(other))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertIn(f"the seat checkouts under {other}: {seat}.", run.stdout)
        self.assertNotIn(str(sweep), run.stdout)
        run = self.run_lever("task", "U7", str(brief), REGIME_SEATS_ROOT=str(self.root / "absent"))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertIn(f"no seat checkout under the seats root {self.root / 'absent'}.", run.stdout)

    def test_task_refuses_a_missing_or_foreign_tree_and_a_brief_that_is_not_there(self):
        """A task is never rendered for a tree that is not there or not the lever's: a unit with no tree, a bare
        directory, a `.git` that is a file (a linked worktree of the checkout under the root, the U566 shape) or a
        symbolic link, a repository with no alternates or with another repository's, one with another origin, one
        whose push path is open (no pushurl) and a detached tree each refuse with exit 2 and one stderr line naming
        the tree; so do a brief that is relative, absent or unreadable, a unit outside the grammar, `--round`
        without a text, a wrong argument count, and a read that fails (the tree's origin, its reflog; standing order
        21): nothing on stdout, the checkout and every tree unchanged."""
        path = self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        wt = self.root / "wt"
        (wt / "U8").mkdir()
        (wt / "U9").mkdir()
        (wt / "U9/.git").symlink_to(path / ".git")
        self.git("worktree", "add", "-q", str(wt / "U10"), "-b", "feat/u10")
        git_init(wt / "U11", env=self.env, cwd=self.root)
        other = git_init(wt / "U12", env=self.env, cwd=self.root)
        (other / ".git/objects/info/alternates").write_text(f"{self.origin}/objects\n")
        self.git("config", "remote.origin.url", str(self.origin), cwd=other)
        self.git("config", "remote.origin.pushurl", PUSHURL, cwd=other)
        self.make_tree("U13")
        self.git("config", "remote.origin.url", f"{self.root}/elsewhere.git", cwd=wt / "U13")
        self.make_tree("U14")
        self.git("config", "--unset", "remote.origin.pushurl", cwd=wt / "U14")
        self.make_tree("U15")
        self.git("checkout", "-q", "--detach", cwd=wt / "U15")
        unreadable = self.root / "unreadable.md"
        unreadable.write_text("# U7\n")
        before = (self.checkout_state(), self.listing(wt))
        cases = [
            (("task", "U16", str(brief)), {}, f"the tree {wt}/U16 does not exist"),
            (("task", "U8", str(brief)), {}, f"{wt}/U8 is no worker repository: {wt}/U8/.git is not a directory"),
            (("task", "U9", str(brief)), {}, f"{wt}/U9/.git is a symbolic link"),
            (
                ("task", "U10", str(brief)),
                {},
                f"{wt}/U10 is no worker repository: {wt}/U10/.git is not a directory (a linked worktree holds a file",
            ),
            (
                ("task", "U11", str(brief)),
                {},
                f"{wt}/U11 is no worker repository of this checkout: cannot read {wt}/U11/.git/objects/info/alternates",
            ),
            (
                ("task", "U12", str(brief)),
                {},
                f"{wt}/U12 is no worker repository of this checkout: its alternates {self.origin}/objects is not the "
                f"objects directory {self.checkout}/.git/objects of {self.checkout}",
            ),
            (
                ("task", "U13", str(brief)),
                {},
                f"{wt}/U13 is no worker repository of this checkout: its origin {self.root}/elsewhere.git is not the "
                f"checkout's {self.origin}",
            ),
            (
                ("task", "U14", str(brief)),
                {},
                f"{wt}/U14 is no worker repository: its push path is not removed (no remote.origin.pushurl)",
            ),
            (
                ("task", "U15", str(brief)),
                {},
                f"cannot read the branch of {wt}/U15 (HEAD is detached, or the read failed)",
            ),
            (
                ("task", "U7", str(brief)),
                failing(f"-C {path} config --get remote.origin.url"),
                f"cannot read remote.origin.url of {path}",
            ),
            (
                ("task", "U7", str(brief)),
                failing("log -g --format=%H refs/heads/feat/u7"),
                f"cannot read the reflog of feat/u7 in {path}",
            ),
            (("task", "U7", "brief.md"), {}, "the brief brief.md is not an absolute path"),
            (
                ("task", "U7", str(self.root / "absent.md")),
                {},
                f"the brief {self.root}/absent.md is not a readable file",
            ),
            (("task", "7", str(brief)), {}, "the unit 7 is not U<n> or U<n><letter>"),
            (
                ("task", "U7", str(brief), "--round"),
                {},
                "usage: worker-worktree.sh task <unit> <brief> [--round <text>]",
            ),
            (("task", "U7", str(brief), "--round", ""), {}, "--round needs a text"),
            (("task", "U7", str(brief), "--later", "x"), {}, "usage: worker-worktree.sh task <unit> <brief>"),
            (("task", "U7"), {}, "usage: worker-worktree.sh task <unit> <brief>"),
            (("task",), {}, "usage: worker-worktree.sh task <unit> <brief>"),
        ]
        if os.geteuid() != 0:
            unreadable.chmod(0)
            cases.append((("task", "U7", str(unreadable)), {}, f"the brief {unreadable} is not a readable file"))
        for argv, env, message in cases:
            with self.subTest(argv=argv, env=env):
                self.assert_refused(self.run_lever(*argv, **env), message)
        self.assertEqual((self.checkout_state(), self.listing(wt)), before)

    def test_verify_passes_on_a_clean_fixture_and_names_a_foreign_worktree_under_each_root(self):
        """`verify <unit>` exits 0 on a tree the lever made beside a clean seat checkout, one `verified` line; a
        linked worktree of the main checkout under `$DOTFILES_WT`, under `${TMPDIR}/dotfiles-wt`, under
        `/private/tmp/dotfiles-wt` (the U566 shape, planted as the `.git/worktrees` entry alone, so nothing outside
        the scratch root is written) or anywhere else under a `dotfiles-wt` directory is each one stdout line naming
        the path, the root or the `dotfiles-wt` component, the `git worktree remove` and, for an entry on a branch of
        its own, the `git branch -d` of that branch after it (the planted entry is on the checkout's own branch,
        which no stray add made, so it names none), exit 1, all four in one run (the lever spells no temporary
        directory of its own, so the last two are the component rule's); a linked worktree elsewhere and the main
        worktree are never named; without TMPDIR the `${TMPDIR}/dotfiles-wt` one is still named, by its component;
        with the entries gone the fixture verifies again; nothing is written anywhere."""
        self.make_tree()
        self.make_seat("sweep-3")
        tmpdir = self.root / "scratch-tmp"
        tmpdir.mkdir()
        run = self.run_lever("verify", "U7", TMPDIR=str(tmpdir))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        verified = (
            f"verified U7: no foreign worktree of {self.checkout} under {self.root}/wt or dotfiles-wt under TMPDIR, "
            f"none with a dotfiles-wt path component; 1 seat checkouts clean under {self.seats_root()}\n"
        )
        self.assertEqual(run.stdout, verified)
        self.git("worktree", "add", "-q", str(self.root / "wt/U8"), "-b", "feat/u8")
        self.git("worktree", "add", "-q", str(tmpdir / "dotfiles-wt/U9"), "-b", "feat/u9")
        self.git("worktree", "add", "-q", str(self.root / "elsewhere/U10"), "-b", "feat/u10")
        self.git("worktree", "add", "-q", str(self.root / "other/dotfiles-wt/U11"), "-b", "feat/u11")
        entry = self.fabricate_worktree("U566", "/private/tmp/dotfiles-wt/U566")
        self.assertIn("worktree /private/tmp/dotfiles-wt/U566\n", self.worktrees() + "\n")
        before = (self.checkout_state(), self.listing(self.root / "wt"), self.listing(self.seats_root()))
        run = self.run_lever("verify", "U7", TMPDIR=str(tmpdir))
        self.assertEqual((run.returncode, run.stderr), (1, ""))
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 4, run.stdout)
        for foreign, root, branch in (
            (f"{self.root}/wt/U8", f"{self.root}/wt", "feat/u8"),
            (f"{tmpdir}/dotfiles-wt/U9", f"{tmpdir}/dotfiles-wt", "feat/u9"),
            ("/private/tmp/dotfiles-wt/U566", "a dotfiles-wt directory", None),
            (f"{self.root}/other/dotfiles-wt/U11", "a dotfiles-wt directory", "feat/u11"),
        ):
            with self.subTest(foreign=foreign):
                line = next(line for line in lines if line.startswith(f"foreign worktree {foreign} "))
                self.assertIn(f"of the main checkout {self.checkout} under {root}:", line)
                remove, delete = self.clearing_commands(line)
                self.assertEqual(remove, f"git -C {self.checkout} worktree remove --force {foreign}")
                self.assertEqual(delete, f"git -C {self.checkout} branch -d {branch}" if branch else None)
        self.assertNotIn("reset --hard", run.stdout, "no finding names a destructive command")
        self.assertNotIn("branch -D", run.stdout, "no finding names a destructive command")
        self.assertNotIn("elsewhere", run.stdout)
        self.assertNotIn(f"worktree {self.checkout} ", run.stdout)
        self.assertEqual(
            (self.checkout_state(), self.listing(self.root / "wt"), self.listing(self.seats_root())), before
        )
        # without TMPDIR in the environment the TMPDIR root is not among the roots, and the worktree under it is still
        # named, by its dotfiles-wt component
        run = self.run_lever("verify", "U7", TMPDIR=None)
        self.assertEqual((run.returncode, run.stderr), (1, ""))
        self.assertEqual(len(run.stdout.splitlines()), 4, run.stdout)
        self.assertIn(
            f"foreign worktree {tmpdir}/dotfiles-wt/U9 of the main checkout {self.checkout} under a dotfiles-wt directory:",
            run.stdout,
        )
        for name in ("wt/U8", "scratch-tmp/dotfiles-wt/U9", "elsewhere/U10", "other/dotfiles-wt/U11"):
            self.git("worktree", "remove", "--force", str(self.root / name))
        shutil.rmtree(entry)
        run = self.run_lever("verify", "U7", TMPDIR=str(tmpdir))
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, verified, ""))

    def test_verify_names_a_dirty_seat_checkout_and_a_staged_change(self):
        """A seat checkout under the seats root with a changed tracked file and an untracked one (the U565 shape) is
        one stdout line naming the seat, the count and the step that clears it; a seat whose only change is staged
        (the index against HEAD, which the working-tree read cannot see) is named too; exit 1 with every line
        printed; a clean seat and a `.`-directory are not named; the read writes nothing in the seat, not even its
        index; an explicit `REGIME_SEATS_ROOT` is the root judged; a local branch of the main checkout named like the
        tree's is no finding (round 3, Codex thread 4604357806: the checkout may hold it from before the tree was
        made); cleared, the fixture verifies."""
        path = self.make_tree()
        sweep = self.make_seat("sweep-3")
        audit = self.make_seat("audit")
        staged = self.make_seat("staged")
        (self.seats_root() / ".state").mkdir()
        (sweep / "README").write_text("dirt\n")
        (sweep / "stray.txt").write_text("stray\n")
        (staged / "README").write_text("staged\n")
        self.git("add", "README", cwd=staged)
        self.git("branch", "feat/u7", "main")
        indexes = ((sweep / ".git/index").read_bytes(), (staged / ".git/index").read_bytes())
        before = (self.checkout_state(), self.listing(path), self.listing(self.seats_root()))
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""))
        self.assertEqual(
            run.stdout.splitlines(),
            [self.dirty_line(staged, ["README"]), self.dirty_line(sweep, ["README", "stray.txt"])],
        )
        self.assertNotIn(str(audit), run.stdout)
        self.assertNotIn("branch -D", run.stdout, "the checkout's branch feat/u7 is no finding")
        self.assertNotIn("reset --hard", run.stdout, "no finding names a destructive command")
        self.assertNotIn("diff HEAD", run.stdout, "no finding advises the diff as the backup")
        self.assertEqual((self.checkout_state(), self.listing(path), self.listing(self.seats_root())), before)
        self.assertEqual(
            ((sweep / ".git/index").read_bytes(), (staged / ".git/index").read_bytes()),
            indexes,
            "the status read wrote no index",
        )
        other = self.root / "other-seats"
        worker = self.make_seat("worker-2", root=other)
        (worker / "stray.txt").write_text("stray\n")
        run = self.run_lever("verify", "U7", REGIME_SEATS_ROOT=str(other))
        self.assertEqual((run.returncode, run.stderr), (1, ""))
        self.assertEqual(run.stdout.splitlines(), [self.dirty_line(worker, ["stray.txt"])])
        self.git("checkout", "--", ".", cwd=sweep)
        (sweep / "stray.txt").unlink()
        self.git("reset", "-q", "--hard", "HEAD", cwd=staged)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertTrue(run.stdout.endswith(f"; 3 seat checkouts clean under {self.seats_root()}\n"), run.stdout)
        self.assertEqual(self.git("rev-parse", "refs/heads/feat/u7"), self.main, "the checkout's branch stands")

    def test_verify_refuses_a_failed_read_instead_of_passing(self):
        """Standing order 21 for the return check: a `git worktree list` that fails, a tree whose branch cannot be
        read, a seat whose toplevel, filter drivers, working-tree listing or index comparison cannot be read (exit
        128 from the PATH `git`), a seat directory that is no repository, a seats root that cannot be listed (mode
        000), regime-env refusing (an empty HOME), an absent tree, a tree that is a linked worktree of the checkout,
        a run from a linked worktree, a unit outside the grammar and a wrong argument count each exit 2 with one
        stderr line naming the read, nothing on stdout: never exit 0, never a finding."""
        path = self.make_tree()
        sweep = self.make_seat("sweep-3")
        self.git("worktree", "add", "-q", str(self.root / "wt/U9"), "-b", "feat/u9")
        cases = [
            (
                ("verify", "U7"),
                failing("worktree list --porcelain"),
                f"cannot read git worktree list of {self.checkout}",
            ),
            (("verify", "U7"), failing("symbolic-ref --quiet HEAD"), f"cannot read the branch of {path}"),
            (
                ("verify", "U7"),
                failing(f"-C {sweep} rev-parse --show-toplevel"),
                f"cannot read the toplevel of the seat checkout {sweep}",
            ),
            (
                ("verify", "U7"),
                failing("config --name-only --get-regexp"),
                f"cannot read the filter drivers of the seat checkout {sweep}",
            ),
            (("verify", "U7"), failing("ls-files -z -m -d -o"), f"cannot read the status of the seat checkout {sweep}"),
            (
                ("verify", "U7"),
                failing("diff-index --cached --name-only -z HEAD"),
                f"cannot read the status of the seat checkout {sweep}",
            ),
            (("verify", "U7"), {"HOME": ""}, "regime-env: HOME is empty, so no store root can be derived under it"),
            (("verify", "U8"), {}, f"the tree {self.root}/wt/U8 does not exist"),
            (
                ("verify", "U9"),
                {},
                f"{self.root}/wt/U9 is no worker repository: {self.root}/wt/U9/.git is not a directory",
            ),
            (("verify", "u7"), {}, "the unit u7 is not U<n> or U<n><letter>"),
            (("verify",), {}, "usage: worker-worktree.sh verify <unit>"),
            (("verify", "U7", "extra"), {}, "usage: worker-worktree.sh verify <unit>"),
        ]
        for argv, env, message in cases:
            with self.subTest(argv=argv, env=env):
                self.assert_refused(self.run_lever(*argv, **env), message)
        run = self.run_lever("verify", "U7", cwd=self.root / "wt/U9")
        self.assert_refused(run, "is a linked worktree")
        self.assertIn("run from the main checkout", run.stderr)
        probe = self.seats_root() / "probe"
        probe.mkdir()
        self.assert_refused(self.run_lever("verify", "U7"), f"cannot read the toplevel of the seat checkout {probe}")
        probe.rmdir()
        if os.geteuid() != 0:
            self.seats_root().chmod(0)
            try:
                self.assert_refused(self.run_lever("verify", "U7"), f"cannot list the seats root {self.seats_root()}")
            finally:
                self.seats_root().chmod(0o755)
        self.git("worktree", "remove", "--force", str(self.root / "wt/U9"))
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)

    # Round 2 of U573 (verdicts/U573-32986760.md): each read below passed as an absence in round 1, and each test is
    # red against that lever.

    def test_a_caller_s_git_environment_does_not_reach_regime_env_s_derivation(self):
        """regime-env runs git of its own for the toplevel the seats root's slug comes from: with the caller's
        `GIT_DIR` pointing at the worker tree, round 1 derived the tree's slug, judged no seat and passed over a dirty
        one, and the caller's `GIT_TRACE` made a file (P1 :526). Every `GIT_*` name is removed before regime-env is
        sourced now: `verify` still names the dirty seat, `task` still lists it among the forbidden paths, and no
        trace file appears."""
        path = self.make_tree()
        sweep = self.make_seat("sweep-3")
        (sweep / "stray.txt").write_text("stray\n")
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        trace = self.root / "git-trace.log"
        env = {"GIT_DIR": str(path / ".git"), "GIT_WORK_TREE": str(path), "GIT_TRACE": str(trace)}
        run = self.run_lever("verify", "U7", **env)
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 1, run.stdout)
        self.assertTrue(
            lines[0].startswith(
                f"dirty seat checkout {sweep} (1 paths changed, deleted, untracked or staged: stray.txt)"
            ),
            lines[0],
        )
        self.assertFalse(trace.exists(), "no git the run caused wrote the caller's GIT_TRACE file")
        run = self.run_lever("task", "U7", str(brief), **env)
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertIn(f"the seat checkouts under {self.seats_root()}: {sweep}.", run.stdout)
        self.assertFalse(trace.exists(), "no git the run caused wrote the caller's GIT_TRACE file")

    def test_an_unsearchable_directory_above_the_seats_root_is_a_failed_read_not_an_absence(self):
        """A file test below a directory this user cannot search answers false for EACCES as for ENOENT: with the
        parent of the seats root at mode 000, round 1 read the root as absent and `verify` passed over a dirty seat
        (P1 :529). The walk from `/` refuses the first directory that cannot be searched, by name, exit 2 with nothing
        on stdout, for `verify` and `task` alike; searchable again, the dirty seat is named, and a root that is cleanly
        absent is still no seat."""
        if os.geteuid() == 0:
            self.skipTest("root searches every directory")
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        (sweep / "stray.txt").write_text("stray\n")
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        parent = self.seats_root().parent
        parent.chmod(0)
        try:
            for argv in (("verify", "U7"), ("task", "U7", str(brief))):
                with self.subTest(argv=argv):
                    self.assert_refused(
                        self.run_lever(*argv),
                        f"cannot search the directory {parent} (permission denied), so whether the seats root "
                        f"{self.seats_root()} exists cannot be read",
                    )
        finally:
            parent.chmod(0o755)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertIn(f"dirty seat checkout {sweep} (1 paths", run.stdout)
        run = self.run_lever("verify", "U7", REGIME_SEATS_ROOT=str(self.root / "absent/seats"))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertTrue(run.stdout.endswith(f"; 0 seat checkouts clean under {self.root}/absent/seats\n"), run.stdout)

    def test_a_branch_the_checkout_holds_is_no_finding_and_a_stray_worktree_s_own_branch_is_its_leftover(self):
        """Codex thread 4604357806 on round 2: `verify` named a local branch of the checkout for being named like the
        tree's branch, as the `git worktree add` leftover, and advised `git branch -D`; a branch the checkout held
        before the tree was made is a supported case (the creation subcommand's own
        `test_a_branch_the_checkout_holds_is_no_conflict_and_the_name_is_the_normalized_one`), so that advice could
        discard its commits. The checkout holds `feat/u7` with a commit of its own before the tree is made: `verify`
        exits 0, names no `branch -d` or `-D`, and the branch keeps its commit. A stray linked worktree on a branch of
        its own is named with that branch's `branch -d` after its `worktree remove`, the leftover of that worktree
        alone; a detached one with none; the printed commands, run in order, clear the fixture."""
        self.git("checkout", "-q", "-b", "feat/u7")
        (self.checkout / "own.txt").write_text("own\n")
        self.git("add", "own.txt")
        self.git("commit", "-q", "-m", "own")
        own = self.git("rev-parse", "HEAD")
        self.git("checkout", "-q", "main")
        self.make_tree()
        self.make_seat("sweep-3")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertNotIn("branch", run.stdout)
        self.assertEqual(self.git("rev-parse", "refs/heads/feat/u7"), own)
        self.git("worktree", "add", "-q", str(self.root / "wt/U8"), "-b", "feat/u8")
        self.git("worktree", "add", "-q", "--detach", str(self.root / "wt/U9"))
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 2, run.stdout)
        self.assertNotIn("feat/u7", run.stdout, "the checkout's branch is not named")
        on_branch = next(line for line in lines if line.startswith(f"foreign worktree {self.root}/wt/U8 "))
        detached = next(line for line in lines if line.startswith(f"foreign worktree {self.root}/wt/U9 "))
        remove, delete = self.clearing_commands(on_branch)
        self.assertEqual(
            (remove, delete),
            (
                f"git -C {self.checkout} worktree remove --force {self.root}/wt/U8",
                f"git -C {self.checkout} branch -d feat/u8",
            ),
        )
        self.assertTrue(
            on_branch.endswith(
                "(the leftover of its worktree add -b; -d refuses a branch with unmerged commits, inspect it before "
                "-D; keep a branch the checkout held before the stray add)"
            ),
            on_branch,
        )
        remove_detached, delete_detached = self.clearing_commands(detached)
        self.assertEqual(
            (remove_detached, delete_detached),
            (f"git -C {self.checkout} worktree remove --force {self.root}/wt/U9", None),
        )
        for command in (remove, delete, remove_detached):
            cleared = subprocess.run(["bash", "-c", command], env=self.env, capture_output=True, text=True, timeout=120)
            self.assertEqual(cleared.returncode, 0, (command, cleared.stderr))
        self.assertNotIn("U8", self.worktrees())
        self.assertNotIn("U9", self.worktrees())
        status, _, _ = self.git_status("rev-parse", "--verify", "--quiet", "refs/heads/feat/u8")
        self.assertNotEqual(status, 0, "the stray worktree's own branch is gone")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(self.git("rev-parse", "refs/heads/feat/u7"), own, "the checkout's branch keeps its commit")

    def test_a_seat_s_fsmonitor_or_hook_runs_nothing_during_the_status_read(self):
        """`--no-optional-locks` keeps the status from writing the seat's index and does not keep a configured
        `core.fsmonitor` from running inside it: round 1 ran a seat's fsmonitor program during `verify` (P2 :594). The
        status runs with `-c core.fsmonitor=false -c core.hooksPath=/dev/null` now: a seat whose config names a
        marker-writing fsmonitor script leaves no marker, the seat is judged as before (clean, then dirty), and the
        same script does run under a plain `git status` in the seat, so the fixture is live."""
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        marker = self.root / "fsmonitor-ran"
        script = self.root / "fsmonitor.sh"
        script.write_text(f"#!/bin/sh\ntouch {marker}\nprintf '/'\n")
        script.chmod(0o755)
        self.git("config", "core.fsmonitor", str(script), cwd=sweep)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertFalse(marker.exists(), "the seat's fsmonitor program did not run inside the status read")
        (sweep / "stray.txt").write_text("stray\n")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertIn(f"dirty seat checkout {sweep} (1 paths", run.stdout)
        self.assertFalse(marker.exists(), "the seat's fsmonitor program did not run inside the status read")
        self.git_status("status", "--porcelain", cwd=sweep)
        self.assertTrue(marker.exists(), "the fixture's fsmonitor program runs under a plain git status")

    def test_a_tag_named_like_the_branch_changes_nothing(self):
        """`symbolic-ref --short HEAD` prints `heads/<name>` when a tag shares the branch's name, so round 1 looked for
        `refs/heads/heads/<name>` and `task` refused the tree's reflog (P2 :511). The branch is the full ref now,
        `refs/heads/` stripped: with the tag in the tree and in the checkout, and the checkout holding a branch of
        the same name (no finding since round 3), `task` renders the branch with its base and `verify` passes."""
        path = self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        self.git("tag", "feat/u7", cwd=path)
        self.git("tag", "feat/u7")
        self.git("branch", "feat/u7", "main")
        run = self.run_lever("task", "U7", str(brief))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertIn(
            f"\nBranch: feat/u7, which the tree is on, made by worker-worktree.sh from {self.main} ", run.stdout
        )
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertTrue(run.stdout.startswith("verified U7: "), run.stdout)

    def test_a_foreign_worktree_whose_path_holds_a_newline_is_named_whole(self):
        """The line form of `git worktree list --porcelain` split a path holding a newline, so round 1 named a
        shortened path and printed a remove command for that wrong path (P2 :567). The list is read with `-z` and
        split on NUL now: the finding names the whole path on one line (its newline shown as `\\n`), and the commands
        it prints, quoted for the shell, remove that worktree and the branch it was on."""
        self.make_tree()
        self.make_seat("sweep-3")
        wt = self.root / "wt" / "U8\nx"
        try:
            wt.mkdir()
        except OSError as error:
            self.skipTest(f"the filesystem refuses a name holding a newline: {error}")
        wt.rmdir()
        self.git("worktree", "add", "-q", str(wt), "-b", "feat/u8")
        self.assertIn(f"worktree {wt}\n", self.worktrees() + "\n")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 1, run.stdout)
        shown = str(wt).replace("\n", "\\n")
        self.assertTrue(
            lines[0].startswith(
                f"foreign worktree {shown} of the main checkout {self.checkout} under {self.root}/wt: a worker tree"
            ),
            lines[0],
        )
        remove, delete = self.clearing_commands(lines[0])
        self.assertTrue(remove.startswith(f"git -C {self.checkout} worktree remove --force $'"), remove)
        self.assertEqual(delete, f"git -C {self.checkout} branch -d feat/u8")
        for command in (remove, delete):
            cleared = subprocess.run(["bash", "-c", command], env=self.env, capture_output=True, text=True, timeout=120)
            self.assertEqual(cleared.returncode, 0, (command, cleared.stderr))
        self.assertNotIn("U8", self.worktrees(), "the printed command removed the worktree it named")
        self.assertFalse(wt.exists())
        status, _, _ = self.git_status("rev-parse", "--verify", "--quiet", "refs/heads/feat/u8")
        self.assertNotEqual(status, 0, "the printed command deleted the branch that worktree was on")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)

    def test_a_unit_holding_a_newline_is_one_refusal_line(self):
        """Every refusal is one stderr line: a unit text holding a newline made two lines in round 1 (P3 :681). Each
        line boundary in the interpolated text is folded to a space now, for `verify` and `task` alike."""
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        for argv in (("verify", "U7\nextra"), ("task", "U7\nextra", str(brief)), ("verify", "U7\rextra")):
            with self.subTest(argv=argv):
                self.assert_refused(self.run_lever(*argv), "the unit U7 extra is not U<n> or U<n><letter>")

    # Round 3 of U573 (verdicts/U573-5f983ea2.md and the Codex threads on the round-2 pull request): each test below
    # is red against the round-2 lever at 5f983ea2f.

    def test_a_link_or_a_file_above_the_seats_root_is_a_failed_read_not_an_absence(self):
        """The carried P1 (:575, round 2's :529): a symbolic link on the way to the seats root whose target lay under
        a mode-000 directory read as absent (`-L` saw the link, `-d` could not see through it), and a regular file
        where a directory should be (ENOTDIR) read as a root holding no seat; each let `verify` pass over a dirty
        seat. The walk follows a link to its target and judges the target's path by the same rule: a target under an
        unsearchable directory refuses naming that directory, a mode-000 target refuses naming the target (not the
        link), and a file on the way refuses naming the file, exit 2 with nothing on stdout, for `verify` and `task`
        alike; searchable again, the dirty seat is named under the root as given; a dangling link stays a clean
        absence."""
        self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        closed = self.root / "closed"
        seat = self.make_seat("worker-2", root=closed / "target/seats")
        (seat / "stray.txt").write_text("stray\n")
        (self.root / "via").symlink_to("closed/target")
        unsearchable = self.root / "unsearchable"
        unsearchable.mkdir()
        (self.root / "via2").symlink_to(unsearchable)
        afile = self.root / "afile"
        afile.write_text("")
        (self.root / "dangling").symlink_to(self.root / "nowhere")
        cases = [
            (
                f"{self.root}/afile/seats",
                f"{afile}, which the seats root {self.root}/afile/seats lies under, is not a directory, so the seats "
                f"root {self.root}/afile/seats cannot be read",
            )
        ]
        if os.geteuid() != 0:
            closed.chmod(0)
            unsearchable.chmod(0)
            cases += [
                (
                    f"{self.root}/via/seats",
                    f"cannot search the directory {closed} (permission denied), so whether the seats root "
                    f"{self.root}/via/seats exists cannot be read",
                ),
                (
                    f"{self.root}/via2/seats",
                    f"cannot search the directory {unsearchable} (permission denied), so whether the seats root "
                    f"{self.root}/via2/seats exists cannot be read",
                ),
            ]
        try:
            for seats_root, message in cases:
                for argv in (("verify", "U7"), ("task", "U7", str(brief))):
                    with self.subTest(seats_root=seats_root, argv=argv):
                        self.assert_refused(self.run_lever(*argv, REGIME_SEATS_ROOT=seats_root), message)
        finally:
            closed.chmod(0o755)
            unsearchable.chmod(0o755)
        run = self.run_lever("verify", "U7", REGIME_SEATS_ROOT=f"{self.root}/via/seats")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertEqual(run.stdout.splitlines(), [self.dirty_line(f"{self.root}/via/seats/worker-2", ["stray.txt"])])
        run = self.run_lever("verify", "U7", REGIME_SEATS_ROOT=f"{self.root}/dangling/seats")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertTrue(run.stdout.endswith(f"; 0 seat checkouts clean under {self.root}/dangling/seats\n"), run.stdout)

    def test_a_failed_git_read_inside_regime_env_is_a_refusal_under_an_explicit_store_and_seats_root(self):
        """P1 :597: regime_env reads the checkout's toplevel in a substitution and, under an explicit `HCOM_DIR`,
        returns 0 when that read fails (the explicit store needs no slug); under an explicit `REGIME_SEATS_ROOT` as
        well, round 2 went on and passed. The lever reads that toplevel through regime-env's own `regime_toplevel`
        first, its status judged, and hands the value to `regime_env`, which then runs no git: with the second
        `rev-parse --git-common-dir` of the run (the first is the lever's own checkout read, which
        `FAKE_GIT_FAIL_SKIP` lets pass) exiting 128, `verify` and `task` refuse with exit 2 naming the read, nothing
        on stdout; without the injection both pass, and the run holds exactly two such reads, so regime-env's own
        never ran."""
        self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        other = self.root / "other-seats"
        self.make_seat("worker-2", root=other)
        env = {"HCOM_DIR": str(self.root / "hcom"), "REGIME_SEATS_ROOT": str(other)}
        injected = {**env, **failing("rev-parse --path-format=absolute --git-common-dir"), "FAKE_GIT_FAIL_SKIP": "1"}
        for argv in (("verify", "U7"), ("task", "U7", str(brief))):
            with self.subTest(argv=argv, injected=True):
                self.assert_refused(
                    self.run_lever(*argv, **injected),
                    "cannot read the toplevel regime-env derives the seats root from (git rev-parse or pwd -P in "
                    f"{self.checkout} failed)",
                )
            with self.subTest(argv=argv, injected=False):
                run = self.run_lever(*argv, **env)
                self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
                reads = [call for call in self.git_calls.read_text().splitlines() if "--git-common-dir" in call]
                self.assertEqual(len(reads), 2, reads)

    def test_a_seat_s_clean_filter_runs_nothing_during_the_status_read(self):
        """P2 :700 and Codex thread 4604459522: round 2's `git status` hashed a changed file of the same length
        through the seat's clean filter (git decides a same-size change by content, the step a clean filter runs
        in), so a filter the seat's config names ran during `verify` and wrote a file. The read closes every filter
        driver the seat's config defines by name (`-c filter.<name>.clean= ... required=false`) and is `ls-files -m
        -d -o` with `diff-index --cached`, no `status`: a seat whose `.gitattributes` assigns a required filter whose
        clean command writes a marker, with a same-length change, is named dirty and the marker is not written; the
        same change under a plain `git status` in the seat does write it, so the fixture is live."""
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        marker = self.root / "clean-filter-ran"
        script = self.root / "clean.sh"
        script.write_text(f"#!/bin/sh\ntouch {marker}\nexec cat\n")
        script.chmod(0o755)
        (sweep / ".gitattributes").write_text("README filter=marker\n")
        self.git("add", ".gitattributes", cwd=sweep)
        self.git("commit", "-q", "-m", "attributes", cwd=sweep)
        self.git("config", "filter.marker.clean", str(script), cwd=sweep)
        self.git("config", "filter.marker.required", "true", cwd=sweep)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertFalse(marker.exists())
        (sweep / "README").write_text("mane\n")  # the same length as the committed `main\n`
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertEqual(run.stdout.splitlines(), [self.dirty_line(sweep, ["README"])])
        self.assertFalse(marker.exists(), "the seat's clean filter did not run inside the read")
        calls = [json.loads(line) for line in self.git_calls.read_text().splitlines()]
        self.assertFalse([call for call in calls if "status" in call], "no git status runs in a seat")
        self.assertTrue([call for call in calls if "filter.marker.clean=" in call and "ls-files" in call], calls)
        self.git_status("status", "--porcelain", cwd=sweep)
        self.assertTrue(marker.exists(), "the fixture's clean filter runs under a plain git status")

    def test_containment_under_a_root_is_judged_by_identity_not_spelling(self):
        """P2 :677: round 2 compared the listed path and the root as strings, as printed and as `pwd -P` resolves
        them, and `pwd -P` keeps the letter case it was given, so `DOTFILES_WT` spelled in another case on a
        case-insensitive volume passed over a foreign worktree under the same directory. Each listed path and each
        directory above it is tested against the roots with `-ef` now: the case alias names the worktree under it
        (skipped where the volume is case-sensitive), and an entry whose directory is gone, spelled through a
        symbolic link to the root (so neither spelling matches), is named under the root as well; with the entries
        gone the fixture verifies."""
        self.make_tree()
        self.make_seat("sweep-3")
        wt = self.root / "wt"
        alias = self.root / "WT"
        self.git("worktree", "add", "-q", str(wt / "U8"), "-b", "feat/u8")
        with self.subTest(spelling="a case alias of the root"):
            if not (alias.exists() and os.path.samefile(alias, wt)):
                self.skipTest("the volume is case-sensitive, so WT is no alias of wt")
            run = self.run_lever("verify", "U7", DOTFILES_WT=str(alias))
            self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
            lines = run.stdout.splitlines()
            self.assertEqual(len(lines), 1, run.stdout)
            self.assertTrue(
                lines[0].startswith(f"foreign worktree {wt}/U8 of the main checkout {self.checkout} under {alias}:"),
                lines[0],
            )
        self.git("worktree", "remove", "--force", str(wt / "U8"))
        self.git("branch", "-D", "feat/u8")
        link = self.root / "link"
        link.symlink_to(wt)
        entry = self.fabricate_worktree("U9", link / "U9")
        self.assertIn(f"worktree {link}/U9\n", self.worktrees() + "\n")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 1, run.stdout)
        self.assertTrue(
            lines[0].startswith(f"foreign worktree {link}/U9 of the main checkout {self.checkout} under {wt}:"),
            lines[0],
        )
        self.assertNotIn("branch -D", lines[0], "an entry on the checkout's own branch names no branch to delete")
        shutil.rmtree(entry)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)

    def test_a_seat_whose_path_holds_a_newline_is_one_seat(self):
        """P2 :605: the seats listing was one path per line, so a seat whose name holds a newline was two names, the
        first no repository (`verify` refused a clean seat) and `task` rendered the forbidden paths in pieces. The
        listing is NUL-separated now: a dirty seat named so is one finding naming the whole path on one line (its
        newline shown as `\\n`, the commands quoting it for the shell), and `task` lists it whole on the
        forbidden-paths line."""
        self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        other = self.root / "other-seats"
        other.mkdir()
        try:
            (other / "w\n2").mkdir()
        except OSError as error:
            self.skipTest(f"the filesystem refuses a name holding a newline: {error}")
        (other / "w\n2").rmdir()
        seat = self.make_seat("w\n2", root=other)
        (seat / "stray.txt").write_text("stray\n")
        shown = str(seat).replace("\n", "\\n")
        run = self.run_lever("verify", "U7", REGIME_SEATS_ROOT=str(other))
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 1, run.stdout)
        self.assertTrue(lines[0].startswith(f"dirty seat checkout {shown} (1 paths changed"), lines[0])
        self.assertIn(": stray.txt): a worker writes in its own tree alone", lines[0])
        run = self.run_lever("task", "U7", str(brief), REGIME_SEATS_ROOT=str(other))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 5, run.stdout)
        self.assertTrue(lines[4].endswith(f"the seat checkouts under {other}: {shown}."), lines[4])

    def test_regime_env_s_refusal_is_one_stderr_line(self):
        """P3 :597 (round 2's :681 carried): regime-env printed its refusal to stderr itself, past the lever's
        one-line fold, so a HOME holding a newline with a store root component regime-env refuses (`.local` a
        symbolic link) made three stderr lines. regime_env runs in a captured substitution now and its words reach
        stderr through `refuse`: one line, exit 2, nothing on stdout, the newline folded to a space."""
        self.make_tree()
        home = self.root / "ho\nme"
        try:
            home.mkdir()
        except OSError as error:
            self.skipTest(f"the filesystem refuses a name holding a newline: {error}")
        (self.root / "elsewhere").mkdir()
        (home / ".local").symlink_to(self.root / "elsewhere")
        run = self.run_lever("verify", "U7", HOME=str(home))
        self.assert_refused(
            run, f"regime-env: the store root component {home}/.local is a symlink; the store root".replace("\n", " ")
        )

    def test_a_foreign_worktree_path_holding_a_carriage_return_is_one_finding_line(self):
        """P3 :641: the finding escaped a newline in the path and nothing else, so a path holding a carriage return
        (or a vertical tab or a form feed, the other characters a text reader ends a line at) split its finding in
        two for the reader. Each is escaped now (`\\r`, `\\v`, `\\f`): three such worktrees are three lines, each
        naming the whole path, and the printed commands remove each with its branch."""
        self.make_tree()
        self.make_seat("sweep-3")
        trees = []
        for unit, char, escaped in (("U8", "\r", "\\r"), ("U9", "\v", "\\v"), ("U10", "\f", "\\f")):
            wt = self.root / "wt" / f"{unit}{char}x"
            try:
                wt.mkdir()
            except OSError as error:
                self.skipTest(f"the filesystem refuses a name holding {escaped}: {error}")
            wt.rmdir()
            self.git("worktree", "add", "-q", str(wt), "-b", f"feat/{unit.lower()}")
            trees.append((wt, str(wt).replace(char, escaped), f"feat/{unit.lower()}"))
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 3, run.stdout)
        for wt, shown, branch in trees:
            with self.subTest(path=shown):
                line = next(line for line in lines if line.startswith(f"foreign worktree {shown} "))
                remove, delete = self.clearing_commands(line)
                self.assertEqual(delete, f"git -C {self.checkout} branch -d {branch}")
                for command in (remove, delete):
                    cleared = subprocess.run(
                        ["bash", "-c", command], env=self.env, capture_output=True, text=True, timeout=120
                    )
                    self.assertEqual(cleared.returncode, 0, (command, cleared.stderr))
                self.assertFalse(wt.exists())
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)

    # Round 4 of U573 (verdicts/U573-5a5aa7fa.md): each test below is red against the round-3 lever at 5a5aa7fa4.

    def test_no_finding_names_a_destructive_command_and_a_stray_branch_s_unmerged_commit_survives_the_printed_steps(
        self,
    ):
        """P1 :875 and P1 :728: the dirty-seat finding advised `git diff HEAD` as the backup and `reset --hard`, and
        the diff omits binary bytes and a staged version cancelled by an unstaged edit; the foreign-worktree finding
        ended in `branch -D`, which drops the last reference of a commit the stray worktree made with an empty
        working-tree diff. No finding names a destructive command now: the dirty seat's line names the seat and
        every changed path and says to move the work out by hand and then restore the seat checkout to its head
        (the lever changes nothing: the staged blob and the binary bytes stand), and the foreign worktree's line
        names `worktree remove --force` after `move any work out by hand` and then `branch -d`, which refuses the
        branch with the unmerged commit, so the commit keeps its reference after the printed steps are run."""
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        (sweep / "README").write_text("staged\n")
        self.git("add", "README", cwd=sweep)
        (sweep / "README").write_text("main\n")  # the working tree cancels the staged version: `git diff HEAD` is empty
        (sweep / "blob.bin").write_bytes(bytes(range(256)))
        staged_blob = self.git("rev-parse", ":README", cwd=sweep)
        self.assertEqual(self.git("diff", "HEAD", "--", "README", cwd=sweep), "", "the fixture's diff is empty")
        wt = self.root / "wt/U8"
        self.git("worktree", "add", "-q", str(wt), "-b", "feat/u8")
        (wt / "work.txt").write_text("work\n")
        self.git("add", "work.txt", cwd=wt)
        self.git("commit", "-q", "-m", "stray work", cwd=wt)
        stray = self.git("rev-parse", "HEAD", cwd=wt)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 2, run.stdout)
        for word in ("reset --hard", "branch -D", "diff HEAD", "clean -"):
            self.assertNotIn(word, run.stdout, word)
        self.assertIn(self.dirty_line(sweep, ["README", "blob.bin"]), lines)
        foreign = next(line for line in lines if line.startswith(f"foreign worktree {wt} "))
        self.assertIn("; move any work out by hand, then git -C ", foreign)
        remove, delete = self.clearing_commands(foreign)
        self.assertEqual(remove, f"git -C {self.checkout} worktree remove --force {wt}")
        self.assertEqual(delete, f"git -C {self.checkout} branch -d feat/u8")
        self.assertTrue(
            foreign.endswith(
                "(the leftover of its worktree add -b; -d refuses a branch with unmerged commits, inspect it before "
                "-D; keep a branch the checkout held before the stray add)"
            ),
            foreign,
        )
        self.assertEqual(self.git("rev-parse", ":README", cwd=sweep), staged_blob, "the read changed nothing")
        self.assertEqual((sweep / "blob.bin").read_bytes(), bytes(range(256)))
        removed = subprocess.run(["bash", "-c", remove], env=self.env, capture_output=True, text=True, timeout=120)
        self.assertEqual(removed.returncode, 0, removed.stderr)
        deleted = subprocess.run(["bash", "-c", delete], env=self.env, capture_output=True, text=True, timeout=120)
        self.assertNotEqual(deleted.returncode, 0, "branch -d refuses the branch with the unmerged commit")
        self.assertIn("not fully merged", deleted.stderr)
        self.assertEqual(self.git("rev-parse", "refs/heads/feat/u8"), stray, "the stray commit keeps its reference")

    def test_a_name_too_long_or_a_link_chain_too_deep_above_the_seats_root_is_a_failed_read_not_an_absence(self):
        """P1 :617 (the carried :575): `[[ -e ]]` answers false for ENAMETOOLONG and ELOOP as for ENOENT, so a seats
        root with a component longer than the system allows, or under a chain of symbolic links deeper than the
        kernel follows, read as absent and `verify` passed with no seat judged. Where a test answers false the path
        is read once more with `/usr/bin/stat` now, and only `No such file or directory` is an absence: the long name
        refuses naming the component and stat's `File name too long`; the chain (40 links, within the walk's own
        ceiling and deeper than the 32 macOS follows) refuses with `Too many levels of symbolic links` where the
        kernel refuses it, and where the kernel follows it (Linux follows 40) the dirty seat under it is named; a
        cleanly absent root is still no seat; `task` refuses alike."""
        self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        long_name = "x" * 300
        long_root = f"{self.root}/{long_name}/seats"
        for argv in (("verify", "U7"), ("task", "U7", str(brief))):
            with self.subTest(argv=argv, case="ENAMETOOLONG"):
                run = self.run_lever(*argv, REGIME_SEATS_ROOT=long_root)
                self.assert_refused(run, f"cannot look up {self.root}/{long_name} (")
                self.assertIn("File name too long", run.stderr)
                self.assertIn(f"so whether the seats root {long_root} exists cannot be read", run.stderr)
        target = self.root / "target"
        seat = self.make_seat("worker-2", root=target / "seats")
        (seat / "stray.txt").write_text("stray\n")
        links = [self.root / f"l{index}" for index in range(1, 41)]
        for link, following in zip(links, [*links[1:], target]):
            link.symlink_to(following)
        chained_root = f"{links[0]}/seats"
        try:
            os.stat(chained_root)
            kernel_refuses = False
        except OSError as error:
            if error.errno != errno.ELOOP:
                raise
            kernel_refuses = True
        for argv in (("verify", "U7"), ("task", "U7", str(brief))):
            with self.subTest(argv=argv, case="ELOOP", kernel_refuses=kernel_refuses):
                run = self.run_lever(*argv, REGIME_SEATS_ROOT=chained_root)
                if kernel_refuses:
                    self.assert_refused(run, "Too many levels of symbolic links")
                    self.assertIn(f"so whether the seats root {chained_root} exists cannot be read", run.stderr)
                elif argv[0] == "verify":
                    self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
                    self.assertEqual(
                        run.stdout.splitlines(), [self.dirty_line(f"{chained_root}/worker-2", ["stray.txt"])]
                    )
                else:
                    self.assertEqual((run.returncode, run.stderr), (0, ""))
                    self.assertIn(f"the seat checkouts under {chained_root}: {chained_root}/worker-2.", run.stdout)
        run = self.run_lever("verify", "U7", REGIME_SEATS_ROOT=f"{self.root}/absent/seats")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertTrue(run.stdout.endswith(f"; 0 seat checkouts clean under {self.root}/absent/seats\n"), run.stdout)

    def test_a_seat_status_read_that_warns_is_a_failed_read_not_a_finding(self):
        """P2 :868 (the first): `git ls-files -o` warns `could not open directory` and exits 0 for a directory inside
        the seat it cannot read (the status-blind producer table), and round 3 merged that warning into the path
        data, so an incomplete read was a dirty finding instead of a refusal. The producer's stderr is captured
        apart from its paths now: a seat holding an untracked directory of mode 000 refuses with exit 2 naming the
        seat and git's words, nothing on stdout; readable again, the directory's file is the one path named."""
        if os.geteuid() == 0:
            self.skipTest("root reads every directory")
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        locked = sweep / "locked"
        locked.mkdir()
        (locked / "note.txt").write_text("note\n")
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o755)
        run = self.run_lever("verify", "U7")
        self.assert_refused(run, f"cannot read the status of the seat checkout {sweep}")
        self.assertIn("Permission denied", run.stderr)
        locked.chmod(0o755)
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertEqual(run.stdout.splitlines(), [self.dirty_line(sweep, ["locked/note.txt"])])

    def test_a_seat_holding_a_submodule_is_refused_by_name(self):
        """P2 :868 (the second): `ls-files -m` and `diff-index --cached` cannot see a change inside a submodule, so
        round 3 judged a seat clean while `git status --porcelain` reported its dirty submodule. A seat holding a
        submodule is refused by name now, before its status is read: one with a committed submodule (`.gitmodules`
        and a gitlink), one with a gitlink in its index alone, and one with a `.gitmodules` file alone each refuse
        with exit 2 naming the seat, nothing on stdout; a seat without one is judged as before."""
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        sub = self.make_seat("with-sub")
        self.git("-c", "protocol.file.allow=always", "submodule", "add", "-q", str(self.origin), "lib", cwd=sub)
        self.git("commit", "-q", "-m", "submodule", cwd=sub)
        (sub / "lib/README").write_text("inner dirt\n")
        self.assertIn("lib", self.git("status", "--porcelain", cwd=sub), "the fixture's submodule is dirty to git")
        run = self.run_lever("verify", "U7")
        self.assert_refused(run, f"the seat checkout {sub} holds a submodule (.gitmodules is present)")
        shutil.rmtree(sub)
        gitlink = self.make_seat("gitlink")
        self.git("update-index", "--add", "--cacheinfo", f"160000,{self.main},lib", cwd=gitlink)
        run = self.run_lever("verify", "U7")
        self.assert_refused(run, f"the seat checkout {gitlink} holds a submodule (the gitlink lib in its index)")
        shutil.rmtree(gitlink)
        modules = self.make_seat("modules")
        (modules / ".gitmodules").write_text("")
        run = self.run_lever("verify", "U7")
        self.assert_refused(run, f"the seat checkout {modules} holds a submodule (.gitmodules is present)")
        shutil.rmtree(modules)
        (sweep / "stray.txt").write_text("stray\n")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertEqual(run.stdout.splitlines(), [self.dirty_line(sweep, ["stray.txt"])])

    def test_the_task_text_and_the_verified_line_show_a_root_or_a_brief_holding_a_carriage_return_on_one_line(self):
        """P3 :927: `task` printed the tree's path raw, so a `DOTFILES_WT` holding a carriage return (which the root
        checks allow: a newline alone is refused) split the mandatory first line for a reader, and the brief's and
        the checkout's paths bypassed `display` too, as did the `verified` line's. Each goes through `display` now:
        with the root and the brief holding a carriage return, the task text is five lines, line 1 names the tree
        with `\\r` and the `cd` quotes the path for the shell, the brief line names the brief with `\\r`, and
        `verify`'s one line names the root with `\\r`; no raw carriage return is printed."""
        wt = self.root / "w\rt"
        try:
            wt.mkdir()
        except OSError as error:
            self.skipTest(f"the filesystem refuses a name holding a carriage return: {error}")
        run = self.run_lever("U7", "feat/u7", "origin/main", DOTFILES_WT=str(wt))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        path = wt / "U7"
        brief = self.root / "br\rief.md"
        brief.write_text("# U7\n")
        self.make_seat("sweep-3")
        shown_path = str(path).replace("\r", "\\r")
        shown_brief = str(brief).replace("\r", "\\r")
        shown_root = str(wt).replace("\r", "\\r")
        run = self.run_lever("task", "U7", str(brief), DOTFILES_WT=str(wt))
        self.assertEqual((run.returncode, run.stderr), (0, ""))
        self.assertNotIn("\r", run.stdout)
        lines = run.stdout.splitlines()
        self.assertEqual(len(lines), 5, run.stdout)
        self.assertEqual(
            lines[0],
            f"Tree: {shown_path} (every command runs here; your first command is `cd $'{shown_path}' && pwd -P`, "
            "and the report's first line is its output)",
        )
        self.assertTrue(lines[1].startswith(f"Brief: {shown_brief} ("), lines[1])
        self.assertTrue(
            lines[4].startswith(
                "Forbidden paths (standing order 27; never run git or edit files there): "
                f"the main checkout {self.checkout}; "
            ),
            lines[4],
        )
        run = self.run_lever("verify", "U7", DOTFILES_WT=str(wt))
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertNotIn("\r", run.stdout)
        self.assertEqual(
            run.stdout,
            f"verified U7: no foreign worktree of {self.checkout} under {shown_root} or dotfiles-wt under TMPDIR, "
            f"none with a dotfiles-wt path component; 1 seat checkouts clean under {self.seats_root()}\n",
        )

    def test_a_failing_uname_is_one_refusal_line_for_task_and_verify(self):
        """P3 :509: `stat_format_read` ran `uname -s` with its stderr uncaptured, so a failing uname printed its own
        line before the refusal, two stderr lines against the one-line contract. Its stderr is captured and folded
        into the refusal now: a PATH `uname` that prints a diagnostic and exits 1 is one stderr line naming the read
        and the words, exit 2, nothing on stdout, for `verify` and `task` alike."""
        self.make_tree()
        brief = self.root / "brief.md"
        brief.write_text("# U7\n")
        path = self.shim("uname", "-s", 'echo "fake-uname: no system name today" >&2; exit 1')
        for argv in (("verify", "U7"), ("task", "U7", str(brief))):
            with self.subTest(argv=argv):
                self.assert_refused(
                    self.run_lever(*argv, PATH=path),
                    "cannot read the operating system name (uname -s): fake-uname: no system name today",
                )

    def test_a_path_both_staged_and_changed_again_is_one_path(self):
        """P3 :873: the working-tree listing and the cached listing were concatenated, so a file with a staged change
        and another change in the working tree was counted twice. The two are deduplicated across each other now:
        such a file is one path, named once, beside an untracked file."""
        self.make_tree()
        sweep = self.make_seat("sweep-3")
        (sweep / "README").write_text("staged\n")
        self.git("add", "README", cwd=sweep)
        (sweep / "README").write_text("changed again\n")
        (sweep / "stray.txt").write_text("stray\n")
        self.assertEqual(self.git("status", "--porcelain", cwd=sweep).splitlines()[0], "MM README")
        run = self.run_lever("verify", "U7")
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertEqual(run.stdout.splitlines(), [self.dirty_line(sweep, ["README", "stray.txt"])])


if __name__ == "__main__":
    unittest.main()
