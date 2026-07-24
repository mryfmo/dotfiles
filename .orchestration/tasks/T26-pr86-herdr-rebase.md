# T26: Rebase PR #86 (herdr codex resolved path) onto current main and land it

## Objective

PR [#86](https://github.com/mryfmo/dotfiles/pull/86)
(`fix/herdr-agents-stray-node-global`) has been CONFLICTING since 2026-07-21.
Rebase it onto current `origin/main` (`4e761ba`), resolve conflicts so BOTH the
PR's fix and main's newer herdr behavior survive, get CI green, and prepare it
for merge.

## PR intent that must survive

1. Launch codex in the herdr pane via the mise-resolved path so a stray
   node-global install can never shadow the pinned version.
2. Detect and purge shadowing `@openai/codex` installs from the mise node tree.

## Main-side behavior that must survive

- Two-pane agents layout (#82 / T18) and prefix+f file-viewer popup (#82 / T19)
  changes to `home/dot_local/bin/common/executable_herdr-agents`.
- All current tests in `tests/unit/test_herdr_agents.py` on main.

## Constraints

- Work in a FRESH worktree from `origin/main`; do not reuse
  `/private/tmp/claude-501/-Users-mryfmo-Workspace-dotfiles/6537dbd1-*/scratchpad/wt-herdr-stray-codex`
  (stale worktree from a dead session). If that stale worktree blocks branch
  checkout, `git worktree remove --force` it first.
- Update the EXISTING PR #86 branch (`fix/herdr-agents-stray-node-global`) via
  rebase + force-push; do not open a new PR.
- Allowed files: `home/dot_local/bin/common/executable_herdr-agents`,
  `tests/unit/test_herdr_agents.py`, plus mechanical rebase resolutions only.
- Forbidden: unrelated cleanups, dependency changes, local bats runs, merge
  before AGMSG-ACCEPTANCE next_action=merge.
- shdoc-compatible English comments for any shell edits.

## Verification

- `uv run python -m unittest tests.unit.test_herdr_agents` green locally;
  `make unit-test`, `make validate-agent-assets`, shellcheck/shfmt green.
- Live end-to-end check (required because this changes pane lifecycle):
  in a DISPOSABLE directory, start a fresh herdr session, verify the codex
  pane launches via the mise-resolved path, then detach and re-attach to
  verify persisted-session restore still lays out correctly. Do NOT restart or
  modify the operator's active workspace (w1C). Record commands and output in
  the validation artifact.
- Push, confirm all GitHub Actions checks and CodeRabbit pass on the PR.

## Expected artifacts

- report: .orchestration/reports/T26-pr86-herdr-rebase.md
- validation: .orchestration/validation/T26-pr86-herdr-rebase.txt
- sandbox: .orchestration/sandboxes/T26-pr86-herdr-rebase.md
- learning: .orchestration/learning/T26-pr86-herdr-rebase.md
- autoskill: .orchestration/autoskill/runs/T26-pr86-herdr-rebase.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review with PR head SHA. max_turns=40
