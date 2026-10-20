---
format: 2
reset_of: dotfiles-T133-ci-efficiency-a01
redesign_task: dotfiles-T133-ci-efficiency-a02
design_sha256: 684257319a5b9b5f5c67fe5852aedd76fd5b9db4bb4f5a1ff0b928a0ad61ab98
redesign_source: dotfiles-T133-inv6-reset-anchors-review-a01
redesign_seat: codex-standard-dot-a012 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T133-ci-efficiency-a01: amendments 2 (P1-3); the lineage was reset to dotfiles-T133-ci-efficiency-a02 by a TASK line with reset_of but without this record and without an accepting RESULT, so make check-regime-boundary kept reporting the S2 line (measured 2026-10-20T14:36Z)."
---

# Design reset: dotfiles-T133-ci-efficiency-a01, anchored 2026-10-20

- **What stopped:** the a01 specification; the lineage continued as dotfiles-T133-ci-efficiency-a02.
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT; the orchestrator skipped that step at the reset (process debt measured on 2026-10-20).
- **Redesign:** `.orchestration/tasks/dotfiles-T133-ci-efficiency-a02.md` at sha256 `684257319a5b9b5f5c67fe5852aedd76fd5b9db4bb4f5a1ff0b928a0ad61ab98` (the bytes of its last dispatch), `reset_of: [dotfiles-T133-ci-efficiency-a01]`.
- **Anchor:** RESULT of `dotfiles-T133-inv6-reset-anchors-review-a01` by codex-standard-dot-a012 at 2026-10-20T14:57:45ZZ: `verdict=accept design_sha256=684257319a5b9b5f5c67fe5852aedd76fd5b9db4bb4f5a1ff0b928a0ad61ab98 lineage=dotfiles-T133-ci-efficiency-a01`, review at `.orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
