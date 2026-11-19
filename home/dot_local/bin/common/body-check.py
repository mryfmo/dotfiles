#!/usr/bin/env python3
"""Refuse a pull request body the audit would file (regime-cutover U619, standing orders 59 and 60).

Measured 2026-11-19: four of the day's Codex verdicts filed findings on the pull request body alone (a changed path
without a threat-table row, a `closed` row whose evidence names no test, a sentence contradicted by the diff, a count
out of date), each costing a round or a disposition row. AGENTS.md's Audit section defines the table: columns
`row | risk | status | evidence`, one row per changed path, one per non-path control, one per orchestrator effect; a
`closed` row's evidence names the test selector that fails without the fix; `residual` names the control;
`out-of-scope` names the unit. The gate levers read the one body line `Program-Unit: <program>/U<n>`. This module is
the check that runs on the body file before every `gh pr create` and `gh pr edit` (hcom-orchestration SKILL, step 3).

CLI: `python3 -I -S body-check.py <body.md> --base <sha> --head <sha> [--repo <dir>]` reads the body and the changed
paths of `git diff --name-only <base>..<head>` in the repository at `--repo` (default the current directory), the
status of every git read checked (a diff or a grep that fails is exit 2 with one stderr line naming it, never a pass;
standing order 21), and refuses with exit 1, one line per fault on stderr and nothing on stdout, when: the body lacks
`## Summary`, `## Contract` with the three sentences starting `Guaranteed:`, `Left out:` and `Trusted:`, or
`## Threat table`; it holds other than exactly one `Program-Unit: <program>/U<n>` line (pr-body-edit.sh's grammar);
the table's header is not `| row | risk | status | evidence |`; a row has other than four cells (an unescaped `|`
inside a cell splits it, as GitHub renders it; `\\|` is the escape); a changed path has no row whose `row` cell is that
path in backticks (a row covers one path; a row whose cell is not a changed path is a non-path row); a row's status is
not `closed`, `residual` or `out-of-scope`; a `closed` row's evidence names no test selector that exists in the
repository at `<head>` (a selector is `test_<name>` or `<Class>Test`, found by `git grep -l -F -w` at the head under
`tests/`, or `tests.unit.<module>`, the file `tests/unit/<module>.py` in the head's tree; the row may name several and
one must exist, so a selector that exists only at the base is refused); a `residual` row names no control (its
evidence is empty); an `out-of-scope` row names no `U<n>`. Exit 0 prints one stdout line
`body-check: <n> paths, <m> rows, ok` when every rule holds (`<m>` the table's rows below the header).

Every rule is one function over the parsed body and the repository's reads, and RULES is the table that maps each
rule to the message its faults print (Model the Domain): a rule is added by one row. The lever reads no network, no
`gh`, no brief and no store, changes no gate, and a body it accepts is still the auditor's to judge. Installed as the
pinned module `~/.local/bin/common/body-check.py` (the generator's `LEVER_MODULES`, as `sweep-scope.py` is), run as
`python3 -I -S` with no third-party import; `tests/unit/test_body_check.py` runs it over a fixture repository.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import Callable, Iterator

USAGE = "usage: body-check.py <body.md> --base <sha> --head <sha> [--repo <dir>]"
PREFIX = "body-check"
SUMMARY = "Summary"
CONTRACT = "Contract"
THREAT_TABLE = "Threat table"
SECTIONS = (SUMMARY, CONTRACT, THREAT_TABLE)
CONTRACT_SENTENCES = ("Guaranteed:", "Left out:", "Trusted:")
HEADER = ("row", "risk", "status", "evidence")
CLOSED = "closed"
RESIDUAL = "residual"
OUT_OF_SCOPE = "out-of-scope"
STATUSES = (CLOSED, RESIDUAL, OUT_OF_SCOPE)
# The one body line the gate levers read, in pr-body-edit.sh's grammar (`unit_line`): a plain unit id.
PROGRAM_UNIT_LINE = re.compile(r"^Program-Unit: [a-z0-9][a-z0-9_-]{0,63}/U[0-9]+$")
PROGRAM_UNIT_PREFIX = "Program-Unit:"
UNIT_ID = re.compile(r"(?<![A-Za-z0-9])U[0-9]+(?![A-Za-z0-9])")
# The three selector forms a `closed` row's evidence may name, each read whole (a longer identifier is another name;
# a path component such as `tests/unit/test_x.py` names a file, not a test, and is no selector).
MODULE_SELECTOR = re.compile(r"(?<![A-Za-z0-9_./])tests\.unit\.([A-Za-z0-9_]+)(?![A-Za-z0-9_./])")
FUNCTION_SELECTOR = re.compile(r"(?<![A-Za-z0-9_./])test_[A-Za-z0-9_]+(?![A-Za-z0-9_/]|\.py)")
CLASS_SELECTOR = re.compile(r"(?<![A-Za-z0-9_./])[A-Z][A-Za-z0-9]*Test(?![A-Za-z0-9_/]|\.py)")
TESTS_DIR = "tests/"
TEST_MODULE_DIR = "tests/unit/"
# A table cell boundary: a `|` not escaped as `\|` (GitHub's one escape inside a cell).
CELL_BOUNDARY = re.compile(r"(?<!\\)\|")
SEPARATOR_CELL = re.compile(r"^:?-+:?$")
SECTION_HEADING = re.compile(r"^## (.*?)\s*$")
# Every git read: replace refs off, paths from the toplevel wherever the command runs, no colour, no external diff.
GIT = ("git", "--no-replace-objects", "-c", "core.quotePath=false", "-c", "diff.relative=false")
GIT_DIFF = ("diff", "-z", "--name-only", "--no-renames", "--no-relative", "--no-ext-diff", "--no-color")


class Unreadable(Exception):
    """The body or the repository cannot be read; the message is the one stderr line (exit 2)."""


class Row:
    """One row of the threat table below its header: its line number in the body and its cells as written."""

    def __init__(self, number: int, cells: list[str]) -> None:
        self.number = number
        self.cells = cells

    @property
    def row(self) -> str:
        return self.cells[0]

    @property
    def status(self) -> str:
        return self.cells[2]

    @property
    def evidence(self) -> str:
        return self.cells[3]

    @property
    def path(self) -> str | None:
        """The path the `row` cell names in backticks, or None for any other cell."""
        cell = self.row
        if len(cell) >= 3 and cell.startswith("`") and cell.endswith("`") and "`" not in cell[1:-1]:
            return cell[1:-1]
        return None


class Body:
    """The body file read as data: its `## ` sections, its `Program-Unit:` lines and its threat table."""

    def __init__(self, text: str) -> None:
        self.lines = text.split("\n")
        self.sections = sections(self.lines)
        self.program_unit_lines = [line for line in self.lines if line.startswith(PROGRAM_UNIT_PREFIX)]
        self.header: tuple[str, ...] | None = None
        self.header_line = ""
        self.rows: list[Row] = []
        table = self.sections.get(THREAT_TABLE)
        if table is not None:
            self.header, self.header_line, self.rows = threat_table(self.lines, *table)

    def contract_sentences(self) -> list[str]:
        """The first word of every line of `## Contract` that starts one of CONTRACT_SENTENCES."""
        bounds = self.sections.get(CONTRACT)
        if bounds is None:
            return []
        start, end = bounds
        return [
            sentence
            for line in self.lines[start:end]
            for sentence in CONTRACT_SENTENCES
            if line.lstrip().startswith(sentence)
        ]

    @property
    def table_rows(self) -> list[Row]:
        """The rows the row rules judge: those of four cells under the one header."""
        if self.header != HEADER:
            return []
        return [row for row in self.rows if len(row.cells) == len(HEADER)]


def sections(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Each `## <name>` heading's name to the line range of its body (after the heading, before the next `## `)."""
    found: dict[str, tuple[int, int]] = {}
    starts = [(number, match[1]) for number, line in enumerate(lines) if (match := SECTION_HEADING.match(line))]
    for index, (number, name) in enumerate(starts):
        end = starts[index + 1][0] if index + 1 < len(starts) else len(lines)
        found.setdefault(name, (number + 1, end))
    return found


