"""Exercise scripts/orchestrator/dsh-srt against a fake srt and a fake dsh (regime-cutover U251, rounds 2 to 4: U251b,
U251c, U251d).

HOME is a scratch directory holding `.dsh/bin/dsh`, a shell script that records its argv, cwd, whole environment and
the `node` its PATH finds to a file (the launcher drops the caller's environment before its first command, so nothing
is read from the environment, and the record path is baked into each fake). The fake `srt` is first on PATH: it
records every argv with the argv its interpreter was started with (`sys.orig_argv`, which tells an explicit
`<interpreter> <srt>` start from the kernel's `#!` lookup), answers `--version` from a control file the test writes
(`0.0.81` by default), plays the canary (the probe script runs for real with paths under a directory that does not
exist, so the three probes fail as the sandbox makes them fail; the control file's `canary` is printed instead when
set, `canary_exit` ends the canary with that status, `leave_canary` writes the canary file behind it), and execs the
command it is given. Its `#!` line is the test interpreter's absolute path by default; `use_env_node_srt` rewrites it
as `/usr/bin/env node`, the real srt's line, with a `node` link to the interpreter in its own directory on the
caller's PATH. The fake tool directory also holds `bwrap`, `socat` and `rg` as copies of the system `true` binary, so
the Linux branch of the launcher (which pins them for srt) reaches the canary. The lists the rendered settings must
carry are read from hcom-seat's source text, so a drift between the two files fails here.

`DSH_SRT_UNDER_TEST` names another launcher file to run (a scratch copy with a guard removed, for the mutation run
of U251b); the default is the checkout's. `launcher_with` writes such a copy itself, pinned by a manifest beside it,
to inject failures into the system producers the launcher names by absolute path (`stat`, `readlink`); `lying_stat`
is a `stat` that passes every call through to the real one and rewrites chosen lines, so a producer can answer
garbage for one path while the launcher's bootstrap check of its own tools still passes.
"""

import hashlib
import json
import os
import re
import shlex
import shutil
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
TRUE = next(path for path in ("/usr/bin/true", "/bin/true") if Path(path).exists())
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
# The programs the launcher may run before containment besides the pinned node and srt pair: its own table, and the
# three paths it names without running them there (`/bin/sh` and `/usr/bin/env` run inside the sandbox, under srt;
# `/usr/bin/sandbox-exec` is only existence-checked).
INSIDE_OR_CHECKED_ONLY = {"/bin/sh", "/usr/bin/env", "/usr/bin/sandbox-exec"}
# Helpers earlier rounds ran before containment, or the auditors planted: none may be looked up now. `sed`, `shasum`
# and `sha256sum` are left out, since `lever_self_check` (the shared U31 form, out of this unit's scope) looks them up.
PLANTABLE = (
    "python3",
    "env",
    "head",
    "uname",
    "stat",
    "readlink",
    "mkdir",
    "rm",
    "mktemp",
    "mv",
    "cut",
    "awk",
    "ls",
    "id",
    "cat",
)

FAKE_SRT = r"""#!{shebang}
import json, os, subprocess, sys
CALLS = {calls!r}
CONTROL = {control!r}
argv = sys.argv[1:]
with open(CALLS, "a", encoding="utf-8") as calls:
    calls.write(
        json.dumps({{"argv": argv, "cwd": os.getcwd(), "env": dict(os.environ), "orig_argv": sys.orig_argv}}) + "\n"
    )
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

# A `stat` that runs the real one and rewrites its answer: every path under the fakes directory reads as root's 0755
# (so the launcher's bootstrap accepts the fakes as system tools), and one chosen path reads as GARBLE (a line, or
# no line at all when GARBLE is None).
LYING_STAT = """#!@PYTHON@
import subprocess, sys
args = sys.argv[1:]
GARBLE_PATH = @GARBLE_PATH@
GARBLE = @GARBLE@
paths = args[args.index("--") + 1 :]
run = subprocess.run(["/usr/bin/stat", *args], capture_output=True, text=True, check=False)
out = []
for path, line in zip(paths, run.stdout.splitlines()):
    if path.startswith(@FAKES@):
        line = "0 755"
    elif path == GARBLE_PATH:
        if GARBLE is None:
            continue
        line = GARBLE
    out.append(line + "\\n")
sys.stdout.write("".join(out))
sys.stderr.write(run.stderr)
sys.exit(run.returncode)
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


