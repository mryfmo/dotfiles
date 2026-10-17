---
task_id: dotfiles-T129-normalised-comparison-lint-a01
seat: claude-review-dot-a005
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-normalised-comparison-lint-a01

- Period: from the AGMSG-TASK (2026-10-17T10:24:09Z; Amendment 1 at 10:52:00Z) to the RESULT.
- Inside the sandbox ran: the branch, every edit, the commits (`git -c commit.gpgsign=false`), every test, lint and ruff run, the HTTPS `git fetch` (the public remote needs no credential), the premise replays and the task-consistency check.
- uv ran offline (`UV_OFFLINE=1` or `--offline`).
- No local mutation was chained onto a call that ran outside the sandbox.
- No Plan Mode, so no Crit plan server was started.

Calls outside the sandbox, each planned in advance and run through the permission gate (Worker Playbook step 4), or through `excludedCommands` for `agmsg-dispatch`:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `git push origin lint/normalised-comparisons-a01`: two attempts failed outside the sandbox too (`git@github.com: Permission denied (publickey)`: the global git config rewrites `https://github.com/` to SSH for pushes and no key is reachable), then the boundary script's form succeeded, `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin lint/normalised-comparisons-a01` (validation §7) | `git push` |
| 2 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head lint/normalised-comparisons-a01 …` (the first call named the body file by the sandbox's `$TMPDIR`, which differs outside it, and failed to open it; the second used the absolute path): PR #387 | `gh` |
| 3 | the second push with the evidence commit, then `gh pr ready <pr>` | `git push`, `gh` |
| 4 | `gh pr checks <pr> --watch` (background, exit status joined) | `gh` |
| 5 | `gh api` reads of the Bot's reviews and comments on the head, at most every 30 seconds, for at most 15 minutes; `gh pr comment <pr> --body '@codex review'` only at 10 minutes without a review | `gh` |
| 6 | after a P0/P1 fix round only: the push, then `gh pr comment <pr> --body '@codex review'` and the same Bot wait (`bot_rounds=2`) | `git push`, `gh` |
| 7 | `agmsg-dispatch … AGMSG-PONG …` (question 1, the two alive notes) and `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T129-normalised-comparison-lint-a01 …` | `agmsg-dispatch` |
