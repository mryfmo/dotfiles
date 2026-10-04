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
        self.trusted_cli = self.home / ".agents/compactiondb/.claude/hooks/contextdb_cli.py"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_cli(self, path: Path, body: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!{sys.executable}\n{body}", encoding="utf-8")

    def run_receiver(self, event: dict | None = None, *, stdin: bool = False) -> subprocess.CompletedProcess[str]:
        payload = json.dumps({"cwd": str(self.project), **(event or {"type": "agent-turn-complete"})})
        return subprocess.run(
            ["bash", str(RECEIVER)] if stdin else ["bash", str(RECEIVER), payload],
            input=payload if stdin else "",
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

    def write_capturing_cli(self) -> None:
        self.write_cli(
            self.trusted_cli,
            "import json, sys\n"
            f"open({str(self.capture)!r}, 'w').write(json.dumps({{'argv': sys.argv[1:], 'input': sys.stdin.read()}}))\n",
        )

    def test_hook_payload_on_stdin_is_ingested(self) -> None:
        self.write_capturing_cli()
        event = {"hook_event_name": "PreCompact", "session_id": "t82", "trigger": "manual"}

        result = self.run_receiver(event, stdin=True)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        capture = json.loads(self.capture.read_text(encoding="utf-8"))
        self.assertEqual(capture["argv"][-3:], ["ingest", "--ingested-from", "codex"])
        self.assertEqual(json.loads(capture["input"]), {"cwd": str(self.project), **event})

    def test_argv_payload_wins_over_stdin(self) -> None:
        self.write_capturing_cli()
        argv_payload = json.dumps({"cwd": str(self.project), "hook_event_name": "SessionEnd", "session_id": "argv"})

        result = subprocess.run(
            ["bash", str(RECEIVER), argv_payload],
            input=json.dumps({"cwd": str(self.project), "session_id": "stdin"}),
            text=True,
            capture_output=True,
            env={**os.environ, "HOME": str(self.home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        capture = json.loads(self.capture.read_text(encoding="utf-8"))
        self.assertEqual(json.loads(capture["input"])["session_id"], "argv")

    def test_invalid_stdin_payload_reports_and_exits_zero(self) -> None:
        self.write_capturing_cli()

        result = subprocess.run(
            ["bash", str(RECEIVER)],
            input="not json",
            text=True,
            capture_output=True,
            env={**os.environ, "HOME": str(self.home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "contextdb-codex-notify: ingest failed\n")
        self.assertFalse(self.capture.exists())

    def test_modules_in_the_session_cwd_cannot_shadow_the_stdlib(self) -> None:
        self.write_capturing_cli()
        hijack = self.root / "hijacked"
        (self.project / "json.py").write_text(f"open({str(hijack)!r}, 'w').write('ran')\n", encoding="utf-8")
        payload = json.dumps({"cwd": str(self.project), "hook_event_name": "SessionEnd", "session_id": "cwd"})

        result = subprocess.run(
            ["bash", str(RECEIVER)],
            input=payload,
            text=True,
            capture_output=True,
            cwd=self.project,
            env={**os.environ, "HOME": str(self.home)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertFalse(hijack.exists())
        self.assertEqual(json.loads(json.loads(self.capture.read_text(encoding="utf-8"))["input"])["session_id"], "cwd")

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
