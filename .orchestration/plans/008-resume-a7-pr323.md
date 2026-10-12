# Plan 008: Resume A7 (PR #323) under plan 007, or not: the decision for the operator

> **Executor instructions**: this plan records the resumption of PR #323 (`dotfiles-T128-worker-stop-and-watch-a02`, head `3a54d340`) as a plan, in plan 007's S7 report form. Nothing in it is executed until the operator chooses an option below. Every figure is pasted command output of 2026-10-12.
>
> **Drift check (at planning time, 04:4xZ; every line below has since moved)**: `git rev-parse origin/main` is `b67ea752`; PR #323 is `OPEN` at `3a54d340e9078ba3565237f6d73a00d8fc2d75e9` with CI 13 of 13 green, all 23 Bot threads replied and resolved, sweep 85 of 85 dispositioned, ledger 24 rows plus the four audit rows, audit `…-a02-audit-3a54d34.md` verdict `incorrect` with four findings; the worker `claude-standard-dot-a003` holds (ACCEPTANCE `under_review`, 03:32Z); the review seat `claude-review-dot-a001` is idle; no amendment or revise has been sent since the operator's halt. If any of these moved, re-read before acting.
>
> **State after decision 2 (09:32Z; re-read 10:49Z, main `c1ae5531`)**: PR #323 is a draft parked at `dc7edcc0` under `dotfiles-T128-worker-stop-and-watch-a02` (`1de19e51…`); worker `claude-standard-dot-a003` released (ACCEPTANCE `superseded`, 09:32:14Z); the review seat `claude-review-dot-a001` re-seated 10:05Z; T712 owns the continuation. This plan is DONE and nothing in it is executed again.

## Status

- **Execution**: DONE: decision 1 = option A (04:4xZ, executed: R1 records, R2 amendment 1 at `1de19e51…`, R3 revise round 1 landed as `dc7edcc0`); decision 2 = option D2 (09:32Z, executed: R7 park at `dc7edcc0`, corrected replies posted, worker released); T712 owns the continuation
- **Priority**: P1 (A7 is the worker-side early stop that plan 007 C-1 and C-8 rely on; A6 is measured on it)
- **Effort**: S to M depending on the option
- **Planned at**: main `b67ea752`, 2026-10-12 04:4xZ

## Decision for the operator (plan 007 S7 report)

### Situation

