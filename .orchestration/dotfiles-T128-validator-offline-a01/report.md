---
task_id: dotfiles-T128-validator-offline-a01
seat: claude-standard-dot-a002
branch: tools/validator-offline
base: 59599783
code_commit: 4730fb1c
pr: 366
task_sha256: 52a5f2099551f2b434c23b0ccefcb426bf5c5b87288ebc3e2b43430d699c779e
---

# Report: dotfiles-T128-validator-offline-a01

- Seat: `claude-standard-dot-a002` in `.claude/worktrees/worker-f`, on a fresh branch `tools/validator-offline` from `origin/main` `59599783`, PR #366. The PR #365 branch stays as it was for its acceptance.
- Task file: sha256 `52a5f209…`, copied byte-identical; the task-consistency check passes on the dispatched file (validation §1). Dispatched 05:42:00Z. All three premises replay equal (§2). No question and no amendment.

## What landed

| Item | File | What it does |
|---|---|---|
| 1 | `Makefile` | One recursive variable `UV_PYYAML = $(if $(shell uv run --offline --with pyyaml python -c 'import yaml' 2> /dev/null && echo y),uv run --offline --with pyyaml,uv run --with pyyaml)`, verbatim from item 1, with its one-line comment, defined just above the `validate-agent-assets` recipe. Both recipes run `$(UV_PYYAML) <script>`. Nothing else changes (validation §3). |
| 2 | `tests/unit/test_makefile_offline.py` (new) | The two named tests; see below. |

## Tests

- `test_validator_targets_try_the_offline_form_first`: the definition holds both forms, and both recipes use the variable.
- `test_the_recipe_falls_back_only_when_the_cache_is_cold`: a stub `uv` first on PATH, which `make`'s `$(shell …)` probe also resolves. Three cases, each asserting the whole call list:
  - `PROBE_RC=0 RUN_RC=0`: probe, then the offline form; exit 0.
  - `PROBE_RC=1 RUN_RC=0`: probe, then the index form; exit 0.
  - `PROBE_RC=0 RUN_RC=1`: probe, then the offline form, and no third call; make fails.

The Check: 2 tests OK; `make -n` of both targets shows the offline form here (validation §4). Beyond the Check, both targets ran for real inside the Claude sandbox and exited 0: `agent asset validation ok` and `generated agent configs are up to date` (§5). That is D10 from this seat. A mutation check of three edits was caught 3 of 3, but not saved as evidence: the fallback order swapped, the probe without `--offline`, and one recipe back on the bare form.

## Caps

Validation §6: outside `tests/` and `.orchestration/`, 1 file, 5 added + 2 deleted = 7 changed lines (cap 200); under `tests/`, 61 added lines (cap 1000); 2 files outside `.orchestration/`.

## CI and the Bot

- PR #366 was opened as a draft. It was marked ready after the evidence commit; the Bot's threads and CI are in the RESULT.

## Not done, or outside scope

- Recursive `=` means the probe runs on each expansion. One recipe expands the variable once, so one probe runs per target, as the stub log shows. `:=` would probe at parse time for every target, which item 1 rules out.
- Understand-Anything hook: did not fire. plan-mode-used: no. cost: n/a.
