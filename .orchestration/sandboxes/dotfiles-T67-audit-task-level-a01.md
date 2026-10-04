# Sandbox: dotfiles-T67-audit-task-level-a01

- **Worktree and branch:** worker-c, branch `feat/audit-task-level` from `origin/main` 3a0816e6. The `git switch -c` was finished with `git symbolic-ref` and `git reset --hard HEAD` on the clean tree. After `gh pr update-branch`, I fast-forwarded to the merge head.
- **Phantom config lock:** the main checkout has an empty read-only `.git/config.lock` (created 10:09:10 local, the sandbox's deny-mask mount point). The unsandboxed `git push -u` could not write the upstream config ("could not lock config file … File exists"), but the push landed (`git ls-remote`). I did not delete the file, because each sandboxed command recreates it.
- **No audit runs:** no `herdr-agents --audit` and no `codex` run against the live workspace. The tests use the fake herdr and a scratch git DIR.
- **Unit tests** ran in the Claude sandbox.
- **Unsandboxed runs** (`dangerouslyDisableSandbox`):
  - `gh pr create/checks/update-branch` and `gh api`;
  - CompactionDB `memory add`;
  - `make validate-agent-assets` in the main checkout;
  - the writes to the main checkout's T67 `.orchestration` files;
  - the `stat` of the lock file;
  - `agmsg-dispatch`.
