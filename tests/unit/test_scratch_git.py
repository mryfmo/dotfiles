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
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import SETTINGS, git_clone, git_init, quiet_git, quiet_git_env  # noqa: E402

quiet_git()  # U100: no git command in this module's scratch repositories starts background maintenance

HERE = Path(__file__).resolve().parent
# A git command whose subcommand is init: ["git", …, "init"], git(…"init"), self.git("init"), and ("init", "-…") argv.
INIT = re.compile(r"""(\bgit\b[^\n]{0,160}?["']init["'])|(\(\s*\(?["']init["'],\s*["']-)|(\[\s*["']init["'],)""")
IDENTITY = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
# The git init/clone call sites in tests/unit that do not go through scratch_git's git_init/git_clone, each with why.
RAW_REPOSITORY_SITES = {
    ("test_scratch_git.py", 'self.git("init", "-q", env=env)'): (
        "raw_init: the environment-layer tests need a repository without the settings in its own config"
    ),
}
SUBCOMMANDS = {"init", "clone"}
MESSAGE = {"-m", "-qm", "--message"}


def calls_quiet_git_at_module_level(tree: ast.Module) -> bool:
    return any(
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "quiet_git"
        for node in tree.body
    )


def repository_sites(tree: ast.Module):
    """Line numbers of the `init`/`clone` literals a git command takes as its subcommand: an argument of a call whose
    name holds `git` (self.git, git, self._git), or an element of an argv list or tuple that starts with it or
    follows "git" or a starred prefix ([*git, "init"]). A literal after -m is a commit message."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
            if "git" not in name.lower() or name in ("git_init", "git_clone"):
                continue
            elements, git_call = node.args, True
        elif isinstance(node, (ast.List, ast.Tuple)):
            elements, git_call = node.elts, False
        else:
            continue
        for index, element in enumerate(elements):
            if not (isinstance(element, ast.Constant) and element.value in SUBCOMMANDS):
                continue
            before = elements[:index]
            if any(isinstance(e, ast.Constant) and e.value in MESSAGE for e in before):
                continue
            led = any(isinstance(e, ast.Starred) or (isinstance(e, ast.Constant) and e.value == "git") for e in before)
            if git_call or index == 0 or led:
                yield element.lineno


class ScratchGitTest(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="scratch-git-test-"))
        self.addCleanup(shutil.rmtree, self.repo, True)
        # No GIT_CONFIG_* entry and no config file: what an env built from scratch, or stripped by a script, carries.
        self.stripped = {"PATH": os.environ["PATH"], "HOME": str(self.repo), "GIT_CONFIG_NOSYSTEM": "1"}
        self.stripped["GIT_CONFIG_GLOBAL"] = os.devnull

    def git(self, *args: str, env: dict | None = None, cwd: Path | None = None) -> str:
        return subprocess.run(
            ["git", "-C", str(cwd or self.repo), "-c", "commit.gpgsign=false", *args],
            env=(os.environ if env is None else env) | IDENTITY,
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        ).stdout.strip()

    def raw_init(self, env: dict) -> None:
        self.git("init", "-q", env=env)

    def test_every_module_that_creates_a_git_repository_quiets_git(self):
        # PR #559: test_pinned_lint_tools committed, git's detached auto maintenance held maintenance.lock, and the
        # test's rmtree failed. Every module that creates a repository calls quiet_git() at module level.
        missing = []
        for path in sorted(HERE.glob("test_*.py")):
            text = path.read_text()
            if INIT.search(text) and not calls_quiet_git_at_module_level(ast.parse(text)):
                missing.append(path.name)
        self.assertEqual([], missing)

    def test_every_git_init_and_clone_goes_through_git_init_or_git_clone(self):
        # The repository then carries the settings in its own config, so no env a later git runs under can drop them.
        raw, seen = [], set()
        for path in sorted(HERE.glob("*.py")):
            if path.name == "scratch_git.py":
                continue
            text = path.read_text()
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)  # a module's own escape sequences are not this test's
                tree = ast.parse(text)
            lines = text.splitlines()
            for lineno in repository_sites(tree):
                site = (path.name, lines[lineno - 1].strip())
                (seen.add if site in RAW_REPOSITORY_SITES else raw.append)(site)
        self.assertEqual([], raw)
        self.assertEqual(set(RAW_REPOSITORY_SITES), seen, "every listed site still exists")

    def test_the_sweep_finds_each_call_form(self):
        forms = (
            'subprocess.run(["git", "init", "-q", str(repo)])',
            'subprocess.run([*git, "init", "-q"])',
            'self.git("init", "-q")',
            'git("clone", "-q", str(origin), str(clone), cwd=temp)',
            'self._git(repo, "init", "-q")',
            'for args in (("init", "-q"), ("add", ".")): git(*args)',
            'for args in (["init", "-q"], ["commit", "-m", "init"]): run(["git", *args])',
        )
        for form in forms:
            with self.subTest(form):
                self.assertEqual([1], list(repository_sites(ast.parse(form))))
        for message in (
            'self.git("commit", "-q", "-m", "init")',
            'git_init(repo, "-b", "main")',
            '("chezmoi", "init")',
        ):
            with self.subTest(message):
                self.assertEqual([], list(repository_sites(ast.parse(message))))

    def test_a_repository_from_git_init_or_git_clone_carries_the_settings_under_any_env(self):
        # The leaks the audit of 87d13808 found: test_sandbox_portability's repo_with() env and test_hcom_seat's signing
        # test both run git with no GIT_CONFIG_* entry of these settings. The repository's own config still has them.
        repositories = {
            "work tree": git_init(self.repo / "work"),
            "bare": git_init(self.repo / "origin.git", "--bare", "-b", "main"),
            "separate git dir": git_init(self.repo / "checkout", f"--separate-git-dir={self.repo / 'gitdir'}"),
        }
        repositories["clone"] = git_clone(self.repo / "origin.git", self.repo / "clone")
        for kind, path in repositories.items():
            for key, value in SETTINGS:
                with self.subTest(kind=kind, key=key):
                    self.assertEqual(value, self.git("config", "--local", "--get", key, env=self.stripped, cwd=path))
        # Without the settings, git 2.56 left maintenance.lock behind a commit in 187 of 200 fresh repositories.
        work = repositories["work tree"]
        for number in range(5):
            (work / "file").write_text(f"{number}\n")
            self.git("add", "-A", env=self.stripped, cwd=work)
            self.git("commit", "-q", "-m", str(number), env=self.stripped, cwd=work)
            self.assertFalse((work / ".git/objects/maintenance.lock").exists(), number)

    def test_an_env_built_from_scratch_carries_the_settings(self):
        env = quiet_git_env(self.stripped)
        self.raw_init(env)
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

    def test_the_settings_win_over_earlier_entries_of_the_same_keys(self):
        # Git takes a key's last value. An env that already holds the four keys, `true` after a `false` of the
        # settings themselves, still ends with the settings in effect.
        earlier = [("commit.gpgsign", "false"), *SETTINGS, ("maintenance.auto", "true"), ("gc.auto", "1")]
        earlier += [("maintenance.autoDetach", "true"), ("gc.autoDetach", "true")]
        base = dict(self.stripped, GIT_CONFIG_COUNT=str(len(earlier)))
        for index, (key, value) in enumerate(earlier):
            base |= {f"GIT_CONFIG_KEY_{index}": key, f"GIT_CONFIG_VALUE_{index}": value}
        self.raw_init(self.stripped)
        self.assertEqual("true", self.git("config", "--get", "maintenance.auto", env=base), "the override is live")
        merged = quiet_git_env(base)
        entries = [(merged[f"GIT_CONFIG_KEY_{i}"], merged[f"GIT_CONFIG_VALUE_{i}"]) for i in range(len(earlier))]
        self.assertEqual(earlier, entries, "the entries already there stay first, unchanged")
        for env in (merged, quiet_git_env(merged)):
            for key, value in SETTINGS:
                with self.subTest(count=env["GIT_CONFIG_COUNT"], key=key):
                    self.assertEqual(value, self.git("config", "--get", key, env=env))
        self.assertEqual(str(len(earlier)), base["GIT_CONFIG_COUNT"], "the input is not changed")


if __name__ == "__main__":
    unittest.main()
