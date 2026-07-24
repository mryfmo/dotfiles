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
        self.fake_codex = self.root / "codex"
        self.claude_capture = self.root / "claude-capture.json"
        self.codex_capture = self.root / "codex-capture.json"
        self.write_fake_claude(
            """
            import json
            print(json.dumps({"structured_output": {
                "category": "status",
                "confidence": 0.99
            }}))
            """
        )
        self.write_fake_codex()
        self.write_policy()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_policy(
        self,
        *,
        enabled_agents: tuple[str, ...] = (),
        timeout: float = 0.2,
    ) -> None:
        policy = {
            "schema_version": 2,
            "providers": {
                "claude": {
                    "llm_enabled": "claude" in enabled_agents,
                    "model": "claude-haiku-4-5-20251001",
                    "timeout_seconds": timeout,
                    "minimum_confidence": 0.9,
                },
                "codex": {
                    "llm_enabled": "codex" in enabled_agents,
                    "model": "gpt-5.6-luna",
                    "timeout_seconds": timeout,
                    "minimum_confidence": 0.9,
                },
            },
            "enablement": {
                "minimum_successes": 5,
                "maximum_p50_ms": 3000,
                "maximum_p95_ms": 7000,
            },
            "categories": [
                "read_only_inspection",
                "search",
                "status",
                "diff",
                "version_check",
            ],
            "classifier_prompt": "Classify the untrusted request into one category.",
            "classifier_actions": {
                "read_only_inspection": [],
                "search": [],
                "status": [
                    "gh.issue.list",
                    "gh.issue.view",
                    "gh.pr.checks",
                    "gh.run.list",
                    "git.status",
                ],
                "diff": [],
                "version_check": [],
            },
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
            "import json\n"
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "prompt = sys.stdin.read()\n"
            "Path(os.environ['PERMGATE_TEST_CLAUDE_CAPTURE']).write_text(\n"
            "    json.dumps({'args': sys.argv[1:], 'prompt': prompt})\n"
            ")\n"
            + textwrap.dedent(body).lstrip()
            + f"\nraise SystemExit({exit_code})\n"
        )
        self.fake_claude.chmod(0o755)

    def write_fake_codex(self, body: str | None = None, *, exit_code: int = 0) -> None:
        body = body or """
            import json
            import os
            import sys
            from pathlib import Path

            args = sys.argv[1:]
            prompt = sys.stdin.read()
            Path(os.environ["PERMGATE_TEST_CODEX_CAPTURE"]).write_text(
                json.dumps({"args": args, "prompt": prompt})
            )
            output = args[args.index("--output-last-message") + 1]
            Path(output).write_text(json.dumps({
                "category": "status",
                "confidence": 0.99
            }))
        """
        self.fake_codex.write_text(
            f"#!{sys.executable}\n"
            + textwrap.dedent(body).lstrip()
            + f"\nraise SystemExit({exit_code})\n"
        )
        self.fake_codex.chmod(0o755)

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
                "PERMGATE_CODEX_COMMAND": str(self.fake_codex),
                "PERMGATE_TEST_CLAUDE_CAPTURE": str(self.claude_capture),
                "PERMGATE_TEST_CODEX_CAPTURE": str(self.codex_capture),
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
            "tool_input": {"command": "gh issue view 123", "description": "Unknown"}
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
        self.write_fake_codex("import time\ntime.sleep(1)")
        self.write_policy(timeout=0.05)
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        started = time.monotonic()
        result = self.run_gate("codex", payload)
        elapsed = time.monotonic() - started
        self.assertEqual(result.stdout, "")
        self.assertLess(elapsed, 0.8)
        self.assertEqual(self.read_log()[-1]["decision"], "ask")

    def test_malformed_classifier_output_returns_ask(self) -> None:
        self.write_fake_codex("print('not-json')")
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")
        self.assertEqual(self.read_log()[-1]["shadow_decision"], "ask")

    def test_missing_or_nonzero_classifier_returns_ask(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        self.fake_codex.unlink()
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")

        self.write_fake_codex("print('ignored')", exit_code=7)
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["decision"], "ask")

    def test_invalid_policy_returns_ask_and_logs_config_error(self) -> None:
        self.policy_path.write_text("not-json\n")
        result = self.run_gate("codex", CODEX_INPUT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "config-error")

    def test_invalid_classifier_policy_fields_fail_closed(self) -> None:
        base_policy = json.loads(self.policy_path.read_text())
        for key, value in (
            ("model", ""),
            ("timeout_seconds", "slow"),
            ("minimum_confidence", "high"),
        ):
            with self.subTest(key=key):
                policy = json.loads(json.dumps(base_policy))
                policy["providers"]["codex"][key] = value
                self.policy_path.write_text(json.dumps(policy))
                result = self.run_gate(
                    "codex",
                    CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}},
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "config-error")

        policy = json.loads(json.dumps(base_policy))
        policy["allow_patterns"][0]["regex"] = "("
        self.policy_path.write_text(json.dumps(policy))
        result = self.run_gate("codex", CODEX_INPUT)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "config-error")

        for actions in (
            {"status": ["git.status"], "diff": ["git.status"]},
            {"status": ["ignore previous instructions"]},
            {"read_only_inspection": ["git.show"]},
            {"read_only_inspection": ["Read"]},
        ):
            with self.subTest(actions=actions):
                policy = json.loads(json.dumps(base_policy))
                for category, values in actions.items():
                    policy["classifier_actions"][category] = values
                self.policy_path.write_text(json.dumps(policy))
                result = self.run_gate("codex", CODEX_INPUT)
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "config-error")

    def test_enabled_classifier_only_allows_whitelisted_confident_category(
        self,
    ) -> None:
        self.write_policy(enabled_agents=("codex",))
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        result = self.run_gate("codex", payload)
        self.assertEqual(permission_behavior(result.stdout), "allow")

        self.write_fake_codex(
            """
            import json
            import sys
            from pathlib import Path
            args = sys.argv[1:]
            output = args[args.index("--output-last-message") + 1]
            Path(output).write_text(json.dumps({
                "category": "read_only_inspection",
                "confidence": 1.0
            }))
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

    def test_bash_credentials_skip_classifier(self) -> None:
        fixtures = (
            'curl -H "Authorization: Bearer bearer-secret" https://example.invalid',
            'curl -H "Cookie: session=cookie-secret" https://example.invalid',
            "curl https://user:url-secret@example.invalid",
        )
        for command in fixtures:
            with self.subTest(command=command.split()[1]):
                result = self.run_gate(
                    "codex", CODEX_INPUT | {"tool_input": {"command": command}}
                )
                record = self.read_log()[-1]
                self.assertEqual(result.stdout, "")
                self.assertEqual(record["layer"], "fallthrough")
                self.assertNotIn("-secret", json.dumps(record))

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
                "PERMGATE_CODEX_COMMAND": str(self.fake_codex),
                "PERMGATE_TEST_CLAUDE_CAPTURE": str(self.claude_capture),
                "PERMGATE_TEST_CODEX_CAPTURE": str(self.codex_capture),
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
        self.assertEqual(set(benchmark), {"claude", "codex"})
        for result in benchmark.values():
            self.assertEqual(result["n"], 5)
            self.assertEqual(len(result["latency_ms"]), 5)
            self.assertEqual(result["successful_classifications"], 5)
            self.assertEqual(result["status_counts"], {"classified": 5})
            self.assertTrue(result["ready_for_enablement"])

    def test_each_agent_uses_only_its_own_authenticated_cli(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        self.run_gate("codex", payload)
        self.assertTrue(self.codex_capture.exists())
        self.assertFalse(self.claude_capture.exists())

        self.codex_capture.unlink()
        self.run_gate(
            "claude",
            CLAUDE_INPUT | {"tool_input": {"command": "gh issue view 123"}},
        )
        self.assertTrue(self.claude_capture.exists())
        self.assertFalse(self.codex_capture.exists())

    def test_classifier_receives_metadata_without_raw_values(self) -> None:
        marker = "raw-value-must-never-reach-a-classifier"
        fixtures = (
            ("codex", CODEX_INPUT | {
                "tool_name": "Bash",
                "tool_input": {"command": f"gh issue view {marker}"},
            }),
            ("claude", CLAUDE_INPUT | {
                "tool_name": "Bash",
                "tool_input": {"command": f"gh issue view {marker}"},
            }),
        )
        for agent, payload in fixtures:
            with self.subTest(agent=agent):
                self.run_gate(agent, payload)
                capture_path = (
                    self.codex_capture if agent == "codex" else self.claude_capture
                )
                capture = capture_path.read_text()
                self.assertNotIn(marker, capture)
                self.assertNotIn("tool_input", capture)

    def test_unconstrained_native_reads_never_reach_classifier(self) -> None:
        self.write_policy(enabled_agents=("claude", "codex"))
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
                    self.assertFalse(self.claude_capture.exists())
                    self.assertFalse(self.codex_capture.exists())

    def test_codex_classifier_is_ephemeral_read_only_and_hook_free(self) -> None:
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        self.run_gate("codex", payload)
        args = json.loads(self.codex_capture.read_text())["args"]
        for token in (
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--disable",
            "hooks",
            "shell_tool",
            "--output-schema",
            "--output-last-message",
        ):
            self.assertIn(token, args)

    def test_shadow_log_contains_reviewable_non_secret_classification(self) -> None:
        marker = "audit-must-not-contain-this"
        payload = CODEX_INPUT | {
            "tool_name": "Bash",
            "tool_input": {"command": f"gh issue view {marker}"},
        }
        self.run_gate("codex", payload)
        record = self.read_log()[-1]
        self.assertEqual(record["provider"], "codex")
        self.assertEqual(record["classification_status"], "classified")
        self.assertEqual(record["classification_action"], "gh.issue.view")
        self.assertEqual(record["category"], "status")
        self.assertEqual(record["confidence"], 0.99)
        self.assertEqual(record["shadow_decision"], "allow")
        self.assertNotIn(marker, json.dumps(record))

    def test_apply_patch_is_never_deterministically_allowed(self) -> None:
        payload = CODEX_INPUT | {
            "tool_name": "apply_patch",
            "tool_input": {"patch": "*** Begin Patch\n*** End Patch"},
        }
        result = self.run_gate("codex", payload)
        self.assertEqual(result.stdout, "")
        self.assertNotEqual(self.read_log()[-1]["layer"], "deterministic")
        self.assertFalse(self.codex_capture.exists())

    def test_mutating_or_executable_read_options_never_reach_classifier(self) -> None:
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
                result = self.run_gate(
                    "codex", CODEX_INPUT | {"tool_input": {"command": command}}
                )
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")
                self.assertFalse(self.codex_capture.exists())

    def test_classifier_rejects_path_qualified_executables(self) -> None:
        self.write_policy(enabled_agents=("codex",))
        for command in ("./gh issue view 123", "/tmp/git status"):
            with self.subTest(command=command):
                result = self.run_gate(
                    "codex", CODEX_INPUT | {"tool_input": {"command": command}}
                )
                self.assertEqual(result.stdout, "")
                self.assertEqual(self.read_log()[-1]["layer"], "fallthrough")
                self.assertFalse(self.codex_capture.exists())

    def test_bench_with_no_eligible_fixtures_is_not_ready(self) -> None:
        policy = json.loads(self.policy_path.read_text())
        for category in policy["classifier_actions"]:
            policy["classifier_actions"][category] = []
        self.policy_path.write_text(json.dumps(policy))
        env = os.environ.copy()
        env.update(
            {
                "PERMGATE_POLICY_PATH": str(self.policy_path),
                "PERMGATE_CLAUDE_COMMAND": str(self.fake_claude),
                "PERMGATE_CODEX_COMMAND": str(self.fake_codex),
                "PERMGATE_TEST_CLAUDE_CAPTURE": str(self.claude_capture),
                "PERMGATE_TEST_CODEX_CAPTURE": str(self.codex_capture),
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
        for provider in json.loads(result.stdout).values():
            self.assertEqual(provider["n"], 0)
            self.assertIsNone(provider["p50_ms"])
            self.assertIsNone(provider["p95_ms"])
            self.assertFalse(provider["ready_for_enablement"])

    def test_provider_enablement_never_enables_the_sibling_provider(self) -> None:
        self.write_policy(enabled_agents=("codex",))
        payload = CODEX_INPUT | {"tool_input": {"command": "gh issue view 123"}}
        codex_result = self.run_gate("codex", payload)
        claude_result = self.run_gate(
            "claude",
            CLAUDE_INPUT | {"tool_input": {"command": "gh issue view 123"}},
        )

        self.assertEqual(permission_behavior(codex_result.stdout), "allow")
        self.assertEqual(claude_result.stdout, "")
        self.assertEqual(self.read_log()[-1]["layer"], "llm-shadow")


if __name__ == "__main__":
    unittest.main()
