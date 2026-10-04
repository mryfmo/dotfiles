# Sandbox record: dotfiles-T92-stop-gate-sandbox-placeholders-a01

- Worker `claude-standard-dot-a007` in its own worktree `.claude/worktrees/worker-e`, on branch `fix/stop-gate-sandbox-placeholders` created from `origin/main` (`06875e4e`) with `--no-track`.
- Bash ran in the Claude Code bubblewrap sandbox by default. These commands ran unsandboxed: `git push`, `gh` calls, `agmsg-dispatch`, the CompactionDB `memory add` in the main checkout, and the artifact writes to the main checkout's `.orchestration/`.
- The sandbox placeholders this task is about (19 untracked entries, 26 `ro` bind mounts under the worktree) were inspected read-only and never modified. Only scratch files under `TMPDIR` were created; one `real-untracked.txt` probe in the worktree was created and removed in the same command.
