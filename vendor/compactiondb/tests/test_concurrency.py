from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from tests.support import TempProject
from contextdb.spool import drain_spool


class ConcurrencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = TempProject()

    def tearDown(self) -> None:
        self.p.close()

    @unittest.skipIf(os.name == "nt", "the CI validation for this artifact runs POSIX process semantics")
    def test_parallel_hook_processes_preserve_all_events(self) -> None:
        hook = Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "contextdb_hook.py"
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.p.root))
        processes = []
        count = 32
        for i in range(count):
            payload = json.dumps(
                {
                    "event_uuid": f"parallel-{i}",
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "parallel",
                    "cwd": str(self.p.root),
                    "prompt": f"parallel event {i}",
                }
            )
            process = subprocess.Popen(
                [sys.executable, str(hook)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
            )
            assert process.stdin is not None
            process.stdin.write(payload)
            process.stdin.close()
            processes.append(process)
        for process in processes:
            stdout = process.stdout.read() if process.stdout else ""
            stderr = process.stderr.read() if process.stderr else ""
            if process.stdout:
                process.stdout.close()
            if process.stderr:
                process.stderr.close()
            process.wait(timeout=30)
            self.assertEqual(0, process.returncode, stderr)
            self.assertEqual("", stdout)
        drain_spool(self.p.paths, self.p.config, blocking_lock=True, max_files=1000)
        self.assertEqual(count, self.p.count("events"))
