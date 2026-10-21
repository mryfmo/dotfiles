---
format: 2
reset_of: dotfiles-T133-worker-write-boundary-a01
redesign_task: dotfiles-T133-worker-write-boundary-a02
design_sha256: ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50
redesign_source: dotfiles-T133-worker-write-boundary-a01-redesign-review-a01
redesign_seat: claude-standard-dot-a009 (standard profile, a context other than the task's author; the review profile authored the a02 text)
reason: "INV-6 S2 on dotfiles-T133-worker-write-boundary-a01: amendments 5 (M-20261018-10); the lineage was reset to a02 by TASK 2561 (reset_of=a01) without this record and without an accepting RESULT, so make check-regime-boundary kept reporting the S2 line (measured 2026-10-20T14:01Z)."
---

# Design reset: dotfiles-T133-worker-write-boundary-a01, anchored 2026-10-20

- **What stopped:** the a01 specification after five amendments. The lineage continued as a02 (TASK 2561, 2026-10-19) and then a03 (TASK 2693, reset_of a02), the live task of worker codex-standard-dot-a010 on PR #431.
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT; the orchestrator had skipped that step at both resets (process debt recorded in the P1-p measurement of 2026-10-20).
- **Redesign:** `.orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md` at sha256 `ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50` (the bytes of its last dispatch, TASK 2652), `reset_of: [dotfiles-T133-worker-write-boundary-a01]`.
- **Anchor:** RESULT of `dotfiles-T133-worker-write-boundary-a01-redesign-review-a01` by claude-standard-dot-a009 at 2026-10-20T14:12:11Z: `verdict=accept design_sha256=ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50`, review at `.orchestration/dotfiles-T133-worker-write-boundary-a01-redesign-review-a01/review.md` (copied from the worker's worktree by the orchestrator, evidence sync).
- **Waiver:** none.
