---
task_id: dotfiles-T128-orchestrator-tools-a01
seat: claude-standard-dot-a003
permission_gated_commands: 9
---

# Sandbox record: dotfiles-T128-orchestrator-tools-a01

- Period: from the AGMSG-TASK (2026-10-13T01:35:13Z) to the RESULT. These ran inside the sandbox: the fetch and the branch switch, the edits, the tests (stubbed binaries in temporary directories), shellcheck, ruff, the mutation proofs, the read-only live `bus-read.sh` runs against the agmsg store, and the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This copy was written before #2, so #2 to #9 are counted in advance; the main-checkout copy gives the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | main-checkout `memory add` | main-checkout `memory add` |
| 2 | the HTTPS push of the new branch | `git push` |
| 3 | `gh pr create --draft --head tools/orchestrator-scripts` | `gh` |
| 4 | `gh pr ready <n>` | `gh` |
| 5 | `gh pr checks <n> --watch` (background, exit status joined) | `gh` |
| 6 | Bot wait from `gh pr ready` | `gh` |
| 7 | reading the Bot review and the check runs of the final head | `gh` |
| 8 | the masked copy of the five evidence files to the main checkout | artifact copy with the repository masker |
| 9 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-orchestrator-tools-a01 …` | `agmsg-dispatch` |
