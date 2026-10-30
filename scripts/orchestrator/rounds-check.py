#!/usr/bin/env python3
"""Allow or refuse a unit's next audit round by the round cap and the two-strike rule (regime-cutover U120, order 36).

`rounds-check.py <store> U<n>` reads `<store>/ledger.tsv` and `<store>/decisions.tsv` as data and exits 0 when the
unit's next audit is allowed, 1 with a one-line reason when it is not, and 2 when the store cannot be read as data (a
missing file, a header that is not the store's, a row with the wrong column count, a ts outside `YYYY-MM-DDThh:mm:ssZ`,
an `incorrect` row from 2026-10-30 on whose evidence does not start with `class=<word>`, standing order 39), naming the
file and line. `rounds-check.py --all <store>` checks every unit of the ledger, prints one line per refused unit and
exits 1 when any is refused. With `--all <path> --base <commit> --head <commit>` the two files are read from the head
commit's tree (`git cat-file blob`), as the `regime` check reads a pull request whose head is never checked out, and a
head whose two files are the blobs of its merge base with the base is nothing to check (exit 0): the check runs on the
records pull requests by their content, never by a branch name.

The rule (standing order 36). An audit row is a ledger row whose verdict is exactly `correct` or `incorrect`. A
mechanism row for U<n> is a decisions row of phase `mechanism-change` whose decision starts with `U<n> ` or `U<n>:` and
whose result names exactly one of ast, parser-module, allowlist, remove, residual. The next audit is refused when the
unit has a mechanism row and two or more `incorrect` rows after its latest one, or has no mechanism row and three or
more audit rows, each naming the row the coordinator must write; it is allowed otherwise. Neither test stands behind
the other: a unit whose counted rows are one mechanism row and two `incorrect` rows after it is refused although it
has fewer than three audit rows (round 3). The rule is forward-looking: an audit
row or a mechanism row whose ts is before RULE_EFFECTIVE (2026-10-30T00:00:00Z, the day standing orders 36 and 39 were
written) is read and validated for shape but counted for neither the cap nor the strikes, the earlier rounds being
P-41's measurement and not a gate; the allowed and refused lines name how many such rows were ignored. The same date is
the one from which an `incorrect` row needs its `class=` token. The class judgement (the `class=` token) stays the
coordinator's: this check counts rows and never reads a pull request.
"""

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass

LEDGER_HEADER = ("ts", "unit", "pr", "head_sha", "verdict", "verifier", "evidence")
DECISIONS_HEADER = ("ts", "phase", "decision", "why", "evidence", "result")
AUDIT_VERDICTS = frozenset(("correct", "incorrect"))
MECHANISM_PHASE = "mechanism-change"
FORMS = ("ast", "parser-module", "allowlist", "remove", "residual")
ROUND_CAP = 3  # audit rows a unit may have before its next round needs a mechanism row
STRIKES = 2  # incorrect rows after the latest mechanism row that need another one
RULE_EFFECTIVE = "2026-10-30T00:00:00Z"  # standing orders 36 and 39: rows before it are read and never counted
# The store's ts is fixed-width UTC, so the text order is the time order and no row needs a parsed date.
TS = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
UNIT = re.compile(r"^U[0-9]+[a-z]?$")
UNIT_PREFIX = re.compile(r"^(U[0-9]+[a-z]?)[ :]")
CLASS = re.compile(r"^class=\S+(\s|$)")
# A form is a whole token of the result: `allowlisted` or `ast-free` names none.
FORM_TOKENS = {form: re.compile(rf"(?<![A-Za-z0-9-]){re.escape(form)}(?![A-Za-z0-9-])") for form in FORMS}
ROW_TO_WRITE = 'decisions.tsv phase=mechanism-change decision="{unit} ..." result names one of ' + "|".join(FORMS)
OBJECT_ID = re.compile(r"^[0-9a-f]{40,64}$")


@dataclass(frozen=True)
class AuditRow:
    """One audit round of `unit`: a ledger row whose verdict is `correct` or `incorrect`."""

    ts: str
    unit: str
    verdict: str
    line: int


@dataclass(frozen=True)
class MechanismRow:
    """A decisions row of phase `mechanism-change` for `unit` whose result names exactly one closing form."""

    ts: str
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


class Malformed(Exception):
    """The store cannot be read as data; the message names the file and the line."""


