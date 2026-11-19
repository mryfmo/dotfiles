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
"no row"). The rows are split on the line feed; the ledger's reader then drops exactly one trailing carriage return
from each line, the header's included, before the cells are checked (`parse_rows(..., trailing_cr=True)`; U597 round
10, verdict U597-67e1eea8 P2 at :381: the base of this unit read a CR LF ledger, and installed stores written that way
must keep reading, so a CR LF ledger parses as before the unit, while a second carriage return, CR CR LF, is a control
character in the last cell and Malformed naming the line and the field as round 8 made it), where the daily file's
reader drops none (the file is new to this unit, so no store holds a CR LF one; a daily row ends in LF alone). A `Row`
carries its ts parsed (`ts`, a datetime, the order every
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
round 5's `strptime` alone read it), no cell holding a control character (round 7; a carriage return included and
never stripped from a daily row, round 8 and round 10, so a daily row ends in LF alone), no empty cell, a `head_sha`
of 40 hex, the verifier and the evidence the exact fields of the sweep rule (`security-audit-skill <pin>`, a findings
file `sweeps/<path>.json`), and, since round 9 (verdict U597-c37800e3 P2 at :393, where the daily reader applied the
sweep row's grammar alone and a recent row of a unit's shape, `TASK U9` with a pinned verifier and an existing
findings path, read back as the day's sweep of main's head), the daily row's own grammar, the exact fields
`ledger-row.py daily` writes: the verifier `security-audit-skill <pin> (full audit mode on the srt worker seat <seat>,
run-<n>; TASK daily-<YYYY-MM-DD>)` (`DAILY_VERIFIER`, the task the daily dispatch's id alone, its day the ts's UTC day
or the day before, a sweep that crosses midnight) and the evidence's seven `; `-separated fields in the writer's order,
`<findings>; <n> findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS; validators sha256 <8 hex>
<8 hex> <8 hex>; artifacts sha256 <8 hex> <8 hex>; recorded <ts>` (`daily_fields_fault`: the count, the two
validators' PASS words, the first 8 hex of the three pins the writer held its private copies of validate-findings.cjs,
validate-coverage-ledger.cjs and report-schema.json to (round 10: the schema's pin too, verdict U597-67e1eea8 P2 at
ledger-row.py:575), the first 8 hex of the sha256 of the writer's private copies of the findings file and the coverage
ledger beside it, the bytes the count and the PASS words were earned over (round 10, the P2 at ledger-row.py:574), and
the recording time under the one ts form), each fault naming the line and the field, so a row shaped like a unit's
sweep row is Malformed, never a daily row. `DailyRow` exposes the parsed fields (`seat`, `run`, `task_day`,
`validator_digests`, `artifact_digests`, `recorded`). `Daily.newest_within(now, max_age)` is the newest row by `(ts,
line)` whose ts lies within the window `now - max_age <= ts <= now + DAILY_FUTURE_SLACK` (60 seconds, the reader's
allowance for a row another host's clock wrote; the writer refuses a ts after its own clock, round 7; round 5: a row
dated further in the future is not within the window, so it does not count and is not refused as malformed, where
round 4's floor alone let a future-dated row waive per-head sweeps until a day after its ts). `ledger.py <store> daily
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
# and a line feed the row's end, so neither is in a cell, and a NUL in an evidence path is dropped by bash's `$(...)`
# when pr-merge.sh captures the row, so the lever would check another file than the one the row names). A cell that
# holds one is Malformed naming the line and the field. A carriage return is one of them wherever it stands in a cell
# (round 8, verdict U597-a28e4793 P3 at :373: the parsers stripped every trailing CR before the cells were checked, so
# a row ending in CR CR LF carried an extra control byte and passed); which reader drops one trailing CR from a line
# before the cells are read is parse_rows's `trailing_cr` (round 10: the ledger's does, the daily file's does not).
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
# The daily row's own grammar (U597 round 9; verdict U597-c37800e3 P2 at :393): the verifier as `ledger-row.py daily`
# composes it, the skill, its pin word (8 or more lowercase hex, SWEEP_VERIFIER's group), the seat (one word), the run
# and the task `daily-<YYYY-MM-DD>`, the daily dispatch's id alone (a unit id is a `sweep` row's task, never a daily
# row's), whose day is the ts's UTC day or the day before it (the writer's rule: a sweep that crosses midnight keeps
# the id it was dispatched under); and the evidence's seven `; `-separated fields in the writer's order: the findings
# file (the sweep rule's field, no whitespace around it), `<n> findings`, the two validators' PASS words, `validators
# sha256 <8 hex> <8 hex> <8 hex>` (the first 8 hex of the pins the writer held its private copies of
# validate-findings.cjs, validate-coverage-ledger.cjs and report-schema.json to, in that order; round 10 added the
# schema's, verdict U597-67e1eea8 P2 at ledger-row.py:575; pr-merge.sh compares each with the manifest's
# `validators_sha256` pins), `artifacts sha256 <8 hex> <8 hex>` (the first 8 hex of the sha256 of the writer's private
# copies of the findings file and the coverage ledger beside it, the one set of bytes the count and the PASS words
# attest; round 10, the P2 at ledger-row.py:574; pr-merge.sh requires the field by shape and never opens the files) and
# `recorded <ts>` (the clock at the write, the one ts form). A row of another shape is Malformed naming the field.
DAILY_VERIFIER = re.compile(
    r"^security-audit-skill ([0-9a-f]{8,}) \(full audit mode on the srt worker seat (\S+), run-(0|[1-9][0-9]*); "
    r"TASK daily-([0-9]{4}-[0-9]{2}-[0-9]{2})\)$"
)
DAILY_VERIFIER_FORM = (
    "security-audit-skill <pin> (full audit mode on the srt worker seat <seat>, run-<n>; TASK daily-<YYYY-MM-DD>)"
)
DAILY_EVIDENCE_FORM = (
    "sweeps/<path>.json; <n> findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS; "
    "validators sha256 <8 hex> <8 hex> <8 hex>; artifacts sha256 <8 hex> <8 hex>; recorded <ts>"
)
DAILY_SEPARATOR = "; "
DAILY_FIELDS = 7
DAILY_COUNT = re.compile(r"^(0|[1-9][0-9]*) findings$")
DAILY_PASSES = ("validate-findings.cjs PASS", "validate-coverage-ledger.cjs PASS")
DAILY_DIGESTS = re.compile(r"^validators sha256 ([0-9a-f]{8}) ([0-9a-f]{8}) ([0-9a-f]{8})$")
DAILY_DIGESTS_FORM = "validators sha256 <8 hex> <8 hex> <8 hex>"
DAILY_ARTIFACTS = re.compile(r"^artifacts sha256 ([0-9a-f]{8}) ([0-9a-f]{8})$")
DAILY_ARTIFACTS_FORM = "artifacts sha256 <8 hex> <8 hex>"
DAILY_RECORDED = "recorded "
DAY_FORMAT = "%Y-%m-%d"


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


def daily_fields_fault(verifier, evidence, at):
    """Why a verifier and an evidence are not those of the daily row `ledger-row.py daily` writes (U597 round 9),
    naming the field, or None, after sweep_fields_fault held the fields the sweep rule's rows share: the verifier
    matches DAILY_VERIFIER with a task day that is the ts `at`'s UTC day or the day before it, and the evidence has
    exactly DAILY_FIELDS `; `-separated fields, the findings file unpadded, `<n> findings`, the two PASS words, the
    three 8-hex validator digests, the two 8-hex artifact digests (round 10) and `recorded <ts>` under the one ts
    form."""
    match = DAILY_VERIFIER.match(verifier)
    if match is None:
        return (
            f"the verifier of a daily sweep row is not {DAILY_VERIFIER_FORM!r} (the daily dispatch's task alone, a "
            f"unit id never): {verifier!r}"
        )
    try:
        task_day = datetime.strptime(match.group(4), DAY_FORMAT)
    except ValueError:
        return f"the TASK day of a daily sweep row is no calendar day: daily-{match.group(4)}"
    behind = (datetime(at.year, at.month, at.day) - task_day).days
    if behind not in (0, 1):
        return (
            f"the TASK day daily-{match.group(4)} of a daily sweep row is neither the UTC day of its ts "
            f"{at.strftime(TS_FORMAT)} nor the day before it"
        )
    fields = evidence.split(DAILY_SEPARATOR)
    if len(fields) != DAILY_FIELDS:
        return (
            f"the evidence of a daily sweep row has {len(fields)} '; '-separated fields, not {DAILY_FIELDS} "
            f"({DAILY_EVIDENCE_FORM!r}): {evidence!r}"
        )
    if fields[0] != fields[0].strip():
        return f"field 1 of the evidence of a daily sweep row, the findings file, is padded with spaces: {fields[0]!r}"
    if DAILY_COUNT.match(fields[1]) is None:
        return f"field 2 of the evidence of a daily sweep row is not '<n> findings': {fields[1]!r}"
    for number, expected in enumerate(DAILY_PASSES, 3):
        if fields[number - 1] != expected:
            return f"field {number} of the evidence of a daily sweep row is not {expected!r}: {fields[number - 1]!r}"
    if DAILY_DIGESTS.match(fields[4]) is None:
        return (
            f"field 5 of the evidence of a daily sweep row is not {DAILY_DIGESTS_FORM!r} (the first 8 hex of the "
            "three pins the writer held its copies of validate-findings.cjs, validate-coverage-ledger.cjs and "
            f"report-schema.json to): {fields[4]!r}"
        )
    if DAILY_ARTIFACTS.match(fields[5]) is None:
        return (
            f"field 6 of the evidence of a daily sweep row is not {DAILY_ARTIFACTS_FORM!r} (the first 8 hex of the "
            f"sha256 of the writer's copies of the findings file and the coverage ledger it validated): {fields[5]!r}"
        )
    if not fields[6].startswith(DAILY_RECORDED) or timestamp(fields[6][len(DAILY_RECORDED) :]) is None:
        return f"field 7 of the evidence of a daily sweep row is not 'recorded <{TS_FORM}>': {fields[6]!r}"
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


def parse_rows(name, text, header, required, trailing_cr):
    """The data rows of one tab-separated store file as `(number, ts, fields)` tuples, or Malformed naming `name` and
    the line: the one row reader of `ledger.tsv` and `daily-sweeps.tsv` (U597 round 10), stating once how a line
    becomes cells. The text is split on the line feed (a trailing one closes the last row); when `trailing_cr` is
    true exactly one carriage return is dropped from the end of each line, the header's included, before anything is
    read, else none. Why the two files differ (round 10, verdict U597-67e1eea8 P2 at :381): the ledger has installed
    stores to keep reading, and the base of this unit read a CR LF `ledger.tsv` (its readers stripped the trailing
    carriage returns), so a CR LF ledger must parse as before the unit; the daily file is new to this unit, no store
    holds a CR LF one, and its rows end in LF alone. Either way the cells are then held to CONTROL (round 7), so a
    second carriage return, CR CR LF (round 8, the P3 at :373), is a control character in the last cell and
    Malformed naming the line and the field. Then the header must be `header` exactly, every other line must split
    on the tab into `header`'s column count, hold no control character in a cell, carry a ts of the one form in its
    first cell and no empty cell among `required` (1-based column numbers)."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if trailing_cr:
        lines = [line[:-1] if line.endswith("\r") else line for line in lines]
    expected = "\t".join(header)
    if not lines or lines[0] != expected:
        found = lines[0] if lines else ""
        raise Malformed(f"{name}:1: the header is {found!r}, not {expected!r}")
    for number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != len(header):
            raise Malformed(f"{name}:{number}: {len(fields)} columns, not {len(header)}")
        control_check(name, number, header, fields)
        at = timestamp(fields[0])
        if at is None:
            raise Malformed(f"{name}:{number}: the ts {fields[0]!r} is not {TS_FORM}")
        for column in required:
            if fields[column - 1] == "":
                raise Malformed(f"{name}:{number}: column {column} ({header[column - 1]}) is empty")
        yield number, at, fields


def parse_ledger(name, text):
    """The Ledger of one `ledger.tsv` text, or Malformed naming `name` and the line (parse_rows with the ledger's
    header and required cells, one trailing carriage return per line dropped: the base's tolerance of a CR LF ledger,
    kept for the installed stores; round 10)."""
    rows = [
        Row(at, *fields[1:], number, fields[0]) for number, at, fields in parse_rows(name, text, HEADER, REQUIRED, True)
    ]
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

    @property
    def seat(self):
        """The srt worker seat the verifier names (DAILY_VERIFIER), or None for a verifier of another shape."""
        match = DAILY_VERIFIER.match(self.verifier)
        return None if match is None else match.group(2)

    @property
    def run(self):
        """The run number the verifier names, as written, or None."""
        match = DAILY_VERIFIER.match(self.verifier)
        return None if match is None else match.group(3)

    @property
    def task_day(self):
        """The `YYYY-MM-DD` of the verifier's `TASK daily-<day>`, or None."""
        match = DAILY_VERIFIER.match(self.verifier)
        return None if match is None else match.group(4)

    @property
    def validator_digests(self):
        """The three 8-hex digest prefixes of the evidence's `validators sha256` field (validate-findings.cjs,
        validate-coverage-ledger.cjs, report-schema.json; round 10 added the schema's), or None."""
        fields = self.evidence.split(DAILY_SEPARATOR)
        match = DAILY_DIGESTS.match(fields[4]) if len(fields) == DAILY_FIELDS else None
        return None if match is None else (match.group(1), match.group(2), match.group(3))

    @property
    def artifact_digests(self):
        """The two 8-hex digest prefixes of the evidence's `artifacts sha256` field (the findings file, the coverage
        ledger; round 10), or None."""
        fields = self.evidence.split(DAILY_SEPARATOR)
        match = DAILY_ARTIFACTS.match(fields[5]) if len(fields) == DAILY_FIELDS else None
        return None if match is None else (match.group(1), match.group(2))

    @property
    def recorded(self):
        """The recording time of the evidence's `recorded <ts>` field as a datetime, or None."""
        fields = self.evidence.split(DAILY_SEPARATOR)
        if len(fields) != DAILY_FIELDS or not fields[6].startswith(DAILY_RECORDED):
            return None
        return timestamp(fields[6][len(DAILY_RECORDED) :])


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
    ledger's strictness (parse_rows with the daily header, every cell required and no trailing carriage return
    dropped: a daily row ends in LF alone, round 8 and round 10), a 40-hex head, the verifier and the evidence the
    exact fields of the sweep rule (U597 round 4) and the daily row's own grammar (round 9: daily_fields_fault, so a
    row of a unit's sweep shape is Malformed, never a daily row)."""
    rows = []
    for number, at, fields in parse_rows(name, text, DAILY_HEADER, DAILY_REQUIRED, False):
        if not SHA.match(fields[1]):
            raise Malformed(f"{name}:{number}: the head_sha of a daily sweep row is not 40 hex: {fields[1]!r}")
        fault = sweep_fields_fault(fields[2], fields[3], "a daily sweep row")
        if fault is None:
            fault = daily_fields_fault(fields[2], fields[3], at)
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
