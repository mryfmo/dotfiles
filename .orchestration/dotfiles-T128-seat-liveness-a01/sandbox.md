---
task_id: dotfiles-T128-seat-liveness-a01
seat: claude-standard-dot-a003
permission_gated_commands: 7
---

# Sandbox record: dotfiles-T128-seat-liveness-a01

Period: from the AGMSG-TASK (2026-10-15T06:05:59Z) to the RESULT. These ran inside the sandbox:

- the fetch, the branch and the task copy with its hash;
- the premises;
- the edits, the tests (with `commit.gpgsign=false` through git's environment), the baseline run on `origin/main` in a scratch worktree, which was removed with `git worktree remove`, shellcheck, shfmt, ruff, the repository validator and the mutation proofs;
- the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call, and each `agmsg-dispatch`. This copy is written before the push. Calls 1 to 7 are counted in advance, and the main-checkout copy gives the final count. A P0 or P1 from the Bot adds a fix round's push and CI watch.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the HTTPS push of `tools/seat-liveness` | `git push` |
| 2 | `gh pr create --draft` and `gh pr ready` | `gh` |
| 3 | `gh pr checks <pr> --watch` with the Bot wait beside it | `gh` |
| 4 | the re-check of the Bot's review, its comments and its summary on the final head (`gh api`) | `gh` |
| 5 | main-checkout `memory add` | main-checkout `memory add` |
| 6 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-seat-liveness-a01 …` | `agmsg-dispatch` |
