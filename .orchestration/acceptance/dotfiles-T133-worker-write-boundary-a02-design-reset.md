---
format: 2
reset_of: dotfiles-T133-worker-write-boundary-a02
redesign_task: dotfiles-T133-worker-write-boundary-a03
design_sha256: 49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b
redesign_source: dotfiles-T133-worker-write-boundary-a02-redesign-review-a01
redesign_seat: claude-standard-dot-a011 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T133-worker-write-boundary-a02: amendments 3 (D-024-34/35); the lineage was reset to a03 (TASK 2693, reset_of=a02) without this record and without an accepting RESULT, so make check-regime-boundary kept reporting the S2 line (measured 2026-10-20T14:01Z)."
---

# Design reset: dotfiles-T133-worker-write-boundary-a02, anchored 2026-10-20

- **What stopped:** the a02 specification after three amendments; the lineage continued as a03 (TASK 2693 and its amendments, the live task of codex-standard-dot-a010 on PR #431).
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT; the orchestrator skipped that step at the reset (process debt recorded in the P1-p measurement of 2026-10-20).
- **Redesign:** `.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md` at sha256 `49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b` (the bytes of its last dispatch, amendments 2-4), `reset_of: [dotfiles-T133-worker-write-boundary-a02]`.
- **Anchor:** RESULT of `dotfiles-T133-worker-write-boundary-a02-redesign-review-a01` by claude-standard-dot-a011: `verdict=accept design_sha256=49161bc7f91b36ea7c20258a40add43b9707b4e7479dbcf3cf57ed330f61082b`, review at `.orchestration/dotfiles-T133-worker-write-boundary-a02-redesign-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
