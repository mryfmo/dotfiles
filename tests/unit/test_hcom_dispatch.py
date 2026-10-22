"""Exercise hcom-dispatch, the private hcom install and the fixture world every hcom bus test shares (T129 a02).

HcomWorld is an isolated fixture root populated from the production declarations: a checkout (a `.git` directory,
copies of the bus scripts, a fake hcom bound in `.agents/worklog/uv-tools/hcom/bin/hcom` with its sha256 beside it)
and a directory standing for the passwd home (the source `home/dot_agents/agent-config.yaml` as the deployed
declaration, a `.hcom/hcom.db` whose SQLite header carries user_version 18, a fake mise and herdr). The scripts reach
it only through their explicit `--passwd-home` argument; no environment variable or checkout file redirects them, and
no live store, socket, pane or PR is touched. The fake hcom implements `send` and the reader's fixed SQL templates
only, so any other SQL exits 2, and it logs every call's argv and environment.
"""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEAM, ORCH, WORKER, PANE = "dotfiles-conformance", "claude-deep-dot", "claude-standard-dot-a008", "w5:pA"
SCRIPTS = (
    "scripts/orchestrator/bus-history.sh",
    "scripts/orchestrator/bus-read.sh",
    "scripts/orchestrator/dispatch.sh",
    "scripts/orchestrator/task-consistency-check.py",
    "scripts/regime-counters.sh",
    "home/dot_local/bin/common/executable_hcom-dispatch",
)
READ = (
    "json_array_length(msg_delivered_to) > 0 AND NOT EXISTS (SELECT 1 FROM json_each(msg_delivered_to) d"
    " LEFT JOIN instances i ON i.name = d.value WHERE COALESCE(i.last_event_id, 0) < events_v.id)"
)
FAKE_HCOM = r"""#!/usr/bin/python3 -I
import json, os, re, sys
from datetime import datetime, timezone
CALLS, READ, BASE = {calls!r}, {read!r}, {base!r}
args, home = sys.argv[1:], os.environ.get("HOME", "")
with open(os.path.join(CALLS, "hcom.jsonl"), "a") as f:
    f.write(json.dumps({{"argv": args, "env": dict(os.environ)}}) + "\n")
if not home.startswith(BASE + "/"):  # a home outside the fixture (the passwd home): never read a live store
    sys.exit(9)
path = os.path.join(home, ".hcom", "fake.json")
state = json.load(open(path))
knob = lambda name: os.path.join(CALLS, name)
if args[:1] == ["send"]:
    cut = args.index("--")
    flags, body = args[1:cut], " ".join(args[cut + 1:])
    target = [a for a in flags if a.startswith("@")][0][1:]
    agent = next((a for a in state["agents"] if target in (a["name"], a["tag"] + "-" + a["name"])), None)
    if agent is None:
        sys.exit(f"Error: No active agent for @{{target}}")
    eid = state["next"]
    state["next"] += 1
    data = {{"delivered_to": [agent["name"]], "from": flags[flags.index("--from") + 1], "mentions": [agent["name"]],
            "scope": "mentions", "sender_kind": "external", "text": body}}
    if "--thread" in flags:
        data["thread"] = flags[flags.index("--thread") + 1]
    ts = datetime.now(timezone.utc).isoformat()
    state["events"].append({{"data": data, "id": eid, "instance": "ext_" + data["from"], "ts": ts, "type": "message"}})
    if os.path.exists(knob("auto-read")):
        state["cursors"][agent["name"]] = eid
    json.dump(state, open(path, "w"))
    out = open(knob("send-output")).read() if os.path.exists(knob("send-output")) else None
    print(out if out is not None else json.dumps({{"delivered_to": [agent["name"]], "event_id": eid}}))
    sys.exit(0)
if args[:1] == ["events"]:
    if os.path.exists(knob("events-fails")):
        sys.exit(1)
    last, sql = int(args[args.index("--last") + 1]), args[args.index("--sql") + 1]
    m = re.fullmatch(r"msg_thread = '([a-z0-9-]+)'(?: AND id = ([0-9]+))?(?: AND (.+))?", sql, re.S)
    if not m or (m.group(3) is not None and m.group(3) != READ):
        sys.exit("Error in SQL WHERE clause")
    rows = [e for e in state["events"] if e.get("type") == "message" and e["data"].get("thread") == m.group(1)]
    rows = [e for e in rows if m.group(2) is None or e["id"] == int(m.group(2))]
    if m.group(3):
        cur = state["cursors"]
        rows = [e for e in rows if e["data"]["delivered_to"] and all(cur.get(n, 0) >= e["id"] for n in e["data"]["delivered_to"])]
    for e in sorted(rows, key=lambda e: e["id"])[-last:]:
        print(json.dumps(e))
    sys.exit(0)
sys.exit(3)
"""
FAKE_MISE = '#!/bin/sh\n[ "$1" = which ] || exit 1\nfor p in "$HOME/.local/share/mise/installs/$2/bin/$2"; do [ -f "$p" ] && echo "$p" && exit 0; done\nexit 1\n'
FAKE_HERDR = "#!/usr/bin/python3 -I\nimport json, sys\nopen({log!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"


