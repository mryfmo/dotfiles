[P2] high confidence home/dot_codex/rules/default.rules:137 — `chezmoi init --one-shot=true mryfmo` escapes the new prohibition: Codex 0.160.0 returns `{"matchedRules":[]}`, although chezmoi accepts this spelling and enables the same apply-and-purge behavior. Add this alternative and a regression test. [chezmoi reference](https://www.chezmoi.io/reference/commands/init/#--one-shot)

The committed unit test and all 72 `rm` flag permutations passed; exact-commit [CI passed](https://github.com/mryfmo/dotfiles/actions/runs/37113167423). No other changeset-specific findings.

📝 まとめ: Audited only `34e7423f`; found one P2 policy gap. No files changed.

Verdict: incorrect