# Sandbox: dotfiles-T73-tool-versions-from-config-a01

- **Worktree and branch:** worker-c, branch `chore/tool-versions-from-config` from `origin/main` 523fda06.
  - The `git switch -c` was finished with `git symbolic-ref` and `git reset --hard HEAD` on the clean tree.
  - After `gh pr update-branch`, I fast-forwarded to the merge head.
  - `git push -u` printed "unable to write upstream branch configuration" (the read-only `.git/config`). The push itself landed: `git ls-remote` shows `60688d49`.
- **Local mise checks:** they used a scratch copy of config.toml and mise.lock under `/tmp/claude-1000/t73-mise-*`, with `mise trust` on that copy. `where`/`which` and `install --dry-run` reported "already installed". No `~/.config/mise` or pin file was changed.
- **Unit tests** ran in the Claude sandbox.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `mise` on the scratch copy, and the smoke script against the installed binaries;
  - `gh pr create/checks/update-branch` and `gh api`;
  - CompactionDB `memory add`;
  - `make validate-agent-assets` in the main checkout;
  - the writes to the main checkout's T73 `.orchestration` files;
  - `agmsg-dispatch`.
