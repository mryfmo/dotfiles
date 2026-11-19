"""Exercise scripts/orchestrator/stall-watch.sh (regime-cutover U621, standing orders 57 and 59; round 2 after verdict
U621-942e9a16, round 3 after verdict U621-b368fced, round 4 after verdict U621-4edab4b0), the schedule and the record
around `stall-check.py`: one tick runs
the checker beside the lever over a store with `<store>/progress` as the progress root, appends one `decisions.tsv` row
of phase `stall` per new stall and prints the checker's row on stdout, once per stall by a marker file
`<store>/progress/<unit>-stalled-<ts>` that is created under a `.partial` name before the row and renamed after it; a
unit without a file is a stall only once the deadline has passed since the tick that first saw it (the
`<unit>-seen-<ts>` marker); `--until-stall` exits 1 at the end of the first tick that records a new stall, every stall
of that tick recorded and printed; `reset <unit>` is one transaction ordered to fail safe (the clock, the progress file
moved aside by rename, only then the markers removed, the print at the end; a failure stops it with exit 3, nothing on
stdout and one stderr line naming the step and what was done) and takes no option; the row is appended through a
descriptor opened with O_NOFOLLOW; a failed checker, a failed record or a
failed read of a partial marker's age is printed on stderr and is exit 3. Every test runs the lever as a subprocess
over a scratch store under a scratch HOME with the real wall clock (the checker takes no injected clock through this
lever, so the progress lines and the `seen` markers are written relative to now); nothing reads the live store or the
real `~/.agents`.
"""

from __future__ import annotations

import errno
import hashlib
import os
import re
import select
import shutil
import subprocess
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/stall-watch.sh"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_stall-watch.sh"
INSTALLED_CHECKER = ROOT / "home/dot_local/bin/common/executable_stall-check.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
UNITS_HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote\n"
DECISIONS_HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"
REFUSED = "stall-watch.sh: refused: "
CONTINUES = "stall-watch.sh: stall-check.py exited 2; the loop continues"
TS = "%Y-%m-%dT%H:%M:%SZ"
HEAD = "a" * 40
WHY = (
    "stall-watch.sh tick (standing orders 57 and 59; U621): the coordinator stops the worker, resets the unit's "
    "markers (stall-watch.sh <store> reset {unit}) and starts a fresh one with the same consolidated brief"
)


def unit_row(unit: str, track: str = "feat", state: str = "in-flight", **cells: str) -> str:
    """One register row of the eight cells; the empty cells are the live table's for a unit without a pull request."""
    values = {"branch": "", "pr": "", "head_sha": "", "brief": f"briefs/{unit}-x.md", "note": "", **cells}
    return "\t".join((unit, track, state, *values.values())) + "\n"


def stamp(minutes_ago: int) -> str:
    """A progress line's clock, `minutes_ago` whole minutes before now, in the lines' own form."""
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).strftime(TS)


def seconds_since(ts: str) -> float:
    """Seconds from the timestamp `ts` (the lines' form) to now."""
    return (datetime.now(timezone.utc) - datetime.strptime(ts, TS).replace(tzinfo=timezone.utc)).total_seconds()


class StallWatchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # Resolved (on macOS the scratch directory is reached through a link): the lever prints `pwd -P` forms.
        self.dir = Path(self.temp.name).resolve()
        self.store = self.dir / "regime-store/dotfiles/regime-cutover"
        self.progress = self.store / "progress"
        self.progress.mkdir(parents=True)
        self.home = self.dir / "home"
        self.home.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}
        # A landed unit, a stalled one (40 minutes), a moving one (1 minute) and an in-flight sweep seat (no file).
        self.write_units(
            unit_row("U1", state="landed", pr="700", head_sha=HEAD),
            unit_row("U2"),
            unit_row("U3"),
            unit_row("U5", track="sweep", pr="701", head_sha=HEAD),
        )
        self.write_decisions()
        self.stalled_line = f"{stamp(40)} U2 start: brief read"
        self.write_progress("U2", self.stalled_line)
        self.write_progress("U3", f"{stamp(1)} U3: red tests pasted")

    def write_units(self, *rows: str, header: str = UNITS_HEADER) -> None:
        (self.store / "units.tsv").write_text(header + "".join(rows))

    def write_decisions(self, *rows: str) -> None:
        (self.store / "decisions.tsv").write_text(DECISIONS_HEADER + "".join(rows))

    def write_progress(self, unit: str, *lines: str) -> Path:
        path = self.progress / f"{unit}-progress.txt"
        path.write_text("\n".join(lines) + "\n")
        return path

    def write_seen(self, unit: str, ts: str) -> Path:
        """The `seen` marker of a unit first found in flight without a file at `ts`, as the lever would have made it."""
        for marker in self.progress.glob(f"{unit}-seen-*"):
            marker.unlink()
        path = self.progress / f"{unit}-seen-{ts}"
        path.touch()
        return path

    def run_lever(
        self,
        *args: str,
        lever: Path = LEVER,
        store: str | None = None,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess:
        argv = [str(lever)] + ([str(self.store)] if store is None else ([store] if store else [])) + list(args)
        return subprocess.run(
            argv, capture_output=True, text=True, check=False, timeout=120, env=env or self.env, cwd=self.dir
        )

    def start_lever(self, *args: str) -> subprocess.Popen:
        return subprocess.Popen(
            [str(LEVER), str(self.store), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.env,
            cwd=self.dir,
        )

    def fake_tool(self, name: str, body: str = "exit 3") -> dict[str, str]:
        """An environment whose PATH puts a `name` of the given body first."""
        bindir = self.dir / "fake"
        bindir.mkdir(exist_ok=True)
        (bindir / name).write_text(f"#!/bin/sh\n{body}\n")
        (bindir / name).chmod(0o755)
        return {**self.env, "PATH": f"{bindir}:{self.env['PATH']}"}

    def python_that_then_runs(self, swap: str) -> dict[str, str]:
        """An environment whose `python3` runs the real one and, after the checker's run, runs `swap` in the shell:
        the failure injection between the lever's preflight check of decisions.tsv and its append (round-1 P2)."""
        real = shutil.which("python3", path=os.environ["PATH"])
        self.assertIsNotNone(real, "the real python3")
        body = "\n".join(
            (
                f'"{real}" "$@"',
                "status=$?",
                'for arg in "$@"; do case "$arg" in */stall-check.py) ' + swap + " ;; esac; done",
                "exit $status",
            )
        )
        return self.fake_tool("python3", body)

    def decisions(self) -> list[list[str]]:
        """The record's rows after its header, each split into its cells."""
        lines = (self.store / "decisions.tsv").read_text().split("\n")
        self.assertEqual(lines[0] + "\n", DECISIONS_HEADER)
        self.assertEqual(lines[-1], "", "the record ends with a newline")
        return [line.split("\t") for line in lines[1:-1]]

    def markers(self) -> list[str]:
        """The `stalled` markers' names, partial ones included."""
        return sorted(path.name for path in self.progress.iterdir() if "-stalled-" in path.name)

    def seen(self) -> list[str]:
        """The `seen` markers' names."""
        return sorted(
            path.name for path in self.progress.iterdir() if "-seen-" in path.name and "-stalled-" not in path.name
        )

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

    def assert_row(self, line: str, unit: str, state: str, last: str) -> str:
        """One stdout row in the checker's form; the age cell is returned."""
        cells = line.split("\t")
        self.assertEqual(len(cells), 4, line)
        self.assertEqual((cells[0], cells[1], cells[3]), (unit, state, last))
        return cells[2]

    def assert_stalled_row(self, row: list[str], unit: str, age: str, last: str, deadline: int = 25) -> None:
        """One decisions row of a `stalled` unit, cell by cell (the clock cell is the tick's, judged by its form)."""
        self.assertEqual(len(row), 6, row)
        ts, phase, decision, why, evidence, result = row
        self.assertEqual(datetime.strptime(ts, TS).strftime(TS), ts)
        self.assertLess(seconds_since(ts), 120, "the row's clock is the tick's")
        self.assertEqual(phase, "stall")
        self.assertEqual(
            decision,
            f"{unit} stalled: the last progress line is {age} minutes old, past the {deadline}-minute deadline",
        )
        self.assertEqual(why, WHY.format(unit=unit))
        self.assertEqual(evidence, f"{self.progress}/{unit}-progress.txt last line: {last}")
        self.assertEqual(result, "open")

    def assert_no_file_row(self, row: list[str], unit: str, first_seen: str, deadline: int = 25) -> None:
        """One decisions row of a `no-file` unit, cell by cell."""
        self.assertEqual(len(row), 6, row)
        ts, phase, decision, why, evidence, result = row
        self.assertEqual(datetime.strptime(ts, TS).strftime(TS), ts)
        self.assertLess(seconds_since(ts), 120, "the row's clock is the tick's")
        self.assertEqual(phase, "stall")
        self.assertEqual(
            decision,
            f"{unit} stalled: no progress file {self.progress}/{unit}-progress.txt since first seen in flight at "
            f"{first_seen}, past the {deadline}-minute deadline",
        )
        self.assertEqual(why, WHY.format(unit=unit))
        self.assertEqual(
            evidence,
            f"stall-check.py row: {unit} no-file - -; first seen without a file at {first_seen} "
            f"(marker {self.progress}/{unit}-seen-{first_seen})",
        )
        self.assertEqual(result, "open")

    def assert_refused(self, run: subprocess.CompletedProcess, *reasons: str) -> None:
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(REFUSED), run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)

    def read_until(self, stream, needle: str, count: int, seconds: float) -> int:
        """Lines read from `stream` until `needle` has been seen `count` times or `seconds` have passed."""
        seen = 0
        deadline = time.monotonic() + seconds
        while seen < count:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            ready, _, _ = select.select([stream], [], [], remaining)
            if not ready:
                break
            line = stream.readline()
            if not line:
                break
            if line.rstrip("\n") == needle:
                seen += 1
        return seen

    def wait_for(self, condition, seconds: float = 30) -> None:
        """Poll `condition` until it holds or `seconds` have passed."""
        deadline = time.monotonic() + seconds
        while not condition():
            self.assertLess(time.monotonic(), deadline, "the condition did not hold in time")
            time.sleep(0.1)

    def test_a_stalled_unit_yields_one_decisions_row_and_one_stdout_line_not_two_on_the_next_tick(self) -> None:
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        rows = run.stdout.splitlines()
        self.assertEqual(len(rows), 1, run.stdout)
        age = self.assert_row(rows[0], "U2", "stalled", self.stalled_line)
        self.assertIn(age, ("40", "41"), "the line was written 40 minutes before setUp")
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"], "the final marker, no partial")
        self.assertEqual(self.seen(), [])
        # The next tick: the marker holds, nothing is appended and nothing is printed.
        before = (self.store / "decisions.tsv").read_bytes()
        again = self.run_lever("--once")
        self.assertEqual((again.returncode, again.stdout, again.stderr), (0, "", ""))
        self.assertEqual((self.store / "decisions.tsv").read_bytes(), before)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])
        # The worker moved again and stalled later: a later last line is a new stall, recorded once more.
        later = f"{stamp(30)} U2: item 2 done"
        self.write_progress("U2", self.stalled_line, later)
        third = self.run_lever("--once")
        self.assertEqual(third.returncode, 1, third.stderr)
        self.assertEqual(third.stderr, "")
        age = self.assert_row(third.stdout.rstrip("\n"), "U2", "stalled", later)
        rows = self.decisions()
        self.assertEqual(len(rows), 2)
        self.assert_stalled_row(rows[1], "U2", age, later)
        self.assertEqual(self.markers(), sorted([f"U2-stalled-{self.stalled_line[:20]}", f"U2-stalled-{later[:20]}"]))

    def test_a_unit_without_a_file_is_a_stall_only_after_the_deadline_since_it_was_first_seen(self) -> None:
        self.write_units(unit_row("U3"), unit_row("U4", track="dsh"))
        # The first tick that finds U4 in flight without a file records the sighting and reports nothing.
        run = self.run_lever("--once")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))
        self.assertEqual(self.decisions(), [])
        self.assertEqual(self.markers(), [])
        (seen,) = self.seen()
        first = seen[len("U4-seen-") :]
        self.assertEqual(datetime.strptime(first, TS).strftime(TS), first)
        self.assertLess(seconds_since(first), 60, "the first-seen time is the tick's clock")
        # A later tick before the deadline: the same sighting, still nothing.
        again = self.run_lever("--once")
        self.assertEqual((again.returncode, again.stdout, again.stderr), (0, "", ""))
        self.assertEqual((self.decisions(), self.markers(), self.seen()), ([], [], [seen]))
        # Twenty minutes after the sighting: still before the 25-minute deadline.
        self.write_seen("U4", stamp(20))
        early = self.run_lever("--once")
        self.assertEqual((early.returncode, early.stdout, early.stderr), (0, "", ""))
        self.assertEqual((self.decisions(), self.markers()), ([], []))
        # At the deadline: the stall is recorded, keyed by the first-seen time.
        first = stamp(25)
        self.write_seen("U4", first)
        late = self.run_lever("--once")
        self.assertEqual(late.returncode, 1, late.stderr)
        self.assertEqual((late.stdout, late.stderr), ("U4\tno-file\t-\t-\n", ""))
        (row,) = self.decisions()
        self.assert_no_file_row(row, "U4", first)
        self.assertEqual(self.markers(), [f"U4-stalled-seen-{first}"])
        self.assertEqual(self.seen(), [f"U4-seen-{first}"])
        # Once recorded, the next tick appends and prints nothing.
        once_more = self.run_lever("--once")
        self.assertEqual((once_more.returncode, once_more.stdout, once_more.stderr), (0, "", ""))
        self.assertEqual(len(self.decisions()), 1)
        # The file appears: the sighting is forgotten on that tick, the recorded stall's marker stays.
        self.write_progress("U4", f"{stamp(1)} U4 start: brief read")
        moving = self.run_lever("--once")
        self.assertEqual((moving.returncode, moving.stdout, moving.stderr), (0, "", ""))
        self.assertEqual((self.seen(), self.markers()), ([], [f"U4-stalled-seen-{first}"]))
        self.assertEqual(len(self.decisions()), 1)

    def test_reset_removes_the_markers_and_a_replacement_workers_stall_is_a_new_row(self) -> None:
        self.write_units(unit_row("U3"), unit_row("U4", track="dsh"))
        first = stamp(30)
        self.write_seen("U4", first)
        run = self.run_lever("--once")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (1, "U4\tno-file\t-\t-\n", ""))
        self.assertEqual(self.markers(), [f"U4-stalled-seen-{first}"])
        # Without a reset the permanent marker would hold: the replacement's silence is the same stall.
        held = self.run_lever("--once")
        self.assertEqual((held.returncode, held.stdout, held.stderr), (0, "", ""))
        # The coordinator resets the unit before the replacement is dispatched: both markers go, each printed.
        reset = self.run_lever("reset", "U4")
        self.assertEqual(
            (reset.returncode, reset.stdout, reset.stderr),
            (0, f"{self.progress}/U4-seen-{first}\n{self.progress}/U4-stalled-seen-{first}\n", ""),
        )
        self.assertEqual((self.markers(), self.seen()), ([], []))
        self.assertEqual(len(self.decisions()), 1, "reset touches no row")
        # A reset of a unit without markers removes and prints nothing.
        empty = self.run_lever("reset", "U4")
        self.assertEqual((empty.returncode, empty.stdout, empty.stderr), (0, "", ""))
        # The replacement's own silence: a new sighting on the next tick, a new stall at its deadline, a new row.
        fresh = self.run_lever("--once")
        self.assertEqual((fresh.returncode, fresh.stdout, fresh.stderr), (0, "", ""))
        (seen,) = self.seen()
        self.assertLess(seconds_since(seen[len("U4-seen-") :]), 60)
        second = stamp(26)
        self.assertNotEqual(second, first)
        self.write_seen("U4", second)
        later = self.run_lever("--once")
        self.assertEqual((later.returncode, later.stdout, later.stderr), (1, "U4\tno-file\t-\t-\n", ""))
        rows = self.decisions()
        self.assertEqual(len(rows), 2)
        self.assert_no_file_row(rows[0], "U4", first)
        self.assert_no_file_row(rows[1], "U4", second)
        self.assertEqual(self.markers(), [f"U4-stalled-seen-{second}"])
        # A reset removes a stalled unit's markers and a partial one as well.
        (self.progress / "U4-stalled-2026-01-01T00:00:00Z.partial").touch()
        full = self.run_lever("reset", "U4")
        self.assertEqual(
            (full.returncode, full.stdout, full.stderr),
            (
                0,
                f"{self.progress}/U4-seen-{second}\n{self.progress}/U4-stalled-2026-01-01T00:00:00Z.partial\n"
                f"{self.progress}/U4-stalled-seen-{second}\n",
                "",
            ),
        )
        self.assertEqual((self.markers(), self.seen()), ([], []))

    def test_until_stall_exits_1_on_the_first_new_stall_with_the_row_and_keeps_running_when_nothing_stalls(
        self,
    ) -> None:
        # A stall on the first tick: the loop ends with exit 1, the row on stdout, the row recorded.
        run = self.run_lever("--until-stall", "--interval-seconds", "1")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        age = self.assert_row(run.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])
        # Nothing stalls (the recorded stall holds, U3 moves, U4 was just seen without a file): the loop keeps
        # running tick after tick (the `seen` marker proves the first tick, the process alive 2.5 seconds later proves
        # the later ones) until TERM ends it through its trap, with nothing printed.
        self.write_units(unit_row("U2"), unit_row("U3"), unit_row("U4", track="dsh"))
        process = self.start_lever("--until-stall", "--interval-seconds", "1")
        with process:
            try:
                self.wait_for(lambda: bool(self.seen()))
                time.sleep(2.5)
                self.assertIsNone(process.poll(), "the loop is still running")
            finally:
                process.terminate()
                process.wait(timeout=30)
            quiet, noise = process.stdout.read(), process.stderr.read()
        self.assertEqual((process.returncode, quiet, noise), (143, "", ""))
        self.assertEqual(len(self.decisions()), 1)
        # A checker failure ends the loop with exit 3 (the plain loop would go on).
        self.write_units(unit_row("U2"), header="id\ttrack\tstate\n")
        failed = self.run_lever("--until-stall", "--interval-seconds", "1")
        self.assertEqual((failed.returncode, failed.stdout), (3, ""), failed.stderr)
        lines = failed.stderr.splitlines()
        self.assertEqual(len(lines), 2, failed.stderr)
        self.assertTrue(lines[0].startswith("stall-check.py: refused: "), lines[0])
        self.assertEqual(lines[1], CONTINUES)
        self.assertEqual(len(self.decisions()), 1)

    def test_two_watchers_started_concurrently_on_the_same_stall_write_one_row(self) -> None:
        marker = f"U2-stalled-{self.stalled_line[:20]}"
        for repetition in range(20):
            with self.subTest(repetition=repetition):
                self.write_decisions()
                for path in self.progress.glob("U2-stalled-*"):
                    path.unlink()
                first, second = self.start_lever("--once"), self.start_lever("--once")
                outputs = [process.communicate(timeout=120) for process in (first, second)]
                codes = sorted((first.returncode, second.returncode))
                self.assertEqual(codes, [0, 1], outputs)
                self.assertEqual([noise for _, noise in outputs], ["", ""])
                printed = [out for out, _ in outputs if out]
                self.assertEqual(len(printed), 1, outputs)
                age = self.assert_row(printed[0].rstrip("\n"), "U2", "stalled", self.stalled_line)
                (row,) = self.decisions()
                self.assert_stalled_row(row, "U2", age, self.stalled_line)
                self.assertEqual(self.markers(), [marker])

    def test_a_failed_append_is_printed_exits_3_and_leaves_no_final_marker(self) -> None:
        record = self.store / "decisions.tsv"
        header = record.read_bytes()
        # decisions.tsv swapped for a link after the preflight check: the O_NOFOLLOW open refuses it, the row goes
        # nowhere (the link's target keeps its header alone), the partial marker is removed.
        env = self.python_that_then_runs(
            f'mv "{record}" "{self.store}/decisions.real" && ln -s decisions.real "{record}"'
        )
        run = self.run_lever("--once", env=env)
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"stall-watch.sh: the row cannot be appended to {record} (it cannot be opened: "
            f"{os.strerror(errno.ELOOP)}); the stall of U2 is not recorded\n",
        )
        self.assertTrue(record.is_symlink())
        self.assertEqual((self.store / "decisions.real").read_bytes(), header)
        self.assertEqual((self.markers(), self.seen()), ([], []), "no final marker and no partial one")
        # The record put back: the next tick records the stall.
        record.unlink()
        (self.store / "decisions.real").rename(record)
        again = self.run_lever("--once")
        self.assertEqual(again.returncode, 1, again.stderr)
        self.assertEqual(again.stderr, "")
        age = self.assert_row(again.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])
        # Separately, decisions.tsv made read-only after the preflight check: the open fails, the same way.
        for path in self.progress.glob("U2-stalled-*"):
            path.unlink()
        self.write_decisions()
        self.addCleanup(record.chmod, 0o644)
        run = self.run_lever("--once", env=self.python_that_then_runs(f'chmod 444 "{record}"'))
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"stall-watch.sh: the row cannot be appended to {record} (it cannot be opened: "
            f"{os.strerror(errno.EACCES)}); the stall of U2 is not recorded\n",
        )
        self.assertEqual(record.read_bytes(), header)
        self.assertEqual(self.markers(), [])

    def test_a_partial_marker_older_than_one_interval_is_removed_and_the_stall_recorded_again(self) -> None:
        marker = self.progress / f"U2-stalled-{self.stalled_line[:20]}"
        partial = marker.with_name(marker.name + ".partial")
        # A watcher killed between its two writes two minutes ago: the stale partial marker is removed, said on
        # stderr, and the stall is recorded (again, when the dead watcher's row made it; here it did not).
        partial.touch()
        old = time.time() - 120
        os.utime(partial, (old, old))
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(
            run.stderr,
            f"stall-watch.sh: the partial marker {partial} was older than one interval (60 s); removed, the stall "
            "of U2 is recorded again\n",
        )
        age = self.assert_row(run.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [marker.name], "the final marker; the partial one is gone")
        # A partial marker younger than one interval is another watcher's record in progress: left alone, nothing
        # appended or printed.
        marker.unlink()
        partial.touch()
        before = (self.store / "decisions.tsv").read_bytes()
        young = self.run_lever("--once")
        self.assertEqual((young.returncode, young.stdout, young.stderr), (0, "", ""))
        self.assertEqual((self.store / "decisions.tsv").read_bytes(), before)
        self.assertEqual(self.markers(), [partial.name])
        # Under a shorter interval the same marker is stale once it is older than that interval.
        old = time.time() - 5
        os.utime(partial, (old, old))
        short = self.run_lever("--once", "--interval-seconds", "2")
        self.assertEqual(short.returncode, 1, short.stderr)
        self.assertEqual(
            short.stderr,
            f"stall-watch.sh: the partial marker {partial} was older than one interval (2 s); removed, the stall "
            "of U2 is recorded again\n",
        )
        self.assert_row(short.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        self.assertEqual(
            len(self.decisions()), 2, "the row appears twice, the accepted side of a kill between the writes"
        )
        self.assertEqual(self.markers(), [marker.name])

    def test_a_unit_with_a_fresh_line_yields_nothing(self) -> None:
        # Moving, done by the bare done line, landed and a sweep seat: no stall anywhere, nothing written.
        self.write_units(
            unit_row("U1", state="landed", pr="700", head_sha=HEAD),
            unit_row("U3"),
            unit_row("U4", track="dsh"),
            unit_row("U5", track="sweep", pr="701", head_sha=HEAD),
        )
        self.write_progress("U4", f"{stamp(90)} U4 start: brief read", f"done, head={HEAD}")
        before = self.listing()
        run = self.run_lever("--once")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))
        self.assertEqual(self.decisions(), [])
        self.assertEqual((self.markers(), self.seen()), ([], []))
        self.assertEqual(self.listing(), before, "the lever wrote nothing")
        # A longer deadline makes the 40-minute line of the default fixture moving as well.
        self.write_units(unit_row("U2"), unit_row("U3"))
        run = self.run_lever("--once", "--deadline-minutes", "45")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))
        self.assertEqual(self.decisions(), [])
        self.assertEqual((self.markers(), self.seen()), ([], []))

    def test_a_failed_stall_check_is_printed_and_does_not_stop_the_loop(self) -> None:
        # One tick: the register's header is wrong, so the checker refuses; its line passes through, the lever names
        # the exit, records nothing and, under --once, exits 3.
        self.write_units(unit_row("U2"), header="id\ttrack\tstate\n")
        before = self.listing()
        run = self.run_lever("--once")
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        lines = run.stderr.splitlines()
        self.assertEqual(len(lines), 2, run.stderr)
        self.assertTrue(lines[0].startswith("stall-check.py: refused: "), lines[0])
        self.assertEqual(lines[1], CONTINUES)
        self.assertEqual(self.listing(), before)
        # The loop: the same failing store every second; the second failure line proves the loop went on after the
        # first, then the process is ended by TERM, which ends the wait between ticks at once.
        process = self.start_lever("--interval-seconds", "1")
        with process:
            try:
                seen = self.read_until(process.stderr, CONTINUES, count=2, seconds=60)
            finally:
                process.terminate()
                process.wait(timeout=30)
            quiet = process.stdout.read()
        self.assertEqual(seen, 2, "two ticks each printed the checker's failure")
        self.assertEqual(process.returncode, 143, "TERM ends the loop through its trap")
        self.assertEqual(quiet, "")
        self.assertEqual(self.listing(), before)

    def test_a_malformed_file_beside_a_stall_is_printed_and_the_stall_is_still_recorded(self) -> None:
        self.write_progress("U3", "hello")
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 3, run.stderr)
        age = self.assert_row(run.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        lines = run.stderr.splitlines()
        self.assertEqual(lines[0], CONTINUES)
        self.assertTrue(lines[1].startswith("stall-watch.sh: U3 malformed: "), lines[1])
        self.assertEqual(len(lines), 2, run.stderr)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])

    def test_a_failed_clock_read_records_nothing_and_the_next_tick_records_the_stall(self) -> None:
        env = self.fake_tool("date")
        before = self.listing()
        run = self.run_lever("--once", env=env)
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertEqual(
            run.stderr, "stall-watch.sh: the clock cannot be read (date -u failed); the tick records nothing\n"
        )
        self.assertEqual(self.decisions(), [])
        self.assertEqual((self.markers(), self.seen()), ([], []), "no marker, so the next tick records the stall")
        self.assertEqual(self.listing(), before)
        again = self.run_lever("--once")
        self.assertEqual(again.returncode, 1, again.stderr)
        self.assertEqual(again.stderr, "")
        age = self.assert_row(again.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])

    def test_refusals_name_the_reason_and_write_nothing(self) -> None:
        link = self.dir / "link-store"
        link.symlink_to(self.store)
        linked = self.dir / "linked"
        linked.mkdir()
        shutil.copy(self.store / "units.tsv", linked / "units.tsv")
        (linked / "decisions.tsv").symlink_to(self.store / "decisions.tsv")
        (linked / "progress").mkdir()
        no_progress = self.dir / "no-progress"
        no_progress.mkdir()
        shutil.copy(self.store / "units.tsv", no_progress / "units.tsv")
        shutil.copy(self.store / "decisions.tsv", no_progress / "decisions.tsv")
        no_record = self.dir / "no-record"
        (no_record / "progress").mkdir(parents=True)
        shutil.copy(self.store / "units.tsv", no_record / "units.tsv")
        before = self.listing()
        cases = (
            ((), "", "a store path is needed"),
            ((str(self.store),), None, "one store, not two"),
            (("--deadline-minutes", "0"), None, "--deadline-minutes 0 is outside 1 to 1440"),
            (("--deadline-minutes", "1441"), None, "--deadline-minutes 1441 is outside 1 to 1440"),
            (("--deadline-minutes", "07"), None, "--deadline-minutes 07 is not 1 to 10 decimal digits"),
            (("--deadline-minutes", "abc"), None, "--deadline-minutes abc is not 1 to 10 decimal digits"),
            (("--deadline-minutes", "1" * 11), None, "is not 1 to 10 decimal digits"),
            (("--deadline-minutes",), None, "--deadline-minutes needs a value"),
            (("--interval-seconds", "86401"), None, "--interval-seconds 86401 is outside 1 to 86400"),
            (("--interval-seconds", "0"), None, "--interval-seconds 0 is outside 1 to 86400"),
            (("--bogus",), None, "unknown option --bogus"),
            (("--once", "--until-stall"), None, "--once and --until-stall are two ways to end; give one"),
            (("reset",), None, "reset needs the unit whose markers are removed"),
            (("reset", "u4"), None, "reset u4: not a unit id of the shape U<n> or U<n><letter>"),
            (("reset", "U4", "U5"), None, "reset takes one unit, not two (U4 and U5)"),
            (("reset", "U4", "--once"), None, "reset takes no option"),
            (("reset", "U4", "--until-stall"), None, "reset takes no option"),
            # Round 3 (verdict U621-b368fced P3 at :247): reset refuses every option, naming it, wherever it stands.
            (("reset", "U4", "--deadline-minutes", "5"), None, "reset takes no option (--deadline-minutes given)"),
            (("--interval-seconds", "5", "reset", "U4"), None, "reset takes no option (--interval-seconds given)"),
            (("--once", "x\ty"), None, "an argument holds a tab, a newline or a carriage return"),
            (("--once",), str(self.dir / "absent"), "is not a directory that can be entered"),
            (("--once",), str(no_record), "decisions.tsv is not a regular file"),
            (("--once",), str(linked), "decisions.tsv is not a regular file"),
            (("--once",), str(no_progress), "progress is not a directory"),
            (("reset", "U2"), str(no_progress), "progress is not a directory"),
        )
        for args, store, reason in cases:
            with self.subTest(args=args, store=store):
                self.assert_refused(self.run_lever(*args, store=store), reason)
        # A store reached through a link is entered and resolved: the refusal names nothing, the tick runs.
        run = self.run_lever("--once", "--deadline-minutes", "45", store=str(link))
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))
        self.assertEqual(self.listing(), before, "no refusal and no quiet tick wrote anything")

    def test_the_installed_layout_runs_the_checker_beside_it(self) -> None:
        bindir = self.home / ".local/bin/common"
        bindir.mkdir(parents=True)
        (self.home / ".agents").mkdir()
        shutil.copy2(MANIFEST, self.home / ".agents/agent-config.yaml")
        shutil.copy2(INSTALLED, bindir / "stall-watch.sh")
        # Without the checker beside it the lever refuses before any tick.
        self.assert_refused(
            self.run_lever("--once", lever=bindir / "stall-watch.sh"),
            f"no stall-check.py beside {bindir}/stall-watch.sh",
        )
        shutil.copy2(INSTALLED_CHECKER, bindir / "stall-check.py")
        run = self.run_lever("--once", lever=bindir / "stall-watch.sh")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        age = self.assert_row(run.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])

    def test_reset_archives_the_progress_file_and_the_replacements_first_tick_is_seen_not_a_stall(self) -> None:
        # Round 3 (verdict U621-b368fced P1 at :275): a reset that left the stale file in place made the replacement
        # stalled the moment the watcher restarted, before it could write a line.
        file = self.progress / "U2-progress.txt"
        previous = file.read_bytes()
        marker = f"U2-stalled-{self.stalled_line[:20]}"
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(self.markers(), [marker])
        # A failed clock read refuses the reset before anything is removed (standing order 21).
        failed = self.run_lever("reset", "U2", env=self.fake_tool("date"))
        self.assertEqual((failed.returncode, failed.stdout), (3, ""), failed.stderr)
        self.assertEqual(
            failed.stderr,
            f"stall-watch.sh: the clock cannot be read (date -u failed); the progress file {file} is not archived and "
            "no marker of U2 is removed\n",
        )
        self.assertEqual(file.read_bytes(), previous)
        self.assertEqual(self.markers(), [marker])
        # The reset: the marker goes and the file is moved aside under the reset's clock, each printed, nothing deleted.
        reset = self.run_lever("reset", "U2")
        self.assertEqual(reset.returncode, 0, reset.stderr)
        self.assertEqual(reset.stderr, "")
        lines = reset.stdout.splitlines()
        self.assertEqual(len(lines), 2, reset.stdout)
        self.assertEqual(lines[0], f"{self.progress}/{marker}")
        archived = Path(lines[1])
        self.assertEqual(archived.parent, self.progress)
        name = re.fullmatch(r"U2-progress\.(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\.txt", archived.name)
        self.assertIsNotNone(name, archived.name)
        self.assertLess(seconds_since(name.group(1)), 60, "the archive is named by the reset's clock")
        self.assertFalse(file.exists(), "the replacement has no file")
        self.assertEqual(archived.read_bytes(), previous, "the previous worker's lines are kept")
        self.assertEqual(
            sorted(path.name for path in self.progress.iterdir()), sorted([archived.name, "U3-progress.txt"])
        )
        self.assertEqual(len(self.decisions()), 1, "reset touches no row")
        # The replacement's first tick: no file, so the first-seen rule applies, a `seen` marker, no row, nothing
        # printed, exit 0 (at b368fced the old file's 40-minute line was a stall at once).
        fresh = self.run_lever("--once")
        self.assertEqual((fresh.returncode, fresh.stdout, fresh.stderr), (0, "", ""))
        (seen,) = self.seen()
        self.assertTrue(seen.startswith("U2-seen-"), seen)
        self.assertLess(seconds_since(seen[len("U2-seen-") :]), 60)
        self.assertEqual((self.markers(), len(self.decisions())), ([], 1))
        self.assertEqual(archived.read_bytes(), previous, "the archive is not the checker's file")
        # A reset when no file exists is quiet about the file: the `seen` marker alone is removed and printed.
        again = self.run_lever("reset", "U2")
        self.assertEqual((again.returncode, again.stdout, again.stderr), (0, f"{self.progress}/{seen}\n", ""))
        self.assertTrue(archived.exists(), "the archive is never deleted")

    def test_two_units_stalling_in_one_tick_both_get_rows_and_both_rows_are_printed_before_the_one_exit_1(self) -> None:
        # Round 3 (verdict U621-b368fced P1 at SKILL:26, f3): the tick records every new stall it finds, prints every
        # row, then exits 1 once; the coordinator handles each row.
        other = f"{stamp(35)} U3: item 1 done"
        self.write_progress("U3", other)
        run = self.run_lever("--until-stall", "--interval-seconds", "1")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        rows = run.stdout.splitlines()
        self.assertEqual(len(rows), 2, run.stdout)
        age_two = self.assert_row(rows[0], "U2", "stalled", self.stalled_line)
        age_three = self.assert_row(rows[1], "U3", "stalled", other)
        recorded = self.decisions()
        self.assertEqual(len(recorded), 2)
        self.assert_stalled_row(recorded[0], "U2", age_two, self.stalled_line)
        self.assert_stalled_row(recorded[1], "U3", age_three, other)
        self.assertEqual(self.markers(), sorted([f"U2-stalled-{self.stalled_line[:20]}", f"U3-stalled-{other[:20]}"]))
        # Both recorded: the next tick appends and prints nothing.
        again = self.run_lever("--once")
        self.assertEqual((again.returncode, again.stdout, again.stderr), (0, "", ""))
        self.assertEqual(len(self.decisions()), 2)
        # A stalled file and a no-file stall in one tick, under --once: two rows, two records, one exit 1.
        self.write_units(unit_row("U2"), unit_row("U3"), unit_row("U4", track="dsh"))
        first = stamp(30)
        self.write_seen("U4", first)
        later = f"{stamp(28)} U2: item 2 done"
        self.write_progress("U2", self.stalled_line, later)
        both = self.run_lever("--once")
        self.assertEqual(both.returncode, 1, both.stderr)
        self.assertEqual(both.stderr, "")
        rows = both.stdout.splitlines()
        self.assertEqual(len(rows), 2, both.stdout)
        age_two = self.assert_row(rows[0], "U2", "stalled", later)
        self.assertEqual(rows[1], "U4\tno-file\t-\t-")
        recorded = self.decisions()
        self.assertEqual(len(recorded), 4)
        self.assert_stalled_row(recorded[2], "U2", age_two, later)
        self.assert_no_file_row(recorded[3], "U4", first)

    def test_a_failed_partial_marker_age_read_is_exit_3_with_its_stderr_line_and_leaves_the_marker_for_the_next_tick(
        self,
    ) -> None:
        # Round 3 (verdict U621-b368fced P2 at :341): a failed `date -r` was read as a young marker, so a stale partial
        # marker could suppress its stall for ever. The wrapper fails `-r` alone and passes the tick's clock read
        # through to the real date.
        marker = self.progress / f"U2-stalled-{self.stalled_line[:20]}"
        partial = marker.with_name(marker.name + ".partial")
        partial.touch()
        old = time.time() - 120
        os.utime(partial, (old, old))
        real = shutil.which("date", path=os.environ["PATH"])
        self.assertIsNotNone(real, "the real date")
        env = self.fake_tool("date", f'for arg in "$@"; do case "$arg" in -r) exit 3 ;; esac; done\nexec "{real}" "$@"')
        complaint = (
            f"stall-watch.sh: the age of the partial marker {partial} cannot be read (date -r failed); it is left for "
            "the next tick and the stall of U2 is not recorded this tick\n"
        )
        before = self.listing()
        run = self.run_lever("--once", env=env)
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertEqual(run.stderr, complaint)
        self.assertEqual(self.decisions(), [])
        self.assertEqual(self.markers(), [partial.name], "the marker is left for the next tick")
        self.assertEqual(self.listing(), before, "nothing written, the marker untouched")
        # Under --until-stall the same failure ends the loop with exit 3 and no row.
        loop = self.run_lever("--until-stall", "--interval-seconds", "1", env=env)
        self.assertEqual((loop.returncode, loop.stdout, loop.stderr), (3, "", complaint))
        self.assertEqual(self.listing(), before)
        # The next tick with a working date reads the marker as stale, removes it and records the stall.
        again = self.run_lever("--once")
        self.assertEqual(again.returncode, 1, again.stderr)
        self.assertEqual(
            again.stderr,
            f"stall-watch.sh: the partial marker {partial} was older than one interval (60 s); removed, the stall "
            "of U2 is recorded again\n",
        )
        age = self.assert_row(again.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        (row,) = self.decisions()
        self.assert_stalled_row(row, "U2", age, self.stalled_line)
        self.assertEqual(self.markers(), [marker.name])

    def test_a_failed_archive_rename_is_exit_3_naming_it_and_leaves_the_file_and_the_markers_untouched(self) -> None:
        # Round 4 (verdict U621-4edab4b0 P2 at :314): at 4edab4b0 reset removed the markers before the rename, so a
        # failed move left the old file beside no marker and the next tick recorded the same stall a second time; now
        # the rename comes first and its failure stops the sequence with nothing done and nothing on stdout.
        file = self.progress / "U2-progress.txt"
        previous = file.read_bytes()
        marker = f"U2-stalled-{self.stalled_line[:20]}"
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(self.markers(), [marker])
        # The clock the test drives: a `date` wrapper on PATH prints one fixed clock, so the archive name is known and
        # the test pre-creates it (an archive name already taken is a failure of the rename).
        clock = "2026-01-01T00:00:00Z"
        env = self.fake_tool("date", f"echo {clock}")
        archive = self.progress / f"U2-progress.{clock}.txt"
        taken = "another reset's archive\n"
        archive.write_text(taken)
        before = self.listing()
        failed = self.run_lever("reset", "U2", env=env)
        self.assertEqual((failed.returncode, failed.stdout), (3, ""), failed.stderr)
        self.assertEqual(failed.stderr.count("\n"), 1, failed.stderr)
        self.assertEqual(
            failed.stderr,
            f"stall-watch.sh: the rename of the progress file {file} to {archive} failed: the archive name is taken; "
            "nothing is done (the file stands and no marker of U2 is removed)\n",
        )
        self.assertEqual(self.listing(), before, "nothing was written, moved or removed")
        self.assertEqual(file.read_bytes(), previous, "the progress file stands")
        self.assertEqual(archive.read_text(), taken, "the taken name is not overwritten")
        self.assertEqual(self.markers(), [marker], "the final marker stands")
        self.assertEqual(len(self.decisions()), 1)
        # The next tick after the failed reset: the final marker still guards the stall, so no second row (at 4edab4b0
        # the marker was already gone and the old file's line was recorded again).
        held = self.run_lever("--once")
        self.assertEqual((held.returncode, held.stdout, held.stderr), (0, "", ""))
        self.assertEqual(len(self.decisions()), 1, "the same stall is not recorded twice")
        # The coordinator fixes the store (the taken name moved aside, nothing deleted) and runs reset again: the
        # success case prints the removed markers in the order removed, then the archive line last, after every step.
        archive.rename(self.progress / f"U2-progress.{clock}.earlier.txt")
        seen = self.write_seen("U2", stamp(50))
        reset = self.run_lever("reset", "U2", env=env)
        self.assertEqual(
            (reset.returncode, reset.stdout, reset.stderr),
            (0, f"{seen}\n{self.progress}/{marker}\n{archive}\n", ""),
        )
        self.assertFalse(file.exists(), "the replacement has no file")
        self.assertEqual(archive.read_bytes(), previous, "the previous worker's lines are kept")
        self.assertEqual((self.markers(), self.seen()), ([], []))
        self.assertEqual(len(self.decisions()), 1, "reset touches no row")

    def test_a_failed_marker_removal_after_the_archive_is_exit_3_naming_the_marker_and_the_archive_which_stands(
        self,
    ) -> None:
        # Round 4 (verdict U621-4edab4b0 P2 at :314; the round brief's item 1): a marker removal that fails after the
        # archive stops the sequence there; the stderr line names the marker, the archive (which stands) and the markers
        # already removed, so the coordinator finishes by hand; nothing is on stdout.
        file = self.progress / "U2-progress.txt"
        previous = file.read_bytes()
        marker = f"U2-stalled-{self.stalled_line[:20]}"
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        seen = self.write_seen("U2", stamp(50))
        # A marker `rm` cannot remove: a directory under a partial marker's name, which the glob lists after the `seen`
        # marker and before the final one; the one injection that needs no wrapper.
        blocked = self.progress / "U2-stalled-2026-01-01T00:00:00Z.partial"
        blocked.mkdir()
        clock = "2026-02-02T00:00:00Z"
        env = self.fake_tool("date", f"echo {clock}")
        archive = self.progress / f"U2-progress.{clock}.txt"
        failed = self.run_lever("reset", "U2", env=env)
        self.assertEqual((failed.returncode, failed.stdout), (3, ""), failed.stderr)
        self.assertEqual(failed.stderr.count("\n"), 1, failed.stderr)
        self.assertEqual(
            failed.stderr,
            f"stall-watch.sh: the marker {blocked} cannot be removed; done before the failure: the progress file {file} "
            f"is archived as {archive}; the markers removed before it: {seen}; finish by hand and run reset U2 again\n",
        )
        self.assertFalse(file.exists(), "the archive was made before the markers")
        self.assertEqual(archive.read_bytes(), previous, "the archive stands")
        self.assertEqual(self.seen(), [], "the marker before the failure was removed")
        self.assertEqual(self.markers(), [blocked.name, marker], "the sequence stopped at the failure")
        self.assertEqual(len(self.decisions()), 1)
        # The coordinator finishes the named step by hand and runs reset again: no file now, so no archive line; the
        # final marker goes; exit 0; the archive is never deleted; the replacement's first tick is a sighting.
        blocked.rmdir()
        again = self.run_lever("reset", "U2", env=env)
        self.assertEqual((again.returncode, again.stdout, again.stderr), (0, f"{self.progress}/{marker}\n", ""))
        self.assertEqual((self.markers(), self.seen()), ([], []))
        self.assertEqual(archive.read_bytes(), previous)
        fresh = self.run_lever("--once")
        self.assertEqual((fresh.returncode, fresh.stdout, fresh.stderr), (0, "", ""))
        self.assertEqual((len(self.seen()), len(self.decisions())), (1, 1))
        # The clock is the first step even without a file: its failure is exit 3 naming it, nothing touched (the
        # listing is taken after the wrapper on PATH is rewritten, so only the store is compared).
        clockless_env = self.fake_tool("date")
        listing = self.listing()
        clockless = self.run_lever("reset", "U2", env=clockless_env)
        self.assertEqual((clockless.returncode, clockless.stdout), (3, ""), clockless.stderr)
        self.assertEqual(
            clockless.stderr,
            f"stall-watch.sh: the clock cannot be read (date -u failed); no marker of U2 is removed (there is no "
            f"progress file {file} to archive)\n",
        )
        self.assertEqual(self.listing(), listing, "nothing was touched")

    def test_the_deployed_twin_equals_the_source_and_hashes_to_its_pin(self) -> None:
        source = LEVER.read_bytes()
        self.assertEqual(INSTALLED.read_bytes(), source)
        self.assertTrue(INSTALLED.stat().st_mode & 0o111, "the generated copy is executable")
        self.assertTrue(LEVER.stat().st_mode & 0o111, "the source is executable")
        self.assertTrue(source.startswith(b"#!/usr/bin/env bash\n"))
        digest = hashlib.sha256(source).hexdigest()
        pins = [line for line in MANIFEST.read_text().splitlines() if line.startswith("      stall-watch.sh: ")]
        self.assertEqual(pins, [f"      stall-watch.sh: {digest}"])


if __name__ == "__main__":
    unittest.main()
