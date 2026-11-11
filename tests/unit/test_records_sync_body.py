"""Exercise the sync body writer of scripts/orchestrator/records-sync.sh (regime-cutover U445, round 2 U445b).

The lever's dry entry point `records-sync.sh [--unit U<n>] --render-body <rows-file> <n> <program> <form> <units-line>
<decisions-line>` prints the pull request's body to stdout with no git or gh call: the one writer the real sync writes
its `--body-file` through. The rows file holds one NUL-terminated entry per changed path, `copy` or `deletion`, a tab
and the published path, read as the lever reads its other listings. The tests run the checkout's lever in place (its
self-check reads the checkout's manifest) under a scratch HOME and assert the body's shape: `## Summary`, the
`## Threat table` with one row per changed path whatever their number (the kind's risk-and-bound sentence, at most 90
characters; the evidence cell `scan clean; <reader> at the head` naming the reader that refuses a malformed record of
that kind, `scan clean; text no gate reads` where none exists, `the diff of this sync; scan clean` for an executable
record) and one row for the gates that read the carried records, the byte bound (a body over 122880 bytes is refused
and nothing is printed), the clean-relative-path rule on every row, the failed-read and NUL refusals, the strict
option grammar (only `--unit` before `--render-body`), `## Contract`, and the `Program-Unit:` line as the last line
before the footer.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/records-sync.sh"
FOOTER = "🤖 Generated with [Claude Code](https://claude.com/claude-code)"
HEADER = "| Path or effect | Change | Risk and bound | Status | Evidence |"
GATES_ROW = (
    "| the orchestrator's gates (pr-merge.sh, rounds-check.py, pr-audit.sh) "
    "| read the carried ledger, decisions and dispositions | a row that admits a merge or hides a round | closed "
    "| every ledger row by its lever; mechanism-change rows name one form; rounds-check.py --all 0 refused |"
)
COPY = "masked copy"
LIMIT = 122880
PREFIX = ".orchestration/orchestrate/prog"
NO_READER = "scan clean; text no gate reads"
EXECUTABLE_RISK = "executable record: a script run by hand; read by no gate; its change is reviewed as code"
EXECUTABLE_EVIDENCE = "the diff of this sync; scan clean"
# One path of every kind the lever's table names, with the kind's risk-and-bound sentence and the evidence cell of a
# copy (round 2: the reader that refuses a malformed record of the kind, run by the regime workflow's checks at the
# head, is the evidence; a kind no gate reads stays closed by the scan alone; an executable record is reviewed as code).
KINDS = (
    (
        "briefs/U1-x.md",
        "text the workers read; brief-check.py refuses a malformed brief",
        "scan clean; brief-check.py at the head",
    ),
    ("verdicts/U1-head.md", "text the coordinator reads for the ledger row; text; no reader", NO_READER),
    (
        "sweeps/U1-findings.json",
        "JSON the merge gate names; a JSON parse refuses a malformed file",
        "scan clean; a JSON parse at the head",
    ),
    ("sweeps/U1-notes.md", "text the merge gate names and never opens; text; no reader", NO_READER),
    ("handoff/01-notes.md", "text for the operator and the next coordinator; text; no reader", NO_READER),
    ("handouts/02-login.md", "text for the operator and the next coordinator; text; no reader", NO_READER),
    (
        "ledger.tsv",
        "read by pr-merge.sh and rounds-check.py; ledger.py refuses a malformed row",
        "scan clean; ledger.py and rounds-check.py --all at the head",
    ),
    (
        "decisions.tsv",
        "rounds-check.py reads the mechanism-change rows and refuses a malformed one",
        "scan clean; rounds-check.py --all at the head",
    ),
    (
        "dispositions.tsv",
        "pr-merge.sh reads the dispositions and refuses a malformed row",
        "scan clean; pr-merge.sh's dispositions reader at the head",
    ),
    ("units.tsv", "the unit rows the coordinator reads; text; no reader", NO_READER),
    (
        "tests/use-cases.tsv",
        "a use-case table check-tables.py validates; a malformed row is refused",
        "scan clean; check-tables.py at the head",
    ),
    ("tests/run-host-rows.py", EXECUTABLE_RISK, EXECUTABLE_EVIDENCE),
    ("tests/host-row-notes.txt", "a record of the program store; text; no reader", NO_READER),
    ("overview.md", "a record of the program store; text; no reader", NO_READER),
)


def copy_row(path, risk, evidence):
    return f"| `{path}` | {COPY} | {risk} | closed | {evidence} |"


def deletion_row(path, risk, evidence):
    return f"| `{path}` | deletion | {risk} | closed | {evidence.replace('scan clean', 'never read, only removed')} |"


class RenderBodyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="records-sync-body-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "home").mkdir()
        (self.root / "tmp").mkdir()
        self.env = {
            "PATH": os.environ["PATH"],
            "HOME": str(self.root / "home"),
            "TMPDIR": str(self.root / "tmp"),
            "LC_ALL": "C",
        }

    def rows_file(self, rows, name="rows"):
        """The rows file: one NUL-terminated `<change>TAB<path>` entry per row, as the lever writes it."""
        path = self.root / name
        path.write_bytes(b"".join(f"{change}\t{path_}\0".encode() for change, path_ in rows))
        return path

    def run_render(
        self, rows, n="7", program="prog", form="checkout", units="", decisions="", unit=None, env=None, before=()
    ):
        rows_path = rows if isinstance(rows, Path) else self.rows_file(rows)
        args = [str(LEVER), *before]
        if unit is not None:
            args += ["--unit", unit]
        args += ["--render-body", str(rows_path), n, program, form, units, decisions]
        return subprocess.run(
            args,
            cwd=self.root,
            env={**self.env, **(env or {})},
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

    def render(self, rows, **kwargs):
        run = self.run_render(rows, **kwargs)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(run.stderr, "", "the dry form prints nothing but the body")
        return run.stdout

    def refused(self, rows, message, **kwargs):
        """Run the dry form and assert the refusal: exit 2, `refused:` and the message on stderr, nothing on stdout."""
        run = self.run_render(rows, **kwargs)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("refused:", run.stderr)
        self.assertIn(message, run.stderr)
        self.assertEqual(run.stdout, "")
        return run.stderr

    def table_rows(self, body):
        """The rows of the Threat table after its header and separator lines."""
        section = body[body.index("## Threat table\n") : body.index("## Contract\n")]
        lines = section.splitlines()
        header = lines.index(HEADER)
        self.assertEqual(lines[header + 1], "| --- | --- | --- | --- | --- |")
        rows = []
        for line in lines[header + 2 :]:
            if not line.startswith("|"):
                break
            rows.append(line)
        return rows

    def test_a_listing_of_mixed_kinds_gives_one_row_per_path_with_the_kind_s_sentence(self):
        rows = [("copy", f"{PREFIX}/{rel}") for rel, _, _ in KINDS]
        body = self.render(rows, units="U2 U3", decisions="2026-11-11T00:00:00Z")
        self.assertIn(f"Records sync 7 of `prog` ({len(KINDS)} file(s))", body)
        self.assertIn("- units.tsv rows added or changed: U2 U3\n", body)
        self.assertIn("- decisions.tsv rows added or changed: 2026-11-11T00:00:00Z\n", body)
        self.assertLess(body.index("## Summary\n"), body.index("## Threat table\n"))
        self.assertLess(body.index("## Threat table\n"), body.index("## Contract\n"))
        table = self.table_rows(body)
        expected = [copy_row(f"{PREFIX}/{rel}", risk, evidence) for rel, risk, evidence in KINDS] + [GATES_ROW]
        self.assertEqual(table, expected)
        for _, risk, _ in KINDS:
            self.assertLessEqual(len(risk), 90, risk)
        rule = body[body.index("## Threat table\n") : body.index(HEADER)]
        self.assertIn("One row per changed path, whatever their number", rule)
        self.assertIn("122880", rule, "the byte bound is stated above the table")
        self.assertIn("`scan clean`", rule, "the shared explanation of the evidence cells stands once, above the table")
        self.assertIn("at the head", rule)
        self.assertIn("executable record", rule)

    def test_a_removed_path_is_a_deletion_row(self):
        rows = [
            ("deletion", f"{PREFIX}/briefs/U9-gone.md"),
            ("deletion", f"{PREFIX}/tests/old-check.py"),
            ("copy", f"{PREFIX}/units.tsv"),
        ]
        table = self.table_rows(self.render(rows))
        self.assertEqual(
            table[0],
            f"| `{PREFIX}/briefs/U9-gone.md` | deletion | text the workers read; brief-check.py refuses a malformed brief"
            " | closed | never read, only removed; brief-check.py at the head |",
        )
        self.assertEqual(
            table[1],
            f"| `{PREFIX}/tests/old-check.py` | deletion | {EXECUTABLE_RISK} | closed "
            "| the diff of this sync; never read, only removed |",
        )
        self.assertEqual(table[2].split(" | ")[1], COPY)
        self.assertEqual(table[-1], GATES_ROW)

    def test_above_150_paths_the_table_still_holds_one_row_per_path(self):
        """Round 2 (U445b, P1 f2 s7): the rule is one row per changed path, always; the bound is the body's bytes, not a
        row count, so 151 paths give 151 rows and the gates row."""
        rows = [("copy", f"{PREFIX}/briefs/U{i}-brief.md") for i in range(150)] + [("deletion", f"{PREFIX}/ledger.tsv")]
        body = self.render(rows)
        table = self.table_rows(body)
        self.assertEqual(len(table), 152, "151 paths: one row each, plus the gates row")
        self.assertEqual(table[-1], GATES_ROW)
        self.assertEqual(table[:150], [copy_row(path, KINDS[0][1], KINDS[0][2]) for _, path in rows[:150]])
        self.assertEqual(table[150], deletion_row(f"{PREFIX}/ledger.tsv", KINDS[6][1], KINDS[6][2]))
        self.assertIn("(151 file(s))", body)
        self.assertNotIn("paths)", body, "no kind summary row")
        self.assertLess(len(body.encode()), LIMIT)

    def test_a_body_over_the_byte_limit_is_refused_with_nothing_printed(self):
        """Round 2 (U445b, P2 f2 s6): the writer measures the rendered body and refuses above 122880 bytes; an ordinary
        sync of 150 paths with long names stays well under it."""
        ordinary = [("copy", f"{PREFIX}/verdicts/U{i}-{'x' * 100}.md") for i in range(150)]
        self.assertLess(len(self.render(ordinary).encode()), LIMIT)
        long_paths = [("copy", f"{PREFIX}/briefs/U{i}-{'x' * 600}.md") for i in range(200)]
        stderr = self.refused(long_paths, "bytes over the 122880-byte limit the regime workflow can read")
        self.assertIn("sync in smaller batches or shorten the evidence", stderr)
        size = int(stderr.split("the body would be ")[1].split(" bytes over")[0])
        self.assertGreater(size, LIMIT)

    def test_an_executable_record_is_named_as_one(self):
        """Round 2 (U445b, P1 f2 s8): `tests/run-host-rows.py` runs shell commands; every `*.py`, `*.sh`, `*.cjs`, `*.js`
        and `*.mjs` path is an executable record whose change is reviewed as code, under `tests/` or anywhere."""
        rows = [
            ("copy", f"{PREFIX}/tests/run-host-rows.py"),
            ("copy", f"{PREFIX}/tests/check-tables.py"),
            ("copy", f"{PREFIX}/tests/run.sh"),
            ("copy", f"{PREFIX}/tool.sh"),
            ("copy", f"{PREFIX}/handoff/probe.cjs"),
            ("copy", f"{PREFIX}/sweeps/U1-run.js"),
            ("copy", f"{PREFIX}/briefs/x.mjs"),
            ("copy", f"{PREFIX}/tests/use-cases.tsv"),
            ("copy", f"{PREFIX}/tests/host-row-notes.txt"),
        ]
        table = self.table_rows(self.render(rows))
        for row, (_, path) in zip(table[:7], rows[:7]):
            self.assertEqual(row, copy_row(path, EXECUTABLE_RISK, EXECUTABLE_EVIDENCE))
        self.assertEqual(table[7], copy_row(rows[7][1], KINDS[10][1], KINDS[10][2]))
        self.assertEqual(table[8], copy_row(rows[8][1], KINDS[12][1], KINDS[12][2]))
        self.assertEqual(table[-1], GATES_ROW)

    def test_the_evidence_cell_names_the_reader_of_the_kind(self):
        """Round 2 (U445b, P1 f10 s5): the selector of a records sync is the reader that refuses a malformed record,
        run by the regime workflow's checks at the head; a kind without one is closed by the scan alone."""
        rows = [("copy", f"{PREFIX}/{rel}") for rel, _, _ in KINDS]
        table = self.table_rows(self.render(rows))
        evidence = {rel: row.split(" | ")[4].rstrip(" |") for (rel, _, _), row in zip(KINDS, table)}
        self.assertEqual(evidence["briefs/U1-x.md"], "scan clean; brief-check.py at the head")
        self.assertEqual(evidence["ledger.tsv"], "scan clean; ledger.py and rounds-check.py --all at the head")
        self.assertEqual(evidence["decisions.tsv"], "scan clean; rounds-check.py --all at the head")
        self.assertEqual(evidence["dispositions.tsv"], "scan clean; pr-merge.sh's dispositions reader at the head")
        self.assertEqual(evidence["tests/use-cases.tsv"], "scan clean; check-tables.py at the head")
        self.assertEqual(evidence["sweeps/U1-findings.json"], "scan clean; a JSON parse at the head")
        for rel in ("verdicts/U1-head.md", "handoff/01-notes.md", "handouts/02-login.md", "units.tsv", "overview.md"):
            self.assertEqual(evidence[rel], NO_READER, rel)
        self.assertEqual(evidence["tests/run-host-rows.py"], EXECUTABLE_EVIDENCE)
        for cell in evidence.values():
            self.assertTrue(
                cell.startswith("scan clean; ") or cell == EXECUTABLE_EVIDENCE, f"the fixed short form: {cell}"
            )

    def test_a_path_that_is_not_a_clean_relative_path_is_refused(self):
        """Round 2 (U445b, P2 f2 s4): `prog/../other/units.tsv` is not inside the program's prefix; every row path is a
        clean relative path (no empty, `.` or `..` component, no leading `/`) under the prefix."""
        good = ("copy", f"{PREFIX}/units.tsv")
        for path in (
            f"{PREFIX}/../other/units.tsv",
            f"{PREFIX}/briefs/../../other/x.md",
            f"{PREFIX}/./units.tsv",
            f"{PREFIX}//units.tsv",
            f"/{PREFIX}/units.tsv",
            f"{PREFIX}/briefs/",
            f"{PREFIX}/..",
            f"{PREFIX}/.",
            f"./{PREFIX}/units.tsv",
        ):
            with self.subTest(path=path):
                stderr = self.refused([good, ("copy", path)], "not a clean relative path")
                self.assertIn(path, stderr, "refused by name")

    def test_a_rows_file_that_cannot_be_read_whole_is_refused(self):
        """Round 2 (U445b, P2 f1 s6): a failed read of the listing is a refusal, never the end of the file: a directory
        and an unreadable file are refused by name before any row is used."""
        directory = self.root / "rows-dir"
        directory.mkdir()
        stderr = self.refused(directory, "not a regular file")
        self.assertIn(str(directory), stderr)
        unreadable = self.rows_file([("copy", f"{PREFIX}/units.tsv")], name="unreadable")
        unreadable.chmod(0)
        self.addCleanup(unreadable.chmod, 0o600)
        if os.access(unreadable, os.R_OK):
            self.skipTest("the file stays readable (root)")
        stderr = self.refused(unreadable, "cannot read the rows file of the body")
        self.assertIn(str(unreadable), stderr)

    def test_a_row_holding_a_nul_or_another_control_character_is_refused(self):
        """Round 2 (U445b, P3 f2 s3): bash `read` drops an embedded NUL; the listing is read NUL-delimited, so a NUL
        ends an entry and the remainder is a malformed row, refused; a newline in a path is a control character."""
        nul = self.root / "nul"
        nul.write_bytes(f"copy\t{PREFIX}/briefs/a\0b.md\0".encode())
        self.refused(nul, "not <change><TAB><path>")
        newline = self.root / "newline"
        newline.write_bytes(f"copy\t{PREFIX}/briefs/a\nb.md\0".encode())
        self.refused(newline, "control character")
        tab = self.root / "tab"
        tab.write_bytes(f"copy\t{PREFIX}/briefs/a\tb.md\0".encode())
        self.refused(tab, "control character")

    def test_only_unit_may_precede_render_body(self):
        """Round 2 (U445b, P3 f2 s2): the dry grammar is `[--unit U<n>] --render-body <six arguments>`; any other
        option before it is refused with the usage line."""
        good = [("copy", f"{PREFIX}/units.tsv")]
        for before in (
            ("--program", "other"),
            ("--base", "origin/main"),
            ("--unit", "U7", "--program", "prog"),
            ("--verbose",),
        ):
            with self.subTest(before=before):
                self.refused(good, "usage:", before=before)
        body = self.render(good, unit="U445")
        self.assertIn("\nProgram-Unit: prog/U445\n", body)
        trailing = subprocess.run(
            [str(LEVER), "--render-body", str(self.rows_file(good)), "7", "prog", "checkout", "", "", "--unit", "U7"],
            cwd=self.root,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(trailing.returncode, 2, trailing.stdout + trailing.stderr)
        self.assertIn("usage:", trailing.stderr)

    def test_the_program_unit_line_is_the_last_line_before_the_footer(self):
        body = self.render([("copy", f"{PREFIX}/units.tsv")], unit="U445")
        lines = body.splitlines()
        self.assertEqual(lines[-1], FOOTER)
        self.assertEqual(lines[-2], "")
        self.assertEqual(lines[-3], "Program-Unit: prog/U445")
        self.assertEqual(body.count("Program-Unit:"), 1)
        default = self.render([("copy", f"{PREFIX}/units.tsv")])
        self.assertIn("\nProgram-Unit: prog/U20\n", default)

    def test_the_contract_section_is_present_and_names_the_store_form(self):
        body = self.render([("copy", f"{PREFIX}/units.tsv")], form="derived")
        self.assertEqual(body.count("## Contract\n"), 1)
        self.assertLess(body.index("## Contract\n"), body.index("Program-Unit: prog/U20\n"))
        contract = body[body.index("## Contract\n") : body.index("Program-Unit: prog/U20\n")]
        bullets = [line for line in contract.splitlines() if line.startswith("- ")]
        self.assertEqual(len(bullets), 5, contract)
        self.assertIn("the derived program store `<store root>/prog/`", bullets[0])
        self.assertIn("from the program store (derived form)", body)
        checkout = self.render([("copy", f"{PREFIX}/units.tsv")], form="checkout")
        self.assertIn("(`.orchestration/orchestrate/prog/`, tracked or untracked and not git-ignored", checkout)

    def test_the_dry_form_calls_neither_git_nor_gh(self):
        bindir = self.root / "bin"
        bindir.mkdir()
        calls = self.root / "calls"
        for name in ("git", "gh"):
            fake = bindir / name
            fake.write_text(f'#!/bin/sh\nprintf "%s\\n" "{name} $*" >> "{calls}"\nexit 1\n')
            fake.chmod(0o755)
        body = self.render([("copy", f"{PREFIX}/units.tsv")], env={"PATH": f"{bindir}:{os.environ['PATH']}"})
        self.assertIn("## Threat table\n", body)
        self.assertFalse(calls.exists(), "no git or gh call")

    def test_a_malformed_row_or_argument_is_refused_before_anything_is_printed(self):
        good = ("copy", f"{PREFIX}/units.tsv")
        cases = (
            ("rows", [good, ("moved", f"{PREFIX}/units.tsv")], {}, "neither copy nor deletion"),
            ("rows", [good, ("copy", ".orchestration/orchestrate/other/units.tsv")], {}, "outside"),
            ("rows", [good, ("copy", "")], {}, "not <change><TAB><path>"),
            ("rows", [good, ("copy", f"{PREFIX}/briefs/a`b.md")], {}, "control character or a backtick"),
            ("rows", [], {}, "holds no row"),
            ("args", [good], {"form": "linked"}, "neither derived nor checkout"),
            ("args", [good], {"n": "0"}, "positive integer"),
            ("args", [good], {"program": "Bad Name"}, "program name"),
        )
        for label, rows, kwargs, message in cases:
            with self.subTest(label=label, message=message):
                self.refused(rows, message, **kwargs)
        cut = self.root / "cut"
        cut.write_bytes(f"copy\t{PREFIX}/units.tsv\0copy\t{PREFIX}/ledger.tsv".encode())  # the last entry has no NUL
        self.refused(cut, "ends mid-entry")
        self.refused(self.root / "absent", "cannot read")
        wrong_count = subprocess.run(
            [str(LEVER), "--render-body", str(self.rows_file([good])), "7", "prog"],
            cwd=self.root,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(wrong_count.returncode, 2, wrong_count.stdout + wrong_count.stderr)
        self.assertIn("usage:", wrong_count.stderr)


if __name__ == "__main__":
    unittest.main()
