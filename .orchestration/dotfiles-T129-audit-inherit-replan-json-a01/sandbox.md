---
task_id: dotfiles-T129-audit-inherit-replan-json-a01
seat: claude-standard-dot-a006
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T129-audit-inherit-replan-json-a01

- Period: from the AGMSG-TASK (bus 2026-10-17T10:24:21Z) to the RESULT.
- Inside the sandbox ran: the branch and the rebase, the commits (`git -c commit.gpgsign=false`), every test, lint and mutant run, the scratch worktree of `origin/main` and its removal (`git worktree remove`), the evidence, the CompactionDB `memory add` in the worktree's own database, the HTTPS `git fetch`, and the HTTPS `git push` in the documented form (`GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles tools/audit-inherit-replan-json`).
- uv ran with `UV_OFFLINE=1`.
- No local mutation was chained onto a call that ran outside the sandbox.

Calls outside the sandbox, through the permission gate (`dangerouslyDisableSandbox`) for `gh` and the one diagnostic run, and through `excludedCommands` for `agmsg-dispatch`; rows 2 to 7 are planned in advance:

| # | Command | Step 4 case |
|--:|---|---|
| 1 | in the scratch worktree of `origin/main`: `UV_OFFLINE=1 uv run python -m unittest tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_accepts_a_dispatch_list; git config --global --get init.defaultBranch`, to tell whether the sandbox caused the gate suite's failures (it did not: the test failed outside it too); read-only, no repository mutation | diagnostic |
| 2 | `gh pr create --draft --repo mryfmo/dotfiles --base main --head tools/audit-inherit-replan-json --title … --body-file …` | `gh` |
| 3 | `gh pr ready <pr>` | `gh` |
| 4 | `gh pr checks <pr> --repo mryfmo/dotfiles --watch` (background, exit status joined) | `gh` |
| 5 | the Bot wait: `gh api` reads of the Bot's reviews, top-level comments and issue comments on the head, at most every 30 seconds up to 15 minutes, and `gh pr comment <pr> --repo mryfmo/dotfiles --body '@codex review'` only at 10 minutes without a review | `gh` |
| 6 | after a P0/P1 fix round only: the push, then `gh pr comment <pr> --body '@codex review'` and the same wait (`bot_rounds=2`) | `gh` |
| 7 | `agmsg-dispatch … AGMSG-RESULT v1 task_id=dotfiles-T129-audit-inherit-replan-json-a01 …` | `agmsg-dispatch` |
