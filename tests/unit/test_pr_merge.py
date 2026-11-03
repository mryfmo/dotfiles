"""Exercise the sweep gate of scripts/orchestrator/pr-merge.sh (regime-cutover U147): a trust-boundary unit, whose brief
in the checkout's own store carries a `TRUST` section (as the checker's own `sections()` finds it: round 2 runs
scripts/orchestrator/brief-check.py through one probe, never a loop of the lever's own), merges only with a `sweep`
ledger row of the unit or a fix unit of it at the audited head, read through scripts/orchestrator/ledger.py and read by
its shape; a unit whose brief has no such section merges as before. The probe answers no mark with exit 3, never 1
(round 3: 1 is the interpreter's status for an uncaught exception, and a checker that did not compile had read as "no
mark"), and a checker it cannot load or run is a refusal naming it. The fixture is PrLeverTestCase of test_pr_levers
(the scratch checkout, the fake gh, `writes()`), the store built as PrMergeTest builds it plus the brief, the checker
and its manifest (the checker's import runs its pin self-check); no test class is imported, since unittest discovery
would run an imported class a second time."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_pr_levers import FOOTER, LEDGER_HEADER, LEVERS, ROOT, SHA_A, SHA_B, PrLeverTestCase, ledger_row  # noqa: E402

MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
DIGEST = "d" * 64
TRUST_SENTENCE = "TRUST: the unit trusts the one ledger reader and reads nothing else of the brief."
TRUST_BRIEF = f"GOAL\nfixture\n\nTRUST\n{TRUST_SENTENCE}\n"
PLAIN_BRIEF = "GOAL\nfixture\n"
# Every line end the checker's `splitlines()` knows beyond LF and CRLF (round 2, finding 1: the lever's own loop split
# on LF alone, so a heading after one of these was a section to the checker and no mark to the lever).
DELIMITERS = (("form feed", "\x0c"), ("vertical tab", "\x0b"), ("bare CR", "\r"), ("NEL", "\x85"), ("U+2028", "\u2028"))
NOT_A_BRIEF = "is not a brief: none of GOAL, CHANGE, CONTEXT is a section"
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
# A reader whose exit-0 answer to the sweep question is a given text (round 2, finding 3).
ANSWERING_SWEEP_READER = """import runpy
import sys

if "sweep" in sys.argv:
    sys.stdout.write({answer!r})
    sys.exit(0)
runpy.run_path({real!r}, run_name="__main__")
"""
# A checker the probe cannot load or run (round 3), with the text the refusal names: a syntax error and conflict markers
# never compile, an empty file and `x = 1` have no `sections` (the except tuple's `module.BriefError` is the first
# attribute asked), and an exit at import is the import's own status; none reaches the checker's pin self-check, a
# statement of its module body, so the round-2 probe died with the interpreter's exit 1 and the lever read "no mark".
BROKEN_CHECKERS = (
    ("a syntax error", "def (\n", "SyntaxError"),
    ("conflict markers before the real text", "<<<<<<< HEAD\n{real}", "SyntaxError"),
    ("an empty file", "", "AttributeError"),
    ("a module holding only x = 1", "x = 1\n", "AttributeError"),
    ("an exit 0 at import", "import sys\nsys.exit(0)\n", "exited 0 at import"),
    ("an exit 1 at import", "import sys\nsys.exit(1)\n", "exited 1 at import"),
)
# A python3 first on PATH that exits 1 for the probe's `-c` form and runs the real interpreter for the reader (round 3:
# the lever's exit-1 path, shown without a checker that could produce it).
FAILING_PROBE_PYTHON = """#!{real}
import os
import sys

if sys.argv[1:4] == ["-I", "-S", "-c"]:
    sys.exit(1)
