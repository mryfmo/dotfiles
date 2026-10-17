# Learning triage: dotfiles-T128-chain-review-scripts-followup-a02

These are candidates only; nothing is promoted.

1. [memory:failure] A test loop whose cases share a temporary repository needs a per-case reset of every artifact a passing run leaves (here the review file, which the script reuses before any check): otherwise one mutant fails every later case, and the mutation table cannot show which case kills which mutant.
2. [memory:decision] When a parser is out of scope, refuse the inputs it would split differently instead of approximating them: the `env -S` refusal names the four features (quote, escape, expansion, comment) and tests one case per feature, with a mutant per feature.
