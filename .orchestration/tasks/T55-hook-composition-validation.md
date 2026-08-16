# T55: Hook-composition static validation (H3)

task_id: T55
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 2)
analysis: .orchestration/analysis/harness-composability-research.md (H3)

[memory: decision — Hook composition across the managed Claude/Codex settings is a validated invariant: no duplicate command per event, permgate first on PermissionRequest, per-event synchronous timeout budget <= 30s, and the intended SessionStart ordering is pinned; violations fail validate-agent-assets.]

## Goal

Approximate the dsh waterfall contract statically: since the harness gives
no composition semantics for multiple hooks on one event, pin the intended
composition as CI-validated invariants.

## Allowed files (edit boundary)

- scripts/validate-agent-assets.py (new check category only; do not touch
  existing categories)
- tests/unit/ (the matching unit-test module; extend or create — state
  which in the report)
- Your artifact paths (T55 five artifacts)
- FORBIDDEN: any change to hook definitions themselves (settings
  templates, agent-config.yaml, vendor settings.fragment.json)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; changes to
hook sources; relaxing any existing validation.

## Work order (exact; ambiguity -> ask via agmsg)

1. Build the per-event hook inventory from these three MANAGED sources:
   - home/.chezmoitemplates/claude-settings-managed.json
   - home/.chezmoitemplates/codex-config-managed.toml (its hooks section)
   - vendor/compactiondb/.claude/settings.fragment.json
     Runtime-generated repo-scoped files (.claude/settings.local.json,
     .codex/hooks.json) are OUT of scope — record the reason (runtime
     artifacts owned by delivery.sh) in the report.
2. Implement these rules as ONE new check category (each violation a
   distinct finding):
   (a) duplicate-command: within one (source, event) no two entries share
   the same command string;
   (b) permgate-first: in every PermissionRequest event list containing
   permgate, permgate is the FIRST entry;
   (c) sync-timeout-budget: for each (source, event), sum the declared
   timeouts of synchronous entries; fail if > 30s (constant
   SYNC_TIMEOUT_BUDGET_S = 30 with a comment citing PLAN H3);
   (d) sessionstart-order: pin the CURRENT relative order of SessionStart
   entries per source as the intended order (read the current sources,
   hard-code the expected command-substring sequence as a constant
   with a comment citing PLAN H3); any reorder fails.
3. Confirm the check passes on the current tree BEFORE writing tests;
   paste the passing output in the validation artifact.
4. Unit tests: for each rule, a fixture that violates it -> check fails
   with the expected finding; plus one fixture mirroring the real sources
   -> passes. Do not shell out to chezmoi; parse the template files
   directly with the same tolerance the script already uses for
   {{ ... }} placeholders (state the parsing approach).
5. Keep runtime under 1s added to validate-agent-assets (it is run in CI
   and pre-commit contexts).

## Validation (record in validation artifact)

1. `make validate-agent-assets` -> green on current tree (paste tail).
2. `make unit-test` -> all green (state totals and new-test count).
3. `make format` -> exit 0.
4. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

- Five artifacts (T55 set).
- Run the T45-contract memory add with the durable fact above; include
  the exact command in the report.
- Reply `AGMSG-RESULT v1 task_id=T55 status=ready_for_review ...`.
  max_turns=20.
