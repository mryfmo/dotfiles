# Acceptance: dot-ua-full-T9-a01

## Scope confirmation (Phase 0.5)

Existing `.ua/.understandignore` patterns approved unchanged, English output, full repository scope EXCEPT two additions: `.orchestration/` (process records; 336 of the current graph's nodes are these and they are not codebase architecture) and `reviews/` (external read-only ADH input baseline). Worker may append those two patterns to `.ua/.understandignore` (allowed under `.ua/**`). Resume with `UNDERSTAND_NO_WORKTREE_REDIRECT=1`.

## Result

status: accepted — orchestrator verified: graph/fingerprints/meta hashes all equal worktree HEAD d906b00; 1,399 nodes / 2,398 edges; zero nodes under `.orchestration/` or `reviews/`; only the four intended files staged; `.ua/intermediate/` remains ignored. Committed as chore(ua) and opened as a PR.
