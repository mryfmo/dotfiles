---
format: 2
task_id: dotfiles-T128-task-review-phase1-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-review-phase1-a01 — one task-file review round over the three Phase 1 task files (review seat half; Codex headless runs the same round)

Drafted 2026-10-12 by the orchestrator seat under plan 007 (Phase 1 T702, T703 and Phase 5 T715). One round, fixed stop condition (SKILL "A task-file review is one round with a fixed stop condition", line 69 on `main`, and the threat-table bullet at line 71); no second round without the operator.

## What to review

- `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md` (T702, `kind: code`, design tier: the gate)
- `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md` (T703, `kind: docs`)
- `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md` (T715, `kind: code`, review tier)

Against: the design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` as it is in the working tree (v18 at `7f007ec4…`, under round 20; your round-20 receipt's INV-6 clause lands as v19 before these tasks dispatch, so read T702 with that clause in mind), plan 007 `.orchestration/plans/007-mistakes-into-mechanisms.md`, the SKILL and AGENTS.md on `main`, and the scripts and tests each file names.

## Stop condition (report against each, per file)

1. No contradiction with the design or plan 007 (the task's sentences against the invariant it implements; T702 against INV-6 with the round-20 clause; T703 against the owner rule of each sentence it adds; T715 against INV-1's tier and INV-2's caps).
2. Every premise holds: re-run each `command` (network and `brew` commands only if your sandbox allows; say which you re-ran) and compare with the pasted `output`.
3. `allowed_files` covers every touch point grep finds for the described change: name the greps (for example callers and tests of `PR_FEEDBACK_DISPOSITION`; `PINNED_SECTIONS` and every `tests/fixtures/regime/*.md` a changed section pins; every wrapper that includes `aws_cli.sh` and every test that reads it).
4. The invariant check: T702's id maps to its `implementing_tasks` entry and the entry's invariant is the one the task implements; T703 and T715 need no entry (review tier).
5. The threat table's three shape rules by hand (a `closed` selector has the form `tests/<file>::<name>`; an `out-of-scope` owner is an id in `implementing_tasks`; a `residual` payload is a sentence of at least 20 characters), and one row per `allowed_files` entry, per non-path control and per orchestrator effect.

## Output

`.orchestration/validation/dotfiles-T128-task-review-phase1-a01.md`: the usual header (`reviewed_at`, `reviewer`, `profile`, `session`, `files:` with each task file's sha256, `design:` with its sha256), then per file the findings (`P0`–`P3`, confidence, `file:line`, one-line rationale) and one line `Task-file verdict: <task id>: accept|revise`. Then `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-phase1-a01 status=ready_for_review verdicts=<id>:<v>,<id>:<v>,<id>:<v> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing tracked files; branches; PRs. Paths resolve in the main checkout (`main` at `36a20d0a`).
