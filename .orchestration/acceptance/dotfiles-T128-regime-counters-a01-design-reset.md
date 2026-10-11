---
format: 2
reset_of: dotfiles-T128-regime-counters-a01
redesign_task: dotfiles-T128-regime-counters-a02
design_sha256: afc46c3b7e7fb91bdc61196921e897327061f189da540b27408e66d122f1b8b7
redesign_source: dotfiles-T128-regime-counters-redesign-a01
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
reason: "design INV-6 on PR 319: after amendment 1 the task has two RESULTs (revises=1) and one amendment, and the audit of 72764f05 found two P1s (status and verdict tokens matched anywhere in a message body; a reset record may name an unrelated, already accepted design) and one P2 (the fixtures put 1735 added lines under tests/ against INV-2's cap of 1000); any further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
---

# Design reset: dotfiles-T128-regime-counters-a01 (PR #319), 2026-10-11

- **What stops:** task id a01's specification. The branch, PR #319, the worker `claude-standard-dot-a004` and the implementation continue under `dotfiles-T128-regime-counters-a02`, which carries the two missing threat rows (first-token reads of `status=`/`verdict=`; the redesign task's `reset_of` must name the task being reset) and the fixture budget, and is otherwise the a01 file at `d9a44b7e…`.
- **Why a reset:** two of the three audit findings are specification gaps of the orchestrator's (the anchor rule did not bind the redesign to the task; the fixture budget was not stated and the acceptance record's cap claim was wrong) and the third is an implementation defect the specification's wording ("counts follow INV-6's sentence") did not pin to first-token reads. The counts leave no second round under the rule.
- **Redesign:** `dotfiles-T128-regime-counters-redesign-a01` on the review seat produces the whole a02 task file; the orchestrator writes it byte-identical from the receipt's block and the review seat confirms its hash (`verdict=accept design_sha256=<hash>`), the anchor the boundary probe reads. The T128 design's own `reset_of` names the T124 waves, so the binding rule holds for the existing resets.
- **Counts carried:** A3 at the reset: tasks 2, amendments 1, questions 0, results 2, revises 1, Bot P0/P1 heads after the first RESULT 0, wall 2 h 23 min to the second RESULT.
- **Waiver:** none.
- **Anchor:** redesign RESULT 479 (`claude-review-dot-a001`, 06:58:42Z, receipt `b4864193…`, `a02_expected_sha256=0cfd6689…`); the file written from the block needed one mechanical fix (the twelfth row's `control:` value held a colon-space and PyYAML rejected the front matter; the orchestrator wrapped that one value in double quotes, nothing else), so the on-disk hash is `afc46c3b…`; the review seat's `verdict=accept design_sha256=afc46c3b…` on the on-disk file is the anchor (confirmed: RESULT 483, 07:01:02Z). Dispatched to `claude-standard-dot-a004` at 07:03Z.
