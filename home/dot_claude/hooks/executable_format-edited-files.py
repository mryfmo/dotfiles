#!/usr/bin/env python3
"""Format files reported by Claude Code hook JSON input.

The hook reads the complete JSON event from stdin, extracts every edited file path
from common Write/Edit/MultiEdit payload shapes, filters by suffix, and invokes
configured format/check commands without going through a shell.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

PYTHON_COMMANDS = [
    ["uvx", "ruff", "format"],
    ["uvx", "ruff", "check", "--fix"],
    ["uvx", "ty", "check"],
]
MARKDOWN_COMMANDS = [
    ["npx", "prettier@2", "--write"],
]


def collect_paths(value: Any) -> set[Path]:
    paths: set[Path] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"file_path", "path"} and isinstance(item, str):
                paths.add(Path(item))
            else:
                paths.update(collect_paths(item))
    elif isinstance(value, list):
        for item in value:
            paths.update(collect_paths(item))
    return paths


def run_commands(commands: list[list[str]], files: list[Path]) -> int:
    status = 0
    if not files:
        return status
    file_args = [str(path) for path in files]
    for command in commands:
        result = subprocess.run(command + file_args, check=False)
        status = max(status, result.returncode)
    return status


def main() -> int:
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        print(f"failed to parse Claude hook input: {error}", file=sys.stderr)
        return 0

    paths = sorted(path for path in collect_paths(payload.get("tool_input", payload)) if path.exists())
    python_files = [path for path in paths if path.suffix == ".py"]
    markdown_files = [path for path in paths if path.suffix == ".md"]

    status = 0
    status = max(status, run_commands(PYTHON_COMMANDS, python_files))
    status = max(status, run_commands(MARKDOWN_COMMANDS, markdown_files))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
