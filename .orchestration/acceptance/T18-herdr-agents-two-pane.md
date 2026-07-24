# T18 acceptance: herdr-agents two-pane layout

- Task: `.orchestration/tasks/T18-herdr-agents-two-pane.md`
- Result: accepted (after one revision round)
- Worktree/branch: `/Users/mryfmo/Workspace/dotfiles-t18` / `feat/herdr-file-viewer-popup`
- Commit: `b9b5eab feat: use two-pane herdr agent layout`

## Adversarial review notes (orchestrator, independent re-verification)

- Read the full whitespace-ignored diff of `executable_herdr-agents`: five
  yazi/files functions deleted; 2-pane rewrites of unambiguity/order/ratio
  repair match the task's geometry spec (single split, adjacency + same
  y/height checks, total/2 target, +-2 tolerance, one resize + convergence
  re-check); legacy `files` pane tolerated via refuse-repair paths and the
  kept `empty_pane_id` exclusion; claude rename ordered before the ambiguity
  guard per the "no mutations beyond the claude rename" requirement.
- Independently re-ran: `uv run pytest tests/unit/test_herdr_agents.py`
  (51 passed), `shellcheck` (clean),
  `shfmt --indent 4 --space-redirects --diff` (clean), `grep -c yazi` → 0,
  `git diff main --stat` (only the two allowed files).
- Revision round: the first submission reformatted the whole script to tab
  indentation because the task's validation command used bare `shfmt -d`
  (extensionless file → editorconfig `[*.sh]` does not match → shfmt tab
  default), which would fail the repo's `make lint`
  (`shfmt --indent 4 --space-redirects --diff .`). Revised commit restores
  repo convention; validation artifact updated to the repo flags.
  Root cause was the orchestrator's task spec, recorded in learning.

## Verdict

- status=accepted; live E2E deferred to Phase C per plan (required before
  merge, covers fresh workspace + persisted legacy-session restore).
