#!/usr/bin/env python3
"""Allow or refuse a unit's next audit round by the round cap and the two-strike rule (regime-cutover U120, order 36).

`rounds-check.py <store> U<n>` reads `<store>/ledger.tsv` (through `ledger.py` beside this file, the one reader of the
ledger since U122 round 6) and `<store>/decisions.tsv` as data and exits 0 when the unit's next audit is allowed, 1
with a one-line reason when it is not, and 2 when the store cannot be read as data (a missing file, a header that is
not the store's, a row with the wrong column count, a ts `strptime` does not read as `YYYY-MM-DDThh:mm:ssZ` (hour 25
included), an empty required ledger cell, an `incorrect` row from 2026-10-30 on whose evidence does not start with
`class=<word>`, standing order 39), naming the
file and line. `rounds-check.py <store> U<n> --pr <pr>` is the lever's form (round 6): a pull request's audit is gated
on a set of units, the body's unit and the `unit` of every ledger row whose `pr` cell is the pull request's number,
because a fix or residual unit (`U<n>b`) writes its parent `U<n>` in the body and keeps `U<n>b` in its rows (standing
order 24); every unit of the set is checked, one line per refused unit and a summary line on stderr, and one refused
unit refuses. `rounds-check.py --all <store>` checks every unit of the ledger, prints one line per refused unit and
exits 1 when any is refused. With `--all <path> --base <commit> --head <commit>` the two files are read from the head
commit's tree (`git cat-file blob`), as the `regime` check reads a pull request whose head is never checked out, and a
head whose two files are the blobs of its merge base with the base is nothing to check (exit 0): the check runs on the
records pull requests by their content, never by a branch name.

The rule (standing order 36). An audit row is a ledger row whose verdict is exactly `correct` or `incorrect`. A
mechanism row for U<n> is a decisions row of phase `mechanism-change` whose decision starts with `U<n> ` or `U<n>:` and
whose result names exactly one of ast, parser-module, allowlist, remove, residual. The next audit is refused when the
unit has a mechanism row and two or more `incorrect` rows of one class (the word of the `class=` token) after its
latest one, or has no mechanism row and three or more audit rows, each naming the row the coordinator must write; it
is allowed otherwise. The strikes are counted per class and the cap per row (round 7): two `incorrect` rows of
unrelated classes after the mechanism row are one strike each and refuse nothing, while three audit rows of three
classes and no mechanism row are the cap. Neither test stands behind the other: a unit whose counted rows are one
mechanism row and two `incorrect` rows of one class after it is refused although it has fewer than three audit rows
(round 3). The rule is forward-looking: an audit
row or a mechanism row whose ts is before RULE_EFFECTIVE (2026-10-30T00:00:00Z, the day standing orders 36 and 39 were
written) is read and validated for shape but counted for neither the cap nor the strikes, the earlier rounds being
P-41's measurement and not a gate; the allowed and refused lines name how many such rows were ignored. The same date is
the one from which an `incorrect` row needs its `class=` token. The class judgement (the `class=` token) stays the
coordinator's: this check compares the tokens' words for equality, judges none, and never reads a pull request.
"""

from __future__ import annotations  # the `str | None` field annotation, read as text by every python3 the lever meets

import argparse
import importlib.util
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime

HERE = os.path.dirname(os.path.realpath(__file__))


def beside(name):
    """The module `<name>.py` beside this file, loaded from that path alone: the check runs under `python3 -I`, which
    puts no script directory on sys.path, and a module found by a search would not be the one beside it. A missing
    file is exit 2 naming it."""
    path = os.path.join(HERE, f"{name}.py")
    if not os.path.isfile(path):
        print(
            f"rounds-check: {path}: no {name}.py beside the check; the ledger is read through it alone", file=sys.stderr
        )
        sys.exit(2)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ledger = beside("ledger")  # the one reader of ledger.tsv (U122 round 6); its Malformed is this check's exit 2

