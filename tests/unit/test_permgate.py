#!/usr/bin/env python3
"""Exercise the fail-closed permgate PermissionRequest hook."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PERMGATE = ROOT / "home/dot_local/bin/common/executable_permgate"

CLAUDE_INPUT = {
    "session_id": "claude-session",
    "transcript_path": "/tmp/transcript.jsonl",
    "cwd": "/tmp/repo",
    "permission_mode": "default",
    "hook_event_name": "PermissionRequest",
    "tool_name": "Bash",
    "tool_input": {"command": "git status --short", "description": "Inspect status"},
    "permission_suggestions": [],
}
CODEX_INPUT = {
    "session_id": "codex-session",
    "turn_id": "turn-1",
    "transcript_path": None,
    "cwd": "/tmp/repo",
    "permission_mode": "default",
    "hook_event_name": "PermissionRequest",
    "model": "gpt-test",
    "tool_name": "Bash",
    "tool_input": {"command": "git status --short", "description": "Inspect status"},
}


def permission_behavior(stdout: str) -> str | None:
    if not stdout:
        return None
    return json.loads(stdout)["hookSpecificOutput"]["decision"]["behavior"]


class PermgateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="permgate-test-")
        self.root = Path(self.temp.name)
        self.policy_path = self.root / "permgate-policy.yaml"
        self.state_path = self.root / "decisions.jsonl"
        self.write_policy()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_policy(self) -> None:
        policy = {
            "schema_version": 3,
            "allow_patterns": [
                {
                    "id": "git-status",
                    "tool": "Bash",
                    "category": "status",
                    "regex": r"^\s*git\s+status(?:\s+[-A-Za-z0-9=.]+)*\s*$",
                    "sources": [{"kind": "test", "count": 3}],
                }
            ],
            "deny_patterns": [
                {
                    "id": "catastrophic-rm",
                    "tool": "Bash",
                    "regex": r"^\s*rm\s+-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*\s+/(?:\s*)$",
                    "message": "Refusing recursive deletion of the filesystem root.",
                    "sources": [{"kind": "safety_invariant", "count": 0}],
                }
            ],
        }
        self.policy_path.write_text(json.dumps(policy, indent=2) + "\n")

    def run_gate(
        self,
        agent: str,
        payload: dict | str,
        *,
        sentinel: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(
            {
                "PERMGATE_POLICY_PATH": str(self.policy_path),
                "PERMGATE_STATE_PATH": str(self.state_path),
                "HOME": str(self.root),
            }
        )
        if sentinel:
            env["PERMGATE_INNER"] = "1"
        else:
            env.pop("PERMGATE_INNER", None)
        stdin = payload if isinstance(payload, str) else json.dumps(payload)
        return subprocess.run(
            [sys.executable, str(PERMGATE), agent],
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )

    def read_log(self) -> list[dict]:
        return [json.loads(line) for line in self.state_path.read_text().splitlines() if line.strip()]

    def test_layer_one_allows_documented_claude_and_codex_contracts(self) -> None:
        for agent, payload in (("claude", CLAUDE_INPUT), ("codex", CODEX_INPUT)):
            with self.subTest(agent=agent):
                result = self.run_gate(agent, payload)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(permission_behavior(result.stdout), "allow")
                decision = json.loads(result.stdout)["hookSpecificOutput"]
                self.assertEqual(decision["hookEventName"], "PermissionRequest")
                self.assertEqual(set(decision["decision"]), {"behavior"})

    def test_layer_one_deny_uses_both_hook_output_schemas(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "rm -rf /", "description": "Dangerous"}}
        for agent in ("claude", "codex"):
            with self.subTest(agent=agent):
                result = self.run_gate(agent, payload)
                self.assertEqual(permission_behavior(result.stdout), "deny")
                decision = json.loads(result.stdout)["hookSpecificOutput"]["decision"]
                self.assertEqual(set(decision), {"behavior", "message"})

    def test_claude_and_codex_hook_outputs_match_golden_bytes(self) -> None:
        fixtures = (
            (
                {"command": "git status --short"},
                ('{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}\n'),
            ),
            (
                {"command": "rm -rf /"},
                (
                    '{"hookSpecificOutput":{"hookEventName":"PermissionRequest",'
                    '"decision":{"behavior":"deny","message":"Refusing recursive '
                    'deletion of the filesystem root."}}}\n'
                ),
            ),
            ({"command": "echo undecided"}, ""),
        )
        for agent, base in (("claude", CLAUDE_INPUT), ("codex", CODEX_INPUT)):
            for tool_input, expected in fixtures:
                with self.subTest(agent=agent, tool_input=tool_input):
                    result = self.run_gate(agent, base | {"tool_input": tool_input})
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, expected)

    def test_undecided_request_falls_through_to_the_native_prompt(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123", "description": "Unknown"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        record = self.read_log()[-1]
        self.assertEqual(record["decision"], "ask")
        self.assertEqual(record["layer"], "fallthrough")

    def test_repository_policy_allows_and_falls_through(self) -> None:
        self.policy_path.write_text((ROOT / "home/dot_agents/permgate-policy.yaml").read_text())
        allowed = self.run_gate("claude", CLAUDE_INPUT | {"tool_input": {"command": "gh pr view 1"}})
        self.assertEqual(permission_behavior(allowed.stdout), "allow")
        undecided = self.run_gate("claude", CLAUDE_INPUT | {"tool_input": {"command": "ls"}})
        self.assertEqual(undecided.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")

    def test_recursion_sentinel_is_a_complete_no_op(self) -> None:
        result = self.run_gate("claude", "not-json", sentinel=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertFalse(self.state_path.exists())

    def test_invalid_policy_returns_ask_and_logs_config_error(self) -> None:
        for text in ("not-json\n", '["schema_version", "allow_patterns", "deny_patterns"]\n'):
            with self.subTest(text=text.strip()):
                self.policy_path.write_text(text)
                result = self.run_gate("codex", CODEX_INPUT)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "config-error")

    def test_invalid_policy_fields_fail_closed(self) -> None:
        base_policy = json.loads(self.policy_path.read_text())
        for label, mutate in (
            ("old schema", lambda policy: policy.update(schema_version=2)),
            ("bad regex", lambda policy: policy["allow_patterns"][0].update(regex="(")),
        ):
            with self.subTest(label):
                policy = json.loads(json.dumps(base_policy))
                mutate(policy)
                self.policy_path.write_text(json.dumps(policy))
                result = self.run_gate("codex", CODEX_INPUT)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "config-error")

    def test_log_shape_redacts_command_and_output(self) -> None:
        secret_marker = "do-not-log-this-argument"
        payload = CODEX_INPUT | {"tool_input": {"command": f"git status --short {secret_marker}"}}
        self.run_gate("codex", payload)
        record = self.read_log()[-1]
        self.assertEqual(
            {
                "ts",
                "agent",
                "tool",
                "input_hash",
                "input_summary",
                "layer",
                "decision",
                "latency_ms",
            },
            set(record),
        )
        self.assertEqual(record["input_summary"], "Bash:git")
        self.assertNotIn(secret_marker, json.dumps(record))
        self.assertEqual(self.state_path.stat().st_mode & 0o777, 0o600)

    def test_allow_pattern_rejects_shell_chaining(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "git status --short; rm -rf /"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")

    def test_git_diff_output_option_is_never_automatically_allowed(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "git diff --output=/tmp/changed.patch"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")

    def test_structured_secret_is_redacted_from_the_summary(self) -> None:
        secret_marker = "structured-secret-must-not-leak"
        payload = CODEX_INPUT | {
            "tool_name": "mcp__vault__read",
            "tool_input": {"api_key": secret_marker},
        }
        result = self.run_gate("codex", payload)
        record = self.read_log()[-1]
        self.assertEqual(result.stdout, "")
        self.assertEqual(record["layer"], "fallthrough")
        self.assertEqual(record["input_summary"], "mcp__vault__read:structured")
        self.assertNotIn(secret_marker, json.dumps(record))

    def test_bash_credentials_fall_through_without_logging_them(self) -> None:
        fixtures = (
            'curl -H "Authorization: Bearer bearer-secret" https://example.invalid',
            'curl -H "Cookie: session=cookie-secret" https://example.invalid',
            "curl https://user:url-secret@example.invalid",
        )
        for command in fixtures:
            with self.subTest(command=command.split()[1]):
                result = self.run_gate("codex", CODEX_INPUT | {"tool_input": {"command": command}})
                record = self.read_log()[-1]
                self.assertEqual(result.stdout, "")
                self.assertEqual(record["layer"], "fallthrough")
                self.assertNotIn("-secret", json.dumps(record))

    def test_script_named_version_is_not_a_version_check(self) -> None:
        self.policy_path.write_text((ROOT / "home/dot_agents/permgate-policy.yaml").read_text())
        for command in ("python3 version", "node version"):
            with self.subTest(command=command):
                result = self.run_gate("codex", CODEX_INPUT | {"tool_input": {"command": command}})
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")

    def test_unconstrained_native_reads_fall_through(self) -> None:
        fixtures = (
            ("Read", {"file_path": "/Users/alice/.ssh/id_rsa"}),
            ("Grep", {"pattern": "secret", "path": "/Users/alice/.ssh"}),
            ("WebFetch", {"url": "http://169.254.169.254/latest/meta-data"}),
        )
        for agent in ("claude", "codex"):
            for tool, tool_input in fixtures:
                with self.subTest(agent=agent, tool=tool):
                    result = self.run_gate(
                        agent,
                        (CLAUDE_INPUT if agent == "claude" else CODEX_INPUT)
                        | {"tool_name": tool, "tool_input": tool_input},
                    )
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")

    def test_apply_patch_is_never_deterministically_allowed(self) -> None:
        payload = CODEX_INPUT | {
            "tool_name": "apply_patch",
            "tool_input": {"patch": "*** Begin Patch\n*** End Patch"},
        }
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertNotEqual(self.read_log()[-1]["layer"], "deterministic")

    def test_mutating_or_executable_read_options_fall_through(self) -> None:
        for command in (
            "git push origin main",
            "rg --pre=malware pattern .",
            "git grep --open-files-in-pager=malware pattern",
            "git log -p",
            "git show HEAD",
            "gh issue view 1 --web=true",
            'gh issue view 1 "--web=true"',
            r"gh issue view 1 --web\=true",
            "gh issue view 1 -w=true",
            'gh issue list --search "$SECRET_TOKEN"',
            "gh issue list --search *.txt",
            "git --config-env=core.fsmonitor=FSMON status --short",
            "git --exec-path=/tmp status",
        ):
            with self.subTest(command=command):
                result = self.run_gate("codex", CODEX_INPUT | {"tool_input": {"command": command}})
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")


if __name__ == "__main__":
    unittest.main()
