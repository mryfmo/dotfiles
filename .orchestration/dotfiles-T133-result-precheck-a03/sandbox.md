---
task_id: dotfiles-T133-result-precheck-a03
round: 1
---

# Sandbox

Claude Code seat `claude-standard-dot-a009` in its own worktree `.claude/worktrees/worker-c`, Bash sandbox on (macOS Seatbelt), auto mode. Branch `tools/result-precheck-a01` (PR #411), continued from 4ed1b27a after `git fetch origin` and `git switch`, each a single command inside the sandbox. The branches `tools/task-generator-plan-check-a01` (#417) and `tools/dispositions-a01` (#419) are untouched.

## Inside the sandbox

- Every edit, and the reset bookkeeping the task directs: the a03 task copy, and `git rm` of the a01 and a02 task copies.
- The red replays, each in a scratch worktree of the reviewed production commit (9cd5514a or 4ed1b27a) with this head's test module copied in, removed with `git worktree remove --force`.
  - A first attempt prefixed `/usr/bin` to PATH, which made `python3` resolve to the system 3.9. The writer then failed on `from datetime import UTC` and the masker failed. That run was discarded as an environment error, not a red result.
  - The rerun used the normal PATH, where `python3` is mise's 3.15.
- The Check commands, the default precheck run and the full unit suite on a pristine `origin/main` worktree.
- The final proof, whose selector worktree is added and removed by the script.
- The test modules, which use temporary repositories with bare origins, the real detector through the real `uv` for the push cases, and stubbed `uv` elsewhere.

## Outside the sandbox or permission-gated

- `gh pr checks` and the Bot listing (Worker Playbook step 4).
- `agmsg-dispatch` for the RESULT.

`git push` runs inside the sandbox with the one-command rule `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/`. Every gh command and git write runs on its own. No `@codex review` is posted. No string naming the PR merge or create commands passes through a Bash heredoc or echo.

## Known sandbox effect

`make unit-test` fails tests that fail identically on a pristine `origin/main` worktree in the same sandbox (validation.md). So the final proof uses `--tests` on this task's two modules, and CI decides the full suite.

effects=none
