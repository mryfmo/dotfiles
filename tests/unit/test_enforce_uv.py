#!/usr/bin/env python3
"""Exercise the enforce-uv PreToolUse output contract without running commands."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


HOOK = Path(__file__).resolve().parents[2] / "home/dot_claude/hooks/executable_enforce-uv.sh"


class EnforceUvTest(unittest.TestCase):
    def hook(self, payload: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["bash", str(HOOK)], input=payload, capture_output=True, text=True, check=False)

    def test_all_blocking_branches_emit_current_deny_json(self) -> None:
        for command, advice in (
            ("pip install requests", "uv add requests"),
            ("pip install -r requirements.txt", "uv add -r requirements.txt"),
            ("pip install --dev pytest", "uv add --dev pytest"),
            ("pip install -e .", "編集可能インストール: uv add -e ."),
            ("pip uninstall -y requests", "uv remove requests"),
            ("pip list", "uv tree"),
            ("pip freeze", "uv export --format requirements-txt"),
            ("pip show requests", "uv show requests"),
            ("pip3 install numpy", "uv add numpy"),
            ("python -m pip install -r requirements.txt", "uv add -r requirements.txt"),
            ("python -m pip install requests", "uv add requests"),
            ("python -m pip list", "uv list"),
            ("python -m pytest", "uv run python -m pytest"),
            ("python script.py", "uv run script.py"),
            ("python3 script.py", "uv run script.py"),
            ("py script.py", "uv run py script.py"),
            (r"""python -m 'mod"quoted\path' """, r'mod"quoted\path'),
        ):
            with self.subTest(command=command):
                result = self.hook(json.dumps({"tool_name": "Bash", "tool_input": {"command": command}}))
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("", result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual({"hookSpecificOutput"}, output.keys())
                decision = output["hookSpecificOutput"]
                self.assertEqual({"hookEventName", "permissionDecision", "permissionDecisionReason"}, decision.keys())
                self.assertEqual("PreToolUse", decision["hookEventName"])
                self.assertEqual("deny", decision["permissionDecision"])
                self.assertIn(advice, decision["permissionDecisionReason"])
                self.assertIn("\n", decision["permissionDecisionReason"])

    def test_nonblocking_input_exits_zero_without_output(self) -> None:
        payloads = ["", "not json", "null", "{}"]
        payloads += [
            json.dumps({"tool_name": tool, "tool_input": {"command": command}})
            for tool, command in (
                ("Bash", "uv run python -V"),
                ("Bash", "uv add requests"),
                ("Bash", "git status"),
                ("Bash", ""),
                ("Read", "pip install requests"),
                ("Bash", "echo python"),
            )
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                result = self.hook(payload)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("", result.stdout)
                self.assertEqual("", result.stderr)


if __name__ == "__main__":
    unittest.main()
