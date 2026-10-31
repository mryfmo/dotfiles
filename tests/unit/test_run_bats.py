"""scripts/ci/run-bats.py under `--timing`, and its job-summary writes (regime-cutover U128).

The fixture tests/fixtures/run-bats/timing-stream.txt is the `bats --formatter cat --timing` stream Bats 1.14.0 (the
home/dot_mise/config.toml pin) printed for two-tests.bats on 2026-10-31; it pins the result line's form, `ok <n>
<name> in <ms>ms`, the duration after the name and before any ` # skip <reason>` directive, and the wrapper's RESULT
pattern is held to it. The wrapper runs here with a fake `bats` first on PATH (a script that cats the fixture, or
prints a stream of the case's own), the summary file is a scratch file, and the case kills what its fake left
running: the wrapper signals nothing.
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WRAPPER = ROOT / "scripts/ci/run-bats.py"
RUNNER = ROOT / "scripts/run_unit_test.sh"
FIXTURES = ROOT / "tests/fixtures/run-bats"
STREAM = FIXTURES / "timing-stream.txt"
BASH = shutil.which("bash") or "/bin/bash"
# The Bats release home/dot_mise/config.toml pins; run_bats refuses any other before the wrapper runs (U127).
BATS_PIN = tomllib.loads((ROOT / "home/dot_mise/config.toml").read_text())["tools"]["http:bats"]["version"]
# The recorded suffix form, written out independently of the wrapper's pattern.
RECORDED_RESULT = re.compile(r"^(ok|not ok) (\d+) (.+?) in (\d+)ms( # skip .*)?$")
FENCE = "```"


def wrapper_module():
    spec = importlib.util.spec_from_file_location("run_bats_wrapper", WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RecordedStreamTest(unittest.TestCase):
    """The fixture is the truth about Bats 1.14.0's `--timing` spelling; the parser follows it."""

    def test_the_recorded_stream_is_a_two_test_run_whose_result_lines_end_in_the_duration(self) -> None:
        lines = STREAM.read_text().splitlines()
        self.assertEqual("1..2", lines[0])
        self.assertEqual("suite tests/fixtures/run-bats/two-tests.bats", lines[1])
        self.assertEqual(
            ["begin 1 [recorded] skipped", "begin 2 [recorded] slow"], [l for l in lines if l.startswith("begin ")]
        )
        results = [line for line in lines if line.startswith(("ok ", "not ok "))]
        self.assertEqual(2, len(results), lines)
        matches = [RECORDED_RESULT.match(line) for line in results]
        self.assertTrue(all(matches), results)
        # The duration is right after the name; a directive, when there is one, comes after the duration.
        self.assertEqual(
            ("1", "[recorded] skipped", " # skip the directive follows the duration"), matches[0].group(2, 3, 5)
        )
        self.assertEqual(("2", "[recorded] slow", None), matches[1].group(2, 3, 5))
        self.assertTrue(all(match.group(4).isdigit() for match in matches), results)
        self.assertGreater(int(matches[1].group(4)), int(matches[0].group(4)), "the slow test is the slower one")
        readme = (FIXTURES / "README.md").read_text()
        self.assertIn(f"Bats {BATS_PIN}", readme)
        self.assertRegex(readme, r"\b2026-10-31\b")

    def test_the_wrapper_pattern_reads_each_recorded_result_line_as_the_fixture_does(self) -> None:
        pattern = wrapper_module().RESULT
        for line in STREAM.read_text().splitlines():
            if not line.startswith(("ok ", "not ok ")):
                continue
            with self.subTest(line=line):
                recorded, read = RECORDED_RESULT.match(line), pattern.fullmatch(line)
                self.assertIsNotNone(read, line)
                self.assertEqual(recorded.group(2, 3, 4), (read["number"], read["name"], read["ms"]))
        # Without `--timing` the line ends at the name (the no-timing run of the same file): no duration to read.
        self.assertIsNone(pattern.fullmatch("ok 2 [recorded] slow"))