@dataclass(frozen=True)
class Store:
    """The two files read once: every audit row, every mechanism row, the mechanism-change rows that count for no
    unit (no unit prefix, or none or several forms) as (ts, unit or None, line, forms), and every unit the ledger names
    in first-seen order."""

    audits: tuple
    mechanisms: tuple
    discounted: tuple
    units: tuple

    def verdict_for(self, unit):
        """Allowed or Refused for the unit's next audit, from the counts of its rows from RULE_EFFECTIVE on."""
        audits, earlier_audits = counted(row for row in self.audits if row.unit == unit)
        mechanisms, earlier_mechanisms = counted(row for row in self.mechanisms if row.unit == unit)
        earlier = earlier_audits + earlier_mechanisms
        latest = mechanisms[-1] if mechanisms else None
        strikes = sum(row.verdict == "incorrect" and (latest is None or row.ts > latest.ts) for row in audits)
        incorrect = sum(row.verdict == "incorrect" for row in audits)
        since = "the start" if latest is None else f"the mechanism-change row of {latest.ts} ({latest.form})"
        ignored = f", {earlier} earlier rows ignored (rule effective {RULE_EFFECTIVE[:10]})" if earlier else ""
        counts = (
            f"{len(audits)} audit rows ({incorrect} incorrect), {strikes} incorrect since {since}, "
            f"{len(mechanisms)} mechanism rows{ignored}"
        )
        discounted = [
            f"decisions.tsv:{line} is a mechanism-change row for {unit} naming {len(forms) or 'no'} form(s)"
            for ts, owner, line, forms in self.discounted
            if owner == unit and ts >= RULE_EFFECTIVE
        ]
        note = "".join(f"; {text}, so it does not count" for text in discounted)
        # the decision table of standing order 36: the strikes stand behind no cap and the cap behind no strikes
        refusals = (
            (latest is not None and strikes >= STRIKES, f"{STRIKES} strikes since that row need another"),
            (latest is None and len(audits) >= ROUND_CAP, "the fourth round needs a mechanism-change row"),
        )
        need = next((need for refused, need in refusals if refused), None)
        if need is None:
            return Allowed(unit, counts)
        return Refused(unit, f"{counts}{note}; {need}: write {ROW_TO_WRITE.format(unit=unit)}")


def counted(rows):
    """The rows from RULE_EFFECTIVE on in ts order, and how many earlier rows were left out of the count."""
    rows = sorted(rows, key=lambda row: row.ts)
    kept = [row for row in rows if row.ts >= RULE_EFFECTIVE]
    return kept, len(rows) - len(kept)


def parse_rows(name, text, header):
    """Every data line of one TSV text as (line number, fields), each line with the header's width and a store ts."""
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
        if not TS.match(fields[0]):
            raise Malformed(f"{name}:{number}: the ts {fields[0]!r} is not YYYY-MM-DDThh:mm:ssZ")
        rows.append((number, fields))
    return rows


def audit_rows(name, rows):
    found = []
    for number, (ts, unit, _pr, _head, verdict, _verifier, evidence) in rows:
        if verdict not in AUDIT_VERDICTS:
            continue
        if verdict == "incorrect" and ts >= RULE_EFFECTIVE and not CLASS.match(evidence):
            raise Malformed(
                f"{name}:{number}: an incorrect row from {RULE_EFFECTIVE} on whose evidence does not start with "
                "class=<word> (standing order 39)"
            )
        found.append(AuditRow(ts, unit, verdict, number))
    return tuple(found)


def mechanism_rows(rows):
    """The mechanism rows, and (ts, unit or None, line, forms) for each mechanism-change row that is not one."""
    found, discounted = [], []
    for number, (ts, phase, decision, _why, _evidence, result) in rows:
        if phase != MECHANISM_PHASE:
            continue
        owner = UNIT_PREFIX.match(decision)
        forms = tuple(form for form, token in FORM_TOKENS.items() if token.search(result))
        if owner is None or len(forms) != 1:
            discounted.append((ts, owner.group(1) if owner else None, number, forms))
            continue
        found.append(MechanismRow(ts, owner.group(1), forms[0], number))
    return tuple(found), tuple(discounted)


def load_store(read, ledger_name, decisions_name):
    """The Store from one reader of the two files; `read(name)` returns the text or raises Malformed."""
    ledger = parse_rows(ledger_name, read("ledger.tsv"), LEDGER_HEADER)
    decisions = parse_rows(decisions_name, read("decisions.tsv"), DECISIONS_HEADER)
    mechanisms, discounted = mechanism_rows(decisions)
    units = tuple(dict.fromkeys(fields[1] for _number, fields in ledger))
    return Store(audit_rows(ledger_name, ledger), mechanisms, discounted, units)


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
    except Malformed as error:
        print(f"rounds-check: {error}", file=sys.stderr)
        return 2
    if not args.all:
        verdict = loaded.verdict_for(args.unit)
        if isinstance(verdict, Refused):
            print(f"rounds-check: {verdict.unit} refused: {verdict.reason}")
            return 1
        print(f"rounds-check: {verdict.unit} allowed: {verdict.counts}")
        return 0
    refused = [verdict for verdict in map(loaded.verdict_for, loaded.units) if isinstance(verdict, Refused)]
    for verdict in refused:
        print(f"rounds-check: {verdict.unit} refused: {verdict.reason}")
    print(f"rounds-check: {len(loaded.units)} units checked, {len(refused)} refused", file=sys.stderr)
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
