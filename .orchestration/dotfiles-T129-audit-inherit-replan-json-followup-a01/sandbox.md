---
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a01
seat: claude-standard-dot-a011
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-audit-inherit-replan-json-followup-a01

- Period: from the AGMSG-TASK (2026-10-18T06:27:55Z) to the PONG that reports the pushed head, and later to the RESULT, after the orchestrator's PING for the PR.
- Worktree: `.claude/worktrees/worker-d`. The T133 branch `tools/ci-efficiency-a01` was committed, pushed (`27613c0c`) and clean before the switch, and it stays for its integration.
- Branch, each a single command as the dispatch note asks: `git fetch origin tools/audit-inherit-replan-json`, then `git switch -c tools/audit-inherit-replan-json-followup-a01 741e24272fd64b6a36c0d6725c53265de1c94982`. The branch is stacked on PR #390's head.
- The following ran inside the sandbox: every edit, the commits (`git -c commit.gpgsign=false`), the tests, shellcheck, shfmt, ruff, the task-consistency check, and the single push. The push uses the HTTPS form `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin tools/audit-inherit-replan-json-followup-a01`, because `~/.config/git/config` rewrites pushes to SSH, which the sandbox's proxy refuses (T133 learning 1).
- `gh pr create` was not run, as the dispatch note says: a live ask rule prompts the operator. The seat pushes, sends `AGMSG-PONG v1 status=alive note=pushed-awaiting-pr-create` with the head, and waits for the orchestrator's PING before it creates the PR.
- The sandbox limit met: this machine's global `commit.gpgsign=true` with SSH signing cannot read `~/.ssh` inside the sandbox. So test fixtures that commit without `-c commit.gpgsign=false` fail. In this task's Check that is `test_require_crit_review` (validation §6a), identically at `741e242`. CI is the authority.
- Scratch worktrees for the red run and the `741e242` baseline were added under the scratchpad and removed with `git worktree remove --force`, the scratch copy holding the tests' untracked output. `git worktree prune` was never run. No Plan Mode was used, so there is no Crit plan server.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox, all through `excludedCommands` (Worker Playbook step 11):

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … 'AGMSG-PONG v1 task_id=dotfiles-T129-audit-inherit-replan-json-followup-a01 status=alive note=pushed-awaiting-pr-create …'` | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … 'AGMSG-RESULT v1 task_id=dotfiles-T129-audit-inherit-replan-json-followup-a01 …'` | `agmsg-dispatch` |
