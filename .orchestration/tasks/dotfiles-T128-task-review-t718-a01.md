---
format: 2
task_id: dotfiles-T128-task-review-t718-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-review-t718-a01 — task-file review of `dotfiles-T128-orchestrator-tools-a01` (review seat half; Codex headless runs the same check on the same hash)

Drafted 2026-10-13 01:30Z by the orchestrator seat under plan 012 option B (operator, 01:05Z): T718's first slice, the three scripts T703's rule text names (`dispatch.sh`, `three-repeat.sh`, `bus-read.sh`) and the counters' class slug, lands before PR #328 merges. File: `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md`, sha256 `9f33e1dec7496bceef2b5f0c2dd498244842e77e5a3062c9a89e570da72ef110`. Design: `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` (v22, receipt round 22). The remainder of the original scope is the draft `dotfiles-T128-orchestrator-tools-a02.md` (not under review).

## Stop condition (one round)

1. No contradiction with the design: `kind: code`, `scripts/orchestrator/` on no design-tier list, INV-2 caps stated in Validation, the gate and the audit runner untouched, `after: []` consistent with plan 012 B (this task precedes T703's merge).
2. The premises hold when replayed (the three `command:` lines, with the executor's binaries; C-18).
3. `allowed_files` covers every touch point: every `scripts/orchestrator/<name>` that PR #328's head `2276a365` names in `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (`git show 2276a365:home/dot_agents/skills/agmsg-orchestration/SKILL.md | grep -o 'scripts/orchestrator/[a-z-]*\.sh' | sort -u`) is in item 1, and the counters' slug item names the line thread 4250028600 points at (`scripts/regime-counters.sh` lines 145 to 147, test line 451).
4. Threat rows at the SKILL row unit (one per `allowed_files` entry, one per non-path control, one per orchestrator effect; C7), the closed row's test name appears verbatim in item 2, and the environment-inputs row names every host binary item 1's scripts call (grep, shasum, jq, agmsg-dispatch, history.sh, uv; C-26).
5. C1 to C10 pass (the orchestrator pasted `OK` at 01:18Z; re-derive C7 and C10 by reading).

## Output

`.orchestration/validation/dotfiles-T128-task-review-t718-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), then exactly one line `Task-file verdict: dotfiles-T128-orchestrator-tools-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-t718-a01 verdict=confirm|revise reviewed_sha256=9f33e1dec7496bceef2b5f0c2dd498244842e77e5a3062c9a89e570da72ef110 validation=<path>`.

## Round 2 (orchestrator, 2026-10-13 01:3xZ)

Round 1: the seat's three findings and the Codex half's one, applied once: the counters row is split into one row per `allowed_files` entry (Codex P2; the checker now refuses a combined row, C7b); item 3 reads the slug from the acceptance record's machine-readable block, a JSON object between the first two `---` lines (the a03 contract as plan 013 A′ amends it, operator 01:2xZ), with `jq`, and prints a title only JSON-quoted in its own field (seat P2 at :81); bus-read.sh names `lib/storage.sh`'s `storage_history` and never the database file (seat P2 at :79); the environment row names git, sort and date (seat P3 at :35). Same stop condition; the sha256 in the round-2 TASK line is the file's.
