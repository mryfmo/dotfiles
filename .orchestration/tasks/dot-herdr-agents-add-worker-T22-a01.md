---
task_id: dot-herdr-agents-add-worker-T22-a01
revision: 4
supersedes: 1
created_at: 2026-09-26T01:55:00Z
---
# AGMSG-TASK dot-herdr-agents-add-worker-T22-a01 (revision 3): implement parallel workers as a herdr-agents mode on top of upstream agmsg `spawn`/`despawn` (no ad-hoc herdr CLI, no re-implemented seating)

Revision 2 note: upstream agmsg (v1.5.0) already seats agents in herdr — `spawn.sh <type> <name> --project <worktree> --terminal-driver herdr [--boot-prompt …]` creates the pane (`herdr tab create --workspace`/`pane split`), starts the CLI with the actas boot prompt, names the pane, writes the placement record and waits for the readiness sentinel; `despawn.sh` tears it down; there is no leader-side pane registration by design (#1152). herdr-agents must therefore CALL spawn/despawn for extra workers rather than re-implementing pane creation, and keep only what upstream does not do: worktree creation/validation, worker-kind profile args (`--model` for claude via spawn options or `HERDR_AGENTS_*`), `AGMSG_CC_MONITOR_KEEP_ALIVE=1` env, delivery mode per worktree, and our labels. Verify locally the herdr caveats (#1307 placement template ignored; `ops.sh` argv "ASSERTED, NOT measured"). Depends on T19 (upstream 1.5.0 installed).

Plan: `.agents/worklog/claude/remediation-plan-20260925.md` §Phase 3 (role/seat model) and the README design. Operator finding 2026-09-25: parallel workers were being created by improvised `herdr tab create`; the README states the design ("one git worktree equals one resident worker in its own tab/workspace; its pane receives the worktree through `herdr pane split <pane> --direction right --cwd <worktree>`; `herdr agent start <name> --kind <kind> --pane <id>`") but no script implements it, so every operator/orchestrator has to interpret it. Turn the design into code with tests and documentation, then forbid raw topology commands (T21 G7).

Repo: your own worktree (assigned at dispatch). Branch `feat/herdr-agents-add-worker` from origin/main (rebase after #182 and T21 land).

## Deliverables
1. `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile <p>]`: creates (or reuses) a **dedicated workspace** for `<worktree>` (`herdr workspace create --cwd <worktree> --label <worker label> --env HERDR_AGENTS_LAYOUT=managed --env HERDR_AGENTS_ROLE=worker …`), splits the worker pane from that workspace's root pane with `herdr pane split <root> --direction right --cwd <worktree>` exactly as README states (decide and document what the root pane is for — the README implies the same two-pane shape; if the root pane should host nothing, say so and keep it as the shell pane), starts the worker with `herdr agent start <name> --kind <kind> --pane <id> -- <profile args>`, handles the Claude trust dialog like the existing worker start, registers the worker's agmsg identity on the worktree path (`join.sh <team> <kind>-<profile>-<suffix>-aNNN <type> <worktree>` — reuse the existing suffix derivation; choose the next free `aNNN`) **with `AGMSG_RESOLVE_PROJECT=0` in the environment of that `join.sh` (or via `spawn.sh --project`, which sets it): upstream 1.5.0 project resolution (#92, docs/design.md) otherwise rewrites a nested or sibling worktree path to the registered main checkout and the worker collides with the orchestrator identity; `delivery.sh set` must also target the worktree path so `session-start.sh` bakes it into the per-process marker**, sets delivery for the worktree (`set turn codex` / `set both claude-code`), and prints the pane id + identity for the orchestrator. Idempotent: re-running for the same worktree reuses the workspace/pane/identity.
2. `herdr-agents --remove-worker <worktree>`: graceful teardown in the documented order (`delivery.sh set off`, `leave.sh`, `herdr workspace close`), refusing when the worktree has uncommitted changes unless `--force`.
3. Naming/labels consistent with the existing `<kind>-worker-<workspace_id>` convention; README herdr-agents section updated to describe the mode as the only sanctioned way to add parallel workers (and the ~3-worker ceiling); agmsg-orchestration SKILL "Parallel workers" section references it.
4. Tests: unit tests in `tests/unit/test_herdr_agents.py` with the existing fake-herdr harness for add/reuse/remove/refuse paths; live E2E in a scratch repo (fresh + restore), verbatim in validation; shellcheck/shfmt clean; validator ok.
5. pr-feedback sweep + CodeRabbit full review on the final head per the pr-integration rule.
6. Live verification carried over from T19 6(b)/(c) (waived there because the worker had no isolated herdr server): in the scratch herdr session used by deliverable 4, run `poke.sh` through the herdr driver against a scratch pane and record exit codes (10/12/13/14/15 semantics; does `herdr agent prompt` work on 0.9.1), and `peek.sh` rc on a closed pane (#1317). Verbatim in validation; failures become upstream issues (URLs in report) with repo-side mitigations only where upstream documents them.

## allowed_files
`home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `README.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md` (+ Codex mirror), artefacts.

## forbidden_actions
touching the live `wE` workspace or the `dotfiles` team registrations; `make update`; merging; local bats; force-push.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "parallel workers are added only via herdr-agents --add-worker (dedicated workspace + pane split --cwd + agent start + identity + delivery); raw herdr topology commands are denied to the orchestrator (G7)". RESULT via send.sh. max_turns=45.

## Revision history
- r2 (09-26 01:55Z): grounded in upstream v1.5.0 spawn/despawn.
- r3 (09-26 02:58Z): deliverable 1 requires `AGMSG_RESOLVE_PROJECT=0` for worker joins (T19 round-1 finding 11); deliverable 6 carries T19 6(b)/(c) live checks.

---

# Revision 4 (2026-09-29) — T34: seat the worker in its own worktree (root fix for the a005 delivery miss) and add parallel workers on upstream spawn/despawn

Revision 4 supersedes revision 3's deliverable list where they differ; the Facts, forbidden_actions and artefacts stand. Prerequisite met: upstream agmsg 1.5.0 is installed on this host (T19 #184, `~/.agents/skills/agmsg/VERSION` = 1.5.0; `spawn.sh`, `despawn.sh`, `poke.sh`, `doctor.sh` present). Evidence for the defect: `.orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md` and the T30/T31/T32/T33x acceptance records — the pair's worker pane runs with `--cwd <main checkout>`, so its SessionStart hook resolves the main-path identities while tasks address `claude-standard-dot-a005` registered at `.claude/worktrees/worker-c`; no watcher or Stop hook ever runs on that path, and every dispatch is found only by an explicit `inbox.sh`.

## Deliverable A (required) — the pair's worker pane is seated in its worktree

1. Manifest field `worker_worktree` in `home/dot_agents/agent-config.yaml` (default `.claude/worktrees/worker-c`, relative to the repository), rendered by `scripts/generate-agent-configs.py` into `~/.agents/model-profiles.env` as `HERDR_AGENTS_WORKER_WORKTREE` (same pattern as `worker_kind`/`worker_profile`; validator rule: relative path under `.claude/worktrees/`). No ad-hoc env overrides beyond the existing manifest→env path.
2. `herdr-agents` full mode, `--attach` worker repair and `--restart-worker`: the worker pane is created/started with `--cwd <repo>/<worker_worktree>` (create the worktree from `origin/main` with `git worktree add --detach` when missing; refuse when the path exists but is not a worktree of this repository). The worker identity is registered at that path with `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <kind>-<profile>-<suffix>-aNNN claude-code|codex <worktree>` (reuse the existing suffix derivation; next free `aNNN`), delivery is set at the worktree path (`set both claude-code` / `set turn codex`), and the pane env carries `AGMSG_CC_MONITOR_KEEP_ALIVE=1`. The T14 guard `require_distinct_worker_identity` becomes unnecessary for a worktree-seated worker (different path → different identity); keep it only for the legacy main-path case and say so.
3. Rules/SKILL/README: the interim "inbox.sh at each milestone" rule (T33a) is marked retired once the worker is worktree-seated; the delivery statement becomes "worker panes run in their worktree; turn delivery reaches them directly".
4. Tests (fake herdr harness, mutation baseline against the unmodified origin/main script): pane created with the worktree cwd; join called with `AGMSG_RESOLVE_PROJECT=0` and the worktree path; delivery set at the worktree path; worktree auto-created from origin/main when missing; refusal when the path is not a worktree; `--restart-worker` re-seats an existing main-path worker pane into the worktree (the migration this host needs).

## Deliverable B (required unless blocked) — parallel workers on upstream seating

5. `herdr-agents --add-worker <worktree> [--kind codex|claude] [--profile <p>]`: seat an additional resident worker through upstream `spawn.sh <type> <name> --project <worktree> --terminal-driver herdr` so a placement record exists and `poke.sh`/`despawn.sh` work. FIRST verify (read-only: `spawn.sh --help`, `scripts/drivers/types/*` manifests) whether spawn can launch the CLI with this repo's profile arguments (`MODEL_PROFILE_<P>_CLAUDE_ARGS` / `_CODEX_ARGS`: model + effort + advisor, not just `--model`). If it can, use it; if it can only pass `--model`, PONG with the manifest evidence and the options (a) spawn with a `--terminal` template wrapping our profile args, (b) seat via the existing `herdr agent start … -- <profile args>` and write the placement record through the upstream lib if it exposes a public writer — the orchestrator rules before you implement.
6. `herdr-agents --remove-worker <worktree>`: `despawn.sh <team> <leader> <name>` (graceful, `--force` passthrough), then `delivery.sh set off`, `leave.sh`, and `herdr workspace close` per the SKILL teardown order; refuse when the worktree has uncommitted changes unless `--force`.
7. README herdr-agents section + SKILL "Parallel workers": `--add-worker`/`--remove-worker` are the only sanctioned way to add or remove workers; the ~3-worker ceiling; raw herdr topology commands stay forbidden (T21 G7).
8. Tests for add (create/reuse/refuse) and remove (graceful/force/refuse-dirty) with fake `spawn.sh`/`despawn.sh`/herdr; shellcheck/shfmt clean; validator ok.

## Acceptance (orchestrator, live)

After merge and `chezmoi apply`: `herdr-agents --restart-worker` on this pair (wJ) re-seats the worker into `.claude/worktrees/worker-c`; a `PING` sent with `agmsg-dispatch` must then arrive as a turn/Monitor delivery WITHOUT the worker running `inbox.sh` (the defect's acceptance criterion); `identities.sh <worktree> claude-code` shows exactly one seat; `doctor.sh --project <worktree>` clean. Deliverable B live E2E (fresh + restore) follows in a scratch repo per revision 3.

## allowed_files (revision 4)

`home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `home/dot_agents/agent-config.yaml`, `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, `README.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_config/codex/AGENTS.md` (mirror sentences only), artefacts at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-herdr-agents-add-worker-T22-a01.md` (main checkout; append a "Revision 4" section).

## forbidden_actions (revision 4)

Touching the live `wJ` workspace or the `dotfiles` team registrations (use a scratch HOME/agmsg store for E2E); `make update`/`make upgrade`/`chezmoi apply`; merging; local bats; force-push except `--force-with-lease` on your own branch; raw herdr topology commands against real panes.

## Completion (revision 4)

Branch `feat/herdr-agents-worker-seat` from `origin/main`; PR (English, attribution); CI green; the five artefacts; CompactionDB decision from the main checkout with command and id pasted; `inbox.sh dotfiles claude-standard-dot-a005` at each milestone (still needed until this very change is deployed); `AGMSG-RESULT v1 revision=4`.

[memory:decision] T34/T22 r4: the herdr-agents worker pane is seated in its own worktree (manifest `worker_worktree` → `HERDR_AGENTS_WORKER_WORKTREE`), its identity registered there with `AGMSG_RESOLVE_PROJECT=0` and delivery set on that path, so task delivery reaches the worker as turn/Monitor events; parallel workers are added and removed only through `herdr-agents --add-worker/--remove-worker` on upstream `spawn.sh`/`despawn.sh` (operator 2026-09-29).

## Revision history (continued)
- r4 (09-29): T34 — worktree seating of the pair worker (root fix for the a005 delivery miss, T30–T33 evidence), `--add-worker/--remove-worker` on upstream 1.5.0 spawn/despawn with a profile-args verification gate, live acceptance criterion = delivery without inbox.sh.
