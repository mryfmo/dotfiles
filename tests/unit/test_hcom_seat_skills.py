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

# U119 round 3 (audit of 8d442d49, P1): the audit route is the Codex lever, and the file the merge gate parses for its
# `## Findings` list is that lever's verdict.md copied into the store; the retired omp-run route wrote no such heading.
# U120 round 6: the documented line carries `--records` (the lever refuses a program pull request without it) and the
# step names exit 3, the round cap's refusal, beside exit 2 and exit 1.
AUDIT_ROUTE = (
    "Every audit is one fresh `~/.local/bin/common/pr-audit.sh <n> --records .orchestration/orchestrate/<program>` run "
    "from your checkout for that head"
)
AUDIT_COPY = "Copy that file to `.orchestration/orchestrate/<program>/verdicts/U<n>-<head8>.md`"
AUDIT_SHAPE = "whose `## Findings` list holds the reader's lines"
# U125 round d: the reader writes the two scores into every finding line and counts the filed findings, which the
# merge gate skips; the list lever is where the operator reads them.
FILED_FINDINGS = (
    "Each finding line carries `[f<n> s<n>]`, the auditor's frequency and severity scores, `Filed: <n>` counts the "
    "findings whose weight (frequency times severity) is under 10, which need no disposition for the merge, and "
    "`scripts/orchestrator/filed-findings.py <store>` lists every filed finding of the store for the operator."
)
ROUND_CAP_EXIT = (
    "Exit 3 is the round cap refused (the treadmill rule above): its stderr names the refused unit (the body's, or a "
    "`U<n>b` the ledger names for that pull request), its counts and the row to write; write that `decisions.tsv` "
    "mechanism-change row and run it again."
)
# U123 round 3 (audit of 8cdb0f9c, P2 SKILL.md:26): step 1 creates the worker's tree with the lever and says why
# a worker tree cannot push; until this test the step-4 selector was cited for it and passed against main's skill.
# Round 4: the tree is a repository of its own, and the coordinator fetches its head by path.
WORKER_WORKTREE = (
    "Create the worker tree with `~/.local/bin/common/worker-worktree.sh <unit> <branch> origin/main`: a worker tree "
    "is a repository of its own that cannot push (its config holds a refused `pushurl`, an empty credential helper "
    "and a `pre-push` hook that exits 1; nothing of your checkout's configuration reaches it, and `git worktree list` "
    "does not list it), and the coordinator fetches its head by path and pushes from the checkout with the `push=` "
    "line the lever prints."
)
# U129 (round 2: the reference-transaction hook): the same step says the checkout itself refuses commits, without
# naming the worker-tree lever a second time.
CHECKOUT_GUARD = (
    "Your checkout refuses every commit, in it and in any linked worktree of it, while a program store exists: "
    "`regime-init` installed `checkout-guard.sh`'s `reference-transaction` hook into its `.git/hooks`, which refuses "
    "any move of a local branch to a commit `origin` does not hold (`--no-verify` is no bypass; "
    "`~/.local/bin/common/checkout-guard.sh check <checkout>` reports it), so a worker that reaches for the "
    "checkout is sent to the worker-tree lever by the tool, not by a sentence (U129)."
)

