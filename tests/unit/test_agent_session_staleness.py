#!/usr/bin/env python3
"""Exercise public-filesystem session staleness detection."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_agent-session-staleness"
CHECKER = ROOT / "scripts/check-agent-runtime.py"


def load_script():
    loader = SourceFileLoader("agent_session_staleness", str(SCRIPT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_agent_runtime_staleness", CHECKER
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentSessionStalenessTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="agent-session-staleness-")
        self.home = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def touch(self, relative_path: str, mtime: float) -> Path:
        path = self.home / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n")
        os.utime(path, (mtime, mtime))
        return path

    def plugin_version(self, version: str, mtime: float) -> Path:
        path = self.home / ".claude/plugins/cache/market/plugin" / version
        path.mkdir(parents=True)
        os.utime(path, (mtime, mtime))
        return path

    def run_script(
        self, *args: str, stdin: str | None = None
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(self.home)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            env=env,
            input=stdin,
            text=True,
            capture_output=True,
            timeout=6,
            check=False,
        )

    def test_hook_first_call_writes_private_baseline_and_is_silent(self) -> None:
        result = self.run_script(
            "hook",
            stdin=json.dumps(
                {"session_id": "session/../../escape", "source": "startup"}
            ),
        )

        state_dir = self.home / ".local/state/agent-staleness"
        state_files = list(state_dir.iterdir())
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")
        self.assertEqual(stat.S_IMODE(state_dir.stat().st_mode), 0o700)
        self.assertEqual(len(state_files), 1)
        self.assertNotIn("session", state_files[0].name)
        self.assertEqual(stat.S_IMODE(state_files[0].stat().st_mode), 0o600)
        self.assertGreater(float(state_files[0].read_text()), 0)

    def test_hook_second_call_detects_asset_updated_after_baseline(self) -> None:
        payload = json.dumps({"session_id": "same-session", "source": "startup"})
        first = self.run_script("hook", stdin=payload)
        state_file = next((self.home / ".local/state/agent-staleness").iterdir())
        baseline = float(state_file.read_text())
        time.sleep(0.02)
        updated_at = time.time()
        self.assertGreater(updated_at, baseline)
        self.touch(".agents/skills/example/SKILL.md", updated_at)

        second = self.run_script(
            "hook",
            stdin=json.dumps({"session_id": "same-session", "source": "compact"}),
        )

        self.assertEqual(first.stdout, "")
        self.assertEqual(first.stderr, "")
        self.assertIn("restart recommended: skills", second.stdout)
        self.assertEqual(second.stderr, "")
        self.assertEqual(float(state_file.read_text()), baseline)

    def test_hook_prunes_state_files_older_than_seven_days(self) -> None:
        state_dir = self.home / ".local/state/agent-staleness"
        state_dir.mkdir(parents=True)
        stale = state_dir / "stale"
        current = state_dir / "current"
        stale.write_text("1\n")
        current.write_text("1\n")
        old = time.time() - 8 * 24 * 60 * 60
        os.utime(stale, (old, old))

        result = self.run_script(
            "hook", stdin=json.dumps({"session_id": "new-session", "source": "resume"})
        )

        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")
        self.assertFalse(stale.exists())
        self.assertTrue(current.exists())

    def test_hook_missing_or_garbage_stdin_is_silent_success(self) -> None:
        for stdin in ("", "{not-json", '{"session_id":"' + "x" * 70_000 + '"}'):
            with self.subTest(stdin_length=len(stdin)):
                result = self.run_script("hook", stdin=stdin)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr, "")
                self.assertFalse((self.home / ".local/state/agent-staleness").exists())

    def test_check_is_silent_when_assets_predate_session(self) -> None:
        since = 1_700_000_000
        self.touch(".agents/skills/example/SKILL.md", since - 10)
        self.touch(".claude/settings.json", since - 10)
        self.plugin_version("1.0.0", since - 10)

        result = self.run_script("check", "--since", str(since))

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_check_reports_new_versions_and_mtimes_deduplicated_by_root(self) -> None:
        since = 1_700_000_000
        self.plugin_version("1.0.0", since - 10)
        self.plugin_version("1.1.0", since + 10)
        self.touch(".agents/skills/example/SKILL.md", since + 10)
        self.touch(".agents/skills/example/notes.md", since + 20)
        self.touch(".claude/settings.json", since + 30)

        result = self.run_script("check", "--since", str(since))
        lines = result.stdout.splitlines()

        self.assertEqual(result.returncode, 0)
        self.assertGreaterEqual(len(lines), 3)
        self.assertLessEqual(len(lines), 5)
        self.assertTrue(all(line.startswith("restart recommended:") for line in lines))
        self.assertEqual(sum("skills" in line for line in lines), 1)
        self.assertTrue(any("claude-plugin:market/plugin" in line for line in lines))
        self.assertTrue(any("claude-settings" in line for line in lines))

    def test_internal_failure_is_silent_success_with_one_stderr_line(self) -> None:
        module = load_script()
        with mock.patch.object(
            module, "collect_updates", side_effect=OSError("fixture failure")
        ):
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = module.guarded_main(
                    ["check", "--since", "1700000000"], home=self.home
                )

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(len(stderr.getvalue().splitlines()), 1)

    def test_runtime_state_and_sqlite_files_are_excluded(self) -> None:
        since = 1_700_000_000
        for relative_path in (
            ".agents/compactiondb/.claude/contextdb/state/runtime.json",
            ".agents/compactiondb/.claude/contextdb/spool/event.json",
            ".agents/compactiondb/.claude/contextdb/health/errors.jsonl",
            ".agents/plugins/example/cache.sqlite3",
            ".agents/skills/agmsg/db/messages.db",
        ):
            self.touch(relative_path, since + 10)

        result = self.run_script("check", "--since", str(since))

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_bounded_scan_finishes_under_wall_limit(self) -> None:
        root = self.home / ".agents/skills/large"
        root.mkdir(parents=True)
        for index in range(6_000):
            (root / f"asset-{index}").write_text("x")

        started = time.monotonic()
        result = self.run_script("check", "--since", str(time.time() + 60))
        elapsed = time.monotonic() - started

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertLess(elapsed, 5)

    def test_no_arguments_prints_ten_recent_updates(self) -> None:
        base = 1_700_000_000
        for index in range(12):
            self.touch(f".agents/plugins/plugin-{index}/asset", base + index)

        result = self.run_script()
        lines = result.stdout.splitlines()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(lines), 10)
        self.assertIn("plugin-11/asset", lines[0])

    def test_doctor_delegates_session_staleness_to_installed_script(self) -> None:
        module = load_checker()
        module.HOME = self.home
        completed = subprocess.CompletedProcess([], 0)
        with mock.patch.object(module.subprocess, "run", return_value=completed) as run:
            result = module.run_session_staleness("1700000000")

        self.assertEqual(result, 0)
        run.assert_called_once_with(
            [
                str(self.home / ".local/bin/common/agent-session-staleness"),
                "check",
                "--since",
                "1700000000",
            ],
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
