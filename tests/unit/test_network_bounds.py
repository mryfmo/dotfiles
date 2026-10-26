"""Every CI Bats run fails a stalled test by name, and every scripted network call ends (regime-cutover U99).

The convention, for setup.sh, install/**, scripts/** (make update, the levers, the CI helpers) and the workflow
steps: curl gets `--connect-timeout 30` and fails a transfer under 1 KB/s for 60 s (`--speed-limit 1024
--speed-time 60`); wget gets `--timeout=60 --tries=3`; `snap install` runs under `timeout`. apt-get needs nothing:
its http and https methods give up a connection or a read that stays silent for Acquire::http::Timeout, 30 s unless
configured (apt methods/basehttp.cc), and https inherits the http value.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from agent_home_isolation import isolate_agent_homes, restore_agent_homes


def setUpModule() -> None:
    isolate_agent_homes()


def tearDownModule() -> None:
    restore_agent_homes()


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts/run_unit_test.sh"
SUPERVISOR = ROOT / "scripts/ci/run-bats.py"
WORKFLOWS = ROOT / ".github/workflows"
BASH = shutil.which("bash") or "/bin/bash"
# Every file that runs a network command on a host or a runner: the bootstrap, the installers, everything under
# scripts/ (update-agent-assets.sh and upgrade-tools.sh behind make update, the release helper, the orchestrator
# levers, the CI helpers) and the workflows. Compiled Python caches are not sources.
NETWORK_SOURCES = [
    ROOT / "setup.sh",
    *sorted((ROOT / "install").rglob("*.sh")),
    *sorted(p for p in (ROOT / "scripts").rglob("*") if p.is_file() and "__pycache__" not in p.parts),
    *sorted(WORKFLOWS.glob("*.y*ml")),
]
# The only lines that name a download without running it. update-agent-assets.sh's manifest_record writes, as data in
# ~/.agents/.installed-manifest.json, the source each asset came from ("curl -fsSL <url>", then its sha256 check); it
# fetches nothing, and the bound flags say nothing about where an asset came from.
NOT_A_CALL = ("manifest_record ",)
# A command, not a mention: the tool followed by an option, or `snap install`/`snap refresh`.
CURL = re.compile(r"(?<![\w.-])curl\s+-")
WGET = re.compile(r"(?<![\w.-])wget\s+-")
SNAP = re.compile(r"(?<![\w.-])snap\s+(?:install|refresh)\b")
# A bare Bats run in a workflow: `bats` as a command word, not run_bats, bats-core or a package list.
BARE_BATS = re.compile(r"(?<![\w/.-])bats\s")


def logical_lines(path: Path) -> list[tuple[int, str]]:
    """The file's commands with backslash continuations joined and comment lines left out, with first line numbers."""
    lines: list[tuple[int, str]] = []
    pending, start = "", 0
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not pending and line.lstrip().startswith("#"):
            continue
        if not pending:
            start = number
        if line.endswith("\\"):
            pending += line[:-1] + " "
            continue
        lines.append((start, pending + line))
        pending = ""
    return lines


def commands(path: Path) -> list[tuple[int, str]]:
    """logical_lines without the messages a script prints and the NOT_A_CALL records, which name a command they do
    not run."""
    return [
        (number, line)
        for number, line in logical_lines(path)
        if not line.lstrip().startswith(("printf ", "echo ", *NOT_A_CALL))
    ]


