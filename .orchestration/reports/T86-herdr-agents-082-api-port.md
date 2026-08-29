# T86 Report — herdr-agents 0.8.2 API port

status: ready_for_review
branch: `fix/herdr-agents-herdr-082-api`
commit: `abc32b1 fix(herdr): port agent launcher to pane API`
pull_request: [#147](https://github.com/mryfmo/dotfiles/pull/147)
ci: green
cost: n/a

## Result

- Replaced removed `agent start --cwd/--workspace/--split/--env/--no-focus` usage with pane creation/reuse, JSON pane-id capture, and `agent start --kind --pane` for Claude and Codex.
- Guarded every newly created target pane with both foreground-shell inspection and a visible-prompt wait. A timed-out start gets one bounded retry; `agent_not_ready` waits for the already registered agent rather than duplicating it.
- Lowercased derived agent names and rejected values outside `^[a-z][a-z0-9_-]{0,31}$`.
- Resolved the Codex profile as environment override, generated `MODEL_PROFILE_INTERACTIVE`, then `standard` fallback.
- Canonicalized workdirs with `pwd -P`, propagated a caller-provided `FPATH`, and retained safe existing-pane repair behavior.
- Updated the fake herdr CLI and regression coverage. Zsh wrapper tests now use their isolated HOME so a developer's mise activation cannot replace the fake PATH.

## Scope

Only these files were committed:

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`

Unrelated changes in `home/dot_agents/skills/agmsg/templates/cmd.claude-code.md` and `home/dot_mise/*` were preserved and never staged.

## Review

The final Crit data review has a resolved review-scope approval record. Evidence: `.agents/worklog/codex/review/20260829_135518_t86_crit.json`; receipt: `.agents/worklog/codex/review/20260829_135518_t86_receipt.md`.

## CompactionDB decisions

Commands executed exactly:

```bash
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'herdr-agents targets the herdr 0.8.2 agent API: pane split (JSON id capture) + shell-readiness wait + agent start --kind --pane; agent names are lowercased and validated against ^[a-z][a-z0-9_-]{0,31}$.'
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'The Codex worker pane profile default is resolved from MODEL_PROFILE_INTERACTIVE in ~/.agents/model-profiles.env (env override HERDR_AGENTS_CODEX_PROFILE wins; standard is the last-resort fallback), keeping model selection single-sourced in agent-config.yaml.'
```

Created memory ids `1d11001e-e5c6-42d0-a5ac-72f930ceb2c2` and `ada64692-886b-445f-8c50-42307b0d9d28`.
