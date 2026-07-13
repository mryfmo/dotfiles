#!/usr/bin/env python3
"""Smoke-test the exact statusline binaries with representative Claude input."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path


CLAUDE_STATUS = {
    "model": {"display_name": "Claude"},
    "workspace": {"current_dir": "/private/tmp"},
    "session_id": "offline-test",
    "transcript_path": "/private/tmp/nonexistent.jsonl",
}
EXPECTED_VERSIONS = {"ccstatusline": "2.2.23", "ccusage": "20.0.17"}


def run(command: list[str], stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    started = time.monotonic()
    result = subprocess.run(
        command,
        input=stdin,
        text=True,
        capture_output=True,
        timeout=5,
    )
    elapsed = time.monotonic() - started
    if result.returncode != 0:
        raise SystemExit(
            f"{' '.join(command)} failed with {result.returncode}: {result.stderr.strip()}"
        )
    if elapsed >= 5:
        raise SystemExit(f"{' '.join(command)} exceeded the 5-second smoke-test limit")
    return result


def require_version(binary: Path, expected: str) -> None:
    output = run([str(binary), "--version"]).stdout.strip()
    if not re.search(rf"(?<![0-9.]){re.escape(expected)}(?![0-9.])", output):
        raise SystemExit(f"{binary.name} reported {output!r}; expected {expected}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ccstatusline", type=Path, required=True)
    parser.add_argument("--ccusage", type=Path, required=True)
    args = parser.parse_args()

    for name in EXPECTED_VERSIONS:
        binary = getattr(args, name)
        if not binary.is_file():
            raise SystemExit(f"missing {name} binary: {binary}")
        require_version(binary, EXPECTED_VERSIONS[name])

    status_json = json.dumps(CLAUDE_STATUS) + "\n"
    run([str(args.ccstatusline)], status_json)
    run([str(args.ccusage), "statusline"], status_json)


if __name__ == "__main__":
    main()
