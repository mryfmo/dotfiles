#!/usr/bin/env python3
"""Exercise deterministic evidence extraction from Pi session JSONL."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_pi-session-evidence"
FIXTURES = ROOT / "tests/unit/fixtures/pi_sessions"
MAX_FILE_BYTES = 50 * 1024 * 1024


class PiSessionEvidenceTest(unittest.TestCase):
    def run_script(self, fixture: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / fixture), *args],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )

    def json_result(self, fixture: str) -> tuple[dict, subprocess.CompletedProcess[str]]:
        result = self.run_script(fixture, "--json")
        return json.loads(result.stdout), result

    def test_linear_session_aggregates_active_assistant_usage(self) -> None:
        evidence, result = self.json_result("linear.jsonl")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertEqual(evidence["activeLeafId"], "t1")
        self.assertEqual(
            evidence["branch"],
            {"totalEntries": 3, "activePathEntries": 3, "leafCount": 1},
        )
        self.assertEqual(evidence["entryCounts"], {"message": 3})
        self.assertEqual(
            evidence["usage"]["tokens"],
            {"input": 10, "output": 4, "cacheRead": 2, "cacheWrite": 1},
        )
        self.assertEqual(evidence["usage"]["cost"]["total"], 0.033)

    def test_last_appended_branch_is_active_and_inactive_usage_is_excluded(self) -> None:
        evidence, _ = self.json_result("branched.jsonl")

        self.assertEqual(evidence["activeLeafId"], "right-leaf")
        self.assertEqual(
            evidence["branch"],
            {"totalEntries": 6, "activePathEntries": 4, "leafCount": 2},
        )
        self.assertEqual(
            evidence["usage"]["tokens"],
            {"input": 13, "output": 3, "cacheRead": 1, "cacheWrite": 4},
        )
        self.assertEqual(evidence["usage"]["cost"]["total"], 3)

    def test_compaction_and_model_changes_keep_order_and_bounds(self) -> None:
        evidence, _ = self.json_result("compaction-model.jsonl")

        self.assertEqual(
            evidence["modelChanges"],
            [
                {"id": "m1", "provider": "openai", "modelId": "gpt-5.6"},
                {
                    "id": "m2",
                    "provider": "anthropic",
                    "modelId": "claude-sonnet-test",
                },
            ],
        )
        compaction = evidence["compactions"][0]
        self.assertEqual(len(compaction["summary"]), 120)
        self.assertEqual(compaction["tokensBefore"], 50000)
        self.assertEqual(compaction["readFiles"], ["src/read.py", "README.md"])
        self.assertEqual(compaction["modifiedFiles"], ["src/write.py"])
        self.assertEqual(
            evidence["usage"]["tokens"],
            {"input": 18, "output": 11, "cacheRead": 8, "cacheWrite": 6},
        )
        self.assertAlmostEqual(evidence["usage"]["cost"]["total"], 0.43)

    def test_malformed_lines_are_counted_warned_and_nonfatal(self) -> None:
        evidence, result = self.json_result("malformed.jsonl")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "warning: skipped 3 malformed line(s)\n")
        self.assertEqual(evidence["malformedLines"], 3)
        self.assertEqual(evidence["activeLeafId"], "leaf")
        self.assertEqual(evidence["branch"]["totalEntries"], 2)

    def test_human_output_contains_acceptance_summary(self) -> None:
        result = self.run_script("compaction-model.jsonl")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Entries: total=6 active=6 leaves=1 malformed=0", result.stdout)
        self.assertIn("Models: openai/gpt-5.6 -> anthropic/claude-sonnet-test", result.stdout)
        self.assertIn("tokensBefore=50000", result.stdout)
        self.assertIn("readFiles=src/read.py,README.md", result.stdout)
        self.assertIn("modifiedFiles=src/write.py", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_session_file_is_not_modified(self) -> None:
        fixture = FIXTURES / "linear.jsonl"
        before = fixture.stat()

        result = self.run_script("linear.jsonl", "--json")
        after = fixture.stat()

        self.assertEqual(result.returncode, 0)
        self.assertEqual((after.st_size, after.st_mtime_ns), (before.st_size, before.st_mtime_ns))

    def test_file_over_50_mib_is_refused_before_json_parsing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pi-session-evidence-") as temp_dir:
            oversized = Path(temp_dir) / "oversized.jsonl"
            with oversized.open("wb") as stream:
                stream.write(b'{"type":"session"}\n')
                stream.truncate(MAX_FILE_BYTES + 1)

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(oversized), "--json"],
                text=True,
                capture_output=True,
                timeout=5,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("session file exceeds 50 MiB limit", result.stderr)

    def test_missing_file_has_clear_error(self) -> None:
        result = self.run_script("missing.jsonl", "--json")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("unable to read session file", result.stderr)


if __name__ == "__main__":
    unittest.main()
