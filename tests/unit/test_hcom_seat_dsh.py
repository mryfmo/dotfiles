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
import signal
import shutil
import stat
import subprocess
import sys
import tarfile
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
# The heads before each round's row: the omp roles' settings are held byte-identical to every one of them.
EARLIER_HEADS = (
    "52873a37745d8141eada2139ea2fa76e2773a60d",  # round one, before the read grants became a role row (U272c)
    "976fd6cdb249c76ac397ede1bbfccd931ad824c1",  # round two, before the deny row and the DSH_HOME refusal (U272d)
    "5b950a97028205f7430a7c9f36f74b91a79e88c8",  # round three, before the refusal read the rendered deny table (U272e)
    "d1ffd91939e4d069b01d0e4d467c12eff971a944",  # round four, before the judge read every rendered grant (U272f)
    "d191911256d88f4a71ebde559500353dbc4d1e19",  # round five, before the exemptions named one row by position (U272g)
)


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
    if os.path.exists(os.path.join(calls, "leave-locked")):
        os.makedirs("locked/inner")
        open("locked/inner/file", "w").close()
        os.chmod("locked/inner", 0)
        os.chmod("locked", 0)
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

    def held_launch(self, *args, count=1, new_session=False, **overrides):
        """Start `count` launches whose dsh waits for `release`, and return them once every dsh has recorded itself,
        so the per-launch slots can be read while they exist; `new_session` makes each launcher its own process
        group, the target of a signal to the group."""
        (self.calls / "hold").touch()
        env = {**self.env, **overrides}
        argv = [str(test_hcom_seat.SEAT), "dsh", "--seats-root", self.seats, "--home", str(self.dsh_home), *args]
        before = len(self.dsh_calls())
        procs = [
            subprocess.Popen(
                argv,
                cwd=self.repo,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=new_session,
            )  # fmt: skip
            for _ in range(count)
        ]
        deadline = time.monotonic() + 60
        while len(self.dsh_calls()) < before + count:
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
        role's own omp profile for the git common directory, the hcom store and the worker profile, the role's own
        read grants; the read denies, the network and everything else are the worker's."""
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
        # allowRead (U272c): the role's own grants, in the row's order; none of the worker's rows but the substituted
        # cwd, state slot and profile (the git directory, the store and the checkout's records are the worker's alone).
        read_w, read_d = worker["filesystem"]["allowRead"], dsh["filesystem"]["allowRead"]
        self.assertEqual(read_w[:3], [clone, common, store])
        self.assertEqual(
            read_d,
            [cwd, state_d, str(self.dsh_home), str(home / ".omp/profiles/dsh"), str(home / ".agents/skills"),
             str(self.tools)],
        )  # fmt: skip
        # denyWrite: the project files under the seat directory move with it; the worker's `.git` file has no dsh
        # counterpart (no worktree); the deny row (U272d: the git common directory, the worker clone's `.git` entry,
        # it being a linked worktree, the hcom store, the records and the other seat's directory) follows the
        # worker's denies; the macOS worktree patterns and every other deny are the same.
        row = [common, clone + "/.git", store, str(self.repo.resolve() / ".orchestration"), clone]
        deny_w = [entry for entry in worker["filesystem"]["denyWrite"] if not entry.startswith(clone + "/")]
        deny_d = [entry for entry in dsh["filesystem"]["denyWrite"] if not entry.startswith(cwd + "/")]
        self.assertEqual([e for e in deny_d if "*" not in e], [e for e in deny_w if "*" not in e] + row)
        self.assertEqual([e for e in deny_d if "*" in e], [e for e in deny_w if "*" in e])
        self.assertEqual(
            [entry[len(cwd) :] for entry in dsh["filesystem"]["denyWrite"] if entry.startswith(cwd + "/")],
            [entry[len(clone) :] for entry in worker["filesystem"]["denyWrite"] if entry.startswith(clone + "/") and entry != clone + "/.git"],
        )  # fmt: skip
        self.assertEqual(dsh["filesystem"]["denyRead"], worker["filesystem"]["denyRead"] + row)
        self.assertEqual(dsh["network"], worker["network"])
        self.assertEqual({k: v for k, v in dsh.items() if k not in ("filesystem", "network")},
                         {k: v for k, v in worker.items() if k not in ("filesystem", "network")})  # fmt: skip
        # The slots are per launch: both are gone once dsh exited; the worker's stay.
        self.assertEqual(self.slots(), (["worker"], ["worker"]))

    def test_the_dsh_read_grants_name_no_git_hcom_or_record_path(self):
        """PR 697 thread 4492139503 (U272c): an allowRead entry re-opens a path under the broad denyRead, so the dsh
        role's list names neither the checkout's git common directory, nor the hcom store, nor the coordinator's
        records under the checkout, by itself or by an ancestor; the checkout stays read-denied. The worker's list
        does name them, so the fixture's paths are the ones the role would have inherited."""
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        dsh = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")["filesystem"]
        checkout = self.repo.resolve()
        common, store, records = checkout / ".git", self.store.resolve(), checkout / ".orchestration/orchestrate"
        for path in (common, store, records):
            with self.subTest(path=str(path)):
                self.assertIn(str(path), worker["allowRead"], "the worker's grant, the one the role used to inherit")
                self.assertFalse(
                    [entry for entry in dsh["allowRead"] if Path(entry) in (path, *path.parents)],
                    f"the dsh role re-opens {path} or an ancestor: {dsh['allowRead']}",
                )
        # The checkout is read-denied and no grant re-opens it or lies under it (the records row was the one that did).
        self.assertIn(str(checkout), dsh["denyRead"])
        for entry in dsh["allowRead"]:
            self.assertNotIn(str(checkout), (entry, *(str(p) for p in Path(entry).parents)), entry)
        self.assertEqual(self.slots(), (["worker"], ["worker"]))

    def test_the_omp_roles_settings_are_byte_identical_to_the_earlier_heads(self):
        """No round's row changes an omp role's settings: the worker's and the orchestrator's `srt-settings.json`
        rendered by this head equal, byte for byte, the ones each earlier head (EARLIER_HEADS) renders on the same
        scratch host. An earlier lever runs from its own tree (git archive of its `scripts/orchestrator` and manifest,
        so its self-check reads its own pin); a checkout without that commit skips it."""
        for head in EARLIER_HEADS:
            probe = subprocess.run(
                ["git", "-C", str(test_hcom_seat.ROOT), "cat-file", "-e", f"{head}^{{commit}}"],
                env=self.env, capture_output=True, text=True, check=False,
            )  # fmt: skip
            if probe.returncode != 0:
                self.skipTest(f"the earlier head {head} is not in this checkout (a shallow or squashed clone)")
            old_root = Path(self.temp.name).resolve() / f"head-{head[:8]}"
            old_root.mkdir()
            archive = old_root / "tree.tar"
            subprocess.run(
                ["git", "-C", str(test_hcom_seat.ROOT), "archive", "--format=tar", "-o", str(archive), head,
                 "scripts/orchestrator", "home/dot_agents/agent-config.yaml"],
                env=self.env, capture_output=True, text=True, check=True,
            )  # fmt: skip
            with tarfile.open(archive) as tar:
                tar.extractall(old_root, **({"filter": "data"} if hasattr(tarfile, "data_filter") else {}))
            old_seat = old_root / "scripts/orchestrator/hcom-seat"
            self.assertTrue(os.access(old_seat, os.X_OK), old_seat)
            for role in ("worker", "orchestrator"):
                rendered = {}
                for label, seat in (("earlier head", old_seat), ("this head", test_hcom_seat.SEAT)):
                    run = subprocess.run(
                        [str(seat), role, "--seats-root", self.seats], cwd=self.repo, env=self.env,
                        capture_output=True, text=True, check=False,
                    )  # fmt: skip
                    self.assertEqual(run.returncode, 0, f"{label} {head[:8]} {role}: {run.stderr}")
                    rendered[label] = Path(self.seats, ".sandbox", role, "srt-settings.json").read_bytes()
                with self.subTest(head=head[:8], role=role):
                    self.assertEqual(rendered["earlier head"], rendered["this head"])
                    self.assertIn(b'"allowRead":[', rendered["this head"])

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
        names, the signing rows) ride as for every role; U312: a caller's token is no input, the token file's is."""
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
        # U312: a caller's token is no input; the token file's value rides as for every role, and no name is passed
        # empty. Without the file (the dsh role runs no login preflight) the child gets no token at all.
        run = self.launch("--", "--version", CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE, USER=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        env = self.dsh_calls()[-1]["env"]
        self.assertEqual(env["CLAUDE_CODE_OAUTH_TOKEN"], FAKE_OAUTH_VALUE)
        self.assertNotIn(CALLER_OAUTH_VALUE, env.values())
        self.assertNotIn("USER", env)
        self.assertNotIn(CALLER_OAUTH_VALUE, run.stdout + run.stderr)
        self.token.unlink()
        run = self.launch("--", "--version", CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE)
        self.assertEqual(run.returncode, 0, run.stderr)
        env = self.dsh_calls()[-1]["env"]
        self.assertNotIn("CLAUDE_CODE_OAUTH_TOKEN", env)
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

    def test_the_dsh_settings_deny_every_git_hcom_and_record_path_for_read_and_write(self):
        """U272c P1 `hcom-seat:1876`: srt reads everything an explicit deny does not name, so removing a grant denied
        nothing. The dsh settings carry a denyRead and a denyWrite row for each path of the role's deny row, by its
        physical path: the checkout's git common directory, the `.git` entry of a linked worktree, the hcom store
        (here outside `~/.local/state/hcom`, as the program's `hcom-regime` is), every `~/.local/state/hcom-*`
        sibling store but the lever's own `hcom-seat` (a file of the name shape is skipped), the records directory and
        another seat's directory. The worker's settings deny none of them: its grants re-open the store and the
        common directory."""
        linked = Path(self.temp.name).resolve() / "linked"
        self.git("worktree", "add", "-q", "--detach", str(linked), "HEAD")
        state = self.home / ".local/state"
        sibling = state / "hcom-regime"
        sibling.mkdir(parents=True)
        (state / "hcom-note").write_text("")
        run = self.seat("worker", "--seats-root", self.seats)
        self.assertEqual(run.returncode, 0, run.stderr)
        worker = self.settings_of("worker")["filesystem"]
        procs = self.held_launch("--", "--version")
        (name,) = [entry for entry in self.slots()[0] if entry != "worker"]
        dsh = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        checkout = self.repo.resolve()
        row = [str(checkout / ".git"), str(linked / ".git"), str(Path(self.seats, "worker/.git")), str(self.store.resolve()),
               str(sibling.resolve()), str(checkout / ".orchestration"), str(Path(self.seats, "worker"))]  # fmt: skip
        for path in row:
            with self.subTest(path=path):
                self.assertIn(path, dsh["denyRead"])
                self.assertIn(path, dsh["denyWrite"])
        self.assertEqual(dsh["denyRead"][-len(row) :], row, "the row in the lever's order, after the worker's denies")
        for path in (str(self.tools.parent), str(state / "hcom-note")):
            self.assertNotIn(path, dsh["denyRead"], path)
        self.assertIn(str(self.tools), dsh["allowRead"], "the lever's own state directory is no store")
        for path in (str(checkout / ".git"), str(self.store.resolve())):
            self.assertNotIn(path, worker["denyRead"], "the worker's grants stay")
            self.assertIn(path, worker["allowRead"])
        self.assertEqual(self.slots(), (["worker"], ["worker"]))
        # The program's own spelling, `HCOM_DIR=~/.local/state/hcom-regime` (the verdict's case): the store is denied
        # once, as the store, not again as a sibling.
        procs = self.held_launch("--", "--version", HCOM_DIR=str(sibling))
        (name,) = [entry for entry in self.slots()[0] if entry != "worker"]
        dsh = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertEqual(dsh["denyRead"].count(str(sibling.resolve())), 1, dsh["denyRead"])
        self.assertEqual(dsh["denyWrite"].count(str(sibling.resolve())), 1, dsh["denyWrite"])
        self.assertNotIn(str(sibling.resolve()), dsh["allowRead"])

    def test_a_dsh_home_that_is_or_holds_a_denied_path_refuses_before_any_mkdir(self):
        """U272c P1 `hcom-seat:1453`: a DSH_HOME whose physical path is, lies inside or contains a path of the deny table
        refuses by name, in a dry run too, before any directory is made: the checkout's `.git` (the overlap check's
        own-`.git` exemption admits it as a write root, so dsh could alter objects and refs; the judge names it by the
        first deny row it lies inside, the checkout), a directory inside it (the overlap invariant's own refusal,
        which runs first) and a directory holding the hcom store. bash's DEBUG trap records every command the launch
        ran; the only mkdir is the private tool directory's."""
        checkout = self.repo.resolve()
        common = checkout / ".git"
        holder = self.store.parent.resolve()
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("the checkout's .git", common, [],
             f"allowRead row {common} is, contains or lies inside {checkout}, a row of its denyRead list", "settings_judge"),
            ("inside the checkout's .git", common / "objects", [],
             f"write root {common / 'objects'} lies inside the main checkout {checkout}", "seat_overlap_check"),
            ("a directory holding the hcom store", holder, [],
             f"allowRead row {holder} is, contains or lies inside {self.store.resolve()}, a row of its denyRead list",
             "settings_judge"),
            ("the checkout's .git, dry run", common, ["--dry-run"],
             f"is, contains or lies inside {checkout}, a row of its denyRead list", "settings_judge"),
        )  # fmt: skip
        for label, home, args, message, check in cases:
            with self.subTest(case=label):
                trace.write_text("")
                run = self.seat("dsh", "--seats-root", self.seats, "--home", str(home), *args, "--", "--version",
                                BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn(check, " ".join(commands), "the refusal is the named check's, recorded")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertFalse((self.home / ".omp").exists())
        self.assertEqual(self.dsh_calls(), [])

    def test_a_hangup_to_a_held_launch_removes_both_slots(self):
        """U272c P2 `hcom-seat:2123`: a SIGHUP (a terminal hangup) or a SIGTERM to the launch's process group ends dsh,
        the shim and the launcher, whose trap removes both per-launch slots and then ends by the same signal, so the
        exit status names it."""
        for sig in (signal.SIGHUP, signal.SIGTERM):
            with self.subTest(signal=sig.name):
                (proc,) = self.held_launch("--", "--version", new_session=True)
                (name,) = self.slots()[0]
                self.assertEqual(self.slots(), ([name], [name]))
                os.killpg(proc.pid, sig)
                out, err = proc.communicate(timeout=60)
                (self.calls / "hold").unlink()
                self.assertEqual((proc.returncode, out), (-sig, ""), err)
                self.assertEqual(self.slots(), ([], []), err)

    def test_a_failing_or_malformed_date_refuses_the_launch_name(self):
        """U272c P2 `hcom-seat:256`: the clock producer that names the per-launch slot fails closed. A `/bin/date` that
        fails after plausible output, prints nothing, prints another shape, a stamp and more, or a stamp with a
        suffix refuses (exit 2) and names no stamp; the real clock prints the shape. The producer runs from the
        lever's own text with the clock's path replaced, as the identity check's stat is."""
        text = test_hcom_seat.SEAT.read_text()
        functions = "\n".join(
            text[text.index(f"{name}() {{") : text.index("\n}\n", text.index(f"{name}() {{")) + 3]
            for name in ("refuse", "utc_stamp")
        )
        self.assertIn("/bin/date", functions)
        clocks = Path(self.temp.name) / "clocks"
        clocks.mkdir()
        cases = {
            "fails after plausible output": "echo 20261106-120000\nexit 1",
            "prints nothing": "exit 0",
            "another shape": "echo 2026-11-06T12:00:00Z",
            "a stamp and more": "echo 20261106-120000\necho 20261106-120001",
            "a stamp with a suffix": "echo 20261106-120000x",
        }
        for n, (label, body) in enumerate(cases.items()):
            with self.subTest(clock=label):
                clock = clocks / f"date-{n}"
                clock.write_text(f"#!/bin/sh\n{body}\n")
                clock.chmod(0o755)
                script = f"set -euo pipefail\n{functions.replace('/bin/date', str(clock))}\n"
                script += 'stamp=$(utc_stamp) || exit 2\necho "named=${stamp}"\n'
                run = subprocess.run(["/bin/bash", "-c", script], capture_output=True, text=True, check=False)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stdout + run.stderr)
                self.assertIn("cannot read the time", run.stderr)
        real = subprocess.run(
            ["/bin/bash", "-c", f"set -euo pipefail\n{functions}\nutc_stamp\n"], capture_output=True, text=True, check=False
        )  # fmt: skip
        self.assertEqual(real.returncode, 0, real.stderr)
        self.assertRegex(real.stdout, r"^\d{8}-\d{6}\n$")

    def test_a_dsh_home_under_an_inherited_deny_refuses_from_the_rendered_table_before_any_mkdir(self):
        """U272d P1 `hcom-seat:1660`: the refusal reads the deny table the role will run under (the worker's inherited
        denies among its rows), not the role's own deny row. A DSH_HOME at the scratch HOME's `.aws` or `.omp/agent`,
        inside `.aws`, or at a directory that holds what a linked deny path (`~/.kube -> <elsewhere>/aws`) physically
        names refuses (exit 2) naming the deny path, in a dry run too, before any directory is made (the DEBUG-trap
        recorder shows the tool directory's mkdir alone); each path named is a row of the settings a launch that goes
        through renders. Round 5 (U272f): the judge names the grant as the role's `allowRead` row."""
        home = self.home.resolve()
        for rel in (".aws/deeper", ".omp/agent"):
            (home / rel).mkdir(parents=True)
        elsewhere = Path(self.temp.name).resolve() / "elsewhere"
        (elsewhere / "aws").mkdir(parents=True)
        (home / ".kube").symlink_to(elsewhere / "aws")
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("~/.aws", home / ".aws", [], f"allowRead row {home / '.aws'} is, contains or lies inside {home / '.aws'},"),
            ("~/.omp/agent", home / ".omp/agent", [],
             f"allowRead row {home / '.omp/agent'} is, contains or lies inside {home / '.omp/agent'},"),
            ("inside ~/.aws", home / ".aws/deeper", [],
             f"allowRead row {home / '.aws/deeper'} is, contains or lies inside {home / '.aws'},"),
            ("holding what a linked deny names", elsewhere, [],
             f"allowRead row {elsewhere} is, contains or lies inside {home / '.kube'} ({elsewhere / 'aws'}),"),
            ("~/.aws, dry run", home / ".aws", ["--dry-run"], f"is, contains or lies inside {home / '.aws'},"),
        )  # fmt: skip
        for label, dsh_home, args, message in cases:
            with self.subTest(case=label):
                trace.write_text("")
                run = self.seat("dsh", "--seats-root", self.seats, "--home", str(dsh_home), *args, "--", "--version",
                                BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertIn("a row of its denyRead list; the launch is refused before anything is made", run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertFalse((home / ".omp/profiles").exists())
        self.assertEqual(self.dsh_calls(), [])
        # Each path named is a row of the rendered settings of a launch that goes through: the rule's one source.
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        for path in (home / ".aws", home / ".omp/agent", home / ".kube"):
            self.assertIn(str(path), rendered["denyRead"])
        self.assertEqual(self.slots(), ([], []))

    def test_records_that_are_a_link_into_dsh_home_refuse_the_home_and_are_denied_by_their_physical_path(self):
        """U272d P2 `hcom-seat:1635`: the records row `<checkout>/.orchestration` enters the deny table in its physical
        form, so a `.orchestration` that is a link into DSH_HOME refuses the DSH_HOME holding it (exit 2, naming the
        records' physical path) before any directory is made, and a `.orchestration` linked elsewhere is denied under
        the path the link names, for read and for write."""
        records = self.dsh_home / "records"
        records.mkdir()
        link = self.repo / ".orchestration"
        link.symlink_to(records)
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(f"allowRead row {self.dsh_home} is, contains or lies inside {records},", run.stderr)
        self.assertFalse(Path(self.seats).exists())
        self.assertEqual(self.dsh_calls(), [])
        link.unlink()
        elsewhere = Path(self.temp.name).resolve() / "records-elsewhere"
        elsewhere.mkdir()
        link.symlink_to(elsewhere)
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        self.assertIn(str(elsewhere), rendered["denyRead"])
        self.assertIn(str(elsewhere), rendered["denyWrite"])
        self.assertNotIn(str(link), rendered["denyRead"])
        self.assertEqual(self.slots(), ([], []))

    def test_a_mode_000_directory_dsh_left_is_removed_and_a_slot_that_remains_fails_the_launch(self):
        """U272d P2 `hcom-seat:2215`: a directory dsh leaves with mode 000 (a nested one inside it too) kept `rm -rf`
        out of the state slot while the launch exited 0; the removal resets the modes first and both slots go, dsh's
        status returned. It fails closed: a slot the lever cannot remove (its parent `.state` made read-only while
        dsh runs) is named on stderr and the launch exits 2, not dsh's 0."""
        (self.calls / "leave-locked").touch()
        run = self.launch("--", "--version")
        (self.calls / "leave-locked").unlink()
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertEqual(self.slots(), ([], []))
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        state = Path(self.seats, ".state")
        os.chmod(state, 0o555)
        try:
            ((status, out, err),) = self.release(procs)
        finally:
            os.chmod(state, 0o700)
        self.assertEqual((status, out), (2, "0.2.1-rc.5\n"), err)
        self.assertIn(f"the per-launch slot {state / name} remains after its removal", err)
        self.assertIn("dsh exited 0; the launch exits 2", err)
        self.assertEqual(self.slots(), ([], [name]))

    def test_a_profile_root_linked_to_a_denied_directory_refuses_before_any_mkdir(self):
        """U272e P1 `hcom-seat:1835`: the role renders `~/.omp/profiles/dsh` into allowWrite and allowRead, and round 4's
        refusal judged three inputs that did not include it, so a profile root linked to `~/.aws` was granted write.
        The judge reads every rendered grant: a profile root that is a link to the scratch HOME's `.aws` refuses
        (exit 2) naming the row, its physical path and the deny, in a dry run too, before any directory is made (the
        DEBUG-trap recorder shows the tool directory's mkdir alone); a link to another omp profile refuses as well
        (the `profile` tag carries only while the grant lies where it is rendered); a real profile directory goes
        through."""
        home = self.home.resolve()
        (home / ".aws").mkdir()
        (home / ".omp/profiles/orchestrator").mkdir(parents=True)
        profile = home / ".omp/profiles/dsh"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("a link to ~/.aws", home / ".aws", [],
             f"allowRead row {profile} ({home / '.aws'}) is, contains or lies inside {home / '.aws'}, a row of its denyRead list"),
            ("a link to ~/.aws, dry run", home / ".aws", ["--dry-run"],
             f"allowRead row {profile} ({home / '.aws'}) is, contains or lies inside {home / '.aws'}, a row of its denyRead list"),
            ("a link to another profile", home / ".omp/profiles/orchestrator", [],
             f"allowRead row {profile} ({home / '.omp/profiles/orchestrator'}) is, contains or lies inside"
             f" {home / '.omp/profiles'}, a row of its denyRead list"),
        )  # fmt: skip
        for label, target, args, message in cases:
            with self.subTest(case=label):
                if profile.is_symlink():
                    profile.unlink()
                profile.symlink_to(target)
                trace.write_text("")
                run = self.launch(*args, "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertTrue(profile.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(sorted(p.name for p in (home / ".aws").iterdir()), [])
        self.assertEqual(self.dsh_calls(), [])
        profile.unlink()
        run = self.launch("--", "--version")
        self.assertEqual((run.returncode, run.stdout), (0, "0.2.1-rc.5\n"), run.stderr)
        self.assertTrue(profile.is_dir() and not profile.is_symlink())
        self.assertEqual(self.slots(), ([], []))

    def test_a_grant_row_under_any_deny_of_the_rendered_tables_refuses(self):
        """U272f: the judge's only source is the rendered tables, so a grant added under any deny of them refuses. The
        judge runs from the lever's own text over the tables a going launch rendered (its allowRead, allowWrite,
        denyRead and denyWrite, the macOS patterns aside) with the structural tags as the lever renders them, each
        naming one row by its list and position (U272g: the own cwd and state slot, rows 0 and 1 of both grant lists,
        the own profile, row 3 of both, the seats-root and project-file denies they overlap and the profiles deny):
        the tables as rendered pass; for every deny path, one row added to allowWrite below it and one added to
        allowRead equal to it each hit, naming the added row and a deny it lies inside (a row equal to a tagged deny
        carries no tag: the tag names the deny's position, not its spelling); a row of the own profile's spelling at
        DSH_HOME's position hits; a tagged row that a link moves off its rendered path hits too."""
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        home = self.home.resolve()
        seats = Path(self.seats).resolve()
        cwd, slot = str(seats / ".state" / name / "cwd"), str(seats / ".state" / name)
        profile, profiles = str(home / ".omp/profiles/dsh"), str(home / ".omp/profiles")
        deny_read = rendered["denyRead"]
        deny_write = [row for row in rendered["denyWrite"] if "*" not in row]
        for kind in ("allowRead", "allowWrite"):
            self.assertEqual([rendered[kind][i] for i in (0, 1, 3)], [cwd, slot, profile], kind)
        tags = [(tag, kind, ix, path) for kind in ("allowRead", "allowWrite")
                for tag, ix, path in (("slot", 0, cwd), ("slot", 1, slot), ("profile", 3, profile))]  # fmt: skip
        tags += [("slot", "denyWrite", ix, row) for ix, row in enumerate(deny_write) if row.startswith(cwd + "/")]
        tags += [
            ("slot", "denyRead", deny_read.index(row), row)
            for row in (str(home / ".local/state/omp-seats"), str(seats))
        ]
        tags += [("profile", "denyRead", deny_read.index(profiles), profiles)]
        self.assertEqual(len(tags), 6 + 8 + 2 + 1, tags)
        text = test_hcom_seat.SEAT.read_text()
        names = ("refuse", "clean_path", "require_clean_path", "physical_path", "physical_each", "ancestors_of")
        names += ("identity_table", "ascii_lower", "within_ix", "tag_row", "row_tag", "settings_judge")
        functions = "\n".join(
            text[text.index(f"\n{fn}() {{") : text.index("\n}\n", text.index(f"\n{fn}() {{")) + 3] for fn in names
        )
        stat_args = "stat_args=(-L -f '%d:%i')" if sys.platform == "darwin" else "stat_args=(-L -c '%d:%i')"

        def judge(allow_read, write, deny_read, deny_write):
            lists = "\n".join(
                f"{var}=({' '.join(shlex.quote(row) for row in rows)})"
                for var, rows in (("allow_read", allow_read), ("write", write), ("deny_read", deny_read), ("deny_write", deny_write))
            )  # fmt: skip
            tagged = "\n".join(f"tag_row {tag} {kind} {ix} {shlex.quote(path)}" for tag, kind, ix, path in tags)
            script = f"set -euo pipefail\n{stat_args}\n{functions}\n{lists}\n"
            script += f"row_tags=() row_tag_kinds=() row_tag_ixs=() row_tag_paths=()\n{tagged}\n"
            script += 'settings_judge || { printf "grant=%s\\ndeny=%s\\n" "${judge_grant}" "${judge_deny}"; exit 3; }\n'
            return subprocess.run(["/bin/bash", "-c", script], capture_output=True, text=True, check=False, timeout=60)

        clear = judge(rendered["allowRead"], rendered["allowWrite"], deny_read, deny_write)
        self.assertEqual((clear.returncode, clear.stdout), (0, ""), clear.stderr)
        denies = [(row, "denyRead") for row in deny_read] + [(row, "denyWrite") for row in deny_write]
        self.assertGreater(len(denies), 40, denies)
        for deny, kind in denies:
            # The deny a hit names is the first row in table order the added row overlaps: the deny itself, one above
            # it, or (for a row equal to it) one below it.
            related = [row for row, _ in denies
                       if Path(deny) == Path(row) or Path(row) in Path(deny).parents or Path(deny) in Path(row).parents]  # fmt: skip
            cases = [
                ("below it in allowWrite", f"{deny}/u272f-added", rendered["allowRead"], [*rendered["allowWrite"], f"{deny}/u272f-added"]),
                ("equal to it in allowRead", deny, [*rendered["allowRead"], deny], rendered["allowWrite"]),
            ]  # fmt: skip
            for label, added, allow_read, write in cases:
                with self.subTest(deny=deny, kind=kind, case=label):
                    hit = judge(allow_read, write, deny_read, deny_write)
                    self.assertEqual(hit.returncode, 3, hit.stdout + hit.stderr)
                    grant, named = hit.stdout.splitlines()
                    self.assertEqual(
                        grant, f"grant={'allowWrite' if 'allowWrite' in label else 'allowRead'} row {added}"
                    )
                    self.assertIn(
                        named.removeprefix("deny=").split(", a row of its ")[0].split(" (")[0], related, hit.stdout
                    )
        # The own profile's spelling at DSH_HOME's position (allowRead row 2): the tag names row 3 alone, so the row
        # hits the profiles deny like any other, where round 5's spelling-keyed tag exempted it.
        same = judge(
            [*rendered["allowRead"][:2], profile, *rendered["allowRead"][3:]],
            rendered["allowWrite"],
            deny_read,
            deny_write,
        )
        self.assertEqual(same.returncode, 3, same.stdout + same.stderr)
        self.assertEqual(
            same.stdout.splitlines(), [f"grant=allowRead row {profile}", f"deny={profiles}, a row of its denyRead list"]
        )
        # A tagged row moved by a link: the profile row is still at its position and spelled as rendered, so its tag
        # is found, and the exemption fails because its physical path is elsewhere.
        shutil.rmtree(home / ".omp/profiles/dsh")
        (home / ".omp/profiles/dsh").symlink_to(home / ".omp/profiles/orchestrator")
        (home / ".omp/profiles/orchestrator").mkdir()
        moved = judge(rendered["allowRead"], rendered["allowWrite"], deny_read, deny_write)
        self.assertEqual(moved.returncode, 3, moved.stdout + moved.stderr)
        self.assertIn(f"grant=allowRead row {profile} ({home / '.omp/profiles/orchestrator'})", moved.stdout)
        self.assertIn(f"deny={profiles}, a row of its denyRead list", moved.stdout)

    def test_a_termination_that_cannot_remove_a_slot_exits_2_naming_it(self):
        """U272e P2 `hcom-seat:2340`: when the slot removal failed under a signal, `set -e` ended the handler before the
        signal was restored, so SIGTERM with a read-only `.state` exited 1 with the slot behind. The handler reads
        the removal's status: the slot that remains is named and the launch exits 2 (not 1, not the signal's
        status); the sandbox slot, which could be removed, is gone."""
        (proc,) = self.held_launch("--", "--version", new_session=True)
        (name,) = self.slots()[0]
        state = Path(self.seats, ".state")
        os.chmod(state, 0o555)
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            out, err = proc.communicate(timeout=60)
        finally:
            os.chmod(state, 0o700)
            (self.calls / "hold").unlink()
        self.assertEqual((proc.returncode, out), (2, ""), err)
        self.assertIn(f"the per-launch slot {state / name} remains after its removal", err)
        self.assertIn("ended by SIGTERM; the launch exits 2 because a per-launch slot remains", err)
        self.assertEqual(self.slots(), ([], [name]))

    def test_a_dsh_home_or_run_root_at_the_profiles_directory_refuses_while_the_own_profile_passes(self):
        """U272f P1 `hcom-seat:1863`: round 5 keyed the exemption tags by rendered spelling, so a DSH_HOME equal to the
        profiles directory, or a `~/.omp/run` linked to it, was rendered in that spelling, inherited the own-profile
        exemption and put the whole profiles directory into allowWrite. A tag now names one row by its list and
        position: a DSH_HOME at the scratch HOME's `.omp/profiles` (holding a working `bin/dsh`), a DSH_HOME equal to
        the own profile `~/.omp/profiles/dsh` (the exempted row's own spelling, at another position) and a `~/.omp/run`
        linked to the profiles directory each refuse (exit 2) naming the profiles deny, before any directory is made
        (the DEBUG-trap recorder shows the tool directory's mkdir alone); the own profile row still passes."""
        home = self.home.resolve()
        profiles = home / ".omp/profiles"
        (profiles / "bin").mkdir(parents=True)
        for path in (profiles / "bin/dsh", profiles / "dsh/bin/dsh"):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(FAKE_DSH.format(calls=str(self.calls)))
            path.chmod(0o755)
        run_root = home / ".omp/run"
        hook = Path(self.temp.name) / "trace-hook.bash"
        hook.write_text('set -T\ntrap \'builtin printf "%s\\0" "$BASH_COMMAND" >> "$U272_TRACE"\' DEBUG\n')
        trace = Path(self.temp.name) / "trace"
        cases = (
            ("DSH_HOME at the profiles directory", profiles, None,
             f"allowRead row {profiles} is, contains or lies inside {profiles}, a row of its denyRead list"),
            ("DSH_HOME at the profiles directory, dry run", profiles, "--dry-run",
             f"allowRead row {profiles} is, contains or lies inside {profiles}, a row of its denyRead list"),
            ("DSH_HOME equal to the own profile", profiles / "dsh", None,
             f"allowRead row {profiles / 'dsh'} is, contains or lies inside {profiles}, a row of its denyRead list"),
            ("~/.omp/run linked to the profiles directory", self.dsh_home, None,
             f"allowWrite row {profiles} is, contains or lies inside {profiles}, a row of its denyRead list"),
        )  # fmt: skip
        for label, dsh_home, option, message in cases:
            with self.subTest(case=label):
                if dsh_home == self.dsh_home:
                    run_root.symlink_to(profiles)
                trace.write_text("")
                run = self.seat("dsh", "--seats-root", self.seats, "--home", str(dsh_home), *([option] if option else []),
                                "--", "--version", BASH_ENV=str(hook), U272_TRACE=str(trace))  # fmt: skip
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(message, run.stderr)
                self.assertIn("the launch is refused before anything is made", run.stderr)
                commands = trace.read_text().split("\0")[:-1]
                self.assertIn("settings_judge", " ".join(commands), "the refusal is the judge's")
                mkdirs = [c for c in commands if re.match(r"(/bin/)?mkdir\b", c)]
                self.assertTrue(mkdirs and all("tools_dir" in c for c in mkdirs), mkdirs)
        self.assertFalse(Path(self.seats).exists())
        self.assertTrue(run_root.is_symlink(), "the launch neither removed nor replaced the link")
        self.assertEqual(self.dsh_calls(), [])
        # The own profile row, at its own position, passes: the same launch goes through once `~/.omp/run` is a
        # directory again, with the profiles directory in no grant list but as the own profile row.
        run_root.unlink()
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        rendered = self.settings_of(name)["filesystem"]
        ((status, out, err),) = self.release(procs)
        self.assertEqual((status, out), (0, "0.2.1-rc.5\n"), err)
        for kind in ("allowRead", "allowWrite"):
            self.assertEqual(rendered[kind][3], str(profiles / "dsh"), kind)
            self.assertNotIn(str(profiles), rendered[kind], kind)
        self.assertIn(str(profiles), rendered["denyRead"])
        self.assertTrue(run_root.is_dir() and not run_root.is_symlink())
        self.assertEqual(self.slots(), ([], []))

    def test_an_unsearchable_state_parent_at_cleanup_exits_2_naming_the_slot(self):
        """U272f P2 `hcom-seat:2347`: `[[ -e ]]` and `[[ -L ]]` are both false for a slot whose parent cannot be
        searched, so a `.state` of mode 000 at cleanup made the lever read its slot as absent and exit 0 with the slot
        behind. The existence read is a status-checked stat: a failed read that is not ENOENT refuses (exit 2) naming
        the slot and the error, on the normal exit and under a signal alike; the sandbox slot, read and removed
        first, is gone."""
        state = Path(self.seats, ".state")
        procs = self.held_launch("--", "--version")
        (name,) = self.slots()[0]
        os.chmod(state, 0)
        try:
            ((status, out, err),) = self.release(procs)
        finally:
            os.chmod(state, 0o700)
        self.assertEqual((status, out), (2, "0.2.1-rc.5\n"), err)
        self.assertIn(f"cannot read whether the per-launch slot {state / name} exists (", err)
        self.assertIn("Permission denied", err)
        self.assertNotIn("remains after its removal", err, "a failed read is not read as a slot that was removed")
        self.assertEqual(self.slots(), ([], [name]))
        shutil.rmtree(state / name)
        (proc,) = self.held_launch("--", "--version", new_session=True)
        (name,) = self.slots()[0]
        os.chmod(state, 0)
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            out, err = proc.communicate(timeout=60)
        finally:
            os.chmod(state, 0o700)
            (self.calls / "hold").unlink()
        self.assertEqual((proc.returncode, out), (2, ""), err)
        self.assertIn(f"cannot read whether the per-launch slot {state / name} exists (", err)
        self.assertEqual(self.slots(), ([], [name]))


if __name__ == "__main__":
    unittest.main()
