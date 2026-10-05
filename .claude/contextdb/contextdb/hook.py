from __future__ import annotations

import json
import os
import stat
import sys
import time
from contextlib import closing
from datetime import datetime, timedelta, timezone
from typing import Any

from .config import load_config
from .normalize import normalize_hook_payload
from .paths import ProjectPaths, project_paths
from .spool import drain_spool, record_error, spool_event


def prune_health_artifacts(paths: ProjectPaths, *, days: int) -> None:
    """Apply the health retention policy shared by hooks and explicit prune."""
    try:
        import fcntl
    except ImportError as exc:
        raise RuntimeError("ContextDB health-log locking requires a POSIX platform") from exc

    cutoff_utc = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        fd = os.open(paths.error_log_path, os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        fd = None
    if fd is not None:
        with os.fdopen(fd, "r+", encoding="utf-8") as log:
            if not stat.S_ISREG(os.fstat(log.fileno()).st_mode):
                raise ValueError("ContextDB health log must be a regular file")
            fcntl.flock(log.fileno(), fcntl.LOCK_EX)
            retained = []
            for line in log.read().splitlines():
                try:
                    record = json.loads(line)
                    if not isinstance(record, dict):
                        raise ValueError("health record must be an object")
                    ts = datetime.fromisoformat(str(record.get("ts_utc", "")).replace("Z", "+00:00"))
                except (ValueError, TypeError, json.JSONDecodeError):
                    retained.append(line)
                    continue
                if ts.tzinfo is None or ts >= cutoff_utc:
                    retained.append(line)
            # Keep the inode, even when empty: appenders may already be waiting on its lock.
            log.seek(0)
            log.write("\n".join(retained) + ("\n" if retained else ""))
            log.truncate()
    cutoff = time.time() - days * 86400
    for path in paths.quarantine_dir.glob("*"):
        if path.name != ".gitkeep" and path.is_file() and path.stat().st_mtime < cutoff:
            path.unlink()


def process_payload(
    payload: dict[str, Any],
    *,
    project_root: str | None = None,
    ingested_from: str | None = None,
    maintenance: bool = True,
) -> None:
    paths = project_paths(payload, project_root)
    try:
        config = load_config(paths)
        event = normalize_hook_payload(payload, paths, config)
        spool_event(paths, event, ingested_from=ingested_from)
        # Non-blocking lock: another hook may already be the single writer.
        # The durable spool remains the source of truth until a later drain succeeds.
        drain_spool(paths, config, blocking_lock=False)
        # `ingest --no-maintenance` skips retention so a short-budget caller
        # (Codex's 3-second SessionEnd hook) only records the event.
        if maintenance and event.get("event_type") == "session_end":
            try:
                from .storage import ContextStore
                days = int(config.get("operations", {}).get("error_log_retention_days", 30))
                prune_health_artifacts(paths, days=days)
                store = ContextStore(paths, config)
                with closing(store.connect()) as conn, conn:
                    store.prune_expired(conn, paths.project_id, days=days)
            except Exception:
                pass
    except Exception as exc:
        record_error(paths, "hook", exc, hook_event_name=payload.get("hook_event_name", "Unknown"))


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw or "{}")
        if not isinstance(payload, dict):
            raise ValueError("hook input must be a JSON object")
        process_payload(payload)
    except Exception as exc:
        try:
            paths = project_paths()
            record_error(paths, "hook-input", exc)
        except Exception:
            pass
    # Logging is non-enforcing: never block the agent and never write to stdout.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