def header(version=18):
    """The first 100 bytes of a WAL-mode SQLite file at the given user_version."""
    head = bytearray(100)
    head[:16], head[18], head[19] = b"SQLite format 3\0", 2, 2
    head[60:64] = version.to_bytes(4, "big")
    return bytes(head)


class HcomWorld:
    """A fixture checkout and passwd home; see the module docstring."""

    def __init__(self, base, root=None, source=ROOT):
        self.base, self.root, self.home, self.calls = base, root or base / "checkout", base / "home", base / "calls"
        for directory in (self.root / ".git", self.home / ".agents", self.home / ".hcom", self.calls):
            directory.mkdir(parents=True, exist_ok=True)
        for rel in SCRIPTS:
            if (source / rel).exists():
                (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / rel, self.root / rel)
        shutil.copy2(ROOT / "home/dot_agents/agent-config.yaml", self.home / ".agents/agent-config.yaml")
        (self.home / ".hcom/hcom.db").write_bytes(header())
        self.state = {
            "agents": [{"name": WORKER, "tag": TEAM}, {"name": ORCH, "tag": TEAM}],
            "events": [],
            "cursors": {},
        }
        self.state["next"] = 1
        self.save()
        self.entry = self.root / ".agents/worklog/uv-tools/hcom/bin/hcom"
        self.entry.parent.mkdir(parents=True)
        self.entry.write_text(FAKE_HCOM.format(calls=str(self.calls), read=READ, base=str(self.base)))
        self.entry.chmod(0o755)
        self.bind()
        installs = self.home / ".local/share/mise/installs"
        self.tool(self.home / ".local/bin/mise", FAKE_MISE)
        self.tool(installs / "herdr/bin/herdr", FAKE_HERDR.format(log=str(self.calls / "herdr.jsonl")))
        self.cache = base / "uv-cache"
        self.cache.mkdir()

    @staticmethod
    def tool(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(0o755)

    def bind(self):
        """Record the entry's sha256 beside it, as update_hcom_private does."""
        Path(f"{self.entry}.sha256").write_text(hashlib.sha256(self.entry.read_bytes()).hexdigest() + "\n")

    def save(self):
        (self.home / ".hcom/fake.json").write_text(json.dumps(self.state))

    def load(self):
        self.state = json.loads((self.home / ".hcom/fake.json").read_text())
        return self.state

    def message(self, sender, to, body, ts=None, thread=TEAM, **data):
        """Append one message event; ts is a datetime, an ISO string or now."""
        self.load()
        eid = self.state["next"]
        self.state["next"] += 1
        ts = ts or datetime.now(UTC)
        ts = ts if isinstance(ts, str) else ts.isoformat()
        fields = {"delivered_to": [to], "from": sender, "mentions": [to], "scope": "mentions", "text": body}
        fields |= {"thread": thread} if thread else {}
        fields |= data
        self.state["events"].append(
            {"data": fields, "id": eid, "instance": f"ext_{sender}", "ts": ts, "type": "message"}
        )
        self.save()
        return eid

    def read(self, name, upto):
        self.load()
        self.state["cursors"][name] = upto
        self.save()

    def knob(self, name, text=""):
        (self.calls / name).write_text(text)

    def hcom_calls(self, verb=None):
        log = self.calls / "hcom.jsonl"
        calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
        return [c for c in calls if verb is None or c["argv"][:1] == [verb]]

    def herdr_calls(self):
        log = self.calls / "herdr.jsonl"
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    def store_digest(self):
        return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((self.home / ".hcom").iterdir())}

    def env(self, **extra):
        return {"PATH": os.environ["PATH"], "UV_CACHE_DIR": str(self.cache), "TMPDIR": str(self.base), **extra}

    def run(self, rel, *args, env=None, cwd=None, fixture=True, stdin=None):
        """Run a script as production does, /bin/bash -p, with --passwd-home first unless fixture is False. A baseline
        script that takes no --passwd-home (main before T129 a02) runs its own route, bash on PATH with the fixture home
        as HOME, so a red there is that route's behaviour, never a usage error."""
        script = self.root / rel
        baseline = fixture and script.exists() and "--passwd-home" not in script.read_text()
        argv = ["bash", str(script)] if baseline else ["/bin/bash", "--noprofile", "--norc", "-p", str(script)]
        argv += ["--passwd-home", str(self.home)] if fixture and not baseline else []
        env = {**(env if env is not None else self.env()), **({"HOME": str(self.home)} if baseline else {})}
        return subprocess.run(
            [*argv, *map(str, args)],
            capture_output=True,
            text=True,
            input=stdin,
            cwd=cwd or self.root,
            env=env,
            timeout=120,
            check=False,
        )


