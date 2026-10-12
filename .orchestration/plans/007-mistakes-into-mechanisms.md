# Plan 007: Turn every detected mistake into a linked record, a grounded correction, and a mechanism the next task consumes

> **Executor instructions**: the orchestrator executes this plan under plan 006's regime (every repository mutation is a worker task; acceptance, audit and integration stay with the orchestrator). Read the plan completely. Phase 0 is in force from the moment this file exists; no new implementation PR is dispatched before Phase 2 closes. The resumption of PR #323 is its own plan (`008-resume-a7-pr323.md`), written in the S7 report form. A STOP condition always wins over task completion. Every figure below is the pasted output of a command run on 2026-10-12 (plans/README.md global rules; the `run-not-recall` rule).
>
> **Drift check**: `git rev-parse origin/main` is `b67ea752` or a descendant; the design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` hashes to `4520b8f0…`; PR #318 is merged (`e83e923d`, task `dotfiles-T128-process-rules-a07` `d5d499ce…`); PR #323 is open at `3a54d340` under `dotfiles-T128-worker-stop-and-watch-a02` (`af519f0f…`) with the audit of that head `incorrect` (four findings) and no corrective action taken since the operator's halt of 03:3xZ.

## Status

- **Execution**: TODO (recorded 2026-10-12 04:32Z at the operator's direction; Phase 0 rules apply immediately; task dispatch waits for the operator's go)
- **Priority**: P0 (the operator's standing principle; the regime loops without it)
- **Effort**: L
- **Risk**: MED (two operator decisions on the critical path: the merge queue and the permission rules)
- **Planned at**: main `b67ea752`, 2026-10-12, from the analysis of 2026-10-11 and 2026-10-12 (PR #318 lineage a01 to a07, PR #323 a01 to a02)

## The operator's principle (2026-10-12), stated as the plan's goal

Round caps and counters (INV-6, S1, the Bot-fix cap) exist to detect a dead end of wrong work early. They are not the goal. The goal is that every detected mistake produces:

1. a detailed record of the wrong work (where, when, evidence ids, which detector fired and at which count, why not earlier, root cause, what should have happened);
2. a detailed record of the corrective means and method, grounded in official documentation and the latest accurate information (source URL, fetch date, the quoted sentence, how it was verified), never in recollection;
3. a link in both directions between the two record types;
4. a fixed procedure when the same finding repeats three times: search these records first; if a matching correction exists, apply it; if not, research official documentation and current accurate sources, record the new correction, then act. Never a fourth round of the same thing without this step.

## Verified figures this plan rests on (commands run 2026-10-12 03:5xZ to 04:2xZ)

- Task-file consistency check (C1 to C6) replayed over the 13 Phase A task files: 10 fail (`process-rules` a01 to a06, `regime-counters` a01/a02, `ci-skip-orchestration` a01/a02); a07 and `worker-stop-and-watch` a01/a02 pass. Dominant checks: C2 (own evidence directory), C4 (an allowed path without a threat row), C6 (receipt pointer at round 16), C3 (successor copy rows).
- Bot findings on PR #318 and #323: 61 top-level comments, P1 30, P2 31, P0 and P3 none. Judged ledger: 7 classes reach three. First-three-words grouping: 0 classes reach three. Trigram Jaccard clustering at 0.35: 1 cluster reaches three and mixes two classes.
- Round cost on PR #318: Codex review latency median 4.7 min (3.0 to 6.2, 18 passes, commit time to review); `test.yaml` CI median 8.5 min (7.9 to 11.5, 20 successful runs). One round is 9 to 12 min; one reset is about 20 min (review seat 3, anchor 1, copy and push 3, CI 8.5, Bot 5).
- Gate grammar: `scripts/require-crit-review.py:26` accepts `fixed:<7-40 hex>` or `not-applicable:<reason>`; it checks a minimum reason length for failure-level items and nothing about evidence.
- Permissions: `home/.chezmoitemplates/claude-settings-managed.json` has `defaultMode: auto`, `ask: []`, and a deny list without `herdr-agents --remove-worker`, `gh pr merge` or `git push`; permgate (`home/dot_local/bin/common/executable_permgate`) is deterministic with default `ask`.
- CompactionDB: FTS5 with the `trigram` tokenizer; semantic search implemented as an external command contract (`{"texts": [...]}` in, `{"model", "embeddings"}` out), disabled; brute-force cosine in Python; this interpreter (`uv` Python 3.15.0, SQLite 3.54.0) has no `enable_load_extension`.
- Official sources read: Codex code review (follows `AGENTS.md` Code Review Rules; "flags only P0 and P1 on GitHub", which the data above contradicts; review trigger is a personal setting), GitHub rulesets (strict up-to-date), merge queue (`merge_group`, same benefit as up-to-date), auto-merge conditions, `gh pr merge --match-head-commit`, Claude Code permission modes (auto mode's classifier; deny → ask → allow; PreToolUse does not bypass rules; conversation boundaries can be lost at compaction), hooks (Stop exit 2 blocks), memory (CLAUDE.md and auto memory are context, not enforcement), SQLite FTS5 (trigram, `bm25()`), EmbeddingGemma (308M v1 under 200 MB quantized; 740M v2, 768-d, Matryoshka 128 to 512, 8k context).

## Working rules for the orchestrator (Phase 0, in force now)

- **Record schema.** `.orchestration/learning/mistakes/M-<yyyymmdd>-<n>.md` with front matter `id`, `artifact`, `found_at`, `detector` (`inv6|s1|audit|bot|operator`), `count_at_detection`, `evidence` (ids, heads, commands), `root_cause`, `should_have_been`, `corrections` (list of C ids), `status`. `.orchestration/learning/corrections/C-<yyyymmdd>-<n>.md` with `id`, `closes` (M ids), `means`, `method`, `sources` (list of `{url, fetched_at, quote, verified_by}`), `mechanism` (`validator:<check>|test:<selector>|fixture:<path>|rule:<file>#<anchor>|setting:<key>|premise:<task>#<n>|plan:<row>`), `verification` (the replay that proves it), `status` (`pending|landed:<sha>`). `.orchestration/learning/index.yaml` lists every M and C with status.
- **The three-repeat procedure.** When a class reaches three on one artifact (the ledger), or `regime-counters.sh` prints an S1 candidate, the next acceptance action is a search: `contextdb memory search <class slug>` and `grep -rl <class slug> .orchestration/learning/corrections/`, pasted into the acceptance record. A matching C with `status: landed` is applied as written; a C with `status: pending` lands first; no match means a new C is researched from official sources and recorded before any dispatch.
- **Evidence-bearing dispositions.** From now on every `not-applicable:<reason>` on a Bot or audit finding carries `; evidence=<command>` with the pasted output in the record; a disposition that cites a rule, a setting or a script quotes the line.
- **Amendments, not replies.** A change to a rule sentence requested of a worker travels as a task amendment (hashed, checked by C1 to C6, confirmed by the review seat), never as a PONG answer.
- **Classes at disposition time.** Every finding gets its class row when it is dispositioned, in the current acceptance record's ledger; the pre-audit check (`ledger-check`) and the fill (zero gaps) remain the preconditions of `orch-audit.sh`.

