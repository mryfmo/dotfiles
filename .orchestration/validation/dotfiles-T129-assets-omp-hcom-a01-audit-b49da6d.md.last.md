[P2] high implementation scripts/update-agent-assets.sh:989 Installing hcom from a temporary wheel leaves uv’s receipt referencing a file deleted by the EXIT trap. Later `make update` invokes `uv tool upgrade --all`; re-resolution after cache eviction cannot recover that source. Retain the verified wheel at a stable path and test the subsequent upgrade. This conclusion follows from [uv’s receipt-based upgrade implementation](https://raw.githubusercontent.com/astral-sh/uv/main/crates/uv-tool-commands/src/upgrade.rs); the existing advisory owner does not fix the audited head.

[P2] high orchestration .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-a01.md:43 The record acknowledges five amendments and five questions, then accepts the task without identifying an INV-6 reset or qualifying waiver. Calling these scoping gaps does not exempt them from the invariant’s counts. D-388-round3 authorizes one additional fix, but does not document release of the amendment/question thresholds. Supply that authorization or reset before integration.

The task has no front-matter invariant map; its prose names these invariants:

INV-2: holds .orchestration/tasks/dotfiles-T129-assets-omp-hcom-a01.md:118 — eight code/test files, 165 production changed lines and 261 test additions satisfy the caps.
INV-6: violated .orchestration/acceptance/dotfiles-T129-assets-omp-hcom-a01.md:43 — threshold-release evidence is missing.

Orchestration findings: 1

All six premises hold against the merge base. Worker records and eight reviewed source hashes match the audited head; shell syntax and in-memory Python compilation pass.

📝 まとめ: Audited [PR #388](https://github.com/mryfmo/dotfiles/pull/388) at `b49da6dd`; recorded two findings and modified nothing.

Not rerun: tests or live installs; live GitHub verification failed, so CI conclusions rely on the supplied final-head snapshot.
Verdict: incorrect