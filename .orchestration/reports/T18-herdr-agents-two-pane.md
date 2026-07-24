# T18 herdr-agents two-pane report

- Status: ready for review
- Worktree: `/Users/mryfmo/Workspace/dotfiles-t18`
- Branch: `feat/herdr-file-viewer-popup`
- Commit: `b9b5eab feat: use two-pane herdr agent layout`
- Changed files:
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `tests/unit/test_herdr_agents.py`

## Result

- Removed automatic files/Yazi pane creation, inspection, restart, and repair.
- New workspaces start Claude in the root pane and Codex with the existing `--split right` default ratio.
- Attach and existing-workspace repair accept only the two managed panes, repair order with at most one swap, and repair 50/50 geometry with one resize attempt plus convergence verification.
- Legacy `files` panes remain unmanaged: attach refuses mutation after the Claude label repair, and full mode never reuses, closes, or splits them.
- Updated the fake CLI harness and two-pane/legacy/unsafe/non-convergence tests first; retained the unrelated Yazi config test.
- Repository shfmt flags (`--indent 4 --space-redirects`) preserve the established four-space convention for the extensionless shell executable; the initial whole-file tab reformat was removed in the revision.

## Review

- Local Crit data review completed without actionable findings.
- Revision review confirmed the amend against `49cdd5f` was whitespace-only and restored repository formatting.
- `make require-crit-review` passed with `AGENT_REVIEWED=1` and repo-local Crit JSON evidence in the isolated worktree.
