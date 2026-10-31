"""Exercise scripts/orchestrator/checkout-guard.sh and the two hooks it installs (regime-cutover U129).

Every test builds a scratch main checkout under a scratch HOME (so the operator's global git configuration is the
scratch `~/.gitconfig`), installs the hooks with the checkout copy of the lever and makes commits with the user's
plain git, the git that runs `.git/hooks/pre-commit`. Nothing reads the real checkout or `~/.local/bin`.
"""

import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/checkout-guard.sh"
HOOKS = ("pre-commit", "post-checkout")
ROUTE = (
    "commits belong in a worker tree: ~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main makes one "
    "under $TMPDIR/dotfiles-wt/<unit> (standing order 29)"
)
REFUSAL = "checkout-guard: this checkout is the coordinator's; " + ROUTE
WARNING = "checkout-guard: warning: this is a linked worktree of the coordinator's checkout"


class CheckoutGuardTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        # The identity lives in the scratch global config, not in GIT_* variables: the lever scrubs those from its
        # own git, and the commits below are the user's plain git, which reads this file.
        (self.home / ".gitconfig").write_text(
            "[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n"
        )
        self.env = quiet_git_env({"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"})
        self.checkout = self.root / "checkout"
        git_init(self.checkout, env=self.env, cwd=self.root)
        (self.checkout / "README").write_text("main\n")
        self.git("add", "README")
        self.git("commit", "-q", "-m", "main")
        self.hooks = self.checkout / ".git/hooks"

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
        return [tuple(line.split("\t")) for line in stdout.splitlines() if "\t" in line]

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

    def install(self):
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 0, run.stderr)
        return run

    def commit(self, cwd=None, *options, env=None):
        """Try one commit of a new file in CWD; (exit status, stderr, the head before)."""
        tree = cwd or self.checkout
        before = self.git("rev-parse", "HEAD", cwd=tree)
        name = f"work-{len(list(tree.iterdir()))}.txt"
        (tree / name).write_text("work\n")
        self.git("add", name, cwd=tree)
        status, _, err = self.git_status("commit", "-q", *options, "-m", "work", cwd=tree, env=env)
        return status, err, before

    def shim(self, pattern, status=128):
        """The env whose PATH `git` exits STATUS on a call whose arguments hold PATTERN, else runs the real git."""
        real = shutil.which("git", path=os.defpath) or shutil.which("git")
        shims = Path(tempfile.mkdtemp(prefix="shim-git-", dir=self.root))
        (shims / "git").write_text(
            f'#!/bin/sh\ncase "$*" in\n*"{pattern}"*) echo "shim: failing {pattern}" >&2; exit {status} ;;\nesac\n'
            f'exec "{real}" "$@"\n'
        )
        (shims / "git").chmod(0o755)
        return {**self.env, "PATH": f"{shims}:{self.env['PATH']}"}

    def test_install_on_a_main_checkout_writes_both_hooks_and_a_second_install_is_a_no_op(self):
        """`install` writes `pre-commit` and `post-checkout` into the checkout's hooks directory, mode 0755, and
        reads them back; `check` reports both as installed; a second install finds its own hooks, prints
        `unchanged` for each and leaves every byte and mode as it was."""
        before = self.run_lever("check", str(self.checkout))
        self.assertEqual(before.returncode, 1, before.stdout)
        self.assertEqual([("absent", str(self.hooks / name)) for name in HOOKS], self.rows(before.stdout))
        run = self.install()
        self.assertEqual([("installed", str(self.hooks / name)) for name in HOOKS], self.rows(run.stdout))
        for name in HOOKS:
            with self.subTest(hook=name):
                hook = self.hooks / name
                self.assertEqual(stat.S_IMODE(hook.stat().st_mode), 0o755)
                text = hook.read_text()
                self.assertTrue(text.startswith("#!/usr/bin/env bash\n"), text[:40])
                self.assertIn(ROUTE.replace("$TMPDIR", "\\$TMPDIR"), text, "the route, its $TMPDIR escaped in the file")
                self.assertIn("# git-isolated: allow a hook runs inside the user's git", text)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertEqual([("installed", str(self.hooks / name)) for name in HOOKS], self.rows(check.stdout))
        state = self.hooks_state()
        again = self.install()
        self.assertEqual([("unchanged", str(self.hooks / name)) for name in HOOKS], self.rows(again.stdout))
        self.assertEqual(self.hooks_state(), state)
        # `install` works from a subdirectory of the checkout too: the toplevel is git's.
        (self.checkout / "sub").mkdir()
        deeper = self.run_lever("install", str(self.checkout / "sub"))
        self.assertEqual(deeper.returncode, 0, deeper.stderr)
        self.assertEqual([("unchanged", str(self.hooks / name)) for name in HOOKS], self.rows(deeper.stdout))

    def test_install_refuses_a_linked_worktree_a_hooks_path_and_a_foreign_hook_and_writes_nothing(self):
        """Each refusal is exit 2 with nothing written: a linked worktree (its hooks are the main checkout's), a
        `core.hooksPath` in the repository's or the operator's global configuration (the hooks would not run), a
        foreign `pre-commit` or `post-checkout` (a file of other content, or a symlink), a path that is no directory
        or no checkout, and a usage error; the foreign hook is never overwritten and the other hook is not written."""
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked), "-b", "linked")
        state = self.hooks_state()
        run = self.run_lever("install", str(linked))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is a linked worktree", run.stderr)
        self.assertEqual(self.hooks_state(), state)

        self.git("config", "core.hooksPath", str(self.root / "elsewhere"))
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn(f"core.hooksPath is {self.root / 'elsewhere'}", run.stderr)
        self.assertEqual(self.hooks_state(), state)
        self.git("config", "--unset", "core.hooksPath")
        with (self.home / ".gitconfig").open("a") as config:
            config.write("[core]\n\thooksPath = ~/global-hooks\n")
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("core.hooksPath is ~/global-hooks", run.stderr)
        self.assertEqual(self.hooks_state(), state)
        (self.home / ".gitconfig").write_text("[user]\n\tname = t\n\temail = t@example.invalid\n")

        for name, other in (("pre-commit", "post-checkout"), ("post-checkout", "pre-commit")):
            with self.subTest(foreign=name):
                (self.hooks / name).write_text("#!/bin/sh\nexit 0\n")
                (self.hooks / name).chmod(0o755)
                foreign = self.hooks_state()
                run = self.run_lever("install", str(self.checkout))
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertIn(f"{self.hooks / name} exists and is not this lever's hook", run.stderr)
                self.assertEqual(self.hooks_state(), foreign)
                self.assertFalse((self.hooks / other).exists(), "the other hook is not written either")
                (self.hooks / name).unlink()
        (self.hooks / "pre-commit").symlink_to(self.root / "nowhere")
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is not this lever's hook", run.stderr)
        self.assertFalse((self.root / "nowhere").exists(), "nothing written through the symlink")
        self.assertFalse((self.hooks / "post-checkout").exists())
        (self.hooks / "pre-commit").unlink()
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
        """Standing order 21: the git directory, the common directory and the `core.hooksPath` read failing (exit
        128 from the PATH git) are each a refusal naming the read, never an absence, with nothing written."""
        state = self.hooks_state()
        for pattern, message in (
            ("rev-parse --path-format=absolute --git-dir", "cannot read the git directory"),
            ("rev-parse --path-format=absolute --git-common-dir", "cannot read the git common directory"),
            ("config --get core.hooksPath", "cannot read core.hooksPath"),
        ):
            with self.subTest(pattern):
                run = self.run_lever("install", str(self.checkout), env=self.shim(pattern))
                self.assertEqual(run.returncode, 2, run.stdout)
                self.assertIn(message, run.stderr)
                self.assertEqual(self.hooks_state(), state)

    def test_a_commit_in_the_checkout_with_a_store_is_refused_with_the_route(self):
        """With `.orchestration/orchestrate/<program>/units.tsv` under the toplevel every commit is refused, printing
        the route to a worker tree; the head does not move; no environment variable bypasses it; `--no-verify`, the
        operator's own hand, is the one bypass and is outside the contract."""
        self.install()
        self.store()
        status, err, before = self.commit()
        self.assertEqual(status, 1, err)
        self.assertIn(REFUSAL, err)
        self.assertEqual(self.git("rev-parse", "HEAD"), before)
        for variable in ("CHECKOUT_GUARD_SKIP", "CHECKOUT_GUARD", "SKIP", "HUSKY", "GIT_HOOKS_SKIP"):
            with self.subTest(variable=variable):
                status, err, before = self.commit(env={**self.env, variable: "1"})
                self.assertEqual(status, 1, err)
                self.assertIn(REFUSAL, err)
        status, err, _ = self.commit(None, "--no-verify")
        self.assertEqual(status, 0, err)
        # The store directory holding a program without units.tsv is no store: the commit passes.
        shutil.rmtree(self.checkout / ".orchestration")
        (self.checkout / ".orchestration/orchestrate/empty").mkdir(parents=True)
        status, err, _ = self.commit()
        self.assertEqual(status, 0, err)

    def test_a_commit_in_a_linked_worktree_of_the_checkout_is_refused(self):
        """A linked worktree shares the main checkout's hooks directory: a commit there is refused while the main
        worktree holds a store, although the linked worktree's own toplevel holds none."""
        self.install()
        self.store()
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked), "-b", "linked")
        self.assertFalse((linked / ".orchestration").exists())
        status, err, before = self.commit(linked)
        self.assertEqual(status, 1, err)
        self.assertIn(REFUSAL, err)
        self.assertEqual(self.git("rev-parse", "HEAD", cwd=linked), before)

    def test_a_commit_in_a_checkout_without_a_store_passes(self):
        """Without a store the pre-commit exits 0 and prints nothing: the hooks are inert in any other repository
        regime-init prepared and in the checkout before its first program."""
        self.install()
        status, err, before = self.commit()
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        self.assertNotEqual(self.git("rev-parse", "HEAD"), before)
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", str(linked), "-b", "linked")
        status, err, _ = self.commit(linked)
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard: this checkout", err)

    def test_worktree_add_prints_the_warning_and_succeeds(self):
        """`git worktree add` runs the post-checkout with a third argument of 1 in the new, linked worktree: the
        warning names the route and the add succeeds; a branch checkout in the main checkout and a file checkout in
        the linked worktree print nothing."""
        self.install()
        self.store()
        linked = self.root / "linked"
        status, _, err = self.git_status("worktree", "add", "-q", str(linked), "-b", "linked")
        self.assertEqual(status, 0, err)
        self.assertIn(WARNING, err)
        self.assertIn(ROUTE, err)
        self.assertTrue((linked / "README").exists())
        self.assertIn(str(linked), self.git("worktree", "list"))
        status, _, err = self.git_status("checkout", "-q", "-b", "topic")
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        (linked / "README").write_text("edited\n")
        status, _, err = self.git_status("checkout", "-q", "--", "README", cwd=linked)
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        status, _, err = self.git_status("checkout", "-q", "-b", "topic2", cwd=linked)
        self.assertEqual(status, 0, err)
        self.assertIn(WARNING, err, "a branch checkout in the linked worktree warns too")

    def test_the_isolated_git_of_the_levers_is_unaffected(self):
        """`git -c core.hooksPath=/dev/null commit`, the flag git-isolated.sh carries, runs no hook of the checkout:
        the levers' own commits are untouched by the guard (records-sync.sh's scratch repository among them)."""
        self.install()
        self.store()
        status, err, before = self.commit()
        self.assertEqual(status, 1, err)
        (self.checkout / "isolated.txt").write_text("isolated\n")
        self.git("add", "isolated.txt")
        status, _, err = self.git_status("-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", "isolated")
        self.assertEqual(status, 0, err)
        self.assertNotIn("checkout-guard", err)
        self.assertNotEqual(self.git("rev-parse", "HEAD"), before)

    @unittest.skipIf(os.geteuid() == 0, "root reads an unreadable directory")
    def test_a_read_failure_on_the_store_glob_refuses_the_commit(self):
        """Fail closed (standing order 21): a store root or a program directory that cannot be listed is a refusal
        naming it, never "no store", so a commit is refused when the hook cannot tell whether a store exists."""
        self.install()
        store = self.store()
        stores = store.parent
        for directory in (stores, store):
            with self.subTest(directory=directory.name):
                mode = directory.stat().st_mode
                directory.chmod(0)
                try:
                    status, err, before = self.commit()
                finally:
                    directory.chmod(stat.S_IMODE(mode))
                self.assertEqual(status, 1, err)
                self.assertIn(f"cannot read {directory}", err)
                self.assertIn("the commit is refused (standing order 21)", err)
                self.assertEqual(self.git("rev-parse", "HEAD"), before)
        shutil.rmtree(self.checkout / ".orchestration")
        status, err, _ = self.commit()
        self.assertEqual(status, 0, err)

    def test_check_reports_drift_and_install_repairs_only_its_own(self):
        """`check` names a changed hook (`differs`, exit 1), one without its execute bit (`not-executable`) and a
        removed one (`absent`); `install` refuses the changed one, restores the bit of its own and rewrites the
        removed one while the other prints `unchanged`."""
        self.install()
        original = (self.hooks / "pre-commit").read_bytes()
        with (self.hooks / "pre-commit").open("a") as hook:
            hook.write("echo drift\n")
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(check.returncode, 1, check.stdout)
        self.assertEqual(
            [("differs", str(self.hooks / "pre-commit")), ("installed", str(self.hooks / "post-checkout"))],
            self.rows(check.stdout),
        )
        run = self.run_lever("install", str(self.checkout))
        self.assertEqual(run.returncode, 2, run.stdout)
        self.assertIn("is not this lever's hook", run.stderr)
        (self.hooks / "pre-commit").write_bytes(original)
        (self.hooks / "pre-commit").chmod(0o644)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(check.returncode, 1, check.stdout)
        self.assertEqual(("not-executable", str(self.hooks / "pre-commit")), self.rows(check.stdout)[0])
        (self.hooks / "post-checkout").unlink()
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(("absent", str(self.hooks / "post-checkout")), self.rows(check.stdout)[1])
        run = self.install()
        self.assertEqual(
            [("installed", str(self.hooks / "pre-commit")), ("installed", str(self.hooks / "post-checkout"))],
            self.rows(run.stdout),
        )
        self.assertEqual(stat.S_IMODE((self.hooks / "pre-commit").stat().st_mode), 0o755)
        self.assertEqual((self.hooks / "pre-commit").read_bytes(), original)
        check = self.run_lever("check", str(self.checkout))
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        (self.hooks / "post-checkout").unlink()
        run = self.install()
        self.assertEqual(
            [("unchanged", str(self.hooks / "pre-commit")), ("installed", str(self.hooks / "post-checkout"))],
            self.rows(run.stdout),
        )

    def test_the_caller_s_git_environment_does_not_redirect_the_identity_reads(self):
        """`GIT_DIR` and `GIT_COMMON_DIR` in the caller's environment would point `rev-parse` at another repository;
        the lever scrubs every `GIT_*` name before its reads, so the hooks land in the checkout named by the path."""
        other = self.root / "other"
        git_init(other, env=self.env, cwd=self.root)
        env = {**self.env, "GIT_DIR": str(other / ".git"), "GIT_WORK_TREE": str(other)}
        run = self.run_lever("install", str(self.checkout), env=env)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual([("installed", str(self.hooks / name)) for name in HOOKS], self.rows(run.stdout))
        self.assertFalse((other / ".git/hooks/pre-commit").exists())


if __name__ == "__main__":
    unittest.main()
