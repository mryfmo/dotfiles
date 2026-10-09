#!/usr/bin/env python3
"""Smoke-test the mise-installed statusline binaries with representative Claude input."""

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
        raise SystemExit(f"{' '.join(command)} failed with {result.returncode}: {result.stderr.strip()}")
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
    # The versions mise resolved (`mise current`); config.toml requests "latest".
    parser.add_argument("--ccstatusline-version", required=True)
    parser.add_argument("--ccusage-version", required=True)
    args = parser.parse_args()

    for name in ("ccstatusline", "ccusage"):
        binary = getattr(args, name)
        version = getattr(args, f"{name}_version")
        if not binary.is_file():
            raise SystemExit(f"missing {name} binary: {binary}")
        require_version(binary, version)

    status_json = json.dumps(CLAUDE_STATUS) + "\n"
    run([str(args.ccstatusline)], status_json)
    run([str(args.ccusage), "statusline"], status_json)


if __name__ == "__main__":
    main()
