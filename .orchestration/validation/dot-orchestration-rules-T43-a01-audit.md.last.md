- [P2] high confidence `scripts/ua-symbol-coverage.py:65` Any failed `git show` is treated as a deleted file; an invalid or unavailable `--repo-ref` therefore marks all symbol losses “explained” and exits 0. Reproduced with an invalid ref and a 19→0 symbol loss; validate the ref and distinguish lookup errors from confirmed deletions.
- [P2] high confidence `scripts/ua-symbol-coverage.py:90` `defs < before` excuses the entire graph decrease, including missing definitions that remain: old=2, source=1, new=0 returns “explained” and exits 0. A partial source deletion must not exempt additional extraction loss.

Read-only checks reproduced both failures and confirmed the claimed eight-file historical regression detection. The added test misses both exemption cases. No additional security or rule-compliance findings identified. CI could not be independently verified because `gh` could not reach GitHub; the filesystem-writing unit test was not run.

📝 まとめ: `557502b` の監査を完了。coverage gate が欠落を見逃す2件の修正が必要です。

Verdict: incorrect