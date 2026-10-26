"""Every CI Bats run names a stalled test, and every scripted download ends (regime-cutover U99).

The download convention, for setup.sh, install/**, scripts/** (make update, the levers, the CI helpers) and the
workflow steps: curl gets `--connect-timeout 30` and fails a transfer under 1 KB/s for 60 s (`--speed-limit 1024
--speed-time 60`); wget gets `--timeout=60 --tries=3`; `snap install` runs under `timeout`. apt-get needs nothing:
its http and https methods give up a connection or a read that stays silent for Acquire::http::Timeout, 30 s unless
configured (apt methods/basehttp.cc), and https inherits the http value.

The download check tokenizes the shell text, so it finds curl and wget wherever they run as a command: a plain
command, after a pipe or `&&`, inside `$(...)` or backticks (also inside double quotes, as in `printf "$(curl …)"`),
after `sudo`, `env`, `timeout`, `if` or an assignment, and inside `bash -c '…'`. A word that only names the tool (a
package list, `command -v curl`, a message, the source a manifest records) is not a command word and is not checked.
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
WRAPPER = ROOT / "scripts/ci/run-bats.py"
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
# Python and Ruby are not shell: none may start curl or wget, as an argv's first element or at the head of a command
# string, since this check cannot see the bounds there. A mention in a comment or a message is not a start.
NOT_SHELL = (".py", ".pyc", ".rb")
FOREIGN_CALL = re.compile(r"""[\[(,]\s*[fr]?["'](?:[^"'\s]*/)?(?:curl|wget)(?:["']|\s)""")
RUBY_CALL = re.compile(r"`(?:curl|wget)\s|%x\(\s*(?:curl|wget)")
# Words that run the next word as the command (with their own options and operands skipped).
PREFIXES = {"sudo", "env", "timeout", "exec", "command", "nohup", "time", "nice", "xargs", "!", "if", "then", "elif"}
PREFIXES |= {"else", "do", "while", "until"}
# Options of a prefix that take the following word as their operand.
OPERAND_OPTIONS = {
    "sudo": {"-u", "-g", "-C", "-D", "-h", "-p", "-r", "-t", "-U"},
    "env": {"-u", "-C", "-S"},
    "timeout": {"-k", "-s"},
    "nice": {"-n"},
    "xargs": {"-I", "-L", "-n", "-P", "-d", "-E", "-s"},
}
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
# The old line pattern: a tool followed by an option on an unquoted command line. The tokenizer must find a call on
# every such line, or it has lost its place in the file (an unbalanced quote) and would miss calls.
LINE_CALL = re.compile(r"^(?:[^\"'#]*[\s;&|(`])?(curl|wget)\s+-")
# A bare Bats run in a workflow or the runner: `bats` as a command word, not run_bats, bats-core or a package list.
BARE_BATS = re.compile(r"(?<![\w/.-])bats\s")


class Lexer:
    """A shell tokenizer good enough to find command words: quotes, escapes, comments, `${…}`, `$(…)`, backticks
    (also inside double quotes) and the separators `; | & ( ) { }` and newline. A token is ("w", text, offset) or
    ("s", "", offset)."""

    def __init__(self, text: str) -> None:
        self.s, self.i, self.tokens = text, 0, []
        self.buf: list[str] | None = None
        self.start = 0

    def flush(self) -> None:
        if self.buf is not None:
            self.tokens.append(("w", "".join(self.buf), self.start))
        self.buf = None

    def add(self, text: str) -> None:
        if self.buf is None:
            self.buf, self.start = [], self.i
        self.buf.append(text)

    def sep(self) -> None:
        self.tokens.append(("s", "", self.i))

    def substitution(self, term: str) -> None:
        self.flush()
        self.sep()
        self.command(term)
        self.sep()

    def command(self, term: str | None = None) -> None:
        s, depth = self.s, 0
        while self.i < len(s):
            c = s[self.i]
            if c == term and (term == "`" or depth == 0):
                self.flush()
                self.i += 1
                return
            if c in " \t":
                self.flush()
                self.i += 1
            elif c == "\\":
                if s.startswith("\\\n", self.i):
                    self.flush()
                else:
                    self.add(s[self.i + 1 : self.i + 2])
                self.i += 2
            elif c == "#" and self.buf is None:
                end = s.find("\n", self.i)
                self.i = len(s) if end < 0 else end
            elif c == "'":
                end = s.find("'", self.i + 1)
                end = len(s) if end < 0 else end
                self.add(s[self.i + 1 : end])
                self.i = end + 1
            elif c == '"':
                self.double()
            elif s.startswith("${", self.i):
                self.add(self.balanced(self.i + 2, "{", "}"))
            elif c == "(" and self.buf and self.buf[-1].endswith("="):
                # An array literal, `NAME=(a b c)`: its words are values, not commands.
                self.add(self.balanced(self.i + 1, "(", ")"))
            elif s.startswith("$(", self.i):
                self.i += 2
                self.substitution(")")
            elif c == "`":
                self.i += 1
                self.substitution("`")
            elif c in ";|&(){}\n":
                self.flush()
                self.sep()
                if term == ")":
                    depth += {"(": 1, ")": -1}.get(c, 0)
                self.i += 1
            else:
                self.add(c)
                self.i += 1
        self.flush()

    def double(self) -> None:
        s = self.s
        self.add("")
        self.i += 1
        while self.i < len(s):
            c = s[self.i]
            if c == '"':
                self.i += 1
                return
            if c == "\\":
                self.add(s[self.i + 1 : self.i + 2])
                self.i += 2
            elif s.startswith("${", self.i):
                self.add(self.balanced(self.i + 2, "{", "}"))
            elif s.startswith("$(", self.i):
                self.i += 2
                self.substitution(")")
            elif c == "`":
                self.i += 1
                self.substitution("`")
            else:
                self.add(c)
                self.i += 1

    def balanced(self, j: int, opening: str, closing: str) -> str:
        """The text from self.i to the closer matching an opener just before j, quotes and comments skipped; the
        position moves past it."""
        s, depth, start = self.s, 1, self.i
        while j < len(s) and depth:
            ch = s[j]
            if ch == "\\":
                j += 2
                continue
            if ch in "'\"":
                end = s.find(ch, j + 1)
                j = (len(s) if end < 0 else end) + 1
                continue
            if ch == "#" and opening == "(" and s[j - 1] in " \t\n":
                end = s.find("\n", j)
                j = len(s) if end < 0 else end
                continue
            depth += {opening: 1, closing: -1}.get(ch, 0)
            j += 1
        self.i = j
        return s[start:j]


def simple_commands(text: str) -> list[list[tuple[str, int]]]:
    """The words of every simple command in the text, each with its offset."""
    lexer = Lexer(text)
    lexer.command()
    commands: list[list[tuple[str, int]]] = [[]]
    for kind, word, offset in lexer.tokens:
        if kind == "s":
            commands.append([])
        else:
            commands[-1].append((word, offset))
    return [command for command in commands if command]


def calls(text: str) -> list[tuple[int, str, list[str], set[str]]]:
    """Every command whose command word is curl, wget or snap: (offset, tool, arguments, prefixes it ran under)."""
    found = []
    for command in simple_commands(text):
        words = [word for word, _ in command]
        index, prefixes = 0, set()
        while index < len(words):
            word = words[index]
            if ASSIGNMENT.match(word):
                index += 1
                continue
            name = os.path.basename(word)
            if name not in PREFIXES:
                break
            if name == "command" and index + 1 < len(words) and words[index + 1] in ("-v", "-V"):
                index = len(words)
                break
            prefixes.add(name)
            index += 1
            while index < len(words) and (words[index].startswith("-") or ASSIGNMENT.match(words[index])):
                index += 2 if words[index] in OPERAND_OPTIONS.get(name, ()) else 1
            if name == "timeout" and index < len(words):
                index += 1  # the duration
        if index >= len(words):
            continue
        name, args = os.path.basename(words[index]), words[index + 1 :]
        if name in ("bash", "sh", "zsh") and "-c" in args[:-1]:
            # The script of `bash -c '…'` is shell too.
            script = args[args.index("-c") + 1]
            found += [(command[index][1], tool, a, p) for _, tool, a, p in calls(script)]
        elif name in ("curl", "wget", "snap"):
            found.append((command[index][1], name, args, prefixes))
    return found


def unbounded(text: str) -> list[str]:
    """The calls in the text that lack the bound, as `line: tool arguments`."""
    bad = []
    for offset, tool, args, prefixes in calls(text):
        joined = " ".join(args)
        if tool == "curl":
            ok = "--connect-timeout" in args and (
                "--max-time" in args or ("--speed-limit" in args and "--speed-time" in args)
            )
        elif tool == "wget":
            ok = any(a.startswith("--timeout=") for a in args) and any(a.startswith("--tries=") for a in args)
        else:
            ok = not args or args[0] not in ("install", "refresh") or "timeout" in prefixes
        if not ok:
            bad.append(f"{text.count(chr(10), 0, offset) + 1}: {tool} {joined}")
    return bad


def is_shell(path: Path) -> bool:
    return path.suffix not in NOT_SHELL and not path.read_bytes()[:64].startswith(
        (b"#!/usr/bin/env python", b"#!/usr/bin/python")
    )


class NetworkBoundTest(unittest.TestCase):
    def test_every_curl_wget_and_snap_call_carries_its_bound(self) -> None:
        bad = []
        for path in NETWORK_SOURCES:
            relative = path.relative_to(ROOT).as_posix()
            if is_shell(path):
                bad += [f"{relative}:{hit}" for hit in unbounded(path.read_text())]
            elif hits := [
                m.group(0)
                for pattern in (FOREIGN_CALL, *((RUBY_CALL,) if path.suffix == ".rb" else ()))
                for m in pattern.finditer(path.read_text(errors="replace"))
            ]:
                bad.append(f"{relative}: starts curl or wget outside the shell: {hits}")
        self.assertEqual([], bad)

    def test_the_tokenizer_keeps_its_place_in_every_file(self) -> None:
        # Every line that plainly starts a download must hold a call the tokenizer found; one that does not means an
        # unbalanced quote put the tokenizer out of step, and calls after it would go unchecked.
        lost, total = [], 0
        for path in NETWORK_SOURCES:
            if not is_shell(path):
                continue
            text = path.read_text()
            lines = {text.count("\n", 0, offset) + 1 for offset, tool, _, _ in calls(text) if tool != "snap"}
            total += len(lines)
            for number, line in enumerate(text.splitlines(), 1):
                if LINE_CALL.search(line.strip()) and number not in lines:
                    lost.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
        self.assertEqual([], lost)
        # The scan saw the calls it checks (a tokenizer that found nothing would pass every tree).
        self.assertGreater(total, 40)

    def test_the_audit_bypasses_are_caught(self) -> None:
        # Audit of c7629e24: a call without options, and downloads inside printf substitutions.
        for snippet in (
            "curl https://x.invalid/a\n",
            "wget https://x.invalid/a\n",
            'printf "%s\\n" "$(curl -fsSL https://x.invalid/a)"\n',
            "printf '%s\\n' `wget -qO - https://x.invalid/a`\n",
            'sum="$(curl -fsSL "${url}" | shasum -a 256)"\n',
            "sudo --preserve-env=http_proxy curl -fsSL https://x.invalid/a -o /tmp/a\n",
            "env -u CI HOME=/tmp curl -fsSL https://x.invalid/a\n",
            "if curl -fsSL https://x.invalid/a; then :; fi\n",
            "true && wget --timeout=60 https://x.invalid/a\n",
            "bash -c 'curl -fsSL https://x.invalid/a'\n",
            "curl --connect-timeout 30 https://x.invalid/a\n",
            "sudo snap install chromium\n",
            "x=1 /usr/bin/curl -fsSL https://x.invalid/a\n",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual(1, len(unbounded(snippet)), snippet)

    def test_python_or_ruby_starting_a_download_is_caught(self) -> None:
        for source in ('subprocess.run(["curl", "-fsSL", url])', "os.system('wget -q https://x.invalid/a')"):
            with self.subTest(source=source):
                self.assertTrue(FOREIGN_CALL.search(source))
        self.assertTrue(RUBY_CALL.search("out = `curl -s https://x.invalid/a`"))
        self.assertIsNone(FOREIGN_CALL.search('"# shell after a pipe (`curl ... | sh`), which no prefix rule"'))

    def test_bounded_calls_and_mere_mentions_pass(self) -> None:
        for snippet in (
            "curl -fsSL --connect-timeout 30 --speed-limit 1024 --speed-time 60 https://x.invalid/a\n",
            'printf "%s" "$(curl -q --connect-timeout 5 --max-time 15 https://x.invalid/a)"\n',
            "readonly PACKAGES=(\n    cmake\n    curl # the bootstrap's fetcher\n    wget\n)\n",
            'for x in ${a[@]+"${a[@]}"}; do :; done\ncurl --connect-timeout 30 --max-time 9 https://x.invalid/a\n',
            "wget --timeout=60 --tries=3 -qO - https://x.invalid/a\n",
            "sudo timeout --kill-after=30 600 snap install chromium\n",
            "command -v curl > /dev/null 2>&1\n",
            "sudo apt-get install -y bats curl iproute2\n",
            'echo "Neither curl nor wget is available; cannot download ${url}." >&2\n',
            "printf 'curl %s\\n' \"$*\" >> calls.log\n",
            'manifest_record "x" installer v1 /t -- "curl -fsSL https://x.invalid/a" "shasum -a 256 <a>"\n',
            "# curl https://x.invalid/a\n",
            "snap list chromium\n",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual([], unbounded(snippet), snippet)


class RunBatsBoundTest(unittest.TestCase):
    """run_bats (scripts/run_unit_test.sh, then scripts/ci/run-bats.py) against a fake `bats` that writes Bats'
    extended stream."""

    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="run-bats-"))
        self.addCleanup(shutil.rmtree, self.temp, True)
        (self.temp / "bin").mkdir()
        # The python3 the runner calls, so the case does not depend on the host's.
        (self.temp / "bin/python3").symlink_to(sys.executable)
        self.pids = self.temp / "pids"
        # The wrapper signals nothing, so the case itself stops what its fake left running.
        self.addCleanup(self.kill_recorded)

    def kill_recorded(self) -> None:
        for line in self.pids.read_text().split() if self.pids.exists() else []:
            try:
                os.kill(int(line), signal.SIGKILL)
            except OSError:
                pass

    def fake_bats(self, body: str) -> None:
        script = self.temp / "bin/bats"
        script.write_text(f'#!{BASH}\nprintf "%s\\n" "$*" > "{self.temp}/args"\n' + textwrap.dedent(body))
        script.chmod(0o755)

    def run_bats(self, bound: str, *args: str) -> tuple[int, str, str, float]:
        env = {
            "PATH": f"{self.temp / 'bin'}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "TMPDIR": str(self.temp),
            "BATS_PER_TEST_TIMEOUT": bound,
            "PIDS": str(self.pids),
        }
        out, err = self.temp / "out", self.temp / "err"
        started = time.monotonic()
        # Files, not pipes: what a stalled test leaves running keeps its copies of stdout and stderr, and the time
        # measured is the wrapper's own return.
        with out.open("w") as stdout, err.open("w") as stderr:
            process = subprocess.Popen(
                [BASH, "-c", 'source "$1" && shift && run_bats "$@"', "_", str(RUNNER), *args],
                env=env, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
            )  # fmt: skip
            status = process.wait(timeout=60)
        return status, out.read_text(), err.read_text(), time.monotonic() - started

    def test_a_stalled_test_is_named_and_the_run_fails_within_the_bound(self) -> None:
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
        status, out, err, elapsed = self.run_bats("2", "-r", "tests/x/")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4)
        self.assertEqual(
            "1..2\nrunning: 1 [x] fast\nok 1 [x] fast\nrunning: 2 [x] misc\n"
            "not ok 2 [x] misc # timeout after 2 s (BATS_PER_TEST_TIMEOUT)\n",
            out,
        )
        self.assertEqual("--formatter cat -r tests/x/\n", (self.temp / "args").read_text())

    def test_output_from_a_running_test_does_not_extend_its_bound(self) -> None:
        self.fake_bats(
            """\
            printf '1..1\\nbegin 1 [x] chatty\\n'
            echo $$ >> "${PIDS}"
            while true; do printf '# still running\\n'; sleep 0.2; done
            """
        )
        status, out, err, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok 1 [x] chatty # timeout after 2 s", out)

    def test_loading_the_files_is_bounded_too(self) -> None:
        # Bats sources every file before its plan line; nothing runs Bats outside the bound (no `bats --count`).
        self.fake_bats('echo $$ >> "${PIDS}"\nsleep 300\n')
        status, out, err, elapsed = self.run_bats("2", "tests/x.bats")
        self.assertEqual(124, status, out + err)
        self.assertLess(elapsed, 4)
        self.assertIn("not ok - Bats printed nothing for 2 s outside a test", out)

    def test_pass_and_fail_statuses_are_kept(self) -> None:
        for code in (0, 1):
            with self.subTest(status=code):
                verdict = "ok 2 [x] b" if code == 0 else "not ok 2 [x] b"
                self.fake_bats(
                    f"""\
                    printf '1..2\\nsuite tests/x.bats\\nbegin 1 [x] a\\nok 1 [x] a\\nbegin 2 [x] b\\n# output of b\\n'
                    printf '{verdict}\\n'
                    exit {code}
                    """
                )
                status, out, err, elapsed = self.run_bats("30", "tests/x.bats")
                self.assertEqual(code, status, err)
                self.assertLess(elapsed, 10)
                self.assertEqual(
                    f"1..2\nrunning: 1 [x] a\nok 1 [x] a\nrunning: 2 [x] b\n# output of b\n{verdict}\n", out
                )

    def test_a_run_that_plans_no_test_fails(self) -> None:
        for body, shown in (("printf '1..0\\n'\n", "0"), ("exit 0\n", "nothing")):
            with self.subTest(plan=shown):
                self.fake_bats(body)
                status, out, err, _ = self.run_bats("30", "--filter-tags", "common,ubuntu:client", "x.bats")
                self.assertEqual(1, status, out + err)
                self.assertIn(f"expected at least one test; Bats planned {shown}", err)

    def test_the_wrapper_signals_nothing(self) -> None:
        # Stopping processes is the step's timeout-minutes and the runner's job, not this wrapper's.
        text = WRAPPER.read_text()
        for api in (r"import signal", r"os\.kill", r"killpg", r"setsid", r"start_new_session", r'"ps"'):
            with self.subTest(api=api):
                self.assertNotRegex(text, api)
        self.assertIn('python3 -I -S "${here}/ci/run-bats.py"', RUNNER.read_text())


def workflow_steps(text: str) -> list[str]:
    """Each step of a workflow, as its text: from its `- ` line to the next step or the end of its list."""
    steps, current, indent = [], None, None
    for line in text.splitlines():
        match = re.match(r"^(\s*)- (?:name|uses|run|id|if|env|shell|with):", line)
        stripped = len(line) - len(line.lstrip())
        if match and (indent is None or len(match.group(1)) == indent):
            if current is not None:
                steps.append("\n".join(current))
            current, indent = [line], len(match.group(1))
        elif current is not None and line.strip() and stripped <= indent:
            steps.append("\n".join(current))
            current, indent = None, None
        elif current is not None:
            current.append(line)
    if current is not None:
        steps.append("\n".join(current))
    return steps


class CiBatsRunTest(unittest.TestCase):
    """Every Bats run CI starts goes through run_bats, in a step with its own timeout-minutes."""

    def test_the_runner_calls_bats_only_through_run_bats(self) -> None:
        calls_ = [line.strip() for line in RUNNER.read_text().splitlines() if BARE_BATS.search(line.split("#")[0])]
        self.assertEqual([], calls_)
        self.assertIn('["bats", "--formatter", "cat", *argv]', WRAPPER.read_text())
        text = RUNNER.read_text()
        for function in ("run_common_test", "run_os_specific_test", "run_files_test"):
            start = text.index(f"function {function}() {{\n")
            self.assertIn("run_bats ", text[start : text.index("\n}\n", start)], function)

    def test_no_workflow_runs_bats_directly(self) -> None:
        bare, through_runner = [], set()
        for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
            for number, line in enumerate(workflow.read_text().splitlines(), 1):
                command = line.split("#")[0].strip()
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

    def test_every_bats_step_has_its_own_timeout(self) -> None:
        found, missing = 0, []
        for workflow in sorted(WORKFLOWS.glob("*.y*ml")):
            for step in workflow_steps(workflow.read_text()):
                if "run_bats" not in step and "run_unit_test.sh" not in step:
                    continue
                found += 1
                match = re.search(r"^\s+timeout-minutes: ([0-9]+)$", step, re.MULTILINE)
                # Above one per-test bound (1200 s, scripts/ci/run-bats.py), so the stalled test is named first.
                if not match or int(match.group(1)) * 60 <= 1200:
                    missing.append(f"{workflow.name}: {step.splitlines()[0].strip()}")
        self.assertEqual([], missing)
        self.assertEqual(3, found)


if __name__ == "__main__":
    unittest.main()
