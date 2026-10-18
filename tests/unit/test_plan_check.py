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
        result = subprocess.run(
            [*run, "--root", str(self.root), *args], env=self.env, capture_output=True, text=True, check=False
        )
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
        with self.subTest(rule="F2 glob"):  # a glob entry overlaps the literal path it matches, named concretely
            self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", "scripts/*.py")
            want = "F2 024-omp-cutover-and-corrective-order.md:11 P-W0 P1-1 and P1-2 share scripts/two.py"
            self.assertEqual(self.plan_check(), (1, [want]))

    def test_f2_detects_intersecting_globs_through_concrete_tree_matches(self):
        # The audit of 9da0ed3 (P2, item 11): two globs overlap through a file both match in the tree; their spellings
        # never decide disjointness.
        self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", "scripts/test_*.py")
        self.edit(".orchestration/tasks/dotfiles-T2-two-a01.md", "scripts/two.py", "scripts/*_check.py")
        (self.root / "scripts").mkdir()
        (self.root / "scripts/test_other.py").write_text("")
        self.assertEqual(self.plan_check(), (0, []))
        (self.root / "scripts/test_check.py").write_text("")
        want = "F2 024-omp-cutover-and-corrective-order.md:11 P-W0 P1-1 and P1-2 share scripts/test_check.py"
        self.assertEqual(self.plan_check(), (1, [want]))

    def test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task(self):
        # The audit of 9da0ed3 (P2, item 16): the task's latest event by timestamp decides, not the last textual match,
        # and another task's event never does.
        line = "[2026-10-18T{}:00:00Z] o → w: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-{}-a01 status={}\n"
        record = self.root / ".orchestration/acceptance/dotfiles-T1-one-a01.md"
        record.parent.mkdir(parents=True)
        events = (("05", "one", "accepted"), ("04", "one", "revise"), ("06", "other", "withdrawn"))
        # The pre-push review of eb20d063: each event of a two-event line has its own status, another task's coming
        # first included, and the untimed last line carries 07:00, so its event for one is the latest.
        two = "`AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-other-a01 status={}` `AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-one-a01 status={}`\n"
        shared = "[2026-10-18T07:00:00Z] " + two.format("withdrawn", "revise") + two.format("revise", "accepted")
        record.write_text("".join(line.format(*e) for e in events) + shared)
        progress = PLANS + "024-progress.tsv"
        self.edit(progress, "updated_jst\n", "updated_jst\ndotfiles-T1-one-a01\ttask\tone\taccepted\te\tt\n")
        self.assertEqual(self.plan_check("--drift"), (0, []))
        self.edit(progress, "\taccepted\t", "\trevise\t")
        want = "drift: 024-progress.tsv:2 dotfiles-T1-one-a01 revise != accepted"
        self.assertEqual(self.plan_check("--drift"), (1, [want]))

    def test_drift_checks_every_sha_and_state_for_each_pr_occurrence(self):
        # The audit of 9da0ed3 (P2, item 17): every sha and state near one #<pr> is compared on its own, so a matching
        # head never hides a conflicting state; association stops at the next #<pr>, so a repeated PR's second
        # occurrence carries its own sha and state assertions.
        self.edit(PLANS + "024-execution.md", "# x\n", "# x\n\n#77 abc1234 merged; #77 def4567 abc1234 CLEAN\n")
        code, lines = self.plan_check("--drift")
        live = "abc1234" + "0" * 5
        want = ["drift: 024-execution.md:3 #77 merged != OPEN", f"drift: 024-execution.md:3 #77 def4567 != {live}"]
        self.assertEqual((code, lines), (1, want))

    def test_invariants_reject_nonempty_quoted_oauth_token_assignments(self):
        # The audit of 9da0ed3 (P2, item 18): quoted and unquoted non-empty values are refused, an empty one is not, and
        # no diagnostic carries the value (built at run time).
        name, value = "ANTHROPIC_OAUTH_" + "TOKEN", "fixture-" + "x" * 8
        self.edit(
            PLANS + "024-execution.md",
            "# x\n",
            f'# x\n\n{name}="{value}"\n{name}=\'{value}\'\n{name}={value}\n{name}=""\n',
        )
        code, lines = self.plan_check("--invariants")
        self.assertEqual(
            (code, lines), (1, [f"invariant: 024-execution.md:{n} {name} with a value" for n in (3, 4, 5)])
        )
        self.assertNotIn(value, "\n".join(lines))


if __name__ == "__main__":
    unittest.main()
