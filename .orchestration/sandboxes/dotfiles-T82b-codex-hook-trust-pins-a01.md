# Sandbox: dotfiles-T82b-codex-hook-trust-pins-a01

- **Sandboxed:** edits, the generator run, unit tests, `make unit-test`, `make render-check`, the validator, prettier, ruff, and the commit.
- **Outside the sandbox, read-only:**
  - reading `~/.codex/config.toml`, `~/.codex/{standard,security}.config.toml` and the installed Ponytail and Crit hook files;
  - reading Codex sources through `gh api`;
  - the dry runs of the base and `standard` modify scripts, with the live files as stdin and output to temp files.
- **`codex app-server`, once:** run outside the sandbox with a 30-second timeout, sending only `initialize` and `hooks/list`. Codex's own state and log databases and model cache under `~/.codex` changed afterwards; other Codex sessions were active, so those writes cannot be attributed. I edited nothing under `~/.codex`.
- **Through the permission gate:** push, `gh pr create`, `gh pr checks`, the bot-wait polling, CompactionDB `memory add`, writing and masking these artifacts in the main checkout (Worker Playbook step 4), and `agmsg-dispatch`.
- **Not done:** no `make update`/`apply`, no edits to permgate, the permgate policy or any Claude-boundary source, no thread resolution, no local bats.
- **Revise round 3:** the same split. Outside the sandbox: the push, `gh pr checks`, the bot-wait polling, writing and masking the artifacts, and `agmsg-dispatch`. The live base dry run was read-only, with output to a temp file. The `codex app-server` probe was not repeated.
- **Revise round 4:** the live base dry run ran inside the sandbox, as the round-4 disposition requires. It read `~/.codex/config.toml` and wrote only under `$TMPDIR`. Outside the sandbox: the push, `gh pr checks`, the bot-wait polling, writing and masking the artifacts, and `agmsg-dispatch`. The scratch worktree that ran the round-4 tests on the previous head was added in the session scratchpad and removed with `git worktree remove --force`, without a prune.
- **Revise round 5:** the live base dry run ran inside the sandbox, reading `~/.codex/config.toml` and writing only under `$TMPDIR`. The scratch worktree for the previous-head test run was added in the session scratchpad and removed with `git worktree remove --force`, without a prune. Outside the sandbox: the push, `gh pr checks`, the bot-wait polling, writing and masking the artifacts, and `agmsg-dispatch`.
- **Revise round 6:** the same split as round 5. The live base dry run ran inside the sandbox, and the scratch worktree for the previous-head test run was removed with `git worktree remove --force`, without a prune.
- **Revise round 7:** the same split as round 5. The live base dry run ran inside the sandbox, and the scratch worktree for the previous-head test run was removed with `git worktree remove --force`, without a prune.
- **Revise round 8:** the same split as round 5. The live base dry run ran inside the sandbox, and the scratch worktree for the previous-head test run was removed with `git worktree remove --force`, without a prune. The restored round-0 blocks were copied from the original raw outputs under `/tmp/claude-1000/t82bv/`.
