---
format: 2
task_id: dotfiles-T128-seat-liveness-followup-a02-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-seat-liveness-followup-a02-review-a01 — confirm the owner task text `dotfiles-T128-seat-liveness-followup-a02` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T128-seat-liveness-followup-a02.md` (its sha256 is the `owner_task_sha256` of the TASK line): the owner task of its lineage (plan 020 step 1, C-51's owner-first rule), which implements the rows under `## Owned by dotfiles-T128-seat-liveness-followup-a02` in `.orchestration/acceptance/dotfiles-T128-seat-liveness-followup-a01.md` as read from `origin/main` (boundary (17), a0e8b8ad).

## Stop condition

1. Item 1 names the record and heading correctly, the rows exist on `origin/main` under that heading (`scripts/orchestrator/owner-rows.sh` or an equivalent read prints them with their classes), and each row's finding text is reachable from the id it names (a Bot thread, a local review file, an audit receipt or a correction record); the no-op clause for an empty section stands.
2. `allowed_files` (`home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`) cover every file the rows' fixes touch and no other code file; the rows that are tool halves of corrections (C-NN:n) or consumer halves name a mechanism the files can carry; the threat rows per path say "only within the owned rows" with the lineage's test cover named.
3. The generic rows are verbatim from `.orchestration/templates/task-short.md` (id substituted); the Completion clause follows plan 020 step 4 as the template's current clause reads it (the Bot's first review's P2 fixed in-PR while INV-6 allows, later P2 and every P3 to the next owner, the S1 sentence, the C-61 sentence) or states its lineage's earlier form with the first-review and C-61 readings applied; no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its premises replay from this checkout (`origin/main` fetched) as `present`.

## Output

`.orchestration/validation/dotfiles-T128-seat-liveness-followup-a02-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-seat-liveness-followup-a02: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-seat-liveness-followup-a02-review-a01 round=<n> verdict=confirm|revise owner_task_sha256=<sha> validation=<path>`.