# The decisions file keeps a reader of its own here; its ts is read by the ledger reader's `timestamp`, the one form.
DECISIONS_HEADER = ("ts", "phase", "decision", "why", "evidence", "result")
AUDIT_VERDICTS = frozenset(("correct", "incorrect"))
MECHANISM_PHASE = "mechanism-change"
FORMS = ("ast", "parser-module", "allowlist", "remove", "residual")
ROUND_CAP = 3  # audit rows a unit may have before its next round needs a mechanism row
STRIKES = 2  # incorrect rows of one class after the latest mechanism row that need another one
RULE_EFFECTIVE = "2026-10-30T00:00:00Z"  # standing orders 36 and 39: rows before it are read and never counted
RULE_EFFECTIVE_AT = ledger.timestamp(RULE_EFFECTIVE)  # the same instant as every row's ts is compared, a datetime
UNIT = re.compile(r"^U[0-9]+[a-z]?$")
PULL_REQUEST = re.compile(r"^[1-9][0-9]{0,9}$")
UNIT_PREFIX = re.compile(r"^(U[0-9]+[a-z]?)[ :]")
CLASS = re.compile(r"^class=(\S+)(?:\s|$)")
# A form is a whole token of the result: `allowlisted` or `ast-free` names none.
FORM_TOKENS = {form: re.compile(rf"(?<![A-Za-z0-9-]){re.escape(form)}(?![A-Za-z0-9-])") for form in FORMS}
ROW_TO_WRITE = 'decisions.tsv phase=mechanism-change decision="{unit} ..." result names one of ' + "|".join(FORMS)
OBJECT_ID = re.compile(r"^[0-9a-f]{40,64}$")


@dataclass(frozen=True)
class AuditRow:
    """One audit round of `unit`: a ledger row whose verdict is `correct` or `incorrect`; `ts` is the row's ts parsed
    (the ledger reader's datetime, the order every count is made in); `klass` is the word of the evidence's `class=`
    token, None for a row without one (allowed before RULE_EFFECTIVE, and for `correct` rows)."""

    ts: datetime
    unit: str
    verdict: str
    line: int
    klass: str | None = None


@dataclass(frozen=True)
class MechanismRow:
    """A decisions row of phase `mechanism-change` for `unit` whose result names exactly one closing form; `ts` is
    parsed, `ts_text` the cell as written, for the lines that name the row."""

    ts: datetime
    ts_text: str
    unit: str
    form: str
    line: int


@dataclass(frozen=True)
class Allowed:
    unit: str
    counts: str


@dataclass(frozen=True)
class Refused:
    unit: str
    reason: str


class Malformed(ledger.Malformed):
    """The store cannot be read as data; the message names the file and the line (the ledger reader's own Malformed
    is the base, so main refuses on either alike)."""


@dataclass(frozen=True)
class Store:
    """The two files read once: every audit row, every mechanism row, the mechanism-change rows that count for no
    unit (no unit prefix, or none or several forms) as (ts, unit or None, line, forms), every unit the ledger names
    in first-seen order, and the (unit, pr) cells of every ledger row in file order."""

    audits: tuple
    mechanisms: tuple
    discounted: tuple
    units: tuple
    pull_requests: tuple

    def units_for(self, pr, body_unit):
        """The units a pull request's audit is gated on: the body's unit, then the unit of every ledger row whose `pr`
        cell is exactly the pull request's number (standing order 24: a fix or residual unit `U<n>b` writes its parent
        `U<n>` in the body and keeps `U<n>b` in its rows), each once, in first-seen order."""
        return tuple(dict.fromkeys((body_unit, *(unit for unit, number in self.pull_requests if number == pr))))

    def verdict_for(self, unit):
        """Allowed or Refused for the unit's next audit, from the counts of its rows from RULE_EFFECTIVE on: the cap
        counts audit rows, the strikes count the `incorrect` rows after the latest mechanism row per class."""
        audits, earlier_audits = counted(row for row in self.audits if row.unit == unit)
        mechanisms, earlier_mechanisms = counted(row for row in self.mechanisms if row.unit == unit)
        earlier = earlier_audits + earlier_mechanisms
        latest = mechanisms[-1] if mechanisms else None
        incorrect = [row for row in audits if row.verdict == "incorrect"]
        strikes = [row for row in incorrect if latest is None or row.ts > latest.ts]
        per_class = {}  # class word -> strikes of that class, in first-seen (ts) order; a counted strike has a class
        for row in strikes:
            per_class[row.klass] = per_class.get(row.klass, 0) + 1
        struck = [klass for klass, count in per_class.items() if count >= STRIKES]
        classes = ", ".join(f"{klass}={count}" for klass, count in per_class.items()) or "none"
        since = "the start" if latest is None else f"the mechanism-change row of {latest.ts_text} ({latest.form})"
        ignored = f", {earlier} earlier rows ignored (rule effective {RULE_EFFECTIVE[:10]})" if earlier else ""
        counts = (
            f"{len(audits)} audit rows ({len(incorrect)} incorrect), {len(strikes)} incorrect since {since} "
            f"(classes: {classes}), {len(mechanisms)} mechanism rows{ignored}"
        )
        discounted = [
            f"decisions.tsv:{line} is a mechanism-change row for {unit} naming {len(forms) or 'no'} form(s)"
            for ts, owner, line, forms in self.discounted
            if owner == unit and ts >= RULE_EFFECTIVE_AT
        ]
        note = "".join(f"; {text}, so it does not count" for text in discounted)
        # the decision table of standing order 36: the strikes (per class) stand behind no cap and the cap (per row)
        # behind no strikes
        refusals = (
            (
                latest is not None and bool(struck),
                f"{STRIKES} strikes of class {' and '.join(struck)} since that row need another",
            ),
            (latest is None and len(audits) >= ROUND_CAP, "the fourth round needs a mechanism-change row"),
        )
        need = next((need for refused, need in refusals if refused), None)
        if need is None:
            return Allowed(unit, counts)
        return Refused(unit, f"{counts}{note}; {need}: write {ROW_TO_WRITE.format(unit=unit)}")


