# Orchestration task: T15 herdr lazy start + claude-triggered 3-pane layout

## Assignment

- Task ID: `T15-herdr-lazy-start-attach-layout`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles`, branch from current `main`
  (`1c2943e`): create `feat/herdr-lazy-start`
- Pre-existing dirty/untracked paths (`home/dot_mise/*`, `plans/`,
  `docs/verification/`, `.orchestration/`, `.agents/`) are NOT yours.

## Desired behavior (operator specification)

1. Launching `herdr` in Ghostty (no args → zsh wrapper → `herdr-session`)
   opens ONE plain terminal only — no files pane, no second terminal.
2. Starting Claude Code inside any herdr terminal transforms that workspace
   into three panes: claude (left) | codex worker (middle) | yazi files
   (far right, 20%) — the 40/40/20 layout already validated in T10.
3. Adding a new herdr workspace behaves the same: its terminal starts plain,
   and starting Claude Code there triggers the same per-workspace 3-pane
   setup. Idempotent: if the workspace already has a live codex/files pane,
   reuse them (the existing repair logic in `herdr-agents`).

## Implementation outline

1. `home/dot_local/bin/common/executable_herdr-session`: remove the
   `herdr-agents "${PWD}"` pre-build; keep usage/help and `exec herdr`.
2. `home/dot_local/bin/common/executable_herdr-agents`: add an `--attach`
   mode alongside the existing default:
   - No-op `exit 0` immediately when `HERDR_ENV`/`HERDR_PANE_ID`/
     `HERDR_WORKSPACE_ID` are unset (hook fires for every Claude session,
     including non-herdr ones — keep this path fast, no herdr calls).
   - In herdr: treat `HERDR_PANE_ID` as the claude pane (claude is already
     starting in it — do NOT run `claude_command`, do NOT launch zed).
     Rename it `claude-orchestrator`.
   - Reuse the existing functions for the rest: if the workspace
     (`HERDR_WORKSPACE_ID`) lacks a files pane → `start_files_pane <claude_pane> <cwd> 0.8`;
     lacks a live codex agent → `start_codex_agent` with
     `codex-worker-${HERDR_WORKSPACE_ID}` (fresh-path order per T10:
     files first from the claude pane, then codex lands between → 40/40/20).
     If they exist, reuse/repair exactly as the existing
     `find_existing_workspace` branch does (yazi restart check included).
   - Guard against double-fire (SessionStart also fires on resume/clear):
     re-running `--attach` on a complete workspace must change nothing.
3. Claude Code SessionStart hook (official mechanism) to run
   `herdr-agents --attach`: wire it in the chezmoi-managed Claude settings.
   Read `home/dot_claude/modify_private_settings.json` first to learn how
   settings are managed; add the hook the same way. The hook command must
   not block Claude startup on failure (`|| true` semantics, redirect output
   to the herdr-agents log).
4. Update shdoc header comments (English) for both scripts per repo policy.
5. Keep the `prefix+alt+a` keybinding (`herdr-agents` full mode) working
   unchanged for manual workspace creation.

## Test requirement

Update `tests/unit/test_herdr_agents.py` (unittest style, runs under
`make unit-test`) to cover: `--attach` no-ops without HERDR env; herdr-session
no longer references herdr-agents; existing full-mode expectations still pass.
Follow the file's existing mocking approach. Write failing tests first.

## Constraints

- allowed_files:
  - `home/dot_local/bin/common/executable_herdr-session`
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `home/dot_claude/modify_private_settings.json` (or the actual settings
    source you identify — report the exact file; STOP if hook wiring would
    require files outside home/dot_claude/)
  - `tests/unit/test_herdr_agents.py`
  - the artifact paths below
- forbidden_actions: `git-commit-push (until orchestrator authorizes);
chezmoi-apply; live-herdr-mutation (do not touch the running herdr session);
deps-or-ci-changes; llm-calls; edits-outside-allowed-files`

## Validation commands (full output into the validation artifact)

- `uv run python -m unittest tests.unit.test_herdr_agents -v`
- `make unit-test`
- `uv run --with pyyaml scripts/validate-agent-assets.py`
- `shellcheck` both scripts (record availability)
- `bash -n` both scripts
- `git status --short` (only allowed files)

## Expected artifacts

- report: `.orchestration/reports/T15-herdr-lazy-start-attach-layout.md`
- validation: `.orchestration/validation/T15-herdr-lazy-start-attach-layout.md`
- sandbox: `.orchestration/sandboxes/T15-herdr-lazy-start-attach-layout.md`
- learning: `.orchestration/learning/T15-herdr-lazy-start-attach-layout.md`
- autoskill: `.orchestration/autoskill/runs/T15-herdr-lazy-start-attach-layout.md`

## STOP conditions

- Claude settings hook wiring cannot be done within home/dot_claude/ →
  STOP and report the actual surface.
- `herdr pane`/`agent` APIs needed for --attach do not support an operation
  (e.g., pane rename of an agent-attached pane) → STOP and report evidence.
- validate-agent-assets.py asserts tokens in these files that conflict →
  STOP and report.

When done send: `AGMSG-RESULT v1 task_id=T15-herdr-lazy-start-attach-layout status=ready_for_review ...` with all artifact paths.
