"""Exercise scripts/orchestrator/acp-record-place.py (regime-cutover U343h) on a scratch broker directory: the record
placed whole and replaced whole, every entry a process that writes the directory can plant (a link, a file, a directory
at `<id>.tmp` and at `<id>`), a directory whose identity is not the one the listener read, a linked or irregular
`<broker-dir>`, an id outside its grammar, a directory open to others, the record's bounds, and each producer's failure
injected through the module's own `os` name, every refusal naming its step. The module is loaded from the file and run
in-process (`main(argv, stdin)`), the form of tests/unit/test_profile_config_place.py; one test runs the file itself
under `python3 -I -S` and holds the installed copy and the manifest pin to it.
"""

import ast
import contextlib
import errno
import hashlib
import importlib.util
import io
import os
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/orchestrator/acp-record-place.py"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_acp-record-place.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
README = ROOT / "scripts/orchestrator/README.md"
RECORD_ID = "acp-w1-20261110-120000-4242"
RUNNING = b"ref=refs/acp-seat/w1/20261110-120000-4242\nreaper=4243\n"
FINAL = RUNNING + b"status=0 push=refs/acp-seat/w1/20261110-120000-4242\n"
VICTIM = b"[default]\naws_access_key_id = AKIAEXAMPLE\n# the protected host file a planted link points at\n"
SHEBANG = "#!/usr/bin/env -S python3 -I"
GRAMMAR = "^acp-[a-z0-9][a-z0-9_-]{0,63}-[0-9]{8}-[0-9]{6}-[0-9]+$"


