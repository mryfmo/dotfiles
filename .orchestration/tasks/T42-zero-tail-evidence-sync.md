# T42: Make evidence sync zero-tail, then land the accumulated tail

## Objective

Amend the orchestration batching rule so evidence sync is a mechanical batch
commit with no artifact ceremony (audit record = the commit itself + agmsg
ACCEPTANCE history), then let the orchestrator land the accumulated
T38–T42 evidence in the new style, leaving zero untracked tail.

## Steps (worker part)

Work **in this worktree** (no scratch worktree this time — the final sweep
needs this tree's untracked evidence files and the branch must remain
checked out here). Branch `chore/zero-tail-evidence-sync` from `main`.

1. `home/dot_config/claude/rules/agmsg-orchestration.md` line 20: replace the
   evidence-sync clause with exactly this text (keep the surrounding bullet
   format and the mise-pair sentence):

   > Sync `.orchestration` evidence at regime or session boundaries as a
   > mechanical batch commit; the orchestrator may perform it directly
   > (bookkeeping, exempt from worker delegation). The sync itself requires
   > no per-task artifact set — its audit record is the commit (message lists
   > the covered task IDs) plus the agmsg ACCEPTANCE history. Write any
   > pending acceptance records first, then commit every `.orchestration`
   > file present so no untracked tail remains. Commit `make upgrade` tool
   > bumps (the mise config/lock pair) as their own chore commit in the same
   > working session as the upgrade; never leave that pair dirty across
   > sessions.

2. Commit exactly that one file:
   `docs(agents): make evidence sync a zero-tail mechanical commit`.
3. Write the T42 artifact set (this rule edit is content work, so normal
   artifact duty applies) as untracked files:
   - report: `.orchestration/reports/T42-zero-tail-evidence-sync.md`
   - validation: `.orchestration/validation/T42-zero-tail-evidence-sync.md`
     (grep proving the new text, old text absent everywhere)
   - sandbox: `.orchestration/sandboxes/T42-zero-tail-evidence-sync.md`
   - learning: `.orchestration/learning/T42-zero-tail-evidence-sync.md`
   - autoskill: `.orchestration/autoskill/runs/T42-zero-tail-evidence-sync.md`
4. **Stay on the branch** (do not check out main) and send the done signal.
   The orchestrator will then write the acceptance record, perform the
   mechanical sweep commit (all untracked `.orchestration` files, T38–T42),
   push, open the PR, and merge on green.

## Forbidden actions

- No push, no PR ops, no merge, no sweep commit (orchestrator's part).
- No edits beyond the single rule file and the T42 artifact files.
- Do not switch branches after committing.

## Done signal

`AGMSG-RESULT v1 task_id=T42-zero-tail-evidence-sync
status=ready_for_review|blocked` with artifact paths. Max turns: 12.