os.execv({real!r}, [{real!r}, *sys.argv[1:]])
"""
PROBE_CONSTANT = re.compile(r"^trust_probe='(.*?)'$", re.DOTALL | re.MULTILINE)


def sweep_row(head=SHA_A, unit="U71", ts="2026-10-25T09:30:00Z", verdict="sweep"):
    """The advisory row the AGENTS.md Audit sweep rule describes: verdict `sweep`, pr `-`, the swept sha, the skill and
    its pin as the verifier, the findings file under the store as the evidence."""
    return f"{ts}\t{unit}\t-\t{head}\t{verdict}\tsecurity-audit-skill c1c8a8c1\tsweeps/{unit}-{head[:8]}.json\n"


def delimited_brief(delimiter, trust=True):
    """A brief whose GOAL holds a trigger word (`shell`) and ends at `delimiter`, then the `TRUST` heading (or a plain
    line), then `CLOSURE` naming `parser-module`: with the heading the checker exits 0, without it 1 (no TRUST section)."""
    heading = f"TRUST\n{TRUST_SENTENCE}\n" if trust else "the body\n"
    return f"GOAL\na shell reader{delimiter}{heading}CLOSURE\nparser-module\n"


class PrMergeSweepGateTest(PrLeverTestCase):
    """U147: the merge lever refuses a trust-boundary pull request whose unit has no sweep row at the audited head."""

    def setUp(self):
        super().setUp()
        self.records = self.repo / ".orchestration/orchestrate/regime-cutover"
        self.records.mkdir(parents=True)
        self.reader = self.repo / "scripts/orchestrator/ledger.py"
        self.reader.parent.mkdir(parents=True)
        shutil.copy2(LEVERS / "ledger.py", self.reader)
        # The checker the lever's trust probe loads by path, and the checkout manifest its import checks its pin in.
        self.checker = self.repo / "scripts/orchestrator/brief-check.py"
        shutil.copy2(LEVERS / "brief-check.py", self.checker)
        (self.repo / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(MANIFEST, self.repo / "home/dot_agents/agent-config.yaml")
        (self.repo / ".git/info/exclude").write_text(".orchestration/\nscripts/\nhome/\n")
        self.briefs = self.records / "briefs"
        self.briefs.mkdir()
        self.fixture_brief = self.brief(TRUST_BRIEF)
        self.ledger(ledger_row(SHA_A))
        self.verdict()
        self.body = f"## Summary\n\nProgram-Unit: regime-cutover/U71\n\n{FOOTER}\n"

    def brief(self, text, name="U71-fixture.md"):
        path = self.briefs / name
        path.write_text(text, encoding="utf-8", newline="")
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

    def check(self, brief):
        """The checker of the clone over `brief`, as the orchestration skill runs it (`python3 -I`, `-S` as the lever)."""
        return subprocess.run(
            [sys.executable, "-I", "-S", str(self.checker), str(brief)],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

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
        """brief-check.py:264-291 (`heading()`, `sections()`): the line right-stripped is the section name. The lever
        reads the same: `TRUST` with trailing blanks or a CR is the mark; `TRUST:` and `the TRUST section` inside a
        sentence are not."""
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

    def test_the_mark_is_read_by_the_checker_s_own_module_whatever_the_line_delimiter(self):
        """Round 2, finding 1: the lever runs the checker's `sections()` through one probe, so a `TRUST` heading after a
        form feed, a vertical tab, a bare CR, NEL or U+2028 is the mark to the lever exactly when it is a TRUST section
        to `brief-check.py` run from the clone (exit 0 with CLOSURE and a trigger word; exit 1 naming the missing
        section without the heading, and then the lever merges)."""
        for name, delimiter in DELIMITERS:
            with self.subTest(name):
                marked = self.brief(delimited_brief(delimiter))
                checked = self.check(marked)
                self.assertEqual((0, "", ""), (checked.returncode, checked.stdout, checked.stderr))
                self.assert_refused_before_ci(
                    self.merge(), f"has no sweep row for U71 (or a fix unit of it) at the audited head {SHA_A}"
                )
                unmarked = self.brief(delimited_brief(delimiter, trust=False))
                checked = self.check(unmarked)
                self.assertEqual(1, checked.returncode, checked.stdout + checked.stderr)
                self.assertIn('GOAL holds "shell"; no TRUST section', checked.stdout)
                self.assert_merged(self.merge())

    def test_a_file_the_checker_cannot_read_as_a_brief_is_refused_naming_it(self):
        """Round 2: the probe's exit 2 is a refusal carrying its line (never "no TRUST section", never the mark): a
        file with none of GOAL, CHANGE or CONTEXT, even one with a `TRUST` heading or an empty one, a heading that
        appears twice (the checker's BriefError) and bytes that are not UTF-8."""
        self.ledger(ledger_row(SHA_A), sweep_row())  # the sweep row is there, so the refusal is the read's alone
        for name, text in (
            ("a TRUST heading and nothing judged", f"TRUST\n{TRUST_SENTENCE}\n"),
            ("SCOPE alone", "SCOPE\n`scripts/orchestrator/pr-merge.sh`\n"),
            ("an empty file", ""),
        ):
            with self.subTest(name):
                self.brief(text)
                self.assert_refused_before_ci(self.merge(), f"{self.fixture_brief} {NOT_A_BRIEF}")
        self.brief("GOAL\nx\nGOAL\ny\nTRUST\n")
        self.assert_refused_before_ci(
            self.merge(), f"cannot read {self.fixture_brief}: GOAL appears twice (lines 1 and 3)"
        )
        self.fixture_brief.write_bytes("GOAL\nfixture caf\xe9\nTRUST\n".encode("latin-1"))
        run = self.merge()
        self.assert_refused_before_ci(run, f"cannot read {self.fixture_brief}: 'utf-8' codec can't decode byte 0xe9")
        self.assertNotIn("Traceback", run.stderr)

    def test_the_brief_is_the_one_regular_file_of_the_unit_in_the_checkout_s_store(self):
        """No brief, two briefs, a symlinked or unreadable brief each refuse by name with no write (standing order 21: a
        brief the gate cannot read is never a brief without a TRUST section); a brief of another unit whose id shares a
        prefix with U71 is no match."""
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
        self.brief(TRUST_BRIEF)
        self.fixture_brief.chmod(0)
        self.addCleanup(self.fixture_brief.chmod, 0o644)
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-0 file")
        self.assert_refused_before_ci(self.merge(), f"cannot read {self.fixture_brief}: [Errno 13] Permission denied")

    def test_a_symlinked_briefs_directory_is_refused_before_the_glob(self):
        """Round 2, finding 2: `briefs/` is checked as `verdicts/` is, so a symlink to a directory outside the store
        holding a plain brief never decides the class; a missing `briefs/` is the same refusal."""
        self.ledger(ledger_row(SHA_A), sweep_row())
        outside = self.root / "outside-briefs"
        outside.mkdir()
        (outside / "U71-x.md").write_text(PLAIN_BRIEF)
        shutil.rmtree(self.briefs)
        self.briefs.symlink_to(outside)
        self.assert_refused_before_ci(
            self.merge(), f"{self.briefs} is not a directory of this user (a symlink or missing)"
        )
        self.briefs.unlink()
        self.assert_refused_before_ci(
            self.merge(), f"{self.briefs} is not a directory of this user (a symlink or missing)"
        )

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
        """Round 2, finding 3: the exit-0 answer is read by its shape, as require_verdict_row reads a row. An empty
        answer, two fields, `none` followed by text, a row with an empty ts and text beside the row each refuse naming
        the reader and the answer, with no write; the reader's own four-field row merges."""
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

    def test_a_checker_the_probe_cannot_load_or_run_is_a_refusal_never_no_mark(self):
        """Round 3 (the audit of da0c2df4, P2 f1 s7): the probe's whole body runs under one try, so a checker that does
        not compile, an empty one, one without `sections` and one that exits at import are each exit 2 with one line
        naming the checker and the exception class or the import exit code, a refusal with no write; the round-2 probe
        died with the interpreter's exit 1, which the lever read as "no mark", and the TRUST brief merged with no sweep
        row. The checker's own pin self-check (its exit 2 and line) passes through as before, and the real checker
        over a plain brief still merges."""
        real = (LEVERS / "brief-check.py").read_text()
        for name, text, reason in BROKEN_CHECKERS:
            with self.subTest(name):
                self.checker.write_text(text.format(real=real))
                run = self.merge()
                self.assert_refused_before_ci(run, f"cannot load {self.checker}: {reason}")
                self.assertNotIn("Traceback", run.stderr)
                self.assertEqual(run.stdout, "", "no receipt")
        self.checker.write_text(real + "# one more line\n")
        run = self.merge()
        self.assert_refused_before_ci(run, f"of {self.checker} differs from the pin in")
        self.assertNotIn("cannot load", run.stderr)
        shutil.copy2(LEVERS / "brief-check.py", self.checker)
        self.brief(PLAIN_BRIEF)
        self.assert_merged(self.merge())

    def test_a_probe_that_exits_1_is_a_failure_with_no_write(self):
        """Round 3: exit 1 is the interpreter's own status for an uncaught exception, so the lever never reads it as
        "no mark" (the round-2 lever did, and merged); a python3 first on PATH that exits 1 for the probe's `-c` form
        makes the lever fail (exit 1) naming the probe, the brief, the checker and the status, with no write."""
        real = shutil.which("python3", path=self.env["PATH"])
        self.assertIsNotNone(real, "the lever needs a python3 on PATH")
        fake_bin = self.root / "fake-python"
        fake_bin.mkdir()
        fake = fake_bin / "python3"
        fake.write_text(FAILING_PROBE_PYTHON.format(real=real))
        fake.chmod(0o755)
        self.env["PATH"] = f"{fake_bin}:{self.env['PATH']}"
        run = self.merge()
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn(f"the trust probe over {self.fixture_brief} ({self.checker}) exited 1", run.stderr)
        self.assertNotIn("refused:", run.stderr)
        self.assertEqual(run.stdout, "", "no receipt")
        self.assertEqual(self.writes(), [])

    def test_the_probe_s_statuses_are_0_3_and_2_never_1(self):
        """The lever's one `trust_probe` constant, run as the lever runs it: 0 for the mark, 3 for a brief without it,
        2 and one stderr line (no traceback) for a checker it cannot load or run; 1 is never its own answer."""
        probes = PROBE_CONSTANT.findall((LEVERS / "pr-merge.sh").read_text())
        self.assertEqual(len(probes), 1, "one single-quoted constant")
        probe = probes[0]

        def ask(brief):
            run = subprocess.run(
                [sys.executable, "-I", "-S", "-c", probe, str(brief), str(self.checker)],
                cwd=self.repo,
                env=self.env,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            return run.returncode, run.stdout, run.stderr

        self.assertEqual((0, "", ""), ask(self.fixture_brief))
        self.assertEqual((3, "", ""), ask(self.brief(PLAIN_BRIEF, "U72-plain.md")))
        real = (LEVERS / "brief-check.py").read_text()
        for name, text, reason in BROKEN_CHECKERS:
            with self.subTest(name):
                self.checker.write_text(text.format(real=real))
                status, out, err = ask(self.fixture_brief)
                self.assertEqual((2, ""), (status, out), err)
                self.assertTrue(err.startswith(f"brief-check: cannot load {self.checker}: "), err)
                self.assertIn(reason, err)
                self.assertEqual(err.count("\n"), 1, "one line")
                self.assertNotIn("Traceback", err)
