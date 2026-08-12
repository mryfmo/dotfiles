#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import the original CompactionDB context_log.db")
    parser.add_argument("--project", default=".")
    parser.add_argument("--legacy-db", help="defaults to .claude/logs/context_log.db")
    return parser.parse_args()


def load_runtime(project: Path):
    sys.path.insert(0, str(project / ".claude" / "contextdb"))
    from contextdb.config import load_config
    from contextdb.normalize import encode_detail, normalize_hook_payload
    from contextdb.paths import project_paths
    from contextdb.spool import drain_spool, spool_event

    return load_config, encode_detail, normalize_hook_payload, project_paths, drain_spool, spool_event


def payload_for(row: sqlite3.Row) -> dict[str, Any]:
    event_type = str(row["event_type"] or "")
    detail = str(row["detail"] or "")
    base: dict[str, Any] = {
        "session_id": str(row["session_id"] or "legacy"),
        "event_uuid": f"legacy-{row['id']}",
        "legacy_event_id": row["id"],
        "legacy_ts": row["ts"],
    }
    if event_type == "user_prompt":
        return {**base, "hook_event_name": "UserPromptSubmit", "prompt": detail}
    if event_type == "tool_use":
        try:
            obj = json.loads(detail)
        except json.JSONDecodeError:
            obj = {"tool_input": {}, "tool_output": detail}
        return {
            **base,
            "hook_event_name": "PostToolUse",
            "tool_name": str(row["tool_name"] or "LegacyTool"),
            "tool_input": obj.get("tool_input", {}),
            "tool_response": obj.get("tool_output", ""),
        }
    if event_type == "compact":
        return {**base, "hook_event_name": "PreCompact", "trigger": "legacy", "custom_instructions": detail}
    return {**base, "hook_event_name": "LegacyEvent", "legacy_summary": row["summary"], "legacy_detail": detail}


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser().resolve()
    legacy = Path(args.legacy_db).expanduser().resolve() if args.legacy_db else project / ".claude" / "logs" / "context_log.db"
    if not legacy.exists():
        print(f"legacy DB not found: {legacy}", file=sys.stderr)
        return 2
    load_config, encode_detail, normalize_hook_payload, project_paths, drain_spool, spool_event = load_runtime(project)
    paths = project_paths(explicit=project)
    config = load_config(paths)
    source = sqlite3.connect(legacy)
    source.row_factory = sqlite3.Row
    try:
        rows = source.execute("SELECT id, ts, session_id, event_type, tool_name, summary, detail FROM events ORDER BY id").fetchall()
    finally:
        source.close()
    for row in rows:
        payload = payload_for(row)
        payload["cwd"] = str(project)
        event = normalize_hook_payload(payload, paths, config)
        event["source"] = "legacy-v1"
        event["normalized_detail"]["legacy_ts"] = row["ts"]
        event["normalized_detail"]["legacy_summary"] = row["summary"]
        event["normalized_detail"], event["detail_json"] = encode_detail(
            event["normalized_detail"], int(config.get("capture", {}).get("max_detail_chars", 100000))
        )
        from contextdb.util import sha256_text

        event["detail_sha256"] = sha256_text(event["detail_json"])
        spool_event(paths, event)
    result = drain_spool(paths, config, blocking_lock=True, max_files=max(len(rows), 1))
    print(f"legacy_rows={len(rows)} inserted={result.inserted} duplicates={result.duplicates} pending={result.remaining}")
    return 0 if result.remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
