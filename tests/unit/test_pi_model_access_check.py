"""Unit tests for the Pi model-access verification harness."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_pi-model-access-check"
ERROR_MESSAGE = (
    "400 You're out of extra usage. "
    + ("x" * 180)
    + "TAIL_MUST_BE_TRUNCATED"
)


FAKE_PI = r"""#!/usr/bin/env python3
import json
import os
import sys

scenario = os.environ.get("FAKE_PI_SCENARIO", "pass")
error_message = os.environ["FAKE_PI_ERROR_MESSAGE"]
args = sys.argv[1:]
with open(os.environ["FAKE_PI_ARGS_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(args) + "\n")

if args == ["--version"]:
    if scenario == "version_fail":
        print("version unavailable", file=sys.stderr)
        raise SystemExit(2)
    print("0.84.2" if scenario == "wrong_version" else "0.84.1")
    raise SystemExit(0)

if "--extension" not in args:
    print("missing explicit extension", file=sys.stderr)
    raise SystemExit(3)

if "--mode" in args and args[args.index("--mode") + 1] == "json":
    if scenario == "print_fail":
        print("provider failure", file=sys.stderr)
        raise SystemExit(2)
    answer = "NOT OK" if scenario == "wrong_answer" else "OK"
    events = [{"type": "agent_start"}]
    if scenario == "reasoning":
        thinking = {
            "role": "assistant",
            "content": [{"type": "thinking", "thinking": "private reasoning"}],
        }
        events.extend([
            {"type": "turn_start"},
            {"type": "message_start", "message": thinking},
            {"type": "message_end", "message": thinking},
        ])
    if scenario == "error_turn":
        message = {
            "role": "assistant",
            "content": [],
            "stopReason": "error",
            "errorMessage": error_message,
        }
    else:
        message = {
            "role": "assistant", "content": [{"type": "text", "text": answer}]
        }
    events.extend([
        {"type": "message_start", "message": message},
        {"type": "message_end", "message": message},
        {"type": "turn_end", "message": message, "toolResults": []},
        {"type": "agent_end", "messages": [message]},
        {"type": "agent_settled"},
    ])
    for event in events:
        print(json.dumps(event))
    raise SystemExit(0)

if "--mode" in args and args[args.index("--mode") + 1] == "rpc":
    for line in sys.stdin:
        command = json.loads(line)
        if command != {
            "id": "t67-check",
            "type": "prompt",
            "message": "Reply with exactly OK",
        }:
            raise SystemExit(5)
        answer = "NOT OK" if scenario == "rpc_wrong_answer" else "OK"
        events = [
            {"id": command.get("id"), "type": "response", "command": "prompt", "success": True},
            {"type": "agent_start"},
        ]
        if scenario == "reasoning":
            thinking = {
                "role": "assistant",
                "content": [{"type": "thinking", "thinking": "private reasoning"}],
            }
            events.extend([
                {"type": "turn_start"},
                {"type": "message_start", "message": thinking},
                {"type": "message_end", "message": thinking},
            ])
        if scenario == "error_turn":
            message = {
                "role": "assistant",
                "content": [],
                "stopReason": "error",
                "errorMessage": error_message,
            }
        else:
            message = {
                "role": "assistant", "content": [{"type": "text", "text": answer}]
            }
        events.extend([
            {"type": "message_start", "message": message},
            {"type": "message_end", "message": message},
        ])
        if scenario != "rpc_no_end":
            events.append({"type": "agent_end", "messages": [], "willRetry": False})
            events.append({"type": "agent_settled"})
        for event in events:
            print(json.dumps(event), flush=True)
        if scenario == "rpc_no_end":
            raise SystemExit(0)
        for _ in sys.stdin:
            pass
        raise SystemExit(0)

raise SystemExit(4)
"""


class PiModelAccessCheckTest(unittest.TestCase):
    """Exercise the checker against a fake Pi JSONL process."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        self.fake_pi = self.bin_dir / "pi"
        self.fake_pi.write_text(textwrap.dedent(FAKE_PI), encoding="utf-8")
        self.fake_pi.chmod(0o755)
        self.home = self.root / "home"
        extension = self.home / ".pi/agent/extensions/permgate.ts"
        extension.parent.mkdir(parents=True)
        extension.write_text("export default function () {}\n", encoding="utf-8")
        self.args_log = self.root / "args.jsonl"

    def write_auth_json(self, value: object) -> None:
        auth_path = self.home / ".pi/agent/auth.json"
        auth_path.write_text(json.dumps(value), encoding="utf-8")

    def run_check(
        self,
        *,
        scenario: str = "pass",
        provider: str | None = "anthropic",
        model: str | None = "test-model",
        include_key: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        env = {
            "PATH": f"{self.bin_dir}:{os.environ['PATH']}",
            "HOME": str(self.home),
            "FAKE_PI_SCENARIO": scenario,
            "FAKE_PI_ERROR_MESSAGE": ERROR_MESSAGE,
            "FAKE_PI_ARGS_LOG": str(self.args_log),
        }
        if provider is not None:
            env["PI_CHECK_PROVIDER"] = provider
        if model is not None:
            env["PI_CHECK_MODEL"] = model
        if include_key:
            env["ANTHROPIC_API_KEY"] = "test-secret-must-not-appear"
        return subprocess.run(
            ["bash", str(SCRIPT)],
            cwd=self.root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def test_passes_print_rpc_and_explicit_extension_load(self) -> None:
        result = self.run_check()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS version: pi 0.84.1", result.stdout)
        self.assertIn("PASS json: assistant replied exactly OK", result.stdout)
        self.assertIn("PASS rpc: agent_end received", result.stdout)
        self.assertIn(
            "RPC envelope KINDS: response,agent_start,message_start,message_end,agent_end",
            result.stdout,
        )
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)
        self.assertNotIn("test-secret-must-not-appear", result.stdout + result.stderr)
        invocations = self.args_log.read_text(encoding="utf-8")
        self.assertIn('"--extension"', invocations)
        self.assertIn('"--provider", "anthropic"', invocations)
        self.assertIn('"--model", "test-model"', invocations)

    def test_skips_model_steps_when_provider_is_not_selected(self) -> None:
        result = self.run_check(provider=None, model=None, include_key=False)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SKIP json: set PI_CHECK_PROVIDER and PI_CHECK_MODEL", result.stdout)
        self.assertIn("SKIP rpc: set PI_CHECK_PROVIDER and PI_CHECK_MODEL", result.stdout)
        self.assertIn("SKIP extension: model-access prerequisites unavailable", result.stdout)

    def test_skips_model_steps_when_documented_key_is_unset(self) -> None:
        result = self.run_check(include_key=False)

        self.assertEqual(result.returncode, 0, result.stderr)
        reason = (
            "set a documented credential environment variable or run /login "
            "for anthropic"
        )
        self.assertIn(f"SKIP json: {reason}", result.stdout)
        self.assertIn(f"SKIP rpc: {reason}", result.stdout)
        self.assertIn("SKIP extension: model-access prerequisites unavailable", result.stdout)

    def test_anthropic_subscription_entry_runs_when_env_key_is_unset(self) -> None:
        sentinel = "anthropic-subscription-secret-must-not-appear"
        self.write_auth_json(
            {
                "anthropic": {
                    "type": "oauth",
                    "access": sentinel,
                    "refresh": f"refresh-{sentinel}",
                    "expires": 9999999999999,
                }
            }
        )

        result = self.run_check(include_key=False)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS json: assistant replied exactly OK", result.stdout)
        self.assertIn("PASS rpc: agent_end received", result.stdout)
        self.assertNotIn(sentinel, result.stdout + result.stderr)

    def test_subscription_auth_entry_runs_model_steps(self) -> None:
        sentinel = "subscription-secret-must-not-appear"
        self.write_auth_json(
            {
                "openai-codex": {
                    "type": "oauth",
                    "access": sentinel,
                    "refresh": f"refresh-{sentinel}",
                    "expires": 9999999999999,
                }
            }
        )

        result = self.run_check(provider="openai-codex", include_key=False)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS json: assistant replied exactly OK", result.stdout)
        self.assertIn("PASS rpc: agent_end received", result.stdout)
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)
        self.assertNotIn(sentinel, result.stdout + result.stderr)

    def test_missing_subscription_entry_skips_with_both_auth_lanes(self) -> None:
        sentinel = "unselected-secret-must-not-appear"
        self.write_auth_json(
            {
                "another-provider": {
                    "type": "oauth",
                    "access": sentinel,
                    "refresh": f"refresh-{sentinel}",
                    "expires": 9999999999999,
                }
            }
        )

        result = self.run_check(provider="openai-codex", include_key=False)

        self.assertEqual(result.returncode, 0, result.stderr)
        reason = (
            "set a documented credential environment variable or run /login "
            "for openai-codex"
        )
        self.assertIn(f"SKIP json: {reason}", result.stdout)
        self.assertIn(f"SKIP rpc: {reason}", result.stdout)
        self.assertIn("SKIP extension: model-access prerequisites unavailable", result.stdout)
        self.assertNotIn(sentinel, result.stdout + result.stderr)
        self.assertEqual(len(self.args_log.read_text(encoding="utf-8").splitlines()), 1)

    def test_malformed_subscription_auth_skips_without_printing_contents(self) -> None:
        sentinel = "malformed-secret-must-not-appear"
        auth_path = self.home / ".pi/agent/auth.json"
        auth_path.write_text(
            f'{{"openai-codex": "{sentinel}"',
            encoding="utf-8",
        )

        result = self.run_check(provider="openai-codex", include_key=False)

        self.assertEqual(result.returncode, 0, result.stderr)
        reason = (
            "set a documented credential environment variable or run /login "
            "for openai-codex"
        )
        self.assertIn(f"SKIP json: {reason}", result.stdout)
        self.assertIn(f"SKIP rpc: {reason}", result.stdout)
        self.assertNotIn(sentinel, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_fails_on_wrong_pinned_version_without_model_calls(self) -> None:
        result = self.run_check(scenario="wrong_version")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL version: expected 0.84.1, got 0.84.2", result.stdout)
        self.assertIn("SKIP json: exact Pi version unavailable", result.stdout)
        self.assertIn("SKIP rpc: exact Pi version unavailable", result.stdout)
        self.assertIn("SKIP extension: exact Pi version unavailable", result.stdout)
        self.assertEqual(len(self.args_log.read_text(encoding="utf-8").splitlines()), 1)

    def test_fails_when_version_command_is_nonzero(self) -> None:
        result = self.run_check(scenario="version_fail")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL version: pi --version failed", result.stdout)
        self.assertIn("SKIP rpc: exact Pi version unavailable", result.stdout)
        self.assertEqual(len(self.args_log.read_text(encoding="utf-8").splitlines()), 1)

    def test_fails_when_print_command_fails_but_still_checks_rpc(self) -> None:
        result = self.run_check(scenario="print_fail")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL json: pi print invocation failed", result.stdout)
        self.assertIn("PASS rpc: agent_end received", result.stdout)
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)

    def test_fails_when_rpc_exits_without_agent_end_and_lists_kinds(self) -> None:
        result = self.run_check(scenario="rpc_no_end")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL rpc: agent_end not received", result.stdout)
        self.assertIn(
            "RPC envelope KINDS: response,agent_start,message_start,message_end",
            result.stdout,
        )
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)

    def test_reasoning_double_message_uses_final_text(self) -> None:
        result = self.run_check(scenario="reasoning")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS json: assistant replied exactly OK", result.stdout)
        self.assertIn("PASS rpc: agent_end received", result.stdout)
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)
        self.assertNotIn("private reasoning", result.stdout + result.stderr)

    def test_json_mismatch_still_checks_rpc_and_extension(self) -> None:
        result = self.run_check(scenario="wrong_answer")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL json: assistant response was not exactly OK", result.stdout)
        self.assertIn("PASS rpc: agent_end received", result.stdout)
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)

    def test_rpc_mismatch_after_agent_end_keeps_extension_confirmation(self) -> None:
        result = self.run_check(scenario="rpc_wrong_answer")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL rpc: assistant response was not exactly OK", result.stdout)
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)

    def test_error_turn_reports_bounded_provider_api_diagnostic(self) -> None:
        result = self.run_check(scenario="error_turn")

        diagnostic = f"provider/API error: {ERROR_MESSAGE[:160]}"
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout.count(diagnostic), 2)
        self.assertNotIn("assistant response was not exactly OK", result.stdout)
        self.assertNotIn("TAIL_MUST_BE_TRUNCATED", result.stdout + result.stderr)
        self.assertIn("PASS extension: permgate.ts loaded via --extension", result.stdout)


if __name__ == "__main__":
    unittest.main()
