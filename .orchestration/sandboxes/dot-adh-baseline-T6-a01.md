# Sandbox
Dedicated worktree; rsync copy and read-only integrity/scan checks. Canonical baseline untouched. No baseline scripts executed, no tests run past scanner-scope stop, no stage/commit/push/PR. No VM or OpenSandbox needed.

## Authorized continuation
Executed existing unit suite and asset validator unchanged in dedicated worktree; no local Bats. Staged only the copied reviews tree. Canonical original and copied baseline bytes remain identical. No external runtime activation or commits.
