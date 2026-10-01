# T44 learning triage

## Candidates

1. **Sandboxed git leaves a `.git/config.lock` stub.** With the Claude Code
   sandbox active, git commands in a linked worktree can leave a read-only
   zero-byte `.git/config.lock` stub on disk. That blocks all later config
   writes (branch tracking, `push -u`, `git config`) for every worktree of
   the repository. Workers under the sandbox should create branches with
   `--no-track`, push with `git push origin HEAD`, and run git metadata
   operations outside the sandbox. The orchestrator should decide whether
   to exclude git from the sandbox (`excludedCommands`) or clean the stub.
2. **Recover a half-applied `git switch -c`.** If `git switch -c` fails only
   on the config lock, the branch ref, index and tree may already have
   moved while HEAD has not. Recover with `git symbolic-ref HEAD
   refs/heads/<branch>` after confirming the index matches the new branch,
   never with `reset` or `checkout -f`.

## Promotion

None. These are candidates only.
