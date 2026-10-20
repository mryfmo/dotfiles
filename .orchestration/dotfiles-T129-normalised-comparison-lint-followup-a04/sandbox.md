---
task_id: dotfiles-T129-normalised-comparison-lint-followup-a04
seat: claude-standard-dot-a008
permission_gated_commands: none (agmsg-dispatch only, through excludedCommands)
---

# Sandbox record: dotfiles-T129-normalised-comparison-lint-followup-a04

- **Seat and arrival:** `claude-standard-dot-a008` in `.claude/worktrees/worker-f`. The TASK (`e58d51b1…`) arrived at 2026-10-20T00:04:25Z. Amendment 1 (`e7019c3c…`) arrived at 00:21:47Z, answering this seat's question PONG of 00:19Z.
- **Branch:** PR #432's `tools/lint-comparisons-followup-a02` continued from its head `b24d3136`, which is the anchor `e520a7fe` plus the chain's main merge. No rewind was made and no second branch or PR was opened.
- **Inside the sandbox ran:** every command, under plan 024 §5.14 item 10:
  - edits and commits (`git -c commit.gpgsign=false`);
  - `git fetch` and `git push`, each one command (HTTPS, `credential.helper=!gh auth git-credential`, `GIT_CONFIG_GLOBAL=/dev/null`);
  - the `gh` reads of the PR, checks and runs;
  - shfmt 3.14.1 (PATH's `…/mise/installs/shfmt/latest/shfmt`) as a subprocess of the lint;
  - the unit tests, the lint, ruff and `make format`.
  - The red proof swapped the anchor's `scripts/lint-comparisons.py` into the worktree and restored it with `git checkout --`. The mutation harness rewrote the same file in memory and restored the original bytes; `git diff --quiet` confirmed both restorations (validation §4, §5). No scratch worktree was made, and `git worktree prune` never ran.
- **Outside the sandbox:** only `agmsg-dispatch`, through `excludedCommands`. No command was refused.

## Which Python runs used `-I`

- Every Python run used the trusted interpreter by its absolute path (`…/mise/installs/python/3.15.0/bin/python3.15`; `uv run python` resolves to 3.10 here, which cannot compile the lint's possessive quantifier) with `-I`:
  - the five Check commands (validation §6 to §10);
  - the lint itself, including the test module's subprocess calls (`sys.executable -I`);
  - the red-proof run, the mutation harness and its inner unittest runs, the tree comparison and the template probe.
- `python -I -m unittest discover -s tests/unit` runs the lint module: `discover -s` puts `tests/unit` on `sys.path` itself.
  - In the full suite, `-I` keeps the checkout root off `sys.path`, so `test_validate_agent_assets`, which imports the `tests` package, fails to load (`ModuleNotFoundError: No module named 'tests'`, validation §7).
  - The sandbox also caused failures in other modules: temporary-repo `git commit` exits 128, `out of pty devices`, `mktemp` is denied under `/var/folders`, and `--base 'main'` does not resolve in a worktree.
  - No failing module runs the lint. CI's `make unit-test` (`uv run python -m unittest discover -s tests/unit -v`) is the suite's authority.
