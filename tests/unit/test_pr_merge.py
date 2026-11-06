"""Exercise the sweep gate of scripts/orchestrator/pr-merge.sh (regime-cutover U147, every unit since U244): a pull
request merges only with a `sweep` ledger row of its unit or a fix unit of it at the audited head, read through
scripts/orchestrator/ledger.py and read by its shape, whatever the unit's brief says; the lever reads no brief and no
brief checker. The admitted row is the exact row of the AGENTS.md Audit sweep rule alone (pr `-`, verifier
`security-audit-skill <pin>` with the pin word a prefix of the manifest's `assets.security-audit-skill.pin`, evidence a
findings file `sweeps/<path>.json` that is a regular file of this user under the store). The fixture is PrLeverTestCase
of test_pr_levers (the scratch checkout, the fake gh, `writes()`, `sweep_row`), the store built as PrMergeTest builds
it plus a plain brief under `briefs/`, which the gate never opens; no test class is imported, since unittest discovery
would run an imported class a second time."""

import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_pr_levers import (  # noqa: E402
    FOOTER,
    LEDGER_HEADER,
    LEVERS,
    MANIFEST_PIN,
    PIN8,
    SHA_A,
    SHA_B,
    PrLeverTestCase,
    ledger_row,
    sweep_row,
)

DIGEST = "d" * 64
# A brief without a `TRUST` section: under U147 such a unit merged with no sweep row; since U244 the gate reads no
# brief, so this unit needs its row like every other.
PLAIN_BRIEF = "GOAL\nfixture\n"
RULE = (
    "every unit and every program milestone gets one sweep of the security-audit skill before its pull request merges"
)
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
# A reader whose exit-0 answer to the sweep question is a given text (U147 round 2, finding 3).
ANSWERING_SWEEP_READER = """import runpy
import sys

if "sweep" in sys.argv:
    sys.stdout.write({answer!r})
    sys.exit(0)
runpy.run_path({real!r}, run_name="__main__")
"""


