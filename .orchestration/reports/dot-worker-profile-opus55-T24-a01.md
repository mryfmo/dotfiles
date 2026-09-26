# Report: dot-worker-profile-opus55-T24-a01

- Worker: claude-standard-dot-a005
- task_rev verified: sha256 of the task file at `a94189f` = `f76016a0fa984bbc9ceaa2b00e1239f08dfd19719aa188d9aa421ebd7dca7c94` (matches); `a94189f` == origin/main. No drift in target files between `8332803` and origin/main.
- Worktree: `.claude/worktrees/worker-c`
- **Step 0:** T21 WIP committed as-is (12 modified + 3 untracked files) on `wip/orchestrator-guardrails-T21` as `c687edb` and pushed to origin. Not reviewed/fixed/extended.
- **Branch:** `feat/worker-profile-opus55` from origin/main `a94189f`, commit `fc71726` (`fc717266cb16042cd282f485517f92fd8277391b`).
- **PR:** https://github.com/mryfmo/dotfiles/pull/185 — not merged. CI all green on head `fc71726` (12 pass, `nix` skipping; verbatim in validation file).
- Evidence: `.orchestration/validation/dot-worker-profile-opus55-T24-a01.md`

[memory:decision] T24: herdr worker profile = standard (claude-opus-5-5 high) via manifest worker_profile; worker_kind stays claude (operator 2026-09-27). CompactionDB id `41b8c762-890e-4584-a308-3a5fe1b237ca`.

## Changes

1. `home/dot_agents/agent-config.yaml`: `standard.claude` → `claude-opus-5-5`/high; `review.claude` → `claude-fable-5`/medium; `worker_profile: standard` (+3-line comment) directly after `worker_kind: claude` (nothing inserted between `adh:` and `interactive_profile:`).
2. `scripts/generate-agent-configs.py`: `worker_profile(manifest)` after `worker_kind()` — returns `manifest.get("worker_profile")`, `fail()` if set and not a `model_profiles` key, None when absent. `render_model_profiles_env()` appends `HERDR_AGENTS_WORKER_PROFILE="<v>"` right after `HERDR_AGENTS_WORKER_KIND` only when set.
3. `executable_herdr-agents` `resolve_worker_profile()`: explicit env `HERDR_AGENTS_WORKER_PROFILE` > `HERDR_AGENTS_CODEX_PROFILE` (early returns unchanged), then local-shadowed `HERDR_AGENTS_WORKER_PROFILE`/`MODEL_PROFILE_INTERACTIVE`/`HERDR_AGENTS_WORKER_KIND`, source env file, print `${HERDR_AGENTS_WORKER_PROFILE:-${MODEL_PROFILE_INTERACTIVE:-standard}}`. Header `@arg` and function `@description` updated. `start_worker_agent()` untouched. (Shadowing `HERDR_AGENTS_WORKER_KIND` too keeps the sourced file from leaking into the caller's scope; the function is called in `$(...)` today, so this is defensive only.)
4. `scripts/validate-agent-assets.py` `validate_agent_manifest()`: after the worker_kind checks, a present `worker_profile` not naming a profile fails with `worker_profile must name a defined model profile: '<value>'`.
5. Docs: README resolution order now includes the manifest step (currently `standard`); `rules/model-selection.md` L4 names `worker_profile` and forbids ad-hoc `HERDR_AGENTS_WORKER_PROFILE` exports.
6. Tests: generator (renders / absent key renders no line / unknown fails), herdr-agents (env-file `HERDR_AGENTS_WORKER_PROFILE=express` beats `MODEL_PROFILE_INTERACTIVE=review`; explicit env `deep` beats env-file `express`; codex worker fixture, same pattern as the existing `test_codex_profile_*` cases), validator (unknown rejected). The herdr default test fails on origin/main code (it would print `review`).
7. Regenerated: diff limited to `home/dot_agents/model-profiles.env` with exactly the 3 expected lines; `claude-settings-managed.json`, codex outputs, and `express-explorer.md` unchanged (0 files under `home/.chezmoitemplates`/`home/dot_claude/agents` in the diff).

## Not done / out of scope

- No merge, force push, `chezmoi apply`, or local bats. worker_kind / interactive_profile / codex settings untouched.
- The understand-anything SessionStart/commit hooks asked for a `.ua/` graph update; skipped because `.ua/` is outside allowed_files.
- Deployment (`chezmoi apply` so `~/.agents/model-profiles.env` picks up `HERDR_AGENTS_WORKER_PROFILE`) is orchestrator-side after acceptance; until then a live `herdr-agents` still launches workers on `deep`.

## CompactionDB command

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T24: herdr worker profile = standard (claude-opus-5-5 high) via manifest worker_profile; worker_kind stays claude (operator 2026-09-27)"
```

cost: n/a
