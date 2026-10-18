"""Exercise C11 to C15 of task-consistency-check.py: one red fixture per check, and the current T133 task files.

The fixtures are task files in a temporary repository whose origin is a bare repository (C15 reads origin/main). The
checker runs through uv with PyYAML, which make unit-test does not provide to this process.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/orchestrator/task-consistency-check.py"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
NONPATH = "".join(
    f'  - control: {name}\n    disposition: "residual: the fixture\'s control for {name}"\n'
    for name in (
        "metadata separators",
        "in-process effects",
        "workflow and interpreter or environment inputs",
        "new or renamed scripts",
        "orchestrator effect merge",
        "orchestrator effect update-branch",
        "orchestrator effect forced worker removal",
    )
)
BASE = f"""---
format: 2
task_id: dotfiles-T9-base-a01
kind: code
allowed_files:
  - scripts/tool.py
  - .orchestration/dotfiles-T9-base-a01/**
design_review:
  receipt: r1
  design: .orchestration/tasks/dotfiles-T9-design-a01.md
invariants:
  INV-1: "the tool prints one line per finding"
threat_table:
  - control: "scripts/tool.py (the tool)"
    disposition: "closed: tests/unit/test_tool.py::test_tool_prints_findings"
  - control: "the evidence under .orchestration/dotfiles-T9-base-a01/ (report.md)"
    disposition: "residual: prose and pasted command output only"
  - control: task metadata
    disposition: "out-of-scope: dotfiles-T9-design-a01"
  - control: "scripts/a.sh (the one file of the glob fixture a row names)"
    disposition: "residual: a fixture row for the C12 case"
{NONPATH}premises:
  - claim: the fixture's premise prints base
    command: printf base
    output: |-
      base
---

# AGMSG-TASK dotfiles-T9-base-a01 — the fixture
"""
DESIGN = '---\nformat: 2\ninvariants:\n  INV-1: "the tool prints one line per finding"\n---\n\n# design\n'
CASES = {
    "C11": (
        '"closed: tests/unit/test_tool.py::test_tool_prints_findings"',
        '"closed: tests/unit/test_tool.py::two words"',
    ),
    "C12": ("  - scripts/tool.py\n", "  - scripts/tool.py\n  - scripts/*.sh\n"),
    "C13": ('"residual: prose and pasted command output only"', '"accepted: prose and pasted command output only"'),
    "C14": ("      base\n---", "      edited\n---"),
    "C15": ('INV-1: "the tool prints one line per finding"', 'INV-1: "the tool prints one line per run"'),
}


class TaskConsistencyC11C15Test(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve() / "repo"
        env = {**os.environ, **GIT_ENV}
        files = {
            ".orchestration/tasks/dotfiles-T9-design-a01.md": DESIGN,
            "scripts/tool.py": "print('tool')\n",
            "scripts/a.sh": "echo a\n",
            "scripts/b.sh": "echo b\n",
        }
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        bare = str(Path(temp.name) / "origin.git")
        for args in (
            ("init", "-q", "-b", "main"),
            ("add", "-A"),
            ("commit", "-q", "-m", "init"),
            ("init", "-q", "--bare", bare),
        ):
            subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=self.repo, env=env, check=True)
        for args in (("remote", "add", "origin", bare), ("push", "-q", "origin", "main"), ("fetch", "-q", "origin")):
            subprocess.run(["git", *args], cwd=self.repo, env=env, check=True)

    def check(self, *tasks, root=None):
        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I", str(CHECKER)]
        result = subprocess.run(
            [*run, "--root", str(root or self.repo), *map(str, tasks)], capture_output=True, text=True
        )
        return result.returncode, result.stdout

    def task(self, text):
        path = self.repo / ".orchestration/tasks/dotfiles-T9-base-a01.md"
        path.write_text(text)
        return path

    def test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged(self):
        code, out = self.check(self.task(BASE))
        self.assertEqual((code, out), (0, "dotfiles-T9-base-a01.md: OK\n"))
        for check, (old, new) in CASES.items():
            with self.subTest(check=check):
                self.assertEqual(BASE.count(old), 1)
                code, out = self.check(self.task(BASE.replace(old, new)))
                findings = out.splitlines()[1:]
                self.assertEqual(code, 1, out)
                self.assertEqual(len(findings), 1, out)
                self.assertTrue(findings[0].strip().startswith(check + " "), out)
        # Amendment 1: C14 collapses whitespace runs (a padded count equals its pasted number) and warns on an absent tool.
        padded = BASE.replace(
            "command: printf base\n    output: |-\n      base", "command: printf '%8s' 1\n    output: |-\n      1"
        )
        self.assertEqual(self.check(self.task(padded)), (0, "dotfiles-T9-base-a01.md: OK\n"))
        for cmd in ("no-such-tool-a01 --list", "no-such-tool-a01 --help | /usr/bin/grep -c x"):
            code, out = self.check(self.task(BASE.replace("command: printf base", f"command: {cmd}")))
            self.assertEqual(code, 0, out)
            self.assertIn("C14: tool absent no-such-tool-a01", out)
        current = sorted((ROOT / ".orchestration/tasks").glob("dotfiles-T133-*.md"))
        with self.subTest(green="the current dotfiles-T133 task files"):
            if not current:
                self.skipTest("no dotfiles-T133 task file in this tree yet (they land with a boundary records PR)")
            code, out = self.check(*current, root=ROOT)
            others = [l for l in out.splitlines() if l.startswith("  ") and not l.strip().startswith("C14")]
            # C14 reruns write-time premises, so the current set is held to C1 to C13 and C15.
            self.assertEqual(others, [], out)


if __name__ == "__main__":
    unittest.main()