## STOP conditions

- **S1 to S4**: as plan 006.
- **S5 (unclosed mistake)**: a reset, S1 stop or `incorrect` audit does not resume until its M record exists with at least one C whose `mechanism` names an existing check, test, fixture, rule, setting or premise, or a plan row id with an owner. A C without a mechanism is a note, not a correction.
- **S6 (search skipped)**: an acceptance action after a third repeat without the pasted search is invalid; the gate refuses it once T702 lands, and the orchestrator refuses it by rule before that.
- **S7 (second S1 cycle on one task: stop and ask the operator)**: S1's set (three repeats → `/effort xhigh` → re-examine the work itself → search the records → correct) runs at most once per task without the operator. When the set would run a second time on the same task (a second class reaches three, or a reset follows an S1 on the same artifact), the orchestrator stops and sends the operator one report with: the situation (heads, counts, what is merged and what is not), the problems and open issues, the root cause, and concrete proposals for the target state in several variants, each priced in rounds and minutes, with the orchestrator's recommendation stated and the list repeated without it. No dispatch, amendment, reset or disposition until the operator chooses. Applied retroactively, S7 would have stopped PR #318 at 00:55Z (the `bookkeeping` S1 after the counters-bullet S1) instead of running a06 and a07; the operator's halt of 03:3xZ on PR #323 is the first S7 in effect. The report format is plan 008's "Decision for the operator" section.

## Mistake records to backfill in Phase 0 (one M each; the eight problems of 2026-10-12)

