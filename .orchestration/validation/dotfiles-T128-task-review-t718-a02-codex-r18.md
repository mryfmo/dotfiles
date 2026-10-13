P2 — High confidence — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:47`: The `dispatch.sh` threat row remains limited to item 4, although item 6 now authorizes ledger-owned changes to this script; such changes would contradict the row instead of being constrained by the new “exactly the owned rows” control.

P2 — High confidence — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:53`: The `regime-counters.sh` threat row similarly covers only item 3, leaving possible item-6 edits without the ledger-bounded residual control applied to `bus-read.sh` and `three-repeat.sh`.

P3 — High confidence — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:107`: The narrative still says the task runs after `dotfiles-T128-orchestrator-tools-a03`, contradicting the amended `after: [dotfiles-T128-orchestrator-tools-a04]` and the 07:22Z change note.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise