"""Exercise the sweep gate and the CI gate of scripts/orchestrator/pr-merge.sh. The sweep gate (regime-cutover U147,
every unit since U244): a pull request merges only with a `sweep` ledger row of its unit or a fix unit of it at the
audited head, read through scripts/orchestrator/ledger.py and read by its shape, whatever the unit's brief says; the
lever reads no brief and no brief checker. The admitted row is the exact row of the AGENTS.md Audit sweep rule alone
(pr `-`, verifier `security-audit-skill <pin>` with the pin word a prefix of the manifest's
`assets.security-audit-skill.pin`, evidence a findings file `sweeps/<path>.json` that is a regular file of this user
under the store). The CI gate (U330): every check of the lever's REQUIRED_CHECKS, the main ruleset's required
contexts, must be listed by `gh pr checks` with bucket `pass`, so a head whose `pull_request` workflows never ran is
refused naming the missing checks, and the array is held equal to the contexts recorded in test_pr_levers. The fixture
is PrLeverTestCase of test_pr_levers (the scratch checkout, the fake gh, `writes()`, `sweep_row`, the green listing),
the store built as PrMergeTest builds it plus a plain brief under `briefs/`, which the gate never opens; no test class
is imported, since unittest discovery would run an imported class a second time."""

import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_pr_levers import (  # noqa: E402
    FOOTER,
    GREEN_CHECKS,
    LEDGER_HEADER,
    LEVERS,
    MANIFEST_PIN,
    PIN8,
    RULESET_REQUIRED_CHECKS,
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
            {"match": r"^pr checks 7 --json bucket,name$", "json": GREEN_CHECKS},
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


# The lever's REQUIRED_CHECKS array as written: `REQUIRED_CHECKS=(`, one single-quoted name per line, `)`.
REQUIRED_CHECKS_CONSTANT = re.compile(r"^REQUIRED_CHECKS=\(\n((?:    '[^'\n]*'\n)+)\)$", re.MULTILINE)
# The checks PR 708's head 792604f9 had on 2026-11-07 (decisions row 2026-11-07T01:45:00Z): `regime`, a
# `pull_request_target` workflow, GitGuardian, and CodeRabbit skipping; none of the `pull_request` workflows, which
# GitHub runs on the merge ref, so a pull request that conflicts with main gets none of them.
PR_708_CHECKS = [
    {"bucket": "pass", "name": "regime"},
    {"bucket": "pass", "name": "GitGuardian Security Checks"},
    {"bucket": "skipping", "name": "CodeRabbit"},
]
VERDICT_TEXT = "## Findings\n\n- none\n\n## Reproduced\n\n- the head builds\n\n## Notes\n\nnone\n\nBlocking: 0\nFiled: 0\nVerdict: correct\n"


def listing(**buckets):
    """The green listing with the named required checks' buckets replaced (`validate="skipping"`); a name with a
    space is passed through a dict (`listing(**{"test (ubuntu-24.04, client)": "pending"})`)."""
    return [{"bucket": buckets.get(check["name"], check["bucket"]), "name": check["name"]} for check in GREEN_CHECKS]


class PrMergeRequiredChecksTest(PrLeverTestCase):
    """U330: the CI gate requires the main ruleset's eight contexts by name. On 2026-11-07 PR 708's head 792604f9
    conflicted with main, GitHub ran none of its `pull_request` workflows, and `gh pr checks` listed three passing
    checks (`regime`, GitGuardian, CodeRabbit skipping); the gate at 668ba887 (at least one check, every bucket `pass`
    or `skipping`) would have merged it with no test leg run. Now every REQUIRED_CHECKS name must be listed with bucket
    `pass`: an absent one, or one listed `skipping`, is refused naming it apart from the red ones (`CI has no result
    for: ...`); a red one refuses as before; every required check `pass` plus extras merges as before. The store holds
    the correct row, its verdict file and the sweep row, so the CI read is the gate that decides."""

    def setUp(self):
        super().setUp()
        self.records = self.repo / ".orchestration/orchestrate/regime-cutover"
        self.records.mkdir(parents=True)
        reader = self.repo / "scripts/orchestrator/ledger.py"
        reader.parent.mkdir(parents=True)
        shutil.copy2(LEVERS / "ledger.py", reader)
        (self.repo / ".git/info/exclude").write_text(".orchestration/\nscripts/\n")
        (self.records / "sweeps").mkdir()
        (self.records / f"sweeps/U71-{SHA_A[:8]}.json").write_text("{}\n")
        (self.records / "ledger.tsv").write_text(LEDGER_HEADER + ledger_row(SHA_A) + sweep_row())
        (self.records / "verdicts").mkdir()
        (self.records / f"verdicts/U71-{SHA_A[:8]}.md").write_text(VERDICT_TEXT)
        self.body = f"## Summary\n\nProgram-Unit: regime-cutover/U71\n\n{FOOTER}\n"

    def merge(self, checks):
        """One run of the lever with `checks` as the `gh pr checks` listing, against a fresh gh call log."""
        self.calls.unlink(missing_ok=True)
        self.answer(
            {
                "match": r"^pr view 7 --json state,baseRefName,headRefOid,isDraft$",
                "json": {"state": "OPEN", "baseRefName": "main", "headRefOid": SHA_A, "isDraft": False},
            },
            {"match": r"^pr view 7 --json body$", "json": {"body": self.body}},
            {"match": r"^pr checks 7 --json bucket,name$", "json": checks},
            {
                "match": r"^pr view 7 --json headRefOid,baseRefName$",
                "json": {"headRefOid": SHA_A, "baseRefName": "main"},
            },
            {"match": rf"^pr merge 7 --squash --match-head-commit {SHA_A}$", "exit": 0, "stderr": "x"},
            {
                "match": r"^pr view 7 --json state,mergeCommit,baseRefName,headRefOid$",
                "json": {"state": "MERGED", "mergeCommit": {"oid": SHA_B}, "baseRefName": "main", "headRefOid": SHA_A},
            },
        )
        return self.run_lever("pr-merge.sh", "7", "--records", str(self.records))

    def assert_merged(self, run):
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, RECEIPT.format(ts="2026-10-25T09:00:00Z"))
        self.assertEqual(self.writes(), [MERGE_CALL])

    def assert_no_result(self, run, named):
        """Refused after the checks read, with no write and no receipt, the missing checks named in the array's order
        and the red-check refusal absent."""
        self.assert_refused(run, f"CI has no result for: {named}; every check of REQUIRED_CHECKS")
        calls = [call[: len(CHECKS_CALL)] for call in self.gh_calls()]  # the recorded call carries its --jq too
        self.assertIn(CHECKS_CALL, calls, "the refusal is the CI gate's, after the checks read")
        self.assertNotIn("CI is not green", run.stderr)
        self.assertEqual(run.stdout, "", "no receipt")

    def test_the_pr_708_listing_is_refused_naming_the_required_checks_it_lacks(self):
        """The PR 708 case: three passing checks, none of them a `pull_request` workflow's. The seven required checks
        the listing lacks are named bare, in the array's order; `regime`, listed and passing, is not among them; no
        check is red, so the refusal is the named-check one alone, with no write."""
        run = self.merge(PR_708_CHECKS)
        absent = [name for name in RULESET_REQUIRED_CHECKS if name != "regime"]
        self.assertEqual(len(absent), 7)
        self.assert_no_result(run, ", ".join(absent))
        named = run.stderr.split("CI has no result for: ")[1].split(";")[0]
        self.assertNotIn("regime", named)
        self.assertNotIn("GitGuardian", named)
        self.assertNotIn("CodeRabbit", named)

    def test_every_required_check_passing_plus_extras_merges_as_before(self):
        """The listing of a pull request whose workflows all ran: the eight required checks `pass`, GitGuardian `pass`,
        CodeRabbit and a docs job `skipping`, in any order."""
        extras = [
            {"bucket": "pass", "name": "GitGuardian Security Checks"},
            {"bucket": "skipping", "name": "CodeRabbit"},
            {"bucket": "skipping", "name": "docs"},
        ]
        self.assert_merged(self.merge([*GREEN_CHECKS, *extras]))
        self.assert_merged(self.merge([*extras, *reversed(GREEN_CHECKS)]))
        self.assert_merged(self.merge(GREEN_CHECKS))

    def test_a_required_check_that_is_skipping_is_no_result_and_a_name_is_compared_whole(self):
        """`skipping` satisfies only a check that is not required: each required check skipping in turn is refused
        naming it with its bucket; a check whose name only starts with a required one (`test` for `test (ubuntu-24.04,
        client)`, `validate (ubuntu-24.04)` for `validate`) is no result for it; a required name listed twice, `pass`
        and `skipping`, is no result either."""
        for name in RULESET_REQUIRED_CHECKS:
            with self.subTest(name):
                self.assert_no_result(self.merge(listing(**{name: "skipping"})), f"{name}=skipping")
        renamed = [
            {
                "bucket": "pass",
                "name": {"test (ubuntu-24.04, client)": "test", "validate": "validate (ubuntu-24.04)"}.get(
                    check["name"], check["name"]
                ),
            }
            for check in GREEN_CHECKS
        ]
        self.assert_no_result(self.merge(renamed), "test (ubuntu-24.04, client), validate")
        twice = [*GREEN_CHECKS, {"bucket": "skipping", "name": "regime"}]
        self.assert_no_result(self.merge(twice), "regime=skipping")
        self.assert_no_result(self.merge(list(reversed(twice))), "regime=skipping")

    def test_a_required_check_that_is_pending_or_red_refuses_as_before_naming_the_red_check(self):
        """A pending, failed or cancelled required check is the red-check refusal of U71, named with its bucket, and
        the named-check refusal does not follow it; an empty listing is still `no check is reported`."""
        for bucket in ("pending", "fail", "cancel"):
            with self.subTest(bucket):
                run = self.merge(listing(**{"test (ubuntu-24.04, client)": bucket}))
                self.assert_refused(run, f"CI is not green on the head {SHA_A}: test (ubuntu-24.04, client)={bucket}")
                self.assertNotIn("CI has no result", run.stderr)
                self.assertEqual(run.stdout, "", "no receipt")
        run = self.merge([])
        self.assert_refused(run, f"no check is reported on the head {SHA_A}")
        self.assertNotIn("CI has no result", run.stderr)

    def test_the_lever_s_required_checks_equal_the_ruleset_s_required_contexts(self):
        """REQUIRED_CHECKS, read from the lever's text as one array of single-quoted names, equals the contexts of
        ruleset 24397953 recorded in test_pr_levers from the 2026-11-07T03:34Z measurement, name for name and in order,
        with no name twice; the deployed copy holds the same bytes; the README's policy-table row for the lever states
        the rule, naming the array and the four job names. A ruleset edit is a change to the lever and to the recorded
        tuple, and a drift between them fails here, never at a merge."""
        text = (LEVERS / "pr-merge.sh").read_text()
        blocks = REQUIRED_CHECKS_CONSTANT.findall(text)
        self.assertEqual(len(blocks), 1, "one REQUIRED_CHECKS array")
        names = [line.strip()[1:-1] for line in blocks[0].splitlines()]
        self.assertEqual(names, list(RULESET_REQUIRED_CHECKS))
        self.assertEqual(len(set(names)), len(names), "no name twice")
        deployed = LEVERS.parents[1] / "home/dot_local/bin/common/executable_pr-merge.sh"
        self.assertEqual(deployed.read_bytes(), (LEVERS / "pr-merge.sh").read_bytes())
        readme = (LEVERS / "README.md").read_text()
        rows = [line for line in readme.splitlines() if line.startswith("| `~/.local/bin/common/pr-merge.sh *`")]
        self.assertEqual(len(rows), 1, "one policy-table row for the lever")
        for word in ("U330", "REQUIRED_CHECKS", "public-bootstrap", "regime", "test", "validate", "PR 708"):
            self.assertIn(word, rows[0])
