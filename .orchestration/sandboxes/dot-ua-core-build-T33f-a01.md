# T33f sandbox record

- No container or VM isolation was used. All git work happened in the
  dedicated worker worktree `.claude/worktrees/worker-c`, on branch
  `fix/ua-core-build` from `origin/main` (7b42472). The worktree was clean
  before the switch.
- The tests use a temp HOME and a restricted PATH of symlinked system tools
  plus fake `pnpm`/`mise`. The real `update-agent-assets.sh` flow, `make
  update`, `mise install` and `pnpm` were never executed. The Claude plugin
  cache and `~/.understand-anything` on this host were only read (for
  `package.json` and the lockfile header).
- The only network access was the read-only
  `gh api repos/pnpm/pnpm/releases` query, for the 7-day window check.
- No `make apply` or `chezmoi apply` was run. The local Bats suite was not
  run. There was no force push and no merge.
