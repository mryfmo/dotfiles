# dotfiles-T78-dead-docs-adh-a01 — sandbox

- Isolation:
  - dedicated worktree `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-d`;
  - branch `chore/dead-docs-adh`, created from `origin/main` 6534df0f (#258) with `git switch --no-track -c`;
  - identity `claude-standard-dot-a006` (Claude Code, `standard`).
- Ran in the Claude Code Bash sandbox: `git rm`, the edits, prettier, the docs unit test, `make unit-test` and `make validate-agent-assets`.
- Ran unsandboxed through the permission gate:
  - `git fetch`/`push`;
  - `gh pr create`/`checks`/`api`;
  - the main-checkout `contextdb_cli.py memory add`;
  - `agmsg-dispatch`.
- Not touched:
  - `home/dot_config/claude/rules/**`, `README.md`;
  - the `adh` model profile and its validators (T79);
  - any code.
- Not run: `make update`/`make apply`, local bats, merge.
- No Plan Mode was used, so `plan-mode-used` does not apply.
