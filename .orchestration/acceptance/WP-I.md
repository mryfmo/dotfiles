# WP-I Acceptance
task_id: WP-I
status: accepted
reviewed_by: orchestrator-fable5
evidence: reports/WP-I.md, validation/WP-I.txt, independent checks — chezmoi diff ~/.codex/config.toml EMPTY, settings pin fable-5[1m]/high (reorder-only diff), validator ok, 51 unit tests pass, modify script executable, baseline TOML parses
notes: Structural fix for runtime-state clobbering; runtime-owned tables (hooks.state/marketplaces/model_availability_nux/projects) preserved by modify_ merge.
