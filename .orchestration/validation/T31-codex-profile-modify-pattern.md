# T31 validation

Worktree: `/Users/mryfmo/Workspace/dotfiles-t31`

```text
$ uv run --with pytest pytest tests/unit/test_generate_agent_configs.py tests/unit/test_check_agent_runtime.py
============================= test session starts ==============================
platform darwin -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/mryfmo/Workspace/dotfiles-t31
collected 34 items

tests/unit/test_generate_agent_configs.py .............                  [ 38%]
tests/unit/test_check_agent_runtime.py ............                      [ 73%]
tests/unit/test_codex_config_merge.py .........                          [100%]

============================== 34 passed in 0.55s ==============================

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ uv run --with pyyaml python scripts/generate-agent-configs.py --check
generated agent configs are up to date

$ printf '<runtime profile with [hooks.state]>' | CHEZMOI_SOURCE_DIR=<fixture> CHEZMOI_HOME_DIR=<fixture> home/dot_codex/modify_standard.config.toml
# Codex model profile "standard"; launch with: codex --profile standard
# Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py.

model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
[hooks.state]
trusted = true

$ git status --short
(no output; clean after commit)
```

`uv run pytest ...` could not locate a pytest executable in this worktree, so the equivalent ephemeral `uv run --with pytest pytest ...` command above was used without modifying dependencies. `scripts/update-agent-assets.sh` was not changed, so shellcheck and shfmt do not apply. Local Bats was intentionally not run.

The new byte-idempotency test feeds a managed standard profile plus a blank line and `[hooks.state]` to `modify_standard.config.toml`, then asserts byte-for-byte unchanged output.

The repeated-table regressions cover two `[[hooks.state.sub]]` occurrences for both generated profile modifiers and `modify_private_config.toml`; all occurrences survive in stable order. Read-only idempotency checks also passed for the four deployed profiles and the deployed base config (with `CHEZMOI_SOURCE_DIR` set to its canonical `home/` source root).
