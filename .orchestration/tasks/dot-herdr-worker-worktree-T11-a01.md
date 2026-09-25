# AGMSG-TASK dot-herdr-worker-worktree-T11-a01: run the herdr worker pane in a dedicated worktree with its own agmsg identity (plan part B1)

Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/melodic-conjuring-sifakis.md` §B1.
Repo (your worktree): `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10` (the same nested worktree used for T10), branch `fix/herdr-agents-worker-worktree`: create it with `git switch -c fix/herdr-agents-worker-worktree origin/main` after the T10 branch has been pushed and the tree is clean. `cd` there first. You are `claude-standard-dot-a003`.

## Problem (verified 2026-09-25)

`home/dot_local/bin/common/executable_herdr-agents` starts the worker pane with `--cwd "${workdir}"` (L155/L157), the same directory as the orchestrator pane. agmsg resolves identity by (project path, agent type). With `worker_kind=claude` (the manifest default now) orchestrator and worker share (path, type), so `whoami.sh /home/moriya/Workspace/dotfiles claude-code` returns the orchestrator identity for both panes, and `bootstrap_agmsg()` (L510–) cannot tell them apart. The agmsg-orchestration rules already require one resident worker per git worktree with `project` = that worktree path; herdr-agents predates `worker_kind=claude` and does not implement it.

## Required design

1. **Worker worktree.** The worker pane's cwd is a dedicated git worktree **inside the repository**, default `<workdir>/.claude/worktrees/worker` (this repository's established convention: `.git/info/exclude` already ignores `**/.claude/worktrees/`, and #176 made the validator skip nested git trees; T9 used `.claude/worktrees/ua-full`). Override with `HERDR_AGENTS_WORKER_WORKTREE=<path>`. If the path exists and is a worktree of the same repository, reuse it; if missing, create it with `git -C <workdir> worktree add <path> -b <branch> origin/main` where `<branch>` defaults to `worker/<basename of path>` (override `HERDR_AGENTS_WORKER_BRANCH`). If it exists but is not a worktree of this repository, refuse with a clear message. Because the worktree is nested, verify `git check-ignore -q <path>` succeeds before creating it and refuse otherwise (an unignored nested tree would pollute `git status` and the scans).
2. **Worker identity.** Register `<worker_kind>-standard-<suffix>-a001` on the worker worktree path (`join.sh <team> <name> <type> <worktree>`), where `<suffix>` is derived exactly as the existing orchestrator identity derives it (read how `claude-remediation-dot`/`codex-standard-dot` are formed today; do not invent a new scheme) and `<type>` is `claude-code` or `codex`. If an identity already exists for (worktree, type), reuse it. Run `delivery.sh set turn <type> <worktree>` (codex) or `set both` (claude-code) against the worktree path, not `${workdir}`.
3. **Collision guard.** `bootstrap_agmsg` checks the orchestrator path and the worker path separately. If the worker kind's agent type equals the orchestrator's type *and* the worker path equals the orchestrator path, exit non-zero with: `herdr-agents: worker and orchestrator would share agmsg identity (<path>, <type>); set HERDR_AGENTS_WORKER_WORKTREE or use a different worker kind`. Keep the existing "Multiple identities" warning semantics (distinct names in TSV column 2).
4. **Codex kind.** `worker_kind=codex` follows the same worktree rule (the rule is kind-independent). Document the behaviour change in README.md (herdr-agents section) and in `home/dot_agents/skills/agmsg-orchestration/SKILL.md` where worker setup is described.
5. **Attach / repair paths.** `--attach`, `find_existing_workspace`, `live_worker_pane_id`, and the repair functions must recognise the worker pane by its worktree cwd, not by `${workdir}`. Trace every `jq ... select(.cwd == $cwd)` and every `${workdir}` use in the file and decide each one explicitly; list the decisions in the report.
6. **Docs.** shdoc-compatible English comments for every new/changed function (`@description`, `@arg`, `@example`). Update the usage() text and the `@arg` header for the new env vars.

## Tests (write first, red → green, evidence in validation)

- `tests/unit/test_herdr_agents.py`: add cases for (a) default worktree path derivation, (b) `HERDR_AGENTS_WORKER_WORKTREE` override, (c) collision guard message and non-zero exit, (d) identity name derivation for claude and codex kinds, (e) delivery invoked against the worktree path. Follow the existing test style in that file (it already exercises `bootstrap_agmsg` with fakes).
- `tests/install/common/lifecycle.bats` or the bats file that covers herdr-agents: add one case for the collision guard. Do **not** run bats locally (repo policy); CI runs it.
- `python3 scripts/validate-agent-assets.py` must pass.
- `python3 -m unittest tests.unit.test_herdr_agents tests.unit.test_runtime_health -q` output pasted verbatim.

## Live E2E (required by the agmsg rules before acceptance; do it, paste verbatim)

Use a throwaway directory under the scratchpad (`/tmp/claude-1000/-home-moriya-Workspace-dotfiles/5277c0a1-6279-4940-bf08-6a23b59b5b84/scratchpad/herdr-e2e-<ts>`) initialised as a git repo with an `origin` remote pointing at a bare clone, so no real repository is touched. Run the modified script from your worktree (`/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10/home/dot_local/bin/common/executable_herdr-agents <dir>`) with `HERDR_AGENTS_WORKER_KIND=claude` and express-profile arguments (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` from `~/.agents/model-profiles.env`; never ad-hoc `--model`). Record:
1. fresh session: `herdr agent list` shows orchestrator and worker with different `cwd`; `whoami.sh <worker worktree> claude-code` returns the worker identity; `identities.sh <dir> claude-code` and `identities.sh <worker worktree> claude-code` each return one line.
2. persisted-session restore: close and re-attach (`herdr-agents --attach` in the same workspace) and show the same three facts again.
3. teardown: `delivery.sh set off claude-code <worker worktree>`, `leave.sh <team> <worker identity>`, `herdr workspace close`, remove the scratch dirs. `identities.sh` for the scratch paths returns nothing.
Do not touch the live `wE` workspace or the `dotfiles` team registrations.

