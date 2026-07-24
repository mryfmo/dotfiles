# Plan 002 learning triage

## Decision

Reusable operational rule recorded in this orchestration artifact; no project
worklog or plan was edited.

## Learning

For Crit CLI 0.18.0 operational evidence, unresolved-only JSON is vacuous after
resolution, while `crit comments --all --json <review.json>` provides the
non-empty resolved-list shape needed for a local mistake-prevention gate.
Accepting that list does not authenticate the reviewer or bind the evidence to
a target; those properties must not be claimed by this local contract.

Linked-worktree commit capability depends on the active sandbox permission
profile, not only source-tree write access. Recheck the current profile before
treating an earlier metadata-permission failure as a persistent STOP condition.

When a guard changes its accepted evidence shape, update and statically assert
every deployed managed instruction, not only repository-root operator docs.
Otherwise installed agents can retain a command that can never satisfy the
guard even though the implementation and top-level documentation agree.

## Apply to

- Future review-guard plans and tests: require non-empty resolved records and
  keep human and agent marker paths separate.
- Sandbox execution: retry the exact Git operation when a later worker receives
  explicit linked-worktree metadata write access.
- Managed agent rules and lifecycle tests: keep the deployed Crit command
  sequence and process-evidence boundary aligned with the review guard.
