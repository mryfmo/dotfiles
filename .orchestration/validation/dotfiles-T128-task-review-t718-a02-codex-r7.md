P2 high `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:111` Item 3 re-specifies the counters and their test, directly violating stop condition 3, which says nothing from a01’s counters may be re-specified.

P2 high `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:111` The prescribed PR #336 disposition lacks the mandatory `; evidence=<command>` clause, so the integration gate will reject it.

P2 high `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:60` The environment-input row omits `jq`, although the newly re-scoped `regime-counters.sh` ledger parsing depends on that host binary.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise