"""Exercise scripts/orchestrator/ledger-row.py (regime-cutover U222), the one writer of a coordinator row of
`ledger.tsv`: each kind composes its row from named arguments and the clock, the verdict and the verifier's fixed
words chosen by the kind, the ledger plus the new line re-read through `ledger.parse_ledger` before anything is
written, and the four shapes that cost a round refused by name. Every test runs over a scratch store (a ledger with
the header and three rows, `verdicts/`, `sweeps/`, a scratch HOME whose `.agents/agent-config.yaml` holds the pin and
whose `.agents/skills/security-audit/` holds the two validators the `daily` kind runs through a fake `node` first on
PATH; U597 round 7) as a subprocess under `python3 -I -S`, the form the coordinator runs."""

import concurrent.futures
import gc
import hashlib
import json
import os
import re
import resource
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
import warnings
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVERS = ROOT / "scripts/orchestrator"
WRITER = LEVERS / "ledger-row.py"
READER = LEVERS / "ledger.py"
HEADER = "ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence\n"
DAILY_HEADER = "ts\thead_sha\tverifier\tevidence\n"
A, B, C = "a" * 40, "b" * 40, "c" * 40
COMMIT = "d" * 40
DIGEST = "f" * 64
PIN = "c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def ts_ago(seconds):
    """A ts `seconds` before now (a negative count: after), in the store's form."""
    return (datetime.now(timezone.utc) - timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")


# The daily row's `--swept-at` (U597 round 6): the sweep's RESULT time, written as the row's ts; an hour before this
# module loaded, within the writer's 24-hour window for the run of these tests.
SWEPT_AT = ts_ago(3600)
# The daily task id is the UTC day the `--swept-at` falls on (U597 round 8): a unit id, or another day's id, is refused.
DAILY_DAY = SWEPT_AT[:10]
DAILY_TASK_ID = f"daily-{DAILY_DAY}"
# The two validators of the installed skill, the fake bytes the scratch HOME installs for each and their sha256 pins
# (round 8): the writer hashes each installed validator against the manifest's
# `assets.security-audit-skill.validators_sha256.<validator>` before `node` runs it.
VALIDATORS = ("validate-findings.cjs", "validate-coverage-ledger.cjs")
FAKE_VALIDATOR = "// the fake node answers for {validator}\n"
VALIDATOR_PINS = {
    validator: hashlib.sha256(FAKE_VALIDATOR.format(validator=validator).encode()).hexdigest()
    for validator in VALIDATORS
}
VALIDATORS_BLOCK = "    validators_sha256:\n" + "".join(
    f"      {validator}: {VALIDATOR_PINS[validator]}\n" for validator in VALIDATORS
)
MANIFEST = (
    "assets:\n"
    "  other-skill:\n"
    "    source: git-commit\n"
    "    pin: 0123456789abcdef0123456789abcdef01234567\n"
    "  security-audit-skill:\n"
    "    source: git-commit\n"
    "    upstream: cloudflare/security-audit-skill\n"
    f"    pin: {PIN}\n" + VALIDATORS_BLOCK + "claude:\n"
    "  levers:\n"
    "    sha256:\n"
    f"      brief-check.py: {'0' * 64}\n"
)
VERDICT_CORRECT = (
    "# Verdict\n\n## Findings\n\n- P2 (high) [f1 s3] tests/unit/test_x.py:3: a note\n\n"
    "Blocking: 0\nFiled: 1\nVerdict: correct\n"
)
VERDICT_INCORRECT = (
    "# Verdict\n\n## Findings\n\n- P1 (high) [f1 s10] scripts/x.sh:10: a hole\n\n"
    "Blocking: 1\nFiled: 3\nVerdict: incorrect\n"
)


# The fake `node` the daily kind's validators run under (U597 round 7): it logs its argv, its working directory, its
# environment and its stdin as one JSON line, then answers by the mode file beside the log (absent: exit 0 with a PASS
# line; `fail <validator>`: exit 1 with two stderr lines for that validator; `silent <validator>`: exit 3 with no
# stderr). The log and the mode are spelled into the script, since the writer hands node no environment but PATH.
FAKE_NODE = """#!{python}
import json, os, sys
with open({log!r}, "a", encoding="utf-8") as log:
    log.write(json.dumps({{"argv": sys.argv[1:], "cwd": os.getcwd(), "env": dict(os.environ), "stdin": sys.stdin.read()}}) + "\\n")
mode = ""
try:
    with open({mode!r}, encoding="utf-8") as handle:
        mode = handle.read().strip()
except FileNotFoundError:
    pass
name = os.path.basename(sys.argv[1]) if len(sys.argv) > 1 else ""
if mode == "fail " + name:
    sys.stderr.write(name + ": 2 validation errors\\nfindings[0]: severity is required\\n")
    sys.exit(1)
if mode == "silent " + name:
    sys.exit(3)
print("PASS " + name)
"""


def row(ts, unit, pr, head, verdict, verifier, evidence):
    return "\t".join((ts, unit, pr, head, verdict, verifier, evidence)) + "\n"


ROWS = (
    row("2026-11-01T01:00:00Z", "U7", "7", A, "pushed", "coordinator (by hand)", "the first head"),
    row("2026-11-01T02:00:00Z", "U7", "7", A, "correct", "pr-audit.sh (round 1)", "verdicts/U7-aaaaaaaa.md: ok"),
    row(
        "2026-11-01T03:00:00Z",
        "U7",
        "-",
        A,
        "sweep",
        f"security-audit-skill {PIN[:8]} (x)",
        "sweeps/U9-aaaaaaaa/findings.json; pr 7",
    ),
)


class LedgerRowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.store = root / "regime-cutover"
        (self.store / "verdicts").mkdir(parents=True)
        (self.store / "sweeps").mkdir()
        self.findings_dir("U9-bbbbbbbb")
        self.ledger = self.store / "ledger.tsv"
        self.ledger.write_text(HEADER + "".join(ROWS))
        self.home = root / "home"
        (self.home / ".agents").mkdir(parents=True)
        self.manifest = self.home / ".agents/agent-config.yaml"
        self.manifest.write_text(MANIFEST)
        # The installed skill's validators at the manifest's install path under the scratch HOME, and the fake node
        # first on PATH (round 7); the caller's NODE_OPTIONS and a canary must reach no validator.
        self.skill = self.home / ".agents/skills/security-audit"
        self.skill.mkdir(parents=True)
        for validator in VALIDATORS:
            (self.skill / validator).write_text(FAKE_VALIDATOR.format(validator=validator))
        self.bin = root / "bin"
        self.bin.mkdir()
        self.node_log = root / "node-calls.jsonl"
        self.node_mode = root / "node-mode"
        node = self.bin / "node"
        node.write_text(FAKE_NODE.format(python=sys.executable, log=str(self.node_log), mode=str(self.node_mode)))
        node.chmod(0o755)
        self.env = {
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "HOME": str(self.home),
            "LC_ALL": "C",
            "NODE_OPTIONS": "--require /nonexistent/preload.js",
            "SECRET_OF_THE_CALLER": "never reaches node",
        }
        self.writer = WRITER

    def findings_dir(self, name, content="[]\n"):
        """`sweeps/<name>/` with its findings file holding `content` and the coverage ledger beside it (round 7: the
        daily kind runs the skill's validator over each)."""
        directory = self.store / "sweeps" / name
        directory.mkdir()
        (directory / "findings.json").write_text(content)
        (directory / "coverage-ledger.json").write_text('{"units": []}\n')
        return directory

    def node_calls(self):
        """The fake node's calls so far, oldest first, each a dict of argv, cwd, env and stdin."""
        if not self.node_log.exists():
            return []
        return [json.loads(line) for line in self.node_log.read_text().splitlines()]

    def run_writer(self, *args, store=None, preexec_fn=None):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(self.writer), str(store or self.store), *args],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
            preexec_fn=preexec_fn,
        )

    def read(self, *args):
        return subprocess.run(
            [sys.executable, "-I", "-S", str(READER), str(self.store), *args],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )

    def assert_appended(self, args, unit, pr, head, verdict, verifier, evidence):
        """The lever appends exactly one line equal to the expected cells but for the ts, which is in TS_FORMAT and
        within the run; stdout names the ts and the line; the row is returned as a list of cells."""
        before = self.ledger.read_bytes()
        start = datetime.now(timezone.utc).replace(microsecond=0)
        run = self.run_writer(*args)
        end = datetime.now(timezone.utc)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        after = self.ledger.read_bytes()
        self.assertTrue(after.startswith(before), "the file is appended, never rewritten")
        added = after[len(before) :].decode()
        self.assertEqual(added.count("\n"), 1, added)
        cells = added[:-1].split("\t")
        self.assertEqual(len(cells), 7, cells)
        ts = cells[0]
        self.assertRegex(ts, TS)
        at = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        self.assertTrue(start <= at <= end, (start, at, end))
        self.assertEqual(cells[1:], [unit, pr, head, verdict, verifier, evidence])
        line = before.count(b"\n") + 1
        self.assertEqual(run.stdout, f"appended {ts} line {line}\n")
        return cells

    def assert_refused(self, args, *reasons, store=None):
        """Exit 2, one stderr line naming each reason, nothing on stdout, the ledger unchanged byte for byte."""
        target = (store or self.store) / "ledger.tsv"
        before = target.read_bytes()
        run = self.run_writer(*args, store=store)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith("ledger-row: refused: "), run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)
        self.assertEqual(target.read_bytes(), before, "nothing was written")
        return run.stderr

    # (a) one test per kind: the appended line equals the expected bytes but for the ts.

    def test_a_merged_row_has_verifier_pr_merge_sh_alone_and_the_receipt_as_evidence(self):
        receipt = f"merged pr=8 head=bbbbbbbb commit={COMMIT} verdict=2026-11-01T02:00:00Z"
        self.assert_appended(
            ("merged", "--pr", "8", "--head", B, "--unit", "U7", "--receipt", receipt),
            "U7",
            "8",
            B,
            "-",
            "pr-merge.sh",
            receipt,
        )
        receipt40 = f"merged pr=8 head={C} commit={COMMIT}"
        self.assert_appended(
            ("merged", "--pr", "8", "--head", C, "--unit", "U7", "--receipt", receipt40, "--note", "CI CLEAN; 1 round"),
            "U7",
            "8",
            C,
            "-",
            "pr-merge.sh",
            f"{receipt40}; CI CLEAN; 1 round",
        )

    def test_a_carried_row_has_the_digest_lever_s_line_as_a_whole_word_before_a_separator(self):
        line = f"carried {A} {B} {DIGEST}"
        self.assert_appended(
            (
                "carried",
                "--pr",
                "7",
                "--head",
                B,
                "--unit",
                "U7",
                "--line",
                line,
                "--note",
                "python3 -I -S from the checkout",
            ),
            "U7",
            "7",
            B,
            "carried",
            "audit-carry.py (python3 -I -S from the checkout)",
            line,
        )
        self.assert_appended(
            (
                "carried",
                "--pr",
                "7",
                "--head",
                B,
                "--unit",
                "U7",
                "--line",
                line,
                "--note",
                "n",
                "--evidence-note",
                "head moved by pr-update-branch.sh",
            ),
            "U7",
            "7",
            B,
            "carried",
            "audit-carry.py (n)",
            f"{line}; head moved by pr-update-branch.sh",
        )

    def test_a_sweep_row_takes_its_pin_word_from_the_manifest_and_its_fixed_evidence_form(self):
        args = (
            "sweep",
            "--head",
            B,
            "--unit",
            "U7b",
            "--seat",
            "sweep-2",
            "--run",
            "52",
            "--task",
            "U9",
            "--findings",
            "sweeps/U9-bbbbbbbb/findings.json",
            "--count",
            "0",
        )
        self.assert_appended(
            args,
            "U7b",
            "-",
            B,
            "sweep",
            f"security-audit-skill {PIN[:8]} (full audit mode on the srt worker seat sweep-2, run-52; TASK U9)",
            "sweeps/U9-bbbbbbbb/findings.json; pr none; 0 findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS",
        )
        self.assert_appended(
            (*args, "--pr", "7", "--count", "2"),
            "U7b",
            "-",
            B,
            "sweep",
            f"security-audit-skill {PIN[:8]} (full audit mode on the srt worker seat sweep-2, run-52; TASK U9)",
            "sweeps/U9-bbbbbbbb/findings.json; pr 7; 2 findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS",
        )

    def assert_daily_appended(self, args, head, verifier, evidence):
        """The `daily` kind appends exactly one row to `daily-sweeps.tsv` (made with its header when absent), the
        ledger untouched byte for byte; the row's ts is the `--swept-at` argument (round 6), the evidence the given
        text then `; recorded <ts>` with the recording time within the run; stdout names the ts and the line; the row
        is returned as a list of cells."""
        daily = self.store / "daily-sweeps.tsv"
        ledger_before = self.ledger.read_bytes()
        before = daily.read_bytes() if daily.exists() else DAILY_HEADER.encode()
        calls_before = len(self.node_calls())
        start = datetime.now(timezone.utc).replace(microsecond=0)
        run = self.run_writer(*args)
        end = datetime.now(timezone.utc)
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout + run.stderr)
        # round 7: the row is written after both validators ran, in order, over the findings file and the coverage
        # ledger beside it, from the installed skill directory alone (round 8: `--skill-dir` is gone)
        skill = self.skill
        findings = self.store / args[args.index("--findings") + 1]
        self.assertEqual(
            [call["argv"] for call in self.node_calls()[calls_before:]],
            [
                [str(skill / "validate-findings.cjs"), str(findings)],
                [str(skill / "validate-coverage-ledger.cjs"), str(findings.parent / "coverage-ledger.json")],
            ],
            "the two validators ran, in order, before the row was written",
        )
        after = daily.read_bytes()
        self.assertTrue(after.startswith(before), "the file is appended, never rewritten")
        added = after[len(before) :].decode()
        self.assertEqual(added.count("\n"), 1, added)
        cells = added[:-1].split("\t")
        self.assertEqual(len(cells), 4, cells)
        swept_at = args[args.index("--swept-at") + 1]
        self.assertEqual(cells[0], swept_at, "the row's ts is the sweep's own time, --swept-at (round 6)")
        self.assertEqual(cells[1:3], [head, verifier])
        prefix = f"{evidence}; recorded "
        self.assertTrue(cells[3].startswith(prefix), cells[3])
        recorded = cells[3][len(prefix) :]
        self.assertRegex(recorded, TS)
        at = datetime.strptime(recorded, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        self.assertTrue(start <= at <= end, (start, at, end))
        line = before.count(b"\n") + 1
        self.assertEqual(run.stdout, f"appended {swept_at} line {line}\n")
        self.assertEqual(self.ledger.read_bytes(), ledger_before, "the ledger is not the daily row's file")
        return cells

    def test_a_daily_row_writes_the_exact_row_of_daily_sweeps_tsv_making_the_file_with_its_header(self):
        """U597 round 4: the `daily` kind writes the one row of the store's `daily-sweeps.tsv`, main's head, the
        verifier of the `sweep` kind with the daily task id, the findings file and the count read from it (round 6:
        no `--count`; the ts is `--swept-at`, the evidence ends with the coordinator's `validators pass` and the
        recording time); the file is made with its header when absent and appended when present; the ledger is
        untouched; `ledger.py daily` reads the newest row back; a unit's id is refused as the task (round 8, verdict
        U597-a28e4793 P2 at ledger-row.py:468: the row that recorded `U9` here read back as the active daily exemption)
        and the second row is another run of the day's id, with its own findings file, since a findings file already
        recorded is refused (round 5), and another run number, since a recorded `(seat, run)` is refused too (round 6)."""
        daily = self.store / "daily-sweeps.tsv"
        args = (
            "daily",
            "--head",
            A,
            "--seat",
            "sweep-3",
            "--run",
            "170",
            "--task",
            DAILY_TASK_ID,
            "--findings",
            "sweeps/U9-bbbbbbbb/findings.json",
            "--swept-at",
            SWEPT_AT,
        )
        verifier = (
            f"security-audit-skill {PIN[:8]} (full audit mode on the srt worker seat sweep-3, run-170; "
            f"TASK {DAILY_TASK_ID})"
        )
        evidence = "sweeps/U9-bbbbbbbb/findings.json; 0 findings; validators pass"
        self.assertFalse(daily.exists())
        self.assert_daily_appended(args, A, verifier, evidence)
        text = daily.read_text()
        self.assertTrue(text.startswith(DAILY_HEADER), text)
        self.assertEqual(text.count("\n"), 2, "the header and one row")
        self.assertFalse(daily.is_symlink())
        self.findings_dir("U9-cccccccc", '[{"id": "F1"}, {"id": "F2"}]\n')
        # round 8: a unit id is no daily task; the arguments that recorded `U9` are refused naming the grammar, with
        # the file unchanged and no validator run
        before = daily.read_bytes()
        run = self.run_writer(
            *args[:5], "--run", "171", "--task", "U9", "--findings", "sweeps/U9-cccccccc/findings.json", *args[11:]
        )
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            "ledger-row: refused: the task 'U9' is not daily-<YYYY-MM-DD>, the coordinator's daily dispatch id; a daily"
            " row records the day's full sweep of main's head alone, and a unit's sweep is a sweep row of the ledger"
            " (the sweep kind)\n",
        )
        self.assertEqual(daily.read_bytes(), before, "nothing appended")
        self.assertEqual(len(self.node_calls()), 2, "no validator ran for the refused row")
        cells = self.assert_daily_appended(
            (*args[:5], "--run", "171", *args[7:9], "--findings", "sweeps/U9-cccccccc/findings.json", *args[11:]),
            A,
            verifier.replace("run-170", "run-171"),
            evidence.replace("U9-bbbbbbbb", "U9-cccccccc").replace("0 findings", "2 findings"),
        )
        self.assertEqual(daily.read_text().count("\n"), 3, "appended, the header once")
        run = self.read("daily", "86400")
        self.assertEqual((run.returncode, run.stderr), (0, ""), run.stdout)
        self.assertEqual(run.stdout, "\t".join(cells) + "\n", "the newest daily row, read back through the reader")
        self.assertEqual(
            sorted(entry.name for entry in self.store.iterdir()),
            ["daily-sweeps.tsv", "ledger.tsv", "sweeps", "verdicts"],
        )

    def test_a_daily_row_refuses_a_bad_head_pin_or_path_and_writes_nothing(self):
        """U597 round 4: every refusal of the `daily` kind is exit 2 with one stderr line, the daily file unchanged
        (or still absent) and the ledger unchanged: a head that is not 40 hex, a task that is not the daily id (a unit
        id included, round 8), a run that is no number, a seat of two words, a findings path outside `sweeps/`, with a `;` in its
        directory or naming no regular file, a manifest without the pin, a daily file that is a symlink, and a daily
        file the reader refuses (a malformed row), which is named with its line (the `--swept-at` refusals and the
        findings file's shape are their own tests, round 6)."""
        daily = self.store / "daily-sweeps.tsv"
        base = {
            "--head": A,
            "--seat": "sweep-3",
            "--run": "170",
            "--task": DAILY_TASK_ID,
            "--findings": "sweeps/U9-bbbbbbbb/findings.json",
            "--swept-at": SWEPT_AT,
        }

        def args(**changes):
            options = {**base, **{f"--{key}": value for key, value in changes.items()}}
            return ("daily", *(part for key, value in options.items() for part in (key, value)))

        def refused(arguments, *reasons):
            before = daily.read_bytes() if daily.exists() else None
            ledger_before = self.ledger.read_bytes()
            run = self.run_writer(*arguments)
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
            self.assertTrue(run.stderr.startswith("ledger-row: refused: "), run.stderr)
            for reason in reasons:
                self.assertIn(reason, run.stderr)
            self.assertEqual(daily.read_bytes() if daily.exists() else None, before, "the daily file is unchanged")
            self.assertEqual(self.ledger.read_bytes(), ledger_before, "the ledger is unchanged")

        for name, arguments, reason in (
            ("a short head", args(head=A[:8]), f"the head {A[:8]!r} is not 40 hex"),
            ("a dash head", args(head="-"), "the head '-' is not 40 hex"),
            ("an upper-case head", args(head=A.upper()), "is not 40 hex"),
            (
                "a task of another shape",
                args(task="daily-2026-1-19"),
                "the task 'daily-2026-1-19' is not daily-<YYYY-MM-DD>, the coordinator's daily dispatch id",
            ),
            (
                "a task that is a word",
                args(task="main"),
                "the task 'main' is not daily-<YYYY-MM-DD>, the coordinator's daily dispatch id",
            ),
            (
                "a task that is a unit id",
                args(task="U9"),
                "the task 'U9' is not daily-<YYYY-MM-DD>, the coordinator's daily dispatch id; a daily row records the "
                "day's full sweep of main's head alone, and a unit's sweep is a sweep row of the ledger (the sweep kind)",
            ),
            ("a run that is no number", args(run="x"), "the run 'x' is not a decimal number"),
            ("a seat of two words", args(seat="sweep 3"), "the seat 'sweep 3' is not one word"),
            (
                "a findings path outside sweeps/",
                args(findings="verdicts/U7-bbbbbbbb.md"),
                "is not sweeps/<dir>/findings.json under the store",
            ),
            (
                "a findings directory with a semicolon",
                args(findings="sweeps/U9;note/findings.json"),
                "is not sweeps/<dir>/findings.json under the store",
            ),
            (
                "a findings file that is missing",
                args(findings="sweeps/U9-missing/findings.json"),
                "is not a regular file under the store: No such file or directory",
            ),
            (
                "a findings path that is a directory",
                args(findings="sweeps/U9-bbbbbbbb/findings.json".replace("findings.json", "findings.json")),
                None,
            ),
        ):
            if reason is None:
                continue
            with self.subTest(name):
                refused(arguments, reason)
        self.assertFalse(daily.exists(), "no refusal before the write made the file")
        # the manifest without the pin: refused naming the manifest, the file still absent
        self.manifest.write_text(MANIFEST.replace(f"    pin: {PIN}\n", ""))
        refused(args(), "holds 0 assets.security-audit-skill.pin lines of 40 hex, not one")
        self.manifest.write_text(MANIFEST)
        self.assertFalse(daily.exists())
        # a symlink at the file's name is refused by the path rule, nothing written through it
        elsewhere = Path(self.temp.name) / "elsewhere.tsv"
        elsewhere.write_text(DAILY_HEADER)
        daily.symlink_to(elsewhere)
        refused(args(), "is a symbolic link")
        self.assertEqual(elsewhere.read_text(), DAILY_HEADER)
        daily.unlink()
        # a file the reader refuses is named with its line, unchanged
        daily.write_text(DAILY_HEADER + "garbage\n")
        refused(args(), f"{daily}:2: 1 columns, not 4")
        daily.write_text("ts\thead\n")
        refused(args(), f"{daily}:1: the header is 'ts\\thead', not")
        # a cell holding a tab is refused before anything is written, as for every kind
        daily.unlink()
        refused(args(seat="sweep\t3"), "holds a tab")
        self.assertFalse(daily.exists())

    DAILY_ARGS = (
        "daily",
        "--head",
        A,
        "--seat",
        "sweep-3",
        "--run",
        "170",
        "--task",
        DAILY_TASK_ID,
        "--findings",
        "sweeps/U9-bbbbbbbb/findings.json",
        "--swept-at",
        SWEPT_AT,
    )
    DAILY_VERIFIER = f"security-audit-skill {PIN[:8]} (full audit mode on the srt worker seat sweep-3, run-170; TASK {DAILY_TASK_ID})"
    DAILY_EVIDENCE = "sweeps/U9-bbbbbbbb/findings.json; 0 findings; validators pass"

    def test_a_daily_row_refuses_a_findings_path_an_existing_row_already_names(self):
        """U597 round 5 (verdict U597-1b3c4b1d P2 at ledger-row.py:408): the writer dated the row by the clock, not
        the sweep, so recording a finished run again refreshed the exemption's window without a new sweep. A
        `--findings` path any existing daily row names (the evidence's first `;`-separated field, stripped) is refused
        with one line naming that row's ts and line, the file unchanged byte for byte; another findings file of
        another run appends; a hand-written row with spaces around the path names it all the same."""
        daily = self.store / "daily-sweeps.tsv"
        first = self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        before = daily.read_bytes()
        for name, arguments in (
            ("the same arguments", self.DAILY_ARGS),
            ("another head and swept-at", (*self.DAILY_ARGS[:2], B, *self.DAILY_ARGS[3:-1], ts_ago(7200))),
            ("another run", (*self.DAILY_ARGS[:6], "171", *self.DAILY_ARGS[7:])),
        ):
            with self.subTest(name):
                run = self.run_writer(*arguments)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(
                    run.stderr,
                    "ledger-row: refused: the findings file sweeps/U9-bbbbbbbb/findings.json is already recorded by"
                    f" the daily sweep row of {first[0]} ({daily}:2); a finished run is not re-recorded to refresh the"
                    " window\n",
                )
                self.assertEqual(daily.read_bytes(), before, "the daily file is unchanged")
        # another findings file of another run is another sweep: appended
        self.findings_dir("daily-2026-11-20", '[{"id": "F1"}]\n')
        other = (
            *self.DAILY_ARGS[:5],
            "--run",
            "171",
            "--task",
            DAILY_TASK_ID,
            "--findings",
            "sweeps/daily-2026-11-20/findings.json",
            *self.DAILY_ARGS[11:],
        )
        self.assert_daily_appended(
            other,
            A,
            self.DAILY_VERIFIER.replace("run-170", "run-171"),
            "sweeps/daily-2026-11-20/findings.json; 1 findings; validators pass",
        )
        self.assertEqual(daily.read_text().count("\n"), 3)
        # a hand-written earlier row with spaces around the path still names the path (the field is stripped)
        daily.write_text(
            DAILY_HEADER
            + f"2026-11-19T01:00:00Z\t{B}\t{self.DAILY_VERIFIER}\t sweeps/U9-bbbbbbbb/findings.json ; 0 findings\n"
        )
        run = self.run_writer(*self.DAILY_ARGS)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(
            f"is already recorded by the daily sweep row of 2026-11-19T01:00:00Z ({daily}:2); a finished run",
            run.stderr,
        )
        self.assertEqual(daily.read_text().count("\n"), 2, "unchanged")

    def test_a_daily_row_refuses_a_seat_and_run_an_existing_row_already_records(self):
        """U597 round 6 (verdict U597-10d46fe0 P2 at ledger-row.py:791): round 5's guard keyed on the findings path
        alone, so the same run's findings copied to another path refreshed the window with the same head, seat, run
        and task. The `(seat, run)` an existing row's verifier carries (`seat <seat>, run-<n>;`, as the writer
        composes it) is refused with one line naming that row's ts and line, the file unchanged byte for byte,
        whatever the head or the time; another run of the seat and the same run of another seat append; a
        hand-written row whose verifier lacks the fields keys on its findings path alone."""
        daily = self.store / "daily-sweeps.tsv"
        first = self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        before = daily.read_bytes()
        for directory in ("daily-2026-11-19-run-170", "daily-2026-11-19-run-171", "daily-2026-11-19-run-170-b"):
            self.findings_dir(directory)
        swept = ts_ago(600)
        task = f"daily-{swept[:10]}"  # the day this swept-at falls on (round 8), the same as DAILY_DAY but at midnight
        verifier = self.DAILY_VERIFIER.replace(DAILY_TASK_ID, task)
        copied = (
            *self.DAILY_ARGS[:7],
            "--task",
            task,
            "--findings",
            "sweeps/daily-2026-11-19-run-170/findings.json",
            "--swept-at",
            swept,
        )
        for name, arguments in (
            ("the same seat and run under another findings path", copied),
            ("with another head too", (*copied[:2], B, *copied[3:])),
        ):
            with self.subTest(name):
                run = self.run_writer(*arguments)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(
                    run.stderr,
                    "ledger-row: refused: run-170 of the seat sweep-3 is already recorded by the daily sweep row of"
                    f" {first[0]} ({daily}:2); a finished run is not re-recorded under another findings path to"
                    " refresh the window\n",
                )
                self.assertEqual(daily.read_bytes(), before, "the daily file is unchanged")
        # another run of the seat appends, and the same run of another seat
        self.assert_daily_appended(
            (*copied[:6], "171", *copied[7:10], "sweeps/daily-2026-11-19-run-171/findings.json", *copied[11:]),
            A,
            verifier.replace("run-170", "run-171"),
            "sweeps/daily-2026-11-19-run-171/findings.json; 0 findings; validators pass",
        )
        self.assert_daily_appended(
            (*copied[:4], "sweep-4", *copied[5:]),
            A,
            verifier.replace("seat sweep-3,", "seat sweep-4,"),
            "sweeps/daily-2026-11-19-run-170/findings.json; 0 findings; validators pass",
        )
        self.assertEqual(daily.read_text().count("\n"), 4)
        # a hand-written earlier row without the seat and run fields keys on its path alone
        daily.write_text(
            DAILY_HEADER + f"2026-11-19T01:00:00Z\t{B}\tsecurity-audit-skill {PIN[:8]} (x)\t"
            "sweeps/daily-2026-11-19-run-170-b/findings.json; 0 findings\n"
        )
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        run = self.run_writer(*copied[:10], "sweeps/daily-2026-11-19-run-170-b/findings.json", *copied[11:])
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("is already recorded by the daily sweep row of 2026-11-19T01:00:00Z", run.stderr)
        self.assertIn("the findings file sweeps/daily-2026-11-19-run-170-b/findings.json", run.stderr)

    def test_a_daily_row_s_ts_is_its_swept_at_time_and_a_future_or_stale_one_is_refused(self):
        """U597 round 6 (verdict U597-10d46fe0 P2 at ledger-row.py:417): round 5 dated the row at recording time, so
        a delayed first recording granted a fresh 24-hour window to a sweep that finished outside it. The row's ts is
        `--swept-at`, the RESULT message's timestamp (the appended row and the receipt carry it; the recording time
        goes into the evidence as `recorded <ts>`), and `ledger.py daily` answers the row by it; a value later than
        the clock at the write is refused as in the future (round 7, verdict U597-301eba2e P3 at :453: round 6 let
        the writer accept 60 seconds ahead, the reader's allowance for rows another host's clock wrote, and this test
        accepted +30 s; the writer has no future slack, and the refusal says whose the allowance is), one more than 24
        hours before the clock as born stale, and a value off the strict form (one digit in a field, no `Z`, a space,
        hour 25, a word, nothing) is refused naming the form, each with one stderr line and no file made; the clock
        itself and 23 hours past are recorded."""
        daily = self.store / "daily-sweeps.tsv"

        def refused(value, *reasons):
            run = self.run_writer(*self.DAILY_ARGS[:-1], value)
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
            self.assertTrue(run.stderr.startswith("ledger-row: refused: --swept-at "), run.stderr)
            self.assertIn(value, run.stderr)
            for reason in reasons:
                self.assertIn(reason, run.stderr)
            self.assertFalse(daily.exists(), "a refusal makes no file")

        refused(ts_ago(-120), "is in the future: later than the clock ", "another host's clock, not for this writer")
        refused(ts_ago(-30), "is in the future: later than the clock ")
        refused(ts_ago(-2), "is in the future: later than the clock ")
        refused(ts_ago(-86400), "is in the future")
        self.assertNotIn(
            "plus 60", self.run_writer(*self.DAILY_ARGS[:-1], ts_ago(-30)).stderr, "no slack in the writer"
        )
        refused(ts_ago(86400 + 120), "is more than 86400 seconds (24 hours) before the clock ", "born stale")
        refused("2026-01-01T00:00:00Z", "born stale")
        for value in (
            "2026-11-9T4:5:6Z",
            "2026-11-19T10:00:00",
            "2026-11-19 10:00:00Z",
            "2026-11-19T25:00:00Z",
            "2026-11-19T10:00:00+00:00",
            "now",
            "",
        ):
            with self.subTest(value):
                refused(value, "is not YYYY-MM-DDThh:mm:ssZ")
        cells = self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        self.assertEqual(cells[0], SWEPT_AT)
        run = self.read("daily", "86400")
        self.assertEqual((run.returncode, run.stdout, run.stderr), (0, "\t".join(cells) + "\n", ""))
        # the clock itself (read before the run, so never after the writer's), and within the window: recorded under
        # their own runs and findings files
        for run_number, age in (("171", 0), ("172", 23 * 3600)):
            with self.subTest(age=age):
                swept = ts_ago(age)
                task = f"daily-{swept[:10]}"  # the task names the day this swept-at falls on (round 8)
                self.findings_dir(f"daily-2026-11-19-run-{run_number}")
                self.assert_daily_appended(
                    (
                        *self.DAILY_ARGS[:5],
                        "--run",
                        run_number,
                        "--task",
                        task,
                        "--findings",
                        f"sweeps/daily-2026-11-19-run-{run_number}/findings.json",
                        "--swept-at",
                        swept,
                    ),
                    A,
                    self.DAILY_VERIFIER.replace("run-170", f"run-{run_number}").replace(DAILY_TASK_ID, task),
                    f"sweeps/daily-2026-11-19-run-{run_number}/findings.json; 0 findings; validators pass",
                )

    def refused_daily(self, arguments, *reasons):
        """Exit 2, one stderr line naming each reason, no daily file; returns the validators the fake node ran."""
        daily = self.store / "daily-sweeps.tsv"
        run = self.run_writer(*arguments)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith("ledger-row: refused: "), run.stderr)
        for reason in reasons:
            self.assertIn(reason, run.stderr)
        self.assertFalse(daily.exists(), "a refusal makes no file")
        ran = [os.path.basename(call["argv"][0]) for call in self.node_calls()]
        self.node_log.unlink(missing_ok=True)
        return ran

    def test_a_daily_row_runs_the_installed_skill_s_two_validators_and_refuses_a_failing_or_missing_one(self):
        """U597 round 7 (verdict U597-301eba2e P2 at ledger-row.py:435): round 6 wrote `validators pass` after a
        JSON-shape check alone, so a findings set without the skill's required fields backed a daily exemption. After
        that check the writer runs the installed skill's validators itself, `node <skill>/validate-findings.cjs
        <findings>` and `node <skill>/validate-coverage-ledger.cjs <coverage-ledger.json beside it>`, `<skill>`
        `~/.agents/skills/security-audit` alone (the manifest's install; round 8: `--skill-dir` is gone and argparse
        refuses it), `node` the first on PATH, each from `/` with the environment reduced to PATH, stdin closed and
        its status read: both exiting 0 writes the row; a validator exiting non-zero is refused naming it, the file
        and its first stderr line (or `no stderr`), no daily file written and the second validator never run after
        the first failed; a missing coverage ledger, a missing skill directory, a skill directory without one
        validator and no node on PATH are refused the same way with no node run."""
        daily = self.store / "daily-sweeps.tsv"
        findings = self.store / "sweeps/U9-bbbbbbbb/findings.json"
        coverage = self.store / "sweeps/U9-bbbbbbbb/coverage-ledger.json"
        # the installed skill under HOME: two runs, in order, from `/`, PATH alone, stdin closed
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        calls = self.node_calls()
        self.assertEqual(
            [call["argv"] for call in calls],
            [
                [str(self.skill / "validate-findings.cjs"), str(findings)],
                [str(self.skill / "validate-coverage-ledger.cjs"), str(coverage)],
            ],
        )
        for call in calls:
            self.assertEqual(call["cwd"], "/", "a neutral working directory")
            self.assertEqual(call["stdin"], "", "stdin is closed")
            self.assertEqual(call["env"]["PATH"], self.env["PATH"])
            self.assertNotIn("NODE_OPTIONS", call["env"], "the caller's node options reach no validator")
            self.assertNotIn("SECRET_OF_THE_CALLER", call["env"], "the caller's environment reaches no validator")
            self.assertNotIn("HOME", call["env"])
        daily.unlink()
        self.node_log.unlink()
        refused = self.refused_daily
        # a failing validator: named with the file and its first stderr line; the second never runs after the first
        self.node_mode.write_text("fail validate-findings.cjs\n")
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                "validate-findings.cjs exited 1 on sweeps/U9-bbbbbbbb/findings.json: validate-findings.cjs: 2 validation"
                " errors; nothing is written",
            ),
            ["validate-findings.cjs"],
        )
        self.node_mode.write_text("fail validate-coverage-ledger.cjs\n")
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                "validate-coverage-ledger.cjs exited 1 on sweeps/U9-bbbbbbbb/coverage-ledger.json:"
                " validate-coverage-ledger.cjs: 2 validation errors; nothing is written",
            ),
            list(VALIDATORS),
        )
        self.node_mode.write_text("silent validate-findings.cjs\n")
        self.assertEqual(
            refused(self.DAILY_ARGS, "validate-findings.cjs exited 3 on sweeps/U9-bbbbbbbb/findings.json: no stderr"),
            ["validate-findings.cjs"],
        )
        self.node_mode.unlink()
        # no coverage ledger beside the findings file: refused by the store's path rule, no node run
        coverage.unlink()
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                f"the coverage ledger path {coverage} is not a regular file under the store: No such file or directory",
            ),
            [],
        )
        coverage.write_text('{"units": []}\n')
        # `--skill-dir` is gone (round 8): argparse refuses it before anything is read, no node run, no file
        run = self.run_writer(*self.DAILY_ARGS, "--skill-dir", str(self.skill))
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("unrecognized arguments: --skill-dir", run.stderr)
        self.assertFalse(daily.exists())
        self.assertEqual(self.node_calls(), [])
        # a missing skill directory under HOME, and a validator missing from it: refused naming the file, no node run
        aside = self.home / "skill-aside"
        shutil.move(self.skill, aside)
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                f"the validator {self.skill}/validate-findings.cjs is not a regular file of this user under the installed"
                f" skill ({self.skill}: No such file or directory); the daily row states 'validators pass' only after the"
                " pinned validator ran",
            ),
            [],
        )
        self.skill.mkdir()
        shutil.copy2(aside / "validate-findings.cjs", self.skill / "validate-findings.cjs")
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                f"the validator {self.skill}/validate-coverage-ledger.cjs is not a regular file of this user under the"
                f" installed skill ({self.skill}/validate-coverage-ledger.cjs: No such file or directory)",
            ),
            [],
        )
        shutil.rmtree(self.skill)
        shutil.move(aside, self.skill)
        # no node on PATH: refused naming it, nothing run
        empty = Path(self.temp.name).resolve() / "empty-bin"
        empty.mkdir()
        path = self.env["PATH"]
        self.env["PATH"] = str(empty)
        self.assertEqual(refused(self.DAILY_ARGS, "no node on PATH; the skill's validators run under it"), [])
        self.env["PATH"] = path
        # with everything in place the row is written
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        # the writer spells the run as this test describes it
        text = WRITER.read_text()
        self.assertIn('SKILL_DIR = "~/.agents/skills/security-audit"', text)
        self.assertIn('VALIDATOR_CWD = "/"', text)
        self.assertIn('env={"PATH": os.environ.get("PATH", "")},', text)
        self.assertIn("stdin=subprocess.DEVNULL,", text)
        self.assertIn("timeout=VALIDATOR_TIMEOUT,", text)
        self.assertNotIn('"--skill-dir"', text, "the option is gone (round 8)")

    def test_a_daily_row_holds_each_validator_to_its_manifest_pin_before_it_runs(self):
        """U597 round 8 (verdict U597-a28e4793 P2 at ledger-row.py:489 and P3 at :522): round 7 stamped the manifest's
        skill pin but took the validators from any `--skill-dir` without authenticating their bytes, so a passing exit
        established nothing of the pinned validators, and a relative directory could pass the file checks and fail
        node's resolution from `/`. Each validator is read from `~/.agents/skills/security-audit/` alone (HOME
        expanded, an absolute path, every component below HOME `lstat`ed and no symlink, the file opened with no link
        followed and a regular file of this user) and its sha256 compared with the manifest's
        `assets.security-audit-skill.validators_sha256.<validator>` before `node` runs it: the pinned bytes pass with
        the fake node, run from the installed path; a validator with one more byte refuses naming the file and both
        digests with no node run and nothing written; a manifest without the block, without one key, with a key twice
        or with a digest of 63 hex, and one whose block sits under another asset, refuses naming the key; `--manifest
        <path>` names the manifest read, so a file holding the pins passes while HOME's lacks them, and a missing one
        refuses naming it; a symbolic link at the skill directory or at the validator refuses naming the component;
        a HOME that is no absolute path refuses."""
        daily = self.store / "daily-sweeps.tsv"
        findings_validator = self.skill / "validate-findings.cjs"
        coverage_validator = self.skill / "validate-coverage-ledger.cjs"
        refused = self.refused_daily
        # the pinned bytes pass with the fake node, run from the installed path
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        self.assertEqual(
            [call["argv"][0] for call in self.node_calls()], [str(findings_validator), str(coverage_validator)]
        )
        daily.unlink()
        self.node_log.unlink()
        # a validator whose bytes differ from the pin: refused naming the file and both digests, no node run
        for validator in VALIDATORS:
            with self.subTest(validator=validator):
                path = self.skill / validator
                original = path.read_bytes()
                changed = original + b"// one more line\n"
                path.write_bytes(changed)
                self.assertEqual(
                    refused(
                        self.DAILY_ARGS,
                        f"sha256 {hashlib.sha256(changed).hexdigest()} of the validator {path} differs from the pin"
                        f" {VALIDATOR_PINS[validator]} of assets.security-audit-skill.validators_sha256.{validator} in"
                        f" {self.manifest}; the installed skill is not the pinned one, so nothing is written",
                    ),
                    [],
                )
                path.write_bytes(original)
        # a manifest without the keys: refused naming the key, no node run
        findings_pin = VALIDATOR_PINS["validate-findings.cjs"]
        coverage_line = f"      validate-coverage-ledger.cjs: {VALIDATOR_PINS['validate-coverage-ledger.cjs']}\n"
        for name, manifest_text, message in (
            (
                "no validators_sha256 block",
                MANIFEST.replace(VALIDATORS_BLOCK, ""),
                "holds 0 assets.security-audit-skill.validators_sha256.validate-findings.cjs lines of 64 hex, not one",
            ),
            (
                "one key missing",
                MANIFEST.replace(coverage_line, ""),
                "holds 0 assets.security-audit-skill.validators_sha256.validate-coverage-ledger.cjs lines of 64 hex",
            ),
            (
                "one key twice",
                MANIFEST.replace(VALIDATORS_BLOCK, VALIDATORS_BLOCK + f"      validate-findings.cjs: {'0' * 64}\n"),
                "holds 2 assets.security-audit-skill.validators_sha256.validate-findings.cjs lines of 64 hex",
            ),
            (
                "a digest of 63 hex",
                MANIFEST.replace(findings_pin, findings_pin[:63]),
                "holds 0 assets.security-audit-skill.validators_sha256.validate-findings.cjs lines of 64 hex",
            ),
            (
                "the block under another asset",
                MANIFEST.replace(VALIDATORS_BLOCK, "").replace(
                    "  other-skill:\n    source: git-commit\n",
                    "  other-skill:\n    source: git-commit\n" + VALIDATORS_BLOCK,
                ),
                "holds 0 assets.security-audit-skill.validators_sha256.validate-findings.cjs lines of 64 hex",
            ),
        ):
            with self.subTest(name):
                self.manifest.write_text(manifest_text)
                self.assertEqual(refused(self.DAILY_ARGS, message, str(self.manifest)), [])
        self.manifest.write_text(MANIFEST)
        # --manifest names the manifest read: a file holding the pins passes while HOME's lacks them; a missing one
        # refuses naming it
        other = Path(self.temp.name).resolve() / "other-manifest.yaml"
        other.write_text(MANIFEST)
        self.manifest.write_text(MANIFEST.replace(VALIDATORS_BLOCK, ""))
        self.assert_daily_appended(
            (*self.DAILY_ARGS, "--manifest", str(other)), A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE
        )
        daily.unlink()
        self.node_log.unlink()
        self.assertEqual(
            refused(
                (*self.DAILY_ARGS, "--manifest", f"{other}.missing"),
                f"cannot read the manifest {other}.missing: No such file or directory",
            ),
            [],
        )
        self.manifest.write_text(MANIFEST)
        # a symbolic link at the skill directory, then at the validator itself (to a file of the pinned bytes)
        aside = self.home / "skill-aside"
        shutil.move(self.skill, aside)
        self.skill.symlink_to(aside)
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                f"{self.skill}, a component of the validator path {findings_validator}, is a symbolic link; the"
                " installed skill is read through real directories alone",
            ),
            [],
        )
        self.skill.unlink()
        shutil.move(aside, self.skill)
        linked = self.home / "linked-validator.cjs"
        shutil.copy2(findings_validator, linked)
        findings_validator.unlink()
        findings_validator.symlink_to(linked)
        self.assertEqual(
            refused(
                self.DAILY_ARGS,
                f"{findings_validator}, a component of the validator path {findings_validator}, is a symbolic link",
            ),
            [],
        )
        findings_validator.unlink()
        shutil.copy2(linked, findings_validator)
        # a HOME that is no absolute path: the manifest named, the validator path refused
        home = self.env["HOME"]
        self.env["HOME"] = "relative/home"
        self.assertEqual(
            refused((*self.DAILY_ARGS, "--manifest", str(other)), "HOME 'relative/home' is not an absolute path"),
            [],
        )
        self.env["HOME"] = home
        # with everything restored the row is written
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        # the writer spells the read as this test describes it
        text = WRITER.read_text()
        self.assertIn('SKILL_PARTS = (".agents", "skills", "security-audit")', text)
        self.assertIn('VALIDATORS_KEY = "validators_sha256"', text)
        self.assertIn("descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)", text)
        self.assertIn("digest = hashlib.sha256(data).hexdigest()", text)
        self.assertIn("if digest != pins[validator]:", text)

    def test_a_daily_row_s_task_is_the_daily_id_of_the_swept_at_day_alone(self):
        """U597 round 8 (verdict U597-a28e4793 P2 at ledger-row.py:468): the daily writer accepted an ordinary unit's
        task, so a unit's scoped sweep could be read back as the active daily exemption of main's head. The task is
        `daily-<YYYY-MM-DD>` alone, the UTC day the `--swept-at` falls on: a unit id (`U9`, `U9b`), a word, an
        unpadded date and the daily id with another day are each refused naming the grammar or both days, with one
        stderr line, no file and no validator run; the matching day passes, and a `--swept-at` of 23 hours ago passes
        under its own day's id."""
        daily = self.store / "daily-sweeps.tsv"
        refused = self.refused_daily

        def arguments(task, swept_at=SWEPT_AT):
            return (*self.DAILY_ARGS[:7], "--task", task, *self.DAILY_ARGS[9:11], "--swept-at", swept_at)

        grammar = (
            "is not daily-<YYYY-MM-DD>, the coordinator's daily dispatch id; a daily row records the day's full sweep"
            " of main's head alone, and a unit's sweep is a sweep row of the ledger (the sweep kind)"
        )
        for task in ("U9", "U9b", "main", "daily-2026-1-19", "Daily-2026-11-19", f"{DAILY_TASK_ID} "):
            with self.subTest(task=task):
                self.assertEqual(refused(arguments(task), f"the task {task!r} {grammar}"), [])
        other_day = (datetime.strptime(DAILY_DAY, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertEqual(
            refused(
                arguments(f"daily-{other_day}"),
                f"the task daily-{other_day} names another day than --swept-at {SWEPT_AT} ({DAILY_DAY} UTC); the daily"
                f" id is daily-{DAILY_DAY}, the day the sweep's RESULT falls on",
            ),
            [],
        )
        self.assertFalse(daily.exists())
        # the matching day passes; 23 hours ago passes under its own day's id, and under today's id only when the
        # days agree
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        swept = ts_ago(23 * 3600)
        task = f"daily-{swept[:10]}"
        self.findings_dir("daily-earlier-run-171")
        earlier = (
            *self.DAILY_ARGS[:5],
            "--run",
            "171",
            "--task",
            task,
            "--findings",
            "sweeps/daily-earlier-run-171/findings.json",
            "--swept-at",
            swept,
        )
        if swept[:10] != DAILY_DAY:
            run = self.run_writer(*earlier[:7], "--task", DAILY_TASK_ID, *earlier[9:])
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertIn(f"names another day than --swept-at {swept}", run.stderr)
        self.assert_daily_appended(
            earlier,
            A,
            self.DAILY_VERIFIER.replace("run-170", "run-171").replace(DAILY_TASK_ID, task),
            "sweeps/daily-earlier-run-171/findings.json; 0 findings; validators pass",
        )
        # the writer spells the grammar once
        text = WRITER.read_text()
        self.assertIn('DAILY_TASK = re.compile(r"^daily-([0-9]{4}-[0-9]{2}-[0-9]{2})$")', text)
        self.assertNotIn("not UNIT.match(args.task) and not DAILY_TASK.match(args.task)", text, "no unit task")

    def test_a_failed_findings_read_is_refused_and_leaves_no_daily_file(self):
        """U597 round 7 (verdict U597-301eba2e P3 at ledger-row.py:509): the writer caught a failed findings read, and
        round 6 tested malformed bytes and failed writes, not the read. A findings file this user cannot open (mode
        000; skipped for root, who opens anything) and an `os.read` raising EIO under the descriptor are each refused
        with one stderr line naming the file and the error, exit 2, no daily file written, no validator run, the
        store's entries as they were."""
        daily = self.store / "daily-sweeps.tsv"
        findings = self.store / "sweeps/U9-bbbbbbbb/findings.json"
        before = self.store_listing()
        if os.geteuid() != 0:
            findings.chmod(0)
            run = self.run_writer(*self.DAILY_ARGS)
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertEqual(
                run.stderr,
                "ledger-row: refused: cannot open the findings file sweeps/U9-bbbbbbbb/findings.json: Permission denied\n",
            )
            self.assertFalse(daily.exists(), "a failed findings read leaves no daily file")
            self.assertEqual(self.node_calls(), [], "no validator ran over a file that could not be read")
            findings.chmod(0o644)
        run = self.inject("read", *self.DAILY_ARGS)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            "ledger-row: refused: cannot read the findings file sweeps/U9-bbbbbbbb/findings.json: Input/output error\n",
        )
        self.assertFalse(daily.exists(), "a failed findings read leaves no daily file")
        self.assertEqual(self.node_calls(), [])
        self.assertEqual(self.store_listing(), before, "no file but the ledger, nothing changed")
        # without the fault the same arguments write the row
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)

    def test_a_control_character_in_an_argument_or_a_cell_is_refused_by_the_writer_and_the_reader_alike(self):
        """U597 round 7 (verdict U597-301eba2e P2 at ledger.py:361): a NUL in a daily row's evidence path was data to
        the reader, and bash's `$(...)` drops a NUL when pr-merge.sh captures the row, so the lever would have checked
        another file than the one the row names. The reader refuses any cell holding `\\x00` to `\\x1f` or `\\x7f` as
        Malformed naming the line and the column, and the writer's argument rule refuses such a character before
        argparse runs, naming it (a `\\x01` in `--what`, a DEL in a note, an escape in the seat; the tab and the line
        breaks keep their names); a daily file or a ledger holding one is a malformed store to the writer and to
        `ledger.py`, named with its line and column, nothing written."""
        daily = self.store / "daily-sweeps.tsv"
        before = self.ledger.read_bytes()
        for name, arguments, label in (
            ("U+0001 in --what", (*self.PUSHED, "--what", "a\x01b"), "a control character U+0001"),
            (
                "a DEL in a note",
                ("merged", "--pr", "8", "--head", B, "--unit", "U7", "--receipt", "r", "--note", "x\x7fy"),
                "a control character U+007F",
            ),
            (
                "an escape in the seat",
                (*self.DAILY_ARGS[:4], "sweep\x1b3", *self.DAILY_ARGS[5:]),
                "a control character U+001B",
            ),
            ("a tab, by its name", (*self.PUSHED, "--what", "a\tb"), "a tab"),
        ):
            with self.subTest(name):
                run = self.run_writer(*arguments)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(
                    f"holds {label}; a cell holds neither a tab, a newline nor a control character", run.stderr
                )
                self.assertEqual(self.ledger.read_bytes(), before)
                self.assertFalse(daily.exists())
        # a daily file holding a NUL in an evidence path: a malformed store to the writer and to the reader
        daily.write_text(
            DAILY_HEADER
            + f"2026-11-19T01:00:00Z\t{B}\t{self.DAILY_VERIFIER}\tsweeps/U9-bbbbbbbb/find\x00ings.json; 0 findings\n"
        )
        malformed = f"{daily}:2: column 4 (evidence) holds a control character U+0000; no cell holds one"
        run = self.run_writer(*self.DAILY_ARGS)
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr, f"ledger-row: refused: {malformed}\n")
        self.assertEqual(daily.read_text().count("\n"), 2, "unchanged")
        run = self.read("daily", "86400")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(malformed, run.stderr)
        # the ledger too: a NUL in an evidence cell is named with its line, and nothing is written
        self.ledger.write_text(HEADER + ROWS[0] + row("2026-11-01T02:00:00Z", "U7", "7", A, "pushed", "c", "x\x00y"))
        held = self.ledger.read_bytes()
        run = self.run_writer(*self.PUSHED, "--what", "w")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(
            run.stderr,
            f"ledger-row: refused: {self.ledger}:3: column 7 (evidence) holds a control character U+0000; no cell holds one\n",
        )
        self.assertEqual(self.ledger.read_bytes(), held)

    def test_a_daily_row_reads_its_count_from_the_findings_file_and_refuses_another_shape(self):
        """U597 round 6 (verdict U597-10d46fe0 P2 at ledger-row.py:416): round 5 took `--count` as an argument and
        stated both validators' PASS after checking that the findings file existed, so invalid or truncated JSON
        backed a daily exemption. The writer opens the findings file it names, parses it as JSON and requires a list
        whose every element is an object: the list's length is the count (three objects are `3 findings`), the
        validators' words are the coordinator's one statement `validators pass`, and a file that is not UTF-8, not
        JSON, truncated, an object, a string, a number, null, or a list holding a number, null, a string, a list or a
        boolean is refused with one line naming the file, no daily file made; `--count` is no argument of the daily
        kind (argparse's exit 2), while the `sweep` kind keeps it."""
        daily = self.store / "daily-sweeps.tsv"
        findings = self.store / "sweeps/U9-bbbbbbbb/findings.json"
        for name, content, reason in (
            ("not UTF-8", b"\xff\n", "is not UTF-8"),
            ("an empty file", b"", "is not JSON"),
            ("truncated JSON", b'[{"id": "F1"}', "is not JSON"),
            ("text", b"3 findings\n", "is not JSON"),
            ("an object", b'{"findings": []}\n', "is not a JSON list of findings but an object"),
            ("a string", b'"[]"\n', "is not a JSON list of findings but a string"),
            ("a number", b"3\n", "is not a JSON list of findings but a number"),
            ("null", b"null\n", "is not a JSON list of findings but null"),
            ("a boolean", b"true\n", "is not a JSON list of findings but a boolean"),
            ("a list holding a number", b"[1]\n", "holds a number at index 0, not an object"),
            ("a list holding null after an object", b"[{}, null]\n", "holds null at index 1, not an object"),
            ("a list holding a string", b'[{}, "F1"]\n', "holds a string at index 1, not an object"),
            ("a list holding a list", b"[[]]\n", "holds a list at index 0, not an object"),
            ("a list holding a boolean", b"[{}, {}, false]\n", "holds a boolean at index 2, not an object"),
        ):
            with self.subTest(name):
                findings.write_bytes(content)
                run = self.run_writer(*self.DAILY_ARGS)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertTrue(
                    run.stderr.startswith("ledger-row: refused: the findings file sweeps/U9-bbbbbbbb/findings.json "),
                    run.stderr,
                )
                self.assertIn(reason, run.stderr)
                self.assertFalse(daily.exists(), "a refusal makes no file")
                self.assertEqual(self.node_calls(), [], "the shape check is the first gate: no validator ran (round 7)")
        # --count is gone from the daily kind: argparse refuses it before anything is read
        findings.write_text("[]\n")
        run = self.run_writer(*self.DAILY_ARGS, "--count", "0")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("unrecognized arguments: --count 0", run.stderr)
        self.assertFalse(daily.exists())
        # three objects are three findings to the count, whatever their fields; the fields are the validators' to judge
        # (round 7), and the fake passes them here
        findings.write_text('[{"id": "F1"}, {"id": "F2", "severity": "P3"}, {}]\n')
        self.assert_daily_appended(
            self.DAILY_ARGS, A, self.DAILY_VERIFIER, "sweeps/U9-bbbbbbbb/findings.json; 3 findings; validators pass"
        )
        # the sweep kind keeps its count argument and its evidence form
        self.assert_appended(
            self.sweep_args(),
            "U7",
            "-",
            B,
            "sweep",
            f"security-audit-skill {PIN[:8]} (full audit mode on the srt worker seat s, run-1; TASK U9)",
            "sweeps/U9-bbbbbbbb/findings.json; pr none; 0 findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS",
        )

    def inject_short_write(self, *args):
        """The lever under `python3 -I -S` with `os.write` replaced by one that lands the first two bytes alone (the
        auditor's fault injection of verdict U597-1b3c4b1d; round 5)."""
        injection = (
            "import os, runpy, sys\n"
            "real = os.write\n"
            "def short(descriptor, data, *rest):\n"
            "    return real(descriptor, data[:2], *rest)\n"
            "os.write = short\n"
            "sys.argv = sys.argv[1:]\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')\n"
        )
        return subprocess.run(
            [sys.executable, "-I", "-S", "-c", injection, str(self.writer), str(self.store), *args],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
        )

    def test_a_short_first_write_of_the_daily_file_leaves_no_file_and_the_rerun_writes_it(self):
        """U597 round 5 (verdict U597-1b3c4b1d P2 at ledger-row.py:506): round 4 made the file with `O_EXCL` and wrote
        the header through it, so a short write left a malformed `daily-sweeps.tsv` that the rerun refused and never
        repaired. The first file is now the header and the row written whole into a temporary file of the store
        directory and renamed onto the name: an `os.write` that lands two bytes is exit 1, one stderr line naming the
        file and the short write, and the store holds no `daily-sweeps.tsv` and no temporary file; an injected
        `fsync`, `replace` or `fchmod` failure leaves the same; the rerun writes the whole file, mode 0644; and a file
        whose header is malformed (an empty file, a wrong header) is refused naming line 1 and left as it is, never
        repaired; a later row is appended as one write, the first file untouched before it."""
        daily = self.store / "daily-sweeps.tsv"
        before = self.store_listing()
        run = self.inject_short_write(*self.DAILY_ARGS)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(f"ledger-row: cannot write {daily}: short write, 2 of "), run.stderr)
        self.assertIn(
            " bytes; the temporary file is removed and no daily-sweeps.tsv exists; the rerun writes it again\n",
            run.stderr,
        )
        self.assertFalse(daily.exists(), "no malformed file is left for the rerun to refuse")
        self.assertEqual(self.store_listing(), before, "no file but the ledger, and no temporary file")
        for function in ("fsync", "replace", "fchmod"):
            with self.subTest(function):
                run = self.inject(function, *self.DAILY_ARGS)
                self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertTrue(run.stderr.startswith(f"ledger-row: cannot write {daily}: "), run.stderr)
                self.assertIn("Input/output error; the temporary file is removed", run.stderr)
                self.assertFalse(daily.exists())
                self.assertEqual(self.store_listing(), before)
        # the rerun writes the whole file, the header and the row, mode 0644, nothing else in the store
        self.assert_daily_appended(self.DAILY_ARGS, A, self.DAILY_VERIFIER, self.DAILY_EVIDENCE)
        self.assertEqual(daily.read_text().count("\n"), 2)
        self.assertEqual(stat.S_IMODE(daily.stat().st_mode), 0o644)
        self.assertEqual(
            sorted(entry.name for entry in self.store.iterdir()),
            ["daily-sweeps.tsv", "ledger.tsv", "sweeps", "verdicts"],
        )
        # a later row is appended as one write to the existing file; a short append truncates back (the ledger's
        # own recovery), the first file whole
        whole = daily.read_bytes()
        self.findings_dir("daily-2026-11-20")
        other = (
            *self.DAILY_ARGS[:5],
            "--run",
            "171",
            "--task",
            DAILY_TASK_ID,
            "--findings",
            "sweeps/daily-2026-11-20/findings.json",
            *self.DAILY_ARGS[11:],
        )
        run = self.inject_short_write(*other)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertTrue(run.stderr.startswith(f"ledger-row: cannot write {daily}: short write, 2 of "), run.stderr)
        self.assertIn(f"truncated back to {len(whole)} bytes", run.stderr)
        self.assertEqual(daily.read_bytes(), whole, "the first file is whole after the failed append")
        self.assert_daily_appended(
            other,
            A,
            self.DAILY_VERIFIER.replace("run-170", "run-171"),
            "sweeps/daily-2026-11-20/findings.json; 0 findings; validators pass",
        )
        # a malformed header is refused naming line 1 and never repaired
        for text, message in (
            ("", f"{daily}:1: the header is '', not"),
            ("ts\thead\n", f"{daily}:1: the header is 'ts\\thead', not"),
            (b"\xff\n".decode("latin-1"), f"{daily}: not UTF-8"),
        ):
            with self.subTest(text=text):
                daily.write_bytes(text.encode("latin-1"))
                run = self.run_writer(*self.DAILY_ARGS)
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertIn(message, run.stderr)
                self.assertEqual(daily.read_bytes(), text.encode("latin-1"), "never repaired")
                self.assertEqual(
                    sorted(entry.name for entry in self.store.iterdir()),
                    ["daily-sweeps.tsv", "ledger.tsv", "sweeps", "verdicts"],
                    "no temporary file",
                )

    def test_an_audit_row_reads_its_word_and_counts_from_the_verdict_file_s_last_lines(self):
        (self.store / "verdicts/U7-bbbbbbbb.md").write_text(VERDICT_CORRECT)
        (self.store / "verdicts/U7b-cccccccc.md").write_text(VERDICT_INCORRECT)
        verifier = "pr-audit.sh (Codex, fresh context; round 1 of U7)"
        self.assert_appended(
            (
                "audit",
                "--pr",
                "7",
                "--head",
                B,
                "--unit",
                "U7",
                "--verdict-file",
                "verdicts/U7-bbbbbbbb.md",
                "--verifier",
                verifier,
            ),
            "U7",
            "7",
            B,
            "correct",
            verifier,
            "verdicts/U7-bbbbbbbb.md: Blocking: 0; Filed: 1; Verdict: correct",
        )
        self.assert_appended(
            (
                "audit",
                "--pr",
                "7",
                "--head",
                C,
                "--unit",
                "U7b",
                "--verdict-file",
                "verdicts/U7b-cccccccc.md",
                "--verifier",
                verifier,
                "--class",
                "read-rigor",
            ),
            "U7b",
            "7",
            C,
            "incorrect",
            verifier,
            "class=read-rigor verdicts/U7b-cccccccc.md: Blocking: 1; Filed: 3; Verdict: incorrect",
        )

    def test_a_pushed_row_has_verifier_coordinator_with_the_how_in_parentheses(self):
        self.assert_appended(
            (
                "pushed",
                "--pr",
                "-",
                "--head",
                B,
                "--unit",
                "U7",
                "--how",
                "fetched by path",
                "--what",
                "round 1: the lever",
            ),
            "U7",
            "-",
            B,
            "pushed",
            "coordinator (fetched by path)",
            "round 1: the lever",
        )
        self.assert_appended(
            (
                "pushed",
                "--pr",
                "7",
                "--head",
                C,
                "--unit",
                "U7",
                "--how",
                "gh pr create",
                "--what",
                "https://github.com/x/y/pull/7",
            ),
            "U7",
            "7",
            C,
            "pushed",
            "coordinator (gh pr create)",
            "https://github.com/x/y/pull/7",
        )

    def test_a_receipt_row_has_the_lever_name_alone_as_its_verifier(self):
        self.assert_appended(
            (
                "receipt",
                "--pr",
                "7",
                "--head",
                "-",
                "--unit",
                "U7",
                "--lever",
                "records-sync.sh",
                "--receipt",
                "synced branch=records/sync-1",
            ),
            "U7",
            "7",
            "-",
            "-",
            "records-sync.sh",
            "synced branch=records/sync-1",
        )
        self.assert_appended(
            (
                "receipt",
                "--pr",
                "7",
                "--head",
                B,
                "--unit",
                "U7",
                "--lever",
                "pr-update-branch.sh",
                "--receipt",
                "updated pr=7: old=aaaaaaaa new=bbbbbbbb",
                "--note",
                "carried row next",
            ),
            "U7",
            "7",
            B,
            "-",
            "pr-update-branch.sh",
            "updated pr=7: old=aaaaaaaa new=bbbbbbbb; carried row next",
        )

    # (b) the refusals: exit 2, one stderr line naming the cause, the ledger unchanged byte for byte.

    def test_b_each_refusal_is_exit_2_with_one_line_and_the_ledger_unchanged(self):
        (self.store / "verdicts/U7-bbbbbbbb.md").write_text(VERDICT_CORRECT)
        (self.store / "verdicts/U7-cccccccc.md").write_text(VERDICT_INCORRECT)
        (self.store / "verdicts/U7-dddddddd.md").write_text("# Verdict\n\nVerdict: correct\n")
        (self.store / "verdicts/U8-bbbbbbbb.md").write_text(VERDICT_CORRECT)
        (self.store / "sweeps/U9-bbbbbbbb/dir.json").mkdir()
        verifier = "pr-audit.sh (round 1)"
        cases = (
            (
                "a merge receipt whose pr disagrees",
                (
                    "merged",
                    "--pr",
                    "8",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--receipt",
                    f"merged pr=9 head=bbbbbbbb commit={COMMIT}",
                ),
                ("pr", "9"),
            ),
            (
                "a merge receipt whose head disagrees",
                (
                    "merged",
                    "--pr",
                    "8",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--receipt",
                    f"merged pr=8 head=cccccccc commit={COMMIT}",
                ),
                ("head", "cccccccc"),
            ),
            (
                "a carried line whose second sha is not the head",
                (
                    "carried",
                    "--pr",
                    "7",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--line",
                    f"carried {A} {C} {DIGEST}",
                    "--note",
                    "n",
                ),
                (C, B),
            ),
            (
                "a carried digest followed by a letter",
                (
                    "carried",
                    "--pr",
                    "7",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--line",
                    f"carried {A} {B} {DIGEST}x",
                    "--note",
                    "n",
                ),
                ("carried <earlier head> <head> <sha256>",),
            ),
            (
                "a sweep findings path outside sweeps/",
                (
                    "sweep",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--seat",
                    "s",
                    "--run",
                    "1",
                    "--task",
                    "U9",
                    "--findings",
                    "verdicts/U9-bbbbbbbb/findings.json",
                    "--count",
                    "0",
                ),
                ("sweeps/<dir>/findings.json",),
            ),
            (
                "a sweep findings path that is a directory",
                (
                    "sweep",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--seat",
                    "s",
                    "--run",
                    "1",
                    "--task",
                    "U9",
                    "--findings",
                    "sweeps/U9-bbbbbbbb/dir.json",
                    "--count",
                    "0",
                ),
                ("sweeps/<dir>/findings.json",),
            ),
            (
                "a sweep findings path that is missing",
                (
                    "sweep",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--seat",
                    "s",
                    "--run",
                    "1",
                    "--task",
                    "U9",
                    "--findings",
                    "sweeps/U9-cccccccc/findings.json",
                    "--count",
                    "0",
                ),
                ("not a regular file",),
            ),
            (
                "a verdict file named by another unit",
                (
                    "audit",
                    "--pr",
                    "7",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--verdict-file",
                    "verdicts/U8-bbbbbbbb.md",
                    "--verifier",
                    verifier,
                ),
                ("verdicts/U7-bbbbbbbb.md",),
            ),
            (
                "a verdict file named by another sha8",
                (
                    "audit",
                    "--pr",
                    "7",
                    "--head",
                    C,
                    "--unit",
                    "U7",
                    "--verdict-file",
                    "verdicts/U7-bbbbbbbb.md",
                    "--verifier",
                    verifier,
                ),
                ("verdicts/U7-cccccccc.md",),
            ),
            (
                "an unscored verdict file",
                (
                    "audit",
                    "--pr",
                    "7",
                    "--head",
                    "d" * 40,
                    "--unit",
                    "U7",
                    "--verdict-file",
                    "verdicts/U7-dddddddd.md",
                    "--verifier",
                    verifier,
                ),
                ("Filed:",),
            ),
            (
                "an incorrect file without --class",
                (
                    "audit",
                    "--pr",
                    "7",
                    "--head",
                    C,
                    "--unit",
                    "U7",
                    "--verdict-file",
                    "verdicts/U7-cccccccc.md",
                    "--verifier",
                    verifier,
                ),
                ("--class",),
            ),
            (
                "a verifier that is not pr-audit.sh",
                (
                    "audit",
                    "--pr",
                    "7",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--verdict-file",
                    "verdicts/U7-bbbbbbbb.md",
                    "--verifier",
                    "coordinator (by hand)",
                ),
                ("pr-audit.sh",),
            ),
            (
                "a pushed row at an audited head",
                ("pushed", "--pr", "7", "--head", A, "--unit", "U7", "--how", "h", "--what", "w"),
                ("already_audited", "2026-11-01T02:00:00Z"),
            ),
            (
                "a receipt row at an audited head",
                (
                    "receipt",
                    "--pr",
                    "7",
                    "--head",
                    A,
                    "--unit",
                    "U7",
                    "--lever",
                    "pr-update-branch.sh",
                    "--receipt",
                    "updated pr=7",
                ),
                ("already_audited", "2026-11-01T02:00:00Z"),
            ),
            (
                "a receipt lever outside the set",
                (
                    "receipt",
                    "--pr",
                    "7",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--lever",
                    "pr-merge.sh",
                    "--receipt",
                    "merged pr=7",
                ),
                ("pr-merge.sh", "records-sync.sh"),
            ),
            (
                "a tab in a note",
                (
                    "merged",
                    "--pr",
                    "8",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--receipt",
                    f"merged pr=8 head=bbbbbbbb commit={COMMIT}",
                    "--note",
                    "a\tb",
                ),
                ("note", "tab"),
            ),
            (
                "a newline in the what",
                ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "a\nb"),
                ("what", "newline"),
            ),
            (
                "a head that is not 40 hex",
                ("pushed", "--pr", "-", "--head", "bbbbbbbb", "--unit", "U7", "--how", "h", "--what", "w"),
                ("40 hex",),
            ),
            (
                "a unit outside U<n>[a-z]",
                ("pushed", "--pr", "-", "--head", B, "--unit", "U7bb", "--how", "h", "--what", "w"),
                ("U7bb",),
            ),
        )
        for name, args, reasons in cases:
            with self.subTest(name):
                self.assert_refused(args, *reasons)
        with self.subTest("a verifier note on the merged kind: no such argument"):
            run = self.run_writer(
                "merged",
                "--pr",
                "8",
                "--head",
                B,
                "--unit",
                "U7",
                "--receipt",
                "merged pr=8 head=bbbbbbbb commit=" + COMMIT,
                "--verifier-note",
                "x",
            )
            self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
            self.assertIn("--verifier-note", run.stderr)
            self.assertEqual(self.ledger.read_text(), HEADER + "".join(ROWS))
        with self.subTest("a pin that is not in the manifest"):
            self.manifest.write_text(MANIFEST.replace(f"    pin: {PIN}\n", ""))
            self.assert_refused(
                (
                    "sweep",
                    "--head",
                    B,
                    "--unit",
                    "U7",
                    "--seat",
                    "s",
                    "--run",
                    "1",
                    "--task",
                    "U9",
                    "--findings",
                    "sweeps/U9-bbbbbbbb/findings.json",
                    "--count",
                    "0",
                ),
                str(self.manifest),
                "security-audit-skill",
            )
        with self.subTest("the merged kind is exempt from the cross-row refusal"):
            self.manifest.write_text(MANIFEST)
            self.assert_appended(
                (
                    "merged",
                    "--pr",
                    "7",
                    "--head",
                    A,
                    "--unit",
                    "U7",
                    "--receipt",
                    f"merged pr=7 head=aaaaaaaa commit={COMMIT}",
                ),
                "U7",
                "7",
                A,
                "-",
                "pr-merge.sh",
                f"merged pr=7 head=aaaaaaaa commit={COMMIT}",
            )

    # (c) a ledger that does not parse is exit 2 naming the line; nothing is written.

    def test_c_a_ledger_that_does_not_parse_is_exit_2_naming_the_line_and_nothing_is_written(self):
        self.ledger.write_text(
            HEADER + ROWS[0] + "2026-11-01T02:00:00Z\tU7\t7\t" + A + "\tcorrect\tpr-audit.sh\n" + ROWS[2]
        )
        self.assert_refused(
            ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "w"),
            f"{self.ledger}:3",
            "6 columns",
        )
        self.ledger.write_text("ts\tunit\n")
        self.assert_refused(
            ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "w"), f"{self.ledger}:1"
        )
        self.ledger.unlink()
        run = self.run_writer("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "w")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn(str(self.ledger), run.stderr)
        self.assertFalse(self.ledger.exists(), "no file is made")

    # (d) the read-back: ledger.py prints the new row.

    def test_d_ledger_py_prints_each_appended_row_as_the_newest_for_its_head(self):
        (self.store / "verdicts/U7-bbbbbbbb.md").write_text(VERDICT_CORRECT)
        cells = self.assert_appended(
            ("pushed", "--pr", "7", "--head", B, "--unit", "U7", "--how", "h", "--what", "the push"),
            "U7",
            "7",
            B,
            "pushed",
            "coordinator (h)",
            "the push",
        )
        self.assertEqual(self.read("verdict", "7", B).stdout, f"{cells[0]}\tU7\tpushed\tthe push\n")
        cells = self.assert_appended(
            (
                "audit",
                "--pr",
                "7",
                "--head",
                B,
                "--unit",
                "U7",
                "--verdict-file",
                "verdicts/U7-bbbbbbbb.md",
                "--verifier",
                "pr-audit.sh (r1)",
            ),
            "U7",
            "7",
            B,
            "correct",
            "pr-audit.sh (r1)",
            "verdicts/U7-bbbbbbbb.md: Blocking: 0; Filed: 1; Verdict: correct",
        )
        audit_ts = cells[0]
        self.assertEqual(
            self.read("verdict", "7", B).stdout,
            f"{cells[0]}\tU7\tcorrect\tverdicts/U7-bbbbbbbb.md: Blocking: 0; Filed: 1; Verdict: correct\n",
        )
        line = f"carried {B} {C} {DIGEST}"
        cells = self.assert_appended(
            ("carried", "--pr", "7", "--head", C, "--unit", "U7", "--line", line, "--note", "n"),
            "U7",
            "7",
            C,
            "carried",
            "audit-carry.py (n)",
            line,
        )
        self.assertEqual(self.read("verdict", "7", C).stdout, f"{cells[0]}\tU7\tcarried\t{line}\n")
        receipt = f"merged pr=7 head={C[:8]} commit={COMMIT}"
        cells = self.assert_appended(
            ("merged", "--pr", "7", "--head", C, "--unit", "U7", "--receipt", receipt),
            "U7",
            "7",
            C,
            "-",
            "pr-merge.sh",
            receipt,
        )
        cells = self.assert_appended(
            (
                "sweep",
                "--head",
                B,
                "--unit",
                "U7",
                "--seat",
                "s",
                "--run",
                "1",
                "--task",
                "U9",
                "--findings",
                "sweeps/U9-bbbbbbbb/findings.json",
                "--count",
                "0",
                "--pr",
                "7",
            ),
            "U7",
            "-",
            B,
            "sweep",
            f"security-audit-skill {PIN[:8]} (full audit mode on the srt worker seat s, run-1; TASK U9)",
            "sweeps/U9-bbbbbbbb/findings.json; pr 7; 0 findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS",
        )
        read = self.read("sweep", "U7", B)
        self.assertEqual(read.returncode, 0, read.stderr)
        self.assertTrue(read.stdout.startswith(f"{cells[0]}\tU7\tsecurity-audit-skill {PIN[:8]} ("), read.stdout)
        # B holds an audit row of pull request 7: a receipt there is refused, so the newest row stays the audit's.
        self.assert_refused(
            ("receipt", "--pr", "7", "--head", B, "--unit", "U7", "--lever", "pr-close.sh", "--receipt", "closed pr=7"),
            "already_audited",
            audit_ts,
        )
        self.assertTrue(self.read("verdict", "7", B).stdout.startswith(f"{audit_ts}\tU7\tcorrect\t"))

    # (e) the installed form: `python3 -I -S` runs the lever from a copied directory with ledger.py beside it.

    def test_e_the_lever_runs_under_python3_I_S_from_a_copied_directory_with_ledger_py_beside_it(self):
        copy = Path(self.temp.name) / "copied/common"
        copy.mkdir(parents=True)
        shutil.copy2(WRITER, copy / "ledger-row.py")
        shutil.copy2(READER, copy / "ledger.py")
        self.writer = copy / "ledger-row.py"
        self.assert_appended(
            ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "w"),
            "U7",
            "-",
            B,
            "pushed",
            "coordinator (h)",
            "w",
        )
        (copy / "ledger.py").unlink()
        run = self.run_writer("pushed", "--pr", "-", "--head", C, "--unit", "U7", "--how", "h", "--what", "w")
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertIn("ledger.py", run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)

    # Round 2 (U222b): the seven findings of verdicts/U222-9187830e.md, each with its red test.

    def sweep_args(self, findings="sweeps/U9-bbbbbbbb/findings.json"):
        return (
            "sweep",
            "--head",
            B,
            "--unit",
            "U7",
            "--seat",
            "s",
            "--run",
            "1",
            "--task",
            "U9",
            "--findings",
            findings,
            "--count",
            "0",
        )

    def test_r2b_a_findings_path_and_a_verdict_path_through_a_symlinked_parent_refuse_naming_the_component(self):
        """(b) the final component is a regular file, but a parent directory is a link out of the store."""
        outside = Path(self.temp.name).resolve() / "outside"
        (outside / "U9-cccccccc").mkdir(parents=True)
        (outside / "U9-cccccccc/findings.json").write_text("[]\n")
        (self.store / "sweeps/U9-cccccccc").symlink_to(outside / "U9-cccccccc")
        self.assert_refused(
            self.sweep_args("sweeps/U9-cccccccc/findings.json"), str(self.store / "sweeps/U9-cccccccc"), "link"
        )
        (outside / "verdicts").mkdir()
        (outside / "verdicts/U7-bbbbbbbb.md").write_text(VERDICT_CORRECT)
        (self.store / "verdicts").rmdir()
        (self.store / "verdicts").symlink_to(outside / "verdicts")
        self.assert_refused(
            (
                "audit",
                "--pr",
                "7",
                "--head",
                B,
                "--unit",
                "U7",
                "--verdict-file",
                "verdicts/U7-bbbbbbbb.md",
                "--verifier",
                "pr-audit.sh (round 1)",
            ),
            str(self.store / "verdicts"),
            "link",
        )

    def test_r2c_a_findings_directory_holding_a_semicolon_refuses_by_the_pattern(self):
        """(c) the sweep reader splits the evidence on `;`, so the directory name is `[A-Za-z0-9._-]` alone."""
        (self.store / "sweeps/U9;note").mkdir()
        (self.store / "sweeps/U9;note/findings.json").write_text("[]\n")
        self.assert_refused(
            self.sweep_args("sweeps/U9;note/findings.json"), "sweeps/<dir>/findings.json", "[A-Za-z0-9._-]"
        )

    def test_r2d_an_unreadable_manifest_directory_refuses_and_an_absent_one_falls_through_to_the_checkout(self):
        """(d) a failed open of `~/.agents/agent-config.yaml` other than ENOENT is a refusal naming it (standing order
        21); ENOENT alone falls through to the checkout's manifest."""
        if os.geteuid() == 0:
            self.skipTest("root reads a mode-000 directory")
        agents = self.home / ".agents"
        agents.chmod(0)
        self.addCleanup(agents.chmod, 0o700)
        self.assert_refused(self.sweep_args(), str(self.manifest), "cannot read the manifest")
        agents.chmod(0o700)
        self.manifest.unlink()
        text = (ROOT / "home/dot_agents/agent-config.yaml").read_text()
        pin = re.search(r"^  security-audit-skill:\n(?:    .*\n)*?    pin: ([0-9a-f]{40})$", text, re.M).group(1)
        self.assert_appended(
            self.sweep_args(),
            "U7",
            "-",
            B,
            "sweep",
            f"security-audit-skill {pin[:8]} (full audit mode on the srt worker seat s, run-1; TASK U9)",
            "sweeps/U9-bbbbbbbb/findings.json; pr none; 0 findings; validate-findings.cjs PASS; validate-coverage-ledger.cjs PASS",
        )

    def test_r2e_a_non_breaking_space_before_carried_or_after_the_digest_refuses(self):
        """(e) the gate's `[[:space:]]` in the C locale is ASCII; a U+00A0 is no separator."""
        for name, line in (
            ("before carried", f"\u00a0carried {A} {B} {DIGEST}"),
            ("after the digest", f"carried {A} {B} {DIGEST}\u00a0note"),
        ):
            with self.subTest(name):
                self.assert_refused(
                    ("carried", "--pr", "7", "--head", B, "--unit", "U7", "--line", line, "--note", "n"),
                    "carried <earlier head> <head> <sha256>",
                )

    def test_r2f_a_store_path_holding_a_newline_refuses(self):
        """(f) the store argument is checked like every other argument."""
        store = Path(self.temp.name).resolve() / "regime\ncutover"
        store.mkdir()
        shutil.copy2(self.ledger, store / "ledger.tsv")
        self.assert_refused(
            ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "w"),
            "store",
            "newline",
            store=store,
        )

    def test_r2g_a_run_under_python3_I_S_leaves_no_pycache_beside_the_lever(self):
        """(g) `ledger.tsv` is the one file the lever writes: the import of `ledger.py` writes no bytecode."""
        copy = Path(self.temp.name) / "copied/common"
        copy.mkdir(parents=True)
        shutil.copy2(WRITER, copy / "ledger-row.py")
        shutil.copy2(READER, copy / "ledger.py")
        self.writer = copy / "ledger-row.py"
        self.assert_appended(
            ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h", "--what", "w"),
            "U7",
            "-",
            B,
            "pushed",
            "coordinator (h)",
            "w",
        )
        self.assertEqual(sorted(os.listdir(copy)), ["ledger-row.py", "ledger.py"], "no __pycache__ beside the lever")

    # Round 3 (U222c, verdicts/U222-0fc41a81.md): the concurrency property and strict arguments (the lock-file
    # and cleanup tests of that round went with the lock file and the temporary in round 4).

    PUSHED = ("pushed", "--pr", "-", "--head", B, "--unit", "U7", "--how", "h")

    def write_large_ledger(self, count=4000):
        """The header plus `count` pushed rows at head A, the auditor's probe size; returns the row texts."""
        rows = [
            row(
                f"2026-10-{1 + i // 86400:02d}T{(i // 3600) % 24:02d}:{(i // 60) % 60:02d}:{i % 60:02d}Z",
                "U7",
                "-",
                A,
                "pushed",
                "coordinator (h)",
                f"row {i}",
            )
            for i in range(count)
        ]
        self.ledger.write_text(HEADER + "".join(rows))
        return rows

    def test_r3a_twelve_concurrent_pushed_calls_against_four_thousand_rows_all_land_once(self):
        """(a) the auditor's probe: a pool of 12 subprocesses, each one `pushed` row against a 4,000-row ledger; every
        call exits 0 and the ledger holds exactly 4,012 rows afterwards, each new row present once (the round-2
        write read, checked and replaced the file from an unlocked snapshot and kept four of twelve)."""
        self.write_large_ledger()
        whats = [f"concurrent push {i}" for i in range(12)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            runs = list(pool.map(lambda what: self.run_writer(*self.PUSHED, "--what", what), whats))
        for what, run in zip(whats, runs):
            self.assertEqual((run.returncode, run.stderr), (0, ""), f"{what}: {run.stdout}{run.stderr}")
            self.assertRegex(run.stdout, r"^appended \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z line \d+\n$")
        lines = self.ledger.read_text().split("\n")
        self.assertEqual(lines.pop(), "", "the file ends with a newline")
        self.assertEqual(lines[0], HEADER[:-1])
        self.assertEqual(len(lines) - 1, 4012, "4,000 rows plus the twelve")
        evidence = [line.split("\t")[6] for line in lines[1:]]
        for what in whats:
            self.assertEqual(evidence.count(what), 1, f"{what} is present once")
        self.assertEqual(
            sorted(int(line.split("\t")[6][4:]) for line in lines[1:4001]), list(range(4000)), "the old rows are whole"
        )

    def test_r3d_a_raw_non_utf8_byte_in_what_is_a_refusal_naming_the_argument_before_anything_is_read(self):
        """(d) the auditor's probe: `--what` holding the byte 0xff, which Python's argv decoding turns into a lone
        surrogate that passes the cell check and failed at the write with a traceback and a temporary left behind;
        now every argument round-trips through strict UTF-8 first: exit 2, one stderr line naming the argument, no
        temporary, the ledger unchanged."""
        before = self.ledger.read_bytes()
        argv = [os.fsencode(sys.executable), b"-I", b"-S", os.fsencode(self.writer), os.fsencode(self.store)]
        argv += [part.encode() for part in self.PUSHED] + [b"--what", b"pushed \xff bytes"]
        run = subprocess.run(argv, capture_output=True, env=self.env, timeout=60, check=False)
        stderr = run.stderr.decode("utf-8", errors="surrogateescape")
        self.assertEqual((run.returncode, run.stdout), (2, b""), stderr)
        self.assertEqual(stderr.count("\n"), 1, stderr)
        self.assertTrue(stderr.startswith("ledger-row: refused: "), stderr)
        self.assertIn("--what", stderr)
        self.assertIn("UTF-8", stderr)
        self.assertNotIn("Traceback", stderr)
        self.assertEqual(self.ledger.read_bytes(), before, "nothing was written")
        self.assertNotIn(".tmp", "".join(os.listdir(self.store)), "no temporary")

    # Round 4 (U222d, verdicts/U222-238f0f55.md): no file but the ledger; the lock, the read and the write through
    # the ledger's own descriptor; one argument rule before argparse.

    STORE_ENTRIES = [
        "ledger.tsv",
        "sweeps",
        "sweeps/U9-bbbbbbbb",
        "sweeps/U9-bbbbbbbb/coverage-ledger.json",
        "sweeps/U9-bbbbbbbb/findings.json",
        "verdicts",
    ]

    def store_listing(self):
        """Every entry under the store, recursively, with the ledger's mode and owner: what a write may not change."""
        names = sorted(str(entry.relative_to(self.store)) for entry in self.store.rglob("*"))
        status = self.ledger.stat()
        return names, stat.S_IMODE(status.st_mode), status.st_uid, status.st_gid

    def test_r4a_a_successful_write_adds_no_entry_to_the_store_and_keeps_the_ledger_s_mode_and_owner(self):
        """(a) the store holds exactly the entries it held before plus nothing (no lock file, no temporary), and the
        ledger's mode (0600 here, the private form) and owner are unchanged."""
        self.ledger.chmod(0o600)
        before = self.store_listing()
        self.assertEqual(before[0], self.STORE_ENTRIES)
        self.assertEqual(before[1], 0o600)
        self.assert_appended(self.PUSHED + ("--what", "w"), "U7", "-", B, "pushed", "coordinator (h)", "w")
        self.assertEqual(self.store_listing(), before, "the store's names, the ledger's mode and owner are unchanged")

    def hold_ledger_lock(self):
        """A subprocess holding `LOCK_EX` on `ledger.tsv` itself for the test's duration; returns once it holds. The
        one cleanup kills it, reaps it and closes the pipe the test opened to it (round 5: an unclosed pipe raised
        `ResourceWarning` in the holder's finalizer on every run)."""
        holder = subprocess.Popen(
            [
                sys.executable,
                "-I",
                "-S",
                "-c",
                "import fcntl, os, sys, time\n"
                "fd = os.open(sys.argv[1], os.O_RDWR)\n"
                "fcntl.flock(fd, fcntl.LOCK_EX)\n"
                "print('held', flush=True)\n"
                "time.sleep(120)\n",
                str(self.ledger),
            ],
            stdout=subprocess.PIPE,
            text=True,
        )

        def stop():
            holder.kill()
            holder.wait()
            holder.stdout.close()

        self.addCleanup(stop)
        self.assertEqual(holder.stdout.readline(), "held\n")
        return holder

    def test_r4c_a_held_lock_on_the_ledger_makes_the_lever_refuse_after_its_wait_naming_the_ledger_while_ledger_py_reads(
        self,
    ):
        """(c) another process holds `LOCK_EX` on `ledger.tsv`: the lever tries non-blocking in a loop for the wait
        (`--lock-wait 1`), then refuses naming the ledger, exit 2, one stderr line, the ledger and the store unchanged;
        `ledger.py <store> verdict ...` run during the hold still reads the ledger (the lock is advisory; the readers
        take none)."""
        expected = self.read("verdict", "7", A)
        self.assertEqual(expected.returncode, 0, expected.stderr)
        self.assertTrue(expected.stdout.startswith("2026-11-01T02:00:00Z\tU7\tcorrect\t"), expected.stdout)
        self.hold_ledger_lock()
        before = self.store_listing()
        content = self.ledger.read_bytes()
        during = self.read("verdict", "7", A)
        self.assertEqual((during.returncode, during.stdout, during.stderr), (0, expected.stdout, ""))
        start = time.monotonic()
        run = self.run_writer("--lock-wait", "1", *self.PUSHED, "--what", "w")
        elapsed = time.monotonic() - start
        self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith("ledger-row: refused: "), run.stderr)
        self.assertIn(str(self.ledger), run.stderr)
        self.assertIn("1 second", run.stderr)
        self.assertNotIn(".ledger.lock", run.stderr)
        self.assertGreaterEqual(elapsed, 1.0, "the lever waited for the lock before refusing")
        self.assertEqual(self.ledger.read_bytes(), content, "nothing was written")
        self.assertEqual(self.store_listing(), before, "no file but the ledger")
        after = self.read("verdict", "7", A)
        self.assertEqual((after.returncode, after.stdout), (0, expected.stdout), after.stderr)

    def test_r4d_a_write_cut_short_by_a_size_limit_exits_1_naming_the_ledger_and_the_ledger_is_byte_identical(self):
        """(d) an RLIMIT_FSIZE of the ledger's length plus 8 bytes (the round-2 fixture's form): the one write of the
        line returns short or fails, the lever truncates the file back to the recorded length, exit 1, one stderr line
        naming the ledger, the ledger byte-identical, the store unchanged."""
        limit = self.ledger.stat().st_size + 8

        def cap():
            resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))

        before = self.store_listing()
        content = self.ledger.read_bytes()
        run = self.run_writer(*self.PUSHED, "--what", "w", preexec_fn=cap)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(f"ledger-row: cannot write {self.ledger}: "), run.stderr)
        self.assertIn(f"truncated back to {len(content)} bytes", run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        self.assertEqual(self.ledger.read_bytes(), content, "the truncate ran: the old file is whole")
        self.assertEqual(self.store_listing(), before, "no file but the ledger")

    def inject(self, function, *args, preexec_fn=None):
        """The lever run through `runpy` under `python3 -I -S` with `os.<function>` replaced by one raising EIO (the
        round-4 injection form); `preexec_fn` runs in the child before the interpreter starts (the size-limit cap)."""
        injection = (
            "import errno, os, runpy, sys\n"
            "def broken(*args, **kwargs):\n"
            "    raise OSError(errno.EIO, os.strerror(errno.EIO))\n"
            f"os.{function} = broken\n"
            "sys.argv = sys.argv[1:]\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')\n"
        )
        return subprocess.run(
            [sys.executable, "-I", "-S", "-c", injection, str(self.writer), str(self.store), *args],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=60,
            check=False,
            preexec_fn=preexec_fn,
        )

    def test_r4e_an_injected_fstat_or_pread_failure_is_one_stderr_line_exit_2_and_the_ledger_unchanged(self):
        """(e) the auditor's injection: `os.fstat` (the length) or `os.pread` (the text) raises EIO under the lock; a
        read refusal, exit 2, one stderr line naming the ledger and the error, no traceback, the ledger and the store
        unchanged."""
        before = self.store_listing()
        content = self.ledger.read_bytes()
        for function in ("fstat", "pread"):
            with self.subTest(function):
                run = self.inject(function, *self.PUSHED, "--what", "w")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
                self.assertTrue(run.stderr.startswith("ledger-row: refused: "), run.stderr)
                self.assertIn(str(self.ledger), run.stderr)
                self.assertIn("Input/output error", run.stderr)
                self.assertNotIn("Traceback", run.stderr)
                self.assertEqual(self.ledger.read_bytes(), content, "nothing was written")
                self.assertEqual(self.store_listing(), before, "no file but the ledger")

    def test_r4f_a_tab_a_newline_and_a_carriage_return_inside_lock_wait_refuse_by_the_argument_rule(self):
        """(f) the auditor's probe: `float()` strips whitespace, so `--lock-wait '1\t'` converted and the row was
        appended; now every element of argv passes the one rule before argparse runs: exit 2 naming the option and
        the character, nothing written."""
        before = self.store_listing()
        for label, value in (("a tab", "1\t"), ("a newline", "1\n"), ("a carriage return", "\r1")):
            with self.subTest(label):
                stderr = self.assert_refused(("--lock-wait", value, *self.PUSHED, "--what", "w"), "--lock-wait", label)
                self.assertNotIn("usage:", stderr)
        self.assertEqual(self.store_listing(), before, "no file but the ledger")

    # Round 5 (U222e, verdicts/U222-60415f10.md, the residual rows of 2026-11-08T17:19:09Z): the write path's four
    # failure paths carry their injection tests; the held-lock helper closes its pipe; the option name in the argument
    # rule's refusal is escaped.

    def assert_write_failure(self, run, content, before):
        """Exit 1, nothing on stdout, one stderr line starting `ledger-row: cannot write <ledger>: `, no traceback,
        the ledger byte-identical, the store unchanged; returns the stderr line."""
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(f"ledger-row: cannot write {self.ledger}: "), run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        self.assertEqual(self.ledger.read_bytes(), content, "the truncate ran: the old file is whole")
        self.assertEqual(self.store_listing(), before, "no file but the ledger")
        return run.stderr

    def test_r5a_an_injected_lseek_failure_exits_1_naming_the_ledger_and_the_ledger_is_byte_identical(self):
        """(a) `os.lseek` (the seat of the offset before the one write) raises EIO under the lock: exit 1, one stderr
        line naming the ledger and the error, the file truncated back to its length, byte-identical."""
        before = self.store_listing()
        content = self.ledger.read_bytes()
        stderr = self.assert_write_failure(self.inject("lseek", *self.PUSHED, "--what", "w"), content, before)
        self.assertIn("Input/output error", stderr)
        self.assertIn(f"truncated back to {len(content)} bytes", stderr)

    def test_r5b_an_injected_fsync_failure_exits_1_naming_the_ledger_and_the_ledger_is_byte_identical(self):
        """(b) `os.fsync` raises EIO after the write landed: exit 1, one stderr line naming the ledger and the error,
        the written line truncated back, the ledger byte-identical."""
        before = self.store_listing()
        content = self.ledger.read_bytes()
        stderr = self.assert_write_failure(self.inject("fsync", *self.PUSHED, "--what", "w"), content, before)
        self.assertIn("fsync: Input/output error", stderr)
        self.assertIn(f"truncated back to {len(content)} bytes", stderr)

    def test_r5c_an_injected_close_failure_after_the_write_exits_1_naming_the_appended_row_which_is_in_the_ledger(
        self,
    ):
        """(c) `os.close` raises EIO after the line was written and synced: exit 1, nothing on stdout, one stderr line
        naming the ledger, the appended row's receipt (`appended <ts> line <n>`) and the error; the row is in the
        ledger, one line appended to the old bytes; the store holds no other new entry."""
        before = self.store_listing()
        content = self.ledger.read_bytes()
        run = self.inject("close", *self.PUSHED, "--what", "w")
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(f"ledger-row: the ledger {self.ledger} was appended ("), run.stderr)
        self.assertIn("but its close failed: Input/output error", run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        after = self.ledger.read_bytes()
        self.assertTrue(after.startswith(content), "the file is appended, never rewritten")
        added = after[len(content) :].decode()
        self.assertEqual(added.count("\n"), 1, added)
        cells = added[:-1].split("\t")
        self.assertRegex(cells[0], TS)
        self.assertEqual(cells[1:], ["U7", "-", B, "pushed", "coordinator (h)", "w"])
        line = content.count(b"\n") + 1
        self.assertIn(f"(appended {cells[0]} line {line}) but its close failed", run.stderr)
        self.assertEqual(self.store_listing(), before, "no file but the ledger")

    def test_r5d_a_short_write_whose_ftruncate_fails_exits_1_naming_the_ledger_as_possibly_holding_a_partial_line(
        self,
    ):
        """(d) the size-limit fixture of (r4d) cuts the one write short and `os.ftruncate` raises EIO: exit 1, one
        stderr line starting with `cannot write <ledger>`, naming the short write, then `the ledger <ledger> may hold a
        partial last line` and the truncate's error; the old bytes are whole at the front of the file and no more than
        the limit's 8 bytes follow them (the partial line the text names); the store holds no other new entry."""
        before = self.store_listing()
        content = self.ledger.read_bytes()
        limit = len(content) + 8

        def cap():
            resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))

        run = self.inject("ftruncate", *self.PUSHED, "--what", "w", preexec_fn=cap)
        self.assertEqual((run.returncode, run.stdout), (1, ""), run.stderr)
        self.assertEqual(run.stderr.count("\n"), 1, run.stderr)
        self.assertTrue(run.stderr.startswith(f"ledger-row: cannot write {self.ledger}: "), run.stderr)
        self.assertIn(f"the ledger {self.ledger} may hold a partial last line: Input/output error", run.stderr)
        self.assertNotIn("truncated back", run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        after = self.ledger.read_bytes()
        self.assertTrue(after.startswith(content), "the old bytes are whole at the front")
        self.assertLessEqual(len(after), limit, "at most the limit's bytes follow them")
        self.assertEqual(self.store_listing(), before, "no file but the ledger")

    def test_r5e_the_held_lock_helper_closes_its_pipe_and_raises_no_resource_warning(self):
        """(e) the helper of (r4c) runs under `warnings.catch_warnings(record=True)` with `ResourceWarning` an error:
        the lever refuses during the hold as in (r4c); the helper's cleanups are run and the holder released inside
        the block; an unclosed pipe would raise the warning in the holder's finalizer, which the interpreter hands to
        `sys.unraisablehook`, so both the recorded warnings and the hook's list are asserted empty."""
        unraisable = []
        hook = sys.unraisablehook
        with warnings.catch_warnings(record=True) as recorded:
            warnings.simplefilter("error", ResourceWarning)
            sys.unraisablehook = unraisable.append
            try:
                holder = self.hold_ledger_lock()
                run = self.run_writer("--lock-wait", "0", *self.PUSHED, "--what", "w")
                self.assertEqual((run.returncode, run.stdout), (2, ""), run.stderr)
                self.assertIn(str(self.ledger), run.stderr)
                self.doCleanups()
                self.assertIsNotNone(holder.returncode, "the helper's cleanups reaped the holder")
                del holder
                gc.collect()
            finally:
                sys.unraisablehook = hook
        self.assertEqual([str(warning.message) for warning in recorded], [])
        self.assertEqual([str(entry.exc_value) for entry in unraisable], [], "the helper closed its pipe")

    def test_r5f_an_option_spelled_with_a_newline_refuses_in_one_stderr_line_holding_the_escaped_name(self):
        """(f) the auditor's probe: `--what` followed by a newline passes the option position of the argument rule,
        whose refusal interpolated the name as typed and so printed two lines; now the name is written in `repr` form:
        exit 2, exactly one stderr line holding `'--what\\n'`, the ledger and the store unchanged."""
        before = self.store_listing()
        stderr = self.assert_refused((*self.PUSHED, "--what\n", "w"), "the option '--what\\n'", "a newline")
        self.assertNotIn("usage:", stderr)
        self.assertEqual(self.store_listing(), before, "no file but the ledger")


if __name__ == "__main__":
    unittest.main()
