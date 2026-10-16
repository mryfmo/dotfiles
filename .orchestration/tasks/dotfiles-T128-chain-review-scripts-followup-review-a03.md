---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-review-a03
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-review-a03 — confirm the task text `dotfiles-T128-chain-review-scripts-followup-a03` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-15 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md` (untracked; its sha256 is the ` it shares the test module):advisory_task_sha256` of the TASK line), the owner task that corrections C-51 (2) and C-50 (3) name: local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the record's earlier row. The Codex half runs first and the seat once after its confirm (C-54). One round, fixed stop condition; round 2 (2026-10-15T22:08:38Z) applies the seat's five round-1 P3s (the owner check's place, exit 2 for both refusals, the token grammar, the stated scope, the provenance clause); round 3 (2026-10-15T22:11:13Z) applies the Codex half's two round-2 P3s (the untouched record asserted byte for byte; the range token and the two-earlier-heads cases).

## Stop condition

1. Item 1 describes the two changes correctly against `scripts/orchestrator/local-advisory.sh` on `origin/main` (its header, arguments, exit codes, the lines it writes or reads) and against the corrections' records (`.orchestration/learning/corrections/`, the two named, and their mistakes), with every failure mode stated and fail-closed; no sentence states an unlanded mechanism as present; the premises read `origin/main` only.
2. The two test names appear verbatim in the closed rows (test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file and test_local_advisory_classes_a_repeat_by_the_earlier_row), the cases are the ones item 2 describes, each with the assertion that fails under the wrong behaviour, and the fakes answer from files the case writes (the temporary repository's review files, record and owner task file), nothing live.
3. The threat table has one row per `allowed_files` entry, the non-path control rows item 1 implies, the generic rows verbatim from `.orchestration/templates/task-short.md` (the new-scripts row says no new script), and the three orchestrator effect rows verbatim; the Completion clause is the template's (the Bot's review of the final head, one fix round, a surviving P0/P1 to the operator, C-50's revise round, the advisory owner named); the cap sentence reads outside `tests/` and outside `.orchestration/`; `allowed_files` is pairwise-disjoint from every in-flight task except where the `after:` field serialises it (the a02 owner task dotfiles-T128-chain-review-scripts-followup-a02 (after).
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-chain-review-scripts-followup-a03.md: OK`), the mask check (`masked 0 match(es)`), and its four premises replay from this checkout (`origin/main` fetched): 0, 1, 2, 3.

## Output

`.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-review-a03.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-chain-review-scripts-followup-a03: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-review-a03 round=1 verdict=confirm|revise  it shares the test module):advisory_task_sha256=<sha> validation=<path>`.