class WrapperTest(unittest.TestCase):
    """scripts/ci/run-bats.py, run as run_bats runs it, against a fake `bats` on PATH."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="run-bats-timing-"))
        self.addCleanup(shutil.rmtree, self.temp, True)
        (self.temp / "bin").mkdir()
        (self.temp / "bin/python3").symlink_to(sys.executable)
        self.pids = self.temp / "pids"
        self.summary = self.temp / "summary.md"
        self.addCleanup(self.kill_recorded)

    def kill_recorded(self) -> None:
        for line in self.pids.read_text().split() if self.pids.exists() else []:
            try:
                os.kill(int(line), signal.SIGKILL)
            except OSError:
                pass

    def fake_bats(self, body: str, version: str = BATS_PIN) -> None:
        script = self.temp / "bin/bats"
        script.write_text(
            f'#!{BASH}\nif [ "$1" = --version ]; then printf "Bats %s\\n" "{version}"; exit 0; fi\n'
            f'printf "%s\\n" "$*" > "{self.temp}/args"\n' + textwrap.dedent(body)
        )
        script.chmod(0o755)

    def fake_bats_cats_the_fixture(self) -> None:
        self.fake_bats(f'exec cat "{STREAM}"\n')

    def environment(self, bound: str, summary: str | None) -> dict[str, str]:
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "TMPDIR": str(self.temp),
            "BATS_PER_TEST_TIMEOUT": bound,
            "PIDS": str(self.pids),
        }
        if summary is not None:
            env["GITHUB_STEP_SUMMARY"] = summary
        return env

    def run_wrapper(self, *args: str, bound: str = "30", summary: str | None = None) -> tuple[int, str, str]:
        return self.run_command([sys.executable, "-I", "-S", str(WRAPPER), *args], bound, summary)

    def run_command(self, command: list[str], bound: str, summary: str | None) -> tuple[int, str, str]:
        out, err = self.temp / "out", self.temp / "err"
        # Files, not pipes: what a stalled test leaves running keeps its copies of stdout and stderr.
        with out.open("w") as stdout, err.open("w") as stderr:
            process = subprocess.Popen(
                command, env=self.environment(bound, summary), stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr
            )
            status = process.wait(timeout=60)
        return status, out.read_text(), err.read_text()

    def test_the_recorded_stream_prints_the_tap_lines_and_the_slowest_line(self) -> None:
        self.fake_bats_cats_the_fixture()
        expected = (
            "1..2\n"
            "running: 1 [recorded] skipped\n"
            "ok 1 [recorded] skipped in 10ms # skip the directive follows the duration\n"
            "running: 2 [recorded] slow\n"
            "ok 2 [recorded] slow in 330ms\n"
            "slowest: 2 [recorded] slow 330 ms\n"
        )
        self.summary.write_text("earlier step\n")
        status, out, err = self.run_wrapper("--timing", "tests/x.bats", summary=str(self.summary))
        self.assertEqual(0, status, out + err)
        self.assertEqual(expected, out)
        self.assertEqual("", err)
        self.assertEqual("--formatter cat --timing tests/x.bats", (self.temp / "args").read_text().strip())
        # Appended after what the step wrote before, in a fenced block under the Bats command.
        self.assertEqual(
            f"earlier step\n{FENCE}text\nbats --formatter cat --timing tests/x.bats\nslowest: 2 [recorded] slow 330 ms\n{FENCE}\n",
            self.summary.read_text(),
        )
        for summary in (None, ""):
            with self.subTest(summary=summary):
                self.summary.unlink(missing_ok=True)
                status, out, err = self.run_wrapper("--timing", "tests/x.bats", summary=summary)
                self.assertEqual((0, expected, ""), (status, out, err))
                self.assertFalse(self.summary.exists())

    def test_a_stall_writes_the_timeout_line_and_the_diagnosis_to_the_log_and_the_summary(self) -> None:
        self.fake_bats(
            """\
            printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] fast\\nok 1 [x] fast in 1ms\\nbegin 2 [x] misc\\n'
            echo $$ >> "${PIDS}"
            sleep 300 &
            echo $! >> "${PIDS}"
            wait
            """
        )
        status, out, err = self.run_wrapper("--timing", "tests/x.bats", bound="2", summary=str(self.summary))
        self.assertEqual(124, status, out + err)
        self.assertEqual("", err)
        named = "1..2\nrunning: 1 [x] fast\nok 1 [x] fast in 1ms\nrunning: 2 [x] misc\n"
        verdict = "not ok 2 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT)\n"
        self.assertTrue(out.startswith(named + verdict), out)
        block = out[len(named) :]
        diagnosis = block[len(verdict) :]
        self.assertTrue(diagnosis.startswith("# diagnosis"), diagnosis)
        self.assertTrue(all(line.startswith("#") for line in diagnosis.splitlines()), diagnosis)
        self.assertNotIn("slowest:", out)
        # The summary holds the same verdict and the same diagnosis block as the log, nothing more.
        self.assertEqual(
            f"{FENCE}text\nbats --formatter cat --timing tests/x.bats\n{block}{FENCE}\n", self.summary.read_text()
        )

    def test_a_result_line_without_the_duration_is_a_malformed_stream_and_the_status_stays_the_suites(self) -> None:
        for code in (0, 1):
            with self.subTest(status=code):
                self.fake_bats(
                    f"""\
                    printf '1..3\\nbegin 1 [x] a\\nok 1 [x] a\\nbegin 2 [x] b\\n'
                    printf 'ok 2 [x] b in 2ms # skip waits in 9ms\\nbegin 3 [x] c\\nnot ok 3 [x] c in 7ms\\n'
                    exit {code}
                    """
                )
                status, out, err = self.run_wrapper("--timing", "tests/x.bats", summary=str(self.summary))
                self.assertEqual(code, status, out + err)
                self.assertEqual(
                    "run-bats: malformed stream: no duration on a result line under --timing: ok 1 [x] a\n", err
                )
                # The timed lines are still read: the directive's ` in 9ms` is not a duration, the not ok line's is.
                self.assertTrue(out.endswith("not ok 3 [x] c in 7ms\nslowest: 3 [x] c 7 ms\n"), out)
                self.assertEqual(
                    code == 0, self.summary.exists(), "a passing run's slowest line, nothing for a failed one"
                )
                self.summary.unlink(missing_ok=True)

    def test_without_timing_the_stream_is_passed_through_and_nothing_is_measured(self) -> None:
        self.fake_bats("printf '1..1\\nbegin 1 [x] a\\nok 1 [x] a\\n'\n")
        status, out, err = self.run_wrapper("tests/x.bats", summary=str(self.summary))
        self.assertEqual(0, status, out + err)
        self.assertEqual("1..1\nrunning: 1 [x] a\nok 1 [x] a\n", out)
        self.assertEqual("", err)
        self.assertFalse(self.summary.exists())

    def test_an_unwritable_summary_is_one_stderr_line_and_changes_no_status(self) -> None:
        unwritable = str(self.temp / "no-such-directory/summary.md")
        self.fake_bats_cats_the_fixture()
        status, out, err = self.run_wrapper("--timing", "tests/x.bats", summary=unwritable)
        self.assertEqual(0, status, out + err)
        self.assertTrue(out.endswith("slowest: 2 [recorded] slow 330 ms\n"), out)
        self.assertEqual(
            [f"run-bats: GITHUB_STEP_SUMMARY={unwritable!r} not written: No such file or directory"], err.splitlines()
        )
        self.fake_bats("printf '1..1\\nbegin 1 [x] misc\\n'\necho $$ >> \"${PIDS}\"\nsleep 300\n")
        status, out, err = self.run_wrapper("--timing", "tests/x.bats", bound="2", summary=unwritable)
        self.assertEqual(124, status, out + err)
        self.assertIn("not ok 1 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT)\n", out)
        self.assertEqual(
            [f"run-bats: GITHUB_STEP_SUMMARY={unwritable!r} not written: No such file or directory"], err.splitlines()
        )

    def test_run_bats_passes_timing_before_its_arguments(self) -> None:
        self.assertIn('python3 -I -S "${here}/ci/run-bats.py" --timing "$@"', RUNNER.read_text())
        self.fake_bats_cats_the_fixture()
        command = [
            BASH,
            "-c",
            'source "$1" && shift && run_bats "$@"',
            "_",
            str(RUNNER),
            "--filter-tags",
            "common",
            "x.bats",
        ]
        status, out, err = self.run_command(command, "30", str(self.summary))
        self.assertEqual(0, status, out + err)
        self.assertEqual(
            "--formatter cat --timing --filter-tags common x.bats", (self.temp / "args").read_text().strip()
        )
        accepted, _, stream = out.partition("\n")
        self.assertTrue(accepted.startswith(f"==> bats {BATS_PIN}, "), out)
        self.assertTrue(stream.endswith("ok 2 [recorded] slow in 330ms\nslowest: 2 [recorded] slow 330 ms\n"), out)
        self.assertIn(
            "bats --formatter cat --timing --filter-tags common x.bats\nslowest: 2 [recorded] slow 330 ms\n",
            self.summary.read_text(),
        )

    def test_the_wrapper_still_signals_nothing(self) -> None:
        text = WRAPPER.read_text()
        for api in (r"import signal", r"os\.kill", r"killpg", r"setsid", r"start_new_session", r"\bkill\b"):
            with self.subTest(api=api):
                self.assertNotRegex(text, api)
        self.assertEqual(1, text.count('["ps", '))


if __name__ == "__main__":
    unittest.main()
