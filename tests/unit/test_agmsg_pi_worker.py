"""Unit tests for the Pi RPC to agmsg bridge."""

from __future__ import annotations

import json
import os
import selectors
import shutil
import sqlite3
import subprocess
import tempfile
import textwrap
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / "home/dot_local/bin/common/executable_agmsg-pi-worker"
JOIN = ROOT / "home/dot_agents/skills/agmsg/scripts/executable_join.sh"
CHECK_INBOX = ROOT / "home/dot_agents/skills/agmsg/scripts/executable_check-inbox.sh"
WHOAMI = ROOT / "home/dot_agents/skills/agmsg/scripts/executable_whoami.sh"
IDENTITIES = ROOT / "home/dot_agents/skills/agmsg/scripts/executable_identities.sh"
CONFIG = ROOT / "home/dot_agents/skills/agmsg/scripts/executable_config.sh"
STORAGE = ROOT / "home/dot_agents/skills/agmsg/scripts/lib/storage.sh"
ACTAS_LOCK = ROOT / "home/dot_agents/skills/agmsg/scripts/lib/actas-lock.sh"

TEAM = "bridge-team"
IDENTITY = "pi-standard-project"
FIXED_INSTRUCTION = (
    "Execute per the task file; send your AGMSG-RESULT using the agmsg_send "
    "tool; your final assistant text is not the RESULT."
)


FAKE_PI = r"""#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

Path(os.environ["FAKE_PI_START_LOG"]).write_text(json.dumps({
    "args": sys.argv[1:],
    "cwd": os.getcwd(),
    "identity": os.environ.get("AGMSG_PI_IDENTITY"),
}), encoding="utf-8")

scenario = os.environ.get("FAKE_PI_SCENARIO", "happy")
if scenario == "die-immediately":
    raise SystemExit(17)

for line in sys.stdin:
    request = json.loads(line)
    with open(os.environ["FAKE_PI_REQUEST_LOG"], "a", encoding="utf-8") as log:
        log.write(json.dumps(request) + "\n")
    if scenario == "die-on-prompt":
        raise SystemExit(18)
    print(json.dumps({
        "id": request.get("id"),
        "type": "response",
        "command": "prompt",
        "success": True,
    }), flush=True)
    for event in (
        {"type": "agent_start"},
        {"type": "message_start", "message": {"role": "assistant", "content": []}},
        {"type": "message_end", "message": {"role": "assistant", "content": []}},
        {"type": "agent_end", "messages": []},
        {"type": "agent_settled"},
    ):
        print(json.dumps(event), flush=True)
"""


FAKE_IDENTITIES = r"""#!/usr/bin/env python3
import os
from pathlib import Path

registrations = Path(os.environ["FAKE_REGISTRATIONS"])
if registrations.exists():
    print(registrations.read_text(encoding="utf-8"), end="")
"""


FAKE_JOIN = r"""#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

with open(os.environ["FAKE_JOIN_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\n")
Path(os.environ["FAKE_REGISTRATIONS"]).write_text(
    f"{sys.argv[1]}\t{sys.argv[2]}\n",
    encoding="utf-8",
)
"""


FAKE_CHECK_INBOX = r"""#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

with open(os.environ["FAKE_CHECK_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps({
        "args": sys.argv[1:],
        "active": os.environ.get("AGMSG_ACTIVE_NAME"),
        "team": os.environ.get("AGMSG_TEAM_FILTER"),
        "force": os.environ.get("AGMSG_CHECK_INBOX_FORCE"),
    }) + "\n")
response = Path(os.environ["FAKE_INBOX_RESPONSE"])
if response.exists():
    value = response.read_text(encoding="utf-8")
    response.write_text("", encoding="utf-8")
    print(value, end="")
"""


FAKE_SEND = r"""#!/usr/bin/env python3
import json
import os
import sys

with open(os.environ["FAKE_SEND_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\n")
"""


