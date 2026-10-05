# dotfiles-T77-harness-dead-code-a01 — sandbox

- Isolation:
  - dedicated worktree `~/Workspace/dotfiles/.claude/worktrees/worker-d`;
  - branch `chore/harness-dead-code`, created from `origin/main` f6320f37 (#259) with `git switch --no-track -c`;
  - identity `claude-standard-dot-a006` (Claude Code, `standard`).
- Ran in the Claude Code Bash sandbox: the edits, `git rm`, the generator write, `make render-check`, `bash -n`/`zsh -n`, shellcheck, shfmt, ruff, prettier, the focused and full unit tests, and `make validate-agent-assets`.
- Ran unsandboxed through the permission gate:
  - `git fetch`/`push`;
  - `gh pr create`/`checks`/`api`;
  - the main-checkout `contextdb_cli.py memory add`;
  - `agmsg-dispatch`.
- Not touched:
  - `home/dot_claude/hooks/executable_enforce-uv.sh` (item 5: Claude boundary, routed to T77b);
  - `.github/workflows/docs.yml`, `vendor/compactiondb/**`, any pin;
  - `.gitignore`, `plans/`.
- Not run: `make update`/`make apply`, local bats, merge.
- No Plan Mode was used, so `plan-mode-used` does not apply.
