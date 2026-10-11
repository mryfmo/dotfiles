"""An .orchestration-only PR runs no bootstrap or test matrix, and every required context still reports (T128 INV-2)."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
REMOTE = WORKFLOWS / "remote.yaml"
TEST = WORKFLOWS / "test.yaml"
AGENT_ASSETS = WORKFLOWS / "agent-assets.yml"
# A copy of the ruleset's required status checks (a unit test cannot read the
# ruleset); this is what changes when the ruleset changes.
REQUIRED_CONTEXTS = frozenset(
    {
        "validate",
        "test (ubuntu-24.04, server)",
        "test (ubuntu-24.04, client)",
        "test (macos-14, client)",
        "public-bootstrap (ubuntu-24.04, server)",
        "public-bootstrap (ubuntu-24.04, client)",
        "public-bootstrap (macos-14, client)",
    }
)
BOOTSTRAP_DECISION = "Decide whether the diff needs a bootstrap"
TEST_DECISION = "Decide whether the diff needs the unit tests"
# The jobs that skip their heavy steps, each with its own decision step and gate.
DECIDING_JOBS = (
    (REMOTE, "public-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
    (REMOTE, "private-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
    (TEST, "test", TEST_DECISION, "steps.decide.outputs.should_test == 'true'"),
)
# Steps a deciding job runs on every diff: setup, the checkout the decision
# needs, the decision, and the notices that say what was skipped.
UNGATED_STEPS = frozenset(
    {
        "Configure isolated HOME",
        "Configure Git defaults",
        "actions/checkout",
        "Checkout repository",
        BOOTSTRAP_DECISION,
        TEST_DECISION,
        "Skip the bootstrap for an .orchestration-only diff",
        "Skip full unit test run for unrelated changes",
        "Explain skipped private bootstrap",
    }
)


def jobs(path: Path) -> dict[str, dict]:
    """Each job's own keys (two-space job names, four-space keys) and its steps, read from the indentation after `jobs:`."""
    result: dict[str, dict] = {}
    job = step = block_key = None
    for line in path.read_text().split("\njobs:\n", 1)[1].split("\n"):
        if re.fullmatch(r"  ([A-Za-z0-9_-]+):", line):
            job = {"keys": {}, "steps": []}
            result[line.strip()[:-1]] = job
            step = block_key = None
            continue
        if job is None:
            continue
        key = re.fullmatch(r"    ([A-Za-z_-]+):(.*)", line)
        if key:
            job["keys"][key.group(1)] = key.group(2).strip()
            step = None
            continue
        item = re.fullmatch(r"      - (.*)", line)
        if item:
            step = {}
            job["steps"].append(step)
            line = "        " + item.group(1)
        if step is None:
            continue
        field = re.fullmatch(r"        ([A-Za-z_-]+):(.*)", line)
        if field:
            block_key = field.group(1)
            step[block_key] = field.group(2).strip()
        elif block_key == "run" and step.get("run") == "|":
            step["script"] = step.get("script", "") + line[10:] + "\n"
    return result


def step_name(step: dict) -> str:
    return step.get("name") or step.get("uses", "").split("@", 1)[0]


def matrix_contexts(path: Path, job: str) -> set[str]:
    """The `job (os, system)` contexts of a matrix job: include pairs, or the os x system product minus exclude."""
    text = path.read_text().split(f"\n  {job}:\n", 1)[1].split("\n    runs-on:", 1)[0]
    pair = r"- os: ([\w.-]+)\n\s+system: (\w+)"
    lists = re.search(r"os: \[([^\]]+)\]\n\s+system: \[([^\]]+)\]", text)
    if not lists:
        return {f"{job} ({os_name}, {system})" for os_name, system in re.findall(pair, text)}
    excluded = set(re.findall(pair, text.split("exclude:", 1)[1].split("include:", 1)[0]))
    return {
        f"{job} ({os_name.strip()}, {system.strip()})"
        for os_name in lists.group(1).split(",")
        for system in lists.group(2).split(",")
        if (os_name.strip(), system.strip()) not in excluded
    }


def decide_script(path: Path, name: str) -> str:
    scripts = [step["script"] for step in jobs(path)[name]["steps"] if step.get("id") == "decide"]
    assert len(scripts) == 1, scripts
    return scripts[0]


