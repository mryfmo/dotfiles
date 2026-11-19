"""Exercise scripts/orchestrator/stall-watch.sh (regime-cutover U621, standing orders 57 and 59), the schedule and the
record around `stall-check.py`: one tick runs the checker beside the lever over a store with `<store>/progress` as the
progress root, appends one `decisions.tsv` row of phase `stall` per new `stalled` or `no-file` unit and prints the
checker's row on stdout, once per stall by a marker file `<store>/progress/<unit>-stalled-<ts>`; a failed checker or a
failed record is printed on stderr and the loop continues. Every test runs the lever as a subprocess over a scratch
store under a scratch HOME with the real wall clock (the checker takes no injected clock through this lever, so the
progress lines are written relative to now); nothing reads the live store or the real `~/.agents`.
"""

from __future__ import annotations

import hashlib
import os
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


def unit_row(unit: str, track: str = "feat", state: str = "in-flight", **cells: str) -> str:
    """One register row of the eight cells; the empty cells are the live table's for a unit without a pull request."""
    values = {"branch": "", "pr": "", "head_sha": "", "brief": f"briefs/{unit}-x.md", "note": "", **cells}
    return "\t".join((unit, track, state, *values.values())) + "\n"


def stamp(minutes_ago: int) -> str:
    """A progress line's clock, `minutes_ago` whole minutes before now, in the lines' own form."""
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).strftime(TS)


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

    def fake_tool(self, name: str, body: str = "exit 3") -> dict[str, str]:
        """An environment whose PATH puts a failing `name` first."""
        bindir = self.dir / "fake"
        bindir.mkdir(exist_ok=True)
        (bindir / name).write_text(f"#!/bin/sh\n{body}\n")
        (bindir / name).chmod(0o755)
        return {**self.env, "PATH": f"{bindir}:{self.env['PATH']}"}

    def decisions(self) -> list[list[str]]:
        """The record's rows after its header, each split into its cells."""
        lines = (self.store / "decisions.tsv").read_text().split("\n")
        self.assertEqual(lines[0] + "\n", DECISIONS_HEADER)
        self.assertEqual(lines[-1], "", "the record ends with a newline")
        return [line.split("\t") for line in lines[1:-1]]

    def markers(self) -> list[str]:
        return sorted(path.name for path in self.progress.iterdir() if "-stalled-" in path.name)

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

    def assert_refused(self, run: subprocess.CompletedProcess, *reasons: str) -> None:
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(REFUSED), run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)

    def test_a_stalled_unit_yields_one_decisions_row_and_one_stdout_line_not_two_on_the_next_tick(self) -> None:
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        rows = run.stdout.splitlines()
        self.assertEqual(len(rows), 1, run.stdout)
        age = self.assert_row(rows[0], "U2", "stalled", self.stalled_line)
        self.assertIn(age, ("40", "41"), "the line was written 40 minutes before setUp")
        (row,) = self.decisions()
        self.assertEqual(len(row), 6, row)
        ts, phase, decision, why, evidence, result = row
        self.assertEqual(datetime.strptime(ts, TS).strftime(TS), ts)
        self.assertEqual(phase, "stall")
        self.assertTrue(decision.startswith("U2 stalled: "), decision)
        self.assertIn(f"the last progress line is {age} minutes old, past the 25-minute deadline", decision)
        self.assertIn("stall-watch.sh", why)
        self.assertIn("starts a fresh one with the same consolidated brief", why)
        self.assertEqual(evidence, f"{self.progress}/U2-progress.txt last line: {self.stalled_line}")
        self.assertEqual(result, "open")
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])
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
        self.assert_row(third.stdout.rstrip("\n"), "U2", "stalled", later)
        self.assertEqual([row[2][:12] for row in self.decisions()], ["U2 stalled: ", "U2 stalled: "])
        self.assertEqual(self.markers(), sorted([f"U2-stalled-{self.stalled_line[:20]}", f"U2-stalled-{later[:20]}"]))

    def test_a_unit_without_a_progress_file_is_a_no_file_stall_recorded_once(self) -> None:
        self.write_units(unit_row("U3"), unit_row("U4", track="dsh"))
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 1, run.stderr)
        self.assertEqual(run.stderr, "")
        self.assertEqual(run.stdout, "U4\tno-file\t-\t-\n")
        (row,) = self.decisions()
        self.assertEqual(row[1], "stall")
        self.assertIn(f"U4 stalled: no progress file {self.progress}/U4-progress.txt since dispatch", row[2])
        self.assertEqual(row[4], "stall-check.py row: U4 no-file - -")
        self.assertEqual(self.markers(), ["U4-stalled-none"])
        again = self.run_lever("--once")
        self.assertEqual((again.returncode, again.stdout, again.stderr), (0, "", ""))
        self.assertEqual(len(self.decisions()), 1)

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
        self.assertEqual(self.markers(), [])
        self.assertEqual(self.listing(), before, "the lever wrote nothing")
        # A longer deadline makes the 40-minute line of the default fixture moving as well.
        self.write_units(unit_row("U2"), unit_row("U3"))
        run = self.run_lever("--once", "--deadline-minutes", "45")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "", ""))
        self.assertEqual(self.decisions(), [])

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
        process = subprocess.Popen(
            [str(LEVER), str(self.store), "--interval-seconds", "1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=self.env,
            cwd=self.dir,
        )
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

    def test_a_malformed_file_beside_a_stall_is_printed_and_the_stall_is_still_recorded(self) -> None:
        self.write_progress("U3", "hello")
        run = self.run_lever("--once")
        self.assertEqual(run.returncode, 3, run.stderr)
        self.assert_row(run.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        lines = run.stderr.splitlines()
        self.assertEqual(lines[0], CONTINUES)
        self.assertTrue(lines[1].startswith("stall-watch.sh: U3 malformed: "), lines[1])
        self.assertEqual(len(lines), 2, run.stderr)
        self.assertEqual([row[2][:12] for row in self.decisions()], ["U2 stalled: "])
        self.assertEqual(self.markers(), [f"U2-stalled-{self.stalled_line[:20]}"])

    def test_a_failed_clock_read_records_nothing_and_the_next_tick_records_the_stall(self) -> None:
        run = self.run_lever("--once", env=self.fake_tool("date"))
        self.assertEqual((run.returncode, run.stdout), (3, ""), run.stderr)
        self.assertEqual(
            run.stderr, "stall-watch.sh: the clock cannot be read (date -u failed); the stall of U2 is not recorded\n"
        )
        self.assertEqual(self.decisions(), [])
        self.assertEqual(self.markers(), [], "the marker is removed, so the next tick records the stall")
        again = self.run_lever("--once")
        self.assertEqual(again.returncode, 1, again.stderr)
        self.assert_row(again.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        self.assertEqual(len(self.decisions()), 1)

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
            (("--once", "x\ty"), None, "an argument holds a tab, a newline or a carriage return"),
            (("--once",), str(self.dir / "absent"), "is not a directory that can be entered"),
            (("--once",), str(no_record), "decisions.tsv is not a regular file"),
            (("--once",), str(linked), "decisions.tsv is not a regular file"),
            (("--once",), str(no_progress), "progress is not a directory"),
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
        self.assert_row(run.stdout.rstrip("\n"), "U2", "stalled", self.stalled_line)
        self.assertEqual(len(self.decisions()), 1)

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
