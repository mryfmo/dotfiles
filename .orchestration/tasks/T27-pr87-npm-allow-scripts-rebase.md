# T27: Rebase PR #87 (npm allow-scripts for agent CLIs) onto main and land it

## Objective

PR [#87](https://github.com/mryfmo/dotfiles/pull/87)
(`fix/npm-allow-scripts-agent-clis`) has been CONFLICTING since 2026-07-21.
Rebase onto current `origin/main`, resolve conflicts (expected mainly in
`tests/install/common/lifecycle.bats`, which #92 also touched), get CI green,
and prepare it for merge.

## PR intent that must survive

Allow the `@anthropic-ai/claude-code` postinstall script through npm's
allow-scripts supply-chain gate so `make upgrade`'s
`repair_mise_npm_packages` step no longer warns and skips it.

## Constraints

- FRESH worktree from `origin/main`; do not reuse the stale
  `/private/tmp/claude-501/-Users-mryfmo-Workspace-dotfiles/6537dbd1-*/scratchpad/wt-npm-allow-scripts`
  worktree (dead session); `git worktree remove --force` it if it blocks the
  branch checkout.
- Update the EXISTING PR #87 branch via rebase + force-push; no new PR.
- Allowed files: `home/dot_zshrc`, `scripts/upgrade-tools.sh`,
  `tests/install/common/lifecycle.bats`, plus mechanical rebase resolutions.
- Forbidden: unrelated cleanups, dependency changes, local bats runs, merge
  before AGMSG-ACCEPTANCE next_action=merge.

## Verification

- `make unit-test`, `make validate-agent-assets`, shellcheck/shfmt green.
- Bats runs on CI only (repo policy): push and confirm all GitHub Actions
  checks and CodeRabbit pass on the PR.
- Live smoke: run the repaired npm allow-scripts path once (the
  `repair_mise_npm_packages` invocation or its equivalent command) and show
  the warning is gone in the validation artifact.

## Expected artifacts

- report: .orchestration/reports/T27-pr87-npm-allow-scripts-rebase.md
- validation: .orchestration/validation/T27-pr87-npm-allow-scripts-rebase.txt
- sandbox: .orchestration/sandboxes/T27-pr87-npm-allow-scripts-rebase.md
- learning: .orchestration/learning/T27-pr87-npm-allow-scripts-rebase.md
- autoskill: .orchestration/autoskill/runs/T27-pr87-npm-allow-scripts-rebase.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review with PR head SHA. max_turns=30
