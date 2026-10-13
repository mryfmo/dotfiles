---
format: 2
task_id: dotfiles-T128-task-review-t718-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-task-review-t718-a02 — task-file review of `dotfiles-T128-orchestrator-tools-a02` (review seat half; Codex headless runs the same check on the same hash)

Drafted 2026-10-13 01:40Z by the orchestrator seat under plan 012 option B: the second slice of T718, the nine scripts the first slice (`dotfiles-T128-orchestrator-tools-a01`, reviewed 01:25Z) left out. File: `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md`; its sha256 is in the TASK line. Design: `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` (v22, receipt round 22). Dispatch happens after a01 merges (`after:`), so the review may precede that merge.

## Stop condition (one round)

1. No contradiction with the design (`kind: code`; `scripts/orchestrator/` on no design-tier list; INV-2 caps in Validation; the gate and the audit runner untouched: `orch-gate.sh` and `orch-audit.sh` only assemble inputs and call `make require-crit-review` and the audit runner).
2. The premises hold when replayed (the `command:` lines, executor's binaries; C-18).
3. `allowed_files` covers every touch point of the nine scripts and their tests, and nothing of a01's three scripts or the counters is re-specified here.
4. Threat rows at the SKILL row unit (C7, C7b), the closed row's test name verbatim in item 2, and the environment-inputs row names every host binary and package the nine scripts use (git, gh, make, codex, shasum, uv; `fill_sweep.py` and `acceptance-front-matter.py` read and write the acceptance record's JSON block with the standard library, as amendment 1 of `dotfiles-T128-gate-evidence-a03` defines it; C-26).
5. C1 to C10 pass (the orchestrator pasted `OK`); `acceptance-front-matter.py` is specified against the amended a03 contract (JSON block, identity triple), not the superseded YAML wording.

## Output

`.orchestration/validation/dotfiles-T128-task-review-t718-a02.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), then exactly one line `Task-file verdict: dotfiles-T128-orchestrator-tools-a02: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-task-review-t718-a02 verdict=confirm|revise reviewed_sha256=<sha> validation=<path>`.
