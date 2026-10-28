"""The Azure apt mirror is dropped before every CI apt use, every apt call a workflow runs ends inside its step, and
the Bats bounds name a stall before the step stops (regime-cutover U102, U109).

actions/runner-images#14823: a slow azure.archive.ubuntu.com node keeps sending data, so apt's 15 s timeout never
fires and apt never moves to the next mirror. scripts/ci/drop-azure-apt-mirror.py removes that entry; every job that
runs apt on a Ubuntu runner calls it first. After the drop every call goes to archive.ubuntu.com, which can print
nothing for 15 minutes during `apt-get update` (runner-images#15040), so each call runs under GNU timeout with apt's
own silence timeout and retries set, in one exact form, and the steps that hold them carry their own timeout-minutes.
The measured budgets below come from passing `test` jobs of October 2026.
"""

from __future__ import annotations

import math
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # dotted runs too; discover -s tests/unit already has it
from test_workflow_orchestration_skip import jobs

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github/workflows"
SCRIPT = ROOT / "scripts/ci/drop-azure-apt-mirror.py"
WRAPPER = ROOT / "scripts/ci/run-bats.py"
# The system python3, as the workflows run it; a host without one (none of CI's) runs the test interpreter instead.
SYSTEM_PYTHON = "/usr/bin/python3" if Path("/usr/bin/python3").exists() else sys.executable
CALL = "/usr/bin/python3 -I -S scripts/ci/drop-azure-apt-mirror.py"
# A step uses apt on the runner when it runs apt-get or apt, setup.sh (its Ubuntu installers), or the install tests
# (scripts/run_unit_test.sh and run_bats, whose real-install cases run apt-get). `make apply-check` (apply-check.yml)
# runs apt only inside its Docker build, against the image's own sources, never the runner's mirror list.
APT_USE = re.compile(
    r"\bapt-get\b|\bapt\s+(?:install|update|upgrade)\b|\bbash\s+\S*setup\.sh\b|\./setup\.sh\b|run_unit_test\.sh|\brun_bats\b"
)
# The jobs that run apt on a Ubuntu runner today; a scan that found fewer would have lost one.
APT_JOBS = {
    ("test.yaml", "test"),
    ("remote.yaml", "public-bootstrap"),
    ("private-bootstrap.yaml", "private-bootstrap"),
    ("ubuntu.yaml", "build"),
}
# Measured, in seconds (passing Ubuntu client jobs, October 2026):
# the time a `Run unit test` step spends outside its slowest test: 88-135 s typically, 284 s at most (run
# 40314461046, where ghostty took 201 s on a slow mirror);
OTHER_TESTS_BUDGET = 300
# the time a `test` job spends before `Run unit test`: at most 409 s (run 40251900588); and after it: at most 10 s.
PRE_STEP_BUDGET = 480
POST_STEP_BUDGET = 60
# The files suite under ubuntu.yaml's and macos.yaml's `Test file existence` (under 1 s in test.yaml), plus the
# brew install of bats-core there.
FILES_STEP_BUDGET = 300
MIRRORS = (
    "http://azure.archive.ubuntu.com/ubuntu/\tpriority:1\n"
    "https://archive.ubuntu.com/ubuntu/\tpriority:2\n"
    "https://security.ubuntu.com/ubuntu/\tpriority:3\n"
)
# U109: every apt call a workflow runs carries its own bound, in one exact form. `timeout` ends a call that keeps
# printing nothing at N seconds and kills it KILL_AFTER seconds later; apt's own options give up a connection or read
# silent for 15 s and move to the next mirror, three times. N is measured per step (the comment next to each call in
# the workflow) with twice the measured time and at least 120 s of margin, so never under MIN_APT_BOUND.
APT_CALL = re.compile(r"\bapt-get\b|\bapt\s+(?:install|update|upgrade|full-upgrade|dist-upgrade)\b")
APT_BOUND = re.compile(
    r"timeout --kill-after=10 ([0-9]+) sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 "
    r"(?:update|install)(?=\s|$)"
)
KILL_AFTER = 10
MIN_APT_BOUND = 120
# A shell word left on the line once the form is removed reopens the call when it starts with one of these, whether
# the value is attached (`-cfoo.conf`), separate, after `=` or quoted (apt reads them all) ...
APT_REOPEN_PREFIXES = {
    "-o": "an option",
    "-c": "a configuration file",
    "--option": "an option",
    "--config-file": "a configuration file",
}
# ... or holds one of these anywhere, in any case (`APT_CONFIG=` at the front, a second `timeout` after `;`).
APT_REOPEN_PARTS = {
    "acquire::": "an Acquire key",
    "apt_config": "the APT_CONFIG variable",
    "timeout": "a second timeout",
}
# (workflow file name, the whole stripped line, exactly) -> why the line may name apt without the form. Empty on this
# head: the three workflows that bootstrap through setup.sh run apt only inside the installers, whose downloads U99
# bounded, and no workflow comment names apt-get. A row must still match a line (test_no_apt_exemption_is_stale).
APT_EXEMPT: dict[tuple[str, str], str] = {}
# Measured, in seconds, outside the apt calls (passing `test` jobs, every matrix row, runs 40314863147 to
# 40610790312): "Install tools" at most 73 s (ubuntu-24.04 server, run 40338292845), 14 to 46 s elsewhere; "Run
# Python unit tests" at most 664 s (macos-15 client, run 40610790312), 189 to 388 s on the Ubuntu rows; "Setup for
# Codecov" under 1 s. Twice the maximum each, so a step bound ends a stall, never a slow passing run.
STEP_REST_BUDGET = {"Install tools": 150, "Run Python unit tests": 1330, "Setup for Codecov": 60}


