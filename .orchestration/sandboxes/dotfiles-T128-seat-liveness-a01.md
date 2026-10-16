---
task_id: dotfiles-T128-seat-liveness-a01
seat: claude-standard-dot-a003
permission_gated_commands: 12
---

# Sandbox record: dotfiles-T128-seat-liveness-a01

Period: from the AGMSG-TASK (2026-10-15T06:05:59Z) to the RESULT. These ran inside the sandbox:

- the fetch, the branch and the task copy with its hash;
- the premises;
- the edits, the tests (with `commit.gpgsign=false` through git's environment), the baseline run on `origin/main` in a scratch worktree, which was removed with `git worktree remove`, shellcheck, shfmt, ruff, the repository validator and the mutation proofs;
- the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call, and each `agmsg-dispatch`. This is the main-checkout copy with the final count: eight calls. They are the branch copy's seven, plus row 3a. The first wait was started with a mistyped head (`ee9293829`, not a prefix of the head) and stopped with TaskStop once it was seen; row 3a reran it with the full sha. The Bot raised no finding, so there was no fix round. Calls 1 to 6 have run when this copy is written (this copy is call 6), and call 7 is the RESULT.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | the HTTPS push of `tools/seat-liveness` | `git push` |
| 2 | `gh pr create --draft` and `gh pr ready` | `gh` |
| 3 | `gh pr checks <pr> --watch` with the Bot wait beside it | `gh` |
| 3a | the wait rerun with the full head `ee9293827b5f…` | `gh` |
| 4 | the re-check of the Bot's review, its comments and its summary on the final head (`gh api`) | `gh` |
| 5 | main-checkout `memory add` | main-checkout `memory add` |
| 6 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-seat-liveness-a01 …` | `agmsg-dispatch` |

**Revise round 2, the final count: twelve calls.** Round 1's eight, and round 2's four: 8 the push of `d3bc745c`, 9 the CI watch, 10 this copy of the round-2 sections into the main-checkout records, masked again, and 11 the round-2 RESULT that follows it. The baseline worktree of validation §4b ran inside the sandbox.

| # | Command | Step 4 case |
|--:|---|---|
| 8 | the HTTPS push of `d3bc745c` | `git push` |
| 9 | `gh pr checks 367 --watch` on that head | `gh` |
| 10 | the round-2 sections copied into the main-checkout records, masked again | artifact copy with the repository masker |
| 11 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-seat-liveness-a01 round=2 …` | `agmsg-dispatch` |

