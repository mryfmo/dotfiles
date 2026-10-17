---
task_id: dotfiles-T128-chain-review-scripts-followup-a02
seat: claude-standard-dot-a003
permission_gated_commands: 7
---

# Sandbox record: dotfiles-T128-chain-review-scripts-followup-a02

Period: from the AGMSG-TASK (2026-10-16T22:28:37Z) to the RESULT. These ran inside the sandbox: the fetch, the branch, the task copy with its hash (read from the main checkout), the reads, the edits, the tests, shellcheck, shfmt, ruff, the mutation proofs, the repository validator and the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call, and each `agmsg-dispatch`. This copy is written before the push, so all seven are counted in advance; the main-checkout copy gives the final count. A P0 or P1 from the Bot adds a fix round's push, `@codex review` and wait.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the HTTPS push of `tools/local-review-env-s-quoting` | `git push` |
| 2 | `gh pr create --draft` and `gh pr ready` | `gh` |
| 3 | `gh pr checks <pr> --watch`, then the `gh api` wait until the Bot's code and security reviews of the head completed, and the read of its reviews, comments and reactions (background) | `gh` |
| 4 | the read of any Bot thread's body (`gh api`) | `gh` |
| 5 | main-checkout `memory add` | main-checkout `memory add` |
| 6 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-a02 …` | `agmsg-dispatch` |