def world(case, **kwargs):
    temp = tempfile.TemporaryDirectory()
    case.addCleanup(temp.cleanup)
    return HcomWorld(Path(temp.name).resolve(), **kwargs)


class HcomDispatchTest(unittest.TestCase):
    def setUp(self):
        self.w = world(self)

    def send(self, *words, code=0, timeout="2", env=None):
        result = self.w.run(
            "home/dot_local/bin/common/executable_hcom-dispatch",
            TEAM,
            ORCH,
            WORKER,
            PANE,
            *words,
            env=self.w.env(AGMSG_DISPATCH_TIMEOUT=timeout, **(env or {})),
        )
        self.assertEqual(code, result.returncode, result.stderr)
        return result

    def test_transport_matrix(self):
        for name, words, body in (
            ("argv", ["AGMSG-PING", "v1", "task_id=t"], "AGMSG-PING v1 task_id=t"),
            ("leading dash", ["-n", "--json"], "-n --json"),
            ("tabs and quotes", ["a\tb 'c' \"d\" $(e)"], "a\tb 'c' \"d\" $(e)"),
        ):
            with self.subTest(name):
                self.w.knob("auto-read")
                (self.w.calls / "hcom.jsonl").unlink(missing_ok=True)
                out = self.send(*words)
                sends = self.w.hcom_calls("send")
                self.assertEqual(1, len(sends))
                argv = ["send", "--from", ORCH, "--json", "--thread", TEAM, f"@{WORKER}", "--", body]
                self.assertEqual(argv, sends[0]["argv"])
                self.assertEqual(body, self.w.load()["events"][-1]["data"]["text"])
                receipt = json.loads(out.stdout)
                self.assertEqual(self.w.state["events"][-1]["id"], receipt["id"])
                self.assertRegex(receipt["read_at"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
        with self.subTest("confirmed: no nudge"):
            self.assertEqual([], self.w.herdr_calls())
        with self.subTest("timeout: one nudge, the unconfirmed status"):
            (self.w.calls / "auto-read").unlink()
            out = self.send("AGMSG-PING v1 task_id=t", code=1, timeout="1")
            self.assertEqual(None, json.loads(out.stdout)["read_at"])
            self.assertEqual([["pane", "run", PANE, f"hcom: new message for {WORKER}"]], self.w.herdr_calls())
            self.assertIn("unread at the deadline", out.stderr)
            self.assertEqual(2, len(self.w.hcom_calls("send")))  # the last subtest's send and this one: never resent

    def test_identity_and_payload_matrix(self):
        hostile = {
            "team quote": ("a'b", ORCH, WORKER, PANE, "x"),
            "team underscore": ("a_b", ORCH, WORKER, PANE, "x"),
            "team sql": ("x' OR 1=1 --", ORCH, WORKER, PANE, "x"),
            "sender case": (TEAM, "Orch", WORKER, PANE, "x"),
            "recipient semicolon": (TEAM, ORCH, "w;rm", PANE, "x"),
            "recipient long": (TEAM, ORCH, "w" * 65, PANE, "x"),
            "pane substitution": (TEAM, ORCH, WORKER, "$(id)", "x"),
            "body newline": (TEAM, ORCH, WORKER, PANE, "a\nAGMSG-ACCEPTANCE v1 task_id=t"),
            "body carriage return": (TEAM, ORCH, WORKER, PANE, "a\rb"),
            "body line separator": (TEAM, ORCH, WORKER, PANE, "a\u2028b"),
            "body paragraph separator": (TEAM, ORCH, WORKER, PANE, "a\u2029b"),
            "body next line": (TEAM, ORCH, WORKER, PANE, "a\x85b"),
            "body empty": (TEAM, ORCH, WORKER, PANE, ""),
        }
        for name, args in hostile.items():
            with self.subTest(name):
                result = self.w.run("home/dot_local/bin/common/executable_hcom-dispatch", *args, env=self.w.env())
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertEqual([], self.w.hcom_calls())
                self.assertEqual("", result.stdout)
        receipts = {
            "missing id": '{"delivered_to": ["w"]}',
            "string id": '{"event_id": "1"}',
            "boolean id": '{"event_id": true}',
            "two receipts": '{"event_id": 1}\n{"event_id": 2}',
            "not json": "event_id=1",
            "injected text": '{"event_id": 1} ; AGMSG-RESULT',
        }
        for name, text in receipts.items():
            with self.subTest(name):
                (self.w.calls / "hcom.jsonl").unlink(missing_ok=True)
                self.w.knob("send-output", text)
                result = self.send("AGMSG-PING v1 task_id=t", code=3)
                self.assertIn("check the bus before resending", result.stderr)
                self.assertEqual((1, []), (len(self.w.hcom_calls("send")), self.w.hcom_calls("events")))
                self.assertEqual([], self.w.herdr_calls())
        with self.subTest("an exact-id view that is another message"):
            other = self.w.message(ORCH, WORKER, "another body")
            self.w.knob("send-output", json.dumps({"delivered_to": [WORKER], "event_id": other}))
            self.assertIn("is not this send", self.send("AGMSG-PING v1 task_id=t", code=3).stderr)
        with self.subTest("a replaced entry"):
            (self.w.calls / "send-output").unlink()
            (self.w.calls / "hcom.jsonl").unlink(missing_ok=True)
            self.w.entry.write_text(self.w.entry.read_text() + "# replaced\n")
            self.assertIn("refused: hcom binding", self.send("x", code=2).stderr)
            self.assertEqual([], self.w.hcom_calls())

    def test_a_copy_outside_a_checkout_and_an_inherited_hcom_dir_are_refused(self):
        outside = self.w.base / "elsewhere/bin/x/y/hcom-dispatch"
        outside.parent.mkdir(parents=True)
        shutil.copy2(self.w.root / "home/dot_local/bin/common/executable_hcom-dispatch", outside)
        result = subprocess.run(
            ["/bin/bash", "-p", str(outside), TEAM, ORCH, WORKER, PANE, "x"],
            capture_output=True,
            text=True,
            env=self.w.env(),
            check=False,
        )
        self.assertEqual((2, True), (result.returncode, "is not inside one" in result.stderr))
        self.assertIn("inherited HCOM_DIR", self.send("x", code=2, env={"HCOM_DIR": str(self.w.base)}).stderr)
        self.assertIn("UV_CACHE_DIR", self.send("x", code=2, env={"UV_CACHE_DIR": "relative"}).stderr)
        self.assertEqual([], self.w.hcom_calls())


class UpdateHcomPrivateTest(unittest.TestCase):
    WHEEL = "hcom-0.7.30-py3-none-macosx_11_0_arm64.whl"

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.checkout = self.base / "checkout"
        for rel in ("scripts/update-agent-assets.sh", "scripts/lib/asset-manifest.sh", "scripts/lib/installer-pins.sh"):
            (self.checkout / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, self.checkout / rel)
        (self.checkout / "vendor/compactiondb").mkdir(parents=True)
        (self.checkout / ".git").mkdir()
        self.home = self.base / "home"
        self.public = self.home / ".local/bin/hcom"
        HcomWorld.tool(self.public, "#!/bin/sh\necho public\n")
        self.wheel_dir = self.home / ".local/share/agent-assets/hcom"
        self.wheel_dir.mkdir(parents=True)
        # A fake uv: it records UV_TOOL_DIR and UV_TOOL_BIN_DIR and installs a stand-in entry where uv would.
        self.log = self.base / "uv.jsonl"
        HcomWorld.tool(
            self.base / "bin/uv",
            "#!/usr/bin/python3 -I\nimport json, os, sys\n"
            f"open({str(self.log)!r}, 'a').write(json.dumps([sys.argv[1:], os.environ.get('UV_TOOL_DIR'), "
            "os.environ.get('UV_TOOL_BIN_DIR')]) + '\\n')\n"
            "d = os.path.join(os.environ.get('UV_TOOL_DIR', os.path.expanduser('~/.local/share/uv/tools')), 'hcom/bin')\n"
            "os.makedirs(d, exist_ok=True)\nopen(os.path.join(d, 'hcom'), 'w').write('#!/bin/sh\\necho private\\n')\n",
        )

    def update(self, wheel_text, expected):
        (self.wheel_dir / self.WHEEL).write_text(wheel_text)
        script = (
            "source scripts/update-agent-assets.sh && uname() { case $1 in -s) echo Darwin ;; -m) echo arm64 ;; esac; } "
            f"&& HCOM_DARWIN_ARM64_SHA256={expected} && update_hcom_private"
        )
        env = {"PATH": f"{self.base / 'bin'}:/usr/bin:/bin", "HOME": str(self.home)}
        return subprocess.run(
            ["bash", "-c", script], cwd=self.checkout, env=env, capture_output=True, text=True, check=False
        )

    def test_update_hcom_private_installs_the_verified_wheel_into_the_private_tool_dir_leaves_the_public_entry_unchanged_and_refuses_a_drifted_wheel(
        self,
    ):
        public = hashlib.sha256(self.public.read_bytes()).hexdigest()
        tools = self.checkout / ".agents/worklog/uv-tools"
        good = hashlib.sha256(b"wheel\n").hexdigest()
        result = self.update("wheel\n", good)
        self.assertEqual(0, result.returncode, result.stderr + result.stdout)
        argv, tool_dir, bin_dir = json.loads(self.log.read_text().splitlines()[-1])
        self.assertEqual(["tool", "install", "--force", str(self.wheel_dir / self.WHEEL)], argv)
        self.assertEqual((str(tools), str(tools / "bin")), (tool_dir, bin_dir))
        entry = tools / "hcom/bin/hcom"
        self.assertEqual(hashlib.sha256(entry.read_bytes()).hexdigest(), Path(f"{entry}.sha256").read_text().strip())
        self.assertEqual(public, hashlib.sha256(self.public.read_bytes()).hexdigest())
        with self.subTest("a drifted wheel"):
            self.log.unlink()
            result = self.update("drifted wheel\n", good)
            self.assertEqual(1, result.returncode)
            self.assertIn("does not hash to its pin", result.stderr)
            self.assertFalse(self.log.exists())
        with self.subTest("chezmoi's rendered copy installs nothing"):
            script = "source scripts/update-agent-assets.sh && update_hcom_private"
            env = {"PATH": f"{self.base / 'bin'}:/usr/bin:/bin", "HOME": str(self.home)}
            env["DOTFILES_SOURCE_DIR"] = str(self.checkout)
            run = subprocess.run(
                ["bash", "-c", script], cwd=self.checkout, env=env, capture_output=True, text=True, check=False
            )
            self.assertEqual((0, False), (run.returncode, self.log.exists()), run.stderr)
        with self.subTest("a replaced entry is refused by the bus scripts"):
            w = world(self)
            w.entry.write_bytes(w.entry.read_bytes() + b"# replaced\n")
            history = w.run("scripts/orchestrator/bus-history.sh", TEAM)
            self.assertEqual((1, "bus-history: refused: hcom binding\n"), (history.returncode, history.stderr))
            self.assertEqual([], w.hcom_calls())


if __name__ == "__main__":
    unittest.main()
