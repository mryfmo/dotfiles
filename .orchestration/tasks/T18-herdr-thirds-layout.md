# T18 — herdr-agents: equal-thirds layout with files pane at far right

## Objective

Make the herdr agents layout an equal three-way split — left to right
`Claude 1/3 | Codex 1/3 | files 1/3` — with the `files` (Yazi) pane always the
rightmost pane, and repair the ratio of already-persisted layouts on attach.

This supersedes the old 40/40/20 target from T10/T15. The operator confirmed
the new target: every pane exactly one third; existing skewed sessions (e.g.
the currently observed 50/25/25) must converge to thirds during attach repair.

## Scope of changes

Target script: `home/dot_local/bin/common/executable_herdr-agents`

### 1. Unify split ratios (files pane = 1/3)

`herdr pane split --ratio R` keeps fraction R for the original pane; the new
pane goes on the RIGHT and gets `1 - R`. Change all three call sites to
`0.667` so the files pane always gets one third:

- attach path (currently `ensure_files_pane "${panes_json}" "${claude_pane_id}" "${workdir}" 0.8`, around line 444)
- existing-workspace repair path (currently `... 0.6`, around line 489)
- fresh-workspace path (currently `start_files_pane "${root_pane_id}" "${workdir}" 0.8`, around line 513)

After the files split, `start_codex_agent` splits the remaining 2/3 pane with
`--split right` (default 50%), yielding 1/3 | 1/3 | 1/3.

### 2. Add attach-time ratio repair

Add a new function `repair_attach_pane_ratio()` (place it after
`repair_attach_pane_order()`) and call it in the attach flow immediately after
the existing `repair_attach_pane_order` call:

- Measure the three panes' `rect.x` / `rect.width` via `herdr pane layout --pane`.
- Reuse the existing guard style: if `attach_panes_are_unambiguous` fails, the
  layout query fails, or rects are not numbers, print a
  `... refusing ratio repair.` message to stderr and return 0 WITHOUT mutating
  anything (same non-destructive policy as order repair).
- If every pane width is within tolerance of total/3 (pick a small tolerance,
  e.g. 2 columns or ~3%), do nothing.
- Otherwise correct widths with `herdr pane resize`.
- IMPORTANT: `herdr pane resize` semantics (absolute vs delta, which neighbor
  shrinks) are undocumented. Before implementing, inspect
  `herdr pane resize --help` and verify actual behavior LIVE in a scratch
  workspace. T16 skipped ratio repair because nested split ratios could not be
  safely mutated — your implementation must fall back to skipping (with the
  refusing message) for any configuration it cannot safely converge.
- shdoc comments in English for the new function; also update comments to
  state the target layout (equal thirds, files far right).

### 3. Tests — `tests/unit/test_herdr_agents.py`

- Update the exact-command assertions pinning `--ratio 0.8` (around lines 333
  and 665) to the new ratio; update any assertion for the old `0.6` path.
- Add tests for ratio repair using the fake herdr CLI:
  (a) widths already equal → no resize command issued;
  (b) skewed widths (e.g. 86/43/43) → resize issued and converges;
  (c) ambiguous panes / failed layout / non-numeric rects → skipped, no mutation.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- Expected artifact paths listed below under `.orchestration/`
- Scratch directories for live verification (outside the repo)

## Forbidden actions

- No dependency changes, no Makefile/CI/hook/permission changes.
- Do not run `make require-crit-review` (orchestrator-side final step).
- Do not run bats locally (repo policy: CI runs bats).
- Do not modify or resize the operator's live `dotfiles agents` workspace/panes;
  do all live verification in scratch workspaces you create and clean up.
- Do not rewrite historical `.orchestration/tasks/*` specs (T10/T15/T16).
- Do not merge the PR.

## Git / PR

- The main worktree has many unrelated untracked changes. Create a separate
  `git worktree` from `main` (e.g. under `~/Workspace/.worktrees/`), branch
  `feat/herdr-thirds-layout`, and apply ONLY this task's changes there.
- Conventional Commit; PR title/description in English; note the layout target
  change (40/40/20 → equal thirds) in the description.
- Push, open the PR with `gh`, then check GitHub Actions results and fix
  failures until CI is green. Report the PR URL and CI status in the report.

## Validation (live E2E is mandatory)

Unit tests alone are insufficient — this changes live desktop behavior. Record
all command output in the validation file:

1. `python3 -m unittest tests.unit.test_herdr_agents` (or the repo's runner) — green.
2. Fresh session: run the modified `herdr-agents <scratch-dir>` → capture
   `herdr pane layout` JSON → three panes, widths each within tolerance of
   total/3, files pane has the greatest `rect.x` and runs yazi.
3. Persisted-session restore: build a deliberately skewed 3-pane layout in a
   scratch workspace (e.g. ~50/25/25), then run the attach path
   (`HERDR_ENV=... HERDR_PANE_ID=... HERDR_WORKSPACE_ID=... herdr-agents --attach`
   from the scratch cwd) → capture before/after `herdr pane layout` →
   order Claude|Codex|files and widths converged to thirds.
4. Clean up scratch workspaces afterwards.

## Expected artifacts

- report: `.orchestration/reports/T18-herdr-thirds-layout.md`
- validation: `.orchestration/validation/T18-herdr-thirds-layout.md`
- sandbox: `.orchestration/sandboxes/T18-herdr-thirds-layout.md`
- learning: `.orchestration/learning/T18-herdr-thirds-layout.md`
- autoskill: `.orchestration/autoskill/runs/T18-herdr-thirds-layout.md`

(Write artifacts under the MAIN worktree `/Users/mryfmo/Workspace/dotfiles/.orchestration/`,
not the task worktree; they stay uncommitted.)

## Done signal

Send `AGMSG-RESULT v1 task_id=T18-herdr-thirds-layout status=ready_for_review|blocked`
with all artifact paths. max_turns=40.
