# T19 Herdr file-viewer popup config report

- Status: ready for review
- Worktree: `/Users/mryfmo/Workspace/dotfiles-t18`
- Branch: `feat/herdr-file-viewer-popup`
- Commit: `968637c feat: add herdr file viewer popup`
- Parent T18 task: accepted

## Result

- Added `prefix+f` as a 90% × 90% session-modal popup that resolves and executes the installed `herdr-file-viewer` plugin.
- Passes the plugin config directory through `HERDR_PLUGIN_CONFIG_DIR`.
- Added plugin config selecting `micro` as the editor.
- Added TOML-backed tests for the popup binding and plugin editor config.

## Review

- Local Crit data review completed without actionable findings.
- `make require-crit-review` passed with repo-local Crit JSON evidence.
