# Sandbox: dot-audit-profile-gpt6-sol-T48-a01

- worker: claude-standard-dot-a005, worktree `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- isolation: dedicated git worktree. I created `fix/audit-profile-gpt6-sol` from origin/main (c8fc05c)
  with `git switch --no-track -c` inside the sandbox (no config write). `feat/orchestration-rules-T43`
  and `fix/sandbox-unix-sockets` were left untouched.
- Unsandboxed, each for a stated T39 limit: the generator write (`uv run --with pyyaml`, uv
  cache), the make targets (uv cache; the unit-test socket-bind test), `git push` (no `-u`), `gh`
  (keyring D-Bus), the main-checkout CompactionDB `memory add`, and writing these main-checkout
  artifacts (the main working tree is outside the Bash write allowlist).
- No auditor run, no `chezmoi apply`, no pane read, no `reviews/**` access. Sandbox deny-mount
  stubs were never added (explicit-path `git add`), and `.git/*.lock` was not removed.
