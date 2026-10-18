"""Exercise plan-check.py on a fixture plan group: a clean group passes and each rule's fixture fails with one line.

plan-check runs through uv with PyYAML; `gh` is a stub on PATH that answers the head written in its calls directory.
"""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN_CHECK = ROOT / "scripts/orchestrator/plan-check.py"
PLANS = ".orchestration/plans/"
GH = '#!/usr/bin/env bash\nprintf \'{"headRefOid":"%s","mergeStateStatus":"CLEAN","isDraft":false,"state":"OPEN"}\' "$(cat "$CALLS/head")"\n'


def task(tid, todo, path):
    return f"---\nformat: 2\nallowed_files:\n  - {path}\n  - .orchestration/{tid}/**\n---\n\n# AGMSG-TASK {tid} — x (plan 024 {todo})\n"


CLEAN = {
    PLANS + "024-todo.md": "| # | 目的 | やること | 完了条件 |\n| --- | --- | --- | --- |\n"
    "| P1-1 one | B1 x | (1) | the first done condition |\n| P1-2 two | M1 y | (2) | the second done condition |\n",
    PLANS + "024-design-mechanism.md": "| id | row |\n| --- | --- |\n| B1 | a bottleneck |\n",
    PLANS + "024-design-quality.md": "| id | row |\n| --- | --- |\n| M1 | a mechanism |\n",
    PLANS + "024-checklists.md": "| # | 確認 | 期待 |\n| --- | --- | --- |\n| DoD1 | `make unit-test` | green |\n",
    PLANS + "024-omp-cutover-and-corrective-order.md": "## 2. 決定\n\n| 決定 | 選択肢 | 既定値 |\n| --- | --- | --- |\n"
    "| D1 merge | (a) or (b) | **(a)** because |\n\n## 6. 波\n\n| 波 | a009 | a008 |\n| --- | --- | --- |\n"
    "| P-W0 | P1-1 | P1-2 (#77 at abc1234, dotfiles-T1-one-a01, D-024-01) |\n\n## 7. STOP\n",
    **{
        PLANS + f"024-{n}.md": "# x\n"
        for n in ("design", "design-programs", "design-prs", "design-evidence", "execution")
    },
    PLANS + "024-progress.tsv": "id\tkind\ttitle\tstate\tevidence\tupdated_jst\n",
    ".orchestration/decisions.tsv": "id\twhen\twhat\twhy\tbasis\tresult\nD-024-01\tt\tw\ty\tb\tdefault\n",
    ".orchestration/tasks/dotfiles-T1-one-a01.md": task("dotfiles-T1-one-a01", "P1-1", "scripts/one.py"),
    ".orchestration/tasks/dotfiles-T2-two-a01.md": task("dotfiles-T2-two-a01", "P1-2", "scripts/two.py"),
}
CASES = {
    "F1": (PLANS + "024-todo.md", "| the second done condition |", "|  |"),
    "F2": (".orchestration/tasks/dotfiles-T2-two-a01.md", "scripts/two.py", "scripts/one.py"),
    "F3": (PLANS + "024-todo.md", "| M1 y |", "| y |"),
    "F4": (PLANS + "024-checklists.md", "`make unit-test`", "make unit-test"),
    "F5": (PLANS + "024-omp-cutover-and-corrective-order.md", "**(a)** because", "(a) because"),
    "F6": (PLANS + "024-execution.md", "# x\n", "# x, see dotfiles-T3-missing-a01\n"),
}


class PlanCheckTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root, self.calls, bin_dir = (Path(temp.name).resolve() / d for d in ("root", "calls", "bin"))
        for directory in (self.calls, bin_dir):
            directory.mkdir()
        (bin_dir / "gh").write_text(GH)
        (bin_dir / "gh").chmod(0o755)
        (self.calls / "head").write_text("abc1234" + "0" * 33)
        self.env = {**os.environ, "CALLS": str(self.calls), "STUB_BIN": str(bin_dir)}
        for rel, text in CLEAN.items():
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.root / rel).write_text(text)

    def plan_check(self, *args):
        # uv run puts its base interpreter's bin directory before PATH (Homebrew's on the macOS runner, which holds a
        # real gh), so the stub goes first inside uv run, as in test_task_checkers.py.
        stub_first = ["sh", "-c", 'PATH="$STUB_BIN:$PATH" exec python -I "$@"', "sh"]
        run = [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", *stub_first, str(PLAN_CHECK)]
        result = subprocess.run([*run, "--root", str(self.root), *args], env=self.env, capture_output=True, text=True)
        return result.returncode, result.stdout.splitlines()

    def edit(self, rel, old, new):
        text = (self.root / rel).read_text()
        self.assertEqual(text.count(old), 1, old)
        (self.root / rel).write_text(text.replace(old, new))
        self.addCleanup((self.root / rel).write_text, text)

    def test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan(self):
        self.assertEqual(self.plan_check("--drift", "--invariants"), (0, []))
        for rule, (rel, old, new) in CASES.items():
            with self.subTest(rule=rule):
                text = (self.root / rel).read_text()
                self.edit(rel, old, new)
                code, lines = self.plan_check()
                (self.root / rel).write_text(text)
                self.assertEqual(code, 1, lines)
                self.assertEqual(len(lines), 1, lines)
                self.assertTrue(lines[0].startswith(rule + " "), lines)
        with self.subTest(rule="drift"):
            (self.calls / "head").write_text("def4567" + "0" * 33)
            code, lines = self.plan_check("--drift")
            (self.calls / "head").write_text("abc1234" + "0" * 33)
            self.assertEqual((code, len(lines)), (1, 1), lines)
            self.assertRegex(lines[0], r"^drift: 024-omp-cutover-and-corrective-order\.md:\d+ #77 abc1234 != def4567")
        with self.subTest(rule="invariants"):
            self.edit(PLANS + "024-execution.md", "# x\n", "# x\n\nrun gh pr merge 77 --admin\n")
            code, lines = self.plan_check("--invariants")
            self.assertEqual((code, lines), (1, ["invariant: 024-execution.md:3 gh pr merge --admin or --auto"]))


if __name__ == "__main__":
    unittest.main()