# U120 (standing order 36): the Gates paragraph names the thresholds rounds-check.py counts (the third audit free, the
# fourth behind a mechanism-change row, two further `incorrect` rows of one class behind another), that the strikes are
# per class and the cap per row (round 7), and the lever flag that runs it.
ROUND_CAP = (
    "A unit's third audit needs no row; its fourth needs a `decisions.tsv` row of phase `mechanism-change` whose "
    "decision starts with the unit id and whose result names one closing form (`ast`, `parser-module`, `allowlist`, "
    "`remove`, or `residual` with the gate clause), and after that row every two further `incorrect` rows need another."
)
TWO_STRIKES = (
    "Two `incorrect` rows of one class are the two strikes, and the round after the second is analysis only, no code"
)
PER_CLASS = (
    "The check counts the strikes per class (the word of each `incorrect` row's `class=` token since the latest "
    "mechanism-change row) and the cap per row, so two `incorrect` rows of unrelated classes after that row are one "
    "strike each and refuse nothing."
)
ROUND_CAP_CHECK = (
    "`scripts/orchestrator/rounds-check.py <store> U<n>` counts the rows; `pr-audit.sh <pr> --records <store>` runs it "
    "before anything else and refuses the round while it exits non-zero"
)
ROUND_CAP_UNITS = (
    "for the body's unit or any unit the ledger names for that pull request (the lever passes `--pr <pr>`: a fix or "
    "residual unit `U<n>b` writes its parent `U<n>` in the body, standing order 24, and keeps `U<n>b` in its rows)"
)

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

    def test_the_audit_route_is_the_codex_lever_whose_verdict_file_the_merge_gate_reads(self):
        text = ORCHESTRATION.read_text()
        verify = step(text, "The loop", 4)
        self.assertIn(AUDIT_ROUTE, verify)
        self.assertNotIn("pr-audit.sh <n>` run", verify, "the documented line carries --records")
        self.assertIn(AUDIT_COPY, verify)
        self.assertIn(AUDIT_SHAPE, verify)
        self.assertIn("[f<n> s<n>] <path>:<line>: <rationale>` or `- none`, then `Blocking: <n>`, `Filed: <n>`", verify)
        self.assertIn(FILED_FINDINGS, verify)
        # the three exits, each named once in the step, the round cap's beside the other two
        self.assertIn("Exit 2 is a refusal named on stderr", verify)
        self.assertIn("exit 1 is a failed read, fetch or codex run", verify)
        self.assertIn(ROUND_CAP_EXIT, verify)
        self.assertEqual(verify.count("Exit 3"), 1)
        # the retired route stays as one history clause, never as the command to run
        self.assertEqual(verify.count("omp-run.sh --role audit"), 1)
        self.assertIn("Until U119 round 3 this step ran `omp-run.sh --role audit`", verify)
        self.assertNotIn("omp-run.sh --role audit", step(text, "The loop", 6))
        self.assertIn("a file without a `## Findings` section is refused by name", step(text, "The loop", 6))

    def test_step_one_creates_the_worker_worktree_with_the_lever_whose_worktree_cannot_push(self):
        brief = step(ORCHESTRATION.read_text(), "The loop", 1)
        self.assertIn(WORKER_WORKTREE, brief)
        self.assertEqual(brief.count("worker-worktree.sh"), 1)
        self.assertIn(CHECKOUT_GUARD, brief)

    def test_the_gates_state_the_round_cap_and_the_two_strikes_the_check_counts(self):
        gates = section(ORCHESTRATION.read_text(), "Gates")
        for sentence in (ROUND_CAP, TWO_STRIKES, PER_CLASS, ROUND_CAP_CHECK, ROUND_CAP_CHECK + " " + ROUND_CAP_UNITS):
            self.assertIn(sentence, gates)
        self.assertNotIn("three strikes", gates)

    def test_a_merge_error_is_rechecked_and_never_retried(self):
        merge = step(ORCHESTRATION.read_text(), "The loop", 6)
        self.assertIn(MERGE_ERROR, merge)
        # The re-read comes before the MERGED line is sent.
        self.assertLess(merge.index(MERGE_ERROR), merge.index("Then `MERGED v1"))

    def test_the_skills_name_the_line_kinds_without_the_retired_prefix_or_pane_argument(self):
        for skill in (WORKER, ORCHESTRATION):
            with self.subTest(skill=skill.parent.name):
                self.assertEqual(skill.read_text().count("AGMSG"), 0)
                # hcom-dispatch takes no pane argument: the line follows the recipient directly.
                self.assertNotRegex(skill.read_text(), r"hcom-dispatch [^`]*<worker> - ")
        receive = step(WORKER.read_text(), "Receive", 1)
        self.assertIn("Its first word is the kind, `TASK v1 task_id=<id> ...`", receive)
        self.assertIn('hcom send --thread <team> -- "RESULT v1 task_id=<id>', section(WORKER.read_text(), "Reply"))
        self.assertIn(
            '<worker> "TASK v1 task_id=U<n> brief=<path> branch=<branch>"',
            step(ORCHESTRATION.read_text(), "The loop", 2),
        )

    def test_a_question_from_another_seat_is_left_to_the_orchestrator(self):
        self.assertIn(QUESTION_NOT_YOURS, step(WORKER.read_text(), "Receive", 5))

    def test_the_policies_readme_records_the_measured_cases(self):
        text = section(POLICIES.read_text(), "Text that policies see")
        for evidence in ("bus row 467", "pane read 2026-10-24T02:33Z", "`*gh pr comment*`", "&& git status"):
            self.assertIn(evidence, text)


if __name__ == "__main__":
    unittest.main()
