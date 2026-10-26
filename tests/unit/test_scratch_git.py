"""Scratch git repositories never start background maintenance (regime-cutover U100; see scratch_git.py)."""

from __future__ import annotations

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import SETTINGS, quiet_git, quiet_git_env  # noqa: E402

quiet_git()  # U100: no git command in this module's scratch repositories starts background maintenance

HERE = Path(__file__).resolve().parent
# A git command whose subcommand is init: ["git", …, "init"], git(…"init"), self.git("init"), and ("init", "-…") argv.
INIT = re.compile(r"""(\bgit\b[^\n]{0,160}?["']init["'])|(\(\s*\(?["']init["'],\s*["']-)|(\[\s*["']init["'],)""")
IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}


def calls_quiet_git_at_module_level(tree: ast.Module) -> bool:
    return any(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "quiet_git"
        for node in tree.body
    )


class ScratchGitTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="scratch-git-test-"))
        self.addCleanup(shutil.rmtree, self.repo, True)

    def git(self, *args: str, env: dict | None = None) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), "-c", "commit.gpgsign=false", *args],
            env=(os.environ if env is None else env) | IDENTITY,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        ).stdout.strip()

    def test_every_module_that_creates_a_git_repository_quiets_git(self):
        # PR #559: test_pinned_lint_tools committed, git's detached auto maintenance held maintenance.lock, and the
        # test's rmtree failed. Every module that creates a repository calls quiet_git() at module level.
        missing = []
        for path in sorted(HERE.glob("test_*.py")):
            text = path.read_text()
            if INIT.search(text) and not calls_quiet_git_at_module_level(ast.parse(text)):
                missing.append(path.name)
        self.assertEqual([], missing)

    def test_a_scratch_repository_has_auto_maintenance_off_and_commits_leave_nothing_running(self):
        self.git("init", "-q")
        for key, value in SETTINGS:
            with self.subTest(key):
                self.assertEqual(value, self.git("config", "--get", key))
        # Without the settings, git 2.56 left maintenance.lock behind a commit in 187 of 200 fresh repositories.
        for number in range(5):
            (self.repo / "file").write_text(f"{number}\n")
            self.git("add", "-A")
            self.git("commit", "-q", "-m", str(number))
            self.assertFalse((self.repo / ".git/objects/maintenance.lock").exists(), number)

    def test_an_env_built_from_scratch_carries_the_settings(self):
        env = quiet_git_env({"PATH": os.environ["PATH"], "HOME": str(self.repo), "GIT_CONFIG_NOSYSTEM": "1"})
        self.git("init", "-q", env=env)
        for key, value in SETTINGS:
            with self.subTest(key):
                self.assertEqual(value, self.git("config", "--get", key, env=env))

    def test_the_shard_runner_quiets_git_for_a_module_that_does_not(self):
        # Process-wide layer: scripts/ci/unittest-shards.py (what `make unit-test` and CI run) passes the settings to
        # every shard, so a module without its own quiet_git() call, started with none of them inherited, has them.
        start = self.repo / "start"
        start.mkdir()
        (start / "test_bare.py").write_text(
            "import os, subprocess, tempfile, unittest\n"
            "class Bare(unittest.TestCase):\n"
            "    def test_settings(self):\n"
            "        repo = tempfile.mkdtemp()\n"
            "        subprocess.run(['git', 'init', '-q', repo], check=True)\n"
            "        for key, value in " + repr(list(SETTINGS)) + ":\n"
            "            got = subprocess.run(['git', '-C', repo, 'config', '--get', key], capture_output=True, text=True)\n"
            "            self.assertEqual(value, got.stdout.strip(), key)\n"
        )
        bare = {name: value for name, value in os.environ.items() if not name.startswith("GIT_CONFIG_")}
        result = subprocess.run(
            [
                sys.executable,
                str(HERE.parents[1] / "scripts/ci/unittest-shards.py"),
                "--start",
                str(start),
                "--jobs",
                "1",
            ],
            env=bare,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_existing_entries_stay_first_and_the_merge_is_idempotent(self):
        base = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "commit.gpgsign", "GIT_CONFIG_VALUE_0": "false"}
        merged = quiet_git_env(base)
        self.assertEqual(str(1 + len(SETTINGS)), merged["GIT_CONFIG_COUNT"])
        self.assertEqual(("commit.gpgsign", "false"), (merged["GIT_CONFIG_KEY_0"], merged["GIT_CONFIG_VALUE_0"]))
        self.assertEqual(
            list(SETTINGS),
            [(merged[f"GIT_CONFIG_KEY_{i}"], merged[f"GIT_CONFIG_VALUE_{i}"]) for i in range(1, 1 + len(SETTINGS))],
        )
        self.assertEqual(merged, quiet_git_env(merged))
        self.assertEqual(base["GIT_CONFIG_COUNT"], "1", "the input is not changed")


if __name__ == "__main__":
    unittest.main()
