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
        "the changed files ran locally (the seat's srt sandbox, the `hcom-seat` canary of U85, bounds its local "
        "runs) and their summary lines are pasted; the full suite is CI's evidence, read from the CI job log "
        "(`preferences.md` standing order 23)."
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
    "for that head from the operator's or the coordinator's terminal outside every seat, never from the seat's "
    "checkout"
)
# U139 round 2 (PR 630 review 4451944031, P1): the lever prints the verdict path and writes no ledger row, so the step
# says the run hands the path back and the orchestrator seat copies the file and writes the row; the old clause had the
# seat read a ledger row the run never produces.
AUDIT_HANDOFF = (
    "the run hands back its verdict path, and the orchestrator seat copies the file and writes the ledger row"
)
AUDIT_HANDOFF_FALSE = "the ledger row the run produces"
AUDIT_COPY = "Copy that file to `.orchestration/orchestrate/<program>/verdicts/U<n>-<head8>.md`"
AUDIT_SHAPE = "whose `## Findings` list holds the reader's lines"
# U125 round d: the reader writes the two scores into every finding line and counts the filed findings, which the
# merge gate skips; the list lever is where the operator reads them.
FILED_FINDINGS = (
    "Each finding line carries `[f<n> s<n>]`, the auditor's frequency and severity scores, `Filed: <n>` counts the "
    "findings whose weight (frequency times severity) is under 10, which need no disposition for the merge, and "
    "`scripts/orchestrator/filed-findings.py <store>` lists every filed finding of the store for the operator."
)
# U144: the security sweep of the AGENTS.md Audit section is a TASK to a worker seat, never an audit route or a verdict,
# and its validated findings are the advisory `sweep` rows written before the merge.
SWEEP_TASK = (
    "the sweep is a TASK to a worker seat naming the `security-audit` skill with an output directory under the seat's "
    "scratch root, never an audit and never a verdict, and its findings, validated with the skill's "
    "`validate-findings.cjs`, are written as the advisory `ledger.tsv` rows that rule names (verdict `sweep`, pr `-`, "
    "the swept head, verifier `security-audit-skill c1c8a8c1`, evidence the findings file under the store) before the "
    "unit's merge."
)
# U597 round 4: the daily sweep of main's head is the coordinator's dispatch once per UTC day from the kit's template,
# recorded with ledger-row.py daily as a row of the store's daily-sweeps.tsv, the row pr-merge.sh reads before it
# skips a head's own sweep row; round 6: the row's ts is the RESULT's timestamp (`--swept-at`), the findings go into a
# run-keyed directory, and the writer reads the count from the file (no `--count`); round 11 (verdict U597-2bebb5ae
# P1 at daily-sweep-brief.md:44): the recording follows the validation and a copy that follows no symbolic link.
DAILY_DISPATCH = (
    "and main's head one full sweep per UTC day, which you dispatch once per UTC day to the sweep seat at main's head "
    "from the kit's brief template `~/.agents/regime/daily-sweep-brief.md` (task id `daily-<YYYY-MM-DD>`; the "
    "`<head>`, `<run>` and `<prev>` placeholders filled) and record, after both validators exit 0 over the seat's "
    "output files and the files are copied without following symbolic links (the template's REPORT names the "
    "commands), with `~/.local/bin/common/ledger-row.py <store> daily --head <head> --seat <seat> --run <n> --task "
    "daily-<YYYY-MM-DD> --findings sweeps/daily-<YYYY-MM-DD>-run-<n>/findings.json --swept-at <ts>` "
    "(`ledger-row.py daily`; `<ts>` the RESULT's bus timestamp, the row's ts; the count is read from the findings "
    "file) as a row of the store's `daily-sweeps.tsv`"
)
# U597 round 13 (verdict U597-30d381ab P1 at pr-merge.sh:1800): a milestone unit, by its `units.tsv` track, gets its
# sweep whatever its paths, dispatched beside the class rule.
MILESTONE_DISPATCH = (
    "as does a milestone unit (its `units.tsv` track `milestone`), whose sweep you dispatch whatever its paths "
    "(`pr-merge.sh` requires its `sweep` row at the audited head whatever the classes answer; U597 round 13)"
)
DAILY_GATE = (
    "skips the row for every other head only while `ledger.py daily 86400` finds a daily sweep of main's head within "
    "24 hours, so a day without its sweep keeps the per-head rule for every head"
)
# U597 round 11 (verdict U597-2bebb5ae P1 at pr-merge.sh:907, :981 and :1609; the mechanism-change decisions row of
# 2026-11-19T15:21:36Z): rounds 9 and 10 bound the exemption to a server policy the lever inferred client-side; the
# lever now reads shas, trees and store rows alone, so step 4 names the tip gate and the tree check in the policy's
# place, and step 6 names the moved-main exit, the receipt printed first, and its recovery. Round 13 (verdict
# U597-30d381ab): the daily row's head on main's line, the carried route of the tip gate, and the landed commit held by
# its first parent and its tree with the landed diff classified on a mismatch.
TIP_GATE = (
    "; the lever reads no server policy to decide it (U597 round 11 removed the up-to-date policy read of rounds 9 and "
    "10): the daily row's head must be main's tip or an ancestor of it (the compare API's status `identical` or "
    "`ahead`, read at both reads; round 13), before the listing it requires main's tip to be swept or exempt, the "
    "tip's landed diff classified against its first parent and, for a class or the cap, a sweep row at the tip, at the "
    "head it was squashed from when the two trees are one, or at the earlier head that head was carried from "
    "(`ledger.py sweep-any`, `ledger.py merge-of`, `ledger.py carried-from`; an empty landed diff needs none), "
    "classifies the diff the squash will land, GitHub's test merge of the head against that tip (`merge_commit_sha`), "
    "beside the head's own listing with the stricter answer standing, and after the merge holds the merge commit's "
    "first parent to that tip and its tree to the test merge's tree, so a landed commit that differs in either (main "
    "moved between the lever's last tip read and GitHub's write) has its landed diff classified through the same "
    "reader: a diff touching no class exits 0 with a line and the receipt stands, a class or the cap exits 1 after the "
    "receipt and the merge commit is swept before the next merge, step 6; U597 round 12, round 13)"
)
# U597 round 12 (verdict U597-097d1615 P2 at SKILL.md:29): the daily workflow ended at recording or declining the row,
# leaving the stop gate's open item for the daily RESULT; step 4 replies to every daily RESULT, `ready_for_review` and
# `partial` alike, with the HOLD line (a sweep is no audit and no merge, so no VERDICT), citing the hook's rule.
DAILY_REPLY = (
    "Reply to every daily RESULT on the bus, `status=ready_for_review` and `status=partial` alike, once the row is "
    'written or declined: the stop gate (`~/.agents/omp/hooks/stop-gate.ts`, "Stop gate" below) holds a RESULT from a '
    "seat you tasked as an open item that owes a VERDICT, MERGED or HOLD line under the RESULT's own `task_id`, as it "
    "does for every worker RESULT, and a sweep is no audit and no merge, so the reply is "
    '`~/.local/bin/common/hcom-dispatch <team> "$(hcom list self name)" <seat> "HOLD v1 task_id=daily-<YYYY-MM-DD> '
    "note=<recorded run-<n> as the day's row | partial, no daily row>\"`, the auditable line that closes the item (the "
    "daily task never gets a VERDICT)"
)
MOVED_MAIN = (
    "Exit 1 after `MERGED` whose stdout is the receipt line and whose stderr line names the merge commit, its first "
    "parent or its tree beside the tip and the test merge's tree classified before the merge, and the class its landed "
    "diff touches (`the landed diff (compare/<parent>...<merge commit>) touches`: `main` moved between the lever's last "
    "tip read and GitHub's write, the one window the lever cannot close, and the diff that landed touches a sweep class "
    "or the cap) or an unreadable parent or tree of the merge commit (U597 round 8, round 11, round 12, round 13) means "
    "the merge happened and the landed diff is a classed one the lever did not classify before the merge, or is "
    "unknown: record the merge from that receipt line with "
    '`~/.local/bin/common/ledger-row.py <store> merged --pr <n> --head <head sha> --unit U<n> --receipt "<receipt '
    'line>"` as for every merge (the lever prints the receipt before its error line so the merge is recorded), then '
    "dispatch a sweep of the merge commit to the sweep seat (a TASK naming the `security-audit` skill at that commit "
    "with an output directory under the seat's scratch root, as step 4's sweep is) and record its validated findings "
    "with `~/.local/bin/common/ledger-row.py <store> sweep --head <merge sha> --unit U<n> --seat <seat> --run <n> "
    "--task U<n> --findings sweeps/<dir>/findings.json --count <n>` as a `sweep` row of the unit at the merge commit, "
    "before the `MERGED` line and `state=landed`: the next merge is refused until that row stands, since `pr-merge.sh` "
    "requires main's tip to be swept or exempt before it merges onto it; the merge is not undone and the lever is "
    "never run again for it. An exit 0 whose stderr says the merge commit's first parent is the tip and its tree the "
    "test merge's tree classified before the merge, or that `main` moved but the landed diff touches no sweep class, "
    "needs no such sweep: the landed diff is the classified one, or touches nothing the tip gate asks a sweep for "
    "(round 13); record and land as usual."
)
# U620 (standing orders 59 and 60): after every `pr-update-branch.sh` the coordinator audited and swept the new head
# again, six times on 2026-11-19, while its diff against main was the audited commit's; the kit's carry (audit-carry.py,
# ledger-row.py carried, the merge gate's carried row and its sweep read at the earlier head) had no step that said
# when to use it. Step 6 runs the digest lever on the new head after the fetch the lever needs (measured: a head the
# checkout has not fetched is its exit 2, `not our ref`), writes the carried row on the carried line and runs no
# fresh audit and no fresh sweep then; a refusal keeps today's fresh audit and sweep.
CARRY_FETCH = (
    "fetch the moved refs into your checkout first, `git fetch origin main <branch>` (`audit-carry.py` reads the heads "
    "from the checkout alone and opens no transport, so a head the checkout has not fetched is its exit 2, `git "
    "upload-pack: not our ref <head>`; measured 2026-11-19 on PRs 808 and 812), then run "
    "`scripts/orchestrator/audit-carry.py <store> U<n> <n> <new head> --repo <checkout> --base origin/main`"
)
CARRY_ROW = (
    "When it prints `carried <earlier> <new head> <digest>`, write the row with `~/.local/bin/common/ledger-row.py "
    '<store> carried --pr <n> --head <new head> --unit U<n> --line "<that line>" --note "<note>"` and run no fresh '
    "audit and no fresh sweep: `pr-merge.sh` accepts the carried row in place of `correct` while the earlier head's "
    "`correct` row and verdict file stand, and reads the sweep row at the earlier head the row names "
    "(`require_sweep_row` asks `ledger.py sweep` for the audited head, which under a carried row is that earlier head, "
    "the head `ledger.py carried-from` answers), so the earlier head's audit and sweep are this head's; CI must be "
    "green on the new head as for every head."
)
CARRY_REFUSED = (
    "When it refuses (exit 1 naming the differing path, or no earlier audited head), the new head gets the fresh audit "
    "and the sweep of step 4 as today; exit 2 is a git or store failure to repair first."
)
CARRY_PER_HEAD = (
    "A head that `pr-update-branch.sh` moved has no row of its own until its `carried` row (above) or its fresh "
    "audit's row is written, and `pr-merge.sh` refuses it until then (the per-head verdict rule)."
)
CARRY_GATE = (
    "gets its own row in `ledger.tsv` before merge: its own fresh-context audit's `correct` row, or a `carried` row "
    "written from `audit-carry.py`'s line when the head's diff against `main` is byte-identical to the last audited "
    "head's (standing order 38; the merge of `main` that `pr-update-branch.sh` makes is the measured case, step 6)"
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
# U130: a brief naming more than two levers is split before any TASK is sent (plan P-41), said once in step 1.
SPLIT_BRIEF = (
    "A brief whose SCOPE names more than two levers (the manifest's `claude.levers.sha256` names; a source and its "
    "generated copy count once, tests and READMEs never) is refused and is split into sequenced units of at most two "
    "levers each before any TASK is sent (plan P-41: multi-lever briefs took 6.5 audits, single-surface ones 2)."
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
# U621 (standing orders 57 and 59; round 2 after verdict U621-942e9a16, round 3 after verdict U621-b368fced, round 4
# after verdict U621-4edab4b0): step 1 states the delegated worker's progress-file contract, the convention
# stall-check.py reads, and the coordinator's use of the stall watcher as a background job under `--until-stall` whose
# exit is the wake (a background job's output reaches the coordinator only when the job exits, so no printed line wakes
# anything); the coordinator reads the exit: 1 is a stall and every row on stdout is one worker to stop, reset (one
# transaction: the progress file archived, then the markers removed) and replace with a fresh worker under the same
# consolidated brief, dispatched only after the reset's exit 0 and its archive line (on exit 3 the stderr line names the
# step to finish by hand before a second reset), before the lever is started again; 3 is the watcher's own failure and
# no worker is touched; 2 is a refusal of the arguments.
WORKER_CONTRACT = (
    "A delegated worker (a Task subagent dispatched into a worker tree) writes `<store>/progress/<unit>-progress.txt`: "
    "one `YYYY-MM-DDTHH:MM:SSZ <text>` line after each item of its brief and the bare `done, head=<sha>` line at the "
    "end, the convention `stall-check.py` reads; the coordinator sets the unit's `units.tsv` state `in-flight` at "
    "dispatch and runs `~/.local/bin/common/stall-watch.sh <store> --until-stall` as a background job for the program "
    "(every 60 seconds it runs `stall-check.py` with a 25-minute deadline over that directory, counts a unit without a "
    "file from the first tick that saw it in flight, and exits 1 at the end of the first tick that records a new "
    "`stalled` or `no-file` unit as a `decisions.tsv` row of phase `stall`, or 3 when the checker or the record "
    "failed): the job's exit is the wake, not a printed line, since a background job's output reaches you only when "
    "the job exits; the line is on its stdout."
)
STALL_ACTION = (
    "Read the job's exit before anything. Exit 1 is a stall: the tick that recorded it recorded every new stall it "
    "found in that tick, each with its marker and its row, and printed every row on stdout, so each printed row is one "
    "stalled worker to replace; for each row, stop that worker, run the lever's `reset <unit>` (one transaction ordered "
    "to fail safe: it reads the clock, moves the unit's progress file aside to `<unit>-progress.<ts>.txt`, a rename "
    "that keeps the previous worker's lines, and only then removes the unit's `seen` and `stalled` markers, printing "
    "each removed marker and the archive line only after every step succeeded, so the replacement starts with no file "
    "and its own silence is a new stall), and dispatch a fresh worker with the same consolidated brief only after the "
    "reset exited 0 and printed the archive line (or no file existed, so there was no line to print); on exit 3 the "
    "reset printed nothing on stdout and one stderr line naming the step that failed and what was already done before "
    "it: read that line, finish the named step by hand or fix the store, run the reset again, and dispatch only after "
    "an exit 0, since a replacement dispatched beside the old progress file is judged stalled at once; start the lever "
    "again only after every row's unit was reset. Exit 3 is the watcher's own failure (the checker or the record), "
    "named on its stderr, "
    "and nothing about any worker is known from it (a row on its stdout beside the failure is a stall that tick did "
    "record, handled as under exit 1): fix the store or the checker and start the lever again without touching a "
    "worker that has no row. Exit 2 is a refusal of the arguments, named on its stderr: fix the line and start the "
    "lever again. The lever itself kills and restarts nothing (standing orders 57 and 59; U621)."
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
        self.assertIn(AUDIT_HANDOFF, verify)
        self.assertNotIn(AUDIT_HANDOFF_FALSE, verify, "pr-audit.sh writes no ledger row; the seat writes it")
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

    def test_step_four_names_the_sweep_as_a_worker_task_whose_findings_are_advisory_rows(self):
        verify = step(ORCHESTRATION.read_text(), "The loop", 4)
        self.assertIn(SWEEP_TASK, verify)
        # U597: the sweep rule by path class; the every-unit sentence is gone, and the daily sweep and the classes
        # cite the operator's sweep rule C of 2026-11-18, not standing order 44, which governs executed tests (round 3);
        # round 4: the daily sweep is the coordinator's dispatch from the kit's template, its row written with
        # ledger-row.py daily, and the lever skips a head's own row only while that row stands; round 13: a milestone
        # unit's sweep is dispatched whatever its paths
        self.assertIn(
            "A unit whose head changes a lever, a policy, credential handling or a deployed executable (the path "
            "classes of `scripts/orchestrator/sweep-scope.py`, U597) also gets one security sweep before its merge, "
            + MILESTONE_DISPATCH
            + ", "
            + DAILY_DISPATCH
            + " (the operator's sweep rule C of 2026-11-18; `pr-merge.sh` refuses",
            verify,
        )
        self.assertIn(DAILY_GATE, verify)
        self.assertEqual(verify.count("daily-sweep-brief.md"), 1)
        self.assertEqual(verify.count("track `milestone`"), 1)
        self.assertNotIn("standing order 44", verify)
        self.assertNotIn("Every unit and every program milestone also gets one security sweep", verify)
        self.assertNotIn("trust-boundary class", verify)
        # the sweep is one sentence of step 4, after the audit route it never replaces
        self.assertLess(verify.index(AUDIT_ROUTE), verify.index(SWEEP_TASK))
        self.assertEqual(verify.count("security-audit-skill c1c8a8c1"), 1)

    def test_step_four_names_the_tip_gate_and_the_tree_check_in_place_of_a_policy_read(self):
        """U597 round 11 (verdict U597-2bebb5ae P1 at pr-merge.sh:907, :981 and :1609): rounds 9 and 10 had step 4 say
        the exemption existed only while a server policy was true, a policy the lever inferred client-side; the lever
        reads shas, trees and store rows alone now, so step 4 names, inside the daily-sweep parenthesis after the daily
        gate, the tip gate (main's tip swept or exempt, `ledger.py sweep-any` and `merge-of`) and the post-merge tree
        check with its step-6 recovery, and no ruleset, policy or U613."""
        verify = step(ORCHESTRATION.read_text(), "The loop", 4)
        self.assertIn(DAILY_GATE + TIP_GATE, verify)
        self.assertLess(verify.index(DAILY_GATE), verify.index(TIP_GATE))
        self.assertEqual(verify.count("`ledger.py sweep-any`"), 1)
        for word in ("U613", "strict_required_status_checks_policy", "ruleset"):
            self.assertNotIn(word, verify, f"step 4 names no {word} (round 11)")
        self.assertNotIn(
            "classified again at the merge commit", verify, "nothing is classified after the merge (round 12)"
        )

    def test_step_four_replies_to_every_daily_result_so_the_stop_gate_s_item_closes(self):
        """U597 round 12 (verdict U597-097d1615 P2 at SKILL.md:29): the stop gate (`home/dot_agents/omp/hooks/stop-gate.ts`,
        MOVES: a RESULT from a seat this seat tasked `owes a VERDICT, MERGED or HOLD line`) held the daily RESULT open
        after the row was written or declined. Step 4 replies to every daily RESULT, `ready_for_review` and `partial`
        alike, with the HOLD line under the daily task id, citing the hook, right after the tip-gate parenthesis and
        before the threat-table clause; the hook's own rule text is the one the sentence cites."""
        verify = step(ORCHESTRATION.read_text(), "The loop", 4)
        self.assertIn(TIP_GATE + ". " + DAILY_REPLY + ", the rule beside the threat-table rule", verify)
        self.assertEqual(verify.count("HOLD v1 task_id=daily-<YYYY-MM-DD>"), 1)
        hook = (ROOT / "home/dot_agents/omp/hooks/stop-gate.ts").read_text()
        self.assertIn('RESULT: [undefined, "owes a VERDICT, MERGED or HOLD line"],', hook, "the rule the step cites")
        self.assertIn("owes a VERDICT, MERGED or HOLD line under the RESULT's own `task_id`", verify)

    def test_step_six_names_the_moved_main_exit_and_the_sweep_of_the_merge_commit(self):
        """U597 round 9 (verdict U597-c37800e3 P2 at SKILL.md:29, the round-8 P2 of the skill): round 8's lever exits 1
        after `MERGED` when the merge commit's first parent is not the main tip read before the listing, and the skill
        treated `MERGED` at the expected head as authority to record landed. Step 6 names that exit (and the unread
        parent) and its recovery: a sweep of the merge commit dispatched to the sweep seat and recorded as a `sweep`
        row of the unit at the merge commit before the `MERGED` line, the ledger row and `state=landed`; the merge is
        never undone and the lever never run twice. Round 11 (verdict U597-2bebb5ae P2 at SKILL.md:31): the lever
        prints the receipt line before its error line, so the step records the merge from it with `ledger-row.py
        merged` first, names the tree check among the exits, says the next merge is refused until the sweep row
        stands, and tells the exit 0 of a moved main whose landed diff touches no class apart. The sentence comes after
        the merge-error sentence and before the `MERGED` line."""
        merge = step(ORCHESTRATION.read_text(), "The loop", 6)
        self.assertIn(MOVED_MAIN, merge)
        self.assertLess(merge.index(MERGE_ERROR), merge.index(MOVED_MAIN))
        self.assertLess(merge.index(MOVED_MAIN), merge.index("Then `MERGED v1"))
        self.assertEqual(merge.count("sweep of the merge commit"), 1)
        self.assertIn("`~/.local/bin/common/ledger-row.py <store> sweep --head <merge sha> --unit U<n>", merge)
        self.assertIn(
            '`~/.local/bin/common/ledger-row.py <store> merged --pr <n> --head <head sha> --unit U<n> --receipt "<receipt line>"`',
            merge,
        )
        self.assertLess(merge.index('--receipt "<receipt line>"'), merge.index("dispatch a sweep of the merge commit"))
        self.assertNotIn("U613", merge)

    def test_step_six_carries_the_verdict_and_the_sweep_across_update_branch_after_the_fetch_the_lever_needs(self):
        """U620 (standing orders 59 and 60): step 6 names, right after the update-branch sentence and before the merge
        sentence, the fetch of the moved refs, then `audit-carry.py` on the new head, the carried row written with
        `ledger-row.py carried` and no fresh audit and no fresh sweep on the carried line, and the fresh audit and
        sweep on a refusal; the fetch comes before the lever (the lever reads the checkout alone, and the coordinator
        measured `not our ref` without it). The per-head sentence of the step names the carried row as the moved head's
        own row, step 5's voiding sentence points at the carry, and the Gates bullet admits the carried row beside the
        fresh audit's; the old sentence that sent every moved head to a fresh audit is gone."""
        text = ORCHESTRATION.read_text()
        merge = step(text, "The loop", 6)
        self.assertIn(CARRY_FETCH + ". " + CARRY_ROW + " " + CARRY_REFUSED + " With a `correct` verdict row", merge)
        self.assertLess(merge.index("never `gh pr update-branch`. "), merge.index(CARRY_FETCH))
        self.assertLess(merge.index("git fetch origin main <branch>"), merge.index("audit-carry.py <store>"))
        self.assertEqual(merge.count("audit-carry.py <store>"), 1)
        self.assertEqual(merge.count("ledger-row.py <store> carried"), 1)
        self.assertIn(CARRY_PER_HEAD, merge)
        self.assertLess(merge.index(CARRY_REFUSED), merge.index(CARRY_PER_HEAD))
        self.assertNotIn("so it gets a fresh audit before the merge", merge)
        self.assertIn(
            "step 6 carries the earlier verdict and sweep to that merge head through `audit-carry.py` when its diff "
            "against `main` is unchanged, and it is audited afresh otherwise.",
            step(text, "The loop", 5),
        )
        gates = section(text, "Gates")
        self.assertIn(CARRY_GATE, gates)
        self.assertIn("never carries over without that row (standing order 18 as amended by U71 and U122)", gates)
        self.assertNotIn("a verdict for an earlier head never carries over (standing order 18", gates)

    def test_step_one_creates_the_worker_worktree_with_the_lever_whose_worktree_cannot_push(self):
        brief = step(ORCHESTRATION.read_text(), "The loop", 1)
        self.assertIn(WORKER_WORKTREE, brief)
        self.assertEqual(brief.count("worker-worktree.sh"), 1)
        self.assertIn(SPLIT_BRIEF, brief)
        self.assertLess(brief.index("the check refuses a brief without one."), brief.index(SPLIT_BRIEF))
        self.assertLess(brief.index(SPLIT_BRIEF), brief.index("Add the `units.tsv` row"))
        self.assertIn(CHECKOUT_GUARD, brief)

    def test_step_one_states_the_delegated_worker_contract_and_the_stall_watcher(self):
        brief = step(ORCHESTRATION.read_text(), "The loop", 1)
        self.assertIn(WORKER_CONTRACT, brief)
        self.assertIn(STALL_ACTION, brief)
        self.assertEqual(brief.count("stall-watch.sh"), 1)
        # Round 2: the wake is the background job's exit, the row on its stdout; no sentence says a printed line wakes
        # the coordinator's wait (verdict U621-942e9a16, f5 s7), and the re-dispatch sentence names `reset <unit>`.
        self.assertIn("the job's exit is the wake, not a printed line", brief)
        self.assertIn("the line is on its stdout.", brief)
        self.assertNotIn("wakes on", brief)
        self.assertEqual(brief.count("`reset <unit>`"), 1)
        self.assertEqual(brief.count("--until-stall"), 1)
        # Round 3: the coordinator reads the exit (verdict U621-b368fced, f4 s6): exit 1 is a stall and every printed
        # row is one worker to replace, reset before the restart (f3 s6); exit 3 is the watcher's failure, no worker
        # touched; the earlier sentence that replaced a worker on every exit is gone.
        self.assertIn("Read the job's exit before anything. Exit 1 is a stall:", brief)
        self.assertIn("each printed row is one stalled worker to replace", brief)
        self.assertIn("start the lever again only after every row's unit was reset.", brief)
        self.assertIn(
            "Exit 3 is the watcher's own failure (the checker or the record), named on its stderr, and nothing about "
            "any worker is known from it",
            brief,
        )
        self.assertIn("start the lever again without touching a worker that has no row.", brief)
        self.assertIn("Exit 2 is a refusal of the arguments", brief)
        self.assertIn("moves the unit's progress file aside to `<unit>-progress.<ts>.txt`", brief)
        self.assertNotIn("On that exit, stop the worker", brief)
        self.assertLess(brief.index("Exit 1 is a stall"), brief.index("Exit 3 is the watcher's own failure"))
        self.assertLess(brief.index("`reset <unit>`"), brief.index("only after every row's unit was reset"))
        # Round 4: the dispatch depends on the reset's exit (verdict U621-4edab4b0 P1 at SKILL:26, f2 s7): the
        # replacement is dispatched only after `reset` exited 0 and printed the archive line (or no file existed); on
        # exit 3 the stderr line names the step, the coordinator finishes it by hand or fixes the store, runs the
        # reset again and dispatches only after an exit 0.
        self.assertIn(
            "one transaction ordered to fail safe: it reads the clock, moves the unit's progress file aside", brief
        )
        self.assertIn("and only then removes the unit's `seen` and `stalled` markers", brief)
        self.assertIn(
            "dispatch a fresh worker with the same consolidated brief only after the reset exited 0 and printed the "
            "archive line (or no file existed, so there was no line to print)",
            brief,
        )
        self.assertIn(
            "on exit 3 the reset printed nothing on stdout and one stderr line naming the step that failed and what was "
            "already done before it: read that line, finish the named step by hand or fix the store, run the reset "
            "again, and dispatch only after an exit 0",
            brief,
        )
        self.assertNotIn("and start a fresh worker with the same consolidated brief;", brief)
        self.assertLess(brief.index("`reset <unit>`"), brief.index("only after the reset exited 0"))
        self.assertLess(brief.index("only after the reset exited 0"), brief.index("dispatch only after an exit 0"))
        self.assertLess(
            brief.index("dispatch only after an exit 0"), brief.index("only after every row's unit was reset")
        )
        # after the release of the worker's tree, before the checkout guard
        release = "run it before any successor is dispatched on the same tree."
        self.assertLess(brief.index(release), brief.index(WORKER_CONTRACT))
        self.assertLess(brief.index(WORKER_CONTRACT), brief.index(STALL_ACTION))
        self.assertLess(brief.index(STALL_ACTION), brief.index(CHECKOUT_GUARD))

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
