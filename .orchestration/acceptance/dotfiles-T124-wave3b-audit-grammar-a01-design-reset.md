---
format: 2
reset_of: dotfiles-T124-wave3b-audit-grammar-a01
redesign_task: dotfiles-T128-regime-v3-a01
redesign_source: dotfiles-T128-design-review-a01
design_sha256: 4520b8f0ac5663a0879acd4eb0fe5a5bc585bdca6c53aac6dae1d5de94bf07a8
redesign_seat: "claude-deep-dot under DESIGN_RESET_WAIVED_BY=operator (decision 2026-10-11, answer \"orchestrator drafts + fresh-context review required\"); reviewed before dispatch by claude-review-dot-a001 on the review profile (AGMSG-TASK dotfiles-T128-design-review-a01 2026-10-10T21:04:16Z); this waiver covers the T128 design only, no further orchestrator-authored design under T128"
reason: "T126 INV-6 (d) reached, reported by the worker itself at 2026-10-10T12:47:13Z (Bot P1 on two post-RESULT heads: 7a83cb66 thread 4237434169, 9fc521fe thread 4237652017); 5 amendments, one of them (Amendment 3) a redirect from a prose grammar to a schema while the PR was open"
---

# Design reset: dotfiles-T124-wave3b-audit-grammar-a01

Written 2026-10-11 by the orchestrator seat on the operator's direction after the 2026-10-10 halt.

- Abandoned: PR #314 `feat/audit-grammar` (worker `claude-standard-dot-a003`, worker-f), closed unmerged and kept as a reference branch; final head 9fc521fe.
- Why not patched: the task changed its deliverable mid-flight (grammar to schema, pane run to detached-worktree runner) and grew to a 555-line runner with 756 lines of tests; the reset threshold fired and the worker reported it correctly.
- Salvaged into the redesign: `scripts/schemas/audit.json`, the AGENTS.md Audit text (auditor's standing over the orchestrator's artifacts, five categories), the `AGMSG-AUDIT` history record. Replacement: a thin runner around `codex exec --output-schema` with a `claude -p --json-schema` fallback (T128 V2).
- Worker seat removed with `herdr-agents --remove-worker`; the worker took no further action.
- **Anchor (added 2026-10-11 06:00Z, plan 006 A3):** `design_sha256` is the whole-file sha256 of the redesign task `dotfiles-T128-regime-v3-a01.md` at v16 (`15957fbc…`), accepted by `claude-review-dot-a001` (round 16, 04:04:48Z, `verdict=accept design_sha256=15957fbc…`) and confirmed by the Codex headless round 17; the `DESIGN_RESET_WAIVED_BY=operator` line above stays as history and is reported as `waiver-unanchored` by the boundary probe until V3a's `regime-waive.sh` exists.
- **Anchor moved to v17 (2026-10-11 07:48Z):** the design is `1d5f4c07…` after round 18 (accepted by `claude-review-dot-a001`, RESULT 504, `verdict=accept design_sha256=1d5f4c07…`); a whole-file anchor follows every accepted design version until V1's canonical hash lands.
- **Anchor at the design's receipt pointer update (07:58Z):** `4520b8f0…` (v17 with `design_review.receipt` naming round 18; round 19 confirms the hash).
