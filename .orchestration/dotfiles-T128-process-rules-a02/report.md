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

## Revise round 1 (ACCEPTANCE 05:52:25Z, audit of `27ea99b2`: incorrect; `previous_head=27ea99b2`)

One commit on `docs/regime-pattern`, recorded in `revise.yaml` beside this report. Each of the four worker-side findings gets a one-sentence rule fix and the token test the ACCEPTANCE names:

1. P1 `AGENTS.md:77`: the secrets-and-home-paths-only rule now binds "the pull-request review by the Codex Bot", and "The task-level audit keeps the full scope of the Audit section." → `test_orchestration_records_rule_binds_the_bot_review_only`.
2. P2 `AGENTS.md:78`: "Until `schemas/task.json` lands in wave V1, the task-file review checks the three shape rules by hand." ends both the SKILL `threat_table` bullet and the AGENTS.md second bullet → `test_shape_is_checked_by_hand_until_the_schema_lands`.
3. P2 `tests/…:329`: four existing sentences pinned, no prose change: the `closed` row whose test does not close it (AGENTS.md), the control enumeration, reviewer independence in the design review, and the design-on-main precondition (SKILL invariants) → `test_pattern_rules_pin_their_safeguards`.
4. P2 `sandboxes/…:29`: Worker Playbook step 2 now says "Commit inside the sandbox, with `git -c commit.gpgsign=false` when the signing key is unreadable there; only the push leaves the sandbox." → `test_workers_commit_inside_the_sandbox`. The deviation it names, my `git add` and `git commit` of `27ea99b2` in the same outside-sandbox call as its push, is now stated in this directory's `sandbox.md` too (it was only in the main-checkout copy); this round's commit ran inside the sandbox.

The fifth finding (the PR-feedback JSON grammar) is the orchestrator's, as the ACCEPTANCE says. Every new or pinned sentence fails its test when removed: 10 of 10, the old first bullet pasted back among them (validation §7). The docs module runs 34 tests, OK. CompactionDB: `aae4a1c4-c1c0-4bbb-bd54-71223252c0f4`.

### Fifth item (addendum, ACCEPTANCE 06:33:46Z) and Bot fix round 1 of the revise

- `108b43bd`: CI 14 of 14 pass, watcher exit 0 (validation §8). Bot review 5482212241 (06:44:25Z) with four threads:
  - 4240566259 (P1, SKILL.md:71): the a01 and a02 task records carry no `threat_table` although the PR edits the rules the Bot reads from the PR tree. The task record is the orchestrator's, so I asked (PONG `status=question`, default: hold the push); the orchestrator answered with Amendment 1 (TASK 06:47:54Z, sha256 `b6500dbf…`, three `residual` rows), copied byte-identical in `e8d20aae` → `fixed:e8d20aae`.
  - 4240566263 (P2, tests:225): the design-review test now asserts "The orchestrator revises once per pair of results" → `fixed:21c160c8`.
  - 4240566266 (P2, SKILL.md:201): Worker Playbook step 2 opens the PR with `gh pr create --draft --head <branch>`, so step 15's `gh pr ready` starts the Bot timer on a draft → `fixed:21c160c8` (`test_workers_open_the_pr_as_a_draft`).
  - 4240566268 (P2, tests:285): the counters test now asserts "and pastes its output into the acceptance record" → `fixed:21c160c8`.
- Fifth item `052eea4c`: the boundary-PR sentence in the invariants now reads "each required job decides inside itself and reports success on an `.orchestration`-only diff; a skipped required job would report Success (fail-open), so no required job carries a job-level `if` or a `needs`." → `test_boundary_merge_sentence_names_the_in_job_decision`, added to `revise.yaml`. It describes PR 320's mechanism, which is not on `main` until PR 320 merges.
- The docs module runs 36 tests, OK; the four new proofs fail their tests, the old boundary clause pasted back among them (validation §8). This is fix round 1 of 2 under the A2 cap; `108b43bd` is the first Bot P1 head after RESULT `27ea99b2` (INV-6 counts heads).
- The final head's CI and Bot wait are in the RESULT and the main-checkout copy of this report.
