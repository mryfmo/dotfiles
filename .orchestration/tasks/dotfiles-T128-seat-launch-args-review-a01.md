---
format: 2
task_id: dotfiles-T128-seat-launch-args-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-seat-launch-args-review-a01 — confirm the task text `dotfiles-T128-seat-launch-args-a01` (review seat half; Codex headless runs the same check first, C-54)

Drafted 2026-10-17 by the orchestrator seat. The reviewed file is `.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md` (its sha256 is the `seat_launch_args_task_sha256` of the TASK line): a new script comparing a seated worker's live process arguments with its rendered profile, run by the boundary check for every seated worker, after the operator's question of 2026-10-17 (M-20261017-05, C-60).

## Stop condition

1. Items 1 and 2 describe the change correctly against `scripts/check-regime-boundary.sh` on `origin/main` (the seated-worker loop, the `--report` mode, "a missing tool skips its check"), `~/.agents/model-profiles.env`'s rendered form (`KEY="value"` lines, `MODEL_PROFILE_<NAME>_<KIND>_ARGS`), the `-n <team>-<name>` token `herdr-agents --add-worker` passes to a claude worker (home/dot_local/bin/common/executable_herdr-agents) and the `--profile <name>` it passes to a codex worker; the identity grammar and every output line and exit code are stated once and the same in items 1, 3 and 4.
2. The two closed rows name their tests verbatim as items 3 and 4 do, each case fails when the behaviour is wrong (the resumed seat, the differing effort, the codex decoy by cwd, the unsourced env value), and the existing tests stay.
3. The threat table has one row per `allowed_files` entry, the two input rows as non-path controls, the generic rows verbatim from `.orchestration/templates/task-short.md` (id substituted), and the Completion clause is the template's current clause with the S1 sentence; no sentence states an unlanded mechanism as present (dispatch.sh's refusal is the tools a04 row, not done).
4. The file passes C1 to C10 and C7b (the orchestrator pasted its `OK`), the mask check (`masked 0 match(es)`), and its three premises replay from this checkout (`origin/main` fetched) with the outputs recorded in the file.

## Output

`.orchestration/validation/dotfiles-T128-seat-launch-args-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-seat-launch-args-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-seat-launch-args-review-a01 round=<n> verdict=confirm|revise seat_launch_args_task_sha256=<sha> validation=<path>`.
