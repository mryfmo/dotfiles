---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": "0b874adb9850ff9647fbc039ec3cf6cc30487488",
  "ledger": [],
  "pr": 400,
  "searches": [],
  "task": "dotfiles-T131-claude-pinned-merge-gate-a01"
}
---
# Acceptance record: dotfiles-T131-claude-pinned-merge-gate-a01

PR #400 `fix/claude-pinned-merge-gate`, the operator's own change applied live on the user's decision of 07:17 JST: the merge and update-branch subcommands of the gh pull-request CLI gated by the PreToolUse hook gh-merge-gate.sh instead of a human ask, the create gate, the SSH pushInsteadOf removal, the NO_COLOR fix, the validator and runtime-check additions. Integrated through the normal path: the worker review task, the sweep, a security-profile headless review, the task-level audit, this record and the gate, then the merge pinned to the audited head.

- 2026-10-17T23:2xZ record created before the first dispatch (Orchestrator Playbook step 6).
- 2026-10-17T23:4xZ #400's head moved from 85e40e77 to 0b874adb (the operator reverted the resolve-thread commit); the record's head follows the current head; a010's review of 85e40e77 (10 findings: 7 P1, 3 P2) is kept as input at .orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/review-85e40e77.md and the review is re-tasked on the current head (amendment 2).
