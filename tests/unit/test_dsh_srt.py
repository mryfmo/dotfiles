"""Exercise scripts/orchestrator/dsh-srt against a fake srt and a fake dsh (regime-cutover U251).

HOME is a scratch directory holding `.dsh/bin/dsh`, a shell script that records its argv, cwd and whole environment
to a file (the launcher starts it under `env -i`, so nothing is read from the environment, and the record path is
baked into each fake). The fake `srt` is first on PATH: it records every argv, answers `--version` from a control
file the test writes (`0.0.81` by default), plays the canary (the probe script runs for real with paths under a
directory that does not exist, so the three probes fail as the sandbox makes them fail; the control file's `canary`
is printed instead when set), and execs the command it is given. The lists the rendered settings must carry are read
from hcom-seat's source text, so a drift between the two files fails here.
"""

import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "scripts/orchestrator/dsh-srt"
SEAT = ROOT / "scripts/orchestrator/hcom-seat"
SYSTEM_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
PYTHON_DIR = str(Path(sys.executable).resolve().parent)
# The names the launcher passes, and nothing else (dsh-srt ENV_NAMES).
ENV_NAMES = {
    "HOME",
    "PATH",
    "USER",
    "DSH_HOME",
    "TMPDIR",
    "LANG",
    "TERM",
    "CLAUDE_CONFIG_DIR",
    "AWS_SHARED_CREDENTIALS_FILE",
    "AWS_CONFIG_FILE",
}
THREE_WORDS = "write-denied read-denied ssh-denied"

FAKE_SRT = r"""#!/usr/bin/env python3
import json, os, subprocess, sys
CALLS = {calls!r}
CONTROL = {control!r}
argv = sys.argv[1:]
with open(CALLS, "a", encoding="utf-8") as calls:
    calls.write(json.dumps({{"argv": argv, "cwd": os.getcwd(), "env": dict(os.environ)}}) + "\n")
control = json.load(open(CONTROL, encoding="utf-8")) if os.path.exists(CONTROL) else {{}}
if argv == ["--version"]:
    version = control.get("version", "0.0.81")
    if version == "fail":
        sys.exit(1)
    print(version)
    sys.exit(0)
command = argv[argv.index("--") + 1 :]
if command[:2] == ["/bin/sh", "-c"]:
    if "canary" in control:
        print(control["canary"])
        sys.exit(0)
    denied = ["/nonexistent-u251/canary", "/nonexistent-u251/settings", "/nonexistent-u251/.ssh"]
    sys.exit(subprocess.run(["/bin/sh", "-c", command[2], command[3], *denied], check=False).returncode)
os.execvp(command[0], command)
"""


def seat_source_lists():
    """The worker seat's lists as hcom-seat's source spells them: the HOME-relative read denies (every `${h}/...`
    entry of the `deny_read=(...)` block and the `deny_read+=(...)` lines), the operator Claude paths, the per-base
    project files and the domain list, each in source order."""
    text = SEAT.read_text()
    block = re.search(r"^\s*deny_read=\((.*?)\)\n", text, re.MULTILINE | re.DOTALL)
    appended = re.findall(r"^\s*deny_read\+=\((.*?)\)\n", text, re.MULTILINE | re.DOTALL)
    under_home = re.findall(r'"\$\{h\}/([A-Za-z0-9._/@+-]+)"', block[1] + "".join(appended))
    claude = re.search(r"operator_claude=\((.*?)\)", text)
    operator = re.findall(r'"\$\{h\}/([A-Za-z0-9._/@+-]+)"', claude[1])
    files_block = re.search(r'^\s*deny_write\+=\("\$\{base\}/(.*?)\)\n', text, re.MULTILINE | re.DOTALL)
    project_files = re.findall(r'"?\$\{base\}/([A-Za-z0-9._/@+-]+)"', '"${base}/' + files_block[1])
    domains = []
    for line in re.findall(r"^\s*domains\+?='(.*)'$", text, re.MULTILINE):
        domains += re.findall(r'"([^"]+)"', line)
    return under_home, operator, project_files, domains


class DshSrtTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.home = root / "home"
        self.dsh_home = self.home / ".dsh"
        (self.dsh_home / "bin").mkdir(parents=True)
        self.calls = root / "calls"
        self.calls.mkdir()
        self.srt_calls = self.calls / "srt"
        self.dsh_record = self.calls / "dsh"
        self.control = self.calls / "srt-control.json"
        self.bindir = root / "bin"
        self.bindir.mkdir()
        (self.bindir / "srt").write_text(FAKE_SRT.format(calls=str(self.srt_calls), control=str(self.control)))
        (self.bindir / "srt").chmod(0o755)
        self.write_fake_dsh(self.dsh_home)
        self.tmpdir = root / "tmp"
        self.tmpdir.mkdir()
        # Built, never inherited: the fake bin, the interpreter the fake srt needs, the system directories.
        self.env = {
            "HOME": str(self.home),
            "PATH": f"{self.bindir}:{PYTHON_DIR}:{SYSTEM_PATH}",
            "TMPDIR": str(self.tmpdir),
            "LANG": "C.UTF-8",
            "TERM": "dumb",
            "USER": "u251",
            "SECRET_OF_THE_CALLER": "never-passed",
        }

    def write_fake_dsh(self, dsh_home):
        dsh = dsh_home / "bin/dsh"
        dsh.parent.mkdir(parents=True, exist_ok=True)
        dsh.write_text(
            "#!/bin/sh\n"
            f"record={shlex.quote(str(self.dsh_record))}\n"
            '{ for a in "$@"; do printf "arg:%s\\n" "$a"; done; printf "cwd:%s\\n" "$(pwd -P)"; '
            'env | sed "s/^/env:/"; } > "$record"\n'
            'echo "fake dsh ran"\n'
        )
        dsh.chmod(0o755)
        return dsh

    def launch(self, *args, cwd=None, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        for key in (key for key, value in overrides.items() if value is None):
            env.pop(key, None)
        return subprocess.run(
            [str(LAUNCHER), *args], cwd=cwd or self.home, env=env, capture_output=True, text=True, check=False
        )

    def srt_calls_made(self):
        if not self.srt_calls.exists():
            return []
        return [json.loads(line) for line in self.srt_calls.read_text().splitlines()]

    def dsh_run(self):
        """The fake dsh's record: its argv, cwd and environment, or None when it never ran."""
        if not self.dsh_record.exists():
            return None
        lines = self.dsh_record.read_text().splitlines()
        argv = [line.removeprefix("arg:") for line in lines if line.startswith("arg:")]
        cwd = next(line.removeprefix("cwd:") for line in lines if line.startswith("cwd:"))
        env = dict(line.removeprefix("env:").split("=", 1) for line in lines if line.startswith("env:"))
        return {"argv": argv, "cwd": cwd, "env": env}

    @staticmethod
    def passed_names(record):
        """The names a recorded environment got from the launcher: without what the process added to its own
        environment (CoreFoundation's `__CF_USER_TEXT_ENCODING` on macOS; a shell's PWD, OLDPWD, SHLVL and `_`)."""
        return set(record) - {"__CF_USER_TEXT_ENCODING", "PWD", "OLDPWD", "SHLVL", "_"}

    def settings_path(self, dsh_home=None):
        return (dsh_home or self.dsh_home) / ".sandbox/srt-settings.json"

    def settings(self, dsh_home=None):
        return json.loads(self.settings_path(dsh_home).read_text())

    @property
    def scratch(self):
        return self.tmpdir / f"dsh-srt-{os.getuid()}"

    def assert_refused(self, run, message):
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertTrue(run.stderr.startswith("dsh-srt: refused: "), run.stderr)
        self.assertIn(message, run.stderr)
        self.assertIsNone(self.dsh_run(), "dsh never starts on a refusal")

    def test_the_rendered_settings_carry_the_worker_seats_lists_read_from_hcom_seat(self):
        run = self.launch("--profile", "thak", "--", "--dump-config")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, "fake dsh ran\n")
        under_home, operator, project_files, domains = seat_source_lists()
        # The source still spells the rows this test was written against (hcom-seat:1743-1746, :1750, :1484, :1720).
        self.assertIn(".ssh", under_home)
        self.assertIn(".local/state/omp-seats", under_home)
        self.assertEqual([".claude", ".claude.json"], operator)
        self.assertIn(".mcp.json", project_files)
        self.assertIn("api.anthropic.com", domains)
        self.assertIn("chatgpt.com", domains)
        settings = self.settings()
        home = str(self.home)
        sandbox = str(self.dsh_home / ".sandbox")
        fs = settings["filesystem"]
        expected_read = [f"{home}/{name}" for name in under_home] + [sandbox] + [f"{home}/{name}" for name in operator]
        self.assertEqual(expected_read, fs["denyRead"], "the worker seat's read denies, verbatim and in order")
        expected_write_deny = (
            [sandbox]
            + [f"{base}/{name}" for base in (str(self.dsh_home), str(self.scratch)) for name in project_files]
            + [f"{home}/{name}" for name in operator]
        )
        self.assertEqual(expected_write_deny, fs["denyWrite"])
        self.assertEqual(
            [str(self.dsh_home), str(self.scratch), str(self.dsh_home / ".state/claude")], fs["allowWrite"]
        )
        self.assertEqual([], fs["allowRead"])
        self.assertEqual(domains, settings["network"]["allowedDomains"], "the worker seat's domain list, verbatim")
        self.assertEqual([], settings["network"]["deniedDomains"])
        self.assertEqual([], settings["network"]["allowUnixSockets"])
        self.assertIs(False, settings["network"]["allowLocalBinding"])
        self.assertIs(True, settings["allowPty"])
        self.assertNotIn("allowNestedUserNamespaces", json.dumps(settings))
        for directory in (self.dsh_home / ".sandbox", self.dsh_home / ".state/claude", self.scratch):
            self.assertTrue(directory.is_dir() and not directory.is_symlink(), directory)
            self.assertEqual(0o700, stat.S_IMODE(os.lstat(directory).st_mode), directory)

    def test_srt_receives_the_version_read_the_canary_and_the_launch(self):
        run = self.launch("--profile", "thak", "--", "--dump-config", "--x", "a b")
        self.assertEqual(run.returncode, 0, run.stderr)
        version, canary, launch = self.srt_calls_made()
        settings = str(self.settings_path())
        self.assertEqual(["--version"], version["argv"])
        self.assertEqual(["--settings", settings, "--", "/bin/sh", "-c"], canary["argv"][:5])
        self.assertEqual(
            ["canary", str(self.dsh_home / ".sandbox/canary"), settings, f"{self.home}/.ssh"], canary["argv"][-4:]
        )
        self.assertIn("ssh-denied", canary["argv"][5])
        self.assertEqual(str(self.scratch), canary["cwd"], "the canary runs where dsh will")
        self.assertEqual(
            [
                "--settings",
                settings,
                "--",
                str(self.dsh_home / "bin/dsh"),
                "--profile",
                "thak",
                "--dump-config",
                "--x",
                "a b",
            ],
            launch["argv"],
        )
        self.assertFalse((self.dsh_home / ".sandbox/canary").exists())
        dsh = self.dsh_run()
        self.assertEqual(["--profile", "thak", "--dump-config", "--x", "a b"], dsh["argv"])
        self.assertEqual(str(self.scratch), dsh["cwd"])
        # Without --profile and with no `--`, dsh gets no argument.
        self.dsh_record.unlink()
        run = self.launch()
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual([], self.dsh_run()["argv"])

    def test_the_environment_is_the_listed_names_and_nothing_else(self):
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        for record in (self.srt_calls_made()[1]["env"], self.srt_calls_made()[2]["env"], self.dsh_run()["env"]):
            self.assertEqual(ENV_NAMES, self.passed_names(record), "the canary, the launch and dsh get the names only")
        env = self.dsh_run()["env"]
        self.assertEqual(str(self.home), env["HOME"])
        self.assertEqual(self.env["PATH"], env["PATH"])
        self.assertEqual("u251", env["USER"])
        self.assertEqual(str(self.dsh_home), env["DSH_HOME"])
        self.assertEqual(str(self.scratch), env["TMPDIR"], "the scratch root is dsh's TMPDIR too")
        self.assertEqual(("C.UTF-8", "dumb"), (env["LANG"], env["TERM"]))
        self.assertEqual(str(self.dsh_home / ".state/claude"), env["CLAUDE_CONFIG_DIR"])
        self.assertEqual(("/dev/null", "/dev/null"), (env["AWS_SHARED_CREDENTIALS_FILE"], env["AWS_CONFIG_FILE"]))
        # A caller name that is unset is not passed as empty, read at srt's launch record (the fake srt is Python,
        # which adds LC_CTYPE to its own environment when LANG is unset, PEP 538). TERM is the exception by bash's
        # own rule: the launcher is a bash script, and bash sets TERM to `dumb` when it starts without one, so the
        # launcher passes that value on.
        self.dsh_record.unlink()
        self.srt_calls.unlink()
        run = self.launch("--", "--version", LANG=None, TERM=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        launch = self.srt_calls_made()[2]["env"]
        self.assertEqual(ENV_NAMES - {"LANG"}, self.passed_names(launch) - {"LC_CTYPE"})
        self.assertEqual("dumb", launch["TERM"])

    def test_a_callers_claude_config_dir_is_denied_like_the_operators_state(self):
        caller = self.home / "claude-config"
        caller.mkdir(parents=True)
        run = self.launch("--", "--version", CLAUDE_CONFIG_DIR=str(caller))
        self.assertEqual(run.returncode, 0, run.stderr)
        fs = self.settings()["filesystem"]
        self.assertIn(str(caller), fs["denyRead"])
        self.assertIn(str(caller), fs["denyWrite"])
        self.assertNotIn(str(caller), fs["allowWrite"])
        self.assertEqual(str(self.dsh_home / ".state/claude"), self.dsh_run()["env"]["CLAUDE_CONFIG_DIR"])
        # ~/.claude itself adds no third entry.
        (self.home / ".claude").mkdir()
        run = self.launch("--", "--version", CLAUDE_CONFIG_DIR=str(self.home / ".claude"))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(1, self.settings()["filesystem"]["denyRead"].count(str(self.home / ".claude")))

    def test_the_render_is_idempotent(self):
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        first = self.settings_path().read_bytes()
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(first, self.settings_path().read_bytes())
        self.assertFalse(self.settings_path().with_suffix(".json.tmp").exists())

    def test_home_comes_from_the_option_the_environment_or_the_default(self):
        other = self.home / "elsewhere/dsh"
        other.mkdir(parents=True)
        self.write_fake_dsh(other)
        run = self.launch("--home", str(other), "--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(str(other), self.dsh_run()["env"]["DSH_HOME"])
        self.assertTrue(self.settings_path(other).exists())
        self.assertFalse(self.settings_path().exists(), "the default home is untouched")
        run = self.launch("--", "--version", DSH_HOME=str(other))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(str(other), self.dsh_run()["env"]["DSH_HOME"])
        self.dsh_record.unlink()
        run = self.launch("--", "--version", DSH_HOME=str(other / "missing"))
        self.assert_refused(run, "is not a directory")

    def test_refusals_exit_2_before_anything_starts(self):
        # No srt on PATH.
        run = self.launch("--", "--version", PATH=f"{PYTHON_DIR}:{SYSTEM_PATH}")
        self.assert_refused(run, "srt (@anthropic-ai/sandbox-runtime) not found on PATH")
        self.assertEqual([], self.srt_calls_made())
        # An srt of another line, one whose version read fails, and one that prints nothing (U141's rule).
        for version in ("0.1.0", "1.0.81", "fail", ""):
            with self.subTest(version=version):
                self.control.write_text(json.dumps({"version": version}))
                run = self.launch("--", "--version")
                self.assert_refused(run, "0.0 line")
                self.assertEqual([["--version"]], [call["argv"] for call in self.srt_calls_made()])
                self.srt_calls.unlink()
        self.control.write_text(json.dumps({"version": "0.0.90"}))
        self.assertEqual(0, self.launch("--", "--version").returncode, "a patch release of the line launches")
        self.control.unlink()
        self.dsh_record.unlink()
        self.srt_calls.unlink()
        # No executable dsh under DSH_HOME.
        (self.dsh_home / "bin/dsh").chmod(0o644)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"no executable dsh under DSH_HOME: {self.dsh_home}/bin/dsh")
        (self.dsh_home / "bin/dsh").unlink()
        self.assert_refused(self.launch("--", "--version"), "no executable dsh under DSH_HOME")
        self.write_fake_dsh(self.dsh_home)
        # The scratch cwd would lie inside a read-denied path (M-21: a denied cwd dies on uv_cwd EPERM).
        denied_tmp = self.home / "Workspace/tmp"
        denied_tmp.mkdir(parents=True)
        run = self.launch("--", "--version", TMPDIR=str(denied_tmp))
        self.assert_refused(run, "would lie inside a read-denied path")
        self.assertFalse((denied_tmp / f"dsh-srt-{os.getuid()}").exists(), "nothing is created")
        # DSH_HOME inside a read-denied path.
        denied_home = self.home / ".codex/dsh"
        denied_home.mkdir(parents=True)
        self.write_fake_dsh(denied_home)
        self.assert_refused(
            self.launch("--home", str(denied_home), "--", "--version"), "lies inside a read-denied path"
        )
        self.assertFalse((denied_home / ".sandbox").exists())
        # A canary that does not answer the three words, and one that leaves the canary file behind.
        for answer in ("write-open read-denied ssh-denied", "write-denied read-open ssh-denied", "", "ok"):
            with self.subTest(canary=answer):
                self.control.write_text(json.dumps({"canary": answer}))
                run = self.launch("--", "--version")
                self.assert_refused(run, f"the sandbox does not hold (canary: {answer}); dsh not started")
        self.control.write_text(json.dumps({"canary": THREE_WORDS}))
        (self.dsh_home / ".sandbox/canary").write_text("")
        # The launcher clears the file before the probe, so a planted one is no failure; a probe that leaves one is.
        self.assertEqual(0, self.launch("--", "--version").returncode)
        self.control.unlink()
        self.dsh_record.unlink()
        # Usage errors.
        for args in (("--profile",), ("--home",), ("--bogus",), ("extra",), ("--profile", "bad name")):
            with self.subTest(args=args):
                run = self.launch(*args)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertTrue(run.stderr.startswith("dsh-srt: refused: "), run.stderr)
        self.assertIsNone(self.dsh_run())

    def test_a_canary_that_runs_for_real_fails_each_probe_the_way_the_sandbox_does(self):
        """The fake srt runs the probe script with three paths under a directory that does not exist, so the launch
        passes only because the script reports each failure as the word the launcher expects."""
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        script = self.srt_calls_made()[1]["argv"][5]
        probe = subprocess.run(
            ["/bin/sh", "-c", script, "canary", "/nonexistent-u251/c", "/nonexistent-u251/s", "/nonexistent-u251/ssh"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual((0, THREE_WORDS + "\n"), (probe.returncode, probe.stdout))
        writable = self.calls / "writable-canary"
        probe = subprocess.run(
            ["/bin/sh", "-c", script, "canary", str(writable), str(LAUNCHER), str(self.calls)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual("write-open read-open ssh-open\n", probe.stdout)
        self.assertTrue(writable.exists())


if __name__ == "__main__":
    unittest.main()
