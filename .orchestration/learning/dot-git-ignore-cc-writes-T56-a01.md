# Learning triage: dot-git-ignore-cc-writes-T56-a01

Candidates only; nothing is promoted.

1. **Match the live file byte for byte.**
   - Lesson: when a tool appends a line to a chezmoi-managed target and that causes `MM`, adding the line to the source somewhere else does not converge. chezmoi still sees the target as changed and prompts. The source has to match the live content exactly (here: a blank line, then the line at EOF).
   - Candidate: future "make the target converge" tasks state the exact live bytes, check them with `chezmoi status --source <worktree> <target>` (empty = in sync) before dispatch, and use that same command as the worker's acceptance check.
2. **Check placement instructions against the stated objective.**
   - Lesson: a placement instruction that contradicts the stated objective should be verified with a read-only chezmoi check and raised as PONG blocked, not followed literally. Here that cost one round trip and avoided a PR that would not have unblocked `make update`.
