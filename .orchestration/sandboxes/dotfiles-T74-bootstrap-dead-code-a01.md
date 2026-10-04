# Sandbox: dotfiles-T74-bootstrap-dead-code-a01

- **Worktree and branch:** worker-c, branch `chore/bootstrap-dead-code` from `origin/main` 138e6a72. The `git switch -c` was finished with `git symbolic-ref` and `git reset --hard HEAD`. Both pushes landed (`git ls-remote`). `push -u` could not write the upstream config because of the phantom `.git/config.lock`.
- **chezmoi rendering** used `execute-template` against the worktree source, a temp config (`data.system=client`) and a temp persistent state. There was no `chezmoi apply` and no change to `~/.config/chezmoi`.
- **`make`:** only `make -n init` (a dry run).
- **No local bats.**
- **Unit tests** ran in the Claude sandbox.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `gh pr create/checks` and `gh api`;
  - CompactionDB `memory add`;
  - the writes to the main checkout's T74 `.orchestration` files;
  - `agmsg-dispatch`.
