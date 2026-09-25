# Acceptance: dot-validator-worktrees-T7-a01

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

- Fix: cached `is_nested_git_tree(directory)` ancestor check applied in both rglob scans; existing part-name skips retained.
- Real reproduction by orchestrator: unpatched validator on main → "possible committed secret in .claude/worktrees/adh-baseline/..."; patched → "agent asset validation ok".
- Unit case red-first for both scans, .git as file and directory; top-level hits still reported. `make unit-test` OK, diff check OK.
- Committed and opened as a PR.