| M | Problem | Evidence | Root cause | Should have been | C |
|---|---|---|---|---|---|
| M-20261012-1 | S1 recognized late (sources at the 6th finding; step15-wait 6 and scope 4 never declared) | PR #318 ledger in `…process-rules-a07.md`; counters S1 line groups titles by first three words | no class recorded at disposition; the only automatic class heuristic is lexical, measured at 0 of 7 | a class row per finding at disposition; three rows stop | C-1, C-4 |
| M-20261012-2 | prose enumerations drifted (sources 6, scope 5, unpinned 7, task-record rows 5) | SKILL line 72 history; AGENTS.md 78; audits 27ea99b/b7ae2d5/4af8939 finding "unpinned" | rule text restated three owners (INV-6, script, plan S1, allowed_files); tests pinned the wording, not the owners | rules reference owners; derived rows and whole sections are checked mechanically | C-2, C-3 |
| M-20261012-3 | orchestrator errors reached the audit (two wrong dispositions, a wrong premise figure, the widened class count) | audit of `3a54d340` findings 2 to 4; PONG 655 answer (2) | dispositions and instructions written without re-reading the design line, the script (`regime-counters.sh:114`) or the settings; no evidence requirement | every `not-applicable` carries pasted evidence; instructions travel as amendments | C-5 |
| M-20261012-4 | successor bookkeeping left behind (a05 oracle row, a06 copy row and directory, a07 receipt; A7 four pointer rounds) | checker replay: 10 of 13 task files fail | dependent fields edited by hand under "nothing else changes" | fields derived from the id and checked before dispatch | C-3, C-6 |
| M-20261012-5 | wall clock missed (PR #318 21 h 24 min with 6 resets; A6 missed on A3 and A7) | PR #318 and #323 timelines; round cost figures above | each mistake above costs a Bot pass (4.7 min) and a CI run (8.5 min); strict up-to-date re-runs CI per merge; whole-file hashing forces a re-anchor per edit | two Bot passes per PR, no reset, no cascade | C-7, C-8 |
| M-20261012-6 | step 15 drew seven findings on its wait procedure | ledger class `step15-wait` | an imperative procedure written clause by clause | a state and transition table pinned whole | C-9 |
| M-20261012-7 | Bot behaviour premise unrecorded (official: P0/P1 only; observed: 31 P2) | `pr-feedback` badge counts | design from observation without the official sentence and the setting | three-point premise (official text, setting, observation) | C-10 |
| M-20261012-8 | "human-only permission gate" claimed where auto mode's classifier decides | disposition on 4244248692; managed settings `defaultMode: auto`, `ask: []` | regime prose confused with the configured mode | irreversible control-plane actions behind settings `ask` rules | C-11 |

## Corrections (one C each; the mechanism each becomes)

| C | Means and method | Mechanism | Sources (official) | Verification |
|---|---|---|---|---|
| C-1 | ledger at disposition; pre-audit `ledger-check`; worker-side early stop | `validator:ledger-check` (T704), `rule:SKILL#counters-bullet` (landed `e83e923d`), A7 step 15 (PR #323) | GitHub REST review comments (`original_commit_id`, `in_reply_to_id`, `per_page` max 100) | replay: the a05 record at 11 of 33 rows fails the check; the a07 record passes |
| C-2 | rules by reference; whole-section fixtures; threat rows derived from `allowed_files` plus a fixed list of orchestrator effects | `fixture:tests/fixtures/regime/*.md` (landed), `validator:C4` (T704/T705), `rule:AGENTS.md#code-review-rules` (T701) | Codex code review follows `AGENTS.md` Code Review Rules | audit of `92634b25`: 33 removal checks fail the fixture test |
| C-3 | task-file consistency check C1 to C6 before every dispatch and anchor; successor generator | `validator:task-consistency-check` (T704), `validator:validate-task` (T705), `scripts/new-successor.py` (T706) | repository schema (V1); `gh pr merge --match-head-commit` for head binding | replay above: 10 of 13 historical files fail |
| C-4 | class candidates from embeddings, decision by judgment | `setting:.claude/contextdb/config.json#semantic` with EmbeddingGemma (T707) | EmbeddingGemma docs; SQLite FTS5 `trigram`, `bm25()` | measured: lexical heuristics 0 of 7 and 1 of 7; embedding grouping to be measured on the 61 titles (T707 acceptance) |
| C-5 | `not-applicable:<reason>; evidence=<command>` enforced by the gate; amendments instead of replies | `validator:require-crit-review#evidence` (T702), `rule:SKILL#orchestrator-playbook` (T703) | Claude Code permission modes (auto mode's classifier), `gh api` | the two wrong dispositions of 2026-10-12 lack an evidence clause and fail the grammar |
| C-6 | front matter generated from the task id | `scripts/new-successor.py` (T706) | repository schema (V1) | generated a0N files pass C1 to C6 |
| C-7 | merge queue with `merge_group`; key-unit design hash; Stop gate ignores anchor RESULTs | `setting:ruleset#merge-queue` (T709, operator), `validator:validate-task#canonical-hash` (006 V1), `rule:agent-stop-gate` (T711) | GitHub merge queue and rulesets; auto-merge | next PR: zero `update-branch` CI re-runs; wall measured |
| C-8 | round budget by construction (one fix round per Bot pass, resets only by rule) | `rule:SKILL#worker-step-15` (A7) | Codex review trigger setting | A6 on the first PR after Phase 2: rounds ≤ 2, resets 0, wall ≤ 2 h |
| C-9 | step 15 as a state and transition table | `fixture:tests/fixtures/regime/worker-step-15.md` (T712) | Claude Code hooks (Stop exit 2) | every transition has a token; a removed row fails |
| C-10 | three-point premise for Bot behaviour | `premise:plan-006#bot-behaviour` (T713) | Codex code review page | the premise names the setting value and the observed counts |
| C-11 | `ask` rules for `herdr-agents --remove-worker *`, `gh pr merge *`, `git push *` | `setting:claude-settings-managed.json#permissions.ask` (T710, operator) | Claude Code permissions (deny → ask → allow; hooks do not bypass; boundaries lost at compaction) | a dry run of each command prompts |

## Phases, atomic tasks, verification, completion

### Phase 0: records and rules (orchestrator, records only, now)

- **T700** Backfill: write M-20261012-1 to 8 and C-1 to C-11 under `.orchestration/learning/{mistakes,corrections}/`, `index.yaml`, and re-express the three existing S1 records (V0, counters bullet, finding classes) in the schema. Verification: every M names at least one C; every C names a mechanism or a plan row; `index.yaml` round-trips with PyYAML. Completion: boundary PR. Metric: 8 M, 11 C, 0 unlinked.

### Phase 1: the orchestrator's structure (problems 2 and 3)

- **T701** B0 design amendment carries the threat-table row unit (PR-controlled = each `allowed_files` entry; orchestrator effects = a fixed list: forced removal, merge, update-branch) and the sentence in AGENTS.md Code Review Rules that names it. Verification: one review pair accepts; the Bot's next records-only PR raises no "missing row" thread. Completion: boundary PR after the pair. Metric: `threat-row-outside-paths` class stays at its count.
- **T702** Gate grammar: `scripts/require-crit-review.py` requires `evidence=` on every `not-applicable` and refuses an acceptance record whose ledger has a class at three without a pasted search (S6). Verification: unit tests with the two wrong dispositions of 2026-10-12 as fixtures (refused) and the corrected ones (accepted). Completion: merged, audit `correct`. Metric: 0 orchestration findings about dispositions on the next two audits.
- **T703** Orchestrator Playbook: the amendment-not-reply rule and the three-repeat procedure as rule text, pinned by fixture. Verification: tokens plus the whole-section fixture. Completion: merged.

### Phase 2: the detectors, made permanent (problems 1 and 4)

- **T704** Promote `ledger-check.py` and `task-consistency-check.py` from the scratchpad to `scripts/` with unit tests; the ten failing historical task files and the pre-fix a05 record become fixtures under `tests/fixtures/lessons/`. Verification: each fixture fails its check; current files pass. Completion: merged; `orch-audit.sh` and the SKILL name the scripts. Metric: replay 10 of 10 detected.
- **T705** V1 validator (`scripts/validate-task.py`) absorbs C1 to C6 and the canonical key hash (plan 006 A302 scope). Verification: the 62 gaming fixtures plus the ten of T704. Completion: merged.
- **T706** `scripts/new-successor.py`: generates a successor's front matter from `task_id` and `reset_of`. Verification: generated a0N files pass C1 to C6; the review seat receives body-only work. Completion: merged.
- **T707** CompactionDB: kinds `mistake` and `correction` with the schema in `content`; `semantic.enabled` with an EmbeddingGemma command (operator decision on the model download, S4); acceptance promotes `[memory:failure]` candidates or rejects them with a reason. Verification: the 61 Bot titles embedded; the seven judged classes recovered as top-k neighbours is reported as a number, not promised. Completion: config landed; the first search-first record cites a `memory search` paste. Cost: one model download (308M, under 200 MB quantized), one embedding per record.
- **T708** A7 worker-side early stop: PR #323 resumed under plan 008 option A (records first, amendment 1, revise round 1 landed as `dc7edcc0`), then parked as a draft under plan 008 decision 2 (option D2, 09:32Z) after the second S1 cycle; the rule lands through T712. DONE as a decision; the mechanism is T712's.

### Phase 3: operator decisions (problems 5 and 8)

- **T709** Merge queue: `merge_group` trigger added to `test.yaml` and `remote.yaml` with the in-job decision of A5 preserved; the ruleset moves from strict up-to-date to the queue. Verification: two PRs merge without `update-branch`; the records-only skip still reports every required context. Completion: operator PR merged (S4). Metric: zero re-run CI per merge.
- **T710** Permissions: `ask` rules for `Bash(herdr-agents --remove-worker *)`, `Bash(gh pr merge *)`, `Bash(git push *)` in the managed settings template; the A7 threat row states the mode. Verification: a dry invocation prompts in auto mode. Completion: operator PR merged (S4).
- **T711** Stop gate: anchor RESULTs (`round=N verdict=accept`) need no separate ACCEPTANCE. Verification: a replay of 2026-10-12's history counts the saved round trips. Completion: merged.

### Phase 4: design items for Phase B (problems 6 and 7)

- **T712** Step 15 and step 7 as state and transition tables (states: draft, ready, waiting, fixing, blocked, result for the worker; watching, pinged, stopped, removed for the orchestrator; inputs: push, CI, Bot pass, PING, PONG, RESULT, ACCEPTANCE), pinned by their fixtures, one token per transition. Input: PR #323 at `dc7edcc0` (its fixtures, Message Contract `head=`, the badged counting rule, the records) and its five open P2 threads (4244811155, 4244811161, 4244811164, 4244811168, 4244811170) as rows, plus the three classes at three or more (`watch-ping-trigger`, `fix-round-definition`, `result-head-binding`). One cap rule stated once (a fix round answers a Codex badged finding; at most two before the third round is reported) and referenced from step 7; "continued pushing" and "without a push" defined from the head sha and the PING's `read_at`. Verification: removal of any row fails; the five threads map to rows. Completion: merged with audit `correct`; A6 measured on this PR.
- **T713** Bot behaviour premise: official sentence, the Codex setting value (operator reads the setting), the observed counts. Verification: the premise block in plan 006 and in A2/A7's task files. Completion: boundary PR.

## Finding coverage

| Problem | M | C | Tasks |
|---|---|---|---|
| 1 late S1 | M-1 | C-1, C-4 | T704, T707, T708 |
| 2 prose drift | M-2 | C-2, C-3 | T701, T704, T705 |
| 3 orchestrator errors | M-3 | C-5 | T702, T703 |
| 4 successor bookkeeping | M-4 | C-3, C-6 | T704, T705, T706 |
| 5 wall clock | M-5 | C-7, C-8 | T709, T711, 006 V1 |
| 6 step 15 | M-6 | C-9 | T712 |
| 7 Bot premise | M-7 | C-10 | T713 |
| 8 permissions | M-8 | C-11 | T710 |

Coverage invariant: each of 1 to 8 appears once; each M names its C; each C names its mechanism.

## Dependency rationale

- Phase 0 before anything: the records are the input of the three-repeat procedure, and S5 forbids resuming PR #323 without them.
- Phase 1 before Phase 2: the gate grammar (T702) is what makes the detectors binding; without it they are advice.
- Phase 2 before any new implementation PR: the replay fixtures prove the detectors on the mistakes they were built for.
- Phase 3 is the operator's: it changes the ruleset and the permission mode, and plan 006 S4 names both.
- Phase 4 rides on B0 (plan 006 Phase 3), which already carries the INV-12 narrowing.

## Acceptance of the plan

- Eight M and eleven C records on `main`, every C with a landed mechanism or an owned plan row.
- The first implementation PR after Phase 2: Bot passes ≤ 2, resets 0, audit `correct` at the first head, wall ≤ 2 h from TASK to merge, zero `update-branch` CI re-runs.
- The three-repeat procedure exercised at least once with a pasted search that found a landed C.
