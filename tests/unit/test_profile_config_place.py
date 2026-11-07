"""Exercise scripts/orchestrator/profile-config-place.py (regime-cutover U310d) on a scratch `agent/` directory: the
placement, the compare, the dry run, every entry a process owning the directory can plant (a link, a directory, a FIFO,
a regular file, at `config.yml`, at the temporary's name and at `agent` itself), the read-back after the rename, and
each producer's failure injected through the module's own `os` and `secrets` names, every refusal naming its step.
The module is loaded from the file and run in-process (`main(argv, stdin)`); one test runs the file itself under
`python3 -I -S` and holds the installed copy and the manifest pin to it.
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
import threading
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "scripts/orchestrator/profile-config-place.py"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_profile-config-place.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
RENDERED = b"modelRoles:\n  default: claude-bridge/claude-opus-5-5\nextensions:\n  - /x/pi-claude-bridge\n"
STALE = b"modelRoles:\n  default: stale/model\n"
SHEBANG = "#!/usr/bin/env -S python3 -I"
VICTIM = b"modelRoles:\n  default: operator/default\n# the host file a planted link points at\n"
FIXED_NAME = ".config.yml." + "0" * 16


def load_helper(path=HELPER):
    spec = importlib.util.spec_from_file_location("profile_config_place", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProfileConfigPlaceTest(unittest.TestCase):
    # The helper under test; a driver may point it at an earlier head's file, where the round-5 replacement probe must
    # fail (U310e ACCEPTANCE 3, the `earlier_lever` form of tests/unit/test_hcom_seat_dsh.py).
    helper = HELPER

    def setUp(self):
        self.module = load_helper(self.helper)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.agent = self.root / "agent"
        self.agent.mkdir(mode=0o700)
        self.config = self.agent / "config.yml"
        self.elsewhere = self.root / "elsewhere"
        self.elsewhere.mkdir()
        self.victim = self.elsewhere / "config.yml"
        self.victim.write_bytes(VICTIM)
        self.uid = os.getuid()
        self.addCleanup(self.unlock)

    def unlock(self):
        for path in (self.agent, self.elsewhere):
            if path.is_dir() and not path.is_symlink():
                path.chmod(0o700)

    def run_helper(self, *args, stdin=RENDERED, agent=None, uid=None):
        argv = [*args, str(self.agent if agent is None else agent), str(self.uid if uid is None else uid)]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = self.module.main(argv, io.BytesIO(stdin))
        return status, out.getvalue(), err.getvalue()

    def run_helper_bounded(self, *args, **kwargs):
        """The run in a thread with a deadline, so a planted FIFO that blocked an open fails the test instead of
        hanging it."""
        results = []
        thread = threading.Thread(target=lambda: results.append(self.run_helper(*args, **kwargs)), daemon=True)
        thread.start()
        thread.join(15)
        if thread.is_alive():
            self.fail("the helper blocked instead of refusing")
        return results[0]

    def assert_refused(self, result, step, *fragments):
        status, out, err = result
        self.assertEqual((status, out), (2, ""), err)
        self.assertEqual(err.count("\n"), 1, err)
        self.assertTrue(err.startswith(f"profile-config-place: refused at {step}: "), err)
        for fragment in fragments:
            self.assertIn(fragment, err)

    def entries(self):
        return sorted(p.name for p in self.agent.iterdir())

    def assert_victim_untouched(self, before):
        after = self.victim.stat()
        self.assertEqual(self.victim.read_bytes(), VICTIM)
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))

    def test_an_absent_config_is_placed_0600_an_equal_one_kept_and_a_different_one_replaced(self):
        self.assertEqual(self.run_helper(), (0, "placed\n", ""))
        self.assertTrue(self.config.is_file() and not self.config.is_symlink())
        self.assertEqual(self.config.read_bytes(), RENDERED)
        self.assertEqual(stat.S_IMODE(self.config.stat().st_mode), 0o600)
        self.assertEqual(self.entries(), ["config.yml"], "no temporary remains")
        before = self.config.stat()
        self.assertEqual(self.run_helper(), (0, "kept\n", ""))
        after = self.config.stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns), "nothing written")
        self.config.write_bytes(STALE)
        self.assertEqual(self.run_helper(), (0, "replaced\n", ""))
        self.assertEqual(self.config.read_bytes(), RENDERED)
        self.assertEqual(stat.S_IMODE(self.config.stat().st_mode), 0o600)
        self.assertEqual(self.entries(), ["config.yml"])

    def test_a_dry_run_reports_absent_differs_or_kept_and_writes_nothing(self):
        self.assertEqual(self.run_helper("--dry-run"), (0, "absent\n", ""))
        self.assertEqual(self.entries(), [])
        self.config.write_bytes(STALE)
        before = self.config.stat()
        self.assertEqual(self.run_helper("--dry-run"), (0, "differs\n", ""))
        self.assertEqual(self.config.read_bytes(), STALE)
        self.config.write_bytes(RENDERED)
        before = self.config.stat()
        self.assertEqual(self.run_helper("--dry-run"), (0, "kept\n", ""))
        after = self.config.stat()
        self.assertEqual((before.st_ino, before.st_mtime_ns), (after.st_ino, after.st_mtime_ns))
        self.assertEqual(self.entries(), ["config.yml"])
        self.agent.chmod(0o500)
        self.assertEqual(self.run_helper("--dry-run", stdin=STALE), (0, "differs\n", ""), "a dry run needs no write")

    def test_a_link_at_config_refuses_naming_it_and_its_target_keeps_its_bytes(self):
        self.config.symlink_to(self.victim)
        before = self.victim.stat()
        for args in ((), ("--dry-run",)):
            with self.subTest(args=args):
                result = self.run_helper(*args)
                self.assert_refused(result, "open-config", f"{self.config}: is a symbolic link; the dsh role writes")
                self.assert_victim_untouched(before)
                self.assertTrue(self.config.is_symlink())
                self.assertEqual(self.entries(), ["config.yml"])
        self.config.unlink()
        self.config.symlink_to(self.elsewhere / "missing")
        self.assert_refused(self.run_helper(), "open-config", "is a symbolic link")
        self.assertEqual(sorted(p.name for p in self.elsewhere.iterdir()), ["config.yml"], "no dangling link followed")

    def test_a_link_planted_at_config_after_the_compare_is_replaced_as_an_entry_and_its_target_untouched(self):
        """The rename's own semantics: a link at the destination is replaced as an entry, never followed."""
        before = self.victim.stat()
        real_fsync = os.fsync

        def plant_then_fsync(fd):
            real_fsync(fd)
            self.config.symlink_to(self.victim)

        with mock.patch.object(self.module.os, "fsync", plant_then_fsync):
            result = self.run_helper()
        self.assertEqual(result, (0, "placed\n", ""))
        self.assertTrue(self.config.is_file() and not self.config.is_symlink())
        self.assertEqual(self.config.read_bytes(), RENDERED)
        self.assert_victim_untouched(before)
        self.assertEqual(self.entries(), ["config.yml"])

    def test_a_directory_at_config_refuses_before_and_after_the_compare(self):
        self.config.mkdir()
        self.assert_refused(self.run_helper(), "fstat-config", f"{self.config}: is not a regular file")
        self.assert_refused(self.run_helper("--dry-run"), "fstat-config", "is not a regular file")
        self.config.rmdir()
        real_fsync = os.fsync

        def plant_then_fsync(fd):
            real_fsync(fd)
            self.config.mkdir()

        with mock.patch.object(self.module.os, "fsync", plant_then_fsync):
            result = self.run_helper()
        self.assert_refused(result, "rename", f"{self.config}: a directory stands at the destination")
        self.assertTrue(self.config.is_dir())
        self.assertEqual(sorted(p.name for p in self.config.iterdir()), [], "nothing moved into the directory")
        self.assertEqual(self.entries(), ["config.yml"], "the temporary is removed")

    def test_every_entry_planted_at_the_temporary_name_refuses_with_eexist_without_blocking(self):
        """With `secrets.token_hex` fixed, the name is known: a FIFO, a regular file, a dangling link, a link to a host
        file and a directory planted there each refuse at the exclusive create; nothing is opened, so a FIFO never
        blocks and the link's target keeps its bytes."""
        planted = self.agent / FIXED_NAME
        before = self.victim.stat()
        cases = (
            ("a FIFO", lambda: os.mkfifo(planted), stat.S_ISFIFO),
            ("a regular file", lambda: planted.write_bytes(b"planted\n"), stat.S_ISREG),
            ("a dangling link", lambda: planted.symlink_to(self.elsewhere / "missing"), stat.S_ISLNK),
            ("a link to a host file", lambda: planted.symlink_to(self.victim), stat.S_ISLNK),
            ("a link to a FIFO", lambda: planted.symlink_to(self.elsewhere / "fifo"), stat.S_ISLNK),
            ("a directory", planted.mkdir, stat.S_ISDIR),
        )
        os.mkfifo(self.elsewhere / "fifo")
        for label, plant, kind in cases:
            with self.subTest(case=label):
                if planted.is_dir() and not planted.is_symlink():
                    planted.rmdir()
                elif planted.exists() or planted.is_symlink():
                    planted.unlink()
                plant()
                with mock.patch.object(self.module.secrets, "token_hex", return_value="0" * 16):
                    result = self.run_helper_bounded()
                self.assert_refused(
                    result, "create-temporary", f"{planted}: an entry already stands at the temporary name; nothing"
                )
                self.assertTrue(kind(os.lstat(planted).st_mode), "the planted entry stands as planted")
                self.assertEqual(self.entries(), [FIXED_NAME])
                self.assert_victim_untouched(before)
        self.assertEqual(sorted(p.name for p in self.elsewhere.iterdir()), ["config.yml", "fifo"])

    def test_a_fifo_at_a_guessable_name_is_never_the_temporary_and_the_config_lands_beside_it(self):
        """Without the seed the name is unknown: FIFOs and links at every guessable name stand while the config lands."""
        names = [".config.yml.tmp", FIXED_NAME, f"config.yml.tmp.{os.getpid()}", ".config.yml.XXXXXX"]
        for name in names[:2]:
            os.mkfifo(self.agent / name)
        for name in names[2:]:
            (self.agent / name).symlink_to(self.victim)
        before = self.victim.stat()
        self.assertEqual(self.run_helper_bounded(), (0, "placed\n", ""))
        self.assertEqual(self.config.read_bytes(), RENDERED)
        self.assertEqual(self.entries(), sorted([*names, "config.yml"]))
        for name in names[:2]:
            self.assertTrue(stat.S_ISFIFO(os.lstat(self.agent / name).st_mode))
        self.assert_victim_untouched(before)

    def test_a_link_or_a_file_at_agent_refuses_and_nothing_reaches_the_target(self):
        link = self.root / "agent-link"
        link.symlink_to(self.elsewhere)
        result = self.run_helper(agent=link)
        self.assert_refused(result, "open-agent", f"{link}: is a symbolic link or not a directory; the dsh role writes")
        self.assertEqual(sorted(p.name for p in self.elsewhere.iterdir()), ["config.yml"])
        plain = self.root / "agent-file"
        plain.write_bytes(b"")
        self.assert_refused(self.run_helper(agent=plain), "open-agent", "is a symbolic link or not a directory")
        self.assert_refused(self.run_helper(agent=self.root / "absent"), "open-agent", "(ENOENT)")

    def test_a_directory_of_another_uid_or_open_to_others_refuses(self):
        self.assert_refused(self.run_helper(uid=self.uid + 1), "fstat-agent", f"is owned by uid {self.uid}, not")
        for mode in (0o770, 0o702, 0o777):
            with self.subTest(mode=oct(mode)):
                self.agent.chmod(mode)
                self.assert_refused(self.run_helper(), "fstat-agent", "is writable by its group or by others")
        self.agent.chmod(0o750)
        self.assertEqual(self.run_helper(), (0, "placed\n", ""))
        self.assertEqual(self.entries(), ["config.yml"])

    @unittest.skipUnless(os.geteuid() == 0, "chown to another uid needs root")
    def test_another_uids_directory_refuses_under_root(self):
        os.chown(self.agent, self.uid + 1, -1)
        self.assert_refused(self.run_helper(), "fstat-agent", f"is owned by uid {self.uid + 1}, not {self.uid}")
        self.assertEqual(self.entries(), [])

    def test_a_config_of_another_uid_or_an_unreadable_one_refuses(self):
        self.config.write_bytes(STALE)
        real_fstat = os.fstat

        def foreign_config(fd):
            info = real_fstat(fd)
            if stat.S_ISREG(info.st_mode) and info.st_size == len(STALE):
                return os.stat_result((*info[:4], self.uid + 1, *info[5:]))
            return info

        with mock.patch.object(self.module.os, "fstat", foreign_config):
            result = self.run_helper()
        self.assert_refused(result, "fstat-config", f"{self.config}: is owned by uid {self.uid + 1}, not {self.uid}")
        if os.geteuid() != 0:
            self.config.chmod(0)
            self.addCleanup(self.config.chmod, 0o600)
            self.assert_refused(self.run_helper(), "open-config", f"{self.config}: cannot open it:", "(EACCES)")
        self.assertEqual(self.entries(), ["config.yml"])

    def test_a_removal_failure_is_reported_with_the_path_that_remains(self):
        """The directory made read-only after the exclusive create (through a patched write): the write's refusal
        carries the unlink's failure and the temporary's path, so nothing is read as removed that was not."""

        def write_after_lockdown(fd, data):
            self.agent.chmod(0o500)
            raise OSError(errno.ENOSPC, "No space left on device")

        with mock.patch.object(self.module.os, "write", write_after_lockdown):
            result = self.run_helper()
        self.assert_refused(result, "write-temporary", "cannot write it: No space left on device (ENOSPC)")
        self.assertIn("; the temporary ", result[2])
        self.assertIn(" remains (unlink: Permission denied (EACCES))", result[2])
        self.agent.chmod(0o700)
        remaining = self.entries()
        self.assertEqual(len(remaining), 1)
        self.assertTrue(remaining[0].startswith(".config.yml."))
        self.assertIn(f"{self.agent}/{remaining[0]} remains", result[2])
        self.assertFalse(self.config.exists())

    def test_each_producers_failure_refuses_naming_its_step_and_leaves_no_temporary(self):
        """Every `os` call of the write path raises in turn (an EIO, EACCES, EROFS, ENOSPC or EXDEV the file system
        would raise); each refusal names its step, the path and the errno, the config is never replaced and no
        temporary remains."""
        real = {name: getattr(os, name) for name in ("open", "fstat", "read", "write", "fsync", "rename")}

        def failing_open(path, flags, mode=0o777, *, dir_fd=None):
            if path == str(self.agent):  # lint-comparisons: allow the name os.open received, no path identity
                raise OSError(errno.EIO, "Input/output error")
            return real["open"](path, flags, mode, dir_fd=dir_fd)

        def failing_config_open(path, flags, mode=0o777, *, dir_fd=None):
            if path == "config.yml":  # lint-comparisons: allow the name os.open received, no path identity
                raise OSError(errno.EACCES, "Permission denied")
            return real["open"](path, flags, mode, dir_fd=dir_fd)

        def failing_create(path, flags, mode=0o777, *, dir_fd=None):
            if path.startswith(".config.yml."):  # lint-comparisons: allow the name os.open received, no path identity
                raise OSError(errno.EROFS, "Read-only file system")
            return real["open"](path, flags, mode, dir_fd=dir_fd)

        def fstat_failing_for(kind):
            def failing(fd):
                info = real["fstat"](fd)
                if kind == "agent" and stat.S_ISDIR(info.st_mode):
                    raise OSError(errno.EIO, "Input/output error")
                if kind == "config" and stat.S_ISREG(info.st_mode) and info.st_size == len(STALE):
                    raise OSError(errno.EIO, "Input/output error")
                if kind == "temporary" and stat.S_ISREG(info.st_mode) and info.st_size == 0:
                    raise OSError(errno.EIO, "Input/output error")
                return info

            return failing

        def raising(code, text):
            def fail(*args, **kwargs):
                raise OSError(code, text)

            return fail

        prefix = f"{self.agent}/.config.yml."
        cases = (
            ("open", failing_open, "open-agent", f"{self.agent}: cannot open it: Input/output error (EIO)"),
            ("fstat", fstat_failing_for("agent"), "fstat-agent", f"{self.agent}: cannot read its identity:", "(EIO)"),
            ("open", failing_config_open, "open-config", f"{self.config}: cannot open it: Permission denied (EACCES)"),
            ("fstat", fstat_failing_for("config"), "fstat-config", f"{self.config}: cannot read its identity:", "(EIO)"),
            ("read", raising(errno.EIO, "Input/output error"), "read-config", f"{self.config}: cannot read it:", "(EIO)"),
            ("open", failing_create, "create-temporary", prefix, "cannot create a temporary file in", "(EROFS)"),
            ("fstat", fstat_failing_for("temporary"), "fstat-temporary", prefix, "cannot read its identity:", "(EIO)"),
            ("fchmod", raising(errno.EPERM, "Operation not permitted"), "fchmod-temporary", prefix, "(EPERM)"),
            ("write", raising(errno.ENOSPC, "No space left on device"), "write-temporary", prefix, "(ENOSPC)"),
            ("fsync", raising(errno.EIO, "Input/output error"), "fsync-temporary", prefix, "cannot flush it:", "(EIO)"),
            ("rename", raising(errno.EXDEV, "Cross-device link"), "rename", f"{self.config}: cannot install it:", "(EXDEV)"),
        )  # fmt: skip
        for name, stand_in, step, *fragments in cases:
            with self.subTest(step=step):
                self.config.write_bytes(STALE)
                with mock.patch.object(self.module.os, name, stand_in):
                    result = self.run_helper()
                self.assert_refused(result, step, *fragments)
                self.assertNotIn("remains", result[2])
                self.assertEqual(self.entries(), ["config.yml"], "no temporary remains")
                self.assertEqual(self.config.read_bytes(), STALE, "a refused run replaces nothing")
        with self.subTest(step="unlink-temporary"):
            self.config.write_bytes(STALE)
            with (
                mock.patch.object(self.module.os, "rename", raising(errno.EXDEV, "Cross-device link")),
                mock.patch.object(self.module.os, "unlink", raising(errno.EPERM, "Operation not permitted")),
            ):
                result = self.run_helper()
            self.assert_refused(result, "rename", "(EXDEV)", f"; the temporary {prefix}", "remains (unlink:", "(EPERM)")
            remaining = [name for name in self.entries() if name != "config.yml"]
            self.assertEqual(len(remaining), 1, "the temporary the unlink could not remove stands")
            self.assertIn(f"{self.agent}/{remaining[0]} remains", result[2])
            self.assertEqual(self.config.read_bytes(), STALE)

    def test_a_writer_that_swaps_the_entry_around_the_rename_ends_in_a_refusal_never_in_other_bytes(self):
        """The round-3 residual, closed by the read-back: a process owning `agent/` that swaps the temporary's entry
        between the write and the rename, or `config.yml` right after the rename, leaves the launch refused at
        `verify-placed`; two launches at once that land the same bytes both pass."""
        real_rename = os.rename
        attacker = b"modelRoles:\n  default: attacker/model\n"

        def swap_source_then_rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            (self.agent / src).unlink()
            (self.agent / src).write_bytes(attacker)
            real_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)

        def rename_then_overwrite(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            real_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
            self.config.write_bytes(attacker)

        def rename_then_same_bytes(src, dst, *, src_dir_fd=None, dst_dir_fd=None):
            real_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd)
            self.config.unlink()
            self.config.write_bytes(RENDERED)

        for label, stand_in in (
            ("the source swapped", swap_source_then_rename),
            ("the destination rewritten", rename_then_overwrite),
        ):
            with self.subTest(case=label):
                with mock.patch.object(self.module.os, "rename", stand_in):
                    result = self.run_helper()
                self.assert_refused(
                    result, "verify-placed", f"{self.config}: does not hold the rendered config after the rename"
                )
                self.assertEqual(self.entries(), ["config.yml"])
                self.config.unlink()
        with mock.patch.object(self.module.os, "rename", rename_then_same_bytes):
            self.assertEqual(self.run_helper(), (0, "placed\n", ""), "a concurrent launch of the same bytes passes")
        self.assertEqual(self.config.read_bytes(), RENDERED)

    def test_a_replacement_during_the_read_back_or_the_compare_is_refused_never_reported_as_placed_or_kept(self):
        """The round-4 verdict's P2 (`verdicts/U310d-28457a6a.md`, profile-config-place.py:225): at 28457a6a the
        read-back validated the inode it had opened, so a writer that replaced `config.yml` during `os.read` was
        reported as `placed` or `kept` while the name held its bytes. Now the read-back runs on the written descriptor
        and the name's identity is read after it: a replacement with other bytes during any read refuses at
        `verify-placed` or `verify-kept` and the attacker's bytes are never reported as the config; one replacement
        with the same bytes (a concurrent launch) passes; a writer that keeps replacing the entry, even with the same
        bytes, refuses."""
        attacker = b"modelRoles:\n  default: attacker/model\n"
        real_read = os.read

        def replacing(data, times):
            count = [0]

            def read(fd, size):
                if count[0] < times:
                    count[0] += 1
                    self.config.unlink(missing_ok=True)
                    self.config.write_bytes(data)
                return real_read(fd, size)

            return read

        cases = (
            ("other bytes during the read-back", None, (), attacker, 99, "verify-placed",
             "does not hold the rendered config after the rename"),
            ("other bytes once during the read-back", None, (), attacker, 1, "verify-placed",
             "does not hold the rendered config after the rename"),
            ("other bytes during the compare", RENDERED, (), attacker, 99, "verify-kept",
             "does not hold the rendered config after the rename"),
            ("other bytes once during the compare", RENDERED, (), attacker, 1, "verify-kept",
             "does not hold the rendered config after the rename"),
            ("other bytes during a dry run's compare", RENDERED, ("--dry-run",), attacker, 1, "verify-kept",
             "does not hold the rendered config after the rename"),
            ("the same bytes on every read", None, (), RENDERED, 99, "verify-placed",
             "config.yml replaced during placement (another inode at the name on every read)"),
        )  # fmt: skip
        for label, before, args, data, times, step, reason in cases:
            with self.subTest(case=label):
                self.config.unlink(missing_ok=True)
                if before is not None:
                    self.config.write_bytes(before)
                with mock.patch.object(self.module.os, "read", replacing(data, times)):
                    result = self.run_helper(*args)
                self.assert_refused(result, step, f"{self.config}: {reason}")
                self.assertEqual(self.entries(), ["config.yml"], "no temporary remains")
                self.assertEqual(self.config.read_bytes(), data, "the name holds the writer's bytes, never reported")
        for label, before, args, word in (
            ("one concurrent placement of the same bytes", None, (), "placed"),
            ("one concurrent placement of the same bytes at the compare", RENDERED, (), "kept"),
            ("one concurrent placement of the same bytes in a dry run", RENDERED, ("--dry-run",), "kept"),
        ):
            with self.subTest(case=label):
                self.config.unlink(missing_ok=True)
                if before is not None:
                    self.config.write_bytes(before)
                with mock.patch.object(self.module.os, "read", replacing(RENDERED, 1)):
                    self.assertEqual(self.run_helper(*args), (0, f"{word}\n", ""))
                self.assertEqual(self.config.read_bytes(), RENDERED)
                self.assertEqual(self.entries(), ["config.yml"])

    def test_usage_errors_exit_1_with_the_usage_line(self):
        for argv in ([], [str(self.agent)], [str(self.agent), "uid"], ["agent", "1"], ["--x", str(self.agent), "1"],
                     ["--dry-run"], [str(self.agent), "1", "extra"]):  # fmt: skip
            with self.subTest(argv=argv):
                out, err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    status = self.module.main(argv, io.BytesIO(RENDERED))
                self.assertEqual((status, out.getvalue()), (1, ""))
                self.assertEqual(err.getvalue(), f"{self.module.USAGE}\n")
        self.assertEqual(self.entries(), [], "a usage error writes nothing")

    def test_the_file_runs_isolated_on_the_standard_library_alone_and_is_shipped_pinned(self):
        run = subprocess.run(
            [sys.executable, "-I", "-S", str(HELPER), str(self.agent), str(self.uid)],
            input=RENDERED, capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, b"placed\n", b""))
        self.assertEqual(self.config.read_bytes(), RENDERED)
        run = subprocess.run(
            [sys.executable, "-I", "-S", str(HELPER), "--dry-run", str(self.agent), str(self.uid)],
            input=STALE, capture_output=True, check=False,
        )  # fmt: skip
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, b"differs\n", b""))
        text = HELPER.read_text()
        tree = ast.parse(text)
        imported = sorted(alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names)
        self.assertEqual(imported, ["errno", "os", "secrets", "stat", "sys"])
        self.assertEqual([node for node in tree.body if isinstance(node, ast.ImportFrom)], [])
        self.assertNotIn("environ", text.replace(ast.get_docstring(tree) or "", ""))
        self.assertNotIn("getenv", text)
        self.assertEqual(text.splitlines()[0], SHEBANG)
        self.assertTrue(os.access(HELPER, os.X_OK))
        self.assertEqual(INSTALLED.read_bytes(), HELPER.read_bytes(), "the installed copy is byte-identical")
        pins = re.findall(r"^      profile-config-place\.py: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)
        self.assertEqual(pins, [hashlib.sha256(HELPER.read_bytes()).hexdigest()])

    def test_the_docs_sentence_and_the_readme_paragraph_name_the_helper_and_its_mechanism(self):
        """docs/deepseek-harness.md (the dsh harness page) and scripts/orchestrator/README.md (the dsh role's profile
        config paragraph) describe the write as it is: the pinned helper beside the lever, one held descriptor of
        `agent/`, the exclusive create at a random name, the rename, the read-back, the refusal by step, this test
        file; a description that promises the earlier rounds' bash write fails here."""
        docs = (ROOT / "docs/deepseek-harness.md").read_text()
        readme = (ROOT / "scripts/orchestrator/README.md").read_text()
        paragraph = next(p for p in readme.split("\n\n") if p.startswith("The dsh role's profile config row"))
        for text, label in ((docs, "docs"), (paragraph, "README paragraph")):
            with self.subTest(text=label):
                for phrase in ("profile-config-place.py", "held descriptor", "`dir_fd`", "`O_NOFOLLOW`", "random name",
                               "rename", "read-back", "tests/unit/test_profile_config_place.py", "U310d"):  # fmt: skip
                    self.assertIn(phrase, text, phrase)
                for stale in ("exec 9>", "noclobber", "`mktemp`", "mktemp(", "tmp_refuse", "profile_config_tmp"):
                    self.assertNotIn(stale, text, stale)
        self.assertIn("refuses with exit 2 naming the step", docs)
        self.assertIn("the dsh role requires `python3`, which runs its profile config helper", readme)


if __name__ == "__main__":
    unittest.main()
