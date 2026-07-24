# T22 Sandbox Record

OpenSandbox was unavailable. The implementation used an isolated git worktree
under `/private/tmp` on `fix/doctor-settings-idempotency`, based on
`origin/main`.

The implementation worktree changed only the four T22 allowlisted files.
Because chezmoi resolves the live source from the main worktree, the same
four-file patch was temporarily applied there solely for the authorized
two-cycle live E2E. It was reverse-applied immediately afterward; main tracked
status was clean.

The live runs intentionally updated managed runtime state through `make update`.
No direct runtime-state edits were made, and no agmsg store files were changed
by the implementation.

After acceptance, the GitHub merge succeeded but the required main-worktree
parity guard was nonempty. The isolated worktree was intentionally retained,
and no guarded reset or branch deletion was performed.

The revised acceptance authorized a clean-tree fast-forward. Main synchronized
to the merge commit, after which the isolated T22 worktree and local topic
branch were removed.
