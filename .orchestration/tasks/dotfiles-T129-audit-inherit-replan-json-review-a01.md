---
format: 2
task_id: dotfiles-T129-audit-inherit-replan-json-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T129-audit-inherit-replan-json-review-a01 — confirm the task text `dotfiles-T129-audit-inherit-replan-json-a01` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md` (its sha256 is the `audit_inherit_replan_json_task_sha256` of the TASK line): plan 023's PR F1: chain-integrate.sh inherits the audit across an update-branch-only head by patch-id, and the S1 re-plan becomes a `replans` object in the record block read by the gate, the counters and the front-matter writer, with the body-line parse removed. Plan 023 (`.orchestration/plans/023-omp-hcom-migration.md`) is its design.

## Stop condition

1. Items 1 and 2 describe the change correctly against `scripts/orchestrator/chain-integrate.sh`, `scripts/require-crit-review.py`, `scripts/regime-counters.sh` and `scripts/orchestrator/acceptance-front-matter.py` on `origin/main` (the audit step and the line-105 refusal; the S1 check and its body scan; the jq S1 line; the block rewrite), with the schema stated once and the same in every item and row.
2. The four closed rows name their tests verbatim as item 3 does, each case fails when the behaviour is wrong (the patch-id mutant, the missing key, the body line alone, the malformed object), and the existing tests stay with their stated moves.
3. The threat table has one row per `allowed_files` entry, the non-path controls as rows, the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted), and the Completion clause is the template's current clause; no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T129-audit-inherit-replan-json-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T129-audit-inherit-replan-json-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-audit-inherit-replan-json-review-a01 round=<n> verdict=confirm|revise audit_inherit_replan_json_task_sha256=<sha> validation=<path>`.
