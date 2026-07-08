# WP-K Learning

## Reusable Learning

- `claude --help` exposes both `--model <model>` and `--effort <level>`, so Herdr-launched Claude panes can pin both model and effort explicitly instead of relying only on settings.
- `codex --help` exposes `--sandbox`, `-m/--model`, and `-c/--config`, so Herdr-launched Codex worker panes can pin sandbox, model, and reasoning effort without reading local Codex config.
- Herdr pane labels can be set with `herdr pane rename <pane_id> <label>`. For Codex agent panes, capture the pane id from `herdr agent start` output and fall back to `herdr agent get <agent>`.

## Applied To

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`

## Promotion

No reusable rule candidate was promoted by this worker. The learning is captured here for orchestrator review only.
