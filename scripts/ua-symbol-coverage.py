#!/usr/bin/env python3
"""Compare function+class node counts per file between two Understand-Anything graphs.

Usage: ua-symbol-coverage.py <old-graph.json> <new-graph.json> [--repo-ref REF]

Prints one row per `filePath` (old count, new count, and the number of
def-like source lines at REF when given) and exits 1 when a file lost
function/class nodes while its source still has at least as many def-like
lines as the old graph had symbols. Without --repo-ref every decrease counts
as a regression; a file whose source is gone at REF, or whose def-like count
fell below the old symbol count, is an explained decrease. `validateGraph`
checks schema and references only, so this is the completeness gate for a
`.ua/` refresh (home/dot_config/claude/rules/understand-anything.md).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SYMBOL_TYPES = {"function", "class"}
PYTHON_DEF = re.compile(r"^\s*(?:async\s+def|def|class)\s+\w+")
RUBY_DEF = re.compile(r"^\s*(?:def|class|module)\s+\S+")
SHELL_DEF = re.compile(r"^\s*(?:function\s+[\w:.-]+|[\w:.-]+\s*\(\))(?:\s*[{(].*)?\s*$")


def symbol_counts(graph_path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in json.loads(graph_path.read_text())["nodes"]:
        path = node.get("filePath")
        if not path:
            continue
        counts.setdefault(path, 0)
        if node.get("type") in SYMBOL_TYPES:
            counts[path] += 1
    return counts


def def_pattern(path: str, text: str) -> re.Pattern[str] | None:
    first = text.split("\n", 1)[0]
    if path.endswith(".py") or "python" in first:
        return PYTHON_DEF
    if path.endswith(".rb") or "ruby" in first:
        return RUBY_DEF
    if path.endswith((".sh", ".bash", ".zsh", ".bats")) or re.search(
        r"\b(?:ba|z)?sh\b", first
    ):
        return SHELL_DEF
    return None


def def_lines(ref: str, path: str) -> int | str | None:
    """Return def-like line count at REF, "-" without a grammar, or None when the file is gone."""
    shown = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    if shown.returncode != 0:
        return None
    pattern = def_pattern(path, shown.stdout)
    if pattern is None:
        return "-"
    return sum(1 for line in shown.stdout.splitlines() if pattern.search(line))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_graph", type=Path)
    parser.add_argument("new_graph", type=Path)
    parser.add_argument("--repo-ref", help="git ref whose source explains decreases")
    args = parser.parse_args(argv)

    old, new = symbol_counts(args.old_graph), symbol_counts(args.new_graph)
    regressions = 0
    print("| file | old | new | def-like lines | status |")
    print("|---|---|---|---|---|")
    for path in sorted(set(old) | set(new)):
        before, after = old.get(path, 0), new.get(path, 0)
        defs = def_lines(args.repo_ref, path) if args.repo_ref else "-"
        status = "ok"
        if after < before:
            gone = args.repo_ref and defs is None
            shrank = isinstance(defs, int) and defs < before
            status = "explained" if gone or shrank else "REGRESSION"
            regressions += status == "REGRESSION"
        print(
            f"| {path} | {before} | {after} | {'gone' if defs is None else defs} | {status} |"
        )
    print(f"files: {len(set(old) | set(new))}, regressions: {regressions}")
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