def load_helper(path=HELPER):
    spec = importlib.util.spec_from_file_location("acp_record_place", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def identity_of(path):
    info = os.stat(path)
    return f"{info.st_dev}:{info.st_ino}"


class AcpRecordPlaceTest(unittest.TestCase):
    def setUp(self):
        self.module = load_helper()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.broker = self.root / "broker"
        self.broker.mkdir(mode=0o700)
        self.identity = identity_of(self.broker)
        self.record = self.broker / RECORD_ID
        self.temporary = self.broker / f"{RECORD_ID}.tmp"
        self.elsewhere = self.root / "elsewhere"
        self.elsewhere.mkdir(mode=0o700)
        self.victim = self.elsewhere / "credentials"
        self.victim.write_bytes(VICTIM)
        self.addCleanup(self.unlock)

    def unlock(self):
        for path in (self.broker, self.elsewhere):
            if path.is_dir() and not path.is_symlink():
                path.chmod(0o700)

    def run_helper(self, *args, stdin=FINAL, broker=None, identity=None, record_id=RECORD_ID):
        argv = [*args, str(self.broker if broker is None else broker), self.identity if identity is None else identity,
                record_id]  # fmt: skip
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = self.module.main(argv, io.BytesIO(stdin))
        return status, out.getvalue(), err.getvalue()

    def assert_refused(self, result, step, *fragments):
        status, out, err = result
        self.assertEqual((status, out), (2, ""), err)
        self.assertEqual(err.count("\n"), 1, err)
        self.assertTrue(err.startswith(f"acp-record-place: refused at {step}: "), err)
        for fragment in fragments:
            self.assertIn(fragment, err)

    def assert_failed(self, result, step, *fragments):
        status, out, err = result
        self.assertEqual((status, out), (1, ""), err)
        self.assertEqual(err.count("\n"), 1, err)
        self.assertTrue(err.startswith(f"acp-record-place: failed at {step}: "), err)
        for fragment in fragments:
            self.assertIn(fragment, err)

    def entries(self):
        return sorted(p.name for p in self.broker.iterdir())

    def elsewhere_entries(self):
        return sorted(p.name for p in self.elsewhere.iterdir())

    def assert_victim_untouched(self, before):
        after = self.victim.stat()
        self.assertEqual(self.victim.read_bytes(), VICTIM)
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))

    def assert_placed(self, data):
        self.assertTrue(self.record.is_file() and not self.record.is_symlink(), "the record is a regular file")
        self.assertEqual(self.record.read_bytes(), data)
        self.assertEqual(stat.S_IMODE(self.record.stat().st_mode), 0o600)
        self.assertEqual(self.entries(), [RECORD_ID], "no temporary remains")

    def test_the_record_is_placed_whole_0600_and_replaced_whole_through_the_temporary(self):
        """The running form, then the final form over it; at the temporary's `fsync` the name still holds the earlier
        bytes whole and the new bytes sit in `<id>.tmp` alone, so a reader sees one form or the other."""
        self.assertEqual(self.run_helper(stdin=RUNNING), (0, "", ""))
        self.assert_placed(RUNNING)
        real_fsync = os.fsync
        seen = []

        def look_then_fsync(fd):
            real_fsync(fd)
            if stat.S_ISREG(os.fstat(fd).st_mode):
                seen.append((self.record.read_bytes(), self.temporary.read_bytes(), self.entries()))

        with mock.patch.object(self.module.os, "fsync", look_then_fsync):
            self.assertEqual(self.run_helper(stdin=FINAL), (0, "", ""))
        self.assertEqual(seen, [(RUNNING, FINAL, [RECORD_ID, f"{RECORD_ID}.tmp"])])
        self.assert_placed(FINAL)

    def test_a_link_planted_at_the_temporary_name_is_removed_and_its_target_keeps_its_bytes(self):
        """The round-5 P1 (verdict U343g-8a049561, acp-broker:1262): a link the Router plants at `<id>.tmp` made the
        reaper's `printf >` overwrite the file it points at. The helper unlinks the entry relative to the held
        descriptor and creates the temporary exclusively with `O_NOFOLLOW`: a link to a host file, a dangling link,
        a link to a directory, a regular file and a FIFO at the name are each removed, the record lands, the target
        keeps its bytes and nothing lands beside it."""
        before = self.victim.stat()
        cases = (
            ("a link to a host file", lambda: self.temporary.symlink_to(self.victim)),
            ("a dangling link", lambda: self.temporary.symlink_to(self.elsewhere / "missing")),
            ("a link to a directory", lambda: self.temporary.symlink_to(self.elsewhere)),
            ("a regular file", lambda: self.temporary.write_bytes(b"planted\n")),
            ("a FIFO", lambda: os.mkfifo(self.temporary)),
        )
        for label, plant in cases:
            with self.subTest(case=label):
                plant()
                self.assertEqual(self.run_helper(stdin=FINAL), (0, "", ""))
                self.assert_placed(FINAL)
                self.assert_victim_untouched(before)
                self.assertEqual(self.elsewhere_entries(), ["credentials"], "nothing landed beside the target")
                self.record.unlink()
        with self.subTest(case="a directory at the temporary name"):
            self.temporary.mkdir()
            result = self.run_helper(stdin=FINAL)
            self.assert_refused(result, "unlink-temporary", f"{self.temporary}: cannot remove the entry")
            self.assertEqual(self.entries(), [f"{RECORD_ID}.tmp"], "nothing written")
            self.temporary.rmdir()

    def test_a_link_planted_at_the_record_name_is_replaced_as_an_entry_and_its_target_untouched(self):
        """The record's final `rename`: a link at `<id>` (to a host file, or to a directory, where `mv -f` would have
        moved the temporary into that directory) is replaced as an entry, never followed; a directory standing at
        `<id>` fails the rename with the temporary removed and nothing moved into it."""
        before = self.victim.stat()
        for label, target in (("a link to a host file", self.victim), ("a link to a directory", self.elsewhere)):
            with self.subTest(case=label):
                self.record.symlink_to(target)
                self.assertEqual(self.run_helper(stdin=FINAL), (0, "", ""))
                self.assert_placed(FINAL)
                self.assert_victim_untouched(before)
                self.assertEqual(self.elsewhere_entries(), ["credentials"], "nothing moved into the directory")
                self.record.unlink()
        with self.subTest(case="a directory at the record's name"):
            self.record.mkdir()
            result = self.run_helper(stdin=FINAL)
            self.assert_failed(result, "rename", f"{self.record}: a directory stands at the record's name")
            self.assertTrue(self.record.is_dir())
            self.assertEqual(sorted(p.name for p in self.record.iterdir()), [], "nothing moved into the directory")
            self.assertEqual(self.entries(), [RECORD_ID], "the temporary is removed")

    def test_a_directory_whose_identity_is_not_the_listeners_is_refused_and_nothing_is_written_anywhere(self):
        """The listener read the broker directory's device and inode once; a directory replaced by another at the
        name (or an argument naming another directory) is refused at `fstat-dir` with exit 2 and no entry made."""
        other = identity_of(self.elsewhere)
        result = self.run_helper(identity=other)
        self.assert_refused(result, "fstat-dir", f"{self.broker}: is {self.identity}, not the broker directory", other)
        self.assertEqual(self.entries(), [])
        moved = self.root / "moved"
        self.broker.rename(moved)
        self.broker.mkdir(mode=0o700)
        result = self.run_helper()
        self.assert_refused(result, "fstat-dir", "not the broker directory the listener made")
        self.assertEqual(self.entries(), [])
        self.assertEqual(sorted(p.name for p in moved.iterdir()), [])
        self.assertEqual(self.elsewhere_entries(), ["credentials"])
        for shape in ("1", "1:2:3", "a:b", ":", "1:", "-1:2", "1:2\n"):
            with self.subTest(identity=shape):
                status, out, err = self.run_helper(identity=shape)
                self.assertEqual((status, out, err), (1, "", f"{self.module.USAGE}\n"))
        self.assertEqual(self.entries(), [])

    def test_a_broker_dir_that_is_a_link_a_file_or_absent_is_refused_before_anything_is_opened_inside(self):
        link = self.root / "broker-link"
        link.symlink_to(self.elsewhere)
        result = self.run_helper(broker=link, identity=identity_of(self.elsewhere))
        self.assert_refused(result, "open-dir", f"{link}: is a symbolic link or not a directory")
        self.assertEqual(self.elsewhere_entries(), ["credentials"])
        plain = self.root / "broker-file"
        plain.write_bytes(b"")
        self.assert_refused(self.run_helper(broker=plain), "open-dir", "is a symbolic link or not a directory")
        self.assert_refused(self.run_helper(broker=self.root / "absent"), "open-dir", "(ENOENT)")
        self.assertEqual(self.entries(), [])

    def test_an_id_outside_the_grammar_or_holding_a_slash_is_refused_and_no_name_reaches_os(self):
        """`<id>` must match the slot grammar, so no `/`, no `..`, no upper case, no newline and no empty name is ever
        passed to an `os` call; a name of 64 characters (the grammar's longest) is accepted."""
        ids = ("w1", "acp-W1-20261110-120000-1", "acp-w1-2026-1", "acp-w1-20261110-120000-", "../x",
               "acp-w1-20261110-120000-1/x", "/acp-w1-20261110-120000-1", "acp-w1-20261110-120000-1\n",
               "acp-" + "a" * 65 + "-20261110-120000-1", "", "acp-w1-20261110-120000-1.tmp", "-acp-w1-20261110-120000-1",
               "acp--20261110-120000-1")  # fmt: skip
        real_open = os.open
        opened = []

        def recording_open(path, flags, mode=0o777, *, dir_fd=None):
            opened.append(path)
            return real_open(path, flags, mode, dir_fd=dir_fd)

        for record_id in ids:
            with self.subTest(record_id=record_id):
                with mock.patch.object(self.module.os, "open", recording_open):
                    result = self.run_helper(record_id=record_id)
                self.assert_refused(result, "id", f"{record_id!r}: is outside {GRAMMAR}")
        self.assertEqual(opened, [], "nothing was opened")
        self.assertEqual(self.entries(), [])
        longest = "acp-" + "a" * 64 + "-20261110-120000-1"
        self.assertEqual(self.run_helper(record_id=longest), (0, "", ""))
        self.assertEqual(self.entries(), [longest])

    def test_a_directory_of_another_uid_or_writable_by_group_or_others_is_refused(self):
        uid = os.getuid()
        with mock.patch.object(self.module.os, "getuid", return_value=uid + 1):
            result = self.run_helper()
        self.assert_refused(result, "fstat-dir", f"{self.broker}: is owned by uid {uid}, not {uid + 1}")
        for mode in (0o770, 0o702, 0o777):
            with self.subTest(mode=oct(mode)):
                self.broker.chmod(mode)
                self.assert_refused(self.run_helper(), "fstat-dir", "is writable by its group or by others")
        self.assertEqual(self.entries(), [])
        self.broker.chmod(0o750)
        self.assertEqual(self.run_helper(), (0, "", ""))
        self.assert_placed(FINAL)

    @unittest.skipUnless(os.geteuid() == 0, "chown to another uid needs root")
    def test_another_uids_directory_refuses_under_root(self):
        os.chown(self.broker, os.getuid() + 1, -1)
        self.assert_refused(self.run_helper(), "fstat-dir", f"is owned by uid {os.getuid() + 1}, not {os.getuid()}")
        self.assertEqual(self.entries(), [])

    def test_the_record_is_at_most_4096_bytes_and_newline_terminated(self):
        """The record's three lines are small; a stdin over 4096 bytes, an empty one or one without its final newline is
        refused at `record` before the directory is opened, and nothing is written."""
        longest = b"x" * 4095 + b"\n"
        self.assertEqual(self.run_helper(stdin=longest), (0, "", ""))
        self.assert_placed(longest)
        self.record.unlink()
        for label, data, reason in (
            ("over the bound", b"x" * 4096 + b"\n", "exceeds 4096 bytes"),
            ("empty", b"", "is empty"),
            ("no final newline", RUNNING + b"status=0 push=none", "does not end with a newline"),
        ):
            with self.subTest(case=label):
                self.assert_refused(
                    self.run_helper(stdin=data), "record", f"{self.record}: the record on stdin {reason}"
                )
                self.assertEqual(self.entries(), [])

    def test_each_producers_failure_names_its_step_and_leaves_no_temporary(self):
        """Before the create, a failing `os` call is a refusal (exit 2) and nothing is made; after it, a failure is
        exit 1 with the temporary unlinked through the held descriptor (its own failure named in the line) and the
        record at the name untouched; a `fsync` of the directory that fails after the rename is exit 1 with the record
        in place."""
        real = {name: getattr(os, name) for name in ("open", "fstat", "write", "fsync", "rename", "unlink")}

        def failing_dir_open(path, flags, mode=0o777, *, dir_fd=None):
            if path == str(self.broker):  # lint-comparisons: allow the name os.open received, no path identity
                raise OSError(errno.EIO, "Input/output error")
            return real["open"](path, flags, mode, dir_fd=dir_fd)

        def failing_create(path, flags, mode=0o777, *, dir_fd=None):
            if path.endswith(".tmp"):  # lint-comparisons: allow the name os.open received, no path identity
                raise OSError(errno.EROFS, "Read-only file system")
            return real["open"](path, flags, mode, dir_fd=dir_fd)

        def fstat_failing_for(kind):
            def failing(fd):
                info = real["fstat"](fd)
                if kind == "dir" and stat.S_ISDIR(info.st_mode):
                    raise OSError(errno.EIO, "Input/output error")
                if kind == "temporary" and stat.S_ISREG(info.st_mode):
                    raise OSError(errno.EIO, "Input/output error")
                return info

            return failing

        def fsync_failing_for_directories(fd):
            if stat.S_ISDIR(real["fstat"](fd).st_mode):
                raise OSError(errno.EIO, "Input/output error")
            return real["fsync"](fd)

        def raising(code, text):
            def fail(*args, **kwargs):
                raise OSError(code, text)

            return fail

        refusals = (
            ("open", failing_dir_open, "open-dir", f"{self.broker}: cannot open it: Input/output error (EIO)"),
            ("fstat", fstat_failing_for("dir"), "fstat-dir", f"{self.broker}: cannot read its identity:", "(EIO)"),
            ("unlink", raising(errno.EPERM, "Operation not permitted"), "unlink-temporary", f"{self.temporary}: cannot remove the entry at the temporary name:", "(EPERM)"),
            ("open", failing_create, "create-temporary", f"{self.temporary}: cannot create it:", "(EROFS)"),
        )  # fmt: skip
        for name, stand_in, step, *fragments in refusals:
            with self.subTest(step=step):
                self.record.write_bytes(RUNNING)
                with mock.patch.object(self.module.os, name, stand_in):
                    result = self.run_helper()
                self.assert_refused(result, step, *fragments)
                self.assertEqual(self.entries(), [RECORD_ID], "nothing made")
                self.assertEqual(self.record.read_bytes(), RUNNING, "a refused run replaces nothing")
        failures = (
            ("fstat", fstat_failing_for("temporary"), "fstat-temporary", f"{self.temporary}: cannot read its identity:", "(EIO)"),
            ("write", raising(errno.ENOSPC, "No space left on device"), "write-temporary", f"{self.temporary}: cannot write it:", "(ENOSPC)"),
            ("fsync", raising(errno.EIO, "Input/output error"), "fsync-temporary", f"{self.temporary}: cannot flush it:", "(EIO)"),
            ("rename", raising(errno.EXDEV, "Cross-device link"), "rename", f"{self.record}: cannot install it:", "(EXDEV)"),
        )  # fmt: skip
        for name, stand_in, step, *fragments in failures:
            with self.subTest(step=step):
                self.record.write_bytes(RUNNING)
                with mock.patch.object(self.module.os, name, stand_in):
                    result = self.run_helper()
                self.assert_failed(result, step, *fragments)
                self.assertNotIn("remains", result[2])
                self.assertEqual(self.entries(), [RECORD_ID], "no temporary remains")
                self.assertEqual(self.record.read_bytes(), RUNNING, "a failed run replaces nothing")
        with self.subTest(step="unlink-temporary after a failure"):
            self.record.write_bytes(RUNNING)
            real_unlink = os.unlink

            def unlink_failing_after_the_create(path, *, dir_fd=None):
                if self.temporary.exists():
                    raise OSError(errno.EPERM, "Operation not permitted")
                return real_unlink(path, dir_fd=dir_fd)

            with (
                mock.patch.object(self.module.os, "rename", raising(errno.EXDEV, "Cross-device link")),
                mock.patch.object(self.module.os, "unlink", unlink_failing_after_the_create),
            ):
                result = self.run_helper()
            self.assert_failed(
                result, "rename", "(EXDEV)", f"; the temporary {self.temporary} remains (unlink:", "(EPERM)"
            )
            self.assertEqual(
                self.entries(), [RECORD_ID, f"{RECORD_ID}.tmp"], "the temporary the unlink could not remove stands"
            )
            self.assertEqual(self.record.read_bytes(), RUNNING)
            self.temporary.unlink()
        with self.subTest(step="fsync-directory"):
            self.record.write_bytes(RUNNING)
            with mock.patch.object(self.module.os, "fsync", fsync_failing_for_directories):
                result = self.run_helper()
            self.assert_failed(result, "fsync-directory", f"{self.broker}: cannot flush the directory:", "(EIO)")
            self.assertNotIn("remains", result[2])
            self.assertEqual(self.entries(), [RECORD_ID])
            self.assertEqual(self.record.read_bytes(), FINAL, "the rename had landed")

    def test_usage_errors_exit_1_with_the_usage_line(self):
        for argv in ([], [str(self.broker)], [str(self.broker), self.identity], ["broker", self.identity, RECORD_ID],
                     ["--x", str(self.broker), self.identity, RECORD_ID], [str(self.broker), self.identity, RECORD_ID, "x"]):  # fmt: skip
            with self.subTest(argv=argv):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    status = self.module.main(argv, io.BytesIO(FINAL))
                self.assertEqual((status, out.getvalue()), (1, ""))
                self.assertEqual(err.getvalue(), f"{self.module.USAGE}\n")
        self.assertEqual(self.entries(), [], "a usage error writes nothing")

    def test_the_file_runs_isolated_on_the_standard_library_alone_and_is_shipped_pinned(self):
        run = subprocess.run(
            [sys.executable, "-I", "-S", str(HELPER), str(self.broker), self.identity, RECORD_ID],
            input=FINAL, capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, b"", b""))
        self.assert_placed(FINAL)
        run = subprocess.run(
            [sys.executable, "-I", "-S", str(HELPER), str(self.broker), identity_of(self.elsewhere), RECORD_ID],
            input=FINAL, capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout), (2, b""))
        self.assertIn(b"acp-record-place: refused at fstat-dir: ", run.stderr)
        text = HELPER.read_text()
        tree = ast.parse(text)
        imported = sorted(alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names)
        self.assertEqual(imported, ["errno", "os", "re", "stat", "sys"])
        self.assertEqual([node for node in tree.body if isinstance(node, ast.ImportFrom)], [])
        self.assertNotIn("environ", text.replace(ast.get_docstring(tree) or "", ""))
        self.assertNotIn("getenv", text)
        self.assertEqual(text.splitlines()[0], SHEBANG)
        self.assertTrue(os.access(HELPER, os.X_OK))
        self.assertEqual(INSTALLED.read_bytes(), HELPER.read_bytes(), "the installed copy is byte-identical")
        pins = re.findall(r"^      acp-record-place\.py: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)
        self.assertEqual(pins, [hashlib.sha256(HELPER.read_bytes()).hexdigest()])

    def test_the_readme_paragraph_names_the_helper_and_its_mechanism(self):
        """scripts/orchestrator/README.md describes the record's write as it is: the pinned helper beside the broker,
        the listener's one read of the directory's identity, one held descriptor, `dir_fd`, the exclusive create, the
        rename, this test file; a description that promises round 5's `printf` and `mv -f` fails here."""
        readme = README.read_text()
        paragraph = next(p for p in readme.split("\n\n") if p.startswith("The exit record's write"))
        for phrase in ("acp-record-place.py", "held directory descriptor", "`dir_fd`", "`O_NOFOLLOW`", "`O_EXCL`",
                       "device and inode", "rename", "claude.levers.sha256", "tests/unit/test_acp_record_place.py",
                       "U310d", "verdict U343g-8a049561"):  # fmt: skip
            self.assertIn(phrase, paragraph, phrase)
        for stale in ("`printf` to `<id>.tmp`", "then `mv -f`"):
            self.assertNotIn(stale, readme, stale)


if __name__ == "__main__":
    unittest.main()
