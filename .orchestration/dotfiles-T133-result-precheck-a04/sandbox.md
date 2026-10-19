---
task_id: dotfiles-T133-result-precheck-a04
round: 1
---

# Sandbox

Claude Code seat `claude-standard-dot-a009`, in its own worktree `.claude/worktrees/worker-c`, with the Bash sandbox on (macOS Seatbelt) in auto mode. Branch `tools/result-precheck-a01` (PR #411) continues from ddf262de after `git fetch origin` and a fast-forward. Each was a single command inside the sandbox.

Inside the sandbox:

- Every edit, and the reset bookkeeping the task directs: `git rm` of the a03 task copy, and the a04 copy taken from the main checkout's dispatched text, which was only read.
- The red replays, each in a scratch worktree of the production commit with this head's test module copied in, each removed with `git worktree remove --force`:
  - ddf262de for the eight hardening regressions;
  - 4ed1b27a for a03's four item 5 to 7 regressions;
  - 9cd5514a for the three revise-1 regressions.
- Both unit modules, shellcheck and shfmt.
- `make unit-test` and `make format` on a pristine detached worktree of the merge base 740772ef, then removed.
- The default precheck run and the final proof, whose selector worktree the script adds and removes.
- The push, with the one-command rule `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/`.

The test fixtures now run with HOME set to a directory inside their own temporary directory, and with no inherited `GIT_CONFIG*` or `XDG_CONFIG*` override (hardening item 4).

Outside the sandbox or permission-gated:

- `gh pr checks`, `gh pr view` and the Bot listing (Worker Playbook step 4).
- `agmsg-dispatch`, for the blocked PONG of 01:20:05Z and for the RESULT.

Each `gh` command and each git write runs as a single command; no `@codex review` comment is posted.

Interruption: none in a04. The seat came to a04 with no audit-pool-a01 work started, so nothing needed committing first.

A stopped run and a denied cleanup:

- The first default precheck run, on bf1bce63, was stopped while its unit-test phase ran, because the correction round edited `result-precheck.sh` under the running script.
- It never reached its EXIT trap, so its private work directory `/tmp/claude-501/result-precheck.UsWK1Z` remains. It holds partial `make unit-test` output, captured unmasked, and no record. Its log had stopped growing before removal was attempted.
- `rm -rf -- /tmp/claude-501/result-precheck.UsWK1Z` was denied at the permission prompt. It was not retried in any other form; the operator may delete the directory.
- A second default run, on 7ccc8287, was corrupted the same way: I edited the ShellCheck directive under it. I restored the committed bytes at once, but bash had already read past them, and it stopped on a syntax error. Its output is discarded, and its EXIT trap removed its own work directory.
- The default run was repeated on the final code head 9f6ec7c9, with nothing edited under it (validation.md).

`make unit-test` fails inside the sandbox on sandbox-denied operations. The failing set is compared with the merge base's in the same sandbox (validation.md), and CI decides the full suite.

effects=none
