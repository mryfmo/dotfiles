# Sandbox: dotfiles-T113-codify-T111-lessons-a01

- **Worktree:** `.claude/worktrees/worker-c`, branch `feat/codify-t111-lessons` from `origin/main` `7d3a45ee` (`git fetch origin`, then `git switch -c … --no-track origin/main`). T112's branch was left untouched.
- **Sandboxed:**
  - the edits and the generator;
  - `chezmoi execute-template`. It read `~/.config/chezmoi` and rendered the configured source path; nothing was written to the canonical clone;
  - `bash -n`, shellcheck and shfmt;
  - the scratch-repository behaviour checks under the session scratchpad (git repositories with a bare origin, and a stubbed `identities.sh` under a temporary HOME);
  - the live `check-regime-boundary.sh --report` (read-only probes);
  - `make -n update` (dry run; no `make update`);
  - render-check, the validator, the unit modules, `make unit-test`, ruff, prettier, `crit status` and both commits.
- **Outside the sandbox (`dangerouslyDisableSandbox`, through the permission gate):**
  - `git push`, `gh pr create`, `gh pr edit 302 --body-file` (body only), the check-runs and `gh pr checks` waits, and the Bot-wait loop;
  - the CompactionDB `memory add` of the decision and failure lines in the main checkout;
  - writing and masking the seven artifacts in the main checkout;
  - `agmsg-dispatch` for the RESULT.
- **Worker review:** one read-only general-purpose subagent, resumed once for the fix commit. It used scratch repositories under `/tmp/claude-1000/review-t113-scratch/` and wrote nothing in the repository.
- **Not done:** no `make update`/`make upgrade`, no touch of `~/.local/share/chezmoi`, no thread resolution, no hand edit of a generated file.

## Revise round 1

- **Same isolation as round 0.**
  - **Sandboxed:** the generator edit and run, the test edit, the unit runs (including the one temporary `git show 7d3a45ee:… > scripts/check-regime-boundary.sh` swap, restored with `git checkout --` and verified clean), ruff, the validator and the commit.
  - **Outside the sandbox through the permission gate:** `git push`, the check-runs wait, `gh pr checks`, the Bot-wait loop, the artifact appends and masking, and `agmsg-dispatch`.
- I did not merge `origin/main` into the branch.

## Revise round 2

- **Same isolation as round 1.**
  - **Sandboxed:** the fast-forward, the edits, the template render and lint, prettier, render-check, the validator, the docs test and the commit.
  - **Outside the sandbox through the permission gate:** `git push`, the CI wait, `gh pr checks`, the Bot-wait loop, the artifact appends and masking, and `agmsg-dispatch`.
