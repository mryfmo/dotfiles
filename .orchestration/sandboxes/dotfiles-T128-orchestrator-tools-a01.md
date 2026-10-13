---
task_id: dotfiles-T128-orchestrator-tools-a01
seat: claude-standard-dot-a003
permission_gated_commands: 30
---

# Sandbox record: dotfiles-T128-orchestrator-tools-a01

- Period: from the AGMSG-TASK (2026-10-13T01:35:13Z) to the RESULT. These ran inside the sandbox: the fetch and the branch switch, the edits, the tests (stubbed binaries in temporary directories), shellcheck, ruff, the mutation proofs, the read-only live `bus-read.sh` runs against the agmsg store, and the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This is the final count, grouped by purpose:

| Calls | Command | Step 4 case |
|--:|---|---|
| 1 | main-checkout `memory add` | main-checkout `memory add` |
| 3 | the HTTPS pushes of `61290da8` (with `gh pr create --draft`, one call), `4843ccb6`, `5b6d5f24` | `git push`, `gh` |
| 1 | `gh pr ready 336` | `gh` |
| 6 | Bot waits from ready or the push (three heads) and `gh pr checks 336 --watch` runs, background, exit status joined (three heads) | `gh` |
| 2 | the re-run CI watcher, and `gh run rerun 38335666287 --failed` with the macOS job check | `gh` |
| 13 | reading failed-job logs, job lists, run lists, Bot reviews and comments, and check runs (`gh run view`, `gh api`) | `gh` |
| 2 | writing §9's and §10's GitHub excerpts to the session scratchpad (the first §9 attempt ran entirely outside the sandbox; it was discarded with `git checkout --` and rebuilt) | `gh` |
| 1 | the masked copy of the five evidence files to the main checkout | artifact copy with the repository masker |
| 1 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-a01 …` | `agmsg-dispatch` |

One sandboxed call ran the real `agmsg-dispatch` by mistake (report, fix round 2); it stopped at the pane check and sent nothing.
