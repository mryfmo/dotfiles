# T33a sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `docs/orchestration-rules-T33a` from `origin/main` (ca4af19). The worktree
  was clean before the switch. Revision 2 was applied on the same branch with
  no rebase.
- Only rule and skill text changed. No scripts, tests, manifests, hooks, or
  permissions were touched. No herdr pane was read or probed.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not
  run: the lifecycle.bats grep tokens were checked with plain `grep -qF`
  instead. There was no force push and no merge.