## Commit / PR

One or more commits, conventional-commit style, e.g. `fix(herdr-agents): run the worker pane in a dedicated worktree with its own agmsg identity`. Push `fix/herdr-agents-worker-worktree`, open the PR (English; body explains the collision, the design above, and the E2E evidence; end with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`), `gh pr checks --watch`, paste the final table. Fix CI failures within allowed_files.

## allowed_files

`home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `tests/install/common/lifecycle.bats` (or the bats file that already covers herdr-agents — name it in the report), `README.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, and the five artefact files. If `scripts/validate-agent-assets.py` forces a change elsewhere, stop and report `blocked` with the reason.

## forbidden_actions

merging the PR; writes outside `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10` except the artefacts and the scratchpad E2E dirs; `chezmoi apply`; `make update`; touching `~/.local/share/chezmoi`, `~/.config/herdr/config.toml`, the live `wE` workspace, or the `dotfiles` team registrations; local bats; force-push; ad-hoc `--model` flags.

## Artefacts (in the main checkout `/home/moriya/Workspace/dotfiles`)

report `.orchestration/reports/dot-herdr-worker-worktree-T11-a01.md` (design decisions per `${workdir}` use, PR URL, commit hashes, `[memory:decision]`: "herdr worker panes run in a dedicated worktree registered as <kind>-standard-<suffix>-aNNN; same (path,type) as the orchestrator is refused"), validation `.orchestration/validation/...`, sandbox, learning, autoskill (same basename). Run `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "..."` from the main checkout; paste command and output into the validation file.

## Done signal

`AGMSG-RESULT v1 task_id=dot-herdr-worker-worktree-T11-a01 status=ready_for_review|blocked pr=<n> report=... validation=... sandbox=... learning=... autoskill=...` via `send.sh dotfiles claude-standard-dot-a003 claude-remediation-dot "<message>"`. max_turns=40.
