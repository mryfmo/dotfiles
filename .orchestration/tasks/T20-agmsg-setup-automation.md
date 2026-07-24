# T20 — Automate agmsg wiring via make update/upgrade and Claude startup

## Objective

Close the automation gap the operator identified: agmsg delivery wiring must be
established (a) by `make update` and `make upgrade`, and (b) by the time a
Claude Code session starts inside herdr, without any manual `delivery.sh`
invocation. Today only the codex turn hook is auto-installed
(`bootstrap_agmsg()` in `executable_herdr-agents`); the claude-code side
(`.claude/settings.local.json` session/stop hooks) exists only because it was
once set by hand, and neither Makefile target touches agmsg at all.

## Required behavior

### 1. Startup bootstrap (herdr-agents)

Extend `bootstrap_agmsg()` in `home/dot_local/bin/common/executable_herdr-agents`:

- Keep the existing $HOME guard, codex turn-hook gate, and identity warnings.
- ALSO ensure claude-code delivery for `${workdir}`:
  - Steady-state gate first, pure file check, NO delivery.sh call when already
    configured: `${workdir}/.claude/settings.local.json` contains the agmsg
    session-start.sh SessionStart hook. Use the REAL nested schema
    (`.hooks.SessionStart[]?.hooks[]?` with `.command` containing
    `agmsg/scripts/session-start.sh`) — same lesson as the T17 jq-path defect.
  - Only when absent: run `delivery.sh set both claude-code "${workdir}"`
    (append to the same log file, `|| true` semantics). Print the known
    one-time effect note (may kill a live same-repo watcher once) and that the
    hooks take effect from the next Claude session.
- Verify a claude-code identity is registered for `${workdir}` via
  `identities.sh "${workdir}" claude-code`, mirroring the codex checks:
  none → print the exact `join.sh <team> <agent-name> claude-code "<workdir>"`
  instruction; multiple → ambiguity warning. Do NOT auto-join (team/agent
  naming is an operator decision per the identity rules).

### 2. Make targets

- Add a `make agmsg-bootstrap` target that runs the same ensure logic for the
  current repository (reuse, don't duplicate: extract the bootstrap into a
  shared script if needed — e.g. call `herdr-agents` bootstrap via a flag like
  `herdr-agents --bootstrap-agmsg [DIR]` that runs ONLY bootstrap_agmsg without
  any pane/layout work, or a small dedicated script under `scripts/`; pick the
  smallest correct factoring and document it).
- Wire it into BOTH `update:` and `upgrade:` targets (after the existing
  steps; must not fail the target when herdr/agmsg assets are absent — degrade
  to a clear skip message).
- `make update` currently applies with `--exclude=scripts`; the bootstrap must
  therefore be an explicit Makefile step, not a chezmoi run script.

### 3. Idempotency / safety (hard requirements)

- Steady state (hooks already present): ZERO `delivery.sh set` calls from both
  startup and make targets — a live watcher must survive repeated
  `make update`, `make upgrade`, and `herdr-agents --attach`.
- First-time setup: exactly one `delivery.sh set` call per missing side.
- Never write user-level (`$HOME`) hooks; repo-scoped only (existing guard).

### 4. Tests — `tests/unit/test_herdr_agents.py` (+ new test file if cleaner)

Failing tests first:

- claude-code hooks present (REAL nested schema fixture from an actual
  `delivery.sh set both` output) → zero delivery.sh calls.
- claude-code hooks absent → exactly one `delivery.sh set both claude-code` call.
- claude-code identity missing/multiple → correct warnings, no join executed.
- Bootstrap-only entry point performs no pane/layout/agent-start calls.
- Existing codex-gate and $HOME-guard tests stay green.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `Makefile`
- `scripts/` (only if a new shared bootstrap script is the chosen factoring)
- `tests/unit/` (test updates and new test modules)
- Expected artifact paths below; scratch dirs outside the repo for live E2E.

## Forbidden actions

- Do not modify `delivery.sh` or anything under `home/dot_agents/skills/agmsg/`
  (watcher kill-scoping is a tracked upstream issue).
- Do not run `delivery.sh set` against `/Users/mryfmo/Workspace/dotfiles`
  (already configured; the live orchestrator watcher must not be killed).
- No dependency/CI/permission changes, no local bats, no merge,
  no `make require-crit-review`.
- Do not touch the operator's live herdr workspace/panes.

## Validation (live E2E mandatory, record everything)

1. Unit tests green (`uv run python -m unittest ...`, `make unit-test`),
   `shellcheck`, `bash -n`.
2. Fresh scratch repo (git init, outside dotfiles): run the bootstrap entry
   point → `.codex/hooks.json` AND `.claude/settings.local.json` created with
   correct nested hook schemas; `delivery.sh status` reports codex=turn,
   claude-code=both.
3. Steady-state: re-run bootstrap and `make agmsg-bootstrap` in that scratch
   repo → zero `delivery.sh set` calls (prove via log/trace), started scratch
   watcher process survives.
4. `make update` and `make upgrade` dry paths: demonstrate the new step runs
   (in the scratch context or with the real run if safe) and degrades to a
   skip message when agmsg scripts are missing.
5. Clean up scratch repos/workspaces and any scratch watcher processes.

## Git / PR

- Separate git worktree from `main`, branch `feat/agmsg-setup-automation`,
  only this task's changes. Conventional Commit, English PR via `gh`,
  check GitHub Actions, fix until green. Report PR URL + CI status.

## Expected artifacts

- report: `.orchestration/reports/T20-agmsg-setup-automation.md`
- validation: `.orchestration/validation/T20-agmsg-setup-automation.md`
- sandbox: `.orchestration/sandboxes/T20-agmsg-setup-automation.md`
- learning: `.orchestration/learning/T20-agmsg-setup-automation.md`
- autoskill: `.orchestration/autoskill/runs/T20-agmsg-setup-automation.md`

Write artifacts under the MAIN worktree `.orchestration/`, uncommitted.

## Done signal

`AGMSG-RESULT v1 task_id=T20-agmsg-setup-automation status=ready_for_review|blocked`
with all artifact paths. max_turns=40.
