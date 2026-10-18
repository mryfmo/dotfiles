---
task_id: dotfiles-T133-result-precheck-a02
round: 1
reset_of: dotfiles-T133-result-precheck-a01
---

# Sandbox

Claude Code seat `claude-standard-dot-a009` in its own worktree `.claude/worktrees/worker-c`, Bash sandbox on (macOS Seatbelt), auto mode, on the branch `tools/result-precheck-a01` (PR #411), which this reset task continues from a5cb73b4, a01's last head.

Inside the sandbox: every edit; the copy of the dispatched task file from the main checkout (read only); shfmt, shellcheck, `uvx ruff`, prettier through `mise x`; the unit tests, which run the scripts as subprocesses in temporary git repositories with stubs on PATH and a temporary bare remote, the secrets and push cases calling the real masker through the real uv; the red runs, each in a detached temporary worktree at a5cb73b4 with the current test file copied in, removed with `git worktree remove --force`; the full-tree masker measurement (a temporary copy of every tracked file, removed afterwards); `make render-check`, `make validate-agent-assets`, `make unit-test`, `make format`, the precheck runs, and the `origin/main` baseline worktree, removed the same way. `git worktree prune` was never run; the 30 worktrees other sessions left registered were not touched.

Permission-gated or outside the sandbox: `gh pr checks`, the Bot listing and `gh` reads (Worker Playbook step 4); `agmsg-dispatch` for the RESULT. `git push` runs inside the sandbox with the one-command rule `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/` (the global `pushInsteadOf` would turn it into SSH, which the sandbox proxy refuses). Every `gh` command and every git write ran on its own, never chained (the no-prompt rule of 05:07Z); no `@codex review` was posted.

Known sandbox effect: `make unit-test` fails tests that fail identically on a pristine `origin/main` worktree in the same sandbox (validation.md), so the final proof uses `--tests` on this task's two modules (Amendment 2 of a01, item 1 here) and CI decides the full suite.

Revise 1 (round 2), after the P1-12 RESULT as the ACCEPTANCE ordered: `git switch tools/result-precheck-a01` and `git merge --ff-only origin/tools/result-precheck-a01` (to the orchestrator's 9cd5514a), each a single command in the sandbox; the fixes, the red and green runs and the precheck with `--previous-head 9cd5514a… --check` ×3 (its selector worktree added and removed by the script) inside the sandbox; `contextdb_cli.py memory add` into this worktree's ledger; then one evidence commit, one push, CI and the Bot window as in round 1.

effects=none
