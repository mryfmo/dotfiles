# T33i sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/orchestration-hygiene-T33i` from `origin/main` (013b3d6). The local
  branch `fix/permgate-codex-stdin`, merged as 07de550, was deleted.
- The mask mode ran on the real T33c audit file only through a scratch copy
  exported with `git show 04746ca:…`. Committed `.orchestration` files were
  not modified, apart from this task's own artifacts, which were masked and
  scanned before hand-over.
- herdr and codex were exercised only through fakes. No real audit, codex,
  or herdr tab or pane was used.
- There was no `make apply`/`chezmoi apply`, no local bats run, no force
  push and no merge.
