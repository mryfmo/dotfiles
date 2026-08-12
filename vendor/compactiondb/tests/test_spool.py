from __future__ import annotations

import os
import unittest

from tests.support import TempProject
from contextdb.normalize import normalize_hook_payload
from contextdb.spool import WriterLock, drain_spool, spool_event


class SpoolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def _event(self, event_uuid: str) -> dict:
        return normalize_hook_payload(
            {
                "event_uuid": event_uuid,
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "cwd": str(self.p.root),
                "prompt": f"event {event_uuid}",
            },
            self.p.paths,
            self.p.config,
        )

    def test_writer_lock_leaves_durable_spool_for_later(self) -> None:
        spool_event(self.p.paths, self._event("lock-test"))
        lock = WriterLock(self.p.paths.lock_path)
        self.assertTrue(lock.acquire())
        try:
            result = drain_spool(self.p.paths, self.p.config, blocking_lock=False)
            self.assertFalse(result.acquired)
            self.assertEqual(1, result.remaining)
        finally:
            lock.release()
        result = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        self.assertEqual(1, result.inserted)
        self.assertEqual(0, result.remaining)

    def test_blocking_writer_lock_has_a_timeout(self) -> None:
        self.p.config["storage"]["writer_lock_timeout_ms"] = 50
        lock = WriterLock(self.p.paths.lock_path)
        self.assertTrue(lock.acquire())
        try:
            spool_event(self.p.paths, self._event("lock-timeout"))
            result = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
            self.assertFalse(result.acquired)
            self.assertIn("not acquired", result.error or "")
            self.assertEqual(1, result.remaining)
        finally:
            lock.release()

    def test_database_lock_does_not_drop_event(self) -> None:
        conn = self.p.store.connect()
        conn.execute("BEGIN IMMEDIATE")
        try:
            spool_event(self.p.paths, self._event("db-lock-test"))
            result = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
            self.assertIsNotNone(result.error)
            self.assertEqual(1, result.remaining)
        finally:
            conn.rollback()
            conn.close()
        result = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        self.assertEqual(1, result.inserted)
        self.assertEqual(0, result.remaining)

    def test_duplicate_event_uuid_is_idempotent(self) -> None:
        event = self._event("same-id")
        spool_event(self.p.paths, event)
        spool_event(self.p.paths, event)
        result = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        self.assertEqual(1, result.inserted)
        self.assertEqual(1, result.duplicates)
        self.assertEqual(1, self.p.count("events"))

    def test_invalid_spool_is_quarantined(self) -> None:
        bad = self.p.paths.incoming_dir / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        result = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        self.assertEqual(1, result.quarantined)
        self.assertFalse(bad.exists())
        self.assertTrue((self.p.paths.quarantine_dir / "bad.json").exists())

    @unittest.skipIf(os.name == "nt", "POSIX permission bits are not authoritative on Windows")
    def test_private_file_modes(self) -> None:
        event_path = spool_event(self.p.paths, self._event("mode-test"))
        self.assertEqual(0o600, event_path.stat().st_mode & 0o777)
        drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        self.assertEqual(0o600, self.p.paths.db_path.stat().st_mode & 0o777)
        self.assertEqual(0o700, self.p.paths.state_dir.stat().st_mode & 0o777)
