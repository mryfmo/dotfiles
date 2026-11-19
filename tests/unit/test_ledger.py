"""Exercise the sweep question of scripts/orchestrator/ledger.py (regime-cutover U147): `newest_sweep(unit, head)` is
the newest row by `(ts, line)` of the unit or a fix unit of it at the head whose verdict starts with the word `sweep`
(the advisory row of the AGENTS.md Audit sweep rule: pr `-`, head the swept sha), a sweep row is no audit row to the
three audit questions, a sweep row with a short head is a malformed store naming the line, and the CLI form
`ledger.py <store> sweep <unit> <head>` prints `<ts>\\t<unit>\\t<verifier>\\t<evidence>` or `none`. Since round 4
(Codex thread 4457544811) only the exact row of the rule answers: pr `-`, verifier `security-audit-skill <pin>` (the pin
8 or more lowercase hex), evidence whose first `;`-field is a relative `sweeps/<path>.json` without `..`; any other
`sweep` row of the unit is a malformed store naming the line and the field, never "no sweep row". The daily question
(U597 round 4): `read_daily` and `Daily.newest_within(now, max_age)` over the store's `daily-sweeps.tsv` with the
ledger's strictness (a missing file None, a malformed row naming the line and the field), and the CLI form `ledger.py
<store> daily <max-age-seconds>` printing `<ts>\\t<head_sha>\\t<verifier>\\t<evidence>` of the newest row within the
window against the clock, or `none`; round 5: the window is bounded above by 60 seconds, so a row dated further in
the future does not count (and is not refused as malformed); round 7: a cell holding a control byte is Malformed to
both parsers, naming the line and the field; round 8: a carriage return is such a byte wherever it stands, never
stripped, so a row ends in LF alone; round 9: the daily row has its own grammar, the exact fields `ledger-row.py
daily` writes (the verifier's seat, run and daily task, the evidence's six fields with the validators' PASS words, the
two digest prefixes and the recording time), so a row of a unit's sweep shape is Malformed naming the field."""

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
READER = ROOT / "scripts/orchestrator/ledger.py"
HEADER = "ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence\n"
A, B = "a" * 40, "b" * 40
SKILL = "security-audit-skill c1c8a8c1"


