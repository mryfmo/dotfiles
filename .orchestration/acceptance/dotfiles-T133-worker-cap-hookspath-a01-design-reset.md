---
format: 2
reset_of: dotfiles-T133-worker-cap-hookspath-a01
redesign_task: dotfiles-T133-worker-cap-hookspath-a02
design_sha256: 661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4
redesign_source: dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01
redesign_seat: claude-standard-dot-a009 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T133-worker-cap-hookspath-a01: amendments 3; the lineage was reset to a02 (TASK 2147) without this record and without an accepting RESULT, so make check-regime-boundary kept reporting the S2 line (measured 2026-10-20T14:01Z)."
---

# Design reset: dotfiles-T133-worker-cap-hookspath-a01, anchored 2026-10-20

- **What stopped:** the a01 specification after three amendments; the lineage continued as a02 (TASK 2147).
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT; the orchestrator skipped that step at the reset (process debt recorded in the P1-p measurement of 2026-10-20).
- **Redesign:** `.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md` at sha256 `661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4` (the bytes of its dispatch), `reset_of: [dotfiles-T133-worker-cap-hookspath-a01]`.
- **Anchor:** RESULT of `dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01` by claude-standard-dot-a009 at 2026-10-20T14:15:54Z: `verdict=accept design_sha256=661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4`, review at `.orchestration/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
