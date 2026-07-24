# T28 learning triage

## Decision

Created validated learn record `20260724_160935_learn.md`.

## Rationale

Applying a temporary worktree as the chezmoi source is unsafe for source-state entries that deploy as symlinks: the live targets can point at the disposable worktree. The reusable corrective rule is to use the canonical source for a full live apply and apply branch-specific regular files narrowly. If an immediate pre-merge live check requires changed symlink-managed content, shadow the exact reviewed branch diff in the canonical source and explicitly reconcile it after merge.

This affected the T28 deployment procedure, not the committed implementation. The temporary references were removed and verified before fixture testing.
