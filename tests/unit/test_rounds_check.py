"""Exercise scripts/orchestrator/rounds-check.py on fixture stores (regime-cutover U120, standing order 36): the round
cap and the two-strike rule as exit codes and one-line reasons, the rows before the rule's effective date that are
read but not counted, the malformed-store refusals naming the file and line, `--all` over several units, and the git
form the `regime` check runs on a pull request's head."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts/orchestrator/rounds-check.py"
STORE = ".orchestration/orchestrate/regime-cutover"
LEDGER_HEADER = "ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence\n"
DECISIONS_HEADER = "ts\tphase\tdecision\twhy\tevidence\tresult\n"
ROW_TO_WRITE = (
    'write decisions.tsv phase=mechanism-change decision="{unit} ..." result names one of '
    "ast|parser-module|allowlist|remove|residual"
)
GIT_ENV = quiet_git_env(
    {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    | {f"GIT_{role}_{k}": v for role in ("AUTHOR", "COMMITTER") for k, v in (("NAME", "t"), ("EMAIL", "t@t"))}
)


def audit(ts, unit, verdict, evidence="class=status findings=1"):
    """One ledger row: an audit round of `unit` at `ts` (`class=` given, as standing order 39 asks)."""
    return (ts, unit, "7", "a" * 40, verdict, "pr-audit.sh", evidence)


def mechanism(ts, unit, result, phase="mechanism-change", sep=" "):
    """One decisions row: the mechanism-change row of `unit` whose result is given."""
    return (ts, phase, f"{unit}{sep}rule f closes as one module", "the class kept coming back", "verdicts", result)


def tsv(header, rows):
    return header + "".join("\t".join(row) + "\n" for row in rows)


def three_incorrect(unit="U7"):
    return [audit(f"2026-10-30T0{n}:00:00Z", unit, "incorrect") for n in (1, 2, 3)]


def four_earlier_incorrect(unit="U7"):
    """Four incorrect rows of the day before the rule (no `class=`, as rows of that day have none)."""
    return [
        audit(f"2026-10-29T0{n}:00:00Z", unit, "incorrect", "findings=1 P2: the status is lost") for n in (1, 2, 3, 4)
    ]


def ignored(count):
    return f"{count} earlier rows ignored (rule effective 2026-10-30)"


class RoundsCheckTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()

    def store(self, ledger=(), decisions=(), ledger_text=None, decisions_text=None):
        """A fixture store under tmp_path: the two files from the rows, or the texts given verbatim."""
        store = self.root / "regime-cutover"
        store.mkdir(exist_ok=True)
        (store / "ledger.tsv").write_text(tsv(LEDGER_HEADER, ledger) if ledger_text is None else ledger_text)
        (store / "decisions.tsv").write_text(
            tsv(DECISIONS_HEADER, decisions) if decisions_text is None else decisions_text
        )
        return store

    def check(self, *args, env=None, cwd=None):
        return subprocess.run(
            [sys.executable, "-I", str(CHECK), *map(str, args)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
            env=env,
            cwd=cwd,
        )

    def test_two_audit_rows_allow_the_next_round(self):
        rows = [audit("2026-10-30T01:00:00Z", "U7", "incorrect"), audit("2026-10-30T02:00:00Z", "U7", "incorrect")]
        run = self.check(self.store(rows), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 allowed: 2 audit rows (2 incorrect), 2 incorrect since the start (classes: status=2), 0 mechanism rows\n",
            run.stdout,
        )

    def test_three_incorrect_rows_without_a_mechanism_row_refuse_naming_the_row_to_write(self):
        run = self.check(self.store(three_incorrect()), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(run.stdout.count("\n"), 1, "one line")
        self.assertIn(
            "rounds-check: U7 refused: 3 audit rows (3 incorrect), 3 incorrect since the start (classes: status=3), 0 mechanism rows",
            run.stdout,
        )
        self.assertIn("the fourth round needs a mechanism-change row: " + ROW_TO_WRITE.format(unit="U7"), run.stdout)

    def test_three_incorrect_rows_and_a_mechanism_row_after_them_allow(self):
        for sep in (" ", ":"):
            with self.subTest(sep=sep):
                decisions = [mechanism("2026-10-30T04:00:00Z", "U7", "parser-module: one strict reader", sep=sep)]
                run = self.check(self.store(three_incorrect(), decisions), "U7")
                self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
                self.assertIn(
                    "U7 allowed: 3 audit rows (3 incorrect), 0 incorrect since the mechanism-change row of "
                    "2026-10-30T04:00:00Z (parser-module) (classes: none), 1 mechanism rows",
                    run.stdout,
                )

    def test_two_more_incorrect_rows_after_the_mechanism_row_refuse_asking_for_another(self):
        rows = three_incorrect()
        rows.append(audit("2026-10-30T05:00:00Z", "U7", "incorrect"))
        rows.append(audit("2026-10-30T06:00:00Z", "U7", "correct", "findings=0"))
        decisions = [mechanism("2026-10-30T04:00:00Z", "U7", "allowlist of the guarded names")]
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)  # one strike after the row
        rows.append(audit("2026-10-30T07:00:00Z", "U7", "incorrect"))
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn(
            "U7 refused: 6 audit rows (5 incorrect), 2 incorrect since the mechanism-change row of 2026-10-30T04:00:00Z"
            " (allowlist) (classes: status=2), 1 mechanism rows; 2 strikes of class status since that row need another: "
            + ROW_TO_WRITE.format(unit="U7"),
            run.stdout,
        )
        # a row at the mechanism row's own ts is not after it, so the strikes are back to one
        rows[-1] = audit("2026-10-30T04:00:00Z", "U7", "incorrect")
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)

    def test_a_mechanism_row_then_two_incorrect_rows_refuse_whatever_the_total_count(self):
        # round 3: the two strikes are counted on their own, not behind the cap; on 05a48d78 the below-three shortcut
        # allowed a unit whose only counted rows were a mechanism row and two incorrect rows after it
        decisions = [mechanism("2026-10-30T04:00:00Z", "U7", "remove")]
        rows = [audit("2026-10-30T05:00:00Z", "U7", "incorrect")]
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 allowed: 1 audit rows (1 incorrect), 1 incorrect since the mechanism-change row of "
            "2026-10-30T04:00:00Z (remove) (classes: status=1), 1 mechanism rows\n",
            run.stdout,
        )
        rows.append(audit("2026-10-30T06:00:00Z", "U7", "incorrect"))
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 refused: 2 audit rows (2 incorrect), 2 incorrect since the mechanism-change row of "
            "2026-10-30T04:00:00Z (remove) (classes: status=2), 1 mechanism rows; 2 strikes of class status since that "
            "row need another: "
            f"{ROW_TO_WRITE.format(unit='U7')}\n",
            run.stdout,
        )
        run = self.check("--all", self.store(rows, decisions))
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertIn("rounds-check: U7 refused: 2 audit rows (2 incorrect)", run.stdout)

    def test_two_incorrect_rows_of_different_classes_after_the_mechanism_row_are_one_strike_each(self):
        """Round 7 (the Codex P2 on c3a9bfdc): the two strikes are two `incorrect` rows of one class (the word of the
        `class=` token), so two rows of unrelated classes after the mechanism row refuse nothing; on c3a9bfdc the word
        was discarded and their sum refused, asking for a mechanism-change row no class had earned."""
        decisions = [mechanism("2026-10-30T04:00:00Z", "U7", "remove")]
        rows = [
            audit("2026-10-30T05:00:00Z", "U7", "incorrect", "class=gate-logic findings=1"),
            audit("2026-10-30T06:00:00Z", "U7", "incorrect", "class=unit-key findings=1"),
        ]
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 allowed: 2 audit rows (2 incorrect), 2 incorrect since the mechanism-change row of "
            "2026-10-30T04:00:00Z (remove) (classes: gate-logic=1, unit-key=1), 1 mechanism rows\n",
            run.stdout,
        )
        # a third class is a third single strike; a token's word is whole and case-kept (`Gate-logic` is another)
        rows.append(audit("2026-10-30T07:00:00Z", "U7", "incorrect", "class=Gate-logic"))
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn("(classes: gate-logic=1, unit-key=1, Gate-logic=1), 1 mechanism rows\n", run.stdout)
        # the same rows with the pull request form, and under --all: still allowed
        run = self.check(self.store(rows, decisions), "U7", "--pr", "7")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        run = self.check("--all", self.store(rows, decisions))
        self.assertEqual((0, ""), (run.returncode, run.stdout), run.stderr)

    def test_two_incorrect_rows_of_one_class_after_the_mechanism_row_refuse_naming_the_class(self):
        decisions = [mechanism("2026-10-30T04:00:00Z", "U7", "remove")]
        rows = [
            audit("2026-10-30T05:00:00Z", "U7", "incorrect", "class=gate-logic findings=1"),
            audit("2026-10-30T06:00:00Z", "U7", "incorrect", "class=unit-key findings=1"),
            audit("2026-10-30T07:00:00Z", "U7", "correct", "findings=0"),
            audit("2026-10-30T08:00:00Z", "U7", "incorrect", "class=unit-key findings=2"),
        ]
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 refused: 4 audit rows (3 incorrect), 3 incorrect since the mechanism-change row of "
            "2026-10-30T04:00:00Z (remove) (classes: gate-logic=1, unit-key=2), 1 mechanism rows; 2 strikes of class "
            f"unit-key since that row need another: {ROW_TO_WRITE.format(unit='U7')}\n",
            run.stdout,
        )
        # two classes at two strikes each are both named; a second mechanism row resets every class
        rows.append(audit("2026-10-30T09:00:00Z", "U7", "incorrect", "class=gate-logic findings=1"))
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertIn("2 strikes of class gate-logic and unit-key since that row need another", run.stdout)
        decisions.append(mechanism("2026-10-30T10:00:00Z", "U7", "allowlist"))
        run = self.check(self.store(rows, decisions), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn(
            "0 incorrect since the mechanism-change row of 2026-10-30T10:00:00Z (allowlist) (classes: none), "
            "2 mechanism rows\n",
            run.stdout,
        )

    def test_three_incorrect_rows_of_three_classes_and_no_mechanism_row_are_the_cap(self):
        """The cap counts rows, not classes (standing order 36): three audit rows of three classes and no mechanism
        row refuse as the fourth round, and the line names the classes one each."""
        rows = [
            audit("2026-10-30T01:00:00Z", "U7", "incorrect", "class=gate-logic findings=1"),
            audit("2026-10-30T02:00:00Z", "U7", "incorrect", "class=unit-key findings=1"),
            audit("2026-10-30T03:00:00Z", "U7", "incorrect", "class=status findings=1"),
        ]
        run = self.check(self.store(rows), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 refused: 3 audit rows (3 incorrect), 3 incorrect since the start (classes: gate-logic=1, "
            "unit-key=1, status=1), 0 mechanism rows; the fourth round needs a mechanism-change row: "
            f"{ROW_TO_WRITE.format(unit='U7')}\n",
            run.stdout,
        )
        # three `correct` rows, which carry no class, are the cap alike
        rows = [audit(f"2026-10-30T0{n}:00:00Z", "U7", "correct", "findings=0") for n in (1, 2, 3)]
        run = self.check(self.store(rows), "U7")
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertIn(
            "3 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows; the fourth",
            run.stdout,
        )

    def test_the_pr_form_gates_on_every_unit_the_ledger_names_for_the_pull_request(self):
        """Round 6 (standing order 24): a fix or residual unit U7b writes `Program-Unit: .../U7` in its body and keeps
        U7b in its ledger rows, so `--pr 7` checks the body's unit and the unit of every ledger row whose pr cell is
        7, one line per refused unit and a summary on stderr; a check of U7 alone read three incorrect U7b rows as
        zero (on f03b01af the flag is usage, exit 2)."""
        run = self.check(self.store(three_incorrect("U7b")), "U7", "--pr", "7")
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertEqual(run.stdout.count("\n"), 1, "one line per refused unit")
        self.assertIn(
            "rounds-check: U7b refused: 3 audit rows (3 incorrect), 3 incorrect since the start (classes: status=3), 0 mechanism rows; "
            "the fourth round needs a mechanism-change row: " + ROW_TO_WRITE.format(unit="U7b"),
            run.stdout,
        )
        self.assertEqual("rounds-check: pull request 7 is gated on 2 units (U7, U7b), 1 refused\n", run.stderr)
        # the body unit alone, for a caller without a pull request, is checked as before
        run = self.check(self.store(three_incorrect("U7b")), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 allowed: 0 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows\n",
            run.stdout,
        )
        # a pull request whose rows name only the body unit behaves as before: three rows refuse, two allow
        run = self.check(self.store(three_incorrect()), "U7", "--pr", "7")
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertEqual(run.stdout.count("\n"), 1, "one line")
        self.assertIn("rounds-check: U7 refused: 3 audit rows (3 incorrect), 3 incorrect since the start", run.stdout)
        self.assertEqual("rounds-check: pull request 7 is gated on 1 units (U7), 1 refused\n", run.stderr)
        run = self.check(self.store(three_incorrect()[:2]), "U7", "--pr", "7")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertEqual(
            "rounds-check: U7 allowed: 2 audit rows (2 incorrect), 2 incorrect since the start (classes: status=2), 0 mechanism rows\n",
            run.stdout,
        )
        self.assertEqual("rounds-check: pull request 7 is gated on 1 units (U7), 0 refused\n", run.stderr)
        # a pr cell that is not the pull request's number is not counted, whatever it looks like
        for cell in ("70", "8", "#7", " 7", "07", "7 ", "-"):
            with self.subTest(cell=cell):
                rows = [
                    (ts, unit, cell, head, verdict, who, why)
                    for ts, unit, _pr, head, verdict, who, why in three_incorrect("U7b")
                ]
                run = self.check(self.store(rows), "U7", "--pr", "7")
                self.assertEqual(0, run.returncode, run.stdout + run.stderr)
                self.assertEqual(
                    "rounds-check: U7 allowed: 0 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows\n",
                    run.stdout,
                )
                self.assertEqual("rounds-check: pull request 7 is gated on 1 units (U7), 0 refused\n", run.stderr)
        # an empty pr cell is no "other pull request": the one ledger reader (U122 round 6, `ledger.py`) requires the
        # ts, unit, pr, head_sha and verdict cells, so the row is a malformed store, exit 2 naming the line
        rows = [
            (ts, unit, "", head, verdict, who, why) for ts, unit, _pr, head, verdict, who, why in three_incorrect("U7b")
        ]
        run = self.check(self.store(rows), "U7", "--pr", "7")
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertIn("ledger.tsv:2: column 3 (pr) is empty", run.stderr)
        # every unit of the set allowed: one allowed line each, the body's first; a unit's rows of another pull request
        # still count for it once the set names it, and a unit named twice is checked once
        rows = three_incorrect("U7b")[:1] + [audit("2026-10-30T02:00:00Z", "U7", "correct", "findings=0")]
        rows.append(("2026-10-30T03:00:00Z", "U7b", "8", "b" * 40, "incorrect", "pr-audit.sh", "class=status"))
        rows.append(("2026-10-30T04:00:00Z", "U7c", "7", "c" * 40, "blocked", "pr-audit.sh", "-"))
        rows.append(("2026-10-30T05:00:00Z", "U7c", "7", "c" * 40, "correct", "pr-audit.sh", "findings=0"))
        run = self.check(self.store(rows), "U7", "--pr", "7")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertEqual(
            [
                "rounds-check: U7 allowed: 1 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows",
                "rounds-check: U7b allowed: 2 audit rows (2 incorrect), 2 incorrect since the start (classes: status=2), 0 mechanism rows",
                "rounds-check: U7c allowed: 1 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows",
            ],
            run.stdout.splitlines(),
        )
        self.assertEqual("rounds-check: pull request 7 is gated on 3 units (U7, U7b, U7c), 0 refused\n", run.stderr)
        # two refused units are two lines; a malformed row refuses as today, before any verdict
        rows = three_incorrect("U7b") + three_incorrect("U7")
        run = self.check(self.store(rows), "U7", "--pr", "7")
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertEqual(["U7", "U7b"], [line.split()[1] for line in run.stdout.splitlines()])
        self.assertEqual("rounds-check: pull request 7 is gated on 2 units (U7, U7b), 2 refused\n", run.stderr)
        rows[1] = audit("2026-10-30T02:00:00Z", "U7b", "incorrect", "findings=1")
        run = self.check(self.store(rows), "U7", "--pr", "7")
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertIn("ledger.tsv:3: an incorrect row from 2026-10-30T00:00:00Z on", run.stderr)

    def test_a_result_naming_two_forms_or_none_is_not_a_mechanism_row(self):
        for result in ("ast and allowlist", "an allowlisted ast-free reader", "", "residual-ish"):
            with self.subTest(result=result):
                decisions = [mechanism("2026-10-30T04:00:00Z", "U7", result)]
                run = self.check(self.store(three_incorrect(), decisions), "U7")
                self.assertEqual(1, run.returncode, run.stdout + run.stderr)
                self.assertIn("0 mechanism rows; decisions.tsv:2 is a mechanism-change row for U7 naming", run.stdout)
                self.assertIn("so it does not count; the fourth round needs a mechanism-change row", run.stdout)
        # another unit's row, a row of another phase, or a row of a fix unit counts for U7 as nothing
        for row in (
            mechanism("2026-10-30T04:00:00Z", "U8", "remove"),
            mechanism("2026-10-30T04:00:00Z", "U7", "remove", phase="treadmill"),
            mechanism("2026-10-30T04:00:00Z", "U7", "remove", sep="b "),
        ):
            with self.subTest(row=row):
                run = self.check(self.store(three_incorrect(), [row]), "U7")
                self.assertEqual(1, run.returncode, run.stdout + run.stderr)
                self.assertIn("0 mechanism rows; the fourth round", run.stdout)

    def test_audit_rows_before_the_rule_date_are_read_but_not_counted(self):
        run = self.check(self.store(four_earlier_incorrect()), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 allowed: 0 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows, "
            f"{ignored(4)}\n",
            run.stdout,
        )

    def test_the_cap_counts_the_rows_from_the_rule_date_only(self):
        rows = four_earlier_incorrect() + three_incorrect()[:2]
        run = self.check(self.store(rows), "U7")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn(
            f"U7 allowed: 2 audit rows (2 incorrect), 2 incorrect since the start (classes: status=2), 0 mechanism rows, {ignored(4)}",
            run.stdout,
        )
        rows = four_earlier_incorrect() + three_incorrect()
        run = self.check(self.store(rows), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            "rounds-check: U7 refused: 3 audit rows (3 incorrect), 3 incorrect since the start (classes: status=3), 0 mechanism rows, "
            f"{ignored(4)}; the fourth round needs a mechanism-change row: {ROW_TO_WRITE.format(unit='U7')}\n",
            run.stdout,
        )
        self.assertNotIn("7 audit rows", run.stdout, "the earlier rows are named as ignored, never counted")

    def test_a_mechanism_row_before_the_rule_date_does_not_count(self):
        decisions = [mechanism("2026-10-29T23:11:27Z", "U7", "allowlist of the guarded names")]
        run = self.check(self.store(three_incorrect(), decisions), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn(
            f"U7 refused: 3 audit rows (3 incorrect), 3 incorrect since the start (classes: status=3), 0 mechanism rows, {ignored(1)}; "
            "the fourth round needs a mechanism-change row",
            run.stdout,
        )
        # an earlier row naming two forms is ignored alike: no note asks the coordinator to repair it
        decisions.append(mechanism("2026-10-29T23:12:00Z", "U7", "ast and allowlist"))
        run = self.check(self.store(three_incorrect(), decisions), "U7")
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertNotIn("does not count", run.stdout)
        # a row at the rule date's first second is counted: here it precedes the three rows, so the strikes refuse
        decisions = [mechanism("2026-10-30T00:00:00Z", "U7", "allowlist of the guarded names")]
        run = self.check(self.store(three_incorrect(), decisions), "U7")
        self.assertEqual((1, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn(
            "3 incorrect since the mechanism-change row of 2026-10-30T00:00:00Z (allowlist) (classes: status=3), 1 mechanism rows; "
            "2 strikes of class status since that row need another",
            run.stdout,
        )
        self.assertNotIn("earlier rows ignored", run.stdout)

    def test_a_malformed_store_exits_2_naming_the_file_and_line(self):
        good = [audit("2026-10-30T01:00:00Z", "U7", "correct", "findings=0")]
        short = tsv(LEDGER_HEADER, good) + "2026-10-30T02:00:00Z\tU7\t7\tincorrect\n"
        wrong_header = tsv(LEDGER_HEADER, good).replace("head_sha", "sha")
        bad_ts = tsv(LEDGER_HEADER, [audit("2026-10-30 01:00", "U7", "correct", "findings=0")])
        long_row = DECISIONS_HEADER + "2026-10-30T01:00:00Z\ta\tb\tc\td\te\tf\n"
        for label, ledger_text, decisions_text, message in (
            ("a short row", short, None, "ledger.tsv:3: 4 columns, not 7"),
            ("a wrong header", wrong_header, None, "ledger.tsv:1: the header is "),
            ("a bad ts", bad_ts, None, "ledger.tsv:2: the ts '2026-10-30 01:00' is not YYYY-MM-DDThh:mm:ssZ"),
            ("a long decisions row", None, long_row, "decisions.tsv:2: 7 columns, not 6"),
            ("an empty decisions file", None, "", "decisions.tsv:1: the header is '', not"),
        ):
            with self.subTest(label=label):
                store = self.store(good, ledger_text=ledger_text, decisions_text=decisions_text)
                run = self.check(store, "U7")
                self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
                self.assertIn(f"rounds-check: {store}/{message}", run.stderr)
                self.assertNotIn("Traceback", run.stderr)
        store = self.store(good)
        (store / "ledger.tsv").unlink()
        run = self.check(store, "U7")
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertIn(f"rounds-check: {store}/ledger.tsv: cannot read: No such file or directory", run.stderr)
        run = self.check("--all", self.root / "absent")
        self.assertEqual(2, run.returncode, run.stdout + run.stderr)
        self.assertIn(f"{self.root}/absent/ledger.tsv: cannot read", run.stderr)

    def test_all_checks_every_unit_and_prints_one_line_per_refused_unit(self):
        rows = three_incorrect()
        rows.append(audit("2026-10-30T01:00:00Z", "U8", "correct", "findings=0"))
        rows.append(("2026-10-30T02:00:00Z", "U9", "9", "b" * 40, "ci-red", "coordinator", "no audit"))
        run = self.check("--all", self.store(rows))
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertEqual(run.stdout.count("\n"), 1, run.stdout)
        self.assertIn("rounds-check: U7 refused: 3 audit rows", run.stdout)
        self.assertEqual("rounds-check: 3 units checked, 1 refused\n", run.stderr)
        run = self.check("--all", self.store(rows, [mechanism("2026-10-30T04:00:00Z", "U7", "remove")]))
        self.assertEqual((0, ""), (run.returncode, run.stdout), run.stderr)
        self.assertEqual("rounds-check: 3 units checked, 0 refused\n", run.stderr)

    def test_an_incorrect_row_without_class_is_malformed_only_from_the_rule_date(self):
        old = audit("2026-10-29T23:59:59Z", "U7", "incorrect", "findings=1 P2: the status is lost")
        run = self.check(self.store([old]), "U7")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertIn(
            f"0 audit rows (0 incorrect), 0 incorrect since the start (classes: none), 0 mechanism rows, {ignored(1)}",
            run.stdout,
        )
        for ts in ("2026-10-30T00:00:00Z", "2026-10-30T00:00:01Z"):
            with self.subTest(ts=ts):
                new = audit(ts, "U7", "incorrect", "findings=1 P2: the status is lost")
                run = self.check(self.store([old, new]), "U7")
                self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
                self.assertIn(
                    "ledger.tsv:3: an incorrect row from 2026-10-30T00:00:00Z on whose evidence does not start with "
                    "class=<word>",
                    run.stderr,
                )
        for evidence in ("class=status findings=1", "class=status", "class=a-b_c;x"):
            with self.subTest(evidence=evidence):
                rows = [old, audit("2026-10-30T00:00:01Z", "U7", "incorrect", evidence)]
                run = self.check(self.store(rows), "U7")
                self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        for evidence in ("class= findings=1", "", " class=x", "Class=x"):
            with self.subTest(evidence=evidence):
                rows = [old, audit("2026-10-30T00:00:01Z", "U7", "incorrect", evidence)]
                run = self.check(self.store(rows), "U7")
                self.assertEqual(2, run.returncode, run.stdout + run.stderr)

    def test_usage_is_refused_before_any_read(self):
        store = self.store()
        for args in (
            (),
            (store,),
            (store, "U7", "--all"),
            (store, "u7"),
            (store, "U7b-"),
            ("--all", store, "--base", "main"),
            (store, "U7", "--base", "main", "--head", "x"),
            (store, "--pr", "7"),
            ("--all", store, "--pr", "7"),
            (store, "U7", "--pr", "x"),
            (store, "U7", "--pr", "0"),
            (store, "U7", "--pr", "-7"),
            (store, "U7", "--pr", "7 "),
            (store, "U7", "--pr"),
        ):
            with self.subTest(args=args):
                run = self.check(*args)
                self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
                self.assertIn("usage:", run.stderr)

    def git(self, *args):
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=self.repo,
            env=GIT_ENV,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def commit(self, files, message):
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def repository(self, base_rows, head_files):
        """A base commit on main holding the store, then a head commit on a branch with HEAD_FILES; main checked out."""
        self.repo = self.root / "repo"
        git_init(self.repo, "-b", "main", env=GIT_ENV)
        base = {f"{STORE}/ledger.tsv": tsv(LEDGER_HEADER, base_rows), f"{STORE}/decisions.tsv": DECISIONS_HEADER}
        self.commit(base, "base")
        self.git("switch", "-q", "-c", "records/sync-9")
        head = self.commit(head_files, "head")
        self.git("switch", "-q", "main")
        return head

    def check_at(self, head, **env):
        return self.check("--all", STORE, "--base", "main", "--head", head, env=GIT_ENV | env, cwd=self.repo)

    def test_the_git_form_reads_the_head_s_store_and_skips_a_head_that_changes_neither_file(self):
        rows = three_incorrect()[:2]
        head = self.repository(rows, {f"{STORE}/ledger.tsv": tsv(LEDGER_HEADER, three_incorrect())})
        run = self.check_at(head)
        self.assertEqual(1, run.returncode, run.stdout + run.stderr)
        self.assertIn("rounds-check: U7 refused: 3 audit rows", run.stdout)
        # the head's rows decide: the base's own store (two rows) is allowed, and the checkout is never moved
        self.assertEqual("main", self.git("branch", "--show-current"))
        run = self.check_at("main")
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertIn("are the merge base's blobs; nothing to check", run.stdout)
        # a program pull request that moves no store file is nothing to check, whatever its branch is named
        self.git("switch", "-q", "-c", "feat/x")
        other = self.commit({"src/tool.sh": "a\n"}, "a program head")
        self.git("switch", "-q", "main")
        run = self.check_at(other)
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertIn(
            f"{STORE}/ledger.tsv and decisions.tsv at {other[:12]} are the merge base's blobs; nothing to check",
            run.stdout,
        )

    def test_the_git_form_fails_closed_when_git_cannot_answer(self):
        rows = [audit("2026-10-30T01:00:00Z", "U7", "correct", "findings=0")]
        head = self.repository(rows, {f"{STORE}/decisions.tsv": DECISIONS_HEADER + "x\n"})
        run = self.check_at(head)
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertIn(f"rounds-check: {head[:12]}:{STORE}/decisions.tsv:2: 1 columns, not 6", run.stderr)
        run = self.check_at("0" * 40)
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertIn("rounds-check: git merge-base main 000000000000", run.stderr)
        self.git("switch", "-q", "-c", "records/sync-10")
        shutil.rmtree(self.repo / ".orchestration")
        gone = self.commit({}, "the store removed")
        self.git("switch", "-q", "main")
        run = self.check_at(gone)
        self.assertEqual(2, run.returncode, run.stdout + run.stderr)
        self.assertIn(f"git rev-parse --verify {gone}:{STORE}/ledger.tsv exited 128", run.stderr)
        fakes = self.root / "fakes"
        fakes.mkdir()
        (fakes / "git").write_text("#!/bin/sh\necho 'git: injected failure' >&2\nexit 1\n")
        (fakes / "git").chmod(0o755)
        run = self.check_at(head, PATH=f"{fakes}:{GIT_ENV['PATH']}")
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertIn(f"rounds-check: git merge-base main {head} exited 1: git: injected failure", run.stderr)


if __name__ == "__main__":
    unittest.main()
