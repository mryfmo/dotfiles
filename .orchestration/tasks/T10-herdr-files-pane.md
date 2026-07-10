# T10-herdr-files-pane

## Objective

Complete the implementation of the approved plan
`.agents/worklog/claude/ghostty-herdr-abundant-cerf.md`: add an auto-refreshing
icon file-list pane (eza, ~20% width, far right) to the herdr agent workspace
built by `herdr-agents`, with unit tests and docs.

Read the plan file first — it contains the full design, verified herdr CLI
signatures, and researched decisions. This task file only scopes your work.

## Current state (IMPORTANT — partial edits already applied)

`home/dot_local/bin/common/executable_herdr-agents` already contains (uncommitted,
authored by the orchestrator; keep them, fix them if you find a defect):

1. Updated shdoc `@brief`/`@description` and `usage()` text mentioning the files pane.
2. `files_command()` — returns the pane command:
   `while :; do clear; eza -1 --icons=always --color=always --group-directories-first; sleep 2; done`
3. `start_files_pane()` — splits `--direction right --ratio 0.4 --cwd <workdir> --no-focus`
   from a given pane, renames the new pane to `files`, runs `files_command` in it.
   Soft-fails (stderr note, `return 0`) when eza is missing or split/parse fails.
4. `has_files_pane()` — jq check for `.result.panes[]? | select(.label == "files")`.

## Remaining work

### A. `home/dot_local/bin/common/executable_herdr-agents`

RATIO SEMANTICS (verified live by orchestrator, supersedes the `0.4` currently
hardcoded in `start_files_pane`): `herdr pane split --ratio R` keeps fraction R
for the ORIGINAL pane; the NEW pane gets `1 - R`. Also verified: with a files
pane already split off the root, `herdr agent start --split right` splits the
workspace's active (root/Claude) pane, so Codex lands BETWEEN Claude and the
files pane (measured 78/77/39 cols ≈ 40/40/20).

1. Change `start_files_pane` to take a ratio as third argument and use it in
   the split call: `start_files_pane <pane_id> <workdir> <ratio>`.
2. Fresh-workspace path — NEW ORDER for a 40/40/20 layout:
   `start_claude_in_pane "${root_pane_id}"`, then
   `start_files_pane "${root_pane_id}" "${workdir}" 0.8 || true` (files pane =
   20% far right), THEN `start_codex_agent` (unchanged call, output may stay
   discarded — the codex pane id is no longer needed here; codex lands in the
   middle).
3. Repair path (existing-workspace branch): after codex/claude repair and before
   `herdr workspace focus`, if `! has_files_pane "${panes_json}"`, call
   `start_files_pane "${codex_pane_id}" "${workdir}" 0.6 || true`
   (codex keeps 60% of its half → files ≈ 20% of total; 50/30/20 is acceptable
   for the repair edge case).
   (`panes_json` staleness after claude repair is fine — claude repair never
   creates a `files`-labeled pane.)
4. Bug guard: `empty_pane_id()` must exclude panes with `label == "files"`,
   otherwise claude repair hijacks the files pane (it has no agent). Herdr
   `pane list` JSON has a per-pane `label` field (verified live).

### B. `tests/unit/test_herdr_agents.py`

1. Add a fake `eza` executable in `setUp` (like `claude`/`codex`).
2. Make the fake herdr `pane split` handler return incrementing pane ids
   (p3, p4, ...) via a counter file so two splits in one test don't collide.
3. Update `test_uses_initial_workspace_pane_for_claude_and_splits_codex_right`:
   assert the files-pane split/rename/run calls. Expected fresh-path call order
   (fake split counter yields p3 first):
   `pane rename w-test:p1 claude-orchestrator` → `pane run w-test:p1 …claude…`
   → `pane split w-test:p1 --direction right --ratio 0.8 --cwd <workdir> --no-focus`
   → `pane rename w-test:p3 files` → `pane run w-test:p3 while :; do …`
   → `agent start codex-worker-w-test …` → `pane rename w-test:p2 codex-worker`.
4. Update the exact-call-list assertion in
   `test_ghostty_herdr_starts_left_right_agents_with_working_agmsg`, AND add a
   `pane split` handler to its inline fake herdr. CRITICAL: that fake executes
   `bash -c "$4"` on `pane run` — the files loop is infinite and would hang the
   test. Restrict execution to the Claude pane (`w-test:p1`); log-only for others.
5. Repair-path fixtures: add `"label"` fields where needed. New/updated tests:
   - existing workspace missing the files pane → split/rename/run files calls issued;
   - existing files pane (fixture pane e.g. `w-old:p9`, `"agent":null,"label":"files"`)
     is NOT picked by claude repair and NOT re-split (no `--ratio` call);
   - fully-populated workspace (claude+codex+files) → no `pane split` at all
     (extend `test_existing_agents_workspace_focuses_without_recreating_agents`).

### C. Docs

- `docs/reference/home/dot_local/bin/common/executable_herdr-agents.md`: describe
  the three-pane layout (Claude left, Codex middle, files pane far right) and the
  eza soft-requirement.
- `docs/reference/home/dot_local/bin/common/executable_herdr-session.md`: update
  only if it describes the two-pane layout.

## Allowed files

- home/dot_local/bin/common/executable_herdr-agents
- tests/unit/test_herdr_agents.py
- docs/reference/home/dot_local/bin/common/executable_herdr-agents.md
- docs/reference/home/dot_local/bin/common/executable_herdr-session.md
- .orchestration/reports/T10-herdr-files-pane.md
- .orchestration/validation/T10-herdr-files-pane.md
- .orchestration/sandboxes/T10-herdr-files-pane.md
- .orchestration/learning/T10-herdr-files-pane.md
- .orchestration/autoskill/runs/T10-herdr-files-pane.md

## Forbidden actions

- git commit / push / branch changes; chezmoi apply
- dependency or Makefile / CI / hook / permission changes
- running or mutating the live herdr server (no `herdr workspace create`,
  `pane split`, `agent start`, etc. — the orchestrator does live verification)
- running bats tests; network installs; LLM API calls
- editing any file outside Allowed files (including the plan file)

## Validation (record command + output in the validation artifact)

1. `bash -n home/dot_local/bin/common/executable_herdr-agents`
2. `shellcheck home/dot_local/bin/common/executable_herdr-agents` (if installed;
   record "not installed" otherwise)
3. `make unit-test` — all tests must pass (uses `uv run python -m unittest
discover -s tests/unit -v`)

## Result protocol

- done_signal: AGMSG-RESULT v1 (team dotfiles-conformance, to orchestrator-fable5)
- status=ready_for_review with all artifact paths, or status=blocked with the
  blocker documented in the report.
- max_turns: 25
