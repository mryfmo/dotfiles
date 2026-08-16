from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from contextdb.recover_hook import recovery_output
from contextdb.recovery import build_recovery_context
from contextdb.spool import drain_spool
from contextdb.util import one_line, sha256_text

from tests.support import TempProject


class RecoverHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()
        self.payload = {
            "hook_event_name": "SessionStart",
            "source": "compact",
            "session_id": "s1",
            "cwd": str(self.p.root),
        }
        self.p.event(
            {
                "hook_event_name": "PostCompact",
                "session_id": "s1",
                "trigger": "auto",
                "compact_summary": "summary",
            }
        )

    def tearDown(self) -> None:
        self.p.close()

    def packet(self, output: dict[str, object]) -> str:
        hook_output = output["hookSpecificOutput"]
        assert isinstance(hook_output, dict)
        packet = hook_output["additionalContext"]
        assert isinstance(packet, str)
        return packet

    def test_injected_packet_is_spooled_then_persisted_with_stored_detail_hash(self) -> None:
        before = self.p.count("events")

        output = recovery_output(self.payload, project_root=str(self.p.root))
        packet = self.packet(output)

        # The packet is assembled from already-redacted ledger data, then passes
        # through the normalizer again before its spool record touches disk.
        self.assertEqual(before, self.p.count("events"))
        self.assertEqual(1, len(list(self.p.paths.incoming_dir.glob("*.json"))))
        drain = drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        self.assertEqual(1, drain.inserted)
        conn = self.p.store.connect()
        try:
            rows = conn.execute(
                "SELECT * FROM events WHERE event_type='recovery_injected' ORDER BY id"
            ).fetchall()
            self.assertEqual(1, len(rows))
            row = rows[0]
            detail = json.loads(row["detail_json"])
            self.assertEqual(packet, detail["recovery_packet"])
            self.assertEqual(one_line(packet, 240), row["summary"])
            self.assertEqual(sha256_text(row["detail_json"]), row["detail_sha256"])
        finally:
            conn.close()

    def test_spool_failure_preserves_response_and_records_one_health_error(self) -> None:
        conn = self.p.store.connect()
        try:
            expected = build_recovery_context(self.p.store, conn, session_id="s1")
        finally:
            conn.close()

        with patch("contextdb.recover_hook.spool_event", side_effect=OSError("spool unavailable")):
            output = recovery_output(self.payload, project_root=str(self.p.root))

        self.assertEqual(expected, self.packet(output))
        errors = [
            json.loads(line)
            for line in self.p.paths.error_log_path.read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(1, len(errors))
        self.assertEqual("recover-hook-recording", errors[0]["stage"])
        self.assertIn("spool unavailable", errors[0]["message"])

    def test_response_envelope_is_unchanged(self) -> None:
        output = recovery_output(self.payload, project_root=str(self.p.root))

        self.assertEqual({"hookSpecificOutput"}, set(output))
        self.assertEqual(
            {"hookEventName", "additionalContext"},
            set(output["hookSpecificOutput"]),
        )
        self.assertEqual("SessionStart", output["hookSpecificOutput"]["hookEventName"])

    def test_second_packet_can_include_first_injection_without_self_recursion(self) -> None:
        first_packet = self.packet(recovery_output(self.payload, project_root=str(self.p.root)))
        second_packet = self.packet(recovery_output(self.payload, project_root=str(self.p.root)))

        self.assertNotIn("(recovery_injected)", first_packet)
        self.assertIn("(recovery_injected)", second_packet)
        conn = self.p.store.connect()
        try:
            self.assertEqual(
                1,
                conn.execute(
                    "SELECT COUNT(*) FROM events WHERE event_type='recovery_injected'"
                ).fetchone()[0],
            )
        finally:
            conn.close()
        drain_spool(self.p.paths, self.p.config, blocking_lock=True)
        conn = self.p.store.connect()
        try:
            self.assertEqual(
                2,
                conn.execute(
                    "SELECT COUNT(*) FROM events WHERE event_type='recovery_injected'"
                ).fetchone()[0],
            )
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
