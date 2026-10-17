[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a02.md:72 The Goal names “lints of a03” as enforcement, but the two-task lineage contains no a03 or prerequisite landing those lints, violating stop condition 3.

[P2] high .orchestration/tasks/dotfiles-T128-process-hardening-a02.md:81 Item 6 excludes step 10 and both rules files from fixture assertions and makes Worker fixture coverage conditional, leaving stop condition 2’s five-group fixture requirement unmet.

📝 まとめ: Hash matched; checker OK; mask 0; premises replayed `1/0/0`; 53 existing tests passed. Fetch and live [PR #378](https://github.com/mryfmo/dotfiles/pull/378) verification failed, so cached refs may be stale.
Task-file verdict: dotfiles-T128-process-hardening-a02: revise