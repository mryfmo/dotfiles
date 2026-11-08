"""regime-store-move, the read-only judge of a program's store move (regime-cutover U221 to U221e, U393).

The fixture is RecordsSyncTest's shape (tests/unit/test_pr_levers.py): a scratch checkout whose committed store
`.orchestration/orchestrate/prog/` holds what origin/main published, a bare origin behind the git wrapper first on
PATH, which maps the checkout's https origin URL onto that bare repository for the fixture's own push and fetch, and a
scratch HOME under which the derived root `<HOME>/.local/state/regime-store/<slug>/` stands, 0700 and empty, as
hcom-seat makes it (U219). The live store is the checkout subtree as the coordinator's main checkout holds it before
the move: a file whose unmasked bytes differ from main's copy (the fixture masks the committed `notes.md` with the
checkout's `validate-agent-assets.py --mask-secrets`, so the checkout store is dirty, as the real one is), and the
program's `redact-words.txt`, which origin/main never holds. The lever runs from the checkout (its self-check reads
the checkout's manifest). Nothing reads the real `~/.local/state`, and the real `git` is reached only through the
wrapper, which logs every call into `FAKE_GIT_LOG` when it is set.

U221d (verdict U221-595a116a, the mechanism change of decisions 2026-11-08T10:26:46Z, form remove): the lever copies
nothing. Before the move it prints the operator's seven-line procedure; after it (the derived store present) it
reports the moved state from `git status --porcelain` of the checkout's store subtree. Every run is held to have
written nothing: the listing, every mode and every mtime under the checkout (its `.git` included), the store root's
emptiness and the scratch `TMPDIR` are equal before and after. The stubs on PATH (`find`, `cat`, `wc`, `tr`, `rm`) and
the wrapper's `FAKE_GIT_FAIL` and `FAKE_GIT_WARN` inject a failure or a warning at each producer.

U221e (verdict U221-af547232, class read-rigor): the printed procedure is the operator's contract, so the fixture runs
its lines as written (`make_derived_store` runs the printed copy line and nothing else; the procedure test runs lines
2 to 6 and then the lever) and the lever's own post-move check judges the result; a name with a trailing space, as a
file or a dangling link, is refused by name; a `ready` run leaves nothing under the fixture's HOME; a producer that
warns while printing a valid value is a failed read; a failed scratch removal ends the run with exit 1 after the
verdict; and `tr` and `git rev-parse` each carry a committed injection, with a `stat` planted on PATH shown never to
be run (the mode read is `/usr/bin/stat`'s).

U393: the comparison with origin/main is gone (the live store is ahead of main after every records sync, so the gate
could never pass). The pre-move verdict is `ready: <n> live files; the derived store is absent`; a live store ahead
of main prints it with the procedure, the wrapper logs no `fetch`, the scratch directory holds no listing of main and
no copy map, and a checkout with no origin at all prints the same.
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
LIVE_FILES = ["briefs/B1.md", "decisions.tsv", "ledger.tsv", "notes.md", "redact-words.txt", "units.tsv"]
# The RecordsSyncTest wrapper's fake network: FAKE_GIT_HTTPS_ORIGIN="<https url>=<bare repository>" maps the https
# origin onto the local bare repository as a command-line insteadOf, and the local transport is re-opened for every
# call, as a caller's own `-c protocol.file.allow=always` would (the library's `protocol.allow=never` refuses it).
# FAKE_GIT_FAIL names a git subcommand the wrapper fails instead of running; FAKE_GIT_WARN names one the wrapper runs
# after one line on stderr (a producer that warns while exiting 0 with its output, the shape read_listing refuses).
# FAKE_GIT_LOG names a file the wrapper appends each call's arguments to, one line per call (U393: a test reads which
# git commands a lever run made).
GIT_WRAPPER = """#!/usr/bin/env python3
import os, subprocess, sys
if os.environ.get("FAKE_GIT_LOG"):
    with open(os.environ["FAKE_GIT_LOG"], "a") as log:
        log.write(" ".join(sys.argv[1:]) + "\\n")