class AgmsgPiWorkerTest(unittest.TestCase):
    """Exercise the bridge against fake agmsg scripts and a fake Pi RPC child."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.scratch = self.root / "scratch"
        self.project = self.scratch / "project"
        self.project.mkdir(parents=True)
        self.outside = self.root / "outside"
        self.outside.mkdir()

        self.home = self.root / "home"
        self.scripts = self.home / ".agents/skills/agmsg/scripts"
        self.scripts.mkdir(parents=True)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        extension = self.home / ".pi/agent/extensions/permgate.ts"
        extension.parent.mkdir(parents=True)
        extension.write_text("export default function () {}\n", encoding="utf-8")
        (extension.parent / "agmsg.ts").write_text(
            "export default function () {}\n", encoding="utf-8"
        )

        self.registrations = self.root / "registrations.tsv"
        self.join_log = self.root / "join.jsonl"
        self.check_log = self.root / "check.jsonl"
        self.send_log = self.root / "send.jsonl"
        self.inbox_response = self.root / "inbox.json"
        self.pi_start_log = self.root / "pi-start.json"
        self.pi_request_log = self.root / "pi-requests.jsonl"

        self.write_executable(self.scripts / "identities.sh", FAKE_IDENTITIES)
        self.write_executable(self.scripts / "join.sh", FAKE_JOIN)
        self.write_executable(self.scripts / "check-inbox.sh", FAKE_CHECK_INBOX)
        self.write_executable(self.scripts / "send.sh", FAKE_SEND)
        self.write_executable(self.bin_dir / "pi", FAKE_PI)

        self.env = os.environ.copy()
        self.env.update(
            {
                "HOME": str(self.home),
                "PATH": f"{self.bin_dir}:{os.environ['PATH']}",
                "FAKE_REGISTRATIONS": str(self.registrations),
                "FAKE_JOIN_LOG": str(self.join_log),
                "FAKE_CHECK_LOG": str(self.check_log),
                "FAKE_SEND_LOG": str(self.send_log),
                "FAKE_INBOX_RESPONSE": str(self.inbox_response),
                "FAKE_PI_START_LOG": str(self.pi_start_log),
                "FAKE_PI_REQUEST_LOG": str(self.pi_request_log),
            }
        )

    @staticmethod
    def write_executable(path: Path, content: str) -> None:
        path.write_text(textwrap.dedent(content), encoding="utf-8")
        path.chmod(0o755)

    def bridge_command(self, project: Path | None = None) -> list[str]:
        return [
            "bash",
            str(BRIDGE),
            "--team",
            TEAM,
            "--identity",
            IDENTITY,
            "--project",
            str(project or self.project),
            "--provider",
            "openai-codex",
            "--model",
            "test-model",
            "--scratch-root",
            str(self.scratch),
        ]

    def queue_message(self, sender: str, body: str) -> None:
        reason = f"1 new message(s) in {TEAM}:\n  [2026-08-17T00:00:00Z] {sender}: {body}\n"
        self.inbox_response.write_text(
            json.dumps({"decision": "block", "reason": reason}),
            encoding="utf-8",
        )

    def start_bridge(
        self,
        *,
        scenario: str = "happy",
    ) -> subprocess.Popen[str]:
        env = self.env | {"FAKE_PI_SCENARIO": scenario}
        process = subprocess.Popen(
            self.bridge_command(),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.addCleanup(self.stop_process, process)
        return process

    @staticmethod
    def stop_process(process: subprocess.Popen[str]) -> None:
        if process.poll() is not None:
            process.communicate(timeout=2)
            return
        process.terminate()
        try:
            process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=2)

    def wait_for_stderr(self, process: subprocess.Popen[str], marker: str) -> str:
        assert process.stderr is not None
        selector = selectors.DefaultSelector()
        selector.register(process.stderr, selectors.EVENT_READ)
        deadline = time.monotonic() + 4
        lines: list[str] = []
        while time.monotonic() < deadline:
            events = selector.select(deadline - time.monotonic())
            if not events:
                break
            line = process.stderr.readline()
            if not line:
                break
            lines.append(line)
            if marker in line:
                return "".join(lines)
        self.fail(
            f"missing stderr marker {marker!r}; returncode={process.poll()}; "
            f"stderr={''.join(lines)!r}"
        )

    @staticmethod
    def read_json_lines(path: Path) -> list[object]:
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_refuses_project_outside_explicit_scratch_root(self) -> None:
        result = subprocess.run(
            self.bridge_command(self.outside),
            env=self.env,
            text=True,
            capture_output=True,
            check=False,
            timeout=4,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside scratch root", result.stderr)
        self.assertFalse(self.pi_start_log.exists())

    def test_task_becomes_correlated_prompt_and_completes_on_agent_end(self) -> None:
        task = "AGMSG-TASK v1 task_id=T99 task_file=.orchestration/tasks/T99.md"
        self.queue_message("orchestrator", task)

        process = self.start_bridge()
        log = self.wait_for_stderr(process, "turn-complete corr=t68-1 task_id=T99")

        self.assertIn("rpc-response corr=t68-1 success=true", log)
        request = self.read_json_lines(self.pi_request_log)[0]
        self.assertEqual(request["id"], "t68-1")
        self.assertEqual(request["type"], "prompt")
        self.assertEqual(request["message"], f"{task}\n{FIXED_INSTRUCTION}")
        start = json.loads(self.pi_start_log.read_text(encoding="utf-8"))
        self.assertEqual(Path(start["cwd"]), self.project.resolve())
        self.assertEqual(
            start["args"],
            [
                "--mode",
                "rpc",
                "--provider",
                "openai-codex",
                "--model",
                "test-model",
                "--extension",
                str(self.home / ".pi/agent/extensions/permgate.ts"),
                "--extension",
                str(self.home / ".pi/agent/extensions/agmsg.ts"),
            ],
        )
        self.assertEqual(start["identity"], IDENTITY)
        self.assertEqual(
            self.read_json_lines(self.join_log),
            [[TEAM, IDENTITY, "pi", str(self.project.resolve())]],
        )
        check = self.read_json_lines(self.check_log)[0]
        self.assertEqual(check["args"], ["pi", str(self.project.resolve())])
        self.assertEqual(check["active"], IDENTITY)
        self.assertEqual(check["team"], TEAM)
        self.assertEqual(check["force"], "1")

    def test_agent_settled_after_agent_end_is_tolerated(self) -> None:
        self.queue_message("orchestrator", "AGMSG-TASK v1 task_id=T100 task_file=T100.md")

        process = self.start_bridge()
        self.wait_for_stderr(process, "turn-complete corr=t68-1 task_id=T100")
        self.wait_for_stderr(process, "rpc-event kind=agent_settled")

        self.assertIsNone(process.poll())

    def test_child_death_sends_blocked_pong_and_exits_nonzero(self) -> None:
        self.queue_message("orchestrator", "AGMSG-TASK v1 task_id=T101 task_file=T101.md")

        process = self.start_bridge(scenario="die-on-prompt")
        _stdout, stderr = process.communicate(timeout=4)

        self.assertNotEqual(process.returncode, 0)
        self.assertIn("bridge-child-died", stderr)
        sent = self.read_json_lines(self.send_log)
        self.assertEqual(sent[0][:3], [TEAM, IDENTITY, "orchestrator"])
        self.assertEqual(
            sent[0][3],
            "AGMSG-PONG v1 task_id=T101 status=blocked note=bridge-child-died",
        )

    def test_ping_sends_bridge_level_alive_pong(self) -> None:
        self.queue_message("orchestrator", "AGMSG-PING v1 task_id=T102 reason=status")

        process = self.start_bridge()
        self.wait_for_stderr(process, "bus-pong status=alive task_id=T102")

        sent = self.read_json_lines(self.send_log)
        self.assertEqual(
            sent,
            [[
                TEAM,
                IDENTITY,
                "orchestrator",
                "AGMSG-PONG v1 task_id=T102 status=alive note=bridge-alive",
            ]],
        )
        self.assertEqual(self.read_json_lines(self.pi_request_log), [])

    def test_fixed_instruction_is_appended_exactly_once(self) -> None:
        task = "AGMSG-TASK v1 task_id=T103 task_file=T103.md"
        self.queue_message("orchestrator", task)

        process = self.start_bridge()
        self.wait_for_stderr(process, "turn-complete corr=t68-1 task_id=T103")

        message = self.read_json_lines(self.pi_request_log)[0]["message"]
        self.assertEqual(message.count(FIXED_INSTRUCTION), 1)
        self.assertTrue(message.endswith(f"\n{FIXED_INSTRUCTION}"))

    def test_bridge_never_sends_agmsg_result(self) -> None:
        self.queue_message("orchestrator", "AGMSG-TASK v1 task_id=T104 task_file=T104.md")

        process = self.start_bridge()
        self.wait_for_stderr(process, "turn-complete corr=t68-1 task_id=T104")

        sent = self.read_json_lines(self.send_log)
        self.assertFalse(any(record[3].startswith("AGMSG-RESULT") for record in sent))

    def test_join_accepts_pi_runtime_type(self) -> None:
        skill = self.root / "join-skill"
        scripts = skill / "scripts"
        scripts.mkdir(parents=True)
        join = scripts / "join.sh"
        shutil.copy2(JOIN, join)

        result = subprocess.run(
            ["bash", str(join), TEAM, IDENTITY, "pi", str(self.project)],
            text=True,
            capture_output=True,
            check=False,
            timeout=4,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        config = json.loads((skill / f"teams/{TEAM}/config.json").read_text(encoding="utf-8"))
        self.assertEqual(
            config["agents"][IDENTITY]["registrations"],
            [{"type": "pi", "project": str(self.project)}],
        )

        rejected = subprocess.run(
            ["bash", str(join), TEAM, "unknown-worker", "unknown", str(self.project)],
            text=True,
            capture_output=True,
            check=False,
            timeout=4,
        )
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("Unknown agent type", rejected.stderr)

    def test_check_inbox_bridge_controls_force_and_narrow_delivery(self) -> None:
        skill = self.root / "inbox-skill"
        scripts = skill / "scripts"
        lib = scripts / "lib"
        lib.mkdir(parents=True)
        for source, destination in (
            (CHECK_INBOX, scripts / "check-inbox.sh"),
            (WHOAMI, scripts / "whoami.sh"),
            (IDENTITIES, scripts / "identities.sh"),
            (CONFIG, scripts / "config.sh"),
            (STORAGE, lib / "storage.sh"),
            (ACTAS_LOCK, lib / "actas-lock.sh"),
        ):
            shutil.copy2(source, destination)

        other_identity = "pi-other-project"
        other_team = "other-team"
        for team, agents in (
            (TEAM, [other_identity, IDENTITY]),
            (other_team, [IDENTITY]),
        ):
            team_dir = skill / "teams" / team
            team_dir.mkdir(parents=True)
            config = {
                "name": team,
                "agents": {
                    agent: {"registrations": [{"type": "pi", "project": str(self.project)}]}
                    for agent in agents
                },
            }
            (team_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")

        store = self.root / "inbox-store"
        store.mkdir()
        db = sqlite3.connect(store / "messages.db")
        db.execute(
            "CREATE TABLE messages (id INTEGER PRIMARY KEY, team TEXT, from_agent TEXT, "
            "to_agent TEXT, body TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, read_at TEXT)"
        )
        for team, target, body in (
            (TEAM, IDENTITY, "AGMSG-TASK v1 task_id=SELECTED"),
            (TEAM, other_identity, "AGMSG-TASK v1 task_id=OTHER_IDENTITY"),
            (other_team, IDENTITY, "AGMSG-TASK v1 task_id=OTHER_TEAM"),
        ):
            db.execute(
                "INSERT INTO messages (team, from_agent, to_agent, body) VALUES (?, ?, ?, ?)",
                (team, "orchestrator", target, body),
            )
        db.commit()
        db.close()

        run_dir = skill / "run"
        run_dir.mkdir()
        (run_dir / f".lastcheck-{IDENTITY}").touch()
        env = os.environ | {
            "AGMSG_STORAGE_PATH": str(store),
            "AGMSG_ACTIVE_NAME": IDENTITY,
            "AGMSG_TEAM_FILTER": TEAM,
            "AGMSG_CHECK_INBOX_FORCE": "1",
        }

        result = subprocess.run(
            ["bash", str(scripts / "check-inbox.sh"), "pi", str(self.project)],
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=4,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("task_id=SELECTED", result.stdout)
        self.assertNotIn("OTHER_IDENTITY", result.stdout)
        self.assertNotIn("OTHER_TEAM", result.stdout)
        db = sqlite3.connect(store / "messages.db")
        states = dict(db.execute("SELECT body, read_at FROM messages"))
        db.close()
        self.assertIsNotNone(states["AGMSG-TASK v1 task_id=SELECTED"])
        self.assertIsNone(states["AGMSG-TASK v1 task_id=OTHER_IDENTITY"])
        self.assertIsNone(states["AGMSG-TASK v1 task_id=OTHER_TEAM"])


if __name__ == "__main__":
    unittest.main()
