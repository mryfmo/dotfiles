# Learning triage: dotfiles-T128-orchestrator-tools-followup-a03

These are candidates only; nothing is promoted.

1. [memory:failure] A test fixture for a duplicate-key refusal must put the exempt value last: PyYAML's default loader keeps the last value, so `kind: review` then `kind: code` is checked even without the refusal, and only `kind: code` then `kind: review` proves it. The mutant without the refusal survived until the second order was added.
2. [memory:decision] A recorder that finds its own row in a sliding window aligns the two windows as two views of one bus and requires a unique shift; a count or a single anchor row fails at the window's edge, under eviction, and on a periodic bus.
3. [memory:failure] `scripts/validate-agent-assets.py` now takes several minutes in the worker sandbox (the secret scan and the regime-boundary report); a gated commit needs a timeout above the default two minutes.
