# WP-I: Stop chezmoi apply from clobbering agent runtime state; pin fable-5 high

task_id: WP-I
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpi

## Problem (measured)

1. `home/dot_claude/private_settings.json` (generated from agent-config.yaml) pins `"model": "opusplan"`. The user's standard is Claude Fable 5 with high effort; every `chezmoi apply` reverts their choice. Live file today has `"model": "claude-fable-5[1m]"` and `"effortLevel": "high"` — that is the DESIRED pinned state.
2. `~/.codex/config.toml` is fully managed (source `home/dot_codex/private_config.toml.tmpl`, generated). Codex itself writes runtime state into that file: `[hooks.state."..."]` trusted hashes, `[marketplaces.*]` last_updated/last_revision, `[tui.model_availability_nux]`, `[projects."..."]` trust. Every apply reverts these → hook-trust dialogs reappear, marketplace/plugin state is lost. Verified via `chezmoi diff ~/.codex/config.toml`.

## Part 1 — settings.json pins (simple)

EDIT home/dot_agents/agent-config.yaml: in the claude settings section change model pin `opusplan` → `claude-fable-5[1m]` and add/ensure `effortLevel: high` is emitted into the generated settings. Regenerate. Verify the generated `home/dot_claude/private_settings.json` now contains `"model": "claude-fable-5[1m]"` and `"effortLevel": "high"` while keeping everything else (defaultMode plan, plansDirectory, permissions, hooks) unchanged.

## Part 2 — codex config.toml modify\_ merge (structural)

Convert `~/.codex/config.toml` from full-file management to a chezmoi `modify_` script so managed keys stay enforced while codex-owned runtime state survives apply.

Design (adjust only if chezmoi docs force you to):

- Generator no longer emits `home/dot_codex/private_config.toml.tmpl` as the deployed file. Instead it emits the managed baseline to a NON-deployed source location (e.g. `home/.chezmoitemplates/codex-config-managed.toml`; anything under .chezmoitemplates is not applied).
- Add an executable chezmoi modify script in `home/dot_codex/` targeting `.codex/config.toml` (check chezmoi docs for exact attribute naming/order for a private modify script, e.g. `modify_private_config.toml`; scripts get current target contents on stdin, must print new contents on stdout, and can locate the source dir via `CHEZMOI_SOURCE_DIR`).
- Merge rules (top-level TOML table chunk granularity):
  - RUNTIME-OWNED table prefixes: `hooks.state`, `marketplaces`, `tui.model_availability_nux`, `projects` → take from current target (stdin) when present; seed from managed baseline when absent.
  - All other tables/keys present in the managed baseline → managed baseline wins.
  - Tables present only in the current target (user/codex additions not in baseline and not runtime-owned) → preserve.
  - Empty/missing stdin (fresh machine) → output equals managed baseline.
- Implementation: bash or python3 (stdlib only — tomllib is read-only, so a line/section-chunk approach is acceptable; python3 available on both OSes via mise/system). Follow repo shdoc conventions if bash; must pass `shfmt --indent 4 --space-redirects`.
- Keep TOML valid: validate output parses with `python3 -c "import tomllib,sys; tomllib.load(open(...,'rb'))"` inside your tests, not at apply time.

Update the toolchain consistently:

- scripts/generate-agent-configs.py: output path change for the codex baseline; keep content generation identical otherwise.
- scripts/validate-agent-assets.py: freshness/parity checks must point at the new baseline path; add a check that the modify script exists and is executable.
- scripts/check-agent-runtime.py: source→target mapping for codex config must reflect the new mechanism.
- tests/unit/: update existing generator/validator tests; ADD unit tests for the merge logic (managed-wins, runtime-preserved, seed-when-absent, fresh-machine, unknown-table-preserved).
- Any bats tests referencing dot_codex/private_config.toml.tmpl (grep tests/) — update paths.
- home/dot*agents/README.md: document the modify* merge and the runtime-owned key list.

## Allowed files (edit boundary)

home/dot_agents/agent-config.yaml, home/dot_agents/README.md, home/dot_codex/** (incl. new modify script), home/.chezmoitemplates/** (new baseline output), home/dot_claude/private_settings.json (regenerated only), scripts/generate-agent-configs.py, scripts/validate-agent-assets.py, scripts/check-agent-runtime.py, tests/unit/**, tests/install/** (only refs to moved codex config paths), plus your artifact paths.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; dependency changes; make require-crit-review (orchestrator's job); editing ghostty/herdr files (WP-J/WP-K own those).

## Validation (run and capture output)

1. `uv run --with pyyaml scripts/generate-agent-configs.py` (or the repo's wrapper) then `git status --porcelain` → only expected files
2. `uv run --with pyyaml scripts/validate-agent-assets.py` → pass
3. `make unit-test` → pass including your new merge tests
4. Simulated merge: feed the CURRENT live `~/.codex/config.toml` (read-only) into the modify script on stdin; show that output preserves the live `hooks.state` hashes and `model_availability_nux`, while managed keys (model, sandbox, mcp_servers) come from the baseline
5. `chezmoi diff ~/.codex/config.toml` → the diff should now show NO reverts of hooks.state/marketplaces/model_availability_nux/projects (managed-key diffs only, ideally empty)
6. `chezmoi diff ~/.claude/settings.json` → shows model/effort pins now matching fable-5 high (i.e. no model clobber relative to live)

## Expected artifacts

- report: .orchestration/reports/WP-I.md
- validation: .orchestration/validation/WP-I.txt
- sandbox: .orchestration/sandboxes/WP-I.md
- learning: .orchestration/learning/WP-I.md
- autoskill: .orchestration/autoskill/runs/WP-I.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpi orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-I status=ready_for_review report=.orchestration/reports/WP-I.md validation=.orchestration/validation/WP-I.txt sandbox=.orchestration/sandboxes/WP-I.md learning=.orchestration/learning/WP-I.md autoskill=.orchestration/autoskill/runs/WP-I.md"
```

max_turns: 60
