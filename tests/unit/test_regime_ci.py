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
CHECKER = "scripts/orchestrator/task-consistency-check.py"
VERIFIER = "scripts/orchestrator/regime-ci.py"
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
    f"  - control: {name}\n    disposition: 'residual: the compensating control of this fixture'\n"
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
SKIPPED = f"regime-ci: warning: {T}: checker skipped: the copy is unverifiable, and the base's checker reads only the base's text"
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
        `task_copy` as result.txt's token, `checker` as the base's checker, `base` as more base files, `branch` as the
        head branch; precheck_head "side" names a commit on another branch. The base also holds the verifier, the
        checkout returns to the base, and the base's verifier runs against the head commit (a02).
        """
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve()
        self.git("init", "-q", "-b", "main")
        base = {CHECKER: more.get("checker") or (ROOT / CHECKER).read_text(), "README": "base\n"} | more.get("base", {})
        base |= {VERIFIER: (ROOT / VERIFIER).read_text()}
        self.commit(base | ({f".orchestration/tasks/{T}.md": dispatched} if dispatched else {}), "base")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")  # the checker's C8 to C10 probe origin/main
        if precheck_head == "side":
            precheck_head = self.commit({"side.txt": "side\n"}, "side")
            self.git("reset", "-q", "--hard", "HEAD~1")
        self.git("switch", "-q", "-c", more.get("branch", "pr"))
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
        self.head = self.git("rev-parse", "HEAD")
        self.git("switch", "-q", "main")
        return self.regime()

    def head_commit(self, files, message):
        """Commit on the head branch and return the checkout to the base."""
        self.git("switch", "-q", "pr")
        self.head = self.commit(files, message)
        self.git("switch", "-q", "main")

    def regime(self, head=None, **env):
        cmd = [*UV, str(self.repo / VERIFIER), "--base", "main", "--head", head or self.head, "--root", str(self.repo)]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env | env, capture_output=True, text=True, timeout=120, check=False
        )

    def test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier(self):
        # Bot P1 4308651010 and 4308651011 (a02 items 5, 6): the head rewrites the verifier and the checker into programs
        # that pass and leave markers, and forges a dispatched text with a matching result token; the base's policy,
        # verifier and checker still decide, the checkout stays at the base, and no head program runs.
        fake = 'import pathlib\npathlib.Path("head-program-ran").write_text("x")\nprint("{line}")\n'
        scripts = {VERIFIER: fake.format(line="regime-ci: ok 1 task(s)"), CHECKER: fake.format(line="task.md: OK")}
        rows = "".join(
            f"  - control: the PR edits {path}\n    disposition: 'residual: the compensating control of this fixture'\n"
            for path in scripts
        )
        policy = TASK.replace("threat_table:\n", "threat_table:\n" + rows).replace("at most 3 ", "at most 999 ")
        policy = policy.replace("  - src/tool.sh\n", "  - src/tool.sh\n" + "".join(f"  - {path}\n" for path in scripts))
        forged = policy.replace("  - src/tool.sh\n", "  - src/tool.sh\n  - stray.sh\n")
        cases = (  # head changes, expected exit, the violation's phrase
            (CODE | scripts, 0, None),
            (CODE | scripts | {"stray.sh": "x\n"}, 1, "allowed-files: stray.sh is outside allowed_files"),
            (CODE | scripts | {"stray.sh": "x\n", f".orchestration/tasks/{T}.md": forged}, 1, "task-copy: "),
        )
        for code, expected, phrase in cases:
            with self.subTest(expected=expected, phrase=phrase):
                copy = forged if f".orchestration/tasks/{T}.md" in code else policy
                result = self.build(copy=copy, dispatched=policy, code=code)
                self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
                self.assertFalse((self.repo / "head-program-ran").exists(), result.stdout)
                self.assertEqual(self.git("rev-parse", "main"), self.git("rev-parse", "HEAD"))
                if phrase:
                    self.assertIn(f"regime-ci: {T}: {phrase}", result.stdout)
                    self.assertIn(f"regime-ci: {T}: allowed-files: stray.sh is outside allowed_files", result.stdout)

    def test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker(self):
        # Worker review P0 of bcbd6949: the checker's C10 passes a backticked literal of the text to `git grep`, so a
        # literal that is a git option runs a command; the base's checker reads only the base's dispatched text.
        marker = Path(tempfile.mkdtemp()) / "pager-ran"
        self.addCleanup(lambda: marker.unlink(missing_ok=True))
        sentence = f'"This names {CHECKER} beside `--open-files-in-pager=touch {marker};:` for the C10 rule."\n'
        hostile = TASK.replace("kind: code", "kind: docs") + sentence
        for dispatched in (None, TASK):
            with self.subTest(dispatched=bool(dispatched)):
                result = self.build(copy=hostile, dispatched=dispatched)
                self.assertFalse(marker.exists(), result.stdout + result.stderr)
                if dispatched:
                    self.assertIn(f"regime-ci: {T}: task-copy: ", result.stdout)
                else:
                    self.assertIn(f"regime-ci: warning: {T}: checker skipped: the copy is unverifiable", result.stdout)
                    self.assertIn(
                        f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)", result.stdout
                    )

    def test_regime_ci_keeps_an_authenticated_predecessor_a_head_only_successor_names(self):
        # Worker review P3: a successor with no dispatched text at the base cannot drop a dispatched task from the check.
        successor = TASK.replace(T, "t1-a02").replace("allowed_files:", f"reset_of: [{T}]\nallowed_files:")
        successor = successor.replace("  - src/tool.sh\n", "  - src/tool.sh\n  - stray.sh\n")
        result = self.build(code=CODE | {"stray.sh": "x\n", ".orchestration/t1-a02/task.md": successor})
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f"regime-ci: {T}: allowed-files: stray.sh is outside allowed_files", result.stdout)
        # a02 amendment 1: the chain counts only when both copies verify, so a verified successor does not drop an
        # unverifiable predecessor either; that predecessor is checked as its own (unverifiable) task
        verified = {".orchestration/tasks/t1-a02.md": successor}
        result = self.build(dispatched=None, base=verified, code=CODE | {".orchestration/t1-a02/task.md": successor})
        self.assertIn(f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)", result.stdout)
        self.assertNotIn("predecessor copy", result.stdout)

    def test_regime_ci_supersedes_a_predecessor_only_when_both_copies_are_byte_equal_to_base(self):
        # The task-level audit of f7d2c48 (P2): both base texts existing is not enough; an altered predecessor copy is a
        # task-copy violation of its own task, never a skipped predecessor.
        later = "t1-a02"
        successor = TASK.replace(T, later).replace("allowed_files:", f"reset_of: [{T}]\nallowed_files:")
        verified = {f".orchestration/tasks/{later}.md": successor}
        code = CODE | {f".orchestration/{later}/task.md": successor}
        result = self.build(copy=TASK + "altered\n", base=verified, code=code)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f"regime-ci: {T}: task-copy: .orchestration/{T}/task.md differs from the base's", result.stdout)
        self.assertNotIn("predecessor copy", result.stdout)

    def test_regime_ci_exempts_records_only_heads_by_content_not_branch_name(self):
        # Bot P1 4308651013 (a02 item 7): a branch name grants nothing; only the changed paths decide records-only.
        branch = "orchestration/x"
        result = self.build(code={"src/tool.sh": "a\n"}, evidence=False, branch=branch)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("regime-ci: no target: 1 changed path(s) outside .orchestration/ and no task copy", result.stdout)
        result = self.regime(GITHUB_HEAD_REF=branch)
        self.assertEqual(1, result.returncode, result.stdout)
        result = self.build(code={".orchestration/validation/note.md": "x\n"}, evidence=False)
        self.assertEqual(
            (0, "regime-ci: no target (records-only)\n"), (result.returncode, result.stdout), result.stderr
        )

    def test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag(self):
        # a02 item 6: without dispatched text at the base the copy is unverifiable, whatever the head claims (a matching
        # result.txt token, a dispatched file of its own); a warning until REGIME_REQUIRE_DISPATCHED=1, then a violation.
        warning = f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)"
        for extra in ({}, {f".orchestration/tasks/{T}.md": TASK}):
            with self.subTest(head_dispatched=bool(extra)):
                result = self.build(dispatched=None, code=CODE | extra)
                self.assertIn(warning, result.stdout)
                if not extra:
                    self.assertEqual(
                        (0, [warning, SKIPPED, "regime-ci: ok 1 task(s)"]),
                        (result.returncode, result.stdout.splitlines()),
                    )
                flagged = self.regime(REGIME_REQUIRE_DISPATCHED="1")
                self.assertEqual(1, flagged.returncode, flagged.stdout)
                self.assertIn(
                    f"regime-ci: {T}: task-copy: task copy unverifiable (no dispatched text at base)", flagged.stdout
                )

    def test_the_regime_workflow_runs_base_code_only(self):
        # Bot P1 4308651010 (a02 items 1, 5): pull_request_target runs the base's workflow and verifier; the head is a
        # fetched ref read as data, never checked out or executed.
        read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
        cmd = [*UV, "-c", read, str(ROOT / ".github/workflows/regime.yml")]
        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        types = ["opened", "synchronize", "reopened", "ready_for_review"]
        self.assertEqual({"pull_request_target": {"types": types}}, doc.get("on", doc.get("true")))
        self.assertEqual(({"contents": "read"}, ["regime"]), (doc["permissions"], list(doc["jobs"])))
        job = doc["jobs"]["regime"]
        self.assertEqual(("ubuntu-24.04", 10, None), (job["runs-on"], job["timeout-minutes"], job.get("permissions")))
        group = doc["concurrency"]
        self.assertEqual(
            ("regime-pr-${{ github.event.pull_request.number }}", True), (group["group"], group["cancel-in-progress"])
        )
        steps = job["steps"]
        pins = [
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7",
        ]
        self.assertEqual(pins, [s["uses"] for s in steps if "uses" in s])
        base = "refs/heads/${{ github.base_ref }}"  # the tip at run time, never a stale base sha (ci:39185982423:1)
        self.assertEqual({"fetch-depth": 0, "ref": base, "persist-credentials": False}, steps[0]["with"])
        self.assertEqual({"enable-cache": False}, steps[1]["with"])
        runs = [s for s in steps if "run" in s]
        fetch, verify = runs
        self.assertIn('git fetch --no-tags origin "refs/pull/${PR_NUMBER}/head:refs/regime/pr-head"', fetch["run"])
        self.assertIn('test "$(git rev-parse refs/regime/pr-head)" = "${HEAD_SHA}"', fetch["run"])
        line = 'uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"'
        self.assertEqual(line, verify["run"])
        head = "${{ github.event.pull_request.head.sha }}"
        self.assertEqual(({"HEAD_SHA": head}, head), (verify["env"], fetch["env"]["HEAD_SHA"]))
        for step in steps:  # no step checks out, switches to or runs anything from the head
            self.assertNotIn("${{", step.get("run", ""))
            self.assertNotRegex(step.get("run", ""), r"git (checkout|switch|worktree|reset)|pr-head:|\./")
            given = json.dumps(step.get("with", {})).replace("refs/heads/", "")  # the base branch's namespace only
            self.assertNotRegex(given, r"head|merge_commit_sha|event\.after|pull/")
            self.assertFalse(step.get("uses", "x").startswith("./"))

    def test_regime_ci_accepts_a_base_that_moved_past_the_merge_base(self):
        # ci:39185982423:1 (PR #420): the job verifies against the base branch's tip, which can be ahead of the PR's merge
        # base and hold policy the fork point lacked. Only the PR's own changes count (base...head), and the dispatched
        # text is read at --base: here it exists only on the moved tip, so reading it at the merge base would warn.
        self.build(dispatched=None)
        later = {"README": "base, later\n", "later.txt": "x\n", f".orchestration/tasks/{T}.md": TASK}
        self.commit(later, "the base branch moves on and gains the dispatched text")  # the checkout is main
        result = self.regime()
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)

    def test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr(self):
        result = self.build()
        self.assertEqual((0, "regime-ci: ok 1 task(s)\n"), (result.returncode, result.stdout), result.stderr)
        no_row = TASK.replace(
            "  - control: the PR edits src/tool.sh\n    disposition: 'residual: the compensating control of this fixture'\n",
            "",
        )
        crash = TASK.replace("threat_table:\n", "threat_table:\n  - a row that is no mapping\n")
        worded = TASK.replace("changed lines outside", "changed lines (added plus deleted) outside")
        four = CODE | {"src/tool.sh": "a\nb\nc\nd\n"}
        breaks = {  # case: (the one change, a phrase of the one violation it gives)
            "task-copy": ({"copy": TASK + "a byte more\n"}, "differs from the base's dispatched"),
            "precheck head": ({"precheck_head": "0" * 40}, "is neither the head"),
            "precheck side": ({"precheck_head": "side"}, "is neither the head"),
            "precheck late": ({"late": {"src/tool.sh": "a\nb\nz\n"}}, "differs from the head outside .orchestration/"),
            "precheck reverted": (  # the prechecked test change reverted to base: out of the net diff, not of the binding
                {"late": {"tests/unit/test_tool.py": None}},
                "differs from the head outside .orchestration/t1-a01/: tests/unit/test_tool.py",
            ),
            "precheck renamed": (  # a prechecked code file moved into the evidence directory is still drift
                {"late": {"src/tool.sh": None, f".orchestration/{T}/tool.sh": "a\nb\nc\n"}},
                "differs from the head outside .orchestration/t1-a01/: src/tool.sh",
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
        # a02 item 6: result.txt's token is a consistency check among the pull request's own records, not authentication
        unverifiable = f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)"
        result = self.build(dispatched=None)
        self.assertEqual(
            (0, [unverifiable, SKIPPED, "regime-ci: ok 1 task(s)"]), (result.returncode, result.stdout.splitlines())
        )
        result = self.build(dispatched=None, task_copy="0" * 64)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f"regime-ci: {T}: task-copy: sha256 ", result.stdout)
        self.assertIn("is not result.txt's task_copy=" + "0" * 64, result.stdout)

    def test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list(self):
        self.build()
        self.git("switch", "-q", "pr")  # a checkout at the head would run the head's verifier and checker
        result = subprocess.run(
            [*UV, str(self.repo / VERIFIER), "--base", "main", "--head", self.head, "--root", str(self.repo)],
            cwd=self.repo,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("regime-ci: checkout: ", result.stdout)
        self.assertIn("not the base", result.stdout)
        self.git("switch", "-q", "--orphan", "lone")
        lone = self.commit({"src/tool.sh": "a\n"}, "a head with no merge base")
        self.git("switch", "-q", "-f", "main")
        result = self.regime(lone)
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertIn("regime-ci: git diff --name-only --no-renames", result.stdout)

    def test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory(self):
        # The checker's C1 compares task_id with the file name, `task` for every copy; regime-ci checks the directory.
        result = self.build(copy=TASK.replace(f"task_id: {T}", "task_id: t9-a01"))
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(f"regime-ci: {T}: task-id: the copy's task_id 't9-a01' is not its directory {T}", result.stdout)
        self.assertNotIn("C1 ", result.stdout)

    def test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage(self):
        # Amendment 1: a later copy whose reset_of names an earlier one is the lineage's only target; the earlier copy
        # warns, and its own .orchestration/ paths are no stray of the later one. Without reset_of, both are targets.
        later = "t1-a02"
        rows = f"  - control: the predecessor copy .orchestration/{T}/task.md\n    disposition: 'residual: the compensating control of this fixture'\n"
        rows += f"  - control: the task copy .orchestration/{later}/task.md\n    disposition: 'residual: the compensating control of this fixture'\n"
        reset = TASK.replace(T, later).replace("allowed_files:", f"reset_of: [{T}]\nallowed_files:")
        reset = reset.replace("threat_table:\n", "threat_table:\n" + rows)
        for text, expected, kept in ((reset, 0, True), (reset, 0, False), (TASK.replace(T, later), 1, True)):
            with self.subTest(reset_of="reset_of" in text, predecessor_copy_kept=kept):
                self.build(evidence=False, base={f".orchestration/tasks/{later}.md": text})
                pre = json.dumps({"head": self.head})
                token, copy = hashlib.sha256(pre.encode()).hexdigest(), hashlib.sha256(text.encode()).hexdigest()
                evidence = {f".orchestration/{later}/precheck.json": pre, f".orchestration/{later}/task.md": text}
                evidence[f".orchestration/{later}/result.txt"] = f"AGMSG-RESULT v1 precheck={token} task_copy={copy}\n"
                predecessor = {f".orchestration/{T}/task.md": TASK} if kept else {}  # a02: deleted in the first push
                self.head_commit(evidence | predecessor | {f".orchestration/{T}/note.md": "x\n"}, "two")
                result = self.regime()
                self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
                if expected == 0:
                    warning = (
                        f"regime-ci: warning: {T}: predecessor copy .orchestration/{T}/task.md (reset_of of {later})"
                    )
                    self.assertEqual([warning] * kept + ["regime-ci: ok 1 task(s)"], result.stdout.splitlines())
                else:
                    self.assertIn(
                        f"regime-ci: {T}: allowed-files: .orchestration/{later}/task.md is outside", result.stdout
                    )

    def test_regime_ci_passes_a_records_only_pr_with_no_target(self):
        result = self.build(code={".orchestration/validation/note.md": "a record\n"}, evidence=False)
        self.assertEqual(
            (0, "regime-ci: no target (records-only)\n"), (result.returncode, result.stdout), result.stderr
        )
        self.head_commit({"src/tool.sh": "a\n"}, "a code change without a task copy")
        result = self.regime()
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("regime-ci: no target: 1 changed path(s) outside .orchestration/ and no task copy", result.stdout)

    def test_regime_ci_warns_without_precheck_and_without_dispatched_text(self):
        result = self.build(dispatched=None, precheck_head="absent")
        warnings = [
            f"regime-ci: warning: {T}: task copy unverifiable (no dispatched text at base)",
            SKIPPED,
            f"regime-ci: warning: {T}: precheck absent",
            "regime-ci: ok 1 task(s)",
        ]
        self.assertEqual((0, warnings), (result.returncode, result.stdout.splitlines()), result.stderr)
        uncapped = TASK.split("## Check")[0]
        result = self.build(copy=uncapped, dispatched=uncapped)
        self.assertIn(f"regime-ci: warning: {T}: no outside cap in the copy's ## Check section", result.stdout)
        self.assertIn(f"regime-ci: warning: {T}: no tests/ cap in the copy's ## Check section", result.stdout)
        result = self.build(code=CODE | {CHECKER: (ROOT / CHECKER).read_text() + "# touched\n"})
        self.assertIn(
            f"regime-ci: warning: the diff changes {CHECKER}; this run executed the base's version", result.stdout
        )


if __name__ == "__main__":
    unittest.main()
