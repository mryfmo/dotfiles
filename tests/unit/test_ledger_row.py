"""Exercise scripts/orchestrator/ledger-row.py (regime-cutover U222), the one writer of a coordinator row of
`ledger.tsv`: each kind composes its row from named arguments and the clock, the verdict and the verifier's fixed
words chosen by the kind, the ledger plus the new line re-read through `ledger.parse_ledger` before anything is
written, and the four shapes that cost a round refused by name. Every test runs over a scratch store (a ledger with
the header and three rows, `verdicts/`, `sweeps/`, a scratch HOME whose `.agents/agent-config.yaml` holds the pin) as
a subprocess under `python3 -I -S`, the form the coordinator runs."""

import concurrent.futures
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
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVERS = ROOT / "scripts/orchestrator"
WRITER = LEVERS / "ledger-row.py"
READER = LEVERS / "ledger.py"
HEADER = "ts\tunit\tpr\thead_sha\tverdict\tverifier\tevidence\n"
A, B, C = "a" * 40, "b" * 40, "c" * 40
COMMIT = "d" * 40
DIGEST = "f" * 64
PIN = "c1c8a8c1471069fb0e188eeaff69b8e8db6564a8"
TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
MANIFEST = (
    "assets:\n"
    "  other-skill:\n"
    "    source: git-commit\n"
    "    pin: 0123456789abcdef0123456789abcdef01234567\n"
    "  security-audit-skill:\n"
    "    source: git-commit\n"
    "    upstream: cloudflare/security-audit-skill\n"
    f"    pin: {PIN}\n"
    "claude:\n"
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
        (self.store / "sweeps/U9-bbbbbbbb").mkdir(parents=True)
        (self.store / "sweeps/U9-bbbbbbbb/findings.json").write_text("[]\n")
        self.ledger = self.store / "ledger.tsv"
        self.ledger.write_text(HEADER + "".join(ROWS))
        self.home = root / "home"
        (self.home / ".agents").mkdir(parents=True)
        self.manifest = self.home / ".agents/agent-config.yaml"
        self.manifest.write_text(MANIFEST)
        self.env = {"PATH": os.environ["PATH"], "HOME": str(self.home), "LC_ALL": "C"}
        self.writer = WRITER

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

    STORE_ENTRIES = ["ledger.tsv", "sweeps", "sweeps/U9-bbbbbbbb", "sweeps/U9-bbbbbbbb/findings.json", "verdicts"]

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
        """A subprocess holding `LOCK_EX` on `ledger.tsv` itself for the test's duration; returns once it holds."""
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
        self.addCleanup(holder.wait)
        self.addCleanup(holder.kill)
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

    def inject(self, function, *args):
        """The lever run through `runpy` under `python3 -I -S` with `os.<function>` replaced by one raising EIO (the
        round-3 injection form)."""
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


if __name__ == "__main__":
    unittest.main()
