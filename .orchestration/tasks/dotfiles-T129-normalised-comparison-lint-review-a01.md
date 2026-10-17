---
format: 2
task_id: dotfiles-T129-normalised-comparison-lint-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T129-normalised-comparison-lint-review-a01 — confirm the task text `dotfiles-T129-normalised-comparison-lint-a01` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` (its sha256 is the `normalised_comparison_lint_task_sha256` of the TASK line): plan 023's PR F2: a lint refusing path, URL and process comparisons by string form, with an allowlist marker, run by `make lint` and CI. Plan 023 (`.orchestration/plans/023-omp-hcom-migration.md`) is its design.

## Stop condition

1. Item 1's rules are stated as a table a reader can check against the fixtures of item 3 and against the existing scripts on `origin/main` (name the violations the lint would find on main and that item 2's marker policy covers); the Makefile and CI entries are read on `origin/main`.
2. The closed row's test fails when a rule is removed (one fixture per rule), the allowed forms are each a fixture, and the existing lints and tests stay green.
3. The threat table has one row per `allowed_files` entry, the non-path controls as rows, the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted), and the Completion clause is the template's current clause; no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T129-normalised-comparison-lint-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T129-normalised-comparison-lint-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-normalised-comparison-lint-review-a01 round=<n> verdict=confirm|revise normalised_comparison_lint_task_sha256=<sha> validation=<path>`.
