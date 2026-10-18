"""Exercise C11 to C15 of task-consistency-check.py: one red fixture per check, and the current T133 task files.

The fixtures are task files in a temporary repository whose origin is a bare repository (C15 reads origin/main). The
checker runs through uv with PyYAML, which make unit-test does not provide to this process.
"""

import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts/orchestrator/task-consistency-check.py"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
UNTRUSTED = "dotfiles-T9-base-a01.md: warning: C14: not run (no trusted sha)\n"  # the checker's stderr line
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

    def check(self, *tasks, root=None, sha=True):
        """Run the checker; `sha` True passes the first file's sha256 as --premises-sha, as for the dispatched text."""
        if sha is True:
            sha = hashlib.sha256(Path(tasks[0]).read_bytes()).hexdigest()
        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I", str(CHECKER)]
        trusted = ["--premises-sha", sha] if sha else []
        result = subprocess.run(
            [*run, "--root", str(root or self.repo), *trusted, *map(str, tasks)],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout + result.stderr

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
            # stdout holds the verdict alone; the warning is stderr's, so no finding parser reads it.
            warning = (
                "dotfiles-T9-base-a01.md: OK\ndotfiles-T9-base-a01.md: warning: C14: tool absent no-such-tool-a01: "
            )
            self.assertTrue(out.startswith(warning), out)
        current = sorted((ROOT / ".orchestration/tasks").glob("dotfiles-T133-*.md"))
        with self.subTest(green="the current dotfiles-T133 task files"):
            if not current:
                self.skipTest("no dotfiles-T133 task file in this tree yet (they land with a boundary records PR)")
            code, out = self.check(*current, root=ROOT, sha=None)
            others = [l for l in out.splitlines() if l.startswith("  ") and not l.strip().startswith("C14")]
            # Without a trusted sha C14 runs nothing, so the current set is held to C1 to C13 and C15.
            self.assertEqual(others, [], out)

    def test_c14_executes_premise_commands_only_for_the_dispatched_sha(self):
        # Revise 1 (the Bot's P1 4306960622): a premise command runs only when the file is the orchestrator's dispatched
        # text, whose sha256 the caller passes; for any other file C14 notes it and executes nothing.
        marker = self.repo / "marker"
        path = self.task(BASE.replace("command: printf base", f"command: touch {marker}; printf base"))
        for sha in (None, "0" * 64):
            with self.subTest(sha=sha):
                code, out = self.check(path, sha=sha)
                self.assertEqual((code, marker.exists()), (0, False), out)
                self.assertEqual(out, f"dotfiles-T9-base-a01.md: OK\n{UNTRUSTED}")
        self.assertEqual(self.check(path), (0, "dotfiles-T9-base-a01.md: OK\n"))
        self.assertTrue(marker.exists())
        marker.unlink()
        edited = self.task(BASE.replace("command: printf base", f"command: touch {marker}; printf edited"))
        code, out = self.check(edited)
        self.assertEqual((code, marker.exists()), (1, True), out)
        self.assertIn("C14 premise output differs from its rerun", out)

    def publish(self, files):
        """Commit files and push them, so origin/main carries them as C10, C12 and C15 read it."""
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        for args in (("add", "-A"), ("commit", "-q", "-m", "publish"), ("push", "-q", "origin", "main")):
            subprocess.run(
                ["git", "-c", "commit.gpgsign=false", *args], cwd=self.repo, env={**os.environ, **GIT_ENV}, check=True
            )
        subprocess.run(["git", "fetch", "-q", "origin"], cwd=self.repo, check=True)

    def test_c14_without_a_trusted_sha_reports_an_explicit_warning(self):
        # The audit of 9da0ed3 (P2, item 8): with no trusted sha C14 runs nothing and says so as a warning, so a
        # structural OK is never read as premises that passed.
        marker = self.repo / "marker"
        path = self.task(BASE.replace("command: printf base", f"command: touch {marker}; printf base"))
        code, out = self.check(path, sha=None)
        self.assertEqual((code, marker.exists(), out), (0, False, f"dotfiles-T9-base-a01.md: OK\n{UNTRUSTED}"))

    def test_c15_requires_the_design_assigned_invariant_id_set(self):
        # The audit of 9da0ed3 (P2, item 9): the design's implementing_tasks fixes the task's invariant ids, so an
        # omitted map, a missing or an extra id is a finding as much as a changed sentence.
        one, two = '"the tool prints one line per finding"', '"the tool exits 1 on a finding"'
        design = (
            f"implementing_tasks:\n  dotfiles-T9-base-a01: [INV-1, INV-2]\ninvariants:\n  INV-1: {one}\n  INV-2: {two}"
        )
        self.publish({".orchestration/tasks/dotfiles-T9-design-a01.md": f"---\nformat: 2\n{design}\n---\n\n# design\n"})
        block, d = f"invariants:\n  INV-1: {one}\n", ".orchestration/tasks/dotfiles-T9-design-a01.md"
        missing = f"C15 invariant {{}} that {d} assigns to dotfiles-T9-base-a01 is missing"
        cases = {
            "only INV-1": (block, [missing.format("INV-2")]),
            "no map": ("", [missing.format("INV-1"), missing.format("INV-2")]),
            "an extra id": (
                block + f"  INV-2: {two}\n  INV-3: {two}\n",
                [f"C15 invariant INV-3 is not one {d} assigns to dotfiles-T9-base-a01"],
            ),
            "a changed sentence": (
                block + '  INV-2: "the tool exits 2"\n',
                [f"C15 invariant INV-2 is not byte-equal to {d} on origin/main"],
            ),
            "the whole assignment": (block + f"  INV-2: {two}\n", []),
        }
        for name, (invariants, want) in cases.items():
            with self.subTest(case=name):
                _, out = self.check(self.task(BASE.replace(block, invariants)))
                self.assertEqual([l.strip() for l in out.splitlines() if l.strip().startswith("C15")], want, out)

    def test_c12_classifies_concrete_glob_matches_before_the_glob_spelling(self):
        # The audit of 9da0ed3 (P2, items 10 and 19): install/** spells no applied kind, but the shell script it matches
        # is executed, so it needs its concrete row; a tests/fixtures/ glob stays exempt.
        self.publish({"install/setup.sh": "echo setup\n", "tests/fixtures/x/run.sh": "echo x\n"})
        rows = '  - control: "install/** (the installers)"\n    disposition: "residual: the C12 case\'s glob entry"\n'
        rows += (
            '  - control: "tests/fixtures/x/** (fixtures)"\n    disposition: "residual: the C12 case\'s exempt glob"\n'
        )
        task = BASE.replace("  - scripts/tool.py\n", "  - scripts/tool.py\n  - install/**\n  - tests/fixtures/x/**\n")
        task = task.replace("threat_table:\n", "threat_table:\n" + rows)
        code, out = self.check(self.task(task))
        self.assertEqual(
            (code, out.splitlines()[1:]),
            (1, ["  C12 the glob install/** matches install/setup.sh, which no threat_table row names"]),
        )
        named = '  - control: "install/setup.sh (the setup script)"\n    disposition: "residual: the C12 case\'s concrete row"\n'
        self.assertEqual(
            self.check(self.task(task.replace("threat_table:\n", "threat_table:\n" + named))),
            (0, "dotfiles-T9-base-a01.md: OK\n"),
        )

    def test_c10_never_passes_a_literal_as_a_git_grep_option(self):
        # PR #418's review (item 20): a backticked literal reaches git grep after -e, so `--open-files-in-pager=<cmd>` is
        # searched for and never run; the old call ran it as soon as the working tree held a match for origin/main.
        marker = self.repo.parent / "pager-ran"
        (self.repo / "scripts/tool.py").write_text("print('origin/main')\n")
        literal = f"--open-files-in-pager=touch {marker}"
        rule = f'\nThe rule: "scripts/tool.py reads `{literal}` before every run of the gate".\n'
        _, out = self.check(self.task(BASE.replace("kind: code", "kind: docs") + rule))
        self.assertFalse(marker.exists(), out)
        self.assertIn(f"C10 rule sentence names scripts/tool.py beside the literal `{literal}`", out)

    def test_c6_confines_design_paths_to_the_checkout(self):
        # PR #418's review (item 20): a design path that leaves --root is a finding and is never opened.
        outside = self.repo.parent / "outside/design.md"
        outside.parent.mkdir()
        outside.write_text("---\ndesign_review:\n  receipt: r9-outside\n---\n")
        task = BASE.replace("design: .orchestration/tasks/dotfiles-T9-design-a01.md", "design: ../outside/design.md")
        _, out = self.check(self.task(task))
        self.assertIn("C6 design path ../outside/design.md is outside the checkout", out)
        self.assertNotIn("r9-outside", out)


if __name__ == "__main__":
    unittest.main()
