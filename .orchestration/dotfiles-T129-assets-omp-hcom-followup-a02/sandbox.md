---
task_id: dotfiles-T129-assets-omp-hcom-followup-a02
seat: claude-standard-dot-a007
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-assets-omp-hcom-followup-a02

- Period: from the AGMSG-TASK (2026-10-17T16:47:37Z) to the RESULT.
- Inside the sandbox (Claude Code, macOS Seatbelt) ran: the branch from PR #398's head 2b91aef9, the commits (`git -c commit.gpgsign=false`); the task copy, the edits, every test, lint and mutation run (uv offline; the updater tests with the evidence-run `mktemp` shim of the a01 task first on PATH); the masker and `make validate-agent-assets`; and the HTTPS `git push` with a one-command `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/` rule (no configuration is written).
- One local mutation ran outside the sandbox, a mistake: `git fetch origin tools/assets-hcom-receipt` was chained after the read-only `gh pr view 398` in one call under the permission gate. It updated only the shared remote-tracking ref of that branch, which the same fetch does inside the sandbox; every other local mutation ran inside.
- Read only, outside this worktree: the main checkout's task file, the a01 and T130 acceptance records and the T130 local review file. Nothing was written outside worker-c except files under `$TMPDIR` and the scratchpad.

Calls outside the sandbox: `gh` reads through the permission gate (`dangerouslyDisableSandbox`) and `agmsg-dispatch` through `excludedCommands`. Since the operator's notice of 01:1x JST every gh write prompts a human, so none runs from this seat at night:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr view 398` (a read) | `gh` |
| 2 | `agmsg-dispatch … AGMSG-PONG v1 task_id=dotfiles-T129-assets-omp-hcom-followup-a02 status=blocked …` naming `gh pr create` | `agmsg-dispatch` |
| 3 | after #398 merges and the approval: `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/assets-hcom-followup-a02 …` and `gh pr ready <pr>` | `gh` (a write: the human's prompt) |
| 4 | `gh pr checks <pr> --watch` and the Bot wait's `gh api` reads | `gh` |
| 5 | `@codex review` only at 10 minutes without a review, a gh write | `gh` |
| 6 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T129-assets-omp-hcom-followup-a02 …` | `agmsg-dispatch` |
