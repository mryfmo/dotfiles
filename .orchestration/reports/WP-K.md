# WP-K Report

Status: ready_for_review

## Summary

- Updated `home/dot_local/bin/common/executable_herdr-agents` so the top pane is renamed `claude-orchestrator` and runs:
  - `CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high`
- Updated the bottom worker launch so Herdr starts Codex with the pinned autonomous-worker command:
  - `codex --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=high`
- Added bottom-pane rename to `codex-worker` after resolving the Codex pane id from `herdr agent start` JSON, falling back to `herdr agent get`.
- Kept the Herdr agent registration collision-safe as `codex-worker-${workspace_id}` rather than fixed `codex-worker`. Prior validated repo learning showed Herdr agent names must be unique across active workspaces, and `herdr agent --help` says targets include unique agent names.
- Updated `tests/unit/test_herdr_agents.py` to verify the pinned Claude/Codex commands and pane rename calls. The file also contains the accepted WP-J Ghostty path update in the shared worktree.

## Notes

- `home/dot_config/herdr/config.toml` was not changed; the existing keybinding description still matches the behavior.
- No agents or workspaces were launched for validation. Only `--help` commands were used for CLI flag verification.
- Forbidden actions were not performed: no commit, no push, no `chezmoi apply`, no bats, no dependency changes, and no orchestrator Herdr workspace start/kill.
