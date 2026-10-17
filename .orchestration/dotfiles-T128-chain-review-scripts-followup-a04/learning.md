# Learning triage: dotfiles-T128-chain-review-scripts-followup-a04

These are candidates only; nothing is promoted.

1. [memory:decision] When a row asks for two guards and the first makes the second unreachable (here the seven-hex suffix check before the literal id match), a mutation run shows the second as a surviving mutant. Report it as defence in depth that survives by construction, and give the first guard its own failing case (the `notes` suffix), instead of writing a test that has to disable the first guard.
2. [memory:decision] A regression test that reproduces an audit should keep the audit's own symptom in its red run: with two matching rows the old script's `tail -1` showed whichever row came last, so the unrelated row is placed last and the red run reads `unrelated-class` as the audit did.
