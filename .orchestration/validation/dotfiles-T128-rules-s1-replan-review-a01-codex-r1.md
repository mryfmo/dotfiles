[P1] high .orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md:11 `tests/fixtures/regime/invariants.md` is missing from allowed_files and the threat table, so changing the counters bullet necessarily breaks the existing whole-section pin unless that fixture also changes.

[P2] high .orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md:66 The re-plan requirement must distinguish S1’s non-advisory count from S6’s all-ledger search threshold, otherwise advisory findings excluded from S1 also trigger the stop.

[P2] high .orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md:67 Items 2–3 assert dispatcher and Stop-gate enforcement without landing clauses or covering dependencies, and the Stop-gate task itself depends on this rules task.

[P2] high .orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md:69 The three proposed tests lack individual names, branch-specific cases and required assertions, leaving stop condition 2’s test requirements unspecified.

[P2] high .orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md:73 The file contains neither the pasted checker `OK` nor `masked 0 match(es)` evidence required by stop condition 4.

📝 まとめ: Hash matched; premises replayed as `0 / 1 / 0`, checker passed, and read-only masking found zero matches; revision is required. Live PR #323 verification and implementation tests were not performed.
Task-file verdict: dotfiles-T128-rules-s1-replan-a01: revise