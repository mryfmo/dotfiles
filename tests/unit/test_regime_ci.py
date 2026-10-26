"""Exercise regime-ci.py on temporary repositories (a base with the verifier, a head branch) and regime.yml."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from scratch_git import git_init, quiet_git  # noqa: E402

quiet_git()  # U100: no git command in this module's scratch repositories starts background maintenance

ROOT = Path(__file__).resolve().parents[2]
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
GIT_ENV = {f"GIT_{role}_{k}": v for role in ("AUTHOR", "COMMITTER") for k, v in (("NAME", "t"), ("EMAIL", "t@t"))}
REFUSAL = "regime-ci: no target: {n} changed path(s) outside .orchestration/ and no Program-Unit line"


class RegimeCiTest(unittest.TestCase):
    def setUp(self):
        env = {k: v for k, v in os.environ.items() if k not in ("GITHUB_HEAD_REF", "PR_BODY", "PR_AUTHOR_ASSOCIATION")}
        # a collaborator's pull request, as the program's own are; the author test varies it
        self.env = env | GIT_ENV | {"GITHUB_HEAD_REF": "tools/t1", "PR_AUTHOR_ASSOCIATION": "COLLABORATOR"}

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

    def build(self, code, branch="pr"):
        """A base commit holding the verifier, then one head commit on a branch; the checkout returns to the base."""
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve()
        git_init(self.repo, "-b", "main", env=self.env)
        stores = {f".orchestration/orchestrate/{p}/units.tsv": "id\n" for p in ("regime-cutover", "other-program")}
        self.commit({VERIFIER: (ROOT / VERIFIER).read_text(), "README": "base\n"} | stores, "base")
        self.git("switch", "-q", "-c", branch)
        self.head = self.commit(code, "head")
        self.git("switch", "-q", "main")
        return self.regime()

    def regime(self, head=None, **env):
        cmd = [*UV, str(self.repo / VERIFIER), "--base", "main", "--head", head or self.head, "--root", str(self.repo)]
        return subprocess.run(
            cmd, cwd=self.repo, env=self.env | env, capture_output=True, text=True, timeout=120, check=False
        )

    def test_regime_ci_passes_a_records_only_pr_by_content_not_branch_name(self):
        # Bot P1 4308651013 (a02 item 7): a branch name grants nothing; only the changed paths decide records-only.
        result = self.build({".orchestration/validation/note.md": "a record\n"})
        self.assertEqual(
            (0, "regime-ci: no target (records-only)\n"), (result.returncode, result.stdout), result.stderr
        )
        branch = "orchestration/x"
        result = self.build({"src/tool.sh": "a\n"}, branch=branch)
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(REFUSAL.format(n=1) + ", first src/tool.sh", result.stdout)
        result = self.regime(GITHUB_HEAD_REF=branch)
        self.assertEqual(1, result.returncode, result.stdout)

    def test_regime_ci_accepts_a_program_pr_by_its_program_unit_marker(self):
        # D-024-131 (U13): a regime-cutover program PR carries its body's own line `Program-Unit: regime-cutover/U<n>`;
        # nothing else in a body passes, and since U26 a task copy under .orchestration/ grants nothing either.
        refusal = REFUSAL.format(n=12)
        code = {f"src/u{i}.sh": "a\n" for i in range(11)} | {
            ".orchestration/t1-a01/task.md": "---\ntask_id: t1-a01\n---\n"
        }
        result = self.build(code | {"src/u11.sh": "a\n"})
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(refusal, result.stdout)
        body = "## Why\n\nThe unit's change.\n\nProgram-Unit: regime-cutover/U3\n\nGenerated with Claude Code\n"
        for accepted in (body, body.replace("\n", "\r\n")):  # a body edited on github.com carries CRLF
            result = self.regime(PR_BODY=accepted)
            self.assertEqual(
                (0, "regime-ci: no target (program unit regime-cutover/U3, D-024-131)\n"),
                (result.returncode, result.stdout),
                result.stderr,
            )
        # U71 (F063): any program whose store the base holds, not only regime-cutover
        result = self.regime(PR_BODY="Program-Unit: other-program/U3")
        self.assertEqual(
            (0, "regime-ci: no target (program unit other-program/U3, D-024-131)\n"),
            (result.returncode, result.stdout),
            result.stderr,
        )
        rejected = (
            "",
            "Program-Unit: regime-cutover/U",
            "Program-Unit: regime-cutover/U3a",
            "Program-Unit: regime-cutover/u3",
            "program-unit: regime-cutover/U3",
            "Program-Unit: /U3",
            "Program-Unit: Regime-cutover/U3",
            "Program-Unit: ../U3",
            "Program-Unit:  regime-cutover/U3",
            " Program-Unit: regime-cutover/U3",
            "Program-Unit: regime-cutover/U3 ",
            "`Program-Unit: regime-cutover/U3`",
            "see Program-Unit: regime-cutover/U3 above",
        )
        for text in rejected:
            result = self.regime(PR_BODY=text)
            self.assertEqual((1, True), (result.returncode, refusal in result.stdout), (text, result.stdout))
        # a well-formed line for a program the base has no store for grants nothing
        result = self.regime(PR_BODY="Program-Unit: no-such-program/U3")
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(
            "names no-such-program, but the base holds no .orchestration/orchestrate/no-such-program/", result.stdout
        )

    def test_regime_ci_grants_the_program_unit_line_only_to_an_owner_member_or_collaborator(self):
        # U71 (F152): before, anyone who wrote the line passed; the payload's author_association now decides
        self.build({"src/tool.sh": "a\n"})
        for author in ("OWNER", "MEMBER", "COLLABORATOR"):
            result = self.regime(PR_BODY="Program-Unit: regime-cutover/U3", PR_AUTHOR_ASSOCIATION=author)
            self.assertEqual(0, result.returncode, (author, result.stdout))
        for author in ("CONTRIBUTOR", "FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER", "NONE", "MANNEQUIN", "collaborator", ""):
            result = self.regime(PR_BODY="Program-Unit: regime-cutover/U3", PR_AUTHOR_ASSOCIATION=author)
            self.assertEqual(1, result.returncode, (author, result.stdout))
            self.assertIn("the Program-Unit line grants nothing to an author whose association is", result.stdout)

    def test_regime_ci_warns_when_the_diff_changes_the_verifier_and_still_runs_the_base_s(self):
        result = self.build({VERIFIER: "import sys\nsys.exit(0)\n"})
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn(
            f"regime-ci: warning: the diff changes {VERIFIER}; this run executed the base's version", result.stdout
        )
        self.assertIn(REFUSAL.format(n=1), result.stdout)

    def test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list(self):
        self.build({"src/tool.sh": "a\n"})
        self.git("switch", "-q", "pr")  # a checkout at the head would run the head's verifier
        result = self.regime(PR_BODY="Program-Unit: regime-cutover/U3")
        self.assertEqual(1, result.returncode, result.stdout)
        self.assertIn("regime-ci: checkout: ", result.stdout)
        self.assertIn("not the base", result.stdout)
        self.git("switch", "-q", "--orphan", "lone")
        lone = self.commit({"src/tool.sh": "a\n"}, "a head with no merge base")
        self.git("switch", "-q", "-f", "main")
        result = self.regime(lone, PR_BODY="Program-Unit: regime-cutover/U3")
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertIn("regime-ci: git diff --name-only --no-renames", result.stdout)

    def test_regime_ci_refuses_a_head_it_cannot_resolve(self):
        self.build({"src/tool.sh": "a\n"})
        result = self.regime("0" * 40, PR_BODY="Program-Unit: regime-cutover/U3")
        self.assertEqual(2, result.returncode, result.stdout)
        self.assertIn("regime-ci: cannot resolve --base main or --head", result.stdout)

    def test_the_regime_workflow_runs_base_code_only(self):
        # Bot P1 4308651010 (a02 items 1, 5): pull_request_target runs the base's workflow and verifier; the head is a
        # fetched ref read as data, never checked out or executed.
        read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1])), default=str))"
        cmd = [*UV, "-c", read, str(ROOT / ".github/workflows/regime.yml")]
        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        # U71 (F155): a body edit re-runs the check, and only pull requests into main run it
        types = ["opened", "edited", "synchronize", "reopened", "ready_for_review"]
        self.assertEqual(
            {"pull_request_target": {"types": types, "branches": ["main"]}}, doc.get("on", doc.get("true"))
        )
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
        line = 'uv run --no-config --no-project python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"'
        self.assertEqual(line, verify["run"])
        head = "${{ github.event.pull_request.head.sha }}"
        body = {"PR_BODY": "${{ github.event.pull_request.body }}"}  # the program marker's source (D-024-131)
        author = {"PR_AUTHOR_ASSOCIATION": "${{ github.event.pull_request.author_association }}"}  # U71, F152
        self.assertEqual(({"HEAD_SHA": head} | body | author, head), (verify["env"], fetch["env"]["HEAD_SHA"]))
        for step in steps:  # no step checks out, switches to or runs anything from the head
            self.assertNotIn("${{", step.get("run", ""))
            self.assertNotRegex(step.get("run", ""), r"git (checkout|switch|worktree|reset)|pr-head:|\./")
            given = json.dumps(step.get("with", {})).replace("refs/heads/", "")  # the base branch's namespace only
            self.assertNotRegex(given, r"head|merge_commit_sha|event\.after|pull/")
            self.assertFalse(step.get("uses", "x").startswith("./"))

    def test_regime_yml_gives_the_checker_no_token(self):
        # F082: regime-ci.py runs only git, so its step gets no GH_TOKEN; the job's token stays contents: read.
        read = "import json, sys, yaml; print(json.dumps(yaml.safe_load(open(sys.argv[1]))))"
        cmd = [*UV, "-c", read, str(ROOT / ".github/workflows/regime.yml")]
        doc = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
        steps = doc["jobs"]["regime"]["steps"]
        self.assertEqual([], [s.get("name", s.get("uses")) for s in steps if "GH_TOKEN" in s.get("env", {})])
        self.assertEqual({"contents": "read"}, doc["permissions"])


if __name__ == "__main__":
    unittest.main()