class NetworkBoundTest(unittest.TestCase):
    def test_every_curl_wget_and_snap_call_carries_its_bound(self) -> None:
        unbounded = []
        for path in NETWORK_SOURCES:
            for number, line in commands(path):
                where = f"{path.relative_to(ROOT)}:{number}: {line.strip()}"
                if CURL.search(line) and not (
                    "--connect-timeout" in line
                    and ("--max-time" in line or ("--speed-limit" in line and "--speed-time" in line))
                ):
                    unbounded.append(where)
                if WGET.search(line) and not ("--timeout=" in line and "--tries=" in line):
                    unbounded.append(where)
                if SNAP.search(line) and not re.search(r"\btimeout\s+(?:--kill-after=\S+\s+)?\S+\s+snap\s", line):
                    unbounded.append(where)
        self.assertEqual([], unbounded)

    def test_the_scan_sees_the_calls_it_checks(self) -> None:
        # A scan that matched nothing would pass every tree, so it must find these calls.
        found = {
            (path.relative_to(ROOT).as_posix(), kind)
            for path in NETWORK_SOURCES
            for _, line in commands(path)
            for kind, pattern in (("curl", CURL), ("wget", WGET), ("snap", SNAP))
            if pattern.search(line)
        }
        for expected in (
            ("setup.sh", "curl"),
            ("setup.sh", "wget"),
            ("scripts/lib/github-release.sh", "wget"),
            ("install/common/aws_cli.sh", "curl"),
            ("install/ubuntu/client/docker.sh", "curl"),
            ("install/ubuntu/client/misc.sh", "snap"),
            ("scripts/update-agent-assets.sh", "curl"),
            (".github/workflows/test.yaml", "curl"),
            (".github/workflows/agent-assets.yml", "curl"),
        ):
            self.assertIn(expected, found)

    def test_only_records_are_left_out(self) -> None:
        # The exclusion takes manifest_record lines and nothing else: each names curl and runs no command itself.
        records = [
            line
            for path in NETWORK_SOURCES
            for _, line in logical_lines(path)
            if line.lstrip().startswith(NOT_A_CALL) and CURL.search(line)
        ]
        self.assertTrue(records)
        for line in records:
            self.assertRegex(line.lstrip(), r'^manifest_record "\w+" installer ')
            self.assertNotRegex(line, r"\$\(|`")


