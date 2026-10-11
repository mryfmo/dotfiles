"""Exercise the INV-6 probe of scripts/check-regime-boundary.sh against a fake agmsg store and fake gh.

The other probes are tested in tests/unit/test_herdr_agents.py; these tests read only the lines the
INV-6 probe prints for their own task ids.
"""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The redesign task file T1-redesign.md and the hash a reset record names for it.
DESIGN_TEXT = "redesign\n"
DESIGN = hashlib.sha256(DESIGN_TEXT.encode()).hexdigest()
RESET = f"---\nformat: 2\nreset_of: T1\nredesign_task: T1-redesign\ndesign_sha256: {DESIGN}\n---\n"
# Same fakes as tests/unit/test_regime_counters.py: the storage facade serves JSONL history and
# refuses a --limit; gh serves $HOME/gh/<path after pulls/, / as _>.json through jq.
STORAGE_SH = """
agmsg_storage_load() { :; }
storage_store_exists() { [[ -f $HOME/history-$1.jsonl ]]; }
storage_history() {
    [[ $# == 1 ]] || return 9
    cat "$HOME/history-$1.jsonl"
}
"""
GH = """#!/usr/bin/env bash
cat > /dev/null # drains whatever stdin it inherits, as a reading command would
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


class RegimeBoundaryCountsTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.temp = Path(temp.name)
        self.home = self.temp / "home"
        self.storage = self.home / ".agents/skills/agmsg/scripts/lib/storage.sh"
        self.storage.parent.mkdir(parents=True)
        self.storage.write_text(STORAGE_SH)
        (self.home / "gh").mkdir()
        bin_dir = self.temp / "bin"
        bin_dir.mkdir()
        (bin_dir / "gh").write_text(GH)
        (bin_dir / "gh").chmod(0o755)
        jq_dir = os.path.dirname(shutil.which("jq"))
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "PATH": os.pathsep.join([str(bin_dir), jq_dir, "/usr/bin", "/bin"]),
        }
        self.main = self.temp / "dotfiles"
        (self.main / "scripts").mkdir(parents=True)
        for name in ("check-regime-boundary.sh", "regime-counters.sh"):
            shutil.copy(ROOT / "scripts" / name, self.main / "scripts")
        (self.main / ".orchestration/tasks").mkdir(parents=True)
        (self.main / ".orchestration/acceptance").mkdir()
        (self.main / ".orchestration/tasks/T1.md").write_text("task\n")
        (self.main / ".orchestration/tasks/T1-redesign.md").write_text(DESIGN_TEXT)
        (self.main / ".orchestration/tasks/T1-other.md").write_text("another design\n")
        git = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-C", str(self.main)]
        subprocess.run([*git, "init", "-q", "-b", "main"], check=True)
        subprocess.run([*git, "add", "."], check=True)
        subprocess.run([*git, "commit", "-q", "-m", "c"], check=True)
        # T1 is over the revise count (three RESULTs) on PR 5, open and unmerged.
        self.messages = [
            ("orch", "AGMSG-TASK v1 task_id=T1"),
            *[("w", "AGMSG-RESULT v1 task_id=T1 status=ready_for_review pr=5 head=aaaaaaa")] * 3,
            *[("orch", "AGMSG-TASK v1 task_id=T9")] * 3,
        ]
        self.pull(5, "open")
        (self.home / "gh/5_comments.json").write_text("[]")
        (self.home / "gh/5_commits.json").write_text(json.dumps([{"sha": "aaaaaaa1"}]))

    def pull(self, number, state, merged=False):
        merged_at = "2026-10-11T00:00:00Z" if merged else None
        (self.home / f"gh/{number}.json").write_text(json.dumps({"state": state, "merged_at": merged_at}))

    def record(self, name, text):
        (self.main / ".orchestration/acceptance" / name).write_text(text)

    def report(self, *extra):
        rows = [*self.messages, *extra]
        (self.home / "history-dotfiles-conformance.jsonl").write_text(
            "".join(
                json.dumps({"id": f"m{i}", "at": "2026-10-11T00:00:00Z", "from": f, "to": "x", "body": b}) + "\n"
                for i, (f, b) in enumerate(rows)
            )
        )
        result = subprocess.run(
            ["bash", str(self.main / "scripts/check-regime-boundary.sh"), "--report"],
            cwd=self.main,
            env=self.env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return [
            line
            for line in result.stdout.splitlines()
            if line.startswith(
                ("regime-boundary: T1 ", "regime-boundary: T2 ", "regime-boundary: T9 ", "regime-boundary: ../")
            )
        ]

    def test_each_listed_task_is_counted_and_an_unsafe_id_is_skipped(self):
        # The fake gh drains its stdin: T2 is still counted after T1's gh calls. A history id
        # that is a path (../acceptance/T7 resolves to an existing .md) is never counted.
        (self.main / ".orchestration/tasks/T2.md").write_text("task\n")
        self.record("T7.md", "x\n")
        self.messages += [("orch", "AGMSG-TASK v1 task_id=T2")] * 3 + [
            ("orch", "AGMSG-TASK v1 task_id=../acceptance/T7")
        ] * 3
        self.assertEqual(
            [
                "regime-boundary: T1 S2: revises 2 >= 2 source=live",
                "regime-boundary: T2 S2: amendments 2 >= 2 source=live",
            ],
            self.report(),
        )

    def test_a_task_over_a_count_is_reported(self):
        # T9 is over the amendment count but has no task file in the main checkout: not counted.
        self.assertEqual(["regime-boundary: T1 S2: revises 2 >= 2 source=live"], self.report())

    def test_an_accepted_record_silences_only_when_the_tasks_pr_is_merged(self):
        reported = ["regime-boundary: T1 S2: revises 2 >= 2 source=live"]
        self.record("T1.md", "- **Decision:** ACCEPTED.\npr=5\n")
        self.assertEqual(reported, self.report())
        # Merged now, but the record must name the task's PR (the first pr= of its RESULTs).
        self.pull(5, "closed", merged=True)
        for text in (
            "- **Decision:** ACCEPTED.\npr=6\n",
            "- **Decision:** ACCEPTED. PR #5\n",
            "- **Decision:** PENDING.\npr=5\n",
        ):
            self.record("T1.md", text)
            self.assertEqual(reported, self.report(), text)
        self.record("T1.md", "status: accepted\npr=5\n")
        self.assertEqual([], self.report())

    def test_a_reset_record_silences_only_when_another_identity_accepted_its_design(self):
        # The accepting RESULT is the design review's, as on the bus: its task_id is not the redesign's.
        accept = f"AGMSG-RESULT v1 task_id=T1-review status=ready_for_review verdict=accept design_sha256={DESIGN}"
        reported = ["regime-boundary: T1 S2: revises 2 >= 2 source=live"]
        self.record("T1-design-reset.md", RESET)
        self.assertEqual(reported, self.report(("orch", accept)))
        self.assertEqual([], self.report(("reviewer", accept)))
        # The same accepted hash anchors nothing for a record naming another redesign task, a
        # missing one, or no hash at all.
        for text in (
            RESET.replace("T1-redesign", "T1-other"),
            RESET.replace("T1-redesign", "T1-missing"),
            RESET.replace(f"design_sha256: {DESIGN}\n", ""),
        ):
            self.record("T1-design-reset.md", text)
            self.assertEqual(reported, self.report(("reviewer", accept)), text)

    def test_a_waiver_line_silences_nothing(self):
        self.record("T1.md", "- **Decision:** ACCEPTED.\nDESIGN_RESET_WAIVED_BY=operator\n")
        self.assertEqual(
            ["regime-boundary: T1 S2: revises 2 >= 2 source=live", "regime-boundary: T1 waiver-unanchored"],
            self.report(),
        )
        # Below every count, or silenced by a merged PR, the waiver line is still reported.
        self.pull(5, "closed", merged=True)
        self.record("T1.md", "- **Decision:** ACCEPTED.\npr=5\nDESIGN_RESET_WAIVED_BY=operator\n")
        self.assertEqual(["regime-boundary: T1 waiver-unanchored"], self.report())
        self.messages = self.messages[:2]
        self.pull(5, "closed")
        self.record("T1.md", "x\n")
        self.record("T1-design-reset.md", "redesign_seat: x under DESIGN_RESET_WAIVED_BY=operator\n")
        self.assertEqual(
            [
                "regime-boundary: T1 waiver-unanchored",
                "regime-boundary: T1 PR #5 closed unmerged without an anchored reset record",
            ],
            self.report(),
        )

    def test_a_pr_closed_unmerged_is_reported_without_an_anchored_reset_record(self):
        self.messages = self.messages[:2]
        self.pull(5, "closed")
        self.assertEqual(["regime-boundary: T1 PR #5 closed unmerged without an anchored reset record"], self.report())
        self.record("T1-design-reset.md", RESET)
        accept = f"AGMSG-RESULT v1 task_id=R status=ready_for_review verdict=accept design_sha256={DESIGN}"
        self.assertEqual([], self.report(("reviewer", accept)))

    def test_the_probe_skips_without_the_counters_script_or_a_readable_store(self):
        (self.main / "scripts/regime-counters.sh").unlink()
        self.assertEqual([], self.report())
        shutil.copy(ROOT / "scripts/regime-counters.sh", self.main / "scripts")
        self.storage.unlink()
        self.assertEqual([], self.report())


if __name__ == "__main__":
    unittest.main()