def counted(rows):
    """The rows from RULE_EFFECTIVE on in ts order, and how many earlier rows were left out of the count."""
    rows = sorted(rows, key=lambda row: row.ts)
    kept = [row for row in rows if row.ts >= RULE_EFFECTIVE_AT]
    return kept, len(rows) - len(kept)


def parse_rows(name, text, header):
    """Every data line of one TSV text as (line number, parsed ts, fields), each line with the header's width and a
    ts the ledger reader's `timestamp` reads (the decisions file's own reader; the ledger's is `ledger.parse_ledger`).
    """
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    expected = "\t".join(header)
    if not lines or lines[0] != expected:
        found = lines[0] if lines else ""
        raise Malformed(f"{name}:1: the header is {found!r}, not {expected!r}")
    rows = []
    for number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != len(header):
            raise Malformed(f"{name}:{number}: {len(fields)} columns, not {len(header)}")
        at = ledger.timestamp(fields[0])
        if at is None:
            raise Malformed(f"{name}:{number}: the ts {fields[0]!r} is not {ledger.TS_FORM}")
        rows.append((number, at, fields))
    return rows


def audit_rows(name, rows):
    """Every audit row of the ledger reader's rows, with the word of its `class=` token; a post-date `incorrect` row
    without one is Malformed."""
    found = []
    for row in rows:
        if row.verdict not in AUDIT_VERDICTS:
            continue
        klass = CLASS.match(row.evidence)
        if row.verdict == "incorrect" and row.ts >= RULE_EFFECTIVE_AT and klass is None:
            raise Malformed(
                f"{name}:{row.line}: an incorrect row from {RULE_EFFECTIVE} on whose evidence does not start with "
                "class=<word> (standing order 39)"
            )
        found.append(AuditRow(row.ts, row.unit, row.verdict, row.line, klass.group(1) if klass else None))
    return tuple(found)


def mechanism_rows(rows):
    """The mechanism rows, and (ts, unit or None, line, forms) for each mechanism-change row that is not one."""
    found, discounted = [], []
    for number, at, (ts, phase, decision, _why, _evidence, result) in rows:
        if phase != MECHANISM_PHASE:
            continue
        owner = UNIT_PREFIX.match(decision)
        forms = tuple(form for form, token in FORM_TOKENS.items() if token.search(result))
        if owner is None or len(forms) != 1:
            discounted.append((at, owner.group(1) if owner else None, number, forms))
            continue
        found.append(MechanismRow(at, ts, owner.group(1), forms[0], number))
    return tuple(found), tuple(discounted)


def load_store(read, ledger_name, decisions_name):
    """The Store from one reader of the two files; `read(name)` returns the text or raises Malformed."""
    rows = ledger.parse_ledger(ledger_name, read("ledger.tsv")).rows
    decisions = parse_rows(decisions_name, read("decisions.tsv"), DECISIONS_HEADER)
    mechanisms, discounted = mechanism_rows(decisions)
    units = tuple(dict.fromkeys(row.unit for row in rows))
    pull_requests = tuple((row.unit, row.pr) for row in rows)
    return Store(audit_rows(ledger_name, rows), mechanisms, discounted, units, pull_requests)


def directory_reader(store):
    def read(name):
        path = os.path.join(store, name)
        try:
            with open(path, encoding="utf-8", newline="") as handle:
                return handle.read()
        except OSError as error:
            raise Malformed(f"{path}: cannot read: {error.strerror}") from None
        except UnicodeDecodeError as error:
            raise Malformed(f"{path}: not UTF-8: {error.reason}") from None

    return read