def step_text(step: dict) -> str:
    """The step's commands, comment lines left out (a decision step names setup.sh in its comments and patterns)."""
    lines = f"{step.get('run', '')}\n{step.get('script', '')}".splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#"))


def job_text(path: Path, name: str) -> str:
    text = path.read_text().split("\njobs:\n", 1)[1]
    body = text.split(f"\n  {name}:\n", 1)[1] if not text.startswith(f"  {name}:\n") else text
    return re.split(r"\n  [a-z][\w-]*:\n", body, maxsplit=1)[0]


def default_bound() -> int:
    return int(re.search(r"^DEFAULT_BOUND = ([0-9]+)$", WRAPPER.read_text(), re.MULTILINE).group(1))


def reopening_word(rest: str) -> str | None:
    """Why the first shell word of `rest` (a line with its bound forms removed) that reopens the call does so, or None.

    Audit of 9058072b: a token regex saw `-o` and `-c` only as separate words, so `-cfoo.conf` and
    `-oDebug::NoLocking=true` passed. Every word is read whole; a quote that never closes refuses the line, since
    its words cannot be told apart."""
    try:
        words = shlex.split(rest)
    except ValueError as error:
        return f"cannot be split into shell words: {error}"
    for word in words:
        lower = word.lower()
        for prefix, why in APT_REOPEN_PREFIXES.items():
            if lower.startswith(prefix):
                return f"{word!r} starts with {prefix!r}: {why}"
        for part, why in APT_REOPEN_PARTS.items():
            if part in lower:
                return f"{word!r} holds {part!r}: {why}"
    return None


def apt_violations(relative: str, text: str, exempt: dict[tuple[str, str], str] | None = None) -> list[str]:
    """The lines of one workflow that name apt outside the bound form, as `file:line: text (why)`."""
    exempt = APT_EXEMPT if exempt is None else exempt
    bad = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        calls = len(APT_CALL.findall(line))
        if not calls or (relative, line) in exempt:
            continue
        where = f"{relative}:{number}: {line}"
        bounds = APT_BOUND.findall(line)
        if len(bounds) != calls:
            bad.append(f"{where} ({calls} apt call(s), {len(bounds)} in the bound form)")
            continue
        low = [n for n in bounds if int(n) < MIN_APT_BOUND]
        if low:
            bad.append(f"{where} (a bound under {MIN_APT_BOUND} s: {low})")
        if line.endswith("\\"):
            bad.append(f"{where} (continues onto the next line, where an option could reopen the call)")
        reopens = reopening_word(APT_BOUND.sub(" ", line.removesuffix("\\")))
        if reopens:
            bad.append(f"{where} (outside the form, {reopens})")
    return bad


