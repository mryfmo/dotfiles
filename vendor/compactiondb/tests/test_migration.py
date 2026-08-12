from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LegacyMigrationTests(unittest.TestCase):
    def test_legacy_database_import_is_idempotent_and_redacted(self) -> None:
        with tempfile.TemporaryDirectory(prefix="contextdb-migrate-") as temp:
            project = Path(temp) / "project"
            install = subprocess.run(
                [sys.executable, str(ROOT / "install.py"), "--project", str(project), "--skip-instructions"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, install.returncode, install.stderr)
            logs = project / ".claude" / "logs"
            logs.mkdir(parents=True)
            legacy = logs / "context_log.db"
            conn = sqlite3.connect(legacy)
            try:
                conn.executescript(
                    """
                    CREATE TABLE events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ts TEXT,
                        session_id TEXT,
                        event_type TEXT,
                        tool_name TEXT,
                        summary TEXT,
                        detail TEXT
                    );
                    """
                )
                conn.execute(
                    "INSERT INTO events(ts,session_id,event_type,tool_name,summary,detail) VALUES(?,?,?,?,?,?)",
                    ("2026-07-01 10:00:00", "legacy-s1", "user_prompt", None, "legacy prompt", "Use api_key=sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"),
                )
                conn.execute(
                    "INSERT INTO events(ts,session_id,event_type,tool_name,summary,detail) VALUES(?,?,?,?,?,?)",
                    (
                        "2026-07-01 10:01:00", "legacy-s1", "tool_use", "Write", "write", 
                        json.dumps({"tool_input": {"file_path": "src/a.py", "content": "print(1)"}, "tool_output": "ok"}),
                    ),
                )
                conn.commit()
            finally:
                conn.close()

            command = [sys.executable, str(ROOT / "migrate_legacy.py"), "--project", str(project)]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            self.assertTrue(legacy.exists())

            db = project / ".claude" / "contextdb" / "state" / "context.db"
            migrated = sqlite3.connect(db)
            migrated.row_factory = sqlite3.Row
            try:
                rows = migrated.execute("SELECT * FROM events ORDER BY id").fetchall()
            finally:
                migrated.close()
            self.assertEqual(2, len(rows))
            joined = "\n".join(str(row["detail_json"]) for row in rows)
            self.assertNotIn("sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456", joined)
            self.assertIn("[REDACTED", joined)
            self.assertIn("duplicates=2", second.stdout)