def load_reader():
    """The reader imported from beside the levers, as rounds-check.py and audit-carry.py import it (registered in
    sys.modules first: dataclasses resolve the class namespace through it)."""
    spec = importlib.util.spec_from_file_location("ledger", READER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["ledger"] = module
    spec.loader.exec_module(module)
    return module


def row(ts, unit, pr, head, verdict, verifier="pr-audit.sh", evidence="https://github.com/acme/widgets/pull/7"):
    return "\t".join((ts, unit, pr, head, verdict, verifier, evidence)) + "\n"


def sweep(ts, head, unit="U7", verdict="sweep"):
    return row(ts, unit, "-", head, verdict, SKILL, f"sweeps/{unit}-{head[:8]}.json")


class LedgerSweepTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Path(self.temp.name) / "regime-cutover"
        self.store.mkdir()
        self.ledger_file = self.store / "ledger.tsv"
        self.reader = load_reader()

    def ledger(self, *rows):
        self.ledger_file.write_text(HEADER + "".join(rows))
        return self.reader.read_ledger(str(self.ledger_file))

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(READER), str(self.store), *args],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )

    def test_newest_sweep_is_the_newest_sweep_row_of_the_unit_and_its_fix_units_at_the_head(self):
        read = self.ledger(
            row("2026-10-30T01:00:00Z", "U7", "7", A, "correct (findings=0)"),  # line 2
            row("2026-10-30T02:00:00Z", "U7", "7", A, "incorrect (round 1)", evidence="class=status"),  # line 3
            row("2026-10-30T02:30:00Z", "U7", "7", A, "carried", evidence=f"carried {B} {A} {'f' * 64}"),  # line 4
            row("2026-10-30T02:40:00Z", "U7", "7", A, "-"),  # line 5
            row("2026-10-30T09:00:00Z", "U7", "-", A, "sweeping"),  # line 6: not the word
            sweep("2026-10-30T05:00:00Z", B),  # line 7: another head
            sweep("2026-10-30T03:00:00Z", A),  # line 8
            sweep("2026-10-30T04:00:00Z", A, unit="U7b"),  # line 9: a fix unit, the latest ts
            sweep("2026-10-30T04:00:00Z", A, verdict="sweep (advisory; 2 findings)"),  # line 10: equal ts, later line
            sweep("2026-10-30T06:00:00Z", A, unit="U8"),  # line 11: another unit
            sweep("2026-10-30T07:00:00Z", A, unit="U70"),  # line 12: a unit whose id starts with U7
        )
        self.assertEqual(
            [r.sweep for r in read.rows], [False, False, False, False, False, True, True, True, True, True, True]
        )
        self.assertEqual(read.newest_sweep("U7", A).line, 10, "the later line at an equal ts")
        self.assertEqual(read.newest_sweep("U7", A).verdict, "sweep (advisory; 2 findings)")
        self.assertEqual(read.newest_sweep("U7", B).line, 7)
        self.assertEqual(read.newest_sweep("U7b", A).line, 9, "U7b's own rows (and its own fix units) only")
        self.assertEqual(read.newest_sweep("U8", A).line, 11)
        self.assertIsNone(read.newest_sweep("U8", B))
        self.assertIsNone(read.newest_sweep("U9", A))
        self.assertIsNone(read.newest_sweep("U7", "c" * 40))

    def test_a_sweep_row_is_no_audit_row(self):
        read = self.ledger(
            row("2026-10-30T01:00:00Z", "U7", "7", A, "correct (findings=0)"),  # line 2
            sweep("2026-10-30T03:00:00Z", A),  # line 3
            sweep("2026-10-30T04:00:00Z", B, unit="U7b"),  # line 4
        )
        self.assertEqual([r.line for r in read.audits("U7")], [2])
        self.assertIsNone(read.rows[1].word)
        self.assertEqual(read.already_audited("U7", A).line, 2, "the audit row, not the newer sweep row")
        self.assertIsNone(read.already_audited("U7", B), "a sweep row at B is no audit of B")
        self.assertIsNone(read.newest_audit_at_another_head("U7", A), "the sweep row at B is no carry source")
        self.assertEqual(read.newest_for_head("7", A).line, 2, "a sweep row's pr is `-`, so no pull request has it")
        only_sweep = self.ledger(sweep("2026-10-30T03:00:00Z", A))
        self.assertEqual(only_sweep.audits("U7"), [])
        self.assertIsNone(only_sweep.already_audited("U7", A))
        self.assertEqual(only_sweep.newest_sweep("U7", A).line, 2)

    def test_a_sweep_row_with_a_short_head_is_malformed_naming_the_line(self):
        read = self.ledger(
            row("2026-10-30T01:00:00Z", "U7", "7", A, "correct (findings=0)"),
            sweep("2026-10-30T03:00:00Z", A[:7]),  # line 3
        )
        with self.assertRaises(self.reader.Malformed) as caught:
            read.newest_sweep("U7", A)
        self.assertEqual(
            str(caught.exception), f"{self.ledger_file}:3: the head_sha of a sweep row is not 40 hex: {A[:7]!r}"
        )
        self.assertEqual(
            [r.line for r in read.audits("U7")], [2], "the short head is a sweep row, so no audit question raises"
        )
        self.assertEqual(read.newest_for_head("7", A).line, 2)

    def test_a_sweep_row_that_is_not_the_exact_row_of_the_rule_is_malformed_naming_the_field(self):
        """Round 4 (Codex thread 4457544811: a row written by hand with verifier `coordinator` admitted the merge): a
        `sweep` row of the unit whose pr is not `-`, whose verifier does not begin with `security-audit-skill <pin>`
        or whose evidence's first `;`-field is not a relative `sweeps/<path>.json` free of `..` is Malformed naming
        the line and the field, at the asked head or another (as the short-head rule); the exact row answers, with a
        note after the pin word or after a `;` in the evidence too, and the audit questions still ignore every one."""
        ts = "2026-10-30T03:00:00Z"
        pr_text = "the pr of a sweep row is not '-': '7'"
        verifier_text = (
            "the verifier of a sweep row does not begin with 'security-audit-skill <pin>' "
            "(the pin 8 or more lowercase hex): {!r}"
        )
        evidence_text = (
            "the evidence of a sweep row does not name a findings file sweeps/<path>.json under the store "
            "(no '..' or empty component): {!r}"
        )
        for name, bad, field in (
            ("pr 7", row(ts, "U7", "7", A, "sweep", SKILL, "sweeps/U7-x.json"), pr_text),
            (
                "verifier coordinator",
                row(ts, "U7", "-", A, "sweep", "coordinator", "sweeps/U7-x.json"),
                verifier_text.format("coordinator"),
            ),
            (
                "the skill alone",
                row(ts, "U7", "-", A, "sweep", "security-audit-skill", "sweeps/U7-x.json"),
                verifier_text.format("security-audit-skill"),
            ),
            (
                "a short pin",
                row(ts, "U7", "-", A, "sweep", "security-audit-skill c1c8a8", "sweeps/U7-x.json"),
                verifier_text.format("security-audit-skill c1c8a8"),
            ),
            (
                "an upper-case pin",
                row(ts, "U7", "-", A, "sweep", "security-audit-skill C1C8A8C1", "sweeps/U7-x.json"),
                verifier_text.format("security-audit-skill C1C8A8C1"),
            ),
            (
                "evidence under verdicts/",
                row(ts, "U7", "-", A, "sweep", SKILL, "verdicts/x.md"),
                evidence_text.format("verdicts/x.md"),
            ),
            (
                "evidence ../x.json",
                row(ts, "U7", "-", A, "sweep", SKILL, "../x.json"),
                evidence_text.format("../x.json"),
            ),
            (
                "evidence sweeps/../x.json",
                row(ts, "U7", "-", A, "sweep", SKILL, "sweeps/../x.json"),
                evidence_text.format("sweeps/../x.json"),
            ),
            (
                "an absolute path",
                row(ts, "U7", "-", A, "sweep", SKILL, "/sweeps/x.json"),
                evidence_text.format("/sweeps/x.json"),
            ),
            ("sweeps alone", row(ts, "U7", "-", A, "sweep", SKILL, "sweeps"), evidence_text.format("sweeps")),
            (
                "a .md under sweeps",
                row(ts, "U7", "-", A, "sweep", SKILL, "sweeps/x.md"),
                evidence_text.format("sweeps/x.md"),
            ),
            (
                "an empty component",
                row(ts, "U7", "-", A, "sweep", SKILL, "sweeps//x.json"),
                evidence_text.format("sweeps//x.json"),
            ),
            (
                "the bad row at another head",
                row(ts, "U7", "-", B, "sweep", "coordinator", "sweeps/U7-x.json"),
                verifier_text.format("coordinator"),
            ),
        ):
            with self.subTest(name):
                read = self.ledger(row("2026-10-30T01:00:00Z", "U7", "7", A, "correct (findings=0)"), bad)  # line 3
                with self.assertRaises(self.reader.Malformed) as caught:
                    read.newest_sweep("U7", A)
                self.assertEqual(str(caught.exception), f"{self.ledger_file}:3: {field}")
                self.assertEqual([r.line for r in read.audits("U7")], [2], "no audit question reads the row")
                self.assertIsNone(read.newest_sweep("U8", A), "another unit's question never sees U7's row")
        full = "c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
        read = self.ledger(
            row(
                ts,
                "U7",
                "-",
                A,
                "sweep",
                f"security-audit-skill {full} (installed 2026-11-03)",
                " sweeps/U7-aaaaaaaa.json ; 2 findings",
            ),
            sweep("2026-10-30T02:00:00Z", A),
        )
        found = read.newest_sweep("U7", A)
        self.assertEqual((found.line, found.sweep_pin, found.sweep_evidence_path), (2, full, "sweeps/U7-aaaaaaaa.json"))
        self.assertEqual(read.rows[1].sweep_pin, "c1c8a8c1")
        self.assertIsNone(read.rows[0].sweep_fault())

    def test_the_cli_prints_the_four_columns_or_none_and_exits_2_on_a_malformed_store(self):
        self.ledger(
            row("2026-10-30T01:00:00Z", "U7", "7", A, "correct (findings=0)"),
            sweep("2026-10-30T03:00:00Z", A),
            sweep("2026-10-30T04:00:00Z", A, unit="U7b"),
        )
        run = self.cli("sweep", "U7", A)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(run.stdout, f"2026-10-30T04:00:00Z\tU7b\t{SKILL}\tsweeps/U7b-{A[:8]}.json\n")
        run = self.cli("sweep", "U7", B)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""))
        run = self.cli("sweep", "U8", A)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""))
        # the audit questions do not change: the verdict form still names the correct row, never the sweep row
        run = self.cli("verdict", "7", A)
        self.assertEqual(
            run.stdout, "2026-10-30T01:00:00Z\tU7\tcorrect (findings=0)\thttps://github.com/acme/widgets/pull/7\n"
        )
        self.ledger(row("2026-10-30T01:00:00Z", "U7", "7", A, "correct"), sweep("2026-10-30T03:00:00Z", A[:7]))
        run = self.cli("sweep", "U7", A)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "")
        self.assertEqual(
            run.stderr, f"ledger: {self.ledger_file}:3: the head_sha of a sweep row is not 40 hex: {A[:7]!r}\n"
        )
        # round 4: a hand-written row is a malformed store naming the field, and an audit row by the coordinator is no
        # sweep row at all, so a store holding only that is `none`
        self.ledger(row("2026-10-30T03:00:00Z", "U7", "-", A, "sweep", "coordinator", "sweeps/U7-x.json"))
        run = self.cli("sweep", "U7", A)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"ledger: {self.ledger_file}:2: the verifier of a sweep row does not begin with "
            "'security-audit-skill <pin>' (the pin 8 or more lowercase hex): 'coordinator'\n",
        )
        self.ledger(row("2026-10-30T01:00:00Z", "U7", "7", A, "correct (findings=0)", verifier="coordinator"))
        run = self.cli("sweep", "U7", A)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""))
        self.ledger_file.write_text("ts\tunit\n")
        run = self.cli("sweep", "U7", A)
        self.assertEqual(run.returncode, 2)
        self.assertIn(f"{self.ledger_file}:1: the header is", run.stderr)
        for args in (("sweep", "U7", A[:8]), ("sweep", "U7b", A), ("sweep", "7", A)):
            with self.subTest(args=args):
                run = self.cli(*args)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("error:", run.stderr)
        run = self.cli("-h")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("sweep", run.stdout)
        self.assertIn("{verdict,carry-source,sweep,daily}", run.stdout)


DAILY_HEADER = "ts\thead_sha\tverifier\tevidence\n"
C = "c" * 40


# The daily row's own grammar (U597 round 9): the fixture rows are the writer's shape, the verifier naming the seat,
# the run and the task of the ts's day, the evidence its six fields; the two digest prefixes are the manifest's of
# round 8 (any 8 hex is the reader's; pr-merge.sh compares them with the manifest's pins).
DAILY_DIGESTS = "e85f232e 2eb280bd"
DAILY_FINDINGS = "sweeps/daily-2026-11-19/findings.json"


def daily_verifier(day, seat="sweep-3", run="170"):
    """The verifier of a daily row as ledger-row.py daily composes it, the task the daily id of `day`."""
    return f"{SKILL} (full audit mode on the srt worker seat {seat}, run-{run}; TASK daily-{day})"


def daily_evidence(path=DAILY_FINDINGS, count=0, digests=DAILY_DIGESTS, recorded="2026-11-19T10:05:00Z"):
    """The evidence of a daily row as ledger-row.py daily writes it: its six `; `-separated fields."""
    return (
        f"{path}; {count} findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS; "
        f"validators sha256 {digests}; recorded {recorded}"
    )


def daily(ts, head, verifier=None, evidence=None):
    """One row of `daily-sweeps.tsv` as ledger-row.py daily writes it (round 9: the task of the ts's day)."""
    if verifier is None:
        verifier = daily_verifier(ts[:10])
    if evidence is None:
        evidence = daily_evidence()
    return "\t".join((ts, head, verifier, evidence)) + "\n"


def ago(seconds):
    """A ts `seconds` before now, in the store's form."""
    return (datetime.now(timezone.utc) - timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


class LedgerDailyTest(unittest.TestCase):
    """U597 round 4: the daily sweep of main's head, the standing control a head outside every sweep class rests on,
    read from the store's `daily-sweeps.tsv` with the ledger's strictness and chosen by its ts against the window."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store = Path(self.temp.name) / "regime-cutover"
        self.store.mkdir()
        self.daily_file = self.store / "daily-sweeps.tsv"
        self.reader = load_reader()

    def write(self, *rows, header=DAILY_HEADER):
        self.daily_file.write_text(header + "".join(rows))
        return self.reader.read_daily(str(self.daily_file))

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(READER), str(self.store), *args],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )

    def test_newest_within_is_the_newest_row_by_ts_within_the_window_and_a_missing_file_is_none(self):
        now = datetime(2026, 11, 19, 12, 0, 0)
        read = self.write(
            daily("2026-11-18T11:00:00Z", A),  # line 2: 25 hours before now
            daily("2026-11-19T10:00:00Z", B),  # line 3: 2 hours
            daily("2026-11-19T09:00:00Z", A),  # line 4: 3 hours
            daily("2026-11-19T10:00:00Z", C),  # line 5: 2 hours, the later line at the equal ts
        )
        self.assertEqual(read.name, str(self.daily_file))
        self.assertEqual([row.line for row in read.rows], [2, 3, 4, 5])
        self.assertEqual((read.rows[0].ts_text, read.rows[0].head_sha), ("2026-11-18T11:00:00Z", A))
        self.assertEqual(read.rows[0].sweep_pin, "c1c8a8c1")
        self.assertEqual(read.rows[0].sweep_evidence_path, "sweeps/daily-2026-11-19/findings.json")
        newest = read.newest_within(now, 86400)
        self.assertEqual((newest.line, newest.head_sha), (5, C), "the later line at an equal ts")
        self.assertEqual(read.newest_within(now, 7200).line, 5, "a row at the window's edge is within it")
        self.assertIsNone(read.newest_within(now, 7199), "a row one second older than the window is not")
        self.assertIsNone(read.newest_within(now, 3600))
        self.assertEqual(
            read.newest_within(datetime(2026, 11, 18, 12, 0, 0), 3600).line,
            2,
            "the rows dated 22 hours ahead of the clock are not within the window (round 5); the past row at its edge is",
        )
        only_past = self.write(daily("2026-11-18T11:00:00Z", A), daily("2026-11-17T11:00:00Z", B))
        self.assertEqual(only_past.newest_within(datetime(2026, 11, 18, 12, 0, 0), 3600).line, 2, "the window moves")
        self.assertIsNone(only_past.newest_within(datetime(2026, 11, 18, 12, 0, 1), 3600), "one second past it")
        read = self.write(
            daily("2026-11-18T11:00:00Z", A),
            daily("2026-11-19T10:00:00Z", B),
            daily("2026-11-19T09:00:00Z", A),
            daily("2026-11-19T10:00:00Z", C),
        )
        self.assertIsNone(self.reader.read_daily(str(self.store / "absent.tsv")), "no file is None, not a refusal")
        header_alone = self.write()
        self.assertEqual(header_alone.rows, ())
        self.assertIsNone(header_alone.newest_within(now, 86400))
        # round 8: a file with CR LF ends is Malformed at its header; the CR is never stripped
        with self.assertRaises(self.reader.Malformed) as caught:
            self.write(
                daily("2026-11-19T10:00:00Z", B).replace("\n", "\r\n"), header=DAILY_HEADER.replace("\n", "\r\n")
            )
        self.assertTrue(str(caught.exception).startswith(f"{self.daily_file}:1: the header is "), caught.exception)

    def test_a_row_dated_more_than_60_seconds_ahead_is_not_within_the_window(self):
        """Round 5 (verdict U597-1b3c4b1d P2 at ledger.py:316): round 4's window had a floor alone, so a row dated in
        the future waived per-head sweeps until a day after its ts. The window is `now - max_age <= ts <= now + 60 s`:
        a row 60 seconds ahead counts, one 61 seconds ahead does not, and such a row is not malformed (the file still
        parses, an older row within the window still answers); the CLI agrees against the clock."""
        self.assertEqual(self.reader.DAILY_FUTURE_SLACK, 60)
        now = datetime(2026, 11, 19, 12, 0, 0)
        read = self.write(
            daily("2026-11-19T11:00:00Z", A),  # line 2: an hour before now
            daily("2026-11-19T12:01:00Z", B),  # line 3: 60 seconds ahead, within
            daily("2026-11-19T12:01:01Z", C),  # line 4: 61 seconds ahead, not within
            daily("2026-11-20T12:00:00Z", C),  # line 5: a day ahead, not within
        )
        self.assertEqual([row.line for row in read.rows], [2, 3, 4, 5], "a future row is data, not malformed")
        self.assertEqual((read.newest_within(now, 86400).line, read.newest_within(now, 86400).head_sha), (3, B))
        self.assertEqual(read.newest_within(now, 86400).ts_text, "2026-11-19T12:01:00Z")
        future_only = self.write(daily("2026-11-19T12:01:01Z", C), daily("2026-11-20T12:00:00Z", C))
        self.assertIsNone(future_only.newest_within(now, 86400), "future rows alone count for nothing")
        self.assertEqual(future_only.newest_within(datetime(2026, 11, 19, 12, 0, 1), 86400).line, 2, "the clock moves")
        self.assertEqual(future_only.newest_within(datetime(2026, 11, 20, 12, 0, 0), 86400).line, 3)
        # the CLI against the clock: a row a day ahead is none, a row 30 seconds ahead stands, an hour-old row beside
        # a day-ahead row is the answer
        day_ahead = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.write(daily(day_ahead, C))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""), "a day ahead is not within")
        soon = (datetime.now(timezone.utc) + timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.write(daily(soon, B))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, daily(soon, B), ""), "30 seconds ahead stands")
        hour_old = ago(3600)
        self.write(daily(hour_old, A), daily(day_ahead, C))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, daily(hour_old, A), ""))

    def test_an_unpadded_ts_is_malformed_to_the_daily_reader_and_the_ledger_alike(self):
        """U597 round 6 (verdict U597-10d46fe0 P3 at ledger.py:343): `strptime` under `%m`, `%d`, `%H`, `%M` and `%S`
        reads one digit as well as two, so the daily reader accepted `2026-11-9T4:5:6Z` under a grammar that spells
        two digits in every field. `timestamp` holds the cell to `TS_SHAPE` first, the one grammar of both files: an
        unpadded field in a daily row or in a ledger row is Malformed naming the line and the form, the padded ts
        still parses, and the CLI exits 2 naming the line."""
        name = str(self.daily_file)
        self.assertEqual(self.reader.TS_SHAPE.pattern, r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
        self.assertEqual(self.reader.timestamp("2026-11-09T04:05:06Z"), datetime(2026, 11, 9, 4, 5, 6))
        for value in (
            "2026-11-9T4:5:6Z",
            "2026-1-09T04:05:06Z",
            "2026-11-9T04:05:06Z",
            "2026-11-09T4:05:06Z",
            "2026-11-09T04:5:06Z",
            "2026-11-09T04:05:6Z",
            "026-11-09T04:05:06Z",
            "2026-11-09T04:05:06",
            "2026-11-09t04:05:06Z",
            "２０２６-11-09T04:05:06Z",
        ):
            with self.subTest(value):
                self.assertIsNone(self.reader.timestamp(value))
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.write(daily(value, A))
                self.assertEqual(str(caught.exception), f"{name}:2: the ts {value!r} is not YYYY-MM-DDThh:mm:ssZ")
                ledger_text = HEADER + "\t".join((value, "U7", "7", A, "pushed", "coordinator", "x")) + "\n"
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.reader.parse_ledger("ledger.tsv", ledger_text)
                self.assertEqual(str(caught.exception), f"ledger.tsv:2: the ts {value!r} is not YYYY-MM-DDThh:mm:ssZ")
        # the CLI: a malformed store naming the line, never "none" and never the padded row beside it
        self.daily_file.write_text(DAILY_HEADER + daily(ago(3600), A) + daily("2026-11-9T4:5:6Z", B))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"{name}:3: the ts '2026-11-9T4:5:6Z' is not YYYY-MM-DDThh:mm:ssZ", run.stderr)

    def test_a_cell_holding_a_control_byte_is_malformed_to_both_parsers_naming_the_line_and_the_field(self):
        """U597 round 7 (verdict U597-301eba2e P2 at ledger.py:361): a NUL in a daily row's evidence path was data to the
        reader, and bash's `$(...)` drops a NUL when pr-merge.sh captures the row, so the lever would have checked
        another file than the one the row names. `CONTROL` (`\\x00` to `\\x1f`, `\\x7f`) in any cell of either file is
        Malformed naming the line, the column and the character: a NUL in the evidence path, a `\\x01` in the verifier,
        a DEL in the head, a carriage return inside the ts (and a trailing one too, round 8), an escape in a
        ledger row's unit; the same text without the byte parses; the CLI exits 2 naming the line, never `none` and
        never the row beside it; and the writer's test holds its own rule to this one."""
        name = str(self.daily_file)
        self.assertEqual(self.reader.CONTROL.pattern, r"[\x00-\x1f\x7f]")
        ts = "2026-11-19T10:00:00Z"
        for case, text, message in (
            (
                "a NUL in the evidence path",
                daily(ts, A, evidence="sweeps/daily-2026-11-19/find\x00ings.json; 0 findings"),
                f"{name}:2: column 4 (evidence) holds a control character U+0000; no cell holds one",
            ),
            (
                "a \\x01 in the verifier",
                daily(ts, A, verifier=SKILL + " (\x01)"),
                f"{name}:2: column 3 (verifier) holds a control character U+0001; no cell holds one",
            ),
            (
                "a DEL in the head",
                daily(ts, A[:-1] + "\x7f"),
                f"{name}:2: column 2 (head_sha) holds a control character U+007F",
            ),
            (
                "a carriage return inside the ts",
                daily(ts + "\r", A),
                f"{name}:2: column 1 (ts) holds a control character U+000D",
            ),
            (
                "a NUL in a second row",
                daily(ts, A) + daily(ts, B, evidence="sweeps/x/y.json\x00"),
                f"{name}:3: column 4 (evidence) holds a control character U+0000",
            ),
        ):
            with self.subTest(case):
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.write(text)
                self.assertEqual(str(caught.exception)[: len(message)], message)
        # round 8: a trailing carriage return is a control byte of the last cell, never the line's end
        with self.assertRaises(self.reader.Malformed) as caught:
            self.write(daily(ts, A).rstrip("\n") + "\r\n")
        self.assertTrue(
            str(caught.exception).startswith(f"{name}:2: column 4 (evidence) holds a control character U+000D"),
            caught.exception,
        )
        # the ledger's parser, the same rule
        for case, line, message in (
            (
                "a NUL in the evidence",
                "\t".join((ts, "U7", "7", A, "pushed", "coordinator", "x\x00y")) + "\n",
                "ledger.tsv:2: column 7 (evidence) holds a control character U+0000; no cell holds one",
            ),
            (
                "an escape in the unit",
                "\t".join((ts, "U7\x1b", "7", A, "pushed", "coordinator", "x")) + "\n",
                "ledger.tsv:2: column 2 (unit) holds a control character U+001B; no cell holds one",
            ),
            (
                "a vertical tab in the verdict",
                "\t".join((ts, "U7", "7", A, "correct\x0b", "pr-audit.sh", "x")) + "\n",
                "ledger.tsv:2: column 5 (verdict) holds a control character U+000B; no cell holds one",
            ),
        ):
            with self.subTest(case):
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.reader.parse_ledger("ledger.tsv", HEADER + line)
                self.assertEqual(str(caught.exception), message)
        self.assertEqual(
            len(
                self.reader.parse_ledger(
                    "ledger.tsv", HEADER + "\t".join((ts, "U7", "7", A, "pushed", "c", "x")) + "\n"
                ).rows
            ),
            1,
        )
        # the CLI: a malformed store naming the line, never `none` and never the clean row beside it
        self.daily_file.write_text(
            DAILY_HEADER
            + daily(ago(3600), A)
            + daily(ago(600), B, evidence="sweeps/daily-2026-11-19/find\x00ings.json")
        )
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"{name}:3: column 4 (evidence) holds a control character U+0000", run.stderr)

    def test_a_carriage_return_is_a_control_byte_never_stripped_so_a_row_ends_in_lf_alone(self):
        """U597 round 8 (verdict U597-a28e4793 P3 at ledger.py:373): round 7's parsers stripped every trailing
        carriage return before the cells were checked, so a row ending in CR CR LF carried an extra control byte
        before a valid-looking terminator and parsed. A carriage return is a control character wherever it stands:
        a daily row ending in CR CR LF and one ending in CR LF are each Malformed naming line 2, the evidence column
        and U+000D, to the parser and to the CLI (exit 2, never `none`), as is a ledger row ending either way; a
        header ending in CR LF is Malformed at line 1; the same rows ending in LF alone parse."""
        ts = "2026-11-19T10:00:00Z"
        name = str(self.daily_file)
        plain = daily(ts, A)
        for case, ending in (("CR CR LF", "\r\r\n"), ("CR LF", "\r\n")):
            with self.subTest(case):
                text = plain.rstrip("\n") + ending
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.reader.parse_daily(name, DAILY_HEADER + text)
                self.assertEqual(
                    str(caught.exception),
                    f"{name}:2: column 4 (evidence) holds a control character U+000D; no cell holds one",
                )
                self.daily_file.write_text(DAILY_HEADER + text, newline="")
                run = self.cli("daily", "86400")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(f"{name}:2: column 4 (evidence) holds a control character U+000D", run.stderr)
                self.assertNotIn("none", run.stdout)
                # the ledger's parser, the same rule, naming its last column
                ledger_line = row(ts, "U7", "7", A, "pushed", "coordinator", "x").rstrip("\n") + ending
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.reader.parse_ledger("ledger.tsv", HEADER + ledger_line)
                self.assertEqual(
                    str(caught.exception),
                    "ledger.tsv:2: column 7 (evidence) holds a control character U+000D; no cell holds one",
                )
        # a header ending in CR LF is Malformed at line 1, before any row
        with self.assertRaises(self.reader.Malformed) as caught:
            self.reader.parse_daily(name, DAILY_HEADER.rstrip("\n") + "\r\n" + plain)
        self.assertTrue(str(caught.exception).startswith(f"{name}:1: the header is "), caught.exception)
        # the rows ending in LF alone parse
        self.assertEqual(len(self.reader.parse_daily(name, DAILY_HEADER + plain).rows), 1)
        self.assertEqual(
            len(
                self.reader.parse_ledger(
                    "ledger.tsv", HEADER + row(ts, "U7", "7", A, "pushed", "coordinator", "x")
                ).rows
            ),
            1,
        )
        # the parsers strip nothing from a line before the cells are checked
        source = READER.read_text()
        self.assertNotIn('rstrip("\\r")', source, "no carriage return is stripped (round 8)")
        self.assertEqual(source.count('fields = line.split("\\t")'), 2, "both parsers split the line as it is")

    def test_a_malformed_daily_file_is_malformed_naming_the_line_and_the_field(self):
        ts = "2026-11-19T10:00:00Z"
        name = str(self.daily_file)
        verifier_text = (
            "the verifier of a daily sweep row does not begin with 'security-audit-skill <pin>' "
            "(the pin 8 or more lowercase hex): {!r}"
        )
        evidence_text = (
            "the evidence of a daily sweep row does not name a findings file sweeps/<path>.json under the store "
            "(no '..' or empty component): {!r}"
        )
        for case, header, rows, message in (
            (
                "a wrong header",
                "ts\thead\n",
                (daily(ts, A),),
                f"{name}:1: the header is 'ts\\thead', not 'ts\\thead_sha\\tverifier\\tevidence'",
            ),
            ("the ledger's header", HEADER, (daily(ts, A),), f"{name}:1: the header is"),
            ("an empty file", "", (), f"{name}:1: the header is '', not"),
            ("three columns", DAILY_HEADER, ("\t".join((ts, A, SKILL)) + "\n",), f"{name}:2: 3 columns, not 4"),
            ("five columns", DAILY_HEADER, (daily(ts, A).rstrip("\n") + "\tx\n",), f"{name}:2: 5 columns, not 4"),
            (
                "hour 25",
                DAILY_HEADER,
                (daily("2026-11-19T25:00:00Z", A),),
                f"{name}:2: the ts '2026-11-19T25:00:00Z' is not YYYY-MM-DDThh:mm:ssZ",
            ),
            (
                "a date without its time",
                DAILY_HEADER,
                (daily("2026-11-19", A),),
                f"{name}:2: the ts '2026-11-19' is not",
            ),
            ("an empty ts", DAILY_HEADER, (daily("", A),), f"{name}:2: the ts '' is not"),
            ("an empty head", DAILY_HEADER, (daily(ts, ""),), f"{name}:2: column 2 (head_sha) is empty"),
            (
                "an empty verifier",
                DAILY_HEADER,
                (daily(ts, A, verifier=""),),
                f"{name}:2: column 3 (verifier) is empty",
            ),
            (
                "an empty evidence",
                DAILY_HEADER,
                (daily(ts, A, evidence=""),),
                f"{name}:2: column 4 (evidence) is empty",
            ),
            (
                "a short head",
                DAILY_HEADER,
                (daily(ts, A[:8]),),
                f"{name}:2: the head_sha of a daily sweep row is not 40 hex: {A[:8]!r}",
            ),
            (
                "verifier coordinator",
                DAILY_HEADER,
                (daily(ts, A, verifier="coordinator"),),
                f"{name}:2: {verifier_text.format('coordinator')}",
            ),
            (
                "a short pin",
                DAILY_HEADER,
                (daily(ts, A, verifier="security-audit-skill c1c8a8"),),
                f"{name}:2: {verifier_text.format('security-audit-skill c1c8a8')}",
            ),
            (
                "evidence under verdicts/",
                DAILY_HEADER,
                (daily(ts, A, evidence="verdicts/x.md"),),
                f"{name}:2: {evidence_text.format('verdicts/x.md')}",
            ),
            (
                "evidence with ..",
                DAILY_HEADER,
                (daily(ts, A, evidence="sweeps/../x.json"),),
                f"{name}:2: {evidence_text.format('sweeps/../x.json')}",
            ),
            (
                "a malformed third row",
                DAILY_HEADER,
                (daily(ts, A), daily(ts, B), "garbage\n"),
                f"{name}:4: 1 columns, not 4",
            ),
        ):
            with self.subTest(case):
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.write(*rows, header=header)
                self.assertIn(message, str(caught.exception))
        self.daily_file.write_bytes(
            DAILY_HEADER.encode() + b"2026-11-19T10:00:00Z\t" + A.encode() + b"\t\xff\tsweeps/x.json\n"
        )
        with self.assertRaises(self.reader.Malformed) as caught:
            self.reader.read_daily(str(self.daily_file))
        self.assertIn(f"{name}: not UTF-8", str(caught.exception))
        if os.geteuid() != 0:
            self.write(daily(ts, A))
            self.daily_file.chmod(0)
            with self.assertRaises(self.reader.Malformed) as caught:
                self.reader.read_daily(str(self.daily_file))
            self.assertIn(f"{name}: cannot read:", str(caught.exception))
            self.daily_file.chmod(0o600)
        # the writer's own row is the exact row (round 9: a note after the pin word or a padded path no longer is;
        # test_a_row_of_a_unit_s_sweep_shape_is_malformed_to_the_daily_reader_and_the_writer_s_row_parses)
        read = self.write(daily(ts, A, evidence=daily_evidence("sweeps/d/findings.json", count=2)))
        self.assertEqual(
            (read.rows[0].sweep_pin, read.rows[0].sweep_evidence_path), ("c1c8a8c1", "sweeps/d/findings.json")
        )

    def test_a_row_of_a_unit_s_sweep_shape_is_malformed_to_the_daily_reader_and_the_writer_s_row_parses(self):
        """U597 round 9 (verdict U597-c37800e3 P2 at ledger.py:393): the daily reader applied the sweep row's grammar
        alone, so a recent row of a unit's shape, `TASK U9` with a pinned verifier and an existing findings path,
        qualified as the day's sweep of main's head with no daily task and no validator result. The daily row has its
        own grammar, the exact fields `ledger-row.py daily` writes: the verifier's seat, run and `TASK
        daily-<YYYY-MM-DD>` (its day the ts's UTC day or the day before it), and the evidence's six `; `-separated
        fields, the findings file unpadded, `<n> findings`, the two validators' PASS words, `validators sha256 <8 hex>
        <8 hex>` and `recorded <ts>`. A `TASK U9` row, the pinned skill alone, a note after the pin, a seat of two
        words, a task day two days before or after the ts or no calendar day, two or seven evidence fields, a padded
        path, a count that is no number, another word than PASS, the two validators swapped, the round-8 `validators
        pass` word, a digest of seven, upper-case or one hex, and a recorded time off the form are each Malformed
        naming the line and the field, to the parser and to the CLI (exit 2, never `none` and never the row beside
        it); the writer's row parses and exposes its fields, under the ts's day and under the day before."""
        name = str(self.daily_file)
        ts = "2026-11-19T10:00:00Z"
        verifier_form = "security-audit-skill <pin> (full audit mode on the srt worker seat <seat>, run-<n>; TASK daily-<YYYY-MM-DD>)"
        unit_shaped = f"{SKILL} (full audit mode on the srt worker seat sweep-3, run-170; TASK U9)"
        evidence_form = (
            "sweeps/<path>.json; <n> findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS; "
            "validators sha256 <8 hex> <8 hex>; recorded <ts>"
        )
        good = daily_evidence()
        for case, text, message in (
            (
                "TASK U9",
                daily(ts, A, verifier=unit_shaped),
                f"{name}:2: the verifier of a daily sweep row is not {verifier_form!r} (the daily dispatch's task alone,"
                f" a unit id never): {unit_shaped!r}",
            ),
            (
                "the pinned skill alone",
                daily(ts, A, verifier=SKILL),
                f"{name}:2: the verifier of a daily sweep row is not",
            ),
            (
                "a note after the pin",
                daily(ts, A, verifier=f"{SKILL} (seat sweep-3, run-170)"),
                f"{name}:2: the verifier of a daily sweep row is not",
            ),
            (
                "a seat of two words",
                daily(ts, A, verifier=daily_verifier("2026-11-19", seat="sweep 3")),
                f"{name}:2: the verifier of a daily sweep row is not",
            ),
            (
                "a task day two days before the ts",
                daily(ts, A, verifier=daily_verifier("2026-11-17")),
                f"{name}:2: the TASK day daily-2026-11-17 of a daily sweep row is neither the UTC day of its ts {ts} nor"
                " the day before it",
            ),
            (
                "a task day after the ts",
                daily(ts, A, verifier=daily_verifier("2026-11-20")),
                f"{name}:2: the TASK day daily-2026-11-20 of a daily sweep row is neither the UTC day of its ts",
            ),
            (
                "a task day no calendar holds",
                daily(ts, A, verifier=daily_verifier("2026-13-45")),
                f"{name}:2: the TASK day of a daily sweep row is no calendar day: daily-2026-13-45",
            ),
            (
                "two evidence fields",
                daily(ts, A, evidence=f"{DAILY_FINDINGS}; 0 findings"),
                f"{name}:2: the evidence of a daily sweep row has 2 '; '-separated fields, not 6 ({evidence_form!r}):"
                f" '{DAILY_FINDINGS}; 0 findings'",
            ),
            (
                "seven evidence fields",
                daily(ts, A, evidence=good + "; note"),
                f"{name}:2: the evidence of a daily sweep row has 7 '; '-separated fields, not 6",
            ),
            (
                "a padded path",
                daily(ts, A, evidence=" " + good),
                f"{name}:2: field 1 of the evidence of a daily sweep row, the findings file, is padded with spaces:"
                f" ' {DAILY_FINDINGS}'",
            ),
            (
                "a count that is no number",
                daily(ts, A, evidence=good.replace("0 findings", "no findings")),
                f"{name}:2: field 2 of the evidence of a daily sweep row is not '<n> findings': 'no findings'",
            ),
            (
                "a count with a leading zero",
                daily(ts, A, evidence=good.replace("0 findings", "01 findings")),
                f"{name}:2: field 2 of the evidence of a daily sweep row is not '<n> findings': '01 findings'",
            ),
            (
                "another word than PASS",
                daily(ts, A, evidence=good.replace("validate-findings.cjs PASS", "validate-findings.cjs FAIL")),
                f"{name}:2: field 3 of the evidence of a daily sweep row is not 'validate-findings.cjs PASS':"
                " 'validate-findings.cjs FAIL'",
            ),
            (
                "the validators swapped",
                daily(
                    ts,
                    A,
                    evidence=good.replace(
                        "validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS",
                        "validate-coverage-ledger.cjs PASS; validate-findings.cjs PASS",
                    ),
                ),
                f"{name}:2: field 3 of the evidence of a daily sweep row is not 'validate-findings.cjs PASS':"
                " 'validate-coverage-ledger.cjs PASS'",
            ),
            (
                "the coverage word lower-case",
                daily(
                    ts,
                    A,
                    evidence=good.replace("validate-coverage-ledger.cjs PASS", "validate-coverage-ledger.cjs pass"),
                ),
                f"{name}:2: field 4 of the evidence of a daily sweep row is not 'validate-coverage-ledger.cjs PASS'",
            ),
            (
                "the round-8 validators pass word",
                daily(ts, A, evidence=good.replace(f"validators sha256 {DAILY_DIGESTS}", "validators pass")),
                f"{name}:2: field 5 of the evidence of a daily sweep row is not 'validators sha256 <8 hex> <8 hex>'",
            ),
            (
                "a digest of seven hex",
                daily(ts, A, evidence=daily_evidence(digests="e85f232 2eb280bd")),
                f"{name}:2: field 5 of the evidence of a daily sweep row is not 'validators sha256 <8 hex> <8 hex>'",
            ),
            (
                "a digest of upper-case hex",
                daily(ts, A, evidence=daily_evidence(digests="E85F232E 2eb280bd")),
                f"{name}:2: field 5 of the evidence of a daily sweep row is not",
            ),
            (
                "one digest",
                daily(ts, A, evidence=daily_evidence(digests="e85f232e")),
                f"{name}:2: field 5 of the evidence of a daily sweep row is not",
            ),
            (
                "a recorded time off the form",
                daily(ts, A, evidence=daily_evidence(recorded="2026-11-19 10:05:00")),
                f"{name}:2: field 6 of the evidence of a daily sweep row is not 'recorded <YYYY-MM-DDThh:mm:ssZ>':"
                " 'recorded 2026-11-19 10:05:00'",
            ),
            (
                "a recorded time of hour 25",
                daily(ts, A, evidence=daily_evidence(recorded="2026-11-19T25:00:00Z")),
                f"{name}:2: field 6 of the evidence of a daily sweep row is not 'recorded <YYYY-MM-DDThh:mm:ssZ>'",
            ),
            (
                "another word than recorded",
                daily(ts, A, evidence=good.replace("recorded 2026-11-19T10:05:00Z", "written 2026-11-19T10:05:00Z")),
                f"{name}:2: field 6 of the evidence of a daily sweep row is not 'recorded <YYYY-MM-DDThh:mm:ssZ>':"
                " 'written 2026-11-19T10:05:00Z'",
            ),
            (
                "a unit-shaped third row beside two good ones",
                daily(ts, A) + daily(ts, B) + daily(ts, A, verifier=unit_shaped),
                f"{name}:4: the verifier of a daily sweep row is not",
            ),
        ):
            with self.subTest(case):
                with self.assertRaises(self.reader.Malformed) as caught:
                    self.write(text)
                self.assertIn(message, str(caught.exception))
        # the CLI: a unit-shaped row beside a good one is exit 2 naming the line, never `none` and never the good row
        self.daily_file.write_text(DAILY_HEADER + daily(ago(3600), A) + daily(ago(600), B, verifier=unit_shaped))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"ledger: {name}:3: the verifier of a daily sweep row is not", run.stderr)
        # the writer's row parses and exposes its fields, under the ts's day and under the day before (a sweep that
        # crossed midnight keeps the id it was dispatched under)
        for day in ("2026-11-19", "2026-11-18"):
            with self.subTest(day=day):
                read = self.write(
                    daily(
                        ts,
                        A,
                        verifier=daily_verifier(day, seat="sweep-3", run="170"),
                        evidence=daily_evidence(count=3, recorded="2026-11-19T10:07:00Z"),
                    )
                )
                row = read.rows[0]
                self.assertEqual((row.sweep_pin, row.sweep_evidence_path), ("c1c8a8c1", DAILY_FINDINGS))
                self.assertEqual((row.seat, row.run, row.task_day), ("sweep-3", "170", day))
                self.assertEqual(row.validator_digests, ("e85f232e", "2eb280bd"))
                self.assertEqual(row.recorded, datetime(2026, 11, 19, 10, 7, 0))
                self.assertEqual(read.newest_within(datetime(2026, 11, 19, 12, 0, 0), 86400).line, 2)
        # a row of another shape exposes None for the fields it lacks, so no caller reads a field that is not there
        row = self.reader.DailyRow(datetime(2026, 11, 19, 10, 0, 0), A, SKILL, "sweeps/x.json", 2, ts)
        self.assertEqual((row.seat, row.run, row.task_day, row.validator_digests, row.recorded), (None,) * 5)
        # the grammar is stated once in the reader
        self.assertEqual(self.reader.DAILY_FIELDS, 6)
        self.assertEqual(self.reader.DAILY_SEPARATOR, "; ")
        self.assertEqual(self.reader.DAILY_PASSES, ("validate-findings.cjs PASS", "validate-coverage-ledger.cjs PASS"))
        self.assertEqual(
            self.reader.DAILY_VERIFIER.pattern,
            r"^security-audit-skill ([0-9a-f]{8,}) \(full audit mode on the srt worker seat (\S+), run-(0|[1-9][0-9]*); "
            r"TASK daily-([0-9]{4}-[0-9]{2}-[0-9]{2})\)$",
        )
        self.assertEqual(self.reader.DAILY_DIGESTS.pattern, r"^validators sha256 ([0-9a-f]{8}) ([0-9a-f]{8})$")
        source = READER.read_text()
        self.assertIn("            fault = daily_fields_fault(fields[2], fields[3], at)\n", source)

    def test_the_cli_prints_the_newest_row_within_the_window_or_none_and_exits_2_on_a_malformed_file(self):
        one_hour, two_hours, day_and_more = ago(3600), ago(7200), ago(25 * 3600)
        self.write(daily(day_and_more, A), daily(two_hours, B), daily(one_hour, C))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(run.stdout, daily(one_hour, C))
        run = self.cli("daily", "5400")
        self.assertEqual(run.stdout, daily(one_hour, C), "the two-hour row is outside a 90-minute window")
        run = self.cli("daily", "1800")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""), "no row within 30 minutes")
        self.write(daily(day_and_more, A))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""), "25 hours is outside one day")
        self.daily_file.unlink()
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""), "no file is none")
        self.daily_file.write_text(DAILY_HEADER + daily(one_hour, A) + "garbage\n")
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr, f"ledger: {self.daily_file}:3: 1 columns, not 4\n")
        self.daily_file.write_text(DAILY_HEADER + daily(one_hour, A, verifier="coordinator"))
        run = self.cli("daily", "86400")
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn(f"ledger: {self.daily_file}:2: the verifier of a daily sweep row does not begin with", run.stderr)
        # the ledger's own questions never read the daily file, and the daily question never reads the ledger
        (self.store / "ledger.tsv").write_text(HEADER + row("2026-10-30T01:00:00Z", "U7", "7", A, "correct"))
        run = self.cli("sweep", "U7", A)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "none\n", ""))
        (self.store / "ledger.tsv").write_text("ts\tunit\n")
        self.write(daily(one_hour, A))
        run = self.cli("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, daily(one_hour, A), ""))
        for args in (
            ("daily",),
            ("daily", "0"),
            ("daily", "-1"),
            ("daily", "x"),
            ("daily", "86400", "x"),
            ("daily", "1.5"),
        ):
            with self.subTest(args=args):
                run = self.cli(*args)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("error:", run.stderr)
