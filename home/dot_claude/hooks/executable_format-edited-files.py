#!/usr/bin/env python3
"""Format files reported by Claude Code hook JSON input.

The hook reads the complete JSON event from stdin, extracts every edited file path
from common Write/Edit/MultiEdit payload shapes, filters by suffix, and runs the
formatter for that suffix without going through a shell. ruff and prettier come
from PATH: their versions are pinned in the mise config, and ruff.toml and
.prettierignore keep vendored and record paths untouched.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

PYTHON_COMMANDS = [
    ["ruff", "format"],
]
MARKDOWN_COMMANDS = [
    ["prettier", "--write"],
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


def repository_root(path: Path) -> Path:
    """The git work tree containing path, else its directory: where the formatter configs live."""
    try:
        result = subprocess.run(
            ["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return path.parent
    root = result.stdout.rstrip("\n")
    return Path(root) if result.returncode == 0 and root else path.parent


def run_commands(commands: list[list[str]], files: list[Path]) -> int:
    status = 0
    # Run from each file's repository root: prettier reads .prettierignore from
    # its working directory, and the session's directory may be another tree.
    by_root: dict[Path, list[str]] = {}
    for path in files:
        resolved = path.resolve()
        by_root.setdefault(repository_root(resolved), []).append(str(resolved))
    for root, file_args in sorted(by_root.items()):
        for command in commands:
            config = root / "ruff.toml"
            if command[0] == "ruff" and config.is_file():
                # Pin the root config: ruff otherwise picks each file's nearest
                # pyproject.toml (vendor/compactiondb) and skips the root exclusions.
                command = [*command, "--config", str(config)]
            try:
                result = subprocess.run(command + file_args, cwd=root, check=False)
            except FileNotFoundError:
                # make update installs every declared mise tool, so a missing formatter means that step was skipped or failed.
                print(
                    f"{command[0]} is not installed; run `make update` (it installs every declared mise tool)",
                    file=sys.stderr,
                )
                status = max(status, 1)
                continue
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
