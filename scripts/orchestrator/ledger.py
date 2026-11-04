#!/usr/bin/env python3
"""The one reader of the program store's `ledger.tsv` (regime-cutover U122 round 6).

Until round 6 three readers each read the ledger by a grammar of their own: `rounds-check.py` and `audit-carry.py`
in Python, `pr-merge.sh` in awk, and the three disagreed on what a ts is (round 6 P1: the merge gate's awk checked
the ts column for its shape alone, so a `carried` row dated `2026-10-25T25:00:00Z` outranked the head's valid
`incorrect` row and the gate merged on the earlier head's `correct`; the digest lever had refused that row since
round 5). The mechanism-change row names the form: one ledger reader, imported by the two Python levers from beside
them and run by the merge gate as `python3 -I -S ledger.py`, so the timestamp form, the header, the column count,
the required cells and the choice of a newest row are each stated once.

`read_ledger(path)` (or `parse_ledger(name, text)` for a text read elsewhere, as `rounds-check.py --head` reads a
git blob) returns a `Ledger` of `Row`s or raises `Malformed` naming the file and line: the first line must be the
header `ts unit pr head_sha verdict verifier evidence`; every other line is split on the tab alone (an empty field
is still a field; U119 round 3), must have the header's column count, a ts `datetime.strptime` reads under
`%Y-%m-%dT%H:%M:%SZ` and nothing else (no shape pattern stands beside it: hour 25 is a ValueError, so a malformed
row), and no empty `ts`, `unit`, `pr`, `head_sha` or `verdict` cell (round 2: an empty cell matched no pull request
and read as "no row"). A `Row` carries its ts parsed (`ts`, a datetime, the order every choice of a newest row is
made in) and as written (`ts_text`, for the lines that name the row), its seven cells and its line number.

The four questions, each the newest row by `(ts, line)` (the later line at an equal ts, the file position deciding
nothing else; round 5): `newest_for_head(pr, head)` is the newest row of the pull request at the full sha, whatever
its verdict (`pr-merge.sh`'s row for the head and for a carried row's source); `newest_audit_at_another_head(unit,
head, pr)` is the newest audit row of the unit or a fix unit of it (`U<n>[a-z]`, standing order 24) at any other
head, an audit row being one whose verdict starts with the word `correct` or `incorrect` (a `carried`, `blocked`,
`sweep` or `-` row is no audit); `already_audited(unit, head, pr)` is the newest audit row of the same units at the
head itself; `newest_sweep(unit, head)` is the newest sweep row of the same units at the head, a sweep row being one
whose verdict starts with the word `sweep` (the advisory row of the `security-audit` skill the AGENTS.md Audit sweep
rule describes; U144, U147), which no audit question sees. A sweep row must be the exact row that rule defines (U147
round 4, Codex thread 4457544811: a row written by hand with verifier `coordinator` admitted the merge without
showing that the pinned skill ran): its `pr` is `-`, its `verifier` begins with the two words `security-audit-skill
<pin>`, `<pin>` 8 or more lowercase hex characters (the lever compares that word with the manifest's pin), and the
first `;`-separated field of its `evidence`, stripped of whitespace, is a relative path under `sweeps/` ending in
`.json` with no `..` or empty component (the findings file under the store). An audit or sweep row whose `head_sha`
is not 40 hex, and a sweep row of the unit that fails any of the three, is Malformed naming the line and the field
(standing order 21: never silently "no sweep row").

`ledger.py <store> verdict <pr> <head>` prints `<ts>\\t<unit>\\t<verdict>\\t<evidence>` of the newest row for the head,
or `none`; `ledger.py <store> carry-source <unit> <head> [--pr <pr>]` prints `<head_sha>\\t<verdict>\\t<unit>` of the
newest audit row at another head (its unit the row's own, a `U<n>b` fix unit's row under `U<n>b`, which names its
verdict file and disposition rows; U125 for the U122 round 6 residual), or `none`; `ledger.py <store> sweep <unit>
<head>` prints `<ts>\\t<unit>\\t<verifier>\\t<evidence>` of the newest sweep row of the unit or a fix unit of it at the
head (`pr-merge.sh`'s sweep gate for a trust-boundary unit, U147), or `none`. Each exits 2 with one stderr line
naming the file and line when the store cannot
be read as data (standing order 21: a failed read is never "no row").
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime

HEADER = ("ts", "unit", "pr", "head_sha", "verdict", "verifier", "evidence")
REQUIRED = range(1, 6)  # ts unit pr head_sha verdict: an empty cell is a malformed row, never "no row"
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"  # the one timestamp form of the store, read by strptime alone
TS_FORM = "YYYY-MM-DDThh:mm:ssZ"  # the same form as the refusals spell it
# A verdict column that starts with the word `correct` or `incorrect` (pr-merge.sh's correct_re, both words).
AUDIT_VERDICT = re.compile(r"^(correct|incorrect)(?:$|[\s(;,])")
# A verdict column that starts with the word `sweep` (the security-audit skill's advisory row, AGENTS.md Audit sweep
# rule; U147): the same word boundary as AUDIT_VERDICT, so `sweep (advisory)` and `sweep;` are sweep rows too.
SWEEP_VERDICT = re.compile(r"^sweep(?:$|[\s(;,])")
# The verifier of a sweep row (U147 round 4): the skill's name, then its pin word (8 or more lowercase hex; the
# manifest's `assets.security-audit-skill.pin` is a 40-hex commit, and the row may hold its prefix), then the end or a
# note after whitespace. The pin word is the group the lever compares with the manifest.
SWEEP_VERIFIER = re.compile(r"^security-audit-skill ([0-9a-f]{8,})(?:$|\s)")
SWEEP_PR = "-"
SWEEP_EVIDENCE_DIR = "sweeps"
SWEEP_EVIDENCE_SUFFIX = ".json"
SHA = re.compile(r"^[0-9a-f]{40}$")
UNIT = re.compile(r"^U[0-9]+$")
PULL_REQUEST = re.compile(r"^[1-9][0-9]{0,9}$")
NONE = "none"


class Malformed(Exception):
    """The ledger cannot be read as data; the message names the file and the line."""


def timestamp(text):
    """The ts cell as a time, or None: `datetime.strptime` under TS_FORMAT and nothing else, so a text outside the
    form and a time no calendar holds (hour 25, month 13) are both None, a malformed row to every reader."""
    try:
        return datetime.strptime(text, TS_FORMAT)
    except ValueError:
        return None


@dataclass(frozen=True)
class Row:
    """One data row of the ledger: the ts parsed and as written, the seven cells, and the line number."""

    ts: datetime
    unit: str
    pr: str
    head_sha: str
    verdict: str
    verifier: str
    evidence: str
    line: int
    ts_text: str

    @property
    def word(self):
        """`correct` or `incorrect` when the verdict starts with that word (an audit row), else None."""
        match = AUDIT_VERDICT.match(self.verdict)
        return match.group(1) if match else None

    @property
    def sweep(self):
        """True when the verdict starts with the word `sweep` (a sweep row, never an audit row)."""
        return SWEEP_VERDICT.match(self.verdict) is not None

    @property
    def sweep_pin(self):
        """The pin word of a sweep row's verifier (`security-audit-skill <pin>`), or None when the verifier is not of
        that form."""
        match = SWEEP_VERIFIER.match(self.verifier)
        return match.group(1) if match else None

    @property
    def sweep_evidence_path(self):
        """The findings file a sweep row names: the first `;`-separated field of the evidence, stripped."""
        return self.evidence.split(";", 1)[0].strip()

    def sweep_fault(self):
        """Why this sweep row is not the row the AGENTS.md Audit sweep rule defines, naming the field, or None (U147
        round 4). The head is judged by the caller, as an audit row's is."""
        if self.pr != SWEEP_PR:
            return f"the pr of a sweep row is not {SWEEP_PR!r}: {self.pr!r}"
        if self.sweep_pin is None:
            return (
                "the verifier of a sweep row does not begin with 'security-audit-skill <pin>' "
                f"(the pin 8 or more lowercase hex): {self.verifier!r}"
            )
        parts = self.sweep_evidence_path.split("/")
        if (
            parts[0] != SWEEP_EVIDENCE_DIR  # lint-comparisons: allow the row's store-relative path is judged as text
            or len(parts) < 2
            or not parts[-1].endswith(SWEEP_EVIDENCE_SUFFIX)
            or any(part in ("", "..") for part in parts[1:])
        ):
            return (
                f"the evidence of a sweep row does not name a findings file {SWEEP_EVIDENCE_DIR}/<path>"
                f"{SWEEP_EVIDENCE_SUFFIX} under the store (no '..' or empty component): {self.evidence!r}"
            )
        return None


