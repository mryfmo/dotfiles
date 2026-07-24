# T15 Herdr lazy-start and attach-layout report

## Status

Ready for orchestrator review. No commit or push was performed.

## Implementation

- `herdr-session` now validates its empty argument contract and directly `exec`s `herdr`, so bare Herdr startup opens one plain terminal.
- `herdr-agents --attach` exits immediately outside Herdr, before dependency checks or command calls.
- Inside Herdr, attach mode treats `HERDR_PANE_ID` as the already-starting Claude pane, renames it `claude-orchestrator`, creates or repairs the Yazi files pane from that pane at ratio `0.8`, then reuses or starts `codex-worker-${HERDR_WORKSPACE_ID}`.
- Attach mode does not start Claude, create/focus a workspace, or open Zed. A complete Claude/Codex/Yazi workspace is mutation-free on rerun.
- The existing full-mode path and `prefix+alt+a` invocation remain available; shared files-pane repair logic was extracted without changing full-mode ratios.
- The Claude settings modifier appends an official `SessionStart` hook to the existing managed `SessionStart` list. The hook logs to `$HOME/.config/herdr/herdr-agents.log` and ends with `|| true`.

## Settings surface

The allowed `home/dot_claude/modify_private_settings.json` modifier is the exact edited surface. It reads the repository's managed Claude baseline and adds the hook only when that baseline exposes a `hooks.SessionStart` list, preserving the modifier's generic merge behavior for baselines without hooks.

## Scope

Implementation and tests changed only:

- `home/dot_local/bin/common/executable_herdr-session`
- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_claude/modify_private_settings.json`
- `tests/unit/test_herdr_agents.py`

The five required T15 orchestration artifacts are the only additional task files.
