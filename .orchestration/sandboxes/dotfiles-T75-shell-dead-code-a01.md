# Sandbox: dotfiles-T75-shell-dead-code-a01

- **Worktree and branch:** worker-c, branch `chore/shell-dead-code` from `origin/main` 40d9eb6c.
  - The `git switch -c` was finished with `git symbolic-ref` and `git reset --hard HEAD` on the clean tree.
  - After `gh pr update-branch`, I fast-forwarded to the merge head.
  - The phantom `.git/config.lock` (see T67) again made `push -u` unable to write the upstream config. The push landed (`git ls-remote`).
- **No apply:** no `chezmoi apply`, no local bats, and no live shell changes. The deploy scope was read from `home/.chezmoitemplates/chezmoiignore.d`.
- **Untouched files:** I did not open or edit the flagged orchestrator file `dotfiles-T67-…-review-receipt.md`.
- **Unit tests** ran in the Claude sandbox.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `gh pr create/checks/update-branch` and `gh api`;
  - CompactionDB `memory add`;
  - `make validate-agent-assets` in the main checkout;
  - the writes to the main checkout's T75 `.orchestration` files;
  - `agmsg-dispatch`.
