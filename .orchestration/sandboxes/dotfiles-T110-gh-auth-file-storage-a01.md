# Sandbox: dotfiles-T110-gh-auth-file-storage-a01

- **Worktree:** `.claude/worktrees/worker-c`, branch `fix/gh-auth-file-storage` from `origin/main` `46002810` (`git switch -c … --no-track`).
- **Sandboxed:**
  - the inbox read (it printed a harmless herdr pane-rename refusal);
  - edits, `bash -n`, shellcheck, ruff (via `uv run --no-project --with ruff`; exact commands and output in the validation file's "Ruff (PONG decision 1, head a431fd46)" section), prettier;
  - the two unit modules, `make unit-test` and the validator;
  - the read-only live gh probes (`gh auth status --json hosts`, tokens redacted with sed, and `--jq … .tokenSource`);
  - the commits, `git push`, `gh pr create`, `gh pr checks` and the bot-wait polling. Since T108/#293 the active login is file-stored, so the sandboxed `gh` and `git push` worked; no 401 occurred and nothing needed the permission gate.
- **Through the permission gate (Worker Playbook step 4):**
  - the CompactionDB `memory add` in the main checkout;
  - writing and masking these artifacts in the main checkout;
  - `agmsg-dispatch`: the first run went into the sandbox, not out through `excludedCommands`, and failed with `Operation not permitted` / `pane not found or unavailable: wT:p1` before inserting a row (checked in messages.db); the retry outside the sandbox delivered the RESULT (row 2064, read 08:59:42Z).
- **Credentials:** no command read, listed or printed a credential value. The one `gh auth status` text probe piped through `sed -E 's/gh[opsu]_[A-Za-z0-9_]+/<redacted>/g'`; gh itself masks the token there. The script and doctor tests ran only against fake HOMEs and a fake `gh`.
- **Not done:** no `make update`/`apply`/`make gh-auth`, no `gh auth login`/`logout`, no thread resolution, no change outside the five allowed files.

## Revise round 1

- Same isolation as round 0: edits, tests, `make unit-test`, the validator, prettier, the commit, `git push`, `gh pr checks` and the Bot polling ran sandboxed; the artifact appends and masking and `agmsg-dispatch` ran outside the sandbox through the permission gate.

## Revise round 2

- Same isolation as rounds 0 and 1: edits, tests, `make unit-test`, the validator, prettier, `crit status`, the task-file `sha256sum` read, the commit, `git push`, `gh pr checks` and the Bot polling ran sandboxed; the artifact appends and masking, and `agmsg-dispatch` ran outside the sandbox through the permission gate.

## Revise round 3

- Same isolation as round 2: edits, tests, `make unit-test`, the validator, prettier, the task-file `sha256sum` read, the commit, `git push`, `gh pr checks` and the Bot polling ran sandboxed; the artifact appends and masking, and `agmsg-dispatch` ran outside the sandbox through the permission gate.
