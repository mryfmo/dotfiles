"""Exercise task-from-plan.py on a fixture plan group in a temporary repository whose origin is a bare repository."""

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
TEMPLATE_ROWS = (
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
FILES = {
    ".orchestration/plans/024-todo.md": "| # | 目的 | やること | 完了条件 |\n| --- | --- | --- | --- |\n"
    "| P1-1 demo generator | B1 a demo purpose | (1) で作る | the generated task passes the consistency check |\n",
    ".orchestration/plans/024-design-programs.md": "# programs\n\n**(1) `scripts/demo.sh`**: prints `printf known-output`"
    " and checks `sh -c 'exit 3'`.\n\n**(2) other**: unused\n",
    ".orchestration/plans/024-design-quality.md": "| id | row |\n| --- | --- |\n| Q-A 境界 | P1-1 のタスクは security: true |\n",
    ".orchestration/plans/024-omp-cutover-and-corrective-order.md": "## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n"
    "| P-W0 | P1-1 demo | P1-2 sibling |\n\n## 7. STOP\n",
    ".orchestration/tasks/dotfiles-T1-sibling-a01.md": "---\nformat: 2\n---\n\n# AGMSG-TASK dotfiles-T1-sibling-a01 — sibling"
    " (plan 024 P1-2)\n\n## Check\n\n`printf check-ran` and `make unit-test`.\n\n## Completion\n\nDone.\n",
    ".orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md": "---\nformat: 2\n---\n\n## Completion\n\nOne PR.\n",
    "scripts/demo.sh": "#!/usr/bin/env bash\necho demo\n",
    "tests/unit/test_demo.py": "# exercises scripts/demo.sh\n",
    "Makefile": "unit-test:\n\t@true\n",
}


class TaskFromPlanTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve() / "repo"
        self.env = {**os.environ, **GIT_ENV, "TMPDIR": temp.name}
        # make unit-test runs without PyYAML, so the fixture's YAML is written by hand and read back through uv.
        rows = "".join(
            f"  - control: {json.dumps(c)}\n    disposition: {json.dumps('residual: the wording of ' + c)}\n"
            for c in TEMPLATE_ROWS
        )
        template = f"---\nformat: 2\nthreat_table:\n{rows}---\n\n# template\n"
        for rel, text in {**FILES, ".orchestration/tasks/dotfiles-T133-result-precheck-a01.md": template}.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        self.git("init", "-q", "-b", "main")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "init")
        self.git("init", "-q", "--bare", str(Path(temp.name) / "origin.git"))
        self.git("remote", "add", "origin", str(Path(temp.name) / "origin.git"))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")

    def git(self, *args):
        run = ["git", "-c", "commit.gpgsign=false", *args]
        return subprocess.run(run, cwd=self.repo, env=self.env, capture_output=True, text=True, check=True).stdout

    def test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs(self):
        out = ".orchestration/tasks/dotfiles-T9-demo-a01.md"
        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I", str(GENERATOR), "P1-1"]
        result = subprocess.run(
            [*run, "--out", out, "--seat", "a009"],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.splitlines()[0], "dotfiles-T9-demo-a01.md: OK")
        text = (self.repo / out).read_text()
        load = "import json, sys, yaml; print(json.dumps(yaml.safe_load(sys.stdin.read().split('\\n---\\n', 1)[0].lstrip('-\\n'))))"
        front = json.loads(
            subprocess.run([*run[:6], "-c", load], input=text, capture_output=True, text=True, check=True).stdout
        )
        self.assertIs(front["security"], True)
        self.assertEqual(
            front["allowed_files"],
            ["scripts/demo.sh", "tests/unit/test_demo.py", ".orchestration/dotfiles-T9-demo-a01/**"],
        )
        first, second = front["premises"]
        self.assertEqual((first["command"], first["output"]), ("printf known-output", "known-output"))
        self.assertEqual(second["command"], "sh -c 'exit 3'")
        self.assertIn("verify:", second["claim"])
        self.assertIn("exits 3", second["claim"])
        self.assertIn("# from: tests/unit/test_demo.py (git grep -l demo.sh)", text)
        self.assertIn("- `printf check-ran` # exit 0 on origin/main", text)
        self.assertIn("(the Check commands of dotfiles-T1-sibling-a01.md)", text)
        self.assertIn("`dotfiles-T9-demo-a01-followup-a01`", text)
        controls = [r["control"] for r in front["threat_table"]]
        self.assertIn("the task-file copy on the branch (.orchestration/dotfiles-T9-demo-a01/task.md)", controls)
        self.assertNotIn("dotfiles-T133-result-precheck-a01", text)
        self.assertEqual(len(self.git("worktree", "list").splitlines()), 1)  # the scratch worktree is gone
        # A checkout without the regime's records (here the row template) is refused by name before anything is written.
        (self.repo / ".orchestration/tasks/dotfiles-T133-result-precheck-a01.md").unlink()
        other = ".orchestration/tasks/dotfiles-T9-other-a01.md"
        refused = subprocess.run(
            [*run, "--out", other], cwd=self.repo, env=self.env, capture_output=True, text=True, check=False
        )
        self.assertEqual((refused.returncode, refused.stdout), (1, ""), refused.stderr)
        self.assertIn(".orchestration/tasks/dotfiles-T133-result-precheck-a01.md", refused.stderr)
        self.assertNotIn("Traceback", refused.stderr)
        self.assertFalse((self.repo / other).exists())


if __name__ == "__main__":
    unittest.main()
