# T26 report: PR #86 Herdr rebase

- Status: ready for review
- PR: https://github.com/mryfmo/dotfiles/pull/86
- Head: `b098ddeb6e1cee836d879621d7fe64aef14e1d14`
- Base: `origin/main` at `4e761ba947069fd31fe718432504a71f571f6092`

## Result

- Removed the clean stale dead-session worktree and created a fresh worktree
  from `origin/main`.
- Rebased the existing two PR commits without adding commits or dependencies.
- Resolved both conflicts by retaining main's manifest-driven Codex
  `--profile` launch, two-pane repair, and file-viewer behavior while applying
  the PR's absolute Codex path and guarded node-global cleanup.
- Force-pushed with a lease pinned to old head `06f9beb`.
- Refreshed the existing PR description to match the complete rebased diff.
- GitHub Actions and CodeRabbit pass; GitHub reports the PR `CLEAN`.
- Did not merge.

## Scope

The PR still changes only:

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`