def run_decision(script: str, env: dict[str, str], cwd: Path) -> str:
    with tempfile.NamedTemporaryFile("r", suffix=".out", delete=False) as output:
        path = Path(output.name)
    try:
        result = subprocess.run(
            ["bash", "-c", script],
            cwd=cwd,
            env={
                **os.environ,
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1",
                "GITHUB_OUTPUT": str(path),
                **env,
            },
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        return path.read_text()
    finally:
        path.unlink()


def scratch_repository(temp: Path):
    """A clone whose origin/main holds home/a and .orchestration/x.md; returns (clone, git)."""
    origin, clone = temp / "origin.git", temp / "clone"

    def git(*args: str, cwd: Path = clone) -> str:
        return subprocess.run(
            ["git", "-C", str(cwd), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
            env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"},
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    git("init", "-q", "--bare", "-b", "main", str(origin), cwd=temp)
    git("clone", "-q", str(origin), str(clone), cwd=temp)
    (clone / "home").mkdir()
    (clone / ".orchestration").mkdir()
    (clone / "home/a").write_text("a\n")
    (clone / ".orchestration/x.md").write_text("x\n")
    git("add", "-A")
    git("commit", "-q", "-m", "base")
    git("push", "-q", "origin", "HEAD:main")
    return clone, git


def pull_request_head(clone: Path, git, branch: str, writes=(), moves=()) -> str:
    git("checkout", "-q", "-B", branch, "origin/main")
    for path, text in writes:
        (clone / path).write_text(text)
    for move in moves:
        git(*move)
    git("add", "-A")
    git("commit", "-q", "--allow-empty", "-m", branch)
    return git("rev-parse", "HEAD")


class RequiredContextsTest(unittest.TestCase):
    def test_the_required_contexts_are_the_workflows_jobs(self) -> None:
        actual = {"validate"} if "validate" in jobs(AGENT_ASSETS) else set()
        actual |= matrix_contexts(TEST, "test") | matrix_contexts(REMOTE, "public-bootstrap")
        self.assertEqual(actual, REQUIRED_CONTEXTS)

    def test_no_required_contexts_job_has_a_job_level_if_or_needs(self) -> None:
        # A skipped job reports Success even as a required check, and so does a job skipped because
        # a job it needs failed: skipping happens step by step, on a decision taken inside the job.
        for path, name in (
            (AGENT_ASSETS, "validate"),
            (TEST, "test"),
            (REMOTE, "public-bootstrap"),
            (REMOTE, "private-bootstrap"),
        ):
            for key in ("if", "needs"):
                with self.subTest(job=name, key=key):
                    self.assertNotIn(key, jobs(path)[name]["keys"])

    def test_no_job_is_left_for_a_required_job_to_need(self) -> None:
        self.assertNotIn("changes", jobs(TEST))
        self.assertNotIn("changes", jobs(REMOTE))


class DecisionStepTest(unittest.TestCase):
    def test_every_heavy_step_carries_its_jobs_decision(self) -> None:
        for path, name, _, gate in DECIDING_JOBS:
            heavy = [step for step in jobs(path)[name]["steps"] if step_name(step) not in UNGATED_STEPS]
            self.assertTrue(heavy, name)
            for step in heavy:
                with self.subTest(job=name, step=step_name(step)):
                    self.assertIn(gate, step.get("if", ""))

    def test_each_deciding_job_decides_after_its_checkout_and_fails_closed(self) -> None:
        for path, name, decide, _ in DECIDING_JOBS:
            with self.subTest(job=name):
                steps = jobs(path)[name]["steps"]
                names = [step_name(step) for step in steps]
                self.assertIn(decide, names)
                checkout = next(
                    index for index, step in enumerate(steps) if "actions/checkout@" in step.get("uses", "")
                )
                self.assertLess(checkout, names.index(decide))
                step = steps[names.index(decide)]
                self.assertEqual(step.get("id"), "decide")
                # A failing decision must fail the required context, never pass it.
                self.assertNotIn("continue-on-error", step)
                self.assertNotIn("if", step)
                before = path.read_text().split(f"\n  {name}:\n", 1)[1].split(f"- name: {decide}", 1)[0]
                self.assertIn("fetch-depth: 0", before)
                self.assertIn("persist-credentials: false", before)

    def test_both_bootstrap_jobs_decide_with_the_same_script(self) -> None:
        self.assertEqual(decide_script(REMOTE, "public-bootstrap"), decide_script(REMOTE, "private-bootstrap"))

    def test_a_main_tests_job_when_present_decides_in_itself(self) -> None:
        # V0's main-tests job is parked; when it lands it takes the same in-job decision step by step.
        job = jobs(TEST).get("main-tests")
        if job is None:
            self.assertNotIn("main-tests", TEST.read_text())
            return
        self.assertNotIn("if", job["keys"])
        self.assertNotIn("needs", job["keys"])
        self.assertIn("decide", [step.get("id") for step in job["steps"]])
        for step in job["steps"]:
            if "run" in step and step_name(step) not in UNGATED_STEPS:
                with self.subTest(step=step_name(step)):
                    self.assertIn("steps.decide.outputs.should_test == 'true'", step.get("if", ""))


class DecisionTest(unittest.TestCase):
    def test_every_event_but_pull_request_bootstraps(self) -> None:
        script = decide_script(REMOTE, "public-bootstrap")
        with tempfile.TemporaryDirectory() as empty:
            for event in ("push", "schedule", "workflow_dispatch"):
                with self.subTest(event=event):
                    self.assertEqual(run_decision(script, {"EVENT_NAME": event}, Path(empty)), "should_run=true\n")

    def test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff(self) -> None:
        script = decide_script(REMOTE, "public-bootstrap")
        cases = {
            "orchestration-only": ([(".orchestration/y.md", "y\n")], [], "false"),
            "mixed": ([(".orchestration/y.md", "y\n"), ("home/b", "b\n")], [], "true"),
            "renamed-out-of-home": ([], [("mv", "home/a", ".orchestration/a")], "true"),
            "deleted-outside": ([], [("rm", "home/a")], "true"),
            "deleted-inside": ([], [("rm", ".orchestration/x.md")], "false"),
            "empty": ([], [], "true"),
        }
        with tempfile.TemporaryDirectory() as temp:
            clone, git = scratch_repository(Path(temp))
            for name, (writes, moves, expected) in cases.items():
                with self.subTest(case=name):
                    head = pull_request_head(clone, git, f"pr-{name}", writes, moves)
                    env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
                    self.assertEqual(run_decision(script, env, clone), f"should_run={expected}\n")

    def test_the_unit_test_decision_skips_an_orchestration_only_diff(self) -> None:
        script = decide_script(TEST, "test")
        with tempfile.TemporaryDirectory() as temp:
            clone, git = scratch_repository(Path(temp))
            for name, writes, expected in (
                ("orchestration-only", [(".orchestration/y.md", "y\n")], "false"),
                ("home", [("home/b", "b\n")], "true"),
            ):
                with self.subTest(case=name):
                    head = pull_request_head(clone, git, f"t-{name}", writes)
                    env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
                    self.assertIn(f"should_test={expected}\n", run_decision(script, env, clone))


if __name__ == "__main__":
    unittest.main()
