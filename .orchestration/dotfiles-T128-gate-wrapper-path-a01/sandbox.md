---
task_id: dotfiles-T128-gate-wrapper-path-a01
seat: claude-standard-dot-a003
permission_gated_commands: 8
---

# Sandbox record: dotfiles-T128-gate-wrapper-path-a01

Period: from the AGMSG-TASK (2026-10-14T06:43:39Z) to the RESULT. These ran inside the sandbox:

- the fetch, the branch and the task copy with its hash;
- the edits, the tests, shellcheck, shfmt, ruff, the `mktemp` probe and the mutation proofs;
- the commits.

`permission_gated_commands` counts every Bash call made with `dangerouslyDisableSandbox`, one per call. This copy is written before the push. Call 1 has run. Calls 2 to 8 are counted in advance, and the main-checkout copy gives the final count.

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `scratchpad/path-probe.sh`: the private bin built as orch-gate.sh does, then `env -i PATH=<private> HOME NO_COLOR=1 gh repo view --json nameWithOwner` and one `git rev-parse` (validation §3) | `gh` |
| 2 | the HTTPS push of `tools/gate-wrapper-path` | `git push` |
| 3 | `gh pr create --draft` and `gh pr ready` | `gh` |
| 4 | `gh pr checks <pr> --watch` with the Bot wait beside it | `gh` |
| 5 | the Bot's reviews and comments on the final head (`gh api`) | `gh` |
| 6 | main-checkout `memory add` | main-checkout `memory add` |
| 7 | the masked copy of the evidence files to the main checkout | artifact copy with the repository masker |
| 8 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-gate-wrapper-path-a01 …` | `agmsg-dispatch` |
