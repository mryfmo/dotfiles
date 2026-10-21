---
format: 2
reset_of: dotfiles-T133-permission-guard-gate-a01
redesign_task: dotfiles-T133-permission-guard-gate-a02
design_sha256: 8623badb987ae8c4c5f66a3ac3ab1bfefb1e347e878c31ae6317eba726f6b1d4
redesign_source: dotfiles-T133-inv6-reset-anchors-review-a01
redesign_seat: codex-standard-dot-a012 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T133-permission-guard-gate-a01: questions 3 (P1-14); the lineage was reset to dotfiles-T133-permission-guard-gate-a02 by a TASK line with reset_of but without this record and without an accepting RESULT, so make check-regime-boundary kept reporting the S2 line (measured 2026-10-20T14:36Z)."
---

# Design reset: dotfiles-T133-permission-guard-gate-a01, anchored 2026-10-20

- **What stopped:** the a01 specification; the lineage continued as dotfiles-T133-permission-guard-gate-a02.
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT; the orchestrator skipped that step at the reset (process debt measured on 2026-10-20).
- **Redesign:** `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md` at sha256 `8623badb987ae8c4c5f66a3ac3ab1bfefb1e347e878c31ae6317eba726f6b1d4` (the bytes of its last dispatch), `reset_of: [dotfiles-T133-permission-guard-gate-a01]`.
- **Anchor:** RESULT of `dotfiles-T133-inv6-reset-anchors-review-a01` by codex-standard-dot-a012 at 2026-10-20T14:57:44ZZ: `verdict=accept design_sha256=8623badb987ae8c4c5f66a3ac3ab1bfefb1e347e878c31ae6317eba726f6b1d4 lineage=dotfiles-T133-permission-guard-gate-a01`, review at `.orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
