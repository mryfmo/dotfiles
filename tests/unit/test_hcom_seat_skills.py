"""Pin the hcom seat skills' text hygiene sentences (U30) and their line kinds (U35): what a seat may put in one bash
call, what a bus line carries, and how the worker gets the audit findings."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "home/dot_agents/skills"
WORKER = SKILLS / "hcom-worker/SKILL.md"
ORCHESTRATION = SKILLS / "hcom-orchestration/SKILL.md"
POLICIES = ROOT / "home/dot_agents/omp/policies/README.md"

QUOTED_DENY = (
    "a deny row matches the whole command or any one segment of it, quoted text included: never put a denied "
    "command's name inside a quoted argument"
)
BUS_LINE = (
    "A bus line carries the kind, `task_id`, `brief=` path, `head=`, `pr=` and a `note=` of at most one sentence "
    "without command names; any instruction longer than that goes into a brief or addendum file the line points "
    "at. A deny row of your own policy matches text inside the line."
)
# The findings file is uncommitted in the orchestrator's checkout, so the worker's worktree lacks it (PR #487
# review 4366101582); the worker reads it by absolute path, never from its clone.
WORKER_READS = "an absolute path under the program's `verdicts/` in the orchestrator's checkout"
WORKER_WAITS = "A `verdict=incorrect` row is not addressed to you; wait for the orchestrator's fix TASK."

# The five first-pass checks (U30 ADDENDUM 2): the worker's pre-RESULT self-check and the orchestrator's pre-audit gate.
SELF_CHECK = (
    (
        "- (a) threat table: when the diff touches a trust boundary, every SCOPE path and non-path control has a "
        'threat-table row (`AGENTS.md` "Orchestration records and trust-boundary code").'
    ),
    (
        "- (b) fail closed: every safety decision reads its producer's exit status and has a failure-injection "
        "test (`preferences.md` standing order 21)."
    ),
    "- (c) destructive scope: every destructive step is scoped to exactly what the brief authorizes and refuses the rest.",
    "- (d) migration: a migration changes the installed state through the real path, not only the generated baseline.",
    (
        "- (e) local runs: the unit's own tests, `make validate-agent-assets`, `make render-check` and the lints over "
        "the changed files ran locally (omp seats have no sandbox) and their summary lines are pasted; the full suite "
        "is CI's evidence, read from the CI job log (`preferences.md` standing order 23)."
    ),
)
SELF_CHECK_HELD = "the orchestrator holds a RESULT without the pasted self-check"
PRE_AUDIT_GATE = (
    "Before any audit, gate the RESULT on the same five checks as the `hcom-worker` SKILL's pre-RESULT "
    "self-check (threat table, fail closed, destructive scope, migration, local runs)"
)
GATE_FIX_FIRST = "one that fails a check gets a `U<n>b` TASK naming the gap before any audit"

# A merge error is not a merge failure (U30 ADDENDUM 3, ACCEPTANCE 8; measured on PR #484).
# U71: the merge lever does the re-read and the orchestrator never runs it twice.
MERGE_ERROR = (
    "the lever re-reads `gh pr view <n> --json state,mergeCommit,baseRefName,headRefOid`; `MERGED` into `main` at the "
    "audited head means the merge happened and its `mergeCommit` is the sha to record, so never run the lever twice "
    "for one head (exit 1 with both shas named means GitHub merged another head or base: tell the operator); the "
    "ledger row names the commit that carries the diff (verify with `git diff <parent> <sha> --stat` non-empty)."
)


# U35: the line kinds without the retired prefix, and a question left to the orchestrator (ADDENDUM 2026-10-24T09:0xZ).
KINDS = ("TASK", "RESULT", "VERDICT", "PONG", "MERGED", "HOLD")
RETIRED_PREFIX = "a leading `AGMSG` on that word, the retired agmsg prefix an older sender may still write, is ignored"
QUESTION_NOT_YOURS = (
    "A `status=question` row from another seat is addressed to the orchestrator; never answer it, not even to say "
    "you cannot."
)


def section(text: str, heading: str) -> str:
    """The body of a `## <heading>` section, up to the next `## ` heading."""
    match = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, heading
    return match.group(1)


def step(text: str, heading: str, number: int) -> str:
    """Numbered step `<number>.` of a section, one line in these skills."""
    match = re.search(rf"^{number}\. .*$", section(text, heading), re.MULTILINE)
    assert match, (heading, number)
    return match.group(0)


class HcomSeatSkillsTest(unittest.TestCase):
    def test_the_worker_keeps_denied_command_names_out_of_quoted_arguments(self):
        self.assertIn(QUOTED_DENY, section(WORKER.read_text(), "Blocked"))

    def test_a_bus_line_carries_ids_paths_and_a_short_note(self):
        self.assertIn(BUS_LINE, step(ORCHESTRATION.read_text(), "The loop", 2))

    def test_the_worker_reads_the_findings_from_a_file(self):
        worker = step(WORKER.read_text(), "Receive", 4)
        self.assertIn(WORKER_WAITS, worker)
        self.assertIn(WORKER_READS, worker)
        # U58: the audit is one omp-run per head, no seat, so the step names no audit seat to wait on or ask.
        self.assertNotIn("audit seat", worker)

    def test_the_worker_pastes_the_five_point_self_check_before_the_result(self):
        reply = section(WORKER.read_text(), "Reply")
        for point in SELF_CHECK:
            self.assertIn(point, reply)
        self.assertIn(SELF_CHECK_HELD, reply)
        self.assertLess(reply.index(SELF_CHECK[-1]), reply.index("send one RESULT line"))

    def test_the_orchestrator_gates_a_result_on_the_same_checks_before_any_audit(self):
        gate = step(ORCHESTRATION.read_text(), "The loop", 3)
        self.assertIn(PRE_AUDIT_GATE, gate)
        self.assertIn(GATE_FIX_FIRST, gate)
        self.assertIn("held with a HOLD line", gate)

    def test_a_merge_error_is_rechecked_and_never_retried(self):
        merge = step(ORCHESTRATION.read_text(), "The loop", 6)
        self.assertIn(MERGE_ERROR, merge)
        # The re-read comes before the MERGED line is sent.
        self.assertLess(merge.index(MERGE_ERROR), merge.index("Then `MERGED v1"))

    def test_the_skills_name_the_line_kinds_without_the_retired_prefix(self):
        for skill in (WORKER, ORCHESTRATION):
            with self.subTest(skill=skill.parent.name):
                self.assertEqual(skill.read_text().count("AGMSG-"), 0)
        receive = step(WORKER.read_text(), "Receive", 1)
        self.assertIn("Its first word is the kind, `TASK v1 task_id=<id> ...`", receive)
        self.assertIn(RETIRED_PREFIX, receive)
        self.assertIn('hcom send --thread <team> -- "RESULT v1 task_id=<id>', section(WORKER.read_text(), "Reply"))
        self.assertIn(
            '- "TASK v1 task_id=U<n> brief=<path> branch=<branch>"', step(ORCHESTRATION.read_text(), "The loop", 2)
        )

    def test_a_question_from_another_seat_is_left_to_the_orchestrator(self):
        self.assertIn(QUESTION_NOT_YOURS, step(WORKER.read_text(), "Receive", 5))

    def test_the_policies_readme_records_the_measured_cases(self):
        text = section(POLICIES.read_text(), "Text that policies see")
        for evidence in ("bus row 467", "pane read 2026-10-24T02:33Z", "`*gh pr comment*`", "&& git status"):
            self.assertIn(evidence, text)


if __name__ == "__main__":
    unittest.main()
