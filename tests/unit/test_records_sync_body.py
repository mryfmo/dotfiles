"""Exercise the sync body writer of scripts/orchestrator/records-sync.sh (regime-cutover U445).

The lever's dry entry point `records-sync.sh [--unit U<n>] --render-body <rows-file> <n> <program> <form> <units-line>
<decisions-line>` prints the pull request's body to stdout with no git or gh call: the one writer the real sync writes
its `--body-file` through. The rows file holds one line per changed path, `copy` or `deletion`, a tab and the published
path. The tests run the checkout's lever in place (its self-check reads the checkout's manifest) under a scratch HOME
and assert the body's shape: `## Summary`, the `## Threat table` with one row per changed path carrying its kind's
risk-and-bound sentence and one row for the gates that read the carried records, the cap rule (past 150 paths, one row
per directory kind with its count), `## Contract`, and the `Program-Unit:` line as the last line before the footer.
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
COPY = "masked copy of the live store's file"
COPY_EVIDENCE = (
    "`--scan-identifiers` zero findings over every carried copy; the change set equals the computed set; "
    "the regime check at the head"
)
DELETION_EVIDENCE = "never read, only removed; the change set equals the computed set; the regime check at the head"
PREFIX = ".orchestration/orchestrate/prog"
# One path of every kind the lever's table names, with the kind's risk-and-bound sentence (the accepted form of the
# sync 54 and PR 759 bodies).
KINDS = (
    ("briefs/U1-x.md", "text the workers read, checked by brief-check.py; no code"),
    ("verdicts/U1-head.md", "text read by ledger-row.py's scorer and pr-merge.sh"),
    ("sweeps/U1-findings.json", "JSON and text the merge gate names and never opens"),
    ("handoff/01-notes.md", "text for the operator and the next coordinator"),
    ("handouts/02-login.md", "text for the operator and the next coordinator"),
    ("ledger.tsv", "read by pr-merge.sh and rounds-check.py; every row written by a lever"),
    ("decisions.tsv", "rounds-check.py reads mechanism-change rows"),
    ("dispositions.tsv", "pr-merge.sh reads"),
    ("units.tsv", "brief-check.py and the coordinator read; no gate"),
    ("tests/use-cases.tsv", "check-tables.py validates"),
    ("overview.md", "a record of the program store; no code, no lever"),
)


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
        path = self.root / name
        path.write_text("".join(f"{change}\t{path_}\n" for change, path_ in rows))
        return path

    def run_render(self, rows, n="7", program="prog", form="checkout", units="", decisions="", unit=None, env=None):
        rows_path = rows if isinstance(rows, Path) else self.rows_file(rows)
        args = [str(LEVER)]
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
        rows = [("copy", f"{PREFIX}/{rel}") for rel, _ in KINDS]
        body = self.render(rows, units="U2 U3", decisions="2026-11-11T00:00:00Z")
        self.assertIn(f"Records sync 7 of `prog` ({len(KINDS)} file(s))", body)
        self.assertIn("- units.tsv rows added or changed: U2 U3\n", body)
        self.assertIn("- decisions.tsv rows added or changed: 2026-11-11T00:00:00Z\n", body)
        self.assertLess(body.index("## Summary\n"), body.index("## Threat table\n"))
        self.assertLess(body.index("## Threat table\n"), body.index("## Contract\n"))
        table = self.table_rows(body)
        expected = [f"| `{PREFIX}/{rel}` | {COPY} | {risk} | closed | {COPY_EVIDENCE} |" for rel, risk in KINDS] + [
            GATES_ROW
        ]
        self.assertEqual(table, expected)

    def test_a_removed_path_is_a_deletion_row(self):
        rows = [("deletion", f"{PREFIX}/briefs/U9-gone.md"), ("copy", f"{PREFIX}/units.tsv")]
        table = self.table_rows(self.render(rows))
        self.assertEqual(
            table[0],
            f"| `{PREFIX}/briefs/U9-gone.md` | deletion | text the workers read, checked by brief-check.py; no code "
            f"| closed | {DELETION_EVIDENCE} |",
        )
        self.assertEqual(table[1].split(" | ")[1], COPY)
        self.assertEqual(table[-1], GATES_ROW)

    def test_past_150_paths_the_table_holds_one_row_per_kind_with_the_count(self):
        """The regime workflow once failed on a 135 KB body (decisions 2026-11-10: under 120 KiB), so the per-path rows
        stop at 150 and a larger sync lists each directory kind once with its count; the rule stands in the line
        above the table."""
        at_cap = [("copy", f"{PREFIX}/briefs/U{i}-{'x' * 180}.md") for i in range(150)]
        body = self.render(at_cap)
        self.assertEqual(len(self.table_rows(body)), 151, "150 paths: one row each, plus the gates row")
        self.assertLess(len(body.encode()), 120 * 1024)
        past = at_cap + [
            ("copy", f"{PREFIX}/verdicts/U1-a.md"),
            ("deletion", f"{PREFIX}/verdicts/U1-b.md"),
            ("copy", f"{PREFIX}/ledger.tsv"),
        ]
        body = self.render(past)
        table = self.table_rows(body)
        self.assertEqual(
            table,
            [
                (
                    "| `briefs/` (150 paths) | 150 masked copies of the live store's files, 0 deletions "
                    "| text the workers read, checked by brief-check.py; no code | closed "
                    "| `--scan-identifiers` zero findings over every carried copy; a deletion is never read, only removed; "
                    "the change set equals the computed set; the regime check at the head |"
                ),
                (
                    "| `verdicts/` (2 paths) | 1 masked copies of the live store's files, 1 deletions "
                    "| text read by ledger-row.py's scorer and pr-merge.sh | closed "
                    "| `--scan-identifiers` zero findings over every carried copy; a deletion is never read, only removed; "
                    "the change set equals the computed set; the regime check at the head |"
                ),
                (
                    "| `ledger.tsv` (1 paths) | 1 masked copies of the live store's files, 0 deletions "
                    "| read by pr-merge.sh and rounds-check.py; every row written by a lever | closed "
                    "| `--scan-identifiers` zero findings over every carried copy; a deletion is never read, only removed; "
                    "the change set equals the computed set; the regime check at the head |"
                ),
                GATES_ROW,
            ],
        )
        self.assertIn("(153 file(s))", body)
        rule = body[body.index("## Threat table\n") : body.index(HEADER)]
        self.assertIn("150", rule, "the cap is stated above the table")
        self.assertIn("one row per directory kind with its count", rule)
        self.assertLess(len(body.encode()), 120 * 1024)

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
            ("rows", [], {}, "holds no row"),
            ("args", [good], {"form": "linked"}, "neither derived nor checkout"),
            ("args", [good], {"n": "0"}, "positive integer"),
            ("args", [good], {"program": "Bad Name"}, "program name"),
        )
        for label, rows, kwargs, message in cases:
            with self.subTest(label=label, message=message):
                run = self.run_render(rows, **kwargs)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertIn("refused:", run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(run.stdout, "")
        cut = self.root / "cut"
        cut.write_text(f"copy\t{PREFIX}/units.tsv\ncopy\t{PREFIX}/ledger.tsv")  # the last entry has no newline
        run = self.run_render(cut)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertIn("ends mid-entry", run.stderr)
        missing = self.run_render(self.root / "absent")
        self.assertEqual(missing.returncode, 2, missing.stdout + missing.stderr)
        self.assertIn("cannot read", missing.stderr)
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
