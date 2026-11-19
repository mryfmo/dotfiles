"""Exercise scripts/orchestrator/body-check.py (regime-cutover U619, standing orders 59 and 60): the check of a pull
request body before `gh pr create` and `gh pr edit`, run as `python3 -I -S` over a fixture repository made through the
suite's scratch-git helper, whose head holds the selectors a passing body names (`test_new_thing`, `NewThingTest`,
`tests.unit.test_new`) and whose base alone holds `test_old_thing` and `tests/unit/test_old.py`; a body that passes,
each fault refused with its line (exit 1, nothing on stdout), a selector that exists only at the base or only in the
working tree, a failed git read (exit 2, naming it), the rules as a table, the twin and the pin, and the documents
that name the lever."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git_env

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/body-check.py"
INSTALLED = ROOT / "home/dot_local/bin/common/body-check.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
OUTPUTS = ROOT / "scripts/generated-agent-outputs.json"
README = ROOT / "scripts/orchestrator/README.md"
SKILL = ROOT / "home/dot_agents/skills/hcom-orchestration/SKILL.md"
IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
PREFIX = "body-check: "
# The paths `git diff --name-only <base>..<head>` lists for the fixture: one removed, one added, one changed, one new.
CHANGED = ("docs/note.md", "scripts/thing.py", "tests/unit/test_new.py", "tests/unit/test_old.py")
# The body that holds: the three sections, the three Contract sentences, one Program-Unit line, the header, a row per
# changed path (each `closed` row naming one selector form that exists at the head), a residual control row and an
# out-of-scope row.
PASSING = """## Summary

A fixture body for the check.

Program-Unit: regime-cutover/U619

## Contract

Guaranteed: the fixture holds.

Left out: nothing.

Trusted: git's listing at two shas.

## Threat table