- Merged: A3 (#319), A5 (#320), A1/A2/A4 (#318, audit `correct` at `92634b25`), boundaries #321 and #322. Not merged: A7 (#323).
- PR #323 history: a01 TASK 01:42Z; Bot passes on `9d001bcb` (6 threads), `2c8dce27` (2), `040b32f9` (6), `3ba70625` (5), `e924c5df` (1), `1d14eed5` (3), `3a54d340` (1, P2 `not-applicable` by the orchestrator); one plan S1 (`class-count-scope`, six findings, 02:17Z) answered by narrowing the worker's count back to the Codex Bot's badged findings; one INV-6 reset (a01 → a02, revises, 02:49Z); 23 threads, all answered and resolved.
- Audit of `3a54d340` (03:31Z): `incorrect`, four findings: (1) P2 the watcher's fix-round definition counts only P0/P1 predecessors while the worker's `fix_rounds` and the A2 cap count any badged fix (this PR's `2c8dce27 → 040b32f9` followed P2s); (2) P2 the orchestrator's `not-applicable` on 4244248692 was wrong on two facts (the threat-table rule names orchestrator effects; the forced removal is not behind a human-only gate: `defaultMode: auto`, `ask: []`); (3) P2 the orchestrator's `not-applicable` on 4244378809 claimed a mismatched RESULT head is "never counted" while `scripts/regime-counters.sh:114` takes the first RESULT permanently; (4) P3 premise 1 of the task record says six reviewed heads after 03:09Z where its own output lists four.
- Counters now (`scripts/regime-counters.sh dotfiles-T128-worker-stop-and-watch-a02`, 03:20Z): `tasks=1 amendments=0 questions=1 results=1 revises=0 bot_p1_heads_after_result=0`. Budget left under INV-6 before a reset to a03: one amendment, one revise, one question, two Bot P0/P1 heads.
- Round costs measured on this repository: Bot pass median 4.7 min, CI median 8.5 min, reset about 20 min, audit about 8 min.

### Problems and open issues

- Two of the four audit findings are the orchestrator's dispositions, not the worker's text: plan 007 M-3 (evidence-less `not-applicable`).
- The fix-round definition and the RESULT-head contract sentence are one-line text changes on the SKILL and the Message Contract; the forced-removal row and the premise figure are task-record changes.
- A6's two-hour wall from the a01 TASK (01:42Z) is already missed (03:42Z passed during the halt); the measurement on this PR can only report the figure.
- `step15-wait` (M-6) says step 15 should become a state table in Phase B; A7's text adds more clauses to the same imperative procedure.

### Root cause (plan 007 M records)

- M-3: dispositions written without re-reading the script and the settings; M-4: task-record fields maintained by hand (the premise figure; the row); M-1: the fix-round definition was written for the INV-6 head count and not checked against the A2 cap's own count (`fix_rounds`); M-5: each of these costs a Bot pass and a CI run.

### Proposals for the target state

| Option | What happens | Rounds and time | Counters after | Risk |
|---|---|---|---|---|
| **A. Continue in place (recommended)** | T700 backfill first (S5). Then a02 amendment 1 (forced-removal row stating the real mode and the pre-removal verification; premise 1 corrected to its own evidence) and INV-3 revise round 1 (fix-round = any badged finding; the contract sentence: the orchestrator checks `head=` against the PR head on the first RESULT, a mismatch is a revise and not the baseline); corrected replies on 4244248692 and 4244378809 with `evidence=`; one worker commit on the current head; Bot pass; re-sweep; re-audit; gate; merge; boundary PR with 007/008 and the records. | 1 worker commit, 1 Bot pass, 1 CI, 1 audit: about 35 to 45 min of wall after the go | amendments 1, revises 1, questions 1, heads 0 to 1 | one more finding of any counted kind resets a02 to a03 (a 20-minute successor, not a loss of content); the Bot may raise a new P1 on the revise head (an INV-6 head) |
| **B. Reset to a03 now** | The review seat writes a03 = a02 plus the four fixes (both text changes and both record changes) in one successor; the worker lands one commit; the rest as A. | 1 redesign (20 min) + 1 commit + 1 Bot pass + 1 CI + 1 audit: about 50 to 60 min | fresh budget (amendments 0, revises 0) | spends a reset on findings that fit inside a02's remaining budget; A6 figures record one more reset |
| **C. Merge the content now, record the rest as debt** | Disposition finding 1 and 3 as `not-applicable` with evidence and merge `3a54d340`; fix the two text lines in Phase B's step-15 table (T712). | 0 rounds; gate and merge about 10 min | unchanged | not allowed as written: finding 1 is a real defect with no refutation, and plan 007 S5/S6 forbid closing an `incorrect` audit without a landed mechanism; listed for completeness, not viable |
| **D. Park #323; fold A7 into the step-15 state table (T712)** | Close #323 as draft at `3a54d340` (input, like PR #317 for V0); write step 15 as a state table in Phase B with A7's rules as rows; one new PR later. | 0 rounds now; the Phase B task later costs one review pair and one PR | A7 counters frozen as recorded | the worker-side early stop (C-1, C-8) is not on `main` until Phase B; plan 007 Phase 2 and the merge-queue measurement run without it; A6 is measured on the later PR instead |

The same list without the recommendation: A (continue in place), B (reset to a03 now), C (merge now with debt; not viable under 007), D (park and fold into the step-15 table).

Recommendation and why: A. The four findings are small and fit inside a02's remaining budget; A7's text is otherwise audited as holding INV-1, 12 and the fixtures; parking (D) delays the worker-side stop that plan 007's detectors assume, and a reset (B) spends 20 minutes to buy budget that A does not need unless the Bot finds a new class. If A hits one more counted finding, the rule's own path is B, with nothing lost.

## Atomic tasks (executed only for the chosen option)

- **R1** (A, B, D) Backfill the four audit findings and the halt as plan 007 M/C records (M-3 and M-8 gain these instances; C-5 and C-11 name them), `index.yaml` updated; the acceptance record of a02 cites the ids. Verification: every finding has an M row and a C id. Completion: records in the main checkout.
- **R2** (A) a02 amendment 1: the forced-removal row with `control: herdr-agents --remove-worker --force on a crossed cap (an orchestrator in-process effect)` and `disposition: residual: before removal the orchestrator re-reads the PR number from the task's branch, compares the identity's worktree with the TASK's repo=, re-derives the counts from a fresh listing, preserves the stopped worktree's evidence and logs the removal; the session runs auto mode (classifier), so the human prompt is the settings ask rule of plan 007 T710 once landed`; premise 1 reads four heads after 03:09Z from its own output. C1 to C6 `OK`; review seat confirms the hash; the reset record stays (no new reset). Verification: checker `OK`; hash confirmed. Completion: dispatched with R3.
- **R3** (A) INV-3 revise round 1: step 7 "A fix round is a push whose predecessor head carries a Codex badged finding of any priority…"; Message Contract "When the first RESULT arrives the orchestrator checks its head= against the PR's head (gh pr view <n> --json headRefOid); a mismatch is answered with status=revise and that RESULT's head is not the baseline"; fixtures `orchestrator-step-7.md` and `message-contract.md` updated; `check=` the watch test, the contract test and the whole-section test; `previous_head=3a54d340…`. Verification: tokens present; fixtures equal sections. Completion: RESULT with the new head.
- **R4** (A, B) Corrected replies on 4244248692 and 4244378809 (`fixed:<sha>` with `evidence=`), re-sweep last, fill, ledger check with the four audit rows, audit of the new head, record, gate, merge `--match-head-commit`, `ff-main`, final ACCEPTANCE. Verification: audit `correct` or every finding dispositioned with evidence; gate `rc=0`. Completion: merged; A6 figures (rounds, heads, resets, wall from 01:42Z) pasted into the a02 record as "not met on the wall, met on rounds and heads" or as measured.
- **R5** (A, B, D) Boundary PR carrying plans 007 and 008, the M/C records, the A7 records and this decision; the next boundary measured against A5's ten minutes.
- **R6** (B only) The review seat writes a03 from a02 plus the four fixes; checker, anchor, dispatch, then R4.
- **R7** (D only) Close #323 as draft with a note naming it as input for T712; record the A7 counters as final.

## STOP conditions

- Plan 007 S5 and S6 apply to R2 to R4 (records first; search pasted if any class reaches three).
- Plan 007 S7: if option A produces one more counted finding after R3, stop again and report (do not go to B silently).
- Plan 006 S4: R2's row names the permission mode; the `ask` rules themselves are T710 (operator PR).

## Finding coverage

| Audit finding of `3a54d340` | Option A task | M / C |
|---|---|---|
| 1 fix-round definition | R3 | M-1 / C-8 |
| 2 forced-removal row and the wrong "human-only gate" | R2, R4 | M-8 / C-11 |
| 3 RESULT-head baseline claim | R3, R4; the script part to plan 007 C-7 (V3a row) | M-3 / C-5 |
| 4 premise 1 figure | R2 | M-4 / C-3 |

## Decision 2 for the operator (plan 007 S7, 2026-10-12 05:1xZ): the second S1 cycle on PR #323

### Situation

- Option A ran: records first (8 M, 11 C, index), amendment 1 (`1de19e51…`, anchored by the review seat after one correction of the introduction), revise round 1; the worker landed one commit `dc7edcc0` (task copy, the two sentences, two fixtures, tokens); CI 13 of 13; audit findings 1 and 3 fixed; the two refuted dispositions have corrected, evidence-bearing replies scripted but not yet posted.
- The Bot's pass on `dc7edcc0`: five P2, no P0/P1. Counters: amendments 1, revises 1, questions 1, INV-6 heads 0. Any further text change is a second revise or amendment, which is a reset to a03 by rule.
- Ledger after this pass: `watch-ping-trigger` 5, `fix-round-definition` 3, `result-head-binding` 3, `class-count-scope` 7 (closed by the narrowing). Plan 007 S7 applies: this is the second S1 cycle on the same task; the orchestrator has stopped.
- Wall from the a01 TASK (01:42Z): 3 h 27 min at this report; Bot passes on this PR: 8; resets: 1; S1 cycles: 2.

### Problems and open issues

- Four of the five P2s are edge cases of the step-7 watch and removal procedure and of the fix-round rule (a push in flight at the PING; "without a push" undefined without push times; the pre-removal checks live in the task row, not in step 7; step 7 counts fix rounds at any priority while step 15 caps P0/P1 fixes). Each clause fixed so far has produced the next clause; seven Bot passes on this PR, 28 threads.
- The fifth (`regime-counters.sh` keeps the first RESULT as the baseline) is a script change outside A7's scope, already a plan 007 C-7 item (V3a).
- The sentence I supplied in R3 ("any badged finding of any priority") created the step 7 versus step 15 contradiction; the audit's finding 1 asked for consistency with the worker's practice, and the consistent form is one cap rule stated once for both playbooks.

### Root cause

- M-6's twin for step 7: the watch and removal procedure is a state machine (inputs: pushes, CI, Bot passes, PING, PONG, RESULT; states: watching, pinged, stopped, removed) written as clauses; clause-level review finds one transition per pass. M-3 again for the R3 sentence written against the audit's wording instead of the cap rule's single owner.

### Proposals for the target state

| Option | What happens | Rounds and time | Risk |
|---|---|---|---|
| **B2. Reset to a03 with the five fixes as text** | The review seat writes a03 = a02 plus: one cap rule ("a fix round is a push answering a Codex badged finding; at most two before the third round is reported") stated in step 15 and referenced from step 7; step 7 states the pre-removal checks; "continued pushing" defined as a commit newer than the PING's `read_at` seen one watch interval later, "without a push" as the head sha unchanged for 45 minutes; the contract keeps the head check and names the script's baseline limitation as plan 007 C-7. Worker: one commit; Bot pass; sweep; audit; gate; merge. | redesign 20 min + commit + CI 8.5 + Bot 5 + audit 8 + gate and merge: about 55 to 65 min | an eighth Bot pass on the same clauses; by the record, each pass on step 7 and 15 has found new edges; a ninth pass means a04 |
| **D2. Park at `dc7edcc0`; redesign step 7 and step 15 as state tables (plan 007 T712) and land them as one Phase B task (recommended)** | #323 stays a draft at `dc7edcc0` as input (its fixtures, the contract `head=`, the badged counting, the records); T712 writes both steps as state and transition tables with one token per transition and whole-section fixtures, the five open threads and the two S1 classes as rows; one new task id, one PR. The two refuted dispositions get their corrected replies now (records only). | 0 rounds now; later one design pair for the tables (B0 scope) and one PR (about 60 to 90 min including review) | the worker-side early stop reaches `main` later; plan 007 Phase 2 and the merge-queue measurement run without it; A6 is measured on the T712 PR |
| **A2. Merge `dc7edcc0` now with the five P2s dispositioned** | 4244811164 `not-applicable` with evidence (outside scope, C-7); the other four would need `fixed:` and have no fix on this head | 0 rounds | not viable under plan 007 S5 and S6 and the pr-integration rule: four real defects without a fix or a refutation |

The same list without the recommendation: B2 (reset to a03 with text fixes), D2 (park and redesign both steps as state tables), A2 (merge with debt; not viable).

Recommendation and why: D2. Two S1 cycles on one task, seven Bot passes, and three classes at three or more all point at the same cause: the watch and the wait are state machines written as prose, and every clause-level fix has drawn the next clause. B2 spends a reset on the eighth clause-level pass of the same kind; D2 changes the form, which plan 007 already schedules (T712) and which M-6 named before this cycle. Nothing of A7's work is lost: `dc7edcc0` holds the fixtures, the contract field, the counting rule and the records, and the state tables start from them.
