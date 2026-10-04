# dotfiles-T62-claude-auto-deny-a01 — report

status: ready_for_review
branch: chore/claude-auto-deny

## Change

- Set user-level Claude `permissions.defaultMode` to `auto` with an explanatory boundary comment.
- Move the five publish-class Bash rules from `ask` to `deny`, remove `Bash(git push:*)`, and preserve `ask: []` without changing the generator.
- Regenerate the managed Claude settings template and add regression assertions for the rendered policy.

## Verification

- SchemaStore's current Claude settings schema includes `auto` in `permissions.defaultMode`.
- Official Claude docs describe `auto` as a permission mode, require user or managed settings for `auto` and `bypassPermissions`, and state that matching ask rules prompt even in auto mode: https://code.claude.com/docs/en/permissions and https://code.claude.com/docs/en/settings.
- `make render-check`, focused unit tests, `make unit-test`, and `make validate-agent-assets` completed successfully. Asset validation reported pre-existing main-checkout orchestration warnings but ended `agent asset validation ok`.

## Review

Crit had no active review file. Independent resolved evidence and receipt are at `.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-crit.json` and `.orchestration/validation/dotfiles-T62-claude-auto-deny-a01-review-receipt.md`; the Crit gate passed with that evidence.

## CompactionDB

`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T62 (operator 2026-10-03): Claude user-level permissions use defaultMode auto; publish-class commands are denied rather than asked; the git push ask is removed because the GitHub ruleset protects main and branch pushes are legitimate.'`

Output: `6edcac14-a57c-4af6-8719-3d907abff970`

cost: n/a