def launcher_system_tools():
    """The launcher's SYSTEM_TOOLS table, and every `/usr/bin/<name>` or `/bin/<name>` token of its code lines (the
    comment lines left out), so the test can hold the two to each other."""
    text = LAUNCHER.read_text()
    table = re.search(r"^SYSTEM_TOOLS=\((.*?)\)$", text, re.MULTILINE)
    tools = table[1].split()
    code = [line for line in text.splitlines() if not line.lstrip().startswith("#")]
    named = set()
    for line in code:
        named.update(re.findall(r"(?<![\w/.}-])(/usr/bin/[a-z0-9_-]+|/bin/[a-z0-9_-]+)", line))
    return tools, named, code


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
        self.root = root
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
        # Explicit: the launcher trusts a tool directory only with no group or other write, whatever the umask.
        self.bindir.chmod(0o755)
        self.write_fake_srt(PYTHON)
        # The Linux branch pins srt's own tools for the settings; binaries, since the launcher refuses a script there.
        for tool in ("bwrap", "socat", "rg"):
            shutil.copy(TRUE, self.bindir / tool)
            (self.bindir / tool).chmod(0o755)
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
        # What the launcher builds from the fake srt's directory, its interpreter's directory and the system
        # directories (dsh-srt RUN_PATH).
        self.run_path = f"{self.bindir}:{PYTHON_DIR}:{SYSTEM_PATH}"

    def inner_path_for(self, path):
        """What dsh gets inside for a caller PATH: RUN_PATH, then the caller's absolute entries that exist, each in
        physical form (`/bin` is `/usr/bin` on a merged-usr Linux)."""
        entries = [os.path.realpath(d) for d in path.split(":") if d.startswith("/") and os.path.isdir(d)]
        return ":".join([self.run_path, *entries])

    @property
    def inner_path(self):
        return self.inner_path_for(self.env["PATH"])

    def write_fake_srt(self, shebang, bindir=None):
        srt = (bindir or self.bindir) / "srt"
        srt.write_text(FAKE_SRT.format(shebang=shebang, calls=str(self.srt_calls), control=str(self.control)))
        srt.chmod(0o755)
        return srt

    def use_env_node_srt(self):
        """The real srt's form: `#!/usr/bin/env node`, with `node` a link to the test interpreter in its own 0755
        directory first on the caller's PATH, so the launcher must look the interpreter up once, pin it and start srt
        as `<interpreter> <srt>`. Returns the directory."""
        self.write_fake_srt("/usr/bin/env node")
        interp = self.root / "interp"
        interp.mkdir()
        interp.chmod(0o755)
        (interp / "node").symlink_to(PYTHON)
        self.env["PATH"] = f"{interp}:{self.env['PATH']}"
        self.run_path = f"{self.bindir}:{interp}:{SYSTEM_PATH}"
        return interp

    def launcher_with(self, replacements):
        """A scratch copy of the launcher with each literal replaced, pinned by a manifest beside it so
        `lever_self_check` accepts the copy (the form of U251b's mutation run, Verification 5), for injecting a
        failure into a producer the launcher names by its absolute path."""
        root = self.root / "copy"
        copy = root / "scripts/orchestrator/dsh-srt"
        copy.parent.mkdir(parents=True, exist_ok=True)
        text = LAUNCHER.read_text()
        for old, new in replacements.items():
            self.assertIn(old, text, "the launcher still names the producer this test replaces")
            text = text.replace(old, new)
        copy.write_text(text)
        copy.chmod(0o755)
        manifest = root / "home/dot_agents/agent-config.yaml"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(f"      dsh-srt: {hashlib.sha256(copy.read_bytes()).hexdigest()}\n")
        return copy

    @property
    def fakes(self):
        fakes = self.root / "fakes"
        fakes.mkdir(exist_ok=True)
        return fakes

    def fake_tool(self, name, script):
        path = self.fakes / name
        path.write_text(script)
        path.chmod(0o755)
        return path

    def lying_stat(self, garble_path=None, garble=None):
        """A `stat` that passes through to the real one, reads the fakes directory as root's 0755 and answers
        `garble` (a line, or none) for `garble_path`."""
        text = (
            LYING_STAT.replace("@PYTHON@", PYTHON)
            .replace("@FAKES@", repr(str(self.fakes) + "/"))
            .replace("@GARBLE_PATH@", repr(garble_path and str(garble_path)))
            .replace("@GARBLE@", repr(garble))
        )
        return self.fake_tool("stat", text)

    def write_fake_dsh(self, dsh_home):
        dsh = dsh_home / "bin/dsh"
        dsh.parent.mkdir(parents=True, exist_ok=True)
        dsh.write_text(
            "#!/bin/sh\n"
            f"record={shlex.quote(str(self.dsh_record))}\n"
            '{ for a in "$@"; do printf "arg:%s\\n" "$a"; done; printf "cwd:%s\\n" "$(pwd -P)"; '
            'printf "node:%s\\n" "$(command -v node || echo none)"; '
            'env | sed "s/^/env:/"; } > "$record"\n'
            'echo "fake dsh ran"\n'
        )
        dsh.chmod(0o755)
        return dsh

    def write_marker_script(self, path, marker):
        """A script that proves it ran by creating `marker`; planted where only a contained dsh could write, or on
        the caller's PATH under a helper's name."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"#!/bin/sh\n: > {shlex.quote(str(marker))}\necho 0.0.81\n")
        path.chmod(0o755)

    def launch(self, *args, cwd=None, launcher=None, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        for key in (key for key, value in overrides.items() if value is None):
            env.pop(key, None)
        return subprocess.run(
            [str(launcher or LAUNCHER), *args],
            cwd=cwd or self.home,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def srt_calls_made(self):
        if not self.srt_calls.exists():
            return []
        return [json.loads(line) for line in self.srt_calls.read_text().splitlines()]

    def dsh_run(self):
        """The fake dsh's record: its argv, cwd, environment and the `node` its PATH found, or None when it never
        ran."""
        if not self.dsh_record.exists():
            return None
        lines = self.dsh_record.read_text().splitlines()
        argv = [line.removeprefix("arg:") for line in lines if line.startswith("arg:")]
        cwd = next(line.removeprefix("cwd:") for line in lines if line.startswith("cwd:"))
        node = next(line.removeprefix("node:") for line in lines if line.startswith("node:"))
        env = dict(line.removeprefix("env:").split("=", 1) for line in lines if line.startswith("env:"))
        return {"argv": argv, "cwd": cwd, "node": node, "env": env}

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

    def assert_nothing_started(self):
        """srt never ran at all, and no directory of the launcher's exists."""
        self.assertEqual([], self.srt_calls_made(), "srt never started")
        self.assertIsNone(self.dsh_run())
        self.assertFalse((self.dsh_home / ".sandbox").exists(), "nothing created")
        self.assertFalse(self.scratch.exists())

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
        if sys.platform.startswith("linux"):
            # hcom-seat:1654-1669: srt's own tools, pinned to the fixture's binaries and named for srt to run by path.
            self.assertEqual(str(self.bindir / "bwrap"), settings["bwrapPath"])
            self.assertEqual(str(self.bindir / "socat"), settings["socatPath"])
            self.assertEqual({"command": str(self.bindir / "rg")}, settings["ripgrep"])
        else:
            self.assertNotIn("bwrapPath", settings)
        for directory in (
            self.dsh_home / ".sandbox",
            self.dsh_home / ".state",
            self.dsh_home / ".state/claude",
            self.scratch,
        ):
            self.assertTrue(directory.is_dir() and not directory.is_symlink(), directory)
            self.assertEqual(0o700, self.mode(directory), directory)
        self.assertEqual(0o600, self.mode(self.settings_path()), "created O_EXCL under umask 077")
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
                "/usr/bin/env",
                f"PATH={self.inner_path}",
                str(self.dsh_home / "bin/dsh"),
                "--profile",
                "thak",
                "--dump-config",
                "--x",
                "a b",
            ],
            launch["argv"],
            "dsh runs by its path with the composed inner PATH applied under srt (hcom-seat:1868)",
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
        probe, canary, launch = self.srt_calls_made()
        for record in (probe["env"], canary["env"], launch["env"], self.dsh_run()["env"]):
            self.assertEqual(
                ENV_NAMES, self.passed_names(record), "the probe, the canary, the launch and dsh: the names only"
            )
        for record in (probe, canary, launch):
            self.assertEqual(self.run_path, record["env"]["PATH"], "srt gets RUN_PATH, nothing of the caller's PATH")
        env = self.dsh_run()["env"]
        self.assertEqual(str(self.home), env["HOME"])
        self.assertEqual(self.inner_path, env["PATH"], "dsh gets RUN_PATH, then the caller's entries")
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
        # The environment is reduced by the shell itself, with no `env -i`: an exported name bash cannot drop
        # (SHELLOPTS, which bash imports readonly) is a refusal before anything runs, not a leak.
        self.dsh_record.unlink()
        self.srt_calls.unlink()
        run = self.launch("--", "--version", SHELLOPTS="braceexpand")
        self.assert_refused(run, "cannot drop SHELLOPTS from the environment")
        self.assertEqual([], self.srt_calls_made(), "srt never started")

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
        # The settings directory is made fresh before the probe, so a planted canary file is no failure; a probe
        # that leaves one is.
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

    def test_no_program_found_on_path_runs_before_containment(self):
        """The round-3 P1s (f1 s10, f2 s10): the JSON reader `python3` and the other helpers were looked up on the
        caller's PATH and ran before containment, a 0775 one among them. Now nothing is looked up but srt and its
        interpreter: a directory first on PATH planting every helper name, `stat` as a 0775 copy, is never run, and
        the launcher's own table names absolute system binaries only."""
        planted = self.root / "planted"
        planted.mkdir()
        planted.chmod(0o755)
        markers = {}
        for name in PLANTABLE:
            markers[name] = self.calls / f"planted-{name}-ran"
            self.write_marker_script(planted / name, markers[name])
        (planted / "stat").chmod(0o775)
        run = self.launch("--", "--version", PATH=f"{planted}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual({}, {name: marker for name, marker in markers.items() if marker.exists()}, "none ran")
        for call in self.srt_calls_made():
            self.assertEqual([PYTHON, str(self.bindir / "srt")], call["orig_argv"][:2])
            # The fake srt's interpreter is the test's python, so the name is judged by basename, not substring.
            self.assertEqual([], [arg for arg in call["argv"] + call["orig_argv"] if Path(arg).name == "python3"])
            self.assertEqual([], [arg for arg in call["orig_argv"] if arg.startswith(str(planted))])
            self.assertEqual(self.run_path, call["env"]["PATH"])
        self.assertEqual(["--version"], self.dsh_run()["argv"])
        # The same with a `python3` planted under DSH_HOME first on PATH, the round-3 reproduction's place: it is
        # neither run nor refused, since nothing looks it up, and its directory never reaches dsh.
        self.dsh_record.unlink()
        marker = self.calls / "planted-python-ran"
        self.write_marker_script(self.dsh_home / "bin/python3", marker)
        run = self.launch("--", "--version", PATH=f"{self.dsh_home}/bin:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(marker.exists())
        self.assertEqual(self.inner_path, self.dsh_run()["env"]["PATH"], "the write-root entry is dropped")
        # The launcher's table: absolute system binaries, root's, none a script; every system path its code names
        # is in the table or runs inside the sandbox only (`/bin/sh`, `/usr/bin/env` under srt) or is only
        # existence-checked (`/usr/bin/sandbox-exec`); and no helper of the earlier rounds is named in code.
        tools, named, code = launcher_system_tools()
        self.assertEqual({"/usr/bin/stat", "/usr/bin/readlink", "/bin/mkdir", "/bin/rm"}, set(tools))
        for tool in tools:
            with self.subTest(tool=tool):
                self.assertTrue(tool.startswith(("/usr/bin/", "/bin/")))
                self.assertEqual(0, os.stat(tool).st_uid, "root's")
                self.assertEqual(0, stat.S_IMODE(os.stat(tool).st_mode) & 0o022, "closed to group and other")
                self.assertNotEqual(b"#!", Path(tool).read_bytes()[:2], "a binary, not a script")
        self.assertEqual(set(), named - set(tools) - INSIDE_OR_CHECKED_ONLY, "no other system path is run")
        for helper in ("python3", "uname", "/usr/bin/head", "env -i", "mktemp", "/bin/mv"):
            self.assertEqual([], [line for line in code if helper in line], helper)

    def test_a_caller_path_entry_is_resolved_physically_and_judged_before_it_reaches_dsh(self):
        """The round-3 P2 (f1 s3): a symbolic link outside DSH_HOME pointing into `DSH_HOME/bin` survived the
        write-root check and entered the inner PATH. Now each entry is resolved physically first, the write-root
        rule judges the physical path, and dsh gets the physical form; an entry failing the trust rule is dropped and
        named in one stderr line, since it runs inside containment only."""
        alias = self.root / "alias"
        alias.symlink_to(self.dsh_home / "bin")
        via_link = self.root / "via-link"
        via_link.symlink_to(self.bindir)
        run = self.launch("--", "--version", PATH=f"{alias}:{via_link}:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual("", run.stderr, "a write-root entry is dropped silently, by design")
        path = self.dsh_run()["env"]["PATH"]
        self.assertNotIn(str(alias), path.split(":"))
        self.assertNotIn(f"{self.dsh_home}/bin", path.split(":"), "the alias into DSH_HOME/bin is gone")
        self.assertNotIn(str(via_link), path.split(":"), "the other link is handed to dsh in physical form")
        self.assertEqual(
            f"{self.run_path}:{self.bindir}:{self.inner_path_for(self.env['PATH'])[len(self.run_path) + 1 :]}", path
        )
        # A 0775 directory on the caller's PATH, and one under a 0777 ancestor: dropped, named, dsh still starts.
        self.dsh_record.unlink()
        loose = self.root / "loose"
        loose.mkdir()
        loose.chmod(0o775)
        open_parent = self.root / "open"
        (open_parent / "bin").mkdir(parents=True)
        open_parent.chmod(0o777)
        run = self.launch("--", "--version", PATH=f"{loose}:{open_parent}/bin:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stdout)
        self.assertEqual(
            "dsh-srt: dropped from dsh's PATH (writable by group or other, or not root's or this user's): "
            f"{loose} (mode 775), {open_parent}/bin (under {open_parent}, mode 777)\n",
            run.stderr,
        )
        self.assertEqual(self.inner_path, self.dsh_run()["env"]["PATH"])
        # Relative and empty entries (the cwd) are never searched for srt and never handed to dsh.
        self.dsh_record.unlink()
        (self.home / "bin").mkdir()
        self.write_marker_script(self.home / "bin/srt", self.calls / "relative-srt-ran")
        run = self.launch("--", "--version", PATH=f":bin:.:{self.env['PATH']}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse((self.calls / "relative-srt-ran").exists())
        self.assertEqual(self.inner_path, self.dsh_run()["env"]["PATH"])

    def test_a_writable_ancestor_of_a_trusted_path_is_refused_naming_it(self):
        """The round-3 P2 (f1 s10): the trust rule covered the tool file and its directory only, so beneath a
        publicly writable, non-sticky ancestor another user could rename the trusted subtree. Now the rule walks
        every component up to `/` for srt, its interpreter, DSH_HOME and TMPDIR; a sticky directory of root's
        (`/tmp`) is the one exception, and a sticky directory of this user's is not."""
        open_parent = self.root / "open"
        open_parent.mkdir()
        open_parent.chmod(0o777)
        # srt's directory under the open ancestor.
        (open_parent / "bin").mkdir()
        self.write_fake_srt(PYTHON, open_parent / "bin")
        run = self.launch("--", "--version", PATH=f"{open_parent}/bin:{PYTHON_DIR}:{SYSTEM_PATH}")
        self.assert_refused(
            run,
            f"the directory of srt {open_parent}/bin lies under {open_parent}: mode 777, writable by group or other"
            " and not a sticky directory of root's",
        )
        self.assert_nothing_started()
        # DSH_HOME under it.
        other = open_parent / "dsh"
        self.write_fake_dsh(other)
        run = self.launch("--home", str(other), "--", "--version")
        self.assert_refused(run, f"DSH_HOME {other} lies under {open_parent}: mode 777")
        self.assertFalse((other / ".sandbox").exists())
        self.assert_nothing_started()
        # TMPDIR under it.
        (open_parent / "tmp").mkdir()
        run = self.launch("--", "--version", TMPDIR=f"{open_parent}/tmp")
        self.assert_refused(run, f"TMPDIR {open_parent}/tmp lies under {open_parent}: mode 777")
        self.assert_nothing_started()
        # A sticky bit does not excuse a directory of this user's.
        open_parent.chmod(0o1777)
        run = self.launch("--", "--version", TMPDIR=f"{open_parent}/tmp")
        self.assert_refused(run, f"TMPDIR {open_parent}/tmp lies under {open_parent}: mode 1777")
        # Another owner is refused by name too: the fixture cannot change owners, so a lying `stat` says so.
        copy = self.launcher_with({"/usr/bin/stat": str(self.lying_stat(self.dsh_home, f"{os.getuid() + 1} 755"))})
        run = self.launch("--", "--version", launcher=copy)
        self.assert_refused(
            run, f"DSH_HOME {self.dsh_home}: owned by uid {os.getuid() + 1}, neither root nor this user"
        )
        self.assert_nothing_started()
        # The exception: `/tmp` is a sticky directory of root's on macOS (`/private/tmp`) and Linux, so a DSH_HOME
        # there launches although `/tmp` is world-writable.
        with tempfile.TemporaryDirectory(dir="/tmp") as under_tmp:
            home = Path(under_tmp).resolve() / "dsh"
            self.write_fake_dsh(home)
            run = self.launch("--home", str(home), "--", "--version")
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(str(home), self.dsh_run()["env"]["DSH_HOME"])

    def test_directories_with_group_or_other_bits_are_refused_and_left_as_they_are(self):
        for directory in (
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
        # The settings directory is the exception: it is this launch's own, replaced whole, so a 0777 one of this
        # user's is not refused but gone, a fresh 0700 one in its place.
        self.dsh_record.unlink()
        (self.dsh_home / ".sandbox").chmod(0o777)
        self.assertEqual(0, self.launch("--", "--version").returncode)
        self.assertEqual(0o700, self.mode(self.dsh_home / ".sandbox"))
        # A directory that is a symbolic link, and one of another identity (a file), are refused too.
        self.dsh_record.unlink()
        (self.scratch).rmdir()
        other = self.tmpdir / "elsewhere"
        other.mkdir(mode=0o700)
        self.scratch.symlink_to(other)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"{self.scratch} is not a real directory of this user")
        self.scratch.unlink()

    def test_the_settings_directory_is_made_fresh_and_a_planted_link_is_never_followed(self):
        """The round-1 P1 reproduction: a link at a predictable name inside `.sandbox` pointed outside every write
        root, and the redirection followed it. Now the directory is removed and created anew by `mkdir -m 0700` on
        every launch and the file is created O_EXCL under noclobber, so whatever was planted is gone before the
        first open: the sentinels stay as they are and the launch goes through."""
        sandbox = self.dsh_home / ".sandbox"
        sandbox.mkdir()
        sandbox.chmod(0o777)
        sentinel_a = self.home / "sentinel-a"
        sentinel_b = self.home / "sentinel-b"
        sentinel_a.write_text("untouched\n")
        sentinel_b.write_text("untouched\n")
        (sandbox / "srt-settings.json").symlink_to(sentinel_a)
        (sandbox / ".srt-settings.planted").symlink_to(sentinel_b)
        (sandbox / "canary").write_text("")
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(("untouched\n", "untouched\n"), (sentinel_a.read_text(), sentinel_b.read_text()))
        self.assertTrue(sandbox.is_dir() and not sandbox.is_symlink())
        self.assertEqual(0o700, self.mode(sandbox))
        self.assertEqual(["srt-settings.json"], os.listdir(sandbox), "the planted names are gone, no temporary left")
        settings = sandbox / "srt-settings.json"
        self.assertTrue(settings.is_file() and not settings.is_symlink())
        self.assertEqual(0o600, self.mode(settings))
        # A `.sandbox` that is itself a link to a directory elsewhere, or a regular file, is refused and left alone:
        # the launcher removes only a real directory of this user.
        self.dsh_record.unlink()
        self.srt_calls.unlink()
        shutil.rmtree(sandbox)
        elsewhere = self.home / "elsewhere"
        elsewhere.mkdir(mode=0o700)
        (elsewhere / "keep").write_text("kept\n")
        sandbox.symlink_to(elsewhere)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"{sandbox} is not a real directory of this user")
        self.assertEqual("kept\n", (elsewhere / "keep").read_text())
        self.assert_nothing_contained_ran()
        sandbox.unlink()
        sandbox.write_text("not a directory\n")
        run = self.launch("--", "--version")
        self.assert_refused(run, f"{sandbox} is not a real directory of this user")
        self.assertEqual("not a directory\n", sandbox.read_text())
        sandbox.unlink()
        # A settings file opened to its group by an earlier launch is replaced with the directory.
        self.assertEqual(0, self.launch("--", "--version").returncode)
        settings.chmod(0o664)
        self.dsh_record.unlink()
        self.assertEqual(0, self.launch("--", "--version").returncode)
        self.assertEqual(0o600, self.mode(settings))

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

    def test_the_version_probe_runs_under_the_reduced_environment(self):
        """The round-2 P2 (f10 s3): the srt version read ran before the environment reduction and received the
        caller's variables. Now it is the first command under the one environment: the names of ENV_NAMES, the
        values the launcher sets, PATH the RUN_PATH it built, and nothing of the caller's."""
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        probe = self.srt_calls_made()[0]
        self.assertEqual(["--version"], probe["argv"])
        self.assertEqual(ENV_NAMES, self.passed_names(probe["env"]))
        self.assertNotIn("SECRET_OF_THE_CALLER", probe["env"])
        self.assertEqual(self.run_path, probe["env"]["PATH"])
        self.assertEqual(str(self.home), probe["env"]["HOME"])
        self.assertEqual("u251", probe["env"]["USER"])
        self.assertEqual(str(self.dsh_home), probe["env"]["DSH_HOME"])
        self.assertEqual(
            (str(self.scratch), str(self.scratch)), (probe["env"]["TMPDIR"], probe["env"]["CLAUDE_CODE_TMPDIR"])
        )
        self.assertEqual(str(self.dsh_home / ".state/claude"), probe["env"]["CLAUDE_CONFIG_DIR"])
        self.assertEqual(
            ("/dev/null", "/dev/null"), (probe["env"]["AWS_SHARED_CREDENTIALS_FILE"], probe["env"]["AWS_CONFIG_FILE"])
        )
        # The probe is started as `<interpreter> <srt>`, the pinned argv, like the canary and the launch.
        for call in self.srt_calls_made():
            self.assertEqual([PYTHON, str(self.bindir / "srt")], call["orig_argv"][:2], call["argv"])

    def test_a_planted_interpreter_never_runs_outside_srt(self):
        """The round-2 P1 (f2 s10) reproduction: srt is a `/usr/bin/env node` script, so the kernel looked `node` up
        on the caller's PATH and a planted `DSH_HOME/bin/node` ran outside containment. Now the launcher looks the
        interpreter up once, refuses it under a write root or in a path writable by group or other, and starts srt as
        `<node> <srt>` under RUN_PATH, so the planted file's marker never appears."""
        interp = self.use_env_node_srt()
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 0, run.stderr)
        for call in self.srt_calls_made():
            self.assertEqual(
                [PYTHON, str(self.bindir / "srt")], call["orig_argv"][:2], "no `#!` lookup left to the kernel"
            )
            self.assertEqual(self.run_path, call["env"]["PATH"])
        self.assertEqual(str(interp / "node"), self.dsh_run()["node"], "inside, dsh finds the pinned interpreter first")
        self.dsh_record.unlink()
        self.srt_calls.unlink()
        # A node planted under DSH_HOME or the scratch root (the first launch created it), first on the caller's PATH:
        # refused unexecuted, srt never started.
        for planted in (self.dsh_home / "bin/node", self.scratch / "node"):
            with self.subTest(planted=str(planted)):
                marker = self.calls / "planted-node-ran"
                self.write_marker_script(planted, marker)
                run = self.launch("--", "--version", PATH=f"{planted.parent}:{self.env['PATH']}")
                self.assert_refused(run, f"node at {planted} lies under a write root of dsh")
                self.assertFalse(marker.exists(), "the planted node never ran")
                self.assertEqual([], self.srt_calls_made(), "srt was not started either")
                self.assertIsNone(self.dsh_run())
                planted.unlink()
        # A node in a directory open to its group, or a node file open to its group, outside every write root: refused
        # by the trust rule, the marker absent.
        loose_dir = self.root / "loose"
        marker = self.calls / "loose-node-ran"
        self.write_marker_script(loose_dir / "node", marker)
        loose_dir.chmod(0o775)
        run = self.launch("--", "--version", PATH=f"{loose_dir}:{self.env['PATH']}")
        self.assert_refused(run, f"the directory of node {loose_dir}: mode 775, writable by group or other")
        loose_dir.chmod(0o755)
        (loose_dir / "node").chmod(0o775)
        run = self.launch("--", "--version", PATH=f"{loose_dir}:{self.env['PATH']}")
        self.assert_refused(run, f"node {loose_dir}/node: mode 775, writable by group or other")
        self.assertFalse(marker.exists())
        self.assertEqual([], self.srt_calls_made())
        # A node planted later on the caller's PATH than the pinned one never runs outside srt: the probe, the canary
        # and the launch get RUN_PATH, which has no entry of the caller's; the marker stays absent.
        (loose_dir / "node").chmod(0o755)
        run = self.launch("--", "--version", PATH=f"{self.env['PATH']}:{loose_dir}")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse(marker.exists())
        for call in self.srt_calls_made():
            self.assertEqual(self.run_path, call["env"]["PATH"])
            self.assertNotIn(str(loose_dir), call["env"]["PATH"])
        self.assertEqual(f"{self.inner_path}:{loose_dir}", self.dsh_run()["env"]["PATH"], "inside, after RUN_PATH")
        self.assertEqual(str(interp / "node"), self.dsh_run()["node"])
        # The caller's entries under a write root are dropped from the inner PATH as well.
        self.dsh_record.unlink()
        run = self.launch("--", "--version", PATH=f"{self.env['PATH']}:{self.dsh_home}/bin")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.inner_path, self.dsh_run()["env"]["PATH"])
        # A planted srt interpreter that is itself a script is refused: the kernel would look its interpreter up.
        self.dsh_record.unlink()
        (interp / "node").unlink()
        self.write_marker_script(interp / "node", marker)
        run = self.launch("--", "--version")
        self.assert_refused(run, f"the interpreter {interp}/node of srt is itself a script")
        self.assertFalse(marker.exists())

    def test_a_stat_that_fails_or_prints_nothing_refuses_at_the_bootstrap_before_anything_runs(self):
        """Standing order 21: `stat` is the one bootstrap trust, read first over the launcher's own system tools. A
        copy of the launcher naming a failing or a silent fake in its place refuses there, with exit 2, before srt,
        dsh or any directory exists; a user-owned fake that answers truthfully is refused as not root's."""
        failing = self.fake_tool("failing", "#!/bin/sh\nexit 1\n")
        silent = self.fake_tool("silent", "#!/bin/sh\nexit 0\n")
        for fake in (failing, silent):
            with self.subTest(fake=fake.name):
                copy = self.launcher_with({"/usr/bin/stat": str(fake)})
                run = self.launch("--", "--version", launcher=copy)
                self.assert_refused(run, "cannot read the owner and mode of the system tools (")
                self.assert_nothing_started()
        truthful = self.fake_tool("truthful", '#!/bin/sh\nexec /usr/bin/stat "$@"\n')
        copy = self.launcher_with({"/usr/bin/stat": str(truthful)})
        run = self.launch("--", "--version", launcher=copy)
        self.assert_refused(run, f"system tool {truthful} is owned by uid {os.getuid()}, not root")
        self.assert_nothing_started()
        # The unchanged copy, pinned the same way, launches: the harness itself is not what refuses.
        copy = self.launcher_with({})
        run = self.launch("--", "--version", launcher=copy)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_an_owner_or_mode_read_that_answers_garbage_refuses_before_anything_runs(self):
        """The round-3 P2 (f10 s4): the owner reads had no failure injection, so a mutant taking a failed owner
        read for root passed. Every owner and mode read is one `stat` answer per path, `<uid> <mode>`; a lying
        `stat` that answers garbage, another owner, an open mode or one line too few for a chosen path refuses the
        launch naming the path, srt never started."""
        dsh = self.dsh_home / "bin/dsh"
        cases = (
            (dsh, "x 755", f"cannot read the mode of the dsh runtime {dsh}"),
            (dsh, "0 7x5", f"cannot read the mode of the dsh runtime {dsh}"),
            (dsh, "", f"cannot read the mode of the dsh runtime {dsh}"),
            (self.dsh_home, None, f"cannot read the owner and mode of DSH_HOME {self.dsh_home} with"),
            (self.dsh_home, f"{os.getuid()} 775", f"DSH_HOME {self.dsh_home}: mode 775, writable by group or other"),
            (self.bindir, "0 777", f"the directory of srt {self.bindir}: mode 777, writable by group or other"),
            (
                self.bindir,
                "502 755",
                f"the directory of srt {self.bindir}: owned by uid 502, neither root nor this user",
            ),
            (self.bindir / "srt", "0 1775", f"srt {self.bindir}/srt: mode 1775, writable by group or other"),
        )
        for garble_path, garble, message in cases:
            with self.subTest(path=str(garble_path), garble=garble):
                copy = self.launcher_with({"/usr/bin/stat": str(self.lying_stat(garble_path, garble))})
                run = self.launch("--", "--version", launcher=copy)
                self.assert_refused(run, message)
                self.assert_nothing_started()
        # The lie about the fakes directory alone changes nothing else: the copy launches.
        copy = self.launcher_with({"/usr/bin/stat": str(self.lying_stat())})
        run = self.launch("--", "--version", launcher=copy)
        self.assertEqual(run.returncode, 0, run.stderr)

    def test_a_readlink_that_fails_or_prints_nothing_refuses_before_anything_runs(self):
        """Standing order 21: the physical resolution of srt (`readlink -f`) is a producer whose status and output
        the launcher checks; a copy naming a failing or a silent fake refuses before srt, dsh or any directory
        exists. The lying `stat` lets the fake pass the bootstrap as a system tool."""
        failing = self.fake_tool("failing", "#!/bin/sh\nexit 1\n")
        silent = self.fake_tool("silent", "#!/bin/sh\nexit 0\n")
        cases = (
            (failing, f"cannot resolve srt at {self.bindir}/srt (readlink -f failed)"),
            (silent, f"cannot resolve srt at {self.bindir}/srt (readlink -f named no file: '')"),
        )
        for fake, message in cases:
            with self.subTest(fake=fake.name):
                copy = self.launcher_with({"/usr/bin/stat": str(self.lying_stat()), "/usr/bin/readlink": str(fake)})
                run = self.launch("--", "--version", launcher=copy)
                self.assert_refused(run, message)
                self.assert_nothing_started()


if __name__ == "__main__":
    unittest.main()
