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
UV = [
    shutil.which("uv") or "uv",
    "run",
    "--no-config",
    "--no-project",
    "--with",
    "pyyaml",
    "python",
    "-I",
]  # as regime.yml
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
        for rel, text in files.items():  # None deletes the file
            (self.repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / rel).unlink() if text is None else (self.repo / rel).write_text(text)
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD")

    def build(
        self, copy=TASK, dispatched=TASK, code=None, precheck_head=None, precheck_token=None, evidence=True, **more
    ):
        """A base commit (the checker, the dispatched text), then a code commit and an evidence commit on a branch.

        more: `late` files committed after the code commit precheck.json names, `precheck_doc` as precheck.json's text,
        `task_copy` as result.txt's token, `checker` as the base's checker, `base` as more base files; precheck_head
        "side" names a commit on another branch.
        """
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve()
        self.git("init", "-q", "-b", "main")
        base = {CHECKER: more.get("checker") or (ROOT / CHECKER).read_text(), "README": "base\n"} | more.get("base", {})
        self.commit(base | ({f".orchestration/tasks/{T}.md": dispatched} if dispatched else {}), "base")
        if precheck_head == "side":
            precheck_head = self.commit({"side.txt": "side\n"}, "side")
            self.git("reset", "-q", "--hard", "HEAD~1")
        self.git("switch", "-q", "-c", "pr")
        code_head = self.commit(CODE if code is None else code, "code")
        if "late" in more:
            self.commit(more["late"], "a change after the precheck")
        if evidence:
            pre = more.get("precheck_doc") or json.dumps({"head": precheck_head or code_head})
            token = precheck_token or hashlib.sha256(pre.encode()).hexdigest()
            copy_token = more.get("task_copy") or hashlib.sha256(copy.encode()).hexdigest()
            result = f"AGMSG-RESULT v1 task_id={T} precheck={token} task_copy={copy_token}\n"
            files = {f".orchestration/{T}/task.md": copy}
            if precheck_head != "absent":
                files |= {f".orchestration/{T}/precheck.json": pre, f".orchestration/{T}/result.txt": result}
            self.commit(files, "evidence")
        return self.regime()

    def regime(self, head="HEAD", **env):
        cmd = [*UV, str(SCRIPT), "--base", "main", "--head", head, "--root", str(self.repo)]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env | env, capture_output=True, text=True, timeout=120, check=False
        )

    def test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr(self):
        result = self.build()
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)
        no_row = TASK.replace("  - control: the PR edits src/tool.sh\n    disposition: residual\n", "")
        crash = TASK.replace("threat_table:\n", "threat_table:\n  - a row that is no mapping\n")
        worded = TASK.replace("changed lines outside", "changed lines (added plus deleted) outside")
        four = CODE | {"src/tool.sh": "a\nb\nc\nd\n"}
        breaks = {  # case: (the one change, a phrase of the one violation it gives)
            "task-copy": ({"copy": TASK + "a byte more\n"}, "differs from the dispatched"),
            "precheck head": ({"precheck_head": "0" * 40}, "is neither the head"),
            "precheck side": ({"precheck_head": "side"}, "is neither the head"),
            "precheck late": ({"late": {"src/tool.sh": "a\nb\nz\n"}}, "differs from the head outside .orchestration/"),
            "precheck reverted": (  # the prechecked test change reverted to base: out of the net diff, not of the binding
                {"late": {"tests/unit/test_tool.py": None}},
                "differs from the head outside .orchestration/t1-a01/: tests/unit/test_tool.py",
            ),
            "precheck symbolic": ({"precheck_doc": '{"head": "HEAD"}'}, "'HEAD' is not a 40-hex commit id"),
            "precheck none": ({"precheck_doc": "{}"}, "None is not a 40-hex commit id"),
            "precheck sha": ({"precheck_token": "0" * 64}, "is not result.txt's precheck=" + "0" * 64),
            "allowed-files": ({"code": CODE | {"stray.txt": ""}}, "stray.txt is outside allowed_files"),
            "caps outside": ({"code": four}, "4 changed lines outside tests/, .orchestration/ exceed 3"),
            "caps tests": (
                {"code": CODE | {"tests/unit/test_tool.py": "x\ny\nz\n"}},
                "3 changed lines under tests/ exceed 2",
            ),
            "caps worded": ({"copy": worded, "dispatched": worded, "code": four}, "exceed 3"),
            "checker": (
                {"copy": no_row, "dispatched": no_row},
                "C4 allowed path has no threat_table row naming it: src/tool.sh",
            ),
            "checker exit": (
                {"checker": 'print("task.md: OK")\nraise SystemExit(1)\n'},
                "no verdict (exit 1): task.md: OK",
            ),
            "checker crash": ({"copy": crash, "dispatched": crash}, "no verdict (exit 1)"),
        }
        for case, (change, phrase) in breaks.items():
            with self.subTest(case=case):
                result = self.build(**change)
                found = [ln for ln in result.stdout.splitlines() if ln.startswith(f"regime-ci: {T}: ")]
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertEqual(1, len(found), result.stdout)
                self.assertTrue(found[0].startswith(f"regime-ci: {T}: {case.split()[0]}: "), found)
                self.assertIn(phrase, found[0])

    def test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config(self):
        # --no-config: a .python-version (or uv.toml) in the checkout cannot steer the checker's uv run
        result = self.build(base={".python-version": "3.99\n"})
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)

    def test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text(self):
        result = self.build(dispatched=None)
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)
        result = self.build(dispatched=None, task_copy="0" * 64)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f"regime-ci: {T}: task-copy: sha256 ", result.stdout)
        self.assertIn("is not result.txt's task_copy=" + "0" * 64, result.stdout)

    def test_regime_ci_refuses_a_checkout_not_at_the_head_and_a_diff_git_cannot_list(self):
        self.build()
        result = self.regime(head="HEAD~1")
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("regime-ci: checkout: ", result.stdout)
        self.git("switch", "-q", "--orphan", "lone")
        self.commit({"src/tool.sh": "a\n"}, "a head with no merge base")
        result = self.regime()
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertIn("regime-ci: git diff --name-only --no-renames", result.stdout)

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
        result = self.regime(
            GITHUB_HEAD_REF="orchestration/boundary-1"
        )  # Files item 2: an orchestration/ head is records-only
        self.assertEqual(
            (0, "regime-ci: no target (records-only)\n"), (result.returncode, result.stdout), result.stderr
        )

    def test_regime_ci_warns_without_precheck_and_without_dispatched_text(self):
        result = self.build(dispatched=None, precheck_head="absent")
        warnings = [
            f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at head, no result.txt)",
            f"regime-ci: warning: {T}: precheck absent",
            "regime-ci: ok 1 task(s)",
        ]
        self.assertEqual((0, warnings), (result.returncode, result.stdout.splitlines()), result.stderr)
        uncapped = TASK.split("## Check")[0]
        result = self.build(copy=uncapped, dispatched=uncapped)
        self.assertIn(f"regime-ci: warning: {T}: no outside cap in the copy's ## Check section", result.stdout)
        self.assertIn(f"regime-ci: warning: {T}: no tests/ cap in the copy's ## Check section", result.stdout)
        result = self.build(code=CODE | {CHECKER: (ROOT / CHECKER).read_text() + "# touched\n"})
        self.assertIn(f"regime-ci: warning: the diff changes {CHECKER}, which this job runs", result.stdout)

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
        self.assertIn(
            "uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py", run[0]["run"]
        )
        self.assertIn("github.event.pull_request.head.sha", json.dumps(run[0]))
        self.assertNotIn("${{", run[0]["run"])  # every expression reaches the shell through env
        group = doc["concurrency"]
        self.assertEqual(
            ("regime-pr-${{ github.event.pull_request.number }}", True), (group["group"], group["cancel-in-progress"])
        )
        self.assertEqual({"contents": "read"}, doc["permissions"])


if __name__ == "__main__":
    unittest.main()
