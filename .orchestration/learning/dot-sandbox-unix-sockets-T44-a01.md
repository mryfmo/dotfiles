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

## Revision 2 triage

1. **Weigh every socket on the host before allowing all Unix sockets.** A blanket socket
   allowance combined with auto-approved sandboxed Bash is only as safe as the most powerful
   socket reachable: `docker.sock` for a docker-group user, the `systemd --user` bus. Trust
   boundary changes need the security-profile review (`model-selection.md`) before acceptance.
   Status: observation, which the orchestrator already recorded in the task file.
2. Candidate check (not done; outside r2's literal scope): the validator could *reject*
   `network.allowAllUnixSockets: true` instead of the generator silently dropping an unknown key,
   so the relaxation cannot return unnoticed. Status: candidate, not promoted.
