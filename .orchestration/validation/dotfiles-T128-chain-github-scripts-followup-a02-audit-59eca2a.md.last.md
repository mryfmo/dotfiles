Audited [PR #375](https://github.com/mryfmo/dotfiles/pull/375) at `59eca2a`. Final-head CI passed all seven module tests.

- [P2] 0.99 implementation `scripts/orchestrator/resolve-threads.sh:33` An empty-ID TSV row containing a backtick stops AWK but leaves `bad` empty, bypassing rejection and skipping later unsafe rows; a read-only reproduction reached stub `gh` instead of exiting 2. Reject malformed IDs or track detection separately from the ID.
- [P2] 1.00 conformance `.orchestration/dotfiles-T128-chain-github-scripts-followup-a02/report.md:16` The audited tree omits required `revise.yaml`, so the C-50 revision’s `previous_head` and test selector are not committed together as the orchestration skill requires.
- [P2] 1.00 orchestration `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-followup-a02.md:34` The reset decision incorrectly counts two ACCEPTANCE messages as revises; INV-6 counts RESULTs minus one. History shows two RESULTs at that decision (`revises=1`) and three after the final RESULT (`revises=2`); the record also omits required counter output.

All three task premises hold: reproduced counts were `1`, `5`, and `0`. The task declares no front-matter invariants; its named design invariants assess as follows:

INV-2: holds `.orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a02.md:69` — two code/test files, 14 changed production lines, 36 added test lines.
INV-6: violated `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-followup-a02.md:34` — reset accounting uses the wrong message population.

Orchestration findings: 1

📝 まとめ: Read-only audit completed; three findings remain. No files changed.

Not checked: a local full-suite rerun or live annotation bodies; the preflight bypass remains.
Verdict: incorrect