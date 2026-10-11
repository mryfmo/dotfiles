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
> `1d5f4c07…` (v17: v16 `15957fbc…` plus the two reset-successor map entries; round 18 accepted by both reviewers); the Phase A
> task files hash to process-rules `65fa3494…`, regime-counters `69fee495…`, ci-skip
> `6dd3d682…` (after the one task-file review round, 04:13Z; dispatch hashes).

## Status

- **Execution**: IN PROGRESS (Phase 0 applied 2026-10-11; Phase A at 07:00Z, nothing merged yet: PR #318 (A1/A2/A4, a003) reset twice under INV-6 on the orchestrator's own specifications (a01: the disposition-grammar class, S1; a02: the amendment threshold after the Bot found no threat table and the review seat a missing row), continuing as a03 written by the review seat; PR #319 (A3, a004) audited `incorrect` at 72764f05 (token matching anywhere in a body; a reset record naming an unrelated accepted design; 1735 added lines under tests/ against INV-2's 1000) and reset the same way, successor a02 being written by the review seat; PR #320 (A5, a003) audited `incorrect` at d6343494 (rename detection in test.yaml's decision; quoted YAML keys in the structural tests) and in revise round 1; the live replay of A3 matched the fixtures; every accepted record now carries pr=; V0 PR #317 parked)
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
- Task-file review: one round, stop condition = no contradiction with the design, premises hold, `allowed_files` complete, one invariant.
- Boundary PRs carry records, not drafts; a boundary PR is never a prerequisite of a dispatch.
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
| A1 | SKILL (regime rules) | design review: both reviewers at once, one revision per pair, 3 rounds then freeze with a residual list; task-file review one round with the stop condition; boundary PRs carry records and gate nothing; trust-boundary tasks carry a threat table (what the PR controls, each entry closed / accepted residual with compensating control / out of scope) that is their completion condition | a separate context judges past task files (T119, V0) as failing the stop condition from the text alone | prettier green, docs test green, merged (task `dotfiles-T128-process-rules-a01`) |
| A2 | SKILL Worker Playbook | `gh pr ready` before the Bot wait; at most 2 Bot-fix rounds before RESULT, the third is reported not fixed; revise ACCEPTANCE carries `previous_head` and one failing-test selector per finding | the round cap and the report form appear once in the text | same PR as A1 |
| A3 | `scripts/regime-counters.sh` + `check-regime-boundary.sh` | per task from history and GitHub: TASKs, amendments, questions, RESULTs, revises, Bot P0/P1 heads after the first RESULT, audits, wall; S1/S2 thresholds printed; the orchestrator runs it before every acceptance action (rule in A1) | replay on T118 (9 revises by INV-6's count, 10 RESULTs), T119 (9 amendments), T124 W1 (Bot P1 on 2 heads after the first RESULT head), V0 (6 Bot P1 heads after the first RESULT head adcf783b) prints those values and the threshold lines | unit tests, `make check-regime-boundary` green, merged (task `dotfiles-T128-regime-counters-a01`) |
| A4 | `AGENTS.md` Code Review Rules | `.orchestration/**` are records and specifications: the Bot reviews them for secrets and home paths only; for trust-boundary code the Bot reviews against the task's threat table and reports missing entries; accepted residuals are not re-raised | the next `.orchestration`-only PR draws no design thread from the Bot | same PR as A1 |
| A5 | `remote.yaml`, `test.yaml` | `.orchestration`-only diffs skip the heavy steps with step-level `if`s; every required context reports success; push and schedule always run | an `.orchestration`-only PR merges within 10 minutes with every required check reported | `gh pr checks` timings in the acceptance record (task `dotfiles-T128-ci-skip-orchestration-a01`) |
| A6 | self-verification | A3's PR is accepted with the pattern: threat table in its task, one task-file review round, Bot cap, counters printed before acceptance, one audit | rounds ≤ 2, wall ≤ 2 h, Bot heads ≤ 2 on that PR | the three metrics in its acceptance record |
| A7 | SKILL Worker Playbook step 15 + Orchestrator Playbook step 7 (`dotfiles-T128-worker-stop-and-watch-a01`, after a03 and regime-counters-a02) | worker-side stop: before each fix commit the worker counts Bot P0/P1 heads after its first RESULT head and Bot thread classes from its step-15 listing and stops at 2 heads (INV-6) or 3 of a class (S1) with `AGMSG-PONG status=blocked note=S1|INV-6 …`; before each push it runs `regime-counters.sh --history-only`; orchestrator-side watch: GitHub and history every 30 minutes after a TASK, PING at 45 minutes without a push, PONG or RESULT, despawn when the PING stays unread while pushes continue past a cap or count; hook-level enforcement stays V3a's | eight docs-test tokens, each failing when its sentence is removed; the worker rule exercised on A7's own PR | merged with its audit `correct` |

**Correction (2026-10-11 07:25Z, from the audits of PR 320):** the Phase 0 rule that a boundary PR is never a dispatch prerequisite contradicts INV-2's hashed sentence (the design must be on `main` before the implementing TASK is dispatched, and the task's invariant sentence must equal `main`'s). INV-2 wins: a hashed design change lands on `main` through a boundary PR before any task that carries one of its sentences is dispatched; a boundary PR still carries no task draft under review. For the Phase A tasks already dispatched under the old rule, the boundary PR `orchestration/boundary-2026-10-11-2` carries design v16 before their final audits and merges, and each PR takes the new base with `gh pr update-branch`. The A1 bullet on `main` after PR #318 says the same (a follow-up docs item if its wording still carries the old sentence).

Dormant-contract PRs are withdrawn from the pattern (Phase B's first design change narrows INV-12 to the undeclared-mode regression guard); `dotfiles-T128-ci-skip-orchestration-contract-a01` is superseded.

Notes carried into Phase B task files from the Phase A review (2026-10-11): V1's `schemas/task.json` takes `threat_table` as an optional list of `{control, disposition}` with `disposition` matching `^(closed|residual|out-of-scope): ` and `after` as an optional list of task ids (PR-2); the design's INV-6 enforcement row and V3a bullet name `scripts/regime-counters.sh`, and the design's own `design_review.receipt` moves to round 16, at the next hashed change (round-16 Claude notes).

## Phases (bottleneck order), atomic tasks, verification, completion (Phase B onward, after A6)

### Phase 1: remove the loop sources (bottleneck 1: rounds)

- **A101** `dotfiles-T128-process-rules-a01` (docs tier, Claude seat, after A301 merges): SKILL review protocol, task-file stop condition, Bot scope (`AGENTS.md` Code Review Rules: `.orchestration/**` drafts are reviewed only for secrets and home paths), boundary cadence, Worker Playbook step 15 `gh pr ready` before the Bot wait and `@codex review` as the explicit trigger when no review arrives in 10 minutes; lands this plan in `plans/006-regime-v3-execution.md` and `plans/README.md`.
  - Verification condition: a boundary push with a changed task draft draws no Bot design thread; the next design review closes within 3 rounds.
  - Verification content: PR #N's Bot threads listed by `scripts/pr-feedback.py`; the next design's review receipts counted.
  - Completion: merged; `make validate-agent-assets` green; the two counts recorded in the acceptance record.
  - Metric: rounds per artifact.
- **A102** Plan amendment (design `implementing_tasks` gains the CI-skip task; one joint confirmation of the new hash, Claude and Codex at once).
  - Verification: both receipts `accept` on the same hash within one round.
  - Completion: receipts recorded; design hash updated in every task file.

### Phase 2: remove the CI wait (bottleneck 2: boundary and PR wall time)

- **A201** `dotfiles-T128-ci-skip-orchestration-a01` (design tier, Claude seat): `remote.yaml` and `test.yaml` skip the bootstrap and test matrices on an `.orchestration`-only diff with the jobs reporting success (the `changes`-job pattern).
  - Verification condition: an `.orchestration`-only PR merges in ≤ 10 minutes with every required check reported.
  - Verification content: `gh pr checks` timings on the next boundary PR pasted.
  - Completion: merged; boundary merge time recorded.
  - Metric: wall time per PR.

### Phase 3: deterministic verification first (bottleneck 1 again: rounds come from model-judged review)

- **A301** V0 `dotfiles-T128-v0-main-tests-a01` (in flight, PR #317, revise round 1 after an `incorrect` audit with 7 findings).
  - Verification condition: the six named test selectors fail on `adcf783b` and pass on the new head; the audit of the new head is `correct`; `main-tests` runs main's harness against the PR.
  - Verification content: validation file with both runs pasted; audit `.last.md`; CI log of `main-tests` on the new head.
  - Completion: merged with `--match-head-commit`; `main-tests` listed as a required check (S4: named in the acceptance record); acceptance record carries rounds, wall, audit count.
  - STOP: S1 if the next audit repeats a finding class of this audit (that would be the third time for "PR-controlled input before the trusted step").
- **A302** V1-contract then V1 (`dotfiles-T128-v1-task-schema-a01`): schema, validator, tier derivation.
  - Verification: `scripts/validate-task.py` rejects each gaming fixture (62 removal cases from PR #313 as the test idea source); `main-tests` green with the contracts promoted.
  - Completion: merged; audit `correct`; metrics recorded.

### Phase 4: the auditor off the critical path (bottleneck 3: audit serial queue)

- **A401** V2-contract then V2 (`dotfiles-T128-v2-audit-schema-and-runner-a01`): schema-validated audit, trusted root, pool of two, `make audit-head` auto-start, `AGMSG-AUDIT` record.
  - Verification condition: two audits of two heads run concurrently from the orchestrator's checkout and each lands its record; a re-run of the same head is refused; an evidence-only head reuses the audit.
  - Verification content: two concurrent `make audit-head` runs pasted with their history records; the refusal; the reuse.
  - Completion: merged; the next PR's audit starts within 5 minutes of green CI without the orchestrator; audit wall ≤ 20 minutes.
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
