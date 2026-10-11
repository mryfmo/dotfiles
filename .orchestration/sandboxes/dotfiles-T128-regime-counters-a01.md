# Sandbox: dotfiles-T128-regime-counters-a01

- Seat: Claude Code worker `claude-standard-dot-a004`, worktree `.claude/worktrees/worker-c`, macOS Seatbelt sandbox per Bash command. Branch `feat/regime-counters` created with `git switch -c feat/regime-counters --no-track origin/main` (no `.git/config` write); the parked `feat/main-tests` branch was not touched.
- Isolation: every edit stayed inside the worktree and `allowed_files` (plus the task's own first-commit path `.orchestration/dotfiles-T128-regime-counters-a01/task.md`). Fixture data and scratch files were written under `$TMPDIR` (`/tmp/claude-501/t128`).
- Commands run outside the sandbox through the permission gate (Worker Playbook step 4's documented cases), each for the reason given:
  - `gh` (pr create/edit/ready/checks, `gh api` for fixtures, CI logs and the Bot wait): inside the sandbox gh fails TLS verification (`x509: OSStatus -26276`).
  - `git push`: as `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git feat/regime-counters`. The global `url.git@github.com:.pushInsteadOf https://github.com/` rewrites an HTTPS push to SSH, and no SSH key is readable (`Permission denied (publickey)`).
  - The live runs of `scripts/regime-counters.sh` (full form) and `make check-regime-boundary`: they call `gh api`; inside the sandbox every Bot count would print `unknown`.
  - Writing these five artifacts into the main checkout and masking them with the repository masker: the main checkout is not writable from the worktree sandbox.
  - `uv run --no-project .claude/hooks/contextdb_cli.py memory add` against the main checkout's CompactionDB.
  - `agmsg-dispatch` (excludedCommands) for the PONG and the RESULT.
- Sandboxed, as documented: agmsg history reads through the storage facade (read-only, schema-guarded), `shellcheck`, `shfmt`, `ruff`, unit tests (with `GIT_CONFIG_GLOBAL=/dev/null` so commits in test fixtures do not try to sign with an unreadable SSH key), the mutation checks, and the `origin/main` baseline in a scratch worktree (`git worktree add --detach $TMPDIR/base-main origin/main`, removed with `git worktree remove`; no `prune`).
- No escalation was requested from another agent; no permission prompt was answered by an agent.