def newest(rows):
    """The row with the latest ts, the later line at an equal ts, or None."""
    return max(rows, key=lambda row: (row.ts, row.line), default=None)


@dataclass(frozen=True)
class Ledger:
    name: str
    rows: tuple

    def newest_for_head(self, pr, head):
        """The newest row of pull request `pr` at the full sha `head`, whatever its verdict, or None."""
        return newest(row for row in self.rows if row.pr == pr and row.head_sha == head)

    def audits(self, unit, pr=None):
        """Every audit row of `unit` or a fix unit of it (`U<n>[a-z]`), of pull request `pr` when given, in file
        order; one whose head_sha is not 40 hex is Malformed."""
        own = re.compile(rf"^{re.escape(unit)}[a-z]?$")
        found = []
        for row in self.rows:
            if row.word is None or not own.match(row.unit) or (pr is not None and row.pr != pr):
                continue
            if not SHA.match(row.head_sha):
                raise Malformed(f"{self.name}:{row.line}: the head_sha of an audit row is not 40 hex: {row.head_sha!r}")
            found.append(row)
        return found

    def newest_audit_at_another_head(self, unit, head, pr=None):
        """The newest audit row of the unit or a fix unit of it at a head other than `head`, or None: the head a
        carry rests on, whatever that row's verdict says (round 5)."""
        return newest(row for row in self.audits(unit, pr) if row.head_sha != head)

    def already_audited(self, unit, head, pr=None):
        """The newest audit row of the unit or a fix unit of it at `head` itself, or None (round 5 P1: a head the
        ledger judged is never carried)."""
        return newest(row for row in self.audits(unit, pr) if row.head_sha == head)

    def newest_sweep(self, unit, head):
        """The newest sweep row of `unit` or a fix unit of it (`U<n>[a-z]`) at `head`, or None (U147: the merge gate's
        sweep row for a trust-boundary unit); a sweep row of those units whose head_sha is not 40 hex, or that is not
        the exact row the AGENTS.md Audit sweep rule defines (pr `-`, verifier `security-audit-skill <pin>`, evidence
        a findings file under `sweeps/`; round 4), is Malformed naming the line and the field, as an audit row is, so
        neither a short sha nor a hand-written row is ever read as "no sweep" (standing order 21)."""
        own = re.compile(rf"^{re.escape(unit)}[a-z]?$")
        found = []
        for row in self.rows:
            if not row.sweep or not own.match(row.unit):
                continue
            if not SHA.match(row.head_sha):
                raise Malformed(f"{self.name}:{row.line}: the head_sha of a sweep row is not 40 hex: {row.head_sha!r}")
            fault = row.sweep_fault()
            if fault is not None:
                raise Malformed(f"{self.name}:{row.line}: {fault}")
            if row.head_sha == head:
                found.append(row)
        return newest(found)


