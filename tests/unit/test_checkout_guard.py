"""Exercise scripts/orchestrator/checkout-guard.sh and the reference-transaction hook it installs (regime-cutover U129).

Every test builds a scratch origin and a clone of it (the "checkout") under a scratch HOME (so the operator's global
git configuration is the scratch `~/.gitconfig`), installs the hook with the checkout copy of the lever and moves refs
with the user's plain git, the git that runs `.git/hooks/reference-transaction`. A second clone mints the commits
origin does not hold, which reach the checkout through `git fetch <path> <branch>` (FETCH_HEAD, no ref moves), the
way a worker's head reaches the coordinator's checkout. Nothing reads the real checkout or `~/.local/bin`.
"""

import ast
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_clone, git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/checkout-guard.sh"
HOOK = "reference-transaction"
ROUND1_HOOKS = ("pre-commit", "post-checkout")
PREFIX = "checkout-guard: "
ROUTE = (
    "commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one "
    "under $TMPDIR/dotfiles-wt/<unit> (standing order 29)"
)
REFUSAL = "checkout-guard: this checkout is the coordinator's; " + ROUTE
FAILED_READ = "the update is refused (standing order 21)"
ZERO = "0" * 40
# The expected bytes `install` and `check` write to the scratch directory before anything else: one `cat` per hook form
# (`reference-transaction`, `pre-commit`, `post-checkout`, `pre-commit.subst`); the next `cat` of an install is the
# write of the hook's bytes to the temporary file in the hooks directory.
SCRATCH_WRITES = 4
# githooks(5), reference-transaction: "For each reference update that was added to the transaction, the hook receives
# on standard input a line of the format: <old-value> SP <new-value> SP <ref-name> LF"; symbolic values are
# `ref:<ref-target>`; the exit status counts in the "preparing" and "prepared" states alone.
LINE = re.compile(r"^(?P<old>[0-9a-f]{40,64}|ref:\S+) (?P<new>[0-9a-f]{40,64}|ref:\S+) (?P<ref>\S+)\n$")


def round1_body(name):
    """The bytes round 1 wrote for hook NAME, kept in the lever's `write_hook` for the upgrade comparison: `pre-commit`
    as its heredoc reads, `pre-commit.subst` as bash 3.2's command substitution wrote it (`$'\\n'` expanded)."""
    tag = "ROUND1_" + name.upper().replace("-", "_").replace(".", "_")
    match = re.search(
        rf"cat << '{tag}' > \"\$2\" \|\| refuse \"cannot write \$2\"\n(.*?)\n{tag}\n", LEVER.read_text(), re.S
    )
    assert match, tag
    return (match.group(1) + "\n").encode()


class CheckoutGuardTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        # The identity lives in the scratch global config, not in GIT_* variables: the lever scrubs those from its
        # own git, and the moves below are the user's plain git, which reads this file.
        (self.home / ".gitconfig").write_text(
            "[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n"
        )
        self.env = quiet_git_env({"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"})
        self.origin = self.root / "origin"
        git_init(self.origin, env=self.env, cwd=self.root)
        (self.origin / "README").write_text("main\n")
        self.git("add", "README", cwd=self.origin)
        self.git("commit", "-q", "-m", "main", cwd=self.origin)
        self.checkout = self.clone(self.root / "checkout")
        self.hooks = self.checkout / ".git/hooks"
        # The commit origin does not hold: minted in another clone, fetched by path (FETCH_HEAD moves no ref).
        other = self.clone(self.root / "other")
        self.git("checkout", "-q", "-b", "work", cwd=other)
        (other / "work.txt").write_text("work\n")
        self.git("add", "work.txt", cwd=other)
        self.git("commit", "-q", "-m", "work", cwd=other)
        self.git("fetch", "-q", str(other), "work")
        self.work = self.git("rev-parse", "FETCH_HEAD")

    def clone(self, path):
        return git_clone(self.origin, path, env=self.env, cwd=self.root)

    def git(self, *args, cwd=None, env=None):
        status, out, err = self.git_status(*args, cwd=cwd, env=env)
        self.assertEqual(status, 0, err)
        return out

    def git_status(self, *args, cwd=None, env=None):
        """(exit status, stdout, stderr) of a git command that may fail."""
        run = subprocess.run(
            ["git", *args], cwd=cwd or self.checkout, env=env or self.env, capture_output=True, text=True, timeout=120
        )
        return run.returncode, run.stdout.strip(), run.stderr

    def run_lever(self, *args, env=None):
        return subprocess.run(
            [str(LEVER), *args], cwd=self.root, env=env or self.env, capture_output=True, text=True, timeout=120
        )

    def rows(self, stdout):
        return [tuple(line[len(PREFIX) :].split("\t")) for line in stdout.splitlines() if line.startswith(PREFIX)]

    def hooks_state(self):
        """Every entry of the hooks directory with its bytes and mode: what a run could have written."""
        if not self.hooks.exists():
            return None
        return {
            entry.name: (entry.read_bytes() if entry.is_file() else None, stat.S_IMODE(entry.lstat().st_mode))
            for entry in self.hooks.iterdir()
        }

    def store(self, checkout=None, program="pilot"):
        store = (checkout or self.checkout) / ".orchestration/orchestrate" / program
        store.mkdir(parents=True)
        (store / "units.tsv").write_text("unit\tstate\n")
        return store

    def install(self, checkout=None):
        run = self.run_lever("install", str(checkout or self.checkout))
        self.assertEqual(run.returncode, 0, run.stderr)
        return run

    def branches(self, cwd=None):
        """Every local branch with its commit, and HEAD's symbolic target (or its commit when detached)."""
        refs = self.git("for-each-ref", "--format=%(refname) %(objectname)", "refs/heads/", cwd=cwd)
        status, head, _ = self.git_status("symbolic-ref", "-q", "HEAD", cwd=cwd)
        if status != 0:
            head = "detached " + self.git("rev-parse", "HEAD", cwd=cwd)
        return refs, head

    def commit(self, cwd=None, *options, env=None):
        """Try one commit of a new file in CWD; (exit status, stderr, the head before)."""
        tree = cwd or self.checkout
        before = self.git("rev-parse", "HEAD", cwd=tree)
        name = f"work-{len(list(tree.iterdir()))}.txt"
        (tree / name).write_text("work\n")
        self.git("add", name, cwd=tree)
        status, _, err = self.git_status("commit", "-q", *options, "-m", "work", cwd=tree, env=env)
        return status, err, before

    def assert_refused(self, status, err, cwd=None):
        self.assertNotEqual(status, 0, err)
        self.assertIn(REFUSAL, err)
        self.assertIn("which no refs/remotes/origin/* ref reaches", err)

    def shim(self, pattern, status=128, name="git", nth=None):
        """The directory whose `NAME` (default `git`) exits STATUS on a call whose arguments hold PATTERN, else runs
        the real NAME from PATH. With NTH, only the NTH such call fails (the calls are counted in the `calls` file
        of the directory, read and written by the shell's builtins so a `cat` shim never runs itself; the caller
        removes the file between runs)."""
        real = shutil.which(name, path=self.env["PATH"])
        shims = Path(tempfile.mkdtemp(prefix=f"shim-{name}-", dir=self.root))
        failing = f'echo "shim: failing {name} {pattern}" >&2; exit {status}'
        if nth is None:
            decision = f"{failing} ;;"
        else:
            decision = (
                f'n=0; [ -f "{shims}/calls" ] && read -r n < "{shims}/calls"; n=$((n + 1)); '
                f'printf "%s\\n" "$n" > "{shims}/calls"; if [ "$n" -eq {nth} ]; then {failing}; fi ;;'
            )
        (shims / name).write_text(f'#!/bin/sh\ncase "$*" in\n*"{pattern}"*) {decision}\nesac\nexec "{real}" "$@"\n')
        (shims / name).chmod(0o755)
        return shims

    def hook_shim(self, pattern):
        """The env under which the hook's own `git` is the shim: git puts its exec path first on a hook's PATH, so
        a PATH shim never reaches a hook; `GIT_EXEC_PATH` names that directory, and the shim there runs the real git
        for everything but PATTERN (the outer command among it)."""
        return {**self.env, "GIT_EXEC_PATH": str(self.shim(pattern))}

    def test_install_on_a_main_checkout_writes_the_hook_and_a_second_install_is_a_no_op(self):
        """`install` writes `reference-transaction` into the checkout's hooks directory, mode 0755, and reads it back;
        `check` reports it installed; a second install finds its own hook, prints `unchanged` and leaves every byte
        and mode as it was; round 1's two hook paths are not written."""
        hook = self.hooks / HOOK
        before = self.run_lever("check", str(self.checkout))
        self.assertEqual(before.returncode, 1, before.stdout)
        self.assertEqual([("absent", str(hook))], self.rows(before.stdout))
        run = self.install()
        self.assertEqual([("installed", str(hook))], self.rows(run.stdout))
        self.assertEqual(stat.S_IMODE(hook.stat().st_mode), 0o755)
        text = hook.read_text()
        self.assertTrue(text.startswith("#!/usr/bin/env -S python3 -I -S\n"), text[:40])
        self.assertIn("worker-worktree.sh <unit> <branch> origin/main makes one ", text)
        self.assertIn("under $TMPDIR/dotfiles-wt/<unit> (standing order 29)", text)
        self.assertIn("# git-isolated: allow", text)
        self.assertIn('"-c", "core.hooksPath=/dev/null"', text)
        for name in ROUND1_HOOKS:
            self.assertFalse((self.hooks / name).exists(), name)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual([("installed", str(hook))], self.rows(check.stdout))
        state = self.hooks_state()
        again = self.install()
        self.assertEqual([("unchanged", str(hook))], self.rows(again.stdout))
        self.assertEqual(self.hooks_state(), state)
        # `install` works from a subdirectory of the checkout too: the toplevel is git's.
        (self.checkout / "sub").mkdir()
        deeper = self.run_lever("install", str(self.checkout / "sub"))
        self.assertEqual(deeper.returncode, 0, deeper.stderr)
        self.assertEqual([("unchanged", str(hook))], self.rows(deeper.stdout))

    def test_install_removes_round_1_s_hooks_and_leaves_any_other_file_at_their_paths(self):
        """An upgraded checkout holds round 1's `pre-commit` and `post-checkout`: `check` names each `stale` (exit 1),
        `install` writes the hook first and then removes each (`removed` rows), so no run leaves the checkout
        unguarded and none keeps a dead hook; a file of other content at either path (the operator's own, or a
        round-1 copy with one byte changed) is left alone and never reported."""
        subst = round1_body("pre-commit.subst")
        self.assertNotEqual(subst, round1_body("pre-commit"))
        self.assertEqual(subst.replace(b"'\n'", b"$'\\n'"), round1_body("pre-commit"), "one token apart")
        for pre_commit in (round1_body("pre-commit"), subst):
            (self.hooks / "pre-commit").write_bytes(pre_commit)
            (self.hooks / "post-checkout").write_bytes(round1_body("post-checkout"))
            for name in ROUND1_HOOKS:
                (self.hooks / name).chmod(0o755)
            check = self.run_lever("check", str(self.checkout))
            self.assertEqual(check.returncode, 1, check.stdout)
            self.assertEqual(
                [("absent", str(self.hooks / HOOK))] + [("stale", str(self.hooks / name)) for name in ROUND1_HOOKS],
                self.rows(check.stdout),
            )
            run = self.install()
            self.assertEqual(
                [("installed", str(self.hooks / HOOK))]
                + [("removed", str(self.hooks / name)) for name in ROUND1_HOOKS],
                self.rows(run.stdout),
            )
            for name in ROUND1_HOOKS:
                self.assertFalse((self.hooks / name).exists(), name)
            check = self.run_lever("check", str(self.checkout))
            self.assertEqual((check.returncode, self.rows(check.stdout)), (0, [("installed", str(self.hooks / HOOK))]))
            (self.hooks / HOOK).unlink()
        self.install()
        # Not round 1's bytes: left alone, not a row, not a refusal.
        changed = bytearray(round1_body("pre-commit"))
        changed[-2:] = b"1\n"
        (self.hooks / "pre-commit").write_bytes(bytes(changed))
        (self.hooks / "post-checkout").write_text("#!/bin/sh\nexit 0\n")
        state = self.hooks_state()
        run = self.install()
        self.assertEqual([("unchanged", str(self.hooks / HOOK))], self.rows(run.stdout))
        self.assertEqual(self.hooks_state(), state)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (0, [("installed", str(self.hooks / HOOK))]))

    def test_install_refuses_a_linked_worktree_and_a_foreign_hook_and_writes_nothing(self):
        """Each refusal is exit 2 with nothing written: a linked worktree (its hooks are the main checkout's), a
        foreign `reference-transaction` (a file of other content, or a symlink), a path that is no directory or no
        checkout, and a usage error; the foreign hook is never overwritten."""
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked), "-b", "linked")
        state = self.hooks_state()
        run = self.run_lever("install", str(linked))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a linked worktree", run.stderr)
        self.assertEqual(self.hooks_state(), state)

        (self.hooks / HOOK).write_text("#!/bin/sh\nexit 0\n")
        (self.hooks / HOOK).chmod(0o755)
        foreign = self.hooks_state()
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"{self.hooks / HOOK} exists and is not this lever's hook", run.stderr)
        self.assertEqual(self.hooks_state(), foreign)
        (self.hooks / HOOK).unlink()
        (self.hooks / HOOK).symlink_to(self.root / "nowhere")
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"{self.hooks / HOOK} is a symlink, not this lever's hook", run.stderr)
        self.assertFalse((self.root / "nowhere").exists(), "nothing written through the symlink")
        (self.hooks / HOOK).unlink()
        self.assertEqual(self.hooks_state(), state)

        outside = self.root / "outside"
        outside.mkdir()
        for label, args in (
            ("no checkout", ["install", str(outside)]),
            ("no directory", ["install", str(self.root / "absent")]),
            ("unknown action", ["remove", str(self.checkout)]),
            ("no argument", ["install"]),
            ("too many", ["install", str(self.checkout), "x"]),
        ):
            with self.subTest(label):
                run = self.run_lever(*args)
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertIn("checkout-guard.sh: refused: ", run.stderr)
        self.assertEqual(self.hooks_state(), state)

    def test_a_failing_read_refuses_before_anything_is_written(self):
        """Standing order 21: the git directory and the common directory (the isolated git) failing with exit 128
        from the PATH git are each a refusal naming the read, never an absence, with nothing written; so is a `cmp`
        that cannot read the hook file."""
        state = self.hooks_state()
        for pattern, message in (
            ("rev-parse --path-format=absolute --git-dir", "cannot read the git directory"),
            ("rev-parse --path-format=absolute --git-common-dir", "cannot read the git common directory"),
        ):
            with self.subTest(pattern):
                env = {**self.env, "PATH": f"{self.shim(pattern)}:{self.env['PATH']}"}
                run = self.run_lever("install", str(self.checkout), env=env)
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertIn(message, run.stderr)
                self.assertEqual(self.hooks_state(), state)
        if os.geteuid() != 0:
            self.install()
            (self.hooks / HOOK).chmod(0o311)
            try:
                for action in ("check", "install"):
                    with self.subTest(action):
                        run = self.run_lever(action, str(self.checkout))
                        self.assertEqual(run.returncode, 2, run.stdout)
                        self.assertIn(f"cannot compare {self.hooks / HOOK} with this lever's {HOOK}", run.stderr)
            finally:
                (self.hooks / HOOK).chmod(0o755)

    def test_a_failing_mktemp_refuses_check_and_install_and_writes_nothing(self):
        """Standing order 21, the one producer round 3 left without an injection test: a `mktemp` on PATH that exits
        28 (as the audit injected) makes `check` and `install` exit 2 naming the scratch directory, with no row and
        the hooks directory unchanged, whether the hook is in place or not."""
        shims = self.shim("", status=28, name="mktemp")
        env = {**self.env, "PATH": f"{shims}:{self.env['PATH']}"}
        for installed in (False, True):
            if installed:
                self.install()
            state = self.hooks_state()
            for action in ("check", "install"):
                with self.subTest(action, installed=installed):
                    run = self.run_lever(action, str(self.checkout), env=env)
                    self.assertEqual(run.returncode, 2, run.stdout)
                    self.assertIn("shim: failing mktemp", run.stderr)
                    self.assertIn("cannot make a scratch directory", run.stderr)
                    self.assertEqual(run.stdout, "")
                    self.assertEqual(self.hooks_state(), state)

    def test_a_failing_toplevel_read_or_hook_write_refuses_check_and_install_and_writes_nothing(self):
        """Standing order 21, the two producers round 4 left without an injection test: the installer's isolated
        `rev-parse --show-toplevel` read (a PATH `git` that exits 28 on it, as the audit injected) and the write of
        the expected hook bytes (a PATH `cat` that exits 28) each make `check` and `install` exit 2 naming the read
        or the write, with no row and the hooks directory unchanged, whether the hook is in place or not."""
        for label, shims, message in (
            (
                "toplevel",
                self.shim("rev-parse --show-toplevel", status=28),
                f"cannot read the toplevel of {self.checkout}",
            ),
            ("cat", self.shim("", status=28, name="cat"), "cannot write "),
        ):
            env = {**self.env, "PATH": f"{shims}:{self.env['PATH']}"}
            for installed in (False, True):
                if installed and not (self.hooks / HOOK).exists():
                    self.install()
                state = self.hooks_state()
                for action in ("check", "install"):
                    with self.subTest(label, action=action, installed=installed):
                        run = self.run_lever(action, str(self.checkout), env=env)
                        self.assertEqual(run.returncode, 2, run.stdout)
                        self.assertIn("shim: failing", run.stderr)
                        self.assertIn(message, run.stderr)
                        self.assertEqual(run.stdout, "")
                        self.assertEqual(self.hooks_state(), state)
            (self.hooks / HOOK).unlink()
        # The control: without a shim on PATH, `install` writes the hook.
        self.install()

    def test_a_failing_write_step_of_install_leaves_the_hook_path_as_found(self):
        """Standing order 21 at every decision of the install's write (audit round 5 P2: writing the hook path in
        place left an empty, a non-executable or an unverified hook behind a refusal; round 5 pinned none of `mkdir`,
        `chmod` and the stale-hook `rm`). The hook's bytes go to a temporary file in the hooks directory, which one
        `mv` renames onto the hook path after the mode is set and the read-back passes; `mkdir` of an absent hooks
        directory, the `cat` that writes those bytes (the fifth cat of a run, after the four scratch copies), `chmod`,
        the read-back `cmp` and the `mv`, each a PATH shim exiting 28, make `install` exit 2 naming the step with no
        row, the hooks directory's listing, bytes and modes unchanged and no temporary file left, whether the hook
        is absent or is this lever's own without its execute bit. The round-1 `rm` comes after the rename by design
        (no run leaves the checkout unguarded): with the hook already in place its failure changes nothing; with the
        hook absent the hook is installed, the round-1 file stays, and the next run removes it."""
        hook = self.hooks / HOOK
        shutil.rmtree(self.hooks)
        env = {**self.env, "PATH": f"{self.shim('', status=28, name='mkdir')}:{self.env['PATH']}"}
        run = self.run_lever("install", str(self.checkout), env=env)
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"cannot make {self.hooks}", run.stderr)
        self.assertEqual(run.stdout, "")
        self.assertFalse(self.hooks.exists(), "the hooks directory stays absent")
        self.install()
        original = hook.read_bytes()
        hook.unlink()
        cat = self.shim("", status=28, name="cat", nth=SCRATCH_WRITES + 1)
        # The count is the install's: `check` writes the four scratch copies and no fifth, so the shim never fires.
        env = {**self.env, "PATH": f"{cat}:{self.env['PATH']}"}
        check = self.run_lever("check", str(self.checkout), env=env)
        self.assertEqual((check.returncode, self.rows(check.stdout)), (1, [("absent", str(hook))]), check.stderr)
        self.assertNotIn("shim", check.stderr)
        (cat / "calls").unlink()
        staged = f"{self.hooks}/.{HOOK}."
        for label, shims, messages in (
            ("cat", cat, (f"cannot write {staged}",)),
            ("chmod", self.shim("", status=28, name="chmod"), (f"cannot make {staged}", " executable")),
            ("cmp", self.shim("", status=28, name="cmp"), ("cannot compare ",)),
            ("mv", self.shim("", status=28, name="mv"), (f"cannot move {staged}", f" onto {hook}")),
        ):
            env = {**self.env, "PATH": f"{shims}:{self.env['PATH']}"}
            for found in ("absent", "own, not executable"):
                if found == "absent":
                    if hook.exists():
                        hook.unlink()
                else:
                    hook.write_bytes(original)
                    hook.chmod(0o644)
                state = self.hooks_state()
                with self.subTest(label, found=found):
                    (shims / "calls").unlink(missing_ok=True)
                    run = self.run_lever("install", str(self.checkout), env=env)
                    self.assertEqual(run.returncode, 2, run.stdout)
                    self.assertIn(f"shim: failing {label}", run.stderr)
                    for message in messages:
                        self.assertIn(message, run.stderr)
                    self.assertEqual(run.stdout, "")
                    self.assertEqual(self.hooks_state(), state)
        # The control: the same checkout, no shim on PATH, the hook without its execute bit is installed in place.
        run = self.install()
        self.assertEqual([("installed", str(hook))], self.rows(run.stdout))
        self.assertEqual((hook.read_bytes(), stat.S_IMODE(hook.stat().st_mode)), (original, 0o755))
        # The round-1 `rm`, after the rename: the pattern names the round-1 path alone, so the trap's own removals run.
        stale = self.hooks / "pre-commit"
        stale.write_bytes(round1_body("pre-commit"))
        stale.chmod(0o755)
        rm = self.shim(f"-- {stale}", status=28, name="rm")
        env = {**self.env, "PATH": f"{rm}:{self.env['PATH']}"}
        state = self.hooks_state()
        run = self.run_lever("install", str(self.checkout), env=env)
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"cannot remove the round-1 {stale}", run.stderr)
        self.assertEqual([("unchanged", str(hook))], self.rows(run.stdout))
        self.assertEqual(self.hooks_state(), state)
        hook.unlink()
        run = self.run_lever("install", str(self.checkout), env=env)
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"cannot remove the round-1 {stale}", run.stderr)
        self.assertEqual([("installed", str(hook))], self.rows(run.stdout))
        self.assertEqual((hook.read_bytes(), stat.S_IMODE(hook.stat().st_mode)), (original, 0o755))
        self.assertEqual(stale.read_bytes(), round1_body("pre-commit"))
        run = self.install()
        self.assertEqual([("unchanged", str(hook)), ("removed", str(stale))], self.rows(run.stdout))
        self.assertFalse(stale.exists())

    def test_every_way_of_authoring_a_commit_is_refused_and_no_branch_moves(self):
        """With `.orchestration/orchestrate/<program>/units.tsv` under the toplevel, every command that would move a
        local branch to a commit origin does not hold is refused with the route: `commit`, `commit --no-verify` (no
        bypass: it skips no reference-transaction hook), `commit --amend`, `merge --no-ff`, `cherry-pick`, `rebase`
        onto such a commit, `branch -f` and `update-ref`. No branch moves; HEAD stays on its branch, except after the
        refused `rebase`, which git leaves detached at the onto commit in its rebase state until `rebase --abort`."""
        self.install()
        self.store()
        before = self.branches()
        status, err, head = self.commit()
        self.assert_refused(status, err)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.git("reset", "-q", "--hard", "origin/main")
        status, err, head = self.commit(None, "--no-verify")
        self.assert_refused(status, err)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.git("reset", "-q", "--hard", "origin/main")
        for label, args in (
            ("amend", ["commit", "-q", "--amend", "--allow-empty", "-m", "amended"]),
            ("merge --no-ff", ["merge", "--no-ff", "--no-edit", "-q", self.work]),
            ("cherry-pick", ["cherry-pick", self.work]),
            ("branch -f", ["branch", "-f", "topic", self.work]),
            ("update-ref", ["update-ref", "refs/heads/topic", self.work]),
        ):
            with self.subTest(label):
                status, _, err = self.git_status(*args)
                self.assert_refused(status, err)
                self.assertEqual(self.branches(), before)
                self.git_status("merge", "--abort")
                self.git_status("cherry-pick", "--quit")
                self.git("reset", "-q", "--hard", "origin/main")
        status, _, err = self.git_status("rebase", "-q", self.work)
        self.assert_refused(status, err)
        self.assertIn("refs/heads/main would move to " + self.work, err)
        self.assertEqual(self.branches()[0], before[0], "no branch moved")
        # git 2.56 refuses at the branch update after it has detached HEAD at the onto commit, and leaves its rebase
        # state for `rebase --abort`; a git that updates the branch first leaves HEAD on it. Either way no branch moved.
        self.assertIn(self.branches()[1], ("refs/heads/main", "detached " + self.work))
        if (self.checkout / ".git/rebase-merge").is_dir():
            self.git("rebase", "--abort")
        self.assertEqual(self.branches(), before)

    def test_a_commit_in_a_linked_worktree_of_the_checkout_is_refused(self):
        """A linked worktree shares the main checkout's hooks directory: a commit there is refused while the main
        worktree holds a store, although the linked worktree's own toplevel holds none; the add itself passes (its
        branch is made at origin's commit)."""
        self.install()
        self.store()
        linked = self.root / "linked"
        status, _, err = self.git_status("worktree", "add", "-q", "-b", "linked", str(linked), "origin/main")
        self.assertEqual(status, 0, err)
        self.assertFalse((linked / ".orchestration").exists())
        status, err, before = self.commit(linked)
        self.assert_refused(status, err)
        self.assertIn("refs/heads/linked would move to", err)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=linked), before)
        self.assertEqual(self.branches(linked)[1], "refs/heads/linked")

    def test_the_moves_the_coordinator_makes_pass(self):
        """Every move that lands a branch on a commit origin holds passes with a store present: `fetch`, `pull
        --ff-only` to origin's new commit, `reset --hard origin/main`, a branch made at or deleted from origin's
        commit, `checkout -b`, `worktree add -b x origin/main`, a tag, a stash and a detached checkout; and `push` of
        a fetched head from the checkout (the push line of worker-worktree.sh) moves no local branch."""
        self.install()
        self.store()
        (self.origin / "second").write_text("second\n")
        self.git("add", "second", cwd=self.origin)
        self.git("commit", "-q", "-m", "second", cwd=self.origin)
        advanced = self.git("rev-parse", "HEAD", cwd=self.origin)
        for label, args in (
            ("fetch", ["fetch", "-q", "origin"]),
            ("pull --ff-only", ["pull", "-q", "--ff-only"]),
            ("reset --hard origin/main", ["reset", "-q", "--hard", "origin/main"]),
            ("branch at origin's commit", ["branch", "topic", "origin/main"]),
            ("branch -D", ["branch", "-q", "-D", "topic"]),
            ("checkout -b", ["checkout", "-q", "-b", "topic2"]),
            ("worktree add", ["worktree", "add", "-q", "-b", "x", str(self.root / "x"), "origin/main"]),
            ("tag", ["tag", "mark", self.work]),
            ("stash", ["stash", "-q"]),
            ("detached checkout", ["checkout", "-q", "--detach", self.work]),
        ):
            with self.subTest(label):
                if label == "stash":
                    (self.checkout / "README").write_text("edited\n")
                status, _, err = self.git_status(*args)
                self.assertEqual(status, 0, err)
                self.assertNotIn("checkout-guard", err)
                if label == "pull --ff-only":
                    self.assertEqual(self.git("rev-parse", "HEAD"), advanced)
        self.git("checkout", "-q", "main")
        # `reset --hard origin/main` after a commit the hook never saw (the isolated git of the levers) passes too.
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-q", "--allow-empty", "-m", "ahead")
        status, _, err = self.git_status("reset", "-q", "--hard", "origin/main")
        self.assertEqual(status, 0, err)
        self.assertEqual(self.git("rev-parse", "HEAD"), advanced)
        status, _, err = self.git_status("push", "-q", str(self.origin), f"{self.work}:refs/heads/from-checkout")
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)

    def test_no_environment_variable_bypasses_the_hook(self):
        """The hook is `python3 -I -S`: `SHELLOPTS=noexec` or `noglob` (which made round 1's bash hook exit 0),
        `BASH_ENV` naming a file that exits 0, `PYTHONPATH` naming a directory with a planted `subprocess` module,
        `PYTHONHOME`, a planted `subprocess.py` beside the hook, and the skip variables of other hook frameworks each
        change nothing: the commit is refused."""
        self.install()
        self.store()
        startup = self.root / "bash_env"
        startup.write_text("exit 0\n")
        planted = self.root / "planted"
        planted.mkdir()
        for name in ("subprocess.py", "os.py"):
            (planted / name).write_text("raise SystemExit(0)\n")
            (self.hooks / name).write_text("raise SystemExit(0)\n")
        self.addCleanup(lambda: [(self.hooks / name).unlink() for name in ("subprocess.py", "os.py")])
        for variable, value in (
            ("SHELLOPTS", "noexec"),
            ("SHELLOPTS", "noglob"),
            ("BASH_ENV", str(startup)),
            ("ENV", str(startup)),
            ("PYTHONPATH", str(planted)),
            ("PYTHONHOME", str(self.root / "nowhere")),
            ("PYTHONSTARTUP", str(planted / "subprocess.py")),
            ("CHECKOUT_GUARD_SKIP", "1"),
            ("SKIP", "checkout-guard"),
            ("HUSKY", "0"),
        ):
            with self.subTest(variable=variable, value=value):
                status, err, before = self.commit(env={**self.env, variable: value})
                self.assert_refused(status, err)
                self.assertEqual(self.git("rev-parse", "HEAD"), before)
                self.git("reset", "-q", "--hard", "origin/main")

    def test_without_a_store_the_hook_passes_everything(self):
        """Without a store the hook exits 0 and prints nothing: `commit`, `merge --no-ff` and a commit in a linked
        worktree pass, as does a program directory holding no `units.tsv`; so the hook is inert in any other
        repository regime-init prepared and in the checkout before its first program."""
        self.install()
        status, err, before = self.commit()
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        self.assertNotEqual(self.git("rev-parse", "HEAD"), before)
        status, _, err = self.git_status("merge", "--no-ff", "--no-edit", "-q", self.work)
        self.assertEqual(status, 0, err)
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked), "-b", "linked")
        status, err, _ = self.commit(linked)
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        (self.checkout / ".orchestration/orchestrate/empty").mkdir(parents=True)
        status, err, _ = self.commit()
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)

    def test_the_isolated_git_of_the_levers_is_unaffected(self):
        """`git -c core.hooksPath=/dev/null commit`, the flag git-isolated.sh carries, runs no hook of the checkout:
        the levers' own commits are untouched by the guard (records-sync.sh's scratch repository among them)."""
        self.install()
        self.store()
        status, err, before = self.commit()
        self.assert_refused(status, err)
        self.git("reset", "-q", "--hard", "origin/main")
        (self.checkout / "isolated.txt").write_text("isolated\n")
        self.git("add", "isolated.txt")
        status, _, err = self.git_status("-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "isolated")
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        self.assertNotEqual(self.git("rev-parse", "HEAD"), before)

    @unittest.skipIf(os.geteuid() == 0, "root reads an unreadable directory")
    def test_a_store_that_cannot_be_read_refuses_the_move(self):
        """Fail closed (standing order 21): `.orchestration` itself (the ancestor round 1 read as "no store"; round 4
        listed `orchestrate` alone, so a mode-0111 `.orchestration` stayed traversable and passed), the `orchestrate`
        directory or a program directory that cannot be listed (mode 000, and mode 0111, which answers a `stat` of its
        `units.tsv` while refusing a listing: round 3 `stat`-ed and passed the commit), a later program directory that
        cannot be listed after a readable one holding a store (round 4 returned at the first `units.tsv`), and an
        `.orchestration` that is a file, are each a refusal naming the directory, never "no store"; an absent
        `.orchestration` is no store."""
        self.install()
        store = self.store()
        stores = store.parent
        later = self.store(program="zz-later")
        self.assertGreater(later.name, store.name, "the unreadable program directory comes after the readable one")
        for directory, named, mode in (
            (stores.parent, stores.parent, 0),
            (stores.parent, stores.parent, 0o111),
            (stores, stores, 0),
            (stores, stores, 0o111),
            (store, store, 0),
            (store, store, 0o111),
            (later, later, 0),
            (later, later, 0o111),
        ):
            with self.subTest(directory=directory.name, mode=oct(mode)):
                restore = directory.stat().st_mode
                directory.chmod(mode)
                try:
                    status, err, before = self.commit()
                    created, _, branch_err = self.git_status("branch", "at-origin", "origin/main")
                finally:
                    directory.chmod(stat.S_IMODE(restore))
                self.assertNotEqual(status, 0, err)
                self.assertIn(f"cannot read {named}", err)
                self.assertIn(FAILED_READ, err)
                self.assertNotIn(REFUSAL, err)
                self.assertEqual(self.git("rev-parse", "HEAD"), before)
                # The audit's probe: a move origin holds is not judged either while the store cannot be read.
                self.assertNotEqual(created, 0, branch_err)
                self.assertIn(f"cannot read {named}", branch_err)
                self.assertEqual(self.git_status("rev-parse", "--verify", "-q", "refs/heads/at-origin")[0], 1)
                self.git("reset", "-q", "--hard", "origin/main")
        shutil.rmtree(self.checkout / ".orchestration")
        (self.checkout / ".orchestration").write_text("a file\n")
        status, err, before = self.commit()
        self.assertNotEqual(status, 0, err)
        self.assertIn(f"cannot read {stores.parent}", err)
        self.assertIn(FAILED_READ, err)
        self.assertEqual(self.git("rev-parse", "HEAD"), before)
        (self.checkout / ".orchestration").unlink()
        self.git("reset", "-q", "--hard", "origin/main")
        status, err, _ = self.commit()
        self.assertEqual(status, 0, err)

    def test_a_checkout_path_holding_a_newline_is_guarded(self):
        """A main checkout whose path holds a newline (which truncated round 1's porcelain read) is guarded in the
        main worktree and in a linked one: the main worktree's path comes from `worktree list --porcelain -z`."""
        checkout = self.clone(self.root / "check\nout")
        self.install(checkout)
        self.store(checkout)
        self.git("fetch", "-q", str(self.root / "other"), "work", cwd=checkout)
        status, err, before = self.commit(checkout)
        self.assert_refused(status, err)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=checkout), before)
        linked = self.root / "linked"
        status, _, err = self.git_status(
            "worktree", "add", "-q", "-b", "linked", str(linked), "origin/main", cwd=checkout
        )
        self.assertEqual(status, 0, err)
        status, err, before = self.commit(linked)
        self.assert_refused(status, err)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=linked), before)

    def test_a_separate_git_directory_whose_name_ends_in_lf_is_installed_into(self):
        """A checkout whose `.git` is a symlink to a separate git directory whose name ends in LF: git resolves both
        `--git-dir` and `--git-common-dir` to that directory, LF and all (its realpath), and runs the hooks there. A
        command substitution strips the LF with git's own line end, so round 5 installed into the stripped sibling
        and `check` reported it over the sibling while the checkout stayed unguarded (audit round 5 P2); the lever
        reads each path whole, so `install` writes into the LF directory and nothing into the sibling, `check` judges
        that file and a commit in the checkout is refused. A `gitdir:` pointer file cannot name such a directory: git
        strips a pointer's trailing newlines (pinned below), which is why the symlink is the one form."""
        lf = self.root / "gitdir\n"
        sibling = self.root / "gitdir"
        checkout = self.clone(self.root / "lf-checkout")
        shutil.move(str(checkout / ".git"), str(lf))
        (checkout / ".git").symlink_to(lf)
        (sibling / "hooks").mkdir(parents=True)
        for option in ("--git-dir", "--git-common-dir"):
            run = subprocess.run(
                ["git", "rev-parse", "--path-format=absolute", option],
                cwd=checkout,
                env=self.env,
                capture_output=True,
                check=False,
                timeout=120,
            )
            self.assertEqual((run.returncode, run.stdout), (0, os.fsencode(lf) + b"\n"), run.stderr)
        hook = lf / "hooks" / HOOK
        run = self.run_lever("install", str(checkout))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, f"{PREFIX}installed\t{hook}\n")
        self.assertEqual(stat.S_IMODE(hook.stat().st_mode), 0o755)
        self.install()
        self.assertEqual(hook.read_bytes(), (self.hooks / HOOK).read_bytes())
        self.assertEqual(list((sibling / "hooks").iterdir()), [], "nothing in the stripped sibling")
        check = self.run_lever("check", str(checkout))
        self.assertEqual((check.returncode, check.stdout), (0, f"{PREFIX}installed\t{hook}\n"), check.stderr)
        self.store(checkout)
        self.git("fetch", "-q", str(self.root / "other"), "work", cwd=checkout)
        status, err, before = self.commit(checkout)
        self.assert_refused(status, err)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=checkout), before)
        # Why the symlink: a `gitdir:` pointer naming the LF directory resolves to the stripped sibling, which is no
        # repository, so git refuses the pointer and the LF directory is unreachable through it.
        (checkout / ".git").unlink()
        (checkout / ".git").write_text(f"gitdir: {lf}\n")
        status, _, err = self.git_status("rev-parse", "--git-dir", cwd=checkout)
        self.assertNotEqual(status, 0, err)
        self.assertIn("gitfile does not point to a valid repository", err)

    def test_a_failing_git_read_of_the_hook_refuses_the_move(self):
        """Standing order 21: each git read of the hook (the toplevel, the worktree list, the remote refs, the
        ancestry, and the ref itself when a creation line arrives) failing with exit 128 is a refusal naming the
        read, never a pass; the branch stays."""
        self.install()
        self.store()
        for pattern in (
            "rev-parse --show-toplevel",
            "worktree list --porcelain -z",
            "for-each-ref --format=%(refname)%09%(objectname) refs/remotes/origin/",
            "merge-base --is-ancestor",
        ):
            with self.subTest(pattern):
                status, err, before = self.commit(env=self.hook_shim(pattern))
                self.assertNotEqual(status, 0, err)
                self.assertIn(f"git {pattern}", err)
                self.assertIn("exited 128: shim: failing", err)
                self.assertIn(FAILED_READ, err)
                self.assertNotIn(REFUSAL, err)
                self.assertEqual(self.git("rev-parse", "HEAD"), before)
                self.git("reset", "-q", "--hard", "origin/main")
        # A creation line (`branch topic`) makes the hook read the ref; that read failing refuses the creation.
        before = self.branches()
        status, _, err = self.git_status("branch", "topic", "origin/main", env=self.hook_shim("rev-parse --verify -q"))
        self.assertNotEqual(status, 0, err)
        self.assertIn("git rev-parse --verify -q refs/heads/topic exited 128: shim: failing", err)
        self.assertIn(FAILED_READ, err)
        self.assertEqual(self.branches(), before)
        # The shim itself passes a move it does not fail: the control for the injection.
        status, err, _ = self.commit(env=self.hook_shim("no-such-read"))
        self.assert_refused(status, err)

    def test_the_prepared_phase_feeds_old_new_ref_lines_as_githooks_documents(self):
        """The format pinned against the running git: a recording `reference-transaction` sees, for one commit, a
        `prepared` state whose stdin is exactly `<old-value> SP <new-value> SP <ref-name> LF` with the branch's old
        and new commits and the resolved `refs/heads/main` (githooks(5)), and the `committed` state after it; the
        hook's parser reads that line and nothing else."""
        log = self.root / "transactions"
        (self.hooks / HOOK).write_text(
            "#!/usr/bin/env -S python3 -I -S\nimport sys\n"
            f"open({str(log)!r}, 'a').write(sys.argv[1] + ' ' + repr(sys.stdin.read()) + chr(10))\n"
        )
        (self.hooks / HOOK).chmod(0o755)
        old = self.git("rev-parse", "HEAD")
        status, err, _ = self.commit()
        self.assertEqual(status, 0, err)
        new = self.git("rev-parse", "HEAD")
        records = [line.split(" ", 1) for line in log.read_text().splitlines()]
        states = [state for state, _ in records]
        self.assertIn("prepared", states)
        self.assertLess(states.index("prepared"), states.index("committed"))
        prepared = [ast.literal_eval(data) for state, data in records if state == "prepared"]
        self.assertIn(f"{old} {new} refs/heads/main\n", prepared)
        for data in prepared:
            for line in data.splitlines(keepends=True):
                self.assertRegex(line, LINE)

    def test_the_hook_judges_the_documented_lines(self):
        """The installed hook run by hand on the documented lines, a store present: a `refs/heads/*` line to a commit
        origin does not hold is refused, as a move or as a creation; one to origin's commit, a deletion, a `ref:`
        value, a tag, a remote-tracking ref, a detached HEAD and the packed backend's creation line for a branch that
        already names the commit pass; a line of another shape is a refusal; the states other than `prepared` exit 0
        whatever the lines; a transaction holding one refused line among passing ones is refused."""
        self.install()
        self.git("branch", "off", self.work)  # before the store exists: a branch already off origin
        self.store()
        held = self.git("rev-parse", "origin/main")
        hook = self.hooks / HOOK

        def run(state, data):
            return subprocess.run(
                [str(hook), state], input=data, cwd=self.checkout, env=self.env, capture_output=True, text=True
            )

        refused = f"{held} {self.work} refs/heads/main\n"
        for label, data in (
            ("origin's commit", f"{held} {held} refs/heads/main\n"),
            ("a branch made at origin's commit", f"{ZERO} {held} refs/heads/topic\n"),
            ("a deletion", f"{self.work} {ZERO} refs/heads/topic\n"),
            ("a symbolic branch", f"{ZERO} ref:refs/heads/main refs/heads/alias\n"),
            ("a tag", f"{ZERO} {self.work} refs/tags/mark\n"),
            ("a remote-tracking ref", f"{held} {self.work} refs/remotes/origin/main\n"),
            ("a detached HEAD", f"{held} {self.work} HEAD\n"),
            ("the packed backend's creation of a branch already at the commit", f"{ZERO} {self.work} refs/heads/off\n"),
            ("old equal to new", f"{self.work} {self.work} refs/heads/off\n"),
            ("nothing", ""),
        ):
            with self.subTest(label):
                result = run("prepared", data)
                self.assertEqual((result.returncode, result.stderr), (0, ""))
        for label, data, ref in (
            ("the commit origin does not hold", refused, "refs/heads/main"),
            (
                "one refused line among passing ones",
                f"{held} {held} refs/heads/main\n{refused}{ZERO} {held} refs/tags/t\n",
                "refs/heads/main",
            ),
            (
                "a new branch at the commit origin does not hold",
                f"{ZERO} {self.work} refs/heads/topic\n",
                "refs/heads/topic",
            ),
        ):
            with self.subTest(label):
                result = run("prepared", data)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn(REFUSAL, result.stderr)
                self.assertIn(f"{ref} would move to {self.work}", result.stderr)
        for label, data in (
            ("two fields", f"{held} refs/heads/main\n"),
            ("four fields", f"{held} {self.work} refs/heads/main extra\n"),
            ("an empty field", f"{held}  refs/heads/main\n"),
            ("a blank line inside", f"\n{held} {held} refs/heads/main\n"),
        ):
            with self.subTest(label):
                result = run("prepared", data)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("is not <old-value> SP <new-value> SP <ref-name>", result.stderr)
                self.assertIn(FAILED_READ, result.stderr)
        for state in ("preparing", "committed", "aborted"):
            with self.subTest(state):
                result = run(state, refused)
                self.assertEqual((result.returncode, result.stderr), (0, ""))

    def test_check_reports_drift_and_install_repairs_only_its_own(self):
        """`check` names a changed hook (`differs`, exit 1), one with a single byte replaced by NUL among them (a
        shell variable would drop the NUL; `cmp` reads it), one without its execute bit (`not-executable`) and a
        removed one (`absent`); `install` refuses the changed one, restores the bit of its own and rewrites the
        removed one."""
        self.install()
        hook = self.hooks / HOOK
        original = hook.read_bytes()
        with hook.open("a") as handle:
            handle.write("print('drift')\n")
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (1, [("differs", str(hook))]))
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is not this lever's hook", run.stderr)
        nul = bytearray(original)
        nul[len(nul) // 2] = 0
        hook.write_bytes(bytes(nul))
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (1, [("differs", str(hook))]))
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertEqual(hook.read_bytes(), bytes(nul), "never overwritten")
        hook.write_bytes(original)
        hook.chmod(0o644)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (1, [("not-executable", str(hook))]))
        run = self.install()
        self.assertEqual([("installed", str(hook))], self.rows(run.stdout))
        self.assertEqual(stat.S_IMODE(hook.stat().st_mode), 0o755)
        self.assertEqual(hook.read_bytes(), original)
        hook.unlink()
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (1, [("absent", str(hook))]))
        run = self.install()
        self.assertEqual([("installed", str(hook))], self.rows(run.stdout))
        self.assertEqual(hook.read_bytes(), original)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)

    def test_a_caller_s_git_environment_pointing_at_another_repository_does_not_move_the_install(self):
        """`GIT_DIR` and `GIT_WORK_TREE` in the caller's environment name another repository: the lever scrubs them
        before its isolated reads, so `install` writes the hook into the checkout named by the path and nothing into
        the other repository, and `check` judges that file."""
        other = self.root / "elsewhere"
        git_init(other, env=self.env, cwd=self.root)
        env = {**self.env, "GIT_DIR": str(other / ".git"), "GIT_WORK_TREE": str(other)}
        run = self.run_lever("install", str(self.checkout), env=env)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual([("installed", str(self.hooks / HOOK))], self.rows(run.stdout))
        self.assertFalse((other / ".git/hooks" / HOOK).exists())
        check = self.run_lever("check", str(self.checkout), env=env)
        self.assertEqual((check.returncode, self.rows(check.stdout)), (0, [("installed", str(self.hooks / HOOK))]))
        check = self.run_lever("check", str(other), env=env)
        self.assertEqual(
            (check.returncode, self.rows(check.stdout)), (1, [("absent", str(other / ".git/hooks" / HOOK))])
        )

    def test_a_replaced_origin_tip_does_not_rewrite_the_ancestry_the_hook_reads(self):
        """A `refs/replace/<origin tip>` ref, or a `GIT_REPLACE_REF_BASE` of the caller naming a tag, that stands a
        fabricated commit whose parent is the worker's commit in for origin's tip makes the worker's commit an ancestor
        of origin's as a plain git reads it (round 2 passed `update-ref main <worker commit>` under both). The hook
        reads with `--no-replace-objects` and `GIT_NO_REPLACE_OBJECTS=1`, so the move is refused under both and no
        branch moves; the replace ref itself (outside refs/heads) and a move to origin's commit pass."""
        self.install()
        self.store()
        held = self.git("rev-parse", "origin/main")
        fabricated = self.git("commit-tree", f"{held}^{{tree}}", "-p", self.work, "-m", "fabricated")
        status, _, err = self.git_status("replace", held, fabricated)
        self.assertEqual(status, 0, err)
        self.assertEqual(self.git("rev-parse", "origin/main^"), self.work, "the replacement is in effect for plain git")
        before = self.branches()
        status, _, err = self.git_status("update-ref", "refs/heads/main", self.work)
        self.assert_refused(status, err)
        self.assertEqual(self.branches(), before)
        self.assertEqual(self.git("rev-parse", "origin/main"), held)
        status, _, err = self.git_status("update-ref", "refs/heads/topic", held)
        self.assertEqual(status, 0, err)
        self.git("branch", "-q", "-D", "topic")
        self.git("replace", "-d", held)
        self.git("update-ref", f"refs/tags/{held}", fabricated)
        env = {**self.env, "GIT_REPLACE_REF_BASE": "refs/tags/"}
        self.assertEqual(self.git("rev-parse", "origin/main^", env=env), self.work, "the tag stands in for plain git")
        status, _, err = self.git_status("update-ref", "refs/heads/main", self.work, env=env)
        self.assert_refused(status, err)
        self.assertEqual(self.branches(), before)

    def test_a_grafted_origin_tip_does_not_rewrite_the_ancestry_the_hook_reads(self):
        """`.git/info/grafts`, or a `GIT_GRAFT_FILE` of the caller, naming the worker's commit as the parent of
        origin's tip makes the worker's commit an ancestor of origin's as a plain git reads it, and
        `--no-replace-objects` leaves grafts alone (round 5 passed `update-ref main <worker commit>` under both with
        origin's refs unchanged; the U71b audit found the same channel in pr-audit.sh). The hook reads with
        `GIT_GRAFT_FILE=/dev/null`, so the move is refused under both forms and no branch moves; a move to origin's
        commit still passes. The replace-object test beside this one still holds for its channel."""
        self.install()
        self.store()
        held = self.git("rev-parse", "origin/main")
        before = self.branches()
        grafts = self.checkout / ".git/info/grafts"
        grafts.parent.mkdir(exist_ok=True)
        grafts.write_text(f"{held} {self.work}\n")
        self.assertEqual(self.git("rev-parse", "origin/main^"), self.work, "the graft is in effect for plain git")
        status, _, err = self.git_status("update-ref", "refs/heads/main", self.work)
        self.assert_refused(status, err)
        self.assertEqual(self.branches(), before)
        self.assertEqual(self.git("rev-parse", "origin/main"), held)
        status, _, err = self.git_status("update-ref", "refs/heads/topic", held)
        self.assertEqual(status, 0, err)
        self.git("branch", "-q", "-D", "topic")
        grafts.unlink()
        self.assertEqual(self.git_status("rev-parse", "--verify", "-q", "origin/main^")[0], 1, "no graft left")
        callers = self.root / "grafts"
        callers.write_text(f"{held} {self.work}\n")
        env = {**self.env, "GIT_GRAFT_FILE": str(callers)}
        self.assertEqual(self.git("rev-parse", "origin/main^", env=env), self.work, "the caller's file is in effect")
        status, _, err = self.git_status("update-ref", "refs/heads/main", self.work, env=env)
        self.assert_refused(status, err)
        self.assertEqual(self.branches(), before)
        self.assertEqual(self.git("rev-parse", "origin/main"), held)

    def test_pack_refs_and_gc_pass_over_a_branch_that_is_already_off_origin(self):
        """A backend update feeds the hook lines whose old and new values are equal: `git pack-refs --all` and `git gc`
        in a guarded checkout holding a branch that is already off origin (made before the store existed; round 2
        aborted the packing with exit 128) succeed and move nothing, while a move of that branch to another commit
        origin does not hold is still refused."""
        self.install()
        self.git("branch", "off", self.work)
        self.store()
        before = self.branches()
        for label, args in (("pack-refs --all", ["pack-refs", "--all"]), ("gc", ["gc", "-q"])):
            with self.subTest(label):
                status, _, err = self.git_status(*args)
                self.assertEqual(status, 0, err)
                self.assertNotIn("checkout-guard", err)
                self.assertEqual(self.branches(), before)
        self.assertIn(f"{self.work} refs/heads/off", (self.checkout / ".git/packed-refs").read_text())
        more = self.git("commit-tree", f"{self.work}^{{tree}}", "-p", self.work, "-m", "more")
        status, _, err = self.git_status("update-ref", "refs/heads/off", more)
        self.assert_refused(status, err)
        self.assertEqual(self.branches(), before)

    @unittest.skipIf(os.geteuid() == 0, "root reads an unreadable directory")
    def test_a_hooks_directory_that_cannot_be_read_refuses_check_and_install(self):
        """Standing order 21: a hooks directory of mode 000 makes `check` and `install` exit 2 naming the read, never
        report the installed hook `absent` (round 2 did, exit 1) or write anything; a file where the directory should
        be is refused too."""
        self.install()
        state = self.hooks_state()
        self.hooks.chmod(0)
        try:
            for action in ("check", "install"):
                with self.subTest(action):
                    run = self.run_lever(action, str(self.checkout))
                    self.assertEqual(run.returncode, 2, run.stdout)
                    self.assertIn(f"cannot read {self.hooks}", run.stderr)
                    self.assertEqual(run.stdout, "")
        finally:
            self.hooks.chmod(0o755)
        self.assertEqual(self.hooks_state(), state)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (0, [("installed", str(self.hooks / HOOK))]))
        flat = self.clone(self.root / "flat")
        if (flat / ".git/hooks").exists():
            shutil.rmtree(flat / ".git/hooks")
        (flat / ".git/hooks").write_text("not a directory\n")
        for action in ("check", "install"):
            with self.subTest(action, hooks="a file"):
                run = self.run_lever(action, str(flat))
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertIn(f"{flat / '.git/hooks'} exists and is not a directory", run.stderr)
                self.assertEqual(run.stdout, "")
        self.assertEqual((flat / ".git/hooks").read_text(), "not a directory\n")

    def test_check_refuses_to_judge_a_symlink_or_a_non_regular_file_at_the_hook_path(self):
        """A symlink at the hook path (even one that resolves to this lever's bytes), a directory and a fifo are not
        judged: `check` and `install` exit 2 naming the kind with no row and nothing written through or over it
        (round 3's `check` read each as `differs`, exit 1); a regular file of other content stays `differs`, exit 1,
        and `install` refuses it; a byte-equal regular file is `installed`."""
        self.install()
        hook = self.hooks / HOOK
        original = hook.read_bytes()
        saved = self.root / "saved-hook"
        saved.write_bytes(original)
        saved.chmod(0o755)
        hook.unlink()
        for kind, make in (
            ("a symlink", lambda: hook.symlink_to(saved)),
            ("a symlink", lambda: hook.symlink_to(self.root / "nowhere")),
            ("a directory", hook.mkdir),
            ("a fifo", lambda: os.mkfifo(hook)),
        ):
            make()
            state = self.hooks_state()
            for action in ("check", "install"):
                with self.subTest(action, kind=kind, target=os.readlink(hook) if hook.is_symlink() else None):
                    run = self.run_lever(action, str(self.checkout))
                    self.assertEqual(run.returncode, 2, run.stdout)
                    self.assertIn(f"{hook} is {kind}, not this lever's hook; {action} does not judge it", run.stderr)
                    self.assertEqual(run.stdout, "")
                    self.assertEqual(self.hooks_state(), state)
            self.assertEqual(saved.read_bytes(), original)
            self.assertFalse((self.root / "nowhere").exists())
            if hook.is_dir() and not hook.is_symlink():
                hook.rmdir()
            else:
                hook.unlink()
        hook.write_text("#!/bin/sh\nexit 0\n")
        hook.chmod(0o755)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (1, [("differs", str(hook))]))
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"{hook} exists and is not this lever's hook", run.stderr)
        self.assertEqual(hook.read_text(), "#!/bin/sh\nexit 0\n")
        hook.write_bytes(original)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual((check.returncode, self.rows(check.stdout)), (0, [("installed", str(hook))]))


if __name__ == "__main__":
    unittest.main()
