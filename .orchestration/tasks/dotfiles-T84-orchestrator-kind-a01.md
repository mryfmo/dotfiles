# AGMSG-TASK dotfiles-T84-orchestrator-kind-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 7, dotfiles-T84). Depends on T80 (merged). Shares `home/dot_agents/agent-config.yaml`, the generator and the validator with T81 and T82; dispatch after both merge.

## Objective

Principle 4 (the same harness on both hosts, in both directions): the manifest names which runtime orchestrates, so T85/T86 can launch a Codex orchestrator without ad-hoc flags.

1. **Manifest** (`home/dot_agents/agent-config.yaml`, next to `worker_kind`): `orchestrator_kind: claude` with a comment mirroring `worker_kind`'s (allowed `claude` or `codex`; `codex` means the pair is driven by `codex-orchestrate`, T86).
2. **Generator** (`scripts/generate-agent-configs.py`): an `orchestrator_kind(manifest)` accessor with default `claude` and the same validation shape as `worker_kind`; `render_model_profiles_env` emits `HERDR_AGENTS_ORCHESTRATOR_KIND="<kind>"` next to `HERDR_AGENTS_WORKER_KIND`. Regenerate `home/dot_agents/model-profiles.env`.
3. **Validator** (`scripts/validate-agent-assets.py`): `orchestrator_kind` must be `claude` or `codex` (like the `worker_kind` check); the rendered env must carry the token; README states the current value the way it states `worker_kind` (`(currently \`claude\`;`), one sentence next to the existing `worker_kind` sentence (README allowed for that sentence only).
4. **Tests:** `tests/unit/test_generate_agent_configs.py` (default, explicit codex, rejected value, env line) and `tests/unit/test_validate_agent_assets.py` (rejected value, README sentence).
5. `herdr-agents` is untouched (T85 consumes the variable).

Forbidden: `home/dot_local/bin/common/executable_herdr-agents`; any profile; any hook.

[memory:decision] dotfiles-T84 (operator 2026-10-03): the manifest's `orchestrator_kind` (claude or codex, default claude) renders to `HERDR_AGENTS_ORCHESTRATOR_KIND` in `model-profiles.env`; the launcher (T85) and `codex-orchestrate` (T86) read it there and never from ad-hoc exports.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/orchestrator-kind --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the new key and comment), `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `home/dot_agents/model-profiles.env` (generator output), `README.md` (the one sentence), `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T84-orchestrator-kind-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
make validate-agent-assets
grep -n HERDR_AGENTS_ORCHESTRATOR_KIND home/dot_agents/model-profiles.env
make unit-test 2>&1 | tail -3
git ls-files -z "*.py" | xargs -0 mise x ruff -- ruff format --config ruff.toml --check
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T84` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=25.

## Dispatch

- 2026-10-05 09:55Z to `claude-standard-dot-a005` (worker-c, wT:p2) after T82 merged as 2e65742c (manifest free; T81 and T85 on main). Branch from `origin/main` 2e65742c or later with `--no-track`. T81b queues behind this PR on the manifest pin. T85 already consumes `HERDR_AGENTS_ORCHESTRATOR_KIND` (default claude) and T86 requires it to be `codex` for a Codex orchestrator; the README herdr-agents section already describes both, so the README sentence here is the `(currently `claude`;` statement next to the worker_kind one.

## Revise round 1 (orchestrator, 2026-10-05 10:45Z) — task-level audit of 55f4d43f is `incorrect` (2)

1. **P2, worker-kind README check regression.** The existing validator check for `worker_kind` looks only for `(currently \`<kind>\`;`, so the new orchestrator sentence satisfies it (manifest worker `claude` + README worker `codex` now passes). Anchor the worker-kind check on its key the way you anchored the orchestrator one (`\`worker_kind\` … (currently \`<kind>\`;`), and add the regression test that the auditor reproduced (README worker kind wrong, orchestrator sentence present → fail).
2. **P3, CompactionDB evidence.** The validation file shows the `memory add` command with `<T84 decision text>` as a placeholder. Paste the actual command and a readback (`uv run .claude/hooks/contextdb_cli.py memory search T84 --session <sid>` or the `memory list` line) so the recorded content is evidenced.

One commit, CI, Bot wait on the diff head (timestamped), RESULT; `gh pr update-branch 272` only if `main` moved.
