#!/usr/bin/env python3
"""Exercise the trusted-runtime boundary of the Codex notify receiver."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECEIVER = ROOT / "home/dot_local/bin/common/executable_contextdb-codex-notify"


class ContextdbCodexNotifyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="contextdb-notify-test-")
        self.root = Path(self.temp.name)
        self.home = self.root / "home"
        self.project = self.root / "project"
        (self.project / ".claude/contextdb").mkdir(parents=True)
        self.capture = self.root / "capture.json"
        self.local_sentinel = self.root / "project-cli-ran"
        self.trusted_cli = (
            self.home
            / ".agents/compactiondb/.claude/hooks/contextdb_cli.py"
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_cli(self, path: Path, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!{sys.executable}\n{body}", encoding="utf-8")

    def run_receiver(self) -> subprocess.CompletedProcess[str]:
        payload = json.dumps({"cwd": str(self.project), "type": "agent-turn-complete"})
        return subprocess.run(
            ["bash", str(RECEIVER), payload],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={
                **os.environ,
                "HOME": str(self.home),
                "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
            },
            check=False,
        )

    def test_project_cli_is_data_only_and_trusted_cli_gets_explicit_root(self) -> None:
        self.write_cli(
            self.project / ".claude/hooks/contextdb_cli.py",
            f"from pathlib import Path\nPath({str(self.local_sentinel)!r}).write_text('ran')\n",
        )
        self.write_cli(
            self.trusted_cli,
            "import json, os, sys\n"
            f"open({str(self.capture)!r}, 'w').write(json.dumps({{"
            "'argv': sys.argv[1:], 'cwd': os.getcwd(), 'input': sys.stdin.read()}))\n",
        )

        result = self.run_receiver()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")
        self.assertFalse(self.local_sentinel.exists())
        capture = json.loads(self.capture.read_text(encoding="utf-8"))
        self.assertEqual(
            capture["argv"],
            [
                "--project-root",
                str(self.project.resolve()),
                "ingest",
                "--ingested-from",
                "codex",
            ],
        )
        self.assertEqual(Path(capture["cwd"]), self.project.resolve())
        self.assertEqual(json.loads(capture["input"])["cwd"], str(self.project))

    def test_missing_trusted_runtime_is_silent(self) -> None:
        result = self.run_receiver()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_non_opted_project_is_silent_even_with_trusted_runtime(self) -> None:
        (self.project / ".claude/contextdb").rmdir()
        self.write_cli(self.trusted_cli, "raise SystemExit(99)\n")

        result = self.run_receiver()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
