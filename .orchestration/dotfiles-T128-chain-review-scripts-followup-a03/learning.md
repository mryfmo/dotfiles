# Learning triage: dotfiles-T128-chain-review-scripts-followup-a03

These are candidates only; nothing is promoted.

1. [memory:decision] A mutant that survives is either a test gap or code with no effect. This run had one of each: the line-range token was untested (a `y.sh:3-9` case now tells it from `y.sh:3-5`), and a backtick strip did nothing because the token's character class already excludes the backtick, so the strip was deleted rather than tested.
2. [memory:decision] Mutants written as literal string replacements (Python's `str.replace`, asserted to match once) avoid both sed's regex escaping and perl's variable interpolation inside `\Q…\E`, which made an earlier task's perl mutants change nothing.
