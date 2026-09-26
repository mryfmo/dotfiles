---
task_id: dot-ua-incremental-T20-a01
revision: 2
---
# AGMSG-TASK dot-ua-incremental-T20-a01: incremental Understand-Anything graph update after the Phase 1 / L.1 merges

Rule: under the agmsg regime, `.ua/` graph (re)builds are repository mutations and go to a worker. The SessionStart/PostToolUse hooks report the graph stale (meta.json pinned to d906b00; main now includes #178 pins, #180 herdr-agents guard, #181 asset manifest, plus `.orchestration` syncs which are excluded by `.understandignore`).

Repo: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`, branch `chore/ua-incremental-20260926` from origin/main (5e40ff9 or later). You are `claude-standard-dot-a005`. Revision 2 (03:2xZ): run now on current main; the post-T16/T19 refresh is a cheap incremental re-run in Stage 3, not a precondition. Preserve first: the worktree is detached at a6df24c with uncommitted T21 work on 5 files — commit it as-is on a new branch `wip/orchestrator-guardrails-T21` (`git switch -c`, one commit `wip(T21): preserve worker-c changes`), push it, then create the T20 branch from origin/main. Do not delete or rebase that WIP branch.

## Steps
1. Read `~/.claude/plugins/cache/understand-anything/understand-anything/<version>/hooks/auto-update-prompt.md` and follow its incremental-update instructions (not FULL_UPDATE unless the tool demands it — report if it does).
2. Commit only `.ua/knowledge-graph.json`, `.ua/fingerprints.json`, `.ua/meta.json` (and `.ua/.understandignore` if changed). Verify `meta.json.gitCommitHash == git rev-parse origin/main` at the time of the update.
3. PR (English), CI green, pr-feedback sweep + CodeRabbit full review on the final head (rate limit applies), RESULT.

## allowed_files
`.ua/**` except `.ua/intermediate/` and `.ua/diff-overlay.json` (gitignored), artefacts.

## forbidden_actions
source changes; FULL_UPDATE without reporting; merging; `make update`; local bats; force-push.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "UA graph updates are batched per integration boundary and run by a worker as an AGMSG-TASK". RESULT via send.sh. max_turns=20.

## Revision history
- r1 (09-25): queued after T16/T19.
- r2 (09-26 03:2xZ): assigned to a005 in worker-c worktree; run now; WIP preservation step added.
