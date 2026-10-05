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

    def test_installer_defaults_to_a_portable_interpreter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            target.mkdir()
            subprocess.run([sys.executable, str(ROOT / "install.py"), "--project", str(target), "--skip-instructions"], check=True, capture_output=True)
            settings = json.loads((target / ".claude" / "settings.json").read_text())
            commands = {handler["command"] for groups in settings["hooks"].values() for group in groups for handler in group["hooks"]}
            self.assertEqual(commands, {"python3"})

    def test_installer_keeps_an_explicit_interpreter_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "project"
            target.mkdir()
            subprocess.run([sys.executable, str(ROOT / "install.py"), "--project", str(target), "--skip-instructions", "--python", sys.executable], check=True, capture_output=True)
            settings = json.loads((target / ".claude" / "settings.json").read_text())
            commands = {handler["command"] for groups in settings["hooks"].values() for group in groups for handler in group["hooks"]}
            self.assertEqual(commands, {str(Path(sys.executable).resolve())})

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

    def test_reinstall_preserves_hook_positions_bytes_and_mtime_without_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            settings_path = target / ".claude" / "settings.json"
            settings_path.parent.mkdir()
            settings = json.loads((ROOT / ".claude" / "settings.fragment.json").read_text())
            for groups in settings["hooks"].values():
                groups.insert(0, {"hooks": [{"command": "before"}]})
                groups.append({"hooks": [{"command": "after"}]})
            settings_path.write_text(json.dumps(settings, indent=4) + "\n\n")
            original = settings_path.read_bytes()
            mtime = settings_path.stat().st_mtime_ns
            command = [sys.executable, str(ROOT / "install.py"), "--project", str(target), "--skip-instructions"]
            for _ in range(2):
                subprocess.run(command, check=True, capture_output=True)
                self.assertEqual(original, settings_path.read_bytes())
                self.assertEqual(mtime, settings_path.stat().st_mtime_ns)
                self.assertEqual([], list(settings_path.parent.glob("settings.json.compactiondb-backup-*")))

    def test_reinstall_preserves_reversed_managed_groups_around_unrelated_hook(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            settings_path = target / ".claude" / "settings.json"
            settings_path.parent.mkdir()
            settings = json.loads((ROOT / ".claude" / "settings.fragment.json").read_text())
            groups = settings["hooks"]["SessionStart"]
            self.assertEqual(["*", "compact"], [g["matcher"] for g in groups])
            settings["hooks"]["SessionStart"] = [groups[1], {"hooks": [{"command": "unrelated"}]}, groups[0]]
            settings_path.write_text(json.dumps(settings, indent=4) + "\n\n")
            original = settings_path.read_bytes()
            mtime = settings_path.stat().st_mtime_ns
            backup = settings_path.with_name("settings.json.compactiondb-backup-existing")
            backup.write_text("existing backup")
            for _ in range(2):
                subprocess.run([sys.executable, str(ROOT / "install.py"), "--project", str(target), "--skip-instructions"], check=True, capture_output=True)
                self.assertEqual(original, settings_path.read_bytes())
                self.assertEqual(mtime, settings_path.stat().st_mtime_ns)
                self.assertEqual([backup], list(settings_path.parent.glob("settings.json.compactiondb-backup-*")))
                self.assertEqual("existing backup", backup.read_text())

    def test_merge_matches_command_sets_replaces_in_place_and_appends_new(self) -> None:
        def group(script, *, command="python3"):
            return {"matcher": None, "hooks": [{"command": command, "args": [f"/old/{script}.py"]}]}
        unrelated = {"hooks": [{"command": "unrelated"}]}
        old_hook = group("contextdb_hook")
        old_recover = group("contextdb_recover")
        new_hook = group("contextdb_hook", command="/new/python")
        new_recover = group("contextdb_recover", command="/new/python")
        new_cli = group("contextdb_cli")
        existing = {"hooks": {"SessionStart": [old_recover, unrelated, group("log_event"), old_hook]}}
        fragment = {"hooks": {"SessionStart": [new_hook, new_recover, new_cli]}}
        merged, added, removed = INSTALLER.merge_settings(existing, fragment)
        self.assertEqual([new_recover, unrelated, new_hook, new_cli], merged["hooks"]["SessionStart"])
        self.assertEqual((3, 3), (added, removed))

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