def apt_stale(files: dict[str, str], exempt: dict[tuple[str, str], str] | None = None) -> list[str]:
    """The exemptions whose workflow no longer holds their whole line, exactly."""
    exempt = APT_EXEMPT if exempt is None else exempt
    lines = {name: {line.strip() for line in text.splitlines()} for name, text in files.items()}
    return [f"{name}: {line}" for name, line in exempt if line not in lines.get(name, set())]


def bounded_steps() -> list[dict]:
    """Three steps in the bound form with the timeout-minutes the formula gives for STEP_REST_BUDGET."""
    form = "timeout --kill-after=10 {} sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 {}"
    return [
        {
            "name": "Install tools",
            "timeout-minutes": "10",
            "run": f"{form.format(180, 'update')}\n{form.format(180, 'install -y bats curl')}",
        },
        {
            "name": "Run Python unit tests",
            "timeout-minutes": "29",
            "run": f"{form.format(150, 'update')}\n{form.format(150, 'install -y jq zsh')}",
        },
        {"name": "Setup for Codecov", "timeout-minutes": "5", "run": form.format(150, "install -y jq curl")},
    ]


def apt_step_problems(workflows: dict[str, dict[str, list[dict]]]) -> list[str]:
    """What would let a stalled apt call outlive its step's name, for `{workflow: {job: steps}}`.

    Steps are keyed by (workflow, job, index), the name carried for the message, so no step replaces another. A
    name used twice in one job is refused on its own: STEP_REST_BUDGET and the exemption table refer to steps by
    name. Then every step with a bounded call has a budget row and the timeout-minutes the formula gives, and
    every budget row has its step."""
    problems, found = [], {}
    for workflow, by_job in workflows.items():
        for job, steps in by_job.items():
            seen: dict[str, int] = {}
            for index, step in enumerate(steps):
                name = step.get("name")
                if name is not None and name in seen:
                    problems.append(f"{workflow}: {job}: step {index} {name!r} repeats the name of step {seen[name]}")
                elif name is not None:
                    seen[name] = index
                bounds = [int(n) for n in APT_BOUND.findall(step_text(step))]
                if bounds:
                    found[(workflow, job, index)] = (name or f"step {index}", sum(n + KILL_AFTER for n in bounds), step)
    names = {name for name, _, _ in found.values()}
    problems.extend(
        f"budget row {name!r} has no step with a bounded apt call" for name in STEP_REST_BUDGET if name not in names
    )
    for (workflow, job, index), (name, apt_seconds, step) in found.items():
        where = f"{workflow}: {job}: step {index} {name!r}"
        if name not in STEP_REST_BUDGET:
            problems.append(f"{where} runs a bounded apt call with no STEP_REST_BUDGET row")
        elif "timeout-minutes" not in step:
            problems.append(f"{where} has no timeout-minutes")
        else:
            expected = math.ceil((apt_seconds + STEP_REST_BUDGET[name]) / 60) + 1
            if int(step["timeout-minutes"]) != expected:
                problems.append(f"{where} has timeout-minutes {step['timeout-minutes']}, the formula gives {expected}")
    return problems


def workflow_texts() -> dict[str, str]:
    return {path.name: path.read_text() for path in sorted(WORKFLOWS.glob("*.y*ml"))}


class MirrorScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = Path(tempfile.mkdtemp(prefix="apt-mirror-"))
        self.addCleanup(lambda: subprocess.run(["rm", "-rf", str(self.temp)], check=False))
        self.list = self.temp / "apt-mirrors.txt"
        (self.temp / "bin").mkdir()
        # A sudo that refuses, so no case can reach the host's own list.
        self.fake("sudo", "echo 'sudo refused by the test' >&2\nexit 1")

    def fake(self, name: str, body: str) -> None:
        path = self.temp / "bin" / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def read_only(self) -> None:
        """Make the list root's to this user, so the script writes it through `sudo -n tee`."""
        self.list.chmod(0o444)
        self.addCleanup(self.list.chmod, 0o644)
        if os.access(self.list, os.W_OK):
            self.skipTest("running as a user who can write a read-only file")

    def through_sudo(self, tee_body: str) -> None:
        """A sudo that runs its command (after checking -n) and a fake tee."""
        self.read_only()
        self.fake("sudo", '[ "$1" = -n ] || exit 64\nshift\nexec "$@"')
        self.fake("tee", tee_body)

    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [SYSTEM_PYTHON, "-I", "-S", str(SCRIPT), *args],
            env={"PATH": f"{self.temp / 'bin'}:/usr/bin:/bin", "HOME": str(self.temp)},
            capture_output=True, text=True, timeout=30, check=False,
        )  # fmt: skip

    def assert_refused(self, result: subprocess.CompletedProcess[str], reason: str) -> None:
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(1, len(result.stderr.splitlines()), result.stderr)
        self.assertIn(reason, result.stderr)

    def test_the_azure_entry_is_removed_and_the_others_kept(self) -> None:
        self.list.write_text(MIRRORS)
        result = self.run_script(str(self.list))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(MIRRORS.split("\n", 1)[1], self.list.read_text())
        self.assertIn("before:", result.stdout)
        self.assertIn("after:", result.stdout)

    def test_a_list_without_the_entry_or_no_list_is_left_alone(self) -> None:
        kept = MIRRORS.split("\n", 1)[1]
        self.list.write_text(kept)
        result = self.run_script(str(self.list))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(kept, self.list.read_text())
        self.assertIn("nothing to change", result.stdout)
        absent = self.run_script(str(self.temp / "absent.txt"))
        self.assertEqual(0, absent.returncode, absent.stderr)
        self.assertIn("absent", absent.stdout)

    def test_a_list_that_would_be_left_empty_is_refused_unchanged(self) -> None:
        only = MIRRORS.split("\n", 1)[0] + "\n"
        self.list.write_text(only)
        self.assert_refused(self.run_script(str(self.list)), "no apt mirror would be left")
        self.assertEqual(only, self.list.read_text())

    def test_only_a_missing_list_is_absent(self) -> None:
        # Audit of db045676: os.path.lexists() read EACCES and ENAMETOOLONG as "absent". Only ENOENT is absent now.
        missing = self.run_script(str(self.temp / "no-such-dir" / "apt-mirrors.txt"))
        self.assertEqual(0, missing.returncode, missing.stderr)
        self.assertIn("is absent", missing.stdout)
        overlong = self.temp / ("x" * 300)
        self.assert_refused(self.run_script(str(overlong)), "File name too long")
        locked = self.temp / "locked"
        locked.mkdir()
        (locked / "apt-mirrors.txt").write_text(MIRRORS)
        locked.chmod(0o000)
        self.addCleanup(locked.chmod, 0o755)
        if os.access(locked / "apt-mirrors.txt", os.R_OK):
            self.skipTest("running as a user who can search a mode-000 directory")
        self.assert_refused(
            self.run_script(str(locked / "apt-mirrors.txt")), f"cannot read {locked}/apt-mirrors.txt: Permission denied"
        )

    def test_a_list_that_cannot_be_read_fails_named_and_is_not_written(self) -> None:
        # Audit of 9a885470: bash's read took a read error for the end of the file. A mode-000 file and a directory.
        self.fake("tee", f'echo tee ran >> "{self.temp}/tee.log"; cat > /dev/null')
        directory = self.temp / "list.d"
        directory.mkdir()
        self.assert_refused(self.run_script(str(directory)), f"cannot read {directory}: Is a directory")
        self.list.write_text(MIRRORS)
        self.list.chmod(0o000)
        self.addCleanup(self.list.chmod, 0o644)
        if not os.access(self.list, os.R_OK):
            self.assert_refused(self.run_script(str(self.list)), f"cannot read {self.list}: Permission denied")
        self.assertFalse((self.temp / "tee.log").exists())

    def test_a_failed_write_fails_named_and_leaves_the_list(self) -> None:
        self.list.write_text(MIRRORS)
        self.read_only()
        self.assert_refused(self.run_script(str(self.list)), "sudo -n tee exited 1: sudo refused by the test")
        self.assertEqual(MIRRORS, self.list.read_text())
        # sudo runs, and tee fails.
        self.through_sudo("cat > /dev/null; echo 'tee: disk full' >&2; exit 5")
        self.assert_refused(self.run_script(str(self.list)), "sudo -n tee exited 5: tee: disk full")
        self.assertEqual(MIRRORS, self.list.read_text())

    def test_a_write_through_sudo_is_read_back_and_kept(self) -> None:
        self.list.write_text(MIRRORS)
        self.through_sudo('chmod 644 "$1" && cat > "$1"')
        result = self.run_script(str(self.list))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(MIRRORS.split("\n", 1)[1], self.list.read_text())

    def test_a_write_that_reads_back_differently_fails_named(self) -> None:
        # tee reports success but leaves other bytes (a truncated or interleaved write).
        self.list.write_text(MIRRORS)
        self.through_sudo('cat > /dev/null; chmod 644 "$1" && printf truncated > "$1"')
        self.assert_refused(self.run_script(str(self.list)), f"{self.list} read back differs from what was written")

    def test_the_only_external_command_is_the_checked_write(self) -> None:
        # Audits of 52035104 and 9a885470: no producer but the write decides anything, and it is checked and bounded.
        text = SCRIPT.read_text()
        self.assertEqual(1, text.count("subprocess.run("))
        self.assertIn('["sudo", "-n", "tee", path]', text)
        self.assertIn("check=True, timeout=WRITE_TIMEOUT", text)
        self.assertNotRegex(text, r"os\.system|os\.popen|shell=True|check=False")

    def test_the_default_list_is_the_runner_image_one(self) -> None:
        self.assertIn('DEFAULT = "/etc/apt/apt-mirrors.txt"', SCRIPT.read_text())
        self.assertIn("actions/runner-images#14823", SCRIPT.read_text())

    def test_the_drop_names_its_re_check(self) -> None:
        # The drop has an exit condition, not an expiry: #14823 was declared mirror-side and healthy on 2026-10-27.
        text = SCRIPT.read_text()
        self.assertIn("when actions/runner-images#14823 is closed", text)
        self.assertIn("three `test (ubuntu-24.04, client)` runs with the drop disabled", text)
        self.assertIn("within 20 percent", text)


