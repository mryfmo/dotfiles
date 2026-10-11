# Report: dotfiles-T128-process-rules-a02

- Seat: `claude-standard-dot-a003` in `.claude/worktrees/worker-f`. This is the reset continuation of `dotfiles-T128-process-rules-a01` (reset record `.orchestration/acceptance/dotfiles-T128-process-rules-a01-design-reset.md`), on the same branch `docs/regime-pattern` and PR #318, from head `aeb6c5ad`.
- Task file sha256 `0a31acb4…` checked against the TASK; first commit `7382fb01` copies it byte-identical to `.orchestration/dotfiles-T128-process-rules-a02/task.md` (the `…-a01/` directory stays as history). Content commit `c31b8327`; Bot fix round 1 `3ff0cade`.

## What changed (`c31b8327`)

1. SKILL "Review and integration invariants": the whole `threat_table` bullet replaced, verbatim from the redesign receipt. It names three disposition forms (`closed: tests/<file>::<name>`, `residual: <sentence>`, `out-of-scope: <task id>`), leaves shape to `schemas/task.json` (wave V1) and substance to the reviewers, and keeps "a missing row is added once, counted as an amendment". No pattern and no placeholder list are left in the prose.
2. AGENTS.md "### Orchestration records and trust-boundary code": the second bullet replaced verbatim; it supersedes the placeholder clause that `77953979` had added. The first and third bullets stay.
3. Tests:
   - `test_a_trust_boundary_task_carries_a_threat_table` replaced verbatim;
   - `test_threat_table_dispositions_carry_a_payload` removed;
   - `test_threat_table_rule_carries_no_grammar` added;
   - `test_code_review_rules_cover_orchestration_records_and_threat_tables` now asserts the new AGENTS.md bullet's sentences instead of the replaced bullet's. The task did not name this edit, but the replacement would otherwise break the test.
4. Thread 4240348412: the by-hand counts read `history.sh` with an explicit `--limit 1000` (or the storage facade) → `test_manual_counts_read_the_whole_history`.
5. Thread 4240348414: the sentence appended to Orchestrator Playbook step 10.1 makes an `open:<thread id>` item a sweep item like any other, so the PR is not merged with the thread open → `test_open_third_round_threads_have_an_integration_outcome`.

Every replacement was checked verbatim against the task file (validation §2); all 15 removal proofs fail their tests, including the old grammar pasted back (§3); the premises hold (§4).

## Bot

- Round 1 on `c31b8327`: 4240382519 (P1, the counters bullet): the manual counts missed review-body findings → `fixed:3ff0cade` (fix round 1 of 2).
- The final head's round, CI and the open threads are in the RESULT and the main-checkout copy of this report.
- Earlier threads on this PR from a01: 4240348412 → `fixed:c31b8327` and 4240348414 → `fixed:c31b8327` (items 4 and 5).

## Notes

- Nothing in this task touched the threat-table payload wording beyond the verbatim replacement; per the task, a Bot finding there is reported, not fixed.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`memory add` printed `05618498-52b4-4708-8262-8b762c5ce8e0` (validation §6).

cost: n/a

## Final head `27ea99b2` (main-checkout copy)

- CI: 14 of 14 pass; the watcher's exit status was joined before the RESULT.
- Bot round 2: code review completed at 05:31:05Z with no findings (no review object, no comment, 👍 at 05:31:09Z). `bot_rounds=2`, one fix round; no thread open from this task.
