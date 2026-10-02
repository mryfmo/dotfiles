# Sandbox: dot-git-ignore-cc-writes-T56-a01

- **Worktree and branch:** worker-c, branch `chore/git-ignore-cc-writes` from `origin/main` 1f3bb5e1. The sandboxed `git switch -c` again stopped on the `.git/config.lock` stub, and I finished it with `git symbolic-ref HEAD refs/heads/chore/git-ignore-cc-writes`. After that, `git status --porcelain --untracked-files=no` was empty.
- **Commit and push:** one commit, `bce7c64b`, committed and pushed sandboxed. `git ls-remote` shows `bce7c64bb152132d03e8c32f024801f22c515bf7`.
- **Ran sandboxed:** read-only chezmoi only (`chezmoi status/diff --source <worktree>`, `chezmoi execute-template`), plus `make render-check` and `make validate-agent-assets`. No apply.
- **Ran unsandboxed** (`dangerouslyDisableSandbox`):
  - `gh pr create` and `gh pr checks`
  - CompactionDB `memory add` in the main checkout
  - the writes to the main checkout's `.orchestration/*/dot-git-ignore-cc-writes-T56-a01.md`
  - `agmsg-dispatch`, for the PONG (message 692) and the RESULT, as the task instructs
- **Placeholder files:** the sandbox placeholders at the worktree root (19 character devices) are untracked and were not staged.
