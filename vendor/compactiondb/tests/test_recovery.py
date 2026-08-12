from __future__ import annotations

import unittest

from tests.support import TempProject
from contextdb.recovery import build_recovery_context


class RecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def test_raw_recovery_never_mixes_sessions(self) -> None:
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "S1_UNIQUE request"})
        self.p.event({"hook_event_name": "PostToolUse", "session_id": "s1", "tool_name": "Write", "tool_input": {"file_path": "src/s1.py", "content": "x=1"}, "tool_response": {"success": True}})
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": "S2_SECRET_CONTEXT request"})
        self.p.event({"hook_event_name": "PostToolUse", "session_id": "s2", "tool_name": "Write", "tool_input": {"file_path": "src/s2.py", "content": "x=2"}, "tool_response": {"success": True}})
        self.p.event({"hook_event_name": "PostCompact", "session_id": "s1", "trigger": "auto", "compact_summary": "S1 compact summary"})
        conn = self.p.store.connect()
        try:
            context = build_recovery_context(self.p.store, conn, session_id="s1")
        finally:
            conn.close()
        self.assertIn("S1_UNIQUE", context)
        self.assertIn("src/s1.py", context)
        self.assertIn("S1 compact summary", context)
        self.assertNotIn("S2_SECRET_CONTEXT", context)
        self.assertNotIn("src/s2.py", context)
        self.assertIn("--session s1", context)

    def test_project_memory_can_cross_sessions_only_after_promotion(self) -> None:
        self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s2",
                "prompt": "[memory:decision] Project-wide API version is v2.",
            }
        )
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "Current session request"})
        conn = self.p.store.connect()
        try:
            context = build_recovery_context(self.p.store, conn, session_id="s1")
        finally:
            conn.close()
        self.assertIn("Project-wide API version is v2", context)

    def test_recovery_respects_character_budget(self) -> None:
        self.p.config["recovery"]["max_chars"] = 1800
        self.p.store.config = self.p.config
        for i in range(30):
            self.p.event(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "s1",
                    "prompt": f"request {i} " + "x" * 300,
                }
            )
        conn = self.p.store.connect()
        try:
            context = build_recovery_context(self.p.store, conn, session_id="s1")
        finally:
            conn.close()
        self.assertLessEqual(len(context), 1800)
        self.assertIn("historical evidence", context)
