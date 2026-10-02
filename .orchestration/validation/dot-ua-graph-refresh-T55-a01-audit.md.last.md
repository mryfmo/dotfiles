- [P2] High confidence `.ua/knowledge-graph.json:8938` — `lineRange` contains prose here and at line 9146. Understand-Anything 2.9.7 rejects these fields and drops two nodes plus 20 edges during loading, contradicting the reported zero validation issues; move the prose to `languageNotes`.
- [P2] High confidence `.ua/knowledge-graph.json:18728` — The rebuild loses all 17 outgoing call edges from `util.py` and all 28 from `attach_comment_files.py`. All 45 calls remain in unchanged source, so graph traversal now omits real dependencies; symbol-count validation misses this regression.

Counts, freshness metadata, and zero symbol-count regressions were reproduced. No additional security or rule-compliance findings. Saved [PR #226](https://github.com/mryfmo/dotfiles/pull/226) CI evidence reports green checks; network failures prevented independent verification.

📝 まとめ: Audited only `98bdf43`; two graph defects require correction.

Verdict: incorrect