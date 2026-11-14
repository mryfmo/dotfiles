"""Exercise scripts/orchestrator/program-status.py (regime-cutover U497), the lever that prints the operator's state
report of a program store in standing order 56's shape, as a subprocess under `python3 -I` over a scratch store: the
report byte for byte in English and with `--ja`, the three state words each from a fixture, a fake `stall-check.py`
beside a copy of the lever, the absent-lever column, every header refusal and the self pin refusal of an altered copy;
and (U497b) every refusal as one stderr line, every stall-check cell checked, and every report item one line; and
(U497c) the gates header read by cell names, every printed cell one line, the tables read byte-exact; and (U496h) the
real stall check's exit 2 with rows (a malformed file beside a stalled worker) read as rows, its exit 2 with nothing on
stdout as its refusal with the reason, and its exit 1 with a traceback or no row as a refusal by name."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/program-status.py"
STALL_CHECK = ROOT / "scripts/orchestrator/stall-check.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
NOW = "2026-11-12T07:00:00Z"
# The kit's own gates template, copied into every new store by regime-init: its header cells are padded.
TEMPLATE_GATES = (ROOT / "home/dot_agents/regime/gates.md").read_text(encoding="utf-8")

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
    "sys.stdout.write('U9\\tmoving\\t1\\tnot in flight\\n')\n"
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
        # The default run is a copy with no `stall-check.py` beside it (the absent-lever column): since U496 the real
        # stall check sits beside the checkout lever, and over this scratch store it would refuse on its progress root.
        self.copy_lever()

    def write_store(self, alpha=ALPHA, beta=BETA, gates=GATES, units=UNITS, decisions=DECISIONS):
        (self.store / "tests/alpha.tsv").write_text(alpha)
        (self.store / "tests/beta.tsv").write_text(beta)
        (self.store / "tests/notes.txt").write_text("not a table\n")
        (self.store / "gates.md").write_text(gates)
        (self.store / "units.tsv").write_text(units)
        (self.store / "decisions.tsv").write_text(decisions)

    def copy_lever(self):
        """A checkout-shaped copy of the lever two levels below a copy of the manifest, so the self check passes on
        the copy and a `stall-check.py` can be written beside it; setUp makes the copy, a second call renews it."""
        checkout = Path(self.temp.name).resolve() / "checkout"
        levers = checkout / "scripts/orchestrator"
        levers.mkdir(parents=True, exist_ok=True)
        (checkout / "home/dot_agents").mkdir(parents=True, exist_ok=True)
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
        return self.run_raw(str(self.store), "--now", NOW, *args)

    def run_raw(self, *argv):
        """The lever under `python3 -I` with exactly `argv` after it."""
        return subprocess.run(
            [sys.executable, "-I", str(self.lever), *argv],
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
        run = subprocess.run(
            [sys.executable, "-I", str(self.lever), str(self.store), "--now", "2026-11-13T06:48:59Z"],
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
        stderr = self.assert_refused("stall-check.py refused this report", "units.tsv unreadable")
        self.assertNotIn("no reason given", stderr)
        # Nothing at all on exit 2 is still its refusal, with no reason to quote.
        self.write_fake(levers, "#!/usr/bin/env -S python3 -I\nimport sys\nsys.exit(2)\n")
        self.assert_refused("stall-check.py refused this report", "no reason given")

    # (g) round 4 (U496h, verdict U496f-0eecc2a9 P1): the checker's exit 2 with rows is a report, never a refusal.

    def test_the_real_stall_check_s_exit_2_with_a_malformed_row_beside_a_stalled_row_reaches_the_report(self):
        """The real checker beside a copy of the lever, over a progress root where U2's last line is 47 minutes old
        and U3's file is garbage: the checker prints both rows and exits 2 with nothing on stderr (U496e), and the
        operator report carries each worker's row, the stalled one never hidden by the malformed one (at 0eecc2a9 the
        exit 2 was read as a refusal, `no reason given`). The checker's exact result is then replayed by a fake that
        writes the same bytes and exits the same, and reads the same."""
        levers = self.copy_lever()
        shutil.copy2(STALL_CHECK, levers / STALL_CHECK.name)
        self.write_store(units=UNITS + unit_row("U3", "feat", "in-flight", "12"))
        progress_root = Path(self.temp.name).resolve() / "wt"
        progress_root.mkdir()
        (progress_root / "U2-progress.txt").write_text("2026-11-12T06:13:00Z U2: read the brief\n")
        (progress_root / "U3-progress.txt").write_text("garbage\n")
        checker = subprocess.run(
            [
                sys.executable,
                "-I",
                str(levers / STALL_CHECK.name),
                str(self.store),
                "--progress-root",
                str(progress_root),
                "--now",
                NOW,
            ],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )
        malformed = "the last line has no YYYY-MM-DDTHH:MM:SSZ timestamp and a space before its text: garbage"
        self.assertEqual(
            (checker.returncode, checker.stdout, checker.stderr),
            (2, f"U2\tstalled\t47\t2026-11-12T06:13:00Z U2: read the brief\nU3\tmalformed\t-\t{malformed}\n", ""),
        )
        expected_tail = [
            "U2 feat pr - progress: stalled, 47 min, 2026-11-12T06:13:00Z U2: read the brief",
            f"U3 feat pr 12 progress: malformed, - min, {malformed}",
        ]
        with self.subTest(checker="the real stall-check.py beside the lever"):
            run = self.run_lever("--progress-root", str(progress_root))
            self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
            lines = run.stdout.splitlines()
            self.assertEqual(lines[-2:], expected_tail)
            self.assertEqual(lines[0], "state: moving: 2 units in flight, last record 12 min ago")
        with self.subTest(checker="a fake replaying the real result byte for byte"):
            self.write_fake(
                levers,
                "#!/usr/bin/env -S python3 -I\nimport sys\n"
                f"sys.stdout.write({checker.stdout!r})\nsys.exit({checker.returncode})\n",
            )
            run = self.run_lever()
            self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
            self.assertEqual(run.stdout.splitlines()[-2:], expected_tail)

    def test_a_stall_check_exit_2_with_rows_and_a_stderr_line_refuses_quoting_the_line(self):
        """Rows and a stderr line together are outside the checker's contract (rows exit 2 with nothing on stderr; a
        refusal with nothing on stdout), so the report is refused, the line quoted."""
        levers = self.copy_lever()
        self.write_fake(
            levers,
            "#!/usr/bin/env -S python3 -I\nimport sys\n"
            "sys.stdout.write('U2\\tmalformed\\t-\\tthe file is empty\\n')\n"
            "print('stall-check.py: refused: and yet', file=sys.stderr)\nsys.exit(2)\n",
        )
        self.assert_refused("stall-check.py", "exited 2", "and yet")

    def test_a_stall_check_exit_1_with_a_traceback_or_no_row_refuses_by_name_never_no_row(self):
        """A checker that crashes (exit 1, a traceback on stderr, nothing on stdout) or exits 1 with nothing at all is
        no report of the workers: the refusal names the checker and quotes the traceback's last line, and `progress:
        no row` is never printed for it (the U499 item, closed here)."""
        levers = self.copy_lever()
        self.write_fake(levers, "#!/usr/bin/env -S python3 -I\nraise RuntimeError('a bug in the checker')\n")
        stderr = self.assert_refused("stall-check.py", "exited 1", "RuntimeError: a bug in the checker")
        self.assertNotIn("no row", stderr)
        self.write_fake(levers, "#!/usr/bin/env -S python3 -I\nimport sys\nsys.exit(1)\n")
        self.assert_refused("stall-check.py", "exited 1", "no row")
        # A traceback with exit 0 is no report either.
        self.write_fake(
            levers,
            "#!/usr/bin/env -S python3 -I\nimport sys\n"
            "sys.stdout.write('U2\\tstalled\\t47\\tread the brief\\n')\nprint('Traceback (most recent call last):\\n  x\\nValueError: late', file=sys.stderr)\n",
        )
        self.assert_refused("stall-check.py", "exited 0", "ValueError: late")

    def test_a_stall_check_row_of_another_shape_refuses(self):
        levers = self.copy_lever()
        self.write_fake(levers, "#!/usr/bin/env -S python3 -I\nprint('U2\\tstalled\\t47')\n")
        self.assert_refused("stall-check.py", "cells")

    def test_an_absent_stall_check_reads_progress_unknown(self):
        self.copy_lever()
        self.assert_report(REPORT_EN)

    def test_a_moving_worker_beside_a_stalled_one_keeps_the_state_moving(self):
        levers = self.copy_lever()
        self.write_fake(levers, FAKE_ROWS.replace("U9\\tmoving", "U3\\tmoving"))
        self.write_store(units=UNITS + unit_row("U3", "feat", "in-flight", "12"))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        lines = run.stdout.splitlines()
        self.assertEqual(lines[0], "state: moving: 2 units in flight, last record 12 min ago")
        self.assertEqual(
            lines[-2:],
            [
                "U2 feat pr - progress: stalled, 47 min, read the brief",
                "U3 feat pr 12 progress: moving, 1 min, not in flight",
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

    # (e) round 2 (U497b): every refusal one stderr line, every stall-check cell checked, every item one line.

    def test_a_stall_check_whose_output_is_not_utf_8_refuses_in_one_line_and_never_tracebacks(self):
        levers = self.copy_lever()
        self.write_fake(
            levers,
            "#!/usr/bin/env -S python3 -I\nimport sys\n"
            "sys.stdout.buffer.write(b'U2\\tstalled\\t47\\tread \\xff the brief\\n')\n",
        )
        self.assert_refused("stall-check.py", "UTF-8")
        self.write_fake(
            levers,
            "#!/usr/bin/env -S python3 -I\nimport sys\n"
            "sys.stderr.buffer.write(b'stall-check.py: refused: \\xff\\n')\nsys.exit(2)\n",
        )
        self.assert_refused("stall-check.py", "UTF-8")

    def test_a_stall_check_row_with_a_nonnumeric_age_or_an_unknown_state_refuses_naming_the_line(self):
        levers = self.copy_lever()
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tstalled\\tabc"))
        self.assert_refused("stall-check.py", "line 2", "age_minutes", "abc")
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tstalled\\t12345678901"))
        self.assert_refused("stall-check.py", "line 2", "age_minutes", "12345678901")
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tstalled\\t"))
        self.assert_refused("stall-check.py", "line 2", "age_minutes")
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tasleep\\t47"))
        self.assert_refused("stall-check.py", "line 2", "state", "asleep")
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tstalled\\t47\\r"))
        self.assert_refused("stall-check.py", "line 2", "carriage return")
        # `-` and every one of the six states pass.
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tunreadable\\t-"))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertEqual(run.stdout.splitlines()[-1], "U2 feat pr - progress: unreadable, - min, read the brief")
        self.write_fake(levers, FAKE_ROWS.replace("U2\\tstalled\\t47", "U2\\tmalformed\\t-"))
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertEqual(run.stdout.splitlines()[-1], "U2 feat pr - progress: malformed, - min, read the brief")
        self.assertEqual(run.stdout.splitlines()[0], "state: moving: 1 units in flight, last record 12 min ago")

    def test_a_tests_table_named_with_a_newline_or_outside_the_name_class_refuses_naming_the_file(self):
        (self.store / "tests/ga\nmma.tsv").write_text(ALPHA)
        self.assert_refused("tests/ga mma.tsv", "[A-Za-z0-9._-]")
        (self.store / "tests/ga\nmma.tsv").unlink()
        for name in ("ga\tmma.tsv", "ga mma.tsv", "gam\x1bma.tsv", "ガンマ.tsv", ".tsv"):
            with self.subTest(name=name):
                (self.store / "tests" / name).write_text(ALPHA)
                stderr = self.assert_refused("[A-Za-z0-9._-]")
                self.assertIn(str(self.store / "tests"), stderr)
                (self.store / "tests" / name).unlink()
        (self.store / "tests/Ga.m_m-a9.tsv").write_text(ALPHA)
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertIn("\nGa.m_m-a9: green 2/2 OK, 0 NG, 0 pending\n", run.stdout)

    def test_now_and_a_decisions_ts_are_held_to_the_exact_shape_before_strptime(self):
        for value in (
            "2026-1-2T3:4:5Z",
            "2026-11-12T07:00:00+00:00",
            "2026-11-12T07:00:00Z\n",
            "２０２６-11-12T07:00:00Z",
        ):
            with self.subTest(now=value):
                run = self.run_raw(str(self.store), "--now", value)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn("program-status.py: refused: --now", run.stderr)
                self.assertIn("<YYYY-MM-DD>T<HH:MM:SS>Z", run.stderr)
        self.write_store(decisions=DECISIONS_HEADER + decision_row("2026-11-12T6:48:00Z"))
        self.assert_refused(str(self.store / "decisions.tsv"), "2026-11-12T6:48:00Z", "<YYYY-MM-DD>T<HH:MM:SS>Z")

    def test_a_header_refusal_names_the_file_and_line_1(self):
        cases = (
            ("tests/beta.tsv", BETA.replace("\tverdict\t", "\tresult\t", 1)),
            ("units.tsv", UNITS.replace("\tpr\t", "\tpull\t", 1)),
            ("decisions.tsv", DECISIONS.replace("ts\tphase", "when\tphase", 1)),
            ("decisions.tsv", ""),
        )
        for relative, text in cases:
            with self.subTest(file=relative, text=text[:12]):
                self.write_store()
                (self.store / relative).write_text(text)
                self.assert_refused(f"{self.store / relative}:1", "header")

    def test_a_store_path_or_a_value_holding_a_newline_refuses_in_one_stderr_line(self):
        run = self.run_raw(str(self.store) + "\nmissing", "--now", NOW)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith("program-status.py: refused: the store "), run.stderr)
        self.assertIn(" missing cannot be read", run.stderr)
        run = self.run_raw(str(self.store) + "\r\nmissing", "--now", NOW)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertNotIn("\r", run.stderr)
        levers = self.copy_lever()
        self.write_fake(
            levers,
            "#!/usr/bin/env -S python3 -I\nimport sys\n"
            "sys.stderr.write('stall-check.py: refused: a\\rb\\n')\nsys.exit(2)\n",
        )
        stderr = self.assert_refused("stall-check.py", "a b")
        self.assertNotIn("\r", stderr)

    # (f) round 3 (U497c): the gates header by cell names, every printed cell one line, tables byte-exact.

    def test_the_kits_template_header_and_the_live_header_are_both_accepted_and_a_misspelled_name_refuses(self):
        open_gate = gate_row("G2", "Confirm the second layer", "any time", "leave", "")
        self.assertIn("| id  | gate | moment | options | default | result |\n", TEMPLATE_GATES, "the padded template")
        self.write_store(gates=TEMPLATE_GATES + open_gate)
        self.assert_report(REPORT_EN)
        self.write_store(gates=GATES)
        self.assert_report(REPORT_EN)
        path = str(self.store / "gates.md")
        self.write_store(gates=GATES.replace(GATES_HEADER, "| id | gate | moment | options | default | results |\n"))
        self.assert_refused(f"{path}:3", "header")
        self.write_store(gates=GATES.replace(GATES_HEADER, "| id | gate | moment | options | default |\n"))
        self.assert_refused(f"{path}:3", "header")
        self.write_store(gates=GATES.replace("| --- | --- | --- | --- | --- | --- |\n", ""))
        self.assert_refused(f"{path}:4", "separator")
        self.write_store(gates=GATES.replace("| --- | --- | --- | --- | --- | --- |\n", "| --- | --- | --- |\n"))
        self.assert_refused(f"{path}:4", "separator")
        self.write_store(gates="# Human gates\n\nno table here\n")
        self.assert_refused(path, "header")

    def test_a_cell_holding_a_line_separator_prints_on_one_line(self):
        levers = self.copy_lever()
        self.write_fake(levers, FAKE_ROWS.replace("read the brief", "read the\\u2029brief\\x85now"))
        self.write_store(
            beta=BETA.replace("b3\t", "b3\u2028x\t"),
            gates=GATES.replace("Confirm the second layer", "Confirm the\u2028second\x0clayer"),
        )
        run = self.run_lever()
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        self.assertEqual(len(run.stdout.splitlines()), 10, run.stdout)
        self.assertEqual(
            run.stdout,
            REPORT_EN.replace("beta b3:", "beta b3 x:")
            .replace("state: moving: 1 units in flight", "state: stopped: every in-flight worker silent")
            .replace("progress: unknown", "progress: stalled, 47 min, read the brief now"),
        )

    def test_a_crlf_tests_table_refuses_naming_the_row(self):
        path = str(self.store / "tests/beta.tsv")
        (self.store / "tests/beta.tsv").write_bytes(BETA.replace("\n", "\r\n").encode("utf-8"))
        self.assert_refused(path, "line 1", "carriage return")
        (self.store / "tests/beta.tsv").write_bytes(
            BETA.replace(test_row("b2", "auto", "NG"), test_row("b2", "auto", "NG").replace("\n", "\r\n")).encode()
        )
        self.assert_refused(path, "line 3", "carriage return")
        self.write_store()
        (self.store / "gates.md").write_bytes(GATES.replace("\n", "\r\n").encode("utf-8"))
        self.assert_refused(str(self.store / "gates.md"), "line 1", "carriage return")


if __name__ == "__main__":
    unittest.main()
