[P2] high implementation scripts/orchestrator/local-advisory.sh:81 Historical filename suffixes enter `grep -E` without validation or escaping. A matching-token file named `t-a01-local-review-.*.md` inherits the last unrelated `local:*:1` row’s class and provenance. The read-only reproduction returned `unrelated-class`; require a seven-hex suffix and literal ID matching.

[P2] high orchestration .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md:85 The task excludes consumers needed for its stated three-row enforcement goal: `chain-integrate.sh:173` drops every `local:` row, and `require-crit-review.py:36` rejects those ledger IDs. Three repeated `quoting` rows therefore produce an empty ledger and never trigger S6. Class propagation alone leaves the claimed correction incomplete.

The task declares no front-matter invariants; its referenced design checks are:

INV-2: holds .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a03.md:225 — 43 production lines changed and 60 test lines added, within caps.
INV-6: violated scripts/orchestrator/chain-integrate.sh:173 — repeated local classes remain excluded from the mandatory three-row search check.

All four premises reproduce, and task/report/validation/sandbox copies match the audited head. Bash syntax, ShellCheck, and Python parsing passed. Saved feedback records 12 successful checks for `d3e8acf`.

Orchestration findings: 1

📝 まとめ: Audited [PR 381](https://github.com/mryfmo/dotfiles/pull/381); found two P2 issues and modified nothing. Unit/Bats tests were not rerun; GitHub live verification was unavailable, so CI assessment relies on supplied evidence.
Verdict: incorrect