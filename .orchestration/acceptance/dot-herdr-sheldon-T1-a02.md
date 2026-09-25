# Acceptance: dot-herdr-sheldon-T1-a02 (closes dot-herdr-sheldon-T1-a01 and dot-docs-align-T1-a01)

status: accepted
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Independent re-derivation

- Worktree reset to d377ad0 (main); re-applied diff limited to the six kept files; ubuntu.toml/setup.bats change dropped as superseded (82d4961).
- README herdr-agents section keeps the worker_kind wording from d004ddb/4d4767b; Makefile keeps the #170 unmerged-index guard.
- Orchestrator reran `make unit-test` OK, asset validator OK, shellcheck OK, `git diff --check` OK; no stale `--split right` / `22.04` / numbering text remains.

## Integration

Committed on `fix/herdr-reload-and-sheldon-client`, PR opened; bats verdict from CI.