def git(*args):
    """One git read with its status checked; a failure is Malformed naming the command, never an empty answer."""
    out = subprocess.run(["git", *args], capture_output=True, check=False)
    if out.returncode:
        detail = out.stderr.decode(errors="replace").strip()[:200]
        raise Malformed(f"git {' '.join(args)} exited {out.returncode}: {detail}")
    return out.stdout


def object_id(text, what):
    found = text.decode(errors="replace").strip()
    if not OBJECT_ID.match(found):
        raise Malformed(f"git named no object for {what}: {found!r}")
    return found


def commit_reader(store, commit):
    def read(name):
        spec = f"{commit}:{store}/{name}"
        try:
            return git("cat-file", "blob", spec).decode("utf-8")
        except UnicodeDecodeError as error:
            raise Malformed(f"{spec}: not UTF-8: {error.reason}") from None

    return read


def unchanged_since_merge_base(store, base, head):
    """Whether both files of the store at `head` are the blobs of the merge base of `base` and `head`."""
    merge_base = object_id(git("merge-base", base, head), f"the merge base of {base} and {head}")
    for name in ("ledger.tsv", "decisions.tsv"):
        blobs = [
            object_id(git("rev-parse", "--verify", f"{commit}:{store}/{name}"), f"{commit}:{store}/{name}")
            for commit in (merge_base, head)
        ]
        if blobs[0] != blobs[1]:
            return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("store", help="the program store directory, or its repository path with --base and --head")
    parser.add_argument("unit", nargs="?", help="the unit whose next audit is asked for, U<n>")
    parser.add_argument("--pr", help="with a unit: the pull request whose ledger rows name the units it is gated on")
    parser.add_argument("--all", action="store_true", help="check every unit of the ledger")
    parser.add_argument("--base", help="with --all: the base commit; the head's files are read from git")
    parser.add_argument("--head", help="with --all: the head commit whose tree holds the store")
    args = parser.parse_args(argv)
    if args.all == (args.unit is not None):
        parser.error("name one unit, or --all")
    if (args.base is None) != (args.head is None) or (args.base is not None and not args.all):
        parser.error("--base and --head go together, with --all")
    if args.unit is not None and not UNIT.match(args.unit):
        parser.error(f"the unit {args.unit!r} is not U<n>")
    if args.pr is not None and (args.all or not PULL_REQUEST.match(args.pr)):
        parser.error("--pr takes the pull request's decimal number, with a unit")
    store = args.store.rstrip("/") or args.store
    try:
        if args.head is not None:
            if unchanged_since_merge_base(store, args.base, args.head):
                print(
                    f"rounds-check: {store}/ledger.tsv and decisions.tsv at {args.head[:12]} are the merge base's blobs; nothing to check"
                )
                return 0
            read = commit_reader(store, args.head)
            names = [f"{args.head[:12]}:{store}/{name}" for name in ("ledger.tsv", "decisions.tsv")]
        else:
            read = directory_reader(store)
            names = [os.path.join(store, name) for name in ("ledger.tsv", "decisions.tsv")]
        loaded = load_store(read, *names)
    except ledger.Malformed as error:
        print(f"rounds-check: {error}", file=sys.stderr)
        return 2
    if args.all:
        units = loaded.units
        summary = f"{len(units)} units checked"
    elif args.pr is not None:
        units = loaded.units_for(args.pr, args.unit)
        summary = f"pull request {args.pr} is gated on {len(units)} units ({', '.join(units)})"
    else:
        units = (args.unit,)
        summary = None
    verdicts = [loaded.verdict_for(unit) for unit in units]
    refused = [verdict for verdict in verdicts if isinstance(verdict, Refused)]
    # one line per refused unit when any is refused; the allowed lines, one per unit, only when none is (--all, which
    # may check a hundred units, prints no allowed line at all)
    for verdict in refused or (() if args.all else verdicts):
        if isinstance(verdict, Refused):
            print(f"rounds-check: {verdict.unit} refused: {verdict.reason}")
        else:
            print(f"rounds-check: {verdict.unit} allowed: {verdict.counts}")
    if summary is not None:
        sys.stdout.flush()  # the lever reads both streams through one pipe: the unit lines come before the summary
        print(f"rounds-check: {summary}, {len(refused)} refused", file=sys.stderr)
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
