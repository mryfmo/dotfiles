# WP-I Report

Status: ready_for_review

## Summary

- Pinned Claude settings in `home/dot_agents/agent-config.yaml` to `claude-fable-5[1m]` with `effortLevel: high`, regenerated `home/dot_claude/private_settings.json`, and taught the generator/validator to enforce the pin.
- Replaced full-file Codex config management with a generated non-deployed baseline at `home/.chezmoitemplates/codex-config-managed.toml` plus executable modify script `home/dot_codex/modify_private_config.toml`.
- The modify script preserves runtime-owned Codex tables for `hooks.state`, `marketplaces`, `tui.model_availability_nux`, and `projects`, while enforcing managed model, sandbox, shell policy, MCP, feature, plugin, and hook baseline sections.
- Updated `scripts/validate-agent-assets.py`, `scripts/check-agent-runtime.py`, unit tests, install lifecycle path checks, and `home/dot_agents/README.md`.

## Files Touched

- `home/dot_agents/agent-config.yaml`
- `home/dot_agents/README.md`
- `home/dot_claude/private_settings.json`
- `home/.chezmoitemplates/codex-config-managed.toml`
- `home/dot_codex/modify_private_config.toml`
- removed `home/dot_codex/private_config.toml.tmpl`
- `scripts/generate-agent-configs.py`
- `scripts/validate-agent-assets.py`
- `scripts/check-agent-runtime.py`
- `tests/unit/test_codex_config_merge.py`
- `tests/unit/test_generate_agent_configs.py`
- `tests/unit/test_validate_agent_assets.py`
- `tests/install/common/lifecycle.bats`

## Notes

- `chezmoi diff ~/.codex/config.toml` is empty after the modify-script fix.
- `chezmoi diff ~/.claude/settings.json` still shows unrelated live-file ordering/plugin-state differences, but the generated target pins `model = claude-fable-5[1m]` and `effortLevel = high`; it no longer downgrades the model.
- No forbidden actions were performed: no commit, no push, no `chezmoi apply`, no bats, no dependency changes, and no `make require-crit-review`.
