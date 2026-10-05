from __future__ import annotations

import json
import os
import time
import unittest

from support import TempProject
from contextdb.hook import process_payload
from contextdb.recover_hook import recovery_output
from contextdb.spool import drain_spool


class HookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def test_post_tool_failure_fields_are_persisted(self) -> None:
        process_payload(
            {
                "hook_event_name": "PostToolUseFailure",
                "session_id": "s1",
                "cwd": str(self.p.root),
                "tool_name": "Bash",
                "tool_input": {"command": "pytest"},
                "tool_use_id": "toolu_1",
                "error": "exit status 1",
                "is_interrupt": False,
                "duration_ms": 100,
            },
            project_root=str(self.p.root),
        )
        drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        conn = self.p.store.connect()
        try:
            row = conn.execute("SELECT * FROM events").fetchone()
            self.assertEqual("tool_failure", row["event_type"])
            self.assertEqual(0, row["success"])
            self.assertIn("exit status 1", row["detail_json"])
        finally:
            conn.close()


    def test_stop_failure_preserves_official_error_fields(self) -> None:
        self.p.event(
            {
                "hook_event_name": "StopFailure",
                "session_id": "s1",
                "error": "rate_limit",
                "error_details": "429 Too Many Requests",
                "last_assistant_message": "API Error: Rate limit reached",
            }
        )
        conn = self.p.store.connect()
        try:
            row = conn.execute("SELECT * FROM events WHERE event_type='turn_failure'").fetchone()
            detail = json.loads(row["detail_json"])
            self.assertEqual("rate_limit", detail["error"])
            self.assertEqual("429 Too Many Requests", detail["error_details"])
            self.assertEqual("API Error: Rate limit reached", detail["last_assistant_message"])
        finally:
            conn.close()

    def test_subagent_and_task_lifecycle_fields_are_normalized(self) -> None:
        self.p.event(
            {
                "hook_event_name": "SubagentStart",
                "session_id": "s1",
                "agent_id": "agent-1",
                "agent_type": "Explore",
            }
        )
        self.p.event(
            {
                "hook_event_name": "TaskCreated",
                "session_id": "s1",
                "task_id": "task-1",
                "task_subject": "Implement authentication",
                "task_description": "Add login endpoint",
                "teammate_name": "implementer",
            }
        )
        self.p.event(
            {
                "hook_event_name": "TaskCompleted",
                "session_id": "s1",
                "task_id": "task-1",
                "task_subject": "Implement authentication",
                "task_description": "Add login endpoint",
                "teammate_name": "implementer",
            }
        )
        conn = self.p.store.connect()
        try:
            rows = conn.execute("SELECT event_type, summary, detail_json FROM events ORDER BY id").fetchall()
            self.assertEqual(["subagent_start", "task_created", "task_completed"], [row["event_type"] for row in rows])
            self.assertIn("Explore", rows[0]["summary"])
            created = json.loads(rows[1]["detail_json"])
            completed = json.loads(rows[2]["detail_json"])
            self.assertEqual("created", created["status"])
            self.assertEqual("completed", completed["status"])
            self.assertEqual("task-1", completed["task_id"])
        finally:
            conn.close()

    def test_recovery_hook_returns_only_structured_json(self) -> None:
        self.p.event({"hook_event_name": "PostCompact", "session_id": "s1", "trigger": "auto", "compact_summary": "summary"})
        output = recovery_output(
            {"hook_event_name": "SessionStart", "source": "compact", "session_id": "s1", "cwd": str(self.p.root)},
            project_root=str(self.p.root),
        )
        encoded = json.dumps(output, ensure_ascii=False)
        decoded = json.loads(encoded)
        self.assertEqual("SessionStart", decoded["hookSpecificOutput"]["hookEventName"])
        self.assertIn("summary", decoded["hookSpecificOutput"]["additionalContext"])

    def test_session_end_prunes_expired_events_and_runtime_logs(self) -> None:
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "old event"})
        conn = self.p.store.connect()
        try:
            with conn:
                conn.execute("UPDATE events SET ts_utc='2000-01-01T00:00:00.000Z'")
        finally:
            conn.close()
        self.p.paths.error_log_path.write_text('{"ts_utc":"2000-01-01T00:00:00Z"}\n', encoding="utf-8")
        quarantined = self.p.paths.quarantine_dir / "old.json"
        quarantined.write_text("{}", encoding="utf-8")
        old = time.time() - 40 * 86400
        os.utime(quarantined, (old, old))
        process_payload(
            {"hook_event_name": "SessionEnd", "session_id": "s1", "cwd": str(self.p.root)},
            project_root=str(self.p.root),
        )
        conn = self.p.store.connect()
        try:
            self.assertEqual(1, conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
        finally:
            conn.close()
        self.assertFalse(quarantined.exists())
        self.assertEqual("", self.p.paths.error_log_path.read_text())

    def test_health_retention_serializes_concurrent_error_appends(self) -> None:
        from concurrent.futures import ThreadPoolExecutor, TimeoutError
        from threading import Event
        from unittest.mock import patch
        from contextdb.hook import prune_health_artifacts
        from contextdb.spool import record_error

        for kept_line in ("", '{"ts_utc":"2999-01-01T00:00:00Z"}\n'):
            with self.subTest(keep_recent=bool(kept_line)):
                self.p.paths.error_log_path.write_text('{"ts_utc":"2000-01-01T00:00:00Z"}\n' + kept_line)
                original_inode = self.p.paths.error_log_path.stat().st_ino
                read_started, release = Event(), Event()
                loads = json.loads

                def paused_loads(line):
                    read_started.set()
                    if not release.wait(5):
                        raise RuntimeError("test did not release retention")
                    return loads(line)

                with ThreadPoolExecutor(max_workers=2) as pool, patch("contextdb.hook.json.loads", side_effect=paused_loads):
                    pruning = pool.submit(prune_health_artifacts, self.p.paths, days=30)
                    self.assertTrue(read_started.wait(5))
                    appending = pool.submit(record_error, self.p.paths, "concurrent", "keep this error")
                    try:
                        appending.result(timeout=0.2)
                    except TimeoutError:
                        pass
                    finally:
                        release.set()
                    pruning.result(timeout=5)
                    appending.result(timeout=5)
                self.assertEqual(original_inode, self.p.paths.error_log_path.stat().st_ino)
                records = [json.loads(line) for line in self.p.paths.error_log_path.read_text().splitlines()]
                self.assertEqual("keep this error", records[-1]["message"])
                self.assertEqual(2 if kept_line else 1, len(records))


class PlatformImportTests(unittest.TestCase):
    def test_imports_and_help_without_fcntl(self) -> None:
        import subprocess
        import sys
        from pathlib import Path

        runtime = Path(__file__).resolve().parents[1] / ".claude/contextdb"
        result = subprocess.run(
            [sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); sys.modules['fcntl'] = None; "
             "import contextdb.hook, contextdb.util; from contextdb.cli import main; main(['--help'])", str(runtime)],
            capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("usage:", result.stdout)

    def test_health_locking_without_fcntl_fails_before_writes(self) -> None:
        import sys
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from contextdb.hook import prune_health_artifacts
        from contextdb.util import append_jsonl

        with tempfile.TemporaryDirectory() as temp, patch.dict(sys.modules, {"fcntl": None}):
            target = Path(temp) / "not-created" / "errors.jsonl"
            with self.assertRaisesRegex(RuntimeError, "ContextDB health-log locking requires a POSIX platform"):
                append_jsonl(target, {"message": "test"})
            self.assertFalse(target.parent.exists())
            with self.assertRaisesRegex(RuntimeError, "ContextDB health-log locking requires a POSIX platform"):
                prune_health_artifacts(None, days=30)
