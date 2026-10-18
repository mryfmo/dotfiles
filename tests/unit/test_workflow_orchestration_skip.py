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
PRIVATE = WORKFLOWS / "private-bootstrap.yaml"
TEST = WORKFLOWS / "test.yaml"
AGENT_ASSETS = WORKFLOWS / "agent-assets.yml"
# Plan 024 Q1: a pull request's newer head cancels its older run; every main push runs to completion.
CONCURRENCY = (
    "\nconcurrency:\n"
    "  group: ${{ github.workflow }}-${{ github.event_name == 'pull_request' && format('pr-{0}', "
    "github.event.pull_request.number) || format('main-{0}', github.sha) }}\n"
    "  cancel-in-progress: ${{ github.event_name == 'pull_request' }}\n"
)
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
    (PRIVATE, "private-bootstrap", BOOTSTRAP_DECISION, "steps.decide.outputs.should_run == 'true'"),
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
        "Skip the bootstrap when no bootstrap path changed",
        "Skip full unit test run for unrelated changes",
        "Explain skipped private bootstrap",
    }
)


PLAIN_KEY = re.compile(r"([a-z0-9_-]+):(?:[ \t](.*))?")


def plain_key(text: str, line: str) -> tuple[str, str]:
    """A `name: value` pair in the plain form, or ValueError: a form the reader does not parse must not read as absent."""
    match = PLAIN_KEY.fullmatch(text)
    if not match:
        raise ValueError(f"unsupported key form inside jobs: {line!r}")
    return match.group(1), (match.group(2) or "").strip()


def jobs(path: Path) -> dict[str, dict]:
    """Each job's own keys (two-space job names, four-space keys) and its steps, read from the indentation after `jobs:`.

    Fails closed: a job name, job key or step key that is not the plain form `name:` (lower-case letters, digits,
    `_` and `-`, the colon right after; no quotes, escapes or flow mappings) raises ValueError, so every structural
    test fails instead of reading an unsupported form as "no `if`". The test environment has no YAML parser.
    """
    result: dict[str, dict] = {}
    job = step = block_key = None
    in_steps = False
    for line in path.read_text().split("\njobs:\n", 1)[1].split("\n"):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if step is not None and block_key == "run" and step.get("run") == "|" and (not stripped or indent >= 10):
            step["script"] = step.get("script", "") + line[10:] + "\n"
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if indent == 0:
            break
        if indent == 2:
            name, value = plain_key(stripped, line)
            if value:
                raise ValueError(f"unsupported job form inside jobs: {line!r}")
            job = {"keys": {}, "steps": []}
            result[name] = job
            step = block_key = None
            in_steps = False
        elif job is None:
            raise ValueError(f"unsupported line before the first job: {line!r}")
        elif not job["keys"] and indent != 4:
            # Sibling keys share one indentation, so a body shifted off four spaces would hide all of them.
            raise ValueError(f"unsupported job body indentation inside jobs: {line!r}")
        elif indent == 4:
            key, value = plain_key(stripped, line)
            job["keys"][key] = value
            in_steps = key == "steps"
            step = block_key = None
        elif in_steps and indent == 6:
            if not stripped.startswith("- "):
                raise ValueError(f"unsupported step form inside jobs: {line!r}")
            step = {}
            job["steps"].append(step)
            block_key, step[block_key] = plain_key(stripped[2:], line)
        elif in_steps and indent == 8:
            if step is None:
                raise ValueError(f"unsupported step form inside jobs: {line!r}")
            block_key, step[block_key] = plain_key(stripped, line)
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
        (clone / path).parent.mkdir(parents=True, exist_ok=True)
        (clone / path).write_text(text)
    for move in moves:
        git(*move)
    git("add", "-A")
    git("commit", "-q", "--allow-empty", "-m", branch)
    return git("rev-parse", "HEAD")


