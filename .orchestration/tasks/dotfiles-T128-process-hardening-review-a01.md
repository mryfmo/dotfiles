---
format: 2
task_id: dotfiles-T128-process-hardening-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-process-hardening-review-a01 — confirm the task text `dotfiles-T128-process-hardening-a01` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T128-process-hardening-a01.md` (its sha256 is the `process_hardening_a01_task_sha256` of the TASK line): the tools half of the six process rules (C-61): regime-counters.sh counts every revise ACCEPTANCE line and prints an S1 watch at a class's second row; chain-integrate.sh inherits the audit across an update-branch-only head by patch-id; chain-finish.sh reads the code verdict and never stops on the record verdict.

## Stop condition

1. Items 1 to 3 describe the change correctly against `scripts/regime-counters.sh`, `scripts/orchestrator/chain-integrate.sh` on `origin/main` and `scripts/orchestrator/chain-finish.sh` on PR #378's head (the after: task), with every output line, exit code and git command named once and the same in the items and the rows.
2. The three closed rows name their tests verbatim as items 4 and 5 do, each case fails when the behaviour is wrong (two revise lines before the first RESULT, a class at two and at three rows, an update-branch head with and without an extra commit, the three verdict forms), and the existing tests stay with their stated values.
3. The threat table has one row per `allowed_files` entry, the non-path controls as rows, the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted), and the Completion clause is the template's current clause (the S1 sentence, the first-review P2 clause and the C-61 sentence); no sentence states an unlanded mechanism as present.
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its three premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T128-process-hardening-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-process-hardening-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-process-hardening-review-a01 round=<n> verdict=confirm|revise process_hardening_a01_task_sha256=<sha> validation=<path>`.
