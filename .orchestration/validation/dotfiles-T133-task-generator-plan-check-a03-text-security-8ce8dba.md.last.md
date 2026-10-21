- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:133 — The filter preflight checks only the parent repository: status can spawn another status inside a selected submodule, whose own configuration can activate `filter.*` commands without that preflight; prohibit submodule traversal or validate each consumed repository, with a nested-filter marker regression. [Git implementation](https://raw.githubusercontent.com/git/git/master/submodule.c)

- [P1] high .orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md:131 — The prescribed flags leave lazy fetching enabled: reading a missing object can trigger an HTTPS fetch using checkout-configured `credential.helper` shell commands, bypassing the filter check and trusted executable selection; disable lazy fetching for inspection reads and add a regression. [Lazy fetching](https://git-scm.com/docs/partial-clone#_handling_missing_objects), [credential helpers](https://git-scm.com/docs/git-config#Documentation/git-config.txt-credentialhelper)

📝 まとめ: Reviewed every threat row and cited acceptance/review context; found two remaining execution-binding gaps for orchestrator disposition.

Not checked: future implementation tests or live deployment; no files changed. Checkout-configured execution remains possible through these paths.
Verdict: incorrect