def advance_origin(temp: Path, git) -> None:
    """Another clone pushes to origin/main: main moved after the job's checkout."""
    other = temp / "other"
    git("clone", "-q", str(temp / "origin.git"), str(other), cwd=temp)
    (other / "home/b").write_text("b\n")
    git("add", "-A", cwd=other)
    git("commit", "-q", "-m", "advance", cwd=other)
    git("push", "-q", "origin", "HEAD:main", cwd=other)


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
            (PRIVATE, "private-bootstrap"),
        ):
            for key in ("if", "needs"):
                with self.subTest(job=name, key=key):
                    self.assertNotIn(key, jobs(path)[name]["keys"])

    def test_the_reader_fails_closed_on_unsupported_key_forms(self) -> None:
        # Audits of dc4e6c37 and d6343494: any key form the reader does not parse exactly must fail the
        # structural tests, never read as "no if" (it replaces test_structural_tests_see_quoted_keys).
        text = REMOTE.read_text()
        job, decide, steps = "\n  public-bootstrap:\n", "        id: decide\n", "    steps:\n"
        forms = {
            "spaced job key": (job, job + "    if : false\n"),
            "escaped job key": (job, job + '    "\\x69f": false\n'),
            "spaced step key": (decide, decide + "        continue-on-error : true\n"),
            "flow-mapping step": (steps, steps + "      - { if: false }\n"),
            "quoted job name": (job, "\n  'public-bootstrap':\n"),
            "quoted step key": (decide, "        'id': decide\n"),
            # Plain keys at an unexpected indentation: a shifted job body, and a step item's keys moved right.
            "shifted job body": ("\njobs:\n", "\njobs:\n  shifted:\n      if: false\n      runs-on: ubuntu-24.04\n"),
            "shifted step item": ("      - name: Decide whether", "      -   name: Decide whether"),
        }
        for name, (old, new) in forms.items():
            with self.subTest(form=name), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "remote.yaml"
                path.write_text(text.replace(old, new, 1))
                with self.assertRaises(ValueError):
                    jobs(path)

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
        self.assertEqual(decide_script(REMOTE, "public-bootstrap"), decide_script(PRIVATE, "private-bootstrap"))

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

    def test_the_unit_test_decision_runs_the_registry_test_for_a_flakes_only_diff(self) -> None:
        # audit:4fe2438:2: test_ci_rerun.py validates .github/flakes.yaml, so a change to it alone must run the tests.
        script = decide_script(TEST, "test")
        with tempfile.TemporaryDirectory() as temp:
            clone, git = scratch_repository(Path(temp))
            head = pull_request_head(clone, git, "t-flakes", [(".github/flakes.yaml", "- {id: x}\n")])
            env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
            self.assertIn("should_test=true\n", run_decision(script, env, clone))

    def test_the_unit_test_decision_ignores_renames(self) -> None:
        # Audit of d6343494: rename detection listed only the .orchestration/ side of home/a's move.
        script = decide_script(TEST, "test")
        with tempfile.TemporaryDirectory() as temp:
            clone, git = scratch_repository(Path(temp))
            head = pull_request_head(clone, git, "t-renamed", moves=[("mv", "home/a", ".orchestration/a")])
            env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
            self.assertIn("should_test=true\n", run_decision(script, env, clone))

    def test_the_decision_survives_a_base_that_moved_after_the_checkout(self) -> None:
        # Thread 4240499289: a shallow fetch of the newer base tip cut its history, so the
        # three-dot diff found no merge base and the required context failed.
        for path, name, expected in (
            (REMOTE, "public-bootstrap", "should_run=false\n"),
            (TEST, "test", "should_test=false\n"),
        ):
            with self.subTest(job=name), tempfile.TemporaryDirectory() as temp:
                clone, git = scratch_repository(Path(temp))
                head = pull_request_head(clone, git, "pr", [(".orchestration/y.md", "y\n")])
                advance_origin(Path(temp), git)
                env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
                self.assertIn(expected, run_decision(decide_script(path, name), env, clone))

    def test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed(self) -> None:
        script = decide_script(REMOTE, "public-bootstrap")
        cases = {
            "python-script": ([("scripts/x.py", "x\n")], "false"),
            "home": ([("home/x", "x\n")], "true"),
            "install": ([("install/x.sh", "x\n")], "true"),
            # chezmoi reads .chezmoiroot; update-agent-assets.sh resolves its source root through vendor/compactiondb.
            "chezmoiroot": ([(".chezmoiroot", "home\n")], "true"),
            "vendor": ([("vendor/compactiondb/x", "x\n")], "true"),
            "orchestration": ([(".orchestration/y.md", "y\n")], "false"),
            "empty": ([], "true"),
        }
        with tempfile.TemporaryDirectory() as temp:
            clone, git = scratch_repository(Path(temp))
            for name, (writes, expected) in cases.items():
                with self.subTest(case=name):
                    head = pull_request_head(clone, git, f"b-{name}", writes)
                    env = {"EVENT_NAME": "pull_request", "BASE_REF": "main", "HEAD_SHA": head}
                    self.assertEqual(run_decision(script, env, clone), f"should_run={expected}\n")
            with self.subTest(case="push"):
                self.assertEqual(run_decision(script, {"EVENT_NAME": "push"}, clone), "should_run=true\n")

    def test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise(self) -> None:
        script = decide_script(TEST, "test")
        with tempfile.TemporaryDirectory() as temp:
            clone, git = scratch_repository(Path(temp))
            base = git("rev-parse", "origin/main")
            for name, writes, macos in (
                ("os-independent", [("scripts/x.py", "x\n"), ("docs/x.md", "x\n"), ("README.md", "x\n")], "false"),
                ("shell", [("home/x.sh", "x\n")], "true"),
                # a01 audit P2: Markdown under home/ or install/ is applied or installed, so it keeps macOS.
                ("home-markdown", [("home/dot_claude/skills/x/SKILL.md", "x\n")], "true"),
                ("install-markdown", [("install/common/README.md", "x\n")], "true"),
            ):
                head = pull_request_head(clone, git, f"m-{name}", writes)
                for event, os_name, expected in (
                    ("pull_request", "macos-14", macos),
                    ("pull_request", "ubuntu-24.04", "true"),
                    ("push", "macos-14", "true"),
                ):
                    with self.subTest(case=name, event=event, os=os_name):
                        env = {"EVENT_NAME": event, "BASE_REF": "main", "BEFORE_SHA": base, "HEAD_SHA": head}
                        output = run_decision(script, env | {"OS": os_name}, clone)
                        self.assertIn(f"should_test={expected}\n", output)
                        self.assertEqual(expected == "false", "skip_reason=os-independent on macos-14\n" in output)


