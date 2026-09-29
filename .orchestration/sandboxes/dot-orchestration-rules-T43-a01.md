# T43 sandbox record

- No container or VM isolation was used. All git work happened in
  `.claude/worktrees/worker-c` on `feat/orchestration-rules-T43` from
  origin/main 258339f, which was clean before the switch.
- Graph comparisons read committed graphs via `git show` into the session
  scratchpad. No `.ua/**` change.
- The unit test creates and removes a temporary git repository under the
  system temp dir.
- Network: `git push` of the task branch, `gh pr create` and `gh pr checks`.
  No `make update`, no local Bats, no force push, no merge.
- Writes outside the worktree were limited to the listed `.orchestration`
  artifacts and the CompactionDB `memory add`.
