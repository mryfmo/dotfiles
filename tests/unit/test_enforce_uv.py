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
            ("python script.py", "uv run python script.py"),
            ("python3 script.py", "uv run python3 script.py"),
            ("py script.py", "uv run py script.py"),
            (r"""python -m 'mod"quoted\path' """, r'mod"quoted\path'),
            # U76 (F137): the advice is the command as written, quotes kept, and a compound line is judged per command.
            ("python3 -c 'print(1)'", "uv run python3 -c 'print(1)'"),
            ("cd x && python foo.py", "uv run python foo.py"),
            ("make lint; pip install requests", "uv add requests"),
            ("cat in.txt | python3 -c 'import sys'", "uv run python3 -c 'import sys'"),
            # U76 audit: a comment or a here-document body is data, the commands around it still count.
            ("echo a#b; python x.py", "uv run python x.py"),
            ("cat <<EOF > notes.txt\npython x.py\nEOF\npython y.py", "uv run python y.py"),
            ("cat <<'EOF'; python z.py\nbody\nEOF", "uv run python z.py"),
            # U76 round 3: an `&` inside a redirection is no separator, so the suggestion keeps the redirection whole.
            ("python3 script.py 2>&1", "uv run python3 script.py 2>&1\n"),
            ("python3 script.py >&2", "uv run python3 script.py >&2\n"),
            ("python3 a.py &>log.txt", "uv run python3 a.py &>log.txt\n"),
            ("python3 script.py >| out", "uv run python3 script.py >| out\n"),
            ("echo a >| f | python x.py", "uv run python x.py"),
            # U76 round 6: an escaped character is part of its word, so `\ #` starts no comment and `\>&` no redirection.
            ("echo \\ # ; python x.py", "uv run python x.py"),
            ("echo a\\#b; python y.py", "uv run python y.py"),
            ("echo \\>&python z.py", "uv run python z.py"),
            ("sleep 1 & python x.py", "uv run python x.py"),
            ("make lint 2>&1 && python y.py", "uv run python y.py"),
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
                ("Bash", "echo 'a; python x'"),
                ("Bash", 'git commit -m "use python && pip here"'),
                ("Bash", "cd x && uv run python foo.py"),
                ("Bash", "echo ok # ; python script.py"),
                ("Bash", "echo \\\\ # ; python script.py"),
                ("Bash", "# python script.py\ngit status"),
                ("Bash", "cat <<EOF > run.sh\npython x.py\nEOF"),
                ("Bash", "cat <<'EOF' > run.sh\npip install x\nEOF\nchmod +x run.sh"),
                ("Bash", "cat <<-EOF\n\tpython x.py\n\tEOF\nls"),
                ("Bash", 'cat <<"END" | tee a <<A2\npython a.py\nEND\npython b.py\nA2'),
                ("Bash", "grep -c x <<< 'python x.py'"),
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
