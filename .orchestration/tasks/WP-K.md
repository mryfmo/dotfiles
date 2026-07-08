# WP-K: Pin the herdr agents layout — Claude orchestrator top, Codex worker bottom

task_id: WP-K
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpk

## Goal

`home/dot_local/bin/common/executable_herdr-agents` already creates a stacked workspace (Claude Code top / Codex bottom, bound to prefix+alt+a via herdr config). Harden it so the layout and models are FIXED regardless of local settings drift:

- Top pane: Claude Code as ORCHESTRATOR — explicitly `claude --model 'claude-fable-5[1m]'` (verify the exact flag with `claude --help`; if a shorter alias like `fable-5` is accepted, prefer the explicit full id). Effort comes from settings (pinned high by WP-I); if `claude` exposes a CLI flag for effort, add it explicitly too.
- Bottom pane: Codex as AUTONOMOUS WORKER — explicitly `codex --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=high` (verify flags with `codex --help`; keep existing CLICOLOR/FORCE_COLOR env).
- Label the panes so roles are visible in herdr: use `herdr pane rename <pane_id> <label>` (labels: `claude-orchestrator`, `codex-worker`) and keep the codex agent name stable (`codex-worker` instead of `codex-${workspace_id}` — check `herdr agent start` name uniqueness constraints across workspaces; if a fixed name collides when two workspaces exist, fall back to `codex-worker-${workspace_id}` and say so in the report).
- Keep zed launch behavior and shdoc comments; script must pass `shfmt --indent 4 --space-redirects --diff`.
- Update the keybinding description in `home/dot_config/herdr/config.toml` only if it no longer matches ("open Claude Code and Codex workspace" is still accurate — change only if you rename the script or semantics).

## Allowed files (edit boundary)

home/dot_local/bin/common/executable_herdr-agents, home/dot_config/herdr/config.toml (description only, if needed), plus your artifact paths.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; dependency changes; starting/killing herdr workspaces of the orchestrator session (you may run `herdr --help` / `claude --help` / `codex --help` read-only to verify flags; do NOT launch new agents to test).

## Validation

1. `bash -n home/dot_local/bin/common/executable_herdr-agents` → ok
2. `shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents` → clean
3. Show `--help` excerpts proving the exact claude/codex flags used exist
4. `git status --porcelain` → only expected changes

## Expected artifacts

- report: .orchestration/reports/WP-K.md
- validation: .orchestration/validation/WP-K.txt
- sandbox: .orchestration/sandboxes/WP-K.md
- learning: .orchestration/learning/WP-K.md
- autoskill: .orchestration/autoskill/runs/WP-K.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpk orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-K status=ready_for_review report=.orchestration/reports/WP-K.md validation=.orchestration/validation/WP-K.txt sandbox=.orchestration/sandboxes/WP-K.md learning=.orchestration/learning/WP-K.md autoskill=.orchestration/autoskill/runs/WP-K.md"
```

max_turns: 25
