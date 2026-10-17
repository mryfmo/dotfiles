[P2] high implementation scripts/orchestrator/local-advisory.sh:62 The guard checks text after the **last** `-local-review-`, so `t-a01-local-review-notes-local-review-aaaaaa1.md` passes as `aaaaaa1`. A matching finding then inherits an unrelated `local:aaaaaa1:1` row’s class and provenance. A read-only probe reproduced this. Strip the exact task prefix before validating the entire suffix, and test this filename.

INV-2: holds .orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a04.md:324 — 10 changed implementation lines and 20 added test lines satisfy the caps.
INV-6: holds .orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a04.md:19 — supplied records show one implementation round and no reset threshold reached.

Orchestration findings: 0

Both premises hold at the dispatch base. Task/evidence copies match; [PR #386](https://github.com/mryfmo/dotfiles/pull/386) and GitHub CI confirm the specified head and passing tests.

Local tests were not rerun; CI logs were checked. Incorrect review attribution remains possible as described above.
Verdict: incorrect