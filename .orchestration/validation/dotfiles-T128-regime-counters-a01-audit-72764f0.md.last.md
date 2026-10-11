[P1] high implementation `scripts/regime-counters.sh:112` — `has()` accepts matching tokens anywhere in the message. Two `PONG status=blocked` messages mentioning a previous `status=question` produce `questions=2`; likewise, `RESULT verdict=revise` mentioning `verdict=accept` passes the reset check at line 117. Both cases reproduced using the head’s extracted jq expressions. The tests omit conflicting fields in explanatory text.

[P1] high implementation `scripts/check-regime-boundary.sh:226` — A reset record can name an unrelated, already approved design and its genuine hash. Nothing binds that approved design to the task being reset; the foreign RESULT then sets `reset_anchored=true`, suppressing threshold and closed-unmerged warnings. The existing negative tests cover mismatched hashes, not replay of an unrelated valid approval. This gaming path is missing from the threat table.

[P2] high orchestration `.orchestration/acceptance/dotfiles-T128-regime-counters-a01.md:6` — The claim that tests remain below INV-2’s 1,000-line cap is false: the diff adds 697 unit-test lines plus 1,038 fixture lines, totaling **1,735 lines under `tests/`**. The design provides no fixture exemption.

The other closed threat rows have supporting coverage: `.orchestration` count isolation, complete history reads, Bot identity and unknown handling, merged-PR anchoring, Amendment 1’s PR-less condition, waiver visibility, and fixture-seam isolation. The status and reset rows remain open for the cases above.

All four recorded fixture counts reproduced, including T119’s **9 amendments** and V0’s **adcf783b first head / 6 subsequent heads**. ShellCheck and Bash syntax checks passed. GitHub independently reports successful final-head workflows for [PR #319](https://github.com/mryfmo/dotfiles/pull/319).

INV-6: violated scripts/regime-counters.sh:112; scripts/check-regime-boundary.sh:248

Orchestration findings: 1

📝 まとめ: Read-only audit completed with three findings; nothing modified. The full local suite was not rerun; false threshold signals and reset bypasses remain.
Verdict: incorrect