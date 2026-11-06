# Needs validation: dotfiles at 179de4dbf984617d48e823ca2123de59dea6d9d3

No unresolved record exists in this run, and the carried run-4 holds none.

The change is test-only, and the source settles each question: whether the new judged ratio still fails a quadratic regression of the secret scan, whether the hang cap and correctness assertions remain, and whether the fixtures hold a real credential or write outside a scratch root.

The one sensitivity note (the report test now times its fixture write, `tests/unit/test_validate_agent_assets.py:3029-3035`) is hardening in `REPORT.md` section 6, not a lead. A bounded local check would settle how much the write dilutes the judged ratio. It was not run, by task rule. In the required sandbox it would be: time the write and `validate_no_obvious_secrets` separately at 8,000 and 64,000 findings in a scratch root.

The records-sync candidate of run-2 to run-4 (`records-sync/redaction/account-identity-residue-in-published-row`) is not on this branch. It stays open on the `records/sync-*` branches.
