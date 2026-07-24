# T21 Learning Triage

## Candidate

- Task-time staging assumptions can drift before worker execution. Capture both
  staged and unstaged patches, verify whether either is empty, and use an exact
  post-transfer allowlist comparison as the content invariant.

## Evidence

- `/tmp/T21-staged.patch` was 0 bytes.
- `/tmp/T21-unstaged.patch` contained all 27 tracked changes.
- The isolated worktree contained exactly 34 expected paths and all local and
  remote validations passed.

## Decision

Reusable and validated, but not promoted by this worker. The orchestrator may
merge it into future worktree-transfer guidance if it is not already covered.

## After-Acceptance Note

With `gh pr merge --delete-branch`, a successfully merged PR can still yield a
nonzero command when the local head branch is checked out in another worktree.
Verify PR merge state before retrying, then remove the verified worktree before
deleting the remaining local and remote branches. This is reusable and
validated here, but remains unpromoted.
