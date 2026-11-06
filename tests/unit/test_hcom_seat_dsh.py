"""Exercise the `dsh` role of scripts/orchestrator/hcom-seat (regime-cutover U272) on the scratch host of
tests/unit/test_hcom_seat.py.

The role differs from the worker by the rows of the lever's role table and nothing else, so the tests hold the role's
settings to the worker's with the named rows substituted, and the launch to what the table says: a per-launch slot,
the listed environment names, the command resolved under `DSH_HOME`, the canary refusal, the exec argv. The shim runs
under `/usr/bin/env -i`, so the fake srt here takes its instructions from a file beside it, never from the
environment, and the fake dsh records what reached it into a file the test names. Nothing real starts.
"""

import json
import os
import re
import shlex
import stat
import subprocess
import sys
import textwrap
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_hcom_seat  # noqa: E402  # the fixture, as a module attribute so its tests are not collected twice

SYSTEM_PATH = test_hcom_seat.SYSTEM_PATH
FAKE_OAUTH_VALUE = test_hcom_seat.FAKE_OAUTH_VALUE
# Built at runtime like FAKE_OAUTH_VALUE, and named without the word the secret scan's `generic-token` rule keys on.
CALLER_OAUTH_VALUE = "caller-" + "value-u272"
# bash itself exports these into every child; the role's list is everything else.
BASH_OWN_NAMES = {"PWD", "SHLVL", "OLDPWD", "_"}


def interpreter_own_names():
    """The names the host's python3 (the fakes' interpreter) adds to an empty environment on its own: Apple's
    /usr/bin/python3 trampoline exports SDKROOT, CPATH, LIBRARY_PATH and MANPATH; a plain interpreter adds none."""
    probe = subprocess.run(
        ["/usr/bin/env", "-i", f"PATH={SYSTEM_PATH}", "python3", "-c", "import json, os; print(json.dumps(sorted(os.environ)))"],
        capture_output=True, text=True, check=True,
    )  # fmt: skip
    return set(json.loads(probe.stdout)) - {"PATH"}


