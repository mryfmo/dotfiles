# AGMSG-TASK dot-validator-worktrees-T7-a01 — validate-agent-assets.py must not scan nested git worktrees

## Defect (reproduced by the orchestrator on main today)

```
$ uv run --with pyyaml python scripts/validate-agent-assets.py
ERROR: possible committed secret in .claude/worktrees/adh-baseline/vendor/compactiondb/validate.py
```

`validate_no_removed_claude_skill()` (~line 1039) and the obvious-secret scan (~line 1080) walk `ROOT.rglob("*")` and skip only `.git`, `site`, `__pycache__` path parts. Worker worktrees live under `.claude/worktrees/<name>/` inside ROOT, so every file of every checked-out worktree is scanned again; the dummy-secret fixture allowlist compares exact ROOT-relative paths, so the nested copies are false positives. The validator therefore fails on any developer machine with an active worktree, while CI (no worktrees) passes.

## Fix (Ponytail: smallest correct diff)

- In both scans, skip any path that is inside a nested git worktree or repository: a directory containing a `.git` file or directory other than ROOT itself. Simplest: add `".claude/worktrees"`-relative prefix skip is NOT enough (worktrees can be anywhere); implement one helper `is_nested_git_tree(path)` that checks each ancestor between ROOT and the file for a `.git` entry, cached per directory, and use it in both loops. Keep the existing part-name skips.
- Unit test in `tests/unit/test_validate_agent_assets.py`: create a temp ROOT with a nested `sub/.git` file and a file inside containing the removed-skill token / a fake secret; assert neither scan reports it; assert a top-level file still is reported. Red-first.

## allowed_files

`scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-validator-worktrees-T7-a01.md`.

## forbidden_actions

no git commit; no push; no PR; no local bats; no other files.

## Validation (verbatim)

`make unit-test`; `uv run --with pyyaml python scripts/validate-agent-assets.py` run from the MAIN worktree `/Users/mryfmo/Workspace/dotfiles` with the patched script copied there? NO — do not touch main; instead reproduce with a temp nested `.git` inside your worktree during the test only. `git diff --check`.

Worktree: `.claude/worktrees/validator-worktrees` (branch `fix/validator-skip-nested-worktrees`) from `origin/main`. max_turns=20. Reply with `AGMSG-RESULT v1`.
