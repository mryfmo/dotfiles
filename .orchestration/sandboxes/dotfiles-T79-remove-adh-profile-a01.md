# dotfiles-T79-remove-adh-profile-a01 — sandbox

- Isolation:
  - dedicated worktree `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-d`;
  - branch `chore/remove-adh-profile`, created from `origin/main` 36ffe6ca with `git switch --no-track -c`, then fast-forwarded to the GitHub update-branch merge 123bf104;
  - identity `claude-standard-dot-a006` (Claude Code, `standard`).
- Ran in the Claude Code Bash sandbox: `git rm`, the edits, the generator write, `make render-check`, ruff, the focused and full unit tests, and `make validate-agent-assets`.
- Ran unsandboxed through the permission gate:
  - `git fetch`/`push`/`merge --ff-only`;
  - `gh pr create`/`update-branch`/`checks`/`api`;
  - the main-checkout `contextdb_cli.py memory add`;
  - `agmsg-dispatch`.
- Not touched:
  - the other profiles;
  - the `claude.*`/`codex.*` blocks;
  - hooks, permissions, sandbox, README.
- Not run: `make update`/`make apply` (the deployed `~/.codex/adh.config.toml` goes on the operator's next apply), local bats, merge.
- No Plan Mode was used, so `plan-mode-used` does not apply.
