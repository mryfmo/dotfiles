"""Exercise task-from-plan.py on a committed fixture plan group in a temporary repository with a bare origin.

The fixture also commits the task records the a01 generator needed (a row template and a Completion file), so each
regression below is red against that generator for the reason it names; the a02 generator reads none of them.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts/orchestrator/task-from-plan.py"
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
PROGRAMS = ".orchestration/plans/024-design-programs.md"
WAVES = ".orchestration/plans/024-omp-cutover-and-corrective-order.md"
LEGACY_ROWS = (
    "the task-file copy on the branch (.orchestration/dotfiles-T133-result-precheck-a01/task.md)",
    "the branch evidence records under .orchestration/dotfiles-T133-result-precheck-a01/ (report.md, validation.md)",
    "task metadata (the front matter of the task copy)",
    "metadata separators (the --- lines)",
    "in-process effects",
    "workflow and interpreter or environment inputs",
    "new or renamed scripts",
    "orchestrator effect merge",
    "orchestrator effect update-branch",
    "orchestrator effect forced worker removal",
)
LEGACY = {  # what the a01 generator read under .orchestration/tasks/; the a02 generator reads none of it
    ".orchestration/tasks/dotfiles-T133-result-precheck-a01.md": "---\nformat: 2\nthreat_table:\n"
    + "".join(
        f"  - control: {json.dumps(c)}\n    disposition: {json.dumps('residual: the legacy wording of ' + c)}\n"
        for c in LEGACY_ROWS
    )
    + "---\n",
    ".orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md": "---\nformat: 2\n---\n\n## Completion\n\nOne PR.\n",
}
FILES = {
    ".orchestration/plans/024-todo.md": "| # | 目的 | やること | 完了条件 |\n| --- | --- | --- | --- |\n"
    "| P1-1 demo generator | B1 a demo purpose | (1) で作る | the generated task passes the consistency check |\n",
    PROGRAMS: "# programs\n\n**(1) `scripts/demo.sh`**: prints `printf known-output` and checks `sh -c 'exit 3'`.\n\n"
    "**(2) other**: unused\n",
    ".orchestration/plans/024-design-quality.md": "| id | row |\n| --- | --- |\n| Q-A 境界 | P1-1 のタスクは security: true |\n",
    WAVES: "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n| P-W0 | P1-1 demo | P1-2 sibling |\n\n## 7. STOP\n",
    "scripts/demo.sh": "#!/usr/bin/env bash\necho demo\n",
    "tests/unit/test_demo.py": "# exercises scripts/demo.sh\n",
    "Makefile": "unit-test:\n\t@true\n",
    **LEGACY,
}
LOAD = "import json, sys, yaml; print(json.dumps(yaml.safe_load(sys.stdin.read().split('\\n---\\n', 1)[0].lstrip('-\\n'))))"


class TaskFromPlanTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.env = {**os.environ, **GIT_ENV, "TMPDIR": temp.name}
        self.commit(FILES, "init", init=True)

    def git(self, *args):
        run = ["git", "-c", "commit.gpgsign=false", *args]
        return subprocess.run(run, cwd=self.repo, env=self.env, capture_output=True, text=True, check=True).stdout

    def commit(self, files, message, init=False):
        """Write and commit files; the first commit also creates the bare origin (make unit-test has no PyYAML)."""
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        if init:
            self.git("init", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        if init:
            self.git("init", "-q", "--bare", str(self.temp / "origin.git"))
            self.git("remote", "add", "origin", str(self.temp / "origin.git"))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")

    def generate(self, *args, todo="P1-1", out=".orchestration/tasks/dotfiles-T9-demo-a01.md"):
        """Run the generator; return (exit, stdout + stderr, front matter or None, text or "")."""
        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I"]
        result = subprocess.run(
            [*run, str(GENERATOR), todo, "--out", out, *args],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        if not (self.repo / out).is_file():
            return result.returncode, result.stdout + result.stderr, None, ""
        text = (self.repo / out).read_text()
        front = json.loads(
            subprocess.run([*run, "-c", LOAD], input=text, capture_output=True, text=True, check=True).stdout
        )
        return result.returncode, result.stdout + result.stderr, front, text

    def test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs(self):
        code, out, front, text = self.generate("--seat", "a009")
        self.assertEqual(code, 0, out)
        self.assertEqual(out.splitlines()[0], "dotfiles-T9-demo-a01.md: OK")
        self.assertIs(front["security"], True)
        allowed = ["scripts/demo.sh", "tests/unit/test_demo.py", ".orchestration/dotfiles-T9-demo-a01/**"]
        self.assertEqual(front["allowed_files"], allowed)
        first, second = front["premises"]
        self.assertEqual((first["command"], first["output"]), ("printf known-output", "known-output"))
        self.assertEqual(second["command"], "sh -c 'exit 3'")
        self.assertTrue(second["claim"].startswith("verify:") and "exits 3" in second["claim"], second)
        self.assertIn("# from: tests/unit/test_demo.py (git grep -l demo.sh)", text)
        head = self.git("rev-parse", "origin/main").strip()
        self.assertIn(f"- `make unit-test`: exit 0 on origin/main {head[:12]}", text)
        self.assertIn("`dotfiles-T9-demo-a01-followup-a01`", text)
        controls = [r["control"] for r in front["threat_table"]]
        self.assertIn("the task-file copy on the branch (.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
        self.assertNotIn("dotfiles-T133-result-precheck-a01", text)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)  # the scratch worktree is gone

    def test_generator_uses_the_bundled_template_without_task_records(self):
        # The audit of 9da0ed3 (P1, item 5): the generator's rows, Check defaults and Completion come from
        # scripts/orchestrator/task-template.md; a checkout without .orchestration/tasks/ generates a passing task.
        self.git("rm", "-q", "-r", ".orchestration/tasks")
        self.commit({}, "no task records")
        code, out, front, text = self.generate()
        self.assertEqual(code, 0, out)
        controls = " || ".join(r["control"] for r in front["threat_table"])
        for name in ("task metadata", "metadata separators", "in-process effects", "orchestrator effect merge"):
            self.assertIn(name, controls)
        self.assertIn("(.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
        self.assertIn("- `make format`: exit ", text)
        self.assertIn("owned by `dotfiles-T9-demo-a01-followup-a01`", text)
        self.assertIn("`task_copy=<sha256 of .orchestration/dotfiles-T9-demo-a01/task.md>`", text)

    def test_generator_refuses_dirty_plan_commands_before_execution(self):
        # The audit of 9da0ed3 (P1, item 6): plan commands run only from a clean, committed 024-* plan group.
        marker = self.temp / "ran"
        program = FILES[PROGRAMS].replace("`printf known-output`", f"`touch {marker}`")
        self.commit({PROGRAMS: program}, "a marker command")
        for dirty in ("unstaged", "staged", "untracked"):
            with self.subTest(dirty=dirty):
                rel = ".orchestration/plans/024-extra.md" if dirty == "untracked" else PROGRAMS
                (self.repo / rel).write_text(program + "\nan uncommitted line\n")
                if dirty == "staged":
                    self.git("add", rel)
                code, out, front, _ = self.generate()
                self.assertEqual((code != 0, marker.exists(), front), (True, False, None), out)
                self.assertIn("uncommitted", out)
                self.git("reset", "-q", "--hard")
                (self.repo / ".orchestration/plans/024-extra.md").unlink(missing_ok=True)
        code, out, front, text = self.generate()
        self.assertEqual((code, marker.exists()), (0, True), out)
        self.assertIn(f"plan group at {self.git('rev-parse', 'HEAD').strip()}", text)

    def test_wave_selection_matches_whole_todo_ids(self):
        # The audit of 9da0ed3 (P2, item 12): P1-1 is a whole id in the seat's column; P1-10 or P1-11 never matches it.
        waves = "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n| P-W0 | P1-10, P1-11 | P1-12 |\n"
        self.commit({WAVES: waves + "| P-W1 | P1-1 | |\n\n## 7. STOP\n"}, "two waves")
        code, out, _, text = self.generate("--seat", "a009")
        self.assertEqual(code, 0, out)
        self.assertIn("wave P-W1", text)
        self.assertIn("seat a009", text)
        self.assertNotIn("P-W0", text)

    def test_generator_preserves_wildcard_scopes_and_their_threat_rows(self):
        # The audit of 9da0ed3 (P2, item 13): `scripts/*.py` and `home/dot_config/**` stay scopes, and every applied file
        # they match gets its concrete row, so the generated task passes C4 and C12.
        program = FILES[PROGRAMS].replace(
            "`scripts/demo.sh`**", "`scripts/demo.sh`**, `scripts/*.py`, `home/dot_config/**`"
        )
        self.commit({PROGRAMS: program, "scripts/tool.py": "print(1)\n", "home/dot_config/x.toml": "a = 1\n"}, "scopes")
        code, out, front, _ = self.generate()
        self.assertEqual(code, 0, out)
        self.assertTrue({"scripts/*.py", "home/dot_config/**"} <= set(front["allowed_files"]), front["allowed_files"])
        controls = " || ".join(r["control"] for r in front["threat_table"])
        for name in ("scripts/*.py", "home/dot_config/**", "scripts/tool.py", "home/dot_config/x.toml"):
            self.assertIn(name, controls)

    def test_program_item_continues_until_the_next_numbered_heading(self):
        # The audit of 9da0ed3 (P2, item 14): a blank line or a fenced block does not end item (1); item (2) does.
        item = "\n\n```\n{schema: x}\n```\n\nThen `scripts/late.sh` runs `printf late-output`.\n\n"
        program = FILES[PROGRAMS].replace("\n\n**(2) other**: unused", item + "**(2) other**: `printf other-item`")
        self.commit({PROGRAMS: program, "scripts/late.sh": "echo late\n"}, "a longer item")
        code, out, front, _ = self.generate()
        self.assertEqual(code, 0, out)
        self.assertIn("scripts/late.sh", front["allowed_files"])
        commands = [p["command"] for p in front["premises"]]
        self.assertIn("printf late-output", commands)
        self.assertNotIn("printf other-item", commands)

    def test_generator_retains_unavailable_single_word_and_redirecting_commands(self):
        # The audit of 9da0ed3 (P2, item 15): a span is a command by its form, not by an executable existing now; the
        # same rule picks the item's `make` targets for the Check.
        written, check = self.temp / "written", self.temp / "check.out"
        spans = f"`no-such-tool-a02 --list`, `pwd`, `printf hi > {written}` and `make unit-test > {check}`"
        self.commit({PROGRAMS: FILES[PROGRAMS].replace("`sh -c 'exit 3'`", spans)}, "command forms")
        code, out, front, text = self.generate()
        self.assertEqual(code, 0, out)
        premises = {p["command"]: p for p in front["premises"]}
        self.assertTrue({"no-such-tool-a02 --list", "pwd", f"printf hi > {written}"} <= set(premises), premises)
        self.assertTrue(premises["no-such-tool-a02 --list"]["claim"].startswith("verify:"), premises)
        self.assertIn("exits 127", premises["no-such-tool-a02 --list"]["claim"])
        self.assertEqual(premises["pwd"]["output"], str(self.repo))
        self.assertEqual((premises[f"printf hi > {written}"]["output"], written.read_text()), ("", "hi"))
        self.assertIn(f"- `make unit-test > {check}`: exit 0 on origin/main", text)
        self.assertNotIn(f"make unit-test > {check}", premises)


if __name__ == "__main__":
    unittest.main()