class RunBatsBoundTest(unittest.TestCase):
    """run_bats (scripts/run_unit_test.sh, then scripts/ci/run-bats.py) against a fake `bats` that writes
    Bats' extended stream."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="run-bats-"))
        self.addCleanup(shutil.rmtree, self.temp, True)
        (self.temp / "bin").mkdir()
        # The python3 the runner calls, so the case does not depend on the host's.
        (self.temp / "bin/python3").symlink_to(sys.executable)
        self.pids = self.temp / "pids"
        self.addCleanup(self.kill_recorded)

    def kill_recorded(self) -> None:
        for pid in self.recorded():
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass

    def recorded(self) -> list[int]:
        return [int(line) for line in self.pids.read_text().split()] if self.pids.exists() else []

    def fake_bats(self, body: str) -> None:
        script = self.temp / "bin/bats"
        script.write_text(f'#!{BASH}\nprintf "%s\\n" "$*" > "{self.temp}/args"\n' + textwrap.dedent(body))
        script.chmod(0o755)

    def run_bats(self, bound: str, *args: str, **extra: str) -> tuple[subprocess.CompletedProcess[str], float]:
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "TMPDIR": str(self.temp),
            "BATS_PER_TEST_TIMEOUT": bound,
            "PIDS": str(self.pids),
            **extra,
        }
        started = time.monotonic()
        # capture_output returns only once every writer of the output pipe is gone, as CI's step would.
        result = subprocess.run(
            [BASH, "-c", 'source "$1" && shift && run_bats "$@"', "_", str(RUNNER), *args],
            env=env, capture_output=True, text=True, timeout=60, check=False,
        )  # fmt: skip
        return result, time.monotonic() - started

    def survivors(self) -> list[int]:
        """The recorded pids still running (a zombie has exited), after up to 5 s for init to reap them."""
        left: list[int] = []
        for _ in range(50):
            out = subprocess.run(["ps", "-A", "-o", "pid=", "-o", "stat="], capture_output=True, text=True, check=True)
            live = {int(f[0]) for f in (line.split() for line in out.stdout.splitlines()) if not f[1].startswith("Z")}
            left = [pid for pid in self.recorded() if pid in live]  # lint-comparisons: allow integer-pids
            if not left:
                return []
            time.sleep(0.1)
        return left

    def test_a_stalled_test_fails_by_name_and_every_process_it_started_stops(self) -> None:
        # The stalled test's grandchild is what kept the PR #570 jobs alive until the job timeout.
        self.fake_bats(
            """\
            printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] fast\\nok 1 [x] fast\\nbegin 2 [x] misc\\n'
            echo $$ >> "${PIDS}"
            sleep 300 &
            echo $! >> "${PIDS}"
            wait
            """
        )
        result, elapsed = self.run_bats("2", "-r", "tests/x/")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 4)
        self.assertEqual(
            "1..2\nok 1 [x] fast\nnot ok 2 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT); stopping Bats\n",
            result.stdout,
        )
        self.assertEqual(2, len(self.recorded()))
        self.assertEqual([], self.survivors())
        self.assertEqual("--formatter cat -r tests/x/\n", (self.temp / "args").read_text())

    def test_descendants_that_leave_the_process_group_or_the_session_are_stopped_too(self) -> None:
        # Audit of f35e47e6: an exported SHELLOPTS=monitor gives Bats' pipeline children process groups of their
        # own. Here one child also calls setpgid itself, one calls setsid, and both hold Bats' output open.
        leave = 'import os, sys, time; os.{}; open(sys.argv[1], "a").write(f"{{os.getpid()}}\\n"); time.sleep(300)'
        self.fake_bats(
            f"""\
            printf '1..1\\nbegin 1 [x] stall\\n'
            echo $$ >> "${{PIDS}}"
            python3 -c '{leave.format("setpgid(0, 0)")}' "${{PIDS}}" | cat &
            echo $! >> "${{PIDS}}"
            python3 -c '{leave.format("setsid()")}' "${{PIDS}}" &
            while [ "$(wc -l < "${{PIDS}}")" -lt 4 ]; do sleep 0.05; done
            wait
            """
        )
        result, elapsed = self.run_bats("2", "tests/x.bats", SHELLOPTS="monitor")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok 1 [x] stall # timeout after 2 s", result.stdout)
        self.assertEqual(4, len(self.recorded()))
        self.assertEqual([], self.survivors())

    def test_output_from_a_running_test_does_not_extend_its_bound(self) -> None:
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] chatty\\n'
            while true; do printf '# still running\\n'; sleep 0.2; done
            """
        )
        result, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok 1 [x] chatty # timeout after 2 s", result.stdout)

    def test_loading_the_files_is_bounded_too(self) -> None:
        # Bats sources every file before its plan line; nothing runs Bats outside the bound (no `bats --count`).
        self.fake_bats("sleep 300\n")
        result, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok - Bats printed nothing for 2 s outside a test", result.stdout)

    def test_a_run_within_the_bound_keeps_bats_lines_and_status(self) -> None:
        self.fake_bats(
            """\
            printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] a\\nok 1 [x] a\\nbegin 2 [x] b\\n# output of b\\n'
            printf 'not ok 2 [x] b\\n'
            exit 1
            """
        )
        result, _ = self.run_bats("30", "tests/x.bats")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("1..2\nok 1 [x] a\n# output of b\nnot ok 2 [x] b\n", result.stdout)

    def test_a_run_that_plans_no_test_fails(self) -> None:
        for body, shown in (("printf '1..0\\n'\n", "0"), ("exit 0\n", "nothing")):
            with self.subTest(plan=shown):
                self.fake_bats(body)
                result, _ = self.run_bats("30", "--filter-tags", "common,ubuntu:client", "tests/files/ubuntu.bats")
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"expected at least one test; Bats planned {shown}", result.stderr)

    def test_a_process_a_passing_run_leaves_behind_is_stopped(self) -> None:
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] a\\nok 1 [x] a\\n'
            sleep 300 &
            echo $! >> "${PIDS}"
            exit 0
            """
        )
        result, elapsed = self.run_bats("30", "tests/x.bats")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 10)
        self.assertIn("Bats exited and left 1 process(es) running", result.stderr)
        self.assertEqual([], self.survivors())


class CiBatsRunTest(unittest.TestCase):
    """Every Bats run CI starts goes through run_bats, and nothing else starts Bats."""

    def test_the_runner_calls_bats_only_through_run_bats(self) -> None:
        calls = [line.strip() for _, line in logical_lines(RUNNER) if BARE_BATS.search(line)]
        self.assertEqual([], calls)
        self.assertIn('["bats", "--formatter", "cat", *argv]', SUPERVISOR.read_text())
        text = RUNNER.read_text()
        for function in ("run_common_test", "run_os_specific_test", "run_files_test"):
            start = text.index(f"function {function}() {{\n")
            self.assertIn("run_bats ", text[start : text.index("\n}\n", start)], function)

    def test_no_workflow_runs_bats_directly(self) -> None:
        bare, through_runner = [], set()
        for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in logical_lines(workflow):
                command = line.strip()
                if "run_bats" in command or "run_unit_test.sh" in command:
                    through_runner.add(workflow.name)
                # Package installs name the bats package; they do not run it.
                if BARE_BATS.search(command) and "install" not in command:
                    bare.append(f"{workflow.name}:{number}: {command}")
        self.assertEqual([], bare)
        self.assertLessEqual({"test.yaml", "macos.yaml", "ubuntu.yaml"}, through_runner)
        unit_test = (WORKFLOWS / "test.yaml").read_text()
        step = unit_test[unit_test.index("- name: Run unit test\n") :]
        step = step[: step.index("\n      - name: ")]
        self.assertEqual(2, step.count("./scripts/run_unit_test.sh"), step)


if __name__ == "__main__":
    unittest.main()
