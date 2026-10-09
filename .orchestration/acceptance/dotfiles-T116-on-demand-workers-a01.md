# Acceptance: dotfiles-T116-on-demand-workers-a01

- **Decision:** ACCEPTED. PR #306 squash-merged to `main` as `b37937ca` (2026-10-09 03:2xZ) with `gh pr merge 306 --squash --match-head-commit ff4ffa0f…`; gate passed at that head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main AUDIT_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… PR_FEEDBACK_EVIDENCE=… make require-crit-review` rc=0; evidence copies removed). PR #306 `feat/on-demand-workers`, final head `ff4ffa0f55a09c36db2467f2568914608aaec4d4` (six commits on main `02d65ca7`: 93ec0b0e launcher, 04c37440 boundary check, 60d49593 prose, dfdbb8c5 Bot P1 fix, bb2edb38 runtime-health assertion, ff4ffa0f stale-site cleanup). Earlier: blocked PONG 01:28Z (one runtime-health assertion outside the allowed files) → Amendment 1; RESULT 02:15Z head bb2edb38; REVISE round 1 (three stale `--restart-worker` prescriptions) → RESULT 02:45Z head ff4ffa0f.
- **Worker:** `claude-standard-dot-a001` (worker-c, w4:p2), dispatched at T114's acceptance on a fresh branch from `02d65ca7`.
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; Bot thread replies and resolution; live verification with the branch launcher (control plane).
- **Origin:** operator directive 2026-10-09 (chat): at Claude Code startup only the orchestrator starts; workers are seated and removed on demand like the auditor; `--restart-worker` goes; the worker cap stays at three (orchestrator decision, noted to the operator).

## What is under acceptance (PR #306, head ff4ffa0f)

- `home/dot_local/bin/common/executable_herdr-agents`: full mode creates the managed workspace with the orchestrator pane only and starts no worker; healing restarts a missing orchestrator in an agentless pane or a pane split from one that is not the audit pane, a files pane or a worker's; `--attach` claims the seat, prints the directive (default worker worktree, `--add-worker`) and never seats, restarts or repairs a worker; `--restart-worker` exits 2 with the remove-then-add hint; `--add-worker [<worktree>]` defaults to the manifest `worker_worktree`; `worker_pane_filter` keeps any Claude worker pane (linked worktree, or a `codex-worker`/`claude-worker` label) out of the orchestrator checks (Bot P1 4225776331). Thirteen resident-pair functions removed (−734 lines net in the launcher).
- `scripts/check-regime-boundary.sh`: the main checkout is the only active seat; an empty manifest worktree is normal; an identity at a linked worktree is `worker still seated at <worktree> (herdr-agents --remove-worker <worktree>)`; the worker-tab check no longer exempts the manifest seat.
- `scripts/validate-agent-assets.py`: the README pin requires `--add-worker` and `--remove-worker` documentation (was `--restart-worker`); tests follow. `home/dot_codex/rules/default.rules`: comment names remove-then-add.
- Prose: rule Activation bullet (`--add-worker [<worktree>]`), SKILL (activation, start checklist, add/remove only, seated workers, cap of three, delivery for spawn-seated workers and `--bootstrap-agmsg` scope, Stop checklist "remove every worker"), README (one-pane full mode, on-demand seating, retirement note, usage block). Tests: 55 retired-behaviour tests deleted, 11 rewritten, 4 added; `test_runtime_health.py` pins the surviving `--add-worker` profile literal; 112 tests of the touched modules pass locally, CI 13 of 13.
- Known risk, recorded: the `--add-worker` spawn options carry two `--config:` lines (network access, writable roots); the installed agmsg 1.5.0 parser emits both (worker probe, validation section 5), while upstream describes the file as a flat map (#273). Unchanged by this PR; revisit if the parser changes.
- Activation: `make update` in the canonical clone after the merge installs the launcher; the resident worker pane left in w4 (worker-c, a001) is removed with `--remove-worker` at this acceptance, and every later worker is seated with `--add-worker`.

## Live verification (orchestrator, branch launcher from the review worktree at ff4ffa0f)

- `--restart-worker <DIR>`: prints the retirement line and exits 2.
- `--directive`: prints the `agmsg-orchestration:` line naming the default worker worktree and `--add-worker`.
- `--attach` from the orchestrator's Herdr pane (w4:p1): claims the seat and prints the directive; the pane list before and after is unchanged (orchestrator, the seated worker-c tab, the audit tab); no worker started, restarted or repaired.
- Not performed here: a fresh full-mode run (it would heal this live workspace rather than create one) and a persisted-session restore; both are the operator's to observe at the next Herdr start after `make update`, and this record names them as the remaining live checks.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, ff4ffa0f (final head) | correct (no findings: 11 files within the task and its amendments, startup, seating, retirement and boundary behaviour match the objective, artifacts present, evidence matches CI and the two resolved Bot threads; a first run of this audit aborted with `Your workspace is out of credits` and was rerun after the operator restored them) |

- Sweep (final at ff4ffa0f): `.orchestration/validation/dotfiles-T116-on-demand-workers-a01-pr-feedback.json`, 13 items, every one dispositioned: Codex Bot P1 4225776331 `fixed:dfdbb8c5`, P1 4225776337 `not-applicable` (installed parser emits both `--config` pairs; known risk above), both replied to and resolved by the orchestrator; the orchestrator's replies, Codex review headers, the Codex and CodeRabbit summaries, three macOS capacity notices and the CodeRabbit skipped status `not-applicable`. Crit evidence `…-crit.json` (2 orchestrator review records) / `…-review-receipt.md`; worker-side `…-worker-crit.json` / `…-worker-review-receipt.md`.
- Bot wait: review of 60d49593 (two P1); none on bb2edb38 or ff4ffa0f within the wait.

## Parallelism

- Single task after T114's merge (files overlap T114); T115 had finished on worker-d.

## CompactionDB

- Worker records: see the report. Orchestrator consolidation `244d475f-f041-449c-8952-13fa562bf31e`.

cost: n/a
