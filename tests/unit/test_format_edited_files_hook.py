import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "home/dot_claude/hooks/executable_format-edited-files.py"


class FormatEditedFilesHookTest(unittest.TestCase):
    def test_formatters_run_from_the_edited_files_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_dir = Path(temp)
            repo = temp_dir / "repo"
            (repo / "records").mkdir(parents=True)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            record = repo / "records/note.md"
            record.write_text("# note\n")
            script = repo / "tool.py"
            script.write_text("x = 1\n")
            (repo / "ruff.toml").write_text("line-length = 120\n")
            bin_dir = temp_dir / "bin"
            bin_dir.mkdir()
            log = temp_dir / "calls.txt"
            for name in ("ruff", "prettier"):
                fake = bin_dir / name
                fake.write_text(f'#!/bin/sh\nprintf "%s %s %s\\n" "{name}" "$(pwd -P)" "$*" >> "{log}"\n')
                fake.chmod(0o755)
            elsewhere = temp_dir / "session-cwd"
            elsewhere.mkdir()
            payload = {"tool_input": {"edits": [{"file_path": str(record)}, {"file_path": str(script)}]}}

            result = subprocess.run(
                [sys.executable, str(HOOK)],
                input=json.dumps(payload),
                cwd=elsewhere,
                env={**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"},
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            root = repo.resolve()
            self.assertEqual(
                sorted(log.read_text().splitlines()),
                [
                    f"prettier {root} --write {root / 'records/note.md'}",
                    f"ruff {root} format --config {root / 'ruff.toml'} {root / 'tool.py'}",
                ],
            )

    def test_a_missing_formatter_is_reported_without_a_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            script = Path(temp) / "tool.py"
            script.write_text("x = 1\n")
            payload = {"tool_input": {"file_path": str(script)}}

            result = subprocess.run(
                [sys.executable, str(HOOK)],
                input=json.dumps(payload),
                env={**os.environ, "PATH": "/nonexistent"},
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "ruff is not installed; run `make update` (it installs every declared mise tool)", result.stderr
            )
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
