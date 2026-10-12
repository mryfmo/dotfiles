[P2] confidence=0.99 implementation `.github/workflows/remote.yaml:66` — Git still quotes filenames containing quotes, backslashes, or control characters despite `core.quotePath=false`. For `.orchestration/quote"file.md`, the emitted leading quote makes the prefix check return `should_run=true`, unnecessarily running bootstrap on an orchestration-only PR. Reproduced the classification with Git-rendered paths; both bootstrap decisions share this defect. Use NUL-delimited paths and add regression coverage. [Git documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corequotePath)

[P3] confidence=1.00 orchestration `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a02.md:8` — The pre-audit record still describes redispatch prospectively with superseded hash `6457b81f…`, omitting the two TASK IDs and main-design digest explicitly required by the task’s evidence row. The submitted amendment instead carries `4de54fde…`; update this record to reflect the actual dispatch.

Verification: 16 structural/security tests passed in memory. [PR #320](https://github.com/mryfmo/dotfiles/pull/320)’s seven required contexts passed at the pinned head, and its feedback sweep follows completed CI. The invariant sentence and implementing-task entry match main’s design, landed through [PR #321](https://github.com/mryfmo/dotfiles/pull/321). Both task premises check out.

INV-2: violated `.github/workflows/remote.yaml:66` — quoted orchestration filenames defeat the bootstrap skip; the design-on-main requirement otherwise holds.

Orchestration findings: 1

📝 まとめ: Read-only audit completed; one classification defect and one orchestration-record omission remain.

Not rerun: filesystem-writing tests, Bats, post-merge timing, or live dispatch history. Files unchanged.
Verdict: incorrect