def cells(line: str) -> list[str]:
    """The cells of a table line: split at every unescaped `|`, the outer empty parts of a leading and a trailing
    pipe dropped, each cell stripped and its `\\|` escapes decoded."""
    parts = CELL_BOUNDARY.split(line)
    if parts and not parts[0].strip():
        parts.pop(0)
    if parts and not parts[-1].strip():
        parts.pop()
    return [part.strip().replace("\\|", "|") for part in parts]


def threat_table(lines: list[str], start: int, end: int) -> tuple[tuple[str, ...] | None, str, list[Row]]:
    """The first table of the section: its header cells (None when the section holds no table line), the header
    line as written, and the rows after the separator line, each table line a line starting with `|`."""
    number = start
    while number < end and not lines[number].lstrip().startswith("|"):
        number += 1
    if number >= end:
        return None, "", []
    header_line = lines[number].strip()
    header = tuple(cells(header_line))
    number += 1
    if (
        number < end
        and lines[number].lstrip().startswith("|")
        and all(SEPARATOR_CELL.match(c) for c in cells(lines[number]))
    ):
        number += 1
    rows: list[Row] = []
    while number < end and lines[number].lstrip().startswith("|"):
        rows.append(Row(number + 1, cells(lines[number])))
        number += 1
    return header, header_line, rows


