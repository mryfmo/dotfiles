"""regime-store-move, the one-time copy of a program's live store to the derived root (regime-cutover U221).

The fixture is RecordsSyncTest's shape (tests/unit/test_pr_levers.py): a scratch checkout whose committed store
`.orchestration/orchestrate/prog/` holds origin/main's masked copies, a bare origin behind the git wrapper first on
PATH, which maps the checkout's https origin URL onto that bare repository, and a scratch HOME under which the derived
root `<HOME>/.local/state/regime-store/<slug>/` is made. The live store is the checkout subtree as the coordinator's
main checkout holds it before the move: a file whose unmasked bytes differ from main's masked blob, and the program's
`redact-words.txt`, which origin/main never holds. The lever runs from the checkout (its self-check reads the checkout's
manifest). Nothing reads the real `~/.local/state`, and the real `git` is reached only through the wrapper.
"""

import hashlib
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
LEVER = ROOT / "scripts/orchestrator/regime-store-move"
MASKER = ROOT / "scripts/validate-agent-assets.py"
URL = "https://github.com/acme/widgets.git"
PLANTED = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
PREFIX = ".orchestration/orchestrate/prog"
# The RecordsSyncTest wrapper's fake network: FAKE_GIT_HTTPS_ORIGIN="<https url>=<bare repository>" maps the https
# origin onto the local bare repository as a command-line insteadOf, and the local transport is re-opened for every
# call, as a caller's own `-c protocol.file.allow=always` would (the library's `protocol.allow=never` refuses it).
GIT_WRAPPER = """#!/usr/bin/env python3
import os, subprocess, sys
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in sys.argv[1:]:
    print("fake-git: failing as asked", file=sys.stderr)
    sys.exit(1)
mapping = ["-c", "protocol.file.allow=always"]
https_origin = os.environ.get("FAKE_GIT_HTTPS_ORIGIN")
if https_origin:
    mapping += ["-c", "url.{1}.insteadOf={0}".format(*https_origin.split("=", 1))]
sys.exit(subprocess.run([os.environ["REAL_GIT"], *mapping, *sys.argv[1:]]).returncode)
"""


class RegimeStoreMoveTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.bindir = self.root / "bin"
        self.bindir.mkdir()
        wrapper = self.bindir / "git"
        wrapper.write_text(GIT_WRAPPER)
        wrapper.chmod(0o755)
        self.home = self.root / "home"
        self.home.mkdir()
        self.tmp = self.root / "tmp"
        self.tmp.mkdir()
        gitconfig = self.root / "gitconfig"
        gitconfig.write_text("[user]\n\tname = t\n\temail = t@example.invalid\n[init]\n\tdefaultBranch = main\n")
        self.origin = self.root / "origin.git"
        self.env = quiet_git_env(
            {
                "PATH": f"{self.bindir}:{os.environ['PATH']}",
                "HOME": str(self.home),
                "TMPDIR": str(self.tmp),
                "LC_ALL": "C",
                "GIT_CONFIG_GLOBAL": str(gitconfig),
                "GIT_CONFIG_NOSYSTEM": "1",
                "REAL_GIT": shutil.which("git", path=os.environ["PATH"]),
                "FAKE_GIT_HTTPS_ORIGIN": f"{URL}={self.origin}",
            }
        )
        git_init(self.origin, "--bare", env=self.env)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git_init(self.repo, env=self.env)
        (self.repo / "scripts").mkdir()
        shutil.copy2(MASKER, self.repo / "scripts/validate-agent-assets.py")
        self.live = self.repo / PREFIX
        (self.live / "briefs").mkdir(parents=True)
        (self.live / "units.tsv").write_text("id\ttrack\nU1\tseats\n")
        (self.live / "decisions.tsv").write_text("ts\tphase\n")
        (self.live / "briefs/B1.md").write_text("brief\n")
        (self.live / "notes.md").write_text(f"token {PLANTED}\n")
        (self.repo / "README").write_text("scratch\n")
        # main holds the masked copy of notes.md (what records-sync.sh publishes); the live file keeps the token.
        self.mask(self.live / "notes.md")
        self.assertNotIn(PLANTED, (self.live / "notes.md").read_text(), "the fixture's masker changed the copy")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")
        (self.live / "notes.md").write_text(f"token {PLANTED}\n")
        (self.live / "redact-words.txt").write_text("# words\nwidgetsecret\n")
        self.git("remote", "add", "origin", URL)
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")
        self.derived = self.home / ".local/state/regime-store/repo/prog"
        self.step = (
            f"git -C {self.repo} checkout -- {PREFIX}\n"
            f"git -C {self.repo} clean -fd -- {PREFIX}\n"
            f"git -C {self.repo} pull --ff-only\n"
        )
        self.before = (self.live_digest(), self.status())

    def mask(self, path):
        subprocess.run(
            ["uv", "run", "--no-project", "python", "-I", str(MASKER), "--mask-secrets", str(path)],
            env=self.env,
            check=True,
            capture_output=True,
        )

    def git(self, *args, cwd=None):
        return subprocess.run(
            [str(self.bindir / "git"), *args],
            cwd=cwd or self.repo,
            env=self.env,
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def run_lever(self, *args, cwd=None, **extra):
        return subprocess.run(
            [str(LEVER), *args],
            cwd=cwd or self.repo,
            env={**self.env, **extra},
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )

    def live_digest(self):
        """Every entry below the live store with its mode and bytes, so a changed, added or removed file shows."""
        digest = hashlib.sha256()
        for path in sorted(entry for entry in self.live.rglob("*") if not entry.is_dir()):
            digest.update(f"{path.relative_to(self.live)} {path.lstat().st_mode:o}\n".encode())
            digest.update(path.read_bytes() if path.is_file() else b"<not a file>")
        return digest.hexdigest()

    def status(self):
        return self.git("status", "--porcelain=v1", "--untracked-files=all")

    def assert_checkout_unchanged(self):
        self.assertEqual((self.live_digest(), self.status()), self.before, "the checkout is byte-identical")
        self.assertEqual(self.git("ls-remote", "--heads", str(self.origin)).count("refs/heads/"), 1, "main only")

    def assert_nothing_written(self, run):
        self.assert_checkout_unchanged()
        self.assertFalse((self.home / ".local").exists(), "nothing is made under HOME")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        self.assertFalse(run.stdout.startswith("copied "), run.stdout)

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)

    def stub(self, name, body):
        """A tool first on PATH in place of the system's; the body is `sh` text that may exec the real one."""
        path = self.bindir / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def restore_live(self):
        """The live store as the fixture made it: main's copies checked out, notes.md unmasked again, nothing extra."""
        self.git("checkout", "-q", "--", PREFIX)
        (self.live / "notes.md").write_text(f"token {PLANTED}\n")
        for extra in ("extra.md", "briefs/B2.md"):
            (self.live / extra).unlink(missing_ok=True)

    def test_check_prints_the_step_and_writes_nothing_when_the_live_store_equals_main_masked(self):
        """`--check`: every read and every comparison, nothing written: the live store's files equal origin/main's
        blobs at the published prefix once masked (notes.md holds a token main holds masked), `redact-words.txt` is
        the one live path main need not hold, and the operator's step is printed as three complete commands."""
        for args in (("prog", "--check"), ("--check", "prog")):
            with self.subTest(args=args):
                run = self.run_lever(*args)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(
                    run.stdout, f"check: 5 files would be copied to {self.derived}; nothing written\n{self.step}"
                )
                self.assertIn(f"regime-store-move: live store {self.live} (5 files)", run.stderr)
                self.assert_nothing_written(run)

    def test_the_move_copies_every_file_into_the_derived_store_verifies_it_and_prints_the_step(self):
        """The default run: the components `regime-store`, `<slug>` and `<program>` made 0700 under the scratch HOME,
        every regular file of the live store copied with `cp -p` (`redact-words.txt` and the unmasked notes.md
        included: the new root is the live store, not main's copy), each read back, the count equal to the listing's,
        `copied <n> files to <dir>` and the step printed, and the checkout byte-identical before and after. A second run
        refuses: the derived store already holds the records."""
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, f"copied 5 files to {self.derived}\n{self.step}")
        self.assert_checkout_unchanged()
        for component in (self.derived.parent.parent, self.derived.parent, self.derived):
            self.assertEqual(stat.S_IMODE(component.lstat().st_mode), 0o700, component)
            self.assertFalse(component.is_symlink())
        copied = sorted(str(entry.relative_to(self.derived)) for entry in self.derived.rglob("*") if entry.is_file())
        self.assertEqual(copied, ["briefs/B1.md", "decisions.tsv", "notes.md", "redact-words.txt", "units.tsv"])
        for relative in copied:
            with self.subTest(file=relative):
                source = self.live / relative
                target = self.derived / relative
                self.assertEqual(target.read_bytes(), source.read_bytes())
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), stat.S_IMODE(source.stat().st_mode))
        self.assertIn(PLANTED, (self.derived / "notes.md").read_text(), "the live file moves as it is, unmasked")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        again = self.run_lever("prog")
        self.assert_refused(again, f"{self.derived} already holds")
        self.assertEqual(
            sorted(str(entry.relative_to(self.derived)) for entry in self.derived.rglob("*") if entry.is_file()), copied
        )
        self.assert_checkout_unchanged()

    def test_a_live_file_that_differs_from_main_masked_or_a_path_main_lacks_or_holds_alone_refuses(self):
        """A records sync is still due when a live file's masked form differs from main's blob, when a live path is
        absent from main (`redact-words.txt` aside), or when main holds a path the live store no longer does (a
        deletion the sync would carry): the refusal names the count, not the paths (a path may hold a redact word),
        and nothing is written, in `--check` and in the default run alike."""
        cases = (
            ("an edited file", lambda: (self.live / "units.tsv").write_text("id\ttrack\nU1\tseats\nU2\tseats\n"), 1),
            ("a file main lacks", lambda: (self.live / "extra.md").write_text("new\n"), 1),
            ("a file main holds alone", lambda: (self.live / "decisions.tsv").unlink(), 1),
            (
                "an edited file and a new one",
                lambda: ((self.live / "units.tsv").write_text("x\n"), (self.live / "briefs/B2.md").write_text("b\n")),
                2,
            ),
        )
        for label, plant, count in cases:
            with self.subTest(label):
                self.restore_live()
                plant()
                for args in (("prog", "--check"), ("prog",)):
                    run = self.run_lever(*args)
                    self.assert_refused(run, f"a records sync is still due ({count} path(s) differ")
                    self.assertNotIn("units.tsv", run.stderr + run.stdout, "no path is named")
                    self.assertFalse((self.home / ".local").exists(), "nothing is made under HOME")
                    self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
                self.restore_live()
                self.assert_checkout_unchanged()

    def test_a_derived_store_that_already_holds_an_entry_or_has_another_mode_refuses(self):
        """A `<root>/<program>` that holds any entry (a dot file too) refuses by name with nothing copied and the
        entry left as it was; a component found with a mode other than 0700, a link or a file at the program's place
        refuses by name (regime-init's component holds)."""
        self.derived.mkdir(parents=True, mode=0o700)
        for parent in (self.derived.parent, self.derived.parent.parent):
            parent.chmod(0o700)
        (self.derived / ".keep").write_text("kept\n")
        for args in (("prog", "--check"), ("prog",)):
            with self.subTest(args=args):
                run = self.run_lever(*args)
                self.assert_refused(run, f"{self.derived} already holds")
                self.assertEqual([entry.name for entry in self.derived.iterdir()], [".keep"])
                self.assert_checkout_unchanged()
        (self.derived / ".keep").unlink()
        self.derived.chmod(0o755)
        run = self.run_lever("prog")
        self.assert_refused(run, f"{self.derived} has mode 755, not 0700")
        self.assertEqual(list(self.derived.iterdir()), [])
        self.derived.rmdir()
        (self.derived.parent / "other").mkdir(mode=0o700)  # another program's store changes nothing
        self.derived.symlink_to(self.derived.parent / "other")
        self.assert_refused(self.run_lever("prog"), f"{self.derived} is a symlink")
        self.derived.unlink()
        self.derived.write_text("")
        self.assert_refused(self.run_lever("prog"), f"{self.derived} is not a real directory of this user")
        self.derived.unlink()
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith(f"copied 5 files to {self.derived}\n"), run.stdout)
        self.assertEqual(sorted(entry.name for entry in (self.derived.parent / "other").iterdir()), [])

    def test_a_symbolic_link_or_an_irregular_entry_in_the_live_store_refuses_before_any_copy(self):
        """Every listed entry must be a regular file with no symlink component: a link to a file, to a directory
        or dangling, and a fifo, each refuse by name before anything is made under HOME, and no file of the live
        store is read through the link (its target's text never appears)."""
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "note.md").write_text("outside the store\n")
        cases = {
            "a link to a file": ("link.md", lambda path: path.symlink_to(outside / "note.md"), "is a symlink"),
            "a link to a directory": ("linked", lambda path: path.symlink_to(outside), "is a symlink"),
            "a dangling link": ("gone.md", lambda path: path.symlink_to(self.root / "nowhere"), "is a symlink"),
            "a fifo": ("pipe", lambda path: os.mkfifo(path), "is not a regular file"),
            "a dot name": (".DS_Store", lambda path: path.write_text("Bud1\n"), "begins with '.'"),
        }
        for label, (name, plant, message) in cases.items():
            with self.subTest(label):
                path = self.live / name
                plant(path)
                for args in (("prog", "--check"), ("prog",)):
                    run = self.run_lever(*args)
                    self.assert_refused(run, message)
                    self.assertNotIn("outside the store", run.stdout + run.stderr)
                    self.assertFalse((self.home / ".local").exists(), "nothing is made under HOME")
                    self.assertEqual(sorted(self.tmp.iterdir()), [])
                path.unlink()
        self.assert_checkout_unchanged()

    def test_a_failed_cp_or_cmp_fails_removes_the_partial_copy_and_names_the_step(self):
        """A `cp` or `cmp` on PATH that exits 7 (the copy of one file, the read-back of one file) ends the run with
        exit 1 naming the tool, its status and the step; the partial copy is removed: the program directory this run
        made is gone, and one that stood empty before (regime-init's) is empty again; the checkout is untouched, and
        the next run without the stub copies everything."""
        real_cp = shutil.which("cp", path="/bin:/usr/bin")
        real_cmp = shutil.which("cmp", path="/bin:/usr/bin")
        stubs = {
            "cp": (
                f'for a; do case $a in */regime-store/*/briefs/B1.md) exit 7 ;; esac; done\nexec {real_cp} "$@"',
                "cp of briefs/B1.md exited 7 (the copy step)",
            ),
            "cmp": (
                f'for a; do case $a in */regime-store/*) exit 7 ;; esac; done\nexec {real_cmp} "$@"',
                "exited 7 (the read-back step)",
            ),
        }
        for tool, (body, message) in stubs.items():
            for pre_made in (False, True):
                with self.subTest(tool=tool, pre_made=pre_made):
                    if pre_made:
                        self.derived.mkdir(parents=True, mode=0o700)
                        for parent in (self.derived.parent, self.derived.parent.parent):
                            parent.chmod(0o700)
                    self.stub(tool, body)
                    run = self.run_lever("prog")
                    self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
                    self.assertIn(message, run.stderr)
                    self.assertIn("the partial copy under", run.stderr)
                    self.assertNotIn("copied ", run.stdout)
                    if pre_made:
                        self.assertEqual(
                            list(self.derived.iterdir()), [], "the pre-made program directory is empty again"
                        )
                        self.assertEqual(stat.S_IMODE(self.derived.lstat().st_mode), 0o700)
                        self.derived.rmdir()
                    else:
                        self.assertFalse(self.derived.exists(), "the program directory this run made is gone")
                    self.assertEqual(sorted(self.tmp.iterdir()), [])
                    self.assert_checkout_unchanged()
                    (self.bindir / tool).unlink()
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith(f"copied 5 files to {self.derived}\n"), run.stdout)

    def test_a_linked_worktree_the_arguments_and_a_missing_live_store_are_refused(self):
        """A linked worktree (a worker's clone) is refused naming it; the arguments are one program in the store
        grammar and an optional `--check`, anything else the usage line; a program with no live store under the
        checkout refuses naming the place; each before anything is read from the store or made under HOME."""
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        self.assert_refused(self.run_lever("prog", cwd=linked), "linked worktree")
        for args, message in (
            ((), "usage:"),
            (("--check",), "usage:"),
            (("prog", "other"), "usage:"),
            (("prog", "--force"), "usage:"),
            (("Bad/Name",), "outside"),
            (("absent",), f"{self.repo}/.orchestration/orchestrate/absent is not a directory of this user"),
        ):
            with self.subTest(args=args):
                self.assert_refused(self.run_lever(*args), message)
        outside = self.root / "outside"
        outside.mkdir()
        self.assert_refused(self.run_lever("prog", cwd=outside), "not in a git checkout")
        self.assertFalse((self.home / ".local").exists())
        self.assertEqual(sorted(self.tmp.iterdir()), [])
        self.assert_checkout_unchanged()


if __name__ == "__main__":
    unittest.main()
