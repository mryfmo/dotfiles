# refkit-P0-07 acceptance record

status: accepted (2026-09-23T11:5xZ)
reviewer: claude-remediation-dot

## Verified independently (4fb3c67 in dotfiles-w1)
- `validate_no_obvious_secrets()` now iterates `git ls-files -z --cached --others --exclude-standard` with an explicit rglob fallback (stderr notice) when git is unavailable. Orchestrator run: `make validate-agent-assets` → ok with the gitignored example venv present; `tests.unit.test_validate_agent_assets` 39 tests OK (two new cases).
- Bookkeeping commit f560b48 records the previously untracked P0-01/P1/P2-A/P2-B artifacts.
- Optional hook item skipped with a reason (already true after P0-06).

cost: n/a
