from __future__ import annotations

import unittest

from contextdb.normalize import normalize_hook_payload
from tests.support import TempProject


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def test_session_scoped_event_queries(self) -> None:
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "alpha only"})
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": "beta only"})
        conn = self.p.store.connect()
        try:
            s1 = self.p.store.recent_events(conn, self.p.paths.project_id, "s1", 10)
            self.assertEqual(1, len(s1))
            self.assertIn("alpha", s1[0]["detail_json"])
            self.assertNotIn("beta", s1[0]["detail_json"])
        finally:
            conn.close()

    def test_fts_search_supports_japanese_substrings(self) -> None:
        self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": "認証方式はOAuth2へ統一する方針です。",
            }
        )
        conn = self.p.store.connect()
        try:
            for query in ("認証方式", "OAuth2"):
                rows = self.p.store.search_events(
                    conn,
                    self.p.paths.project_id,
                    query,
                    session_id="s1",
                    limit=10,
                )
                self.assertEqual(1, len(rows), query)
        finally:
            conn.close()

    def test_unspecified_session_returns_project_memories_only(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                self.p.store.add_memory(
                    conn, project_id=self.p.paths.project_id, session_id="", scope="project",
                    kind="decision", content="project-visible",
                )
                self.p.store.add_memory(
                    conn, project_id=self.p.paths.project_id, session_id="s1", scope="session",
                    kind="open_task", content="session-one-only",
                )
                self.p.store.add_memory(
                    conn, project_id=self.p.paths.project_id, session_id="s2", scope="session",
                    kind="open_task", content="session-two-only",
                )
            default_rows = self.p.store.current_memories(conn, self.p.paths.project_id)
            session_rows = self.p.store.current_memories(conn, self.p.paths.project_id, session_id="s1")
            self.assertEqual(["project-visible"], [row["content"] for row in default_rows])
            self.assertEqual({"project-visible", "session-one-only"}, {row["content"] for row in session_rows})
        finally:
            conn.close()

    def test_heuristic_memory_stays_session_scoped(self) -> None:
        self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": "このセッションでは必ずローカルDBを使うこと。",
            }
        )
        conn = self.p.store.connect()
        try:
            project_only = self.p.store.current_memories(conn, self.p.paths.project_id)
            s1 = self.p.store.current_memories(conn, self.p.paths.project_id, session_id="s1")
            s2 = self.p.store.current_memories(conn, self.p.paths.project_id, session_id="s2")
            self.assertEqual([], project_only)
            self.assertTrue(any(row["kind"] == "constraint" for row in s1))
            self.assertFalse(any(row["kind"] == "constraint" for row in s2))
        finally:
            conn.close()


    def test_identical_session_memories_are_deduplicated_only_within_session(self) -> None:
        prompt = "このセッションでは必ずローカルDBを使うこと。"
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": prompt})
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": prompt})
        self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": prompt})
        conn = self.p.store.connect()
        try:
            rows = conn.execute(
                "SELECT session_id, scope, content FROM memories WHERE kind='constraint' ORDER BY id"
            ).fetchall()
            self.assertEqual(2, len(rows))
            self.assertEqual({"s1", "s2"}, {row["session_id"] for row in rows})
            self.assertTrue(all(row["scope"] == "session" for row in rows))
            self.assertEqual(1, len(self.p.store.current_memories(conn, self.p.paths.project_id, session_id="s1")))
            self.assertEqual(1, len(self.p.store.current_memories(conn, self.p.paths.project_id, session_id="s2")))
        finally:
            conn.close()

    def test_postcompact_summary_becomes_durable_memory(self) -> None:
        self.p.event(
            {
                "hook_event_name": "PostCompact",
                "session_id": "s1",
                "trigger": "auto",
                "compact_summary": "Implemented auth flow; remaining task is integration testing.",
            }
        )
        conn = self.p.store.connect()
        try:
            memories = self.p.store.current_memories(
                conn,
                self.p.paths.project_id,
                session_id="s1",
            )
            self.assertEqual(1, len(memories))
            self.assertEqual("compact_summary", memories[0]["kind"])
        finally:
            conn.close()

    def test_superseding_memory_is_append_only_projection(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                first = self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id="",
                    scope="project",
                    kind="decision",
                    content="Use SQLite.",
                )
                second = self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id="",
                    scope="project",
                    kind="decision",
                    content="Use PostgreSQL.",
                    supersedes_memory_uuid=first,
                )
                self.p.store.rebuild_memory_blocks(conn, self.p.paths.project_id)
            current = self.p.store.current_memories(conn, self.p.paths.project_id)
            self.assertEqual([second], [row["memory_uuid"] for row in current])
            self.assertEqual(2, int(conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]))
        finally:
            conn.close()

    def test_hierarchical_blocks_and_session_isolation(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                for i in range(20):
                    self.p.store.add_memory(
                        conn,
                        project_id=self.p.paths.project_id,
                        session_id="",
                        scope="project",
                        kind="fact",
                        content=f"project fact {i}",
                    )
                self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id="s1",
                    scope="session",
                    kind="open_task",
                    content="s1 only task",
                )
                self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id="s2",
                    scope="session",
                    kind="open_task",
                    content="s2 only task",
                )
                block_count = self.p.store.rebuild_memory_blocks(conn, self.p.paths.project_id)
            self.assertGreater(block_count, 20)
            lines = self.p.store.hierarchical_memory_context(conn, self.p.paths.project_id, session_id="s1")
            text = "\n".join(lines)
            self.assertIn("s1 only task", text)
            self.assertNotIn("s2 only task", text)
            self.assertTrue(any(line.startswith("M1-") for line in lines))
        finally:
            conn.close()


    def test_prune_batches_more_than_sqlite_variable_limit(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                for i in range(1005):
                    event = normalize_hook_payload(
                        {
                            "hook_event_name": "UserPromptSubmit",
                            "session_id": "bulk",
                            "cwd": str(self.p.root),
                            "prompt": f"ordinary event {i}",
                        },
                        self.p.paths,
                        self.p.config,
                    )
                    self.p.store.insert_event(conn, event, ingested_from="test")
                conn.execute(
                    "UPDATE events SET ts_utc='2000-01-01T00:00:00.000Z' WHERE project_id=?",
                    (self.p.paths.project_id,),
                )
                removed = self.p.store.prune_expired(conn, self.p.paths.project_id, days=0)
            self.assertEqual(1005, removed)
            self.assertEqual(0, int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]))
            if self.p.store.fts_tokenizer(conn) != "none":
                self.assertEqual(0, int(conn.execute("SELECT COUNT(*) FROM events_fts").fetchone()[0]))
        finally:
            conn.close()

    def test_prune_removes_raw_event_but_keeps_memory(self) -> None:
        self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": "[memory:decision] Keep the durable decision.",
            }
        )
        conn = self.p.store.connect()
        try:
            with conn:
                removed = self.p.store.prune_expired(conn, self.p.paths.project_id, days=0)
            self.assertEqual(1, removed)
            self.assertEqual(0, int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]))
            self.assertEqual(1, len(self.p.store.current_memories(conn, self.p.paths.project_id)))
        finally:
            conn.close()
