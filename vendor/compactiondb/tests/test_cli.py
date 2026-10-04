from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout

from contextdb.cli import main

from tests.support import TempProject


class CliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "hello contextdb"})
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": "other session"})

    def tearDown(self) -> None:
        self.p.close()

    def invoke(self, args: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--project-root", str(self.p.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_recent_with_explicit_session(self) -> None:
        code, out, err = self.invoke(["recent", "30", "--session", "s1"])
        self.assertEqual(0, code, err)
        self.assertIn("hello contextdb", out)
        self.assertNotIn("other session", out)

    def test_show_rejects_cross_session_access_by_default(self) -> None:
        conn = self.p.store.connect()
        try:
            other_id = conn.execute("SELECT id FROM events WHERE session_id='s2'").fetchone()[0]
        finally:
            conn.close()
        code, out, err = self.invoke(["show", str(other_id), "--session", "s1"])
        self.assertEqual(2, code)
        self.assertIn("different session", err)

    def test_health_json(self) -> None:
        code, out, err = self.invoke(["--json", "health"])
        self.assertEqual(0, code, err)
        value = json.loads(out)
        self.assertEqual("ok", value["integrity"])

    def test_ingest_records_explicit_source(self) -> None:
        source = self.p.root / "codex-turn.json"
        source.write_text(
            json.dumps(
                {
                    "hook_event_name": "Stop",
                    "session_id": "codex-thread",
                    "cwd": str(self.p.root),
                    "last_assistant_message": "done",
                }
            ),
            encoding="utf-8",
        )

        code, out, err = self.invoke(["ingest", str(source), "--ingested-from", "codex"])

        self.assertEqual(0, code, err)
        self.assertIn("pending=0", out)
        conn = self.p.store.connect()
        try:
            row = conn.execute(
                "SELECT ingested_from FROM events WHERE session_id='codex-thread'"
            ).fetchone()
        finally:
            conn.close()
        self.assertEqual("codex", row["ingested_from"])

    def test_ingest_normalizes_a_codex_notify_payload(self) -> None:
        source = self.p.root / "codex-notify.json"
        source.write_text(
            json.dumps(
                {
                    "type": "agent-turn-complete",
                    "thread-id": "codex-thread-2",
                    "turn-id": "turn-1",
                    "cwd": str(self.p.root),
                    "client": "codex-tui",
                    "input-messages": ["rename the helper"],
                    "last-assistant-message": "renamed",
                }
            ),
            encoding="utf-8",
        )

        code, out, err = self.invoke(["ingest", str(source), "--ingested-from", "codex"])

        self.assertEqual(0, code, err)
        conn = self.p.store.connect()
        try:
            row = conn.execute(
                "SELECT hook_event_name, event_type, agent_id, detail_json FROM events WHERE session_id='codex-thread-2'"
            ).fetchone()
        finally:
            conn.close()
        self.assertEqual(("Stop", "turn_stop", "codex-tui"), (row["hook_event_name"], row["event_type"], row["agent_id"]))
        self.assertEqual("renamed", json.loads(row["detail_json"])["last_assistant_message"])

        # A repeated delivery of the same turn is one event (stable event_uuid from thread-id and turn-id).
        code, out, err = self.invoke(["ingest", str(source), "--ingested-from", "codex"])
        self.assertEqual(0, code, err)
        conn = self.p.store.connect()
        try:
            count = conn.execute("SELECT COUNT(*) FROM events WHERE session_id='codex-thread-2'").fetchone()[0]
        finally:
            conn.close()
        self.assertEqual(1, count)

    def test_prune_enforces_the_size_cap_and_vacuums(self) -> None:
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "[memory:decision] Keep it."})
        # An unpromoted session_outcome candidate goes with its event; the promoted one stays.
        self.p.event({"hook_event_name": "Stop", "session_id": "s1", "last_assistant_message": "The task completed."})
        self.assertEqual(2, self.p.count("memory_candidates"))
        config = json.loads(self.p.paths.config_path.read_text(encoding="utf-8"))
        config["capture"]["max_db_bytes"] = 1
        self.p.paths.config_path.write_text(json.dumps(config), encoding="utf-8")

        code, out, err = self.invoke(["--json", "prune"])

        self.assertEqual(0, code, err)
        result = json.loads(out)
        self.assertEqual(4, result["size_cap_removed_events"])
        self.assertTrue(result["vacuumed"])
        self.assertEqual(0, self.p.count("events"))
        self.assertEqual(1, self.p.count("memories"))
        conn = self.p.store.connect()
        try:
            rows = conn.execute("SELECT kind, promoted_memory_uuid FROM memory_candidates").fetchall()
        finally:
            conn.close()
        self.assertEqual(["decision"], [row["kind"] for row in rows])
        self.assertIsNotNone(rows[0]["promoted_memory_uuid"])

    def test_ingest_rejects_invalid_source(self) -> None:
        code, out, err = self.invoke(["ingest", "missing.json", "--ingested-from", "Codex!"])

        self.assertEqual(2, code)
        self.assertEqual("", out)
        self.assertIn("invalid ingestion source", err)
