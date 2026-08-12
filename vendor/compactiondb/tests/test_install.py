from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("compactiondb_installer", ROOT / "install.py")
assert SPEC and SPEC.loader
INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER)


class InstallerTests(unittest.TestCase):
    def test_merge_replaces_only_previous_contextdb_groups(self) -> None:
        existing = {
            "hooks": {
                "PostToolUse": [
                    {"matcher": "Bash", "hooks": [{"type": "command", "command": "other-tool"}]},
                    {"matcher": "*", "hooks": [{"type": "command", "command": "python3", "args": ["/old/contextdb_hook.py"]}]},
                ]
            }
        }
        fragment = {
            "hooks": {
                "PostToolUse": [
                    {"matcher": "*", "hooks": [{"type": "command", "command": "/new/python", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/contextdb_hook.py"]}]}
                ]
            }
        }
        merged, added, removed = INSTALLER.merge_settings(existing, fragment)
        self.assertEqual(1, added)
        self.assertEqual(1, removed)
        groups = merged["hooks"]["PostToolUse"]
        self.assertEqual(2, len(groups))
        self.assertTrue(any(g["hooks"][0]["command"] == "other-tool" for g in groups))
        self.assertTrue(any(g["hooks"][0]["command"] == "/new/python" for g in groups))

    def test_installer_is_idempotent_in_a_separate_project(self) -> None:
        with tempfile.TemporaryDirectory(prefix="contextdb-install-") as temp:
            target = Path(temp) / "target"
            (target / ".claude").mkdir(parents=True)
            (target / ".claude" / "settings.json").write_text(
                json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo unrelated"}]}]}}),
                encoding="utf-8",
            )
            command = [sys.executable, str(ROOT / "install.py"), "--project", str(target)]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(0, first.returncode, first.stderr)
            self.assertEqual(0, second.returncode, second.stderr)
            settings = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
            self.assertTrue(any(g["hooks"][0]["command"] == "echo unrelated" for g in settings["hooks"]["Stop"]))
            serialized = json.dumps(settings)
            self.assertEqual(1, serialized.count("contextdb_recover.py"))
            self.assertTrue((target / ".claude" / "hooks" / "contextdb_cli.py").exists())

    def test_installer_can_run_against_its_own_extracted_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="contextdb-self-") as temp:
            copy = Path(temp) / "package"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "context.db", ".writer.lock"))
            result = subprocess.run(
                [sys.executable, str(copy / "install.py"), "--project", str(copy), "--skip-instructions"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
