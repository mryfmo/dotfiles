# Report: dotfiles-T128-process-rules-a01

- Seat: `claude-standard-dot-a003` (Claude Code, profile `standard`) in `.claude/worktrees/worker-f`.
- Task file `.orchestration/tasks/dotfiles-T128-process-rules-a01.md`, sha256 `65fa3494…` checked against the TASK's `task_sha256`, read in full, with the design `dotfiles-T128-regime-v3-a01.md` (INV-3, INV-8) for the evidence and revise contract.
- Branch `docs/regime-pattern` from `origin/main` `b896d9bc` (`git switch -c … --no-track origin/main`). The first commit `1c59f1cc` copies the task file byte-identical to `.orchestration/dotfiles-T128-process-rules-a01/task.md`. Draft PR #318 opened at 04:19Z, 3 minutes after the TASK (04:16:13Z); rule commit `f7c229ff`; `gh pr ready` at 04:21:24Z, before the Bot wait.

## What changed

- **A1, SKILL "Review and integration invariants"**, five new bullets:
  - paired design-review rounds: both reviewers get the same design hash at the same time, one revision per pair of results, no round opened while one is open, at most three revision rounds, then a frozen design with a residual list that is worker input; the review judges invariants, threat model, trust anchors and premises for contradiction and enforceability only;
  - a task-file review is one round with the fixed stop condition;
  - a boundary PR carries no task draft under review and never gates a dispatch;
  - a trust-boundary task carries a `threat_table` (`{control, disposition}`, disposition matching `^(closed|residual|out-of-scope): `), one row per thing the PR or the orchestrator controls, as its completion condition; a missing row is added once, as an amendment; `schemas/task.json` (wave V1) takes the key as optional;
  - `scripts/regime-counters.sh <task id>` (A3) output is pasted before every acceptance action, and S1 and S2 are decided from it.
- **A2, SKILL Worker Playbook step 15 and the Message Contract**: `gh pr ready` before the wait; `@codex review` after 10 minutes without a Bot review of the final head; P0/P1 fixes at most twice, and the third Bot round is reported unfixed with `bot_rounds=3` and the open threads; a revise ACCEPTANCE carries `previous_head=` and one `check=tests/<file>::<name>` per finding, which the worker records in `.orchestration/<task id>/revise.yaml`. The `check=` spelling follows design INV-3.
- **A4, AGENTS.md "## Code Review Rules"**: the new subsection "Orchestration records and trust-boundary code". `.orchestration/**` is reviewed for secrets and home-directory paths only. Trust-boundary code is reviewed against the task's `threat_table`: report a missing row or a `closed` row whose test does not close it, never re-raise a `residual` row. Lint and formatting stay with CI.
- **`tests/unit/test_agmsg_orchestration_docs.py`**: a new class `AgmsgRegimePatternTest` with 8 tests. Each scopes its assertion to the section that owns the rule (the invariants section, step 15, the Message Contract, the AGENTS.md subsection). Each of the 11 rule sentences was removed in a scratch copy and its test failed (validation §3).

## Deviation, stated: Orchestrator Playbook step 3 is not edited

PR 317 (`feat/main-tests`, open) rewrites the one-line step 3 paragraph and inserts a Worker Playbook step 16 right after step 15. Any edit to step 3, or to the line before that insertion, would conflict with it. So:

- the A1 task-authoring rules (the one-round task-file review and the `threat_table`) sit in "Review and integration invariants";
- the step 15 edits keep its last line unchanged.

I told the orchestrator by PONG at 04:20Z and proceeded on that default.

## Notes

- The task names `scripts/regime-counters.sh` (A3) and the S1/S2 decisions; neither exists on `main` yet. The rule text names A3 as the script's source.
- `scripts/validate-task.py` is not on `origin/main`, so the task file was checked by its sha256 and read by hand.
- Evidence: per design INV-8 and the task's "evidence beside it", the report, validation, sandbox, learning and autoskill files are committed under `.orchestration/dotfiles-T128-process-rules-a01/`. Masked copies sit at the TASK message's `expected_*` paths in the main checkout.
- `history.sh` printed an agmsg placement-guard notice: pane `w5:p4` is recorded under an older seat id. It is informational, and the premise count was unaffected.
- Understand-Anything hook: did not fire. plan-mode-used: no.

## CompactionDB

`cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 plan 006 Phase A …'` printed `70b799fb-e5e6-41be-b4d4-f82208c715d9` (validation §5).

## CI and Bot

- Bot round 1, on `f7c229ff` (review 5481888792 at 04:26:14Z, 5 minutes after `gh pr ready`, so no `@codex review` was needed): two findings, both fixed in `e9ae8b65` (fix round 1 of 2).
  - 4240250137 (P1): `scripts/regime-counters.sh` does not exist yet → the rule now counts by hand until A3 lands: `fixed:e9ae8b65`.
  - 4240250141 (P2): the CI watch blocked the Bot timer → both run together, timed from ready: `fixed:e9ae8b65`.
