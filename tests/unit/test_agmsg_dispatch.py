"""Exercise dispatch with isolated storage and fake agent CLIs."""

import os
import shutil
import sqlite3
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "home/dot_local/bin/common/executable_agmsg-dispatch"
LIB = ROOT / "home/dot_agents/skills/agmsg/scripts/lib"


class AgmsgDispatchTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        scripts = self.root / ".agents/skills/agmsg/scripts"
        (scripts / "lib").mkdir(parents=True)
        for name in ("storage.sh", "identifier.sh"):
            shutil.copyfile(LIB / name, scripts / "lib" / name)
        self.db = self.root / "alternate/messages.db"
        self.db.parent.mkdir()
        with sqlite3.connect(self.db) as db:
            db.execute("""CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT, team TEXT NOT NULL,
                from_agent TEXT NOT NULL, to_agent TEXT NOT NULL, body TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now')),
                read_at TEXT)""")
        self.calls = self.root / "calls"
        self.calls.write_text("")
        self.write_script(scripts / "send.sh", r"""
source "$(dirname "$0")/lib/storage.sh"
body="${4//\'/\'\'}"
sqlite3 "$(agmsg_db_path)" "INSERT INTO messages(team,from_agent,to_agent,body) VALUES ('$1','$2','$3','$body');"
if [[ ${FAKE_STATUS} == working && ${FAKE_READ} == yes ]]; then
    sqlite3 "$(agmsg_db_path)" "UPDATE messages SET read_at='read';"
fi
""")
        bindir = self.root / "bin"
        bindir.mkdir()
        self.write_script(bindir / "herdr", """
if [[ $1 == pane && $2 == list ]]; then
    pane_status=$FAKE_STATUS
    listed=$(cat "$FAKE_CALLS.list" 2>/dev/null || printf 0)
    printf '%s' "$((listed + 1))" > "$FAKE_CALLS.list"
    if [[ -n ${FAKE_AFTER_STATUS:-} && $listed -gt 0 ]]; then
        pane_status=$FAKE_AFTER_STATUS
    fi
    printf '{"result":{"panes":[{"pane_id":"%s","agent_status":"%s"}]}}\n' "${FAKE_PANE:-w1:p1}" "$pane_status"
else
    printf '%s\n' "$*" >> "$FAKE_CALLS"
    [[ ${FAKE_WAKE_FAIL:-no} != yes ]] || exit 9
    if [[ $FAKE_READ == yes || ${FAKE_WAKE_READ:-no} == yes ]]; then
        sqlite3 "$AGMSG_STORAGE_PATH/messages.db" "UPDATE messages SET read_at='read';"
    fi
fi
""")
        self.env = dict(os.environ, HOME=str(self.root),
                        PATH=f"{bindir}:{os.environ['PATH']}",
                        AGMSG_STORAGE_PATH=str(self.db.parent),
                        AGMSG_DISPATCH_TIMEOUT="1", FAKE_CALLS=str(self.calls),
                        FAKE_STATUS="idle", FAKE_READ="yes")

    def write_script(self, path, body):
        path.write_text("#!/usr/bin/env bash\nset -eu\n" + body)
        path.chmod(0o755)

    def dispatch(self):
        return subprocess.run(
            ["bash", str(SCRIPT), "team", "sender", "worker", "w1:p1",
             "private-message-body"], env=self.env, capture_output=True,
            text=True, timeout=10)

    def test_idle_wakes_once_and_reads(self):
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = self.calls.read_text().splitlines()
        self.assertEqual(len(calls), 1)
        self.assertIn("inbox.sh team worker", calls[0])
        self.assertNotIn("private-message-body", calls[0] + result.stdout + result.stderr)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute("SELECT body FROM messages").fetchone()[0],
                             "private-message-body")

    def test_working_does_not_wake(self):
        self.env["FAKE_STATUS"] = "working"
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls.read_text(), "")

    def test_unread_retries_once_then_fails(self):
        self.env["FAKE_READ"] = "no"
        result = self.dispatch()
        self.assertEqual(result.returncode, 1)
        self.assertIn("unread", result.stderr)
        self.assertEqual(len(self.calls.read_text().splitlines()), 2)
        self.assertNotIn("private-message-body", result.stdout + result.stderr)

    def test_working_unread_never_wakes(self):
        self.env.update(FAKE_STATUS="working", FAKE_READ="no")
        result = self.dispatch()
        self.assertEqual(result.returncode, 1)
        self.assertIn("unread", result.stderr)
        self.assertEqual(self.calls.read_text(), "")

    def test_default_store_uses_shared_helper(self):
        default_db = self.root / ".agents/skills/agmsg/db/messages.db"
        default_db.parent.mkdir()
        shutil.move(self.db, default_db)
        del self.env["AGMSG_STORAGE_PATH"]
        self.env["FAKE_STATUS"] = "working"
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_timeout_does_not_send(self):
        self.env["AGMSG_DISPATCH_TIMEOUT"] = "1+1"
        result = self.dispatch()
        self.assertEqual(result.returncode, 1)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM messages").fetchone()[0], 0)

    def test_worker_becoming_idle_after_send_is_woken(self):
        self.env.update(FAKE_STATUS="working", FAKE_AFTER_STATUS="idle",
                        FAKE_READ="no", FAKE_WAKE_READ="yes")
        result = self.dispatch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.calls.read_text().splitlines()), 1)

    def test_retry_does_not_wake_newly_working_pane(self):
        self.env.update(FAKE_AFTER_STATUS="working", FAKE_READ="no")
        result = self.dispatch()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(self.calls.read_text().splitlines()), 1)

    def test_timeout_is_one_shared_budget(self):
        self.env.update(FAKE_READ="no", AGMSG_DISPATCH_TIMEOUT="2")
        started = time.monotonic()
        result = self.dispatch()
        self.assertEqual(result.returncode, 1)
        self.assertLess(time.monotonic() - started, 3.0)
        self.assertIn("sent message 1;", result.stderr)

    def test_missing_pane_inserts_nothing(self):
        self.env["FAKE_PANE"] = "w1:p9"
        result = self.dispatch()
        self.assertEqual(result.returncode, 1)
        self.assertIn("pane", result.stderr)
        with sqlite3.connect(self.db) as db:
            self.assertEqual(db.execute("SELECT count(*) FROM messages").fetchone()[0], 0)

    def test_wake_failure_identifies_sent_message(self):
        self.env["FAKE_WAKE_FAIL"] = "yes"
        result = self.dispatch()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("sent message 1;", result.stderr)
        self.assertNotIn("private-message-body", result.stderr)


if __name__ == "__main__":
    unittest.main()
