# Sandbox: dotfiles-T98c-claude-seat-artifact-write-exception-a01

- **Sandboxed:** edits, the docs test, `make unit-test`, the validator, prettier, ruff (`ruff format --check`; output in the validation file, "Ruff" section), and the commit.
- **Unsandboxed, through the permission gate:**
  - push, `gh pr create`, `gh pr checks --watch`, and the bot-wait polling;
  - CompactionDB `memory add`;
  - writing and masking these five artifacts in the main checkout's `.orchestration/` (now the documented Worker Playbook step 4 case);
  - `agmsg-dispatch`.
- **No scratch worktrees**, and no `git worktree prune`.
- **Not done:** no other file, no `make update`/`apply`, no thread resolution, no local bats.
