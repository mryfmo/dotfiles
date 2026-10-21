---
format: 2
reset_of: dotfiles-T133-worker-write-boundary-a03
redesign_task: dotfiles-T133-worker-write-boundary-slice1-a01
design_sha256: e39dc8fbf4143509c53438d070648a6b03ba211c4af9da1def7534a7167c4bdc
redesign_source: dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02
redesign_seat: codex-standard-dot-a012 (standard profile, a context other than the task's author)
reason: "INV-6 S2 on dotfiles-T133-worker-write-boundary-a03: amendments 4 (D-024-34/35 and the two later amendments) and the worker's runtime-naming block (PONG runtime-blocked-pong.txt, 2026-10-20T06:05Z); re-plan v2 J2 replaced the single a04 reset text by five slices, slice 1 being the reset carrier"
---

# Design reset: dotfiles-T133-worker-write-boundary-a03, anchored 2026-10-21

- **What stopped:** the a03 specification after four amendments and the a010 runtime-naming block; the a04 single reset text (653 lines) was withdrawn undispatched after its C-80 round 1 P2.
- **Why this record now:** plan 006 A3 / V3a silence a reached INV-6 threshold only with a reset record whose redesign another context accepted in a RESULT.
- **Redesign:** `.orchestration/tasks/dotfiles-T133-worker-write-boundary-slice1-a01.md` at sha256 `e39dc8fbf4143509c53438d070648a6b03ba211c4af9da1def7534a7167c4bdc` (design 2 round 2: 189 lines, 7 allowed_files, 37 threat rows, `reset_of: [dotfiles-T133-worker-write-boundary-a03]`, `after: [dotfiles-T133-trusted-entrypoint-pins-a01, dotfiles-T133-worker-sandbox-exclusions-a02]`); the allocation of a04's 22 paths and 90 threat rows across five slices is `.orchestration/plans/024-allocation.tsv`; slices 2-5 and the owners `dotfiles-T133-trusted-entrypoint-descendants-followup-a01`, `dotfiles-T133-agmsg-hardening-a01` exist as task files.
- **Anchor:** RESULT 2948 of `dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02` by codex-standard-dot-a012: `verdict=accept design_sha256=e39dc8fbf4143509c53438d070648a6b03ba211c4af9da1def7534a7167c4bdc`, review `.orchestration/dotfiles-T133-worker-write-boundary-slice1-a01-redesign-review-a02/review.md` (review a01 rejected the earlier bytes 3844d937: F1 prerequisite-baseline conflict, F2 `Keep after: []`; both resolved).
- **Dispatch:** not yet; slice 1 is sent to codex-standard-dot-a010 at these bytes after `dotfiles-T133-trusted-entrypoint-pins-a01` and PR #448 merge (the Checks block is pasted at dispatch; the anchored bytes are the design and must not change).
- **Waiver:** none.