class WorkflowTriggerTest(unittest.TestCase):
    def test_the_matrices_do_not_fail_fast(self) -> None:
        # Amendment 1: a failing matrix job never cancels its siblings, so each required context reports its own
        # conclusion and ci-rerun.sh never meets a cancellation that only a sibling's failure caused.
        for path, name in ((TEST, "test"), (REMOTE, "public-bootstrap"), (PRIVATE, "private-bootstrap")):
            with self.subTest(job=name):
                block = path.read_text().split(f"\n  {name}:\n", 1)[1].split("\n    runs-on:", 1)[0]
                self.assertIn("\n    strategy:\n      fail-fast: false\n      matrix:\n", block)

    def test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run(self) -> None:
        for path in (TEST, REMOTE, AGENT_ASSETS):
            with self.subTest(workflow=path.name):
                text = path.read_text()
                self.assertEqual(1, text.count("\nconcurrency:"))
                self.assertIn(CONCURRENCY, text.split("\njobs:\n", 1)[0])

    def test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script(
        self,
    ) -> None:
        on = PRIVATE.read_text().split("\non:\n", 1)[1].split("\n\n", 1)[0]
        self.assertEqual({"push", "schedule", "workflow_dispatch"}, set(re.findall(r"^  ([a-z_]+):", on, re.MULTILINE)))
        self.assertIn("  push:\n    branches: [main]\n", on)
        self.assertIn('    - cron: "0 0 * * 5"', on)
        self.assertEqual(["public-bootstrap"], list(jobs(REMOTE)))
        self.assertEqual(["private-bootstrap"], list(jobs(PRIVATE)))
        self.assertEqual(decide_script(REMOTE, "public-bootstrap"), decide_script(PRIVATE, "private-bootstrap"))


if __name__ == "__main__":
    unittest.main()
