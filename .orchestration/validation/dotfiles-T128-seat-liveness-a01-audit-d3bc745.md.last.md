[P2] high implementation home/dot_local/bin/common/executable_herdr-agents:1920 Failed identity enumeration leaves `seat_rows` empty, bypassing both the leader check and every pane-state check; `--stale` then closes the matching standalone worker workspace at line 1975. A memory-only probe confirmed exit 0 and workspace closure without establishing `gone`.

[P2] high implementation home/dot_local/bin/common/executable_herdr-agents:1965 Archive preparation happens after `leave.sh` removes the identity. If `run/stale` is a regular file or cannot be created, retirement exits with the identity already removed and the placement record still in `spawn.*`; subsequent retries cannot discover it through identities. A memory-only failure probe confirmed this ordering.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-seat-liveness-a01.md:57 The archive defect is dispositioned solely by deferring it to a follow-up task, contrary to the integration rule prohibiting deferral as a disposition. Its evidence command also fails: the named owner task is absent from `origin/main` at the audited base, and no local owner hash or supporting output is recorded.

[P3] high orchestration .orchestration/validation/dotfiles-T128-seat-liveness-a01-pr-feedback.json:139 The evidence selector compares `.url` with the string `"None"`, but this status has JSON `null`; replay produces no output, so the recorded command does not substantiate the disposition.

INV-2: holds .orchestration/tasks/dotfiles-T128-seat-liveness-a01.md:87 — Applicable caps pass: four non-record files, 167 production lines changed, 169 test lines added. No front-matter invariant map is declared.

Orchestration findings: 2

For [PR #367](https://github.com/mryfmo/dotfiles/pull/367), the final head’s 12 check runs and commit status pass. [Ubuntu CI logs](https://github.com/mryfmo/dotfiles/actions/runs/38702954580/job/116315317693) confirm all 202 tests in the two affected modules passed. All four premises replay correctly, and the task-copy hash matches.

📝 まとめ: Read-only audit completed; two implementation findings and two orchestration findings remain. Nothing was modified.

Not checked: local unit/bats suites or live seat teardown; failure probes used memory-only stubs.
Verdict: incorrect