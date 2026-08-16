from __future__ import annotations

import hashlib
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout

from contextdb.cli import main
from contextdb.probe import generate_probes
from contextdb.recovery import build_recovery_context

from tests.support import TempProject


class ProbeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def add_memory(self, kind: str, content: str, *, scope: str = "session", session_id: str = "s1") -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id=session_id,
                    scope=scope,
                    kind=kind,
                    content=content,
                )
        finally:
            conn.close()

    def file_event(self, tool_name: str, path: str, *, session_id: str = "s1") -> None:
        self.p.event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": session_id,
                "tool_name": tool_name,
                "tool_input": {"file_path": path},
                "tool_response": {"success": True},
            }
        )

    def probes(self, session_id: str = "s1") -> list[dict[str, str]]:
        conn = self.p.store.connect(initialize=False)
        try:
            return generate_probes(self.p.store, conn, session_id=session_id)
        finally:
            conn.close()

    def populated(self) -> None:
        self.p.event(
            {
                "hook_event_name": "PostToolUseFailure",
                "session_id": "s1",
                "tool_name": "Bash",
                "tool_input": {"command": "make"},
                "error": "compile failed",
            }
        )
        self.file_event("Write", "src/a.py")
        self.file_event("Edit", "src/b.py")
        self.file_event("Edit", "src/a.py")
        self.add_memory("decision", "Use SQLite for local state.")
        self.add_memory("decision", "Keep the ledger append-only.", scope="project")
        self.add_memory("open_task", "Add the recovery smoke test.")
        self.p.event(
            {
                "hook_event_name": "TaskCreated",
                "session_id": "s1",
                "task_id": "task-open",
                "task_subject": "Document the probe CLI",
            }
        )

    def test_populated_session_generates_all_probe_types(self) -> None:
        self.populated()

        probes = {probe["type"]: probe for probe in self.probes()}

        self.assertEqual({"recall", "artifact", "decision", "continuation"}, set(probes))
        self.assertIn("compile failed", probes["recall"]["ground_truth"])
        self.assertEqual("src/a.py (edit, 2x)\nsrc/b.py (edit, 1x)", probes["artifact"]["ground_truth"])
        self.assertIn("[session/decision] Use SQLite for local state.", probes["decision"]["ground_truth"])
        self.assertIn("[project/decision] Keep the ledger append-only.", probes["decision"]["ground_truth"])
        self.assertIn("[session/open_task] Add the recovery smoke test.", probes["continuation"]["ground_truth"])
        self.assertIn("Document the probe CLI (task-open)", probes["continuation"]["ground_truth"])

    def test_empty_session_skips_every_probe_type(self) -> None:
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "other", "prompt": "unrelated"})

        self.assertEqual([], self.probes())

    def test_schema_and_cli_json_are_pinned(self) -> None:
        self.populated()
        out, err = io.StringIO(), io.StringIO()

        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--project-root", str(self.p.root), "probe", "--session", "s1", "--json"])

        self.assertEqual(0, code, err.getvalue())
        payload = json.loads(out.getvalue())
        self.assertEqual({"probes"}, set(payload))
        self.assertIsInstance(payload["probes"], list)
        for probe in payload["probes"]:
            self.assertEqual({"type", "question", "ground_truth"}, set(probe))
            self.assertIsInstance(probe["type"], str)
            self.assertIsInstance(probe["question"], str)
            self.assertIsInstance(probe["ground_truth"], str)
            self.assertTrue(probe["ground_truth"].strip())

    def test_other_session_data_never_enters_ground_truth(self) -> None:
        self.populated()
        self.p.event(
            {
                "hook_event_name": "PostToolUseFailure",
                "session_id": "other",
                "tool_name": "Bash",
                "error": "OTHER_FAILURE",
            }
        )
        self.file_event("Write", "OTHER_FILE", session_id="other")
        self.add_memory("decision", "OTHER_DECISION", session_id="other")
        self.add_memory("open_task", "OTHER_TASK", session_id="other")
        self.p.event(
            {
                "hook_event_name": "TaskCreated",
                "session_id": "other",
                "task_id": "other-task",
                "task_subject": "OTHER_EVENT_TASK",
            }
        )

        serialized = json.dumps(self.probes(), ensure_ascii=False)

        self.assertNotIn("OTHER_", serialized)

    def test_recall_prefers_first_post_tool_failure_then_falls_back(self) -> None:
        self.p.event({"hook_event_name": "StopFailure", "session_id": "s1", "error": "EARLY_GENERAL"})
        self.p.event(
            {
                "hook_event_name": "PostToolUseFailure",
                "session_id": "s1",
                "tool_name": "Bash",
                "error": "FIRST_TOOL_FAILURE",
            }
        )
        self.p.event(
            {
                "hook_event_name": "PostToolUseFailure",
                "session_id": "s1",
                "tool_name": "Bash",
                "error": "SECOND_TOOL_FAILURE",
            }
        )

        recall = self.probes()[0]["ground_truth"]

        self.assertIn("FIRST_TOOL_FAILURE", recall)
        self.assertNotIn("EARLY_GENERAL", recall)
        self.assertNotIn("SECOND_TOOL_FAILURE", recall)

        other = TempProject()
        try:
            other.event({"hook_event_name": "StopFailure", "session_id": "fallback", "error": "GENERAL_ONLY"})
            conn = other.store.connect(initialize=False)
            try:
                fallback = generate_probes(other.store, conn, session_id="fallback")[0]["ground_truth"]
            finally:
                conn.close()
            self.assertIn("GENERAL_ONLY", fallback)
        finally:
            other.close()

    def test_artifact_ground_truth_matches_recovery_section(self) -> None:
        self.file_event("Write", "src/a.py")
        self.file_event("Edit", "src/b.py")
        self.file_event("Edit", "src/a.py")
        conn = self.p.store.connect(initialize=False)
        try:
            artifact = generate_probes(self.p.store, conn, session_id="s1")[0]["ground_truth"]
            context = build_recovery_context(self.p.store, conn, session_id="s1")
        finally:
            conn.close()
        section = context.split("## File modifications\n", 1)[1].split("\n\n## Recent activity\n", 1)[0]

        self.assertEqual(section, artifact)

    def test_probe_cli_does_not_change_database_content(self) -> None:
        self.populated()
        before = hashlib.sha256(self.p.paths.db_path.read_bytes()).hexdigest()
        out, err = io.StringIO(), io.StringIO()

        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--project-root", str(self.p.root), "probe", "--session", "s1", "--json"])

        after = hashlib.sha256(self.p.paths.db_path.read_bytes()).hexdigest()
        self.assertEqual(0, code, err.getvalue())
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
