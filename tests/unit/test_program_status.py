"""Exercise scripts/orchestrator/program-status.py (regime-cutover U497), the lever that prints the operator's state
report of a program store in standing order 56's shape, as a subprocess under `python3 -I` over a scratch store: the
report byte for byte in English and with `--ja`, the three state words each from a fixture, a fake `stall-check.py`
beside a copy of the lever, the absent-lever column, every header refusal and the self pin refusal of an altered copy."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/program-status.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
NOW = "2026-11-12T07:00:00Z"

TESTS_HEADER = "id\tuse_case\tsource\tkind\thost\tcommand\texpected\tobserved\tverdict\tts\n"
UNITS_HEADER = "id\ttrack\tstate\tbranch\tpr\thead_sha\tbrief\tnote\n"
DECISIONS_HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"
GATES_HEADER = "| id | gate | moment | options | default | result |\n"
STALL_HEADER = "unit\tstate\tage_minutes\tlast_line\n"


def test_row(row_id, kind, verdict, command="uv run python -m unittest tests.unit.test_x"):
    return "\t".join((row_id, "a-case", "docs:1", kind, "macos", command, "exit 0", "exit 0", verdict, NOW)) + "\n"


def unit_row(unit, track, state, pr):
    return "\t".join((unit, track, state, f"feat/{unit}", pr, "", f"briefs/{unit}-x.md", "a note")) + "\n"


def decision_row(ts):
    return "\t".join((ts, "worker", "a step", "a reason", "evidence", "U2")) + "\n"


def gate_row(gate_id, gate, moment, default, result):
    return f"| {gate_id} | {gate} | {moment} | run / leave | {default} | {result} |\n"


ALPHA = TESTS_HEADER + test_row("a1", "auto", "OK") + test_row("a2", "auto", "OK")
BETA = (
    TESTS_HEADER
    + test_row("b1", "auto", "OK")
    + test_row("b2", "auto", "NG")
    + test_row("b3", "operator", "pending", "run make deploy-kit on the laptop")
)
BETA_GREEN = TESTS_HEADER + test_row("b1", "auto", "OK") + test_row("b2", "operator", "OK")
GATES = (
    "# Human gates\n\n"
    + GATES_HEADER
    + "| --- | --- | --- | --- | --- | --- |\n"
    + gate_row("G1", "Adopt the plan", "after wave 1", "adopt", "PASSED 2026-10-23T01:31:20Z")
    + gate_row("G2", "Confirm the second layer", "any time", "leave", "")
)
UNITS = UNITS_HEADER + unit_row("U1", "fix", "landed", "10") + unit_row("U2", "feat", "in-flight", "")
UNITS_LANDED = UNITS_HEADER + unit_row("U1", "fix", "landed", "10") + unit_row("U2", "feat", "landed", "11")
DECISIONS = DECISIONS_HEADER + decision_row("2026-11-12T06:00:00Z") + decision_row("2026-11-12T06:48:00Z")

REPORT_EN = (
    "state: moving: 1 units in flight, last record 12 min ago\n"
    "elements\n"
    "alpha: green 2/2 OK, 0 NG, 0 pending\n"
    "beta: red 1/3 OK, 1 NG, 1 pending\n"
    "operator acts\n"
    "beta b3: run make deploy-kit on the laptop\n"
    "operator decisions\n"
    "G2: Confirm the second layer (any time; default leave)\n"
    "agent running\n"
    "U2 feat pr - progress: unknown\n"
)
REPORT_JA = (
    "状態: 進んでいる: 1 units in flight, last record 12 min ago\n"
    "要素\n"
    "alpha: green 2/2 OK, 0 NG, 0 pending\n"
    "beta: red 1/3 OK, 1 NG, 1 pending\n"
    "操作者の作業\n"
    "beta b3: run make deploy-kit on the laptop\n"
    "操作者の判断\n"
    "G2: Confirm the second layer (any time; default leave)\n"
    "agent が動かしているもの\n"
    "U2 feat pr - progress: unknown\n"
)

FAKE_ROWS = (
    "#!/usr/bin/env -S python3 -I\n"
    "import pathlib, sys\n"
    "pathlib.Path(sys.argv[0] + '.argv').write_text('\\n'.join(sys.argv[1:]) + '\\n')\n"
    "sys.stdout.write('unit\\tstate\\tage_minutes\\tlast_line\\n')\n"
    "sys.stdout.write('U2\\tstalled\\t47\\tread the brief\\n')\n"
    "sys.stdout.write('U9\\tfresh\\t1\\tnot in flight\\n')\n"
)
FAKE_REFUSES = (
    "#!/usr/bin/env -S python3 -I\n"
    "import sys\n"
    "print('stall-check.py: refused: units.tsv unreadable', file=sys.stderr)\n"
    "sys.exit(2)\n"
)


class ProgramStatusTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.store = root / "regime-cutover"
        (self.store / "tests").mkdir(parents=True)
        self.write_store()
        self.home = root / "home"
        self.home.mkdir()
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}
        self.lever = LEVER

    def write_store(self, alpha=ALPHA, beta=BETA, gates=GATES, units=UNITS, decisions=DECISIONS):
        (self.store / "tests/alpha.tsv").write_text(alpha)
        (self.store / "tests/beta.tsv").write_text(beta)
        (self.store / "tests/notes.txt").write_text("not a table\n")
        (self.store / "gates.md").write_text(gates)
        (self.store / "units.tsv").write_text(units)
        (self.store / "decisions.tsv").write_text(decisions)

    def copy_lever(self):
        """A checkout-shaped copy of the lever two levels below a copy of the manifest, so the self check passes on
        the copy and a `stall-check.py` can be written beside it."""
        checkout = Path(self.temp.name).resolve() / "checkout"
        levers = checkout / "scripts/orchestrator"
        levers.mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(MANIFEST, checkout / "home/dot_agents/agent-config.yaml")
        shutil.copy2(LEVER, levers / LEVER.name)
        self.lever = levers / LEVER.name
        return levers

    def write_fake(self, levers, text):
        fake = levers / "stall-check.py"
        fake.write_text(text)
        fake.chmod(0o755)
        return fake

    def run_lever(self, *args):
        return subprocess.run(
            [sys.executable, "-I", str(self.lever), str(self.store), "--now", NOW, *args],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )

    def assert_report(self, expected, *args):
        run = self.run_lever(*args)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertEqual(run.stdout, expected)
        return run

    def assert_refused(self, *reasons, args=()):
        """Exit 2, one stderr line naming each reason, nothing on stdout."""
        run = self.run_lever(*args)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith("program-status.py: refused: "), run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)
        return run.stderr

    def store_listing(self):
        return sorted(str(path.relative_to(self.store)) for path in self.store.rglob("*"))

    # (a) the report, byte for byte.

    def test_the_report_in_english_byte_for_byte_and_no_file_written(self):
        before = self.store_listing()
        self.assert_report(REPORT_EN)
        self.assertEqual(self.store_listing(), before, "the lever writes no file")

    def test_ja_prints_the_five_headings_and_the_state_word_in_the_operators_forms_and_nothing_else_translated(self):
        self.assert_report(REPORT_JA, "--ja")

    def test_the_signal_is_yellow_with_a_pending_row_and_no_ng_and_grey_with_no_row_or_another_verdict(self):
        yellow = TESTS_HEADER + test_row("b1", "auto", "OK") + test_row("b2", "not-started", "pending")
        self.write_store(beta=yellow)
        run = self.assert_report(
            REPORT_EN.replace("beta: red 1/3 OK, 1 NG, 1 pending", "beta: yellow 1/2 OK, 0 NG, 1 pending").replace(
                "beta b3: run make deploy-kit on the laptop", "none"
            )
        )
        self.assertIn("\noperator acts\nnone\n", run.stdout)
        self.write_store(beta=TESTS_HEADER)
        self.assert_report(
            REPORT_EN.replace("beta: red 1/3 OK, 1 NG, 1 pending", "beta: grey 0/0 OK, 0 NG, 0 pending").replace(
                "beta b3: run make deploy-kit on the laptop", "none"
            )
        )
        self.write_store(beta=TESTS_HEADER + test_row("b1", "auto", "skipped"))
        self.assert_report(
            REPORT_EN.replace("beta: red 1/3 OK, 1 NG, 1 pending", "beta: grey 0/1 OK, 0 NG, 0 pending").replace(
                "beta b3: run make deploy-kit on the laptop", "none"
            )
        )

    def test_a_closed_gate_and_a_landed_unit_print_no_line_and_an_empty_section_reads_none(self):
        gates = GATES.replace(gate_row("G2", "Confirm the second layer", "any time", "leave", ""), "")
        self.write_store(gates=gates, units=UNITS_LANDED, beta=BETA_GREEN.replace("OK\t" + NOW, "pending\t" + NOW))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertIn("\noperator decisions\nnone\n", run.stdout)
        self.assertIn("\nagent running\nnone\n", run.stdout)

    # (b) the three state words.

    def test_done_when_every_table_is_green(self):
        self.write_store(beta=BETA_GREEN)
        run = self.run_lever()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines()[0], "state: done: every table green, last record 12 min ago")
        run = self.run_lever("--ja")
        self.assertEqual(run.stdout.splitlines()[0], "状態: 完了: every table green, last record 12 min ago")

    def test_stopped_when_nothing_is_in_flight_and_an_act_or_a_decision_waits(self):
        self.write_store(units=UNITS_LANDED)
        run = self.run_lever()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stdout.splitlines()[0],
            "state: stopped: nothing in flight, waiting on 1 operator acts and 1 decisions, last record 12 min ago",
        )
        self.assertIn("\nagent running\nnone\n", run.stdout)
        run = self.run_lever("--ja")
        self.assertTrue(run.stdout.startswith("状態: 止まっている: nothing in flight"), run.stdout)

    def test_moving_otherwise_even_with_nothing_in_flight_when_nothing_waits(self):
        gates = GATES.replace(gate_row("G2", "Confirm the second layer", "any time", "leave", ""), "")
        beta = TESTS_HEADER + test_row("b1", "auto", "OK") + test_row("b2", "auto", "NG")
        self.write_store(units=UNITS_LANDED, gates=gates, beta=beta)
        run = self.run_lever()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.splitlines()[0], "state: moving: 0 units in flight, last record 12 min ago")

    def test_the_age_is_now_minus_the_last_decision_row_in_whole_minutes(self):
        run = self.run_lever()
        self.assertIn("last record 12 min ago", run.stdout.splitlines()[0])
        self.lever = LEVER
        run = subprocess.run(
            [sys.executable, "-I", str(LEVER), str(self.store), "--now", "2026-11-13T06:48:59Z"],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("last record 1440 min ago", run.stdout.splitlines()[0])

    # (c) stall-check.py beside the lever.

    def test_a_stall_check_beside_the_lever_feeds_the_progress_column_and_a_stalled_worker_stops_the_state(self):
        levers = self.copy_lever()
        fake = self.write_fake(levers, FAKE_ROWS)
        progress_root = str(Path(self.temp.name).resolve() / "wt")
        run = self.run_lever("--progress-root", progress_root)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        lines = run.stdout.splitlines()
        self.assertEqual(lines[0], "state: stopped: every in-flight worker silent, last record 12 min ago")
        self.assertEqual(lines[-1], "U2 feat pr - progress: stalled, 47 min, read the brief")
        self.assertNotIn("U9", run.stdout, "a row of a unit not in flight prints nothing")
        # --now and --progress-root pass through to the stall check, after the store.
        self.assertEqual(
            (fake.parent / "stall-check.py.argv").read_text(),
            f"{self.store}\n--progress-root\n{progress_root}\n--now\n{NOW}\n",
        )

    def test_a_stall_check_exit_2_refuses_the_report(self):
        levers = self.copy_lever()
        self.write_fake(levers, FAKE_REFUSES)
        self.assert_refused("stall-check.py", "units.tsv unreadable")

    def test_a_stall_check_row_of_another_shape_refuses(self):
        levers = self.copy_lever()
        self.write_fake(levers, "#!/usr/bin/env -S python3 -I\nprint('U2\\tstalled\\t47')\n")
        self.assert_refused("stall-check.py", "cells")

    def test_an_absent_stall_check_reads_progress_unknown(self):
        self.copy_lever()
        self.assert_report(REPORT_EN)

    def test_a_fresh_worker_beside_a_stalled_one_keeps_the_state_moving(self):
        levers = self.copy_lever()
        self.write_fake(levers, FAKE_ROWS.replace("U9\\tfresh", "U3\\tfresh"))
        self.write_store(units=UNITS + unit_row("U3", "feat", "in-flight", "12"))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        lines = run.stdout.splitlines()
        self.assertEqual(lines[0], "state: moving: 2 units in flight, last record 12 min ago")
        self.assertEqual(
            lines[-2:],
            [
                "U2 feat pr - progress: stalled, 47 min, read the brief",
                "U3 feat pr 12 progress: fresh, 1 min, not in flight",
            ],
        )

    # (d) every refusal: exit 2, one stderr line, nothing on stdout.

    def test_each_header_refusal_names_the_file(self):
        cases = (
            ("tests/beta.tsv", BETA.replace("\tverdict\t", "\tresult\t", 1)),
            ("gates.md", GATES.replace(GATES_HEADER, "| id | gate | moment | result |\n")),
            ("units.tsv", UNITS.replace("\tpr\t", "\tpull\t", 1)),
            ("decisions.tsv", DECISIONS.replace("ts\tphase", "when\tphase", 1)),
        )
        for relative, text in cases:
            with self.subTest(file=relative):
                self.write_store()
                (self.store / relative).write_text(text)
                self.assert_refused(str(self.store / relative), "header")

    def test_a_row_of_another_width_a_missing_file_and_an_empty_decisions_table_refuse(self):
        (self.store / "tests/beta.tsv").write_text(BETA + "b4\tauto\n")
        self.assert_refused(str(self.store / "tests/beta.tsv"), "line 5", "cells")
        self.write_store()
        (self.store / "gates.md").write_text(GATES + "| G3 | a gate | now |\n")
        self.assert_refused(str(self.store / "gates.md"), "line 7", "cells")
        self.write_store()
        (self.store / "units.tsv").unlink()
        self.assert_refused(str(self.store / "units.tsv"))
        self.write_store(decisions=DECISIONS_HEADER)
        self.assert_refused(str(self.store / "decisions.tsv"), "no row")
        self.write_store(decisions=DECISIONS_HEADER + decision_row("yesterday"))
        self.assert_refused(str(self.store / "decisions.tsv"), "yesterday")

    def test_a_bad_now_and_a_store_that_is_no_directory_refuse(self):
        run = subprocess.run(
            [sys.executable, "-I", str(LEVER), str(self.store), "--now", "2026-11-12 07:00"],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("program-status.py: refused: --now", run.stderr)
        run = subprocess.run(
            [sys.executable, "-I", str(LEVER), str(self.store / "units.tsv"), "--now", NOW],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("not a directory", run.stderr)

    def test_an_altered_copy_refuses_on_its_self_pin_before_anything_is_read(self):
        self.copy_lever()
        with open(self.lever, "a", encoding="utf-8") as handle:
            handle.write("# altered\n")
        (self.store / "units.tsv").unlink()  # unread: the pin refusal comes first
        stderr = self.assert_refused("sha256 ", "differs from the pin in")
        self.assertIn("home/dot_agents/agent-config.yaml", stderr)

    def test_the_checkout_lever_is_executable_and_runs_python3_isolated(self):
        self.assertEqual(LEVER.stat().st_mode & 0o777, 0o755)
        self.assertEqual(LEVER.read_text().splitlines()[0], "#!/usr/bin/env -S python3 -I")


if __name__ == "__main__":
    unittest.main()
