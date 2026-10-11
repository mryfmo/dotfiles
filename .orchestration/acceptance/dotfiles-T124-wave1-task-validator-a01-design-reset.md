---
format: 2
reset_of: dotfiles-T124-wave1-task-validator-a01
redesign_task: dotfiles-T128-regime-v3-a01
redesign_seat: "claude-deep-dot under DESIGN_RESET_WAIVED_BY=operator (decision 2026-10-11, answer \"orchestrator drafts + fresh-context review required\"); reviewed before dispatch by claude-review-dot-a001 on the review profile (AGMSG-TASK dotfiles-T128-design-review-a01 2026-10-10T21:04:16Z); this waiver covers the T128 design only, no further orchestrator-authored design under T128"
reason: "T126 INV-6 reached on its own implementing PR: 8 amendments (limit 4), 2 revise rounds (limit 2), 6 PONG questions, 52 Bot threads on 10 heads (33 on a hand-written validator); the orchestrator was preparing a waiver instead of a reset"
---

# Design reset: dotfiles-T124-wave1-task-validator-a01

Written 2026-10-11 by the orchestrator seat on the operator's direction after the 2026-10-10 halt; the operator chose "reset and rebuild small" over a waiver.

- Abandoned: PR #313 `feat/task-validator` (worker `claude-standard-dot-a001`, worker-c), closed unmerged and kept as a reference branch; final head 52bb69fc.
- Why not patched: 33 of the 52 Bot findings are bypass findings against a 503-line validator with its own YAML parser and a 316-line glob matcher, written on the premise that PyYAML is unavailable where the validator runs; the Makefile and CI already install it with `uv run --with pyyaml`. A wrong premise, not a defect list. The PR also exceeded the design's own 15-file limit (20 files, +2,642 lines).
- Salvaged into the redesign: the format-2 key set, the process-tier table, the test ideas. Replacement: a JSON Schema for task files validated by the `jsonschema` library, a short validator, and a main-pinned CI job (T128 V1).
- Worker seat removed with `herdr-agents --remove-worker`; the worker took no further action.
