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
TEST = ROOT / ".github/workflows/test.yaml"
# The render-only subtrees of home/ and the targets chezmoi gives them; the bootstrap must neither execute nor read
# any of these targets, or a change there needs the full bootstrap again.
RENDER_ONLY = {
    # Per skill, not the whole of .agents/skills: the installers own agmsg, crit*, understand* and poteto-mode there.
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


class MakeUnitTestTest(unittest.TestCase):
    def make(self, *args: str) -> str:
        # A make that runs this suite passes MAKELEVEL and MAKEFLAGS down; GNU make then prints "Entering directory".
        env = {
            key: value for key, value in os.environ.items() if key not in {"UNIT_TEST_JOBS", "MAKEFLAGS", "MAKELEVEL"}
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


class TypeScriptTestsStepTest(unittest.TestCase):
    # U39 addendum 2: the bun tests of the stop gate and the openai-siwc extension run in CI.
    DIRECTORIES = ("home/dot_agents/omp/hooks/tests", "home/dot_agents/omp/extensions/openai-siwc/tests")

    def step(self) -> str:
        return (
            TEST.read_text().split("      - name: Run the omp TypeScript tests\n", 1)[1].split("\n      - name: ", 1)[0]
        )

    def test_the_ubuntu_client_cell_runs_bun_over_each_directory(self) -> None:
        step = self.step()
        gate = "steps.decide.outputs.should_test == 'true' && matrix.os == 'ubuntu-24.04' && matrix.system == 'client'"
        self.assertIn(f"if: ${{{{ {gate} }}}}\n", step)
        self.assertIn("set -euo pipefail\n", step)
        self.assertIn('mise -C "${RUNNER_TEMP}/statusline-mise" install bun\n', step)
        self.assertIn(f"for tests in {' '.join(self.DIRECTORIES)}; do\n", step)
        self.assertIn('"${bun_bin}" test "./${tests}"\n', step)
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


if __name__ == "__main__":
    unittest.main()
