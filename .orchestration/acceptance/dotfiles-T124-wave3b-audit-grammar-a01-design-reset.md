---
format: 2
reset_of: dotfiles-T124-wave3b-audit-grammar-a01
redesign_task: dotfiles-T128-regime-v3-a01
redesign_seat: "claude-deep-dot under DESIGN_RESET_WAIVED_BY=operator (decision 2026-10-11, answer \"orchestrator drafts + fresh-context review required\"); reviewed before dispatch by claude-review-dot-a001 on the review profile (AGMSG-TASK dotfiles-T128-design-review-a01 2026-10-10T21:04:16Z); this waiver covers the T128 design only, no further orchestrator-authored design under T128"
reason: "T126 INV-6 (d) reached, reported by the worker itself at 2026-10-10T12:47:13Z (Bot P1 on two post-RESULT heads: 7a83cb66 thread 4237434169, 9fc521fe thread 4237652017); 5 amendments, one of them (Amendment 3) a redirect from a prose grammar to a schema while the PR was open"
---

# Design reset: dotfiles-T124-wave3b-audit-grammar-a01

Written 2026-10-11 by the orchestrator seat on the operator's direction after the 2026-10-10 halt.

- Abandoned: PR #314 `feat/audit-grammar` (worker `claude-standard-dot-a003`, worker-f), closed unmerged and kept as a reference branch; final head 9fc521fe.
- Why not patched: the task changed its deliverable mid-flight (grammar to schema, pane run to detached-worktree runner) and grew to a 555-line runner with 756 lines of tests; the reset threshold fired and the worker reported it correctly.
- Salvaged into the redesign: `scripts/schemas/audit.json`, the AGENTS.md Audit text (auditor's standing over the orchestrator's artifacts, five categories), the `AGMSG-AUDIT` history record. Replacement: a thin runner around `codex exec --output-schema` with a `claude -p --json-schema` fallback (T128 V2).
- Worker seat removed with `herdr-agents --remove-worker`; the worker took no further action.
