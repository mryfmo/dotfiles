#!/usr/bin/env python3
"""Smoke-test the exact statusline binaries with representative Claude input."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import tomllib
from pathlib import Path


CLAUDE_STATUS = {
    "model": {"display_name": "Claude"},
    "workspace": {"current_dir": "/private/tmp"},
    "session_id": "offline-test",
    "transcript_path": "/private/tmp/nonexistent.jsonl",
}
MISE_CONFIG = Path(__file__).resolve().parents[1] / "home/dot_mise/config.toml"


def expected_versions() -> dict[str, str]:
    """The pins in home/dot_mise/config.toml, the one place they are declared."""
    tools = tomllib.loads(MISE_CONFIG.read_text())["tools"]
    return {name: tools[f"npm:{name}"] for name in ("ccstatusline", "ccusage")}


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
    args = parser.parse_args()

    for name, version in expected_versions().items():
        binary = getattr(args, name)
        if not binary.is_file():
            raise SystemExit(f"missing {name} binary: {binary}")
        require_version(binary, version)

    status_json = json.dumps(CLAUDE_STATUS) + "\n"
    run([str(args.ccstatusline)], status_json)
    run([str(args.ccusage), "statusline"], status_json)


if __name__ == "__main__":
    main()
