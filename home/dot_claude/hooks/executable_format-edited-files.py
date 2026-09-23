#!/usr/bin/env python3
"""Format files reported by Claude Code hook JSON input.

The hook reads the complete JSON event from stdin, extracts every edited file path
from common Write/Edit/MultiEdit payload shapes, and filters by suffix. Files are then
grouped by the git repository that contains them (via `git -C <parent> rev-parse
--show-toplevel`; a file outside any git repository is grouped by its own parent
directory), and each formatter runs once per group with the group's root as `cwd` and
file paths made relative to that root. Running from each file's own repository root,
rather than whatever directory the hook happened to inherit, lets prettier discover a
`.prettierignore` and lets ruff discover `ruff.toml`/`pyproject.toml` the same way they
would from an interactive shell at the repo root. Ruff is also passed `--force-exclude`,
since ruff only honors `exclude`/`extend-exclude` for explicit CLI paths (as this hook
always passes) when that flag is set.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PYTHON_COMMANDS = [
    ["uvx", "ruff", "format", "--force-exclude"],
    ["uvx", "ruff", "check", "--fix", "--force-exclude"],
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


def repository_root(path: Path) -> Path:
    """The git toplevel containing `path`, or its parent directory if none."""
    parent = path.parent
    result = subprocess.run(
        ["git", "-C", str(parent), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return parent
    return Path(result.stdout.strip())


def group_by_repository_root(paths: list[Path]) -> dict[Path, list[Path]]:
    groups: dict[Path, list[Path]] = {}
    for path in paths:
        groups.setdefault(repository_root(path), []).append(path)
    return groups


def run_commands(
    commands: list[list[str]], files: list[Path], *, prettier_ignore: bool = False
) -> int:
    status = 0
    if not files:
        return status
    for root, group_files in group_by_repository_root(files).items():
        relative_args = [str(f.relative_to(root)) for f in group_files]
        for command in commands:
            full_command = list(command)
            if prettier_ignore:
                ignore_path = root / ".prettierignore"
                if ignore_path.is_file():
                    full_command += ["--ignore-path", str(ignore_path)]
            result = subprocess.run(full_command + relative_args, cwd=root, check=False)
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

    paths = sorted(
        {
            path.resolve()
            for path in collect_paths(payload.get("tool_input", payload))
            if path.exists()
        }
    )
    python_files = [path for path in paths if path.suffix == ".py"]
    markdown_files = [path for path in paths if path.suffix == ".md"]

    status = 0
    status = max(status, run_commands(PYTHON_COMMANDS, python_files))
    status = max(
        status, run_commands(MARKDOWN_COMMANDS, markdown_files, prettier_ignore=True)
    )
    return status


if __name__ == "__main__":
    raise SystemExit(main())
