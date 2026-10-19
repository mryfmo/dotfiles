"""Exercise plan forms, drift, invariants and confined glob enumeration."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.unit.test_task_consistency_c11_c15 import fixture_cache, uv_command

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
    @classmethod
    def setUpClass(cls):
        fixture_cache()

    def test_globs_never_resolve_outside_root(self):
        outside = self.root.parent / "outside"
        outside.mkdir()
        (outside / "private-name.py").write_text("")
        (self.root / "linked").symlink_to(outside, target_is_directory=True)
        (self.root / "scripts").mkdir()
        (self.root / "internal").symlink_to(self.root / "scripts", target_is_directory=True)
        (self.root / "scripts/link.py").symlink_to(outside / "private-name.py")
        for pattern in (str(outside / "*.py"), "../outside/*.py", "linked/**/*.py", "internal/**/*.py", "scripts/*.py"):
            self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", pattern)
            code, lines = self.plan_check()
            self.assertEqual(code, 1, lines)
            self.assertIn("outside", " ".join(lines))
            self.assertNotIn("private-name", " ".join(lines))
            path = self.root / ".orchestration/tasks/dotfiles-T1-one-a01.md"
            path.write_text(path.read_text().replace(pattern, "scripts/one.py"))
        (self.root / "scripts/link.py").unlink()
        (self.root / "scripts/two.py").touch()
        self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", "scripts/*.py")
        self.assertIn("share scripts/two.py", " ".join(self.plan_check()[1]))

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
        self.env.update(UV_CACHE_DIR=fixture_cache(), GIT_CONFIG_GLOBAL="/dev/null")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, env=self.env)

    def plan_check(self, *args):
        head = (self.calls / "head").read_text()
        binding = f"import importlib.util,sys,subprocess,json;spec=importlib.util.spec_from_file_location('plan',sys.argv.pop(1));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.run=lambda root,*args:subprocess.CompletedProcess(args,0,json.dumps(dict(headRefOid={head!r},mergeStateStatus='CLEAN',isDraft=False,state='OPEN')),'') if args[0]=='gh' else subprocess.CompletedProcess(args,1,'','');sys.exit(m.main())"
        run = [*uv_command(), "-c", binding, str(PLAN_CHECK)]
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
        self.edit(".orchestration/tasks/dotfiles-T1-one-a01.md", "scripts/one.py", "scripts/test_*.py")
        self.edit(".orchestration/tasks/dotfiles-T2-two-a01.md", "scripts/two.py", "scripts/*_check.py")
        (self.root / "scripts").mkdir()
        (self.root / "scripts/test_other.py").write_text("")
        self.assertEqual(self.plan_check(), (0, []))
        (self.root / "scripts/test_check.py").write_text("")
        want = "F2 024-omp-cutover-and-corrective-order.md:11 P-W0 P1-1 and P1-2 share scripts/test_check.py"
        self.assertEqual(self.plan_check(), (1, [want]))

    def test_drift_uses_the_latest_timestamped_acceptance_for_the_same_task(self):
        line = "[2026-10-18T{}:00:00Z] o → w: AGMSG-ACCEPTANCE v1 task_id=dotfiles-T1-{}-a01 status={}\n"
        record = self.root / ".orchestration/acceptance/dotfiles-T1-one-a01.md"
        record.parent.mkdir(parents=True)
        events = (("05", "one", "accepted"), ("04", "one", "revise"), ("06", "other", "withdrawn"))
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
        self.edit(PLANS + "024-execution.md", "# x\n", "# x\n\n#77 abc1234 merged; #77 def4567 abc1234 CLEAN\n")
        code, lines = self.plan_check("--drift")
        live = "abc1234" + "0" * 5
        want = ["drift: 024-execution.md:3 #77 merged != OPEN", f"drift: 024-execution.md:3 #77 def4567 != {live}"]
        self.assertEqual((code, lines), (1, want))

    def test_invariants_reject_nonempty_quoted_oauth_token_assignments(self):
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
