[P2] high orchestration .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a06.md:45 Item 1 still requires a red-then-green test for every owned row. Report.md:40 and revise.yaml:8 reinterpret this as applying only to rows naming a test, but the dispatched hash remains unchanged and no test was added. The previous finding remains unresolved; reconcile the requirement through a hashed task amendment.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a06.md:150 The orchestrator sent a revise without recording the required fresh `regime-counters.sh` output or resolving unknown counts. The dispatch-time zero counts cannot establish eligibility for that later round.

Task invariants: no `INV-n` declarations or design mapping exist in this task. The inherited change caps hold, and the task-copy SHA-256 matches dispatch.

Orchestration findings: 2

Verified: the corrected supersession range is accurate; [PR #402](https://github.com/mryfmo/dotfiles/pull/402) supports the recorded creation and merge details. [PR #434](https://github.com/mryfmo/dotfiles/pull/434) matches the pinned head and has successful Actions runs. No executable changes or exposed secrets were found.

📝 まとめ: Read-only audit completed; two orchestration findings remain. Nothing was modified.

Not rerun: local tests or whole-bus history; CI skipped unit-test execution. The checkout was dirty, so committed files were inspected through pinned Git objects; the clean-tree audit prerequisite remains unmet.
Verdict: incorrect