def parse_ledger(name, text):
    """The Ledger of one `ledger.tsv` text, or Malformed naming `name` and the line."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    expected = "\t".join(HEADER)
    if not lines or lines[0].rstrip("\r") != expected:
        found = lines[0] if lines else ""
        raise Malformed(f"{name}:1: the header is {found!r}, not {expected!r}")
    rows = []
    for number, line in enumerate(lines[1:], 2):
        fields = line.rstrip("\r").split("\t")
        if len(fields) != len(HEADER):
            raise Malformed(f"{name}:{number}: {len(fields)} columns, not {len(HEADER)}")
        at = timestamp(fields[0])
        if at is None:
            raise Malformed(f"{name}:{number}: the ts {fields[0]!r} is not {TS_FORM}")
        for column in REQUIRED:
            if fields[column - 1] == "":
                raise Malformed(f"{name}:{number}: column {column} ({HEADER[column - 1]}) is empty")
        rows.append(Row(at, *fields[1:], number, fields[0]))
    return Ledger(name, tuple(rows))


def read_text(path):
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            return handle.read()
    except OSError as error:
        raise Malformed(f"{path}: cannot read: {error.strerror}") from None
    except UnicodeDecodeError as error:
        raise Malformed(f"{path}: not UTF-8: {error.reason}") from None


def read_ledger(path):
    """The Ledger of the file at `path`, or Malformed (a file that cannot be read or is not UTF-8 included)."""
    return parse_ledger(path, read_text(path))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("store", help="the program store directory holding ledger.tsv")
    forms = parser.add_subparsers(dest="form", required=True)
    verdict = forms.add_parser(
        "verdict", help="the newest row for a head: <ts>\\t<unit>\\t<verdict>\\t<evidence>, or none"
    )
    verdict.add_argument("pr", help="the pull request's decimal number")
    verdict.add_argument("head", help="the head, 40 hex")
    source = forms.add_parser(
        "carry-source", help="the newest audit row at another head: <head_sha>\\t<verdict>\\t<unit>, or none"
    )
    source.add_argument("unit", help="the body's unit, U<n>; its fix units U<n>[a-z] count with it")
    source.add_argument("head", help="the current head, 40 hex")
    source.add_argument(
        "--pr", help="the pull request's decimal number; without it, the unit's rows of every pull request"
    )
    sweep = forms.add_parser(
        "sweep", help="the newest sweep row of the unit at the head: <ts>\\t<unit>\\t<verifier>\\t<evidence>, or none"
    )
    sweep.add_argument("unit", help="the body's unit, U<n>; its fix units U<n>[a-z] count with it")
    sweep.add_argument("head", help="the audited head, 40 hex")
    args = parser.parse_args(argv)
    if not SHA.match(args.head):
        parser.error(f"the head {args.head!r} is not 40 hex")
    if args.form == "verdict" and not PULL_REQUEST.match(args.pr):
        parser.error(f"the pull request {args.pr!r} is not a decimal number")
    if args.form in ("carry-source", "sweep") and not UNIT.match(args.unit):
        parser.error(f"the unit {args.unit!r} is not U<n>")
    if args.form == "carry-source" and args.pr is not None and not PULL_REQUEST.match(args.pr):
        parser.error(f"the pull request {args.pr!r} is not a decimal number")
    store = args.store.rstrip("/") or args.store
    try:
        ledger = read_ledger(os.path.join(store, "ledger.tsv"))
        if args.form == "verdict":
            row = ledger.newest_for_head(args.pr, args.head)
            print(NONE if row is None else "\t".join((row.ts_text, row.unit, row.verdict, row.evidence)))
        elif args.form == "sweep":
            row = ledger.newest_sweep(args.unit, args.head)
            print(NONE if row is None else "\t".join((row.ts_text, row.unit, row.verifier, row.evidence)))
        else:
            row = ledger.newest_audit_at_another_head(args.unit, args.head, args.pr)
            print(NONE if row is None else "\t".join((row.head_sha, row.verdict, row.unit)))
    except Malformed as error:
        print(f"ledger: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
