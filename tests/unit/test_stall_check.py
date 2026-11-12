"""Exercise scripts/orchestrator/stall-check.py (regime-cutover U496, round 2 U496b, round 3 U496c and U496d), the
coordinator's one reader of the in-flight workers' progress files: one row per `units.tsv` row whose state is
`in-flight` and whose track is not `sweep`, in the register's order, `unit<TAB>state<TAB>age_minutes<TAB>last_line`,
the state one of `moving`, `stalled`, `done`, `no-file` and `unreadable` (a file that yields no text or a last line
outside the grammar is that one unit's row, exit 2, never a refusal that hides the other units), the one run-level
refusal a register that cannot be read, the register's header and the paths held before anything is read, the store
and the progress root each held as a directory descriptor, every file opened relative to that descriptor without
following a link and judged on its own descriptor. Every test but the swap tests runs the lever as a subprocess under
`python3 -I` over a scratch store and a scratch progress root with the clock injected by `--now`; the swap tests
import the lever and time a swap between its `lstat` and its `open`, of one file and of the validated root; nothing
reads the live store, `/tmp/dotfiles-wt` or the real `~/.agents`, and the lever is proved to write nothing.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/stall-check.py"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_stall-check.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote\n"
NOW = "2026-11-12T06:30:00Z"
HEAD = "a" * 40
REFUSED = "stall-check.py: refused: "


def unit_row(unit: str, track: str = "feat", state: str = "in-flight", **cells: str) -> str:
    """One register row of the eight cells; the empty cells are the live table's for a unit without a pull request."""
    values = {"branch": "", "pr": "", "head_sha": "", "brief": f"briefs/{unit}-x.md", "note": "", **cells}
    return "\t".join((unit, track, state, *values.values())) + "\n"


class StallCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # The scratch directory as given (on macOS `/var/...`, a path through a link the lever resolves itself).
        self.dir = Path(self.temp.name)
        self.store = self.dir / "regime-store/dotfiles/regime-cutover"
        self.store.mkdir(parents=True)
        self.progress = self.dir / "dotfiles-wt"
        self.progress.mkdir()
        self.home = self.dir / "home"
        self.home.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}
        # Three in-flight units of three tracks, a landed one and an in-flight sweep seat, in this order.
        self.write_units(
            unit_row("U1", state="landed", pr="700", head_sha=HEAD),
            unit_row("U2"),
            unit_row("U3", track="fix", branch="fix/x", pr="701", head_sha=HEAD),
            unit_row("U4", track="dsh"),
            unit_row("U5", track="sweep", pr="701", head_sha=HEAD),
        )
        # U2 moving (3 minutes), U3 stalled (14 minutes), U4 done (10 minutes); the trailing newline every append
        # leaves, and a first line older than the deadline that decides nothing.
        self.write_progress(
            "U2", "2026-11-12T06:10:00Z U2 start: brief read", "2026-11-12T06:27:00Z U2: red tests pasted"
        )
        self.write_progress("U3", "2026-11-12T06:16:00Z U3 start: brief read")
        self.write_progress(
            "U4", "2026-11-12T06:05:00Z U4 start: brief read", f"2026-11-12T06:20:00Z done, head={HEAD}"
        )
        self.expected = (
            "U2\tmoving\t3\t2026-11-12T06:27:00Z U2: red tests pasted\n"
            "U3\tstalled\t14\t2026-11-12T06:16:00Z U3 start: brief read\n"
            f"U4\tdone\t10\t2026-11-12T06:20:00Z done, head={HEAD}\n"
        )

    def write_units(self, *rows: str, header: str = HEADER) -> None:
        (self.store / "units.tsv").write_text(header + "".join(rows))

    def write_progress(self, unit: str, *lines: str, end: str = "\n") -> Path:
        path = self.progress / f"{unit}-progress.txt"
        path.write_text("\n".join(lines) + end)
        return path

    def run_lever(
        self,
        *args: str,
        store: str | None = None,
        root: str | None = None,
        now: str | None = NOW,
        lever: Path = LEVER,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess:
        argv = [sys.executable, "-I", str(lever), str(self.store) if store is None else store]
        argv += ["--progress-root", str(self.progress) if root is None else root] if root != "" else []
        argv += ["--now", now] if now is not None else []
        argv += list(args)
        return subprocess.run(
            argv, capture_output=True, text=True, check=False, timeout=60, env=env or self.env, cwd=self.dir
        )

    def lever_bytecode(self) -> list[str]:
        """The names under `scripts/orchestrator/__pycache__` that are this lever's bytecode (`stall-check*`), the
        proof the run and the in-process import compiled nothing to disk. The directory itself is no evidence: CI's
        earlier test modules import `ledger.py` from `scripts/orchestrator` and leave their bytecode there, so an
        assertion on the directory held on a fresh tree and failed on every CI leg (round 3, U496c)."""
        cache = LEVER.parent / "__pycache__"
        if not cache.is_dir():
            return []
        return sorted(name for name in os.listdir(cache) if name.startswith("stall-check"))

    def listing(self) -> list[tuple[str, int, int]]:
        """Every entry under the scratch directory with its size and mtime, the proof that nothing was written."""
        entries = []
        for base, dirs, files in os.walk(self.dir):
            for name in sorted(dirs) + sorted(files):
                status = os.lstat(os.path.join(base, name))
                entries.append(
                    (os.path.relpath(os.path.join(base, name), self.dir), status.st_size, status.st_mtime_ns)
                )
        return sorted(entries)

    def assert_refused(self, run: subprocess.CompletedProcess, *reasons: str) -> str:
        """Exit 2, nothing on stdout, one stderr line in the levers' words naming every reason, no traceback."""
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(REFUSED), run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)
        return run.stderr

    # CHANGE 1: the three states of a worker, the sweep row ignored, the row shape and the exit code.

    def test_one_row_per_in_flight_unit_in_register_order_and_the_sweep_row_ignored(self) -> None:
        """Three in-flight units: one moving (a line 3 minutes old), one stalled (14 minutes), one done; the landed
        row and the in-flight sweep row (a sweep seat reports on the bus, not in a file) are no rows; the rows in the
        register's order, tab-separated, `age_minutes` an integer, `last_line` the whole last line; exit 1 for the
        stalled one; nothing on stderr."""
        self.assertEqual(self.lever_bytecode(), [], "no bytecode of the lever before the run")
        before = self.listing()
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout, run.stderr), (1, self.expected, ""))
        self.assertEqual(self.listing(), before, "no file was written, none was touched")
        self.assertEqual(self.lever_bytecode(), [], "no bytecode of the lever after the run")

    def test_exit_0_when_every_row_is_moving_or_done(self) -> None:
        self.write_progress("U3", "2026-11-12T06:16:00Z U3 start: brief read", "2026-11-12T06:29:30Z U3: committing")
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(
            run.stdout,
            "U2\tmoving\t3\t2026-11-12T06:27:00Z U2: red tests pasted\n"
            "U3\tmoving\t0\t2026-11-12T06:29:30Z U3: committing\n"
            f"U4\tdone\t10\t2026-11-12T06:20:00Z done, head={HEAD}\n",
        )

    def test_a_done_line_prefixed_with_the_unit_id_is_done_and_another_unit_s_is_not(self) -> None:
        """The workers write `<unit> done, head=<sha>` as often as the brief's bare `done, head=<sha>` (U490 and U495
        measured 2026-11-12), so the row's own id before `done,` is the done form too; another unit's id is not, and
        the age decides."""
        self.write_progress("U4", f"2026-11-12T06:20:00Z U4 done, head={HEAD}")
        run = self.run_lever()
        self.assertIn(f"U4\tdone\t10\t2026-11-12T06:20:00Z U4 done, head={HEAD}\n", run.stdout)
        self.write_progress("U4", f"2026-11-12T06:10:00Z U3 done, head={HEAD}")
        run = self.run_lever()
        self.assertIn(f"U4\tstalled\t20\t2026-11-12T06:10:00Z U3 done, head={HEAD}\n", run.stdout)
        self.write_progress("U4", "2026-11-12T06:29:00Z U4: done with the tests, committing")
        run = self.run_lever()
        self.assertIn("U4\tmoving\t1\t2026-11-12T06:29:00Z U4: done with the tests, committing\n", run.stdout)

    def test_a_unit_without_a_progress_file_is_no_file_with_a_dash_age_and_exit_1(self) -> None:
        """The worker never wrote its first line: reported like a stall, `-` for the age and the line."""
        (self.progress / "U2-progress.txt").unlink()
        self.write_progress("U3", "2026-11-12T06:29:00Z U3: committing")
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (1, ""), run.stdout)
        self.assertEqual(
            run.stdout,
            "U2\tno-file\t-\t-\n"
            "U3\tmoving\t1\t2026-11-12T06:29:00Z U3: committing\n"
            f"U4\tdone\t10\t2026-11-12T06:20:00Z done, head={HEAD}\n",
        )

    def test_an_empty_in_flight_set_prints_nothing_and_exits_0(self) -> None:
        self.write_units(unit_row("U1", state="landed"), unit_row("U5", track="sweep"))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))

    def test_the_age_is_whole_minutes_and_a_tab_or_carriage_return_in_the_line_is_a_space(self) -> None:
        """`age_minutes` is the floor of the last line's age in minutes, so 3 minutes 59 seconds is 3; the contract
        is tab-separated lines, so a tab or a carriage return inside the worker's free text is one space in the cell
        and the row keeps its four cells."""
        self.write_progress("U2", "2026-11-12T06:26:01Z U2:\tstep one\rdone")
        run = self.run_lever()
        self.assertIn("U2\tmoving\t3\t2026-11-12T06:26:01Z U2: step one done\n", run.stdout)
        self.assertEqual(run.stdout.count("\t"), 9, run.stdout)

    # CHANGE 1: the options.

    def test_the_deadline_option_moves_the_boundary_and_a_bad_value_is_refused(self) -> None:
        """`--deadline-minutes` defaults to 10: an age equal to it is moving, one more minute is stalled; the 14-minute
        unit is moving under 14 and stalled under 13; a value that is not 1 to 10 decimal digits without a leading
        zero, or is outside 1 to 1440 (24 hours), is a one-line exit-2 refusal, a 4301-digit value included (it raised
        `int()`'s digit limit as a traceback at d1256438, verdict U496-d1256438 P2); 1 and 1440 are accepted."""
        self.write_progress("U3", "2026-11-12T06:20:00Z U3 start: brief read")
        run = self.run_lever()
        self.assertIn("U3\tmoving\t10\t", run.stdout)
        self.assertEqual(run.returncode, 0)
        self.write_progress("U3", "2026-11-12T06:19:00Z U3 start: brief read")
        run = self.run_lever()
        self.assertIn("U3\tstalled\t11\t", run.stdout)
        self.assertEqual(run.returncode, 1)
        self.write_progress("U3", "2026-11-12T06:16:00Z U3 start: brief read")
        run = self.run_lever("--deadline-minutes", "14")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertIn("U3\tmoving\t14\t", run.stdout)
        run = self.run_lever("--deadline-minutes", "13")
        self.assertEqual(run.returncode, 1)
        self.assertIn("U3\tstalled\t14\t", run.stdout)
        for value in ("-1", "x", "1.5", "", "010", "10 ", "0", "1441", "9" * 4301, "1" * 11):
            with self.subTest(value=value):
                self.assert_refused(self.run_lever("--deadline-minutes", value), "--deadline-minutes")
        for value in ("1", "1440"):
            with self.subTest(value=value):
                run = self.run_lever("--deadline-minutes", value)
                self.assertEqual(run.stderr, "", run.stdout)
                self.assertIn(run.returncode, (0, 1))
                self.assertEqual(run.stdout.count("\n"), 3)

    def test_the_now_option_is_the_clock_and_a_bad_one_is_refused(self) -> None:
        """`--now` injects the clock in the progress lines' own form; twenty minutes later every line is stalled; a
        value of another shape, a date that is none, or one that is not UTC is a refusal naming the option."""
        run = self.run_lever(now="2026-11-12T06:50:00Z")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(
            run.stdout,
            "U2\tstalled\t23\t2026-11-12T06:27:00Z U2: red tests pasted\n"
            "U3\tstalled\t34\t2026-11-12T06:16:00Z U3 start: brief read\n"
            f"U4\tdone\t30\t2026-11-12T06:20:00Z done, head={HEAD}\n",
        )
        for value in ("2026-11-12 06:50:00", "2026-11-12T06:50:00+00:00", "2026-13-40T06:50:00Z", "now", ""):
            with self.subTest(value=value):
                self.assert_refused(self.run_lever(now=value), "--now")

    def test_without_now_the_clock_is_the_wall_clock(self) -> None:
        """Lines written now are moving; the age is 0 when the lever runs within the minute."""
        from datetime import datetime, timezone

        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.write_progress("U2", f"{ts} U2: now")
        self.write_progress("U3", f"{ts} U3: now")
        self.write_progress("U4", f"{ts} done, head={HEAD}")
        run = self.run_lever(now=None)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(
            run.stdout,
            f"U2\tmoving\t0\t{ts} U2: now\nU3\tmoving\t0\t{ts} U3: now\nU4\tdone\t0\t{ts} done, head={HEAD}\n",
        )

    def test_the_default_progress_root_is_slug_wt_under_tmpdir_from_the_store_s_parent_name(self) -> None:
        """Without `--progress-root` the root is the temporary directory (`$TMPDIR` when set and not empty, else the
        system default) plus `<slug>-wt`, the slug the store path's parent directory name (`dotfiles` for
        `.../regime-store/dotfiles/regime-cutover`), the root `worker-worktree.sh` uses: with `TMPDIR` the scratch
        directory (given through macOS's `/var` link, with and without the trailing separator this host's `TMPDIR`
        carries) the rows come from `<scratch>/dotfiles-wt`; with a slug no host has, the root is no directory and
        the run is a refusal naming the path as composed and as resolved physically (`/private/var` for `/var`;
        standing order 21: a missing root is a wrong root, never an empty set of workers); an empty `TMPDIR` is no
        root of `''` but the system default, the `${TMPDIR:-...}` rule (round 3, U496c: CI's portability guard
        refuses a spelled temporary path)."""
        for tmpdir in (str(self.dir), str(self.dir) + "/"):
            with self.subTest(tmpdir=tmpdir):
                run = self.run_lever(root="", env={**self.env, "TMPDIR": tmpdir})
                self.assertEqual((run.returncode, run.stdout, run.stderr), (1, self.expected, ""))
        slug = f"u496-no-such-slug-{os.getpid()}"
        store = self.dir / "regime-store" / slug / "regime-cutover"
        store.mkdir(parents=True)
        shutil.copy2(self.store / "units.tsv", store / "units.tsv")
        composed, resolved = self.dir / f"{slug}-wt", self.dir.resolve() / f"{slug}-wt"
        self.assert_refused(
            self.run_lever(store=str(store), root="", env={**self.env, "TMPDIR": str(self.dir)}),
            "progress root",
            f"'{composed}' ({resolved}) cannot be read",
        )
        self.assert_refused(
            self.run_lever(store=str(store), root="", env={**self.env, "TMPDIR": ""}),
            "progress root",
            f"'/tmp/{slug}-wt'",
        )

    # CHANGE 1 (round 2, U496b): a bad progress file is one unit's row; then the refusals, each exit 2 with one stderr
    # line and nothing on stdout.

    def test_an_unreadable_progress_file_is_that_unit_s_row_and_the_other_rows_still_print(self) -> None:
        """A file that exists but yields no text, or whose last line carries no timestamp of the form, is that one
        unit's `unreadable` row: `-` for the age, the last line in the fourth cell when there is one (`-` when the
        file gave no text); the other units' rows print as before, nothing goes to stderr, and the run exits 2, the
        maximum over the rows, never a refusal that hides every other unit (verdict U496-d1256438 P1 :338)."""
        path = self.progress / "U3-progress.txt"
        cases = [
            ("empty", lambda: path.write_bytes(b""), "-"),
            ("blank last line", lambda: path.write_text("2026-11-12T06:16:00Z U3 start\n\n"), "-"),
            (
                "no timestamp",
                lambda: path.write_text("2026-11-12T06:16:00Z U3 start\nU3: committing\n"),
                "U3: committing",
            ),
            ("no space after the timestamp", lambda: path.write_text("2026-11-12T06:16:00Z\n"), "2026-11-12T06:16:00Z"),
            (
                "a local time",
                lambda: path.write_text("2026-11-12T15:16:00+09:00 U3 start\n"),
                "2026-11-12T15:16:00+09:00 U3 start",
            ),
            (
                "no such date",
                lambda: path.write_text("2026-13-40T06:16:00Z U3 start\n"),
                "2026-13-40T06:16:00Z U3 start",
            ),
            (
                "after --now",
                lambda: path.write_text("2026-11-12T06:30:01Z U3 start\n"),
                "2026-11-12T06:30:01Z U3 start",
            ),
            ("a tab in a bad line", lambda: path.write_text("U3:\tstep one\rdone\n"), "U3: step one done"),
            ("not UTF-8", lambda: path.write_bytes(b"2026-11-12T06:16:00Z U3 \xff\n"), "-"),
            ("a directory", lambda: path.mkdir(), "-"),
            ("a symbolic link", lambda: path.symlink_to(self.progress / "U2-progress.txt"), "-"),
        ]
        if os.geteuid() != 0:
            cases.insert(
                0, ("mode 000", lambda: (path.write_text("2026-11-12T06:16:00Z U3 start\n"), path.chmod(0)), "-")
            )
        for label, plant, last in cases:
            with self.subTest(case=label):
                plant()
                try:
                    run = self.run_lever()
                    self.assertEqual((run.returncode, run.stderr), (2, ""), run.stdout)
                    self.assertEqual(
                        run.stdout,
                        "U2\tmoving\t3\t2026-11-12T06:27:00Z U2: red tests pasted\n"
                        f"U3\tunreadable\t-\t{last}\n"
                        f"U4\tdone\t10\t2026-11-12T06:20:00Z done, head={HEAD}\n",
                    )
                finally:
                    # The planted entry goes after each case, whatever it was, so the next case starts from no entry.
                    if path.is_symlink():
                        path.unlink()
                    elif path.is_dir():
                        path.rmdir()
                    elif path.exists():
                        path.chmod(0o644)
                        path.unlink()

    def test_a_bare_done_line_without_a_timestamp_is_that_unit_s_unreadable_row_not_a_refusal(self) -> None:
        """The brief's literal `done, head=<40 hex>` as the last line with no timestamp (U497's worker, measured
        2026-11-12T06:48Z) refused the whole run at d1256438 and hid every other unit; it is now U4's row
        `unreadable<TAB>-<TAB>done, head=<sha>`, the other two rows print, exit 2, nothing on stderr; the same for the
        bare `<unit> done, head=<sha>` and for any other text without the timestamp."""
        for last in (f"done, head={HEAD}", f"U4 done, head={HEAD}", "all tests green, committing"):
            with self.subTest(last=last):
                self.write_progress("U4", "2026-11-12T06:05:00Z U4 start: brief read", last)
                run = self.run_lever()
                self.assertEqual((run.returncode, run.stderr), (2, ""), run.stdout)
                self.assertEqual(
                    run.stdout,
                    "U2\tmoving\t3\t2026-11-12T06:27:00Z U2: red tests pasted\n"
                    "U3\tstalled\t14\t2026-11-12T06:16:00Z U3 start: brief read\n"
                    f"U4\tunreadable\t-\t{last}\n",
                )

    def test_a_progress_path_that_is_a_link_outside_the_root_is_unreadable_and_the_target_s_text_never_printed(
        self,
    ) -> None:
        """A progress path that is a symbolic link to a file outside the progress root (the swap the verdict's P1 :281
        reproduced) is that unit's `unreadable` row with `-` for the line: the target's text reaches neither stdout
        nor stderr; a link to a directory and a dangling link are the same row."""
        outside = self.dir / "outside" / "secret.txt"
        outside.parent.mkdir()
        outside.write_text("2026-11-12T06:29:00Z OUTSIDE-SECRET-LINE\n")
        path = self.progress / "U3-progress.txt"
        for target in (outside, self.dir, self.dir / "no-such-file"):
            with self.subTest(target=str(target)):
                path.unlink()
                path.symlink_to(target)
                run = self.run_lever()
                self.assertEqual((run.returncode, run.stderr), (2, ""), run.stdout)
                self.assertIn("U3\tunreadable\t-\t-\n", run.stdout)
                self.assertNotIn("OUTSIDE-SECRET-LINE", run.stdout + run.stderr)
                self.assertEqual(run.stdout.count("\n"), 3, run.stdout)

    def load_lever(self):
        """The lever as a module of this process (its top level defines; the self check and `main` run under
        `__main__` alone), for the one check a subprocess cannot time: a swap between its `lstat` and its `open`."""
        spec = importlib.util.spec_from_file_location("stall_check_under_test", LEVER)
        module = importlib.util.module_from_spec(spec)
        # No bytecode beside the lever: the import writes no `__pycache__` the subprocess tests would then see.
        with mock.patch.object(sys, "dont_write_bytecode", True):
            spec.loader.exec_module(module)
        return module

    def test_a_file_swapped_between_the_lstat_and_the_open_is_unreadable_and_no_outside_text_is_read(self) -> None:
        """The lever `lstat`s the name under the held root, opens it with `O_NOFOLLOW | O_CLOEXEC` relative to the
        root's descriptor and `fstat`s the file's descriptor (a regular file on the device and inode the `lstat` saw)
        before it reads from that descriptor. Swapping the file for a link to an outside file right after the `lstat`
        (the verdict's deterministic swap) gives `unreadable`, `-`, `-`; swapping it for the outside file itself
        (another inode) gives the same row, never the outside line, which `judge` returned at d1256438."""
        module = self.load_lever()
        now = datetime.strptime(NOW, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        root = module.held_root(str(self.progress.resolve()), "progress root")
        self.addCleanup(os.close, root)
        path = self.progress / "U3-progress.txt"
        outside = self.dir / "outside.txt"
        outside.write_text("2026-11-12T06:29:00Z OUTSIDE-SECRET-LINE\n")
        real_open = os.open

        def swap_for_a_link(*args, **kwargs):
            path.unlink()
            path.symlink_to(outside)
            return real_open(*args, **kwargs)

        def swap_for_the_outside_file(*args, **kwargs):
            os.replace(outside, path)
            return real_open(*args, **kwargs)

        self.assertEqual(
            module.judge(root, "U3", now, 10), ("stalled", "14", "2026-11-12T06:16:00Z U3 start: brief read")
        )
        with mock.patch.object(module.os, "open", swap_for_a_link):
            self.assertEqual(module.judge(root, "U3", now, 10), ("unreadable", "-", "-"))
        path.unlink()
        self.write_progress("U3", "2026-11-12T06:16:00Z U3 start: brief read")
        with mock.patch.object(module.os, "open", swap_for_the_outside_file):
            row = module.judge(root, "U3", now, 10)
        self.assertEqual(row, ("unreadable", "-", "-"))
        self.assertNotIn("OUTSIDE-SECRET-LINE", "".join(row))
        self.assertEqual(path.read_text(), "2026-11-12T06:29:00Z OUTSIDE-SECRET-LINE\n", "the swap took place")

    def run_main_in_process(self, module, swapping_open) -> tuple[int, str, str]:
        """`main` over the scratch store and root with `os.open` patched by `swapping_open`, as the swap test runs
        `judge`: the exit code (a refusal's SystemExit folded in), stdout and stderr."""
        argv = [str(self.store), "--progress-root", str(self.progress), "--now", NOW]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            with mock.patch.object(module.os, "open", swapping_open):
                try:
                    code = module.main(argv)
                except SystemExit as stop:
                    code = stop.code
        return code, out.getvalue(), err.getvalue()

    def test_the_validated_root_swapped_for_a_link_to_another_directory_is_never_read_through(self) -> None:
        """Verdict U496-6f774696 P1 :290: at 6f774696 the auditor replaced the validated progress root with a symbolic
        link to another directory before the lookup, `os.lstat(<root>/<name>)` and `os.open(<path>, O_NOFOLLOW)`
        followed the root link (O_NOFOLLOW guards the last component alone) and the other directory's file was
        printed as a moving worker line. The root is now opened once as a directory descriptor
        (`O_RDONLY | O_DIRECTORY | O_NOFOLLOW | O_CLOEXEC`, `fstat` matched against the validated root's `lstat`) and
        every progress file is opened by its bare name relative to it, so the same swap, timed at the first progress
        file's `os.open` as the file swap test times its own, reads the validated directory still (the rows unchanged
        when the directory was renamed aside; `unreadable` for the file whose open the swap preceded and `no-file` for
        the rest when it was removed) and never the other directory's text; the swap timed at the root's own open is
        a refusal naming the root, nothing on stdout."""
        module = self.load_lever()
        real_open = os.open
        outside = self.dir / "outside-wt"
        outside.mkdir()
        for unit in ("U2", "U3", "U4"):
            (outside / f"{unit}-progress.txt").write_text(f"2026-11-12T06:29:00Z OUTSIDE-SECRET-LINE {unit}\n")
        root = self.progress.resolve()
        aside = self.dir / "aside-wt"

        def swap_at_the_first_progress_file(how):
            def swapping_open(path, flags, *args, **kwargs):
                if os.fspath(path).endswith("U2-progress.txt") and not os.path.islink(root):
                    how()
                    os.symlink(outside, root)
                return real_open(path, flags, *args, **kwargs)

            return swapping_open

        def swap_at_the_root_open(path, flags, *args, **kwargs):
            if flags & os.O_DIRECTORY and os.fspath(path).endswith("dotfiles-wt") and not os.path.islink(root):
                os.rename(root, aside)
                os.symlink(outside, root)
            return real_open(path, flags, *args, **kwargs)

        with self.subTest(swap="the directory renamed aside, a link in its place"):
            code, out, err = self.run_main_in_process(
                module, swap_at_the_first_progress_file(lambda: os.rename(root, aside))
            )
            self.assertTrue(os.path.islink(root), "the swap took place")
            self.assertEqual((code, out, err), (1, self.expected, ""))
            os.unlink(root)
            os.rename(aside, root)
        with self.subTest(swap="the directory removed, a link in its place"):
            code, out, err = self.run_main_in_process(
                module, swap_at_the_first_progress_file(lambda: shutil.rmtree(root))
            )
            self.assertTrue(os.path.islink(root), "the swap took place")
            self.assertEqual((code, err), (2, ""), out)
            self.assertEqual(out, "U2\tunreadable\t-\t-\nU3\tno-file\t-\t-\nU4\tno-file\t-\t-\n")
            os.unlink(root)
            root.mkdir()
            self.write_progress("U2", "2026-11-12T06:27:00Z U2: red tests pasted")
            self.write_progress("U3", "2026-11-12T06:16:00Z U3 start: brief read")
            self.write_progress("U4", f"2026-11-12T06:20:00Z done, head={HEAD}")
        with self.subTest(swap="between the root's validation and its open"):
            code, out, err = self.run_main_in_process(module, swap_at_the_root_open)
            self.assertTrue(os.path.islink(root), "the swap took place")
            self.assertEqual((code, out), (2, ""), err)
            self.assertEqual(err.count("\n"), 1, err)
            self.assertTrue(err.startswith(REFUSED), err)
            self.assertIn(f"progress root {root}", err)
            self.assertNotIn("Traceback", err)
            os.unlink(root)
            os.rename(aside, root)
        self.assertNotIn("OUTSIDE-SECRET-LINE", out + err)

    def test_a_platform_whose_os_open_lacks_dir_fd_is_a_refusal_naming_it(self) -> None:
        """The relative opens need `dir_fd` (`os.open` and `os.lstat` in `os.supports_dir_fd`, true on macOS and
        Linux, judged once at import); a platform without it is one refusal naming `dir_fd`, nothing on stdout."""
        module = self.load_lever()
        self.assertTrue(module.DIR_FD_SUPPORTED, "this host opens relative to a directory descriptor")
        with mock.patch.object(module, "DIR_FD_SUPPORTED", False):
            code, out, err = self.run_main_in_process(module, os.open)
        self.assertEqual((code, out), (2, ""), err)
        self.assertTrue(err.startswith(REFUSED), err)
        self.assertIn("dir_fd", err)
        self.assertEqual(err.count("\n"), 1, err)

    def test_the_readme_table_row_names_the_row_contract_for_an_unreadable_file(self) -> None:
        """Verdict U496-6f774696 P2 :328: the seat-lever table's `stall-check.py` row said an unreadable progress file
        refuses the run, the round-1 contract round 2 replaced; the row names the five states, `unreadable` as that
        one unit's row and never a refusal, and the root held as a directory descriptor."""
        readme = (ROOT / "scripts/orchestrator/README.md").read_text()
        rows = [line for line in readme.splitlines() if line.startswith("| `~/.local/bin/common/stall-check.py *`")]
        self.assertEqual(len(rows), 1, "one table row for the lever")
        row = rows[0]
        self.assertNotIn("an unreadable file a refusal", row)
        for words in ("`unreadable`", "that unit's row", "never a refusal", "directory descriptor"):
            self.assertIn(words, row)

    def test_the_register_is_held_to_its_header_and_its_shape_before_any_file_is_read(self) -> None:
        """`units.tsv` absent, with another header, with a row of another width, with an id that is no unit, with a
        carriage return, or a symbolic link: exit 2 naming the file (and the line), nothing on stdout."""
        units = self.store / "units.tsv"
        real = str(units.resolve())
        units.unlink()
        self.assert_refused(self.run_lever(), real)
        self.write_units(unit_row("U2"), header="id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\n")
        self.assert_refused(self.run_lever(), real, "header")
        self.write_units(unit_row("U2"), header="ID\tTRACK\tSTATE\tBRANCH\tPR\tHEAD_SHA\tBRIEF\tNOTE\n")
        self.assert_refused(self.run_lever(), real, "header")
        self.write_units(unit_row("U2"), "U3\tfix\tin-flight\t\t\t\t\n")
        self.assert_refused(self.run_lever(), real, "line 3", "7 cells")
        self.write_units(unit_row("U2"), unit_row("U3") + "\n")
        self.assert_refused(self.run_lever(), real, "line 4")
        self.write_units(unit_row("U2"), unit_row("../U3"))
        self.assert_refused(self.run_lever(), real, "line 3", "'../U3'")
        self.write_units(unit_row("U2"), unit_row("U3", note="a note\r"))
        self.assert_refused(self.run_lever(), real, "line 3", "carriage return")
        self.write_units(unit_row("U2"))
        shutil.move(units, self.store / "register.tsv")
        units.symlink_to(self.store / "register.tsv")
        self.assert_refused(self.run_lever(), "units.tsv", "symbolic link")
        units.unlink()
        units.mkdir()
        self.assert_refused(self.run_lever(), real)

    def test_an_unclean_or_wrong_path_is_refused(self) -> None:
        """The store and the progress root are each an absolute path without an empty, `.` or `..` component (so no
        trailing or repeated separator), resolved by the lever itself, and a directory; a relative path, a path through
        `..`, a file, or a missing directory is a refusal naming the argument."""
        for store in ("regime-store/dotfiles/regime-cutover", f"{self.store}/", f"{self.store}/../regime-cutover"):
            with self.subTest(store=store):
                self.assert_refused(self.run_lever(store=store), "store", store)
        for root in ("dotfiles-wt", f"{self.progress}/", f"{self.progress}/./", f"{self.dir}/no-such-root"):
            with self.subTest(root=root):
                self.assert_refused(self.run_lever(root=root), "progress root", root)
        self.assert_refused(self.run_lever(store=str(self.store / "units.tsv")), "store", "not a directory")
        self.assert_refused(self.run_lever(store=str(self.dir / "no-such-store")), "store", "no-such-store")
        self.assert_refused(
            self.run_lever(root=str(self.progress / "U2-progress.txt")), "progress root", "not a directory"
        )
        for argv in (
            ("--progress-root", str(self.progress), "--now", NOW),
            (str(self.store), "--progress-root", str(self.progress), "--now", NOW, "--extra"),
            (str(self.store), "--progress-root"),
            (str(self.store), "--now", NOW, str(self.progress)),
        ):
            with self.subTest(argv=argv):
                run = subprocess.run(
                    [sys.executable, "-I", str(LEVER), *argv],
                    capture_output=True,
                    text=True,
                    env=self.env,
                    cwd=self.dir,
                )
                self.assert_refused(run)
        run = subprocess.run(
            [sys.executable, "-I", str(LEVER), str(self.store), "--progress-root", f"{self.progress}\n"],
            capture_output=True,
            text=True,
            env=self.env,
            cwd=self.dir,
        )
        self.assert_refused(run, "argument 3", "newline")

    # CHANGE 1: the self pin.

    def installed_layout(self) -> tuple[Path, dict[str, str]]:
        """The deployed layout under the scratch HOME (tests/unit/test_lever_self_check.py's): the copy chezmoi installs
        at ~/.local/bin/common/stall-check.py and the manifest at ~/.agents/agent-config.yaml."""
        (self.home / ".local/bin/common").mkdir(parents=True)
        (self.home / ".agents").mkdir()
        copy = self.home / ".local/bin/common/stall-check.py"
        shutil.copy2(INSTALLED, copy)
        shutil.copy2(MANIFEST, self.home / ".agents/agent-config.yaml")
        return copy, dict(self.env)

    def test_the_self_check_refuses_an_altered_installed_copy_naming_the_digest_and_passes_the_pinned_one(self) -> None:
        """Before anything is read the lever hashes itself against `claude.levers.sha256.stall-check.py` in the manifest
        beside it (brief-check.py's form): the installed copy under the physical `~/.local/bin/common` reads the
        deployed `~/.agents/agent-config.yaml`, the checkout copy the checkout's; a differing digest, a zeroed or a
        missing pin, and an unreadable manifest are each exit 2 with one line and nothing on stdout."""
        copy, env = self.installed_layout()
        pin = re.search(r"^      stall-check\.py: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)[1]
        self.assertEqual(hashlib.sha256(INSTALLED.read_bytes()).hexdigest(), pin, "the committed pin is current")
        self.assertEqual(INSTALLED.read_bytes(), LEVER.read_bytes(), "the installed copy is the checkout's bytes")
        self.assertEqual(INSTALLED.stat().st_mode & 0o111, 0o111, "the generated copy is executable")
        self.assertEqual(LEVER.stat().st_mode & 0o111, 0o111, "the source is executable")
        self.assertTrue(
            LEVER.read_text().startswith("#!/usr/bin/env -S python3 -I\n"), "the lever's own interpreter line"
        )
        run = self.run_lever(lever=copy, env=env)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (1, self.expected, ""))
        with copy.open("a") as handle:
            handle.write('print("rewritten")\n')
        altered = hashlib.sha256(copy.read_bytes()).hexdigest()
        self.assertEqual(
            self.assert_refused(self.run_lever(lever=copy, env=env)),
            f"{REFUSED}sha256 {altered} of {copy.resolve()} differs from the pin in {self.home}/.agents/agent-config.yaml\n",
        )
        # The deployed manifest is the installed copy's, not the checkout's: a zeroed deployed pin refuses the sound copy.
        shutil.copy2(INSTALLED, copy)
        manifest = self.home / ".agents/agent-config.yaml"
        manifest.write_text(
            manifest.read_text().replace(f"      stall-check.py: {pin}", "      stall-check.py: " + "0" * 64)
        )
        self.assert_refused(self.run_lever(lever=copy, env=env), f"differs from the pin in {manifest}")
        manifest.write_text(MANIFEST.read_text().replace(f"      stall-check.py: {pin}\n", ""))
        self.assert_refused(self.run_lever(lever=copy, env=env), "no single sha256 pin for stall-check.py in")
        manifest.unlink()
        self.assert_refused(self.run_lever(lever=copy, env=env), f"manifest unreadable: {manifest}")
        # The checkout copy reads the checkout manifest: a scratch checkout with a zeroed pin refuses its copy too.
        checkout = self.dir / "checkout"
        (checkout / "scripts/orchestrator").mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(LEVER, checkout / "scripts/orchestrator/stall-check.py")
        (checkout / "home/dot_agents/agent-config.yaml").write_text(
            MANIFEST.read_text().replace(f"      stall-check.py: {pin}", "      stall-check.py: " + "0" * 64)
        )
        self.assert_refused(
            self.run_lever(lever=checkout / "scripts/orchestrator/stall-check.py", env=env),
            "differs from the pin in",
            "checkout/scripts/orchestrator/../../home/dot_agents/agent-config.yaml",
        )


if __name__ == "__main__":
    unittest.main()
