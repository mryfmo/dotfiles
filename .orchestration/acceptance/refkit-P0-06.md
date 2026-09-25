# refkit-P0-06 acceptance record

status: accepted (2026-09-23T11:4xZ)
reviewer: claude-remediation-dot

## Verified independently (dc8063c in dotfiles-w1)
- Hook groups files by `git rev-parse --show-toplevel`, runs with `cwd=root`, relative paths, prettier `--ignore-path <root>/.prettierignore`, ruff `--force-exclude`. Orchestrator ran the hook from `/tmp` against scratch copies of a kit `.md` and a kit `.py` inside the worktree: both SHA-256 unchanged. Unit test `tests/unit/test_format_edited_files.py` passes (1 test, real git in a temp repo, formatters faked).
- `make validate-agent-assets` failure is pre-existing and unrelated: `validate_no_obvious_secrets()` walks `ROOT.rglob("*")` and does not honour `.gitignore`, so the gitignored example venv trips the scanner → refkit-P0-07.
- Note: for an excluded `.py` the hook now exits 1 (a formatter reports "no files"/`ty` error) although nothing is changed; cosmetic, tracked in P0-07 as optional.
- Untracked `.orchestration/**/refkit-{P0-01,P1,P2-A,P2-B}.md` in w1 will be committed by the worker as a chore in P0-07 (bookkeeping).
- The worker cherry-picked P0-05 (`b6acdfc`) onto feat/references-kit-v4 as allowed; merge with the -p3 branch will de-duplicate.
- Deployment to `$HOME` requires `chezmoi apply` by the user (recorded for the final report).

cost: n/a
