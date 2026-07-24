# T27 report: PR #87 npm allow-scripts rebase

## Result

- Rebased the existing `fix/npm-allow-scripts-agent-clis` branch onto `origin/main`.
- Resolved the lifecycle test conflict by preserving main's required-failure assertions and adding the scoped allow-scripts regression assertion.
- Dropped the duplicate `scripts/upgrade-tools.sh` insertion because current main already contains the same scoped allow-scripts flag.
- Kept the remaining `claude-update` fix and the shared repair regression assertion.
- Force-pushed the existing branch with lease and updated PR #87's title and body to match the final two-line diff.
- Did not merge.

## Final state

- PR: https://github.com/mryfmo/dotfiles/pull/87
- Head: `350291393bd051a00e264402cf04d220df0e2c7d`
- Base: `5d6acf84f00d735fd17ff8fb790f561f0591087e`
- Mergeability: `MERGEABLE`
- Merge state: `CLEAN`
- Changed files: `home/dot_zshrc`, `tests/install/common/lifecycle.bats`
- GitHub Actions: all required jobs passed; Nix was intentionally skipped by workflow conditions.
- CodeRabbit: pass (`Review rate limited` status detail).

## Review

- Final diff was inspected against `origin/main`; only the two allowed files differ.
- `git diff --check` passed and no conflict markers remain.
- `make require-crit-review` reported: `Review not required: no meaningful review trigger found.`
