---
format: 2
task_id: dotfiles-T129-assets-omp-hcom-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T129-assets-omp-hcom-review-a01 — confirm the task text `dotfiles-T129-assets-omp-hcom-a01` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md` (its sha256 is the `assets_omp_hcom_task_sha256` of the TASK line): plan 023's PR A: omp and hcom as pinned assets of the manifest, installed and refreshed by update-agent-assets.sh, reported by check-tools, with a unit test and a CI bats test. Plan 023 (`.orchestration/plans/023-omp-hcom-migration.md`) is its design.

## Stop condition

1. Items 1 to 3 describe the change correctly against the manifest's assets section, scripts/update-agent-assets.sh and scripts/check-tools.sh on origin/main (the existing source types and their install flow), and the omp and hcom install forms match the plan's facts.
2. The closed row's test fails without the pin check; the bats test is CI-only as the repository's test policy says; the existing tests stay.
3. The threat table has one row per `allowed_files` entry, the non-path controls as rows, the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted), and the Completion clause is the template's current clause; no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T129-assets-omp-hcom-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T129-assets-omp-hcom-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-assets-omp-hcom-review-a01 round=<n> verdict=confirm|revise assets_omp_hcom_task_sha256=<sha> validation=<path>`.
