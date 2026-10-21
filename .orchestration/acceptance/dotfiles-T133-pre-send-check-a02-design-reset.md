---
format: 2
reset_of: dotfiles-T133-pre-send-check-a02
redesign_task: dotfiles-T133-pre-send-check-a03
design_sha256: 53f78f967929b80987eb515affaabde637d12c1f52edb8bce5262c95f8282f77
redesign_source: dotfiles-T133-pre-send-check-a03-redesign-review-a01
redesign_seat: claude-standard-dot-a011 (standard profile, a context other than the task's author and implementer)
reason: "D-024-51 fixed in advance that any finding remaining after round 2 of PR #442 resets the lineage to a03 by another context; the round-2 audit of 1d72f169 found six P2, each in a class of the round-1 audit (argument-injection-bypass third row, S1 re-plan line), so D-024-56 executed the reset; the a03 text replaces Bash regex parsing over echoed checker output with one Python module over a single buffer."
---

# Design reset: dotfiles-T133-pre-send-check-a02, anchored 2026-10-21T07:25Z

- **What stopped:** the a02 implementation after two worker rounds (a008): six P2 at 78882410, six P2 in the same classes at 1d72f169; no third round (D-024-51).
- **Why this record now:** the reset is a decision consequence (D-024-56) and the regime's reset form (plan 006 A3 / V3a) wants the redesign accepted by another context before dispatch.
- **Redesign:** `.orchestration/tasks/dotfiles-T133-pre-send-check-a03.md` at sha256 `53f78f967929b80987eb515affaabde637d12c1f52edb8bce5262c95f8282f77` (117 lines, 4 allowed_files incl. the new `scripts/orchestrator/pre_send.py`, `reset_of: [dotfiles-T133-pre-send-check-a02]`, caps 360/480 from the merge-base, six red-then-green fixtures named per audit row, Checks pasted: merge-base e00de4e0, inherited 104/260). Authored by author-loop round 1 from `brief-pre-send-a03.md`; security:false, no C-80 (D-024-46).
- **Anchor:** RESULT 2980 of `dotfiles-T133-pre-send-check-a03-redesign-review-a01` by claude-standard-dot-a011: `verdict=accept design_sha256=53f78f967929b80987eb515affaabde637d12c1f52edb8bce5262c95f8282f77`; one P3 (the pinned uv fallback path goes stale but falls to a fixed refusal) recorded as advisory owned by `dotfiles-T133-pre-send-check-followup-a01`; review at `.orchestration/dotfiles-T133-pre-send-check-a03-redesign-review-a01/review.md` in worker-d until the next records boundary.
- **Dispatch:** to claude-standard-dot-a009 (worker-c) at these bytes, continuing PR #442's branch `tools/pre-send-check-a01` from 1d72f169; a008 holds and does not implement a03.
- **Waiver:** none.
