---
task_id: dot-herdr-agents-add-worker-T22-a01
revision: 2
supersedes: 1
created_at: 2026-09-26T01:55:00Z
---
# AGMSG-TASK dot-herdr-agents-add-worker-T22-a01 (revision 2): implement parallel workers as a herdr-agents mode on top of upstream agmsg `spawn`/`despawn` (no ad-hoc herdr CLI, no re-implemented seating)

Revision 2 note: upstream agmsg (v1.5.0) already seats agents in herdr — `spawn.sh <type> <name> --project <worktree> --terminal-driver herdr [--boot-prompt …]` creates the pane (`herdr tab create --workspace`/`pane split`), starts the CLI with the actas boot prompt, names the pane, writes the placement record and waits for the readiness sentinel; `despawn.sh` tears it down; there is no leader-side pane registration by design (#1152). herdr-agents must therefore CALL spawn/despawn for extra workers rather than re-implementing pane creation, and keep only what upstream does not do: worktree creation/validation, worker-kind profile args (`--model` for claude via spawn options or `HERDR_AGENTS_*`), `AGMSG_CC_MONITOR_KEEP_ALIVE=1` env, delivery mode per worktree, and our labels. Verify locally the herdr caveats (#1307 placement template ignored; `ops.sh` argv "ASSERTED, NOT measured"). Depends on T19 (upstream 1.5.0 installed).

Plan: `.agents/worklog/claude/remediation-plan-20260925.md` §Phase 3 (role/seat model) and the README design. Operator finding 2026-09-25: parallel workers were being created by improvised `herdr tab create`; the README states the design ("one git worktree equals one resident worker in its own tab/workspace; its pane receives the worktree through `herdr pane split <pane> --direction right --cwd <worktree>`; `herdr agent start <name> --kind <kind> --pane <id>`") but no script implements it, so every operator/orchestrator has to interpret it. Turn the design into code with tests and documentation, then forbid raw topology commands (T21 G7).

Repo: your own worktree (assigned at dispatch). Branch `feat/herdr-agents-add-worker` from origin/main (rebase after #182 and T21 land).

## Deliverables
1. `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile <p>]`: creates (or reuses) a **dedicated workspace** for `<worktree>` (`herdr workspace create --cwd <worktree> --label <worker label> --env HERDR_AGENTS_LAYOUT=managed --env HERDR_AGENTS_ROLE=worker …`), splits the worker pane from that workspace's root pane with `herdr pane split <root> --direction right --cwd <worktree>` exactly as README states (decide and document what the root pane is for — the README implies the same two-pane shape; if the root pane should host nothing, say so and keep it as the shell pane), starts the worker with `herdr agent start <name> --kind <kind> --pane <id> -- <profile args>`, handles the Claude trust dialog like the existing worker start, registers the worker's agmsg identity on the worktree path (`join.sh <team> <kind>-<profile>-<suffix>-aNNN <type> <worktree>` — reuse the existing suffix derivation; choose the next free `aNNN`), sets delivery for the worktree (`set turn codex` / `set both claude-code`), and prints the pane id + identity for the orchestrator. Idempotent: re-running for the same worktree reuses the workspace/pane/identity.
2. `herdr-agents --remove-worker <worktree>`: graceful teardown in the documented order (`delivery.sh set off`, `leave.sh`, `herdr workspace close`), refusing when the worktree has uncommitted changes unless `--force`.
3. Naming/labels consistent with the existing `<kind>-worker-<workspace_id>` convention; README herdr-agents section updated to describe the mode as the only sanctioned way to add parallel workers (and the ~3-worker ceiling); agmsg-orchestration SKILL "Parallel workers" section references it.
4. Tests: unit tests in `tests/unit/test_herdr_agents.py` with the existing fake-herdr harness for add/reuse/remove/refuse paths; live E2E in a scratch repo (fresh + restore), verbatim in validation; shellcheck/shfmt clean; validator ok.
5. pr-feedback sweep + CodeRabbit full review on the final head per the pr-integration rule.

## allowed_files
`home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `README.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md` (+ Codex mirror), artefacts.

## forbidden_actions
touching the live `wE` workspace or the `dotfiles` team registrations; `make update`; merging; local bats; force-push.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "parallel workers are added only via herdr-agents --add-worker (dedicated workspace + pane split --cwd + agent start + identity + delivery); raw herdr topology commands are denied to the orchestrator (G7)". RESULT via send.sh. max_turns=45.
