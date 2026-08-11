# T41 Cognee removal

Committed the complete scoped removal in the isolated worktree:

`10d8fc4 chore(agents): remove the Cognee memory stack`

The expanded edit scope resolved the two previously out-of-scope references. Generator, validator, Python compile, shell syntax, generator idempotency, and `tests/unit/test_require_crit_review.py` (25 passed) all succeed.

- `home/.chezmoiremove: .local/bin/common/start-cognee-mcp`

The updated task exempts `.chezmoiremove`; no other Cognee reference remains.
