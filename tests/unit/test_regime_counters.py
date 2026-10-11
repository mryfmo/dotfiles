"""Exercise scripts/regime-counters.sh on exported and synthetic agmsg history and gh api data.

Fixtures under tests/fixtures/regime-counters/ were exported on 2026-10-11:
- `<task id>.tsv`: the dotfiles-conformance history read through agmsg's storage facade (the read
  the script makes), rows whose body contains `task_id=<task id>`, as
  `jq -r '[.id, .at, .from, .to, .body] | @tsv'`;
- `pr-<n>.json`: `gh api --paginate repos/mryfmo/dotfiles/pulls/<n>/comments` and `.../commits`,
  kept to the fields the script reads, each comment body cut to its title line;
then masked with `scripts/validate-agent-assets.py --mask-secrets`.
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
SCRIPT = ROOT / "scripts/regime-counters.sh"
FIXTURES = ROOT / "tests/fixtures/regime-counters"
T118 = "dotfiles-T118-rolling-tools-single-update-a01"
T119 = "dotfiles-T119-rolling-release-assets-a01"
T124 = "dotfiles-T124-wave1-task-validator-a01"
V0 = "dotfiles-T128-v0-main-tests-a01"
V0_BOT_HEADS = {"32fe9a36", "56ca6c69", "de138f65", "f6528bba", "2602f575", "e314c502"}
# Stand-in for the agmsg storage facade (the stop gate's fake): team history from JSONL; it fails
# when asked for a --limit or when the busy timeout was left at its default. With $HOME/sqlite-rev
# it poses as the sqlite driver at that schema revision (current revision: 9).
STORAGE_SH = """
_AGMSG_STORAGE_SCHEMA_REV=9
agmsg_storage_load() { [[ -e $HOME/sqlite-rev ]] && _AGMSG_STORAGE_LOADED=sqlite; :; }
_sqlite_db() { printf '%s/history-%s.jsonl' "$HOME" "$1"; }
agmsg_sqlite() { cat "$HOME/sqlite-rev"; }
storage_store_exists() { [[ -f $HOME/history-$1.jsonl ]]; }
storage_history() {
    [[ $# == 1 && ${AGMSG_BUSY_TIMEOUT:-} == 1000 ]] || return 9
    cat "$HOME/history-$1.jsonl"
}
"""
# Fake gh: logs each call, serves $HOME/gh/<path after pulls/, / as _>.json through jq, and fails
# when the file is missing or a list endpoint is read without --paginate.
GH = """#!/usr/bin/env bash
echo "$*" >> "$HOME/gh-calls"
path="" filter=. paginate=false
while (($#)); do
    case $1 in
        --paginate) paginate=true ;;
        --jq) filter=$2 && shift ;;
        repos/*) path=${1#*/pulls/} ;;
    esac
    shift
done
file="$HOME/gh/${path//\\//_}.json"
[[ -f $file && ( $path != */* || $paginate == true ) ]] || exit 1
exec jq -rc "$filter" "$file"
"""


def badge(level, title):
    return (
        f"**<sub><sub>![{level} Badge](https://img.shields.io/badge/{level}-orange?style=flat)</sub></sub>  {title}**"
    )


def comment(commit, title, level="P1", bot=True, reply=None, login="chatgpt-codex-connector[bot]"):
    return {
        "user": {"login": login if bot else "someone", "type": "Bot" if bot else "User"},
        "in_reply_to_id": reply,
        "original_commit_id": commit,
        "body": badge(level, title) + "\n\nDetails.",
    }


def tsv(*messages):
    """`id at from to body` rows, one minute apart, from (sender, body) pairs."""
    return "".join(
        f"m{i}\t2026-10-11T{i // 60:02d}:{i % 60:02d}:00Z\t{sender}\torch\t{body}\n"
        for i, (sender, body) in enumerate(messages)
    )


def fields(line):
    return dict(re.findall(r"(\w+)=(\S+)", line))


class RegimeCountersTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name)
        self.home = self.temp / "home"
        scripts = self.home / ".agents/skills/agmsg/scripts"
        (scripts / "lib").mkdir(parents=True)
        (scripts / "lib/storage.sh").write_text(STORAGE_SH)
        (self.home / "gh").mkdir()
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(GH)
        (bin_dir / "gh").chmod(0o755)
        self.env = {**os.environ, "HOME": str(self.home), "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}"}

    def run_counters(self, *args, script=SCRIPT, code=0):
        result = subprocess.run(
            ["bash", str(script), *args], capture_output=True, text=True, env=self.env, timeout=30, check=False
        )
        self.assertEqual(result.returncode, code, result.stderr)
        return result.stdout.splitlines()

    def write(self, name, text):
        path = self.temp / name
        path.write_text(text)
        return str(path)

    def store(self, rows_tsv):
        """Put TSV rows into the fake live store as storage_history JSONL."""
        keys = ("id", "at", "from", "to", "body")
        lines = [dict(zip(keys, row.split("\t", 4))) for row in rows_tsv.splitlines()]
        (self.home / "history-dotfiles-conformance.jsonl").write_text("".join(json.dumps(r) + "\n" for r in lines))

    def fixture(self, task, pr=None, *extra):
        args = [task, "--history-file", str(FIXTURES / f"{task}.tsv")]
        args += ["--github-file", str(FIXTURES / f"pr-{pr}.json")] if pr else ["--history-only"]
        return self.run_counters(*args, *extra)

    def github(self, commits, comments):
        return self.write("gh.json", json.dumps({"comments": comments, "commits": [{"sha": c} for c in commits]}))

    # Fixtures exported from the real store and gh api.

    def test_t118_fixture_counts_revises_from_results(self):
        # The plan's baseline names T118 "the 20-revise task" (20 ACCEPTANCE status=revise);
        # INV-6 counts RESULTs minus one, which the fixture puts at 9.
        lines = self.fixture(T118)
        self.assertEqual(
            {"tasks": "2", "amendments": "1", "questions": "0", "results": "10", "revises": "9"},
            {k: fields(lines[0])[k] for k in ("tasks", "amendments", "questions", "results", "revises")},
        )
        self.assertIn("S2: revises 9 >= 2 source=fixture", lines)

    def test_t119_fixture_counts_every_task_after_the_first_as_an_amendment(self):
        # Ten TASKs: eight carry amendment=, the ninth after the first is the 21:48:45Z
        # note=task-file-repaired re-dispatch, which INV-6's sentence counts too.
        lines = self.fixture(T119)
        got = fields(lines[0])
        self.assertEqual(
            ("10", "9", "8", "6", "5"),
            (got["tasks"], got["amendments"], got["questions"], got["results"], got["revises"]),
        )
        self.assertIn("wall=2026-10-09T21:26:24Z..2026-10-10T08:29:00Z (11:02)", lines[0])
        self.assertEqual(
            [
                "S2: revises 5 >= 2 source=fixture",
                "S2: amendments 9 >= 2 source=fixture",
                "S2: questions 8 >= 2 source=fixture",
            ],
            [line for line in lines if line.startswith("S2:")],
        )

    def test_t124_wave1_fixture_counts_bot_heads_after_the_first_result_head(self):
        lines = self.fixture(T124, 313)
        got = fields(lines[0])
        self.assertEqual("a11e36176f7021df4160efb553a170bd680a5f30", got["first_result_head"])
        self.assertEqual("2", got["bot_p1_heads_after_result"])
        self.assertIn("S2: bot_p1_heads 2 >= 2 source=fixture", lines)

    def test_v0_fixture_counts_bot_heads_after_the_first_result_head(self):
        # The first RESULT (01:42Z) names adcf783b; 32fe9a36 is the second RESULT's head and
        # counts as one after it; 98f1d250 carries only a P2.
        lines = self.fixture(V0, 317)
        got = fields(lines[0])
        self.assertEqual(
            ("adcf783b06d9081280991a3727f8a21c3c61ac85", "6", "1", "1"),
            (got["first_result_head"], got["bot_p1_heads_after_result"], got["withdrawn"], got["revises"]),
        )
        detail = fields(next(line for line in lines if line.startswith("detail:")))
        self.assertEqual(V0_BOT_HEADS, {sha[:8] for sha in detail["bot_heads"].split(",")})

    # Threat table, closed rows.

    def test_a_forged_acceptance_record_changes_no_count(self):
        repo = self.temp / "repo"
        (repo / "scripts").mkdir(parents=True)
        shutil.copy(SCRIPT, repo / "scripts")
        for sub, text in (
            ("acceptance", "- **Decision:** ACCEPTED.\npr=317\nrevises=0 amendments=0\n"),
            ("tasks", "x\n"),
        ):
            (repo / ".orchestration" / sub).mkdir(parents=True)
            (repo / ".orchestration" / sub / f"{V0}.md").write_text(text)
        args = (V0, "--history-file", str(FIXTURES / f"{V0}.tsv"), "--github-file", str(FIXTURES / "pr-317.json"))
        self.assertEqual(self.run_counters(*args), self.run_counters(*args, script=repo / "scripts/regime-counters.sh"))

    def test_a_reset_hash_is_accepted_only_by_a_design_result_from_another_identity(self):
        design, other = "a" * 64, "b" * 64
        messages = [
            ("orch", "AGMSG-TASK v1 task_id=T1"),
            ("orch", f"AGMSG-RESULT v1 task_id=R1 status=ready_for_review verdict=accept design_sha256={design}"),
            ("rev-b", f"AGMSG-RESULT v1 task_id=R1 status=ready_for_review verdict=revise design_sha256={design}"),
            ("rev-c", f"AGMSG-RESULT v1 task_id=R1 status=ready_for_review verdict=accept design_sha256={other}"),
        ]

        def reset(*rows):
            history = self.write("h.tsv", tsv(*rows))
            return self.run_counters("T1", "--history-only", "--reset-hash", design, "--history-file", history)[-1]

        self.assertEqual(f"reset: design_sha256={design} accepted_by=none source=fixture", reset(*messages))
        foreign = ("rev-a", f"AGMSG-RESULT v1 task_id=R1 status=ready_for_review verdict=accept design_sha256={design}")
        self.assertEqual(f"reset: design_sha256={design} accepted_by=rev-a source=fixture", reset(*messages, foreign))

    def test_a_600_row_history_counts_fully_through_the_storage_facade(self):
        filler = [("w", "AGMSG-PONG v1 task_id=OTHER status=alive")] * 595
        self.store(
            tsv(
                ("orch", "AGMSG-TASK v1 task_id=T1"),
                ("w", "AGMSG-PONG v1 task_id=T1 status=question"),
                *filler,
                ("orch", "AGMSG-TASK v1 task_id=T1 amendment=1"),
                ("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
                ("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
            )
        )
        got = fields(self.run_counters("T1", "--history-only")[0])
        self.assertEqual(
            ("2", "1", "1", "2", "1"),
            (got["tasks"], got["amendments"], got["questions"], got["results"], got["revises"]),
        )

    def test_a_store_at_another_schema_revision_is_unreadable(self):
        self.store(tsv(("orch", "AGMSG-TASK v1 task_id=T1")))
        (self.home / "sqlite-rev").write_text("8\n")
        self.run_counters("T1", "--history-only", code=1)
        (self.home / "sqlite-rev").write_text("9\n")
        self.assertEqual("1", fields(self.run_counters("T1", "--history-only")[0])["tasks"])

    def test_every_result_counts_as_a_revise_whatever_its_status(self):
        lines = self.run_counters(
            "T1",
            "--history-only",
            "--history-file",
            self.write(
                "h.tsv",
                tsv(
                    ("orch", "AGMSG-TASK v1 task_id=T1"),
                    ("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
                    ("orch", "AGMSG-ACCEPTANCE v1 task_id=T1 status=withdrawn"),
                    ("w", "AGMSG-RESULT v1 task_id=T1 status=blocked"),
                    ("orch", "AGMSG-ACCEPTANCE v1 task_id=T1 status=parked"),
                    ("w", "AGMSG-PONG v1 task_id=T1 status=blocked"),
                    ("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review"),
                    # A later task_id= token is free text: this RESULT is T2's.
                    ("w", "AGMSG-RESULT v1 task_id=T2 status=ready_for_review supersedes task_id=T1"),
                ),
            ),
        )
        got = fields(lines[0])
        self.assertEqual(("3", "2", "1", "0"), (got["results"], got["revises"], got["withdrawn"], got["questions"]))
        detail = fields(lines[-1])
        self.assertEqual(
            ("m1,m3,m6", "m2", "m0", "orch"),
            (detail["results"], detail["withdrawn"], detail["tasks"], detail["authors"]),
        )

    def test_bot_heads_are_unknown_when_gh_fails(self):
        lines = self.run_counters(V0, "--history-file", str(FIXTURES / f"{V0}.tsv"))
        self.assertEqual("unknown", fields(lines[0])["bot_p1_heads_after_result"])
        self.assertFalse([line for line in lines if "bot_p1_heads" in line and line.startswith("S2:")])
        self.assertIn("pulls/317/comments", (self.home / "gh-calls").read_text())

    def test_bot_heads_are_unknown_without_a_first_result_head(self):
        history = self.write(
            "h.tsv",
            tsv(
                ("orch", "AGMSG-TASK v1 task_id=T1"),
                ("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review pr=9 previous_head=aaaaaaa"),
                ("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review pr=9 head=bbbbbbb"),
            ),
        )
        gh = self.github(["aaaaaaa1", "bbbbbbb1", "ccccccc1"], [comment("ccccccc1", "x"), comment("ccccccc1", "y")])
        self.assertEqual(
            "unknown",
            fields(self.run_counters("T1", "--history-file", history, "--github-file", gh)[0])[
                "bot_p1_heads_after_result"
            ],
        )

    def test_bot_heads_are_unknown_for_a_counted_comment_without_original_commit_id(self):
        data = json.loads((FIXTURES / "pr-317.json").read_text())
        next(c for c in data["comments"] if "P1 Badge" in c["body"])["original_commit_id"] = None
        lines = self.run_counters(
            V0, "--history-file", str(FIXTURES / f"{V0}.tsv"), "--github-file", self.write("gh.json", json.dumps(data))
        )
        self.assertEqual("unknown", fields(lines[0])["bot_p1_heads_after_result"])

    def test_bot_heads_are_unknown_when_the_first_result_head_is_not_a_pr_commit(self):
        history = self.write(
            "h.tsv", tsv(("orch", "AGMSG-TASK v1 task_id=T1"), ("w", "AGMSG-RESULT v1 task_id=T1 head=fffffff"))
        )
        gh = self.github(["aaaaaaa1", "bbbbbbb1"], [comment("bbbbbbb1", "x")])
        self.assertEqual(
            "unknown",
            fields(self.run_counters("T1", "--history-file", history, "--github-file", gh)[0])[
                "bot_p1_heads_after_result"
            ],
        )

    def test_only_p0_and_p1_heads_after_the_first_result_head_count(self):
        history = self.write(
            "h.tsv", tsv(("orch", "AGMSG-TASK v1 task_id=T1"), ("w", "AGMSG-RESULT v1 task_id=T1 head=bbbbbbb"))
        )
        commits = ["aaaaaaa1", "bbbbbbb1", "ccccccc1", "ddddddd1", "eeeeeee1"]
        gh = self.github(
            commits,
            [
                comment("aaaaaaa1", "before"),
                comment("bbbbbbb1", "at the head", "P0"),
                comment("ccccccc1", "after", "P0"),
                comment("ccccccc1", "after again"),
                comment("ddddddd1", "a P2 only", "P2"),
                comment("eeeeeee1", "human", bot=False),
                comment("eeeeeee1", "reply", reply=1) | {"body": "no badge"},
                # Another GitHub App using the same badge markup is not the Codex Bot.
                comment("ddddddd1", "other app", "P0", login="other-reviewer[bot]"),
                comment("eeeeeee1", "other app", login="other-reviewer[bot]"),
            ],
        )
        lines = self.run_counters("T1", "--history-file", history, "--github-file", gh)
        self.assertEqual("1", fields(lines[0])["bot_p1_heads_after_result"])
        self.assertEqual("ccccccc1", fields(lines[-1])["bot_heads"])

    def test_bot_heads_read_every_page_through_gh_api(self):
        self.store((FIXTURES / f"{V0}.tsv").read_text())
        data = json.loads((FIXTURES / "pr-317.json").read_text())
        for name in ("comments", "commits"):
            (self.home / "gh" / f"317_{name}.json").write_text(json.dumps(data[name]))
        lines = self.run_counters(V0)
        self.assertEqual("6", fields(lines[0])["bot_p1_heads_after_result"])
        self.assertTrue(all("--paginate" in call for call in (self.home / "gh-calls").read_text().splitlines()))

    def test_every_line_names_its_source(self):
        fixture = self.fixture(V0, 317, "--reset-hash", "c" * 64)
        self.assertGreater(len(fixture), 3)
        self.assertTrue(all(line.endswith(" source=fixture") for line in fixture), fixture)
        self.store((FIXTURES / f"{T119}.tsv").read_text())
        live = self.run_counters(T119, "--history-only")
        self.assertTrue(all(line.endswith(" source=live") for line in live), live)
        self.assertTrue(all(line.endswith(" source=live") for line in self.run_counters("--list-tasks")))

    def test_the_boundary_check_never_passes_a_test_seam(self):
        boundary = (ROOT / "scripts/check-regime-boundary.sh").read_text()
        self.assertIn("regime-counters.sh", boundary)
        self.assertNotIn("--history-file", boundary)
        self.assertNotIn("--github-file", boundary)

    # Thresholds, modes and usage.

    def test_thresholds_are_inv6_constants(self):
        once = [
            ("orch", "AGMSG-TASK v1 task_id=T1"),
            ("w", "AGMSG-PONG v1 task_id=T1 status=question"),
            ("w", "AGMSG-RESULT v1 task_id=T1"),
        ]
        twice = once + [
            ("orch", "AGMSG-TASK v1 task_id=T1 amendment=1"),
            ("w", "AGMSG-PONG v1 task_id=T1 status=question"),
            ("w", "AGMSG-RESULT v1 task_id=T1"),
        ]
        thrice = twice + [("orch", "AGMSG-TASK v1 task_id=T1 amendment=2"), ("w", "AGMSG-RESULT v1 task_id=T1")]
        s2 = lambda rows: [
            line
            for line in self.run_counters("T1", "--history-only", "--history-file", self.write("h.tsv", tsv(*rows)))
            if line.startswith("S2:")
        ]
        self.assertEqual([], s2(once))
        self.assertEqual(["S2: questions 2 >= 2 source=fixture"], s2(twice))
        self.assertEqual(
            [
                "S2: revises 2 >= 2 source=fixture",
                "S2: amendments 2 >= 2 source=fixture",
                "S2: questions 2 >= 2 source=fixture",
            ],
            s2(thrice),
        )

    def test_the_pr_is_none_without_a_pr_token_and_invalid_for_a_non_numeric_one(self):
        rows = [("orch", "AGMSG-TASK v1 task_id=T1"), ("w", "AGMSG-RESULT v1 task_id=T1 head=aaaaaaa")]
        detail = lambda *more: fields(
            self.run_counters("T1", "--history-file", self.write("h.tsv", tsv(*rows, *more)))[-1]
        )
        self.assertEqual("none", detail()["pr"])
        self.assertEqual("invalid", detail(("w", "AGMSG-RESULT v1 task_id=T1 pr=none"))["pr"])
        self.assertEqual("9", detail(("w", "AGMSG-RESULT v1 task_id=T1 pr=9"))["pr"])
        # Only a numeric PR is fetched: the fake gh logs its single call, for pulls/9.
        self.assertEqual(
            ["api --paginate repos/{owner}/{repo}/pulls/9/comments --jq .[]"],
            (self.home / "gh-calls").read_text().splitlines(),
        )

    def test_history_only_never_calls_gh(self):
        self.store((FIXTURES / f"{V0}.tsv").read_text())
        lines = self.run_counters(V0, "--history-only", "--pr", "317")
        self.assertEqual("skipped", fields(lines[0])["bot_p1_heads_after_result"])
        self.assertFalse((self.home / "gh-calls").exists())
        self.assertFalse([line for line in lines if line.startswith("S1:")])

    def test_s1_candidates_are_bot_title_classes_seen_three_times(self):
        history = self.write(
            "h.tsv", tsv(("orch", "AGMSG-TASK v1 task_id=T1"), ("w", "AGMSG-RESULT v1 task_id=T1 head=aaaaaaa"))
        )
        gh = self.github(
            ["aaaaaaa1"],
            [
                comment("aaaaaaa1", "Reject skipped contract tests"),
                comment("aaaaaaa1", "Reject  Skipped CONTRACT runs", "P2"),
                comment("aaaaaaa1", "reject skipped contract ids", "P3"),
                comment("aaaaaaa1", "Bind exemptions to scripts"),
                comment("aaaaaaa1", "Bind exemptions to paths"),
                comment("aaaaaaa1", "Bind exemptions to x", bot=False),
                comment("aaaaaaa1", "Bind exemptions to y", reply=7),
                comment("aaaaaaa1", "Bind exemptions to z", login="other-reviewer[bot]"),
            ],
        )
        lines = self.run_counters("T1", "--history-file", history, "--github-file", gh)
        self.assertEqual(
            ["S1: candidate class=reject skipped contract count=3 source=fixture"],
            [line for line in lines if line.startswith("S1:")],
        )

    def test_list_tasks_prints_each_task_id_once(self):
        self.store(
            tsv(
                ("orch", "AGMSG-TASK v1 task_id=T2"),
                ("orch", "AGMSG-TASK v1 task_id=T1"),
                ("orch", "AGMSG-TASK v1 task_id=T2 amendment=1"),
                ("w", "AGMSG-RESULT v1 task_id=T3"),
                ("orch", "AGMSG-TASK v2 task_id=T4"),
            )
        )
        self.assertEqual(["T1 source=live", "T2 source=live"], self.run_counters("--list-tasks"))

    def test_usage_errors_exit_2(self):
        for args in (
            (),
            ("T1", "T2"),
            ("T1", "--pr"),
            ("T1", "--pr", "x"),
            ("T1", "--reset-hash", "abc"),
            ("T1", "--bogus"),
        ):
            with self.subTest(args=args):
                self.run_counters(*args, code=2)


if __name__ == "__main__":
    unittest.main()
