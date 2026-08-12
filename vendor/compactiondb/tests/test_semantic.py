from __future__ import annotations

import sys
import unittest

from tests.support import TempProject


class SemanticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()
        self.embedder = self.p.root / "fake_embedder.py"
        self.embedder.write_text(
            """
import json, sys
payload = json.load(sys.stdin)
out = []
for text in payload['texts']:
    value = text.casefold()
    out.append([
        float(sum(word in value for word in ('auth', 'login', 'oauth', '認証'))),
        float(sum(word in value for word in ('database', 'sqlite', 'backup', 'db'))),
        min(len(value), 1000) / 1000.0,
    ])
json.dump({'model': 'fake-semantic-v1', 'embeddings': out}, sys.stdout)
""".strip()
            + "\n",
            encoding="utf-8",
        )
        self.p.config["semantic"] = {
            "enabled": True,
            "command": [sys.executable, str(self.embedder)],
            "model": "fake-semantic-v1",
            "timeout_seconds": 10,
            "batch_size": 8,
        }
        self.p.store.config = self.p.config

    def tearDown(self) -> None:
        self.p.close()

    def test_embedding_model_mismatch_is_rejected(self) -> None:
        helper = self.p.root / "mismatch_embed.py"
        helper.write_text(
            "import json,sys\n"
            "x=json.load(sys.stdin)\n"
            "print(json.dumps({'model':'unexpected','embeddings':[[1.0] for _ in x['texts']]}))\n",
            encoding="utf-8",
        )
        self.p.config["semantic"] = {
            "enabled": True, "command": [sys.executable, str(helper)],
            "model": "configured", "timeout_seconds": 5, "batch_size": 8,
        }
        self.p.store.config = self.p.config
        conn = self.p.store.connect()
        try:
            with conn:
                self.p.store.add_memory(
                    conn, project_id=self.p.paths.project_id, session_id="",
                    scope="project", kind="fact", content="one",
                )
            with self.assertRaisesRegex(ValueError, "does not match"):
                self.p.store.index_memory_embeddings(conn, self.p.paths.project_id)
        finally:
            conn.close()

    def test_external_semantic_embedding_adapter(self) -> None:
        conn = self.p.store.connect()
        try:
            with conn:
                auth = self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id="",
                    scope="project",
                    kind="decision",
                    content="Use OAuth authentication for login.",
                )
                database = self.p.store.add_memory(
                    conn,
                    project_id=self.p.paths.project_id,
                    session_id="",
                    scope="project",
                    kind="procedure",
                    content="Back up the SQLite database every day.",
                )
                result = self.p.store.index_memory_embeddings(conn, self.p.paths.project_id)
            self.assertEqual(2, result["indexed"])
            matches = self.p.store.semantic_search_memories(
                conn,
                self.p.paths.project_id,
                "認証 login",
                limit=2,
            )
            self.assertEqual(auth, matches[0]["memory"]["memory_uuid"])
            self.assertEqual(database, matches[1]["memory"]["memory_uuid"])
            self.assertGreater(matches[0]["score"], matches[1]["score"])
        finally:
            conn.close()
