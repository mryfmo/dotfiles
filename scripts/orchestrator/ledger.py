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
is still a field; U119 round 3), must have the header's column count, a ts of the one shape `YYYY-MM-DDThh:mm:ssZ`
(`TS_SHAPE`: four digits, then two in every other field; U597 round 6, where `strptime` alone read `2026-11-9T4:5:6Z`
under a form that spells two digits) that `datetime.strptime` then reads under `%Y-%m-%dT%H:%M:%SZ` (hour 25 is a
ValueError, so a malformed row), no cell holding a control character (`CONTROL`, `\\x00` to `\\x1f` and `\\x7f`; U597
round 7, where a NUL in a daily row's evidence path was data to the reader and dropped by the lever's `$(...)`), and
no empty `ts`, `unit`, `pr`, `head_sha` or `verdict` cell (round 2: an empty cell matched no pull request and read as
"no row"). A `Row` carries its ts parsed (`ts`, a datetime, the order every
choice of a newest row is made in) and as written (`ts_text`, for the lines that name the row), its seven cells and
its line number.

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

The daily sweep (regime-cutover U597 round 4; the operator's sweep rule C of 2026-11-18): main's head gets one full
sweep of the `security-audit` skill per UTC day, the standing control a head outside every sweep class rests on, and
its rows live in the store's own file `daily-sweeps.tsv` (header `ts head_sha verifier evidence`), written by
`ledger-row.py daily` and read here alone. `read_daily(path)` returns a `Daily` of `DailyRow`s, or None when no file
exists at the path (the day's first sweep is not yet recorded: `none` to the lever, never a refusal), or raises
Malformed with the ledger's strictness: the header exact, four cells per row split on the tab alone, a ts of the one
shape `timestamp` reads (`TS_SHAPE`, then `strptime`; round 6: `2026-11-9T4:5:6Z` is Malformed naming the line, where
round 5's `strptime` alone read it), no cell holding a control character (round 7), no empty cell, a `head_sha` of 40
hex, and the verifier and the evidence the exact fields of the sweep rule (`security-audit-skill <pin>`, a findings
file `sweeps/<path>.json`), each fault naming the line and the field. `Daily.newest_within(now, max_age)` is the
newest row by `(ts, line)` whose ts lies within the window `now - max_age <= ts <= now + DAILY_FUTURE_SLACK` (60
seconds, the reader's allowance for a row another host's clock wrote; the writer refuses a ts after its own clock,
round 7; round 5: a row dated further in the future is not within the window, so it does not count and is not refused
as malformed, where round 4's floor alone let a future-dated row waive per-head sweeps until a day after its ts). `ledger.py <store> daily
<max-age-seconds>` prints `<ts>\\t<head_sha>\\t<verifier>\\t<evidence>` of that row against the clock (UTC), or `none`
(no file, or no row within the window); `pr-merge.sh` asks it with 86400 and skips a head's own sweep row only on a
row, so the exemption of rule C is bound to the control it rests on.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

HEADER = ("ts", "unit", "pr", "head_sha", "verdict", "verifier", "evidence")
REQUIRED = range(1, 6)  # ts unit pr head_sha verdict: an empty cell is a malformed row, never "no row"
TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"  # the one timestamp form of the store, read by strptime alone
TS_FORM = "YYYY-MM-DDThh:mm:ssZ"  # the same form as the refusals spell it
# The shape every ts cell has before the calendar check (U597 round 6): four ASCII digits, then two in each of the five
# other fields, the literals in their places; `strptime` alone accepts one digit where the form spells two.
TS_SHAPE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
# No cell of either file holds a control character (U597 round 7: `\x00` to `\x1f` and `\x7f`; a tab is the separator
# and a line break the row's end, so neither is in a cell, and a NUL in an evidence path is dropped by bash's `$(...)`
# when pr-merge.sh captures the row, so the lever would check another file than the one the row names). A cell that
# holds one is Malformed naming the line and the field.
CONTROL = re.compile(r"[\x00-\x1f\x7f]")
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
# The daily sweep file of the store (U597 round 4): main's head, one full sweep per UTC day, each run one row.
DAILY_FILE = "daily-sweeps.tsv"
DAILY_HEADER = ("ts", "head_sha", "verifier", "evidence")
DAILY_REQUIRED = range(1, 5)  # every cell: a row without a verifier or an evidence is no sweep
# The window's upper bound (round 5): a daily row may be dated this many seconds after now and no further; a row dated
# later is not within the window. The allowance is the reader's alone, for a row another host's clock wrote and this
# host reads (the clocks' skew): the writer, `ledger-row.py daily`, refuses a `--swept-at` after its own clock (round
# 7), so a row this host wrote is never dated ahead.
DAILY_FUTURE_SLACK = 60
MAX_AGE = re.compile(r"^[1-9][0-9]*$")


def sweep_pin_of(verifier):
    """The pin word of a sweep verifier (`security-audit-skill <pin>`), or None when the verifier is not of that form."""
    match = SWEEP_VERIFIER.match(verifier)
    return match.group(1) if match else None


def sweep_evidence_path_of(evidence):
    """The findings file a sweep evidence names: the first `;`-separated field, stripped."""
    return evidence.split(";", 1)[0].strip()


def sweep_fields_fault(verifier, evidence, kind):
    """Why a verifier and an evidence are not those of the row the AGENTS.md Audit sweep rule defines, naming the
    field, or None: the verifier begins with `security-audit-skill <pin>`, the pin 8 or more lowercase hex, and the
    evidence's first `;`-field is a relative `sweeps/<path>.json` with no `..` or empty component. `kind` names the
    row in the message (`a sweep row`, `a daily sweep row`); one rule for the ledger's sweep rows and the daily file's
    (U147 round 4; U597 round 4)."""
    if sweep_pin_of(verifier) is None:
        return (
            f"the verifier of {kind} does not begin with 'security-audit-skill <pin>' "
            f"(the pin 8 or more lowercase hex): {verifier!r}"
        )
    parts = sweep_evidence_path_of(evidence).split("/")
    if (
        parts[0] != SWEEP_EVIDENCE_DIR  # lint-comparisons: allow the row's store-relative path is judged as text
        or len(parts) < 2
        or not parts[-1].endswith(SWEEP_EVIDENCE_SUFFIX)
        or any(part in ("", "..") for part in parts[1:])
    ):
        return (
            f"the evidence of {kind} does not name a findings file {SWEEP_EVIDENCE_DIR}/<path>"
            f"{SWEEP_EVIDENCE_SUFFIX} under the store (no '..' or empty component): {evidence!r}"
        )
    return None


class Malformed(Exception):
    """The ledger cannot be read as data; the message names the file and the line."""


def timestamp(text):
    """The ts cell as a time, or None: the shape TS_SHAPE first (U597 round 6: `strptime` reads one digit as well as
    two under `%m`, `%d`, `%H`, `%M` and `%S`, so `2026-11-9T4:5:6Z` passed a form that spells two), then
    `datetime.strptime` under TS_FORMAT, so a text outside the form and a time no calendar holds (hour 25, month 13)
    are both None, a malformed row to every reader."""
    if TS_SHAPE.match(text) is None:
        return None
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
        return sweep_pin_of(self.verifier)

    @property
    def sweep_evidence_path(self):
        """The findings file a sweep row names: the first `;`-separated field of the evidence, stripped."""
        return sweep_evidence_path_of(self.evidence)

    def sweep_fault(self):
        """Why this sweep row is not the row the AGENTS.md Audit sweep rule defines, naming the field, or None (U147
        round 4). The head is judged by the caller, as an audit row's is."""
        if self.pr != SWEEP_PR:
            return f"the pr of a sweep row is not {SWEEP_PR!r}: {self.pr!r}"
        return sweep_fields_fault(self.verifier, self.evidence, "a sweep row")


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


def control_check(name, number, header, fields):
    """Malformed naming the line, the column and the character when a cell holds a control character (U597 round 7;
    CONTROL): one rule for the ledger's rows and the daily file's."""
    for column, field in enumerate(fields, 1):
        found = CONTROL.search(field)
        if found is not None:
            raise Malformed(
                f"{name}:{number}: column {column} ({header[column - 1]}) holds a control character "
                f"U+{ord(found.group()):04X}; no cell holds one"
            )


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
        control_check(name, number, HEADER, fields)
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


@dataclass(frozen=True)
class DailyRow:
    """One data row of `daily-sweeps.tsv`: the ts parsed and as written, the four cells, and the line number."""

    ts: datetime
    head_sha: str
    verifier: str
    evidence: str
    line: int
    ts_text: str

    @property
    def sweep_pin(self):
        return sweep_pin_of(self.verifier)

    @property
    def sweep_evidence_path(self):
        return sweep_evidence_path_of(self.evidence)


@dataclass(frozen=True)
class Daily:
    name: str
    rows: tuple

    def newest_within(self, now, max_age):
        """The newest row by `(ts, line)` whose ts lies within `now - max_age <= ts <= now + DAILY_FUTURE_SLACK`
        (`now` a naive UTC datetime, as the rows' ts are), or None: the daily sweep a head outside every class rests
        on. A row dated more than DAILY_FUTURE_SLACK seconds after now is not within the window (round 5)."""
        floor = now - timedelta(seconds=max_age)
        ceiling = now + timedelta(seconds=DAILY_FUTURE_SLACK)
        return newest(row for row in self.rows if floor <= row.ts <= ceiling)


def parse_daily(name, text):
    """The Daily of one `daily-sweeps.tsv` text, or Malformed naming `name`, the line and the field, with the
    ledger's strictness: the header exact, four cells split on the tab alone, a ts under the one form, no empty cell,
    a 40-hex head, and the verifier and the evidence the exact fields of the sweep rule (U597 round 4)."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    expected = "\t".join(DAILY_HEADER)
    if not lines or lines[0].rstrip("\r") != expected:
        found = lines[0] if lines else ""
        raise Malformed(f"{name}:1: the header is {found!r}, not {expected!r}")
    rows = []
    for number, line in enumerate(lines[1:], 2):
        fields = line.rstrip("\r").split("\t")
        if len(fields) != len(DAILY_HEADER):
            raise Malformed(f"{name}:{number}: {len(fields)} columns, not {len(DAILY_HEADER)}")
        control_check(name, number, DAILY_HEADER, fields)
        at = timestamp(fields[0])
        if at is None:
            raise Malformed(f"{name}:{number}: the ts {fields[0]!r} is not {TS_FORM}")
        for column in DAILY_REQUIRED:
            if fields[column - 1] == "":
                raise Malformed(f"{name}:{number}: column {column} ({DAILY_HEADER[column - 1]}) is empty")
        if not SHA.match(fields[1]):
            raise Malformed(f"{name}:{number}: the head_sha of a daily sweep row is not 40 hex: {fields[1]!r}")
        fault = sweep_fields_fault(fields[2], fields[3], "a daily sweep row")
        if fault is not None:
            raise Malformed(f"{name}:{number}: {fault}")
        rows.append(DailyRow(at, *fields[1:], number, fields[0]))
    return Daily(name, tuple(rows))


def read_daily(path):
    """The Daily of the file at `path`, None when no file exists there (FileNotFoundError alone: the day's first
    sweep is not yet recorded), or Malformed (a file that exists and cannot be read, or is not UTF-8, included:
    standing order 21)."""
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            text = handle.read()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise Malformed(f"{path}: cannot read: {error.strerror}") from None
    except UnicodeDecodeError as error:
        raise Malformed(f"{path}: not UTF-8: {error.reason}") from None
    return parse_daily(path, text)


def utc_now():
    """The clock as a naive UTC datetime, the form the rows' ts parse to."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


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
    daily = forms.add_parser(
        "daily",
        help=(
            "the newest daily sweep of main's head within the window, from daily-sweeps.tsv: "
            "<ts>\\t<head_sha>\\t<verifier>\\t<evidence>, or none"
        ),
    )
    daily.add_argument("max_age", help="the window in seconds before now; a row older than it is not within")
    args = parser.parse_args(argv)
    if args.form != "daily" and not SHA.match(args.head):
        parser.error(f"the head {args.head!r} is not 40 hex")
    if args.form == "verdict" and not PULL_REQUEST.match(args.pr):
        parser.error(f"the pull request {args.pr!r} is not a decimal number")
    if args.form in ("carry-source", "sweep") and not UNIT.match(args.unit):
        parser.error(f"the unit {args.unit!r} is not U<n>")
    if args.form == "carry-source" and args.pr is not None and not PULL_REQUEST.match(args.pr):
        parser.error(f"the pull request {args.pr!r} is not a decimal number")
    if args.form == "daily" and not MAX_AGE.match(args.max_age):
        parser.error(f"the window {args.max_age!r} is not a positive number of seconds")
    store = args.store.rstrip("/") or args.store
    try:
        if args.form == "daily":
            read = read_daily(os.path.join(store, DAILY_FILE))
            row = None if read is None else read.newest_within(utc_now(), int(args.max_age))
            print(NONE if row is None else "\t".join((row.ts_text, row.head_sha, row.verifier, row.evidence)))
            return 0
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
