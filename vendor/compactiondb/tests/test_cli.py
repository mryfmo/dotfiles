from __future__ import annotations

import io
import json
import os
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout

from support import TempProject
from contextdb.cli import main
from contextdb.normalize import normalize_hook_payload



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

    def test_explicit_prune_applies_configured_health_retention(self) -> None:
        from datetime import datetime, timedelta, timezone
        config = json.loads(self.p.paths.config_path.read_text()) if self.p.paths.config_path.exists() else {}
        config["operations"] = {"error_log_retention_days": 3}
        self.p.paths.config_path.write_text(json.dumps(config))
        old = datetime.now(timezone.utc) - timedelta(days=5)
        recent = datetime.now(timezone.utc) - timedelta(days=1)
        lines = [json.dumps({"ts_utc": t.isoformat()}) for t in (old, recent)]
        self.p.paths.error_log_path.write_text("\n".join([*lines, "invalid", "null", "[]"]) + "\n")
        for name, timestamp in (("old.json", old.timestamp()), ("recent.json", recent.timestamp()), (".gitkeep", old.timestamp())):
            path = self.p.paths.quarantine_dir / name
            path.write_text("{}")
            os.utime(path, (timestamp, timestamp))
        code, _, err = self.invoke(["prune"])
        self.assertEqual(0, code, err)
        self.assertEqual([lines[1], "invalid", "null", "[]"], self.p.paths.error_log_path.read_text().splitlines())
        self.assertEqual({"recent.json", ".gitkeep"}, {p.name for p in self.p.paths.quarantine_dir.iterdir()})
        self.p.paths.error_log_path.write_text(lines[0] + "\n")
        self.invoke(["prune"])
        self.assertEqual("", self.p.paths.error_log_path.read_text())

    def test_prune_rejects_invalid_health_policy_before_removing_events(self) -> None:
        for operations in (None, [], {"error_log_retention_days": -1}, {"error_log_retention_days": "3"}, {"error_log_retention_days": True}, {"error_log_retention_days": 1000000}, {"error_log_retention_days": 10 ** 100}):
            with self.subTest(operations=operations):
                self.p.paths.config_path.write_text(json.dumps({"operations": operations}))
                code, _, err = self.invoke(["prune", "--days", "0"])
                self.assertEqual(2, code, err)
                self.assertIn("operations", err)
                self.assertEqual(2, self.p.count("events"))

    def test_prune_refuses_symlinked_health_log_without_touching_target(self) -> None:
        outside = self.p.root / "outside.jsonl"
        original = '{"ts_utc":"2000-01-01T00:00:00Z"}\n{"ts_utc":"2999-01-01T00:00:00Z"}\n'
        outside.write_text(original)
        self.p.paths.error_log_path.symlink_to(outside)
        code, _, err = self.invoke(["prune", "--days", "0"])
        self.assertEqual(2, code, err)
        self.assertEqual(2, self.p.count("events"))
        self.assertEqual(original, outside.read_text())
        self.assertTrue(self.p.paths.error_log_path.is_symlink())

    def test_prune_rejects_invalid_utf8_health_log_before_removing_events(self) -> None:
        self.p.paths.error_log_path.write_bytes(b"\xff")
        code, _, err = self.invoke(["prune", "--days", "0"])
        self.assertEqual(2, code, err)
        self.assertEqual(2, self.p.count("events"))
        self.assertEqual(b"\xff", self.p.paths.error_log_path.read_bytes())

    def test_ingest_no_maintenance_records_session_end_without_retention(self) -> None:
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
        source = self.p.root / "codex-session-end.json"
        source.write_text(
            json.dumps({"hook_event_name": "SessionEnd", "session_id": "codex-end", "cwd": str(self.p.root)}),
            encoding="utf-8",
        )

        code, out, err = self.invoke(["ingest", str(source), "--ingested-from", "codex", "--no-maintenance"])

        self.assertEqual(0, code, err)
        conn = self.p.store.connect()
        try:
            rows = conn.execute("SELECT session_id, event_type FROM events ORDER BY id").fetchall()
        finally:
            conn.close()
        self.assertEqual(["s1", "s2", "codex-end"], [row["session_id"] for row in rows])
        self.assertEqual("session_end", rows[-1]["event_type"])
        self.assertTrue(quarantined.exists())
        self.assertTrue(self.p.paths.error_log_path.exists())

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

    def _bulk_events_expiring(self, count: int, expired: int) -> int:
        """Insert count FTS-heavy events, mark the first `expired` as expired, return the file bytes."""
        conn = self.p.store.connect()
        try:
            with conn:
                for i in range(count):
                    event = normalize_hook_payload(
                        {
                            "hook_event_name": "UserPromptSubmit",
                            "session_id": "bulk",
                            "cwd": str(self.p.root),
                            "prompt": " ".join(f"token{i}x{j}" for j in range(150)),
                        },
                        self.p.paths,
                        self.p.config,
                    )
                    self.p.store.insert_event(conn, event, ingested_from="test")
                conn.execute(
                    "UPDATE events SET expires_at_utc='2000-01-01T00:00:00.000Z' WHERE id IN "
                    "(SELECT id FROM events ORDER BY id LIMIT ?)",
                    (expired,),
                )
            used, free = self.p.store._page_bytes(conn)
            return used + free
        finally:
            conn.close()

    def _set_cap(self, max_db_bytes: int) -> None:
        config = json.loads(self.p.paths.config_path.read_text(encoding="utf-8"))
        config["capture"]["max_db_bytes"] = max_db_bytes
        self.p.paths.config_path.write_text(json.dumps(config), encoding="utf-8")

    def _file_bytes(self) -> int:
        conn = self.p.store.connect()
        try:
            used, free = self.p.store._page_bytes(conn)
            return used + free
        finally:
            conn.close()

    def test_prune_vacuums_after_a_retention_only_shrink(self) -> None:
        before = self._bulk_events_expiring(300, expired=200)
        self._set_cap(before - 1)

        code, out, err = self.invoke(["--json", "prune"])

        self.assertEqual(0, code, err)
        result = json.loads(out)
        self.assertEqual((200, 0, True), (result["removed_events"], result["size_cap_removed_events"], result["vacuumed"]))
        self.assertLess(self._file_bytes(), before - 1)

    def test_prune_reclaims_the_fts_pages_when_retention_empties_the_table(self) -> None:
        fresh = self._file_bytes()
        before = self._bulk_events_expiring(300, expired=302)  # every event, including the two from setUp
        self._set_cap(fresh * 4)
        self.assertGreater(before, fresh * 4)

        code, out, err = self.invoke(["--json", "prune"])

        self.assertEqual(0, code, err)
        result = json.loads(out)
        self.assertEqual((0, True), (result["size_cap_removed_events"], result["vacuumed"]))
        self.assertEqual(0, self.p.count("events"))
        self.assertLessEqual(self._file_bytes(), fresh * 4)

    def test_ingest_rejects_invalid_source(self) -> None:
        code, out, err = self.invoke(["ingest", "missing.json", "--ingested-from", "Codex!"])

        self.assertEqual(2, code)
        self.assertEqual("", out)
        self.assertIn("invalid ingestion source", err)
