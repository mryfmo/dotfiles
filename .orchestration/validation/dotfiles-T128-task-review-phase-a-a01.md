---
reviewed_at: 2026-10-11T04:09:41Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4
task: dotfiles-T128-task-review-phase-a-a01
round: 1
files:
  - dotfiles-T128-process-rules-a01@43b784f0c95985fe (prefix; full hash in the TASK line)
  - dotfiles-T128-regime-counters-a01@f5fa311984ba0836
  - dotfiles-T128-ci-skip-orchestration-a01@2c748ade3c9bafb9
verdicts:
  dotfiles-T128-process-rules-a01: "revise: PR-1 review tier not docs, PR-2 threat_table key absent from V1's schema, PR-3 premise 2 output is not raw"
  dotfiles-T128-regime-counters-a01: "revise: RC-1 withdrawn and superseded exclusions contradict INV-6, RC-2 check-regime-boundary.sh has no declared test module, RC-3 the new boundary probe must skip in the herdr-agents scratch test"
  dotfiles-T128-ci-skip-orchestration-a01: "revise: CS-1 after is empty while item 1 gates V0's main-tests job, CS-2 the ruleset-list assertion needs a named constant"
---

# Task-file review: plan 006 Phase A (process-rules, regime-counters, ci-skip), one round

Stop condition applied: design v16 at 15957fbc; premises re-run where local; allowed_files against grep; one invariant per task with the contract-id rule; a threat table for the trust-boundary tasks. PyYAML check: regime-counters carries INV-6 and ci-skip INV-2 byte-identical to v16 with the right map entries; process-rules carries no invariant, as a docs-kind task with no map entry should; all three point at the round-16 receipt. The contract task dotfiles-T128-ci-skip-orchestration-contract-a01 carries superseded_by: dotfiles-T128-ci-skip-orchestration-a01, and plan 006 Phase A names the same three ids.

Environment note on the re-runs: inside this seat's sandbox the agmsg history reader failed until TMPDIR was pointed at a writable directory (a here-document in lib/storage.sh needs one; the error surfaces as "no partition driver"); with that, history.sh returns 413 rows. This is the seat's environment, not a finding against any task.

## dotfiles-T128-process-rules-a01: revise

1. PR-1 (contradiction with INV-1): the task and the plan call it docs tier, but INV-1 lists the agmsg-orchestration SKILL and AGENTS.md in the review tier by name (and both match the gate's review lists today), so the derived tier is review and the pipeline includes one schema audit. kind: docs may stay; the sentence "Docs tier: prose and the docs test only" becomes review tier with its audit.
2. PR-2 (contradiction with the design as V1 implements it): A1 item 4 puts a threat_table key in task front matter, and A3 and A5 already carry one. V1's schema (its item 1) has additionalProperties: false and no threat_table, so every such task file fails validation the day V1 lands. V1's item 1 needs threat_table as an optional array of {control, disposition} with disposition matching ^(closed|residual|out-of-scope): ; a note for V1, which is not in this round.
3. PR-3 (premises must be raw output): premise 2's second line reads 191:## Code Review Rules; on main the heading is AGENTS.md:67 (grep -n, AGENTS.md last changed at feab6452). Premise 1's history count reads 24; at review time it is 26 (rounds 15 and 16 since), so stamp the count with its time. The gh halves of premises 1 and 2 are unverifiable from this seat. Premise 3 holds (447 words).
4. allowed_files complete: the SKILL, AGENTS.md and the docs test module; the rule file is untouched at its budget. No worker question beyond the tier sentence.

## dotfiles-T128-regime-counters-a01: revise

1. RC-1 (contradiction with INV-6): rows 3 and 4 of the threat table and item 1 exclude RESULTs with status=withdrawn or status=superseded and start the Bot-head count after the first non-withdrawn RESULT. INV-6 counts every RESULT for the task_id minus one and starts Bot heads after the first RESULT; the message contract has no withdrawn or superseded status, and the 42 RESULTs in history carry only ready_for_review (41) and blocked (1), so V0's "1 withdrawn RESULT" fixture expectation is not derivable from history. Count per the sentence; a withdrawal mechanism would be a hashed change to INV-6 and the contract, not a counter option.
2. RC-2 (allowed_files under V0's convention): scripts/check-regime-boundary.sh is a declared non-data script and its module tests/unit/test_check_regime_boundary.py is neither on main nor declared; the task puts the boundary test into test_regime_counters.py, which V0's step (b0) fails once V0 is on main, and after: is empty so the order against V0 is unstated. Declare the module, or set after: and state the ordering.
3. RC-3 (touch point grep finds): tests/unit/test_herdr_agents.py:2809-2815 copies check-regime-boundary.sh alone into a scratch worktree and runs it with --report. The new probe runs regime-counters.sh live; in that scratch the script is absent beside it and no agmsg store is readable, so the probe must skip when either is missing, as the other probes skip on a missing tool, or that module, not in allowed_files, fails.
4. Threat table: rows 1, 2, 5, 6, 7 are closable or honestly residual. Add the two rows the Codex round-16 review asked for (orchestrator-authored suppression records anchored to history and GitHub; the PR controls the script, the tests and the fixtures) and one more: a RESULT with no head= token or a PR whose review_comment items carry no original_commit_id yields unknown, never 0 (item 1 says so only for a gh failure). The fixtures exported from the real store carry message bodies, so they go through the masker before commit.
5. Premises: premise 1's history half holds (10 T119 TASKs, both command forms); its gh half is unverifiable here. Premise 2 holds (lines 51, 56, 57, 60, 65, 71 as pasted). Round-16 notes already in the task: audits=unknown until V2 is stated; the history-only mode the hook needs is V3a's to call and worth one flag here.

## dotfiles-T128-ci-skip-orchestration-a01: revise

1. The round-a201 items are applied: step-level if on every heavy step with the two wrong forms named, push, schedule and workflow_dispatch always run, agent-assets.yml dropped, the workflow-security pins named, the contract dependency withdrawn. The threat table's four rows are right, the first honestly residual with its compensating controls.
2. CS-1 (contradiction inside the task): after: is empty, but item 1 gates "the main-tests job", which exists only once V0 merges; either after: [dotfiles-T128-v0-main-tests-a01] or "when the job is present", and the test in item 2 must not require a main-tests job that is not there.
3. CS-2 (worker question): item 2 asserts "the context names match the ruleset's list", which a unit test cannot read from GitHub; say it compares against a constant that copies premise 1's seven contexts, and that the constant is the thing to update when the ruleset changes.
4. Premises: premise 1's sed half holds; both gh halves are unverifiable from this seat.

## Not changed by this review

The design at v16 and its receipt pointer (still round 15, noted in the round-16 design receipt).
