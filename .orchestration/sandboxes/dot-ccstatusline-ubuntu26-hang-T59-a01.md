# Sandbox: dot-ccstatusline-ubuntu26-hang-T59-a01

- **Worktree and branch:** worker-c, branch `fix/ccstatusline-ubuntu26-hang` from `origin/main` 750cc4a9. The switch was finished with `git symbolic-ref` after the `.git/config.lock` stub stopped it, and the index was clean afterwards.
- **Commits and push:** four commits (three temporary diagnostics, one fix), committed and pushed sandboxed with no force push. The final head is `cc19dd4c`.
- **Local checks (sandboxed):**
  - read the ccstatusline 2.2.30 bundle in `~/.local/share/mise/installs` (read-only)
  - `make unit-test` and `make validate-agent-assets`
  - a single unittest for the guard fix
  - a pyyaml load of `test.yaml` through `uv run --with pyyaml`

  No local bats were run, and no `make apply`.
- **Diagnostics ran on the CI canary cell only:** `strace`, `fincore`, `NODE_DEBUG` and `MISE_LOG_LEVEL=trace`.
- **Ran unsandboxed** (`dangerouslyDisableSandbox`):
  - `gh pr create/edit/ready/checks/view`, `gh run view --log` and `gh api` (runner-images readmes)
  - CompactionDB `memory add`
  - the writes to the main checkout's T59 `.orchestration` files
  - `agmsg-dispatch`, for PONG 707 and the RESULT
