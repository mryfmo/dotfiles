import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / "home/dot_claude/hooks/executable_format-edited-files.py"


def prettier_runs() -> bool:
    """True only when prettier actually starts: a mise shim with no version set is on PATH but exits non-zero."""
    try:
        return subprocess.run(["prettier", "--version"], capture_output=True, timeout=30, check=False).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


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
            calls = {
                name: (cwd, args.split())
                for name, cwd, args in (line.split(" ", 2) for line in log.read_text().splitlines())
            }
            prettier_cwd, prettier_args = calls["prettier"]
            self.assertEqual(prettier_cwd, str(root))
            self.assertIn("--no-config", prettier_args)
            self.assertIn(str(root / "records/note.md"), prettier_args)
            self.assertEqual(
                calls["ruff"], (str(root), ["format", "--config", str(root / "ruff.toml"), str(root / "tool.py")])
            )

    @unittest.skipUnless(prettier_runs(), "prettier cannot run on this host")
    def test_project_prettier_config_code_never_runs(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            marker = repo / "MARKER"
            # A sandboxed command can write this file; the hook runs outside the sandbox.
            (repo / "prettier.config.js").write_text(
                f'require("fs").writeFileSync({json.dumps(str(marker))}, "ran");\nmodule.exports = {{ tabWidth: 8 }};\n'
            )
            document = repo / "a.md"
            document.write_text("# T\n\n*  a\n")

            result = subprocess.run(
                [sys.executable, str(HOOK)],
                input=json.dumps({"tool_input": {"file_path": str(document)}}),
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertEqual(document.read_text(), "# T\n\n- a\n")

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
