# Acceptance: dotfiles-T89-add-worker-same-workspace-a01

- **Decision:** ACCEPTED. PR #239 squash-merged to `main` as `3a0816e6` (final head `672f720e8238134000b205181830af445b82f982`; substantive commits 55d7e77c, 37cf5e47, 958468ba; base `a575b3cc`, update-branch onto `523fda06`). Merged without `--delete-branch`; worker-c holds `feat/add-worker-same-workspace`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `ba6a86a4…` → `1cbabe95…` (PONG decision 1: q1=A own workspace without a pair; q2=a tab per worker inside the pair workspace); both matched.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Operator instruction carried:** 「並列化は同じ spaces 内で行うべき」 (2026-10-04).

## What was accepted (5 files, +301/−23)

- `herdr-agents --add-worker`: resolves the pair workspace (same lookup as restart/audit/full mode); with one, seats the worker through the unchanged upstream `spawn.sh --window` path with `HERDR_WORKSPACE_ID=<pair>` (tab and pane labelled `<team>:<name>`, pair tab untouched, placement record and `linkage=` line unchanged); "already seated" also recognises a labelled pane with an agent in the pair workspace; without a pair workspace the own-workspace pane-less flow is unchanged.
- `--remove-worker`: `close_worker_tab` closes only a tab whose panes all carry the worker label or are unlabelled and agentless; a legacy own workspace is still closed (needed for the live migration). Exits 2 on duplicate pair workspaces.
- Full-mode repair: `has_claude_pane`/`empty_pane_id` skip added-worker panes (self-named label + cwd in a linked worktree), so an added Claude worker is never taken for the orchestrator and an exited worker's pane is never reused for the pair worker (extension beyond the PONG premise, justified: those helpers scan the whole workspace).
- `check-regime-boundary.sh`: legacy workspace check kept; new "additional worker tab still open in <pair>" check.
- README/SKILL sentences; the README codex spawn-options line gains the T64 flags. Seven new tests, each failing against the code it guards; 722 unit tests OK.

## Audit

| commit | verdict | findings → disposition |
|---|---|---|
| 55d7e77c | incorrect | P2 unlabelled-pane tab close → fixed:958468ba; P2 `has_claude_pane` counts an added worker → fixed:37cf5e47; P2 `empty_pane_id` picks an exited added worker → fixed:37cf5e47 |
| 37cf5e47, 958468ba | correct | — |

## Codex Bot / sweep

- 1 thread (P2, same as the first audit finding) fixed in 958468ba, replied and resolved; thumbs-up on 958468ba and 672f720e. Sweep (head 672f720e): 9 items, 0 failure/warning, all dispositioned.

## Gate

- `.claude/worktrees/orchestrator-review` at 672f720e with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` exit 0; copies removed.

## Caveats accepted (proven at the live migration)

- Herdr drops a tab when `despawn.sh` closes its only pane (else an empty tab remains, invisible to the boundary check); concurrent `--audit` tab creation vs. the pane diff (the placement record path is preferred when present).

## CompactionDB

- Worker decision `9c11dc0f-9fff-4d47-9018-f870a5398948` says "panes"; amended at acceptance: each added worker gets its own tab in the pair workspace (see the acceptance-time `memory add`).

## Follow-ups routed

- Spawn-seated workers never receive the `workspace create --env` variables (`AGMSG_RESOLVE_PROJECT`, `AGMSG_CC_MONITOR_KEEP_ALIVE`, `HERDR_AGENTS_LAYOUT`) → launcher follow-up task (plan note).
- README pane-less paragraph (~555) still names `team.sh --json`/`poke.sh` → T83.

## Operator follow-up (live migration, at a task boundary after `make update`)

- For worker-d (a006) and worker-e (a007): `herdr-agents --remove-worker .claude/worktrees/<w>` (closes the legacy workspace), then `herdr-agents --add-worker .claude/worktrees/<w>` (seats it in a tab of wT, prints `linkage=…`). `make check-regime-boundary` then reports any added-worker tab left open instead of legacy workspaces.
