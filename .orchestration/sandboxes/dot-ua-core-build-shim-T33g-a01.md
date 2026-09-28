# T33g sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/ua-core-build-shim` from `origin/main` (4bc28b7).
- Fake `pnpm`/`mise` only, under a restricted PATH and a temp HOME.
  `make -n update` is a dry run that prints recipe lines without executing
  them. No real mise, pnpm or network install was run.
- `tests/install/common/lifecycle.bats` was edited per the revision-2
  ruling but not run locally (repo policy: bats runs in CI).
- There was no `make apply`/`chezmoi apply`, no force push and no merge.
