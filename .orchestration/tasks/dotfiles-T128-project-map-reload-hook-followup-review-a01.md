---
format: 2
task_id: dotfiles-T128-project-map-reload-hook-followup-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-project-map-reload-hook-followup-review-a01 — confirm the owner task `dotfiles-T128-project-map-reload-hook-followup-a01` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-14 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-followup-a01.md` (untracked; its sha256 is the `owner_task_sha256` of the TASK line), the owner task of the project-map reload hook lineage, written when the first advisory P2 appeared (the worker's own P2 on PR #353's head 30cbfb4d, 06:33Z: `worker:30cbfb4:1`, the tab fallback between the hook's two agent-browser calls) as the lineage task's Completion requires, from the shape of `dotfiles-T128-task-checkers-followup-a01` (pair-confirmed 06:21Z today; the premises and the no-op clause come from that review). One round, fixed stop condition.

## Stop condition

1. The file's front matter equals the lineage task's (`dotfiles-T128-project-map-reload-hook-a01.md`, amendment 2) except: the id, no `reset_of`, its own evidence directory in `allowed_files`, `after:` the lineage task, its own two premises (the T704 owner's shape: the lineage task file and the lineage record's owner section on `origin/main`, each `absent` today) in place of the lineage's seven, the lineage's generic rows kept verbatim (the agent-browser daemon row among them) but the new-scripts row saying no new script, and one residual row per lineage code, config or test entry in the "only within the owned rows (item 1)" form.
2. Item 1 is closed: the owned rows are exactly the `## Owned by dotfiles-T128-project-map-reload-hook-followup-a01` section of `.orchestration/acceptance/dotfiles-T128-project-map-reload-hook-a01.md` on `origin/main` (today untracked, landing with the next boundary; the no-op clause covers a missing or empty section); nothing outside it can be claimed; a `local-finding:` or `audit-finding:` line naming this owner, or a lineage report's advisory finding, is the same evidence as a sweep disposition.
3. No sentence states an unlanded mechanism as present; the Completion clause matches plan 020 step 4 (the Bot's single review, one fix round, a surviving P0/P1 to the operator, P2 recorded under the same heading for the next owner task); the cap sentence reads outside `tests/` and outside `.orchestration/`.
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-project-map-reload-hook-followup-a01.md: OK`) and the brief check (2 claims, 19 controls).

## Output

`.orchestration/validation/dotfiles-T128-project-map-reload-hook-followup-review-a01.md`: the usual header with both sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-project-map-reload-hook-followup-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-project-map-reload-hook-followup-review-a01 round=1 verdict=confirm|revise owner_task_sha256=<sha> validation=<path>`.

## Round 2 (orchestrator, after the round-1 RESULTs of 06:51Z)

The Codex half's P1 is on this brief: stop condition 1 did not list the two premises among the permitted differences from the lineage front matter; it now does. The seat's P2: premise 2 checked only that the lineage record exists, while its owner section is written at the lineage's RESULT, so a boundary landing the record first would make the premise `present` and the no-op clause drop the first row; premise 2's command now greps the record on `origin/main` for the `## Owned by` heading (`absent` today) and its claim says so. The seat's P3: "Its first row is" now reads "will be …, written to the owner section at the lineage's RESULT". The seat's record-only P3 (class vocabulary `advisory-p2`): the planned row keeps a descriptive class, because the class column feeds the three-repeat counter (`three-repeat.sh`, S1), where one shared slug would count unrelated advisory findings together; noted in the lineage record. Input checker `OK`, 19 controls, 2 claims. Same four stop conditions on the new hash (`owner_task_sha256` of the round-2 TASK line).
