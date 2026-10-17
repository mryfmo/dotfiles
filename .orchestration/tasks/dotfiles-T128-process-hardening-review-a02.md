---
format: 2
task_id: dotfiles-T128-process-hardening-review-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-hardening-review-a02 — confirm the task text `dotfiles-T128-process-hardening-a02` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T128-process-hardening-a02.md` (its sha256 is the `process_hardening_a02_task_sha256` of the TASK line): the rules half of the six process rules (C-61) in the SKILL's counters, task-level audit, step 10 and Worker Playbook text and in the two always-loaded rules files, each sentence pinned by a docs test and its fixture.

## Stop condition

1. Items 1 to 5 name the sentences and their places correctly against the SKILL and the two rules files on `origin/main` (the counters bullet, the task-level audit bullet with its update-branch sentence, step 10's P2 clause, the Worker Playbook, the pr-integration and agmsg-orchestration rules), and each new sentence repeats none of the phrases the existing docs tests pin (`test_three_repeats_start_with_a_pasted_correction_search`, `test_advisory_rows_are_excluded_from_the_class_counts`, `test_counters_bullet_names_owners_not_sources`).
2. Item 6 names five tests, one per sentence group, each asserting the sentence in the rule text and in its fixture; the existing tests stay green and the rules files stay within `test_word_budgets`.
3. The threat table has one row per `allowed_files` entry, the non-path controls as rows, the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted), and the Completion clause is the template's current clause (the S1 sentence, the first-review P2 clause and the C-61 sentence); no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its three premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T128-process-hardening-review-a02.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-process-hardening-a02: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-hardening-review-a02 round=<n> verdict=confirm|revise process_hardening_a02_task_sha256=<sha> validation=<path>`.
