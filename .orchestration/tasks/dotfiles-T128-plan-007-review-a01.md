---
format: 2
task_id: dotfiles-T128-plan-007-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-plan-007-review-a01 — one independent review round of plans 007 and 008 (review seat and Codex headless at once)

Drafted 2026-10-12 09:5xZ by the orchestrator seat, as step 4 of the operator's chosen order (1 → 4 → 2 → 3). The plans were written by the orchestrator, the author of the mistakes they record; this is the one independent read before Phase 1 and 2 consume hours. One round; the stop condition is fixed; no second round without the operator.

## What to review

- `.orchestration/plans/007-mistakes-into-mechanisms.md` (the principle, the verified figures, Phase 0 rules, STOP S5 to S7, M and C tables, tasks T700 to T713, coverage) and `.orchestration/plans/008-resume-a7-pr323.md` (two decisions, executed).
- Against: `.orchestration/plans/006-regime-v3-execution.md` (Phase 0 rules, S1 to S4, Phase B rows B0, V1, V2, V3a), `plans/README.md` (plan convention), the design `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` (INV-2, INV-6, INV-7, INV-12), `.orchestration/learning/index.yaml` and the M/C records, and the official sentences the plans cite (Codex code review, GitHub rulesets and merge queue, `gh pr merge`, Claude Code permissions and permission modes, hooks, memory, SQLite FTS5, EmbeddingGemma); fetch any you need to confirm, from outside the sandbox.

## Stop condition (report against each)

1. Every problem 1 to 8 has exactly one M, each M at least one C, each C a mechanism that exists or a plan row with an owner (S5 would hold on the records as they stand).
2. No task of 007 contradicts plan 006's Phase B rows or the design's invariants; T701's threat-row unit is compatible with INV-12 and the SKILL threat-table bullet on `main`.
3. The verified figures are the pasted outputs they claim to be (re-run any one of them: the checker replay, the badge counts, the Bot latency, the CI median).
4. The three-repeat procedure and S7 are executable as written by an orchestrator with the tools named (what it searches, what it pastes, what it waits for).
5. Nothing in 007 or 008 restates an owner's rule where a reference would do (the class of PR #318's `sources`).

## Output

`.orchestration/validation/dotfiles-T128-plan-007-review-a01.md`: the usual header, one finding per line with `P0`–`P3`, confidence, `file:line`, one-line rationale, then one verdict line `Plan verdict: accept` or `Plan verdict: revise` with the list of edits. Then `AGMSG-RESULT v1 task_id=dotfiles-T128-plan-007-review-a01 status=ready_for_review verdict=<accept|revise> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing tracked files; branches; PRs.
