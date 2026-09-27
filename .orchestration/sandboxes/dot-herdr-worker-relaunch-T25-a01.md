# Sandbox

OpenSandbox not used.

- Writes: worktree `.claude/worktrees/worker-c` only, on branch `feat/herdr-worker-relaunch` (commit `3be4656`, pushed); opened PR #186. In the main checkout, only these `.orchestration` artifacts and one CompactionDB decision record (`692f51c0-2d96-4fdb-9cd9-2bf1ea57aa28`).
- Live herdr: read-only calls only (`herdr workspace list`, `herdr pane list --workspace wF`, `herdr agent list`, `herdr agent --help`, `herdr agent prompt --help`). I used them to confirm the root cause: the pair workspace `wF` is labeled `dotfiles`, not `dotfiles agents`. No pane or workspace was created, prompted, killed, or closed. Tests used only the fake-binary pattern.
- Round 2: rebased onto origin/main `668ff64` and ran one `git push --force-with-lease=refs/heads/feat/herdr-worker-relaunch:3be46563bf21c9e509c825d3f4357c235661a0ef`, which the orchestrator allowed for that round only. The final head is `f9b158a`.
- Not run: `make apply`, `chezmoi apply`, local bats, merge, any other force push.
