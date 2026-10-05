from __future__ import annotations

import unittest

from support import TempProject
from contextdb.normalize import normalize_hook_payload


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

    def test_explicit_memory_marker_supports_tag_and_inline_forms(self) -> None:
        prompts = (
            "[memory:decision] Project-wide API version is v2.",
            "Read README.md and tell me ... Also note [memory: e2e-test decision — this scratch project validates CompactionDB hooks] for the record.",
            "[memory:decision — Use SQLite for local state.] trailing prose is not memory",
        )
        for index, prompt in enumerate(prompts):
            self.p.event({"hook_event_name": "UserPromptSubmit", "session_id": f"s{index}", "prompt": prompt})
        conn = self.p.store.connect()
        try:
            rows = conn.execute("SELECT kind, content FROM memories ORDER BY id").fetchall()
            self.assertEqual("decision", rows[0]["kind"])
            self.assertEqual("Project-wide API version is v2.", rows[0]["content"])
            self.assertEqual("fact", rows[1]["kind"])
            self.assertEqual("e2e-test decision — this scratch project validates CompactionDB hooks", rows[1]["content"])
            self.assertEqual("decision", rows[2]["kind"])
            self.assertEqual("Use SQLite for local state.", rows[2]["content"])
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

    def _bulk_events(self, conn, count: int) -> None:
        with conn:
            for i in range(count):
                event = normalize_hook_payload(
                    {
                        "hook_event_name": "UserPromptSubmit",
                        "session_id": "bulk",
                        "cwd": str(self.p.root),
                        "prompt": f"event {i} " + "x" * 2000,
                    },
                    self.p.paths,
                    self.p.config,
                )
                self.p.store.insert_event(conn, event, ingested_from="test")

    def test_size_cap_deletes_the_oldest_events_until_the_pages_fit(self) -> None:
        conn = self.p.store.connect()
        try:
            self._bulk_events(conn, 200)
            used, _ = self.p.store._page_bytes(conn)
            first, last = conn.execute("SELECT MIN(id), MAX(id) FROM events").fetchone()
            with conn:
                removed = self.p.store.enforce_size_cap(conn, self.p.paths.project_id, used - 1)
            self.assertEqual(100, removed)  # one batch of the oldest events brings the pages under the cap
            self.assertLess(self.p.store._page_bytes(conn)[0], used)
            remaining = conn.execute("SELECT MIN(id), MAX(id) FROM events").fetchone()
            self.assertGreater(remaining[0], first)
            self.assertEqual(last, remaining[1])
            with conn:
                self.assertEqual(0, self.p.store.enforce_size_cap(conn, self.p.paths.project_id, used))
        finally:
            conn.close()

    def test_size_cap_under_fts_keeps_events_that_fit(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                for i in range(400):
                    event = normalize_hook_payload(
                        {
                            "hook_event_name": "UserPromptSubmit",
                            "session_id": "fts",
                            "cwd": str(self.p.root),
                            "prompt": " ".join(f"word{i}x{j}" for j in range(150)),
                        },
                        self.p.paths,
                        self.p.config,
                    )
                    self.p.store.insert_event(conn, event, ingested_from="test")
                if self.p.store.fts_tokenizer(conn) != "none":
                    conn.execute("INSERT INTO events_fts(events_fts) VALUES('optimize')")
            full, _ = self.p.store._page_bytes(conn)
            cap = full * 6 // 10
            with conn:
                removed = self.p.store.enforce_size_cap(conn, self.p.paths.project_id, cap)
            remaining = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
            self.assertGreater(remaining, 0)  # dead FTS pages no longer force deleting everything
            self.assertEqual(400, removed + remaining)
            self.assertLessEqual(self.p.store._page_bytes(conn)[0], cap)
        finally:
            conn.close()

    def test_size_cap_reclaims_orphaned_candidates_before_any_newer_event(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                for i in range(200):
                    event = normalize_hook_payload(
                        {
                            "hook_event_name": "Stop",
                            "session_id": "old",
                            "cwd": str(self.p.root),
                            "last_assistant_message": f"task {i} completed. " + "y" * 1500,
                        },
                        self.p.paths,
                        self.p.config,
                    )
                    self.p.store.insert_event(conn, event, ingested_from="test")
                conn.execute("UPDATE events SET ts_utc='2000-01-01T00:00:00.000Z'")
                self.p.store.prune_expired(conn, self.p.paths.project_id, days=0)
            self.assertEqual(0, int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]))
            self.assertEqual(200, int(conn.execute("SELECT COUNT(*) FROM memory_candidates").fetchone()[0]))
            self._bulk_events(conn, 10)
            with conn:
                self.p.store.optimize_fts(conn)  # measure as enforce_size_cap does
            used, _ = self.p.store._page_bytes(conn)
            with conn:
                removed = self.p.store.enforce_size_cap(conn, self.p.paths.project_id, used - 1)
            self.assertEqual(0, removed)
            self.assertEqual(10, int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]))
            self.assertEqual(0, int(conn.execute("SELECT COUNT(*) FROM memory_candidates").fetchone()[0]))
        finally:
            conn.close()

    def test_size_cap_reclaims_orphan_sessions_before_newer_events(self) -> None:
        for keep_events in (False, True):
            with self.subTest(keep_events=keep_events):
                conn = self.p.store.connect()
                try:
                    with conn:
                        conn.execute("DELETE FROM sessions")
                    if keep_events:
                        self._bulk_events(conn, 10)
                    with conn:
                        conn.executemany(
                            "INSERT INTO sessions(project_id, session_id, last_seen_at_utc, session_title) VALUES(?,?,?,?)",
                            [(self.p.paths.project_id, f"orphan-{i}", "test", "x" * 2000) for i in range(300)],
                        )
                        conn.execute("INSERT INTO sessions(project_id,session_id,last_seen_at_utc) VALUES('other-project','keep','now')")
                    used, _ = self.p.store._page_bytes(conn)
                    with conn:
                        removed = self.p.store.enforce_size_cap(conn, self.p.paths.project_id, used - 4096)
                    self.assertEqual(0, removed)
                    self.assertEqual(10 if keep_events else 0, conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])
                    self.assertEqual(0, conn.execute("SELECT COUNT(*) FROM sessions WHERE session_id LIKE 'orphan-%'").fetchone()[0])
                    self.assertEqual(1, conn.execute("SELECT COUNT(*) FROM sessions WHERE project_id='other-project'").fetchone()[0])
                    self.assertLess(self.p.store._page_bytes(conn)[0], used)
                    with conn:
                        conn.execute("DELETE FROM sessions WHERE project_id='other-project'")
                finally:
                    conn.close()

    def test_size_cap_reclaims_sessions_after_each_event_batch(self) -> None:
        conn = self.p.store.connect()
        try:
            self._bulk_events(conn, 110)
            with conn:
                self.p.store.enforce_size_cap(conn, self.p.paths.project_id, 1)
            self.assertEqual(0, conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0])
        finally:
            conn.close()

    def test_capping_every_event_returns_the_fts_pages(self) -> None:
        conn = self.p.store.connect()
        try:
            fresh, _ = self.p.store._page_bytes(conn)
            self._bulk_events(conn, 200)
            with conn:
                self.p.store.enforce_size_cap(conn, self.p.paths.project_id, 1)
            self.p.store.vacuum_if_fragmented(conn, threshold_bytes=0, force=True)
            self.assertLessEqual(self.p.store._page_bytes(conn)[0], fresh)
        finally:
            conn.close()

    def test_vacuum_runs_only_over_the_free_page_threshold_or_when_forced(self) -> None:
        conn = self.p.store.connect()
        try:
            self._bulk_events(conn, 200)
            with conn:
                self.p.store.prune_expired(conn, self.p.paths.project_id, days=-1)
            free = self.p.store._page_bytes(conn)[1]
            self.assertGreater(free, 0)
            self.assertFalse(self.p.store.vacuum_if_fragmented(conn, threshold_bytes=free))
            self.assertTrue(self.p.store.vacuum_if_fragmented(conn, threshold_bytes=free - 1))
            self.assertEqual(0, self.p.store._page_bytes(conn)[1])
            self.assertTrue(self.p.store.vacuum_if_fragmented(conn, threshold_bytes=free, force=True))
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
