# Sandbox: dotfiles-T111-project-map-subagent-a01

- **Worktree:** `.claude/worktrees/worker-c`, branch `feat/project-map-subagent` from `origin/main` `8e9bd072` (`git fetch origin`, then `git switch -c feat/project-map-subagent --no-track origin/main`).
- **Sandboxed:**
  - the inbox reads (they printed a harmless herdr pane-rename refusal);
  - `git fetch origin` (it printed a harmless `.gitmodules` permission warning) and the branch switch;
  - the edits, the generator run, `make render-check`, the validator, the two unit modules, `make unit-test` and prettier;
  - both commits, and the ruff format fix and check (`mise x ruff -- ruff format --config ruff.toml`);
  - the final-head re-run of every validation command.
- **Outside the sandbox (`dangerouslyDisableSandbox`, through the permission gate):**
  - `git push origin feat/project-map-subagent`, `gh pr create`, `gh pr checks 299 --watch`, `gh run view --log-failed`, the PR feedback `gh api` reads, the Bot-wait `gh api` loop and `gh pr edit 299 --body-file` (PR body only; the head stayed `0c1d280b`). Since T108/#293 a file-stored gh login works inside the sandbox too (T110 sandbox record), so taking these through the gate was unnecessary but harmless; no credential value was read or printed.
  - the CompactionDB `memory add` of both decision lines in the main checkout;
  - writing and masking these seven artifacts (report, validation, sandbox, learning, autoskill, worker-crit JSON, worker review receipt) in the main checkout;
  - `agmsg-dispatch`: the first run, for the T111 PONG, went into the sandbox instead of out through `excludedCommands` and failed with `Operation not permitted` / `pane not found or unavailable: w1A:p1`. The retry outside the sandbox delivered it (messages.db row 2144, read 2026-10-06T22:53:41Z). The RESULT was sent outside the sandbox from the start.
- **Safety check:** a validation wrapper of the form `bash -c "<cmd>"` was refused by the built-in removal safety check before running anything. Each validation command was then run directly.
- **Not done:** no `make update`/`make upgrade`, no edit under `~/.claude/**`, no thread resolution, no new model profile or manifest key, no hand edit of a generated file.
- **Worker review:** one read-only general-purpose subagent reviewed the diff (it read files and ran read-only git only, and it ran no tests). Read-only on the host: `ls`/`cat` of `~/.claude/agents/project-map.md` and `~/.claude/agent-memory/project-map/` to verify its P3. Nothing was written there.

## Revise round 1

- Same isolation as round 0. Ran sandboxed: the SKILL.md edits, the generator, render-check, the validator, the unit modules, `make unit-test`, ruff, prettier and the commit. Ran outside the sandbox through the permission gate: `git push`, `gh pr checks`, the check-runs `gh api` read, the Bot-wait loop, the read-only host probes of item 4 (`stat`, `sed -n`, `cat`, `grep`, `ls` under `~/.claude/`, nothing written), the artifact appends and masking, and `agmsg-dispatch`.

## Revise round 2

- Same isolation as round 1. Ran sandboxed: the generator edit and run, render-check, the validator, the unit modules, `make unit-test`, ruff, prettier and the commit. Ran outside the sandbox through the permission gate: `git push`, the check-runs `gh api` wait and read, `gh pr checks`, the Bot-wait loop, the PR feedback reads, the artifact appends and masking, and `agmsg-dispatch`.
