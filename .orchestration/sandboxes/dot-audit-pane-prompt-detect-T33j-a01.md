# T33j sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/audit-pane-prompt-detect` from `origin/main` (d7a5947). The merged
  local branch `fix/orchestration-hygiene-T33i` was deleted.
- The mutation baseline temporarily replaced the worktree script with
  `git show origin/main:home/dot_local/bin/common/executable_herdr-agents`,
  then restored the change from a scratchpad copy. The diff was checked
  afterwards.
- herdr and codex were exercised only through fakes. Real herdr was used for
  `--help` only; no real pane was read or probed, and no audit, codex, or
  herdr tab or pane was used.
- There was no `make apply`/`chezmoi apply`, no local bats run, no force
  push and no merge.
