# AGMSG-TASK dotfiles-T105-orchestrator-kind-codex-a01 (draft, dispatched only when the operator is ready to run the codex legs)

Purpose: step 1 of the operator procedure in `.orchestration/validation/e2e-codex-claude-linux.md` and `e2e-codex-codex-linux.md`. Kind: manifest key only; a Claude seat is allowed (no permission, sandbox or hook boundary).

## Objective

1. `home/dot_agents/agent-config.yaml`: `orchestrator_kind: claude` → `orchestrator_kind: codex` (the one key; its comment stays).
2. `home/dot_agents/model-profiles.env`: rendered (`HERDR_AGENTS_ORCHESTRATOR_KIND="codex"`), `make render-check` clean.
3. No other change. Tests that pin the rendered value, if any, follow it.

Forbidden: any other file; `make update`; thread resolution.

## Repo / branch

worker-c, `git switch -c chore/orchestrator-kind-codex --no-track origin/main`; verify task_rev; PR to `main`; CI green; Bot wait; RESULT. Artifacts at the standard seven `dotfiles-T105-orchestrator-kind-codex-a01` paths. max_turns=8.

## After acceptance (orchestrator, then operator)

The orchestrator merges and runs `make update`, which renders `codex`; from that moment `herdr-agents` refuses the Claude-pair modes, so the orchestrator ends its own session right after sending the operator the leg command. Operator: in a plain shell at the main checkout root, with the claude worker still seated,
`codex-orchestrate --max-turns 3 --timeout 1800 --team dotfiles "Dispatch dotfiles-T87-probe to the seated worker: run make render-check in its worktree and send AGMSG-RESULT; then ORCHESTRATION-DONE."`
Then re-seat the worker as codex (`herdr-agents --remove-worker .claude/worktrees/worker-c` is not needed: use `--add-worker .claude/worktrees/worker-d --kind codex`) and repeat the command for the codex→codex leg. Evidence paths and what to paste: the two e2e files. Then T106 (revert) is dispatched by the restarted Claude orchestrator, or by the operator with the same task text and `codex` → `claude`.
