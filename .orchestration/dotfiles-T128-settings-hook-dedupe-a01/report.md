# RESULT report: dotfiles-T128-settings-hook-dedupe-a01

Status: local implementation complete; publication and required render-check blocked by current network/dependency availability.
Branch:fix/managed-post-tool-use-dedupe
Base:595997831afcc05b266c9f245456df54725628db (origin/main and canonical main agree).
Task-copy SHA256:461643b4c10fd146416e0dd3c237b8a3ffbc2fe07098f9ab4cf827e40bc679f4

## Change

[memory:decision] PostToolUse now joins MANAGED_HOOK_PREDICATES with a predicate matching the existing SessionStart shape. MANAGED_POST_TOOL_USE_SCRIPTS names format-edited-files.py and project-map-reload.sh; the predicate accepts a dict/string command only after shlex.split succeeds and matches any token basename against that constant. Existing merge_managed_entries and merge_hooks are unchanged. This routes the stale formatter-only entry through in-place replacement instead of additive duplication; mixed entries keep hooks classified as unmanaged in their existing entry.

Only home/dot_claude/modify_private_settings.json and tests/unit/test_claude_settings_merge.py change outside task evidence. Source12 added lines (limit200 changed), tests29 added lines (limit1000). One new method test_managed_post_tool_use_replaces_stale_format_only_entry covers stale+managed duplicates, stale alone, mixed custom commands, absent key and additional malformed/nonstring/unrelated commands. It failed before implementation in six subcases, then all20 tests passed; the nineteen existing tests are unchanged.

## Validation

The full20-test settings-merge module passes. Native installed Ruff0.17.0 format-check passes for the test module; lint reports two diagnostics identical to the base by code/line/message (EXE001 test shebang/non-executable, UP022 pre-existing subprocess pipes), zero new diagnostics. Source diff-check passes. Crit data is absent; independent read-only review found no defect within the specified contract, with resolved JSON and receipt saved here. The gate result follows in validation.md.

make render-check cannot resolve PyYAML from PyPI due DNS restriction; the supported UV_OFFLINE retry also fails because dependency metadata is absent from the task cache. A direct no-dependency Python import confirms PyYAML absent. Ruff's initial uv --with attempt likewise failed cache resolution, but the already installed native Ruff was used through uv run without installing anything. An initial diagnostic reader tried to parse empty Ruff JSON after that failed resolution and raised JSONDecodeError; it produced no lint result and changed no source. Only the later native Ruff JSON is evidence for the two baseline diagnostics.

## Limits and effects

After merge, make update/chezmoi apply and a Claude Code restart are operator steps; none was run here. The change removes duplicate managed PostToolUse entries on apply, retaining hooks classified as unmanaged. As expressly specified, any parsed token with a managed basename is classified as managed: an unrelated same-named script or a command argument with such a basename is not protected as unmanaged. This limitation is disclosed rather than claiming all arbitrary custom commands survive.

No installed settings, template, manifest, renderer, PermissionRequest, SessionStart or hook executable changed. No command string from settings is executed by the new predicate. Tests run only the modify script against temporary managed/current settings. No local bats, dependency/config/policy change, browser Crit, Plan Mode or merge. Existing graph is stale; no graph update. CompactionDB consolidation remains orchestrator-owned because main state is outside writable roots; no memory ID claimed.

## Publication blocker

git fetch origin main failed: Could not resolve host:github.com. Current origin/main and canonical main already equal the required59599783, so local work uses that base without manufacturing a ref. The current sandbox also denies the Herdr socket, as observed in the preceding seat-check; progress replies use the provided agmsg send.sh storage path without a terminal wake. No escalation or alternate network route was used. A normal publication attempt and its exact output will be recorded after commit; no PR, CI or Bot review is claimed until they actually exist.

cost: n/a
