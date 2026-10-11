---
format: 2
reset_of: dotfiles-T128-process-rules-a02
redesign_task: dotfiles-T128-process-rules-a03
design_sha256: 867ea4ca7c86f6518432a12254c3befc471184140b46b66aea2c53e6cb5ec78d
redesign_source: dotfiles-T128-process-rules-redesign-a02
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
reason: "design INV-6 amendment threshold on PR 318 under task a02: amendment 1 (06:53Z) added the threat_table the relay task lacked (Bot P1 4240566259), and the review seat's round-4 item found a missing row (the PR edits the docs test module that pins its own rule sentences); a second amendment is the second AGMSG-TASK after the first, the count INV-6 names, so the rule's path is a reset with a redesign by another context"
---

# Design reset: dotfiles-T128-process-rules-a02 (PR #318), 2026-10-11

- **What stops:** task id a02's specification (the relay of the redesign of a01's threat-table rule). Its content stands: items 1 to 5, the revise round's five checks and the three Bot P2 fixes are carried into a03 unchanged; the branch, PR #318 and the worker continue.
- **Why a reset and not a second amendment:** INV-6 counts AGMSG-TASKs after the first; a02 has one (amendment 1) and a second would reach the threshold of 2. The cause is the orchestrator's under-specification twice over (no threat table in the relay; then an incomplete one). The rule exists for exactly that: the specification is re-done by a context other than the author.
- **Redesign:** `dotfiles-T128-process-rules-redesign-a02` on the review seat produces the whole a03 task file (a02 at `b6500dbf…` plus the fourth row, the row-1 citation fix, the ids and the history paragraph); the orchestrator writes it byte-identical from the receipt and the review seat confirms its hash with `verdict=accept design_sha256=<hash>`, the anchor the boundary probe reads.
- **Counts carried:** PR #318 so far: a01 (RESULTs 2, revises 1, Bot P1 heads after the first RESULT 4 → reset 1), a02 (RESULTs 1, revises 1 in progress, amendments 1, questions 1, Bot P1 heads after the first RESULT 1: `108b43bd`).
- **Waiver:** none.
- **Anchor:** redesign RESULT 471 (`claude-review-dot-a001`, 06:52:46Z, receipt `e890f0ad…`, `a03_expected_sha256=867ea4ca…`); the a03 file written from the receipt's block hashes to `867ea4ca…` (matches); the probe's anchor is that identity's `verdict=accept design_sha256=867ea4ca…` (confirmed: RESULT 476, 06:57:11Z, `verdict=accept design_sha256=867ea4ca…`).
