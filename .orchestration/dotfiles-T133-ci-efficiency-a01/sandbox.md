---
task_id: dotfiles-T133-ci-efficiency-a01
seat: claude-standard-dot-a011
permission_gated_commands: see the table
---

# Sandbox record: dotfiles-T133-ci-efficiency-a01

- Period: from the AGMSG-TASK (2026-10-18T04:22:16Z) and amendment 1 (04:34:47Z) to the RESULT.
- Worktree: `.claude/worktrees/worker-d`. Item 0(a) finished T132 on `tools/make-update-followups-a01` first: records commit `6121555d`, push, `gh pr ready 405` and `gh pr ready 402`. The worker review of T132 found a P1 before that commit, fixed in `7eb9438f`/`09414805` (T132's records). This task then started on a fresh branch `tools/ci-efficiency-a01` from `origin/main` `99a4a80f` (`git switch -c … --no-track`). The T132 branch was committed, pushed and clean before the switch.
- Inside the sandbox ran: every edit, the commits (`git -c commit.gpgsign=false`), the tests, shellcheck, shfmt, ruff, prettier, `make format`, `make render-check`, the task-consistency check, the HTTPS `git fetch`, and the `gh` reads and writes listed below. `gh` works inside the sandbox on this machine.
- Network beyond the default, granted per command through `allowed_domains`: the measurement's failed-job log reads needed `results-receiver.actions.githubusercontent.com`, `*.actions.githubusercontent.com` and `*.blob.core.windows.net`. `gh` also needed `XDG_CACHE_HOME=$TMPDIR/gh-cache`, because the sandbox denies `~/.cache/gh` (measure.md "How").
- Push: `git push` fails inside the sandbox since `~/.config/git/config` carries `url.git@github.com:.pushInsteadOf https://github.com/`; the SSH connection is refused by the proxy. Every push therefore uses the HTTPS form `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin <branch>`, inside the sandbox. No other global setting is involved.
- Tests that run `update_omp`/`update_hcom` need the validation-only `mktemp` shim in the scratchpad, as in T132. `make unit-test` ran with it (validation §4a), and CI is the authority.
- Scratch worktrees for the red run were added under the scratchpad and removed with `git worktree remove`. `git worktree prune` was never run. No Plan Mode was used, so there is no Crit plan server.
- No local mutation was chained onto a call that ran outside the sandbox.

GitHub writes, all inside the sandbox and all named by item 0 or the Completion clause: `gh pr ready 405`, `gh pr ready 402`, `gh pr create --draft --base main --head tools/ci-efficiency-a01 …` (the plain create form) and `gh pr ready <this PR>` when CI is green. No comment, review or edit was run, and `ci-rerun.sh` was never run against GitHub.

Calls outside the sandbox, all through `excludedCommands` (Worker Playbook step 11):

| # | Command | Step 4 case |
|--:|---|---|
| 1 | `agmsg-dispatch … 'AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-a01 status=question …'` (the `allowed_files` gap, answered by amendment 1) | `agmsg-dispatch` |
| 2 | `agmsg-dispatch … 'AGMSG-RESULT v1 task_id=dotfiles-T132-make-update-followups-a01 …'` (item 0(a)) | `agmsg-dispatch` |
| 3 | `agmsg-dispatch … 'AGMSG-RESULT v1 task_id=dotfiles-T133-ci-efficiency-a01 …'` | `agmsg-dispatch` |