class PrMergeSweepGateTest(PrLeverTestCase):
    """U244: the merge lever refuses a pull request whose unit has no sweep row at the audited head, whatever its brief."""

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
        self.brief = self.briefs / "U71-fixture.md"
        self.brief.write_text(PLAIN_BRIEF)
        # The findings files the fixture sweep rows name: the gate requires each under `<store>/sweeps/`.
        self.sweeps = self.records / "sweeps"
        self.sweeps.mkdir()
        for unit, head in (("U71", SHA_A), ("U71b", SHA_A), ("U71", SHA_B)):
            self.findings(unit, head)
        self.ledger(ledger_row(SHA_A))
        self.verdict()
        self.body = f"## Summary\n\nProgram-Unit: regime-cutover/U71\n\n{FOOTER}\n"

    def findings(self, unit="U71", head=SHA_A):
        path = self.sweeps / f"{unit}-{head[:8]}.json"
        path.write_text("{}\n")
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

    def test_a_unit_with_a_plain_brief_and_no_sweep_row_is_refused_naming_the_rule(self):
        """U244: the brief has no `TRUST` section, which under U147 merged the unit with no sweep row; now the refusal
        names the unit, the head and the sweep rule, never the brief, and reads the same with no `briefs/` at all."""
        run = self.merge()
        self.assert_refused_before_ci(
            run, f"has no sweep row for U71 (or a fix unit of it) at the audited head {SHA_A}"
        )
        self.assertIn(RULE, run.stderr)
        self.assertNotIn("brief", run.stderr)
        self.assertNotIn("TRUST", run.stderr)
        self.assertEqual(run.stdout, "", "no receipt")
        shutil.rmtree(self.briefs)
        run = self.merge()
        self.assert_refused_before_ci(
            run, f"has no sweep row for U71 (or a fix unit of it) at the audited head {SHA_A}"
        )
        self.assertEqual(run.stdout, "", "no receipt")

    def test_a_unit_with_a_plain_brief_merges_with_a_well_formed_sweep_row(self):
        """U244: the row of the rule admits the merge whatever the brief says, and with the brief or `briefs/` gone,
        or `briefs/` a symlink to a directory outside the store, the outcome is the same: the gate opens no brief."""
        self.ledger(ledger_row(SHA_A), sweep_row())
        self.assert_merged(self.merge())
        self.brief.unlink()
        self.assert_merged(self.merge())
        shutil.rmtree(self.briefs)
        self.assert_merged(self.merge())
        outside = self.root / "outside-briefs"
        outside.mkdir()
        self.briefs.symlink_to(outside)
        self.assert_merged(self.merge())

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

    def test_a_reader_answer_that_is_neither_none_nor_one_row_of_four_fields_is_refused(self):
        """U147 round 2, finding 3: the exit-0 answer is read by its shape, as require_verdict_row reads a row. An
        empty answer, two fields, `none` followed by text, a row with an empty ts and text beside the row each refuse
        naming the reader and the answer, with no write; the reader's own four-field row merges."""
        self.ledger(ledger_row(SHA_A), sweep_row())
        row = sweep_row().rstrip("\n")
        answer_row = "\t".join(row.split("\t")[i] for i in (0, 1, 5, 6))  # ts, unit, verifier, evidence
        for name, answer in (
            ("an empty answer", ""),
            ("two fields", "2026-10-25T09:30:00Z\tU71\n"),
            ("none followed by text on the line", "none (no row)\n"),
            ("none followed by a second line", "none\nledger: a note\n"),
            ("a row with an empty ts", "\tU71\tsecurity-audit-skill c1c8a8c1\tsweeps/x.json\n"),
            ("text beside the row", f"ledger: a warning\n{answer_row}\n"),
        ):
            with self.subTest(name):
                self.reader.write_text(ANSWERING_SWEEP_READER.format(answer=answer, real=str(LEVERS / "ledger.py")))
                run = self.merge()
                self.assert_refused_before_ci(run, f"answered the sweep question for U71 at {SHA_A}")
                self.assertIn(f"{self.reader}", run.stderr)
                self.assertIn(answer.strip() or "nothing", run.stderr)
        self.reader.write_text(ANSWERING_SWEEP_READER.format(answer=answer_row + "\n", real=str(LEVERS / "ledger.py")))
        self.assert_merged(self.merge())

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

    def test_only_the_exact_sweep_row_of_the_rule_admits_the_merge(self):
        """U147 round 4 (Codex thread 4457544811): the row the AGENTS.md Audit sweep rule defines merges, with the full
        40-hex pin or a note after the pin word and after a `;` in the evidence too; a row written by hand (pr `7`,
        verifier `coordinator`, the skill without its pin, evidence under `verdicts/` or with `..`) is a malformed
        store to the reader, exit 2 naming the line and the field with no write, never a sweep and never "no sweep
        row"; and a pin word that is no prefix of the manifest's `assets.security-audit-skill.pin` (`deadbeef`, or the
        pin with one more character) refuses naming both pins."""
        for name, row in (
            ("the first 8 characters of the pin", sweep_row()),
            ("the full pin", sweep_row(verifier=f"security-audit-skill {MANIFEST_PIN}")),
            ("twelve characters of the pin", sweep_row(verifier=f"security-audit-skill {MANIFEST_PIN[:12]}")),
            (
                "notes after the pin word and the evidence",
                sweep_row(
                    verifier=f"security-audit-skill {PIN8} (installed 2026-11-03)",
                    evidence=f"sweeps/U71-{SHA_A[:8]}.json; 2 findings, both filed",
                ),
            ),
        ):
            with self.subTest(name):
                self.ledger(ledger_row(SHA_A), row)
                self.assert_merged(self.merge())
        for name, row, field in (
            # dated before the correct row, so the verdict question (newest row for pr 7) still names that row
            ("pr 7", sweep_row(pr="7", ts="2026-10-25T08:00:00Z"), "the pr of a sweep row is not '-': '7'"),
            (
                "verifier coordinator",
                sweep_row(verifier="coordinator"),
                "the verifier of a sweep row does not begin with 'security-audit-skill <pin>' (the pin 8 or more lowercase hex): 'coordinator'",
            ),
            (
                "the skill alone",
                sweep_row(verifier="security-audit-skill"),
                "the verifier of a sweep row does not begin with 'security-audit-skill <pin>'",
            ),
            (
                "evidence under verdicts/",
                sweep_row(evidence=f"verdicts/U71-{SHA_A[:8]}.md"),
                "the evidence of a sweep row does not name a findings file sweeps/<path>.json under the store",
            ),
            (
                "evidence with ..",
                sweep_row(evidence=f"sweeps/../sweeps/U71-{SHA_A[:8]}.json"),
                "the evidence of a sweep row does not name a findings file sweeps/<path>.json under the store",
            ),
        ):
            with self.subTest(name):
                self.ledger(ledger_row(SHA_A), row)
                run = self.merge()
                self.assert_refused_before_ci(run, f"ledger.tsv:3: {field}")
                self.assertNotIn("has no sweep row", run.stderr)
        for name, pin in (("deadbeef", "deadbeef"), ("the pin with one more character", MANIFEST_PIN + "0")):
            with self.subTest(name):
                self.ledger(ledger_row(SHA_A), sweep_row(verifier=f"security-audit-skill {pin}"))
                run = self.merge()
                self.assert_refused_before_ci(
                    run,
                    f"the sweep row of U71 at {SHA_A} names pin {pin}, which is not a prefix of the manifest's "
                    f"assets.security-audit-skill.pin {MANIFEST_PIN}",
                )
                self.assertIn("agent-config.yaml", run.stderr)

    def test_the_lever_reads_the_row_s_verifier_and_evidence_by_their_shape_whatever_the_reader_answered(self):
        """U147 round 4: the reader refuses a hand-written row, and the lever reads the exit-0 answer by its shape all
        the same (round 2), so a reader whose answer names another verifier, a short pin, an evidence path outside
        `sweeps/`, one with `..` or an empty component is a refusal naming the field, with no write."""
        self.ledger(ledger_row(SHA_A), sweep_row())
        ts = "2026-10-25T09:30:00Z"
        for name, verifier, evidence, message in (
            (
                "verifier coordinator",
                "coordinator",
                f"sweeps/U71-{SHA_A[:8]}.json",
                "names 'coordinator' as its verifier, not the pinned skill",
            ),
            (
                "the skill alone",
                "security-audit-skill",
                f"sweeps/U71-{SHA_A[:8]}.json",
                "names 'security-audit-skill' as its verifier",
            ),
            (
                "a short pin",
                "security-audit-skill c1c8",
                f"sweeps/U71-{SHA_A[:8]}.json",
                "names 'c1c8' as the skill's pin, not 8 or more lowercase hex",
            ),
            (
                "evidence under verdicts/",
                f"security-audit-skill {PIN8}",
                "verdicts/x.md",
                "names 'verdicts/x.md' as its evidence, not a findings file sweeps/<path>.json",
            ),
            (
                "evidence with ..",
                f"security-audit-skill {PIN8}",
                "sweeps/../x.json",
                "the findings file sweeps/../x.json of the sweep row of U71",
            ),
            (
                "an empty component",
                f"security-audit-skill {PIN8}",
                "sweeps//x.json",
                "the findings file sweeps//x.json of the sweep row of U71",
            ),
            (
                "a . component",
                f"security-audit-skill {PIN8}",
                "sweeps/./x.json",
                "the findings file sweeps/./x.json of the sweep row of U71",
            ),
        ):
            with self.subTest(name):
                answer = f"{ts}\tU71\t{verifier}\t{evidence}\n"
                self.reader.write_text(ANSWERING_SWEEP_READER.format(answer=answer, real=str(LEVERS / "ledger.py")))
                run = self.merge()
                self.assert_refused_before_ci(run, message)
                self.assertEqual(run.stdout, "", "no receipt")

    def test_the_findings_file_a_sweep_row_names_must_be_a_regular_file_of_this_user_under_the_store(self):
        """U147 round 4: the evidence path is a file the gate stats under `<store>/sweeps/` (never opened): a missing
        file, a symlink to a file outside the store, a directory, another user's file and a `sweeps/` that is a symlink
        each refuse naming the path with no write; the file restored, the merge goes through."""
        self.ledger(ledger_row(SHA_A), sweep_row())
        path = self.sweeps / f"U71-{SHA_A[:8]}.json"
        named = f"{path}, the findings file the sweep row of U71 at {SHA_A} names, is not a regular file of this user"
        path.unlink()
        self.assert_refused_before_ci(self.merge(), named)
        outside = self.root / "outside.json"
        outside.write_text("{}\n")
        path.symlink_to(outside)
        self.assert_refused_before_ci(self.merge(), named)
        path.unlink()
        path.mkdir()
        self.assert_refused_before_ci(self.merge(), named)
        path.rmdir()
        # another user's file: a hard link keeps the target's owner; a kernel that forbids the link (Linux
        # protected_hardlinks), another filesystem or a root run cannot show this case and skips it
        try:
            os.link("/etc/hosts", path)
        except OSError:
            other = None
        else:
            other = path.stat().st_uid != os.geteuid()
        if other:
            self.assert_refused_before_ci(self.merge(), named)
        if path.exists():
            path.unlink()
        self.findings()
        elsewhere = self.root / "elsewhere-sweeps"
        shutil.move(self.sweeps, elsewhere)
        self.sweeps.symlink_to(elsewhere)
        self.assert_refused_before_ci(
            self.merge(), f"{self.sweeps} is not a directory of this user (a symlink or missing)"
        )
        self.sweeps.unlink()
        shutil.move(elsewhere, self.sweeps)
        self.assert_merged(self.merge())
