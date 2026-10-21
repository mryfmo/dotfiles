---
format: 2
reset_of: dotfiles-T128-chain-review-scripts-followup-a07
redesign_task: dotfiles-T128-chain-review-scripts-followup-a08
design_sha256: 93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b
redesign_source: dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01
redesign_seat: claude-standard-dot-a011 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T128-chain-review-scripts-followup-a07 (PR #439, head a644a7d9): two amendments (one the orchestrator's erroneous resend 2710, M-20261020-03) and the audit P1 audit:a644a7d:1 (review content read from the worker-writable shared object store, design 5.14 item 8); D-024-41 reset the lineage to a08, D-024-52 narrowed a08 to the private-bare-clone local review with the chain hardening owned by a09, D-024-53 corrected the recalled inherited figures and pasted Checks before the anchor review."
---

# Design reset: dotfiles-T128-chain-review-scripts-followup-a07, anchored 2026-10-21

- **What stopped:** the a07 specification after two amendments and the P1 of its final-head audit; PR #439 stays open and a08 continues its branch `tools/chain-review-scripts-followup-a07`.
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT.
- **Redesign:** `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md` at sha256 `93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b` (138 lines, 6 allowed_files, `reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]`, Checks pasted: merge-base b8213131, main a811f133, inherited 27+6 and 94+8 lines). C-80 history: design 1 one round, design 2 two rounds, round 3 `…-text-security-cbc39be.md` Verdict correct on the design bytes cbc39be; the only later change is the Checks block and the B:117 figures (D-024-53).
- **Anchor:** RESULT 2969 of `dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01` by claude-standard-dot-a011: `verdict=accept design_sha256=93e4c6a41646d07dddace2ee76c9439dc2d8af4067605bbd477f3f082d1c2c5b`, round 2 after the round 1 reject (RESULT 2967, empty Checks block); review `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08-redesign-review-a01/review.md` in the seat's worktree (worker-d) until the next records boundary.
- **Dispatch:** to codex-standard-dot-a013 (worker-h) at these bytes, with no subsequent paste (B:130); the dispatch line and its counters snapshot are recorded in the a08 acceptance record.
- **Waiver:** none.
