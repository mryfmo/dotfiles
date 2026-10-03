- [P2] high confidence `plans/004-harden-and-lock-the-supply-chain.md:91` — Formatting replaces installer globs with underscore-containing patterns, excluding all 29 installer scripts from documented ShellCheck validation; repeated in `plans/005-make-runtime-health-and-verification-truthful.md:92`.
- [P2] high confidence `plans/001-contain-starship-cleanup.md:57` — Padding inserted inside the regex makes the removal scan miss dangerous deletions; equivalent corruption breaks supply-chain scans in `plans/004-harden-and-lock-the-supply-chain.md:87` and `:88`.

All 35 changed Python files retain identical syntax trees. [CI passed](https://github.com/mryfmo/dotfiles/actions/runs/37090108004), but did not detect these command regressions. No additional security, rule-compliance, evidence-integrity, or reporting findings.

📝 まとめ: Audited only `e5648fa6`; identified two Markdown command regressions. No files changed.

Verdict: incorrect