#!/usr/bin/env python3
"""Refuse a U274 use-case table that breaks the DATA SHAPE; print row counts per table.

Usage: python3 -I check-tables.py <table.tsv>...

A table is one header row `id use_case source kind host command expected observed verdict ts` and data rows of
exactly ten tab-separated cells. Refused, each with the file, the line and the reason: a wrong column count (which
is also what a tab inside a cell produces), a carriage return or a bare newline inside a cell (a line that is not a
complete row), a `kind` outside {auto, host, operator, not-started}, a `host` outside {macos, ubuntu}, a `verdict`
outside {OK, NG, pending}, an `auto` row still `pending`, a `not-started` row whose `expected` names no `M-<n>` plan
item, an empty `id`, `use_case`, `source`, `command` or `expected`, a repeated `id`, a `pending` row with an
`observed` or a `ts`, an `OK` or `NG` row without both. Exit 0 and one count line per table when every table passes;
exit 1 after printing every refusal otherwise; exit 2 on usage or an unreadable file.
"""

import re
import sys
from pathlib import Path

HEADER = ["id", "use_case", "source", "kind", "host", "command", "expected", "observed", "verdict", "ts"]
KINDS = {"auto", "host", "operator", "not-started"}
HOSTS = {"macos", "ubuntu"}
VERDICTS = {"OK", "NG", "pending"}
REQUIRED = ("id", "use_case", "source", "command", "expected")
PLAN_ITEM = re.compile(r"\bM-\d+\b")
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def check(path: Path) -> tuple[list[str], dict[str, int]]:
    faults: list[str] = []
    counts = {"rows": 0, **{kind: 0 for kind in sorted(KINDS)}, **{verdict: 0 for verdict in sorted(VERDICTS)}}
    # newline="" keeps a carriage return as data; the default read would fold it into a line break.
    text = path.read_text(encoding="utf-8", newline="")
    if "\r" in text:
        faults.append(f"{path}: carriage return inside the file")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    else:
        faults.append(f"{path}: the file does not end with a newline")
    if not lines or lines[0].split("\t") != HEADER:
        faults.append(f"{path}:1: the header is not {' '.join(HEADER)}")
        return faults, counts
    seen: set[str] = set()
    for number, line in enumerate(lines[1:], start=2):
        cells = line.split("\t")
        if len(cells) != len(HEADER):
            faults.append(f"{path}:{number}: {len(cells)} cells, not {len(HEADER)} (a tab or newline inside a cell)")
            continue
        row = dict(zip(HEADER, cells))
        counts["rows"] += 1
        for name in REQUIRED:
            if not row[name].strip():
                faults.append(f"{path}:{number}: empty {name}")
        if row["id"] in seen:
            faults.append(f"{path}:{number}: repeated id {row['id']}")
        seen.add(row["id"])
        kind, host, verdict = row["kind"], row["host"], row["verdict"]
        if kind not in KINDS:
            faults.append(f"{path}:{number}: kind {kind!r} not in {sorted(KINDS)}")
        else:
            counts[kind] += 1
        if host not in HOSTS:
            faults.append(f"{path}:{number}: host {host!r} not in {sorted(HOSTS)}")
        if verdict not in VERDICTS:
            faults.append(f"{path}:{number}: verdict {verdict!r} not in {sorted(VERDICTS)}")
        else:
            counts[verdict] += 1
        if kind == "auto" and verdict == "pending":
            faults.append(f"{path}:{number}: auto row {row['id']} left pending")
        if kind == "not-started" and not PLAN_ITEM.search(row["expected"]):
            faults.append(f"{path}:{number}: not-started row {row['id']} names no M-<n> item in expected")
        if verdict == "pending" and (row["observed"] or row["ts"]):
            faults.append(f"{path}:{number}: pending row {row['id']} carries observed or ts")
        if verdict in {"OK", "NG"} and (not row["observed"] or not TS.match(row["ts"])):
            faults.append(f"{path}:{number}: judged row {row['id']} lacks observed or a UTC ts")
    return faults, counts


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    all_faults: list[str] = []
    report: list[str] = []
    for arg in argv[1:]:
        path = Path(arg)
        try:
            faults, counts = check(path)
        except OSError as exc:
            print(f"{path}: cannot read: {exc}", file=sys.stderr)
            return 2
        all_faults.extend(faults)
        report.append(
            f"{path.name}\trows={counts['rows']}\tauto={counts['auto']}\thost={counts['host']}"
            f"\toperator={counts['operator']}\tnot-started={counts['not-started']}"
            f"\tOK={counts['OK']}\tNG={counts['NG']}\tpending={counts['pending']}"
        )
    for fault in all_faults:
        print(fault, file=sys.stderr)
    if all_faults:
        return 1
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
