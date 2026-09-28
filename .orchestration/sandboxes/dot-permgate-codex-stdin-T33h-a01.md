# T33h sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/permgate-codex-stdin` from `origin/main` (a4bddfc). The worktree was
  clean before the switch. The local branch `fix/ua-core-build-shim`, merged
  as 2b30a21, was deleted as the task allows.
- Only fake `claude`/`codex` CLIs were used, inside the tests' temp
  directories; no real classifier was run. The open-pipe stdin was created
  and closed within the test process.
- The permgate policy, hooks and other scripts were untouched. There was no
  `make apply`/`chezmoi apply`, no local bats run, no force push and no
  merge.
