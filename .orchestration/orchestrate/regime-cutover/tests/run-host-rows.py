#!/usr/bin/env python3
"""Run the `host` rows of the U274 use-case tables on this host and write observed, verdict and ts back.

Usage: python3 -I run-host-rows.py --worktree DIR [--tables DIR] [--notes FILE] [--replay FILE] [--raw-out FILE]
                                   [--timeout SECONDS] [--host macos] [TABLE.tsv ...]

Selects every row with `kind=host`, `host=<host>` and `verdict=pending`, runs its `command` with `bash -lc` from the
worktree root (the seats' bus environment `HCOM_DIR`, `HCOM_TEAM` set), with one timeout per row, and writes back:

  observed  `exit <N>; <stdout+stderr>` on one line, tabs and newlines folded to spaces, at most 300 characters;
            a hand judgement is appended as `judged: <why>` and the output is trimmed to make room for it
  verdict   OK when the expected cell's `exit <N>` matches and every quoted literal appears (a literal preceded by
            `no` or `not` must be absent); a row whose expected cell has neither is judged by the notes file alone;
            a row judged by hand is OK only when both the machine rule and the hand judgement say so; a row the
            notes file says is not runnable is NG with the reason
  ts        the UTC time the command finished

The notes file (default `host-row-notes.txt` beside this script, tab-separated, named off the tables' `*.tsv` glob)
has the header `id run cwd verdict why`:
  run      empty runs the command cell as written; `SKIP: <reason>` records NG without running; any other text is
           the shell that resolves the cell's placeholder (the cell itself is never edited)
  cwd      an alternative working directory (the cell names one), empty for the worktree root
  verdict  OK or NG from the hand judgement, empty when the machine rule alone decides
  why      the one-line reason written into observed as `judged: <why>`

`--replay FILE` re-judges from the raw results of an earlier run (written to `--raw-out`, default
/tmp/u288/raw.json) without running any command, so a hand judgement can be added after the outputs are read.
Prints one summary line per table: OK, NG, pending counts over the selected rows. Exit 0 when every table was
written; exit 2 on a malformed table, a missing worktree or an unreadable notes file.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HEADER = ["id", "use_case", "source", "kind", "host", "command", "expected", "observed", "verdict", "ts"]
NOTES_HEADER = ["id", "run", "cwd", "verdict", "why"]
OBSERVED_MAX = 300
EXIT_RE = re.compile(r"\bexit (\d+)\b")
# A quoted literal is bounded by non-word characters on both sides, so an apostrophe inside prose (`the skill's`) is
# not an opening quote; `no` or `not` before it makes the literal one that must be absent.
LITERAL_RE = re.compile(r"(no |not )?(?<![A-Za-z0-9])(?:'([^']+)'|\"([^\"]+)\")(?![A-Za-z0-9])")
SEAT_ENV = {"HCOM_DIR": str(Path.home() / ".local/state/hcom-regime"), "HCOM_TEAM": "regime"}


def fold(text: str) -> str:
    return " ".join(text.replace("\t", " ").split())


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_table(path: Path) -> list[list[str]]:
    text = path.read_text(encoding="utf-8", newline="")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    rows = [line.split("\t") for line in lines]
    if not rows or rows[0] != HEADER:
        raise ValueError(f"{path}: the header is not {' '.join(HEADER)}")
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != len(HEADER):
            raise ValueError(f"{path}:{number}: {len(row)} cells, not {len(HEADER)}")
    return rows


def write_table(path: Path, rows: list[list[str]]) -> None:
    path.write_text("".join("\t".join(row) + "\n" for row in rows), encoding="utf-8", newline="")


def read_notes(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    rows = [line.split("\t") for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not rows or rows[0] != NOTES_HEADER:
        raise ValueError(f"{path}: the header is not {' '.join(NOTES_HEADER)}")
    notes: dict[str, dict[str, str]] = {}
    for number, row in enumerate(rows[1:], start=2):
        if len(row) != len(NOTES_HEADER):
            raise ValueError(f"{path}:{number}: {len(row)} cells, not {len(NOTES_HEADER)}")
        note = dict(zip(NOTES_HEADER, row))
        if note["verdict"] not in {"", "OK", "NG"}:
            raise ValueError(f"{path}:{number}: verdict {note['verdict']!r} is not OK, NG or empty")
        if note["verdict"] and not note["why"]:
            raise ValueError(f"{path}:{number}: a hand verdict needs a why")
        notes[note["id"]] = note
    return notes


def run_row(shell: str, cwd: Path, timeout: float) -> dict[str, object]:
    env = {**os.environ, **SEAT_ENV}
    try:
        done = subprocess.run(
            ["bash", "-lc", shell], cwd=cwd, env=env, capture_output=True, text=True, errors="replace",
            timeout=timeout, stdin=subprocess.DEVNULL,
        )
        return {"exit": done.returncode, "stdout": done.stdout, "stderr": done.stderr, "timeout": False, "ts": utc_now()}
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return {"exit": None, "stdout": out, "stderr": err, "timeout": True, "ts": utc_now()}


def machine_verdict(expected: str, exit_code: int | None, output: str) -> tuple[bool | None, list[str]]:
    """Return (verdict or None when the rule says nothing, reasons for a miss)."""
    reasons: list[str] = []
    decided = False
    for match in EXIT_RE.finditer(expected):
        decided = True
        if exit_code != int(match.group(1)):
            reasons.append(f"expected exit {match.group(1)}, got {exit_code}")
    for match in LITERAL_RE.finditer(expected):
        decided = True
        negated, literal = match.group(1), match.group(2) or match.group(3)
        present = literal in output
        if negated and present:
            reasons.append(f"literal {literal!r} present but expected absent")
        if not negated and not present:
            reasons.append(f"literal {literal!r} absent")
    if not decided:
        return None, []
    return not reasons, reasons


def compose_observed(prefix: str, output: str, suffix: str) -> str:
    room = OBSERVED_MAX - len(prefix) - len(suffix)
    if room < 0:
        return (prefix + suffix)[:OBSERVED_MAX]
    return prefix + output[:room] + suffix


def judge(row: dict[str, str], raw: dict[str, object], note: dict[str, str]) -> tuple[str, str, str]:
    if raw.get("skipped"):
        observed = compose_observed("not run: ", str(raw["reason"]), "")
        return observed, "NG", str(raw["ts"])
    exit_code = raw["exit"]
    output = fold(str(raw["stdout"]) + " " + str(raw["stderr"]))
    prefix = f"exit {exit_code}; " if not raw["timeout"] else "exit timeout; "
    verdict_machine, reasons = machine_verdict(row["expected"], exit_code if not raw["timeout"] else None, output)
    hand = note.get("verdict", "")
    parts: list[str] = []
    if reasons:
        parts.append("; ".join(reasons))
    if hand:
        parts.append(note["why"])
    elif verdict_machine is None:
        parts.append("no hand judgement supplied for an expected cell without exit N or a quoted literal")
    suffix = f" judged: {' / '.join(parts)}" if parts else ""
    if hand:
        verdict = "OK" if hand == "OK" and verdict_machine is not False else "NG"
    else:
        verdict = "OK" if verdict_machine else "NG"
    return compose_observed(prefix, output, suffix), verdict, str(raw["ts"])


def main(argv: list[str]) -> int:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--worktree", required=True, type=Path)
    parser.add_argument("--tables", type=Path, default=here)
    parser.add_argument("--notes", type=Path, default=here / "host-row-notes.txt")
    parser.add_argument("--replay", type=Path)
    parser.add_argument("--raw-out", type=Path, default=Path("/tmp/u288/raw.json"))
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--host", default="macos")
    parser.add_argument("tables_files", nargs="*", type=Path)
    args = parser.parse_args(argv[1:])
    if not args.worktree.is_dir():
        print(f"worktree {args.worktree} is not a directory", file=sys.stderr)
        return 2
    try:
        notes = read_notes(args.notes)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 2
    raw_all: dict[str, dict[str, object]] = {}
    if args.replay:
        raw_all = json.loads(args.replay.read_text(encoding="utf-8"))
    table_paths = args.tables_files or sorted(args.tables.glob("*.tsv"))
    tables: dict[Path, list[list[str]]] = {}
    for path in table_paths:
        try:
            tables[path] = read_table(path)
        except (OSError, ValueError) as exc:
            print(exc, file=sys.stderr)
            return 2
    summary: list[str] = []
    for path, rows in tables.items():
        counts = {"OK": 0, "NG": 0, "pending": 0}
        for row_cells in rows[1:]:
            row = dict(zip(HEADER, row_cells))
            selected = row["kind"] == "host" and row["host"] == args.host
            if args.replay:
                selected = selected and (row["verdict"] == "pending" or row["id"] in raw_all)
            else:
                selected = selected and row["verdict"] == "pending"
            if not selected:
                continue
            note = notes.get(row["id"], {})
            raw = raw_all.get(row["id"])
            if raw is None:
                if args.replay:
                    counts["pending"] += 1
                    print(f"{path.name} {row['id']}: no raw result in {args.replay}; left pending", file=sys.stderr)
                    continue
                run = note.get("run", "")
                if run.startswith("SKIP:"):
                    raw = {"skipped": True, "reason": run[len("SKIP:"):].strip(), "ts": utc_now()}
                else:
                    cwd = Path(note["cwd"]).expanduser() if note.get("cwd") else args.worktree
                    print(f"{path.name} {row['id']}: running", file=sys.stderr, flush=True)
                    raw = run_row(run or row["command"], cwd, args.timeout)
                    if run:
                        raw["resolved_shell"] = run
                raw_all[row["id"]] = raw
            observed, verdict, ts = judge(row, raw, note)
            row_cells[HEADER.index("observed")] = observed
            row_cells[HEADER.index("verdict")] = verdict
            row_cells[HEADER.index("ts")] = ts
            counts[verdict] += 1
        write_table(path, rows)
        summary.append(f"{path.name}\tOK={counts['OK']}\tNG={counts['NG']}\tpending={counts['pending']}")
    args.raw_out.parent.mkdir(parents=True, exist_ok=True)
    args.raw_out.write_text(json.dumps(raw_all, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\n".join(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
