# T41 acceptance

status: accepted (after two unblock rounds)
task_id: T41-remove-cognee
reviewed_by: claude-deep-dot (orchestrator)
date: 2026-08-12

## Review history

- Block 1 (valid): the task's allowed-file list omitted
  `scripts/require-crit-review.py` and its unit test, both referencing the
  cognee launcher in the lifecycle trigger list — scope extended (steps 8b/8c).
- Block 2 (valid): the task's zero-result sweep contradicted its own
  `.chezmoiremove` retirement entry — sweep exemption added.

## Independent verification

- Single commit 10d8fc4, 14 files, +2/-299; scope matches the task exactly.
- `.chezmoiremove` gains `.local/bin/common/start-cognee-mcp` (existing
  style), `cognee:` data gate removed from `.chezmoi.yaml.tmpl`, generated
  codex/claude MCP configs regenerated without cognee, guard trigger list and
  its test updated.
- Repo-wide case-insensitive sweep clean except the intentional retirement
  entry; validator ok; generator idempotent; `test_require_crit_review.py`
  25 passed (orchestrator re-ran all of these on the branch worktree).
- Worker used a scratch worktree (/private/tmp/dotfiles-t41) instead of
  branch-switching the shared tree — accepted as an improvement; orchestrator
  cleans up scratch worktrees after merge.

next_action: orchestrator pushes, opens the PR, merges on green, prunes
scratch worktrees.
