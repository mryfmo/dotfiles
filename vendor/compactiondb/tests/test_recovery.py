from __future__ import annotations

import unittest

from contextdb.recovery import build_recovery_context

from tests.support import TempProject


class RecoveryTests(unittest.TestCase):
    SECTIONS = (
        "Goal",
        "File modifications",
        "Recent activity",
        "Decisions",
        "Open tasks",
        "Failures",
        "Compact summary",
    )

    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def context(self, session_id: str = "s1") -> str:
        conn = self.p.store.connect()
        try:
            return build_recovery_context(self.p.store, conn, session_id=session_id)
        finally:
            conn.close()

    def section(self, context: str, title: str) -> str:
        index = self.SECTIONS.index(title)
        body = context.split(f"## {title}\n", 1)[1]
        for next_title in self.SECTIONS[index + 1 :]:
            marker = f"\n\n## {next_title}\n"
            if marker in body:
                return body.split(marker, 1)[0].strip()
        return body.strip()

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

    def test_raw_recovery_never_mixes_sessions(self) -> None:
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "S1_UNIQUE request"})
        self.file_event("Write", "src/s1.py")
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": "S2_SECRET_CONTEXT request"})
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": "We decided S2_MEMORY."})
        self.file_event("Write", "src/s2.py", session_id="s2")
        self.p.event(
            {
                "hook_event_name": "PostCompact",
                "session_id": "s1",
                "trigger": "auto",
                "compact_summary": "S1 compact summary",
            }
        )
        context = self.context()
        self.assertIn("S1_UNIQUE", context)
        self.assertIn("src/s1.py", context)
        self.assertIn("S1 compact summary", context)
        self.assertNotIn("S2_SECRET_CONTEXT", context)
        self.assertNotIn("S2_MEMORY", context)
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
        context = self.context()
        self.assertIn("Project-wide API version is v2", context)

    def test_file_modifications_deduplicate_count_and_order_by_recency(self) -> None:
        self.file_event("Write", "src/a.py")
        self.file_event("Edit", "src/b.py")
        self.file_event("Edit", "src/a.py")
        self.file_event("Read", "src/read_only.py")

        modified = self.section(self.context(), "File modifications")

        self.assertIn("src/a.py (edit, 2x)", modified)
        self.assertIn("src/b.py (edit, 1x)", modified)
        self.assertLess(modified.index("src/a.py"), modified.index("src/b.py"))
        self.assertNotIn("read_only.py", modified)

    def test_file_modifications_budget_drops_oldest_with_tail(self) -> None:
        self.p.config["recovery"]["files_budget_chars"] = 90
        self.p.store.config = self.p.config
        for name in ("one", "two", "three", "four"):
            self.file_event("Write", f"src/{name}.py")

        modified = self.section(self.context(), "File modifications")

        self.assertIn("src/four.py (write, 1x)", modified)
        self.assertNotIn("src/one.py", modified)
        self.assertIn("... and 3 more modified files (see contextdb files)", modified)
        self.assertLessEqual(len(modified), 90)

    def test_empty_session_has_every_section_heading_and_none_body(self) -> None:
        context = self.context()

        for title in self.SECTIONS:
            self.assertEqual("(none)", self.section(context, title), title)
        self.assertLessEqual(len(context), self.p.config["recovery"]["max_chars"])

    def test_compact_summary_coexists_after_authoritative_sections(self) -> None:
        self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": "[memory:decision] Adopt SQLite for local state.",
            }
        )
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "Second prompt"})
        self.file_event("Write", "src/app.py")
        self.p.event(
            {
                "hook_event_name": "PostCompact",
                "session_id": "s1",
                "trigger": "auto",
                "compact_summary": "Reference-only compact summary.",
            }
        )

        context = self.context()

        self.assertIn(
            "If the compact summary conflicts with the sections below, the ledger-derived sections are authoritative.",
            context,
        )
        section_positions = [context.index(f"## {title}") for title in self.SECTIONS]
        self.assertEqual(sorted(section_positions), section_positions)
        self.assertIn("- Latest decision: Adopt SQLite for local state.", self.section(context, "Goal"))
        activity = self.section(context, "Recent activity")
        self.assertLess(activity.index("Recent user instructions"), activity.index("Recent event flow"))
        self.assertLess(activity.index("Recent event flow"), activity.index("Files referenced or changed"))
        self.assertIn("Reference material", self.section(context, "Compact summary"))
        self.assertIn("Reference-only compact summary", self.section(context, "Compact summary"))

    def test_open_tasks_subtracts_completed_task_events(self) -> None:
        self.p.event(
            {
                "hook_event_name": "TaskCreated",
                "session_id": "s1",
                "task_id": "task-done",
                "task_subject": "Completed task",
            }
        )
        self.p.event(
            {
                "hook_event_name": "TaskCreated",
                "session_id": "s1",
                "task_id": "task-open",
                "task_subject": "Open task",
            }
        )
        self.p.event(
            {
                "hook_event_name": "TaskCompleted",
                "session_id": "s1",
                "task_id": "task-done",
                "task_subject": "Completed task",
            }
        )

        open_tasks = self.section(self.context(), "Open tasks")

        self.assertIn("Open task (task-open)", open_tasks)
        self.assertNotIn("Completed task", open_tasks)

    def test_recovery_respects_character_budget(self) -> None:
        self.p.config["recovery"]["max_chars"] = 1800
        self.p.config["recovery"]["files_budget_chars"] = 300
        self.p.store.config = self.p.config
        for i in range(30):
            self.p.event(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "s1",
                    "prompt": f"request {i} " + "x" * 300,
                }
            )
            self.file_event("Write", f"src/generated_{i}.py")
        self.p.event(
            {
                "hook_event_name": "PostCompact",
                "session_id": "s1",
                "trigger": "auto",
                "compact_summary": "summary " + "y" * 3000,
            }
        )

        context = self.context()

        self.assertLessEqual(len(context), 1800)
        self.assertIn("historical evidence", context)
        for title in self.SECTIONS:
            self.assertIn(f"## {title}", context)