- Bot round 2, on `ddadd5c9` (review 5481907744 at 04:34:46Z, 5 minutes after the push): four findings, all fixed in `962d268d` (fix round 2 of 2).
  - 4240269216 (P1): trust boundary judged from the diff, missing table reported: `fixed:962d268d`.
  - 4240269218 (P1): `open:<thread id>` label for third-round threads: `fixed:962d268d`.
  - 4240269219 (P2): the `check=` selector asserted: `fixed:962d268d`.
  - 4240269222 (P1): manual counters read the PR's GitHub review comments: `fixed:962d268d`.
- A third Bot round, on the head that carries this report, is not fixed (A2). Its threads, CI on the final head and the round count are in the RESULT and in the main-checkout copy of this report.

cost: n/a

## Revise round 1 (ACCEPTANCE at 04:50:34Z, previous_head `9a46c3c4`)

Round-0 final head `9a46c3c4`: CI 14 of 14 pass; Bot round 3 left three P2 threads, which A2 says are not fixed. The orchestrator ruled them real rule gaps and asked for root-cause fixes. All three are fixed in `e115dbba`, one sentence each, with the assertions under the selectors the ACCEPTANCE named. They are recorded in `.orchestration/dotfiles-T128-process-rules-a01/revise.yaml` (`round: 1`, `previous_head`, `checks`).

- 4240290382: a review-body finding is listed as `open:review-<review id>` → `test_open_review_body_findings_have_an_identifier`.
- 4240290387: dispositions match `^(closed|residual|out-of-scope): \S` → `test_threat_table_dispositions_carry_a_payload`. The bare-prefix token moved into this test from `test_a_trust_boundary_task_carries_a_threat_table`.
- 4240290391: the worker waits for the background CI watcher's exit status before the RESULT; non-zero means no RESULT until CI passes → `test_the_ci_watch_is_joined_before_the_result`. `test_bot_fix_rounds_are_capped_and_the_pr_is_ready_first` now splits its `open:` token, so the parenthetical can sit inside it.

Each check fails on a `9a46c3c4` tree with this head's docs test and passes on `e115dbba`; all 21 sentence-removal proofs fail their test (validation §3, §8). A2's cap applies again in this round: at most two fix rounds, then the RESULT.

One sandboxed command was refused by the permission gate: a previous-head check that started with `rm -rf "$P"`. I re-ran it in a fresh `mktemp -d` directory with no deletion. Sandbox record, deviations.

### Revise round 1, Bot round 1 (on `ac3794f9`)

- 4240321113 (P1): `residual: none` passed the payload rule, and reviewers never re-raised a residual row. Fixed in `88150d33`: a residual row holds back a finding only when its named control mitigates the risk; a missing, placeholder or ineffective control is reported (`fixed:88150d33`). This is fix round 1 of 2 in this revise round, so T126 INV-6 (d) counts one head with a Bot P1 after the first RESULT.

### Revise round 1, Bot round 2 (on `6635030f`)

- 4240334094 (P1): an `out-of-scope` row with a placeholder or wrong owner is now reported, like a placeholder `residual` row (`fixed:77953979`).
- 4240334098 (P2): the task-review test asserts each stop criterion (`fixed:77953979`).
- **T128 INV-6 count reached:** Codex Bot P1 on two heads after the first RESULT (`ac3794f9`, `6635030f`). Under INV-6 the merge is refused until a reset record or a waiver exists. That is the orchestrator's S2 decision; I reported it by PONG at 05:04Z and continued under the revise note's A2 cap. This is fix round 2 of 2; a third Bot round goes unfixed into the RESULT.

## Revise round 1 final head `aeb6c5ad` (main-checkout copy)

- CI: 14 of 14 checks pass. The watcher's exit status was joined before the RESULT (exit 0).
- Bot round 3 of the revise round (review 5481987826 at 05:09:48Z): two P1 threads, not fixed under A2 (`bot_rounds=3`).
  - `open:4240348412`: the manual counts call `history.sh` without `--limit`, so they see only its 20 default rows and undercount on long tasks. One-line fix: name `history.sh <team> --limit 1000`, as the task's premise command does.
  - `open:4240348414`: an `open:` thread makes the RESULT valid but has no path through step 10.1 (every sweep item `fixed:`/`not-applicable:`) or 10.5 (every thread resolved). That is a contract decision for the orchestrator: for example, an `open:` thread blocks integration until a disposition, a threat-table row or a reset. It is an orchestration-level gap, not a wording fix I can make alone.
- T128 INV-6 count: Codex Bot P1 on three heads after the first RESULT (`ac3794f9`, `6635030f`, `aeb6c5ad`), above the threshold of two. This is the orchestrator's S2 decision; I reported it at 05:04Z.