FAKE_SRT = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, subprocess, sys
    conf = json.load(open(os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "srt.json")))
    argv = sys.argv[1:]
    with open(os.path.join(conf["calls"], "srt"), "a") as calls:
        calls.write(json.dumps({"argv": argv, "env": sorted(os.environ), "cwd": os.getcwd()}) + "\\n")
    if argv == ["--version"]:
        print("0.0.81")
        sys.exit(0)
    command = argv[argv.index("--") + 1 :]
    if command[:2] == ["/bin/sh", "-c"]:
        answer = os.path.join(conf["calls"], "canary-answer")
        if os.path.exists(answer):
            print(open(answer).read().strip())
            sys.exit(0)
        denied = ["/nonexistent-u272/canary", "/nonexistent-u272/settings", "/nonexistent-u272/.ssh",
                  "/nonexistent-u272/.claude/debug/canary"]
        sys.exit(subprocess.run(["/bin/sh", "-c", command[2], command[3], *denied], check=False).returncode)
    os.execvp(command[0], command)
    """
)
FAKE_DSH = textwrap.dedent(
    """\
    #!/usr/bin/env python3
    import json, os, sys, time
    calls = {calls!r}
    with open(os.path.join(calls, "dsh"), "a") as record:
        record.write(json.dumps({{"argv": sys.argv[1:], "argv0": sys.argv[0], "cwd": os.getcwd(),
                                 "env": dict(os.environ)}}) + "\\n")
    if "--version" in sys.argv[1:]:
        print("0.2.1-rc.5")
    deadline = time.monotonic() + 30
    while os.path.exists(os.path.join(calls, "hold")) and not os.path.exists(os.path.join(calls, "release")):
        if time.monotonic() > deadline:
            sys.exit("fake dsh: never released")
        time.sleep(0.05)
    status = os.path.join(calls, "dsh-status")
    sys.exit(int(open(status).read()) if os.path.exists(status) else 0)
    """
)


class HcomSeatDshTest(test_hcom_seat.SeatFixture):
    def setUp(self):
        super().setUp()
        (self.bindir / "srt").write_text(FAKE_SRT)
        (self.bindir / "srt.json").write_text(json.dumps({"calls": str(self.calls)}))
        self.dsh_home = Path(self.temp.name).resolve() / "dsh-home"
        (self.dsh_home / "bin").mkdir(parents=True)
        self.dsh = self.dsh_home / "bin/dsh"
        self.dsh.write_text(FAKE_DSH.format(calls=str(self.calls)))
        self.dsh.chmod(0o755)

    def dsh_calls(self):
        return self.calls_of("dsh")

    def launch(self, *args, **overrides):
        return self.seat("dsh", "--seats-root", self.seats, "--home", str(self.dsh_home), *args, **overrides)

    def held_launch(self, *args, count=1, **overrides):
        """Start `count` launches whose dsh waits for `release`, and return them once every dsh has recorded itself,
        so the per-launch slots can be read while they exist."""
        (self.calls / "hold").touch()
        env = {**self.env, **overrides}
        argv = [str(test_hcom_seat.SEAT), "dsh", "--seats-root", self.seats, "--home", str(self.dsh_home), *args]
        procs = [
            subprocess.Popen(argv, cwd=self.repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for _ in range(count)
        ]
        deadline = time.monotonic() + 60
        while len(self.dsh_calls()) < count:
            if time.monotonic() > deadline or any(proc.poll() is not None for proc in procs):
                outputs = [proc.communicate() for proc in procs]
                self.fail(f"a launch ended before its dsh recorded itself: {outputs}")
            time.sleep(0.05)
        return procs

    def release(self, procs):
        (self.calls / "release").touch()
        results = [proc.communicate() for proc in procs]
        (self.calls / "hold").unlink()
        (self.calls / "release").unlink()
        return [(proc.returncode, out, err) for proc, (out, err) in zip(procs, results)]

    def slots(self):
        """The per-launch sandbox and state slots that exist now, as (sandbox names, state names)."""
        sandbox = Path(self.seats, ".sandbox")
        state = Path(self.seats, ".state")
        return (
            sorted(p.name for p in sandbox.iterdir()) if sandbox.exists() else [],
            sorted(p.name for p in state.iterdir()) if state.exists() else [],
        )

    def test_the_dsh_settings_are_the_workers_but_the_named_rows(self):
        """The role table's rows are the only difference: the cwd and state slot for the worktree, DSH_HOME and the
        role's own omp profile for the git common directory, the hcom store and the worker profile; the read denies,
        the network and everything else are the worker's."""
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")
        procs = self.held_launch("--", "--version")
        sandboxes, states = self.slots()
        (name,) = [entry for entry in sandboxes if entry != "worker"]
        self.assertEqual(sorted(states), sorted(["worker", name]))
        self.assertRegex(name, r"^dsh-\d{8}-\d{6}-\d+$")
        dsh = self.settings_of(name)
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        home = self.home.resolve()
        clone, cwd = str(Path(self.seats, "worker")), str(Path(self.seats, ".state", name, "cwd"))
        state_w, state_d = str(Path(self.seats, ".state/worker")), str(Path(self.seats, ".state", name))
        common, store = str((self.repo / ".git").resolve()), str(self.store.resolve())
        # allowWrite: the worker's first five rows are the clone, its state, the common directory, the store and its
        # profile; the dsh role's are the cwd, its state, DSH_HOME and its profile; the rest is the same list.
        write_w, write_d = worker["filesystem"]["allowWrite"], dsh["filesystem"]["allowWrite"]
        self.assertEqual(write_w[:5], [clone, state_w, common, store, str(home / ".omp/profiles/worker")])
        self.assertEqual(write_d[:4], [cwd, state_d, str(self.dsh_home), str(home / ".omp/profiles/dsh")])
        self.assertEqual(write_d[4:], write_w[5:])
        self.assertIn(str(home / ".omp/run"), write_d)
        self.assertNotIn(common, write_d)
        self.assertNotIn(store, write_d)
        # allowRead: the same substitution, the checkout's records included for both.
        read_w, read_d = worker["filesystem"]["allowRead"], dsh["filesystem"]["allowRead"]
        substitute = {clone: cwd, str(home / ".omp/profiles/worker"): str(home / ".omp/profiles/dsh"), state_w: state_d}
        self.assertEqual(read_d, [substitute.get(entry, entry) for entry in read_w])
        # denyWrite: the project files under the seat directory move with it; the worker's `.git` file has no dsh
        # counterpart (no worktree); every other deny is the same.
        deny_w = [entry for entry in worker["filesystem"]["denyWrite"] if not entry.startswith(clone + "/")]
        deny_d = [entry for entry in dsh["filesystem"]["denyWrite"] if not entry.startswith(cwd + "/")]
        self.assertEqual(deny_d, deny_w)
        self.assertEqual(
            [entry[len(cwd) :] for entry in dsh["filesystem"]["denyWrite"] if entry.startswith(cwd + "/")],
            [entry[len(clone) :] for entry in worker["filesystem"]["denyWrite"] if entry.startswith(clone + "/") and entry != clone + "/.git"],
        )  # fmt: skip
        self.assertEqual(dsh["filesystem"]["denyRead"], worker["filesystem"]["denyRead"])
        self.assertEqual(dsh["network"], worker["network"])
        self.assertEqual({k: v for k, v in dsh.items() if k not in ("filesystem", "network")},
                         {k: v for k, v in worker.items() if k not in ("filesystem", "network")})  # fmt: skip
        # The slots are per launch: both are gone once dsh exited; the worker's stay.
        self.assertEqual(self.slots(), (["worker"], ["worker"]))

    def test_two_launches_at_once_share_no_settings_file_and_each_slot_goes_with_its_dsh(self):
        """U251d P1 `:704`: every launch has its own sandbox, settings file, state slot and CLAUDE_CONFIG_DIR."""
        procs = self.held_launch("--", "--version", count=2)
        sandboxes, states = self.slots()
        self.assertEqual(len(sandboxes), 2, sandboxes)
        self.assertEqual(sandboxes, states)
        for name in sandboxes:
            self.assertTrue(Path(self.seats, ".sandbox", name, "srt-settings.json").is_file(), name)
            self.assertTrue(Path(self.seats, ".sandbox", name, "bin/dsh").is_file(), name)
            self.assertTrue(Path(self.seats, ".state", name, "cwd").is_dir(), name)
            self.assertTrue(Path(self.seats, ".state", name, "claude").is_dir(), name)
            self.assertEqual(stat.S_IMODE(os.lstat(Path(self.seats, ".state", name)).st_mode), 0o700)
        records = self.dsh_calls()
        self.assertEqual(sorted(Path(record["env"]["HCOM_SEAT_SANDBOX"]).name for record in records), sandboxes)
        self.assertEqual(len({record["env"]["CLAUDE_CONFIG_DIR"] for record in records}), 2)
        self.assertEqual(len({record["cwd"] for record in records}), 2)
        launches = [call for call in self.calls_of("srt") if call["argv"][2:4] == ["--", "/usr/bin/env"]]
        self.assertEqual(len({launch["argv"][1] for launch in launches}), 2, "two settings files")
        for status, out, err in self.release(procs):
            self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertEqual(self.slots(), ([], []))
        # dsh's own status comes back, and a failing dsh leaves no slot either.
        (self.calls / "dsh-status").write_text("7")
        run = self.launch("--", "--version")
        self.assertEqual(run.returncode, 7, run.stderr)
        self.assertEqual(self.slots(), ([], []))

    def test_the_environment_reaching_dsh_is_the_listed_names_and_the_shims_exports(self):
        """U251d P1 `:146` and U251b P2 `:325`: nothing of the caller's environment reaches the shim, srt or dsh but
        the listed names; the shim's own exports (the bridge child's CLAUDE_CONFIG_DIR, the token, the AWS file
        names, the signing rows) ride as for every role; the caller's token wins over the token file."""
        caller = {
            "SECRET_OF_THE_CALLER": "never", "NODE_OPTIONS": "--require /tmp/evil.js", "USER": "u272",
            "LANG": "C.UTF-8", "TERM": "xterm", "HCOM_TEAM": "repo",
        }  # fmt: skip
        run = self.launch("--profile", "thak", "--", "--version", **caller)
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        (dsh,) = self.dsh_calls()
        env = dsh["env"]
        expected = {
            "HOME", "PATH", "DSH_HOME", "OMP_PROFILE", "USER", "LANG", "TERM", "UV_CACHE_DIR", "CLAUDE_CONFIG_DIR",
            "CLAUDE_CODE_OAUTH_TOKEN", "AWS_SHARED_CREDENTIALS_FILE", "AWS_CONFIG_FILE", "GIT_CONFIG_COUNT",
            "GIT_CONFIG_KEY_0", "GIT_CONFIG_VALUE_0", "GIT_CONFIG_KEY_1", "GIT_CONFIG_VALUE_1", "HCOM_SEAT_SANDBOX",
        }  # fmt: skip
        self.assertEqual(set(env) - BASH_OWN_NAMES - interpreter_own_names(), expected)
        self.assertEqual(
            {env["USER"], env["LANG"], env["TERM"], env["OMP_PROFILE"], env["DSH_HOME"]},
            {"u272", "C.UTF-8", "xterm", "dsh", str(self.dsh_home)},
        )
        self.assertEqual(env["CLAUDE_CODE_OAUTH_TOKEN"], FAKE_OAUTH_VALUE, "the token file, exported by the shim")
        self.assertTrue(env["PATH"].startswith(f"{self.tools}:/usr/bin:/bin:/usr/sbin:/sbin:"), env["PATH"])
        self.assertRegex(env["CLAUDE_CONFIG_DIR"], rf"^{re.escape(self.seats)}/\.state/dsh-\d{{8}}-\d{{6}}-\d+/claude$")
        self.assertEqual(Path(dsh["cwd"]).resolve(), Path(env["CLAUDE_CONFIG_DIR"]).parent / "cwd")
        self.assertEqual((env["AWS_SHARED_CREDENTIALS_FILE"], env["AWS_CONFIG_FILE"]), ("/dev/null", "/dev/null"))
        self.assertEqual(dsh["argv"], ["--profile", "thak", "--version"])
        # The canary and the launch srt saw the same reduced names (the version probe runs under the lever's own).
        version, canary, launch = self.calls_of("srt")
        self.assertEqual(version["argv"], ["--version"])
        for call in (canary, launch):
            self.assertNotIn("SECRET_OF_THE_CALLER", call["env"])
            self.assertNotIn("NODE_OPTIONS", call["env"])
            self.assertNotIn("HCOM_TEAM", call["env"])
        self.assertNotIn(FAKE_OAUTH_VALUE, run.stdout + run.stderr)
        # A caller's token wins over the token file; no name is passed empty.
        run = self.launch("--", "--version", CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE, USER=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        env = self.dsh_calls()[-1]["env"]
        self.assertEqual(env["CLAUDE_CODE_OAUTH_TOKEN"], CALLER_OAUTH_VALUE)
        self.assertNotIn("USER", env)
        self.assertNotIn(CALLER_OAUTH_VALUE, run.stdout + run.stderr)

    def test_the_command_and_its_home_are_resolved_and_refused_like_a_tool(self):
        """`<DSH_HOME>/bin/dsh` must be an executable regular file under a clean, existing DSH_HOME; the dsh options
        belong to the dsh role alone; a DSH_HOME inside a protected path is refused by the overlap invariant; a tool
        planted under DSH_HOME never runs. Every refusal is exit 2 with nothing created or started."""
        spaced = Path(self.temp.name).resolve() / "dsh home"
        spaced.mkdir()
        planted_home = Path(self.temp.name).resolve() / "planted-home"
        (planted_home / "bin").mkdir(parents=True)
        (planted_home / "bin/dsh").write_text(FAKE_DSH.format(calls=str(self.calls)))
        (planted_home / "bin/dsh").chmod(0o755)
        marker = Path(self.temp.name) / "planted-ran"
        for tool in ("node", "python3"):
            (planted_home / "bin" / tool).write_text(f"#!/bin/sh\n: > {shlex.quote(str(marker))}\nexit 0\n")
            (planted_home / "bin" / tool).chmod(0o755)
        no_command = Path(self.temp.name).resolve() / "no-command"
        (no_command / "bin").mkdir(parents=True)
        not_executable = Path(self.temp.name).resolve() / "not-executable"
        (not_executable / "bin").mkdir(parents=True)
        (not_executable / "bin/dsh").write_text("#!/bin/sh\nexit 0\n")
        inside = self.repo / "dsh-home"
        (inside / "bin").mkdir(parents=True)
        (inside / "bin/dsh").write_text("#!/bin/sh\nexit 0\n")
        (inside / "bin/dsh").chmod(0o755)
        cases = [
            (["dsh", "--home", str(self.temp.name) + "/absent", "--", "--version"], {}, "DSH_HOME is not a directory"),
            (["dsh", "--home", str(spaced), "--", "--version"], {}, "is not a clean absolute path"),
            (["dsh", "--home", str(no_command), "--", "--version"], {}, "cannot resolve the dsh command to a physical executable file"),
            (["dsh", "--home", str(not_executable), "--", "--version"], {}, "cannot resolve the dsh command to a physical executable file"),
            (["dsh", "--home", str(self.dsh_home), "--profile", "bad name", "--", "--version"], {}, "profile 'bad name' is outside"),
            (["dsh", "--home", str(self.dsh_home), "--ext", str(self.bridge)], {}, "--ext is an option of the omp roles"),
            (["worker", "--profile", "thak"], {}, "--profile, --home and -- are options of the dsh role"),
            (["worker", "--", "--version"], {}, "--profile, --home and -- are options of the dsh role"),
            (["dsh", "--home", str(inside), "--", "--version"], {}, "lies inside the main checkout"),
            (["dsh", "--home", str(planted_home), "--", "--version"], {"PATH": f"{planted_home}/bin:{self.env['PATH']}"}, "lies under the seat write root"),
            (["dsh", "--", "--version"], {"DSH_HOME": str(self.temp.name) + "/absent"}, "DSH_HOME is not a directory"),
        ]  # fmt: skip
        for argv, env, message in cases:
            with self.subTest(argv=argv[1:]):
                run = self.seat(*argv, "--seats-root", self.seats, **env)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])
        self.assertFalse(marker.exists(), "a planted node or python3 under DSH_HOME never ran")
        # The planted home launches once its bin is off the caller's PATH: the tools come from elsewhere, and the
        # planted files, under DSH_HOME, are never resolved or run.
        run = self.seat("dsh", "--home", str(planted_home), "--seats-root", self.seats, "--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertFalse(marker.exists())
        # The environment's DSH_HOME is the default; --home wins over it.
        run = self.seat("dsh", "--seats-root", self.seats, "--", "--version", DSH_HOME=str(self.dsh_home))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(self.dsh_calls()[-1]["env"]["DSH_HOME"], str(self.dsh_home))

    def test_a_canary_that_finds_the_sandbox_open_starts_no_dsh(self):
        """The dsh shim refuses as the omp shim does when the canary answers anything but the four words, and the
        per-launch slots go with the refusal."""
        for answer in (
            "write-open read-denied ssh-denied debug-denied",
            "write-denied read-denied ssh-denied",
            "write-denied read-denied ssh-denied debug-open",
        ):
            with self.subTest(answer=answer):
                (self.calls / "canary-answer").write_text(answer + "\n")
                run = self.launch("--", "--version")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn("the sandbox does not hold", run.stderr)
                self.assertIn("dsh not started", run.stderr)
                self.assertEqual(self.dsh_calls(), [])
                self.assertEqual(self.slots(), ([], []))
        (self.calls / "canary-answer").unlink()
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)

    def test_srt_receives_the_canary_and_the_exec_argv_and_a_dry_run_creates_nothing(self):
        """The exec argv: `--settings <per-launch file> -- /usr/bin/env PATH=<seat path> <physical dsh> [--profile
        <name>] <args>`; the canary runs under the same file first; the dry run prints the foreground launch line
        with the environment names and no token, and makes no slot."""
        run = self.launch("--profile", "thak", "--", "--version", "--flag", USER="u272")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        version, canary, launch = self.calls_of("srt")
        self.assertEqual(version["argv"], ["--version"])
        settings = canary["argv"][1]
        self.assertRegex(settings, rf"^{re.escape(self.seats)}/\.sandbox/dsh-\d{{8}}-\d{{6}}-\d+/srt-settings\.json$")
        self.assertEqual(canary["argv"][:5], ["--settings", settings, "--", "/bin/sh", "-c"])
        self.assertEqual(launch["argv"][:4], ["--settings", settings, "--", "/usr/bin/env"])
        self.assertEqual(
            launch["argv"][4], f"PATH={self.tools}:/usr/bin:/bin:/usr/sbin:/sbin:{self.bindir}:{SYSTEM_PATH}"
        )
        self.assertEqual(launch["argv"][5:], [str(self.dsh.resolve()), "--profile", "thak", "--version", "--flag"])
        (dsh,) = self.dsh_calls()
        self.assertEqual(dsh["argv0"], str(self.dsh.resolve()))
        before = len(self.calls_of("srt"))
        run = self.launch("--dry-run", "--", "--version", USER="u272", CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE)
        self.assertEqual(run.returncode, 0, run.stderr)
        line = shlex.split(run.stdout)
        self.assertEqual(line[:2], ["/usr/bin/env", "-i"])
        self.assertEqual(
            line[2:7],
            [f"HOME={self.home}", f"PATH={self.tools}:/usr/bin:/bin:/usr/sbin:/sbin", f"DSH_HOME={self.dsh_home}",
             "OMP_PROFILE=dsh", "USER=u272"],
        )  # fmt: skip
        self.assertRegex(line[7], rf"^{re.escape(self.seats)}/\.sandbox/dsh-\d{{8}}-\d{{6}}-\d+/bin/dsh$")
        self.assertEqual(line[8:], ["--version"])
        self.assertNotIn(CALLER_OAUTH_VALUE, run.stdout + run.stderr)
        self.assertEqual(len(self.calls_of("srt")), before + 1, "the dry run reads the srt version and starts nothing")
        self.assertEqual(len(self.dsh_calls()), 1)
        self.assertEqual(self.slots(), ([], []), "the dry run makes no per-launch slot")


if __name__ == "__main__":
    unittest.main()
