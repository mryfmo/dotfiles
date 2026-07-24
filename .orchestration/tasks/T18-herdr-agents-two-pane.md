# Orchestration task: T18 herdr-agents two-pane layout (drop auto Yazi files pane)

## Assignment

- Task ID: `T18-herdr-agents-two-pane`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles`
- The main worktree is dirty with UNRELATED changes. Create a separate git
  worktree from `main` (e.g. `git worktree add ../dotfiles-t18 -b
feat/herdr-file-viewer-popup main`) and do ALL work there. Report the
  worktree path in your result report. Do NOT touch the main worktree.
- Pre-existing dirty/untracked paths in the main worktree (`home/dot_mise/*`,
  `home/.chezmoitemplates/*`, `home/dot_agents/*`, `home/dot_config/claude/*`,
  `home/dot_config/codex/*`, `tests/unit/test_generate_agent_configs.py`,
  `.orchestration/`, `.agents/`) are NOT yours.

## Problem (verified by orchestrator)

`home/dot_local/bin/common/executable_herdr-agents` auto-creates a right-side
`files` pane running Yazi (ratio 0.667) in all three flows (new workspace,
attach, existing-workspace repair), producing a 3-pane layout. The operator
replaced this with an on-demand `prefix+f` popup file viewer (separate task
T19), so the workspace must become exactly 2 panes: claude-orchestrator
(left) and codex-worker (right), ~50/50.

## Desired behavior

1. No files/Yazi pane is ever created or repaired. Zero `yazi` references
   remain in the script (`grep -c yazi` == 0).
2. New-workspace flow: claude in the initial pane, codex started via the
   existing `herdr agent start ... --split right` (default ratio 0.5 gives
   50/50 — do NOT add a ratio argument).
3. Attach and existing-workspace flows create/repair only the 2 managed
   panes. Order repair: claude left, codex right (single swap). Ratio
   repair: 50/50 target, +-2 cell tolerance, one resize attempt then
   re-inspect, warn if not converged. Refuse repair (warning, exit 0, no
   mutation) when panes are ambiguous or unmanaged panes are present.
4. Legacy tolerance: a persisted pre-change session restores a third pane
   labeled `files` (plain shell, no launch_argv). This MUST NOT be closed,
   split, or reused: attach detects it as an unmanaged extra pane, logs the
   existing "ambiguous ... refusing repair" warning, and leaves layout
   untouched while both agents keep working. Keep the `"files"` label
   exclusion in `empty_pane_id` (guards claude repair from hijacking the
   legacy pane) with a short comment noting why it survives.

## Implementation sketch (orchestrator-reviewed; adjust if the code disagrees)

- Delete whole functions: `start_yazi_in_pane`, `start_files_pane`,
  `ensure_files_pane`, `files_pane_id`, `pane_runs_yazi`.
- Rewrite: header shdoc + `usage()` (drop Yazi wording);
  `attach_panes_are_unambiguous` (managed set `[claude, codex]`);
  `repair_attach_pane_order` (2-pane, one `herdr pane swap`);
  `repair_attach_pane_ratio` (2-pane: exactly 2 managed panes sorted by x,
  one `direction == "right"` split spanning the width, adjacency check,
  target = total/2, +-2 tolerance).
- Delete: `require_command yazi`; the `ensure_files_pane` call in attach
  flow; the files-related block in the existing-workspace flow (files pane
  capture + ensure + post-creation ratio repair); the
  `start_files_pane ... 0.667` call in the new-workspace flow.
- All shdoc comments in English (repo comment policy).

## Test requirement (update FIRST, same commit)

`tests/unit/test_herdr_agents.py`:

- Harness: remove the `yazi` fake executable, the `pane process-info` branch
  of the herdr fake, `process_info*` fixtures and `write_process_info`.
  Rework `write_ratio_layout` (and 3-pane `write_workspace_state` usages) to
  2-pane fixtures.
- Delete tests that only exercise yazi/files-pane behavior (missing-yazi
  guards, files-pane restart/inspection/propagation tests, nested-thirds
  skew repair).
- Rewrite 3-pane assumptions to 2-pane halves for the attach/build/repair/
  idempotency/agmsg-bootstrap tests (assert: no `pane split --ratio` for a
  files pane, no `pane run ... yazi`, single codex split, one swap for order
  repair, 50/50 ratio repair, unsafe-geometry skips).
- Legacy tolerance tests: 3-pane fixture including a `files`-labeled shell
  pane → attach refuses repair with the ambiguity warning, exit 0, no
  mutations beyond the claude rename; full mode on a workspace containing a
  legacy files pane → no split/reuse of it, focus succeeds. Keep the
  `empty_pane_id` exclusion test (minus process-info).
- Keep untouched: `test_yazi_edit_opener_prefers_zed_with_editor_fallback`
  (yazi stays a mise-managed tool; only herdr-agents drops it), YAZI_CONFIG
  assertions, all agmsg/zshrc/ghostty tests not affected by pane-count.

## Constraints

- Allowed files: `home/dot_local/bin/common/executable_herdr-agents`,
  `tests/unit/test_herdr_agents.py`, plus the expected artifact paths under
  `.orchestration/` in the MAIN worktree.
- Forbidden actions: editing any other file; dependency changes; touching
  `home/dot_mise/*` or `home/dot_config/herdr/*` (T19 scope); `chezmoi
apply`; any live herdr mutation (`herdr pane|server|plugin ...`); running
  `bats` locally; `git push`; commits outside the T18 worktree.
- Commit on `feat/herdr-file-viewer-popup` in the T18 worktree with a
  Conventional Commit message.

## Validation (record full output)

1. `uv run pytest tests/unit/test_herdr_agents.py` (green)
2. `shellcheck home/dot_local/bin/common/executable_herdr-agents`
3. `shfmt -d home/dot_local/bin/common/executable_herdr-agents`
4. `grep -c yazi home/dot_local/bin/common/executable_herdr-agents` → `0`
   (grep exits 1; show the output)

## Expected artifacts (exact paths, MAIN worktree)

- report: `.orchestration/reports/T18-herdr-agents-two-pane.md`
- validation: `.orchestration/validation/T18-herdr-agents-two-pane.md`
- sandbox: `.orchestration/sandboxes/T18-herdr-agents-two-pane.md`
- learning: `.orchestration/learning/T18-herdr-agents-two-pane.md`
- autoskill: `.orchestration/autoskill/runs/T18-herdr-agents-two-pane.md`

## Done signal

`AGMSG-RESULT v1` with `task_id=T18-herdr-agents-two-pane`,
`status=ready_for_review|blocked`, and all artifact paths. Max turns: 25.
