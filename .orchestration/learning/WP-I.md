# WP-I Learning

## Reusable Learning

- Chezmoi `modify_` scripts receive the current target content on stdin and must write the full desired target on stdout. For a generated baseline under `.chezmoitemplates`, the modify script must render any source/home placeholders it depends on before merging, because it is reading the baseline file directly rather than having chezmoi template it as a target.
- Runtime-owned TOML table merging should operate by runtime prefix group, not only exact table name, to preserve current-file ordering for current-only runtime descendants such as additional `hooks.state.*` entries.

## Applied To

- `home/dot_codex/modify_private_config.toml`
- `tests/unit/test_codex_config_merge.py`
- `scripts/check-agent-runtime.py`

## Promotion

No reusable rule candidate was promoted by this worker. The learning is captured here for orchestrator review only.
