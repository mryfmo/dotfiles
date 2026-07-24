# T22: Make `make update` idempotent for the Claude settings doctor check

## Objective

After every `make update`, `./scripts/check-agent-runtime.py` currently fails with
`Claude settings managed keys differ ... ~/.claude/settings.json`. Fix the root
cause so two consecutive `make update` runs each leave the doctor free of this
error, land the fix as a PR with green CI.

## Root cause (verified by orchestrator, 2026-07-23)

- `make update` → `scripts/update-agent-assets.sh` → `ensure_herdr_integrations()`
  (lines ~283-292) runs `herdr integration install claude`, which REWRITES
  `~/.claude/settings.json` with herdr's own JSON serialization: different
  object key order (e.g. `command` before `type`), different hook-section order
  (`PostToolUse` before `PreToolUse`), and different `SessionStart` array entry
  order (herdr-agents `--attach` entry before the managed `herdr-agent-state`
  entry).
- Doctor's `same_modified()` in `scripts/check-agent-runtime.py` (lines ~47-62)
  requires `modify(current) == current` BYTE-identical, so any cosmetic
  re-serialization by the herdr writer fails the check even when content is
  semantically identical.
- Evidence: `python3 -m json.tool` diff shows only ordering differences;
  a sorted-keys diff shows only the SessionStart entry-order difference.

## Required fix (two parts)

1. `home/dot_claude/modify_private_settings.json`: make the merge
   order-preserving — for keys and hook-array entries that already exist in the
   current file, keep the current relative order; only append managed entries
   that are missing. Managed VALUES still win for managed keys. Goal:
   `json.loads(modify(current)) == json.loads(current)` whenever current is
   semantically compliant, regardless of who serialized it last.
2. `scripts/check-agent-runtime.py`: for the Claude settings check (and only
   for JSON targets), compare `json.loads(modify(current)) ==
json.loads(current)` instead of byte equality. Real value drift (wrong
   model, missing hook, extra managed key value) must STILL fail.

Reconcile with the existing test
`test_claude_settings_merge.test_desired_current_output_is_byte_identical` —
update it if its fixture assumes managed-first ordering, but keep a
byte-idempotency property: `modify(modify(x)) == modify(x)`.

## Tests to add/extend

- `tests/unit/test_claude_settings_merge.py`:
  - current has SessionStart `[attach-hook, managed-state-hook]` and managed
    defines only the state hook → output preserves current order and content;
    `json.loads(modify(current)) == json.loads(current)`.
  - key-order variation of a managed hook object (`command` before `type`) is
    accepted unchanged.
- `tests/unit/test_check_agent_runtime.py` (or wherever same_modified is
  covered): cosmetic re-serialization passes; a real value change (e.g.
  different `model`) still fails.

## Verification (log everything to the validation artifact)

1. `uv run python -m unittest discover -s tests/unit` → all green.
2. Live E2E in /Users/mryfmo/Workspace/dotfiles (allowed for this task):
   `make update && ./scripts/check-agent-runtime.py; make update && ./scripts/check-agent-runtime.py`
   → NO `Claude settings managed keys differ` error in either run. The known
   pre-existing `agmsg/db-flue-pi` failure is expected and out of scope.
3. Branch `fix/doctor-settings-idempotency` from origin/main in a separate
   worktree, commit `fix(doctor): compare managed Claude settings semantically
and preserve current hook order`, push, `gh pr create` (English), CI green.
   Do NOT merge before AGMSG-ACCEPTANCE next_action=merge; after acceptance,
   merge + guarded main sync exactly as in T21.

## Allowed files

- `home/dot_claude/modify_private_settings.json`
- `scripts/check-agent-runtime.py`
- `tests/unit/test_claude_settings_merge.py`
- `tests/unit/test_check_agent_runtime.py`
- `tests/unit/test_runtime_health.py` (only if an assertion there breaks)
- Artifacts below; `/tmp/T22-*` scratch.
- Live runs limited to: `make update`, `./scripts/check-agent-runtime.py`,
  unit tests, git/gh for the PR flow.

## Forbidden actions

- `make upgrade`, local bats, editing other launchers/manifest/generator,
  touching `~/.agents/skills/agmsg` stores, merging before acceptance,
  force-push, committing `.orchestration/` or `.agents/`, secrets in artifacts.
- Do not "fix" the doctor by deleting or weakening the check for real drift.

## Expected artifacts

- report: .orchestration/reports/T22-doctor-settings-idempotency.md
- validation: .orchestration/validation/T22-doctor-settings-idempotency.txt
- sandbox: .orchestration/sandboxes/T22-doctor-settings-idempotency.md
- learning: .orchestration/learning/T22-doctor-settings-idempotency.md
- autoskill: .orchestration/autoskill/runs/T22-doctor-settings-idempotency.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review (or blocked). max_turns=40
