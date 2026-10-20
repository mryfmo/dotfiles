[P2] high orchestration .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md:45 Item 1 requires a red-then-green test for every owned row, but the dispatch note limits this to rows naming a test, and report.md:36 relies on that exception. Reconcile the hashed task with the intended records-only scope; its completion criteria currently contradict the dispatch.

[P3] high evidence .orchestration/dotfiles-T128-chain-review-scripts-followup-a06/a05-gh-calls.md:4 The supersession names a05 sandbox.md lines 12–18, but the planned gh commands actually occupy lines 19–21. The declared replacement excludes the entries it corrects; report.md:34 repeats the incorrect range.

Task invariants: no `INV-n` declarations exist. Inherited caps hold: zero code changes and zero test additions. The task-copy SHA-256 matches dispatch.

Orchestration findings: 1

Verified: [PR #402’s](https://github.com/mryfmo/dotfiles/pull/402) timeline supports the recorded actions; [PR #434](https://github.com/mryfmo/dotfiles/pull/434) matches the requested head and has ten successful checks. No executable changes or exposed secrets were found.

📝 まとめ: Read-only audit completed; two record inconsistencies remain.
Not rerun: local tests or whole-bus history. CI skipped test execution for this records-only diff.
Verdict: incorrect