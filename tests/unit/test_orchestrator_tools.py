"""Exercise the scripts under scripts/orchestrator/ with stubbed host binaries.

Each script runs as a subprocess from its copy in a temporary git repository, with `agmsg-dispatch`, `shasum`,
`uv`, `gh`, `make`, `codex` and an interpreter `gate-python` stubbed on PATH and `history.sh` stubbed in the directory `AGMSG_SCRIPTS` names;
git is the real one, against a bare repository standing in for `origin`. A stub records its argv NUL-separated,
so an argument is compared byte for byte (`gh` and `make` append one line per call).
The dispatch checker case alone replaces the `uv` stub with a logging wrapper around the real `uv` next on PATH, so
the module needs a real uv with PyYAML in its cache or reachable index for that case.
"""

import fcntl
import hashlib
import importlib.util
import json
import os
import pwd
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from tests.unit.test_pr_feedback import GhFixture

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "scripts/orchestrator"
RECORD = 'printf \'%s\\0\' "$@" > "$CALLS/{name}"\n'
# A run records its argv, cwd and environment, prints {name}-output and fails while {name}-fails exists.
RUN = RECORD + 'pwd -P > "$CALLS/{name}-cwd"\n/usr/bin/env > "$CALLS/{name}-env"\n'
RUN += '/bin/cat "$CALLS/{name}-output" 2> /dev/null\n[[ ! -f "$CALLS/{name}-fails" ]] || exit 2\n'
STUBS = {
    "agmsg-dispatch": "#!/usr/bin/env bash\n"
    + RECORD.format(name="agmsg-dispatch")
    # A send puts its row on the stub bus with the marker in dispatch-marker; dispatch-fails sends nothing.
    + '[[ -f "$CALLS/dispatch-fails" ]] && exit 1\n'
    + '[[ -f "$CALLS/dispatch-marker" ]] && printf "  %s [2026-10-13T03:00:00Z] %s → %s: %s\\n" '
    + '"$(cat "$CALLS/dispatch-marker")" "$2" "$3" "$5" >> "$CALLS/history"\nexit 0\n',
    "shasum": '#!/usr/bin/env python3\nimport hashlib, sys\np = sys.argv[-1]\nprint(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + p)\n',
    # As uv does, a .python-version in the cwd that names an executable runs it.
    "uv": "#!/bin/bash\n"
    + 'pv="$(cat .python-version 2> /dev/null)" && [[ -x ${pv} ]] && exec "${pv}" "$@"\n'
    + RUN.format(name="uv"),
    "gate-python": "#!/bin/bash\n" + RUN.format(name="gate-python"),
    "gh": '#!/usr/bin/env bash\necho "$*" >> "$CALLS/gh.log"\n[[ "$1 $2" != "pr create" ]] || echo https://github.test/pull/9\n',
    "make": '#!/usr/bin/env bash\necho "$*" >> "$CALLS/make.log"\n[[ ! -f "$CALLS/make-fails" ]] || exit 2\n',
    # codex reads its stdin to the end (empty when the caller closed it) and writes its -o file.
    "codex": "#!/usr/bin/env bash\n"
    + RECORD.format(name="codex")
    + 'cat > "$CALLS/codex-stdin"\nwhile (($#)); do [[ $1 != -o ]] || out=$2; shift; done\n'
    # codex-silent writes no -o file; codex-stale writes one dated 2000.
    + '[[ -z ${out:-} || -f "$CALLS/codex-silent" ]] || echo "Verdict: correct" > "$out"\n'
    + '[[ -z ${out:-} || ! -f "$CALLS/codex-stale" ]] || touch -t 200001010000 "$out"\n'
    + 'echo transcript\nexit "$(cat "$CALLS/codex-status" 2> /dev/null || echo 0)"\n',
}
GIT_ENV = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
HISTORY_SH = "#!/usr/bin/env bash\n" + RECORD.format(name="history.sh") + 'cat "$CALLS/history"\n'


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class OrchestratorToolsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name).resolve()
        self.binding = GhFixture(self.temp / "gh-binding")
        self.repo = self.temp / "repo"
        self.repo.mkdir()
        self.binding.git(self.repo, "init", "-q")
        shutil.copytree(TOOLS, self.repo / "scripts/orchestrator")
        self.calls = self.temp / "calls"
        self.calls.mkdir()
        bin_dir, agmsg = self.temp / "bin", self.temp / "agmsg"
        for directory, stubs in ((bin_dir, STUBS), (agmsg, {"history.sh": HISTORY_SH})):
            directory.mkdir()
            for name, text in stubs.items():
                (directory / name).write_text(text)
                (directory / name).chmod(0o755)
        self.env = {
            **self.binding.env,
            "UV_CACHE_DIR": os.environ.get("UV_CACHE_DIR", str(Path.home() / ".cache/uv")),
            "UV_PYTHON": sys._base_executable,
            "CALLS": str(self.calls),
            "AGMSG_SCRIPTS": str(agmsg),
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "TMPDIR": str(self.temp),
            **GIT_ENV,
        }

    def run_tool(self, name, *args, code=0, env=None, cwd=None, stdin=None):
        result = subprocess.run(
            ["bash", str(self.repo / "scripts/orchestrator" / name), *map(str, args)],
            capture_output=True,
            text=True,
            input=stdin,
            cwd=cwd or self.repo,
            env={**self.env, **(env or {})},
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stderr)
        return result

    def call(self, name):
        path = self.calls / name
        return path.read_text().split("\0")[:-1] if path.exists() else None

    def git(self, *args, cwd=None):
        return self.binding.git(cwd or self.repo, *args)

    def origin(self, *files):
        """Commit the given repo files as main, and push it to a bare repository that is `origin`."""
        self.git("add", "--", *files)
        self.git("commit", "-q", "--allow-empty", "-m", "init")
        self.git("branch", "-M", "main")
        bare = self.temp / "origin.git"
        bare.mkdir()
        self.binding.git(bare, "init", "-q", "--bare", bare=True)
        self.git("remote", "add", "origin", str(self.temp / "origin.git"))
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")

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

    def test_dispatch_refuses_a_task_line_without_task_sha256_or_with_a_second_line(self):
        self.write(".orchestration/tasks/t.md", "task\n")
        for line, code, needle in (
            # Thread 4254163604: a TASK whose file is not hash-bound is never sent.
            ("AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md", 1, "needs task_sha256="),
            (f"AGMSG-TASK v1 task_id=t task_sha256={sha('task' + chr(10))}", 1, "needs task_file="),
            ("AGMSG-TASK v1 task_id=t\nAGMSG-TASK v1 task_id=u", 2, "more than one line"),
            # Thread 4254107304: a blank line after the message is a second line, not a trailing newline.
            ("AGMSG-PING v1 task_id=t\n", 2, "more than one line"),
            # Thread 4256541716: command substitution would drop the NUL and send another line.
            ("AGMSG-PING v1 task_id=t\0 reason=check", 2, "holds a NUL byte"),
        ):
            with self.subTest(needle=needle, code=code):
                self.assertIn(needle, self.dispatch(line, code=code).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))

    def test_dispatch_passes_the_line_byte_identical(self):
        # Run from another checkout: a relative task_file= is the script's own checkout's (thread 4253994697).
        pr = self.temp / "pr"
        pr.mkdir()
        self.binding.git(pr, "init", "-q")
        self.write(".orchestration/tasks/t.md", "task\n")
        self.write("design.md", "design\n")
        line = (
            f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_sha256={sha('task' + chr(10))}"
            f" design=design.md design_sha256={sha('design' + chr(10))}"
            # Thread 4256541725: a reference to the previous design, checked as hex and never recomputed.
            f" previous_design_sha256={sha('old design')} note=a;b(c)`d`$(e)"
        )
        self.write("line.txt", line + "\n")
        self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", str(self.repo / "line.txt"), cwd=pr)
        self.assertEqual(["team", "orch", "worker", "w5:pA", line], self.call("agmsg-dispatch"))

    def test_dispatch_refuses_a_line_without_a_task_id(self):
        # Thread 4254893065: a message without exactly one non-empty task_id= is never sent, nor recorded.
        record = self.write(".orchestration/acceptance/t.md", '---\n{"task": "t"}\n---\n')
        before = record.read_text()
        for line in (
            "AGMSG-PING v1 reason=check",
            "AGMSG-PING v1 task_id= reason=check",
            "AGMSG-ACCEPTANCE v1 task_id=t task_id=u status=accepted",
        ):
            with self.subTest(line=line):
                self.write("line.txt", line + "\n")
                result = self.run_tool(
                    "dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record), code=1
                )
                self.assertIn("exactly one non-empty task_id=", result.stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))
                self.assertEqual(before, record.read_text())

    def test_dispatch_refuses_malformed_lines(self):
        for line, code, needle in (
            ("hello task_id=t", 2, "not an AGMSG-TASK"),
            (f"AGMSG-ACCEPTANCE v1 task_id=t amended_task_sha256={sha('x')}", 1, "amended_task_sha256 has no"),
            ("AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_sha256=abc", 1, "not 64 lowercase hex"),
            ("AGMSG-ACCEPTANCE v1 task_id=t previous_design_sha256=abc", 1, "previous_design_sha256 is not 64"),
            # Thread 4254771302: a hash field whose name has a digit is checked like any other.
            (
                f"AGMSG-ACCEPTANCE v1 task_id=t a02_expected=x.md a02_expected_sha256={sha('x')}",
                1,
                "a02_expected_sha256: ",
            ),
            # Thread 4254494989: a repeated source key leaves an unhashed second path in the line.
            (
                f"AGMSG-TASK v1 task_id=t task_file=.orchestration/tasks/t.md task_file=other.md task_sha256={sha('task' + chr(10))}",
                1,
                "task_file= appears more than once",
            ),
            # Thread 4254399800: a line naming the file both ways could bind the wrong artifact.
            (
                f"AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_file=e.md design_sha256={sha('x')}",
                1,
                "both design_file= and design=",
            ),
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.dispatch(line, code=code).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))

    @staticmethod
    def gate_block(path):
        """The record's block, loaded as the gate does: standard json, duplicate keys and NaN refused."""

        def refuse(pairs):
            keys = [k for k, _ in pairs]
            assert len(keys) == len(set(keys)), keys
            return dict(pairs)

        def constant(name):
            raise AssertionError(f"non-finite number {name}")

        text = path.read_text()
        assert text.startswith("---\n"), text
        end = text.index("\n---\n", 3)
        return json.loads(text[4:end], object_pairs_hook=refuse, parse_constant=constant), text[end + 5 :]

    def test_dispatch_records_the_sent_line_with_its_read_marker(self):
        # Thread 4254107312: the a04 rule's dispatch: key, written after the send.
        record = self.write(
            ".orchestration/acceptance/t.md", '---\n{"format": 1, "task": "t", "ledger": []}\n---\n\nProse.\n'
        )
        ping = "AGMSG-PING v1 task_id=t reason=check"
        # Thread 4254399807: an older identical row on the bus is not this send.
        (self.calls / "history").write_text(f"  ● [2026-10-12T00:00:00Z] orch → worker: {ping}\n")
        (self.calls / "dispatch-marker").write_text("○")
        self.write("line.txt", ping + "\n")
        inode = record.stat().st_ino
        self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record))
        # Thread 4254844595: the record is replaced whole (a new inode), never rewritten in place.
        self.assertNotEqual(inode, record.stat().st_ino)
        self.assertEqual(["t.md"], sorted(p.name for p in record.parent.iterdir()))
        block, prose = self.gate_block(record)
        self.assertEqual({"dispatch": [f"{ping} read_at=read"], "format": 1, "ledger": [], "task": "t"}, block)
        self.assertEqual("\nProse.\n", prose)
        # Thread 4254399805: team-wide, never with an agent, which would rename the calling pane.
        self.assertEqual(["team", "", "200"], self.call("history.sh"))
        # A record without a block gets one holding only dispatch; an unread message says so.
        plain = self.write(".orchestration/acceptance/u.md", "Prose only.\n")
        (self.calls / "dispatch-marker").write_text("●")
        self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(plain))
        self.assertEqual(({"dispatch": [f"{ping} read_at=unread"]}, "Prose only.\n"), self.gate_block(plain))
        # Thread 4256987087: a CRLF record's block is found and its prose keeps every byte.
        crlf = self.repo / ".orchestration/acceptance/c.md"
        crlf.write_bytes(b'---\r\n{"task": "t"}\r\n---\r\n\r\nProse.\r\n')
        self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(crlf))
        self.assertTrue(crlf.read_bytes().endswith(b'"task": "t"\n}\n---\n\r\nProse.\r\n'), crlf.read_bytes())
        self.assertEqual({"dispatch": [f"{ping} read_at=unread"], "task": "t"}, self.gate_block(crlf)[0])
        # A send that adds no row records nothing, though identical rows are already on the bus.
        (self.calls / "dispatch-fails").write_text("")
        before = record.read_text()
        result = self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record), code=1)
        self.assertIn("this send added no bus row", result.stderr)
        self.assertEqual(before, record.read_text())
        # Thread 4254844587: another task's record is refused before anything is sent.
        (self.calls / "dispatch-fails").unlink()
        (self.calls / "agmsg-dispatch").unlink()
        other = self.write(".orchestration/acceptance/w.md", '---\n{"task": "u"}\n---\n')
        result = self.run_tool("dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(other), code=1)
        self.assertIn("is the record of task u, the line is task t", result.stderr)
        self.assertIsNone(self.call("agmsg-dispatch"))

    def test_dispatch_refuses_an_unwritable_record_before_sending(self):
        # The local review of 0d199475 (C-32): a record the atomic replace would fail on is refused before the send.
        self.write("line.txt", "AGMSG-PING v1 task_id=t reason=check\n")
        (self.calls / "history").write_text("")
        locked = self.write("locked/t.md", '---\n{"task": "t"}\n---\n')
        locked.parent.chmod(0o555)
        self.addCleanup(locked.parent.chmod, 0o755)
        missing = self.repo / ".orchestration/acceptance/absent.md"
        # Thread 4256541708: a missing record and one under a regular file are refused whoever runs the test.
        under_file = self.repo / "line.txt/t.md"
        for record in (missing, under_file, locked):
            with self.subTest(record=str(record.relative_to(self.repo))):
                if record == locked and os.geteuid() == 0:
                    self.skipTest("root writes a read-only directory")
                result = self.run_tool(
                    "dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record), code=1
                )
                self.assertIn(f"the record {record} cannot be written", result.stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))
        self.assertFalse(missing.exists())

    def test_dispatch_refuses_a_malformed_record_block_before_sending(self):
        self.write("line.txt", "AGMSG-PING v1 task_id=t reason=check\n")
        (self.calls / "history").write_text("")
        for block, needle in (
            ('["t"]', "the block is not a JSON object"),
            ('{"task": "t",}', "the block is not valid JSON"),
            ('{"task": "t", "task": "t"}', "duplicate key task"),
            ('{"task": "t", "dispatch": {}}', "dispatch is not a list"),
        ):
            with self.subTest(needle=needle):
                record = self.write(".orchestration/acceptance/t.md", f"---\n{block}\n---\n")
                result = self.run_tool(
                    "dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", str(record), code=1
                )
                self.assertIn(needle, result.stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))
                self.assertEqual(f"---\n{block}\n---\n", record.read_text())

    def test_dispatch_line_grammar_table(self):
        # Item 4's input grammar (C-31): one refused line per row the tests above do not cover.
        self.write(".orchestration/tasks/t.md", "task\n")
        task = f"task_file=.orchestration/tasks/t.md task_sha256={sha('task' + chr(10))}"
        for line, code, needle in (
            ("AGMSG-TASK task_id=t", 2, "not an AGMSG-TASK"),
            (f"AGMSG-TASK v1 AGMSG-TASK v1 task_id=t {task}", 2, "AGMSG-TASK is not a <key>=<value> token"),
            (f"AGMSG-TASK v1 task_id=t task_sha256={sha('task' + chr(10))}", 1, "needs task_file="),
            ("AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_sha256=ABC", 1, "not 64 lowercase hex"),
            (
                f"AGMSG-ACCEPTANCE v1 task_id=t design=d.md design_file=e.md design_sha256={sha('x')}",
                1,
                "both design_file=",
            ),
            (
                f"AGMSG-ACCEPTANCE v1 task_id=t design=d.md design=e.md design_sha256={sha('x')}",
                1,
                "design= appears more",
            ),
            (f"AGMSG-ACCEPTANCE v1 task_id=t design=absent.md design_sha256={sha('x')}", 1, "absent.md does not exist"),
            ("AGMSG-PING v1 task_id=t note=two words", 2, "words is not a <key>=<value> token"),
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.dispatch(line, code=code).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))
        for line in (
            f"AGMSG-ACCEPTANCE v1 task_id=t previous_design_sha256={sha('old')}",
            f"AGMSG-TASK\tv1\ttask_id=t\t{task.replace(' ', chr(9))}",
        ):
            with self.subTest(line=line):
                self.dispatch(line)
                self.assertEqual(line, self.call("agmsg-dispatch")[4])
                (self.calls / "agmsg-dispatch").unlink()

    def test_dispatch_refuses_a_tab_separated_task_without_its_hash_fields(self):
        # Thread 4260535901: a tab after AGMSG-TASK must not skip the required-field check.
        self.write(".orchestration/tasks/t.md", "task\n")
        for line, needle in (
            ("AGMSG-TASK\tv1\ttask_id=t", "needs task_file="),
            ("AGMSG-TASK\tv1 task_id=t task_file=.orchestration/tasks/t.md", "needs task_sha256="),
        ):
            with self.subTest(needle=needle):
                self.assertIn(needle, self.dispatch(line, code=1).stderr)
                self.assertIsNone(self.call("agmsg-dispatch"))

    def test_dispatch_record_path_tokenizes_and_locks(self):
        record = self.write(".orchestration/acceptance/t.md", '---\n{"task": "t"}\n---\n')
        (self.calls / "history").write_text("")
        (self.calls / "dispatch-marker").write_text("○")
        args = ["team", "orch", "worker", "w5:pA"]
        # Thread 4255272793: the record check reads the validator's task_id, whatever whitespace precedes it.
        self.write("line.txt", "AGMSG-PING v1 \ttask_id=u reason=check\n")
        result = self.run_tool("dispatch.sh", *args, "line.txt", str(record), code=1)
        self.assertIn("is the record of task t, the line is task u", result.stderr)
        self.assertIsNone(self.call("agmsg-dispatch"))
        # Thread 4255272797: both sends wait for the record directory's lock, then both are recorded.
        lines = [f"AGMSG-PING v1\ttask_id=t reason=r{n}" for n in (0, 1)]
        for n, line in enumerate(lines):
            self.write(f"line{n}.txt", line + "\n")
        lock = os.open(record.parent, os.O_RDONLY)
        fcntl.flock(lock, fcntl.LOCK_EX)
        script = str(self.repo / "scripts/orchestrator/dispatch.sh")
        procs = [
            subprocess.Popen(
                ["bash", script, *args, f"line{n}.txt", str(record)],
                cwd=self.repo,
                env=self.env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for n in (0, 1)
        ]
        deadline = time.monotonic() + 20
        while len((self.calls / "history").read_text().splitlines()) < 2 and time.monotonic() < deadline:
            time.sleep(0.05)
        time.sleep(0.5)
        self.assertEqual([None, None], [proc.poll() for proc in procs])
        self.assertEqual('---\n{"task": "t"}\n---\n', record.read_text())
        fcntl.flock(lock, fcntl.LOCK_UN)
        os.close(lock)
        for proc in procs:
            _, err = proc.communicate(timeout=30)
            self.assertEqual(0, proc.returncode, err)
        self.assertEqual(
            sorted(f"{line} read_at=read" for line in lines), sorted(self.gate_block(record)[0]["dispatch"])
        )

    def checker_dispatch(self):
        """A stub checker beside the copied dispatch.sh and a fake uv that logs, then runs the real uv next on PATH."""
        self.write(
            "scripts/orchestrator/task-consistency-check.py",
            "import re, sys\nf = sys.argv[-1]\ntid = re.search(r'^task_id: (\\S+)', open(f).read(), re.M)[1]\n"
            "if f'.orchestration/{tid}/**' in open(f).read():\n    sys.exit(print(f'{f}: OK'))\n"
            "print(f'{f}: FAIL')\nprint(f'  C2 allowed_files lacks .orchestration/{tid}/**')\nsys.exit(1)\n",
        )
        # The fake records each call's exact argv, directory and environment, then runs the real uv next on PATH; uv
        # runs under env -i, so the calls directory is written into it. Python adds no variable of its own.
        (self.temp / "bin/uv").unlink()
        fake = self.temp / "fake-uv/uv"
        fake.parent.mkdir()
        fake.write_text(
            "#!/usr/bin/env python3\nimport json, os, shutil, sys\n"
            f"calls = {str(self.calls)!r}\n"
            "with open(os.path.join(calls, 'uv.log'), 'a') as f:\n    f.write(' '.join(sys.argv[1:]) + '\\n')\n"
            "record = {'argv': sys.argv[1:], 'cwd': os.getcwd(), 'env': dict(os.environ)}\n"
            "with open(os.path.join(calls, 'uv-calls.jsonl'), 'a') as f:\n    f.write(json.dumps(record) + '\\n')\n"
            # uv-cold stands for a cache without PyYAML: the offline probe fails as uv --offline would.
            "if os.path.exists(os.path.join(calls, 'uv-cold')) and sys.argv[-1] == 'import yaml':\n    sys.exit(1)\n"
            "here = os.path.dirname(os.path.realpath(__file__))\n"
            "path = os.pathsep.join(p for p in os.environ['PATH'].split(os.pathsep) if os.path.realpath(p) != here)\n"
            "real = shutil.which('uv', path=path)\n"
            f"os.execv(real, [real, '--cache-dir', {self.env['UV_CACHE_DIR']!r}, *sys.argv[1:]])\n"
        )
        fake.chmod(0o755)
        env = {"PATH": f"{fake.parent}{os.pathsep}{self.env['PATH']}"}
        record = self.write(".orchestration/acceptance/t.md", '---\n{"task": "t"}\n---\n')
        (self.calls / "history").write_text("")
        (self.calls / "dispatch-marker").write_text("○")
        rel = ".orchestration/tasks/t.md"

        def send(front, code, cwd=None, extra=None):
            text = self.write(rel, f"---\nformat: 2\ntask_id: t\n{front}---\n\nBody.\n").read_text()
            line = self.write("line.txt", f"AGMSG-TASK v1 task_id=t task_file={rel} task_sha256={sha(text)}\n")
            for name in ("uv.log", "uv-calls.jsonl"):
                (self.calls / name).unlink(missing_ok=True)
            args = ["team", "orch", "worker", "w5:pA", line, record]
            result = self.run_tool("dispatch.sh", *args, code=code, env={**env, **(extra or {})}, cwd=cwd)
            return result, (self.calls / "uv.log").read_text()

        return rel, record, send

    def test_dispatch_refuses_a_task_file_failing_the_checker(self):
        # C-52: the checker beside the script is a stub that fails a file lacking its own evidence directory.
        rel, record, send = self.checker_dispatch()
        lacking = "allowed_files:\n  - scripts/x.sh\n"
        # Both orders of the duplicate key: PyYAML alone would keep the last value, review in the second.
        duplicates = ("kind: review\nkind: code\n", "kind: code\nkind: review\n")
        for kind in ("kind: code\n", 'kind: "code"\n', "", *duplicates, "kind: review\n: broken\n"):
            with self.subTest(kind=kind):
                result, log = send(kind + lacking, 1)
                self.assertIn(f"dispatch: {self.repo / rel} fails the task-consistency check", result.stderr)
                self.assertIn("C2 allowed_files lacks .orchestration/t/**", result.stderr)
                self.assertIn(f"task-consistency-check.py --root {self.repo} {self.repo / rel}", log)
                self.assertIsNone(self.call("agmsg-dispatch"))
                self.assertEqual('---\n{"task": "t"}\n---\n', record.read_text())
        # A cold cache stops the send with exit 2 and the warming command, never a fetch through the index.
        (self.calls / "uv-cold").write_text("")
        result, log = send("kind: code\n" + lacking, 2)
        self.assertIn("PyYAML is not in the uv cache", result.stderr)
        self.assertIn("make validate-agent-assets", result.stderr)
        self.assertEqual(1, log.count("run "))
        self.assertIsNone(self.call("agmsg-dispatch"))
        (self.calls / "uv-cold").unlink()
        _, log = send("kind: review\n", 0)
        # The Makefile's UV_PYYAML probe comes first, then the brief parse in the form it chose.
        self.assertRegex(
            log.splitlines()[0],
            r"^run --no-config --no-project --offline --python /\S+ --with pyyaml python -I -c import yaml$",
        )
        self.assertNotIn("task-consistency-check.py", log)
        self.assertIn("python -I -c", log)
        self.assertEqual(1, len(self.gate_block(record)[0]["dispatch"]))

    def test_dispatch_runs_uv_on_a_pinned_interpreter_whatever_the_caller_state(self):
        # local:9df6b0c:1 (C-57), with the Bot's P1s 4292675906, 4299651928 and 4300102967: a caller's project, its
        # .python-version, an inherited virtual environment, uv override or PYTHONPATH, all at once, choose nothing.
        _, record, send = self.checker_dispatch()
        pwn = self.write("pwn", f'#!/bin/sh\ntouch "{self.calls}/pwned"\nexit 1\n')
        pwn.chmod(0o755)
        caller = self.temp / "caller"
        (caller / ".venv/bin").mkdir(parents=True)
        (caller / ".venv/bin/python").symlink_to(pwn)
        (caller / ".venv/pyvenv.cfg").write_text("home = /nonexistent\n")
        (caller / "pyproject.toml").write_text(
            '[project]\nname = "caller"\nversion = "0"\ndependencies = ["no-such-package-dispatch-a03"]\n'
        )
        (caller / ".python-version").write_text(f"{pwn}\n")
        (caller / "pylib").mkdir()
        (caller / "pylib/yaml.py").write_text(f"open({str(self.calls / 'pwned')!r}, 'w')\n")
        state = {"VIRTUAL_ENV": str(caller / ".venv"), "CONDA_PREFIX": str(caller / ".venv"), "UV_PYTHON": str(pwn)}
        state |= {"PYTHONPATH": str(caller / "pylib"), "AGMSG_STORAGE_PATH": str(self.temp / "store")}
        # 4300738707: a planted HOME whose uv.toml names a planted index, and audit:ef74eae:1's GIT_DIR/GIT_WORK_TREE.
        (caller / "home/.config/uv").mkdir(parents=True)
        (caller / "home/.config/uv/uv.toml").write_text('index-url = "http://127.0.0.1:9/simple"\n')
        other = self.temp / "other"
        other.mkdir()
        self.binding.git(other, "init", "-q")
        state |= {"HOME": str(caller / "home"), "GIT_DIR": str(other / ".git"), "GIT_WORK_TREE": str(other)}
        _, _ = send("kind: review\n", 0, cwd=caller, extra=state)
        self.assertFalse((self.calls / "pwned").exists())
        # Positive identity: the exact argv and the exact environment of every uv call, so no other input can reach it.
        home = pwd.getpwuid((self.repo / "scripts/orchestrator/dispatch.sh").stat().st_uid).pw_dir
        path = f"{self.temp / 'fake-uv'}{os.pathsep}{self.env['PATH']}"
        found = subprocess.run(
            ["env", "-i", f"PATH={path}", f"HOME={home}", "mise", "which", "python3"],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        python = found if found.startswith("/") else shutil.which("python3", path=path)
        given = {**self.env, **state}
        expected_env = {"PATH": path, "HOME": home, "UV_CACHE_DIR": f"{home}/.cache/uv"}
        expected_env |= {k: v for k, v in given.items() if k in ("LANG", "LC_ALL") and v}
        expected_env |= {k: v for k, v in given.items() if k.startswith("AGMSG_")}
        head = [
            "run",
            "--no-config",
            "--no-project",
            "--offline",
            "--python",
            python,
            "--with",
            "pyyaml",
            "python",
            "-I",
        ]
        task = str(self.repo / ".orchestration/tasks/t.md")
        calls = [json.loads(line) for line in (self.calls / "uv-calls.jsonl").read_text().splitlines()]
        self.assertEqual(2, len(calls))  # the probe and the brief parse; a brief runs no checker
        self.assertEqual([*head, "-c", "import yaml"], calls[0]["argv"])
        self.assertEqual([*head, "-c", task], [*calls[1]["argv"][:11], calls[1]["argv"][12]])
        self.assertEqual(13, len(calls[1]["argv"]))
        for call in calls:
            # macOS adds __CF_USER_TEXT_ENCODING to every process, after env -i too; it is no input the script passes.
            call["env"].pop("__CF_USER_TEXT_ENCODING", None)
            self.assertEqual(expected_env, call["env"])
            self.assertEqual(str(self.repo), call["cwd"])
        self.assertEqual(1, len(self.gate_block(record)[0]["dispatch"]))

    def test_dispatch_resolves_its_root_without_inherited_git_variables(self):
        # audit:ef74eae:1: an inherited GIT_DIR and GIT_WORK_TREE redirected the root the checker trusts; under it,
        # C6 found no design file and accepted a stale receipt. The stub checker emulates C6 and prints its root.
        _, record, _ = self.checker_dispatch()
        self.write(
            "scripts/orchestrator/task-consistency-check.py",
            "import pathlib, re, sys\nroot, f = pathlib.Path(sys.argv[sys.argv.index('--root') + 1]), sys.argv[-1]\n"
            "print(f'root: {root}')\ntext = open(f).read()\n"
            "design, receipt = re.search(r'design: (\\S+)', text)[1], re.search(r'receipt: (\\S+)', text)[1]\n"
            "if (root / design).exists() and f'receipt: {receipt}' not in (root / design).read_text():\n"
            "    print(f'{f}: FAIL\\n  C6 design_review.receipt is stale')\n    sys.exit(1)\nprint(f'{f}: OK')\n",
        )
        self.write("d.md", "design_review:\n  receipt: r2\n")
        task = self.write(
            ".orchestration/tasks/t.md",
            "---\nformat: 2\ntask_id: t\nkind: code\nallowed_files:\n  - .orchestration/t/**\n"
            "design_review:\n  receipt: r1\n  design: d.md\n---\n\nBody.\n",
        )
        line = self.write("line.txt", f"AGMSG-TASK v1 task_id=t task_file={task} task_sha256={sha(task.read_text())}\n")
        other = self.temp / "other"
        other.mkdir()
        self.binding.git(other, "init", "-q")
        env = {
            "PATH": f"{self.temp / 'fake-uv'}{os.pathsep}{self.env['PATH']}",
            "GIT_DIR": str(other / ".git"),
            "GIT_WORK_TREE": str(other),
        }
        args = ["team", "orch", "worker", "w5:pA", line, record]
        result = self.run_tool("dispatch.sh", *args, code=1, env=env)
        self.assertIn(f"root: {self.repo}\n", result.stderr)
        self.assertIn("C6 design_review.receipt is stale", result.stderr)
        checker = f"{self.repo}/scripts/orchestrator/task-consistency-check.py --root {self.repo} {task}"
        self.assertIn(checker, (self.calls / "uv.log").read_text())
        self.assertIsNone(self.call("agmsg-dispatch"))
        self.assertEqual('---\n{"task": "t"}\n---\n', record.read_text())

    def test_dispatch_reads_a_bounded_history_window(self):
        # C-53: each read answers the window the case writes, window-1 before the send and window-2 after it.
        (self.temp / "agmsg/history.sh").write_text(
            '#!/usr/bin/env bash\necho "$*" >> "$CALLS/history.log"\n'
            'n=$(($(cat "$CALLS/reads" 2> /dev/null || echo 0) + 1)) && echo "${n}" > "$CALLS/reads"\n'
            'cat "$CALLS/window-${n}"\n'
        )
        ping = "AGMSG-PING v1 task_id=t reason=check"
        self.write("line.txt", ping + "\n")
        empty = '---\n{"task": "t"}\n---\n'
        record = self.write(".orchestration/acceptance/t.md", empty)

        def row(ts, text=ping, mark="●", sender="orch", to="worker"):
            return f"  {mark} [2026-10-15T00:{ts}Z] {sender} → {to}: {text}"

        def send(pre, post, code=0, window=None):
            for n, rows in ((1, pre), (2, post)):
                (self.calls / f"window-{n}").write_text("".join(r + "\n" for r in rows))
            for name in ("reads", "history.log"):
                (self.calls / name).unlink(missing_ok=True)
            record.write_text(empty)
            env = {"BUS_READ_WINDOW": window} if window else None
            result = self.run_tool(
                "dispatch.sh", "team", "orch", "worker", "w5:pA", "line.txt", record, code=code, env=env
            )
            self.assertEqual([], list(self.temp.glob("dispatch-window.*")))
            return result

        def recorded():
            return self.gate_block(record)[0]["dispatch"]

        # Eviction plus collision: the oldest row of a full window equals the line and leaves it.
        full = [row("00:00")] + [row(f"{i // 60:02}:{i % 60:02}", f"x{i}") for i in range(1, 200)]
        send(full, full[1:] + [row("59:00", mark="○")])
        self.assertEqual([f"{ping} read_at=read"], recorded())
        self.assertEqual(["team  200", "team  200"], (self.calls / "history.log").read_text().splitlines())
        send(full[150:], full[151:] + [row("59:00", mark="○")], window="50")
        self.assertEqual(["team  50", "team  50"], (self.calls / "history.log").read_text().splitlines())
        # Same second: the newest pre-send row equals the line; the second such row is this send.
        a, b = row("01:00", "a"), row("02:00", "b")
        send([a, b, row("03:00")], [a, b, row("03:00"), row("03:00", mark="○")])
        self.assertEqual([f"{ping} read_at=read"], recorded())
        # Another seat's row lands after this send: the line's row is still the one recorded.
        send([a, b], [a, b, row("03:00", mark="○"), row("03:01", "AGMSG-PONG v1 task_id=t", "●", "worker", "orch")])
        self.assertEqual([f"{ping} read_at=read"], recorded())
        refusals = (
            ([a, b], [row("04:00", "c"), row("05:00", "d"), row("06:00")], "raise BUS_READ_WINDOW"),
            ([a, b], [a, b], "this send added no bus row"),
            ([row("07:00", "p")] * 200, [row("07:00", "p")] * 200, "does not align uniquely"),
        )
        for pre, post, message in refusals:
            with self.subTest(message=message):
                self.assertIn(message, send(pre, post, code=1).stderr)
                self.assertEqual(empty, record.read_text())

    # three-repeat.sh

    def test_three_repeat_rejects_a_class_that_is_not_a_slug_and_runs_the_cli_from_its_own_checkout(self):
        for value in ("Reject skipped contract", "a;b"):
            with self.subTest(value=value):
                self.assertIn("usage", self.run_tool("three-repeat.sh", value, code=2).stderr)
        self.assertIsNone(self.call("uv"))
        # Thread 4254771284: a slug that looks like an option reaches the CLI after --, as its query.
        (self.calls / "uv-output").write_text("No matches.\n")
        self.write(".orchestration/learning/mistakes/M-0.md", "classes: [x]\n")
        self.run_tool("three-repeat.sh", "--help")
        self.assertEqual(["memory", "search", "--limit", "1000", "--", "--help"], self.call("uv")[3:])
        # Thread 4253994697: a PR worktree's contextdb CLI is PR-controlled code, so the root is the script's own.
        pr = self.temp / "pr"
        pr.mkdir()
        self.binding.git(pr, "init", "-q")
        (pr / ".orchestration/learning/mistakes").mkdir(parents=True)
        (pr / ".orchestration/learning/mistakes/M-PR.md").write_text("classes: [bookkeeping]\n")
        self.write(".orchestration/learning/mistakes/M-OWN.md", "classes: [bookkeeping]\n")
        (self.calls / "uv-output").write_text("No matches.\n")
        out = self.run_tool("three-repeat.sh", "bookkeeping", cwd=pr).stdout.splitlines()
        self.assertEqual("search: bookkeeping -> M-OWN.md", out[0])
        self.assertEqual(str(self.repo / ".claude/hooks/contextdb_cli.py"), self.call("uv")[2])
        self.assertEqual(str(self.repo), (self.calls / "uv-cwd").read_text().strip())

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
            [
                "search: bookkeeping -> M-20261012-2.md, M-20261012-4.md",
                "search-body: bookkeeping -> M-20261011-1.md, M-20261012-2.md, M-20261012-4.md",
                "compactiondb: bookkeeping -> 2 matches",
            ],
            out,
        )
        cli = str(self.repo / ".claude/hooks/contextdb_cli.py")
        self.assertEqual(
            ["run", "--no-project", cli, "memory", "search", "--limit", "1000", "--", "bookkeeping"], self.call("uv")
        )
        (self.calls / "uv-output").write_text("No matches.\n")
        self.assertEqual(
            ["search: absent -> none", "search-body: absent -> none", "compactiondb: absent -> 0 matches"],
            self.run_tool("three-repeat.sh", "absent").stdout.splitlines(),
        )

    def test_three_repeat_prints_body_matches_and_states_a_capped_memory_count(self):
        mistakes = ".orchestration/learning/mistakes"
        self.write(f"{mistakes}/M-1.md", "id: M-1\nclasses: [bookkeeping]\n")
        # Thread 4255494137: a class named in the prose only is a body match, never a classes: match.
        self.write(f"{mistakes}/M-2.md", "id: M-2\nclasses: [sources]\nThe Bookkeeping slipped.\n")
        (self.calls / "uv-output").write_text("".join(f"{i:08x}-0000 row\n" for i in range(1000)))
        self.assertEqual(
            [
                "search: bookkeeping -> M-1.md",
                "search-body: bookkeeping -> M-1.md, M-2.md",
                "compactiondb: bookkeeping -> >=1000 matches (capped)",
            ],
            self.run_tool("three-repeat.sh", "bookkeeping").stdout.splitlines(),
        )
        self.assertEqual(["memory", "search", "--limit", "1000", "--", "bookkeeping"], self.call("uv")[3:])

    # bus-read.sh

    def history(self, *messages):
        """history.sh rows from (minutes ago or a literal <at>, from, to, body), after one line that is not a row."""
        now = datetime.now(UTC)
        rows = ["agmsg: a line that is not a message"]
        for ago, sender, to, body in messages:
            at = ago if isinstance(ago, str) else (now - timedelta(minutes=ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append(f"  ○ [{at}] {sender} → {to}: {body}")
        (self.calls / "history").write_text("\n".join(rows) + "\n")

    def test_bus_read_lists_an_open_task_with_minutes_since_its_latest_event(self):
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
        *lines, skipped = self.run_tool("bus-read.sh", "team").stdout.splitlines()
        self.assertEqual("skipped=1", skipped)
        self.assertEqual(["T1", "T3"], [re.search(r"task=(\S+)", line).group(1) for line in lines])
        fields = [dict(re.findall(r"(\w+)=(\S+)", line)) for line in lines]
        self.assertEqual(["w1", "w3"], [f["seat"] for f in fields])
        self.assertEqual(["yes", "no"], [f["silent"] for f in fields])
        for f, minutes in zip(fields, (45, 10), strict=True):
            self.assertLessEqual(abs(int(f["minutes"]) - minutes), 1, f)
        self.assertEqual(["team", "", "100000"], self.call("history.sh"))
        only = self.run_tool("bus-read.sh", "team", "T3").stdout.splitlines()
        self.assertEqual(2, len(only))
        self.assertIn("task=T3 ", only[0])
        self.assertEqual(["open: none", "skipped=1"], self.run_tool("bus-read.sh", "team", "T2").stdout.splitlines())

    def open_tasks(self):
        """bus-read.sh's (task, seat) pairs and its final line."""
        out = self.run_tool("bus-read.sh", "team").stdout
        return re.findall(r"^open: task=(\S+) seat=(\S+) ", out, re.MULTILINE), out.splitlines()[-1]

    def test_bus_read_ignores_closers_between_other_endpoints(self):
        # Thread 4255494133: only the opener's endpoints close a task, as in the stop gate's worker-seat branch;
        # the local review of 5b99a744: and only the latest TASK's endpoints reopen it with a revise.
        self.history(
            (30, "orch", "w1", "AGMSG-TASK v1 task_id=T1"),
            (25, "w9", "orch", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
            (24, "w9", "w1", "AGMSG-ACCEPTANCE v1 task_id=T1 status=accepted"),
            (23, "w9", "orch", "AGMSG-PONG v1 task_id=T1 status=blocked"),
            (20, "orch", "w2", "AGMSG-TASK v1 task_id=T2"),
            # The audit of 3e5cad37: a body is split on runs of spaces and tabs, as the stop gate's awk splits it.
            (10, "w2", "orch", "AGMSG-PONG\tv1  task_id=T2\tstatus=blocked"),
            (9, "orch", "w3", "AGMSG-TASK v1 task_id=T3"),
            (8, "w3", "orch", "AGMSG-RESULT v1 task_id=T3 status=ready_for_review"),
            (7, "w9", "w8", "AGMSG-ACCEPTANCE v1 task_id=T3 status=revise"),
            (6, "w9", "w3", "AGMSG-ACCEPTANCE v1 task_id=T3 status=revise"),
        )
        self.assertEqual(([("T1", "w1")], "skipped=1"), self.open_tasks())
        # Thread 4256987076: w9's later rows do not reset the silence clock of T1's pair (its TASK, 30 minutes ago).
        self.assertIn(" silent=yes", self.run_tool("bus-read.sh", "team").stdout.splitlines()[0])

    def test_bus_read_closes_a_task_on_any_non_revise_acceptance(self):
        # Thread 4255494139: no status whitelist; any ACCEPTANCE from the opener's sender but revise closes.
        self.history(
            (40, "orch", "w1", "AGMSG-TASK v1 task_id=T1"),
            (39, "orch", "w1", "AGMSG-ACCEPTANCE v1 task_id=T1 status=closed-historical"),
            (38, "orch", "w2", "AGMSG-TASK v1 task_id=T2"),
            (37, "orch", "w2", "AGMSG-ACCEPTANCE v1 task_id=T2 status=hold"),
            (36, "orch", "w3", "AGMSG-TASK v1 task_id=T3"),
            (35, "orch", "w3", "AGMSG-ACCEPTANCE v1 task_id=T3"),
            (34, "orch", "w4", "AGMSG-TASK v1 task_id=T4"),
            (33, "w4", "orch", "AGMSG-RESULT v1 task_id=T4 status=ready_for_review"),
            (32, "orch", "w4", "AGMSG-ACCEPTANCE v1 task_id=T4 status=revise"),
        )
        self.assertEqual(([("T4", "w4")], "skipped=1"), self.open_tasks())

    def test_bus_read_skips_and_counts_malformed_rows(self):
        # The Codex round-2 receipt (C-28): each rejected row would close T1 if it counted; none is an exit.
        self.history(
            (30, "orch", "w1", "AGMSG-TASK v1 task_id=T1"),
            (20, "orch", "w1", "AGMSG-PING v1 task_id=T1 reason=check"),
            (20, "w1", "orch", "AGMSG-RESULT task_id=T1"),
            (20, "w1", "orch", "AGMSG-RESULT v1 status=ready_for_review"),
            (20, "w1", "orch", "AGMSG-RESULT v1 task_id= status=ready_for_review"),
            (20, "w1", "orch", "AGMSG-RESULT v1 task_id=T1 task_id=T1"),
            (20, "orch", "w1", "AGMSG-ACCEPTANCE v1 task_id=T1 status=accepted status=accepted"),
            ("yesterday", "w1", "orch", "AGMSG-RESULT v1 task_id=T1"),
        )
        # Thread 4256541723: history.sh marks a row ● or ○, so any other first token is not a row.
        with (self.calls / "history").open("a") as f:
            f.write("  X [2026-10-13T00:00:00Z] w1 → orch: AGMSG-RESULT v1 task_id=T1\n")
        # The helper's first line (a shape mismatch) and the eight rows after the TASK.
        self.assertEqual(([("T1", "w1")], "skipped=9"), self.open_tasks())
        # An empty history is one empty line on jq's input, never a skipped row.
        (self.calls / "history").write_text("")
        self.assertEqual(["open: none", "skipped=0"], self.run_tool("bus-read.sh", "team").stdout.splitlines())

    def test_bus_read_refuses_a_read_that_reaches_its_limit(self):
        self.history(*[(i, "orch", "w1", f"AGMSG-TASK v1 task_id=T{i}") for i in range(3)])
        result = self.run_tool("bus-read.sh", "team", code=1, env={"BUS_READ_LIMIT": "3"})
        self.assertIn("reached its limit of 3 rows", result.stderr)
        # Thread 4256987062: lines are counted before any is skipped, the helper's first line included.
        self.history(*[(i, "orch", "w1", f"AGMSG-TASK v1 task_id=T{i}") for i in range(2)])
        result = self.run_tool("bus-read.sh", "team", code=1, env={"BUS_READ_LIMIT": "3"})
        self.assertIn("reached its limit of 3 rows", result.stderr)

    # boundary.sh, ff-main.sh, replay.sh

    def boundary(self, code):
        self.origin()
        self.write(".orchestration/acceptance/x.md", "record\n")
        message = self.write("msg.txt", "chore(orchestration): boundary\n\nBody.\n")
        (self.calls / "uv-output").write_text("")
        result = self.run_tool("boundary.sh", "2026-10-13-1", message, code=code)
        return result, message, "orchestration/boundary-2026-10-13-1"

    def test_boundary_stops_before_commit_when_the_validator_fails(self):
        (self.calls / "make-fails").write_text("")
        _, _, branch = self.boundary(code=2)
        self.assertEqual(self.git("rev-parse", "origin/main"), self.git("rev-parse", branch))
        self.assertEqual("", self.git("ls-remote", "origin", branch))
        self.assertFalse((self.calls / "gh.log").exists())
        self.assertEqual("validate-agent-assets\n", (self.calls / "make.log").read_text())
        self.assertEqual(".orchestration/acceptance/x.md", self.call("uv")[-1])

    def test_boundary_commits_pushes_and_queues_the_pr(self):
        _, message, branch = self.boundary(code=0)
        self.assertEqual("chore(orchestration): boundary", self.git("log", "-1", "--format=%s", branch))
        self.assertEqual(".orchestration/acceptance/x.md", self.git("show", "--name-only", "--format=", branch))
        self.assertEqual(self.git("rev-parse", branch), self.git("ls-remote", "origin", branch).split()[0])
        self.assertEqual(
            [
                f"pr create --base main --head {branch} --title chore(orchestration): boundary --body-file {message}",
                f"pr merge {branch} --squash --auto",
            ],
            (self.calls / "gh.log").read_text().splitlines(),
        )
        self.assertEqual(1, len(self.git("worktree", "list").splitlines()))

    def test_boundary_deletes_a_deleted_file_and_a_renamed_files_old_path(self):
        # The a02 record's owned rows (4260535916, local:7b574d3:1): a deletion and a rename reach the boundary commit.
        for name in ("gone", "old", "kept"):
            self.write(f".orchestration/{name}.md", f"{name}\n")
        self.origin(".orchestration")
        os.remove(self.repo / ".orchestration/gone.md")
        self.git("mv", ".orchestration/old.md", ".orchestration/new.md")
        message = self.write("msg.txt", "chore(orchestration): boundary\n")
        (self.calls / "uv-output").write_text("")
        self.run_tool("boundary.sh", "2026-10-13-1", message)
        branch = "orchestration/boundary-2026-10-13-1"
        changed = self.git("show", "--no-renames", "--name-status", "--format=", branch).splitlines()
        self.assertEqual(["D\t.orchestration/gone.md", "A\t.orchestration/new.md", "D\t.orchestration/old.md"], changed)
        tree = self.git("ls-tree", "-r", "--name-only", branch, ".orchestration").splitlines()
        self.assertEqual([".orchestration/kept.md", ".orchestration/new.md"], tree)
        # The masker gets the copies only.
        masker = self.call("uv")
        self.assertEqual([".orchestration/new.md"], masker[masker.index("--mask-secrets") + 1 :])

    def test_boundary_keeps_a_name_with_a_newline_one_path(self):
        # PR #361 thread 4277862535: a newline in a name does not split it; the part after it, three bytes cut,
        # would name a file outside the repository for the masker to rewrite.
        self.origin()
        victim = self.temp / "victim.md"
        victim.write_text("victim\n")
        name = f".orchestration/d\n   {victim}"
        self.write(name, "x\n")
        message = self.write("msg.txt", "chore(orchestration): boundary\n")
        (self.calls / "uv-output").write_text("")
        self.run_tool("boundary.sh", "2026-10-13-1", message)
        masker = self.call("uv")
        self.assertEqual([name], masker[masker.index("--mask-secrets") + 1 :])
        tree = self.git("ls-tree", "-r", "-z", "--name-only", "orchestration/boundary-2026-10-13-1", ".orchestration")
        self.assertEqual([name], [path for path in tree.split("\0") if path])
        self.assertEqual("victim\n", victim.read_text())

    def test_boundary_deletes_a_name_with_glob_characters_literally(self):
        # The a05 record's owned row audit:2e77a33:1: a deleted `a*.md` or `[x].md` is a name, not a pattern,
        # so `ab.md` and `x.md`, which those patterns match, stay in the boundary commit's tree.
        for name in ("a*.md", "ab.md", "[x].md", "x.md"):
            self.write(f".orchestration/{name}", f"{name}\n")
        self.origin(".orchestration")
        os.remove(self.repo / ".orchestration/a*.md")
        os.remove(self.repo / ".orchestration/[x].md")
        message = self.write("msg.txt", "chore(orchestration): boundary\n")
        (self.calls / "uv-output").write_text("")
        self.run_tool("boundary.sh", "2026-10-13-1", message)
        branch = "orchestration/boundary-2026-10-13-1"
        changed = self.git("show", "--name-status", "--format=", branch).splitlines()
        self.assertEqual(["D\t.orchestration/[x].md", "D\t.orchestration/a*.md"], sorted(changed))
        tree = self.git("ls-tree", "-r", "--name-only", branch, ".orchestration").splitlines()
        self.assertEqual([".orchestration/ab.md", ".orchestration/x.md"], tree)

    def test_ff_main_keeps_local_edits_across_the_fast_forward(self):
        self.write(".orchestration/a.md", "a\n")
        self.origin(".orchestration/a.md")
        other = self.temp / "other"
        self.git("clone", "-q", "-b", "main", str(self.temp / "origin.git"), str(other))
        for name in ("b", "c"):
            (other / f".orchestration/{name}.md").write_text(f"{name}\n")
        self.git("add", ".orchestration", cwd=other)
        self.git("commit", "-q", "-m", "boundary", cwd=other)
        self.git("push", "-q", "origin", "main", cwd=other)
        # A local edit of a tracked file, an untracked copy equal to main's, and one that differs.
        self.write(".orchestration/a.md", "a local\n")
        self.write(".orchestration/b.md", "b\n")
        self.write(".orchestration/c.md", "c local\n")
        out = self.run_tool("ff-main.sh").stdout.splitlines()
        self.assertEqual(["restored: .orchestration/a.md", "restored: .orchestration/c.md"], out[:2])
        self.assertEqual(self.git("rev-parse", "origin/main"), self.git("rev-parse", "HEAD"))
        self.assertEqual(["a local\n", "b\n", "c local\n"], [self.write_back(n) for n in "abc"])
        # A refused fast-forward puts every moved file back.
        self.git("commit", "-q", "--allow-empty", "-m", "diverge")
        self.git("commit", "-q", "--allow-empty", "-m", "ahead", cwd=other)
        self.git("push", "-q", "origin", "main", cwd=other)
        self.assertIn("refused", self.run_tool("ff-main.sh", code=1).stderr)
        self.assertEqual(["a local\n", "b\n", "c local\n"], [self.write_back(n) for n in "abc"])

    def test_ff_main_keeps_a_local_deletion_across_the_fast_forward(self):
        # The a02 record's owned rows (4260535924, local:9ad0c15:4): a locally deleted tracked file stays deleted,
        # here one that origin/main also changes, so the fast-forward needs it restored first.
        self.write(".orchestration/d.md", "d\n")
        self.origin(".orchestration/d.md")
        other = self.temp / "other"
        self.git("clone", "-q", "-b", "main", str(self.temp / "origin.git"), str(other))
        (other / ".orchestration/d.md").write_text("d upstream\n")
        self.git("commit", "-q", "-am", "boundary", cwd=other)
        self.git("push", "-q", "origin", "main", cwd=other)
        os.remove(self.repo / ".orchestration/d.md")
        self.assertIn("deleted: .orchestration/d.md", self.run_tool("ff-main.sh").stdout.splitlines())
        self.assertEqual(self.git("rev-parse", "origin/main"), self.git("rev-parse", "HEAD"))
        self.assertFalse((self.repo / ".orchestration/d.md").exists())
        # A refused fast-forward leaves it deleted too.
        self.git("commit", "-q", "--allow-empty", "-m", "diverge")
        self.git("commit", "-q", "--allow-empty", "-m", "ahead", cwd=other)
        self.git("push", "-q", "origin", "main", cwd=other)
        self.assertIn("refused", self.run_tool("ff-main.sh", code=1).stderr)
        self.assertFalse((self.repo / ".orchestration/d.md").exists())

    def write_back(self, name):
        return (self.repo / f".orchestration/{name}.md").read_text()

    def test_replay_propagates_the_command_status(self):
        self.origin()
        result = self.run_tool("replay.sh", "echo $PATH; exit 7", code=7)
        self.assertEqual(["/usr/bin:/bin", "exit=7"], result.stdout.splitlines())
        self.assertEqual(1, len(self.git("worktree", "list").splitlines()))

    # codex-review.sh, design-keydiff.py, fill_sweep.py

    def test_codex_review_closes_stdin_fixes_the_profile_and_needs_the_hash(self):
        reviewed = self.write("design.md", "design\n")
        template = self.write("prompt.txt", "Review design.md at @@SHA@@.\n")
        receipt, transcript = self.temp / "receipt.md", self.temp / "transcript.txt"
        (self.calls / "codex-status").write_text("3")
        result = self.run_tool(
            "codex-review.sh",
            reviewed,
            template,
            receipt,
            transcript,
            code=3,
            env={"CODEX_PROFILE": "deep"},
            stdin="open\n",
        )
        prompt = f"Review design.md at {sha('design' + chr(10))}."
        self.assertEqual(
            [
                "--profile",
                "review",
                "exec",
                "--sandbox",
                "read-only",
                "-C",
                str(self.repo),
                "-c",
                "approval_policy=never",
            ]
            + ["-o", str(receipt), prompt],
            self.call("codex"),
        )
        self.assertEqual("", (self.calls / "codex-stdin").read_text())
        self.assertEqual("transcript\n", transcript.read_text())
        self.assertIn(f"sha256={sha('design' + chr(10))} receipt={receipt}", result.stdout)
        (self.calls / "codex").unlink()
        self.write("prompt.txt", "Review design.md.\n")
        self.assertIn(
            "no @@SHA@@", self.run_tool("codex-review.sh", reviewed, template, receipt, transcript, code=2).stderr
        )
        self.assertIsNone(self.call("codex"))

    def test_design_keydiff_names_the_changed_invariant(self):
        design = "---\ninvariants:\n  INV-1: one\n  INV-6: {0}\npremises: []\n---\n\n# Design\n"
        self.write("design.md", design.format("six"))
        self.git("add", "design.md")
        self.git("commit", "-q", "-m", "design")
        self.write("design.md", design.format("six, amended") + "\nA paragraph.\n")
        result = subprocess.run(
            [shutil.which("uv"), "run", "--no-project", "--with", "pyyaml", "python", "-I"]
            + [str(self.repo / "scripts/orchestrator/design-keydiff.py"), "design.md"],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual("invariants ['INV-6']\n", result.stdout)

    def sweep(self, items):
        return self.write("sweep.json", json.dumps({"pr": 9, "items": [{**i, "disposition": ""} for i in items]}))

    def fill_sweep(self, *args, code=0):
        script = str(self.repo / "scripts/orchestrator/fill_sweep.py")
        result = subprocess.run(
            [sys.executable, "-I", script, *map(str, args)], capture_output=True, text=True, check=False
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result.stdout

    def test_fill_sweep_refuses_a_not_applicable_without_evidence(self):
        url = "https://github.test/pull/9"
        sweep = self.sweep(
            [
                {"source": "review_comment", "bot": True, "url": f"{url}#discussion_r11", "body": "P2", "level": "P2"},
                {"source": "issue_comment", "bot": True, "url": f"{url}#issuecomment-12", "body": "Summary"},
            ]
        )
        before = sweep.read_text()

        def fill(reply, code):
            reply = {"id": 21, "user": {"login": "o"}, "in_reply_to_id": 11, "body": reply}
            return self.fill_sweep(
                sweep, self.write("c.json", json.dumps([reply])), "--orchestrator-login", "o", code=code
            )

        self.assertIn(
            "GAP discussion_r11 review_comment P2 not-applicable:the line is gone",
            fill("`not-applicable:the line is gone`", 1),
        )
        self.assertEqual(before, sweep.read_text())
        fill("`not-applicable:the line is gone; evidence=git show HEAD:x`", 0)
        self.assertEqual(
            [
                "not-applicable:the line is gone; evidence=git show HEAD:x",
                "not-applicable:bot summary or onboarding comment, no finding; "
                + f"""evidence=jq --argjson u '"{url}#issuecomment-12"' '.items[] | select(.url == $u)' {sweep}""",
            ],
            [i["disposition"] for i in json.loads(sweep.read_text())["items"]],
        )

    def test_fill_sweep_fills_only_notice_annotations_and_success_statuses(self):
        url = "https://github.test/pull/9/checks"
        levels = [("annotation", lv) for lv in ("notice", "warning", "failure")]
        levels += [("status", lv) for lv in ("success", "failure", "error", "pending")]
        sweep = self.sweep(
            [{"source": s, "bot": True, "url": f"{url}#{s}-{lv}", "body": lv, "level": lv} for s, lv in levels]
        )
        before = sweep.read_text()
        out = self.fill_sweep(sweep, self.write("c.json", "[]"), "--orchestrator-login", "o", code=1)
        self.assertEqual(
            ["annotation-warning", "annotation-failure", "status-failure", "status-error", "status-pending"],
            re.findall(r"^GAP (\S+)", out, re.MULTILINE),
        )
        self.assertIn("items 7 filled 2 gaps 5", out)
        self.assertEqual(before, sweep.read_text())

    def test_fill_sweep_ignores_a_disposition_reply_from_another_login(self):
        # a05 item 7: only a reply by --orchestrator-login supplies a disposition, and only that login's
        # "Disposition (orchestrator" comment takes the own-reply rule.
        url = "https://github.test/pull/9"
        own = {"source": "review_comment", "bot": False, "body": "Disposition (orchestrator): fixed"}
        sweep = self.sweep(
            [
                {"source": "review_comment", "bot": True, "url": f"{url}#discussion_r11", "body": "P1", "level": "P1"},
                {**own, "author": "mallory", "url": f"{url}#discussion_r22"},
                {**own, "author": "orch", "url": f"{url}#discussion_r23"},
            ]
        )
        before = sweep.read_text()

        def comments(login):
            reply = {"id": 21, "user": {"login": login}, "in_reply_to_id": 11, "body": "`fixed:abcdef1`"}
            return self.write("c.json", json.dumps([reply]))

        out = self.fill_sweep(sweep, comments("mallory"), "--orchestrator-login", "orch", code=1)
        self.assertIn("ignored-reply 21 mallory\n", out)
        self.assertEqual(["discussion_r11", "discussion_r22"], re.findall(r"^GAP (\S+)", out, re.MULTILINE))
        self.assertEqual(before, sweep.read_text())
        # The option's grammar: absent, without a value, malformed, or given twice is exit 2 before any write;
        # the last row repeats it where the comments path belongs, so the positional count alone would pass.
        c = comments("orch")
        for args in (
            (c,),
            (c, "--orchestrator-login"),
            (c, "--orchestrator-login", "has space"),
            (c, "--orchestrator-login", "x" * 40),
            (c, "--orchestrator-login", "o/r"),
            (c, "--orchestrator-login", "orch", "--orchestrator-login", "orch"),
            ("--orchestrator-login", "orch", "--orchestrator-login", "orch"),
        ):
            with self.subTest(args=args):
                self.assertEqual("", self.fill_sweep(sweep, *args, code=2))
                self.assertEqual(before, sweep.read_text())
        out = self.fill_sweep(sweep, comments("orch"), "--orchestrator-login", "orch", code=1)
        self.assertEqual(["discussion_r22"], re.findall(r"^GAP (\S+)", out, re.MULTILINE))
        self.fill_sweep(
            sweep, comments("orch"), self.write("x.tsv", "22\tfixed:abcdef2\n"), "--orchestrator-login", "orch"
        )
        dispositions = [i["disposition"] for i in json.loads(sweep.read_text())["items"]]
        self.assertEqual(["fixed:abcdef1", "fixed:abcdef2"], dispositions[:2])
        self.assertTrue(dispositions[2].startswith("not-applicable:the orchestrator disposition reply"), dispositions)

    def test_fill_sweep_leaves_a_badged_review_body_a_gap(self):
        # a05 item 8: a P0 to P3 badge in the Bot's image form makes a body a finding; a bare P0 is not a badge.
        url = "https://github.test/pull/9"
        sweep = self.sweep(
            [
                {
                    "source": "review",
                    "url": f"{url}#pullrequestreview-31",
                    "body": "![P1 Badge](https://b.test/p1) x",
                    "level": "commented",
                },
                {"source": "review", "url": f"{url}#pullrequestreview-32", "body": "x", "level": "commented"},
                {
                    "source": "issue_comment",
                    "url": f"{url}#issuecomment-33",
                    "body": '{"blockingSeverityThreshold":"P0"}',
                },
                {"source": "annotation", "url": f"{url}#annotation-34", "body": "![P3 Badge](x)", "level": "notice"},
            ]
        )
        comments = self.write("c.json", "[]")
        out = self.fill_sweep(sweep, comments, "--orchestrator-login", "o", code=1)
        self.assertEqual(["pullrequestreview-31", "annotation-34"], re.findall(r"^GAP (\S+)", out, re.MULTILINE))
        extra = self.write("x.tsv", "pullrequestreview-31\tfixed:abcdef1\nannotation-34\tfixed:abcdef2\n")
        self.fill_sweep(sweep, comments, extra, "--orchestrator-login", "o")
        self.assertEqual(
            [
                "fixed:abcdef1",
                "not-applicable:review object without a finding",
                "not-applicable:bot summary or onboarding comment, no finding",
                "fixed:abcdef2",
            ],
            [i["disposition"].split("; evidence=")[0] for i in json.loads(sweep.read_text())["items"]],
        )

    def test_fill_sweep_fills_only_a_commented_review(self):
        # The a02 record's owned row audit:046901b:1: a review that requests changes, approves or was dismissed
        # stays a gap, the Bot's own review too.
        url = "https://github.test/pull/9#pullrequestreview"
        levels = [("x", "commented"), ("x", "changes_requested"), ("x", "approved"), ("x", "dismissed")]
        levels += [("Codex Review", "commented"), ("Codex Review", "changes_requested")]
        sweep = self.sweep(
            [{"source": "review", "url": f"{url}-{n}", "body": b, "level": lv} for n, (b, lv) in enumerate(levels)]
        )
        out = self.fill_sweep(sweep, self.write("c.json", "[]"), "--orchestrator-login", "o", code=1)
        gaps = re.findall(r"^GAP (\S+)", out, re.MULTILINE)
        self.assertEqual(
            ["pullrequestreview-1", "pullrequestreview-2", "pullrequestreview-3", "pullrequestreview-5"], gaps
        )

    def test_fill_sweep_refuses_a_shared_url_key_and_takes_an_item_id(self):
        # The a02 record's owned rows audit:8576645:2 and audit:046901b:2: the annotations of one check run share
        # its URL, so a row for that URL fills none of them; `item#<n>` names one, and never an item whose fragment
        # is `item-0` (PR #361 thread 4277862537).
        url = "https://github.test/runs/7"
        items = [
            {"source": "annotation", "url": url, "body": lv, "level": lv} for lv in ("warning", "failure", "notice")
        ]
        items.append({"source": "status", "url": "https://ci.test/x#item-0", "body": "ci", "level": "failure"})
        sweep = self.sweep(items)
        comments = self.write("c.json", "[]")

        def fill(rows, code):
            return self.fill_sweep(sweep, comments, self.write("x.tsv", rows), "--orchestrator-login", "o", code=code)

        out = fill(f"{url}\tfixed:abcdef1\n", 1)
        self.assertEqual(
            [f"shared-key {url} item#{n}" for n in range(3)], re.findall(r"^shared-key .*", out, re.MULTILINE)
        )
        self.assertEqual(["item#0", "item#1", "item-0"], re.findall(r"^GAP (\S+)", out, re.MULTILINE))
        rows = "item#0\tfixed:abcdef1\nitem#1\tfixed:abcdef2\n"
        self.assertEqual(["item-0"], re.findall(r"^GAP (\S+)", fill(rows, 1), re.MULTILINE))
        fill(rows + "item-0\tfixed:abcdef3\n", 0)
        self.assertEqual(
            [
                "fixed:abcdef1",
                "fixed:abcdef2",
                f"not-applicable:runner capacity notice, no finding; evidence=jq '.items[2]' {sweep}",
                "fixed:abcdef3",
            ],
            [i["disposition"] for i in json.loads(sweep.read_text())["items"]],
        )

    def test_fill_sweep_sees_a_collision_after_the_discussion_r_strip(self):
        # The a05 record's owned row audit:2e77a33:2: a review fragment `discussion_r123` and a status fragment
        # `123` differ but share the lookup key `123`, so one row `123` fills neither; `item#<n>` takes over.
        url = "https://github.test/pull/9"
        sweep = self.sweep(
            [
                {"source": "review_comment", "url": f"{url}#discussion_r123", "body": "P1", "level": "P1"},
                {"source": "status", "url": "https://ci.test/x#123", "body": "ci", "level": "failure"},
            ]
        )
        before = sweep.read_text()
        comments = self.write("c.json", "[]")
        out = self.fill_sweep(
            sweep, comments, self.write("x.tsv", "123\tfixed:abcdef1\n"), "--orchestrator-login", "o", code=1
        )
        self.assertEqual(
            ["shared-key 123 item#0", "shared-key 123 item#1"], re.findall(r"^shared-key .*", out, re.MULTILINE)
        )
        self.assertEqual(["item#0", "item#1"], re.findall(r"^GAP (\S+)", out, re.MULTILINE))
        self.assertEqual(before, sweep.read_text())
        self.fill_sweep(
            sweep,
            comments,
            self.write("x.tsv", "item#0\tfixed:abcdef1\nitem#1\tfixed:abcdef2\n"),
            "--orchestrator-login",
            "o",
        )
        self.assertEqual(
            ["fixed:abcdef1", "fixed:abcdef2"], [i["disposition"] for i in json.loads(sweep.read_text())["items"]]
        )

    def test_fill_sweep_selects_a_null_url_status_by_source_and_check(self):
        # The a05 record's owned rows audit:e9404a6:2 and audit:39c186a:2: a status whose url is JSON null gets an
        # evidence command that selects it, not `select(.url == "None")`; PR #368 thread 4280648512: its context is
        # external, so a quote in it neither ends the jq argument nor runs the rest as shell code.
        item = {
            "source": "status",
            "url": None,
            "check": "Code'Rabbit\" $(touch pwned); touch pwned",
            "body": "CodeRabbit: skipped",
            "level": "success",
        }
        sweep = self.sweep([item])
        self.fill_sweep(sweep, self.write("c.json", "[]"), "--orchestrator-login", "o")
        [filled] = json.loads(sweep.read_text())["items"]
        reason, command = filled["disposition"].split("; evidence=")
        self.assertEqual("not-applicable:CI status, no finding", reason)
        self.assertTrue(command.startswith("jq --argjson s "), command)
        # The command, replayed, shows the item and nothing else runs.
        shown = subprocess.run(["bash", "-c", command], cwd=self.temp, capture_output=True, text=True, check=True)
        self.assertEqual(filled, json.loads(shown.stdout))
        self.assertFalse((self.temp / "pwned").exists())

    def test_fill_sweep_quotes_the_url_form_evidence(self):
        # PR #368 revise round 2 (the audit of cfebc1f): a status's url is its external target_url, so a quote in it
        # neither ends the jq argument nor runs the rest as shell or jq code when the evidence command is replayed.
        item = {
            "source": "status",
            "url": 'https://ci.test/x\'" $(touch pwned); touch pwned; echo "#7',
            "check": "ci",
            "body": "ci",
            "level": "success",
        }
        sweep = self.sweep([item])
        self.fill_sweep(sweep, self.write("c.json", "[]"), "--orchestrator-login", "o")
        [filled] = json.loads(sweep.read_text())["items"]
        reason, command = filled["disposition"].split("; evidence=")
        self.assertEqual("not-applicable:CI status, no finding", reason)
        self.assertTrue(command.startswith("jq --argjson u "), command)
        # The command, replayed, shows the item and nothing else runs.
        shown = subprocess.run(["bash", "-c", command], cwd=self.temp, capture_output=True, text=True, check=True)
        self.assertEqual(filled, json.loads(shown.stdout))
        self.assertFalse((self.temp / "pwned").exists())

    # orch-audit.sh

    def test_orch_audit_refuses_a_run_that_leaves_no_fresh_receipt(self):
        # a05 item 9: an earlier receipt of the audited head, here and tracked on main (so in the review
        # checkout too), never stands in for a run that wrote no new one.
        self.write("scripts/validate-agent-assets.py", "")
        self.origin("scripts/validate-agent-assets.py", "scripts/orchestrator/ledger-check.py")
        pr = self.temp / "pr"
        self.git("worktree", "add", "-q", "-b", "pr", str(pr), "main")
        self.git("commit", "-q", "--allow-empty", "-m", "change", cwd=pr)
        receipt = f".orchestration/validation/t-a01-audit-{self.git('rev-parse', 'HEAD', cwd=pr)[:7]}.md.last.md"
        self.write(receipt, "Verdict: correct\n")
        self.git("add", "--", receipt)
        self.git("commit", "-q", "-m", "earlier audit")
        self.git("push", "-q", "origin", "main")
        self.git("fetch", "-q", "origin")
        review = self.repo / ".claude/worktrees/orchestrator-review"
        self.git("worktree", "add", "-q", "--detach", str(review), "origin/main")
        (self.calls / "uv-output").write_text("")
        for mode in ("codex-silent", "codex-stale"):
            with self.subTest(mode=mode):
                (self.calls / mode).write_text("")
                result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, code=3)
                (self.calls / mode).unlink()
                self.assertIn("wrote no new", result.stderr)
                self.assertNotIn("Verdict", result.stdout)
                self.assertEqual("", self.git("status", "--porcelain", cwd=review))
        out = self.run_tool("orch-audit.sh", "t-a01", pr, 9).stdout
        self.assertTrue(out.endswith(": Verdict: correct\n"), out)

    def test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap(self):
        # Plan 007 T704 item 3: without --ledger-check, ledger-check.py beside the script runs on every audit.
        self.write("scripts/validate-agent-assets.py", "")
        self.origin("scripts/validate-agent-assets.py", "scripts/orchestrator/ledger-check.py")
        pr = self.temp / "pr"
        self.git("worktree", "add", "-q", "-b", "pr", str(pr), "main")
        self.git("commit", "-q", "--allow-empty", "-m", "change", cwd=pr)
        self.git("worktree", "add", "-q", "--detach", str(self.repo / ".claude/worktrees/orchestrator-review"), "main")
        # The uv stub runs a .python-version executable: this one drops `run --no-project` and runs python.
        shim = self.write("python-shim", f'#!/usr/bin/env bash\nshift 3\nexec "{sys.executable}" "$@"\n')
        shim.chmod(0o755)
        self.write(".python-version", f"{shim}\n")
        url = "https://github.test/pull/9#discussion_r"
        codex = {"source": "review_comment", "bot": True, "author": "chatgpt-codex-connector[bot]"}
        items = [{**codex, "url": f"{url}{n}", "disposition": "fixed:abcdef1"} for n in (4250000001, 4250000002)]
        self.write(".orchestration/validation/t-a01-pr-feedback.json", json.dumps({"pr": 9, "items": items}))
        self.write(".orchestration/acceptance/t-a01.md", "4250000001\tother\n")
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, code=3)
        self.assertIn("sweep gaps 0\nledger rows 1; findings 2; gaps 1\nGAP 4250000002\n", result.stdout)
        self.assertIn("the ledger is incomplete; refused", result.stderr)
        self.assertIsNone(self.call("codex"))
        # --ledger-check keeps its meaning: an override must name a script tracked in this repository.
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, "--ledger-check", shim, code=2)
        self.assertIn(f"{shim} is not a script tracked in this repository; refused", result.stderr)

    def test_orch_audit_runs_the_ledger_check_isolated_from_sibling_modules(self):
        # Round 2 (Bot thread 4279174373, the audit of b84e81f0): the ledger check runs under python -I, so an
        # untracked json.py beside it, which exits 9 when imported, is never imported and the audit passes.
        self.write("scripts/validate-agent-assets.py", "")
        self.origin("scripts/validate-agent-assets.py", "scripts/orchestrator/ledger-check.py")
        self.write("scripts/orchestrator/json.py", "raise SystemExit(9)\n")
        pr = self.temp / "pr"
        self.git("worktree", "add", "-q", "-b", "pr", str(pr), "main")
        self.git("commit", "-q", "--allow-empty", "-m", "change", cwd=pr)
        self.git("worktree", "add", "-q", "--detach", str(self.repo / ".claude/worktrees/orchestrator-review"), "main")
        shim = self.write("python-shim", f'#!/usr/bin/env bash\nshift 3\nexec "{sys.executable}" "$@"\n')
        shim.chmod(0o755)
        self.write(".python-version", f"{shim}\n")
        codex = {"source": "review_comment", "bot": True, "author": "chatgpt-codex-connector[bot]"}
        url = "https://github.test/pull/9#discussion_r4250000001"
        items = [{**codex, "url": url, "disposition": "fixed:abcdef1"}]
        self.write(".orchestration/validation/t-a01-pr-feedback.json", json.dumps({"pr": 9, "items": items}))
        self.write(".orchestration/acceptance/t-a01.md", "4250000001\tother\n")
        # The run stops later at this fixture's masker call; the ledger check before it has run and passed.
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, code=3)
        self.assertIn("sweep gaps 0\nledger rows 1; findings 1; gaps 0\n", result.stdout)
        self.assertNotIn("the ledger is incomplete", result.stderr)

    def test_orch_audit_refuses_a_ledger_check_that_differs_from_head(self):
        # Owned row audit:c1f60f7:2: the default ledger-check.py and an override are each run only when tracked and
        # unchanged from HEAD, as the validator is; a refusal runs neither the check nor codex.
        self.write("scripts/validate-agent-assets.py", "")
        self.write("other-check.py", "import sys\nsys.exit(0)\n")
        self.origin("scripts/validate-agent-assets.py", "scripts/orchestrator/ledger-check.py", "other-check.py")
        pr = self.temp / "pr"
        self.git("worktree", "add", "-q", "-b", "pr", str(pr), "main")
        self.git("commit", "-q", "--allow-empty", "-m", "change", cwd=pr)
        self.git("worktree", "add", "-q", "--detach", str(self.repo / ".claude/worktrees/orchestrator-review"), "main")
        shim = self.write("python-shim", f'#!/usr/bin/env bash\nshift 3\nexec "{sys.executable}" "$@"\n')
        shim.chmod(0o755)
        self.write(".python-version", f"{shim}\n")
        self.write(".orchestration/validation/t-a01-pr-feedback.json", json.dumps({"pr": 9, "items": []}))
        self.write(".orchestration/acceptance/t-a01.md", "")
        default = self.repo / "scripts/orchestrator/ledger-check.py"
        # Untracked: the default is checked as an override is.
        self.git("rm", "-q", "--cached", "--", "scripts/orchestrator/ledger-check.py")
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, code=2)
        self.assertIn(f"{default} is not a script tracked in this repository; refused", result.stderr)
        self.git("reset", "-q", "--", "scripts/orchestrator/ledger-check.py")
        with default.open("a") as edited:
            edited.write("# a local edit\n")
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, code=2)
        self.assertIn(f"{default} differs from HEAD; refused", result.stderr)
        self.assertNotIn("ledger rows", result.stdout)
        self.git("checkout", "-q", "--", "scripts/orchestrator/ledger-check.py")
        other = self.write("other-check.py", "import sys\nsys.exit(0)  # a local edit\n")
        result = self.run_tool("orch-audit.sh", "t-a01", pr, 9, "--ledger-check", other, code=2)
        self.assertIn(f"{other} differs from HEAD; refused", result.stderr)
        self.assertIsNone(self.call("codex"))

    # acceptance-front-matter.py, orch-gate.sh

    def front_matter(self, *args, code=0):
        script = str(self.repo / "scripts/orchestrator/acceptance-front-matter.py")
        result = subprocess.run(
            [sys.executable, "-I", script, "t-a01", "sweep.json", self.repo, *map(str, args)],
            cwd=self.repo,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(code, result.returncode, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def gate_module(self):
        spec = importlib.util.spec_from_file_location("gate", ROOT / "scripts/require-crit-review.py")
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        return gate

    def test_acceptance_front_matter_binds_head_and_pr_and_keeps_the_record(self):
        shutil.copy(ROOT / "scripts/require-crit-review.py", self.repo / "scripts/require-crit-review.py")
        self.write(".orchestration/learning/mistakes/M-1.md", "---\nclasses: [stale-path, other]\n---\n")
        self.write(".orchestration/learning/mistakes/M-2.md", "---\nclasses: [other]\n---\n")
        self.origin()
        head = self.git("rev-parse", "HEAD")
        self.write("sweep.json", json.dumps({"pr": 9, "head_sha": head, "items": []}))
        old = {
            "task": "t-a01",
            "dispatch": ["AGMSG-TASK v1 task_id=t-a01"],
            "ledger": [{"id": "4250000001", "class": "stale-path"}],
        }
        record = self.write(".orchestration/acceptance/t-a01.md", "---\n" + json.dumps(old) + "\n---\n\n# Record\n")
        rows = ["4250000001\tother", "4250000002\tstale-path", "audit:abcdef1:1\tstale-path", "4250000003\tother"]
        out = self.front_matter("--ledger", self.write("ledger.tsv", "\n".join(rows) + "\n"))
        self.assertIn("kept-ledger-row 4250000001", out)
        block, rest = self.gate_block(record)
        self.assertEqual(
            ("t-a01", head, 9, 1, "\n# Record\n"), (block["task"], block["head"], block["pr"], block["format"], rest)
        )
        self.assertEqual(old["dispatch"], block.get("dispatch"))
        self.assertEqual(["stale-path", "stale-path", "stale-path", "other"], [r["class"] for r in block["ledger"]])
        self.assertEqual([{"class": "stale-path", "records": ["M-1.md"]}], block["searches"])
        self.assertEqual([], block["audit_findings"])
        self.assertEqual([], self.gate_module().record_field_errors(block, "t-a01", head, 9))
        written = record.read_text()
        # A row the gate's field checks refuse, a sweep of another head and a record with a duplicate key are
        # refused, and nothing is written.
        self.assertIn("ledger row 4", self.front_matter("--ledger", self.write("bad.tsv", "42\tother\n"), code=1))
        self.assertEqual(written, record.read_text())
        self.write("sweep.json", json.dumps({"pr": 9, "head_sha": "0" * 40, "items": []}))
        self.assertIn("the sweep was collected for head", self.front_matter(code=1))
        self.assertEqual(written, record.read_text())
        self.write("sweep.json", json.dumps({"pr": 9, "head_sha": head, "items": []}))
        record.write_text('---\n{"task": "t-a01", "task": "t-a02"}\n---\n')
        self.assertIn("duplicate key task", self.front_matter(code=1))
        self.assertEqual('---\n{"task": "t-a01", "task": "t-a02"}\n---\n', record.read_text())

    def test_acceptance_front_matter_takes_audit_findings_only_for_an_incorrect_audit(self):
        shutil.copy(ROOT / "scripts/require-crit-review.py", self.repo / "scripts/require-crit-review.py")
        self.origin()
        head = self.git("rev-parse", "HEAD")
        self.write("sweep.json", json.dumps({"pr": 9, "head_sha": head, "items": []}))
        summary = self.write(
            f".orchestration/validation/t-a01-audit-{head[:7]}.md.last.md", "- [P1] high a.sh:1 x\nVerdict: incorrect\n"
        )
        record = self.repo / ".orchestration/acceptance/t-a01.md"
        reason = "advisory, owned by the follow-up task"
        dispositions = self.write("audit.tsv", f"1\t{reason}\tgrep -n x a.sh\n")
        self.assertIn("--audit-dispositions is required", self.front_matter(code=1))
        self.assertFalse(record.exists())
        wrong = self.write("wrong.tsv", f"2\t{reason}\tgrep -n x a.sh\n")
        self.assertIn("names finding 2", self.front_matter("--audit-dispositions", wrong, code=1))
        self.assertFalse(record.exists())
        self.front_matter("--audit-dispositions", dispositions)
        findings = self.gate_block(record)[0]["audit_findings"]
        self.assertEqual([{"n": "1", "reason": reason, "evidence": "grep -n x a.sh"}], findings)
        summary.write_text("Verdict: correct\n")
        self.assertIn(
            "--audit-dispositions is refused", self.front_matter("--audit-dispositions", dispositions, code=1)
        )
        self.front_matter()
        self.assertEqual([], self.gate_block(record)[0]["audit_findings"])

    def test_front_matter_keeps_and_validates_the_replans_object(self):
        # Plan 023 F1: the C-59 re-plans live in the block as replans; the rewrite keeps them, another shape is exit 2.
        shutil.copy(ROOT / "scripts/require-crit-review.py", self.repo / "scripts/require-crit-review.py")
        self.origin()
        head = self.git("rev-parse", "HEAD")
        self.write("sweep.json", json.dumps({"pr": 9, "head_sha": head, "items": []}))
        record = self.repo / ".orchestration/acceptance/t-a01.md"
        self.front_matter()
        self.assertEqual({}, self.gate_block(record)[0]["replans"])
        replan = {key: f"the {key} part" for key in ("specification", "design", "implementation", "verification")}
        record.write_text("---\n" + json.dumps({"task": "t-a01", "replans": {"stale-path": replan}}) + "\n---\n")
        self.front_matter()
        self.assertEqual({"stale-path": replan}, self.gate_block(record)[0]["replans"])
        for label, replans, key in (
            ("a list", ["stale-path"], "replans"),
            (
                "a missing part",
                {"stale-path": {k: v for k, v in replan.items() if k != "design"}},
                "replans.stale-path",
            ),
            ("an extra part", {"stale-path": {**replan, "notes": "more"}}, "replans.stale-path"),
            ("a blank part", {"stale-path": {**replan, "design": " "}}, "replans.stale-path"),
            ("a key that is no slug", {"Stale Path": replan}, "replans.Stale Path"),
        ):
            with self.subTest(label):
                text = "---\n" + json.dumps({"task": "t-a01", "replans": replans}) + "\n---\n"
                record.write_text(text)
                self.assertIn(f"{key} must be", self.front_matter(code=2))
                self.assertEqual(text, record.read_text())

    def gate(self, link=False, plant=False):
        """origin/main with the gate files, a PR head, the review worktree, evidence; the head tracks a symlink when
        `link`, and when `plant` a `.python-version` naming its own executable `pwn`, which touches `pwned`."""
        for rel in ("scripts/require-crit-review.py", "scripts/validate-agent-assets.py"):
            self.write(rel, "gate\n")
        self.write("scripts/pr-feedback.py", (ROOT / "scripts/pr-feedback.py").read_text())
        self.origin("scripts/require-crit-review.py", "scripts/validate-agent-assets.py", "scripts/pr-feedback.py")
        worktree = self.temp / "pr"
        self.git("worktree", "add", "-q", "-b", "pr", str(worktree), "main")
        v = ".orchestration/validation/t-a01"
        if link:
            (worktree / ".orchestration/validation").mkdir(parents=True)
            (worktree / f"{v}-crit.json").symlink_to(self.temp / "outside.txt")
            self.git("add", ".orchestration", cwd=worktree)
        if plant:
            (worktree / "pwn").write_text('#!/usr/bin/env bash\ntouch "$CALLS/pwned"\n')
            (worktree / "pwn").chmod(0o755)
            (worktree / ".python-version").write_text("./pwn\n")
            self.git("add", "pwn", ".python-version", cwd=worktree)
        self.git("commit", "-q", "--allow-empty", "-m", "change", cwd=worktree)
        head = self.git("rev-parse", "HEAD", cwd=worktree)
        self.git(
            "worktree", "add", "-q", "--detach", str(self.repo / ".claude/worktrees/orchestrator-review"), "origin/main"
        )
        self.write(f"{v}-pr-feedback.json", json.dumps({"pr": 9, "head_sha": head, "items": []}))
        for rel in (
            f"{v}-audit-{head[:7]}.md",
            f"{v}-audit-{head[:7]}.md.last.md",
            f"{v}-review-receipt.md",
            f"{v}-crit.json",
        ):
            self.write(rel, "x\n")
        self.write(".orchestration/acceptance/t-a01.md", "---\n{}\n---\n")
        (self.calls / "uv-output").write_text(f"{self.temp}/bin/gate-python\n")
        # env -i drops CALLS, so the gate interpreter's stub carries the calls directory itself.
        binding = f'[[ $* != *--gh-binding* ]] || exec "{self.binding.python}" "$@"\n'
        (self.temp / "bin/gate-python").write_text(
            STUBS["gate-python"].replace("#!/bin/bash\n", "#!/bin/bash\n" + binding).replace("$CALLS", str(self.calls))
        )
        (self.temp / "bin/uv").write_text(STUBS["uv"].replace("$CALLS", str(self.calls)))
        return worktree, head

    def run_gate(self, worktree, code=0):
        # The overrides a caller's shell may hold must not reach the gate.
        env = {"AUDIT_DISPOSITIONS": "retired.md", "CRIT_REVIEW": "off", "CRIT_REVIEWED": "1"}
        result = self.run_tool("orch-gate.sh", "t-a01", worktree, 9, code=code, env=env)
        review = self.repo / ".claude/worktrees/orchestrator-review"
        self.assertEqual("", self.git("status", "--porcelain", cwd=review))
        self.assertEqual(self.git("rev-parse", "origin/main"), self.git("rev-parse", "HEAD", cwd=review))
        return result

    def test_orch_gate_runs_this_checkouts_gate_on_the_review_worktree_with_the_gate_inputs(self):
        worktree, head = self.gate()
        self.run_gate(worktree)
        gate = str(self.repo / "scripts/require-crit-review.py")
        self.assertEqual(["-I", "-P", gate, "--base", "origin/main"], self.call("gate-python"))
        self.assertEqual(
            str(self.repo / ".claude/worktrees/orchestrator-review"),
            (self.calls / "gate-python-cwd").read_text().strip(),
        )
        env = (self.calls / "gate-python-env").read_text().splitlines()
        env = dict(line.split("=", 1) for line in env if "=" in line)
        v = ".orchestration/validation/t-a01"
        expected = {
            "ACCEPTANCE_EVIDENCE": ".orchestration/acceptance/t-a01.md",
            "AUDIT_EVIDENCE": f"{v}-audit-{head[:7]}.md",
            "PR_FEEDBACK_EVIDENCE": f"{v}-pr-feedback.json",
            "REVIEW_EVIDENCE": f"{v}-review-receipt.md",
            "AGENT_REVIEWED": "1",
        }
        self.assertEqual(expected, {k: env.get(k) for k in expected})
        # Names only: a failure must not print the environment's values.
        self.assertEqual([], [k for k in sorted(env) if k in ("AUDIT_DISPOSITIONS", "CRIT_REVIEW", "CRIT_REVIEWED")])

    def test_orch_gate_runs_the_gate_under_an_explicit_environment(self):
        worktree, _ = self.gate()
        # The private PATH is gone after the run, so the gate stub lists it while it runs.
        gate = self.temp / "bin/gate-python"
        gate.write_text(gate.read_text() + f'printf "%s\\n" "$PATH"/* > "{self.calls}/gate-python-bin"\n')
        startup = self.write("startup.py", "")
        leaked = {"PYTHONPATH": ".", "PYTHONSTARTUP": str(startup), "PYTHONHOME": str(self.temp)}
        self.run_tool("orch-gate.sh", "t-a01", worktree, 9, env={**leaked, "CRIT_REVIEW": "off", "CRIT_REVIEWED": "1"})
        env = (self.calls / "gate-python-env").read_text().splitlines()
        env = dict(line.split("=", 1) for line in env if "=" in line)
        allowed = {"PATH", "HOME", "PYTHONSAFEPATH", "AGENT_REVIEWED", "REVIEW_EVIDENCE", "PR_FEEDBACK_EVIDENCE"}
        allowed |= {"AUDIT_EVIDENCE", "ACCEPTANCE_EVIDENCE", "GH_TOKEN", "UV_CACHE_DIR"}
        # The names the stub's own bash exports; PWD last, as GitGuardian reads a string literal after it as a password.
        own = {"SHLVL", "_", "PWD"}
        # Names only, so a failure prints no value.
        self.assertEqual(sorted(allowed | own), sorted(env))
        # PATH is one private directory of links to gh and git, not the caller's PATH.
        self.assertEqual(1, len(env["PATH"].split(os.pathsep)))
        listed = (self.calls / "gate-python-bin").read_text().split()
        self.assertEqual([f"{env['PATH']}/gh", f"{env['PATH']}/git"], listed)
        expected = (self.env["HOME"], "1", "1")
        self.assertEqual(expected, (env["HOME"], env["PYTHONSAFEPATH"], env["AGENT_REVIEWED"]))
        self.assertEqual(["-I", "-P"], self.call("gate-python")[:2])

    def test_orch_gate_returns_the_gate_status_and_restores_the_review_worktree(self):
        worktree, _ = self.gate()
        (self.calls / "gate-python-fails").write_text("")
        self.assertIn("gate rc=2", self.run_gate(worktree, code=2).stdout)

    def test_orch_gate_pins_the_interpreter_before_entering_the_review_worktree(self):
        worktree, _ = self.gate(plant=True)
        self.run_gate(worktree)
        self.assertFalse((self.calls / "pwned").exists(), "the head's .python-version executable ran")
        self.assertEqual(["python", "find"], self.call("uv"))
        self.assertEqual(str(self.repo), (self.calls / "uv-cwd").read_text().strip())
        self.assertEqual("-I", self.call("gate-python")[0])

    def test_orch_gate_restores_the_review_worktree_when_setup_fails(self):
        worktree, _ = self.gate()
        # cp copies, then fails: the review worktree is at the head with partial evidence when the run stops.
        (self.temp / "bin/cp").write_text("#!/usr/bin/env bash\n" + RECORD.format(name="cp") + '/bin/cp "$@"\nexit 1\n')
        (self.temp / "bin/cp").chmod(0o755)
        self.run_gate(worktree, code=1)
        self.assertTrue(self.call("cp")[-1].startswith(str(self.repo / ".claude/worktrees/orchestrator-review")))
        self.assertIsNone(self.call("gate-python"))

    def test_orch_gate_refuses_another_prs_sweep_or_a_changed_gate_before_the_review_worktree_moves(self):
        worktree, head = self.gate()
        sweep = self.repo / ".orchestration/validation/t-a01-pr-feedback.json"
        gate = self.repo / "scripts/require-crit-review.py"
        for needle, path, text in (
            ("is not the sweep of PR 9", sweep, json.dumps({"pr": 8, "head_sha": head, "items": []})),
            ("the gate here differs from origin/main's", gate, "def main(): pass\n"),
        ):
            with self.subTest(needle=needle):
                kept = path.read_text()
                path.write_text(text)
                self.assertIn(needle, self.run_gate(worktree, code=2).stderr)
                path.write_text(kept)
                self.assertIsNone(self.call("uv"))

    def test_orch_gate_refuses_a_head_that_tracks_a_symlink_under_orchestration(self):
        (self.temp / "outside.txt").write_text("outside\n")
        worktree, _ = self.gate(link=True)
        self.assertIn("tracks a symlink under .orchestration", self.run_gate(worktree, code=2).stderr)
        self.assertEqual("outside\n", (self.temp / "outside.txt").read_text())
        self.assertIsNone(self.call("uv"))

    def test_orch_gate_leaves_the_review_worktree_as_it_was_on_a_refusal_before_the_checkout(self):
        # The a02 record's owned row audit:a235637:1: the shims refusal comes before the head's checkout, so the
        # trap moves nothing, here a review worktree that is clean but not at origin/main.
        worktree, head = self.gate()
        review = self.repo / ".claude/worktrees/orchestrator-review"
        self.git("checkout", "-q", "--detach", head, cwd=review)
        self.binding.declaration({"gh": {"version": "2.102.0", "path": "~/mise/shims/gh"}})
        result = self.run_tool("orch-gate.sh", "t-a01", worktree, 9, code=2)
        self.assertEqual("refused: gh binding", result.stderr.strip())
        self.assertEqual(head, self.git("rev-parse", "HEAD", cwd=review))
        self.assertEqual("", self.git("status", "--porcelain", cwd=review))
        self.assertIsNone(self.call("gate-python"))


if __name__ == "__main__":
    unittest.main()
