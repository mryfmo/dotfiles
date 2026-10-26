"""Every CI Bats run fails a stalled test by name, and the installers' network calls end (regime-cutover U99).

The installers' convention: curl gets `--connect-timeout 30` and fails a transfer under 1 KB/s for 60 s
(`--speed-limit 1024 --speed-time 60`); wget gets `--timeout=60 --tries=3`; `snap install` runs under `timeout`.
apt-get needs nothing: its http and https methods give up a connection or a read that stays silent for
Acquire::http::Timeout, 30 s unless configured (apt methods/basehttp.cc), and https inherits the http value.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "scripts/run_unit_test.sh"
WORKFLOWS = ROOT / ".github/workflows"
BASH = shutil.which("bash") or "/bin/bash"
# What a host runs to install: the bootstrap, the installers and the release helper they share.
INSTALL_SOURCES = [ROOT / "setup.sh", ROOT / "scripts/lib/github-release.sh", *sorted((ROOT / "install").rglob("*.sh"))]
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
    """logical_lines without the messages a script prints, which may name a command without running it."""
    return [
        (number, line) for number, line in logical_lines(path) if not line.lstrip().startswith(("printf ", "echo "))
    ]


class InstallerNetworkBoundTest(unittest.TestCase):
    def test_every_curl_wget_and_snap_call_carries_its_bound(self) -> None:
        unbounded = []
        for path in INSTALL_SOURCES:
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
            for path in INSTALL_SOURCES
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
        ):
            self.assertIn(expected, found)


class RunBatsBoundTest(unittest.TestCase):
    """run_bats (scripts/run_unit_test.sh) against a fake `bats` that writes Bats' extended stream."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="run-bats-"))
        self.addCleanup(shutil.rmtree, self.temp, True)
        (self.temp / "bin").mkdir()

    def fake_bats(self, body: str) -> None:
        script = self.temp / "bin/bats"
        script.write_text(f'#!{BASH}\nprintf "%s\\n" "$*" > "{self.temp}/args"\n' + textwrap.dedent(body))
        script.chmod(0o755)

    def run_bats(self, bound: str, *args: str) -> tuple[subprocess.CompletedProcess[str], float]:
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "TMPDIR": str(self.temp),
            "BATS_PER_TEST_TIMEOUT": bound,
        }
        started = time.monotonic()
        result = subprocess.run(
            [BASH, "-c", 'source "$1" && shift && run_bats "$@"', "_", str(RUNNER), *args],
            env=env, capture_output=True, text=True, timeout=60, check=False,
        )  # fmt: skip
        return result, time.monotonic() - started

    def assert_gone(self, pid_file: Path) -> None:
        pid = int(pid_file.read_text())
        for _ in range(50):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.1)
        os.kill(pid, signal.SIGKILL)
        self.fail(f"process {pid} outlived run_bats")

    def test_a_stalled_test_fails_by_name_and_its_whole_process_group_stops(self) -> None:
        # The stalled test's grandchild is what kept the PR #570 jobs alive until the job timeout.
        self.fake_bats(
            f"""\
            printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] fast\\nok 1 [x] fast\\nbegin 2 [x] misc\\n'
            sleep 300 &
            echo $! > "{self.temp}/grandchild"
            wait
            """
        )
        result, elapsed = self.run_bats("2", "-r", "tests/x/")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 30)
        self.assertEqual(
            "1..2\nok 1 [x] fast\nnot ok 2 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT); stopping Bats\n",
            result.stdout,
        )
        self.assert_gone(self.temp / "grandchild")
        self.assertEqual("--formatter cat -r tests/x/\n", (self.temp / "args").read_text())

    def test_output_from_a_running_test_does_not_extend_its_bound(self) -> None:
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] chatty\\n'
            while true; do printf '# still running\\n'; sleep 0.2; done
            """
        )
        result, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 30)
        self.assertIn("not ok 1 [x] chatty # timeout after 2 s", result.stdout)

    def test_silence_outside_a_test_is_bounded_too(self) -> None:
        self.fake_bats("printf '1..1\\n'\nsleep 300\n")
        result, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, result.returncode, result.stdout + result.stderr)
        self.assertLess(elapsed, 30)
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


class CiBatsRunTest(unittest.TestCase):
    """Every Bats run CI starts goes through run_bats."""

    def test_the_runner_calls_bats_only_through_run_bats(self) -> None:
        calls = [line.strip() for _, line in logical_lines(RUNNER) if BARE_BATS.search(line)]
        self.assertEqual(
            [
                'bats --formatter cat "$@" < /dev/null > "${dir}/stream" &',
                'test_count="$(HOME="${FILES_TEST_HOME:?FILES_TEST_HOME is required}" bats --count "${bats_args[@]}")"',
            ],
            calls,
        )
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
