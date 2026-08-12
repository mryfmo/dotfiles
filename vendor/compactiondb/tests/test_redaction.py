from __future__ import annotations

import json
import unittest

from tests.support import TempProject


class RedactionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    def test_secret_patterns_are_redacted_before_persistence(self) -> None:
        secret = "sk-ant-abcdefghijklmnopqrstuvwxyz012345"
        event = self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": f"password=hunter2 token={secret}",
            }
        )
        self.assertNotIn("hunter2", event["detail_json"])
        self.assertNotIn(secret, event["detail_json"])
        self.assertGreaterEqual(event["redaction_count"], 2)
        conn = self.p.store.connect()
        try:
            row = conn.execute("SELECT detail_json, sensitivity FROM events").fetchone()
            self.assertNotIn(secret, row["detail_json"])
            self.assertEqual("restricted", row["sensitivity"])
        finally:
            conn.close()

    def test_sensitive_file_content_is_omitted(self) -> None:
        secret = "github_pat_abcdefghijklmnopqrstuvwxyz0123456789"
        event = self.p.event(
            {
                "hook_event_name": "PostToolUse",
                "session_id": "s1",
                "tool_name": "Write",
                "tool_input": {"file_path": ".env", "content": f"TOKEN={secret}"},
                "tool_response": {"filePath": ".env", "success": True},
            }
        )
        self.assertNotIn(secret, event["detail_json"])
        self.assertIn("sensitive_path", event["detail_json"])
        self.assertEqual("restricted", event["sensitivity"])

    def test_large_detail_remains_valid_bounded_json(self) -> None:
        self.p.config["capture"]["max_detail_chars"] = 1200
        event = self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": "日本語の長い入力" * 1000,
            }
        )
        self.assertLessEqual(len(event["detail_json"]), 1200)
        parsed = json.loads(event["detail_json"])
        self.assertTrue(parsed.get("_truncated"))
        self.assertIn("prompt", parsed)

    def test_spool_contains_only_sanitized_event(self) -> None:
        secret = "AKIAABCDEFGHIJKLMNOP"
        event = self.p.event(
            {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "s1",
                "prompt": secret,
            },
            drain=False,
        )
        spool = next(self.p.paths.incoming_dir.glob("*.json"))
        text = spool.read_text(encoding="utf-8")
        self.assertNotIn(secret, text)
        self.assertIn("REDACTED", text)

    def test_additional_provider_and_env_secrets_are_redacted(self) -> None:
        secrets = (
            "AWS_SECRET_ACCESS_KEY=super-secret-value",
            "SERVICE_TOKEN=token-value",
            "sk_live_1234567890abcdefghijkl",
            "xoxb-1234567890-abcdefghijkl",
            "AIza" + "A" * 35,
        )
        event = self.p.event(
            {"hook_event_name": "UserPromptSubmit", "session_id": "s1", "prompt": " ".join(secrets)}
        )
        for secret in secrets:
            self.assertNotIn(secret, event["detail_json"])
        self.assertGreaterEqual(event["redaction_count"], len(secrets))

    def test_additional_sensitive_paths_omit_content(self) -> None:
        for path in (".netrc", ".npmrc", ".pypirc", ".docker/config.json", ".ssh/authorized_keys"):
            event = self.p.event(
                {
                    "hook_event_name": "PostToolUse",
                    "session_id": "s1",
                    "tool_name": "Write",
                    "tool_input": {"file_path": path, "content": "exotic-value"},
                }
            )
            self.assertNotIn("exotic-value", event["detail_json"])
            self.assertTrue(event["sensitivity"] == "restricted", path)