def selectors(evidence: str) -> list[str]:
    """The test selectors the evidence names, module forms first (each removed before the shorter forms are read, so
    `tests.unit.test_x` is one module selector and not also the function `test_x`), without repeats."""
    named: list[str] = []
    rest = evidence
    for match in MODULE_SELECTOR.finditer(evidence):
        named.append(match[0])
    rest = MODULE_SELECTOR.sub(" ", rest)
    for pattern in (FUNCTION_SELECTOR, CLASS_SELECTOR):
        named.extend(match[0] for match in pattern.finditer(rest))
    unique: list[str] = []
    for name in named:
        if name not in unique:
            unique.append(name)
    return unique


class Repository:
    """The repository's reads at two fixed shas: the changed paths of `<base>..<head>`, and whether a selector exists
    at `<head>` under `tests/`. Every read's status is checked; a failure is Unreadable."""

    def __init__(self, directory: str, base: str, head: str) -> None:
        for rev in (base, head):
            if not rev or rev.startswith("-"):
                raise Unreadable(f"{rev!r} is not a revision")
        if not directory or directory.startswith("-"):
            raise Unreadable(f"{directory!r} is not a directory")
        self.directory = directory
        self.base = base
        self.head = head
        self._found: dict[str, bool] = {}
        self._test_files: set[str] | None = None

    def git(self, *args: str, what: str) -> tuple[int, bytes, str]:
        """Run git in the repository: the exit status, stdout and the first stderr line; a git that cannot run is
        Unreadable naming `what`."""
        command = [*GIT, "-C", self.directory, *args]
        try:
            out = subprocess.run(command, capture_output=True, check=False)
        except OSError as error:
            raise Unreadable(f"cannot run git for {what}: {error.strerror}") from None
        detail = out.stderr.decode(errors="replace").strip().splitlines()
        return out.returncode, out.stdout, (detail[0][:200] if detail else "no output")

    def changed_paths(self) -> list[str]:
        """`git diff --name-only <base>..<head>`, NUL-separated, read as text; a failed diff or an empty listing is
        Unreadable (an empty listing is a failed read or nothing to check, never a body that holds)."""
        what = f"git diff --name-only {self.base}..{self.head}"
        status, stdout, detail = self.git(*GIT_DIFF, f"{self.base}..{self.head}", "--", what=what)
        if status:
            raise Unreadable(f"{what} exited {status}: {detail}")
        try:
            text = stdout.decode()
        except UnicodeDecodeError:
            raise Unreadable(f"{what} listed a path that is not UTF-8") from None
        entries = text.split("\0")
        if entries and entries[-1] == "":
            entries.pop()
        if not entries or any(not entry for entry in entries):
            raise Unreadable(f"{what} names no changed path; nothing to hold the table to")
        return entries

    def test_files(self) -> set[str]:
        """The files under `tests/` in the head's tree, read once."""
        if self._test_files is None:
            what = f"git ls-tree -r --name-only {self.head} -- {TESTS_DIR}"
            status, stdout, detail = self.git(
                "ls-tree", "-r", "-z", "--name-only", self.head, "--", TESTS_DIR, what=what
            )
            if status:
                raise Unreadable(f"{what} exited {status}: {detail}")
            self._test_files = {entry for entry in stdout.decode(errors="replace").split("\0") if entry}
        return self._test_files

    def selector_exists(self, selector: str) -> bool:
        """Whether the selector exists at the head: a module as its file under `tests/unit/`, a function or a class as
        a whole word `git grep -l -F -w` finds under `tests/`."""
        if selector in self._found:
            return self._found[selector]
        module = MODULE_SELECTOR.fullmatch(selector)
        if module:
            exists = (
                f"{TEST_MODULE_DIR}{module[1]}.py" in self.test_files()
            )  # lint-comparisons: allow a tree listing's entries, the set git ls-tree printed
        else:
            what = f"git grep -l -F -w -e {selector} {self.head} -- {TESTS_DIR}"
            status, _, detail = self.git(
                "grep", "-I", "-l", "-F", "-w", "-e", selector, self.head, "--", TESTS_DIR, what=what
            )
            if status == 0:
                exists = True
            elif status == 1:
                exists = False
            else:
                raise Unreadable(f"{what} exited {status}: {detail}")
        self._found[selector] = exists
        return exists


# A fault is the fields its message names; each rule yields its faults as dicts and RULES pairs it with its message.
Fault = dict[str, object]
Rule = Callable[[Body, Repository, list[str]], Iterator[Fault]]


