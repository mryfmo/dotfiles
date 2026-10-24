---
task_id: dotfiles-T133-result-precheck-a01
round: 1
amendment: 1
---

# Sandbox

Claude Code seat `claude-standard-dot-a009` in its own worktree `.claude/worktrees/worker-c`, Bash sandbox on (macOS Seatbelt), auto mode.

Item 0 ran first on `tools/omp-config-render`: the two parked records were masked and committed as 2e978db7 (`git -c commit.gpgsign=false`), pushed over HTTPS inside the sandbox with the one-command rule `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/` (the global `pushInsteadOf` turns the HTTPS remote into SSH, which the sandbox proxy refuses), and opened as draft PR #406 with `gh pr create` outside the sandbox through the permission gate (Worker Playbook step 4).

The auto-mode classifier then denied two commands: the `agmsg-dispatch` of the item 0 PONG ("Unrequested Commit in a Connected App") and a chain of `git fetch origin`, `git switch -c tools/result-precheck-a01 --no-track origin/main` and the task-file copy ("External System Writes"). Neither was retried in another form; a blocked PONG (message 2090) reported both, and the orchestrator's PING of 04:30:59Z re-tasked the switch alone inside the sandbox, which then ran (origin/main was current at 99a4a80f, so no fetch).

Inside the sandbox: every edit; the task-file copies (`cp` from the main checkout, read only); shfmt, shellcheck, `uvx ruff`, prettier through `mise x`; the unit tests, which run the scripts as subprocesses in temporary git repositories with stubs on PATH and a bare temporary remote (the secrets-mode and pre-push cases call the real masker through the real uv); a mutation check that disabled one control at a time in a backed-up copy and restored it (hash verified); `make render-check`, `make validate-agent-assets`, `make unit-test`, `make format` and the precheck itself.

Permission-gated or outside the sandbox: `gh pr create` for #406 and for this task's PR, `gh pr ready`, `gh pr checks` and the Bot listing (Worker Playbook step 4); `agmsg-dispatch` (in `claude.sandbox.excludedCommands`) for the PONGs and the RESULT. `git push` runs inside the sandbox with the HTTPS rule above.

Known sandbox effect: `make unit-test` fails 296 tests here (the 8 `test_agmsg_*` tests of `tests/unit/test_runtime_health.py` among them, which fail because `mktemp` is denied the system temp directory); validation.md shows the identical set failing on a pristine `origin/main` worktree in the same sandbox.

effects=none
