"""regime-store-move, the one-time copy of a program's live store to the derived root (regime-cutover U221, U221b).

The fixture is RecordsSyncTest's shape (tests/unit/test_pr_levers.py): a scratch checkout whose committed store
`.orchestration/orchestrate/prog/` holds origin/main's masked copies, a bare origin behind the git wrapper first on
PATH, which maps the checkout's https origin URL onto that bare repository, and a scratch HOME under which the derived
root `<HOME>/.local/state/regime-store/<slug>/` is made. The live store is the checkout subtree as the coordinator's
main checkout holds it before the move: a file whose unmasked bytes differ from main's masked blob, and the program's
`redact-words.txt`, which origin/main never holds. The lever runs from the checkout (its self-check reads the checkout's
manifest). Nothing reads the real `~/.local/state`, and the real `git` is reached only through the wrapper.

U221b (verdict U221-e82581f3, class move-race): the wrapper runs a shell snippet when the lever's scratch fetch runs
(`FAKE_GIT_ON_FETCH`), the window between the live store's manifest and the copy, and the stubs on PATH (`cp`, `cmp`,
`mv`, `find`, `uv`, the hash tool) inject a failure, a warning or a concurrent write at each producer and each step.
"""

import hashlib
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
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/regime-store-move"
MASKER = ROOT / "scripts/validate-agent-assets.py"
URL = "https://github.com/acme/widgets.git"
PLANTED = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
PREFIX = ".orchestration/orchestrate/prog"
SYSTEM_PATH = "/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin"
STAGING = re.compile(r"^\.prog\.moving-[0-9]+$")
IDENTITY = re.compile(
    r"^regime-store-move: staging (\S+) \(identity ([0-9]+):([0-9]+)\) renamed to (\S+)$", re.MULTILINE
)
# The RecordsSyncTest wrapper's fake network: FAKE_GIT_HTTPS_ORIGIN="<https url>=<bare repository>" maps the https
# origin onto the local bare repository as a command-line insteadOf, and the local transport is re-opened for every
# call, as a caller's own `-c protocol.file.allow=always` would (the library's `protocol.allow=never` refuses it).
# FAKE_GIT_ON_FETCH is a shell snippet run before a `fetch`: a write that lands while the lever's scratch fetch runs.
GIT_WRAPPER = """#!/usr/bin/env python3
import os, subprocess, sys
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in sys.argv[1:]:
    print("fake-git: failing as asked", file=sys.stderr)
    sys.exit(1)
if os.environ.get("FAKE_GIT_ON_FETCH") and "fetch" in sys.argv[1:]:
    subprocess.run(["/bin/sh", "-c", os.environ["FAKE_GIT_ON_FETCH"]], check=True)
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
        self.store_root = self.home / ".local/state/regime-store/repo"
        self.derived = self.store_root / "prog"
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

    def live_files(self):
        """The store-relative paths of the live store's regular files, what the lever's manifest lists."""
        return sorted(str(entry.relative_to(self.live)) for entry in self.live.rglob("*") if entry.is_file())

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

    def staging_entries(self):
        """Every `.prog.moving-<pid>` entry under the store root and under the final name, wherever the rename left it."""
        found = []
        for parent in (self.store_root, self.derived):
            if parent.is_dir() and not parent.is_symlink():
                found += [str(entry) for entry in parent.iterdir() if STAGING.match(entry.name)]
        return found

    def assert_nothing_under_the_final_name(self, run):
        """A failed or refused run: no staging directory anywhere under the root, nothing at the final name, the
        scratch directory removed, the checkout untouched (the planted writes restored by the caller first)."""
        self.assertEqual(self.staging_entries(), [], "no staging directory is left")
        self.assertFalse(self.derived.exists() or self.derived.is_symlink(), "nothing under the final name")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        self.assertNotIn("copied ", run.stdout)
        self.assert_checkout_unchanged()

    def assert_refused(self, run, message):
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)

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

    def hash_tool(self):
        """The hash tool the lever picks: `sha256sum` when the system has one, else `shasum`."""
        return "sha256sum" if shutil.which("sha256sum", path=SYSTEM_PATH) else "shasum"

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

    def make_derived_store(self, text="id\tx\nU7\tz\n"):
        """The sh snippet a concurrent writer runs: the program store made 0700 under the root with a units.tsv."""
        return f"umask 077 && mkdir -p {self.derived} && printf '%s' '{text}' > {self.derived}/units.tsv"

    def restore_live(self):
        """The live store as the fixture made it: main's copies checked out, notes.md unmasked again, nothing extra."""
        if (self.live / "notes.md").is_symlink():
            (self.live / "notes.md").unlink()
        self.git("checkout", "-q", "--", PREFIX)
        (self.live / "notes.md").write_text(f"token {PLANTED}\n")
        for extra in ("extra.md", "briefs/B2.md", "briefs/B3.md"):
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

    def test_the_move_copies_every_file_into_a_staging_directory_renames_it_into_place_and_prints_the_step(self):
        """The default run (U221b test (f)): the components `regime-store` and `<slug>` made 0700 under the scratch
        HOME, every regular file of the live store's manifest copied with `cp -p` into the staging directory
        `<root>/.prog.moving-<pid>` (`redact-words.txt` and the unmasked notes.md included: the new root is the live
        store, not main's copy), each read back, the staging directory renamed to the final name by `mv -n`, and the
        final name's identity (device and inode, the stderr line) equal to the staging directory's; `copied <n> files`
        names the manifest's count; the checkout is byte-identical before and after; no staging entry remains. A
        second run refuses: the final name exists."""
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, f"copied {len(self.live_files())} files to {self.derived}\n{self.step}")
        self.assert_checkout_unchanged()
        renamed = IDENTITY.search(run.stderr)
        self.assertIsNotNone(renamed, run.stderr)
        staging, device, inode, final = renamed.groups()
        self.assertEqual(Path(staging).parent, self.store_root)
        self.assertRegex(Path(staging).name, STAGING)
        self.assertEqual(final, str(self.derived))
        identity = self.derived.lstat()
        self.assertEqual((int(device), int(inode)), (identity.st_dev, identity.st_ino), "the renamed directory")
        self.assertEqual(self.staging_entries(), [], "the staging directory is the final name now")
        for component in (self.store_root.parent, self.store_root, self.derived):
            self.assertEqual(stat.S_IMODE(component.lstat().st_mode), 0o700, component)
            self.assertFalse(component.is_symlink())
        copied = sorted(str(entry.relative_to(self.derived)) for entry in self.derived.rglob("*") if entry.is_file())
        self.assertEqual(copied, ["briefs/B1.md", "decisions.tsv", "notes.md", "redact-words.txt", "units.tsv"])
        self.assertEqual(copied, self.live_files())
        for relative in copied:
            with self.subTest(file=relative):
                source = self.live / relative
                target = self.derived / relative
                self.assertEqual(target.read_bytes(), source.read_bytes())
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), stat.S_IMODE(source.stat().st_mode))
        self.assertIn(PLANTED, (self.derived / "notes.md").read_text(), "the live file moves as it is, unmasked")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        again = self.run_lever("prog")
        self.assert_refused(again, f"{self.derived} already exists")
        self.assertEqual(
            sorted(str(entry.relative_to(self.derived)) for entry in self.derived.rglob("*") if entry.is_file()), copied
        )
        self.assertEqual(self.staging_entries(), [])
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

    def test_a_derived_store_that_already_exists_or_has_another_mode_refuses(self):
        """A `<root>/<program>` that exists at the start refuses by name before the fetch, whether it holds an entry
        (a dot file too) or stands empty: the move renames its staging directory to that name and never writes into a
        directory that is already there (U221b); a component found with a mode other than 0700, a link or a file at
        the program's place refuses by name (regime-init's component holds). Nothing is copied and the entry is left as
        it was."""
        self.derived.mkdir(parents=True, mode=0o700)
        for parent in (self.derived.parent, self.derived.parent.parent):
            parent.chmod(0o700)
        (self.derived / ".keep").write_text("kept\n")
        for args in (("prog", "--check"), ("prog",)):
            with self.subTest(args=args):
                run = self.run_lever(*args)
                self.assert_refused(run, f"{self.derived} already exists")
                self.assertEqual([entry.name for entry in self.derived.iterdir()], [".keep"])
                self.assertEqual(self.staging_entries(), [])
                self.assert_checkout_unchanged()
        (self.derived / ".keep").unlink()
        for args in (("prog", "--check"), ("prog",)):
            with self.subTest(args=args, empty=True):
                run = self.run_lever(*args)
                self.assert_refused(run, f"{self.derived} already exists")
                self.assertEqual(list(self.derived.iterdir()), [])
                self.assertEqual(self.staging_entries(), [])
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
        self.assertEqual(self.staging_entries(), [])
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

    def test_a_failed_cp_cmp_or_mv_fails_removes_the_staging_directory_and_names_the_step(self):
        """A `cp`, `cmp` or `mv` on PATH that exits 7 (the copy of one file into the staging directory, the read-back
        of one file, the rename) ends the run with exit 1 naming the tool, its status and the step; the staging
        directory is removed by its own name, nothing stands at the final name, the store root is left empty, the
        checkout is untouched, and the next run without the stub copies everything."""
        stubs = {
            "cp": ("*/regime-store/*/briefs/B1.md", "cp of briefs/B1.md exited 7 (the copy step)"),
            "cmp": ("*/regime-store/*", "exited 7 (the read-back step)"),
            "mv": ("*/regime-store/*", "exited 7 (the rename step)"),
        }
        for tool, (pattern, message) in stubs.items():
            with self.subTest(tool=tool):
                self.failing_stub(tool, pattern)
                run = self.run_lever("prog")
                self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
                self.assertIn(message, run.stderr)
                self.assertIn("the staging directory", run.stderr)
                self.assertIn("was removed", run.stderr)
                self.assertEqual(sorted(self.store_root.iterdir()), [], "the store root is empty again")
                self.assert_nothing_under_the_final_name(run)
                self.unstub(tool)
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith(f"copied 5 files to {self.derived}\n"), run.stdout)

    def test_a_record_added_or_edited_during_the_move_refuses_naming_the_count_and_leaves_nothing_under_the_root(self):
        """U221b test (a) (verdict P1 `:492`): the live store's manifest (every path with its size and sha256) is taken
        once at the start and taken again after the copy; a record added while the scratch fetch runs (the git
        wrapper's hook) or edited while the copy runs (a `cp` stub, on its first call into the staging directory)
        makes the second manifest differ, and the run refuses naming the count of changed paths with exit 2: no
        staging directory and nothing at the final name are left, so the printed step can delete no record."""
        marker = self.root / "cp-first-call"
        edit_once = (
            f"for a; do case $a in */regime-store/*) if [ ! -e {marker} ]; then : > {marker}; "
            f"printf 'U9\\tseats\\n' >> {self.live}/units.tsv; fi ;; esac; done\nexec {self.real('cp')} \"$@\""
        )
        cases = (
            ("a record added during the fetch", {"FAKE_GIT_ON_FETCH": f"printf 'b\\n' > {self.live}/briefs/B2.md"}, 1),
            (
                "two records added during the fetch",
                {
                    "FAKE_GIT_ON_FETCH": f"printf 'b\\n' > {self.live}/briefs/B2.md && printf 'n\\n' > {self.live}/extra.md"
                },
                2,
            ),
            ("a record edited during the copy", {"stub": ("cp", edit_once)}, 1),
        )
        for label, how, count in cases:
            with self.subTest(label):
                self.unstub("cp")
                marker.unlink(missing_ok=True)
                self.restore_live()
                env = {}
                if "stub" in how:
                    self.stub(*how["stub"])
                else:
                    env = how
                run = self.run_lever("prog", **env)
                self.assert_refused(run, f"the live store changed during the move ({count} path")
                self.assertIn("nothing moved", run.stderr)
                self.assertNotIn("units.tsv", run.stderr, "no path is named")
                self.assertNotIn("B2.md", run.stderr, "no path is named")
                self.unstub("cp")
                marker.unlink(missing_ok=True)
                self.restore_live()
                self.assert_nothing_under_the_final_name(run)
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith(f"copied 5 files to {self.derived}\n"), run.stdout)

    def test_a_destination_that_appears_during_the_move_makes_the_rename_refuse_and_leaves_it_untouched(self):
        """U221b test (b) (verdict P1 `:482`): a `<root>/<program>` made by another writer after the start, holding a
        `units.tsv`, is never written into. Appearing during the fetch, it is found before the rename and the run
        refuses by name; appearing between that hold and the rename (the `mv` stub makes it, then runs the real
        `mv -n`, which moves the staging directory into the directory that took the name), the final name's identity
        differs from the staging directory's and the run refuses; either way the file keeps its bytes, the staging
        directory is removed wherever the rename left it, and nothing else under the final name is touched."""
        text = "id\tx\nU7\tz\n"
        cases = (
            ("during the fetch", {"FAKE_GIT_ON_FETCH": self.make_derived_store(text)}, "appeared during the move"),
            (
                "between the hold and the rename",
                {"stub": ("mv", f'{self.make_derived_store(text)}\nexec {self.real("mv")} "$@"')},
                "is not the staging directory after the rename",
            ),
        )
        for label, how, message in cases:
            with self.subTest(label):
                self.unstub("mv")
                env = {}
                if "stub" in how:
                    self.stub(*how["stub"])
                else:
                    env = how
                run = self.run_lever("prog", **env)
                self.assert_refused(run, message)
                self.assertIn("nothing moved", run.stderr)
                self.assertEqual((self.derived / "units.tsv").read_text(), text, "the file is untouched")
                self.assertEqual([entry.name for entry in self.derived.iterdir()], ["units.tsv"], "nothing else")
                self.assertEqual(self.staging_entries(), [], "the staging directory is removed wherever it stands")
                self.assertEqual(sorted(self.tmp.iterdir()), [])
                self.assertNotIn("copied ", run.stdout)
                self.unstub("mv")
                shutil.rmtree(self.derived)
                self.assert_checkout_unchanged()
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.startswith(f"copied 5 files to {self.derived}\n"), run.stdout)

    def test_an_extra_entry_under_the_root_survives_a_failed_run(self):
        """U221b test (c) (verdict P1 `:482`, the cleanup; verdict line 18: an extra destination file written during
        the fetch was deleted by the cleanup): the failure cleanup removes the staging directory alone, by its own
        name. Another program's store and a stray file under the root, present before a run whose read-back fails,
        are still there after it, and so is a file another writer put under the final name while the scratch fetch
        ran: nothing under the final name is this run's, so nothing there is removed."""
        self.store_root.mkdir(parents=True, mode=0o700)
        self.store_root.parent.chmod(0o700)
        (self.store_root / "other").mkdir(mode=0o700)
        (self.store_root / "other/units.tsv").write_text("other\n")
        (self.store_root / "stray.txt").write_text("stray\n")
        self.failing_stub("cmp", "*/regime-store/*")
        hook = f"umask 077 && mkdir -p {self.derived} && printf 'theirs\\n' > {self.derived}/extra.md"
        run = self.run_lever("prog", FAKE_GIT_ON_FETCH=hook)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("exited 7 (the read-back step)", run.stderr)
        self.assertEqual(sorted(entry.name for entry in self.store_root.iterdir()), ["other", "prog", "stray.txt"])
        self.assertEqual((self.store_root / "other/units.tsv").read_text(), "other\n")
        self.assertEqual((self.store_root / "stray.txt").read_text(), "stray\n")
        self.assertEqual([entry.name for entry in self.derived.iterdir()], ["extra.md"], "the other writer's file")
        self.assertEqual((self.derived / "extra.md").read_text(), "theirs\n")
        self.assertEqual(self.staging_entries(), [], "no staging directory is left")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        self.assertNotIn("copied ", run.stdout)
        self.assert_checkout_unchanged()
        self.unstub("cmp")

    def test_a_source_file_replaced_by_a_link_during_the_fetch_refuses(self):
        """U221b test (d) (verdict line 19, kept): a live file replaced by a symbolic link while the scratch fetch
        runs refuses with exit 2 and nothing under the final name: a link to other bytes fails the masked comparison
        (a sync is still due); a link to the same bytes passes it and is refused by the walk after the copy, which
        holds every entry to the derived walk's shape again. The target's text never appears."""
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "note.md").write_text("outside the store\n")
        (outside / "same.md").write_text(f"token {PLANTED}\n")
        cases = (
            ("a link to other bytes", outside / "note.md", "a records sync is still due"),
            ("a link to the same bytes", outside / "same.md", "is a symlink"),
        )
        for label, target, message in cases:
            with self.subTest(label):
                hook = f"rm {self.live}/notes.md && ln -s {target} {self.live}/notes.md"
                run = self.run_lever("prog", FAKE_GIT_ON_FETCH=hook)
                self.assert_refused(run, message)
                self.assertNotIn("outside the store", run.stdout + run.stderr)
                self.assertTrue((self.live / "notes.md").is_symlink(), "the hook ran")
                self.restore_live()
                self.assert_nothing_under_the_final_name(run)

    def test_an_injected_failure_or_warning_of_each_read_or_step_refuses_and_leaves_nothing_under_the_root(self):
        """U221b test (e) (verdict P2 `tests:306`, standing order 21): each producer the decision rests on fails
        closed. A read that fails or warns (the source walk, the destination walk, the hash of a manifest entry, the
        `origin` URL, the identity of the final name) refuses with exit 2; a step after the reads that fails (the
        scratch fetch, the masker) exits 1; each names the producer, leaves no staging directory and nothing at the
        final name."""
        live = "*/.orchestration/orchestrate/*"
        staging = "*/regime-store/*"
        cases = (
            ("the source walk fails", lambda: self.failing_stub("find", live), {}, 2, ("find", "walk of")),
            ("the source walk warns", lambda: self.warning_stub("find", live), {}, 2, ("find", "walk of")),
            ("the destination walk fails", lambda: self.failing_stub("find", staging), {}, 2, ("find", "walk of")),
            ("the destination walk warns", lambda: self.warning_stub("find", staging), {}, 2, ("find", "walk of")),
            (
                "the hash of a manifest entry",
                lambda: self.failing_stub(self.hash_tool(), live),
                {},
                2,
                (self.hash_tool(), "cannot hash"),
            ),
            ("the origin URL read", lambda: None, {"FAKE_GIT_FAIL": "config"}, 2, ("remote.origin.url",)),
            (
                "the identity read of the final name",
                lambda: self.stub("mv", "exit 0"),
                {},
                2,
                ("cannot read the identity of", "/usr/bin/stat"),
            ),
            ("the scratch fetch", lambda: None, {"FAKE_GIT_FAIL": "fetch"}, 1, ("git fetch main from origin failed",)),
            ("the masker", lambda: self.stub("uv", "exit 7"), {}, 1, ("masking the copies failed (exit 7)",)),
        )
        for label, plant, env, status, messages in cases:
            with self.subTest(label):
                self.unstub("find", "mv", "uv", "sha256sum", "shasum")
                plant()
                run = self.run_lever("prog", **env)
                self.assertEqual(run.returncode, status, run.stdout + run.stderr)
                for message in messages:
                    self.assertIn(message, run.stderr)
                if status == 2:
                    self.assertIn("refused:", run.stderr)
                self.unstub("find", "mv", "uv", "sha256sum", "shasum")
                self.assert_nothing_under_the_final_name(run)
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
