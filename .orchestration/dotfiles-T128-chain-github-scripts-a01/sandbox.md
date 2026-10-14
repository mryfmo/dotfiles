---
task_id: dotfiles-T128-chain-github-scripts-a01
seat: claude-standard-dot-a003
permission_gated_commands: 8
---

# Sandbox record: dotfiles-T128-chain-github-scripts-a01

Period: from the AGMSG-TASK (2026-10-14T08:59:19Z) to the RESULT. These ran inside the sandbox:

- the fetch, the branch and the task copy with its hash;
- the edits, the tests, shellcheck, shfmt, ruff, the repository validator, the wall-hours probe and the mutation proofs;
- the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This copy is written before the push. Calls 1 to 8 are counted in advance, and the main-checkout copy gives the final count. A P0 or P1 from the Bot adds a fix round's push and CI watch.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the HTTPS push of `tools/chain-github-scripts` | `git push` |
| 2 | `gh pr create --draft` and `gh pr ready` | `gh` |
| 3 | `gh pr checks <pr> --watch` with the Bot wait beside it (background) | `gh` |
| 4 | the Bot's review and comments on the final head (`gh api`) | `gh` |
| 5 | the review body and each inline comment (`gh api`) | `gh` |
| 6 | main-checkout `memory add` | main-checkout `memory add` |
| 7 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 8 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-github-scripts-a01 …` | `agmsg-dispatch` |
