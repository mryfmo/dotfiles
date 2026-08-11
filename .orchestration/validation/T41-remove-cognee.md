# T41 validation evidence

Completed checks:

```text
agent asset validation ok
tests/unit/test_require_crit_review.py: 25 passed
generator idempotency passed
Python compile and edited shell syntax passed
```

The final requested sweep has exactly one intentional result:

```text
home/.chezmoiremove: .local/bin/common/start-cognee-mcp
```

The updated task explicitly exempts that retirement entry. Commit: `10d8fc4 chore(agents): remove the Cognee memory stack` (14 files, 2 insertions, 299 deletions).
