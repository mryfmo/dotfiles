#!/usr/bin/env python3
"""Exercise safe value storage in the agmsg send entrypoint."""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "home/dot_agents/skills/agmsg/scripts"
SEND = SCRIPTS / "executable_send.sh"


class AgmsgSendTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="agmsg-send-test-")
        self.store = Path(self.temp.name)
        self.db = self.store / "messages.db"
        with sqlite3.connect(self.db) as conn:
            conn.executescript(
                """
                CREATE TABLE messages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  team TEXT NOT NULL,
                  from_agent TEXT NOT NULL,
                  to_agent TEXT NOT NULL,
                  body TEXT NOT NULL,
                  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  read_at TEXT
                );
                """
            )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_identifiers_store_message(self) -> None:
        values = ("a" + "_" * 63, "a", "to-agent_1", "plain body")

        result = subprocess.run(
            [str(SEND), *values],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "AGMSG_STORAGE_PATH": str(self.store)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"Sent to {values[2]} in team {values[0]}\n")
        with sqlite3.connect(self.db) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone(), (1,))
            self.assertEqual(
                conn.execute(
                    "SELECT team, from_agent, to_agent, body FROM messages"
                ).fetchone(),
                values,
            )

    def test_invalid_identifiers_fail_before_storage_access(self) -> None:
        fields = ("team", "from", "to")
        invalid_values = (
            "bad'name",
            "bad name",
            "bad;name",
            "Bad",
            "_bad",
            "a" * 65,
        )

        for field_index, field in enumerate(fields):
            for case_index, invalid_value in enumerate(invalid_values):
                storage = self.store / f"invalid-{field}-{case_index}"
                values = ["team-1", "from_agent", "to-agent", "body"]
                values[field_index] = invalid_value

                result = subprocess.run(
                    [str(SEND), *values],
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={**os.environ, "AGMSG_STORAGE_PATH": str(storage)},
                    check=False,
                )

                with self.subTest(field=field, value=invalid_value):
                    self.assertEqual(result.returncode, 1)
                    self.assertEqual(result.stdout, "")
                    self.assertEqual(
                        result.stderr,
                        "Usage: send.sh <team> <from> <to> <message> "
                        "(identifiers must match "
                        "^[a-z0-9][a-z0-9_-]{0,63}$)\n",
                    )
                    self.assertFalse(storage.exists())

    def test_quote_bearing_body_round_trips(self) -> None:
        values = (
            "team-1",
            "from_agent",
            "to-agent",
            "body'); DROP TABLE messages; -- 'intact",
        )

        result = subprocess.run(
            [str(SEND), *values],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "AGMSG_STORAGE_PATH": str(self.store)},
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, f"Sent to {values[2]} in team {values[0]}\n")
        with sqlite3.connect(self.db) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM messages").fetchone(), (1,))
            self.assertEqual(
                conn.execute(
                    "SELECT team, from_agent, to_agent, body FROM messages"
                ).fetchone(),
                values,
            )

    def test_touched_shell_entrypoints_have_shdoc_headers(self) -> None:
        for relative in (
            "executable_send.sh",
            "executable_whoami.sh",
            "executable_check-inbox.sh",
        ):
            text = (SEND.parent / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("# @file ", text)
                self.assertIn("# @brief ", text)


class AgmsgRegistrationGrammarTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="agmsg-registration-test-")
        self.root = Path(self.temp.name)
        self.case_number = 0

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_skill(self) -> Path:
        self.case_number += 1
        skill = self.root / f"case-{self.case_number}"
        scripts = skill / "scripts"
        (scripts / "lib").mkdir(parents=True)
        for name in ("join", "rename", "rename-team"):
            shutil.copy2(SCRIPTS / f"executable_{name}.sh", scripts / f"{name}.sh")
        for name in ("storage.sh", "identifier.sh"):
            source = SCRIPTS / "lib" / name
            if source.exists():
                shutil.copy2(source, scripts / "lib" / name)
        return skill

    def run_script(
        self, skill: Path, name: str, *args: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(skill / "scripts" / f"{name}.sh"), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "AGMSG_STORAGE_PATH": str(skill / "db")},
            check=False,
        )

    def seed_team_and_db(self, skill: Path) -> None:
        team = skill / "teams" / "team-1"
        team.mkdir(parents=True, exist_ok=True)
        (team / "config.json").write_text(
            json.dumps(
                {
                    "name": "team-1",
                    "agents": {
                        "agent-1": {
                            "registrations": [
                                {"type": "codex", "project": "/tmp/project"}
                            ]
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        db_dir = skill / "db"
        db_dir.mkdir()
        with sqlite3.connect(db_dir / "messages.db") as conn:
            conn.executescript(
                """
                CREATE TABLE messages (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  team TEXT NOT NULL,
                  from_agent TEXT NOT NULL,
                  to_agent TEXT NOT NULL,
                  body TEXT NOT NULL
                );
                INSERT INTO messages (team, from_agent, to_agent, body)
                VALUES ('team-1', 'agent-1', 'agent-2', 'body');
                """
            )

    def state(self, skill: Path) -> dict[str, bytes]:
        return {
            str(path.relative_to(skill)): path.read_bytes()
            for path in sorted(skill.rglob("*"))
            if path.is_file() and path.relative_to(skill).parts[0] in {"teams", "db"}
        }

    def assert_usage_rejection(
        self,
        result: subprocess.CompletedProcess[str],
        usage: str,
    ) -> None:
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(
            result.stderr,
            f"Usage: {usage} (identifiers must match "
            "^[a-z0-9][a-z0-9_-]{0,63}$)\n",
        )

    def test_join_rejects_invalid_team_and_agent_without_mutation(self) -> None:
        for field_index in (0, 1):
            for invalid in ("bad'name", "bad name", "Bad"):
                skill = self.make_skill()
                args = ["team-1", "agent-1", "codex", "/tmp/project"]
                args[field_index] = invalid

                result = self.run_script(skill, "join", *args)

                with self.subTest(field=field_index, invalid=invalid):
                    self.assert_usage_rejection(
                        result, "join.sh <team> <agent_id> <type> <project_path>"
                    )
                    self.assertEqual(self.state(skill), {})
                    self.assertFalse((skill / "teams").exists())

    def test_rename_rejects_invalid_identifiers_without_mutation(self) -> None:
        for field_index in (0, 1, 2):
            for invalid in ("bad'name", "bad name", "Bad"):
                skill = self.make_skill()
                self.seed_team_and_db(skill)
                before = self.state(skill)
                args = ["team-1", "agent-1", "agent-new"]
                args[field_index] = invalid

                result = self.run_script(skill, "rename", *args)

                with self.subTest(field=field_index, invalid=invalid):
                    self.assert_usage_rejection(
                        result, "rename.sh <team> <old_name> <new_name>"
                    )
                    self.assertEqual(self.state(skill), before)

    def test_team_rename_rejects_invalid_names_without_mutation(self) -> None:
        for field_index in (0, 1):
            for invalid in ("bad'name", "bad name", "Bad"):
                skill = self.make_skill()
                self.seed_team_and_db(skill)
                before = self.state(skill)
                args = ["team-1", "team-new"]
                args[field_index] = invalid

                result = self.run_script(skill, "rename-team", *args)

                with self.subTest(field=field_index, invalid=invalid):
                    self.assert_usage_rejection(
                        result, "rename-team.sh <old_team> <new_team>"
                    )
                    self.assertEqual(self.state(skill), before)

    def test_valid_registration_and_renames_still_work(self) -> None:
        skill = self.make_skill()

        joined = self.run_script(
            skill, "join", "team-1", "agent-1", "codex", "/tmp/project"
        )
        self.assertEqual(joined.returncode, 0, joined.stderr)
        joined_config = json.loads(
            (skill / "teams" / "team-1" / "config.json").read_text()
        )
        self.assertIn("agent-1", joined_config["agents"])
        self.seed_team_and_db(skill)

        renamed = self.run_script(
            skill, "rename", "team-1", "agent-1", "agent-new"
        )
        self.assertEqual(renamed.returncode, 0, renamed.stderr)
        with sqlite3.connect(skill / "db" / "messages.db") as conn:
            self.assertEqual(
                conn.execute("SELECT from_agent FROM messages").fetchone(),
                ("agent-new",),
            )

        team_renamed = self.run_script(
            skill, "rename-team", "team-1", "team-new"
        )
        self.assertEqual(team_renamed.returncode, 0, team_renamed.stderr)
        self.assertFalse((skill / "teams" / "team-1").exists())
        config = json.loads(
            (skill / "teams" / "team-new" / "config.json").read_text()
        )
        self.assertEqual(config["name"], "team-new")
        self.assertIn("agent-new", config["agents"])
        with sqlite3.connect(skill / "db" / "messages.db") as conn:
            self.assertEqual(
                conn.execute("SELECT team FROM messages").fetchone(),
                ("team-new",),
            )

    def test_identifier_grammar_has_one_source_of_truth(self) -> None:
        literal = "^[a-z0-9][a-z0-9_-]{0,63}$"
        matches = {
            str(path.relative_to(SCRIPTS)): path.read_text(encoding="utf-8").count(
                literal
            )
            for path in SCRIPTS.rglob("*.sh")
            if literal in path.read_text(encoding="utf-8")
        }
        self.assertEqual(matches, {"lib/identifier.sh": 1})

        for relative in (
            "executable_send.sh",
            "executable_join.sh",
            "executable_rename.sh",
            "executable_rename-team.sh",
        ):
            text = (SCRIPTS / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn('source "$SCRIPT_DIR/lib/identifier.sh"', text)
                self.assertIn("# @file ", text)
                self.assertIn("# @brief ", text)


if __name__ == "__main__":
    unittest.main()
