# AGMSG-TASK dot-worker-kind-guard-T14-a01: worker_kind validation and the same-type identity guard (plan Phase 1.2 / 1.3)

Plan: `/home/moriya/Workspace/dotfiles/.agents/worklog/claude/remediation-plan-20260925.md` §Phase 1 (1.2, 1.3). Read the plan's §0 and §2 first so the guard's message states the real problem.
Repo (your worktree): `/home/moriya/Workspace/dotfiles/.claude/worktrees/env-converge-T10`. You are `claude-standard-dot-a003`.

## Preparation (your worktree currently holds PR #179's branch with one uncommitted bats fix)

1. `git status --porcelain` — expect only `tests/install/ubuntu/common/bwrap_apparmor.bats` modified.
2. Commit it on the current branch `feat/claude-sandbox-manifest` as `test(install): capture the fake sudo log on stderr in bwrap_apparmor.bats` (no push; PR #179 is parked for Phase 4).
3. `git fetch origin && git switch -c fix/worker-kind-guard origin/main`.

## 1.2 — validator and README consistency (worker_kind stays `claude` for now; the operator decides the value after Codex login)

- `scripts/validate-agent-assets.py`: in the manifest validation, require `worker_kind` present and in `{"codex", "claude"}`; fail otherwise. Also require that README.md's herdr-agents section states the same current value as the manifest (today README L303 says "currently `claude`"); implement as: extract the manifest value and assert the literal ``(currently `<value>`;`` appears in README.md. Keep it that simple.
- `tests/unit/test_validate_agent_assets.py`: positive case, invalid value case, README mismatch case.
- `README.md` L328: the worker profile default is documented as `standard`; the code default is `MODEL_PROFILE_INTERACTIVE` from `~/.agents/model-profiles.env` (H:73-89), `standard` only when the env file is absent. Fix the sentence to match the code.

## 1.3 — temporary same-type identity guard in `home/dot_local/bin/common/executable_herdr-agents`

Facts: agmsg identity resolves by (project path, agent type). With `worker_kind=claude`, orchestrator and worker are both `claude-code` on the same `workdir`, and `whoami.sh` returns `multiple=true` or the orchestrator's single name for both. Phase 3 replaces this with the upstream agmsg role/seat model; this guard only stops the silent collision until then.

- Add `worker_agmsg_type()`: `codex` → `codex`, `claude` → `claude-code`.
- Before starting or reusing a worker pane (both full mode and `--attach`), if `worker_agmsg_type == claude-code` (same as the orchestrator's type) then run `identities.sh "${workdir}" claude-code`, count distinct names in column 2. If the count is `< 2`, print to stderr:
  `herdr-agents: worker_kind=claude would share the orchestrator's agmsg identity on <workdir> (only <n> claude-code identity registered). Register a worker role first (join.sh <team> <role> claude-code <workdir>) or use worker_kind=codex. See remediation-plan-20260925.md §Phase 3.` and exit 2. If `>= 2`, continue (Phase 3 will make this the normal path).
- The guard must not run for `worker_kind=codex`.
- `bootstrap_agmsg`: when `worker_kind=claude`, treat exactly two distinct claude-code names as healthy (no "Multiple identities ... ambiguous" warning) and do not print the "No agmsg Codex identity" hint nor create `.codex/hooks.json`. Keep current behaviour for `worker_kind=codex`.
- Tests in `tests/unit/test_herdr_agents.py` using the existing fake `identities.sh` pattern: (a) claude kind + one claude-code identity → exit 2 with the message, no pane split/agent start; (b) claude kind + two identities → proceeds; (c) codex kind → unaffected; (d) bootstrap with claude kind and two names → no warning; (e) bootstrap with claude kind does not touch `.codex/hooks.json`. shdoc English comments for new functions.
- Bats: if a bats file covers herdr-agents, add one case; do not run bats locally.

## Validation (verbatim in the validation file)

`uv run --with pyyaml scripts/validate-agent-assets.py`; `python3 -m unittest tests.unit.test_herdr_agents tests.unit.test_validate_agent_assets tests.unit.test_generate_agent_configs -q`; `git diff --stat origin/main...HEAD`; `gh pr checks <n>` final table.

## Commit / PR

Two commits: `fix(validate): constrain worker_kind and keep README in step with the manifest`, `fix(herdr-agents): refuse a same-type worker that would share the orchestrator agmsg identity`. Push `fix/worker-kind-guard`, PR in English (problem, guard semantics, tests), `gh pr checks --watch`, final table. On CI failure fix within allowed_files (fixture bugs count as within scope) or report blocked.

## allowed_files

`scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, `README.md`, `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, one bats file (name it), the artefacts. The preparation commit touches only `tests/install/ubuntu/common/bwrap_apparmor.bats` on the parked branch.

## forbidden_actions

changing `worker_kind`'s value; pushing `feat/claude-sandbox-manifest`; merging; `make update`/`make upgrade`/`chezmoi apply`; writes outside your worktree except artefacts; local bats; force-push.

## Artefacts (in `/home/moriya/Workspace/dotfiles`)

report/validation/sandbox/learning/autoskill at `.orchestration/<dir>/dot-worker-kind-guard-T14-a01.md`. `[memory:decision]`: "worker_kind is validated to codex|claude and README must state the manifest value; a same-type claude worker is refused unless a second claude-code identity (worker role) is registered on the workdir (temporary guard until the agmsg role model, plan Phase 3)". `contextdb_cli.py memory add` from the main checkout; paste command and output.

## Done signal

`AGMSG-RESULT v1 task_id=dot-worker-kind-guard-T14-a01 status=ready_for_review|blocked pr=<n> report=... validation=... sandbox=... learning=... autoskill=...` via `send.sh dotfiles claude-standard-dot-a003 claude-remediation-dot "<message>"`. max_turns=30.
