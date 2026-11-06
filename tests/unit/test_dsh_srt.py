"""Exercise scripts/orchestrator/dsh-srt against a fake srt and a fake dsh (regime-cutover U251, round 2 U251b).

HOME is a scratch directory holding `.dsh/bin/dsh`, a shell script that records its argv, cwd and whole environment
to a file (the launcher starts it under `env -i`, so nothing is read from the environment, and the record path is
baked into each fake). The fake `srt` is first on PATH: it records every argv, answers `--version` from a control
file the test writes (`0.0.81` by default), plays the canary (the probe script runs for real with paths under a
directory that does not exist, so the three probes fail as the sandbox makes them fail; the control file's `canary`
is printed instead when set, `canary_exit` ends the canary with that status, `leave_canary` writes the canary file
behind it), and execs the command it is given. The lists the rendered settings must carry are read from hcom-seat's
source text, so a drift between the two files fails here.

`DSH_SRT_UNDER_TEST` names another launcher file to run (a scratch copy with a guard removed, for the mutation run
of U251b); the default is the checkout's.
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
LAUNCHER = Path(os.environ.get("DSH_SRT_UNDER_TEST") or ROOT / "scripts/orchestrator/dsh-srt")
SEAT = ROOT / "scripts/orchestrator/hcom-seat"
SYSTEM_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
PYTHON = str(Path(sys.executable).resolve())
PYTHON_DIR = str(Path(PYTHON).parent)
# The names the launcher passes to srt, and nothing else (dsh-srt ENV_NAMES).
ENV_NAMES = {
    "HOME",
    "PATH",
    "USER",
    "DSH_HOME",
    "TMPDIR",
    "CLAUDE_CODE_TMPDIR",
    "LANG",
    "TERM",
    "CLAUDE_CONFIG_DIR",
    "AWS_SHARED_CREDENTIALS_FILE",
    "AWS_CONFIG_FILE",
}
# The names srt 0.0.81 adds inside the sandbox on its own (dist/sandbox/sandbox-utils.js generateProxyEnvVars,
# :667-840; measured on macOS 2026-11-06 under the rendered settings). Documented, not asserted absent: the fake srt
# adds none of them, and a real srt adds all of them on top of ENV_NAMES. TMPDIR is set by srt to the value of the
# CLAUDE_CODE_TMPDIR the launcher passes (:688-691), which is why that name is in ENV_NAMES.
SRT_ADDED_ENV_NAMES = {
    "SANDBOX_RUNTIME",
    "TMPDIR",
    "NO_PROXY",
    "no_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "GIT_CONFIG_PARAMETERS",
    "ALL_PROXY",
    "all_proxy",
    "GRPC_PROXY",
    "grpc_proxy",
    "SRT_SSH_PROXY_COMMAND",
    "GIT_SSH_COMMAND",
    "FTP_PROXY",
    "ftp_proxy",
    "RSYNC_PROXY",
    "DOCKER_HTTP_PROXY",
    "DOCKER_HTTPS_PROXY",
    "CLOUDSDK_PROXY_TYPE",
    "CLOUDSDK_PROXY_ADDRESS",
    "CLOUDSDK_PROXY_PORT",
    "CLOUDSDK_PROXY_USERNAME",
    "CLOUDSDK_PROXY_PASSWORD",
    "JAVA_TOOL_OPTIONS",
}
THREE_WORDS = "write-denied read-denied ssh-denied"

FAKE_SRT = r"""#!{python}
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
        status = 0
    else:
        denied = ["/nonexistent-u251/canary", "/nonexistent-u251/settings", "/nonexistent-u251/.ssh"]
        status = subprocess.run(["/bin/sh", "-c", command[2], command[3], *denied], check=False).returncode
    if control.get("leave_canary"):
        open(command[4], "w", encoding="utf-8").close()
    sys.exit(control.get("canary_exit", status))
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


