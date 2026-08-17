#!/usr/bin/env python3
"""Exercise safe value storage in the agmsg send entrypoint."""

from __future__ import annotations

import os
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SEND = ROOT / "home/dot_agents/skills/agmsg/scripts/executable_send.sh"


class AgmsgSendTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="agmsg-send-test-")
        self.store = Path(self.temp.name)
        self.db = self.store / "messages.db"
        with sqlite3.connect(self.db) as conn:
            conn.executescript(
                """
                CREATE TABLE messages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  team TEXT NOT NULL,
                  from_agent TEXT NOT NULL,
                  to_agent TEXT NOT NULL,
                  body TEXT NOT NULL,
                  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  read_at TEXT
                );
                """
            )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_single_quotes_round_trip_without_sql_injection(self) -> None:
        values = (
            "team' OR 1=1 --",
            "from'agent",
            "to'agent",
            "body'); DROP TABLE messages; -- 'intact",
        )

        result = subprocess.run(
            [str(SEND), *values],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "AGMSG_STORAGE_PATH": str(self.store)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"Sent to {values[2]} in team {values[0]}\n")
        with sqlite3.connect(self.db) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone(), (1,))
            self.assertEqual(
                conn.execute(
                    "SELECT team, from_agent, to_agent, body FROM messages"
                ).fetchone(),
                values,
            )

    def test_touched_shell_entrypoints_have_shdoc_headers(self) -> None:
        for relative in (
            "executable_send.sh",
            "executable_whoami.sh",
            "executable_check-inbox.sh",
        ):
            text = (SEND.parent / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("# @file ", text)
                self.assertIn("# @brief ", text)


if __name__ == "__main__":
    unittest.main()
