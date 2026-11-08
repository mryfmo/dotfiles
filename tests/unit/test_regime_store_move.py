"""regime-store-move, the read-only judge of a program's store move (regime-cutover U221, U221b, U221c, U221d).

The fixture is RecordsSyncTest's shape (tests/unit/test_pr_levers.py): a scratch checkout whose committed store
`.orchestration/orchestrate/prog/` holds origin/main's masked copies, a bare origin behind the git wrapper first on
PATH, which maps the checkout's https origin URL onto that bare repository, and a scratch HOME under which the derived
root `<HOME>/.local/state/regime-store/<slug>/` stands, 0700 and empty, as hcom-seat makes it (U219). The live store is
the checkout subtree as the coordinator's main checkout holds it before the move: a file whose unmasked bytes differ
from main's masked blob, and the program's `redact-words.txt`, which origin/main never holds. The lever runs from the
checkout (its self-check reads the checkout's manifest). Nothing reads the real `~/.local/state`, and the real `git`
is reached only through the wrapper.

U221d (verdict U221-595a116a, the mechanism change of decisions 2026-11-08T10:26:46Z, form remove): the lever copies
nothing. Before the move it judges whether a records sync is still due and prints the operator's seven-line procedure;
after it (the derived store present) it reports the moved state from `git status --porcelain` of the checkout's store
subtree. Every run is held to have written nothing: the listing, every mode and every mtime under the checkout (its
`.git` included), the store root's emptiness and the scratch `TMPDIR` are equal before and after. The stubs on PATH
(`find`, `uv`, `install`, `cat`, `wc`) and the wrapper's `FAKE_GIT_FAIL` inject a failure or a warning at each
producer and each step.
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
LEVER = ROOT / "scripts/orchestrator/regime-store-move"
MASKER = ROOT / "scripts/validate-agent-assets.py"
URL = "https://github.com/acme/widgets.git"
PLANTED = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
PREFIX = ".orchestration/orchestrate/prog"
SYSTEM_PATH = "/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin"
LIVE_FILES = ["briefs/B1.md", "decisions.tsv", "notes.md", "redact-words.txt", "units.tsv"]
# The RecordsSyncTest wrapper's fake network: FAKE_GIT_HTTPS_ORIGIN="<https url>=<bare repository>" maps the https
# origin onto the local bare repository as a command-line insteadOf, and the local transport is re-opened for every
# call, as a caller's own `-c protocol.file.allow=always` would (the library's `protocol.allow=never` refuses it).
# FAKE_GIT_FAIL names a git subcommand the wrapper fails instead of running.
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
        # Runs last-in first-out: the modes a test took away are given back before the directory goes.
        self.addCleanup(self.restore_modes, self.root)
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
        # The store root as hcom-seat makes it (U219): `regime-store` and `<slug>` 0700, the program store absent.
        self.store_root = self.home / ".local/state/regime-store/repo"
        self.store_root.mkdir(parents=True)
        self.store_root.parent.chmod(0o700)
        self.store_root.chmod(0o700)
        self.derived = self.store_root / "prog"
        self.ready = "ready: 4 live files equal origin/main's masked copies\n"
        self.procedure = (
            f"1. Stop every seat and end every coordinator process: run regime-stop --all in {self.repo} (the stop of "
            "the kit, regime-start --stop --all), confirm with hcom list -v that no seat of this checkout is alive, "
            "and close every session that runs a lever of the kit against it.\n"
            f"2. cp -a {self.live} {self.derived}\n"
            f"3. diff -r {self.live} {self.derived} && find {self.derived} -type f | wc -l   # expect no line from "
            "diff and the count 5 (4 compared files and redact-words.txt)\n"
            f"4. git -C {self.repo} checkout -- {PREFIX}\n"
            f"5. git -C {self.repo} clean -fd -- {PREFIX}\n"
            f"6. git -C {self.repo} pull --ff-only\n"
            "7. regime-store-move prog\n"
        )
        self.before = self.snapshot()

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

    @staticmethod
    def restore_modes(root):
        """Every directory below `root` searchable and writable, every file writable, for the directory's removal."""
        for dirpath, dirnames, filenames in os.walk(root):
            for entry in [Path(dirpath)] + [Path(dirpath) / name for name in dirnames + filenames]:
                if entry.is_symlink():
                    continue
                try:
                    mode = stat.S_IMODE(entry.lstat().st_mode)
                    entry.chmod(mode | (0o700 if entry.is_dir() else 0o200))
                except OSError:
                    pass

    def snapshot(self):
        """What a run must leave as it found it: every entry under the checkout (`.git` included) with its mode, its
        mtime and its size, the entries under the store root, and the entries of the scratch TMPDIR."""
        checkout = {}
        for entry in sorted(self.repo.rglob("*")):
            info = entry.lstat()
            checkout[str(entry.relative_to(self.repo))] = (info.st_mode, info.st_mtime_ns, info.st_size)
        return checkout, self.root_entries(), sorted(self.tmp.iterdir())

    def root_entries(self):
        """Every entry below the store root, with the bytes of each file (a derived store must be left as it was)."""
        found = {}
        for entry in sorted(self.store_root.rglob("*")):
            found[str(entry.relative_to(self.store_root))] = (
                entry.lstat().st_mode,
                entry.read_bytes() if entry.is_file() and not entry.is_symlink() else None,
            )
        return found

    def assert_nothing_written(self, run, snapshot=None):
        """The checkout, the store root and the scratch TMPDIR are as they were before the run (the scratch
        directory removed), and origin still holds main alone."""
        self.assertEqual(self.snapshot(), snapshot or self.before, "nothing under the checkout or the root changed")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        self.assertEqual(self.git("ls-remote", "--heads", str(self.origin)).count("refs/heads/"), 1, "main only")

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)
        self.assertEqual(run.stdout, "", "a refusal prints no verdict and no procedure")

    def restore_live(self):
        """The live store as the fixture made it: main's copies checked out, notes.md unmasked again, nothing extra."""
        if (self.live / "notes.md").is_symlink():
            (self.live / "notes.md").unlink()
        self.git("checkout", "-q", "--", PREFIX)
        (self.live / "notes.md").write_text(f"token {PLANTED}\n")
        (self.live / "redact-words.txt").write_text("# words\nwidgetsecret\n")
        for extra in ("extra.md", "briefs/B2.md"):
            (self.live / extra).unlink(missing_ok=True)

    def make_derived_store(self):
        """The derived store as the operator's copy leaves it: every file of the live store, the directory 0700."""
        shutil.copytree(self.live, self.derived)
        self.derived.chmod(0o700)

    def stub(self, name, body):
        """A tool first on PATH in place of the system's; the body is `sh` text that may exec the real one."""
        path = self.bindir / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def unstub(self, *names):
        for name in names:
            (self.bindir / name).unlink(missing_ok=True)

    def real(self, name):
        """The system's tool, for a stub that passes the calls it does not inject through."""
        path = shutil.which(name, path=SYSTEM_PATH)
        self.assertIsNotNone(path, f"{name} on {SYSTEM_PATH}")
        return path

    def failing_stub(self, name, pattern, status=7):
        """`name` exits `status` when any argument matches the sh pattern, else runs the system's tool."""
        self.stub(name, f'for a; do case $a in {pattern}) exit {status} ;; esac; done\nexec {self.real(name)} "$@"')

    def warning_stub(self, name, pattern):
        """`name` writes one line to stderr when any argument matches the pattern, then runs the system's tool."""
        self.stub(
            name,
            f"for a; do case $a in {pattern}) echo '{name}: warning: injected' >&2 ;; esac; done\n"
            f'exec {self.real(name)} "$@"',
        )

    def test_the_pre_move_run_prints_ready_and_the_procedure_and_writes_nothing(self):
        """U221d test (a): with the derived store absent and the live store's files equal to origin/main's blobs at
        the published prefix once masked (notes.md holds a token main holds masked; `redact-words.txt` is the one
        live path main need not hold), the run prints `ready: 4 ...` and the seven numbered lines of the operator's
        procedure, byte-exact for the fixture's paths, and writes nothing: every entry under the checkout keeps its
        mode, mtime and size, the store root stays empty, the scratch directory goes, and the live store's modes are
        as they were (no quiescence by mode). The run is repeatable: the second prints the same."""
        for attempt in (1, 2):
            with self.subTest(attempt=attempt):
                run = self.run_lever("prog")
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(run.stdout, self.ready + self.procedure)
                self.assertIn(
                    f"regime-store-move: live store {self.live} (5 files); derived store {self.derived}", run.stderr
                )
                self.assertIn("equals the live store masked", run.stderr)
                self.assertNotIn("made unwritable", run.stderr)
                self.assertEqual(run.stdout.count("\n"), 8, "one verdict line and seven lines")
                self.assertEqual(run.stdout.count("cp -a"), 1, "the copy is the operator's, once")
                self.assertIn(PLANTED, (self.live / "notes.md").read_text(), "the live file is untouched")
                self.assertFalse(self.derived.exists(), "the lever makes no derived store")
                self.assert_nothing_written(run)

    def test_a_live_file_that_differs_from_main_masked_or_a_path_main_lacks_or_holds_alone_refuses(self):
        """U221d test (b): a records sync is still due when a live file's masked form differs from main's blob, when a
        live path is absent from main (`redact-words.txt` aside), or when main holds a path the live store no longer
        does (a deletion the sync would carry): the refusal names the count, not the paths (a path may hold a redact
        word), no procedure is printed, and nothing is written."""
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
                before = self.snapshot()
                run = self.run_lever("prog")
                self.assert_refused(run, f"a records sync is still due ({count} path(s) differ")
                self.assertIn("the procedure is not printed", run.stderr)
                self.assertNotIn("units.tsv", run.stderr + run.stdout, "no path is named")
                self.assertNotIn("regime-store-move prog", run.stdout + run.stderr, "no procedure")
                self.assert_nothing_written(run, before)
        self.restore_live()

    def test_a_derived_store_present_reports_moved_when_the_checkout_store_is_clean_and_refuses_when_it_is_not(self):
        """U221d test (c): with the derived store present (the operator's copy: every live file, the directory 0700)
        the lever judges the operator's step by `git status --porcelain` of the checkout's store subtree. The
        fixture's checkout store is dirty (notes.md modified, `redact-words.txt` untracked): `refused: the checkout
        store is not clean (2 entries); finish the step`, exit 2, no verdict on stdout. After the step (main's copies
        checked out, `redact-words.txt` gone) it prints `moved: the derived store holds 5 files; the checkout store
        is clean against HEAD` and exits 0. Either way nothing is written: the derived store's bytes, the checkout
        and the scratch directory are as before. A `git status` that fails refuses naming it; a derived store with
        no file, with another mode, a link or a file at the program's place refuses by name."""
        self.make_derived_store()
        before = self.snapshot()
        run = self.run_lever("prog")
        self.assert_refused(run, "the checkout store is not clean (2 entries); finish the step")
        self.assertNotIn("ready:", run.stdout + run.stderr)
        self.assert_nothing_written(run, before)
        with self.subTest("git status fails"):
            run = self.run_lever("prog", FAKE_GIT_FAIL="status")
            self.assert_refused(run, f"cannot read git status of {PREFIX} (git status failed or warned")
            self.assert_nothing_written(run, before)
        # The operator's step, lines 4 and 5 of the procedure: the checkout store holds main's copies alone.
        self.git("checkout", "-q", "--", PREFIX)
        (self.live / "redact-words.txt").unlink()
        self.assertEqual(self.git("status", "--porcelain", "--", PREFIX), "", "the fixture's step is finished")
        before = self.snapshot()
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout, "moved: the derived store holds 5 files; the checkout store is clean against HEAD\n"
        )
        self.assertIn(
            f"regime-store-move: derived store {self.derived} (5 files); checkout store {self.live} clean", run.stderr
        )
        self.assertNotIn("ready:", run.stdout)
        self.assert_nothing_written(run, before)
        self.assertIn(PLANTED, (self.derived / "notes.md").read_text(), "the derived store holds the live bytes")
        with self.subTest("an empty derived store"):
            shutil.rmtree(self.derived)
            self.derived.mkdir(mode=0o700)
            before = self.snapshot()
            run = self.run_lever("prog")
            self.assert_refused(run, f"the derived store {self.derived} exists and holds no file")
            self.assert_nothing_written(run, before)
        with self.subTest("another mode, a link, a file"):
            self.derived.chmod(0o755)
            before = self.snapshot()
            self.assert_refused(self.run_lever("prog"), f"{self.derived} has mode 755, not 0700")
            self.assert_nothing_written(run, before)
            self.derived.rmdir()
            (self.derived.parent / "other").mkdir(mode=0o700)  # another program's store changes nothing
            self.derived.symlink_to(self.derived.parent / "other")
            self.assert_refused(self.run_lever("prog"), f"{self.derived} is a symlink")
            self.derived.unlink()
            self.derived.write_text("")
            self.assert_refused(self.run_lever("prog"), f"{self.derived} is not a real directory of this user")
            self.derived.unlink()
            self.assertEqual(sorted(entry.name for entry in self.store_root.iterdir()), ["other"])

    def test_a_symbolic_link_or_an_irregular_entry_in_the_live_store_refuses(self):
        """U221d test (d), the live store's shape: every listed entry must be a regular file with no symlink
        component. A link to a file, to a directory or dangling, a fifo and a dot name each refuse by name before
        the fetch, no file of the live store is read through the link (its target's text never appears), no
        procedure is printed and nothing is written."""
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
                before = self.snapshot()
                run = self.run_lever("prog")
                self.assert_refused(run, message)
                self.assertIn("the procedure is not printed", run.stderr)
                self.assertNotIn("outside the store", run.stdout + run.stderr)
                self.assertNotIn("a records sync is still due", run.stderr, "refused before the fetch")
                self.assert_nothing_written(run, before)
                path.unlink()
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")

    def test_a_non_https_origin_an_absent_store_root_and_each_injected_read_or_step_failure_refuse(self):
        """U221d test (d), the producers (standing order 21): a non-https origin URL refuses before the fetch; a store
        root that does not exist refuses naming it (hcom-seat makes it); a read that fails or warns (the live store's
        walk, the `origin` URL, the counts by `wc`) refuses with exit 2 naming the producer; a step after the reads
        that fails (the scratch fetch, the tools tree's `install -d`, the `cat` of a live file into its scratch copy,
        the masker) exits 1 naming the step. Each prints no procedure and writes nothing, and the run without the
        injection prints the procedure again."""
        live = "*/.orchestration/orchestrate/*"
        tools = ("find", "uv", "install", "cat", "wc")
        cases = (
            ("the source walk fails", lambda: self.failing_stub("find", live), {}, 2, ("find", "walk of")),
            ("the source walk warns", lambda: self.warning_stub("find", live), {}, 2, ("find", "walk of")),
            ("the origin URL read", lambda: None, {"FAKE_GIT_FAIL": "config"}, 2, ("remote.origin.url",)),
            (
                "the count of the live store",
                lambda: self.failing_stub("wc", "-c"),
                {},
                2,
                ("cannot count the live store",),
            ),
            (
                "the count of the compared files",
                lambda: self.failing_stub("wc", "-l"),
                {},
                2,
                ("cannot count the compared files (wc failed)",),
            ),
            ("the scratch fetch", lambda: None, {"FAKE_GIT_FAIL": "fetch"}, 1, ("git fetch main from origin failed",)),
            (
                "the tools tree",
                lambda: self.failing_stub("install", "*/tools/*"),
                {},
                1,
                ("cannot make the tools tree",),
            ),
            (
                "the read of a live file into its scratch copy",
                lambda: self.failing_stub("cat", live),
                {},
                1,
                ("the read of a live file into its scratch copy failed (cat)",),
            ),
            ("the masker", lambda: self.stub("uv", "exit 7"), {}, 1, ("masking the copies failed (exit 7)",)),
        )
        for label, plant, env, status, messages in cases:
            with self.subTest(label):
                self.unstub(*tools)
                plant()
                run = self.run_lever("prog", **env)
                self.assertEqual(run.returncode, status, run.stdout + run.stderr)
                for message in messages:
                    self.assertIn(message, run.stderr)
                if status == 2:
                    self.assertIn("refused:", run.stderr)
                self.assertEqual(run.stdout, "", "no verdict and no procedure")
                self.unstub(*tools)
                self.assert_nothing_written(run)
        with self.subTest("a non-https origin"):
            self.git("remote", "set-url", "origin", "git@github.com:acme/widgets.git")
            before = self.snapshot()
            run = self.run_lever("prog")
            self.assert_refused(run, "needs an https origin URL, not git@github.com:acme/widgets.git")
            self.assert_nothing_written(run, before)
            self.git("remote", "set-url", "origin", URL)
        with self.subTest("the store root does not exist"):
            self.store_root.rmdir()
            before = self.snapshot()
            run = self.run_lever("prog")
            self.assert_refused(run, f"the store root {self.store_root} does not exist")
            self.assertFalse(self.store_root.exists(), "the lever makes no root")
            self.assertEqual(self.snapshot(), before)
            self.store_root.mkdir(mode=0o700)
        before = self.snapshot()
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, self.ready + self.procedure)
        self.assert_nothing_written(run, before)

    def test_a_linked_worktree_the_arguments_and_a_missing_live_store_are_refused(self):
        """U221d test (e) with the earlier refusals: a linked worktree (a worker's clone) is refused naming it; the one
        argument is a program in the store grammar, and anything else is the usage line, `--check` included (the flag
        is gone: one mode remains) and a second argument of any kind; a program with no live store under the checkout
        refuses naming the place; each before anything is read from the store or written anywhere."""
        linked = self.root / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked))
        before = self.snapshot()
        self.assert_refused(self.run_lever("prog", cwd=linked), "linked worktree")
        for args, message in (
            ((), "usage: regime-store-move <program>"),
            (("--check",), "usage: regime-store-move <program>"),
            (("prog", "--check"), "usage: regime-store-move <program>"),
            (("--check", "prog"), "usage: regime-store-move <program>"),
            (("prog", "other"), "usage: regime-store-move <program>"),
            (("prog", "--force"), "usage: regime-store-move <program>"),
            (("Bad/Name",), "outside"),
            (("absent",), f"{self.repo}/.orchestration/orchestrate/absent is not a directory of this user"),
        ):
            with self.subTest(args=args):
                run = self.run_lever(*args)
                self.assert_refused(run, message)
                self.assertNotIn("regime-store-move: live store", run.stderr, "nothing read from the store")
        outside = self.root / "outside"
        outside.mkdir()
        self.assert_refused(self.run_lever("prog", cwd=outside), "not in a git checkout")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(sorted(self.tmp.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
