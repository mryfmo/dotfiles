# Sandbox: dotfiles-T98-evidence-home-path-masking-a01

- **Sandboxed:**
  - edits;
  - the re-mask run over the worktree's tracked `.orchestration` (the main checkout was not touched);
  - the verification script, unit tests, `make unit-test`, `make render-check`, `make validate-agent-assets` and ruff;
  - commits, including the local history rewrite before the first push: `git reset --hard 2b7e3797` plus a cherry-pick, both on this unpushed branch.
- **Unsandboxed:**
  - `git push`, `gh pr create`, `gh pr checks --watch` and the bot-wait polling;
  - CompactionDB `memory add` and readback;
  - masking these five artifacts in the main checkout;
  - `agmsg-dispatch`.
- **Scratch worktrees:** none in round 0. In revise round 1, one was created to restore the verbatim "11" grep (`git worktree add --detach <scratchpad>/t98-f318 f3181a63`, under the session scratchpad) and removed with `git worktree remove --force` only. No `git worktree prune` was run in any round, and `git worktree list` showed no leftover entry afterwards (validation file).
- **Not done:**
  - no change to `SECRET_PATTERN` or to what counts as a credential;
  - no edit to the launcher, the rule or any worker worktree;
  - no `make update`/`apply`/`upgrade`;
  - no merge, force push or thread resolution;
  - no local bats.