class AptJobTest(unittest.TestCase):
    def test_every_job_that_runs_apt_on_ubuntu_drops_the_mirror_first(self) -> None:
        found, late = set(), []
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            for name, job in jobs(path).items():
                if "ubuntu" not in job["keys"].get("runs-on", "") + job_text(path, name):
                    continue
                steps = job["steps"]
                uses = [index for index, step in enumerate(steps) if APT_USE.search(step_text(step))]
                if not uses:
                    continue
                found.add((path.name, name))
                calls = [index for index, step in enumerate(steps) if step.get("run") == CALL]
                if not calls or calls[0] > uses[0]:
                    late.append(f"{path.name}: {name}: first apt use at step {uses[0]}, mirror step at {calls[:1]}")
        self.assertEqual([], late)
        self.assertEqual(APT_JOBS, found)

    def test_the_mirror_is_dropped_in_one_place(self) -> None:
        # One definition: no workflow edits the list itself.
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                self.assertNotIn("apt-mirrors.txt", path.read_text())
                self.assertNotIn("azure.archive", path.read_text().replace("azure\\.archive", ""))


class AptBoundRuleTest(unittest.TestCase):
    """Every apt call a workflow runs ends inside its step: the exact bound form on its own line, or an exemption row
    with a reason. Closed-world, as U99's download rule (decisions.tsv `treadmill-u99-scanner`): the text is matched,
    never parsed."""

    FORM = "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3"

    def test_every_apt_call_in_a_workflow_carries_the_bound_or_is_exempted(self) -> None:
        bad = [hit for name, text in workflow_texts().items() for hit in apt_violations(name, text)]
        self.assertEqual([], bad)

    def test_no_apt_exemption_is_stale(self) -> None:
        texts = workflow_texts()
        self.assertEqual([], apt_stale(texts))
        # The table is the only way out, so a scan that saw fewer calls than test.yaml's two updates and three
        # installs would be a broken scan.
        bounded = sum(len(APT_BOUND.findall(line)) for text in texts.values() for line in text.splitlines())
        self.assertGreaterEqual(bounded, 5)

    def test_the_bypasses_fail(self) -> None:
        for snippet in (
            "sudo apt-get update",
            "sudo apt install -y jq",
            f"{self.FORM} update && sudo apt-get install -y jq",
            "timeout 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=0 180 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 0 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 60 sudo apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 180 sudo apt-get -o Acquire::http::Timeout=0 -o Acquire::Retries=3 update",
            "timeout --kill-after=10 180 sudo apt-get -o Acquire::Retries=3 -o Acquire::http::Timeout=15 update",
            f"{self.FORM} -o acquire::http::timeout=0 update",
            f"{self.FORM} install -y -o Acquire::Retries=0 jq",
            f"{self.FORM} install -y jq -c /tmp/apt.conf",
            f"{self.FORM} install -y jq --config-file=/tmp/apt.conf",
            f"APT_CONFIG=/tmp/apt.conf {self.FORM} update",
            f"{self.FORM} update \\",
            f"{self.FORM} update; timeout 5 true",
            f"{self.FORM} upgrade -y",
            "# sudo apt-get update",
            'echo "apt-get update"',
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual(1, len(apt_violations("x.yaml", snippet + "\n", {})), snippet)

    def test_the_bound_form_passes(self) -> None:
        for snippet in (
            f"{self.FORM} update",
            f"{self.FORM} install -y bats curl iproute2 parallel ruby",
            f"{self.FORM} update && {self.FORM} install -y jq zsh",
            "apt-mirrors.txt and drop-azure-apt-mirror.py are other words",
        ):
            with self.subTest(snippet=snippet):
                self.assertEqual([], apt_violations("x.yaml", snippet + "\n", {}), snippet)

    def test_an_exemption_needs_its_exact_line(self) -> None:
        table = {("x.yaml", "# apt-get runs inside setup.sh"): "comment; names the tool without running it"}
        self.assertEqual([], apt_violations("x.yaml", "  # apt-get runs inside setup.sh\n", table))
        self.assertEqual(1, len(apt_violations("x.yaml", "# apt-get runs inside setup.sh now\n", table)))
        self.assertEqual([], apt_stale({"x.yaml": "  # apt-get runs inside setup.sh\n"}, table))
        self.assertEqual(
            ["x.yaml: # apt-get runs inside setup.sh"],
            apt_stale({"x.yaml": "# apt-get runs inside setup.sh now\n"}, table),
        )

    def test_a_reopening_word_fails_attached_separate_after_equals_or_quoted(self) -> None:
        # Audit of 9058072b: `-cfoo.conf` and `-oDebug::NoLocking=true` passed a regex that saw `-c` and `-o` only
        # as separate words. Each table entry is shown failing in every spelling apt reads, with its cause named.
        for prefix, why in APT_REOPEN_PREFIXES.items():
            value = "Debug::NoLocking=true" if prefix in ("-o", "--option") else "foo.conf"
            for tail in (
                f"{prefix}{value}",
                f"{prefix} {value}",
                f"{prefix}={value}",
                f'"{prefix}{value}"',
                f"'{prefix}' {value}",
                f"{prefix.upper()}{value}",
            ):
                with self.subTest(tail=tail):
                    bad = apt_violations("x.yaml", f"{self.FORM} install -y jq {tail}\n", {})
                    self.assertEqual(1, len(bad), bad)
                    self.assertIn(f"starts with {prefix!r}: {why}", bad[0])
        for part, why in APT_REOPEN_PARTS.items():
            for tail in (part, f"{part.upper()}=0", f"x{part}y", f'"{part} 5"', f"'{part}'"):
                with self.subTest(tail=tail):
                    bad = apt_violations("x.yaml", f"{self.FORM} install -y jq {tail}\n", {})
                    self.assertEqual(1, len(bad), bad)
                    self.assertIn(f"holds {part!r}: {why}", bad[0])
        with self.subTest(tail="an unclosed quote"):
            bad = apt_violations("x.yaml", f'{self.FORM} install -y "jq\n', {})
            self.assertEqual(1, len(bad), bad)
            self.assertIn("cannot be split into shell words: No closing quotation", bad[0])


class BoundOrderTest(unittest.TestCase):
    """A stalled test is named, and its diagnosis printed, before any step or job timeout stops it."""

    def step(self, workflow: str, job: str, name: str) -> dict:
        (step,) = [s for s in jobs(WORKFLOWS / workflow)[job]["steps"] if s.get("name") == name]
        return step

    def test_a_slow_test_then_a_stalled_one_are_both_inside_the_unit_test_step(self) -> None:
        # PR #559: ghostty took 832 s (under the old 1200 s bound) on a slow mirror, then misc stalled; the step's
        # 35 minutes ran out 25 s before misc's bound, so nothing named it. The step holds one earlier test as slow
        # as the bound allows, the stalled test's bound and the other tests' measured time.
        step_seconds = int(self.step("test.yaml", "test", "Run unit test")["timeout-minutes"]) * 60
        self.assertLess(2 * default_bound() + OTHER_TESTS_BUDGET, step_seconds)

    def test_the_unit_test_step_and_the_rest_of_the_job_fit_in_the_job(self) -> None:
        step_seconds = int(self.step("test.yaml", "test", "Run unit test")["timeout-minutes"]) * 60
        job_seconds = int(jobs(WORKFLOWS / "test.yaml")["test"]["keys"]["timeout-minutes"]) * 60
        self.assertLess(PRE_STEP_BUDGET + step_seconds + POST_STEP_BUDGET, job_seconds)

    def test_the_files_steps_fit_the_bound(self) -> None:
        for workflow in ("ubuntu.yaml", "macos.yaml"):
            with self.subTest(workflow=workflow):
                step_seconds = int(self.step(workflow, "build", "Test file existence")["timeout-minutes"]) * 60
                self.assertLess(default_bound() + FILES_STEP_BUDGET, step_seconds)

    def test_no_workflow_raises_the_per_test_bound(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.y*ml")):
            with self.subTest(workflow=path.name):
                self.assertNotIn("BATS_PER_TEST_TIMEOUT:", path.read_text())
                self.assertNotIn("BATS_PER_TEST_TIMEOUT=", path.read_text())

    def test_every_step_that_runs_apt_ends_a_stall_inside_its_own_bound(self) -> None:
        # The step's timeout-minutes is the ceiling of its apt bounds (each N plus the kill delay) plus the measured
        # rest of the step, plus one minute: a stall ends under the step's name, never at the job's timeout.
        parsed = {
            path.name: {job: body["steps"] for job, body in jobs(path).items()}
            for path in sorted(WORKFLOWS.glob("*.y*ml"))
        }
        self.assertEqual([], apt_step_problems(parsed))

    def test_a_step_without_its_bound_cannot_hide_behind_a_later_step_of_the_same_name(self) -> None:
        # Audit of 9058072b: the registry was keyed by step name, so a later "Setup for Codecov" that carried
        # timeout-minutes replaced the earlier one that ran apt without it. Steps are keyed by (job, index) now, and
        # a name used twice in one job is refused on its own, since the budget table refers to steps by name.
        steps = bounded_steps()
        self.assertEqual([], apt_step_problems({"x.yaml": {"test": steps}}))
        del steps[2]["timeout-minutes"]
        later = {**bounded_steps()[2], "run": "echo later\n" + bounded_steps()[2]["run"]}
        problems = apt_step_problems({"x.yaml": {"test": [*steps, later]}})
        self.assertEqual(
            [
                "x.yaml: test: step 3 'Setup for Codecov' repeats the name of step 2",
                "x.yaml: test: step 2 'Setup for Codecov' has no timeout-minutes",
            ],
            problems,
        )
        # The same name in another job is another step; unnamed steps have no name to collide.
        unnamed = {"run": "echo unnamed"}
        self.assertEqual(
            [],
            apt_step_problems({"x.yaml": {"test": [*bounded_steps(), unnamed, unnamed], "other": [later]}}),
        )

    def test_a_bounded_step_off_the_formula_or_outside_the_budget_table_is_named(self) -> None:
        steps = bounded_steps()
        steps[0]["timeout-minutes"] = "9"
        self.assertEqual(
            ["x.yaml: test: step 0 'Install tools' has timeout-minutes 9, the formula gives 10"],
            apt_step_problems({"x.yaml": {"test": steps}}),
        )
        steps = bounded_steps()
        steps[2]["name"] = "Upload coverage"
        self.assertEqual(
            [
                "budget row 'Setup for Codecov' has no step with a bounded apt call",
                "x.yaml: test: step 2 'Upload coverage' runs a bounded apt call with no STEP_REST_BUDGET row",
            ],
            apt_step_problems({"x.yaml": {"test": steps}}),
        )
        steps = bounded_steps()
        del steps[1]["name"]
        self.assertEqual(
            [
                "budget row 'Run Python unit tests' has no step with a bounded apt call",
                "x.yaml: test: step 1 'step 1' runs a bounded apt call with no STEP_REST_BUDGET row",
            ],
            apt_step_problems({"x.yaml": {"test": steps}}),
        )


if __name__ == "__main__":
    unittest.main()
