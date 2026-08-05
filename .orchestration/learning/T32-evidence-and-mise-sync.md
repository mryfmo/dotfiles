# T32 learning

Date: 2026-07-25

## Learnings

- A command that copies from main and commits must run with the task worktree as its working directory; source and destination paths alone do not scope Git operations.
- After a main-worktree remediation, treat main as copy-only and run every Git command from the dedicated worktree.

## Plan Updates

- For future evidence syncs, verify `pwd` and `git rev-parse --show-toplevel` in the task worktree immediately before every commit.
