---
task_id: dotfiles-T128-chain-review-scripts-followup-a04
seat: claude-standard-dot-a007
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T128-chain-review-scripts-followup-a04

- Period: from the AGMSG-TASK (2026-10-17T10:16:41Z) to the RESULT.
- Inside the sandbox (Claude Code, macOS Seatbelt) ran: the HTTPS `git fetch`; the branch, the task copy, the edits and the commit (`git -c commit.gpgsign=false`); every test, lint and mutation run; the masker and `make validate-agent-assets` (uv in its offline form); and the HTTPS `git push`, with a one-command `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/` rule so the configured SSH push URL is not used (no configuration is written).
- Read only, outside this worktree: the main checkout's task file (`$MAIN/.orchestration/tasks/<task>.md`). Nothing was written outside worker-c except files under `$TMPDIR` and the scratchpad.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox: `gh` through the permission gate (`dangerouslyDisableSandbox`, since Seatbelt denies gh's TLS trust lookup, Worker Playbook step 4) and `agmsg-dispatch` through `excludedCommands`. These rows are planned in advance, so no evidence update moves the head after the Bot's review:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/chain-review-scripts-followup-a04 …` | `gh` |
| 2 | `gh pr ready <pr>` | `gh` |
| 3 | `gh pr checks <pr> --watch` (background, exit status joined) | `gh` |
| 4 | the Bot wait: `gh api --paginate` reads of the Bot's reviews, top-level review comments and issue comments on the head, every 30 seconds for at most 15 minutes, and `gh pr comment <pr> --body '@codex review'` only at 10 minutes without a review | `gh` |
| 5 | `gh pr view` reads of the head and its state | `gh` |
| 6 | after a P0/P1 fix round only: the push (inside, as above), then `gh pr comment <pr> --body '@codex review'` and the same Bot wait for the re-review (`bot_rounds=2`) | `gh` |
| 7 | `agmsg-dispatch … AGMSG-PONG v1 …` and `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T128-chain-review-scripts-followup-a04 …` | `agmsg-dispatch` |
