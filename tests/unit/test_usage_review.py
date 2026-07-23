"""Tests for the usage snapshot and review report."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "scripts/usage-report.py"
SNAPSHOT_PATH = ROOT / "scripts/usage-snapshot.sh"


def load_report_module():
    spec = importlib.util.spec_from_file_location("usage_report", REPORT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load usage-report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(
    captured_at: str,
    models: list[dict[str, object]] | dict[str, dict[str, object]],
) -> dict[str, object]:
    return {
        "captured_at": captured_at,
        "weekly": {"weekly": [{"modelBreakdowns": models}]},
        "daily": {"daily": []},
    }


class UsageReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def write_snapshot(
        self,
        name: str,
        captured_at: str,
        models: list[dict[str, object]] | dict[str, dict[str, object]],
    ) -> Path:
        path = self.temp_dir / name
        path.write_text(json.dumps(snapshot(captured_at, models)))
        return path

    def test_snapshot_does_not_rewrite_existing_daily_file(self) -> None:
        repo = self.temp_dir / "repo"
        scripts = repo / "scripts"
        usage_dir = repo / ".agents/worklog/claude/usage"
        bin_dir = repo / "bin"
        scripts.mkdir(parents=True)
        usage_dir.mkdir(parents=True)
        bin_dir.mkdir()
        shutil.copy2(SNAPSHOT_PATH, scripts / SNAPSHOT_PATH.name)
        today = subprocess.run(
            ["date", "+%Y%m%d"], text=True, capture_output=True, check=True
        ).stdout.strip()
        existing = usage_dir / f"{today}.json"
        existing.write_text('{"keep":"unchanged"}\n')
        marker = repo / "ccusage-called"
        stub = bin_dir / "ccusage"
        stub.write_text(f"#!/usr/bin/env bash\ntouch {marker}\n")
        stub.chmod(0o755)
        env = {**os.environ, "PATH": f"{bin_dir}:/usr/bin:/bin"}

        result = subprocess.run(
            ["bash", str(scripts / SNAPSHOT_PATH.name)],
            text=True,
            capture_output=True,
            env=env,
        )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual('{"keep":"unchanged"}\n', existing.read_text())
        self.assertFalse(marker.exists())

    def test_report_computes_share_ratio_and_baseline_deltas(self) -> None:
        report = load_report_module()
        baseline = self.write_snapshot(
            "20260701.json",
            "2026-07-01T09:00:00+09:00",
            [
                {
                    "modelName": "claude-fable-5",
                    "inputTokens": 10,
                    "outputTokens": 20,
                    "cacheReadTokens": 50,
                },
                {
                    "modelName": "claude-opus-4-8",
                    "inputTokens": 10,
                    "outputTokens": 20,
                    "cacheReadTokens": 0,
                },
            ],
        )
        self.write_snapshot(
            "20260708.json",
            "2026-07-08T09:00:00+09:00",
            {
                "claude-fable-5": {
                    "inputTokens": 30,
                    "outputTokens": 70,
                    "cacheReadTokens": 100,
                },
                "claude-opus-4-8": {
                    "inputTokens": 10,
                    "outputTokens": 30,
                    "cacheReadTokens": 10,
                },
            },
        )

        lines = report.generate_report(
            self.temp_dir, baseline_path=baseline, today=date(2026, 7, 8)
        )
        text = "\n".join(lines)

        self.assertIn(
            "claude-fable: input=30 (+20), output=70 (+50), "
            "cache-read=100 (+50), output-share=70.0% (+20.0pp), "
            "cache-read-ratio=50.0% (-12.5pp)",
            text,
        )
        self.assertIn(
            "interactive-downgrade-candidate: yes "
            "(claude-fable non-cache=100, share=71.4%; "
            "largest=claude-fable 100)",
            text,
        )
        self.assertIn(
            "REVIEW DUE (+7d): review-2026-07-08.md is missing", text
        )
        self.assertIn("quality side (rework/review misses) is manual", text)

    def test_report_emits_due_windows_and_matching_notes_suppress_them(self) -> None:
        report = load_report_module()
        baseline = self.write_snapshot(
            "20260701.json",
            "2026-07-01T09:00:00+09:00",
            [
                {
                    "modelName": "claude-fable-5",
                    "inputTokens": 10,
                    "outputTokens": 10,
                    "cacheReadTokens": 0,
                }
            ],
        )
        self.write_snapshot(
            "20260715.json",
            "2026-07-15T09:00:00+09:00",
            [
                {
                    "modelName": "claude-fable-5",
                    "inputTokens": 20,
                    "outputTokens": 20,
                    "cacheReadTokens": 0,
                }
            ],
        )
        (self.temp_dir / "review-2026-07-08.md").write_text("# +7d review\n")

        lines = report.generate_report(
            self.temp_dir, baseline_path=baseline, today=date(2026, 7, 15)
        )
        text = "\n".join(lines)

        self.assertNotIn("REVIEW DUE (+7d)", text)
        self.assertIn(
            "REVIEW DUE (+14d): review-2026-07-15.md is missing", text
        )

    def test_candidate_is_no_when_another_claude_family_is_larger(self) -> None:
        report = load_report_module()
        baseline = self.write_snapshot(
            "20260701.json",
            "2026-07-01T09:00:00+09:00",
            [
                {
                    "modelName": "claude-fable-5",
                    "inputTokens": 10,
                    "outputTokens": 10,
                    "cacheReadTokens": 0,
                }
            ],
        )
        self.write_snapshot(
            "20260702.json",
            "2026-07-02T09:00:00+09:00",
            [
                {
                    "modelName": "claude-fable-5",
                    "inputTokens": 10,
                    "outputTokens": 10,
                    "cacheReadTokens": 0,
                },
                {
                    "modelName": "claude-sonnet-5",
                    "inputTokens": 50,
                    "outputTokens": 50,
                    "cacheReadTokens": 0,
                },
            ],
        )

        lines = report.generate_report(
            self.temp_dir, baseline_path=baseline, today=date(2026, 7, 2)
        )

        self.assertIn(
            "interactive-downgrade-candidate: no "
            "(claude-fable non-cache=20, share=16.7%; "
            "largest=claude-sonnet 100)",
            lines,
        )

    def test_malformed_latest_snapshot_warns_and_never_raises(self) -> None:
        report = load_report_module()
        baseline = self.write_snapshot(
            "20260701.json",
            "2026-07-01T09:00:00+09:00",
            [
                {
                    "modelName": "claude-fable-5",
                    "inputTokens": 10,
                    "outputTokens": 10,
                    "cacheReadTokens": 0,
                }
            ],
        )
        (self.temp_dir / "20260702.json").write_text("{not-json")

        lines = report.generate_report(
            self.temp_dir, baseline_path=baseline, today=date(2026, 7, 2)
        )

        self.assertTrue(any(line.startswith("WARN:") for line in lines))
        self.assertIn(
            "quality side (rework/review misses) is manual — "
            "decide via PR, never automatically",
            lines,
        )


if __name__ == "__main__":
    unittest.main()
