"""Exercise hcom-dispatch and bus-history.sh.

The fake `hcom` under tests/fixtures/hcom/ speaks the `send --json` and `events` dialect captured from hcom 0.7.30 on
2026-10-23 (events-u5team.jsonl holds three captured rows). When a real `hcom` is on PATH, one test also runs both
scripts against a private store under a scratch HOME (`HCOM_DIR`), never the real store.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DISPATCH = ROOT / "scripts/orchestrator/hcom-dispatch"
HISTORY = ROOT / "scripts/orchestrator/bus-history.sh"
FIXTURES = ROOT / "tests/fixtures/hcom"
RECEIPT = re.compile(r"^id=(\d+) at=(\S+) to=(\S+) kind=(\S+)\n$")
LINE = 'AGMSG-TASK v1 task_id=T1 tab\there quo"te'
ESCAPED_LINE = 'AGMSG-TASK v1 task_id=T1 tab\\there quo"te'


class HcomDispatchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.store = self.root / "hcom"
        self.store.mkdir()
        (self.store / "hcom.db").touch()
        self.calls = self.root / "calls"
        self.calls.mkdir()
        bindir = self.root / "bin"
        bindir.mkdir()
        (bindir / "hcom").symlink_to(FIXTURES / "fake-hcom.py")
        self.env = {
            **os.environ,
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HCOM_DIR": str(self.store),
            # A scratch HOME: an empty HCOM_DIR makes the scripts derive a store under HOME (regime-env, U33).
            "HOME": str(self.root),
            "FAKE_HCOM_CALLS": str(self.calls),
            "FAKE_HCOM_AGENTS": "nemo,bigboss",
        }

    def run_script(self, script, *args, env=None, **overrides):
        return subprocess.run(
            [str(script), *args], capture_output=True, text=True, env={**(env or self.env), **overrides}, timeout=60
        )

    def hcom_calls(self):
        path = self.calls / "argv"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_send_prints_a_receipt_the_history_finds_again(self):
        sent = self.run_script(DISPATCH, "u5team", "orch", "nemo", "w1:p2", LINE)
        self.assertEqual(sent.returncode, 0, sent.stderr)
        receipt = RECEIPT.match(sent.stdout)
        self.assertIsNotNone(receipt, sent.stdout)
        event_id, at, to, kind = receipt.groups()
        self.assertEqual((to, kind), ("nemo", "AGMSG-TASK"))
        self.assertEqual(
            self.hcom_calls(),
            [
                ["send", "@nemo", "--thread", "u5team", "--from", "orch", "--json", "--", LINE],
                ["events", "--type", "message", "--thread", "u5team", "--sql", f"id = {event_id}", "--full"],
            ],
        )
        history = self.run_script(HISTORY, "u5team", "--limit", "10")
        self.assertEqual(history.returncode, 0, history.stderr)
        self.assertEqual(history.stdout, f"{event_id}\t{at}\torch\tnemo\tAGMSG-TASK\t{ESCAPED_LINE}\n")

    def test_words_are_joined_and_a_leading_dash_reaches_hcom_unparsed(self):
        sent = self.run_script(DISPATCH, "u5team", "orch", "nemo", "w1:p2", "-x", "AGMSG-PING", "v1", "task_id=T1")
        self.assertEqual(sent.returncode, 0, sent.stderr)
        self.assertEqual(self.hcom_calls()[0][-2:], ["--", "-x AGMSG-PING v1 task_id=T1"])
        self.assertTrue(sent.stdout.endswith(" to=nemo kind=-x\n"), sent.stdout)

    def test_an_unknown_seat_is_refused_by_hcom_and_nothing_is_read(self):
        sent = self.run_script(DISPATCH, "u5team", "orch", "nemo", "w1:p2", LINE, FAKE_HCOM_AGENTS="bigboss")
        self.assertEqual((sent.returncode, sent.stdout), (1, ""))
        self.assertIn("Error: No active agent for @nemo", sent.stderr)
        self.assertEqual(len(self.hcom_calls()), 1)

    def test_malformed_identifiers_and_an_empty_line_send_nothing(self):
        for argv in (
            ["Team", "orch", "nemo", "w1:p2", LINE],
            ["u5team", "-orch", "nemo", "w1:p2", LINE],
            ["u5team", "orch", "nemo/x", "w1:p2", LINE],
            ["u5team", "orch", "nemo", "w1:p2", ""],
            ["u5team", "orch", "nemo", "w1:p2"],
        ):
            with self.subTest(argv=argv):
                sent = self.run_script(DISPATCH, *argv)
                self.assertEqual((sent.returncode, sent.stdout), (1, ""), sent.stderr)
        self.assertEqual(self.hcom_calls(), [])

    def test_an_absent_store_refuses_both_scripts_before_any_hcom_call(self):
        empty = self.root / "empty"
        empty.mkdir()
        for store in (str(empty), ""):
            for script, args in ((DISPATCH, ("u5team", "orch", "nemo", "w1:p2", LINE)), (HISTORY, ("u5team",))):
                with self.subTest(script=script.name, store=store):
                    run = self.run_script(script, *args, HCOM_DIR=store)
                    self.assertEqual((run.returncode, run.stdout), (1, ""))
                    # An empty HCOM_DIR derives this checkout's store, unbound here, so the binding refusal comes first.
                    self.assertRegex(run.stderr, "store absent" if store else "has no origin file binding it")
        self.assertEqual(self.hcom_calls(), [])

    def test_a_sent_id_the_bus_does_not_hold_is_refused(self):
        sent = self.run_script(DISPATCH, "u5team", "orch", "nemo", "w1:p2", LINE, FAKE_HCOM_HIDE_EVENTS="1")
        self.assertEqual((sent.returncode, sent.stdout), (1, ""))
        self.assertIn("was not found in thread u5team", sent.stderr)

    def test_history_prints_the_captured_rows_as_escaped_tsv_in_id_order(self):
        shutil.copy(FIXTURES / "events-u5team.jsonl", self.store / "events.jsonl")
        history = self.run_script(HISTORY, "u5team")
        self.assertEqual(history.returncode, 0, history.stderr)
        self.assertEqual(
            history.stdout.splitlines(),
            [
                "3\t2026-10-23T01:20:24.911135+00:00\tu5team-orch\tnemo\tAGMSG-TASK\t"
                'AGMSG-TASK v1 task_id=t1 tab\\tin quo"te',
                "4\t2026-10-23T01:20:24.968790+00:00\tu5team-aud\tnemo\tAGMSG-PING\tAGMSG-PING v1 task_id=t1",
                "6\t2026-10-23T01:20:25.025634+00:00\tnemo\t-\tAGMSG-RESULT\tAGMSG-RESULT v1 task_id=t1 status=done",
            ],
        )
        self.assertEqual(
            self.hcom_calls(), [["events", "--type", "message", "--thread", "u5team", "--full", "--last", "200"]]
        )

    def test_history_filters_by_kind_limit_and_since_and_refuses_bad_options(self):
        shutil.copy(FIXTURES / "events-u5team.jsonl", self.store / "events.jsonl")
        since = "2026-10-23T01:20:24"
        by_kind = self.run_script(HISTORY, "u5team", "--kind", "AGMSG-PING", "--limit", "2", "--since", since)
        self.assertEqual(by_kind.returncode, 0, by_kind.stderr)
        self.assertEqual([row.split("\t")[0] for row in by_kind.stdout.splitlines()], ["4"])
        self.assertEqual(self.hcom_calls()[-1][-4:], ["--last", "2", "--after", since])
        for args in (("u5team", "--limit", "0"), ("u5team", "--limit"), ("u5team", "--bogus", "1"), ("Team",), ()):
            with self.subTest(args=args):
                run = self.run_script(HISTORY, *args)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(len(self.hcom_calls()), 1)

    @unittest.skipUnless(shutil.which("hcom"), "a real hcom is not on PATH")
    def test_a_real_hcom_round_trip_stays_inside_a_private_store(self):
        store, home = self.root / "real-hcom", self.root / "home"
        home.mkdir()
        env = {"PATH": os.environ["PATH"], "HOME": str(home), "HCOM_DIR": str(store), "TMPDIR": self.temp.name}

        def hcom(*args):
            return subprocess.run(["hcom", *args], capture_output=True, text=True, env=env, cwd=self.root, timeout=20)

        started = hcom("start")
        self.assertEqual(started.returncode, 0, started.stderr)
        seat = re.search(r"\[hcom:([^\]]+)\]", started.stdout).group(1)
        self.assertTrue((store / "hcom.db").is_file())
        sent = self.run_script(DISPATCH, "u5team", "orch", seat, "w1:p2", LINE, env=env)
        self.assertEqual(sent.returncode, 0, sent.stderr)
        event_id, at, to, kind = RECEIPT.match(sent.stdout).groups()
        self.assertEqual((to, kind), (seat, "AGMSG-TASK"))
        reply = hcom(
            "send", "--name", seat, "--thread", "u5team", "--json", "--", "AGMSG-RESULT v1 task_id=T1 status=done"
        )
        self.assertEqual(reply.returncode, 0, reply.stderr)
        history = self.run_script(HISTORY, "u5team", "--limit", "10", env=env)
        self.assertEqual(history.returncode, 0, history.stderr)
        rows = [row.split("\t") for row in history.stdout.splitlines()]
        self.assertEqual(rows[0], [event_id, at, "orch", seat, "AGMSG-TASK", ESCAPED_LINE])
        self.assertEqual(rows[1][2:], [seat, "-", "AGMSG-RESULT", "AGMSG-RESULT v1 task_id=T1 status=done"])
        self.assertEqual(len(rows), 2)
        refused = self.run_script(DISPATCH, "u5team", "orch", "nobody", "w1:p2", LINE, env=env)
        self.assertEqual((refused.returncode, refused.stdout), (1, ""))
        self.assertIn("No active agent for @nobody", refused.stderr)
        self.assertFalse((home / ".hcom").exists())


if __name__ == "__main__":
    unittest.main()
