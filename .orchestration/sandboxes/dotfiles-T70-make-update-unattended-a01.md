# dotfiles-T70-make-update-unattended-a01 — sandbox

- Isolation: dedicated git worktree `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-d`, branch `fix/make-update-unattended` from `origin/main` c6de5156. Worker identity: `claude-standard-dot-a006` (Claude Code, `standard` profile).
- Claude Code Bash sandbox (bubblewrap) for edits, tests, and local gates. The following steps ran unsandboxed through the normal permission gate, and none of them needed agent-to-agent approval:
  - `git push origin HEAD:refs/heads/fix/make-update-unattended`, `gh pr create`, `gh pr checks`, `gh api`: network boundary.
  - `python3 .claude/hooks/contextdb_cli.py memory add` in the main checkout: `.claude/contextdb/state` is read-only inside this worktree's sandbox (`[Errno 30] Read-only file system`).
  - `agmsg-dispatch` PONG/RESULT: the herdr socket returned `PermissionDenied` inside the sandbox.
- The sandbox left a 0-byte read-only stub at `/home/moriya/Workspace/dotfiles/.git/config.lock`, which blocks git config writes. The branch was therefore created with `--no-track` and pushed without `-u`.
- `git status` in the worktree shows sandbox phantom stubs (`.bash_profile`, `.bashrc`, `.claude/agents`, …) as untracked. They are not task files and were neither staged nor touched.
- No `make update`, `make upgrade`, `make apply`, or local bats was run. One ad-hoc fake-herdr shell exercise of the recipe was denied by the permission gate and not retried, so the Herdr branch behaviour is covered by `lifecycle.bats` in CI.
