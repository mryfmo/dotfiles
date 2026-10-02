# Sandbox: dot-ci-runner-label-pin-T58-a01

- **Worktree and branch:** worker-c, branch `chore/ci-runner-label-pin` from `origin/main` 3c4c2cec. The switch was finished with `git symbolic-ref` after the `.git/config.lock` stub stopped it, and the index was clean afterwards.
- **Commit and push:** one commit, `88f79736`, committed and pushed sandboxed. `git ls-remote` shows `88f797360b3d7b590e5e5d1e56f9c0b1b842d88e`.
- **Ran sandboxed:** `git grep`, `make unit-test` (Python unit tests only, no bats), `make validate-agent-assets`, shellcheck and shfmt. No local bats were run, and no `make apply`.
- **Ran unsandboxed** (`dangerouslyDisableSandbox`):
  - `gh pr create/checks/view` and `gh run view`
  - CompactionDB `memory add`
  - the writes to the main checkout's T58 `.orchestration` files
  - `agmsg-dispatch`, for PONG 702 and the RESULT
