from __future__ import annotations

import hashlib
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

from contextdb.cli import main
from contextdb.config import load_config
from contextdb.recall import normalize_scores, recall

from tests.support import TempProject


class RecallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def add_memory(self, content: str, *, scope: str = "project", session_id: str = "") -> str:
        conn = self.p.store.connect()
        try:
            with conn:
                memory_uuid = self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id=session_id,
                    scope=scope,
                    kind="decision",
                    content=content,
                )
        finally:
            conn.close()
        assert memory_uuid is not None
        return memory_uuid

    def results(
        self,
        query: str,
        *,
        session_id: str | None = None,
        k: int = 5,
        rho: float = 0.6,
    ) -> list[dict[str, object]]:
        conn = self.p.store.connect(initialize=False)
        try:
            return recall(self.p.store, conn, query, session_id=session_id, k=k, rho=rho)
        finally:
            conn.close()

    def invoke(self, args: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--project-root", str(self.p.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_lexical_only_ranking_is_deterministic(self) -> None:
        self.add_memory("rareterm rareterm rareterm primary")
        self.add_memory("rareterm secondary")

        first = self.results("rareterm")
        second = self.results("rareterm")

        self.assertEqual(first, second)
        memories = [row for row in first if row["record_type"] == "memory"]
        self.assertEqual(
            ["rareterm rareterm rareterm primary", "rareterm secondary"],
            [row["summary"] for row in memories],
        )
        self.assertEqual(["lexical", "lexical"], [row["via"] for row in memories])
        self.assertGreater(float(memories[0]["score"]), float(memories[1]["score"]))

    def test_semantic_fusion_uses_existing_embedding_pathway(self) -> None:
        embedder = self.p.root / "fake_embedder.py"
        embedder.write_text(
            "import json,sys\n"
            "data=json.load(sys.stdin)\n"
            "vectors=[]\n"
            "for text in data['texts']:\n"
            "    value=text.casefold()\n"
            "    vectors.append([1.0,0.0] if value == 'needle' or 'semantic target' in value else [0.0,1.0])\n"
            "json.dump({'model':'fake-recall-v1','embeddings':vectors},sys.stdout)\n",
            encoding="utf-8",
        )
        self.p.config["semantic"] = {
            "enabled": True,
            "command": [sys.executable, str(embedder)],
            "model": "fake-recall-v1",
            "timeout_seconds": 10,
            "batch_size": 8,
        }
        self.p.store.config = self.p.config
        lexical_uuid = self.add_memory("needle lexical memory")
        semantic_uuid = self.add_memory("semantic target memory")
        conn = self.p.store.connect()
        try:
            with conn:
                indexed = self.p.store.index_memory_embeddings(conn, self.p.paths.project_id)
        finally:
            conn.close()
        self.assertEqual(2, indexed["indexed"])

        results = self.results("needle", k=2, rho=0.4)

        self.assertEqual([semantic_uuid, lexical_uuid], [row["memory_uuid"] for row in results])
        self.assertAlmostEqual(0.6, float(results[0]["score"]))
        self.assertAlmostEqual(0.4, float(results[1]["score"]))
        self.assertEqual(["semantic", "fused"], [row["via"] for row in results])

    def test_min_max_degenerate_scores_normalize_to_one(self) -> None:
        self.assertEqual({"only": 1.0}, normalize_scores({"only": 4.2}))
        self.assertEqual(
            {"first": 1.0, "second": 1.0},
            normalize_scores({"first": -3.0, "second": -3.0}),
        )
        self.assertEqual({}, normalize_scores({}))

    def test_event_closure_uses_three_paths_deduplicates_and_inherits_score(self) -> None:
        self.p.event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "s1",
                "tool_name": "Bash",
                "tool_use_id": "shared-tool",
                "tool_input": {"command": "uniquequery", "file_path": "src/shared.py"},
                "tool_response": {"success": True},
            }
        )
        self.p.event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "s1",
                "tool_name": "Read",
                "tool_input": {"file_path": "src/shared.py"},
                "tool_response": {"success": True},
            }
        )
        self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": "filler",
            }
        )
        self.p.event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "s1",
                "tool_name": "Bash",
                "tool_use_id": "shared-tool",
                "tool_input": {"command": "tool sibling"},
                "tool_response": {"success": True},
            }
        )
        self.p.event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "s1",
                "tool_name": "Write",
                "tool_input": {"file_path": "src/shared.py"},
                "tool_response": {"success": True},
            }
        )

        results = self.results("uniquequery", session_id="s1", k=10)

        self.assertEqual("lexical", results[0]["via"])
        self.assertEqual(1.0, results[0]["score"])
        closure = results[1:]
        self.assertEqual(
            ["closure:tool_use_id", "closure:adjacent", "closure:shared_file"],
            [row["via"] for row in closure],
        )
        self.assertEqual([0.5, 0.5, 0.5], [row["score"] for row in closure])
        self.assertEqual(len(closure), len({row["event_uuid"] for row in closure}))

    def test_session_filter_keeps_project_memory_and_excludes_other_session(self) -> None:
        self.p.event(
            {"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "isokey current event"}
        )
        self.p.event(
            {"hook_event_name": "UserPromptSubmit", "session_id": "s2", "prompt": "isokey OTHER_EVENT"}
        )
        self.add_memory("isokey SESSION_ONE", scope="session", session_id="s1")
        self.add_memory("isokey OTHER_MEMORY", scope="session", session_id="s2")
        self.add_memory("isokey PROJECT_VISIBLE")

        serialized = json.dumps(self.results("isokey", session_id="s1", k=10), ensure_ascii=False)

        self.assertIn("current event", serialized)
        self.assertIn("SESSION_ONE", serialized)
        self.assertIn("PROJECT_VISIBLE", serialized)
        self.assertNotIn("OTHER_", serialized)

    def test_recall_cli_does_not_change_database_content(self) -> None:
        self.p.event(
            {"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": "readonlykey event"}
        )
        before = hashlib.sha256(self.p.paths.db_path.read_bytes()).hexdigest()

        code, out, err = self.invoke(["recall", "readonlykey", "--session", "s1", "--json"])

        after = hashlib.sha256(self.p.paths.db_path.read_bytes()).hexdigest()
        self.assertEqual(0, code, err)
        self.assertTrue(json.loads(out))
        self.assertEqual(before, after)

    def test_recall_config_validation_and_cli_k_override(self) -> None:
        self.p.paths.config_path.write_text(
            json.dumps({"version": 1, "recall": {"rho": 0.25, "k": 1}}),
            encoding="utf-8",
        )
        config = load_config(self.p.paths)
        self.assertEqual({"rho": 0.25, "k": 1}, config["recall"])
        for suffix in ("one", "two", "three"):
            self.p.event(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "s1",
                    "prompt": f"overridekey {suffix}",
                }
            )

        code, out, err = self.invoke(
            ["recall", "overridekey", "--session", "s1", "--k", "2", "--json"]
        )

        self.assertEqual(0, code, err)
        self.assertEqual(2, len(json.loads(out)))
        with self.subTest("rho above one"):
            self.p.paths.config_path.write_text(
                json.dumps({"version": 1, "recall": {"rho": 1.1}}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, r"recall\.rho must be <= 1\.0"):
                load_config(self.p.paths)
        with self.subTest("negative k"):
            self.p.paths.config_path.write_text(
                json.dumps({"version": 1, "recall": {"k": -1}}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, r"recall\.k must be an integer >= 0"):
                load_config(self.p.paths)


if __name__ == "__main__":
    unittest.main()
