"""regime-start, regime-stop and the supervisor pass (regime-cutover U36).

The checkout's own levers run (regime-start calls the hcom-seat beside it, which runs seat-login-preflight) against
`tests/fixtures/regime-start/fake-hcom.py` under the name `hcom`, which keeps its seats in a JSON state file. HOME is a
scratch directory holding the seat overlays and the extension directories hcom-seat checks; the checkout is a
scratch git repository; the store is an explicit scratch directory unless a test says otherwise. Nothing starts a real
seat or reads the real `~/.local/state`.
"""

import fcntl
import hashlib
import json
import os
import plistlib
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
START = ROOT / "scripts/orchestrator/regime-start"
STOP = ROOT / "scripts/orchestrator/regime-stop"
FAKE_HCOM = ROOT / "tests/fixtures/regime-start/fake-hcom.py"
PLIST = ROOT / "home/Library/LaunchAgents/com.mryfmo.dotfiles.regime-supervisor.plist.tmpl"
SERVICE = ROOT / "home/dot_config/systemd/user/regime-supervisor.service.tmpl"
TIMER = ROOT / "home/dot_config/systemd/user/regime-supervisor.timer.tmpl"
CHEZMOI = shutil.which("chezmoi")
BINARY_STAND_IN = Path(os.path.realpath("/usr/bin/true"))
# A process that takes the kernel lock on argv[1], says so, and keeps it until it is killed.
HOLDER = "import fcntl, sys, time; h = open(sys.argv[1], 'a'); fcntl.flock(h, fcntl.LOCK_EX); print('held', flush=True); time.sleep(120)"
GIT_IDENTITY = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
}


