# T38: Batched .orchestration evidence sync (T35 + T36 + T37) and mise pair

## Objective

Converge the accumulated orchestration evidence into git per the batching
rule, plus the leftover mise tool-bump pair, on a dedicated chore branch.

## Steps (exact)

1. From current `main`, create branch `chore/orchestration-evidence-t35-t37`
   in this worktree (`git checkout -b ...`). Do NOT touch the four
   T37-modified tracked files (scripts/update-agent-assets.sh,
   scripts/validate-agent-assets.py, tests/install/common/lifecycle.bats,
   README.md) — they belong to PR #112 and must stay out of both commits.
2. Commit 1 — `chore(orchestration): sync T35/T36/T37 evidence`:
   `git add .orchestration/` (all T35/T36/T37 tasks, reports, validation,
   sandboxes, learning, autoskill/runs, acceptance — including this T38 task
   file). Nothing else.
3. Commit 2 — `chore(mise): commit managed toolchain bump`:
   `git add home/dot_mise/config.toml home/dot_mise/mise.lock`. Nothing else.
4. Switch back to `main` (`git checkout main`). Do not push.
5. Commit messages in English, one line each as above.

## Forbidden actions

- No push, no PR creation, no merge (orchestrator handles those).
- No edits to any file content — this task only stages and commits existing
  state.
- Do not add `.ua/` (pending operator decision) or `.agents/worklog/`.

## Expected artifacts

- report: `.orchestration/reports/T38-evidence-sync.md` (note: written AFTER
  the sync commits, so it stays uncommitted as the converged one-task tail
  per the batching rule — this is intended)
- validation: `.orchestration/validation/T38-evidence-sync.md` — include
  `git log --oneline -2 chore/orchestration-evidence-t35-t37` and
  `git show --stat` for both commits
- sandbox: `.orchestration/sandboxes/T38-evidence-sync.md`
- learning: `.orchestration/learning/T38-evidence-sync.md`
- autoskill: `.orchestration/autoskill/runs/T38-evidence-sync.md`

## Done signal

`AGMSG-RESULT v1 task_id=T38-evidence-sync status=ready_for_review|blocked`
with all artifact paths. Max turns: 15.
