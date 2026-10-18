"""Exercise regime-ci.py on temporary repositories (a base with the dispatched text, a head with its copy) and regime.yml."""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/orchestrator/regime-ci.py"
CHECKER = "scripts/orchestrator/task-consistency-check.py"
UV = [shutil.which("uv") or "uv", "run", "--no-project", "--with", "pyyaml", "python", "-I"]
T = "t1-a01"
ROWS = "".join(
    f"  - control: {name}\n    disposition: residual\n"
    for name in (
        "the PR edits src/tool.sh",
        "the PR edits tests/unit/test_tool.py",
        f"the evidence under .orchestration/{T}/",
        "task metadata",
        "metadata separators",
        "in-process effects",
        "workflow and interpreter or environment inputs",
        "new or renamed scripts",
        "orchestrator effect merge",
        "orchestrator effect update-branch",
        "orchestrator effect forced worker removal",
    )
)
TASK = (
    f"---\nformat: 2\ntask_id: {T}\nkind: code\nsecurity: false\nallowed_files:\n  - src/tool.sh\n"
    f"  - tests/unit/test_tool.py\n  - .orchestration/{T}/**\nthreat_table:\n{ROWS}premises: []\n---\n\n# {T}\n\n"
    "## Check\n\nat most 3 changed lines outside `tests/` and `.orchestration/`, 2 under `tests/`.\n"
)
CODE = {"src/tool.sh": "a\nb\nc\n", "tests/unit/test_tool.py": "x = 1\ny = 2\n"}
GIT_ENV = {f"GIT_{role}_{k}": v for role in ("AUTHOR", "COMMITTER") for k, v in (("NAME", "t"), ("EMAIL", "t@t"))}


class RegimeCiTest(unittest.TestCase):
    def setUp(self):
        env = {k: v for k, v in os.environ.items() if k != "GITHUB_HEAD_REF"}
        self.env = env | GIT_ENV | {"GITHUB_HEAD_REF": "tools/t1"}

    def git(self, *args):
        cmd = ["git", "-c", "commit.gpgsign=false", *args]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env, check=True, capture_output=True, text=True
        ).stdout.strip()

    def commit(self, files, message):
        for rel, text in files.items():
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).write_text(text)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def build(self, copy=TASK, dispatched=TASK, code=None, precheck_head=None, precheck_token=None, evidence=True):
        """A base commit (the checker, the dispatched text), then a code commit and an evidence commit on a branch."""
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve()
        self.git("init", "-q", "-b", "main")
        base = {CHECKER: (ROOT / CHECKER).read_text(), "README": "base\n"}
        self.commit(base | ({f".orchestration/tasks/{T}.md": dispatched} if dispatched else {}), "base")
        self.git("switch", "-q", "-c", "pr")
        code_head = self.commit(CODE if code is None else code, "code")
        if evidence:
            pre = json.dumps({"head": precheck_head or code_head})
            token = precheck_token or hashlib.sha256(pre.encode()).hexdigest()
            result = (
                f"AGMSG-RESULT v1 task_id={T} precheck={token} task_copy={hashlib.sha256(copy.encode()).hexdigest()}\n"
            )
            files = {f".orchestration/{T}/task.md": copy}
            if precheck_head != "absent":
                files |= {f".orchestration/{T}/precheck.json": pre, f".orchestration/{T}/result.txt": result}
            self.commit(files, "evidence")
        return self.regime()

    def regime(self):
        cmd = [*UV, str(SCRIPT), "--base", "main", "--head", "HEAD", "--root", str(self.repo)]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env, capture_output=True, text=True, timeout=120, check=False
        )

    def test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr(self):
        result = self.build()
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)
        no_row = TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")
        breaks = {
            "task-copy": {"copy": TASK + "a byte more\n"},
            "precheck head": {"precheck_head": "0" * 40},
            "precheck sha": {"precheck_token": "0" * 64},
            "allowed-files": {"code": CODE | {"stray.txt": ""}},
            "caps": {"code": CODE | {"src/tool.sh": "a\nb\nc\nd\n"}},
            "checker": {"copy": no_row, "dispatched": no_row},
        }
        for case, change in breaks.items():
            with self.subTest(case=case):
                result = self.build(**change)
                found = [ln for ln in result.stdout.splitlines() if ln.startswith(f"regime-ci: {T}: ")]
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(1, len(found), result.stdout)
                self.assertTrue(found[0].startswith(f"regime-ci: {T}: {case.split()[0]}: "), found)
        self.assertIn("C4 allowed path has no threat_table row naming it: src/tool.sh", found[0])

    def test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory(self):
        # The checker's C1 compares task_id with the file name, `task` for every copy; regime-ci checks the directory.
        result = self.build(copy=TASK.replace(f"task_id: {T}", "task_id: t9-a01"))
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f"regime-ci: {T}: task-id: the copy's task_id 't9-a01' is not its directory {T}", result.stdout)
        self.assertNotIn("C1 ", result.stdout)

    def test_regime_ci_passes_a_records_only_pr_with_no_target(self):
        result = self.build(code={".orchestration/validation/note.md": "a record\n"}, evidence=False)
        self.assertEqual(
            (0, "regime-ci: no target (records-only)\n"), (result.returncode, result.stdout), result.stderr
        )
        self.commit({"src/tool.sh": "a\n"}, "a code change without a task copy")
        result = self.regime()
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("regime-ci: no target: 1 changed path(s) outside .orchestration/ and no task copy", result.stdout)

    def test_regime_ci_warns_without_precheck_and_without_dispatched_text(self):
        result = self.build(dispatched=None, precheck_head="absent")
        warnings = [
            f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at head, no result.txt)",
            f"regime-ci: warning: {T}: precheck absent",
            "regime-ci: ok 1 task(s)",
        ]
        self.assertEqual((0, warnings), (result.returncode, result.stdout.splitlines()), result.stderr)

    def test_the_regime_workflow_pins_its_actions_runs_on_the_pr_head_and_cancels_superseded_runs(self):
        read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
        cmd = [*UV, "-c", read, str(ROOT / ".github/workflows/regime.yml")]
        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        self.assertEqual(["regime"], list(doc["jobs"]))
        steps = doc["jobs"]["regime"]["steps"]
        pins = ["actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"]
        pins.append("astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7")
        self.assertEqual(pins, [s["uses"] for s in steps if "uses" in s])
        head = "${{ github.event.pull_request.head.sha }}"
        self.assertEqual(head, steps[0]["with"]["ref"])
        run = [s for s in steps if "run" in s]
        self.assertEqual(1, len(run))
        self.assertIn("scripts/orchestrator/regime-ci.py", run[0]["run"])
        self.assertIn("github.event.pull_request.head.sha", json.dumps(run[0]))
        self.assertNotIn("${{", run[0]["run"])  # every expression reaches the shell through env
        group = doc["concurrency"]
        self.assertEqual(
            ("regime-pr-${{ github.event.pull_request.number }}", True), (group["group"], group["cancel-in-progress"])
        )
        self.assertEqual({"contents": "read"}, doc["permissions"])


if __name__ == "__main__":
    unittest.main()
