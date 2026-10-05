# AGMSG-TASK dotfiles-T85-launcher-orchestrator-kind-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 7, dotfiles-T85). Depends on T84 (manifest `orchestrator_kind` → `HERDR_AGENTS_ORCHESTRATOR_KIND`). Touches `executable_herdr-agents` and its tests only; dispatch after T84 merges.

## Objective

Principle 4: the launcher knows which runtime orchestrates and refuses to start a Claude pair when the manifest says Codex, and it exposes the regime directive on demand so `codex-orchestrate` (T86) can seed a Codex orchestrator's first turn.

1. **Resolve `orchestrator_kind`** the way `resolve_worker_kind` does: `HERDR_AGENTS_ORCHESTRATOR_KIND` from the environment, else from `~/.agents/model-profiles.env`, else `claude`; validate `claude|codex`.
2. **Refuse the Claude pair under `codex`:** full mode, `--attach` and `--restart-worker` exit 2 with `herdr-agents: orchestrator_kind=codex: use codex-orchestrate` before touching Herdr (no workspace, pane or seat is created or changed). `--add-worker`, `--remove-worker`, `--audit`, `--bootstrap-agmsg` keep working under either kind (they do not seat an orchestrator).
3. **`--directive`:** prints exactly the `agmsg-orchestration:` directive line `print_regime_directive "$(pwd -P)"` would print for a regime repository, nothing for a repository without the regime, and exits 0 before `require_command herdr` (it must work with no Herdr server and in a plain shell). Usage text updated.
4. **Tests** (`tests/unit/test_herdr_agents.py`, fake CLIs): `codex` kind → exit 2, no `herdr` invocation, no agmsg join; `claude` kind unchanged; `--directive` in a seated fixture prints one line and nothing in an unseated one; `--directive` succeeds with `herdr` absent from PATH.
5. README usage lines for `--directive` and the `orchestrator_kind=codex` refusal (two sentences in the herdr-agents section).

Forbidden: any Codex seat-claim or `--attach` rewrite for a Codex orchestrator (an exec loop has no pane); profiles; the manifest; the generator.

[memory:decision] dotfiles-T85 (operator 2026-10-03): `herdr-agents` reads `HERDR_AGENTS_ORCHESTRATOR_KIND` (manifest `orchestrator_kind`); under `codex` the Claude-pair modes refuse with exit 2 and point at `codex-orchestrate`; `--directive` prints the regime directive line without Herdr so a Codex orchestrator's first turn can carry it.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c feat/launcher-orchestrator-kind --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`, `README.md` (the two sentences)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T85-launcher-orchestrator-kind-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
mise x shfmt -- shfmt -i 4 -sr -d home/dot_local/bin/common/executable_herdr-agents; shellcheck home/dot_local/bin/common/executable_herdr-agents
uv run python -m unittest tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test 2>&1 | tail -3
make validate-agent-assets
HERDR_AGENTS_ORCHESTRATOR_KIND=codex bash home/dot_local/bin/common/executable_herdr-agents --attach "$PWD"; echo "rc=$?"
bash home/dot_local/bin/common/executable_herdr-agents --directive; echo "rc=$?"
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the agmsg-orchestration SKILL Worker Playbook (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text (Claude seat) or say the orchestrator records it (Codex seat).
5. `AGMSG-RESULT v1 task_id=dotfiles-T85` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.

## Dispatch

- 2026-10-05 07:20Z to `claude-standard-dot-a005` (worker-c, wT:p2), in parallel with T82 (a006) and T86 (a007): the launcher file and its tests are disjoint from both, and the README sentences land in different sections (prose rule). The dependency on T84 is soft: resolve `HERDR_AGENTS_ORCHESTRATOR_KIND` exactly as `resolve_worker_kind` resolves its variable, defaulting to `claude` while T84 has not yet rendered the key; T84 lands the manifest side. Branch from `origin/main` 2527be54 or later with `--no-track`.
