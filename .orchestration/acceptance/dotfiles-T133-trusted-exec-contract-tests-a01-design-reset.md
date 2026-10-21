---
format: 2
reset_of: dotfiles-T133-trusted-exec-contract-tests-a01
redesign_task: dotfiles-T133-trusted-exec-contract-tests-a02
design_sha256: 0b1923a6299109c1f8db3a56dfbba3cc6ac0c5217d08a577322f99f5617e4380
redesign_source: dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01
redesign_seat: claude-standard-dot-a009 (standard profile, a context other than the task's author; the review profile authored the a02 text)
reason: "INV-6 S2 on dotfiles-T133-trusted-exec-contract-tests-a01 (PR #436): three RESULTs (round 1, revise 1 for the audit of 9545e59f, the records-only amendment round that repaired the orchestrator's unhashed text change), revises=2, measured by make check-regime-boundary at 2026-10-20T14:01Z. The code at 612f75f5 is complete and twice audited; a02 changes no code."
---

# Design reset: dotfiles-T133-trusted-exec-contract-tests-a01 (PR #436), anchored 2026-10-20

- **What stops:** the a01 specification. PR #436 (head 9cc6c96b after update-branch, code 612f75f5), the worker claude-standard-dot-a011 and the implementation continue under `dotfiles-T133-trusted-exec-contract-tests-a02`, a records-only round (the a02 task copy; report.md names the three unchanged code files and their sha256).
- **Why a reset:** INV-6 S2 by the count of RESULTs; the third RESULT was the records-only round that repaired an orchestrator omission (the revise-1 instruction changed line 136's requirement without a hashed amendment, audit:a561e64:3). The two implementation P2 of the a561e64 audit stay advisory under `dotfiles-T133-trusted-exec-contract-tests-followup-a01`.
- **Redesign:** `.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a02.md` at sha256 `0b1923a6299109c1f8db3a56dfbba3cc6ac0c5217d08a577322f99f5617e4380` (review profile; two checker fixes by the orchestrator: `retained_predecessor_directories` and the two copy rows), `reset_of: [dotfiles-T133-trusted-exec-contract-tests-a01]`.
- **Anchor:** RESULT of `dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01` by claude-standard-dot-a009 at 2026-10-20T14:19:49Z: `verdict=accept design_sha256=0b1923a6299109c1f8db3a56dfbba3cc6ac0c5217d08a577322f99f5617e4380`, review at `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01-redesign-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
