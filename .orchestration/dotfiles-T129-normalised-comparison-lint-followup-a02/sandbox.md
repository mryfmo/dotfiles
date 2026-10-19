---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a02
seat: claude-standard-dot-a008
permission_gated_commands: none (agmsg-dispatch only, through excludedCommands)
---

# Sandbox record: dotfiles-T129-normalised-comparison-lint-followup-a02

- **Seat and arrival:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The AGMSG-TASK arrived at 2026-10-19T11:36:30Z, and amendment 1 at 11:39:57Z.
- **Branch:** `tools/lint-comparisons-followup-a02` was cut fresh from `origin/main` `51ba5801` with `git switch --no-track -c`, so no upstream config was written. PR #410's branch, where worker-f stood, was left as it was.
- **Inside the sandbox ran:** every command, under plan 024 §5.14 item 10:
  - edits and commits (`git -c commit.gpgsign=false`);
  - `git fetch` and `git push`, each one command;
  - the `gh` reads of checks and reviews;
  - the unit tests, the lint, ruff, prettier, shfmt and `make format`;
  - scratch worktrees under `$TMPDIR`, each removed with `git worktree remove --force`. `git worktree prune` never ran.
- **Outside the sandbox:** only `agmsg-dispatch`, through `excludedCommands`. No command was refused.

## Which Python runs used `-I` (process row audit:4f5be51:14)

- **With `-I`:**
  - every run of the lint itself: `uv run --no-project python -I scripts/lint-comparisons.py …`, and the test module's own subprocess calls, which start it as `sys.executable -I`;
  - the mutant and fixture probe scripts (`uv run --no-project python -I $TMPDIR/…`);
  - the task-consistency check (`uv run --offline --no-project --with pyyaml python -I …`);
  - the masker (`scripts/validate-agent-assets.py --mask-secrets`, through `python -I`).
- **Without `-I`:** the unittest runner, `uv run python -m unittest tests/unit/test_lint_comparisons.py -v`, which is the Check's own command, and the mutant script's inner unittest calls. `-m unittest` has to import the `tests` package from the checkout, which `-I`'s isolation of `sys.path` would refuse. The lint it exercises runs isolated.