def srt_added_write_paths(home):
    """The paths srt 0.0.81 makes writable without a listing, which the launcher denies (dsh-srt table, from
    sandbox-utils.js:499-517): `/tmp/claude`, `/private/tmp/claude` (on macOS, or where it exists) and
    `~/.npm/_logs`."""
    paths = ["/tmp/claude"]
    if sys.platform == "darwin" or Path("/private/tmp/claude").exists():
        paths.append("/private/tmp/claude")
    return paths + [f"{home}/.npm/_logs"]


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
        (self.bindir / "srt").write_text(
            FAKE_SRT.format(python=PYTHON, calls=str(self.srt_calls), control=str(self.control))
        )
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

    def write_marker_script(self, path, marker):
        """A script that proves it ran by creating `marker`; planted where only a contained dsh could write."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!/bin/sh\n: > {shlex.quote(str(marker))}\necho 0.0.81\n")
        path.chmod(0o755)

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

    @staticmethod
    def mode(path):
        return stat.S_IMODE(os.lstat(path).st_mode)

    def assert_refused(self, run, message):
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertTrue(run.stderr.startswith("dsh-srt: refused: "), run.stderr)
        self.assertIn(message, run.stderr)
        self.assertIsNone(self.dsh_run(), "dsh never starts on a refusal")

    def assert_nothing_contained_ran(self):
        """srt was asked its version at most, never given a command; dsh never ran."""
        self.assertEqual([], [call["argv"] for call in self.srt_calls_made() if call["argv"] != ["--version"]])
        self.assertIsNone(self.dsh_run())

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
            + srt_added_write_paths(home)
        )
        self.assertEqual(expected_write_deny, fs["denyWrite"], "the seat's write denies, then srt's own write paths")
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
        for directory in (
            self.dsh_home / ".sandbox",
            self.dsh_home / ".state",
            self.dsh_home / ".state/claude",
            self.scratch,
        ):
            self.assertTrue(directory.is_dir() and not directory.is_symlink(), directory)
            self.assertEqual(0o700, self.mode(directory), directory)
        self.assertEqual(0o600, self.mode(self.settings_path()), "mktemp's file, renamed whole")
        self.assertEqual([self.settings_path().name], os.listdir(self.dsh_home / ".sandbox"), "no temporary left")

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

    def test_the_environment_passed_to_srt_is_the_listed_names_and_nothing_else(self):
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
        self.assertEqual(str(self.scratch), env["CLAUDE_CODE_TMPDIR"], "the name srt reads for the TMPDIR it sets")
        self.assertEqual(("C.UTF-8", "dumb"), (env["LANG"], env["TERM"]))
        self.assertEqual(str(self.dsh_home / ".state/claude"), env["CLAUDE_CONFIG_DIR"])
        self.assertEqual(("/dev/null", "/dev/null"), (env["AWS_SHARED_CREDENTIALS_FILE"], env["AWS_CONFIG_FILE"]))
        # The names srt adds inside are srt's, none of them a name the launcher passes (TMPDIR is set by both to the
        # same value: the launcher's for srt itself, srt's for the child from CLAUDE_CODE_TMPDIR).
        self.assertEqual({"TMPDIR"}, ENV_NAMES & SRT_ADDED_ENV_NAMES)
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
        self.assertEqual([self.settings_path().name], os.listdir(self.dsh_home / ".sandbox"))

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
        # The scratch cwd would lie inside a path srt makes writable on its own, which the launcher denies.
        srt_tmp = self.home / ".npm/_logs/tmp"
        srt_tmp.mkdir(parents=True)
        run = self.launch("--", "--version", TMPDIR=str(srt_tmp))
        self.assert_refused(run, "would lie inside a path srt makes writable on its own")
        self.assertFalse((srt_tmp / f"dsh-srt-{os.getuid()}").exists(), "nothing is created")
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

    def test_a_json_reader_that_fails_refuses_before_the_canary(self):
        """Standing order 21: the settings check reads python3's status, and a reader that fails is a refusal, not a
        pass; nothing contained runs."""
        reader = self.bindir / "python3"
        reader.write_text("#!/bin/sh\nexit 3\n")
        reader.chmod(0o755)
        run = self.launch("--", "--version")
        self.assert_refused(run, "do not parse as JSON")
        self.assert_nothing_contained_ran()
        self.assertTrue(self.settings_path().exists(), "the file was rendered; its check failed")
        reader.unlink()
        self.assertEqual(0, self.launch("--", "--version").returncode, "the real reader passes the same file")

    def test_a_canary_process_that_fails_or_says_more_refuses(self):
        # The canary process exits non-zero, with the three words printed.
        self.control.write_text(json.dumps({"canary": THREE_WORDS, "canary_exit": 1}))
        run = self.launch("--", "--version")
        self.assert_refused(run, "the sandbox canary did not run under")
        self.assertIsNone(self.dsh_run())
        self.assertEqual(2, len(self.srt_calls_made()), "the version read and the canary, no launch")
        # The canary prints another line after the three words.
        self.srt_calls.unlink()
        self.control.write_text(json.dumps({"canary": THREE_WORDS + "\nwrite-open"}))
        run = self.launch("--", "--version")
        self.assert_refused(run, "the sandbox does not hold (canary: ")
        self.assertEqual(2, len(self.srt_calls_made()))
        # The canary answers the three words but its file exists afterwards.
        self.srt_calls.unlink()
        self.control.write_text(json.dumps({"canary": THREE_WORDS, "leave_canary": True}))
        run = self.launch("--", "--version")
        self.assert_refused(run, f"the sandbox does not hold (canary: {THREE_WORDS}); dsh not started")
        self.assertTrue((self.dsh_home / ".sandbox/canary").exists(), "the leftover the launcher saw")
        self.assertEqual(2, len(self.srt_calls_made()))

    def test_a_runtime_a_contained_dsh_could_have_replaced_never_runs_outside_srt(self):
        dsh = self.dsh_home / "bin/dsh"
        # A dsh runtime writable by its group, or by anyone, is refused before anything runs.
        for mode in (0o775, 0o757, 0o777):
            with self.subTest(mode=oct(mode)):
                dsh.chmod(mode)
                run = self.launch("--", "--version")
                self.assert_refused(run, f"the dsh runtime {dsh} has mode {mode & 0o777:o}")
                self.assertEqual([], self.srt_calls_made(), "refused before srt is even looked up")
        dsh.chmod(0o755)
        # A dsh runtime that is a symbolic link is refused, wherever it points.
        real = self.write_fake_dsh(self.home / "elsewhere")
        dsh.unlink()
        dsh.symlink_to(real)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"the dsh runtime {dsh} is not a regular file of this user")
        self.assertEqual([], self.srt_calls_made())
        dsh.unlink()
        self.write_fake_dsh(self.dsh_home)
        # An srt found under DSH_HOME or the scratch root (a contained dsh may write both) is refused unexecuted,
        # the reproduction of the round-1 P1: the planted file would mark its run, and no mark appears.
        self.scratch.mkdir(mode=0o700)
        for planted in (self.dsh_home / "bin/srt", self.scratch / "srt"):
            with self.subTest(planted=str(planted)):
                marker = self.calls / "planted-ran"
                self.write_marker_script(planted, marker)
                run = self.launch("--", "--version", PATH=f"{planted.parent}:{self.env['PATH']}")
                self.assert_refused(run, f"srt at {planted} lies under a write root of dsh")
                self.assertFalse(marker.exists(), "the planted srt never ran")
                self.assertEqual([], self.srt_calls_made(), "the real fake srt was not reached either")
                planted.unlink()
        # The same for the JSON reader: a python3 planted under DSH_HOME is refused unexecuted.
        marker = self.calls / "planted-python-ran"
        planted = self.dsh_home / "bin/python3"
        self.write_marker_script(planted, marker)
        run = self.launch("--", "--version", PATH=f"{self.bindir}:{planted.parent}:{SYSTEM_PATH}")
        self.assert_refused(run, f"python3 at {planted} lies under a write root of dsh")
        self.assertFalse(marker.exists())
        self.assert_nothing_contained_ran()
        planted.unlink()
        # A symbolic link on PATH whose target lies under a write root is refused by the target.
        link = self.bindir / "python3"
        link.symlink_to(self.dsh_home / "bin/dsh")
        run = self.launch("--", "--version")
        self.assert_refused(run, f"python3 at {link} lies under a write root of dsh")
        link.unlink()
        self.assertEqual(0, self.launch("--", "--version").returncode, run.stderr)

    def test_directories_with_group_or_other_bits_are_refused_and_left_as_they_are(self):
        for directory in (
            self.dsh_home / ".sandbox",
            self.dsh_home / ".state",
            self.dsh_home / ".state/claude",
            self.scratch,
        ):
            for mode in (0o777, 0o750, 0o701):
                with self.subTest(directory=str(directory), mode=oct(mode)):
                    directory.mkdir(parents=True, exist_ok=True)
                    if (self.dsh_home / ".state").exists():
                        (self.dsh_home / ".state").chmod(0o700)
                    directory.chmod(mode)
                    run = self.launch("--", "--version")
                    self.assert_refused(run, f"{directory} has mode {mode:o}; a directory dsh-srt relies on")
                    self.assertEqual(mode, self.mode(directory), "the launcher changes no mode it did not set")
                    self.assert_nothing_contained_ran()
                    if self.srt_calls.exists():
                        self.srt_calls.unlink()
            directory.chmod(0o700)
        self.assertEqual(0, self.launch("--", "--version").returncode, "0700 everywhere launches")
        # A directory that is a symbolic link, and one of another identity (a file), are refused too.
        self.dsh_record.unlink()
        (self.scratch).rmdir()
        other = self.tmpdir / "elsewhere"
        other.mkdir(mode=0o700)
        self.scratch.symlink_to(other)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"{self.scratch} is not a real directory of this user")
        self.scratch.unlink()

    def test_a_planted_settings_link_never_changes_anything_outside_the_sandbox(self):
        """The round-1 P1 reproduction: a link at a predictable name inside `.sandbox` pointed outside every write
        root, and the redirection followed it. Now the file is written through mktemp's name and renamed onto the
        final name, which is refused when it is a link."""
        sandbox = self.dsh_home / ".sandbox"
        sandbox.mkdir(mode=0o700)
        sentinel_tmp = self.home / "sentinel-tmp"
        sentinel_final = self.home / "sentinel-final"
        sentinel_tmp.write_text("untouched\n")
        sentinel_final.write_text("untouched\n")
        (sandbox / "srt-settings.json.tmp").symlink_to(sentinel_tmp)
        (sandbox / "srt-settings.json").symlink_to(sentinel_final)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"the settings file {sandbox}/srt-settings.json is not a regular file of this user")
        self.assertEqual("untouched\n", sentinel_final.read_text())
        self.assertEqual("untouched\n", sentinel_tmp.read_text())
        self.assert_nothing_contained_ran()
        self.assertEqual(
            {"srt-settings.json.tmp", "srt-settings.json"}, set(os.listdir(sandbox)), "no temporary file left"
        )
        # With the final name free, the planted `.tmp` link is never opened: the sentinel stays, and the settings
        # are a regular 0600 file of this user.
        (sandbox / "srt-settings.json").unlink()
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual("untouched\n", sentinel_tmp.read_text())
        settings = sandbox / "srt-settings.json"
        self.assertTrue(settings.is_file() and not settings.is_symlink())
        self.assertEqual(0o600, self.mode(settings))
        self.assertEqual({"srt-settings.json.tmp", "srt-settings.json"}, set(os.listdir(sandbox)))
        # A final name that is a regular file of this user but open to its group is refused as well.
        settings.chmod(0o664)
        self.dsh_record.unlink()
        run = self.launch("--", "--version")
        self.assert_refused(run, f"the settings file {settings} has mode 664")

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
