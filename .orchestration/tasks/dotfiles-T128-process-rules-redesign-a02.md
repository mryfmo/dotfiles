---
format: 2
task_id: dotfiles-T128-process-rules-redesign-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-rules-redesign-a02 — the reset redesign of the a02 task (INV-6: amendments threshold)

Drafted 2026-10-11 06:5xZ by the orchestrator seat. `dotfiles-T128-process-rules-a02` (PR #318) reached INV-6's amendment threshold by the orchestrator's own under-specification: the relay task carried no `threat_table` (Bot P1 4240566259; amendment 1 added three rows) and the added table missed the row for the PR's control of its own oracle, `tests/unit/test_agmsg_orchestration_docs.py` (your round-4 item). A second amendment would be the second TASK after the first, the count INV-6 names, so the rule's path is a reset: a redesign written by a context other than the author. You are that context; this is read-only.

## What to produce

The complete text of the successor task file `dotfiles-T128-process-rules-a03.md`: the a02 file at sha256 `b6500dbfbd86d40ffc9227ef9533317060da4cdf9536a8517d96a8ef7ee6d421` (read it from `.orchestration/tasks/dotfiles-T128-process-rules-a02.md`) with exactly these changes and no other:

1. `task_id: dotfiles-T128-process-rules-a03`; `reset_of: [dotfiles-T128-process-rules-a01, dotfiles-T128-process-rules-a02]`.
2. The fourth `threat_table` row: the PR edits `tests/unit/test_agmsg_orchestration_docs.py`, the module that pins its own rule sentences, so it controls the oracle too; `residual:` the orchestrator's diff review and the audit from `main` (main-tests is no control here: the module is declared and would run only in dormant-contract mode).
3. Row 1's citation: INV-7 (the Bot's review is swept feedback, never a design receipt) and R8, not trust anchor 4.
4. The heading and first paragraph say a03 continues a02 on the same branch and PR (`docs/regime-pattern`, #318) from the worker's current head, with items 1 to 5, the revise round's five checks and the three Bot P2 fixes of `21c160c8` carried over unchanged; the "Amendment 1" paragraph becomes a "History" paragraph naming the two resets (a01: the disposition-grammar class; a02: the amendment threshold) in two sentences.
5. The worker's first commit of a03 copies the file byte-identical to `.orchestration/dotfiles-T128-process-rules-a03/task.md` (the a01 and a02 directories stay as history).

## Output

`.orchestration/validation/dotfiles-T128-process-rules-redesign-a02.md` with the usual header and the whole a03 file in one fenced block (` ```markdown ` … ` ``` `), then `AGMSG-RESULT v1 task_id=dotfiles-T128-process-rules-redesign-a02 status=ready_for_review verdict=redesign receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. The orchestrator writes the a03 file from the block and asks you for one confirmation of its hash (`verdict=accept design_sha256=<hash>`), the reset anchor. max_turns=3. Forbidden: editing tracked files; branches; PRs.