| row | risk | status | evidence |
| --- | --- | --- | --- |
| `docs/note.md` | a stale sentence | out-of-scope | U620 owns the docs |
| `scripts/thing.py` | the thing breaks | closed | `test_new_thing` fails without the fix |
| `tests/unit/test_new.py` | a test loosened | closed | `NewThingTest` holds the cases |
| `tests/unit/test_old.py` | a test dropped | closed | `tests.unit.test_new` carries its cases |
| the fixture's one control | the control fails | residual | the control is read at the head |
"""
OK_LINE = "body-check: 4 paths, 5 rows, ok\n"
ROW_THING = "| `scripts/thing.py` | the thing breaks | closed | `test_new_thing` fails without the fix |"
ROW_CONTROL = "| the fixture's one control | the control fails | residual | the control is read at the head |"
ROW_DOCS = "| `docs/note.md` | a stale sentence | out-of-scope | U620 owns the docs |"
HEADER = "| row | risk | status | evidence |"


def load_lever():
    spec = importlib.util.spec_from_file_location("body_check", LEVER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class BodyCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="body-check-test-")
        cls.env = quiet_git_env(
            {**os.environ, **IDENTITY, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}
        )
        cls.repo = Path(cls.temp.name) / "repo"
        git_init(cls.repo, env=cls.env)
        cls.write("tests/unit/test_old.py", "def test_old_thing():\n    pass\n\n\nclass OldThingTest:\n    pass\n")
        cls.write("tests/unit/test_kept.py", "def test_kept_thing():\n    pass\n")
        cls.write("scripts/thing.py", "print(1)\n")
        cls.git("add", "-A")
        cls.git("commit", "-q", "-m", "base")
        cls.base = cls.git("rev-parse", "HEAD")
        (cls.repo / "tests/unit/test_old.py").unlink()
        cls.write("tests/unit/test_new.py", "def test_new_thing():\n    pass\n\n\nclass NewThingTest:\n    pass\n")
        cls.write("scripts/thing.py", "print(2)\n")
        cls.write("docs/note.md", "a note\n")
        cls.git("add", "-A")
        cls.git("commit", "-q", "-m", "head")
        cls.head = cls.git("rev-parse", "HEAD")
        # a selector in the working tree alone: the check reads the head's tree, never the checkout
        cls.write("tests/unit/test_wt.py", "def test_working_tree_thing():\n    pass\n")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    @classmethod
    def write(cls, relative: str, text: str) -> None:
        path = cls.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    @classmethod
    def git(cls, *args: str) -> str:
        return subprocess.run(
            ["git", "-c", "commit.gpgsign=false", *args],
            cwd=cls.repo,
            env=cls.env,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        ).stdout.strip()

    def run_lever(self, body: str, *, base=None, head=None, repo=None, lever=LEVER, cwd=None, argv=None):
        """The lever as the coordinator runs it, `python3 -I -S`, over `body` written to a scratch file."""
        path = Path(self.temp.name) / "body.md"
        path.write_text(body)
        if argv is None:
            argv = [str(path), "--base", base or self.base, "--head", head or self.head]
            if repo is not False:
                argv += ["--repo", str(repo or self.repo)]
        return subprocess.run(
            [sys.executable, "-I", "-S", str(lever), *argv],
            cwd=cwd or self.temp.name,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    def assert_refused(self, run, *lines: str):
        """Exit 1, nothing on stdout, every stderr line the lever's, and each expected fault among them."""
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "", "nothing on stdout")
        faults = run.stderr.splitlines()
        self.assertTrue(faults, "one line per fault")
        for fault in faults:
            self.assertTrue(fault.startswith(PREFIX), fault)
        for line in lines:
            self.assertTrue(any(line in fault for fault in faults), f"{line!r} not in {faults}")
        return faults

    def replaced(self, old: str, new: str, body: str = PASSING) -> str:
        self.assertIn(old, body)
        return body.replace(old, new)

    def test_the_fixture_lists_the_four_changed_paths(self):
        listed = self.git("diff", "--name-only", f"{self.base}..{self.head}").split("\n")
        self.assertEqual(sorted(listed), sorted(CHANGED))
        self.assertIn("test_old_thing", self.git("show", f"{self.base}:tests/unit/test_old.py"))
        self.assertEqual(self.git("ls-tree", "--name-only", self.head, "--", "tests/unit/test_old.py"), "")
        self.assertEqual(self.git("ls-tree", "--name-only", self.head, "--", "tests/unit/test_wt.py"), "")

    def test_a_body_that_holds_passes_with_the_one_line(self):
        run = self.run_lever(PASSING)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(run.stdout, OK_LINE)
        self.assertEqual(run.stderr, "")
        # the repository defaults to the current directory
        run = self.run_lever(PASSING, repo=False, cwd=self.repo)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, OK_LINE, ""))
        # the installed copy is the same program
        run = self.run_lever(PASSING, lever=INSTALLED)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, OK_LINE, ""))

    def test_each_fault_is_refused_with_its_line(self):
        cases = (
            ("no Summary", self.replaced("## Summary", "## Overview"), "the body has no `## Summary` section"),
            ("no Contract", self.replaced("## Contract", "## Terms"), "the body has no `## Contract` section"),
            (
                "no Guaranteed",
                self.replaced("Guaranteed:", "Guarantees:"),
                "the `## Contract` section has no sentence starting `Guaranteed:`",
            ),
            (
                "no Left out",
                self.replaced("Left out:", "Left-out:"),
                "the `## Contract` section has no sentence starting `Left out:`",
            ),
            ("no Trusted", self.replaced("Trusted:", "Trusts:"), "no sentence starting `Trusted:`"),
            (
                "no Threat table",
                self.replaced("## Threat table", "## Threats"),
                "the body has no `## Threat table` section",
            ),
            (
                "no Program-Unit",
                self.replaced("Program-Unit: regime-cutover/U619\n", ""),
                "the body holds 0 `Program-Unit:` lines, not exactly one",
            ),
            (
                "two Program-Unit lines",
                self.replaced("Program-Unit: regime-cutover/U619\n", "Program-Unit: regime-cutover/U619\n" * 2),
                "the body holds 2 `Program-Unit:` lines, not exactly one",
            ),
            (
                "a fix-round unit id",
                self.replaced("Program-Unit: regime-cutover/U619", "Program-Unit: regime-cutover/U619b"),
                "the body holds a malformed one ('Program-Unit: regime-cutover/U619b') `Program-Unit:` lines",
            ),
            (
                "another header",
                self.replaced(HEADER, "| path | risk | status | evidence |"),
                "the threat table's header is `| path | risk | status | evidence |`, not `| row | risk | status | evidence |`",
            ),
            (
                "no table line in the section",
                self.replaced(PASSING[PASSING.index(HEADER) :], "no table here\n"),
                "the threat table's header is `missing (the section holds no table line)`",
            ),
            (
                "a changed path without its row",
                self.replaced(ROW_THING + "\n", ""),
                "the changed path `scripts/thing.py` has no threat-table row whose `row` cell is `scripts/thing.py`",
            ),
            (
                "a path row without backticks is a non-path row",
                self.replaced("| `scripts/thing.py` |", "| scripts/thing.py |"),
                "the changed path `scripts/thing.py` has no threat-table row",
            ),
            (
                "a status outside the three",
                self.replaced("| the thing breaks | closed |", "| the thing breaks | open |"),
                "threat-table row at line 20 (`scripts/thing.py`) has the status `open`, not closed, residual or out-of-scope",
            ),
            (
                "a closed row naming no selector",
                self.replaced("`test_new_thing` fails without the fix", "a test fails without the fix"),
                (
                    "threat-table row at line 20 (`scripts/thing.py`) is closed but its evidence names no test selector that"
                    " exists at the head (`test_<name>`, `<Class>Test` or `tests.unit.<module>`; named: none named)"
                ),
            ),
            (
                "a closed row naming a selector that does not exist",
                self.replaced("`test_new_thing` fails", "`test_missing_thing` fails"),
                (
                    "(`scripts/thing.py`) is closed but its evidence names no test selector that exists at the head"
                    " (`test_<name>`, `<Class>Test` or `tests.unit.<module>`; named: test_missing_thing)"
                ),
            ),
            (
                "a closed row naming a class that does not exist",
                self.replaced("`NewThingTest` holds", "`MissingThingTest` holds"),
                "(`tests/unit/test_new.py`) is closed but its evidence names no test selector",
            ),
            (
                "a closed row naming a module that does not exist at the head",
                self.replaced("`tests.unit.test_new` carries", "`tests.unit.test_old` carries"),
                (
                    "(`tests/unit/test_old.py`) is closed but its evidence names no test selector that exists at the head"
                    " (`test_<name>`, `<Class>Test` or `tests.unit.<module>`; named: tests.unit.test_old)"
                ),
            ),
            (
                "a closed row naming a test file's path, not a selector",
                self.replaced("`test_new_thing` fails", "`tests/unit/test_new.py` fails"),
                (
                    "(`scripts/thing.py`) is closed but its evidence names no test selector that exists at the head"
                    " (`test_<name>`, `<Class>Test` or `tests.unit.<module>`; named: none named)"
                ),
            ),
            (
                "a closed row naming a longer identifier",
                self.replaced("`test_new_thing` fails", "`test_new_thing_x` fails"),
                "named: test_new_thing_x)",
            ),
            (
                "a closed row naming a selector of the working tree alone",
                self.replaced("`test_new_thing` fails", "`test_working_tree_thing` fails"),
                "named: test_working_tree_thing)",
            ),
            (
                "a residual row without its control",
                self.replaced(ROW_CONTROL, "| the fixture's one control | the control fails | residual | |"),
                (
                    "threat-table row at line 23 (the fixture's one control) is residual but names no control (its evidence"
                    " is empty)"
                ),
            ),
            (
                "an out-of-scope row without its unit",
                self.replaced(
                    ROW_DOCS, "| `docs/note.md` | a stale sentence | out-of-scope | another unit owns the docs |"
                ),
                "threat-table row at line 19 (`docs/note.md`) is out-of-scope but names no unit `U<n>`",
            ),
            (
                "an unescaped pipe inside a cell",
                self.replaced("`test_new_thing` fails", "`a || b` and `test_new_thing` fails"),
                (
                    "threat-table row at line 20 has 6 cells, not 4 (an unescaped `|` inside a cell splits it as GitHub"
                    " renders it; write `\\|`)"
                ),
            ),
        )
        for label, body, line in cases:
            with self.subTest(label):
                self.assert_refused(self.run_lever(body), line)

    def test_a_selector_that_exists_only_at_the_base_is_refused(self):
        """The head's tests hold the named selector, never the base's: `test_old_thing` and `OldThingTest` exist in
        `tests/unit/test_old.py` at the base alone."""
        for selector in ("test_old_thing", "OldThingTest"):
            with self.subTest(selector):
                body = self.replaced("`test_new_thing` fails", f"`{selector}` fails")
                faults = self.assert_refused(self.run_lever(body), f"named: {selector})")
                self.assertEqual(len(faults), 1, faults)
                # the same body against a head that is the base passes that row, since the base holds the selector
                run = self.run_lever(body, base=f"{self.base}~0", head=self.base)
                self.assertEqual(run.returncode, 2, "a diff of a sha with itself lists nothing: a failed read")

    def test_a_closed_row_may_name_several_selectors_and_one_must_exist(self):
        body = self.replaced(
            "`test_new_thing` fails", "`test_missing_thing` and `test_new_thing`, or `NewThingTest`, fail"
        )
        run = self.run_lever(body)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, OK_LINE, ""))
        body = self.replaced("`test_new_thing` fails", "`test_missing_thing` and `test_kept_thing` fail")
        run = self.run_lever(body)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, OK_LINE, ""), "an unchanged test file counts")

    def test_an_escaped_pipe_stays_inside_its_cell(self):
        body = self.replaced("`test_new_thing` fails", "`a \\|\\| b` and `test_new_thing` fails")
        run = self.run_lever(body)
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, OK_LINE, ""))

    def test_every_fault_of_a_body_is_listed_in_one_run(self):
        body = self.replaced("## Summary", "## Overview")
        body = self.replaced("Trusted:", "Trusts:", body)
        body = self.replaced(ROW_THING + "\n", "", body)
        body = self.replaced("`NewThingTest` holds", "`MissingThingTest` holds", body)
        faults = self.assert_refused(
            self.run_lever(body),
            "no `## Summary` section",
            "no sentence starting `Trusted:`",
            "the changed path `scripts/thing.py` has no threat-table row",
            "named: MissingThingTest)",
        )
        self.assertEqual(len(faults), 4, faults)

    def test_a_missing_table_reports_the_section_once_not_every_path(self):
        body = self.replaced(PASSING[PASSING.index("## Threat table") :], "")
        faults = self.assert_refused(self.run_lever(body), "the body has no `## Threat table` section")
        self.assertEqual(len(faults), 1, faults)
        body = self.replaced(HEADER, "| path | risk | status | evidence |")
        faults = self.assert_refused(self.run_lever(body), "the threat table's header is")
        self.assertEqual(len(faults), 1, "a header of another shape leaves the rows unjudged")

    def test_a_failed_git_read_is_exit_2_naming_it_never_a_pass(self):
        """Standing order 21: the diff's and the grep's status are read; a failure is exit 2 with one stderr line."""
        cases = (
            ("an unknown head", {"head": "0" * 40}, f"git diff --name-only {self.base}..{'0' * 40} exited 128"),
            ("an option as a head", {"head": "--output=/dev/null"}, "'--output=/dev/null' is not a revision"),
            ("no repository", {"repo": Path(self.temp.name) / "nowhere"}, "exited 128"),
            ("nothing changed", {"head": None, "base": None}, "names no changed path"),
        )
        for label, options, line in cases:
            with self.subTest(label):
                if options.get("head", "") is None:
                    options = {"base": self.head, "head": self.head}
                run = self.run_lever(PASSING, **options)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertEqual(run.stdout, "")
                self.assertEqual(run.stderr.count("\n"), 1, "one stderr line")
                self.assertTrue(run.stderr.startswith(PREFIX), run.stderr)
                self.assertIn(line, run.stderr)
        # the body file itself: absent, and not UTF-8 (the repository read first, so the diff is the same as above)
        absent = [str(self.repo / "absent.md"), "--base", self.base, "--head", self.head, "--repo", str(self.repo)]
        run = self.run_lever(PASSING, argv=absent)
        self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
        self.assertEqual(run.stdout, "")
        self.assertEqual(run.stderr, f"{PREFIX}cannot read {self.repo / 'absent.md'}: No such file or directory\n")
        binary = Path(self.temp.name) / "binary.md"
        binary.write_bytes(PASSING.encode().replace(b"fixture body", b"\xff\xfe body"))
        run = self.run_lever(
            PASSING, argv=[str(binary), "--base", self.base, "--head", self.head, "--repo", str(self.repo)]
        )
        self.assertEqual((run.returncode, run.stdout, run.stderr), (2, "", f"{PREFIX}{binary} is not UTF-8\n"))

    def test_usage_is_exit_2(self):
        usage = "usage: body-check.py <body.md> --base <sha> --head <sha> [--repo <dir>]"
        for argv in (
            [],
            ["body.md"],
            ["body.md", "--base", self.base],
            ["body.md", "--head", self.head],
            ["--base", self.base, "--head", self.head],
            ["body.md", "--base", self.base, "--head", self.head, "--repo"],
            ["body.md", "--base", self.base, "--head", self.head, "extra.md"],
            ["body.md", "--base", self.base, "--head", self.head, "--base", self.base],
            ["body.md", "--base", self.base, "--head", self.head, "--verbose"],
        ):
            with self.subTest(argv):
                run = self.run_lever(PASSING, argv=argv)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)
                self.assertEqual(run.stderr, f"{PREFIX}{usage}\n")
                self.assertEqual(run.stdout, "")

    def test_the_rules_are_a_table_of_functions_and_messages(self):
        """Model the Domain: every rule is one function paired with the message its faults print, and the parsed body
        is read through the same functions the CLI runs, so a rule is added by one row."""
        lever = load_lever()
        self.assertEqual(len(lever.RULES), 10)
        for rule, message in lever.RULES:
            with self.subTest(rule.__name__):
                self.assertTrue(callable(rule))
                self.assertTrue(rule.__name__.startswith("rule_"))
                self.assertIsInstance(message, str)
        self.assertEqual(len({rule for rule, _ in lever.RULES}), len(lever.RULES), "each rule once")
        self.assertEqual(lever.HEADER, ("row", "risk", "status", "evidence"))
        self.assertEqual(lever.STATUSES, ("closed", "residual", "out-of-scope"))
        self.assertEqual(lever.CONTRACT_SENTENCES, ("Guaranteed:", "Left out:", "Trusted:"))
        # the selector grammar: module forms first, a path component is no selector, each name once
        self.assertEqual(
            lever.selectors(
                "`tests.unit.test_x` and `test_y`, `FooTest`, `tests/unit/test_z.py`, `test_y` again, `self.test_w`,"
                " `unittest_v`, `FooTestCase`, `test_u/`"
            ),
            ["tests.unit.test_x", "test_y", "FooTest"],
        )
        self.assertEqual(lever.selectors(""), [])
        # the cells: an unescaped pipe splits, `\|` is decoded, the outer pipes are dropped
        self.assertEqual(lever.cells("| a | b \\| c | d |"), ["a", "b | c", "d"])
        self.assertEqual(lever.cells("| a | b | c | d |"), ["a", "b", "c", "d"])
        self.assertEqual(lever.cells("| a | `b || c` | d |"), ["a", "`b", "", "c`", "d"])
        body = lever.Body(PASSING)
        self.assertEqual(body.header, lever.HEADER)
        self.assertEqual([row.path for row in body.rows], [*CHANGED, None])
        self.assertEqual(body.contract_sentences(), list(lever.CONTRACT_SENTENCES))
        self.assertEqual(body.program_unit_lines, ["Program-Unit: regime-cutover/U619"])
        # the Program-Unit grammar is pr-body-edit.sh's
        unit_line = re.search(
            r"^unit_line='(.*)'$", (ROOT / "scripts/orchestrator/pr-body-edit.sh").read_text(), re.MULTILINE
        )
        self.assertEqual(lever.PROGRAM_UNIT_LINE.pattern, unit_line[1])

    def test_the_lever_is_stdlib_only_and_runs_under_isolated_mode(self):
        text = LEVER.read_text()
        imports = re.findall(r"^(?:from (\S+) import|import (\S+))", text, re.MULTILINE)
        for module in (a or b for a, b in imports):
            with self.subTest(module):
                self.assertIn(module, ("__future__", "collections.abc", "re", "subprocess", "sys"))
        self.assertTrue(text.startswith("#!/usr/bin/env python3\n"))

    def test_the_twin_and_the_pin(self):
        """The generator installs the lever as a pinned module like `sweep-scope.py` (`LEVER_MODULES`): the bare name
        under `home/dot_local/bin/common`, byte-identical, no `executable_` twin, one `claude.levers.sha256` line equal
        to the source's digest, and the generated index's row."""
        self.assertTrue(INSTALLED.is_file(), f"{INSTALLED.relative_to(ROOT)} is missing")
        self.assertEqual(INSTALLED.read_bytes(), LEVER.read_bytes())
        self.assertFalse((ROOT / "home/dot_local/bin/common/executable_body-check.py").exists())
        self.assertFalse(os.access(INSTALLED, os.X_OK), "a module, run as python3 -I -S, never by path")
        digest = hashlib.sha256(LEVER.read_bytes()).hexdigest()
        pins = re.findall(r"^      body-check\.py: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)
        self.assertEqual(pins, [digest], "one pin, the source's digest")
        outputs = json.loads(OUTPUTS.read_text())
        rows = [row for row in outputs["outputs"] if row.get("source") == "home/dot_local/bin/common/body-check.py"]
        self.assertEqual(len(rows), 1, rows)
        self.assertEqual(rows[0]["target"], ".local/bin/common/body-check.py")
        self.assertFalse(rows[0]["executable"])
        self.assertEqual(rows[0]["sha256"], digest)
        generator = (ROOT / "scripts/generate-agent-configs.py").read_text()
        self.assertRegex(generator, r'LEVER_MODULES = frozenset\(\{[^}]*"body-check\.py"[^}]*\}\)')

    def test_the_documents_name_the_lever(self):
        readme = README.read_text()
        self.assertIn("## `body-check.py`: ", readme)
        self.assertIn("| the pull request body before `gh pr create` and `gh pr edit` (U619)", readme)
        self.assertIn("`tests/unit/test_body_check.py`", readme)
        skill = SKILL.read_text()
        step = re.search(r"^3\. RESULT\..*$", skill, re.MULTILINE)[0]
        self.assertIn(
            "`python3 -I -S ~/.local/bin/common/body-check.py <body file> --base <main tip> --head <head sha>`", step
        )
        self.assertIn("before every `gh pr create` and `gh pr edit`", step.lower())


if __name__ == "__main__":
    unittest.main()
