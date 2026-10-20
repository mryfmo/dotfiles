Reviewed [PR #440](https://github.com/mryfmo/dotfiles/pull/440), exact range `60a6fb2…cedc7f5`. Found three P2 issues:

1. **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:420`** — NFC normalization changes the filename before confinement checking: on Linux, an escaping `tests/fixtures/cafe\u0301.py` symlink is checked as the distinct `café.py` path and can receive the fixture exemption. Resolve the original enumerated path; normalize only comparison values.

2. **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:440`** — An internal directory symlink such as `tests/fixtures/alias → scripts/` passes confinement but escapes coverage because traversal skips directory links and this condition checks only files. Reject such aliases or explicitly validate their coverage without silently skipping them.

3. **P2 · High confidence · `scripts/orchestrator/task-consistency-check.py:469`** — Eleven valid item rows plus another row naming both `5.14 item 0` and `5.14 item 1` pass C16: the combined row contributes nothing to either count. Reject multi-item rows and count every occurrence when detecting duplicates.

The first two undermine the threat table’s fixture/evidence symlink control and path-normalization assurances; the third leaves the C16 control incomplete. The other closed controls—interpreter-selection order, token forwarding, canonical-main reads, and canonical receipt/hash binding—match the inspected implementation. Shell-free probes, safe YAML loading, and fixed repository/host arguments showed no additional injection or deserialization defect. Declared parent-startup, shared-cache, same-UID, and shared-credential risks remain residuals.

Focused, read-only checks of AST-extracted functions reproduced all three gaps; filesystem conditions were modeled. Source/test hashes matched the latest evidence, and the recorded scanner alert matched a synthetic-token digest.

📝 まとめ: 指定差分と threat_table のセキュリティレビューを完了し、P2 を3件報告しました。修正と受け入れ判断は orchestrator に委ねます。

Not checked: full test execution or live CI (`gh` could not connect); no files changed. Declared execution/cache/credential risks remain.
Verdict: incorrect