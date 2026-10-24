"""Exercise hcom-reply, the audit seat's one writable route (U6d).

The fake `hcom` under tests/fixtures/hcom/ records every argv and answers `list self name` with `FAKE_HCOM_SELF`, as hcom
resolves `self` from the launch environment of a seat it started; unset, it fails as hcom 0.7.30 does from a plain shell
(`Cannot use 'self' without identity`, measured 2026-10-23).
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPLY = ROOT / "home/dot_local/bin/common/executable_hcom-reply"
FIXTURES = ROOT / "tests/fixtures/hcom"
VERDICT = "VERDICT v1 task_id=U11-audit verdict=correct head=3153f9ce6722b4356d1c2738bf5b9cb4dac9bd64"


class HcomReplyTest(unittest.TestCase):
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
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HCOM_DIR": str(self.store),
            "FAKE_HCOM_CALLS": str(self.calls),
            "FAKE_HCOM_SELF": "audit-tuba",
        }

    def reply(self, *args, **overrides):
        env = {key: value for key, value in {**self.env, **overrides}.items() if value is not None}
        return subprocess.run([str(REPLY), *args], check=False, capture_output=True, text=True, env=env, timeout=60)

    def hcom_calls(self):
        path = self.calls / "argv"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_the_line_is_sent_as_the_launched_identity_and_the_receipt_passes_through(self):
        sent = self.reply("regime", "--", VERDICT)
        self.assertEqual(sent.returncode, 0, sent.stderr)
        self.assertEqual(sent.stdout, '{"delivered_to":[],"event_id":1}\n')
        self.assertEqual(
            self.hcom_calls(),
            [["list", "self", "name"], ["send", "--thread", "regime", "--name", "audit-tuba", "--", VERDICT]],
        )

    def test_words_after_the_separator_are_one_line_and_a_flag_there_is_text(self):
        sent = self.reply("regime", "--", "--name", "soma", "PONG", "v1", "task_id=U11-audit")
        self.assertEqual(sent.returncode, 0, sent.stderr)
        self.assertEqual(
            self.hcom_calls()[-1],
            ["send", "--thread", "regime", "--name", "audit-tuba", "--", "--name soma PONG v1 task_id=U11-audit"],
        )

    def test_no_identity_refuses_before_any_send(self):
        refused = self.reply("regime", "--", VERDICT, FAKE_HCOM_SELF=None)
        self.assertEqual((refused.returncode, refused.stdout), (2, ""))
        self.assertIn("no hcom identity", refused.stderr)
        self.assertEqual(self.hcom_calls(), [["list", "self", "name"]])

    def test_a_caller_chosen_identity_or_a_malformed_call_sends_nothing(self):
        empty = self.root / "empty"
        empty.mkdir()
        for args, overrides, reason in (
            (("regime", "--", VERDICT), {"HCOM_DIR": None}, "HCOM_DIR is unset"),
            (("regime", "--", VERDICT), {"HCOM_DIR": str(empty)}, "store absent"),
            (("Regime", "--", VERDICT), {}, "outside"),
            (("--name", "worker-soma", "regime", "--", VERDICT), {}, "outside"),
            (("regime", "--name", "worker-soma", "--", VERDICT), {}, "must be --"),
            (("regime", "--from", "orch", "--", VERDICT), {}, "must be --"),
            (("regime", "-b", "--", VERDICT), {}, "must be --"),
            (("regime", "x", "--", VERDICT), {}, "must be --"),
            (("regime", VERDICT), {}, "must be --"),
            (("regime", "--"), {}, "empty line"),
            (("regime", "--", ""), {}, "empty line"),
            (("regime",), {}, "usage"),
            ((), {}, "usage"),
        ):
            with self.subTest(args=args, overrides=overrides):
                refused = self.reply(*args, **overrides)
                self.assertEqual((refused.returncode, refused.stdout), (2, ""), refused.stderr)
                self.assertIn(reason, refused.stderr)
        self.assertEqual(self.hcom_calls(), [])


if __name__ == "__main__":
    unittest.main()
