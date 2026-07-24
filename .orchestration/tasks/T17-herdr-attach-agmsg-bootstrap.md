# Orchestration task: T17 herdr --attach agmsg worker bootstrap + acceptance rule

## Assignment

- Task ID: `T17-herdr-attach-agmsg-bootstrap`
- Executor model: `gpt-5.6-sol`
- Reasoning effort: `high`
- Repo: `/Users/mryfmo/Workspace/dotfiles`, branch: continue on
  `feat/herdr-attach-order-repair` AFTER T16 is accepted (orchestrator will
  confirm in the AGMSG-TASK message; if told otherwise, branch from `main`).
- Pre-existing dirty/untracked paths (`home/dot_mise/*`, `.orchestration/`,
  `.agents/`, `plans/`, `docs/verification/`) are NOT yours.

## Problem (verified by orchestrator)

`herdr-agents` spawns a bare `codex` process (start_codex_agent). Nothing
wires the spawned worker into the agmsg bus: repo-scoped turn delivery
(`.codex/hooks.json`) only exists if someone ran `delivery.sh set turn codex
<repo>` manually, and nobody verifies the canonical worker identity is
registered. Result: "claude starts, codex pane appears, but agmsg
collaboration is not set up."

## Desired behavior (Fix B)

1. In `home/dot_local/bin/common/executable_herdr-agents`, after the codex
   agent is started OR reused (both attach mode and full mode), run a
   best-effort agmsg bootstrap:
   - If `~/.agents/skills/agmsg/scripts/delivery.sh` does not exist → skip
     silently (agmsg not installed; herdr-agents must keep working without it).
   - Run `delivery.sh set turn codex "${workdir}"` — idempotent; installs the
     repo-scoped `.codex/hooks.json` Stop hook so the worker auto-receives
     inbox messages each turn.
   - Verify a codex identity is registered for this repo via
     `identities.sh "${workdir}" codex`: if none, print a one-line stderr
     warning naming the join command; if multiple teams/agents, print a
     one-line stderr warning about ambiguity. Do NOT auto-join (team and
     identity naming need operator judgment per the agmsg-orchestration
     rule) and do NOT run actas-claim (requires the worker session id, which
     does not exist at spawn time).
   - Bootstrap failures must never break Claude startup or the layout:
     `|| true` semantics, output to the existing herdr-agents log path
     convention.
2. Fast no-op path (`--attach` outside herdr, `HERDR_AGENTS_LAYOUT=managed`)
   unchanged and still first — no agmsg calls there.

## Desired behavior (Fix C)

3. In `home/dot_config/claude/rules/agmsg-orchestration.md`, add ONE concise
   bullet to the existing list: acceptance of tasks that change live desktop
   behavior (herdr layout/session, pane lifecycle, delivery hooks) requires
   the orchestrator to run a live end-to-end verification covering BOTH a
   fresh session and a persisted-session restore before ACCEPT; unit tests
   and static checks alone are insufficient. Match the file's existing tone
   and formatting; keep it to one bullet.

## Test requirement

Update `tests/unit/test_herdr_agents.py` FIRST (failing tests, existing
mocking approach): (a) bootstrap invoked with the right args after codex
start/reuse in attach mode; (b) skipped silently when delivery.sh is absent;
(c) a failing bootstrap does not fail the script. Existing tests still pass.

## Constraints

- allowed_files:
  - `home/dot_local/bin/common/executable_herdr-agents`
  - `home/dot_config/claude/rules/agmsg-orchestration.md`
  - `tests/unit/test_herdr_agents.py`
  - the artifact paths below
- forbidden_actions: `git-commit-push (until orchestrator authorizes);
chezmoi-apply; live-herdr-mutation (read-only herdr CLI allowed);
agmsg-state-mutation (do not run delivery.sh set / join.sh / send.sh against
the live store yourself — reading scripts and --help is fine);
deps-or-ci-changes; llm-calls; edits-outside-allowed-files`
- Live E2E is the orchestrator's job after acceptance.

## Validation commands (full output into the validation artifact)

- `uv run python -m unittest tests.unit.test_herdr_agents -v`
- `make unit-test`
- `uv run --with pyyaml scripts/validate-agent-assets.py`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents` (record availability)
- `bash -n home/dot_local/bin/common/executable_herdr-agents`
- `git status --short` (only allowed files)

## Expected artifacts

- report: `.orchestration/reports/T17-herdr-attach-agmsg-bootstrap.md`
- validation: `.orchestration/validation/T17-herdr-attach-agmsg-bootstrap.md`
- sandbox: `.orchestration/sandboxes/T17-herdr-attach-agmsg-bootstrap.md`
- learning: `.orchestration/learning/T17-herdr-attach-agmsg-bootstrap.md`
- autoskill: `.orchestration/autoskill/runs/T17-herdr-attach-agmsg-bootstrap.md`

## STOP conditions

- `delivery.sh set turn` is not idempotent or has side effects that could
  kill live watchers per its own documentation → STOP and report evidence.
- The rules file is generated/managed such that direct edits are forbidden
  (check for a managed-baseline mechanism first) → STOP and report the
  actual surface.

When done send: `AGMSG-RESULT v1 task_id=T17-herdr-attach-agmsg-bootstrap status=ready_for_review report=... validation=... sandbox=... learning=... autoskill=...`