def rule_sections(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    for name in SECTIONS:
        if name not in body.sections:
            yield {"name": name}


def rule_contract_sentences(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    if CONTRACT not in body.sections:
        return
    present = body.contract_sentences()
    for sentence in CONTRACT_SENTENCES:
        if sentence not in present:
            yield {"sentence": sentence}


def rule_program_unit(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    lines = body.program_unit_lines
    if len(lines) != 1:
        yield {"count": len(lines)}
    elif not PROGRAM_UNIT_LINE.match(lines[0]):
        yield {"count": f"a malformed one ({lines[0]!r})"}


def rule_header(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    if THREAT_TABLE in body.sections and body.header != HEADER:
        yield {"header": body.header_line or "missing (the section holds no table line)"}


def rule_cells(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    if body.header != HEADER:
        return
    for row in body.rows:
        if len(row.cells) != len(HEADER):
            yield {"number": row.number, "count": len(row.cells)}


def rule_path_rows(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    if body.header != HEADER:
        return
    covered = {row.path for row in body.table_rows}
    for changed in paths:
        if changed not in covered:  # lint-comparisons: allow git's listing against the table's cells, both read as text
            yield {"path": changed}


def rule_status(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    for row in body.table_rows:
        if row.status not in STATUSES:
            yield {"number": row.number, "row": row.row, "status": row.status}


def rule_closed(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    for row in body.table_rows:
        if row.status != CLOSED:
            continue
        named = selectors(row.evidence)
        if not any(repo.selector_exists(selector) for selector in named):
            yield {"number": row.number, "row": row.row, "named": ", ".join(named) or "none named"}


def rule_residual(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    for row in body.table_rows:
        if row.status == RESIDUAL and not row.evidence:
            yield {"number": row.number, "row": row.row}


def rule_out_of_scope(body: Body, repo: Repository, paths: list[str]) -> Iterator[Fault]:
    for row in body.table_rows:
        if row.status == OUT_OF_SCOPE and not UNIT_ID.search(row.evidence):
            yield {"number": row.number, "row": row.row}


# The table: each rule beside the message its faults print (`str.format` over the fault's fields).
RULES: tuple[tuple[Rule, str], ...] = (
    (rule_sections, "the body has no `## {name}` section"),
    (rule_contract_sentences, "the `## Contract` section has no sentence starting `{sentence}`"),
    (rule_program_unit, "the body holds {count} `Program-Unit:` lines, not exactly one `Program-Unit: <program>/U<n>`"),
    (rule_header, "the threat table's header is `{header}`, not `| row | risk | status | evidence |`"),
    (
        rule_cells,
        (
            "threat-table row at line {number} has {count} cells, not 4 (an unescaped `|` inside a cell splits it as"
            " GitHub renders it; write `\\|`)"
        ),
    ),
    (rule_path_rows, "the changed path `{path}` has no threat-table row whose `row` cell is `{path}`"),
    (
        rule_status,
        "threat-table row at line {number} ({row}) has the status `{status}`, not closed, residual or out-of-scope",
    ),
    (
        rule_closed,
        (
            "threat-table row at line {number} ({row}) is closed but its evidence names no test selector that exists at"
            " the head (`test_<name>`, `<Class>Test` or `tests.unit.<module>`; named: {named})"
        ),
    ),
    (
        rule_residual,
        "threat-table row at line {number} ({row}) is residual but names no control (its evidence is empty)",
    ),
    (rule_out_of_scope, "threat-table row at line {number} ({row}) is out-of-scope but names no unit `U<n>`"),
)


def faults(body: Body, repo: Repository, paths: list[str]) -> list[str]:
    """Every rule's faults as its message lines, in RULES order."""
    return [message.format(**fault) for rule, message in RULES for fault in rule(body, repo, paths)]


def read_body(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as error:
        raise Unreadable(f"cannot read {path}: {error.strerror}") from None
    except UnicodeDecodeError:
        raise Unreadable(f"{path} is not UTF-8") from None


def parse_args(argv: list[str]) -> tuple[str, str, str, str]:
    """`<body.md> --base <sha> --head <sha> [--repo <dir>]` in any order of the options; anything else is usage."""
    body: str | None = None
    options: dict[str, str] = {}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ("--base", "--head", "--repo"):
            if index + 1 >= len(argv) or arg in options:
                raise Unreadable(USAGE)
            options[arg] = argv[index + 1]
            index += 2
        elif arg.startswith("-") or body is not None:
            raise Unreadable(USAGE)
        else:
            body = arg
            index += 1
    if body is None or "--base" not in options or "--head" not in options:
        raise Unreadable(USAGE)
    return body, options["--base"], options["--head"], options.get("--repo", ".")


def main(argv: list[str]) -> int:
    try:
        body_path, base, head, directory = parse_args(argv)
        repo = Repository(directory, base, head)
        paths = repo.changed_paths()
        body = Body(read_body(body_path))
        lines = faults(body, repo, paths)
    except Unreadable as error:
        print(f"{PREFIX}: {error}", file=sys.stderr)
        return 2
    if lines:
        for line in lines:
            print(f"{PREFIX}: {line}", file=sys.stderr)
        return 1
    print(f"{PREFIX}: {len(paths)} paths, {len(body.rows)} rows, ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
