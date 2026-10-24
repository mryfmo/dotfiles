---
task_id: dotfiles-T133-dispositions-a01
round: 1
---

# Sandbox

Claude Code seat `claude-standard-dot-a009` in its own worktree `.claude/worktrees/worker-c`, with the Bash sandbox on (macOS Seatbelt) in auto mode. The branch `tools/dispositions-a01` was created fresh from `origin/main` de3b73cc after one `git fetch origin`. Both are single commands inside the sandbox. The branches `tools/result-precheck-a01` (#411) and `tools/task-generator-plan-check-a01` (#417) are untouched.

Inside the sandbox ran:

- every edit;
- the task-file copy from the main checkout (read only);
- both test modules, which use temporary repositories, a file URL, a stub `gh` that fails, and a fake gate interpreter that hands `dispositions.py` to the real one;
- the red run, in a scratch worktree of the code head with `orch-gate.sh` restored from `origin/main` and removed with `git worktree remove --force`;
- `make format`, `shfmt -d` and `shellcheck` on `orch-gate.sh`, and ruff on the changed files;
- the legacy-evidence counts;
- `contextdb_cli.py memory add` into this worktree's ledger.

Outside the sandbox, each as a single command:

- the real run of `dispositions.py 409 4fe24380… --feedback <main checkout sweep>`, so that `gh api repos/mryfmo/dotfiles/pulls/comments/<id>` resolves the two thread commits (read-only GET);
- the gh commands of the PR (Worker Playbook step 4);
- `agmsg-dispatch` for the RESULT.

`git push` runs inside the sandbox with the one-command rule `-c url.https://github.com/mryfmo/.pushInsteadOf=https://github.com/mryfmo/`. No `@codex review` was posted. No string naming the PR-create or merge commands passed through a Bash heredoc or echo; the PR body was written with the file tool.

`origin/main` moved to 3e41e36a (#409) during the task, so the caps are read three-dot against the merge base de3b73cc.

Revise 1 (round 2): `git switch tools/dispositions-a01` and `git merge --ff-only origin/tools/dispositions-a01` (to the orchestrator's fa47987b), each a single command; the red replay in a scratch worktree of fa47987b and the Check inside the sandbox. The real run is redone per the audit: the two `gh api .../pulls/comments/<id>` reads outside the sandbox, one command each, and `dispositions.py --commits` inside it, so the helper itself never leaves the sandbox. A first replay attempt passed zsh's `$T:test_...`, which zsh reads as the `:t` modifier; it mangled the arguments and was discarded and rerun with `${T}`.

effects=none
