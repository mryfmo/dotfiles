#!/usr/bin/env python3
"""List every filed finding of a program store, the issue list the operator reads (regime-cutover U125 round d).

`filed-findings.py <store>` reads every `<store>/verdicts/*.md` and prints one tab-separated table, `unit head8
priority f s path:line rationale`, of every finding whose weight (frequency times severity, the two scores of the
`[f<n> s<n>]` token) is under WEIGHT_THRESHOLD, sorted by unit then head, then the last line `filed findings: <n>`;
exit 0. A filed finding is reported by the audit and merged without a disposition (the weighted finding rule of
AGENTS.md "Audit", U124; the reader of pr-audit.sh counts them as `Filed: <n>` since U125 round a and the merge gate
skips them since round b), so this list is where they are read after the fact.

One grammar. The Findings section is read by `findings_of` of `audit-carry.py` beside this file, imported from that
path alone (the one reader behind the carry lever, under FINDINGS_GRAMMAR, the sentence pr-merge.sh states too); this
file parses no finding line of its own. The unit and the head are the file's name, `<unit>-<sha8>.md` (a fix unit's
`U<n>b-<sha8>.md`; an early re-audit `-r<n>` suffix is kept), and a name of another shape is exit 2 naming it.

A verdict of a form before the scored reader is skipped with one stderr note naming the file, never refused: the
reader writes a `Filed: <n>` line since U125 round a, and a verdict without that line is an earlier reader's (the
omp-run route, retired 2026-10-25, wrote no `## Findings` section or a table in it; the reader before U125 wrote
`- P<n> (<confidence>) <path>:<line>: <rationale>` without the scores), belongs to a merged unit and carries no score
to read; `scored` of `audit-carry.py` is the one predicate that says so, read by the carry lever too (U126), and this
file spells the `Filed:` marker nowhere. A verdict with the line is read strictly, and one the reader refuses (a score
outside 1 to 10, a line of another shape, `- none` beside a finding, an empty section) is exit 2 naming the file and
line, and so is a verdicts directory or file that cannot be read (standing order 21: a failed read is never "no filed
findings").
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))


def beside(name):
    """The module `<name>.py` beside this file, loaded from that path alone: the list runs under `python3 -I`, which
    puts no script directory on sys.path, and a module found by a search would not be the one beside it. A missing
    file, or one the import cannot read, is exit 2 naming it (standing order 21)."""
    path = os.path.join(HERE, f"{name}.py")
    if not os.path.isfile(path):
        print(
            f"filed-findings: {path}: no {name}.py beside the list; the findings are read through it alone",
            file=sys.stderr,
        )
        sys.exit(2)
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except OSError as error:
        print(f"filed-findings: {path}: cannot read: {error.strerror}", file=sys.stderr)
        sys.exit(2)
    except ImportError as error:
        print(f"filed-findings: {path}: cannot import: {error}", file=sys.stderr)
        sys.exit(2)
    return module


# The one reader of a Findings section (U125 round c) and of what a scored verdict is (`scored`, U126); its Malformed
# is exit 2.
audit_carry = beside("audit-carry")

# The weighted finding rule (AGENTS.md "Audit", U124): a finding weighs frequency times severity and is filed under
# this number, the one the reader of pr-audit.sh applies and pr-merge.sh names; tests.unit.test_filed_findings keeps
# this copy equal to the gate's.
WEIGHT_THRESHOLD = 10
# A verdict file's name as the SKILL copies it, `U<n>-<head8>.md`, a fix unit's under `U<n>b`, and the `-r<n>` suffix
# of the early re-audits of one head (U109).
VERDICT_NAME = re.compile(r"^(U([0-9]+)([a-z]?))-([0-9a-f]{8})(-r[0-9]+)?\.md$")
HEADER = ("unit", "head8", "priority", "f", "s", "path:line", "rationale")


def filed_findings(store):
    """Every filed finding of the store's verdict files as rows of HEADER's shape, sorted by unit then head, and the
    notes for the files skipped; Malformed for a store that cannot be read as data."""
    directory = os.path.join(store, "verdicts")
    try:
        names = sorted(name for name in os.listdir(directory) if name.endswith(".md"))
    except OSError as error:
        raise audit_carry.Malformed(f"{directory}: cannot read: {error.strerror}") from None
    rows, notes = [], []
    for name in names:
        match = VERDICT_NAME.match(name)
        if match is None:
            raise audit_carry.Malformed(f"{os.path.join(directory, name)}: not a verdict file name, U<n>-<sha8>.md")
        unit, head8 = match.group(1), match.group(4)
        verdict_file = os.path.join(directory, name)
        if not audit_carry.scored(verdict_file):
            notes.append(
                f"filed-findings: {verdict_file}: skipped, no `Filed: <n>` line, a verdict of a reader before U125"
            )
            continue
        listed = audit_carry.findings_of(verdict_file)
        key = (int(match.group(2)), match.group(3), head8, name)
        for priority, frequency, severity, path, line, rationale in listed:
            if frequency * severity < WEIGHT_THRESHOLD:
                rows.append((key, (unit, head8, priority, str(frequency), str(severity), f"{path}:{line}", rationale)))
    rows.sort(key=lambda row: row[0])
    return [row for _key, row in rows], notes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("store", help="the program store directory")
    args = parser.parse_args(argv)
    store = args.store.rstrip("/") or args.store
    try:
        rows, notes = filed_findings(store)
    except audit_carry.Malformed as error:
        print(f"filed-findings: {error}", file=sys.stderr)
        return 2
    for note in notes:
        print(note, file=sys.stderr)
    print("\t".join(HEADER))
    for row in rows:
        print("\t".join(row))
    print(f"filed findings: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
