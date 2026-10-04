#!/usr/bin/env python3
"""The tracked .gitignore hides the Claude Code sandbox placeholder targets."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDERS = (
    ".bash_profile .bashrc .claude/agents .claude/commands .claude/launch.json .claude/loop.md"
    " .claude/output-styles .claude/routines .claude/skills .claude/workflows .gitconfig .gitmodules"
    " .idea .mcp.json .profile .ripgreprc .vscode .zprofile .zshrc"
).split()


class SandboxPlaceholderIgnoreTest(unittest.TestCase):
    def setUp(self) -> None:
        # A fresh repository with only the tracked .gitignore: the shared
        # .git/info/exclude and the user's global excludes cannot mask a gap.
        self.repo = Path(tempfile.mkdtemp(prefix="gitignore-placeholders-"))
        self.addCleanup(shutil.rmtree, self.repo)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        shutil.copyfile(ROOT / ".gitignore", self.repo / ".gitignore")

    def check_ignore(self, path: str) -> int:
        return subprocess.run(
            ["git", "-c", "core.excludesFile=/dev/null", "check-ignore", "-q", "--no-index", path],
            cwd=self.repo,
            check=False,
        ).returncode

    def test_every_placeholder_is_ignored_at_the_root_only(self) -> None:
        for path in PLACEHOLDERS:
            with self.subTest(path=path):
                self.assertEqual(self.check_ignore(path), 0)
                self.assertEqual(self.check_ignore(f"home/{path}"), 1)

    def test_claude_settings_stay_visible(self) -> None:
        for path in (".claude/settings.json", ".claude/settings.local.json"):
            with self.subTest(path=path):
                self.assertEqual(self.check_ignore(path), 1)


if __name__ == "__main__":
    unittest.main()
