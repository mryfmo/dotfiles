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
- The evidence commit after `e9ae8b65` carries this report. CI and the Bot round on the final head are named in the RESULT and in the main-checkout copy of this report.

cost: n/a
