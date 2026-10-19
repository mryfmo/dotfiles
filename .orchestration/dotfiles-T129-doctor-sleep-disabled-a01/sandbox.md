---
task_id: dotfiles-T129-doctor-sleep-disabled-a01
seat: claude-review-dot-a005
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-doctor-sleep-disabled-a01

- Period: from the AGMSG-TASK (2026-10-17T13:50:58Z; Amendment 1 at 14:14:53Z) to the RESULT.
- Inside the sandbox ran: the branch, every edit, the commits (`git -c commit.gpgsign=false`), the test, shellcheck, shfmt, `make doctor` (its runtime check fails there because the sandbox denies mise's network host; recorded as is), the HTTPS `git fetch`, the premise replay and the task-consistency check.
- No local mutation was chained onto a call that ran outside the sandbox. No Plan Mode, so no Crit plan server.

Calls outside the sandbox, planned in advance and run through the permission gate (Worker Playbook step 4), or through `excludedCommands` for `agmsg-dispatch`:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin doctor/sleep-disabled-a01` (the boundary script's form: the global config rewrites HTTPS pushes to SSH and the seat reaches no key) | `git push` |
| 2 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head doctor/sleep-disabled-a01 …` | `gh` |
| 3 | the second push with the evidence commit, then `gh pr ready <pr>` | `git push`, `gh` |
| 4 | `gh pr checks <pr> --watch` (background) and the bounded Bot wait (`gh api` reads at most every 30 seconds for at most 15 minutes; `gh pr comment <pr> --body '@codex review'` only at 10 minutes without a review) | `gh` |
| 5 | after a P0/P1 fix round only: the push, then `@codex review` and the same wait (`bot_rounds=2`) | `git push`, `gh` |
| 6 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T129-doctor-sleep-disabled-a01 …` | `agmsg-dispatch` |
