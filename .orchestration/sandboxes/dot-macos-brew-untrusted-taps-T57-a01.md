# Sandbox: dot-macos-brew-untrusted-taps-T57-a01

- **Worktree and branch:** worker-c, branch `fix/macos-brew-untrusted-taps` from `origin/main` 18d192aa. As before, the switch was finished with `git symbolic-ref` after the `.git/config.lock` stub stopped it, and the index was clean afterwards.
- **Commit and push:** one commit, `f314ab2a`, committed and pushed sandboxed. `git ls-remote` shows `f314ab2a5f0606f3987f23e1d295a3ec91dd97b0`.
- **Ran sandboxed:**
  - `shellcheck`, `shfmt` (bare form and the pinned `mise x shfmt@3.14.1` form)
  - `make validate-agent-assets`
  - a plain-bash smoke test with a fake `brew`. No bats were run locally, no `make apply`, and no real `brew`, which is absent on this Linux host.
- **Ran unsandboxed** (`dangerouslyDisableSandbox`):
  - `gh api`, to read the Homebrew/brew source at tag 7.0.7 and the check-run annotations
  - `gh pr create`, `gh pr checks` and `gh run view --log`
  - `scripts/pr-feedback.py`
  - CompactionDB `memory add` in the main checkout
  - the writes to the main checkout's `.orchestration/*/dot-macos-brew-untrusted-taps-T57-a01.md`
  - `agmsg-dispatch`
- **WebFetch:** one read of https://docs.brew.sh/Tap-Trust.
- **Denied command:** one Bash command with an inline `bash -c` script plus `rm -rf` was denied by the permission layer. I reran it as a scratch-file script without the cleanup.

## Revise round 1

- **Commits and push:** two new commits, `50c833b3` (measurement) and `f568eab6` (final), both on the same branch with no force push. They were committed and pushed sandboxed. `git ls-remote` shows `f568eab6a1032a9d134d89cb43f3b0200f2016fc`.
- **Ran unsandboxed:**
  - `gh pr checks/edit/view`, `gh run view --log`, `gh api` (annotations), and `scripts/pr-feedback.py`
  - the rewrites and appends to the main checkout's T57 `.orchestration` files
  - `agmsg-dispatch`
- **Sandboxed checks:** `shellcheck`, `shfmt` (both forms), `make validate-agent-assets` and the plain-bash smoke test. No local bats were run, and no `make apply`.