if os.environ.get("FAKE_GIT_FAIL") and os.environ["FAKE_GIT_FAIL"] in sys.argv[1:]:
    print("fake-git: failing as asked", file=sys.stderr)
    sys.exit(1)
if os.environ.get("FAKE_GIT_WARN") and os.environ["FAKE_GIT_WARN"] in sys.argv[1:]:
    print("fake-git: warning: injected", file=sys.stderr)
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
        (self.live / "ledger.tsv").write_text("ts\tunit\tevent\n")
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
        # `-u`: the procedure's line 6 is `git pull --ff-only`, which needs the branch's upstream (the coordinator's
        # main tracks origin/main).
        self.git("push", "-q", "-u", "origin", "main")
        self.git("fetch", "-q", "origin")
        # The store root as hcom-seat makes it (U219): `regime-store` and `<slug>` 0700, the program store absent.
        self.store_root = self.home / ".local/state/regime-store/repo"
        self.store_root.mkdir(parents=True)
        self.store_root.parent.chmod(0o700)
        self.store_root.chmod(0o700)
        self.derived = self.store_root / "prog"
        self.ready = self.ready_line(6)
        self.procedure = self.procedure_for(6)
        self.before = self.snapshot()

    def ready_line(self, count):
        """The pre-move verdict for a live store of `count` files (U393: the count alone, no comparison with main)."""
        return f"ready: {count} live files; the derived store is absent\n"

    def procedure_for(self, count):
        """The seven printed lines for the fixture's paths and a live store of `count` files, byte-exact."""
        return (
            f"1. Stop every seat and end every coordinator process: run regime-stop --all in {self.repo} (the stop of "
            "the kit, regime-start --stop --all), confirm with hcom list -v that no seat of this checkout is alive, "
            "and close every session that runs a lever of the kit against it.\n"
            f"2. cp -a {self.live} {self.derived} && chmod -R go-rwx {self.derived}\n"
            f"3. diff -r {self.live} {self.derived} && find {self.derived} -type f | wc -l   # expect no line from "
            f"diff and the count {count}\n"
            f"4. git -C {self.repo} checkout -- {PREFIX}\n"
            f"5. git -C {self.repo} clean -fd -- {PREFIX}\n"
            f"6. git -C {self.repo} pull --ff-only\n"
            "7. regime-store-move prog\n"
        )

    def mask(self, path):
        # The fixture's own uv cache lies under the scratch root, outside HOME: what the lever's run leaves under
        # HOME is then the lever's alone (the HOME test).
        subprocess.run(
            ["uv", "run", "--no-project", "python", "-I", str(MASKER), "--mask-secrets", str(path)],
            env={**self.env, "UV_CACHE_DIR": str(self.root / "fixture-uv-cache")},
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

    def run_line(self, command):
        """One printed line of the procedure, run as written by `sh -c` from the checkout under the fixture's PATH
        (the git wrapper first), the operator's terminal."""
        return subprocess.run(
            ["sh", "-c", command],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )

    def procedure_lines(self, stdout):
        """The seven printed lines with their `<n>. ` prefixes removed, after the verdict line: line 1 is a sentence,
        lines 2 to 6 are commands, line 7 is this lever."""
        lines = stdout.splitlines()
        self.assertEqual(lines[0] + "\n", self.ready)
        self.assertEqual(len(lines), 8, stdout)
        commands = []
        for number, line in enumerate(lines[1:], start=1):
            prefix = f"{number}. "
            self.assertTrue(line.startswith(prefix), line)
            commands.append(line[len(prefix) :])
        return commands

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

    def home_entries(self):
        """Every entry under the fixture's HOME: what a run may not add to (uv's cache, or anything else)."""
        return sorted(str(entry.relative_to(self.home)) for entry in self.home.rglob("*"))

    def assert_nothing_written(self, run, snapshot=None, origin=True):
        """The checkout, the store root and the scratch TMPDIR are as they were before the run (the scratch
        directory removed), and origin, when the test kept one, still holds main alone."""
        self.assertEqual(self.snapshot(), snapshot or self.before, "nothing under the checkout or the root changed")
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")
        if origin:
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
        """The derived store as the procedure's copy line leaves it: the line the lever prints (line 2), run as
        written and nothing more; the fixture adds no chmod of its own (U221e: round 4's fixture did, and hid that
        `cp -a` alone left the store 0755, which the lever's post-move check refuses)."""
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        copy_line = self.procedure_lines(run.stdout)[1]
        self.assertTrue(copy_line.startswith("cp -a "), copy_line)
        done = self.run_line(copy_line)
        self.assertEqual(done.returncode, 0, copy_line + "\n" + done.stdout + done.stderr)
        self.assertTrue(self.derived.is_dir(), "the printed copy line makes the derived store")

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
        """U221d test (a), reshaped by U393: with the derived store absent, the run prints `ready: 6 live files; the
        derived store is absent` and the seven numbered lines of the operator's procedure, byte-exact for the
        fixture's paths, with one stderr line naming the live store, its count and the absent derived store, and
        writes nothing: every entry under the checkout keeps its mode, mtime and size, the store root stays empty, the
        scratch directory goes, and the live store's modes are as they were (no quiescence by mode). The run is
        repeatable: the second prints the same."""
        for attempt in (1, 2):
            with self.subTest(attempt=attempt):
                run = self.run_lever("prog")
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(run.stdout, self.ready + self.procedure)
                self.assertEqual(
                    run.stderr,
                    f"regime-store-move: live store {self.live} (6 files); derived store {self.derived} absent\n",
                )
                self.assertEqual(run.stdout.count("\n"), 8, "one verdict line and seven lines")
                self.assertEqual(run.stdout.count("cp -a"), 1, "the copy is the operator's, once")
                self.assertIn(PLANTED, (self.live / "notes.md").read_text(), "the live file is untouched")
                self.assertFalse(self.derived.exists(), "the lever makes no derived store")
                self.assert_nothing_written(run)

    def test_a_live_store_ahead_of_origin_main_prints_ready_and_the_procedure_without_a_fetch(self):
        """U393 test (a): the live store is ahead of origin/main after every records sync (the coordinator writes its
        verdict row and file, its sweep set and its merge row around the sync's own listing), so a live store with one
        row appended to `ledger.tsv` and one new file `verdicts/x.md`, main unchanged, prints `ready: 7 live files;
        the derived store is absent` and the seven lines byte-exact with the count 7. The git wrapper logs every call
        of the run: each is the checkout's `rev-parse`, none a `fetch`, `init`, `ls-tree`, `cat-file` or
        `hash-object`. The scratch directory, listed by the `rm` stub before its removal, held the producers' outputs
        and the file list, and no `main-listing`, `copy-map`, scratch repository, tools tree, uv cache or masker log.
        Nothing is written and the scratch directory is removed."""
        with (self.live / "ledger.tsv").open("a") as ledger:
            ledger.write("2026-11-08T13:00:00Z\tU1\tmerged\n")
        (self.live / "verdicts").mkdir()
        (self.live / "verdicts/x.md").write_text("verdict\n")
        self.assertEqual(self.git("rev-parse", "origin/main"), self.git("rev-parse", "HEAD"), "main is unchanged")
        self.assertNotEqual(self.git("status", "--porcelain", "--", PREFIX), "", "the live store is ahead of main")
        before = self.snapshot()
        git_log = self.root / "lever-git.log"
        scratch_log = self.root / "scratch-listing.txt"
        self.stub(
            "rm",
            f'for a; do case $a in */regime-store-move.*) ls -A "$a" > {scratch_log} ;; esac; done\n'
            f'exec {self.real("rm")} "$@"',
        )
        run = self.run_lever("prog", FAKE_GIT_LOG=str(git_log))
        self.unstub("rm")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, self.ready_line(7) + self.procedure_for(7))
        self.assertEqual(
            run.stderr, f"regime-store-move: live store {self.live} (7 files); derived store {self.derived} absent\n"
        )
        logged = git_log.read_text().splitlines()
        self.assertTrue(logged, "the wrapper logged the lever's git calls")
        for call in logged:
            self.assertIn("rev-parse", call, f"a git call that is not the checkout's rev-parse: {call}")
            for word in ("fetch", "init", "ls-tree", "cat-file", "hash-object"):
                self.assertNotIn(word, call, f"the lever ran git {word}")
        held = scratch_log.read_text().split()
        self.assertIn("toplevel.out", held, "the rm stub listed the scratch directory before its removal")
        self.assertIn("rels", held, "the live store's file list was written into the scratch directory")
        for name in ("main-listing", "copy-map", "repo.git", "tools", "uv-cache", "differ", "mask.log"):
            self.assertNotIn(name, held, f"the scratch directory held {name}")
        self.assertNotIn("still due", run.stderr)
        self.assertFalse(self.derived.exists(), "the lever makes no derived store")
        self.assert_nothing_written(run, before)

    def test_the_pre_move_run_needs_no_origin(self):
        """U393 test (b): with the fixture's bare origin removed (no fetch source at all; the checkout's remote URL
        still names it) the pre-move run prints the same `ready:` line and the same procedure as with the origin in
        place, exits 0, and writes nothing: the lever reads no origin before the move."""
        shutil.rmtree(self.origin)
        before = self.snapshot()
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, self.ready + self.procedure)
        self.assertEqual(
            run.stderr, f"regime-store-move: live store {self.live} (6 files); derived store {self.derived} absent\n"
        )
        self.assert_nothing_written(run, before, origin=False)

    def test_the_printed_procedure_run_as_written_ends_with_the_lever_reporting_moved(self):
        """U221e test (a) (verdict U221-af547232 P1 `:221`): the printed procedure is the operator's contract, so its
        lines are run as printed: line 1 is a sentence (skipped as text), lines 2 to 6 run by `sh -c` from the
        checkout (the copy with the group and other bits removed, the comparison and the count, the checkout's own
        `checkout --`, `clean -fd --` and `pull --ff-only`), each exit 0, line 3 printing the count alone (no line
        from diff), and line 7, this lever, reports `moved: ...` with exit 0. The derived store is 0700 and every
        entry below it closed to group and others by the printed copy line alone (round 4's `cp -a` kept the
        checkout store's 0755 and the post-move check refused it; the fixture's extra chmod hid that), it holds the
        live bytes (notes.md's token), and the checkout store is clean against HEAD."""
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        lines = self.procedure_lines(run.stdout)
        self.assertTrue(lines[0].startswith("Stop every seat and end every coordinator process"), lines[0])
        self.assertEqual(lines[6], "regime-store-move prog")
        outputs = []
        for command in lines[1:6]:
            done = self.run_line(command)
            self.assertEqual(done.returncode, 0, f"{command}\n{done.stdout}{done.stderr}")
            outputs.append(done.stdout)
        self.assertEqual(outputs[1].split(), ["6"], "line 3: no line from diff, the count 6")
        self.assertEqual(stat.S_IMODE(self.derived.lstat().st_mode), 0o700, "the printed copy line leaves 0700")
        for entry in sorted(self.derived.rglob("*")):
            self.assertEqual(stat.S_IMODE(entry.lstat().st_mode) & 0o077, 0, f"{entry} is open to group or others")
        self.assertEqual(
            sorted(str(entry.relative_to(self.derived)) for entry in self.derived.rglob("*") if entry.is_file()),
            LIVE_FILES,
        )
        self.assertIn(PLANTED, (self.derived / "notes.md").read_text(), "the derived store holds the live bytes")
        self.assertEqual(self.git("status", "--porcelain", "--", PREFIX), "", "lines 4 and 5 finished the step")
        moved = self.run_lever("prog")
        self.assertEqual(moved.returncode, 0, moved.stdout + moved.stderr)
        self.assertEqual(
            moved.stdout, "moved: the derived store holds 6 files; the checkout store is clean against HEAD\n"
        )
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")

    def test_a_derived_store_present_reports_moved_when_the_checkout_store_is_clean_and_refuses_when_it_is_not(self):
        """U221d test (c): with the derived store present (the printed copy line run as written: every live file,
        the directory 0700) the lever judges the operator's step by `git status --porcelain` of the checkout's store
        subtree. The fixture's checkout store is dirty (notes.md modified, `redact-words.txt` untracked): `refused:
        the checkout store is not clean (2 entries); finish the step`, exit 2, no verdict on stdout. After the step
        (main's copies checked out, `redact-words.txt` gone) it prints `moved: the derived store holds 6 files; the
        checkout store is clean against HEAD` and exits 0. Either way nothing is written: the derived store's bytes,
        the checkout and the scratch directory are as before. A `git status` that fails refuses naming it; a derived
        store with no file, with another mode, a link or a file at the program's place refuses by name."""
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
            run.stdout, "moved: the derived store holds 6 files; the checkout store is clean against HEAD\n"
        )
        self.assertIn(
            f"regime-store-move: derived store {self.derived} (6 files); checkout store {self.live} clean", run.stderr
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
        the procedure, no file of the live store is read through the link (its target's text never appears), no
        procedure is printed and nothing is written. U221e test (b) (verdict U221-af547232 P2 `:308`): a name with a
        trailing space (`units.tsv ` beside `units.tsv`), as a file or as a dangling link, and one with a leading
        space, each refuse by name: the listing is read with `IFS= read -r -d ''`, so the
        space reaches the shape check instead of being trimmed off (round 4's `read` passed both as `ready`)."""
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "note.md").write_text("outside the store\n")
        cases = {
            "a link to a file": ("link.md", lambda path: path.symlink_to(outside / "note.md"), "is a symlink"),
            "a link to a directory": ("linked", lambda path: path.symlink_to(outside), "is a symlink"),
            "a dangling link": ("gone.md", lambda path: path.symlink_to(self.root / "nowhere"), "is a symlink"),
            "a fifo": ("pipe", lambda path: os.mkfifo(path), "is not a regular file"),
            "a dot name": (".DS_Store", lambda path: path.write_text("Bud1\n"), "begins with '.'"),
            "a trailing space": (
                "units.tsv ",
                lambda path: path.write_text("id\ttrack\nU1\tseats\n"),
                "begins or ends with a space: 'units.tsv '",
            ),
            "a dangling link with a trailing space": (
                "units.tsv ",
                lambda path: path.symlink_to(self.root / "nowhere"),
                "begins or ends with a space: 'units.tsv '",
            ),
            "a leading space": (" notes.md", lambda path: path.write_text("x\n"), "begins or ends with a space"),
        }
        for label, (name, plant, message) in cases.items():
            with self.subTest(label):
                path = self.live / name
                plant(path)
                try:
                    before = self.snapshot()
                    run = self.run_lever("prog")
                    self.assert_refused(run, message)
                    self.assertIn("the procedure is not printed", run.stderr)
                    self.assertNotIn("outside the store", run.stdout + run.stderr)
                    self.assert_nothing_written(run, before)
                finally:
                    path.unlink(missing_ok=True)
        self.assertEqual(sorted(self.tmp.iterdir()), [], "the scratch directory is removed")

    def test_a_ready_run_leaves_nothing_under_home_and_no_scratch_directory(self):
        """U221e test (c) (verdict U221-af547232 P2 `:478`), reshaped by U393: a `ready` run writes nothing under
        HOME: HOME holds exactly the entries the fixture made (the store root and its parents) afterwards, and the
        scratch directory is gone. (Round 4's masker run left `<HOME>/.cache/uv` behind; U393 removed the masker from
        the lever, so no tool of the run has a cache to leave.)"""
        home_before = self.home_entries()
        self.assertNotIn(".cache", home_before, "the fixture's own masker run wrote nothing under HOME")
        run = self.run_lever("prog")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, self.ready + self.procedure)
        self.assertEqual(self.home_entries(), home_before, "the run added an entry under HOME")
        self.assert_nothing_written(run)

    def test_a_failed_scratch_removal_ends_the_run_with_exit_1_naming_the_directory_after_the_verdict(self):
        """U221e test (e) (verdict U221-af547232 P2 `:184`): the scratch directory holds the producers' outputs and
        the live store's file list, so its removal is a step whose status is read. An `rm` that exits 7 on the scratch directory leaves the verdict
        line and the procedure on stdout as printed, then one line on stderr naming the directory left behind, and
        the run exits 1 (round 4 warned and exited 0). The checkout and the store root are untouched; the fixture
        removes the directory itself."""
        self.failing_stub("rm", "*/regime-store-move.*")
        run = self.run_lever("prog")
        self.unstub("rm")
        left = sorted(self.tmp.iterdir())
        self.assertEqual(len(left), 1, left)
        self.assertTrue(left[0].is_dir() and left[0].name.startswith("regime-store-move."), left)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertEqual(run.stdout, self.ready + self.procedure, "the verdict and the procedure stand")
        self.assertIn(f"regime-store-move: could not remove {left[0]}", run.stderr)
        self.assertTrue(run.stderr.rstrip("\n").endswith(")"), run.stderr)
        self.assertLess(run.stderr.index(f"derived store {self.derived} absent"), run.stderr.index("could not remove"))
        shutil.rmtree(left[0])
        self.assert_nothing_written(run)

    def test_an_absent_store_root_and_each_injected_read_failure_refuse(self):
        """U221d test (d), the producers (standing order 21), reshaped by U393 (no fetch, no masker and no comparison
        remain to inject): a store root that does not exist refuses naming it (hcom-seat makes it); a read that fails
        or warns (the live store's walk by `find`, the counts by `tr` and `wc`, the checkout's toplevel by `git
        rev-parse`, the read-back of a scratch file by `cat`) refuses with exit 2 naming the producer. Each prints no
        procedure and writes nothing, and the run without the injection prints the procedure again. U221e tests (d)
        and (f) (verdict U221-af547232 P2 `:203` and tests `:396`): a `wc` or a `tr` that prints a valid count and a
        warning on stderr is a failed read (round 4 read the status alone), and `tr` and `git rev-parse` each carry an
        injection, failing and warning; a `stat` planted on PATH changes nothing, since the mode read is
        `/usr/bin/stat`'s (the kit's form, so a coreutils `stat` first on PATH never steers it)."""
        live = "*/.orchestration/orchestrate/*"
        tools = ("find", "cat", "wc", "tr", "stat")
        cases = (
            ("the source walk fails", lambda: self.failing_stub("find", live), {}, 2, ("find", "walk of")),
            ("the source walk warns", lambda: self.warning_stub("find", live), {}, 2, ("find", "walk of")),
            (
                "the checkout's toplevel fails",
                lambda: None,
                {"FAKE_GIT_FAIL": "rev-parse"},
                2,
                ("git rev-parse", "not in a git checkout"),
            ),
            (
                "the checkout's toplevel warns",
                lambda: None,
                {"FAKE_GIT_WARN": "rev-parse"},
                2,
                ("git rev-parse", "wrote to its stderr"),
            ),
            (
                "the count of the live store fails (wc)",
                lambda: self.failing_stub("wc", "-c"),
                {},
                2,
                ("cannot count the live store", "wc -c exited 7"),
            ),
            (
                "the count of the live store warns (wc)",
                lambda: self.warning_stub("wc", "-c"),
                {},
                2,
                ("cannot count the live store", "wc -c exited 0 and wrote to its stderr"),
            ),
            (
                "the count of the live store fails (tr)",
                lambda: self.failing_stub("tr", "-cd"),
                {},
                2,
                ("cannot count the live store", "tr -cd exited 7"),
            ),
            (
                "the count of the live store warns (tr)",
                lambda: self.warning_stub("tr", "-cd"),
                {},
                2,
                ("cannot count the live store", "tr -cd exited 0 and wrote to its stderr"),
            ),
            (
                "the read-back of a scratch file",
                lambda: self.failing_stub("cat", "*/toplevel.out"),
                {},
                2,
                ("read_file: cannot read", "toplevel.out (cat exited 7)", "not in a git checkout"),
            ),
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
        with self.subTest("a stat planted on PATH is never run"):
            self.failing_stub("stat", "*")
            run = self.run_lever("prog")
            self.unstub("stat")
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            self.assertEqual(run.stdout, self.ready + self.procedure)
            self.assert_nothing_written(run)
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
