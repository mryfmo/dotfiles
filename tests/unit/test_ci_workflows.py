"""The CI critical path (U39): the sharded unit-test runner and the render-only subtrees the bootstrap may skip."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHARDS = ROOT / "scripts/ci/unittest-shards.py"
REMOTE = ROOT / ".github/workflows/remote.yaml"
# The render-only subtrees of home/ and the targets chezmoi gives them; the bootstrap must neither execute nor read
# any of these targets, or a change there needs the full bootstrap again.
RENDER_ONLY = {
    "dot_agents/skills": [".agents/skills/{skill}"],
    "dot_agents/omp/policies": [".agents/omp/policies"],
    "dot_claude/rules": [".claude/rules"],
    "dot_config/claude/rules": [".config/claude/rules"],
    "dot_local/bin": [".local/bin/common", ".local/bin/server"],
}
# What setup.sh runs on a host: itself, the installers, the libraries and the chezmoi scripts that include them.
BOOTSTRAP_READERS = (
    "setup.sh",
    "install",
    "scripts/lib",
    "scripts/update-agent-assets.sh",
    "scripts/gh-auth.sh",
    "home/.chezmoiscripts",
)


def render_only_reads(files: list[Path]) -> list[str]:
    """Each `file: target` where a bootstrap reader names a render-only source path or the target chezmoi gives it."""
    skills = sorted(path.name for path in (ROOT / "home/dot_agents/skills").iterdir() if path.is_dir())
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


def shards(start: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SHARDS), "--start", str(start), *args],
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
            self.assertIn("4 tests in 2 modules", result.stdout)
            self.assertRegex(result.stdout, r"\nRan 4 tests in [0-9.]+s \(2 modules, 2 jobs\)\nOK \(skipped=1\)\n\Z")
            # Each module's own verbose unittest output is printed, so a failure reads as it does in the serial run.
            self.assertIn("test_one (test_a.A", result.stdout)

    def test_a_failing_test_fails_the_run_and_names_its_module(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            failing = "class F(unittest.TestCase):\n    def test_f(self):\n        self.assertEqual(1, 2)\n"
            start = suite(temp, {"test_a.py": PASSING, "test_f.py": failing})
            result = shards(start, "--jobs", "2")
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED module test_f.py: exit 1, FAILED", result.stdout)
            self.assertTrue(result.stdout.rstrip().endswith("FAILED (failures=1, skipped=1)"), result.stdout)

    def test_a_module_that_does_not_import_fails_the_run(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            start = suite(temp, {"test_a.py": PASSING, "test_broken.py": "import no_such_module_u39\n"})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED module test_broken.py", result.stdout)

    def test_a_module_that_dies_without_a_summary_fails_the_run(self) -> None:
        # A shard that exits 0 before unittest prints its summary must not read as a pass.
        with tempfile.TemporaryDirectory() as temp:
            dying = "import os\n\nclass D(unittest.TestCase):\n    def test_d(self):\n        os._exit(0)\n"
            start = suite(temp, {"test_a.py": PASSING, "test_d.py": dying})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("FAILED module test_d.py: exit 0, no unittest summary", result.stdout)

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
            self.assertIn("6 tests in 1 modules", result.stdout)
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

    def test_an_empty_start_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            start = suite(temp, {})
            result = shards(start)
            self.assertEqual(result.returncode, 1)
            self.assertIn("found no test modules", result.stderr)


class MakeUnitTestTest(unittest.TestCase):
    def make(self, *args: str) -> str:
        env = {key: value for key, value in os.environ.items() if key not in {"UNIT_TEST_JOBS", "MAKEFLAGS"}}
        return subprocess.run(
            ["make", "-n", "unit-test", *args], cwd=ROOT, env=env, capture_output=True, text=True, check=True
        ).stdout

    def test_the_serial_form_is_the_unchanged_discover_command(self) -> None:
        self.assertEqual(self.make("UNIT_TEST_JOBS=1"), "uv run python -m unittest discover -s tests/unit -v\n")

    def test_the_default_runs_the_shards_on_every_cpu(self) -> None:
        self.assertEqual(self.make(), "uv run python scripts/ci/unittest-shards.py --start tests/unit --jobs 0\n")
        self.assertIn("--jobs 3\n", self.make("UNIT_TEST_JOBS=3"))


class RenderOnlySubtreesTest(unittest.TestCase):
    def test_the_bootstrap_decision_allows_exactly_the_render_only_subtrees(self) -> None:
        allowed = re.search(r"paths_match -qv '\^home/\(([^)]+)\)/'", REMOTE.read_text())
        self.assertIsNotNone(allowed)
        self.assertEqual(set(allowed.group(1).split("|")), set(RENDER_ONLY))

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


if __name__ == "__main__":
    unittest.main()
