"""Exercise scripts/orchestrator/{dispatch,three-repeat,bus-read}.sh with stubbed host binaries.

Each script runs as a subprocess in a temporary git repository, with `agmsg-dispatch`, `shasum` and
`uv` stubbed on PATH and `history.sh` stubbed in the directory `AGMSG_SCRIPTS` names; every stub
records its argv NUL-separated, so an argument is compared byte for byte.
"""

import hashlib
import os
import re
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "scripts/orchestrator"
RECORD = 'printf \'%s\\0\' "$@" > "$CALLS/{name}"\n'
STUBS = {
    "agmsg-dispatch": "#!/usr/bin/env bash\n" + RECORD.format(name="agmsg-dispatch"),
    "shasum": '#!/usr/bin/env python3\nimport hashlib, sys\np = sys.argv[-1]\nprint(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + p)\n',
    "uv": "#!/usr/bin/env bash\n" + RECORD.format(name="uv") + 'cat "$CALLS/uv-output"\n',
}
HISTORY_SH = "#!/usr/bin/env bash\n" + RECORD.format(name="history.sh") + 'cat "$CALLS/history"\n'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class OrchestratorToolsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.repo = self.temp / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        bin_dir, agmsg = self.temp / "bin", self.temp / "agmsg"
        for directory, stubs in ((bin_dir, STUBS), (agmsg, {"history.sh": HISTORY_SH})):
            directory.mkdir()
            for name, text in stubs.items():
                (directory / name).write_text(text)
                (directory / name).chmod(0o755)
        self.env = {
            **os.environ,
            "CALLS": str(self.calls),
            "AGMSG_SCRIPTS": str(agmsg),
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        }

    def run_tool(self, name, *args, code=0, env=None):
        result = subprocess.run(
            ["bash", str(TOOLS / name), *args],
            capture_output=True,
            text=True,
            cwd=self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def call(self, name):
        path = self.calls / name
        return path.read_text().split("\0")[:-1] if path.exists() else None

    def write(self, rel, text):
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    # dispatch.sh

    def dispatch(self, line, code=0):
        self.write("line.txt", line + "\n")
        return self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", code=code)

    def test_dispatch_refuses_a_line_whose_sha256_field_does_not_match_its_file(self):
        self.write(".orchestration/tasks/t.md", "task\n")
        line = f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_sha256={sha('other')}"
        result = self.dispatch(line, code=1)
        self.assertIn("task_sha256 mismatch", result.stderr)
        self.assertIsNone(self.call("agmsg-dispatch"))

    def test_dispatch_passes_the_line_byte_identical(self):
        self.write(".orchestration/tasks/t.md", "task\n")
        self.write("design.md", "design\n")
        line = (
            f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_sha256={sha('task' + chr(10))}"
            f" design=design.md design_sha256={sha('design' + chr(10))} note=a;b(c)`d`$(e)"
        )
        self.dispatch(line)
        self.assertEqual(["team", "orch", "worker", "w5:pA", line], self.call("agmsg-dispatch"))

    def test_dispatch_refuses_malformed_lines(self):
        for line, code, needle in (
            ("AGMSG-TASK v1 task_id=t\nAGMSG-TASK v1 task_id=u", 2, "more than one line"),
            ("hello task_id=t", 2, "not an AGMSG-TASK"),
            (f"AGMSG-TASK v1 task_id=t amended_task_sha256={sha('x')}", 1, "amended_task_sha256 has no"),
            ("AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_sha256=abc", 1, "not 64 lowercase hex"),
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.dispatch(line, code=code).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))

    # three-repeat.sh

    def test_three_repeat_refuses_a_class_that_is_not_a_slug(self):
        for value in ("Reject skipped contract", "a;b"):
            with self.subTest(value=value):
                self.assertIn("usage", self.run_tool("three-repeat.sh", value, code=2).stderr)
        self.assertIsNone(self.call("uv"))

    def test_three_repeat_prints_the_records_search_line(self):
        mistakes = ".orchestration/learning/mistakes"
        self.write(f"{mistakes}/M-20261012-4.md", "id: M-20261012-4\nclasses: [bookkeeping]\n")
        self.write(f"{mistakes}/M-20261012-2.md", "id: M-20261012-2\nclasses: [sources, bookkeeping]\n")
        # The gate's match: a line that begins with `classes:`, so neither a later mention nor a prose one counts.
        self.write(
            f"{mistakes}/M-20261011-1.md", "id: M-20261011-1\nclasses: [sources]\nnote: old classes: bookkeeping\n"
        )
        (self.calls / "uv-output").write_text("0f1e2d3c-aaaa-bbbb x\n1a2b3c4d-cccc-dddd y\n")
        out = self.run_tool("three-repeat.sh", "bookkeeping").stdout.splitlines()
        self.assertEqual(
            ["search: bookkeeping -> M-20261012-2.md, M-20261012-4.md", "compactiondb: bookkeeping -> 2 matches"], out
        )
        self.assertEqual(
            ["run", "--no-project", ".claude/hooks/contextdb_cli.py", "memory", "search", "bookkeeping"],
            self.call("uv"),
        )
        (self.calls / "uv-output").write_text("No matches.\n")
        self.assertEqual(
            ["search: absent -> none", "compactiondb: absent -> 0 matches"],
            self.run_tool("three-repeat.sh", "absent").stdout.splitlines(),
        )

    # bus-read.sh

    def history(self, *messages):
        """history.sh rows from (minutes ago, from, to, body)."""
        now = datetime.now(UTC)
        rows = ["agmsg: a line that is not a message"]
        for ago, sender, to, body in messages:
            at = (now - timedelta(minutes=ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append(f"  ○ [{at}] {sender} → {to}: {body}")
        (self.calls / "history").write_text("\n".join(rows) + "\n")

    def test_bus_read_lists_open_tasks_with_their_minutes_since_the_latest_event(self):
        self.history(
            (60, "orch", "w1", "AGMSG-TASK v1 task_id=T1"),
            (45, "w1", "orch", "AGMSG-PONG v1 task_id=T1 status=alive"),
            (50, "orch", "w2", "AGMSG-TASK v1 task_id=T2"),
            (40, "w2", "orch", "AGMSG-RESULT v1 task_id=T2 status=ready_for_review"),
            (30, "orch", "w3", "AGMSG-TASK v1 task_id=T3"),
            (20, "w3", "orch", "AGMSG-RESULT v1 task_id=T3 status=ready_for_review"),
            (10, "orch", "w3", "AGMSG-ACCEPTANCE v1 task_id=T3 status=revise"),
            (9, "orch", "w4", "AGMSG-TASK v1 task_id=T4"),
            (8, "orch", "w4", "AGMSG-ACCEPTANCE v1 task_id=T4 status=withdrawn"),
            (7, "orch", "w2", "AGMSG-ACCEPTANCE v1 task_id=T2 status=under_review"),
        )
        lines = self.run_tool("bus-read.sh", "team").stdout.splitlines()
        self.assertEqual(["T1", "T3"], [re.search(r"task=(\S+)", line).group(1) for line in lines])
        fields = [dict(re.findall(r"(\w+)=(\S+)", line)) for line in lines]
        self.assertEqual(["w1", "w3"], [f["seat"] for f in fields])
        self.assertEqual(["yes", "no"], [f["silent"] for f in fields])
        for f, minutes in zip(fields, (45, 10), strict=True):
            self.assertLessEqual(abs(int(f["minutes"]) - minutes), 1, f)
        self.assertEqual(["team", "", "100000"], self.call("history.sh"))
        only = self.run_tool("bus-read.sh", "team", "T3").stdout.splitlines()
        self.assertEqual(1, len(only))
        self.assertIn("task=T3 ", only[0])
        self.assertEqual(["open: none"], self.run_tool("bus-read.sh", "team", "T2").stdout.splitlines())

    def test_bus_read_refuses_a_read_that_reaches_its_limit(self):
        self.history(*[(i, "orch", "w1", f"AGMSG-TASK v1 task_id=T{i}") for i in range(3)])
        result = self.run_tool("bus-read.sh", "team", code=1, env={"BUS_READ_LIMIT": "3"})
        self.assertIn("reached its limit of 3 rows", result.stderr)


if __name__ == "__main__":
    unittest.main()
