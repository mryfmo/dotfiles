---
format: 2
task_id: dotfiles-T128-task-review-phase1-amend-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-review-phase1-amend-a01 — confirm amendment 1 of the two dispatched Phase 1 task files (review seat half; Codex headless runs the same check)

Drafted 2026-10-12 12:3xZ by the orchestrator seat. The Codex Bot's review of PR #328 (T703, head `9b2c02a1`, review 5490674624) raised three findings that are defects in the orchestrator's task text, and the worker held with `AGMSG-PONG status=question` (12:27:06Z) instead of patching around them. The plan 007 amendment rule says a rule-sentence change travels as a hashed amendment confirmed by the review seat; this is that confirmation. One round.

## What changed (amendment 1 of each)

- `.orchestration/tasks/dotfiles-T128-playbook-rules-a01.md` (T703): F1 thread 4247933544: the orchestrator-effects row split into three rows (merge; update-branch; forced worker removal); F2 thread 4247933561: item 5's invariant check qualified to tasks that carry an `invariants` key; F3 thread 4247933574: item 3's search keyed on the mistake records' new `classes:` field (`grep -l 'classes:.*<slug>' .orchestration/learning/mistakes/`, then `corrections:` through `index.yaml`, plus the CompactionDB memory search); the heading and intro carry the amendment note.
- `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md` (T702): the same row split; item 2's `search:` line grammar keyed the same way; the heading and intro carry the amendment note. The INV-6 sentence in its `invariants:` block is unchanged.
- Context: `.orchestration/learning/mistakes/M-20261012-14.md`, `M-20261012-15.md`, `corrections/C-16.md`, `C-17.md` (the records), the 14 existing mistake records now carrying `classes:`, plan 007's Phase 0 schema and procedure lines, and the checker's new C7 (one row per non-path control name and per effect name; main's copies of the three Phase 1 files fail it, the amended six pass).

## Stop condition (report against each, per file)

1. The diff of each amended file against its copy on `main` (`683384ea`) contains only what the list above says (`git diff HEAD -- <file>`).
2. F1, F2 and F3 are answered as the Bot wrote them (quote the thread and the sentence that answers it); F2's qualification does not exempt a task that does carry `invariants` (T702 still maps to `[INV-6]`).
3. The keyed search works on the records as they are: `grep -l 'classes:.*bookkeeping' .orchestration/learning/mistakes/` names M-20261012-4 (corrections C-3, C-6) and `grep -l 'classes:.*sources' …` names M-20261012-1 and M-20261012-2 only.
4. T702's `invariants.INV-6` is byte-equal to the design's INV-6 (design v20 at `7a067b19…` on `main`), and both files pass C1 to C7 (`task-consistency-check.py` is the orchestrator's; state the result the orchestrator pasted and re-derive C7 by reading the rows).

## Output

`.orchestration/validation/dotfiles-T128-task-review-phase1-amend-a01.md`: the usual header with each amended file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: <task id>: confirm|revise` per file, then `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-phase1-amend-a01 status=ready_for_review verdicts=<id>:<v>,<id>:<v> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing tracked files; branches; PRs. Paths resolve in the main checkout (`main` at `683384ea`).
