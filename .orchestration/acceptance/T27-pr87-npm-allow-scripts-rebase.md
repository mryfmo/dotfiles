# T27 acceptance: PR #87 npm allow-scripts rebase

- Task: `.orchestration/tasks/T27-pr87-npm-allow-scripts-rebase.md`
- Result: PR [#87](https://github.com/mryfmo/dotfiles/pull/87), rebased head
  `350291393bd051a00e264402cf04d220df0e2c7d` on `5d6acf8`.
- Verdict: **accepted** (next_action=merge).

## Verification performed

- Independent diff read: final diff is exactly two lines in two files —
  `claude-update()` in `home/dot_zshrc` gains
  `--allow-scripts=@anthropic-ai/claude-code`, and `lifecycle.bats` pins the
  scoped `--allow-scripts="${npm_package}"` flag in `upgrade-tools.sh`.
- The worker's dedup claim verified independently: main's
  `scripts/upgrade-tools.sh:293` already carries the scoped flag, and main's
  `dot_zshrc` did not — dropping the duplicate hunk was correct and the new
  bats assertion converts main's existing behavior into a regression guard.
- Live smoke in validation: the exact npm command shape with the scoped
  allow-scripts installed claude-code 2.1.218 with no allow-scripts warning
  and a native arm64 binary present (postinstall actually ran).
- `make unit-test` (226 OK), `make validate-agent-assets`, shellcheck/shfmt,
  `zsh -n`, `git diff --check` all green; bats on CI only per policy.
- CI at head `3502913`: all GitHub Actions jobs SUCCESS (nix skipped by
  workflow condition), CodeRabbit SUCCESS, merge state CLEAN/MERGEABLE.

## Next action (delegated to worker)

Squash-merge PR #87 with branch deletion, verify clean tracked tree, ff-only
sync of local `main`, remove the T27 worktree and any leftover stale
`wt-npm-allow-scripts` worktree registration, reply
AGMSG-RESULT v1 task_id=T27 status=merged with the merge commit hash.
