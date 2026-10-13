[P1] High — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:20`: The task re-specifies `scripts/regime-counters.sh` and its test, directly violating stop condition 3, which forbids re-specifying a01’s counters.

[P1] High — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:106`: `acceptance-front-matter.py` has no defined source or preservation rule for `searches`, nor a way to supply the required `{n, reason, evidence}` audit dispositions; an S6-triggering ledger or incorrect audit can therefore produce a record rejected by amendment 1’s gate contract, and line 110 tests only the identity triple.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise