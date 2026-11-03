"""Exercise the sweep question of scripts/orchestrator/ledger.py (regime-cutover U147): `newest_sweep(unit, head)` is
the newest row by `(ts, line)` of the unit or a fix unit of it at the head whose verdict starts with the word `sweep`
(the advisory row of the AGENTS.md Audit sweep rule: pr `-`, head the swept sha), a sweep row is no audit row to the
three audit questions, a sweep row with a short head is a malformed store naming the line, and the CLI form
`ledger.py <store> sweep <unit> <head>` prints `<ts>\\t<unit>\\t<verifier>\\t<evidence>` or `none`."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
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
        self.assertIn("{verdict,carry-source,sweep}", run.stdout)
