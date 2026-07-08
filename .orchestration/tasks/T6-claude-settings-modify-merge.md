# T6: Manage ~/.claude/settings.json via chezmoi modify\_ merge (RR-9 class fix)

task_id: T6
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-gpt55-high

## Background (why)

`make update` (chezmoi apply) stops on an interactive "has changed since
chezmoi last wrote it" prompt for `~/.claude/settings.json` (non-TTY: Error 1).
Claude Code itself rewrites the deployed file (currently the only semantic
drift is `enabledPlugins`: source `{}` vs deployed
`{"crit@crit": true, "ponytail@ponytail": true}`; the other ~147 diff lines
are key-ordering/trailing-newline churn from Claude Code's own formatter).
A plain-file source either wipes runtime plugin enables or blocks apply.
PR #62 already solved the same class for Codex with
`home/dot_codex/modify_private_config.toml` + `.chezmoitemplates/codex-config-managed.toml`.
Apply the same pattern to Claude settings.

## Goal

1. **New** `home/.chezmoitemplates/claude-settings-managed.json` — the managed
   baseline, content taken from the current `home/dot_claude/private_settings.json`.
   Follow the codex template precedent for `{{ .chezmoi.homeDir }}`
   placeholders (the SessionStart hook command contains an absolute home
   path). Keep `make validate-agent-assets` green — it currently reads
   `home/dot_claude/private_settings.json` (lines ~179 and ~496 of
   scripts/validate-agent-assets.py) and must be pointed at the new baseline.
2. **New** `home/dot_claude/modify_private_settings.json` — python3 merge
   script, same structure as `home/dot_codex/modify_private_config.toml`
   (CHEZMOI_SOURCE_DIR / CHEZMOI_HOME_DIR handling, render of the managed
   template, stdin = current target, stdout = merged). Merge policy (JSON,
   so use json — much simpler than the TOML chunker):
   - RUNTIME_KEYS = ("enabledPlugins",): always taken from current target
     when present (fallback to managed when current is empty/missing/invalid).
   - All other managed keys: managed value wins (deep-replace at top level;
     no partial merge inside managed values).
   - Keys present only in current target: preserved (future Claude-runtime
     keys survive).
   - **Ordering stability**: build the result starting from the CURRENT
     file's key order (dict insertion order), overwriting values; append
     managed-only keys at the end in managed order. Output
     `json.dumps(merged, indent=2) + "\n"`. Rationale: Claude Code rewrites
     the file in its own order; if the merge output preserves current order
     when values match, steady-state `chezmoi diff` is empty and apply stops
     churning.
   - Empty or whitespace-only stdin → output rendered managed baseline.
   - Invalid JSON on stdin → output rendered managed baseline (fail-safe,
     do not crash apply); note this behavior in the script docstring.
3. **Delete** `home/dot_claude/private_settings.json` (replaced by 1+2).
4. **Update every reference** to the old source path:
   - scripts/check-agent-runtime.py (~line 137 mapping)
   - scripts/validate-agent-assets.py (~lines 179, 496-500)
   - tests/unit/test_generate_agent_configs.py (`settings_path`)
   - tests/install/common/lifecycle.bats (grep for `ccgate claude`)
   - README/docs mentions if any (`grep -rn private_settings.json`)
5. **New unit test** `tests/unit/test_claude_settings_merge.py` modeled on
   `tests/unit/test_codex_config_merge.py`. Cover at least: managed-wins for
   a managed key; `enabledPlugins` preserved from current; current-only key
   preserved; empty stdin → managed; invalid JSON stdin → managed;
   idempotence (merge(merge(x)) == merge(x)); when current already equals
   desired, output == current (ordering stability); trailing newline.

## Allowed files (edit boundary)

- home/.chezmoitemplates/claude-settings-managed.json (new)
- home/dot_claude/modify_private_settings.json (new)
- home/dot_claude/private_settings.json (delete)
- scripts/check-agent-runtime.py, scripts/validate-agent-assets.py (reference updates only)
- tests/unit/test_claude_settings_merge.py (new), tests/unit/test_generate_agent_configs.py, tests/unit/test_validate_agent_assets.py (only if its fixtures reference the old path), tests/install/common/lifecycle.bats (path fix only)
- README.md / docs only if they reference the old path (minimal diff)
- home/dot_agents/agent-config.yaml (`claude.settings_path` reference update only) — scope expansion granted 2026-07-08 after blocked report
- home/dot_agents/README.md (old-path reference update only) — scope expansion granted 2026-07-08 after blocked report
- plus your artifact paths under .orchestration/

## Forbidden actions

git commit; git push; chezmoi apply; make update/upgrade; make require-crit-review; dependency changes; editing ~/.claude/_ or ~/.config/_ directly (repo sources only; READING ~/.claude/settings.json is allowed for merge simulation); running bats locally (repo policy — CI runs it); herdr pane/workspace/agent operations.

## Validation (record outputs in the validation artifact)

1. `uv run python -m unittest discover -s tests/unit -v` → all green including the new merge tests
2. `make validate-agent-assets` (or its script directly) → ok with the new baseline path
3. Merge simulation against the real deployed file: `python3 home/dot_claude/modify_private_settings.json < ~/.claude/settings.json` (with CHEZMOI_SOURCE_DIR=$PWD/home CHEZMOI_HOME_DIR=$HOME) → show that output preserves `enabledPlugins` {crit,ponytail}, enforces managed keys, and that piping the OUTPUT back through the script is byte-identical (idempotence)
4. `python3 -m py_compile` on both new/changed python files
5. `git status --porcelain` → only expected changes

## Expected artifacts

- report: .orchestration/reports/T6.md
- validation: .orchestration/validation/T6.txt
- sandbox: .orchestration/sandboxes/T6.md
- learning: .orchestration/learning/T6.md
- autoskill: .orchestration/autoskill/runs/T6.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT v1 task_id=T6 status=ready_for_review report=.orchestration/reports/T6.md validation=.orchestration/validation/T6.txt sandbox=.orchestration/sandboxes/T6.md learning=.orchestration/learning/T6.md autoskill=.orchestration/autoskill/runs/T6.md"
```

max_turns: 25
