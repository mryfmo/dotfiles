"""Exercise scripts/orchestrator/filed-findings.py on a fixture store (regime-cutover U125 round d): the table of every
finding under the weight threshold across the store's verdict files, read by the finding reader of audit-carry.py; a
verdict of a form before the scored reader skipped with a note; a malformed scored verdict, a name of another shape or
a store that cannot be read refused as exit 2 naming the file."""

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/filed-findings.py"
LEVERS = LEVER.parent
HEADER = "unit\thead8\tpriority\tf\ts\tpath:line\trationale"


def finding(priority, path, line, rationale, confidence="high", f=5, s=5):
    """A `## Findings` line as pr-audit.sh's reader writes it since U125 round a."""
    return f"- {priority} ({confidence}) [f{f} s{s}] {path}:{line}: {rationale}"


def verdict_text(*findings, verdict="correct", filed="Filed: 0\n"):
    """A verdict file as the reader writes it since U125 round a; `filed=""` is the reader before it."""
    listed = "\n".join(findings or ("- none",))
    return f"## Findings\n\n{listed}\n\n## Reproduced\n\n- none\n\n## Notes\n\nnone\n\nBlocking: 0\n{filed}Verdict: {verdict}\n"


class FiledFindingsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.store = self.root / "regime-cutover"
        self.verdicts = self.store / "verdicts"
        self.verdicts.mkdir(parents=True)

    def verdict(self, name, *findings, text=None):
        path = self.verdicts / name
        path.write_text(verdict_text(*findings) if text is None else text)
        return path

    def run_list(self, *args, lever=LEVER):
        return subprocess.run(
            [sys.executable, "-I", str(lever), *args], capture_output=True, text=True, timeout=60, check=False
        )

    def test_every_finding_under_the_threshold_is_listed_sorted_by_unit_then_head(self):
        """The table is one row per finding whose weight (f times s) is under 10, whatever its priority, from every
        verdict file of the store, in unit order (U7 before U7b before U12, by number then suffix) then head order; a
        finding at or above the threshold and a `- none` verdict add no row, and the last line is the count."""
        self.verdict(
            "U12-bbbbbbbb.md",
            finding("P3", "docs/a.md", 4, "a wording slip", "low", f=1, s=1),
            finding("P1", "scripts/x.sh", 9, "rare and mild: no run has produced the case", f=1, s=9),
        )
        self.verdict("U7-dddddddd.md")
        self.verdict(
            "U7-aaaaaaaa.md",
            finding("P2", "scripts/y.sh", 12, "the product is the threshold", f=2, s=5),
            finding("P2", "scripts/z.sh", 3, "cosmetic", f=2, s=4),
            finding("P0", "scripts/w.sh", 1, "ten by ten", f=10, s=10),
        )
        self.verdict("U7b-cccccccc.md", finding("P2", "tests/t.py", 70, "a fixture name", "medium", f=3, s=3))
        self.verdict("U7-eeeeeeee-r2.md", finding("P3", "README.md", 1, "a re-audit's note", f=1, s=2))
        run = self.run_list(str(self.store))
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(
            run.stdout.splitlines(),
            [
                HEADER,
                "U7\taaaaaaaa\tP2\t2\t4\tscripts/z.sh:3\tcosmetic",
                "U7\teeeeeeee\tP3\t1\t2\tREADME.md:1\ta re-audit's note",
                "U7b\tcccccccc\tP2\t3\t3\ttests/t.py:70\ta fixture name",
                "U12\tbbbbbbbb\tP3\t1\t1\tdocs/a.md:4\ta wording slip",
                "U12\tbbbbbbbb\tP1\t1\t9\tscripts/x.sh:9\trare and mild: no run has produced the case",
                "filed findings: 5",
            ],
        )

    def test_a_store_without_filed_findings_prints_the_header_and_a_zero(self):
        self.verdict("U7-aaaaaaaa.md")
        self.verdict("U7-bbbbbbbb.md", finding("P1", "scripts/x.sh", 9, "boom", f=2, s=5))
        run = self.run_list(str(self.store) + "/")
        self.assertEqual((0, "", f"{HEADER}\nfiled findings: 0\n"), (run.returncode, run.stderr, run.stdout))

    def test_a_verdict_of_a_form_before_the_scored_reader_is_skipped_with_a_note(self):
        """Merged units predate the scores: the reader writes `Filed: <n>` since U125 round a, so a verdict without
        that line is an earlier reader's (the omp-run route without a `## Findings` section or with a table in it, the
        reader before U125 with the unscored line form), one stderr note naming the file and no refusal, and the
        scored files beside them are still listed."""
        omp_run = self.verdict(
            "U103-11bfd143.md",
            text="- **P2, high confidence** — [tests/unit/t.py:326](t.py:326): the check ignores the shell\n\n"
            "Reproduced:\n\n- both variants passed\n\nVerdict: incorrect\n",
        )
        table = self.verdict(
            "U2-9a795960.md",
            text="## Findings\n\n| id | P | file:line | one line | proposed fix |\n| --- | --- | --- | --- | --- |\n"
            "| F1 | P2 | a.sh:1 | a line | a fix |\n\nVerdict: incorrect\n",
        )
        unscored = self.verdict(
            "U124-184d9e3d.md",
            text=verdict_text(
                "- P1 (high) scripts/orchestrator/pr-threads-check.sh:237: unbounded digits overflow bash arithmetic",
                "- P3 (high) scripts/orchestrator/pr-threads-check.sh:182: a malformed reply names no score",
                filed="",
            ),
        )
        self.verdict("U125-2d91d55c.md", finding("P2", "scripts/orchestrator/audit-carry.py", 1, "a note", f=1, s=3))
        run = self.run_list(str(self.store))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(
            run.stderr.splitlines(),
            [
                f"filed-findings: {path}: skipped, no `Filed: <n>` line, a verdict of a reader before U125"
                for path in (omp_run, unscored, table)
            ],
        )
        self.assertEqual(
            run.stdout.splitlines(),
            [HEADER, "U125\t2d91d55c\tP2\t1\t3\tscripts/orchestrator/audit-carry.py:1\ta note", "filed findings: 1"],
        )

    def test_a_malformed_scored_verdict_is_exit_2_naming_the_file(self):
        """A scored verdict the reader refuses is a malformed store, never a skipped file or an empty list: a score
        outside 1 to 10, a scored line beside an unscored one, `- none` beside a finding, an empty section, a file
        that cannot be read, and a verdict file whose name is not `U<n>-<sha8>.md`; the `Filed: <n>` line makes each
        the scored reader's."""
        good = self.verdict("U7-aaaaaaaa.md", finding("P2", "scripts/z.sh", 3, "cosmetic", f=2, s=4))
        cases = (
            (
                "a score of 0",
                "U8-bbbbbbbb.md",
                verdict_text(finding("P2", "a.sh", 1, "zero", f=0, s=4)),
                "'f0' is not one of 1 to 10",
            ),
            (
                "a score of 11",
                "U8-bbbbbbbb.md",
                verdict_text(finding("P2", "a.sh", 1, "eleven", f=1, s=11)),
                "'s11' is not one of 1 to 10",
            ),
            (
                "an unscored line under the reader's Filed: line",
                "U8-bbbbbbbb.md",
                verdict_text("- P3 (low) b.sh:2: unscored"),
                "U8-bbbbbbbb.md:3: not a Findings line",
            ),
            (
                "a scored line beside an unscored one",
                "U8-bbbbbbbb.md",
                verdict_text(finding("P2", "a.sh", 1, "scored", f=1, s=4), "- P3 (low) b.sh:2: unscored"),
                "U8-bbbbbbbb.md:4: not a Findings line",
            ),
            (
                "- none beside a finding",
                "U8-bbbbbbbb.md",
                verdict_text("- none", finding("P2", "a.sh", 1, "scored", f=1, s=4)),
                "lists '- none' beside a finding line",
            ),
            (
                "an empty section",
                "U8-bbbbbbbb.md",
                "## Findings\n\n## Notes\n\nnone\n\nFiled: 0\nVerdict: correct\n",
                "lists nothing",
            ),
            ("a name of another shape", "U8-bbbbbbb.md", verdict_text(), "not a verdict file name, U<n>-<sha8>.md"),
            ("a name without a unit", "notes.md", verdict_text(), "not a verdict file name, U<n>-<sha8>.md"),
        )
        for name, filename, text, message in cases:
            with self.subTest(name):
                path = self.verdict(filename, text=text)
                run = self.run_list(str(self.store))
                self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
                self.assertIn(f"filed-findings: {path}", run.stderr)
                self.assertIn(message, run.stderr)
                path.unlink()
        unreadable = self.verdict("U8-bbbbbbbb.md", finding("P2", "a.sh", 1, "unreadable", f=1, s=4))
        unreadable.chmod(0)
        self.addCleanup(unreadable.chmod, 0o644)
        run = self.run_list(str(self.store))
        self.assertEqual(
            (2, "", f"filed-findings: {unreadable}: cannot read: Permission denied\n"),
            (run.returncode, run.stdout, run.stderr),
        )
        unreadable.chmod(0o644)
        self.assertEqual(self.run_list(str(self.store)).returncode, 0, good)

    def test_a_verdicts_directory_that_cannot_be_read_is_exit_2_naming_it(self):
        shutil.rmtree(self.verdicts)
        run = self.run_list(str(self.store))
        self.assertEqual((2, ""), (run.returncode, run.stdout), run.stderr)
        self.assertEqual(run.stderr, f"filed-findings: {self.verdicts}: cannot read: No such file or directory\n")

    def test_the_findings_are_read_through_the_carry_lever_beside_the_list(self):
        """One grammar: the list imports `findings_of` from audit-carry.py beside it and parses no finding line of its
        own, so a copy without that reader, or with one the import cannot read, is exit 2 naming the file."""
        copies = self.root / "copies"
        copies.mkdir()
        shutil.copy2(LEVER, copies / "filed-findings.py")
        self.verdict("U7-aaaaaaaa.md", finding("P2", "scripts/z.sh", 3, "cosmetic", f=2, s=4))
        run = self.run_list(str(self.store), lever=copies / "filed-findings.py")
        self.assertEqual(
            (
                2,
                "",
                f"filed-findings: {copies}/audit-carry.py: no audit-carry.py beside the list; the findings are read through it alone\n",
            ),
            (run.returncode, run.stdout, run.stderr),
        )
        for name in ("audit-carry.py", "ledger.py"):
            shutil.copy2(LEVERS / name, copies / name)
        unreadable = copies / "audit-carry.py"
        unreadable.chmod(0)
        self.addCleanup(unreadable.chmod, 0o644)
        run = self.run_list(str(self.store), lever=copies / "filed-findings.py")
        self.assertEqual(
            (2, "", f"filed-findings: {unreadable}: cannot read: Permission denied\n"),
            (run.returncode, run.stdout, run.stderr),
        )
        unreadable.chmod(0o644)
        run = self.run_list(str(self.store), lever=copies / "filed-findings.py")
        self.assertEqual((0, ""), (run.returncode, run.stderr), run.stdout)
        self.assertEqual(run.stdout.splitlines()[-1], "filed findings: 1")

    def test_the_threshold_is_the_merge_gate_s_number(self):
        """The list names the weight threshold once, the number pr-merge.sh assigns once as WEIGHT_THRESHOLD (the
        reader's number, kept equal to AGENTS.md by test_review_rules)."""
        listed = re.findall(r"^WEIGHT_THRESHOLD = (\d+)$", LEVER.read_text(), re.MULTILINE)
        gate = re.findall(r"^WEIGHT_THRESHOLD=(\d+)$", (LEVERS / "pr-merge.sh").read_text(), re.MULTILINE)
        self.assertEqual(len(listed), 1, listed)
        self.assertEqual(len(gate), 1, gate)
        self.assertEqual(listed, gate)

    def test_the_usage_is_checked_first(self):
        run = self.run_list()
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertIn("usage:", run.stderr)
        run = self.run_list(str(self.store), "extra")
        self.assertEqual(run.returncode, 2, run.stderr)


if __name__ == "__main__":
    unittest.main()
