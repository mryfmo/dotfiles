# AGMSG-TASK dot-herdr-worker-relaunch-T25-a01

## Objective

Operator correction (2026-09-27): the orchestrator/worker pair must always
live in ONE herdr workspace, and worker (re)launch must be documented, ruled,
and checked in the repository — not left as session memory.

Observed failure being codified (see
`.orchestration/learning/rule_candidates/herdr-worker-relaunch.md`): after the
worker agent was exited, `herdr-agents <DIR>` (full mode) run from inside the
pair workspace created a duplicate workspace with its own orchestrator pane,
because the exited worker had left `<ws>:p2` as an agentless labeled shell
pane; `--attach` then refused ("panes are ambiguous or include unmanaged
panes"). Recovery required `/exit` prompts plus `herdr workspace close`.

[memory:decision] T25: worker relaunch and the one-workspace-per-pair
invariant are enforced in herdr-agents itself (restart mode + full-mode
duplicate guard), documented in README, ruled in agmsg-orchestration.md, and
checked by validator + unit tests (operator 2026-09-27).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`
  (currently detached at 47d76b8; no uncommitted files expected — if any
  exist, stop and report via AGMSG-PONG).
- `git fetch origin`, then `git switch -c feat/herdr-worker-relaunch origin/main`.
- `.orchestration` artifacts go to the main checkout paths below.

## Deliverables

### 1. `home/dot_local/bin/common/executable_herdr-agents`

a. New mode `herdr-agents --restart-worker [DIR]` (DIR defaults to the current
directory, like full mode):

- Locate the managed pair workspace for DIR (orchestrator pane labeled
  `claude-orchestrator`, worker pane labeled `<kind>-worker` /
  `claude-worker`, panes' cwd = DIR). Exit 2 with a clear message when no
  managed workspace exists (point at full mode) or when the layout is
  ambiguous (unmanaged/extra panes), consistent with attach-mode refusals.
- If a worker agent is running in the worker pane, stop it with
  `herdr agent prompt <pane> "/exit"` and wait (bounded, reuse existing
  wait helpers) until the agent is gone; then start the worker in the SAME
  pane via the existing start path (`start_worker_agent` /
  `herdr agent start <name> --kind <worker_kind> --pane <id>` with profile
  args resolved through `resolve_worker_profile` /
  `MODEL_PROFILE_<PROFILE>_CLAUDE_ARGS`), including the existing claude
  workspace-trust dialog handling. Never create panes or workspaces in
  this mode.
  b. Full-mode duplicate guard: when a herdr-agents-managed workspace for DIR
  already exists, full mode must never create a second workspace. It heals
  the existing one — including the previously-unhandled case of an
  agentless labeled worker pane, which it reuses by starting the worker
  agent in place (same code path as --restart-worker) — or exits 2 with an
  instructive message. Preserve the existing behavior of leaving unmanaged
  panes untouched.
  c. Update the usage/help text and shdoc comments (English) for both changes.

### 2. Documentation: `README.md`

In the herdr-agents section, document: the one-workspace-per-pair invariant
(never run full mode from inside the pair), `--restart-worker` and when to use
it (e.g. after a `worker_profile`/`worker_kind` change so new launch args take
effect), and stray-workspace teardown (`herdr agent prompt <pane> "/exit"`
then `herdr workspace close <id>`).

### 3. Rule: `home/dot_config/claude/rules/agmsg-orchestration.md`

Add one bullet to the existing list: worker pane (re)launches go only through
`herdr-agents` modes (full/attach/`--restart-worker`); never run full mode
from inside an existing pair workspace; a worker model/profile change is
activated with `--restart-worker`, with launch args sourced from
`~/.agents/model-profiles.env`, never ad-hoc flags.

### 4. Check: `scripts/validate-agent-assets.py`

Mirror the existing worker_kind README check: fail when `README.md` does not
mention `--restart-worker` in the herdr-agents documentation (simple token
check with a truthful message). Keep it minimal — no new config surface.

### 5. Tests

- `tests/unit/test_herdr_agents.py`: (a) `--restart-worker` restarts the
  worker in the existing pane with the resolved profile args (fake herdr
  binary pattern already used by the suite); (b) `--restart-worker` exits 2
  when no managed workspace exists; (c) full mode with an existing managed
  workspace for DIR does not create a new workspace and starts the worker in
  the agentless labeled pane; (d) existing tests stay green.
- `tests/unit/test_validate_agent_assets.py`: README missing
  `--restart-worker` fails validation.
- Do not run bats locally (repo policy); CI covers lifecycle.bats. If
  lifecycle.bats asserts full-mode behavior that the guard changes, update it
  in the same PR (allowed below) and let CI verify.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `README.md`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `scripts/validate-agent-assets.py`
- `tests/unit/test_herdr_agents.py`
- `tests/unit/test_validate_agent_assets.py`
- `tests/install/common/lifecycle.bats` (only if its existing assertions
  conflict with the new guard)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-herdr-worker-relaunch-T25-a01.md` (main checkout)

## Forbidden actions

- Touching `home/dot_agents/agent-config.yaml`, generated outputs, permgate,
  hooks configs, dependency changes, or anything under `reviews/ADH_Integrated_Plan/`.
- Merging the PR; force push; local bats; `make apply`/`chezmoi apply`; any
  write outside the repo worktree except the listed `.orchestration` paths.
- Killing panes/workspaces or driving the live herdr session for testing —
  unit tests use the fake-binary pattern only.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck home/dot_local/bin/common/executable_herdr-agents
git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description, ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI; fix and re-push until green.
2. Artifacts at the exact expected paths; validation contains every command's
   verbatim output and the PR number/head SHA.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T25: herdr-agents gains --restart-worker and a full-mode duplicate-workspace guard; README/rule/validator/tests codify the one-workspace-per-pair invariant (operator 2026-09-27)"`
   — paste the command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `status=blocked` with report if
   stuck. Include a `cost:` line in the report.
