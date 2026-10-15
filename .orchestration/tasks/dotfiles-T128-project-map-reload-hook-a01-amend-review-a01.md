---
format: 2
task_id: dotfiles-T128-project-map-reload-hook-a01-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-project-map-reload-hook-a01-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-project-map-reload-hook-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 (the TASK line's bus time is the dispatch time) by the orchestrator seat. The Codex worker's PONG of 05:29:15Z (working): read literally, the Check's "at most 200 changed lines outside `tests/`" counts the task copy (110 lines) and the evidence records under `.orchestration/`, which no task has ever capped (INV-2's convention; a05 and a06 reported "files outside .orchestration" and "added non-test" lines); the text did not say so. The task file is not on `main`: the pre-amendment copy is the pair-confirmed version cc6ac23f (seat and Codex round 3, 05:23Z), kept beside this brief; `git diff --no-index <that copy> <the file>` shows one changed sentence and one new section. Amended file: `.orchestration/tasks/dotfiles-T128-project-map-reload-hook-a01.md`, sha256 `452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07`; the pre-amendment copy is on `main` (`not on main; pre-amendment pair-confirmed copy cc6ac23f3e87015f139dc4037963671cfdad188913be10193192759b876b2a67`).

## What changed (amendment 1)

1. The Check's cap sentence reads "outside `tests/` and outside `.orchestration/`", with the reason in a parenthesis (the task copy and the evidence records are committed on the branch as every task does and are never capped).
2. A `## Change of 2026-10-14 (amendment 1 …)` section stating 1. Nothing else changes.

## Stop condition

1. The diff of the task file against its pre-amendment pair-confirmed copy (the orchestrator's scratchpad `hook-task-before-amend1.md`, sha256 cc6ac23f3e87015f139dc4037963671cfdad188913be10193192759b876b2a67; the file is not on `main` yet) contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) and `amend-sweep.sh` for the superseded terms (pasted); `reset_of`, the copy rows and the evidence directory are unchanged.

## Output

`.orchestration/validation/dotfiles-T128-project-map-reload-hook-a01-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-project-map-reload-hook-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-project-map-reload-hook-a01-amend-review-a01 verdict=confirm|revise amended_task_sha256=452a344479136254b1cfa266204827e4a715a4e26489bc751c5b7ee33d8e2b07 validation=<path>`.
