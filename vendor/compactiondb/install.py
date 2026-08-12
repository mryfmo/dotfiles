#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BEGIN = "<!-- compactiondb:begin -->"
END = "<!-- compactiondb:end -->"
GITIGNORE_LINES = [
    ".claude/contextdb/state/*",
    "!.claude/contextdb/state/.gitkeep",
    ".claude/contextdb/spool/incoming/*",
    "!.claude/contextdb/spool/incoming/.gitkeep",
    ".claude/contextdb/spool/quarantine/*",
    "!.claude/contextdb/spool/quarantine/.gitkeep",
    ".claude/contextdb/health/*",
    "!.claude/contextdb/health/.gitkeep",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or upgrade CompactionDB in a Claude Code project")
    parser.add_argument("--project", default=".", help="target project root")
    parser.add_argument("--python", default=sys.executable, help="Python executable stored in hook settings")
    parser.add_argument("--skip-instructions", action="store_true", help="do not update CLAUDE.md")
    parser.add_argument("--migrate-legacy", action="store_true", help="import .claude/logs/context_log.db after installation")
    return parser.parse_args()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def replace_python(settings: dict[str, Any], executable: str) -> dict[str, Any]:
    cloned = json.loads(json.dumps(settings))
    for groups in cloned.get("hooks", {}).values():
        for group in groups:
            for handler in group.get("hooks", []):
                args = handler.get("args") or []
                if any("contextdb_" in str(item) or "query_log.py" in str(item) for item in args):
                    handler["command"] = executable
    return cloned


def _is_contextdb_group(group: dict[str, Any]) -> bool:
    for handler in group.get("hooks", []):
        command = str(handler.get("command") or "")
        args = [str(item) for item in (handler.get("args") or [])]
        joined = " ".join([command, *args])
        if "contextdb_" in joined or "query_log.py" in joined or "log_event.py" in joined or "on_compact.py" in joined:
            return True
    return False


def merge_settings(existing: dict[str, Any], fragment: dict[str, Any]) -> tuple[dict[str, Any], int, int]:
    """Replace only prior ContextDB groups while preserving every unrelated hook."""
    result = json.loads(json.dumps(existing))
    hooks = result.setdefault("hooks", {})
    added = 0
    removed = 0
    for event, groups in fragment.get("hooks", {}).items():
        current = hooks.setdefault(event, [])
        retained = [group for group in current if not _is_contextdb_group(group)]
        removed += len(current) - len(retained)
        existing_keys = {canonical(group) for group in retained}
        for group in groups:
            key = canonical(group)
            if key not in existing_keys:
                retained.append(group)
                existing_keys.add(key)
                added += 1
        hooks[event] = retained
    return result, added, removed


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    destination = path.with_name(f"{path.name}.compactiondb-backup-{stamp}")
    shutil.copy2(path, destination)
    return destination


def append_instruction(path: Path, snippet: str) -> bool:
    if path.exists():
        text = path.read_text(encoding="utf-8")
    else:
        text = ""
    if BEGIN in text and END in text:
        before, remainder = text.split(BEGIN, 1)
        _, after = remainder.split(END, 1)
        updated = before.rstrip() + "\n\n" + snippet.strip() + "\n" + after.lstrip("\n")
    else:
        updated = text.rstrip() + ("\n\n" if text.strip() else "") + snippet.strip() + "\n"
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def update_gitignore(path: Path) -> int:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = set(text.splitlines())
    missing = [line for line in GITIGNORE_LINES if line not in lines]
    if missing:
        text = text.rstrip() + ("\n" if text else "") + "\n".join(missing) + "\n"
        path.write_text(text, encoding="utf-8")
    return len(missing)


def copy_file(source: Path, destination: Path, *, executable: bool = False) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        same = source.resolve() == destination.resolve()
    except OSError:
        same = False
    if not same:
        shutil.copy2(source, destination)
    if executable:
        try:
            os.chmod(destination, 0o755)
        except OSError:
            pass


def main() -> int:
    args = parse_args()
    source = Path(__file__).resolve().parent
    target = Path(args.project).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    target_claude = target / ".claude"
    target_hooks = target_claude / "hooks"
    target_contextdb = target_claude / "contextdb"
    target_hooks.mkdir(parents=True, exist_ok=True)
    target_contextdb.mkdir(parents=True, exist_ok=True)

    for name in ("contextdb_hook.py", "contextdb_recover.py", "contextdb_cli.py", "query_log.py"):
        copy_file(source / ".claude" / "hooks" / name, target_hooks / name, executable=True)

    runtime_source = source / ".claude" / "contextdb" / "contextdb"
    runtime_target = target_contextdb / "contextdb"
    if runtime_source.resolve() != runtime_target.resolve():
        shutil.copytree(
            runtime_source,
            runtime_target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
    config_target = target_contextdb / "config.json"
    if not config_target.exists():
        copy_file(source / ".claude" / "contextdb" / "config.json", config_target)
    try:
        os.chmod(config_target, 0o600)
    except OSError:
        pass
    for relative in ("state", "spool/incoming", "spool/quarantine", "health"):
        directory = target_contextdb / relative
        directory.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(directory, 0o700)
        except OSError:
            pass
        (directory / ".gitkeep").touch(exist_ok=True)

    settings_path = target_claude / "settings.json"
    current: dict[str, Any] = {}
    if settings_path.exists():
        current = json.loads(settings_path.read_text(encoding="utf-8"))
        if not isinstance(current, dict):
            raise ValueError(f"settings must be a JSON object: {settings_path}")
    fragment = json.loads((source / ".claude" / "settings.fragment.json").read_text(encoding="utf-8"))
    fragment = replace_python(fragment, str(Path(args.python).expanduser().resolve()))
    merged, added, removed = merge_settings(current, fragment)
    settings_backup = backup(settings_path) if settings_path.exists() and canonical(current) != canonical(merged) else None
    settings_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    instructions_changed = False
    if not args.skip_instructions:
        snippet = (source / "snippets" / "CLAUDE_CONTEXTDB.md").read_text(encoding="utf-8")
        instructions_changed = append_instruction(target / "CLAUDE.md", snippet)
    gitignore_added = update_gitignore(target / ".gitignore")

    print(f"project={target}")
    print(f"python={Path(args.python).expanduser().resolve()}")
    print(f"hook_groups_added={added}")
    print(f"previous_contextdb_hook_groups_removed={removed}")
    print(f"claude_md_updated={str(instructions_changed).lower()}")
    print(f"gitignore_lines_added={gitignore_added}")
    if settings_backup:
        print(f"settings_backup={settings_backup}")

    if args.migrate_legacy:
        migration = source / "migrate_legacy.py"
        code = os.spawnv(os.P_WAIT, str(Path(args.python).expanduser().resolve()), [str(args.python), str(migration), "--project", str(target)])
        if code:
            return code
    print(f"Run: {Path(args.python).expanduser().resolve()} .claude/hooks/contextdb_cli.py health")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
