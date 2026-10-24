"""regime-start, regime-stop and the supervisor pass (regime-cutover U36).

The checkout's own levers run (regime-start calls the hcom-seat beside it, which runs seat-login-preflight) against
`tests/fixtures/regime-start/fake-hcom.py` under the name `hcom`, which keeps its seats in a JSON state file. HOME is a
scratch directory holding the seat overlays and the extension directories hcom-seat checks; the checkout is a
scratch git repository; the store is an explicit scratch directory unless a test says otherwise. Nothing starts a real
seat or reads the real `~/.local/state`.
"""

import json
import os
import plistlib
import shutil
import subprocess
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
        for role in ("orchestrator", "worker", "audit"):
            for kind, body in (("policies", "tools: {}\n"), ("profiles", "modelRoles: {}\n")):
                path = self.home / f".agents/omp/{kind}/{role}.yml"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body)
        for ext in (
            ".local/lib/omp-extensions/pi-claude-bridge",
            ".agents/omp/extensions/openai-siwc",
            ".agents/omp/hooks",
        ):
            (self.home / ext).mkdir(parents=True)
        bindir = self.temp / "bin"
        bindir.mkdir()
        (bindir / "hcom").symlink_to(FAKE_HCOM)
        self.state = self.temp / "hcom-state.json"
        self.store = self.temp / "store"
        self.store.mkdir()
        self.repo = self.temp / "pilot"
        self.repo.mkdir()
        self.env = {
            "HOME": str(self.home),
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "TMPDIR": str(self.temp),
            "FAKE_HCOM_STATE": str(self.state),
            "HCOM_DIR": str(self.store),
            "HCOM_TEAM": "pilot",
            "REGIME_START_WAIT_SECONDS": "4",
            **GIT_IDENTITY,
        }
        self.git("init", "-q")
        self.git("commit", "-q", "--allow-empty", "-m", "init")
        self.conf = self.home / ".local/state/regime-supervisor/pilot.conf"

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
        good = self.conf.read_text()
        for bad in (
            good.replace("hcom_team=pilot", "hcom_team=Bad Team"),
            good + "exec=evil\n",
            good.replace("fails=0", "fails=x"),
        ):
            with self.subTest(bad=bad.splitlines()[-1]):
                self.conf.write_text(bad)
                run = self.run_lever(START, "--supervise", cwd=self.temp)
                self.assertEqual(run.returncode, 0)
                self.assertIn(f"skipped {self.conf}", run.stderr)
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
        conf = dict(
            line.split("=", 1)
            for line in (self.home / ".local/state/regime-supervisor/dotfiles.conf").read_text().splitlines()
        )
        self.assertEqual((conf["hcom_dir"], conf["hcom_team"]), (str(legacy), "regime"))
        self.assertIn("regime-start launched", self.log(legacy))


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


if __name__ == "__main__":
    unittest.main()
