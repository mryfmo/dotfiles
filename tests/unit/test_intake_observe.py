"""scripts/orchestrator/intake-observe.py over a fixture store built from the upstream schema (regime-cutover U317).

The fixture's tables are the `CREATE TABLE` text of the pinned dsh-superagent archive's `src/app/store.ts`: line 74
(`thread`) and line 76 (`decision`), copied verbatim into SCHEMA below. The would-accept record is the one
`src/policy.ts:57` returns for a positive assessment of an inferred candidate outside auto mode: `kind: 'ignore'`,
`audit.would_accept: true`, a reason of code `observed` (`src/core/reasons.ts:25`, `Observe mode: would accept
({text})`), saved as JSON in the `value` column by `src/app/store.ts:245`. Every row the lever writes names such a
Decision and nothing else; the store is read read-only and a symlink or a non-regular file there is refused.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEVER = ROOT / "scripts/orchestrator/intake-observe.py"
INSTALLED = ROOT / "home/dot_local/bin/common/executable_intake-observe.py"
MANIFEST = ROOT / "home/dot_agents/agent-config.yaml"
ROUNDS_CHECK = ROOT / "scripts/orchestrator/rounds-check.py"
# src/app/store.ts:74 and :76 of dsh-superagent-prototype at 8c32a9dc5d72c033816c6a8110b37f40cf94fba4.
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS thread (key TEXT PRIMARY KEY, value TEXT NOT NULL);",
    "CREATE TABLE IF NOT EXISTS decision (id TEXT PRIMARY KEY, thread TEXT NOT NULL, value TEXT NOT NULL);",
)
OBSERVED = {"code": "observed", "values": {"text": "a typo fix in README.md"}}


def decision(identifier: str, thread: str, at: str, **fields) -> dict:
    """A Decision as the Engine records it, defaulting to the would-accept shape of src/policy.ts:57."""
    base = {
        "id": identifier,
        "evalId": f"eval-{identifier}",
        "threadKey": thread,
        "triggerIds": [f"trigger-{identifier}"],
        "policyVersion": "mandate-v3:test",
        "at": at,
        "kind": "ignore",
        "reason": [OBSERVED],
        "strength": "inferred",
        "audit": {
            "matches": [{"rule_id": "copy", "reason": "a typo"}],
            "rule_assessments": [{"rule_id": "copy", "matched": True, "reason": "a typo"}],
            "would_accept": True,
            "proposal": {"title": "Fix the typo", "scope": "README.md"},
        },
    }
    base.update(fields)
    return base


class IntakeObserveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.db = self.dir / "state/orchestrator.sqlite"
        self.db.parent.mkdir()
        self.tsv = self.dir / "decisions.tsv"
        connection = sqlite3.connect(self.db)
        for statement in SCHEMA:
            connection.execute(statement)
        connection.commit()
        connection.close()

    def save(self, *decisions: dict, threads: dict[str, dict] | None = None) -> None:
        """The Store's writes: `INSERT INTO decision VALUES (?,?,?)` with the JSON value (src/app/store.ts:245)."""
        connection = sqlite3.connect(self.db)
        for entry in decisions:
            connection.execute(
                "INSERT INTO decision VALUES (?,?,?) ON CONFLICT(id) DO UPDATE SET value=excluded.value, thread=excluded.thread",
                (entry["id"], entry["threadKey"], json.dumps(entry)),
            )
        for key, thread in (threads or {}).items():
            connection.execute("INSERT OR REPLACE INTO thread VALUES (?,?)", (key, json.dumps(thread)))
        connection.commit()
        connection.close()

    def run_lever(self, *args: str, script: Path = LEVER) -> subprocess.CompletedProcess:
        argv = [sys.executable, "-I", str(script), *(args or (str(self.db), str(self.tsv)))]
        return subprocess.run(argv, capture_output=True, text=True, check=False, timeout=60)

    def rows(self) -> list[list[str]]:
        """The data rows of the table (the header the lever writes on creation is not a row)."""
        if not self.tsv.exists():
            return []
        return [line.split("\t") for line in self.tsv.read_text().splitlines()[1:]]

    def test_the_fixture_schema_is_the_archives_create_table_text(self) -> None:
        # store.ts:74 and :76 at the pin; a bump that changes either line changes this fixture with it.
        self.assertEqual("CREATE TABLE IF NOT EXISTS thread (key TEXT PRIMARY KEY, value TEXT NOT NULL);", SCHEMA[0])
        self.assertEqual(
            "CREATE TABLE IF NOT EXISTS decision (id TEXT PRIMARY KEY, thread TEXT NOT NULL, value TEXT NOT NULL);",
            SCHEMA[1],
        )

    def test_appends_one_row_per_would_accept_decision_and_prints_the_count(self) -> None:
        self.save(
            decision("d1", "github:12", "2026-11-07T01:00:00Z"),
            decision("d2", "github:12", "2026-11-07T01:10:00Z", reason=[{"code": "noRuleMatched"}], audit={}),
            decision(
                "d3",
                "github:14",
                "2026-11-07T01:20:00Z",
                kind="accept",
                reason=[{"code": "said", "values": {"text": "ok"}}],
            ),
            # would_accept without the observe code: not this lever's row (the allowlist needs both).
            decision("d4", "github:15", "2026-11-07T01:30:00Z", reason=[{"code": "said", "values": {"text": "x"}}]),
            decision("d5", "github:13", "2026-11-07T02:00:00Z", triggerIds=["t-a", "t-b"]),
            threads={"github:13": {"key": "github:13", "meta": {"label": "#13 Fix the typo"}}},
        )
        result = self.run_lever()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("2\n", result.stdout)
        rows = self.rows()
        self.assertEqual(2, len(rows))
        for row in rows:
            self.assertEqual(6, len(row), row)
            self.assertRegex(row[0], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
            self.assertEqual("intake-observe", row[1])
            self.assertEqual("Observe mode: would accept (a typo fix in README.md)", row[3])
            self.assertEqual("-", row[5])
        self.assertEqual("github-source would-accept: github:12 trigger=trigger-d1 rules=copy", rows[0][2])
        self.assertEqual("d1", rows[0][4])
        self.assertEqual("github-source would-accept: #13 Fix the typo trigger=t-a,t-b rules=copy", rows[1][2])
        self.assertEqual("d5", rows[1][4])

    def test_a_second_run_appends_nothing_and_only_newer_decisions_follow(self) -> None:
        self.save(
            decision("d1", "github:12", "2026-11-07T01:00:00Z"), decision("d5", "github:13", "2026-11-07T02:00:00Z")
        )
        first = self.run_lever()
        self.assertEqual("2\n", first.stdout, first.stderr)
        text = self.tsv.read_text()
        again = self.run_lever()
        self.assertEqual((0, "0\n"), (again.returncode, again.stdout), again.stderr)
        self.assertEqual(text, self.tsv.read_text())
        # A Decision older than the last one written is not appended; a newer one is.
        self.save(
            decision("d6", "github:16", "2026-11-07T01:30:00Z"), decision("d7", "github:17", "2026-11-07T03:00:00Z")
        )
        third = self.run_lever()
        self.assertEqual("1\n", third.stdout, third.stderr)
        self.assertEqual(["d1", "d5", "d7"], [row[4] for row in self.rows()])
        self.assertEqual(text, "".join(line + "\n" for line in self.tsv.read_text().splitlines()[:3]))

    def test_tabs_and_newlines_in_the_decision_text_become_spaces(self) -> None:
        reason = {"code": "observed", "values": {"text": "line one\nline\ttwo"}}
        self.save(
            decision("d1", "github:12", "2026-11-07T01:00:00Z", reason=[reason]),
            threads={"github:12": {"key": "github:12", "meta": {"label": "a\tlabel\nhere"}}},
        )
        result = self.run_lever()
        self.assertEqual("1\n", result.stdout, result.stderr)
        rows = self.rows()
        self.assertEqual(6, len(rows[0]))
        self.assertEqual("github-source would-accept: a label here trigger=trigger-d1 rules=copy", rows[0][2])
        self.assertEqual("Observe mode: would accept (line one line two)", rows[0][3])

    def test_refuses_a_store_that_is_a_symlink_or_not_a_regular_file_and_appends_nothing(self) -> None:
        self.save(decision("d1", "github:12", "2026-11-07T01:00:00Z"))
        link = self.dir / "link.sqlite"
        link.symlink_to(self.db)
        directory = self.dir / "dir.sqlite"
        directory.mkdir()
        for path, word in (
            (link, "is a symlink"),
            (directory, "is not a regular file"),
            (self.dir / "absent", "does not exist"),
        ):
            with self.subTest(path=path.name):
                result = self.run_lever(str(path), str(self.tsv))
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)
                self.assertIn(f"intake-observe: the store {path} {word}", result.stderr)
                self.assertFalse(self.tsv.exists(), "nothing appended")
        self.tsv.symlink_to(self.dir / "elsewhere.tsv")
        result = self.run_lever()
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"intake-observe: the decisions table {self.tsv} is a symlink", result.stderr)
        self.assertFalse((self.dir / "elsewhere.tsv").exists())

    def test_the_store_is_read_read_only(self) -> None:
        self.save(decision("d1", "github:12", "2026-11-07T01:00:00Z"))
        os.chmod(self.db, 0o444)
        before = self.db.read_bytes()
        result = self.run_lever()
        self.assertEqual((0, "1\n"), (result.returncode, result.stdout), result.stderr)
        self.assertEqual(before, self.db.read_bytes(), "the store's bytes are as they were")
        self.assertIn("?mode=ro", LEVER.read_text())

    def test_a_value_that_is_not_a_json_object_refuses_the_run_with_nothing_appended(self) -> None:
        connection = sqlite3.connect(self.db)
        connection.execute("INSERT INTO decision VALUES ('bad', 'github:1', '[1, 2]')")
        connection.commit()
        connection.close()
        result = self.run_lever()
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("holds no JSON object", result.stderr)
        self.assertFalse(self.tsv.exists())

    def test_usage_and_the_installed_copy(self) -> None:
        result = self.run_lever(str(self.db))
        self.assertEqual(2, result.returncode)
        self.assertIn("usage: intake-observe.py <orchestrator.sqlite> <decisions.tsv>", result.stderr)
        self.assertEqual(LEVER.read_bytes(), INSTALLED.read_bytes(), "the deployed copy holds the same bytes")
        self.assertTrue(os.access(LEVER, os.X_OK))

    def test_a_created_table_carries_the_header_rounds_check_reads_and_an_existing_one_gets_rows_alone(self) -> None:
        # verdicts/U317 P2 :185: a created decisions.tsv had no header and rounds-check.py rejected it. The header is
        # rounds-check's DECISIONS_HEADER joined by tabs, written once, on creation alone.
        match = re.search(r"^DECISIONS_HEADER = \((.*)\)$", ROUNDS_CHECK.read_text(), re.MULTILINE)
        header = "\t".join(name.strip().strip('"') for name in match[1].split(","))
        self.assertEqual("ts\tphase\tdecision\twhy\tevidence\tresult", header)
        self.save(decision("d1", "github:12", "2026-11-07T01:00:00Z"))
        result = self.run_lever()
        self.assertEqual((0, "1\n"), (result.returncode, result.stdout), result.stderr)
        lines = self.tsv.read_text().splitlines()
        self.assertEqual(header, lines[0])
        self.assertEqual(2, len(lines))
        self.assertEqual(6, len(lines[1].split("\t")), "every row has the header's width")
        self.save(decision("d2", "github:13", "2026-11-07T02:00:00Z"))
        result = self.run_lever()
        self.assertEqual((0, "1\n"), (result.returncode, result.stdout), result.stderr)
        lines = self.tsv.read_text().splitlines()
        self.assertEqual([header], [line for line in lines if line == header], "one header, never a second")
        self.assertEqual(3, len(lines))
        # An existing table of the coordinator's is appended to as it is, header and all.
        existing = self.dir / "store.tsv"
        existing.write_text(header + "\n2026-11-07T00:00:00Z\tphase\tdecision\twhy\tevidence\tresult\n")
        result = self.run_lever(str(self.db), str(existing))
        self.assertEqual((0, "2\n"), (result.returncode, result.stdout), result.stderr)
        self.assertEqual(4, len(existing.read_text().splitlines()))
        self.assertEqual(header, existing.read_text().splitlines()[0])
        # Nothing to append creates no table.
        empty_db = self.dir / "state/empty.sqlite"
        connection = sqlite3.connect(empty_db)
        for statement in SCHEMA:
            connection.execute(statement)
        connection.commit()
        connection.close()
        result = self.run_lever(str(empty_db), str(self.dir / "never.tsv"))
        self.assertEqual((0, "0\n"), (result.returncode, result.stdout), result.stderr)
        self.assertFalse((self.dir / "never.tsv").exists())

    def test_a_table_that_cannot_be_read_is_one_refusal_line_with_exit_2_and_nothing_appended(self) -> None:
        # verdicts/U317 P3 :182: an unreadable existing table escaped the handler as a traceback with exit 1.
        self.save(decision("d1", "github:12", "2026-11-07T01:00:00Z"))
        self.tsv.write_bytes(b"\xff\xfe not utf-8\n")
        result = self.run_lever()
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)
        self.assertEqual(1, len(result.stderr.splitlines()), result.stderr)
        self.assertTrue(
            result.stderr.startswith(f"intake-observe: the decisions table {self.tsv} could not be read: "),
            result.stderr,
        )
        self.assertEqual(b"\xff\xfe not utf-8\n", self.tsv.read_bytes(), "nothing appended")
        if os.geteuid() == 0:
            self.skipTest("mode 000 does not stop root, so the unreadable-mode case is skipped")
        self.tsv.write_text("")
        self.tsv.chmod(0)
        self.addCleanup(self.tsv.chmod, 0o600)
        result = self.run_lever()
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)
        self.assertEqual(1, len(result.stderr.splitlines()), result.stderr)
        self.assertIn(f"intake-observe: the decisions table {self.tsv} could not be read: ", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def installed_layout(self) -> tuple[Path, Path, dict[str, str]]:
        """The deployed layout under a scratch HOME (tests/unit/test_lever_self_check.py's): the copy chezmoi installs
        at ~/.local/bin/common/intake-observe.py and the manifest at ~/.agents/agent-config.yaml."""
        home = self.dir / "home"
        (home / ".local/bin/common").mkdir(parents=True)
        (home / ".agents").mkdir()
        copy = home / ".local/bin/common/intake-observe.py"
        shutil.copy2(INSTALLED, copy)
        shutil.copy2(MANIFEST, home / ".agents/agent-config.yaml")
        env = {"PATH": os.environ["PATH"], "HOME": str(home), "LC_ALL": "C"}
        return home, copy, env

    def run_copy(self, copy: Path, env: dict[str, str]) -> subprocess.CompletedProcess:
        argv = [sys.executable, "-I", str(copy), str(self.db), str(self.tsv)]
        return subprocess.run(argv, capture_output=True, text=True, check=False, timeout=60, env=env, cwd=self.dir)

    def test_the_self_check_refuses_an_altered_installed_copy_naming_the_digest_and_passes_the_pinned_one(self) -> None:
        # verdicts/U317 P2 :169: an altered installed copy with the original pin ran and appended a row. The lever now
        # hashes itself against claude.levers.sha256.intake-observe.py in the manifest beside it, in brief-check.py's
        # form, before it reads anything: a different digest is exit 2 with one line and nothing on stdout.
        self.save(decision("d1", "github:12", "2026-11-07T01:00:00Z"))
        home, copy, env = self.installed_layout()
        pin = re.search(r"^      intake-observe\.py: ([0-9a-f]{64})$", MANIFEST.read_text(), re.MULTILINE)[1]
        self.assertEqual(hashlib.sha256(INSTALLED.read_bytes()).hexdigest(), pin, "the committed pin is current")
        result = self.run_copy(copy, env)
        self.assertEqual((0, "1\n"), (result.returncode, result.stdout), result.stderr)
        self.tsv.unlink()
        with copy.open("a") as handle:
            handle.write('print("rewritten")\n')
        altered = hashlib.sha256(copy.read_bytes()).hexdigest()
        result = self.run_copy(copy, env)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertEqual("", result.stdout)
        self.assertEqual(
            f"intake-observe.py: refused: sha256 {altered} of {copy.resolve()} differs from the pin in {home}/.agents/agent-config.yaml\n",
            result.stderr,
        )
        self.assertFalse(self.tsv.exists(), "nothing appended")
        # The deployed manifest is the installed copy's, not the checkout's: a zeroed deployed pin refuses the sound copy.
        shutil.copy2(INSTALLED, copy)
        manifest = home / ".agents/agent-config.yaml"
        manifest.write_text(
            manifest.read_text().replace(f"      intake-observe.py: {pin}", "      intake-observe.py: " + "0" * 64)
        )
        result = self.run_copy(copy, env)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"differs from the pin in {manifest}", result.stderr)
        manifest.write_text(MANIFEST.read_text().replace(f"      intake-observe.py: {pin}\n", ""))
        result = self.run_copy(copy, env)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("refused: no single sha256 pin for intake-observe.py in", result.stderr)
        manifest.unlink()
        result = self.run_copy(copy, env)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(f"refused: manifest unreadable: {manifest}", result.stderr)
        self.assertFalse(self.tsv.exists())
        # The checkout copy reads the checkout manifest: a scratch checkout with a zeroed pin refuses its copy too.
        checkout = self.dir / "checkout"
        (checkout / "scripts/orchestrator").mkdir(parents=True)
        (checkout / "home/dot_agents").mkdir(parents=True)
        shutil.copy2(LEVER, checkout / "scripts/orchestrator/intake-observe.py")
        (checkout / "home/dot_agents/agent-config.yaml").write_text(
            MANIFEST.read_text().replace(f"      intake-observe.py: {pin}", "      intake-observe.py: " + "0" * 64)
        )
        result = self.run_copy(checkout / "scripts/orchestrator/intake-observe.py", env)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("differs from the pin in", result.stderr)
        self.assertIn("checkout/scripts/orchestrator/../../home/dot_agents/agent-config.yaml", result.stderr)


if __name__ == "__main__":
    unittest.main()
