# AGMSG-TASK dot-ua-incremental-T20-a01: incremental Understand-Anything graph update after the Phase 1 / L.1 merges

Rule: under the agmsg regime, `.ua/` graph (re)builds are repository mutations and go to a worker. The SessionStart/PostToolUse hooks report the graph stale (meta.json pinned to d906b00; main now includes #178 pins, #180 herdr-agents guard, #181 asset manifest, plus `.orchestration` syncs which are excluded by `.understandignore`).

Repo: nested worktree, branch `chore/ua-incremental-<date>` from origin/main after T16 and T19 land (batch to avoid churn). You are `claude-standard-dot-a003`.

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
