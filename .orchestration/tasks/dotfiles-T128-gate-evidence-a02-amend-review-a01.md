---
format: 2
task_id: dotfiles-T128-gate-evidence-a02-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-gate-evidence-a02-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-gate-evidence-a02` (review seat half; Codex headless runs the same check)

Drafted 2026-10-12 14:2xZ by the orchestrator seat. On PR #329 the class `search-command-scan` reached three (4248233012, 4248697658, 4248934830: bypasses of substring and regex checks over the pasted `search:` line) and 4248934816 found the greedy delimiter split; the three-repeat set ran (S1 record `.orchestration/learning/plan-006-s1-gate-evidence-search-command-scan-2026-10-12.md`, M-20261012-20, C-22). The task text changes by amendment, confirmed by the review seat. One round.

## What changed (amendment 1 of a02)

- Item 1: the disposition splits at the first `; evidence=`; a second delimiter is refused.
- Item 2: the gate recomputes the records search (`grep -rl 'classes:.*<slug>' .orchestration/learning/mistakes/` from the repository root) and compares its set with the record's fixed-template line `search: <slug> -> <sorted basenames or none>`; the CompactionDB half is an unvalidated paste; no pasted command text is read (INV-12's no-hand-written-parser rule).
- Heading and intro carry the amendment note. Nothing else changes (the `invariants.INV-6` block, the threat table, the premises).

## Stop condition

1. The diff of the task file against its copy on `main` (`7cbe5405`) contains only what the list above says.
2. The new S6 check cannot be satisfied by any text that is not the recomputed set (no substring of command text is consulted), and the disposition grammar has exactly one accepted shape; both are consistent with INV-6's clause ("… a finding-class table with three rows of one class and no pasted search of the correction records") read as the records search being present and true, and with INV-12's enforcement row.
3. The file passes C1 to C9 (the orchestrator pasted OK; re-derive C7 and C9 by hand) and `invariants.INV-6` is byte-equal to the design.

## Output

`.orchestration/validation/dotfiles-T128-gate-evidence-a02-amend-review-a01.md`: header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-gate-evidence-a02: confirm|revise`, then `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-a02-amend-review-a01 status=ready_for_review verdicts=dotfiles-T128-gate-evidence-a02:<v> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing tracked files; branches; PRs.
