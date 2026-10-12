# Plan 006: Execute regime v3 by bottleneck, one correction at a time

> **Executor instructions**: the orchestrator executes this plan phase by phase and
> dispatches nothing outside it. Each atomic task names its work, its verification
> condition, its verification content, its completion condition and the metric it
> moves. A STOP condition always wins over task completion. The plan is landed in
> `plans/006-regime-v3-execution.md` by the first worker task (A101) and this copy is
> the orchestrator's record until then.
>
> **Drift check**: `git rev-parse origin/main` is `b896d9bc` or a descendant; the
> design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` hashes to
> `4520b8f0…` (v17 with its `design_review.receipt` naming round 18: hashed keys as in v17 `1d5f4c07…`, round 18 and the round-19 pointer confirmation accepted by both reviewers); the Phase A
> task files hash to process-rules a07 `d5d499ce…` (merged in #318 as e83e923d; a04 to a06 superseded), regime-counters a02 `a161f7e7…` (merged, #319), ci-skip a02
> `4de54fde…` (merged, #320), A7 parked: PR #323 draft at `dc7edcc0`, task `dotfiles-T128-worker-stop-and-watch-a02` `1de19e51…` (round-7 text `23417dde…` plus four pointer rounds, the a02 reset and one amendment); plan 007 T712 owns the continuation; the a01 dispatch hashes were `65fa3494…`, `69fee495…`, `6dd3d682…` (04:13Z).

## Status

- **Execution**: IN PROGRESS (Phase A at 01:41Z: PR #318 (A1/A2/A4) merged 01:40:38Z as e83e923d after the a03 to a07 lineage (audit of 92634b25 correct); A7 dispatched to a003 at 01:42Z on a fresh branch from e83e923d (PR #323, draft 01:47:33Z); boundary PR #322 merged 01:48:19Z as b67ea752 (1 min 21 s) and #324 merged 09:38:31Z as d1f98104 (1 min 58 s; plans 007/008 and the M/C records on main), A5's ≤ 10-minute criterion met twice; status at 01:50Z; merged: boundary #321 (09:40Z), A5 PR #320 (21:44Z, main 0e522059), A3 PR #319 (22:03Z, main 52575497: `scripts/regime-counters.sh` and the INV-6 boundary probe are on `main`; the orchestrator now runs the script itself before every acceptance action); PR #318 (A1/A2/A4): a03 updated onto 52575497 (b7ae2d54), audited (4 P2, revise round 1), then Bot P1 on two heads of that round (INV-6 reset to a04 at 22:42Z, record `dotfiles-T128-process-rules-a03-design-reset.md`); a04 amendment 1 at 22:56Z for a third P1 the orchestrator had missed; plan S1 at 23:08Z on the counters bullet (six Bot P1 threads of one class; cause record `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`): a05 by the review seat, the worker continues from 7800ef92 with one commit, then sweep, audit, gate, merge; A7 (PR #323) ran a01 (`84d8acde…` → `b0b84598…`) and a02 (`af519f0f…` → `1de19e51…`), two plan 007 S1 cycles and one INV-6 reset, and was parked as a draft at `dc7edcc0` on 2026-10-12 09:32Z by the operator (plan 008 decision 2, option D2); its content continues as plan 007 T712 (step 7 and step 15 as state tables); boundary #322 merged separately; A6 measured on the T712 PR (A7's PR #323 parked at dc7edcc0 missed it: wall, rounds and resets; heads met); V0 parked for B0)
- **Companion plan**: `007-mistakes-into-mechanisms.md` (recorded 2026-10-12 04:32Z at the operator's direction): the linked mistake and correction records, the three-repeat search-first procedure, and STOP S5/S6; its Phase 0 rules are in force for this plan's remaining work, and PR #323 (A7 a02, halted 03:3xZ) resumes only under S5.
- **Priority**: P0 (the regime cannot ship implementation while it loops)
- **Effort**: L
- **Risk**: MED (operator PRs on the critical path of Phases 4 and 6)
- **Planned at**: main `b896d9bc`, 2026-10-11, after the 2026-10-10 halt and the operator's directions of 2026-10-10 and 2026-10-11

## Goal and the three metrics

Goal: every rule of the regime is mechanical, the auditor can find the orchestrator's
and the worker's mistakes, and the auditor is never the queue. The plan is judged by
three measured numbers per merged PR, recorded in each acceptance record:

| metric | baseline (T118/T119/T124, boundary #316) | target by Phase 4 | target by Phase 7 |
|---|---|---|---|
| rounds per artifact (revise rounds per PR; review rounds per design or task file) | 5 to 20 per PR; 13+7 per design; 19 per task set | ≤ 2 per PR; ≤ 3 per design; 1 per task file | ≤ 1 per PR |
| wall time per PR (TASK to merge) | 10.6 h, 11.1 h; boundary merge 25 to 60 min | ≤ 4 h; boundary ≤ 10 min | ≤ 3 h |
| cost per PR (tokens where measurable; otherwise seat-hours and audit count) | n/a everywhere | measured on every PR | within tier budget |

## Working rules for the orchestrator (Phase 0, in force now)

- One revision per pair of reviewer results; no review round is opened while one is open.
- Design review: Claude and Codex on the same hash at once; at most 3 revision rounds; then freeze with a residual list.
- Pre-audit evidence check (2026-10-12 00:16Z, from the `evidence` class of PR #318, four audits in a row): the task-level audit starts only when the sweep fill reports zero gaps and the finding-class ledger check passes (every Bot top-level finding of the sweep and every `[P` line of the lineage's audits has a class row in the acceptance record); the orchestrator's `orch-audit.sh` refuses otherwise. A rule that requires a tool is dispatched after the tool is on `main` (the `tool-not-on-main` class). Pre-dispatch task-file consistency check (2026-10-12 00:55Z, from the `bookkeeping` class of PR #318, three findings on three successive task copies): before every dispatch and every anchor request the orchestrator runs `task-consistency-check.py` on the task file (task id equals the file name; `allowed_files` covers the task's own `.orchestration/<id>/**` and no other task's; the copies row names every `reset_of` id and the task; every allowed `tests/` path has an oracle row; no residual binds a predecessor's hash; the task names the design's current receipt: C1 to C6); V1's validator takes the six checks. Correction (2026-10-11 23:46Z, Bot 4243732324 on PR #318): the third pair freezes only on its accept; a revise or reject at the third pair freezes nothing and sends the design back to a context other than its author, never to a fourth pair.
- Task-file review: one round, stop condition = no contradiction with the design, premises hold, `allowed_files` complete, one invariant. One round applies per version of a task file's content: content added after the review (for example from a Bot finding on a boundary PR) gets one review of the addition only, counted as a further round in the record; a task file still under review is not carried by a boundary PR (A7 was, from 07:27Z to 09:40Z: its round-6 text reached `main` with #321 before the withdrawal commit; the next boundary carries its final text together with its dispatch).
- Boundary PRs carry records, not drafts (corrected 07:25Z: a hashed design change lands through a boundary PR before any task carrying one of its sentences is dispatched, as INV-2 says; see the correction below the Phase A table).
- Every revise ACCEPTANCE carries `previous_head=` and one `check=` test selector per finding (INV-3 by hand until V3c).
- Stage 2 is not skipped by a draft: the Codex Bot reviewed every non-draft PR (#310 to #316) and did not review draft #317 within the 15-minute window. Until A101 moves `gh pr ready` into the Worker Playbook before the Bot wait, the orchestrator marks the PR ready and posts `@codex review` on the RESULT head itself, waits for that review (15-minute cap), sweeps it, and only then audits.
- The orchestrator runs at `xhigh` from 2026-10-11T02:25Z (operator `/effort xhigh`), as S1 requires for the re-examination of this plan.

## STOP conditions

- **S1 (three repeated findings)**: the same class of finding three times on one artifact (design, task file, PR), from any reviewer, Bot or auditor. Stop that artifact. Switch the orchestrator to `xhigh` effort (operator `/effort xhigh`; effort changes keep the prompt cache on Fable 5.1), re-examine the plan phase that produced the artifact, record the cause in `.orchestration/learning/`, and resume only with a changed task or a changed plan step. Never a fourth round of the same thing.
- **S2 (reset)**: INV-6 counts (2 revises, 2 amendments, 2 questions, Bot P0/P1 on 2 post-RESULT heads, audit P0-P1 on 2 heads) stop the task and send it back to design by a context other than its author.
- **S3 (metric regression)**: a phase that worsens any of the three metrics against the previous phase's measurement is stopped and re-planned before the next phase.
- **S4 (operator boundary)**: any waiver, ruleset change, Actions policy change, or operator PR is named in the acceptance record and never performed silently.

## Phase A (operator direction 2026-10-11, approved 「すすめてよい」): establish the recommended pattern before any feature wave

The order below replaces the earlier interleaving: no implementation wave is dispatched until A1 to A5 are merged and A6 shows the pattern working on itself. V0 (PR #317) is parked at `98f1d250` as a draft and is re-specified under the pattern as the first Phase B task.

| # | target | content | verification condition | completion |
|---|---|---|---|---|
| A1 | SKILL (regime rules) | design review: both reviewers at once, one revision per pair, 3 rounds then freeze with a residual list; task-file review one round with the stop condition; boundary PRs carry records and gate nothing; trust-boundary tasks carry a threat table (what the PR controls, each entry closed / accepted residual with compensating control / out of scope) that is their completion condition | a separate context judges past task files (T119, V0) as failing the stop condition from the text alone | prettier green, docs test green, merged 2026-10-12 01:40:38Z as e83e923d (task `dotfiles-T128-process-rules-a01` → a02 → a03 → a04 → a05 → a06 → a07 on PR #318: six resets, INV-6 on five and plan S1 on two, plus the `bookkeeping` S1 answered by the pre-dispatch check; S1 2026-10-11 23:08Z on the counters bullet changed this row's form: the acceptance-decision bullet states obligations by reference (the script's output pasted; a pasted reading per INV-6 component the script prints as `unknown`; S1 from the record's finding-class table) and names no source; cause record `.orchestration/learning/plan-006-s1-process-rules-counters-bullet-2026-10-11.md`) |
| A2 | SKILL Worker Playbook | `gh pr ready` before the Bot wait; at most 2 Bot-fix rounds before RESULT, the third is reported not fixed; revise ACCEPTANCE carries `previous_head` and one failing-test selector per finding | the round cap and the report form appear once in the text | same PR as A1 |
| A3 | `scripts/regime-counters.sh` + `check-regime-boundary.sh` | per task from history and GitHub: TASKs, amendments, questions, RESULTs, revises, Bot P0/P1 heads after the first RESULT, audits, wall; S1/S2 thresholds printed; the orchestrator runs it before every acceptance action (rule in A1) | replay on T118 (9 revises by INV-6's count, 10 RESULTs), T119 (9 amendments), T124 W1 (Bot P1 on 2 heads after the first RESULT head), V0 (6 Bot P1 heads after the first RESULT head adcf783b) prints those values and the threshold lines | unit tests, `make check-regime-boundary` green, merged (task `dotfiles-T128-regime-counters-a01`) |
| A4 | `AGENTS.md` Code Review Rules | `.orchestration/**` are records and specifications: the Bot reviews them for secrets and home paths only; for trust-boundary code the Bot reviews against the task's threat table and reports missing entries; accepted residuals are not re-raised | the next `.orchestration`-only PR draws no design thread from the Bot | same PR as A1 |
| A5 | `remote.yaml`, `test.yaml` | `.orchestration`-only diffs skip the heavy steps with step-level `if`s; every required context reports success; push and schedule always run | an `.orchestration`-only PR merges within 10 minutes with every required check reported | `gh pr checks` timings in the acceptance record (task `dotfiles-T128-ci-skip-orchestration-a01`) |
| A6 | self-verification | first run on A3's PR #319 (a01 → a02): rounds ≤ 2 and Bot P0/P1 heads ≤ 2 were met, wall was 3 h 26 min against ≤ 2 h (two orchestrator specification gaps and one reset; cause and figures in `.orchestration/acceptance/dotfiles-T128-regime-counters-a02.md`), so the wall criterion is not met by A3 and A6 is re-run on A7's PR (the next Phase A PR, under the worker self-stop rule it introduces) with the same three criteria; the A3 figures stand as the pattern's first measurement | rounds ≤ 2, wall ≤ 2 h, Bot heads ≤ 2 on A7's PR | the three metrics in A7's acceptance record; Phase B (B0) starts only after that record shows the criteria met, or the operator re-plans the criterion |
| A7 | SKILL Worker Playbook step 15 + Orchestrator Playbook step 7 (`dotfiles-T128-worker-stop-and-watch-a01`, after process-rules-a07 (merged) and regime-counters-a02) | worker-side stop: before each fix commit the worker counts Bot P0/P1 heads after its first RESULT head and Bot thread classes from its step-15 listing and stops at 2 heads (INV-6) or 3 of a class (S1) with `AGMSG-PONG status=blocked note=S1|INV-6;heads=…;classes=…;threads=…`; before each push it runs `regime-counters.sh --history-only`; orchestrator-side watch: GitHub and history every 30 minutes after a TASK, PING at 45 minutes without a push, PONG or RESULT, despawn when the PING stays unread while pushes continue past a cap or count; hook-level enforcement stays V3a's; PARKED 2026-10-12 09:32Z at PR #323 `dc7edcc0` (plan 008 decision 2): the rules land through plan 007 T712 as state tables; A7 edits step 15 and step 7, so its commit updates `tests/fixtures/regime/worker-step-15.md` and `orchestrator-step-7.md` (a05 item 10's golden sections) and its `allowed_files` names them; one more finding of the `step15-wait` class on A7's PR stops A7 for a re-specification of step 15 as one state machine | fourteen docs-test tokens, each failing when its sentence is removed, and the two section fixtures updated in the same commit; the worker rule exercised on A7's own PR | merged with its audit `correct` |

**Correction (2026-10-11 07:25Z, from the audits of PR 320):** the Phase 0 rule that a boundary PR is never a dispatch prerequisite contradicts INV-2's hashed sentence (the design must be on `main` before the implementing TASK is dispatched, and the task's invariant sentence must equal `main`'s). INV-2 wins: a hashed design change lands on `main` through a boundary PR before any task that carries one of its sentences is dispatched; a boundary PR still carries no task draft under review. For the Phase A tasks already dispatched under the old rule, the boundary PR `orchestration/boundary-2026-10-11-2` carries design v16 before their final audits and merges, and each PR takes the new base with `gh pr update-branch`. The A1 bullet on `main` after PR #318 says the same (a follow-up docs item if its wording still carries the old sentence).

Dormant-contract PRs are withdrawn from the pattern (Phase B's first design change narrows INV-12 to the undeclared-mode regression guard); `dotfiles-T128-ci-skip-orchestration-contract-a01` is superseded.

Notes carried into Phase B task files from the Phase A review (2026-10-11): V1's `schemas/task.json` takes `threat_table` as an optional list of `{control, disposition}` with `disposition` matching `^(closed|residual|out-of-scope): ` and `after` as an optional list of task ids (PR-2); the design's INV-6 enforcement row and V3a bullet name `scripts/regime-counters.sh`, and the design's own `design_review.receipt` moves to round 16, at the next hashed change (round-16 Claude notes).

## Phases (bottleneck order), atomic tasks, verification, completion (Phase B onward, after A6)

### Phase 1: remove the loop sources (bottleneck 1: rounds)

- **A101, A102**: executed in Phase A (A1/A2/A4 on PR #318 as `process-rules-a01` → a02 → a03 → a04 → a05 → a06 → a07, merged as e83e923d; the map amendments as design rounds 16 to 19). No Phase B work remains here.

### Phase 2: remove the CI wait (bottleneck 2: boundary and PR wall time)

- **A201**: executed in Phase A (A5 on PR #320 as `ci-skip-orchestration-a01` → a02, in-job fail-closed decision, no `changes` job, no `needs`). The ≤ 10-minute measurement is taken on the first `.orchestration`-only PR after its merge and pasted into its acceptance record.

### Phase 3: deterministic verification first (bottleneck 1 again: rounds come from model-judged review)

- **B0** design amendment (one review pair, then a boundary PR before any Phase B dispatch, as INV-2 requires): INV-12 narrowed to the undeclared-change regression guard; the dormant-contract clause removed; `main-tests` decides inside its own job like A5's workflows (no `changes` job, no `needs`). B0's hashed changes also add the V0 successor's `implementing_tasks` entry (`<new V0 id>: [INV-12]`, beside the parked a01 entry) and any other Phase B successor id, so INV-2's map lookup holds for them on `main` before dispatch. B0 also re-specifies every Phase B task file that touches a trust boundary (V1, V1b, V1c, V2, V2b, V3a to V3d, V4, V5a, V5b, V6) with a `threat_table` and the A1 rules (premises as pasted output, one task-file review round each) before its dispatch; no Phase B task is dispatched from its pre-Phase-A text.
- **A301** V0: re-specified under the pattern by a context other than its author as a new task id (PR #317 stays parked as input: its 14 Bot threads and the audit of `adcf783b`), with a threat table, the in-job decision A5 established, and the narrowed INV-12 from B0.
  - Verification condition: the six named test selectors fail on `adcf783b` and pass on the new head; the audit of the new head is `correct`; `main-tests` runs main's harness against the PR.
  - Verification content: validation file with both runs pasted; audit `.last.md`; CI log of `main-tests` on the new head.
  - Completion: merged with `--match-head-commit`; `main-tests` listed as a required check (S4: named in the acceptance record); acceptance record carries rounds, wall, audit count.
  - STOP: S1 if the next audit repeats a finding class of this audit (that would be the third time for "PR-controlled input before the trusted step").
- **A302** V1 (`dotfiles-T128-v1-task-schema-a01`; no contract PR, withdrawn by the Phase A correction): schema (with `threat_table`, `reset_of`, `after`), validator, tier derivation. When it lands, the schema is the single owner of the threat-table shape and the AGENTS.md Code Review bullets shrink to one review sentence and a pointer (the `scope` class of PR #318, five findings on three restatements). The validator also takes the six cross-field checks of `task-consistency-check.py` (the `bookkeeping` class).
  - Verification: `scripts/validate-task.py` rejects each gaming fixture (62 removal cases from PR #313 as the test idea source); `main-tests` green.
  - Completion: merged; audit `correct`; metrics recorded.

### Phase 4: the auditor off the critical path (bottleneck 3: audit serial queue)

- **A401** V2 (`dotfiles-T128-v2-audit-schema-and-runner-a01`; no contract PR): schema-validated audit, trusted root, pool of two, `make audit-head` auto-start, `AGMSG-AUDIT` record, atomic reservation of a head so a second run of the same head is refused (INV-5).
  - Verification condition: two audits of two heads run concurrently from the orchestrator's checkout and each lands its record; a re-run of the same head is refused; an evidence-only head reuses the audit.
  - Verification content: two concurrent `make audit-head` runs pasted with their history records; the refusal; the reuse.
  - Completion: merged; the next PR's audit starts within 5 minutes of green CI by the orchestrator's `make audit-head` (no daemon or watcher; V2 forbids one), measured from the CI completion time to the audit's start; audit wall ≤ 20 minutes.
  - Metric: wall time per PR; audit count per PR.
- **A402** V2b (operator PR: gate reads the JSON, category lock, tree-equality reuse).
  - Verification: `make require-crit-review` refuses a hand-edited `.last.md`; accepts an evidence-only head; refuses a `not-applicable` on an orchestration finding.
  - Completion: merged; Codex security-profile review recorded.

### Phase 5: the CI gate for task files and PR shape

- **A501** V1c (`regime` job: task.md validation, workflow-edit refusal), then **A502** V1b (caps, invariant set and sentences, contract-id lookup).
  - Verification: a PR without task.md is refused; an over-cap PR is refused; a wrong invariant sentence is refused; the `workflow_dispatch` dry run against closed PR #313 passes.
  - Completion: merged; `regime` listed as required; the Actions event policy allows `pull_request_target` (S4; deadline 2026-11-02).
  - Metric: rounds per PR (task defects found at dispatch, not in rounds).

### Phase 6: the reset made mechanical

- **A601** V3a (operator PR: counters in the gate and the Stop hooks, `regime-waive.sh`, boundary detector), **A602** V3b, **A603** V3c, **A604** V3d.
  - Verification: a replay of T119's history against the counters fires the reset at the amendment count; a replay of this plan's own design-review history fires S1 at round 3.
  - Completion: merged; the replays pasted in the acceptance records.
  - Metric: rounds per artifact (hard-stopped).

### Phase 7: the rest

- **A701** V4 (design-review runner, both identities), **A702** V5a, **A703** V5b (cost fields; from here every acceptance record carries measured tokens), **A704** V6 (permgate; operator PR).
  - Completion: each merged with its audit `correct`; the three metrics recorded; the plan's targets compared with the measurements in `plans/README.md`'s status row.

## Finding coverage (every repeated finding of 2026-10-10/11 is assigned once)

| class | where it repeated | plan task that removes the cause |
|---|---|---|
| no convergence condition for review | design rounds 1-13, task-file rounds 1-19 | Phase 0 rules; A101 |
| Bot reviewing drafts on every boundary push | #316: 12, 10, 6, 8, 7, 4 threads | A101 (Bot scope), Phase 0 (boundary cadence) |
| 25-minute bootstrap on `.orchestration`-only diffs | every boundary push | A201 |
| audit as a serial, orchestrator-started step | T119 (4 audits, 1.3 h), V0 | A401 |
| orchestrator-authored evidence trusted by the gate | Codex rounds 7-9; V0 audit finding 7 | A402, A601, A703 |
| PR-controlled input executed before a trusted step | V0 audit findings 1-3 | A301 revise 1; STOP S1 if it recurs |
| task text keyed on the wrong object | V0 audit finding 4 (orchestration) | A301 revise 1; A501 (task validation), A101 (task stop condition) |
| waiver the orchestrator can write | Codex round 7, 8 | A601 (`regime-waive.sh`, record outside sandbox write roots) |

## Plan quality self-audit

- [x] Phases ordered by the measured bottleneck, not by invariant number.
- [x] Every atomic task has a verification condition, verification content, completion condition and a metric.
- [x] STOP S1 encodes the operator's rule: three repeated findings stop the artifact and re-examine the plan at `xhigh`.
- [x] Operator actions (ruleset, Actions policy, operator PRs) are named per task (S4).
- [x] The repository's plan conventions (`plans/README.md`: drift check, finding coverage, status, DONE needs audit plus review/CI evidence) are followed; this file is landed in `plans/` by A101.
- [ ] Operator review of this plan before the next dispatch (A101 onward); A301 continues because it is required by every ordering.