class RegimeStartTest(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="regime-start-")).resolve()
        self.addCleanup(shutil.rmtree, self.temp, True)
        self.home = self.temp / "home"
        for role in ("orchestrator", "worker"):
            for kind, body in (("policies", "tools: {}\n"), ("profiles", "modelRoles: {}\n")):
                path = self.home / f".agents/omp/{kind}/{role}.yml"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body)
            # U75: hcom-seat passes the role's standing rules as --append-system-prompt and refuses without them.
            rules = self.home / f".agents/omp/rules/{role}.md"
            rules.parent.mkdir(parents=True, exist_ok=True)
            rules.write_text("## Regime\n")
        for ext in (
            ".local/lib/omp-extensions/pi-claude-bridge",
            ".agents/omp/extensions/openai-siwc",
            ".agents/omp/hooks",
        ):
            (self.home / ext).mkdir(parents=True)
        bindir = self.temp / "bin"
        bindir.mkdir()
        (bindir / "hcom").symlink_to(FAKE_HCOM)
        # hcom-seat requires herdr, omp and srt (and bwrap, socat and rg on Linux) before it launches (U85); the fake
        # hcom runs none of them, so copies of the system's `true` binary stand in (hcom-seat checks real executables).
        for tool in ("herdr", "omp", "srt", "bwrap", "socat", "rg"):
            shutil.copy(BINARY_STAND_IN, bindir / tool)
        self.state = self.temp / "hcom-state.json"
        self.store = self.temp / "store"
        self.store.mkdir()
        self.repo = self.temp / "pilot"
        self.repo.mkdir()
        self.env = {
            "HOME": str(self.home),
            # The fake bin and the system directories only: no tool of the host or the runner (a mise shim of claude)
            # reaches hcom-seat's tool resolution unless this fixture plants it.
            "PATH": f"{bindir}:/usr/bin:/bin",
            "TMPDIR": str(self.temp),
            "FAKE_HCOM_STATE": str(self.state),
            "HCOM_DIR": str(self.store),
            "HCOM_TEAM": "pilot",
            "REGIME_START_WAIT_SECONDS": "4",
            **GIT_IDENTITY,
        }
        self.git("init", "-q")
        self.git("commit", "-q", "--allow-empty", "-m", "init")
        self.registry = self.home / ".local/state/regime-supervisor"
        self.conf = self.conf_of(self.repo)
        self.lock = self.registry / "supervisor.lock"

    def conf_of(self, toplevel, slug="pilot"):
        """The checkout's registration: `<slug>-<first 12 hex of sha256(toplevel)>.conf` (U36 F3)."""
        return self.registry / f"{slug}-{hashlib.sha256(str(toplevel).encode()).hexdigest()[:12]}.conf"

    def make_repo(self, path):
        path.mkdir(parents=True)
        self.git("init", "-q", cwd=path)
        self.git("commit", "-q", "--allow-empty", "-m", "init", cwd=path)
        return path

    def lock_is_free(self):
        """Whether the kernel lock can be taken right now (this test process tries, then lets it go)."""
        with open(self.lock, "a") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            fcntl.flock(handle, fcntl.LOCK_UN)
            return True

    def paused_pass(self, new_session=False):
        """A supervisor pass whose launch is paused inside the fake hcom; returns (process, release file)."""
        pause = self.temp / f"release-{len(list(self.temp.glob('release-*')))}"
        process = subprocess.Popen(
            [str(START), "--supervise"], cwd=self.temp, env={**self.env, "FAKE_LAUNCH_PAUSE": str(pause)},
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=new_session,
        )  # fmt: skip
        self.addCleanup(lambda: process.poll() is None and process.kill())
        started = Path(f"{pause}.started")
        # hcom-seat's checks before it launches (U85) take seconds, more under a loaded parallel run: wait up to 120 s,
        # and stop at once with the pass's stderr if it ends without reaching the launch.
        for _ in range(1200):
            if started.exists() or process.poll() is not None:
                break
            time.sleep(0.1)
        self.assertTrue(
            started.exists(), f"the pass reached its launch: {'' if process.poll() is None else process.stderr.read()}"
        )
        return process, pause

    def background(self, lever, *args, **extra):
        process = subprocess.Popen(
            [str(lever), *args], cwd=self.repo, env={**self.env, **extra}, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )  # fmt: skip
        self.addCleanup(lambda: process.poll() is None and process.kill())
        return process

    def assert_no_hcom_call_held_the_lock(self):
        self.assertEqual([call["argv"][:2] for call in self.hcom()["calls"] if call["fd9"]], [])

    def kills(self):
        return [call for call in self.hcom()["calls"] if call["argv"][:1] == ["kill"]]

    def git(self, *args, cwd=None):
        subprocess.run(["git", *args], cwd=cwd or self.repo, env=self.env, check=True, capture_output=True)

    def run_lever(self, lever, *args, cwd=None, **overrides):
        env = {**self.env, **{key: value for key, value in overrides.items() if value is not None}}
        for key in (key for key, value in overrides.items() if value is None):
            env.pop(key, None)
        return subprocess.run(
            [str(lever), *args], cwd=cwd or self.repo, env=env, capture_output=True, text=True, timeout=120, check=False
        )

    def hcom(self):
        return json.loads(self.state.read_text()) if self.state.exists() else {"alive": [], "stopped": [], "calls": []}

    def launches(self):
        return [call for call in self.hcom()["calls"] if call["argv"][:1] == ["omp"]]

    def registration(self):
        return dict(line.split("=", 1) for line in self.conf.read_text().splitlines())

    def log(self, store=None):
        path = (store or self.store) / "supervisor.log"
        return path.read_text() if path.exists() else ""

    def crash(self, reason="process_exit by:system"):
        """The seat dies without an hcom kill: gone from the alive list, with hcom's stop record."""
        state = self.hcom()
        seat = state["alive"].pop()
        state["stopped"].append({**seat, "reason": reason})
        self.state.write_text(json.dumps(state))
        return seat

    def test_start_launches_once_registers_and_says_where_to_type(self):
        first = self.run_lever(START)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(
            first.stdout,
            f"orchestrator-rafa is listening on team pilot. Type your instruction in the pane `orchestrator`; the store is {self.store}.\n",
        )
        (launch,) = self.launches()
        self.assertEqual(launch["argv"][-2:], ["--hcom-team", "pilot"])
        self.assertEqual((launch["HCOM_DIR"], launch["HCOM_TEAM"]), (str(self.store), "pilot"))
        self.assertEqual(
            self.registration(),
            {"toplevel": str(self.repo), "hcom_dir": str(self.store), "hcom_team": "pilot", "program": "",
             "seat": "orchestrator-rafa", "base": "rafa", "fails": "0", "next": "0"},
        )  # fmt: skip
        again = self.run_lever(START)
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertTrue(again.stdout.startswith("orchestrator-rafa is already alive on team pilot."), again.stdout)
        self.assertEqual(len(self.launches()), 1, "an alive orchestrator is reported, never duplicated")
        self.assertIn("regime-start launched orchestrator-rafa", self.log())

    def test_a_seat_without_its_standing_rules_launches_nothing(self):
        """U75: the orchestrator's rules file is required; regime-start reports hcom-seat's refusal, and no omp starts."""
        rules = self.home / ".agents/omp/rules/orchestrator.md"
        for content in (None, ""):
            with self.subTest(rules=content):
                rules.unlink(missing_ok=True)
                if content is not None:
                    rules.write_text(content)
                run = self.run_lever(START)
                self.assertNotEqual(run.returncode, 0, run.stdout)
                self.assertIn(f"standing rules absent or empty: {rules}", run.stderr)
                self.assertEqual(self.launches(), [])
        rules.write_text("## Regime\n")
        started = self.run_lever(START)
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertIn(str(rules), self.launches()[0]["argv"])

    def test_a_program_names_its_store_and_must_exist(self):
        refused = self.run_lever(START, "pilot")
        self.assertEqual(refused.returncode, 2)
        self.assertIn("run regime-init pilot first", refused.stderr)
        self.assertEqual(self.launches(), [])
        program = self.repo / ".orchestration/orchestrate/pilot"
        program.mkdir(parents=True)
        run = self.run_lever(START, "pilot")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(run.stdout.endswith(f"the store is {program}.\n"), run.stdout)
        self.assertEqual(self.run_lever(START, "Bad/Name").returncode, 2)

    def test_the_supervisor_relaunches_a_seat_that_died(self):
        self.assertEqual(self.run_lever(START).returncode, 0)
        for reason in ("process_exit by:system", "exit:shutdown by:session"):
            with self.subTest(reason=reason):
                dead = self.crash(reason)
                # The pass runs from anywhere, with no store in its environment, as launchd or systemd runs it.
                run = self.run_lever(START, "--supervise", cwd=self.temp, HCOM_DIR=None, HCOM_TEAM=None)
                self.assertEqual(run.returncode, 0, run.stderr)
                alive = self.hcom()["alive"]
                self.assertEqual(len(alive), 1)
                self.assertEqual(self.registration()["seat"], alive[0]["name"])
                self.assertIn(f"no orchestrator alive (last seat {dead['name']}:", self.log())
                self.assertIn(f"relaunched {alive[0]['name']}", self.log())
                self.assertEqual(self.launches()[-1]["HCOM_TEAM"], "pilot", "the registered team, explicitly")
        quiet = self.run_lever(START, "--supervise", cwd=self.temp)
        self.assertEqual(quiet.returncode, 0)
        self.assertEqual(len(self.launches()), 3, "an alive seat is left alone")

    def test_an_hcom_kill_is_a_stop_on_purpose(self):
        self.assertEqual(self.run_lever(START).returncode, 0)
        kill = subprocess.run(["hcom", "kill", "orchestrator-rafa", "--go"], env=self.env, check=False)
        self.assertEqual(kill.returncode, 0)
        run = self.run_lever(START, "--supervise", cwd=self.temp)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(len(self.launches()), 1)
        self.assertFalse(self.conf.exists(), "the supervision ends with the registration")
        self.assertIn("orchestrator-rafa was stopped with hcom kill; supervision of", self.log())

    def test_regime_stop_ends_the_supervision_and_stops_the_seat(self):
        self.assertEqual(self.run_lever(START).returncode, 0)
        worker = {"name": "worker-zulu", "base": "zulu", "tag": "worker", "status": "listening"}
        state = self.hcom()
        state["alive"].append(worker)
        self.state.write_text(json.dumps(state))
        stop = self.run_lever(STOP, HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(stop.stdout, "regime-stop: stopped orchestrator-rafa\n")
        self.assertFalse(self.conf.exists())
        self.assertEqual([seat["name"] for seat in self.hcom()["alive"]], ["worker-zulu"])
        self.assertEqual(self.run_lever(START, "--supervise", cwd=self.temp).returncode, 0)
        self.assertEqual(len(self.launches()), 1, "nothing relaunched after regime-stop")
        self.assertEqual(self.run_lever(START).returncode, 0)
        everything = self.run_lever(STOP, "--all")
        self.assertEqual(everything.returncode, 0, everything.stderr)
        self.assertEqual(self.hcom()["alive"], [])
        self.assertEqual(self.run_lever(STOP, "--bogus").returncode, 2)

    def test_a_failed_relaunch_backs_off(self):
        self.assertEqual(self.run_lever(START).returncode, 0)
        self.crash()
        before = time.time()
        failed = self.run_lever(START, "--supervise", cwd=self.temp, FAKE_LAUNCH_FAILS="1")
        self.assertEqual(failed.returncode, 0, failed.stderr)
        registration = self.registration()
        self.assertEqual(registration["fails"], "1")
        self.assertGreaterEqual(int(registration["next"]), int(before) + 59)
        self.assertIn("relaunch failed (1 in a row); next attempt in 60 s", self.log())
        self.assertIn("hcom-seat orchestrator exited 1", self.log())
        launches = len(self.launches())
        self.assertEqual(self.run_lever(START, "--supervise", cwd=self.temp).returncode, 0)
        self.assertEqual(len(self.launches()), launches, "no attempt inside the backoff window")
        self.conf.write_text(self.conf.read_text().replace(f"next={registration['next']}", "next=0"))
        self.assertEqual(self.run_lever(START, "--supervise", cwd=self.temp).returncode, 0)
        self.assertEqual(self.registration()["fails"], "0", "a seat seen alive resets the backoff")

    def test_a_failed_read_or_a_bad_registration_launches_nothing(self):
        self.assertEqual(self.run_lever(START).returncode, 0)
        self.crash()
        launches = len(self.launches())
        listed = self.run_lever(START, "--supervise", cwd=self.temp, FAKE_LIST_FAILS="1")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertIn("hcom list failed; nothing launched", self.log())
        garbled = self.run_lever(START, "--supervise", cwd=self.temp, FAKE_STOPPED_GARBLED="1")
        self.assertEqual(garbled.returncode, 0, garbled.stderr)
        self.assertIn("cannot read the stop record of orchestrator-rafa; nothing launched", self.log())
        refused = self.run_lever(START, FAKE_LIST_FAILS="1")
        self.assertEqual(refused.returncode, 2)
        self.assertIn("hcom list failed", refused.stderr)
        self.assertEqual(len(self.launches()), launches)

    def test_a_seat_that_never_comes_alive_is_a_failure(self):
        run = self.run_lever(START, FAKE_LAUNCH_SILENT="1", REGIME_START_WAIT_SECONDS="0")
        self.assertEqual(run.returncode, 1)
        self.assertIn(f"no orchestrator seat alive in {self.store} after 0 s", run.stderr)
        self.assertFalse(self.conf.exists())

    def test_the_dotfiles_program_keeps_its_pre_move_store_and_team(self):
        """Until the one-time move, the dotfiles seats talk on `regime` in `hcom-regime` (decisions 10:19:06Z)."""
        repo = self.temp / "dotfiles"
        repo.mkdir()
        self.git("init", "-q", cwd=repo)
        self.git("commit", "-q", "--allow-empty", "-m", "init", cwd=repo)
        legacy = self.home / ".local/state/hcom-regime"
        legacy.mkdir(parents=True)
        (legacy / "hcom.db").write_text("")
        run = self.run_lever(START, cwd=repo, HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("has not moved its store yet", run.stderr)
        (launch,) = self.launches()
        self.assertEqual((launch["HCOM_DIR"], launch["HCOM_TEAM"]), (str(legacy), "regime"))
        self.assertEqual(launch["argv"][-2:], ["--hcom-team", "regime"])
        conf = dict(line.split("=", 1) for line in self.conf_of(repo, "dotfiles").read_text().splitlines())
        self.assertEqual((conf["hcom_dir"], conf["hcom_team"]), (str(legacy), "regime"))
        self.assertIn("regime-start launched", self.log(legacy))

    def test_a_registration_must_hold_every_key_once_or_nothing_launches(self):
        """U36 F4: a missing, repeated, unknown or empty key, a truncated file or a seat that is not
        `orchestrator-<base>` is skipped and logged; it never launches and never skips the stop record."""
        self.assertEqual(self.run_lever(START).returncode, 0)
        kill = subprocess.run(["hcom", "kill", "orchestrator-rafa", "--go"], env=self.env, check=False)
        self.assertEqual(kill.returncode, 0)
        good = self.conf.read_text()
        lines = good.splitlines()
        cases = {
            "base missing": "\n".join(line for line in lines if not line.startswith("base=")) + "\n",
            "seat missing": "\n".join(line for line in lines if not line.startswith("seat=")) + "\n",
            "truncated": "\n".join(lines[:3]) + "\n",
            "truncated mid-line": good[: good.index("base=") + 3],
            "empty": "",
            "empty base": good.replace("base=rafa", "base="),
            "repeated key": good + "base=zulu\n",
            "unknown key": good + "exec=evil\n",
            "a line without a key": good + "rafa\n",
            "seat not orchestrator-<base>": good.replace("seat=orchestrator-rafa", "seat=orchestrator-zulu"),
            "bad team": good.replace("hcom_team=pilot", "hcom_team=Bad Team"),
            "unbounded counter": good.replace("fails=0", "fails=99999"),
            "not a number": good.replace("next=0", "next=x"),
        }
        for label, text in cases.items():
            with self.subTest(label):
                self.conf.write_text(text)
                run = self.run_lever(START, "--supervise", cwd=self.temp)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertIn(f"skipped {self.conf}: ", run.stderr)
                self.assertEqual(self.conf.read_text(), text, "an unusable registration is never removed or rewritten")
                stop = self.run_lever(STOP)
                self.assertEqual(stop.returncode, 2, stop.stdout)
                self.assertIn("is unusable", stop.stderr)
        self.assertEqual(len(self.launches()), 1, "nothing relaunched the seat stopped with hcom kill")
        self.assertEqual(len(self.kills()), 1, "a stop from an unusable registration kills nothing")

    def test_two_checkouts_with_one_basename_keep_separate_registrations(self):
        """U36 F3: a registration belongs to one canonical toplevel; stop and start never adopt another's."""
        other = self.make_repo(self.temp / "elsewhere/pilot")
        other_store = self.temp / "other-store"
        other_store.mkdir()
        self.assertEqual(self.run_lever(START).returncode, 0)
        run = self.run_lever(START, cwd=other, HCOM_DIR=str(other_store))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertNotEqual(self.conf, self.conf_of(other))
        self.assertEqual(
            sorted(path.name for path in self.registry.glob("*.conf")),
            sorted([self.conf.name, self.conf_of(other).name]),
        )
        # Stopping the second checkout stops only its seat and its registration.
        stop = self.run_lever(STOP, cwd=other, HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(
            [(call["argv"][1], call["HCOM_DIR"]) for call in self.kills()], [("orchestrator-zulu", str(other_store))]
        )
        self.assertTrue(self.conf.exists())
        self.assertFalse(self.conf_of(other).exists())
        # A registration copied under another checkout's name is refused, not adopted.
        shutil.copy(self.conf, self.conf_of(other))
        forged = self.run_lever(STOP, cwd=other, HCOM_DIR=None, HCOM_TEAM=None)
        self.assertEqual(forged.returncode, 2)
        self.assertIn("the file name does not belong to the toplevel", forged.stderr)
        self.assertEqual(len(self.kills()), 1)
        self.conf_of(other).unlink()
        # A registered checkout cannot be moved to another store or team without regime-stop.
        moved = self.run_lever(START, HCOM_DIR=str(other_store))
        self.assertEqual(moved.returncode, 2)
        self.assertIn("run regime-stop first", moved.stderr)
        self.assertIn(f"hcom_dir={self.store}", self.conf.read_text())
        # A store whose origin names another checkout is refused, an explicit store included.
        (other_store / "origin").write_text(f"{other}\n")
        for lever in (START, STOP):
            with self.subTest(lever=lever.name):
                third = self.make_repo(self.temp / f"third-{lever.name}/pilot")
                refused = self.run_lever(lever, cwd=third, HCOM_DIR=str(other_store))
                self.assertEqual(refused.returncode, 2)
                self.assertIn(f"the store {other_store} belongs to {other}", refused.stderr)
        (self.store / "origin").write_text(f"{other}\n")
        self.crash()
        launches = len(self.launches())
        skipped = self.run_lever(START, "--supervise", cwd=self.temp)
        self.assertIn(f"the store {self.store} belongs to {other}", skipped.stderr)
        self.assertEqual(len(self.launches()), launches)

    def test_stop_waits_for_a_relaunch_in_flight_however_old_the_lock_looks(self):
        """U36 F2: a live owner keeps the lock: aged by a day, and after other processes tried and exited, stop
        still waits for the paused relaunch, then stops the seat it launched; nothing survives."""
        self.assertEqual(self.run_lever(START).returncode, 0)
        inode = self.lock.stat().st_ino
        self.crash()
        supervise, pause = self.paused_pass()
        day_old = time.time() - 24 * 3600
        os.utime(self.lock, (day_old, day_old))
        # Non-owners try and exit while the pass holds the lock; their exits release nothing.
        skipped = self.run_lever(START, "--supervise", cwd=self.temp)
        self.assertEqual(skipped.returncode, 0)
        self.assertIn(f"pid {supervise.pid} holds {self.lock}; this pass skips", skipped.stderr)
        refused = self.run_lever(START, REGIME_LOCK_WAIT_SECONDS="1")
        self.assertEqual(refused.returncode, 2)
        self.assertIn(f"pid {supervise.pid} still holds {self.lock} after 1 s; nothing changed", refused.stderr)
        stop = self.background(STOP)
        time.sleep(2)
        self.assertIsNone(stop.poll(), "regime-stop waits for the lock the paused pass holds")
        self.assertFalse(self.lock_is_free())
        pause.touch()
        self.assertEqual(supervise.wait(60), 0, supervise.communicate()[1])
        out, err = stop.communicate(timeout=60)
        self.assertEqual(stop.returncode, 0, err)
        self.assertEqual(out, "regime-stop: stopped orchestrator-zulu\n", "the stop sees and stops the relaunched seat")
        self.assertFalse(self.conf.exists(), "the pass's rewrite does not survive the stop")
        self.assertEqual(self.hcom()["alive"], [])
        self.assertTrue(self.lock_is_free())
        self.assertEqual(self.lock.stat().st_ino, inode, "the lock file is never removed or replaced")
        self.assertEqual(self.run_lever(START, "--supervise", cwd=self.temp).returncode, 0)
        self.assertEqual(len(self.launches()), 2, "nothing relaunched after the stop")
        self.assert_no_hcom_call_held_the_lock()

    def test_killing_the_supervising_shell_keeps_the_lock_while_its_launch_runs(self):
        """The subshell that runs a launch keeps the lock until the launch returns, so killing regime-start itself
        cannot let a stop in ahead of a launch still in flight."""
        self.assertEqual(self.run_lever(START).returncode, 0)
        self.crash()
        supervise, pause = self.paused_pass()
        os.kill(supervise.pid, signal.SIGKILL)
        supervise.wait(10)
        stop = self.background(STOP)
        time.sleep(2)
        self.assertIsNone(stop.poll(), "the launch still in flight holds the lock")
        self.assertFalse(self.lock_is_free())
        pause.touch()
        out, err = stop.communicate(timeout=60)
        self.assertEqual(stop.returncode, 0, err)
        self.assertEqual(out, "regime-stop: stopped orchestrator-zulu\n")
        self.assertEqual(self.hcom()["alive"], [])
        self.assertFalse(self.conf.exists())
        self.assertTrue(self.lock_is_free())

    def test_a_dead_owner_releases_the_lock_at_once(self):
        """The kernel drops the lock with its last holder: a killed holder, or a pass killed with its whole launch,
        never blocks the next start or stop, and no launch continues outside the lock."""
        # The directory exists before the holder starts, so its open cannot race the mkdir (U36c audit).
        self.registry.mkdir(parents=True, exist_ok=True)
        holder = subprocess.Popen(
            [sys.executable, "-I", "-c", HOLDER, str(self.lock)],
            stdout=subprocess.PIPE, text=True,
        )  # fmt: skip
        self.addCleanup(lambda: holder.poll() is None and holder.kill())
        self.assertEqual(holder.stdout.readline(), "held\n")
        self.assertEqual(self.run_lever(START, REGIME_LOCK_WAIT_SECONDS="1").returncode, 2)
        holder.kill()
        holder.wait(10)
        started = self.run_lever(START, REGIME_LOCK_WAIT_SECONDS="0")
        self.assertEqual(started.returncode, 0, started.stderr)
        self.crash()
        supervise, _pause = self.paused_pass(new_session=True)
        os.killpg(supervise.pid, signal.SIGKILL)
        supervise.wait(10)
        stop = self.run_lever(STOP, REGIME_LOCK_WAIT_SECONDS="2")
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(stop.stdout, "regime-stop: no seat to stop in " + str(self.store) + "; supervision ended\n")
        self.assertEqual(self.hcom()["alive"], [], "the killed launch never added a seat")
        self.assertFalse(self.conf.exists())
        self.assertTrue(self.lock_is_free())

    def test_a_detached_seat_never_holds_the_lock(self):
        """hcom-seat and every hcom call get descriptor 9 closed, so a long-lived process the launch leaves behind
        does not keep the lock: right after regime-start returns, regime-stop takes it without waiting."""
        linger = self.temp / "linger.pid"
        started = self.run_lever(START, FAKE_LAUNCH_LINGER=str(linger))
        self.assertEqual(started.returncode, 0, started.stderr)
        pid = int(linger.read_text())
        self.addCleanup(lambda: subprocess.run(["kill", str(pid)], check=False, capture_output=True))
        os.kill(pid, 0)  # the detached process is alive
        self.assertTrue(self.lock_is_free())
        stop = self.run_lever(STOP, REGIME_LOCK_WAIT_SECONDS="0")
        self.assertEqual(stop.returncode, 0, stop.stderr)
        self.assertEqual(stop.stdout, "regime-stop: stopped orchestrator-rafa\n")
        self.assert_no_hcom_call_held_the_lock()

    def test_a_lock_held_by_another_process_refuses_start_and_stop_and_a_pass_skips(self):
        self.registry.mkdir(parents=True)
        with open(self.lock, "a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.truncate(0)
            handle.write(f"{os.getpid()}\n")
            handle.flush()
            for lever in (START, STOP):
                with self.subTest(lever=lever.name):
                    run = self.run_lever(lever, REGIME_LOCK_WAIT_SECONDS="1")
                    self.assertEqual(run.returncode, 2)
                    self.assertIn(f"pid {os.getpid()} still holds {self.lock} after 1 s; nothing changed", run.stderr)
            run = self.run_lever(START, "--supervise", cwd=self.temp)
            self.assertEqual(run.returncode, 0)
            self.assertEqual(self.launches(), [])
            fcntl.flock(handle, fcntl.LOCK_UN)
        run = self.run_lever(START, REGIME_LOCK_WAIT_SECONDS="0")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(self.lock.is_file())
        self.assertTrue(self.lock_is_free(), "released when regime-start exits")

    def test_the_backoff_saturates_and_the_counter_is_bounded(self):
        """U36 F5: the delay is computed by saturated doubling, never by a shift that overflows."""
        self.assertEqual(self.run_lever(START).returncode, 0)
        self.crash()
        good = self.conf.read_text()
        for fails, expected, delay in (
            ("0", "1", 60), ("1", "2", 120), ("4", "5", 960), ("5", "6", 1800), ("59", "60", 1800),
            ("63", "64", 1800), ("9998", "9999", 1800), ("9999", "9999", 1800),
        ):  # fmt: skip
            with self.subTest(fails=fails):
                self.conf.write_text(good.replace("fails=0", f"fails={fails}"))
                before = int(time.time())
                run = self.run_lever(START, "--supervise", cwd=self.temp, FAKE_LAUNCH_FAILS="1")
                self.assertEqual(run.returncode, 0, run.stderr)
                registration = dict(line.split("=", 1) for line in self.conf.read_text().splitlines())
                self.assertEqual(registration["fails"], expected)
                self.assertGreaterEqual(int(registration["next"]), before + delay)
                self.assertLessEqual(int(registration["next"]), int(time.time()) + delay)
                self.assertIn(f"relaunch failed ({expected} in a row); next attempt in {delay} s", self.log())


def render(path, os_name):
    with tempfile.TemporaryDirectory() as temp:
        return subprocess.run(
            [CHEZMOI, "--source", temp, "--cache", f"{temp}/cache", "--persistent-state", f"{temp}/state",
             "execute-template", "--init", "--override-data",
             json.dumps({"chezmoi": {"os": os_name, "homeDir": "/render-home"}})],
            input=path.read_text(), text=True, capture_output=True, check=True,
        ).stdout  # fmt: skip


@unittest.skipUnless(CHEZMOI, "chezmoi is not installed")
class SupervisorDefinitionTest(unittest.TestCase):
    """The launchd agent and the systemd user units run the same pass, at the same interval, with the same PATH."""

    def test_launchd_and_systemd_run_the_same_pass(self):
        plist = plistlib.loads(render(PLIST, "darwin").encode())
        self.assertEqual(plist["Label"], "com.mryfmo.dotfiles.regime-supervisor")
        command = ["/render-home/.local/bin/common/regime-start", "--supervise"]
        self.assertEqual(plist["ProgramArguments"], command)
        self.assertTrue(plist["RunAtLoad"])
        self.assertEqual((plist["StandardOutPath"], plist["StandardErrorPath"]), ("/dev/null", "/dev/null"))
        # U36 F1: launchd loads ~/Library/LaunchAgents at every login, so the job ships disabled; only the
        # operator's `launchctl enable` override, which launchd keeps across logins and boots, loads it.
        self.assertIs(plist["Disabled"], True)
        service = render(SERVICE, "linux").splitlines()
        timer = render(TIMER, "linux").splitlines()
        self.assertIn(f"ExecStart={' '.join(command)}", service)
        self.assertIn("Type=oneshot", service)
        self.assertIn(f"Environment=PATH={plist['EnvironmentVariables']['PATH']}", service)
        self.assertIn(f"OnUnitActiveSec={plist['StartInterval']}", timer)
        self.assertIn("OnStartupSec=60", timer)
        self.assertIn("WantedBy=timers.target", timer)
        ignore = ROOT / "home/.chezmoitemplates/chezmoiignore.d"
        self.assertIn("Library", (ignore / "ubuntu/common").read_text().splitlines())
        self.assertIn(".config/systemd", (ignore / "macos").read_text().splitlines())

    def test_nothing_enables_the_supervisor_but_the_operator(self):
        """U36 F1: no managed file links the timer into timers.target.wants or runs launchctl or systemctl for the
        supervisor, so a fresh login on a fresh host starts none; the README carries the persistent commands."""
        self.assertEqual(list((ROOT / "home").rglob("*.wants")), [])
        hits = []
        for root in (
            ROOT / "home/.chezmoiscripts",
            ROOT / "install",
            ROOT / "scripts",
            ROOT / "Makefile",
            ROOT / "setup.sh",
        ):
            for path in [root] if root.is_file() else [path for path in root.rglob("*") if path.is_file()]:
                text = path.read_text(errors="replace")
                if "regime-supervisor" in text and ("launchctl" in text or "systemctl" in text):
                    hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])
        readme = (ROOT / "README.md").read_text()
        for command in (
            "launchctl enable gui/$(id -u)/com.mryfmo.dotfiles.regime-supervisor",
            "launchctl disable gui/$(id -u)/com.mryfmo.dotfiles.regime-supervisor",
            "systemctl --user enable --now regime-supervisor.timer",
            "systemctl --user disable --now regime-supervisor.timer",
        ):
            self.assertIn(command, readme)


if __name__ == "__main__":
    unittest.main()
