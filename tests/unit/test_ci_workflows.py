"""The CI critical path (U39): the sharded unit-test runner, its matrix rows and aggregators (regime-cutover U622), the
render-only subtrees the bootstrap may skip, and the apply-check image's cached build (U610)."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from workflow_lock import load_yaml, lockfile  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SHARDS = ROOT / "scripts/ci/unittest-shards.py"
REMOTE = ROOT / ".github/workflows/remote.yaml"
TEST = ROOT / ".github/workflows/test.yaml"
APPLY_CHECK = ROOT / ".github/workflows/apply-check.yml"
DOCKERFILE = ROOT / "Dockerfile"
MAKEFILE = ROOT / "Makefile"
MAKE = shutil.which("make")
# U610: the bounds the runner's own apt gets (scripts/ci/drop-azure-apt-mirror.py; test_apt_mirror.py FORM_WORDS), on
# every apt-get of the image build too, so a stalled archive.ubuntu.com fails the layer fast.
APT_BOUNDS = "-o Acquire::http::Timeout=15 -o Acquire::Retries=3"
# The two buildx actions, pinned as the kit pins every action: a full semver tag in the workflow and one entry of
# .github/workflows/actions.lock (test_workflow_security.py) whose commit is the tag's sha and whose ids are the docker
# organisation's and the repository's, the identity the runner verifies at run time.
DOCKER_OWNER_ID = 5429470
BUILDX_ACTIONS = {"docker/setup-buildx-action": 288485773, "docker/build-push-action": 241092383}
# The build arguments make docker-image passes, in its order; make docker-build-args prints each as `NAME=value`.
# APT_WEEK (round 3, verdict of 1c416678 P2): the ISO week of the build, `date -u +%G-W%V`, the apt layer's cache key.
BUILD_ARGS = ("USERNAME", "APT_WEEK", "DOCKERFILE_ID", "CHEZMOI_VERSION", "CHEZMOI_SHA256")
# make docker-build-args prints the five in that order; the two resolved on the host without a fetch come first.
PRINTED = "printf 'USERNAME=%s\\nAPT_WEEK=%s\\nDOCKERFILE_ID=%s\\nCHEZMOI_VERSION=%s\\nCHEZMOI_SHA256=%s\\n'"
# The ISO week as the Makefile reads it, checked (a `$(…)` read without its status is a defect, AGENTS.md Audit).
WEEK_READ = 'apt_week="$(date -u +%G-W%V)" || {'
# The three required status contexts of the main ruleset (read 2026-11-19 through the rulesets API; the constant
# scripts/orchestrator/pr-merge.sh REQUIRED_CHECKS holds the same names), kept by the aggregator jobs of test.yaml
# since U622 split each pair into shard rows.
REQUIRED_TEST_CHECKS = ("test (macos-15, client)", "test (ubuntu-24.04, client)", "test (ubuntu-24.04, server)")
# The matrix rows U622 gives each os: a quarter of the plan per macOS row (5 concurrent macOS jobs on the Free plan),
# a half per Ubuntu row, the ubuntu-26.04 canary included.
SHARD_ROWS = {
    ("macos-15", "client"): ("1/4", "2/4", "3/4", "4/4"),
    ("ubuntu-24.04", "client"): ("1/2", "2/2"),
    ("ubuntu-24.04", "server"): ("1/2", "2/2"),
    ("ubuntu-26.04", "client"): ("1/2", "2/2"),
}
# The render-only subtrees of home/ and the targets chezmoi gives them; the bootstrap must neither execute nor read
# any of these targets, or a change there needs the full bootstrap again.
RENDER_ONLY = {
    # Per skill, not the whole of .agents/skills: the installers own crit* and poteto-mode there.
    "dot_agents/skills": [".agents/skills/{skill}"],
    "dot_agents/omp/policies": [".agents/omp/policies"],
    "dot_claude/rules": [".claude/rules"],
    "dot_config/claude/rules": [".config/claude/rules"],
    # Not dot_local/bin itself: a file there renders to ~/.local/bin/<name>, where the installers run mise and omp.
    "dot_local/bin/common": [".local/bin/common"],
    "dot_local/bin/server": [".local/bin/server"],
}
# chezmoi source-name attributes, stripped to reach a target name (the ones this tree uses and their neighbours).
ATTRIBUTES = ("private_", "readonly_", "executable_", "exact_", "empty_", "symlink_", "literal_")
# What setup.sh runs on a host: itself, the installers, the libraries and the chezmoi scripts that include them.
BOOTSTRAP_READERS = (
    "setup.sh",
    "install",
    "scripts/lib",
    "scripts/update-agent-assets.sh",
    "scripts/gh-auth.sh",
    "home/.chezmoiscripts",
)


sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes
from workflow_lock import load_yaml


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


def target_of(source: str) -> str:
    """The target path chezmoi gives a source path relative to home/: attributes stripped, dot_ to a dot, .tmpl off."""
    parts = []
    for part in source.split("/"):
        while part.startswith(ATTRIBUTES):
            part = part[next(len(a) for a in ATTRIBUTES if part.startswith(a)) :]
        part = "." + part[4:] if part.startswith("dot_") else part
        parts.append(part.removesuffix(".tmpl"))
    return "/".join(parts)


def skill_names() -> list[str]:
    """The target name of every entry directly in home/dot_agents/skills, a directory or a file."""
    return sorted(target_of(path.name) for path in (ROOT / "home/dot_agents/skills").iterdir())


def render_only_reads(files: list[Path]) -> list[str]:
    """Each `file: target` where a bootstrap reader names a render-only source path or the target chezmoi gives it."""
    skills = skill_names()
    needles = [f"home/{subtree}" for subtree in RENDER_ONLY] + [f'"{subtree}' for subtree in RENDER_ONLY]
    for targets in RENDER_ONLY.values():
        for target in targets:
            needles += [target.format(skill=skill) for skill in skills] if "{skill}" in target else [target]
    found = []
    for path in files:
        text = path.read_text(errors="replace")
        # Nothing word-like after the needle: .agents/skills/hcom-worker does not match hcom-worker-extra.
        found += [f"{path}: {needle}" for needle in needles if re.search(re.escape(needle) + r"(?![\w-])", text)]
    return found


def shards(start: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SHARDS), "--start", str(start), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


def suite(temp: str, modules: dict[str, str]) -> Path:
    start = Path(temp) / "unit"
    start.mkdir()
    for name, body in modules.items():
        (start / name).write_text("import unittest\n\n" + textwrap.dedent(body))
    return start


def dry_run_plan(output: str) -> list[tuple[str, int]]:
    """The `--dry-run` listing as (shard name, test count) in its order; nothing else of the output is a plan line."""
    return [(m.group(1), int(m.group(2))) for m in re.finditer(r"^  (\S.*): (\d+) tests$", output, re.MULTILINE)]


def matrix_rows(matrix: dict) -> list[dict[str, str]]:
    """The rows GitHub builds from a `strategy.matrix`: the product of its lists, less every combination an `exclude`
    entry matches on all of its keys, plus each `include` entry that matches no combination as a row of its own
    (docs.github.com, "Running variations of jobs in a workflow"; the includes here add rows, none extends one)."""
    keys = [key for key in matrix if key not in ("include", "exclude")]
    rows: list[dict[str, str]] = [{}]
    for key in keys:
        rows = [{**row, key: str(value)} for row in rows for value in matrix[key]]
    for excluded in matrix.get("exclude", []):
        rows = [row for row in rows if any(row.get(k) != str(v) for k, v in excluded.items())]
    for included in matrix.get("include", []):
        extra = {k: str(v) for k, v in included.items()}
        if not any(all(row.get(k) == v for k, v in extra.items() if k in row) for row in rows):
            rows.append(extra)
    return rows


PASSING = """
class A(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ready = True

    def test_one(self):
        self.assertTrue(self.ready)

    def test_sub(self):
        for value in (1, 2):
            with self.subTest(value=value):
                self.assertGreater(value, 0)

    @unittest.skip("host-specific")
    def test_skipped(self):
        pass
"""


class UnittestShardsTest(unittest.TestCase):
    def test_a_passing_suite_reports_one_combined_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            start = suite(
                temp,
                {
                    "test_a.py": PASSING,
                    "test_b.py": "class B(unittest.TestCase):\n    def test_b(self):\n        pass\n",
                },
            )
            result = shards(start, "--jobs", "2")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("4 tests in 2 modules, 2 shards", result.stdout)
            self.assertRegex(
                result.stdout, r"\nRan 4 tests in [0-9.]+s \(2 modules, 2 shards, 2 jobs\)\nOK \(skipped=1\)\n\Z"
            )
            # Each module's own verbose unittest output is printed, so a failure reads as it does in the serial run.
            self.assertIn("test_one (test_a.A", result.stdout)

    def test_a_failing_test_fails_the_run_and_names_its_module(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            failing = "class F(unittest.TestCase):\n    def test_f(self):\n        self.assertEqual(1, 2)\n"
            start = suite(temp, {"test_a.py": PASSING, "test_f.py": failing})
            result = shards(start, "--jobs", "2")
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED shard test_f.py: exit 1, FAILED", result.stdout)
            self.assertTrue(result.stdout.rstrip().endswith("FAILED (failures=1, skipped=1)"), result.stdout)

    def test_a_module_that_does_not_import_fails_the_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            start = suite(temp, {"test_a.py": PASSING, "test_broken.py": "import no_such_module_u39\n"})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED shard test_broken.py", result.stdout)

    def test_a_module_that_dies_without_a_summary_fails_the_run(self) -> None:
        # A shard that exits 0 before unittest prints its summary must not read as a pass.
        with tempfile.TemporaryDirectory() as temp:
            dying = "import os\n\nclass D(unittest.TestCase):\n    def test_d(self):\n        os._exit(0)\n"
            start = suite(temp, {"test_a.py": PASSING, "test_d.py": dying})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED shard test_d.py: exit 0, no unittest summary", result.stdout)

    def test_a_module_that_runs_fewer_tests_than_discovery_found_fails_the_run(self) -> None:
        # The parent counts with discovery; a shard whose own run sees fewer tests (here: a module that drops a
        # class when it is the only module loaded) fails on the count, not on its own OK.
        with tempfile.TemporaryDirectory() as temp:
            calls = Path(temp) / "calls"
            # The parent loads the module twice (one discovery of the whole pattern, one of the file); the shard's
            # load, the third, drops the class.
            fewer = f"""
            from pathlib import Path

            def load_tests(loader, tests, pattern):
                calls = Path({str(calls)!r})
                count = int(calls.read_text()) + 1 if calls.exists() else 1
                calls.write_text(str(count))
                return unittest.TestSuite() if count > 2 else tests

            class G(unittest.TestCase):
                def test_g(self):
                    pass
            """
            start = suite(temp, {"test_g.py": fewer})
            result = shards(start)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn("ran 0 tests, discovery found 1", result.stdout)

    def test_two_modules_of_one_file_name_run_in_one_shard(self) -> None:
        # -p matches the file name in every package, so both run together and every test is counted once.
        with tempfile.TemporaryDirectory() as temp:
            start = suite(temp, {"test_a.py": PASSING})
            package = start / "pkg"
            package.mkdir()
            (package / "__init__.py").write_text("")
            (package / "test_a.py").write_text("import unittest\n" + textwrap.dedent(PASSING))
            result = shards(start)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("6 tests in 1 modules, 1 shards", result.stdout)
            self.assertIn("\nRan 6 tests in ", result.stdout)

    def test_per_file_discovery_that_misses_tests_of_the_whole_fails_before_any_shard_runs(self) -> None:
        # A load_tests that answers the file pattern differently from test*.py: the shards would not run the
        # serial suite, so the run fails before it starts.
        with tempfile.TemporaryDirectory() as temp:
            narrowing = """
            def load_tests(loader, tests, pattern):
                return tests if pattern == "test*.py" else unittest.TestSuite()

            class N(unittest.TestCase):
                def test_n(self):
                    pass
            """
            start = suite(temp, {"test_a.py": PASSING, "test_n.py": narrowing})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("per-file discovery found 3 tests, one discovery of test*.py 4", result.stderr)
            self.assertNotIn("=====", result.stdout)

    def test_discovery_imports_from_the_working_directory_like_python_m_unittest(self) -> None:
        # test_validate_agent_assets.py imports tests.unit.test_generate_agent_configs: the parent's count must
        # import it as `python -m unittest` does, or the count check fails a passing suite.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            unit = root / "tests/unit"
            unit.mkdir(parents=True)
            (unit / "helper_values.py").write_text("VALUE = 1\n")
            (unit / "test_imports.py").write_text(
                "import unittest\n\nfrom tests.unit.helper_values import VALUE\n\n"
                "class I(unittest.TestCase):\n    def test_i(self):\n        self.assertEqual(VALUE, 1)\n\n"
                "    def test_j(self):\n        self.assertEqual(VALUE, 1)\n"
            )
            result = shards(Path("tests/unit"), cwd=root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            # A failed import counts as one test, so two tests tell it from a pass.
            self.assertIn("2 tests in 1 modules, 1 shards", result.stdout)

    def test_a_big_module_runs_as_several_shards_that_select_exactly_its_tests(self) -> None:
        # test_a is a prefix of test_ab: a substring -k pattern would run it twice and fail the count.
        with tempfile.TemporaryDirectory() as temp:
            big = "class S(unittest.TestCase):\n" + "".join(
                f"    def test_{name}(self):\n        pass\n" for name in ("a", "ab", "abc", "b", "c")
            )
            start = suite(temp, {"test_big.py": big, "test_small.py": PASSING})
            result = shards(start, "--split", "2")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("8 tests in 2 modules, 5 shards", result.stdout)
            for index in (1, 2, 3):
                self.assertIn(f"===== test_big.py[{index}/3]: ", result.stdout)
            self.assertEqual(1, result.stdout.count("test_ab (test_big.S"))
            self.assertIn("(2 modules, 5 shards, ", result.stdout)

    def test_a_failure_in_a_split_module_names_its_shard(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            big = "class S(unittest.TestCase):\n" + "".join(
                f"    def test_{index}(self):\n        self.assertNotEqual({index}, 3)\n" for index in range(4)
            )
            start = suite(temp, {"test_big.py": big})
            result = shards(start, "--split", "2")
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED shard test_big.py[2/2]: exit 1, FAILED", result.stdout)
            self.assertNotIn("FAILED shard test_big.py[1/2]", result.stdout)

    def test_a_module_with_load_tests_is_not_split(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            loaded = "def load_tests(loader, tests, pattern):\n    return tests\n\n" + PASSING
            start = suite(temp, {"test_loaded.py": loaded})
            result = shards(start, "--split", "1")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("3 tests in 1 modules, 1 shards", result.stdout)

    def test_an_empty_start_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            start = suite(temp, {})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("found no test modules", result.stderr)

    def test_a_shard_part_runs_its_share_of_the_plan_biggest_first(self) -> None:
        # The plan is the biggest-first order; part K of N is every N-th shard from the K-th, so with two modules of
        # three and one tests, part 1/2 is the big one and 2/2 the small one, each a complete run with its own summary.
        with tempfile.TemporaryDirectory() as temp:
            start = suite(
                temp,
                {
                    "test_a.py": PASSING,
                    "test_b.py": "class B(unittest.TestCase):\n    def test_b(self):\n        pass\n",
                },
            )
            first = shards(start, "--jobs", "2", "--shard", "1/2")
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertIn("3 tests in 1 modules, 1 shards under", first.stdout)
            self.assertIn(", shard 1/2 of 2, 2 at a time", first.stdout)
            self.assertIn("===== test_a.py: 3 tests", first.stdout)
            self.assertNotIn("test_b.py", first.stdout)
            self.assertRegex(
                first.stdout, r"\nRan 3 tests in [0-9.]+s \(1 modules, 1 shards, 2 jobs\)\nOK \(skipped=1\)\n\Z"
            )
            second = shards(start, "--jobs", "2", "--shard", "2/2")
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertIn("1 tests in 1 modules, 1 shards under", second.stdout)
            self.assertIn("===== test_b.py: 1 tests", second.stdout)
            self.assertNotIn("test_a.py", second.stdout)
            # A failing shard fails its part as it fails the whole run.
            failing = "class F(unittest.TestCase):\n    def test_f(self):\n        self.assertEqual(1, 2)\n"
            (start / "test_f.py").write_text("import unittest\n\n" + failing)
            # test_f (1 test) and test_b (1 test) tie on size and sort by name: part 2/2 is test_b, 3/3 is test_f.
            self.assertEqual(shards(start, "--shard", "2/2").returncode, 0)
            third = shards(start, "--shard", "3/3")
            self.assertEqual(third.returncode, 1)
            self.assertIn("FAILED shard test_f.py: exit 1, FAILED", third.stdout)

    def test_a_shard_outside_its_count_is_a_usage_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            start = suite(temp, {"test_a.py": PASSING})
            for part, message in (
                ("0/4", "'0/4': K must be in 1..N"),
                ("5/4", "'5/4': K must be in 1..N"),
                ("4", "'4' is not K/N"),
                ("a/b", "'a/b' is not K/N"),
                ("1/0", "'1/0': K must be in 1..N"),
            ):
                with self.subTest(part=part):
                    result = shards(start, "--shard", part, "--dry-run")
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn(f"argument --shard: {message}", result.stderr)
                    self.assertEqual("", result.stdout)
            # More parts than shards: the empty part is a failure, never a silent pass.
            result = shards(start, "--shard", "2/2")
            self.assertEqual(result.returncode, 1)
            self.assertIn("shard 2/2 of 1 is empty", result.stderr)

    def test_dry_run_prints_the_plan_and_runs_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            failing = "class F(unittest.TestCase):\n    def test_f(self):\n        self.assertEqual(1, 2)\n"
            big = "class S(unittest.TestCase):\n" + "".join(
                f"    def test_{i}(self):\n        pass\n" for i in range(4)
            )
            start = suite(temp, {"test_a.py": PASSING, "test_f.py": failing, "test_big.py": big})
            result = shards(start, "--split", "3", "--dry-run")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("8 tests in 3 modules, 4 shards under", result.stdout)
            self.assertEqual(
                [("test_a.py", 3), ("test_big.py[1/2]", 2), ("test_big.py[2/2]", 2), ("test_f.py", 1)],
                dry_run_plan(result.stdout),
            )
            self.assertNotIn("=====", result.stdout)
            self.assertNotIn("Ran ", result.stdout)
            # The parts of the plan together list every shard once, each part in the plan's order.
            whole = dry_run_plan(result.stdout)
            parts = [
                dry_run_plan(shards(start, "--split", "3", "--dry-run", "--shard", f"{k}/3").stdout) for k in (1, 2, 3)
            ]
            self.assertEqual([whole[0::3], whole[1::3], whole[2::3]], parts)
            self.assertEqual(sorted(whole), sorted(shard for part in parts for shard in part))

    def test_the_quarters_and_halves_of_the_real_plan_list_every_shard_once(self) -> None:
        # The plan CI's rows run (--start tests/unit from the repository root, as make unit-test runs it): the N parts of
        # each os's count together are the whole plan, every shard once, and no part is empty.
        whole = shards(Path("tests/unit"), "--dry-run", cwd=ROOT)
        self.assertEqual(whole.returncode, 0, whole.stdout + whole.stderr)
        plan = dry_run_plan(whole.stdout)
        self.assertGreater(len(plan), 100, whole.stdout)
        self.assertEqual(len(plan), len(set(plan)))
        self.assertIn(f"{len(plan)} shards under tests/unit, ", whole.stdout)
        for count in sorted({len(parts) for parts in SHARD_ROWS.values()}):
            with self.subTest(parts=count):
                listed: list[tuple[str, int]] = []
                for k in range(1, count + 1):
                    part = shards(Path("tests/unit"), "--dry-run", "--shard", f"{k}/{count}", cwd=ROOT)
                    self.assertEqual(part.returncode, 0, part.stdout + part.stderr)
                    self.assertIn(f", shard {k}/{count} of {len(plan)}, ", part.stdout)
                    quarter = dry_run_plan(part.stdout)
                    self.assertEqual(plan[k - 1 :: count], quarter)
                    self.assertTrue(quarter)
                    listed += quarter
                self.assertEqual(sorted(plan), sorted(listed))
                self.assertEqual(len(plan), len(listed))


class MakeUnitTestTest(unittest.TestCase):
    def make(self, *args: str) -> str:
        # A make that runs this suite passes MAKELEVEL and MAKEFLAGS down; GNU make then prints "Entering directory".
        env = {
            key: value
            for key, value in os.environ.items()
            if key not in {"UNIT_TEST_JOBS", "UNIT_TEST_SHARD", "MAKEFLAGS", "MAKELEVEL"}
        }
        return subprocess.run(
            ["make", "--no-print-directory", "-n", "unit-test", *args],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

    def test_the_serial_form_is_the_unchanged_discover_command(self) -> None:
        self.assertEqual(self.make("UNIT_TEST_JOBS=1"), "uv run python -m unittest discover -s tests/unit -v\n")

    def test_the_default_runs_the_shards_on_every_cpu(self) -> None:
        warm, run = self.make().splitlines()
        # PyYAML enters the uv cache before any shard starts (offline first, as UV_PYYAML probes).
        self.assertRegex(warm, r"^uv run (--offline )?--with pyyaml python -c 'import yaml'$")
        self.assertEqual(run, "uv run python scripts/ci/unittest-shards.py --start tests/unit --jobs 0")
        self.assertTrue(self.make("UNIT_TEST_JOBS=3").endswith("--jobs 3\n"))

    def test_every_test_job_runs_the_shards_and_fails_on_their_status(self) -> None:
        step = TEST.read_text().split("      - name: Run Python unit tests\n", 1)[1].split("\n      - name: ", 1)[0]
        step = "".join(line + "\n" for line in step.splitlines() if not line.lstrip().startswith("#"))
        self.assertIn('UNIT_TEST_JOBS="$(( 2 * cpus ))" make unit-test\n', step)
        for weakening in ("continue-on-error", "|| true", "set +e", "UNIT_TEST_JOBS=1"):
            with self.subTest(weakening=weakening):
                self.assertNotIn(weakening, step)
        self.assertNotIn("U39 measurement", TEST.read_text())

    def test_unit_test_shard_narrows_the_run_to_one_part(self) -> None:
        # The step's env sets UNIT_TEST_SHARD to the row's K/N; make passes it to the runner and nothing else changes.
        warm, run = self.make("UNIT_TEST_SHARD=2/4").splitlines()
        self.assertRegex(warm, r"^uv run (--offline )?--with pyyaml python -c 'import yaml'$")
        self.assertEqual(run, "uv run python scripts/ci/unittest-shards.py --start tests/unit --jobs 0 --shard 2/4")
        self.assertTrue(self.make("UNIT_TEST_JOBS=6", "UNIT_TEST_SHARD=1/2").endswith("--jobs 6 --shard 1/2\n"))
        self.assertEqual(self.make("UNIT_TEST_JOBS=1", "UNIT_TEST_SHARD=1/2"), self.make("UNIT_TEST_JOBS=1"))


class ShardMatrixTest(unittest.TestCase):
    """Regime-cutover U622: the test job runs as matrix shard rows and three aggregators keep the ruleset's names."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.document = load_yaml(TEST)
        cls.jobs = cls.document["jobs"]

    def test_the_matrix_gives_macos_four_parts_and_ubuntu_two(self) -> None:
        job = self.jobs["test"]
        self.assertEqual("test-shard (${{ matrix.os }}, ${{ matrix.system }}, ${{ matrix.shard }})", job["name"])
        self.assertFalse(job["strategy"]["fail-fast"])
        rows = matrix_rows(job["strategy"]["matrix"])
        expected = [
            {"os": os_, "system": system, "shard": shard}
            for (os_, system), parts in SHARD_ROWS.items()
            for shard in parts
        ]
        by_row = lambda row: (row["os"], row["system"], row["shard"])
        self.assertEqual(sorted(expected, key=by_row), sorted(rows, key=by_row))
        self.assertEqual(10, len(rows))

    def test_the_row_runs_its_part_through_the_steps_env(self) -> None:
        steps = {step.get("name"): step for step in self.jobs["test"]["steps"]}
        step = steps["Run Python unit tests"]
        self.assertEqual({"UNIT_TEST_SHARD": "${{ matrix.shard }}"}, step["env"])
        self.assertEqual(25, step["timeout-minutes"])
        self.assertIn('UNIT_TEST_JOBS="$(( 2 * cpus ))" make unit-test\n', step["run"])
        # No other step and no job-level env names the shard: tests/unit/test_apt_mirror.py pins the names in scope of
        # the apt steps, and the Bats suite, the lints and the smoke tests run whole in every row.
        self.assertNotIn("UNIT_TEST_SHARD", self.jobs["test"].get("env", {}))
        for name, other in steps.items():
            if name != "Run Python unit tests":
                with self.subTest(step=name):
                    self.assertNotIn("UNIT_TEST_SHARD", str(other.get("env", {})) + str(other.get("run", "")))
        # The Bats coverage is the same in every row of a pair: the first row alone uploads it.
        upload = steps["Upload coverage to Codecov"]
        self.assertIn("startsWith(matrix.shard, '1/')", upload["if"])
        self.assertIn("matrix.os == 'ubuntu-24.04'", upload["if"])

    def test_the_required_check_names_are_aggregators_over_the_shard_rows(self) -> None:
        # The ruleset requires the three names (only the admin changes it); each is a job that needs the shard job,
        # runs however the rows ended and fails unless the matrix succeeded, so green means every shard passed.
        by_name = {job.get("name"): (job_id, job) for job_id, job in self.jobs.items()}
        self.assertEqual(set(REQUIRED_TEST_CHECKS), set(by_name) - {self.jobs["test"]["name"]})
        for required in REQUIRED_TEST_CHECKS:
            with self.subTest(check=required):
                _, job = by_name[required]
                self.assertNotIn("strategy", job)  # one check per name, never a matrix
                self.assertEqual("test", job["needs"])
                self.assertEqual("${{ always() }}", job["if"])
                self.assertEqual({"SHARDS_RESULT": "${{ needs.test.result }}"}, job["env"])
                self.assertIn("timeout-minutes", job)
                (step,) = job["steps"]
                self.assertIn('if [ "${SHARDS_RESULT}" != success ]; then\n', step["run"])
                self.assertIn("exit 1\n", step["run"])
                for weakening in ("continue-on-error", "|| true", "set +e", "success()", "failure()"):
                    self.assertNotIn(weakening, str(job))
        # No job id or matrix name collides with a required name: the shard rows report under test-shard (...).
        self.assertFalse(set(REQUIRED_TEST_CHECKS) & set(self.jobs))
        self.assertTrue(self.jobs["test"]["name"].startswith("test-shard ("))
        # pr-merge.sh requires the same names: a renamed check here would be a merge refusal there.
        lever = (ROOT / "scripts/orchestrator/pr-merge.sh").read_text()
        for required in REQUIRED_TEST_CHECKS:
            self.assertIn(f"    '{required}'\n", lever)

    def test_a_dispatched_run_may_put_the_macos_rows_on_another_image(self) -> None:
        # The measurement of U622: `macos_runner` (default macos-15) is the runs-on of the macos-15 rows alone; the
        # matrix label, the job names and OS stay macos-15, and a dispatched run tests every row whatever the diff.
        on = self.document["true"]  # PyYAML (YAML 1.1) reads the key `on` as the boolean true, the JSON carrier "true"
        inputs = on["workflow_dispatch"]["inputs"]
        self.assertEqual(["macos_runner"], list(inputs))
        self.assertEqual("macos-15", inputs["macos_runner"]["default"])
        self.assertEqual("string", inputs["macos_runner"]["type"])
        job = self.jobs["test"]
        self.assertEqual("${{ matrix.os == 'macos-15' && inputs.macos_runner || matrix.os }}", job["runs-on"])
        self.assertEqual("${{ matrix.os }}", job["env"]["OS"])
        for other_id, other in self.jobs.items():
            if other_id != "test":
                with self.subTest(job=other_id):
                    self.assertEqual("ubuntu-24.04", other["runs-on"])
        decide = next(step for step in job["steps"] if step.get("id") == "decide")
        dispatch = 'if [ "${EVENT_NAME}" = workflow_dispatch ] || [ "${paths}" -eq 0 ]; then\n'
        self.assertIn(dispatch, decide["run"])
        after = decide["run"].split(dispatch, 1)[1]
        self.assertTrue(after.startswith('  echo "should_test=true" >> "${GITHUB_OUTPUT}"\n'), after[:120])

    def test_the_matrix_reader_follows_githubs_exclude_and_include_rules(self) -> None:
        matrix = {
            "os": ["a", "b"],
            "n": [1, 2],
            "exclude": [{"os": "a", "n": 2}, {"os": "c"}],
            "include": [{"os": "c", "n": 3}, {"os": "b", "n": 1}],
        }
        self.assertEqual(
            [{"os": "a", "n": "1"}, {"os": "b", "n": "1"}, {"os": "b", "n": "2"}, {"os": "c", "n": "3"}],
            matrix_rows(matrix),
        )


class TypeScriptTestsStepTest(unittest.TestCase):
    # U39 addendum 2: the bun tests of the stop gate and the openai-siwc extension run in CI; since regime-cutover
    # U145 on every test cell, because the macOS cell is the one closest to the hosts the seats run on.
    DIRECTORIES = ("home/dot_agents/omp/hooks/tests", "home/dot_agents/omp/extensions/openai-siwc/tests")

    def step(self) -> str:
        return (
            TEST.read_text().split("      - name: Run the omp TypeScript tests\n", 1)[1].split("\n      - name: ", 1)[0]
        )

    def test_every_test_cell_runs_bun_over_each_directory(self) -> None:
        step = self.step()
        gate = "steps.decide.outputs.should_test == 'true'"
        self.assertIn(f"if: ${{{{ {gate} }}}}\n", step)
        # A later edit that narrows the step to one cell (an os or system term in the condition) fails here by name.
        condition = next(line for line in step.splitlines() if line.strip().startswith("if: "))
        for cell_term in ("matrix.os", "matrix.system", "runner.os"):
            with self.subTest(cell_term=cell_term):
                self.assertNotIn(cell_term, condition)
        self.assertIn("set -euo pipefail\n", step)
        self.assertIn('mise -C "${RUNNER_TEMP}/statusline-mise" install bun\n', step)
        self.assertIn(f"for tests in {' '.join(self.DIRECTORIES)}; do\n", step)
        # ADDENDUM 3: the suites and anything they spawn get the same bun, never mise's unresolvable shim.
        bun_lines = [line.strip() for line in step.splitlines() if '"${bun_bin}" test' in line]
        self.assertEqual(['PATH="${bun_bin_dir}:${PATH}" "${bun_bin}" test "./${tests}"'], bun_lines)
        self.assertIn('printf \'%s\\n\' "${bun_bin_dir}" >> "${GITHUB_PATH}"\n', step)
        # requests.test.ts imports the installed omp: the repository's own pinned, checksum-verified installer puts
        # it in a scratch HOME, and a missing package fails the step before bun runs.
        self.assertIn("bash -c 'source ./scripts/update-agent-assets.sh && update_omp'\n", step)
        self.assertIn('HOME="${omp_home}"', step)
        install = step.index("update_omp")
        self.assertLess(install, step.index('test -f "${OMP_PACKAGE_DIR}/package.json"\n'))
        self.assertLess(step.index('test -f "${OMP_PACKAGE_DIR}/package.json"\n'), step.index("for tests in"))
        for weakening in ("continue-on-error", "|| true", "set +e"):
            with self.subTest(weakening=weakening):
                self.assertNotIn(weakening, step)

    def run_install_block(self, step: str) -> tuple[Path, Path, list[str]]:
        """Run the step's omp install lines, from omp_home= to the update_omp call, against stubs.

        The stub curl records where update_omp downloads and then fails, so nothing is fetched; the outer TMPDIR
        points elsewhere, so a step that does not set its own TMPDIR downloads there.
        """
        lines = step.splitlines()
        first = next(i for i, line in enumerate(lines) if line.strip().startswith('omp_home="'))
        last = next(i for i, line in enumerate(lines) if "update_omp'" in line)
        block = "\n".join(line.strip() for line in lines[first : last + 1])
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        temp = Path(holder.name)
        runner_temp, outer_tmp, stubs, node = (
            temp / "runner-temp",
            temp / "outer-tmp",
            temp / "stubs",
            temp / "node/bin",
        )
        for directory in (runner_temp, outer_tmp, stubs, node):
            directory.mkdir(parents=True)
        log = temp / "curl.log"
        (stubs / "mise").write_text(f'#!/bin/sh\necho "{node.parent}"\n')
        (stubs / "npm").write_text("#!/bin/sh\nexit 0\n")
        (stubs / "bun").write_text("#!/bin/sh\nexit 0\n")
        (stubs / "curl").write_text(
            f'#!/bin/sh\nwhile [ $# -gt 0 ]; do [ "$1" = -o ] && echo "$2" >> "{log}"; shift; done\nexit 22\n'
        )
        for stub in stubs.iterdir():
            stub.chmod(0o755)
        script = f'set -euo pipefail\nbun_bin="{stubs}/bun"\n{block}\n'
        env = {**os.environ, "PATH": f"{stubs}{os.pathsep}{os.environ['PATH']}", "RUNNER_TEMP": str(runner_temp)}
        env["TMPDIR"] = str(outer_tmp)
        subprocess.run(["bash", "-c", script], cwd=ROOT, env=env, capture_output=True, text=True, check=False)
        downloads = log.read_text().split() if log.exists() else []
        return runner_temp, outer_tmp, downloads

    def test_the_omp_install_downloads_under_runner_temp(self) -> None:
        # Audit F2 of fed47ef6: update_omp's download directory comes from mktemp under TMPDIR, else /tmp.
        runner_temp, outer_tmp, downloads = self.run_install_block(self.step())
        self.assertEqual(1, len(downloads), downloads)
        self.assertTrue(Path(downloads[0]).is_relative_to(runner_temp / "omp-tmp"), downloads)
        self.assertEqual([], list(outer_tmp.iterdir()))

    def test_the_containment_check_sees_a_step_without_its_own_tmpdir(self) -> None:
        # The instrument shows the failure it detects: the same step without TMPDIR= downloads under the outer one.
        step = self.step().replace(' TMPDIR="${omp_tmp}"', "", 1)
        self.assertNotIn('TMPDIR="${omp_tmp}"', step)
        runner_temp, outer_tmp, downloads = self.run_install_block(step)
        self.assertEqual(1, len(downloads), downloads)
        self.assertTrue(Path(downloads[0]).is_relative_to(outer_tmp), downloads)
        self.assertFalse(Path(downloads[0]).is_relative_to(runner_temp))

    def test_each_directory_holds_bun_tests(self) -> None:
        # bun fails a filter without test files; this says which directory moved before CI does.
        for directory in self.DIRECTORIES:
            with self.subTest(directory=directory):
                self.assertTrue(sorted((ROOT / directory).glob("*.test.ts")), directory)


class InstallToolsChecksumToolTest(unittest.TestCase):
    """U109 rounds 21 and 22: the "Install tools" step picks the checksum tool from `sha256sum --version` and checks the
    chezmoi download through `curl | grep | checker`. The round 11 decision ran the producer inside `[[ ]]`, so its exit
    status was lost (round 21, audit of 76f1a732); the pipeline ran under the step's implicit `bash -e` with no
    `pipefail`, so a curl that printed the checksum line and then exited 42 let the step go on (round 22, audit of
    c01bb0a5). The body is run here as the runner runs a step that names no `shell:` (`bash -e {0}`), from a scratch
    directory with stubs first on PATH, up to the decision or through the whole pipeline."""

    GNU = "sha256sum (GNU coreutils) 9.4"
    DARWIN = "sha256sum (Darwin) 1.0"  # macOS 15 to 27: text_cmds md5.c `version()` prints this and exits 0
    TAG = "v2.66.0"
    ARTIFACT = "chezmoi_2.66.0_linux_amd64.tar.gz"  # the uname stub answers Linux/x86_64
    ARTIFACT_TEXT = "not a tarball: the pipeline checks these bytes and tar runs after it"
    PIPELINE_END = "shasum -a 256 --check --strict; fi)"

    @classmethod
    def body(cls, text: str) -> list[str]:
        """The step's `run:` body, dedented, one entry per line."""
        step = text.split("      - name: Install tools\n", 1)[1].split("\n      - name: ", 1)[0]
        return textwrap.dedent(step.split("        run: |\n", 1)[1]).splitlines()

    @classmethod
    def decision(cls, text: str) -> str:
        """The body from its first line to the line before the first download."""
        lines = cls.body(text)
        first_download = next(i for i, line in enumerate(lines) if line.startswith("curl "))
        block = "\n".join(lines[:first_download]) + "\n"
        assert "sha256_tool=" in block, block
        assert not any("curl" in line for line in block.splitlines() if not line.lstrip().startswith("#")), block
        return block

    @classmethod
    def checksum(cls, text: str) -> str:
        """The body from its first line through the checksum pipeline: both downloads, the `grep` and the checker."""
        lines = cls.body(text)
        end = next(i for i, line in enumerate(lines) if line.endswith(cls.PIPELINE_END))
        block = "\n".join(lines[: end + 1]) + "\n"
        assert 2 == sum(line.startswith("curl ") for line in block.splitlines()), block
        assert '| grep "  ${artifact}$"' in block and "github_release_attestation" not in block, block
        return block

    def run_body(
        self, block: str, stubs: dict[str, str | None], tools: tuple[str, ...] = ()
    ) -> subprocess.CompletedProcess[str]:
        """Run `block` as the runner runs a step that names no `shell:` (`bash --noprofile --norc -e`, no `pipefail`:
        round 21 ran `-eo pipefail`, the `shell: bash` form, which is not this step's), from a scratch directory whose
        PATH holds only the stubs: a `uname` answering Linux/x86_64, each `stubs` entry as a `sh` script (None: absent
        from PATH), and each of `tools` linked from the host. The scratch `scripts/lib/github-release.sh` answers a tag
        without the network. A `printf` after the block shows whether the step went on past it, and an EXIT trap
        prints the selection, or `none`, whatever the body did."""
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        scratch = Path(holder.name)
        stub_dir = scratch / "stubs"
        stub_dir.mkdir()
        (scratch / "scripts/lib").mkdir(parents=True)
        (scratch / "scripts/lib/github-release.sh").write_text(f"github_release_tag() {{ printf '{self.TAG}\\n'; }}\n")
        (stub_dir / "uname").write_text('#!/bin/sh\ncase "$1" in -s) echo Linux ;; -m) echo x86_64 ;; esac\n')
        for name, script in stubs.items():
            if script is not None:
                (stub_dir / name).write_text(f"#!/bin/sh\n{script}\n")
        for stub in stub_dir.iterdir():
            stub.chmod(0o755)
        for name in tools:
            tool = shutil.which(name)
            if tool is not None:
                (stub_dir / name).symlink_to(tool)
        script = scratch / "install-tools.sh"
        script.write_text(
            'trap \'printf "selected=%s\\n" "${sha256_tool-none}"\' EXIT\n' + block + "printf 'went on\\n'\n"
        )
        bash = shutil.which("bash")
        assert bash is not None
        env = {
            "PATH": str(stub_dir),
            "HOME": str(scratch),
            "OS": "ubuntu-24.04",
            "SYSTEM": "client",
            "RUNNER_TEMP": str(scratch),
        }
        return subprocess.run(
            [bash, "--noprofile", "--norc", "-e", str(script)],
            cwd=scratch,
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
        )

    def run_decision(self, block: str, sha256sum: str | None) -> subprocess.CompletedProcess[str]:
        return self.run_body(block, {"sha256sum": sha256sum})

    def curl(self, checksums: str, status: int) -> str:
        """A `curl` that writes ARTIFACT_TEXT to the path after `-o` (the first download, exit 0) and otherwise prints
        `checksums` and exits with `status` (the checksums download)."""
        printed = "".join(f"printf '%s\\n' '{line}'\n" for line in checksums.splitlines())
        return (
            'out=\nwhile [ $# -gt 0 ]; do case "$1" in -o) out="$2"; shift ;; esac; shift; done\n'
            f"if [ -n \"${{out}}\" ]; then printf '%s\\n' '{self.ARTIFACT_TEXT}' > \"${{out}}\"; exit 0; fi\n"
            f"{printed}exit {status}\n"
        )

    def checksums(self, digest: str) -> str:
        """A release checksums file: the artifact's line among two other platforms', so the `grep` selects."""
        return (
            f"{'0' * 64}  chezmoi_2.66.0_darwin_arm64.tar.gz\n"
            f"{digest}  {self.ARTIFACT}\n"
            f"{'f' * 64}  chezmoi_2.66.0_linux_arm64.tar.gz\n"
        )

    def test_the_decision_reads_every_status_of_sha256sum(self) -> None:
        # A failing `sha256sum --version` ends the step with its status before any tool is selected; a banner that
        # is not GNU's, or no sha256sum at all, selects shasum. On 76f1a732 the exit-42 cases went on, one with
        # sha256sum selected and one with shasum.
        block = self.decision(TEST.read_text())
        for case, stub, status, stdout in (
            ("GNU banner, exit 0", f"echo '{self.GNU}'\nexit 0", 0, "went on\nselected=sha256sum\n"),
            ("GNU banner, exit 42", f"echo '{self.GNU}'\nexit 42", 42, "selected=none\n"),
            ("no output, exit 42", "exit 42", 42, "selected=none\n"),
            ("no sha256sum on PATH", None, 0, "went on\nselected=shasum\n"),
            ("the BSD banner, exit 0", f"echo '{self.DARWIN}'\nexit 0", 0, "went on\nselected=shasum\n"),
        ):
            with self.subTest(case=case):
                result = self.run_decision(block, stub)
                self.assertEqual((status, stdout), (result.returncode, result.stdout), result.stderr)

    def test_the_checksum_pipeline_ends_the_step_on_every_producers_status(self) -> None:
        # Round 22 (audit of c01bb0a5): the pipeline is `curl | grep | checker` and the step names no `shell:`, so
        # without the body's own `set -o pipefail` only the checker's status reached `bash -e`. A curl that prints
        # the valid file and exits 42 ends the step with 42 (on c01bb0a5 it went on with 0); the real `grep` and
        # the host's checker (the decision selects it from the real `sha256sum`, shasum where there is none or it
        # is BSD's) pass the valid file, and fail an empty one or a wrong digest on both heads.
        self.assertTrue(shutil.which("shasum") or shutil.which("sha256sum"), "a checker on the host's PATH")
        block = self.checksum(TEST.read_text())
        digest = hashlib.sha256(f"{self.ARTIFACT_TEXT}\n".encode()).hexdigest()
        for case, checksums, curl_status, status, went_on in (
            ("the valid file, curl exit 0", self.checksums(digest), 0, 0, True),
            ("the valid file, then curl exit 42", self.checksums(digest), 42, 42, False),
            ("nothing printed, curl exit 0", "", 0, 1, False),
            ("a wrong digest, curl exit 0", self.checksums("1" * 64), 0, 1, False),
        ):
            with self.subTest(case=case):
                result = self.run_body(
                    block, {"curl": self.curl(checksums, curl_status)}, tools=("grep", "sha256sum", "shasum")
                )
                self.assertEqual(
                    (status, went_on),
                    (result.returncode, "went on\n" in result.stdout),
                    (result.stdout, result.stderr),
                )
                if went_on:
                    self.assertIn(f"{self.ARTIFACT}: OK\n", result.stdout)

    def test_the_body_sets_pipefail_before_anything_else(self) -> None:
        # The producers' statuses reach `bash -e` only through the body's own option, since the step keeps the
        # runner's default shell (tests/unit/test_apt_mirror.py reads the step with no `shell:` key).
        self.assertEqual("set -euo pipefail", self.body(TEST.read_text())[0])

    def test_the_decision_is_spelled_in_literal_command_words(self) -> None:
        # The tree rule of tests/unit/test_apt_mirror.py reads every command word; the decision gives it `command`,
        # `sha256sum` and assignments, never an expansion in command position, and no `[[ ]]` around the producer.
        block = self.decision(TEST.read_text())
        self.assertIn('sha256sum_banner="$(sha256sum --version)"\n', block)
        self.assertNotIn('[[ "$(sha256sum', block)
        self.assertNotIn("2> /dev/null)", block)


class RenderOnlySubtreesTest(unittest.TestCase):
    def test_the_bootstrap_decision_allows_exactly_the_render_only_subtrees(self) -> None:
        allowed = re.search(r"paths_match -qv '\^home/\(([^)]+)\)/'", REMOTE.read_text())
        self.assertIsNotNone(allowed)
        self.assertEqual(set(allowed.group(1).split("|")), set(RENDER_ONLY))

    def test_each_allowed_subtree_is_scanned_at_the_whole_of_its_target(self) -> None:
        # Audit F1 of fed47ef6: dot_local/bin was allowed while only .local/bin/common and .local/bin/server were
        # scanned, so a new home/dot_local/bin/executable_mise would skip the bootstrap unscanned. Every allowed
        # subtree's own target is scanned, or for the skills every entry under it.
        for subtree, targets in RENDER_ONLY.items():
            with self.subTest(subtree=subtree):
                whole = target_of(subtree)
                if targets == [f"{whole}/{{skill}}"]:
                    self.assertTrue(skill_names())
                else:
                    self.assertEqual(targets, [whole])

    def test_target_of_follows_chezmoi_source_names(self) -> None:
        cases = {
            "dot_local/bin/common": ".local/bin/common",
            "dot_local/bin/executable_mise": ".local/bin/mise",
            "dot_claude/rules/symlink_regime.md.tmpl": ".claude/rules/regime.md",
            "private_dot_ssh/private_executable_x": ".ssh/x",
        }
        for source, target in cases.items():
            with self.subTest(source=source):
                self.assertEqual(target_of(source), target)

    def test_the_bootstrap_neither_executes_nor_reads_a_render_only_target(self) -> None:
        files = [
            path
            for reader in BOOTSTRAP_READERS
            for path in ([ROOT / reader] if (ROOT / reader).is_file() else sorted((ROOT / reader).rglob("*")))
            if path.is_file()
        ]
        self.assertGreater(len(files), 20)
        self.assertEqual([], render_only_reads(files))

    def test_the_scan_sees_a_reader_of_a_render_only_target(self) -> None:
        # The instrument shows the failure it detects: an installer that runs a lever, includes a skill source or
        # reads a seat policy; a longer name that only starts like a target is not a read.
        with tempfile.TemporaryDirectory() as temp:
            cases = {
                "lever": ('"${HOME}/.local/bin/common/hcom-seat" --check\n', True),
                "include": ('{{ include "dot_agents/skills/hcom-worker/SKILL.md" }}\n', True),
                "policy": ("cat ~/.agents/omp/policies/worker.yml\n", True),
                "longer-name": ("ls ~/.agents/skills/hcom-worker-extra\n", False),
            }
            for name, (text, found) in cases.items():
                with self.subTest(case=name):
                    reader = Path(temp) / f"{name}.sh"
                    reader.write_text(text)
                    self.assertEqual(found, bool(render_only_reads([reader])))


class ApplyCheckImageCacheTest(unittest.TestCase):
    """U610 (runs 44475635634 and 44497689181, cancelled at the job's 15-minute timeout inside the image's apt-get):
    the apply-container job builds the image with buildx against the Actions cache, with build arguments from
    `make docker-build-args`, so `make apply-check` after it reuses the image; the Dockerfile's apt-get is bounded."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.job = load_yaml(APPLY_CHECK)["jobs"]["apply-container"]
        cls.steps = cls.job["steps"]
        cls.lock = lockfile()

    def step_using(self, action: str) -> dict:
        found = [step for step in self.steps if str(step.get("uses", "")).startswith(f"{action}@")]
        self.assertEqual(1, len(found), f"one step uses {action}: {found}")
        return found[0]

    def test_the_image_is_built_with_buildx_against_the_actions_cache(self) -> None:
        build = self.step_using("docker/build-push-action")["with"]
        self.assertEqual("type=gha", build["cache-from"])
        self.assertEqual("type=gha,mode=max", build["cache-to"])
        # The checked-out tree and its Dockerfile, loaded into the daemon under the name make docker-image inspects.
        self.assertEqual((".", "Dockerfile", True), (build["context"], build["file"], build["load"]))
        self.assertEqual("dotfiles", build["tags"])
        self.assertIn("DOCKER_IMAGE_NAME=dotfiles\n", MAKEFILE.read_text())
        # A plain single-platform image, as `docker build` makes it: no attestation manifest around it.
        self.assertIs(False, build["provenance"])
        self.assertEqual(
            [f"{name}=${{{{ steps.image.outputs.{name} }}}}" for name in BUILD_ARGS], build["build-args"].splitlines()
        )

    def test_the_steps_run_in_the_order_the_cache_needs(self) -> None:
        # Checkout, the arguments, the builder, the build, then make apply-check; nothing conditional in between.
        names = [str(step["uses"]).split("@", 1)[0] if "uses" in step else str(step["run"]) for step in self.steps]
        self.assertEqual(
            [
                "actions/checkout",
                'make docker-build-args >> "${GITHUB_OUTPUT}"',
                "docker/setup-buildx-action",
                "docker/build-push-action",
                "make apply-check",
            ],
            names,
        )
        self.assertEqual("image", self.steps[1]["id"])
        self.assertFalse([step for step in self.steps if "if" in step or "continue-on-error" in step])

    def test_the_build_arguments_come_from_make_docker_build_args(self) -> None:
        # The resolve step holds the one credential the host side needs; the build step gets none.
        resolve, build = self.steps[1], self.step_using("docker/build-push-action")
        self.assertEqual(["GITHUB_TOKEN"], list(resolve["env"]))
        self.assertNotIn("env", build)
        text = MAKEFILE.read_text()
        # The target prints exactly the names the workflow reads, and make docker-image passes the same five.
        self.assertIn(PRINTED, text)
        self.assertIn(f'{PRINTED} "$${{username}}" "$${{apt_week}}"', text)
        (build_line,) = [line for line in text.splitlines() if '" build -t $(DOCKER_IMAGE_NAME)' in line]
        self.assertEqual(list(BUILD_ARGS), re.findall(r"--build-arg ([A-Z0-9_]+)=", build_line))

    @unittest.skipUnless(MAKE, "make is not installed")
    def test_make_docker_build_args_verifies_before_it_prints(self) -> None:
        # The dry run shows the recipe's shell: the same resolution and host-side verification as docker-image
        # (test_github_release.py runs both with stubs), then the four lines, and no build.
        result = subprocess.run(
            [MAKE, "-n", "CONTAINER_ENGINE=docker", "docker-build-args"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        shell = result.stdout
        for needle in (
            "github_release_tag twpayne/chezmoi",
            "github_release_verified_sha256 twpayne/chezmoi",
            WEEK_READ,
            f'{PRINTED} "${{username}}" "${{apt_week}}"',
        ):
            self.assertIn(needle, shell)
        self.assertNotIn(" build ", shell)
        self.assertLess(shell.index("github_release_verified_sha256"), shell.index("printf 'USERNAME="))

    def test_the_buildx_actions_are_pinned_as_the_kit_pins_every_action(self) -> None:
        row = self.lock["workflows"][".github/workflows/apply-check.yml"]
        for action, repo_id in BUILDX_ACTIONS.items():
            with self.subTest(action=action):
                reference = self.step_using(action)["uses"]
                tag = reference.split("@", 1)[1]
                self.assertRegex(tag, r"\Av\d+\.\d+\.\d+\Z")
                entry = self.lock["dependencies"][reference]
                self.assertEqual(tag, entry["ref"])
                self.assertRegex(entry["commit"], r"\Asha1-[0-9a-f]{40}\Z")
                self.assertEqual((DOCKER_OWNER_ID, repo_id), (entry["owner_id"], entry["repo_id"]))
                self.assertNotIn("uses", entry)  # both are node actions with no transitive action
                self.assertIn(reference, row)

    def test_the_job_timeout_stays_at_fifteen_minutes(self) -> None:
        self.assertEqual(15, self.job["timeout-minutes"])

    def test_every_apt_get_of_the_dockerfile_carries_the_runner_bounds(self) -> None:
        # Each call, from its name to the next operator, on the logical line (continuations joined as the shell
        # joins them): the two options first, then the verb, and no second option that could reopen them.
        logical = DOCKERFILE.read_text().replace("\\\n", " ")
        calls = [call.strip() for call in re.findall(r"\bapt-get\b[^&|;]*", logical)]
        self.assertEqual(2, len(calls), calls)
        for call in calls:
            with self.subTest(call=call):
                words = call.split()
                self.assertEqual(["apt-get", *APT_BOUNDS.split()], words[:5])
                self.assertIn(words[5], ("update", "install"))
                self.assertFalse([word for word in words[6:] if word.startswith(("-o", "-c", "--option", "--config"))])

    def test_the_scan_sees_an_unbounded_apt_get(self) -> None:
        # The instrument shows the failure it detects: the Dockerfile before U610.
        before = DOCKERFILE.read_text().replace(f"apt-get {APT_BOUNDS} ", "apt-get ")
        self.assertNotIn(APT_BOUNDS, before)
        calls = re.findall(r"\bapt-get\b[^&|;]*", before.replace("\\\n", " "))
        self.assertEqual(2, len(calls))
        self.assertFalse([call for call in calls if call.split()[1:5] == APT_BOUNDS.split()])

    def dockerfile_instructions(self) -> tuple[list[str], int]:
        """The Dockerfile's instructions on their logical lines (continuations joined as the parser joins them,
        comments and blank lines left out), and the index of the one RUN that calls apt-get."""
        logical = DOCKERFILE.read_text().replace("\\\n", " ")
        instructions = [line.strip() for line in logical.splitlines() if line.strip() and not line.startswith("#")]
        (index,) = [i for i, line in enumerate(instructions) if re.search(r"\bapt-get\b", line)]
        return instructions, index

    def test_the_apt_step_ends_under_a_wall_clock_bound_inside_the_jobs_timeout(self) -> None:
        # Round 3 (verdict of 1c416678, P1 at Dockerfile:15): Acquire::http::Timeout bounds the silence between bytes,
        # not the transfer, so a mirror trickling 105 MB at under 100 KB/s ran the layer past the job's 15 minutes.
        # coreutils timeout (in ubuntu:24.04) bounds the whole step, under the job's timeout-minutes; both numbers
        # are read from their files, none copied here.
        instructions, index = self.dockerfile_instructions()
        match = re.fullmatch(r"RUN timeout (\d+) sh -c '([^']*)'", instructions[index])
        self.assertIsNotNone(match, instructions[index])
        seconds, command = int(match.group(1)), match.group(2)
        self.assertLess(seconds, self.job["timeout-minutes"] * 60)
        # Both calls, the update and the install, run inside the bounded command, nothing after it on the line.
        self.assertEqual(2, len(re.findall(r"\bapt-get\b", command)))
        self.assertRegex(command, r"\Aapt-get .* update &&\s+apt-get .* install -y --no-install-recommends\s.*\S\Z")

    def test_the_scan_sees_the_apt_step_without_the_wall_clock_bound(self) -> None:
        # The instrument shows the failure it detects: the Dockerfile of round 1 (1c416678), apt's idle bounds alone.
        instructions, index = self.dockerfile_instructions()
        before = re.sub(r"\ARUN timeout \d+ sh -c '([^']*)'\Z", r"RUN \1", instructions[index])
        self.assertTrue(before.startswith("RUN apt-get "), before)
        self.assertIsNone(re.fullmatch(r"RUN timeout (\d+) sh -c '([^']*)'", before))

    def test_the_apt_layer_is_keyed_by_the_iso_week(self) -> None:
        # Round 3 (verdict of 1c416678, P2 at apply-check.yml:64): a cached apt layer kept its build day's packages for
        # as long as the Dockerfile was unchanged. ARG APT_WEEK right before the apt RUN puts the week into the
        # layer's cache key (every RUN after an ARG uses it implicitly); the workflow passes it from make
        # docker-build-args, and make docker-image passes the same value, so a local build keys the same way.
        instructions, index = self.dockerfile_instructions()
        self.assertEqual("ARG APT_WEEK", instructions[index - 1])
        self.assertEqual([index - 1], [i for i, line in enumerate(instructions) if "APT_WEEK" in line])
        build = self.step_using("docker/build-push-action")["with"]
        self.assertIn("APT_WEEK=${{ steps.image.outputs.APT_WEEK }}", build["build-args"].splitlines())
        text = MAKEFILE.read_text()
        self.assertIn(WEEK_READ.replace("$", "$$"), text)
        (build_line,) = [line for line in text.splitlines() if '" build -t $(DOCKER_IMAGE_NAME)' in line]
        self.assertIn('--build-arg APT_WEEK="$${apt_week}"', build_line)
        self.assertIn("APT_WEEK=%s\\n", text)
        # The format is the ISO week: the ISO year, a W, the two-digit week (2026-W47 on the day of this round).
        week = subprocess.run(["date", "-u", "+%G-W%V"], text=True, capture_output=True, check=True).stdout.strip()
        self.assertRegex(week, r"\A\d{4}-W(0[1-9]|[1-4]\d|5[0-3])\Z")


if __name__ == "__main__":
    unittest.main()
