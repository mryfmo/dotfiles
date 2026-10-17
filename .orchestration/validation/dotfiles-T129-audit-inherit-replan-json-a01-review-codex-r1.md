[P2] high .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md:87 Copying an audit containing findings to the new head leaves parent-qualified ledger IDs unchanged, so the existing gate rejects it with `S6: ledger lacks audit:<new sha7>:1`; inheritance needs an explicit finding-ID policy.

[P2] high .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md:89 Removing the patch-id comparison cannot fail the positive case, while adding a normal PR commit changes the first parent, so the negative test must preserve an eligible receipt-bearing parent and change the merge result’s patch-id.

[P2] high .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-a01.md:32 The permitted migrations omit existing gate tests that remove or replace body lines and the counters’ ASCII-token test, leaving assertions that fail after moving re-plans into JSON.

📝 まとめ: Hash, premises, checker, mask and Completion checks passed against local origin/main. No files changed or implementation tests run; remote freshness verification failed because GitHub DNS resolution failed.
Task-file verdict: dotfiles-T129-audit-inherit-replan-json-a01: revise.