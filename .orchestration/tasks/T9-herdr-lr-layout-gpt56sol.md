# T9: herdr agents layout left/right + codex gpt-5.6-sol, drop Ghostty auto-start

task_id: T9
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-gpt55-high

## Background (why)

User decision (2026-07-10): Ghostty must NOT auto-start Herdr anymore, and
quitting Herdr (ctrl-b+q) must return to the zsh prompt instead of closing the
Ghostty surface. The managed layout should start only when the user runs bare
`herdr` inside Ghostty (the `herdr()` zsh function in `home/dot_zshrc` already
provides this path and needs no change; `herdr-session` runs as a child of the
interactive zsh, so exiting Herdr naturally returns to the prompt).
Layout change: Claude Code (orchestrator, `claude-fable-5[1m]` effort high) on
the LEFT, Codex (autonomous worker, `gpt-5.6-sol` reasoning high, agmsg
collaboration) on the RIGHT — currently they are stacked (Claude above Codex).
Also, live `~/.codex/config.toml` already uses `gpt-5.6-sol` but the chezmoi
source of truth still says `gpt-5.5`, so the next `chezmoi apply` would roll
the default model back; the user confirmed the managed default must move to
`gpt-5.6-sol` too.

Approved plan (reference, read-only):
/Users/mryfmo/.agents/worklog/claude/dotfiles-ghostty-herdr-herdr-claude-code-stateless-wand.md

## Goal

1. `home/dot_config/ghostty/config`: delete the trailing block
   `# Start first Ghostty surface through the Herdr session entrypoint.` +
   `initial-command = /bin/zsh -lc 'exec herdr-session'`. Nothing else.
2. `home/dot_local/bin/common/executable_herdr-agents`:
   - `start_codex_agent()`: `--split down` → `--split right`, and
     `-m gpt-5.5` → `-m gpt-5.6-sol` (keep `model_reasoning_effort=high`).
   - Existing-workspace repair path:
     `herdr pane split "${codex_pane_id}" --direction down` → `--direction right`;
     `herdr pane swap --pane "${claude_pane_id}" --direction up` → `--direction left`.
   - Update shdoc comments/usage text ("above Codex", "stacked panes") to
     left/right wording. English, shdoc format preserved.
   - CLI support confirmed by orchestrator: `herdr pane split ... --direction right|down`,
     `herdr pane swap --direction left|right|up|down`, `herdr agent start ... --split right|down`.
3. `home/dot_agents/agent-config.yaml`: `codex.model: gpt-5.5` → `gpt-5.6-sol`;
   `tui.model_availability_nux` key `gpt-5.5: 2` → `gpt-5.6-sol: 2`.
4. Regenerate the managed template (do NOT hand-edit it):
   `uv run --with pyyaml python scripts/generate-agent-configs.py`
   → updates `home/.chezmoitemplates/codex-config-managed.toml` (and possibly
   other generated adapters; keep whatever the generator produces).
5. `tests/unit/test_herdr_agents.py`: update expected call strings
   (`--split down`→`--split right`, `pane split ... --direction down`→`right`,
   `swap ... --direction up`→`left`, `gpt-5.5`→`gpt-5.6-sol`, e2e assertion
   `split=down`→`split=right`) and rename tests/docstrings using "below"
   vocabulary to left/right wording.
6. `README.md` "Herdr and Ghostty agent workspace" section (~line 197):
   remove the "Ghostty starts its first surface with herdr-session" claim;
   describe instead that bare `herdr` inside Ghostty starts the managed layout
   via herdr-session (Claude left = orchestrator, Codex right = worker), and
   that exiting Herdr returns to the shell. English, minimal diff.

Do NOT change: `home/dot_zshrc` herdr()/`executable_herdr-session`, the zed
auto-open in herdr-agents, gpt-5.5 prose mentions in
`home/dot_codex/ccgate.jsonnet` and `home/dot_config/codex/AGENTS.md`
(illustrative guidance, not config values).

## Allowed files (edit boundary)

- home/dot_config/ghostty/config
- home/dot_local/bin/common/executable_herdr-agents
- home/dot_agents/agent-config.yaml
- home/.chezmoitemplates/codex-config-managed.toml (via generator only)
- any other file the generator regenerates (report them)
- tests/unit/test_herdr_agents.py
- README.md (Herdr/Ghostty section only)
- plus your artifact paths under .orchestration/

## Forbidden actions

git commit; git push; chezmoi apply; make update/upgrade; make require-crit-review; editing deployed files under ~ (repo sources only); local bats; herdr pane/workspace/agent operations; restarting Ghostty; dependency changes.

## Validation (record outputs in the validation artifact)

1. `bash -n home/dot_local/bin/common/executable_herdr-agents` → ok
2. `uv run --with pyyaml python scripts/generate-agent-configs.py` → rerun a
   second time and show `git status --porcelain` is stable (idempotent).
3. `uv run python -m unittest discover -s tests/unit -v` → green
4. `grep -n 'initial-command' home/dot_config/ghostty/config` → no matches
5. `grep -n 'gpt-5.5' home/dot_local/bin/common/executable_herdr-agents home/dot_agents/agent-config.yaml home/.chezmoitemplates/codex-config-managed.toml tests/unit/test_herdr_agents.py` → no matches
6. `git status --porcelain` + `git diff --stat` → only expected changes

## Expected artifacts

- report: .orchestration/reports/T9.md
- validation: .orchestration/validation/T9.txt
- sandbox: .orchestration/sandboxes/T9.md
- learning: .orchestration/learning/T9.md
- autoskill: .orchestration/autoskill/runs/T9.md (record "not-used" if unused)

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT v1 task_id=T9 status=ready_for_review report=.orchestration/reports/T9.md validation=.orchestration/validation/T9.txt sandbox=.orchestration/sandboxes/T9.md learning=.orchestration/learning/T9.md autoskill=.orchestration/autoskill/runs/T9.md"
```

max_turns: 25
