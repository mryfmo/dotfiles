---
format: 2
reset_of: dotfiles-T128-ci-skip-orchestration-a01
redesign_task: dotfiles-T128-ci-skip-orchestration-a02
design_sha256: 2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
redesign_source: dotfiles-T128-ci-skip-redesign-a01
redesign_seat: claude-review-dot-a001 (review profile, a context other than the task's author)
reason: "design INV-6 on PR 320: two RESULTs (456, 485: revises=1) and one amendment; the second audit (dc4e6c37) found the hand-written workflow reader's class a second time (spaced, escaped and flow-mapping keys after the first audit's quoted keys) and re-raised the design-on-main prerequisite (main at b896d9bc holds neither the task's implementing_tasks entry nor its INV-2 sentence); a further round reaches a threshold, so the rule's path is a reset with a redesign by another context"
---

# Design reset: dotfiles-T128-ci-skip-orchestration-a01 (PR #320), 2026-10-11

- **What stops:** task id a01's specification. The branch, PR #320, the worker `claude-standard-dot-a003` and the implementation (in-job fail-closed decision, no `needs`, no job-level `if`, `--no-renames`, the required-context constant) continue under `dotfiles-T128-ci-skip-orchestration-a02`.
- **Why a reset:** the reader finding recurred as a class (quoted keys, then spaced and escaped keys and flow mappings); fixing it form by form is the pattern the operator's rule forbids, and the specification said nothing about unsupported syntax. The design-on-main finding is the orchestrator's: the task was dispatched under plan 006 Phase 0's rule that a boundary is never a dispatch prerequisite, which contradicts INV-2's hashed sentence ("the design file must be on main (through a boundary PR) before the implementing TASK is dispatched"); the auditor is right. The remedy is mechanical: design v16 goes to `main` by the boundary PR `orchestration/boundary-2026-10-11-2` before this PR's final audit, and the plan's Phase 0 rule is corrected to INV-2's text (recorded in plan 006).
- **Redesign:** `dotfiles-T128-ci-skip-redesign-a01` on the review seat produces the whole a02 task file (fail-closed reader row with four mutation tests; the design-on-main row with the boundary PR in `after:`); the orchestrator writes it byte-identical from the receipt and the review seat confirms its hash (`verdict=accept design_sha256=<hash>`), the anchor.
- **Counts carried:** A5 at the reset: tasks 2, amendments 1, questions 0, results 2, revises 1, Bot P0/P1 heads after the first RESULT 0, wall 05:42Z to 07:13Z (1 h 31 min).
- **Waiver:** none.
- **Anchor:** redesign RESULT 496 (`claude-review-dot-a001`, 07:33:43Z, receipt `c55e1585…`, `a02_expected_sha256=2c3a5ee2…`, matched on disk); the review seat's `verdict=accept design_sha256=2c3a5ee2…` is the anchor (confirmed: RESULT 502, 07:37:09Z, byte-for-byte). `after:` stays `[]` (V1 types it as task ids); the boundary dependency is the design-on-main row. The successor ids need `implementing_tasks` entries (v16 maps the a01 ids only): design v17 adds `dotfiles-T128-ci-skip-orchestration-a02: [INV-2]` and `dotfiles-T128-regime-counters-a02: [INV-6]`, reviewed as a pair (round 18) and carried by the next boundary PR.
