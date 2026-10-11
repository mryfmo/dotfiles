# AGMSG-TASK dotfiles-T128-task-review-phase-a-a01

Drafted 2026-10-11 by the orchestrator seat. The one-round task-file review of plan 006 Phase A, under the stop condition the pattern fixes: no contradiction with design v16 (whole-file sha256 in the AGMSG-TASK `design_sha256=`), premises hold (re-run each command; the `output` must be the raw output), `allowed_files` complete for the touch points `grep` finds, one invariant per task (a task without an `invariants` key is docs tier), and for a trust-boundary task a `threat_table` whose rows cover what the PR and the orchestrator control. Anything finer belongs to the worker and the implementation PR. Read-only; one receipt; Claude seat on the review profile.

Files, in the main checkout:

1. `.orchestration/tasks/dotfiles-T128-process-rules-a01.md` (A1, A2, A4; docs tier; SKILL and AGENTS.md).
2. `.orchestration/tasks/dotfiles-T128-regime-counters-a01.md` (A3; design tier by effect; threat table is the completion condition: report a missing row or a `closed` row whose stated test cannot close it).
3. `.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md` (A5; design tier: workflows; your round-a201 items were applied; now carries a threat table and no contract-first dependency).

Also confirm `.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-contract-a01.md` is marked `superseded_by` A5 and `.orchestration/plans/006-regime-v3-execution.md` Phase A names the same three ids.

Output `.orchestration/validation/dotfiles-T128-task-review-phase-a-a01.md` with the usual header (`reviewed_at`, `reviewer`, `profile`, `session`, `design: <path>@<sha256>`), one `<task id>@<sha256>` line per file, per file `verdict: ready | revise: <numbered items, each one sentence naming the rule it fails>`; then `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-phase-a-a01 status=ready_for_review verdicts=<id:verdict;…> receipt=<path>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator applies the items once and dispatches; there is no second round. Forbidden: editing any tracked file; branches; PRs; `make update`. max_turns=4.
