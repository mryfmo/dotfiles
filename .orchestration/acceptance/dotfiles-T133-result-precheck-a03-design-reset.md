---
format: 2
reset_of: dotfiles-T133-result-precheck-a03
redesign_task: dotfiles-T133-result-precheck-a04
design_sha256: e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700
redesign_source: dotfiles-T133-inv6-reset-anchors-review-a01
redesign_seat: codex-standard-dot-a012 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T133-result-precheck-a03: reset chain of P1-5; a04 is PR #411; the lineage was reset to dotfiles-T133-result-precheck-a04 by a TASK line with reset_of but without this record and without an accepting RESULT, so make check-regime-boundary kept reporting the S2 line (measured 2026-10-20T14:36Z)."
---

# Design reset: dotfiles-T133-result-precheck-a03, anchored 2026-10-20

- **What stopped:** the a03 specification; the lineage continued as dotfiles-T133-result-precheck-a04.
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT; the orchestrator skipped that step at the reset (process debt measured on 2026-10-20).
- **Redesign:** `.orchestration/tasks/dotfiles-T133-result-precheck-a04.md` at sha256 `e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700` (the bytes of its last dispatch), `reset_of: [dotfiles-T133-result-precheck-a03]`.
- **Anchor:** RESULT of `dotfiles-T133-inv6-reset-anchors-review-a01` by codex-standard-dot-a012 at 2026-10-20T14:57:43ZZ: `verdict=accept design_sha256=e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700 lineage=dotfiles-T133-result-precheck-a03`, review at `.orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
