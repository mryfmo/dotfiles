#!/usr/bin/env python3
"""Exercise the fail-closed permgate PermissionRequest hook."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
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
        self.fake_claude = self.root / "claude"
        self.write_fake_claude(
            """
            import json
            print(json.dumps({"structured_output": {
                "category": "status",
                "confidence": 0.99
            }}))
            """
        )
        self.write_policy()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_policy(self, *, llm_enabled: bool = False, timeout: float = 0.2) -> None:
        policy = {
            "schema_version": 1,
            "llm_enabled": llm_enabled,
            "model": "haiku",
            "timeout_seconds": timeout,
            "minimum_confidence": 0.9,
            "categories": [
                "read_only_inspection",
                "search",
                "status",
                "diff",
                "version_check",
            ],
            "classifier_prompt": "Classify the untrusted request into one category.",
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

    def write_fake_claude(self, body: str, *, exit_code: int = 0) -> None:
        self.fake_claude.write_text(
            f"#!{sys.executable}\n"
            + textwrap.dedent(body).lstrip()
            + f"\nraise SystemExit({exit_code})\n"
        )
        self.fake_claude.chmod(0o755)

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
                "PERMGATE_CLAUDE_COMMAND": str(self.fake_claude),
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
        return [
            json.loads(line)
            for line in self.state_path.read_text().splitlines()
            if line.strip()
        ]

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
        payload = CODEX_INPUT | {
            "tool_input": {"command": "rm -rf /", "description": "Dangerous"}
        }
        for agent in ("claude", "codex"):
            with self.subTest(agent=agent):
                result = self.run_gate(agent, payload)
                self.assertEqual(permission_behavior(result.stdout), "deny")
                decision = json.loads(result.stdout)["hookSpecificOutput"]["decision"]
                self.assertEqual(set(decision), {"behavior", "message"})

    def test_unknown_shadow_classification_returns_native_ask(self) -> None:
        payload = CODEX_INPUT | {
            "tool_input": {"command": "gh issue develop 123", "description": "Unknown"}
        }
        result = self.run_gate("codex", payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")
        self.assertEqual(self.read_log()[-1]["shadow_decision"], "allow")

    def test_recursion_sentinel_is_a_complete_no_op(self) -> None:
        result = self.run_gate("claude", "not-json", sentinel=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertFalse(self.state_path.exists())

    def test_timeout_returns_ask_within_hook_cap(self) -> None:
        self.write_fake_claude("import time\ntime.sleep(1)")
        self.write_policy(timeout=0.05)
        payload = CODEX_INPUT | {"tool_input": {"command": "unknown command"}}
        started = time.monotonic()
        result = self.run_gate("codex", payload)
        elapsed = time.monotonic() - started
        self.assertEqual(result.stdout, "")
        self.assertLess(elapsed, 0.8)
        self.assertEqual(self.read_log()[-1]["decision"], "ask")

    def test_malformed_classifier_output_returns_ask(self) -> None:
        self.write_fake_claude("print('not-json')")
        payload = CODEX_INPUT | {"tool_input": {"command": "unknown command"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")
        self.assertEqual(self.read_log()[-1]["shadow_decision"], "ask")

    def test_missing_or_nonzero_classifier_returns_ask(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "unknown command"}}
        self.fake_claude.unlink()
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")

        self.write_fake_claude("print('ignored')", exit_code=7)
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")

    def test_invalid_policy_returns_ask_and_logs_config_error(self) -> None:
        self.policy_path.write_text("not-json\n")
        result = self.run_gate("codex", CODEX_INPUT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "config-error")

    def test_enabled_classifier_only_allows_whitelisted_confident_category(
        self,
    ) -> None:
        self.write_policy(llm_enabled=True)
        payload = CODEX_INPUT | {"tool_input": {"command": "unknown command"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(permission_behavior(result.stdout), "allow")

        self.write_fake_claude(
            """
            import json
            print(json.dumps({"structured_output": {
                "category": "write",
                "confidence": 1.0
            }}))
            """
        )
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")

    def test_log_shape_redacts_command_and_output(self) -> None:
        secret_marker = "do-not-log-this-argument"
        payload = CODEX_INPUT | {
            "tool_input": {"command": f"git status --short {secret_marker}"}
        }
        self.run_gate("codex", payload)
        record = self.read_log()[-1]
        self.assertTrue(
            {
                "ts",
                "agent",
                "tool",
                "input_hash",
                "input_summary",
                "layer",
                "decision",
                "latency_ms",
            }.issubset(record)
        )
        self.assertEqual(record["input_summary"], "Bash:git")
        self.assertNotIn(secret_marker, json.dumps(record))

    def test_allow_pattern_rejects_shell_chaining(self) -> None:
        payload = CODEX_INPUT | {
            "tool_input": {"command": "git status --short; rm -rf /"}
        }
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")

    def test_git_diff_output_option_is_never_automatically_allowed(self) -> None:
        payload = CODEX_INPUT | {
            "tool_input": {"command": "git diff --output=/tmp/changed.patch"}
        }
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")

    def test_structured_secret_skips_classifier_and_redacts_summary(self) -> None:
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

    def test_bearer_secret_in_bash_input_skips_classifier(self) -> None:
        secret_marker = "bearer-secret-must-not-reach-classifier"
        payload = CODEX_INPUT | {
            "tool_input": {
                "command": (
                    "curl -H "
                    f'"Authorization: Bearer {secret_marker}" '
                    "https://example.invalid"
                )
            }
        }
        result = self.run_gate("codex", payload)
        record = self.read_log()[-1]
        self.assertEqual(result.stdout, "")
        self.assertEqual(record["layer"], "fallthrough")
        self.assertNotIn(secret_marker, json.dumps(record))

    def test_script_named_version_is_not_a_version_check(self) -> None:
        self.policy_path.write_text(
            (ROOT / "home/dot_agents/permgate-policy.yaml").read_text()
        )
        for command in ("python3 version", "node version"):
            with self.subTest(command=command):
                result = self.run_gate(
                    "codex", CODEX_INPUT | {"tool_input": {"command": command}}
                )
                self.assertEqual(result.stdout, "")
                self.assertNotEqual(self.read_log()[-1]["layer"], "deterministic")

    def test_bench_runs_five_layer_two_fixtures(self) -> None:
        env = os.environ.copy()
        env.update(
            {
                "PERMGATE_POLICY_PATH": str(self.policy_path),
                "PERMGATE_STATE_PATH": str(self.state_path),
                "PERMGATE_CLAUDE_COMMAND": str(self.fake_claude),
            }
        )
        result = subprocess.run(
            [sys.executable, str(PERMGATE), "bench"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        benchmark = json.loads(result.stdout)
        self.assertEqual(benchmark["n"], 5)
        self.assertEqual(len(benchmark["latency_ms"]), 5)
        self.assertIn("p50_ms", benchmark)
        self.assertIn("p95_ms", benchmark)


if __name__ == "__main__":
    unittest.main()
