[P2] high implementation home/dot_local/bin/common/executable_herdr-agents:1949 A dangling `run/stale` symlink makes `-e` false, bypassing the archive check. Delivery is disabled and the identity removed before `mkdir -p` fails at line 1980, leaving the placement record undiscoverable through identities. Include `-L` in the existence check and add a regression case.

The task declares no invariant mapping; its named clauses assess as follows:

INV-2: holds .orchestration/validation/dotfiles-T128-seat-liveness-followup-a01.md:794 — two code/test files, 17 production lines changed and 48 test lines added satisfy the caps.
INV-6: holds .orchestration/acceptance/dotfiles-T128-seat-liveness-followup-a01.md:36 — supplied records show one revise, below the reset threshold.

Both task premises hold against the supplied merge base: counts 6 and 7. Worker artifacts match the committed copies.

Orchestration findings: 0

📝 まとめ: Completed the read-only audit of [PR 377](https://github.com/mryfmo/dotfiles/pull/377) at `bf650af1`; found one remaining archive failure. Modified nothing.
Not rerun: filesystem-mutating tests; live CI was inaccessible through gh and web. Syntax checks passed; saved CI reports 12 successful checks.
Verdict: incorrect