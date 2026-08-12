from __future__ import annotations

import json
import unittest

from tests.support import TempProject
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
