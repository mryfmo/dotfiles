# AGMSG-TASK dot-orchestrator-pane-profile-args-T47-a01

## Objective

The `herdr-agents` orchestrator pane (p1) comes up on the organization's default
model instead of the interactive profile. Observed 2026-09-30: the pair launched
by `herdr-agents` from Herdr put the orchestrator on `claude-sonnet-5-5` (27/27
turns, session e7734322) while `~/.claude/settings.json` says
`model: claude-fable-5-1`, and Claude Code itself reported "Your organization's
default (`Sonnet 5.5`) applies on restart" (`~/.claude.json`
`orgModelDefaultCache.override_user_selection = true`). The worker pane launched
the same evening with `--model claude-opus-5-5` from
`MODEL_PROFILE_STANDARD_CLAUDE_ARGS` ran 189/189 turns on opus. Only the
orchestrator pane lacks the flag:

- `home/dot_local/bin/common/executable_herdr-agents` `start_claude_in_pane`
  (:606-627) starts a bare `claude` unless `HERDR_AGENTS_CLAUDE_ARGS` is set;
- `start_worker_agent` (:654-675) sources `~/.agents/model-profiles.env` and
  passes `MODEL_PROFILE_<PROFILE>_CLAUDE_ARGS` to `start_agent_in_pane`.

Make the orchestrator pane resolve its profile the same way. Model IDs stay in
`model_profiles` (`agent-config.yaml`); the launcher only forwards the rendered
env, exactly as it already does for workers.

Deliver:

1. `home/dot_local/bin/common/executable_herdr-agents`
   - `start_claude_in_pane`: source `${HOME}/.agents/model-profiles.env` when
     present (same pattern as `start_worker_agent`), read
     `MODEL_PROFILE_${MODEL_PROFILE_INTERACTIVE^^}_CLAUDE_ARGS` (empty
     `MODEL_PROFILE_INTERACTIVE` → no profile args, no error), then append
     `HERDR_AGENTS_CLAUDE_ARGS` **after** the profile args (mirrors the worker's
     `HERDR_AGENTS_CLAUDE_WORKER_ARGS`). Both call sites (full mode :1822, the
     `--attach` heal when p1 has no Claude :1784) go through this function; do
     not add a second code path.
   - Header: update `@arg HERDR_AGENTS_CLAUDE_ARGS` (:45-47) to "appended after
     the interactive profile args" and add one `@description` sentence naming
     `MODEL_PROFILE_INTERACTIVE` as the orchestrator pane's profile source.
   - Print one summary line when the orchestrator agent is started:
     `orchestrator_profile=<name|none> args=<rendered args or none>` (stdout,
     same style as the existing summary lines). Never print secrets; the env
     file holds model names and flags only.
2. `tests/unit/test_herdr_agents.py`
   - New test: fake `$HOME/.agents/model-profiles.env` with
     `MODEL_PROFILE_INTERACTIVE="deep"` and
     `MODEL_PROFILE_DEEP_CLAUDE_ARGS="--model claude-fable-5-1 --effort high --advisor fable"`;
     full mode; the calls log (`herdr-calls.txt`) contains
     `agent start claude-orchestrator-w-test --kind claude --pane w-test:p1 --timeout 30000 -- --model claude-fable-5-1 --effort high --advisor fable`.
   - New test: same env file plus `HERDR_AGENTS_CLAUDE_ARGS="--model haiku --effort low"`
     → the `--` tail is `--model claude-fable-5-1 --effort high --advisor fable --model haiku --effort low`
     (profile first, override appended; Claude takes the last `--model`).
   - Existing `test_claude_agent_accepts_manifest_profile_arguments_for_e2e`
     (:1490-1499) pins `-- --model haiku --effort low`. Keep it green as is if the
     test HOME has no env file; if you must change its expectation, say exactly
     why in the report.
   - Reuse the existing fakes (fake `herdr` argv capture at line ~114 →
     `herdr-calls.txt`); never touch a live pane.
3. `make unit-test`, `make validate-agent-assets`,
   `shellcheck home/dot_local/bin/common/executable_herdr-agents` green.
   PR (English) from `fix/orchestrator-pane-profile-args`.

Out of scope: model/profile values, `agent-config.yaml`, `model-profiles.env`,
`settings.json`, sandbox settings, the organization default itself (operator
lane), automatic seating, the Understand-Anything hook. A bare `claude` typed
outside `herdr-agents` still gets the organization default; do not try to fix
that here.

[memory:decision] T47: `herdr-agents` starts the orchestrator pane with
`MODEL_PROFILE_<MODEL_PROFILE_INTERACTIVE>_CLAUDE_ARGS` from
`~/.agents/model-profiles.env`, then appends `HERDR_AGENTS_CLAUDE_ARGS`; a
`settings.json` model alone loses to an organization default with
`override_user_selection` (observed 2026-09-30, session e7734322 on Sonnet 5.5
while settings said fable-5-1).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.
- Branch `fix/orchestrator-pane-profile-args` from `origin/main` (`git fetch`
  first). The worktree currently sits on `fix/plain-start-visibility` (T45 WIP,
  PR #216, head 89e95e4, clean of tracked changes): switch branches, do not
  touch that branch or PR. T45 resumes after this task.
- `git status` may list nobody-owned zero-byte character-device entries
  (`.bashrc`, `.zshrc`, `.gitconfig`, `.mcp.json`, `.claude/launch.json`, …):
  they are Claude-sandbox deny-mount stubs (T39), not dirt. Use explicit-path
  `git add`; never `git add -A`.
- Run config-writing git outside the sandbox and push without `-u` (T39
  `.git/config.lock` hazard); never remove `.git/*.lock`.
- Ignore the Understand-Anything auto-update hook.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestrator-pane-profile-args-T47-a01.md`
- `.agents/worklog/codex/**` waived.

## Forbidden actions

- Editing any model or profile value (`agent-config.yaml`,
  `model-profiles.env`, `settings.json`, `generate-agent-configs.py`), sandbox
  settings, or anything under `~/.agents/skills/agmsg/` (upstream).
- Pane reads; merge; force-push; `--delete-branch`; editing
  `.orchestration/acceptance/**`; local `bats`; touching
  `fix/plain-start-visibility`.
- Escalating any action outside the sandbox/allowlist for approval: fail it,
  send `AGMSG-PONG v1 status=blocked` with the exact command and boundary.

## Validation commands (verbatim output into the validation file)

- `make unit-test`
- `make validate-agent-assets`
- `shellcheck home/dot_local/bin/common/executable_herdr-agents`
- `git diff --stat origin/main...HEAD`
- `gh pr view <n> --json url,headRefOid,mergeStateStatus`
- `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] above>"`

## Expected artifacts

- report/validation/sandbox/learning/autoskill at the paths above; report
  carries `cost:`, PR URL, head sha, the CompactionDB command.

max_turns=30. done_signal=AGMSG-RESULT v1.
