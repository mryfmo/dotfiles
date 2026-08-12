from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout

from tests.support import TempProject
from contextdb.cli import main


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
