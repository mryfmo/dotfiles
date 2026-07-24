# Orchestration task: T16 herdr --attach layout order verification & repair

## Assignment

- Task ID: `T16-herdr-attach-layout-order-repair`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles`, branch from current `main`
  (`cab6de1`): create `feat/herdr-attach-order-repair`
- Pre-existing dirty/untracked paths (`home/dot_mise/*`, `.orchestration/`,
  `.agents/`, `plans/`, `docs/verification/`) are NOT yours.

## Problem (root cause, verified by orchestrator)

T15 shipped `herdr-agents --attach` but attach mode only checks pane
EXISTENCE, never ORDER. Herdr persists sessions in
`~/.config/herdr/session.json`; a repair earlier today saved workspace `w13`
with the files pane as the ROOT (leftmost) pane. Every subsequent `herdr`
launch restores files | claude | codex, and `--attach` sees "files pane
exists, codex live" → reuses everything → the wrong order persists forever.
The intended layout is claude | codex | files at 40/40/20 (T10/T15).

## Desired behavior

1. `herdr-agents --attach` (after the existing ensure/reuse steps in
   `home/dot_local/bin/common/executable_herdr-agents:293-310`) verifies the
   left-to-right visual order of the three panes: `claude-orchestrator`,
   `codex-worker`(the pane of agent `codex-worker-<workspace>`), `files`.
2. If the order is wrong, repair it with `herdr pane swap --source-pane ID
--target-pane ID` operations until the order is claude | codex | files.
   Determine current order from x-coordinates via `herdr pane layout` (or
   `herdr pane edges`) — inspect the real JSON shape with read-only calls
   before coding; do not guess field names.
3. Best-effort ratio repair toward 40/40/20 using `herdr pane resize` ONLY if
   the observed layout JSON gives enough information to compute it safely;
   otherwise skip ratio repair and record why in the report (order repair is
   the hard requirement).
4. Idempotent: when the order is already correct, `--attach` performs zero
   mutating herdr calls beyond the existing behavior. Re-running twice
   changes nothing.
5. Panes other than the three managed labels must not be touched. If the
   workspace has extra/ambiguous panes (e.g. two `files` labels), refuse the
   order repair with a clear stderr message and exit 0 (do not break Claude
   startup) — same spirit as the existing `ensure_files_pane` ambiguity
   guard.
6. Full mode and non-herdr no-op paths unchanged.

## Implementation notes

- Reuse existing helpers (`json_agent_pane_id`, `files_pane_id`,
  `live_codex_pane_id`, pane-list JSON already fetched at `:297`). Add the
  smallest possible new function(s), shdoc-commented in English.
- `herdr pane swap --source-pane ID --target-pane ID` and
  `herdr pane layout [--pane ID]` exist (verified in CLI help). Read-only
  herdr calls (list/get/layout/edges/help) are allowed for exploration.
- Keep the fast no-op path (`:266-269`) untouched and first.

## Test requirement

Update `tests/unit/test_herdr_agents.py` (unittest style, existing mocking
approach) FIRST with failing tests covering: (a) wrong order files|claude|codex
triggers the expected swap sequence; (b) correct order performs no swap;
(c) ambiguous panes → no swap, exit 0. Existing tests must still pass.

## Constraints

- allowed_files:
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `tests/unit/test_herdr_agents.py`
  - the artifact paths below
- forbidden_actions: `git-commit-push (until orchestrator authorizes);
chezmoi-apply; live-herdr-mutation (no mutating herdr calls against the
running session — read-only herdr CLI is allowed); deps-or-ci-changes;
llm-calls; edits-outside-allowed-files`
- E2E on the live herdr session is the ORCHESTRATOR's job after acceptance;
  do not attempt it.

## Validation commands (full output into the validation artifact)

- `uv run python -m unittest tests.unit.test_herdr_agents -v`
- `make unit-test`
- `uv run --with pyyaml scripts/validate-agent-assets.py`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents` (record availability)
- `bash -n home/dot_local/bin/common/executable_herdr-agents`
- `git status --short` (only allowed files)

## Expected artifacts

- report: `.orchestration/reports/T16-herdr-attach-layout-order-repair.md`
- validation: `.orchestration/validation/T16-herdr-attach-layout-order-repair.md`
- sandbox: `.orchestration/sandboxes/T16-herdr-attach-layout-order-repair.md`
- learning: `.orchestration/learning/T16-herdr-attach-layout-order-repair.md`
- autoskill: `.orchestration/autoskill/runs/T16-herdr-attach-layout-order-repair.md`

## STOP conditions

- `herdr pane layout`/`edges` JSON does not expose pane x-order → STOP and
  report the actual JSON shape with evidence.
- Swap semantics make deterministic three-pane ordering impossible → STOP
  with evidence.

When done send: `AGMSG-RESULT v1 task_id=T16-herdr-attach-layout-order-repair status=ready_for_review report=... validation=... sandbox=... learning=... autoskill=...`
