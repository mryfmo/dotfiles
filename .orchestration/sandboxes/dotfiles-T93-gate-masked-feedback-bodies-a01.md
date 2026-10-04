# Sandbox: dotfiles-T93-gate-masked-feedback-bodies-a01

- **Sandboxed:** git fetch, branch, commit and push. The phantom `.git/config.lock` made `git switch -c` and `push -u` warn; I finished with `git reset --hard origin/main` on the new branch, and the push landed, verified with `git ls-remote`.
- **Also sandboxed:** `make unit-test`, `make validate-agent-assets`, the unittest runs, the scratch mise runs of ruff and prettier, and the Python NUL scans.
- **Unsandboxed:**
  - `inbox.sh`, `history.sh` and `agmsg-dispatch`;
  - `gh pr create`, `gh pr edit`, `gh api` and `gh pr checks`, which get 401 inside the sandbox;
  - the pushes of `4db6083a` and `63e8fd90`, each in the same unsandboxed call as a timestamp lookup;
  - `gh pr update-branch 251`;
  - CompactionDB `memory add` from the main checkout.
- **Aborted capture:** a zsh `$ref:` history-modifier expansion stopped one comparison capture after it had overwritten `scripts/require-crit-review.py` with the base version. I restored it from the scratch copy and verified it against HEAD.
- **Denied:** one Bash call with `rm -rf` on a scratch dir under `$TMPDIR`. It was redone without `rm` in a fresh scratch dir.
- **Writes outside the worktree:** only scratch files under `$TMPDIR` and the five T93 artifacts in the main checkout's `.orchestration`, written with Python.
- **Not done, as the task forbids:** no merge, no force push, no push to main, no thread resolution, no local bats, no `make update`, `make apply` or `make upgrade`, no `~/.codex` edits.

## Revise round 1

- **Sandboxed:** edits, tests, the commit and the NUL scans.
- **Unsandboxed:** the pushes of `56546541` and `62cf4aa9`, two `gh pr update-branch` calls (the first raced the push and was retried), `gh` polling, and these artifact writes.
- A zsh `echo` turned `\0` and `\x00` in a command label into real NUL bytes in a scratch capture. I rewrote the label line with Python and checked the capture held 0 NUL bytes before pasting it.

## Revise round 2

- **Sandboxed:** edits, tests and the commit.
- **Unsandboxed:** the push, `gh` polling, and these artifact writes. The UTF-16 check of the main checkout was a read-only Python scan; nothing outside the worktree was modified.
