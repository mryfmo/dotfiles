# WP-J Report

Status: ready_for_review

## Summary

- Added `home/dot_config/ghostty/config` from the current live `~/.config/ghostty/config` as the managed Ghostty source.
- Preserved the live baseline exactly, including Japanese comments, and appended a managed extras section with:
  - `window-padding-x = 8`
  - `window-padding-y = 4`
  - `confirm-close-surface = true`
  - `shell-integration = detect`
- Deleted inert `home/dot_config/ghostty/config.ghostty.tmpl`.
- Fixed all `config.ghostty` references found by grep in:
  - `README.md`
  - `install/macos/common/defaults.sh`
  - `tests/files/macos.bats`
  - `tests/unit/test_herdr_agents.py`

## Notes

- No live `$HOME` files were edited.
- No cross-owned `config.ghostty` references remained to report; every grep finding was a direct stale Ghostty path reference and was fixed.
- Full `git status --porcelain` still includes accepted WP-I changes in the shared worktree. WP-J-specific status is limited to the Ghostty config path swap and the four reference fixes.
- Forbidden actions were not performed: no commit, no push, no `chezmoi apply`, no bats, and no dependency changes.
