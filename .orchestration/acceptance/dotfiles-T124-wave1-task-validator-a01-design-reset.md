---
format: 2
reset_of: dotfiles-T124-wave1-task-validator-a01
redesign_task: dotfiles-T128-regime-v3-a01
design_sha256: 4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
redesign_seat: "claude-deep-dot under DESIGN_RESET_WAIVED_BY=operator (decision 2026-10-11, answer \"orchestrator drafts + fresh-context review required\"); reviewed before dispatch by claude-review-dot-a001 on the review profile (AGMSG-TASK dotfiles-T128-design-review-a01 2026-10-10T21:04:16Z); this waiver covers the T128 design only, no further orchestrator-authored design under T128"
reason: "T126 INV-6 reached on its own implementing PR: 8 amendments (limit 4), 2 revise rounds (limit 2), 6 PONG questions, 52 Bot threads on 10 heads (33 on a hand-written validator); the orchestrator was preparing a waiver instead of a reset"
---

# Design reset: dotfiles-T124-wave1-task-validator-a01

Written 2026-10-11 by the orchestrator seat on the operator's direction after the 2026-10-10 halt; the operator chose "reset and rebuild small" over a waiver.

- Abandoned: PR #313 `feat/task-validator` (worker `claude-standard-dot-a001`, worker-c), closed unmerged and kept as a reference branch; final head 52bb69fc.
- Why not patched: 33 of the 52 Bot findings are bypass findings against a 503-line validator with its own YAML parser and a 316-line glob matcher, written on the premise that PyYAML is unavailable where the validator runs; the Makefile and CI already install it with `uv run --with pyyaml`. A wrong premise, not a defect list. The PR also exceeded the design's own 15-file limit (20 files, +2,642 lines).
- Salvaged into the redesign: the format-2 key set, the process-tier table, the test ideas. Replacement: a JSON Schema for task files validated by the `jsonschema` library, a short validator, and a main-pinned CI job (T128 V1).
- Worker seat removed with `herdr-agents --remove-worker`; the worker took no further action.
- **Anchor (added 2026-10-11 06:00Z, plan 006 A3):** `design_sha256` is the whole-file sha256 of the redesign task `dotfiles-T128-regime-v3-a01.md` at v16 (`15957fbc…`), accepted by `claude-review-dot-a001` (round 16, 04:04:48Z, `verdict=accept design_sha256=15957fbc…`) and confirmed by the Codex headless round 17; the `DESIGN_RESET_WAIVED_BY=operator` line above stays as history and is reported as `waiver-unanchored` by the boundary probe until V3a's `regime-waive.sh` exists.
- **Anchor moved to v17 (2026-10-11 07:48Z):** the design is `1d5f4c07…` after round 18 (accepted by `claude-review-dot-a001`, RESULT 504, `verdict=accept design_sha256=1d5f4c07…`); a whole-file anchor follows every accepted design version until V1's canonical hash lands.
- **Anchor at the design's receipt pointer update (07:58Z):** `4520b8f0…` (v17 with `design_review.receipt` naming round 18; round 19 confirms the hash).
