[P2] high — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:20` — `scripts/regime-counters.sh` and its test overlap a01’s counter scope, directly violating stop-condition item 3’s requirement that the counters not be re-specified.

[P2] high — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:111` — The closed ledger-shape control requires every row’s `id` to be a string, but the specified regression test covers only a bare-string row and a non-slug `class`, so an implementation accepting non-string or missing `id` can pass.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise