"""Exercise the sweep gate of scripts/orchestrator/pr-merge.sh (regime-cutover U147): a trust-boundary unit, whose brief
in the checkout's own store carries a `TRUST` section (the heading grammar of brief-check.py), merges only with a
`sweep` ledger row of the unit or a fix unit of it at the audited head, read through scripts/orchestrator/ledger.py;
a unit whose brief has no such section merges as before. The fixture is PrLeverTestCase of test_pr_levers (the scratch
checkout, the fake gh, `writes()`), the store built as PrMergeTest builds it plus the brief; no test class is imported,
since unittest discovery would run an imported class a second time."""

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_pr_levers import FOOTER, LEDGER_HEADER, LEVERS, SHA_A, SHA_B, PrLeverTestCase, ledger_row  # noqa: E402

DIGEST = "d" * 64
TRUST_BRIEF = "GOAL\nfixture\n\nTRUST\nTRUST: the unit trusts the one ledger reader.\n"
PLAIN_BRIEF = "GOAL\nfixture\n"
RECEIPT = f"merged pr=7 head={SHA_A} commit={SHA_B} verdict={{ts}}\n"
MERGE_CALL = ["pr", "merge", "7", "--squash", "--match-head-commit", SHA_A]
CHECKS_CALL = ["pr", "checks", "7", "--json", "bucket,name"]
# A reader that answers every question but the sweep one, which fails with a status that is neither 0 nor 2.
FAILING_SWEEP_READER = """import runpy
import sys

if "sweep" in sys.argv:
    sys.stderr.write("ledger: the sweep question could not be read\\n")
    sys.exit(3)
runpy.run_path({real!r}, run_name="__main__")
"""


def sweep_row(head=SHA_A, unit="U71", ts="2026-10-25T09:30:00Z", verdict="sweep"):
    """The advisory row the AGENTS.md Audit sweep rule describes: verdict `sweep`, pr `-`, the swept sha, the skill and
    its pin as the verifier, the findings file under the store as the evidence."""
    return f"{ts}\t{unit}\t-\t{head}\t{verdict}\tsecurity-audit-skill c1c8a8c1\tsweeps/{unit}-{head[:8]}.json\n"


class PrMergeSweepGateTest(PrLeverTestCase):
    """U147: the merge lever refuses a trust-boundary pull request whose unit has no sweep row at the audited head."""

    def setUp(self):
        super().setUp()
        self.records = self.repo / ".orchestration/orchestrate/regime-cutover"
        self.records.mkdir(parents=True)
        self.reader = self.repo / "scripts/orchestrator/ledger.py"
        self.reader.parent.mkdir(parents=True)
        shutil.copy2(LEVERS / "ledger.py", self.reader)
        (self.repo / ".git/info/exclude").write_text(".orchestration/\nscripts/\n")
        self.briefs = self.records / "briefs"
        self.briefs.mkdir()
        self.fixture_brief = self.brief(TRUST_BRIEF)
        self.ledger(ledger_row(SHA_A))
        self.verdict()
        self.body = f"## Summary\n\nProgram-Unit: regime-cutover/U71\n\n{FOOTER}\n"

    def brief(self, text, name="U71-fixture.md"):
        path = self.briefs / name
        path.write_text(text)
        return path

    def ledger(self, *rows):
        (self.records / "ledger.tsv").write_text(LEDGER_HEADER + "".join(rows))

    def verdict(self, head=SHA_A, unit="U71"):
        (self.records / "verdicts").mkdir(exist_ok=True)
        (self.records / f"verdicts/{unit}-{head[:8]}.md").write_text(
            "## Findings\n\n- none\n\n## Reproduced\n\n- the head builds\n\n## Notes\n\nnone\n\nBlocking: 0\nFiled: 0\nVerdict: correct\n"
        )

    def github(self, head=SHA_A):
        self.answer(
            {
                "match": r"^pr view 7 --json state,baseRefName,headRefOid,isDraft$",
                "json": {"state": "OPEN", "baseRefName": "main", "headRefOid": head, "isDraft": False},
            },
            {"match": r"^pr view 7 --json body$", "json": {"body": self.body}},
            {"match": r"^pr checks 7 --json bucket,name$", "json": [{"bucket": "pass", "name": "test"}]},
            {
                "match": r"^pr view 7 --json headRefOid,baseRefName$",
                "json": {"headRefOid": head, "baseRefName": "main"},
            },
            {"match": rf"^pr merge 7 --squash --match-head-commit {head}$", "exit": 0, "stderr": "x"},
            {
                "match": r"^pr view 7 --json state,mergeCommit,baseRefName,headRefOid$",
                "json": {"state": "MERGED", "mergeCommit": {"oid": SHA_B}, "baseRefName": "main", "headRefOid": head},
            },
        )

    def merge(self):
        """One run of the lever against a fresh gh call log, so `writes()` is this run's."""
        self.calls.unlink(missing_ok=True)
        self.github()
        return self.run_lever("pr-merge.sh", "7", "--records", str(self.records))

    def assert_merged(self, run, ts="2026-10-25T09:00:00Z"):
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, RECEIPT.format(ts=ts))
        self.assertEqual(self.writes(), [MERGE_CALL])

    def assert_refused_before_ci(self, run, message):
        self.assert_refused(run, message)
        self.assertNotIn(CHECKS_CALL, self.gh_calls(), "refused before CI is read")

    def test_a_trust_boundary_unit_without_a_sweep_row_is_refused_before_any_write(self):
        run = self.merge()
        self.assert_refused_before_ci(
            run, f"has no sweep row for U71 (or a fix unit of it) at the audited head {SHA_A}"
        )
        self.assertIn(f"the brief {self.fixture_brief} carries the TRUST section", run.stderr)
        self.assertIn("one sweep of the security-audit skill before its pull request merges", run.stderr)
        self.assertEqual(run.stdout, "", "no receipt")

    def test_a_sweep_row_of_the_unit_at_the_head_merges_and_the_receipt_is_the_verdict_row_s(self):
        self.ledger(ledger_row(SHA_A), sweep_row())
        self.assert_merged(self.merge())
        # the word boundary of the reader: `sweep (advisory)` is a sweep row, `sweeping` is not
        self.ledger(ledger_row(SHA_A), sweep_row(verdict="sweep (advisory, 2 findings)"))
        self.assert_merged(self.merge())
        for name, rows in (
            ("a sweep row at another head", (ledger_row(SHA_A), sweep_row(head=SHA_B))),
            ("a verdict that only starts with the letters", (ledger_row(SHA_A), sweep_row(verdict="sweeping"))),
            ("a sweep row of another unit", (ledger_row(SHA_A), sweep_row(unit="U72"))),
            ("a sweep row of a unit whose id starts with U71", (ledger_row(SHA_A), sweep_row(unit="U710"))),
            ("a correct row alone, whatever its evidence says", (ledger_row(SHA_A, evidence="sweep done"),)),
        ):
            with self.subTest(name):
                self.ledger(*rows)
                self.assert_refused_before_ci(self.merge(), "has no sweep row for U71")

    def test_a_fix_unit_s_sweep_row_satisfies_the_gate(self):
        # standing order 24: U71b writes `Program-Unit: regime-cutover/U71`, and its sweep row is under U71b
        self.ledger(ledger_row(SHA_A), sweep_row(unit="U71b"))
        self.assert_merged(self.merge())
        self.ledger(ledger_row(SHA_A), sweep_row(unit="U71bb"))
        self.assert_refused_before_ci(self.merge(), "has no sweep row for U71")

    def test_a_unit_whose_brief_has_no_trust_section_merges_without_a_sweep_row(self):
        self.brief(PLAIN_BRIEF)
        self.assert_merged(self.merge())
        self.assertNotIn("sweep", self.merge().stderr)

    def test_the_mark_is_the_brief_checker_s_heading_grammar(self):
        """brief-check.py:264-268 (`heading()`): the line right-stripped is the section name. The lever reads the same:
        `TRUST` with trailing blanks or a CR is the mark; `TRUST:` and `the TRUST section` inside a sentence are not."""
        for text in ("GOAL\nx\nTRUST   \nthe body\n", "GOAL\nx\nTRUST\r\nthe body\r\n", "GOAL\nx\nTRUST"):
            with self.subTest(text=text):
                self.brief(text)
                self.assert_refused_before_ci(self.merge(), "has no sweep row for U71")
        for text in (
            "GOAL\nx\nTRUST: the unit trusts the reader.\n",
            "GOAL\nx\nThe brief of U1 carries the TRUST section.\n",
            "GOAL\nx\n TRUST\nindented is no heading\n",
            "GOAL\nx\nTRUSTED\n",
        ):
            with self.subTest(text=text):
                self.brief(text)
                self.assert_merged(self.merge())

    def test_the_brief_is_the_one_regular_file_of_the_unit_in_the_checkout_s_store(self):
        """No brief, two briefs, a symlinked or unreadable or empty brief each refuse by name with no write (standing
        order 21: a brief the gate cannot read is never a brief without a TRUST section); a brief of another unit
        whose id shares a prefix with U71 is no match."""
        self.ledger(ledger_row(SHA_A), sweep_row())
        glob = f"{self.briefs}/U71-*.md"
        self.fixture_brief.unlink()
        self.assert_refused_before_ci(self.merge(), f"the brief of U71 is not one file: nothing matches {glob}")
        self.brief(TRUST_BRIEF, "U7-x.md")
        self.brief(TRUST_BRIEF, "U710-x.md")
        self.assert_refused_before_ci(self.merge(), f"the brief of U71 is not one file: nothing matches {glob}")
        self.brief(TRUST_BRIEF)
        self.assert_merged(self.merge())  # the two other units' briefs are not U71's
        second = self.brief(TRUST_BRIEF, "U71-second.md")
        run = self.merge()
        self.assert_refused_before_ci(
            run, f"the brief of U71 is not one file: {self.fixture_brief}, {second} all match {glob}"
        )
        second.unlink()
        elsewhere = self.root / "elsewhere.md"
        elsewhere.write_text(TRUST_BRIEF)
        self.fixture_brief.unlink()
        self.fixture_brief.symlink_to(elsewhere)
        self.assert_refused_before_ci(self.merge(), f"{self.fixture_brief} is not a regular file of this user")
        self.fixture_brief.unlink()
        self.fixture_brief.mkdir()
        self.assert_refused_before_ci(self.merge(), f"{self.fixture_brief} is not a regular file of this user")
        self.fixture_brief.rmdir()
        self.brief("")
        self.assert_refused_before_ci(self.merge(), f"{self.fixture_brief} is empty")
        self.brief(TRUST_BRIEF)
        self.fixture_brief.chmod(0)
        self.addCleanup(self.fixture_brief.chmod, 0o644)
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-0 file")
        self.assert_refused_before_ci(self.merge(), f"cannot read {self.fixture_brief} (read_file exited 2)")

    def test_a_sweep_row_with_a_short_head_is_a_malformed_store_not_a_missing_row(self):
        self.ledger(ledger_row(SHA_A), sweep_row(head=SHA_A[:7]))
        self.assert_refused_before_ci(self.merge(), "ledger.tsv:3: the head_sha of a sweep row is not 40 hex")

    def test_a_reader_that_fails_on_the_sweep_question_is_a_failure_with_no_write(self):
        self.ledger(ledger_row(SHA_A), sweep_row())
        self.reader.write_text(FAILING_SWEEP_READER.format(real=str(LEVERS / "ledger.py")))
        run = self.merge()
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("exited 3 reading", run.stderr)
        self.assertIn("for the sweep row of U71", run.stderr)
        self.assertEqual(self.writes(), [])

    def test_a_carried_head_needs_the_sweep_row_at_the_earlier_head(self):
        """The audited head is the one require_verdict_row set: under a `carried` row it is the earlier head whose
        verdict file the merge reads, so a head moved by pr-update-branch.sh needs no second sweep, and a sweep of the
        carried head alone does not stand for the audited one."""
        earlier = ledger_row(SHA_B)
        carried = ledger_row(
            SHA_A, "carried", ts="2026-10-25T10:00:00Z", evidence=f"carried {SHA_B} {SHA_A} {DIGEST} (audit-carry.py)"
        )
        (self.records / f"verdicts/U71-{SHA_A[:8]}.md").unlink()
        self.verdict(head=SHA_B)
        self.ledger(earlier, carried)
        self.assert_refused_before_ci(
            self.merge(), f"has no sweep row for U71 (or a fix unit of it) at the audited head {SHA_B}"
        )
        self.ledger(earlier, carried, sweep_row(head=SHA_A))
        self.assert_refused_before_ci(self.merge(), f"at the audited head {SHA_B}")
        self.ledger(earlier, carried, sweep_row(head=SHA_B))
        self.assert_merged(self.merge(), ts="2026-10-25T10:00:00Z")
