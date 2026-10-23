# M-20261022-02 — a task text prescribed the textual shape of omp bash.patterns three times, each wrong against the documented matcher

- When: 2026-10-22 08:42Z to 09:30Z (dotfiles-T129-omp-seat-policy-a01, anchor rounds 1-3 by a011).
- What: the text (orchestrator-authored) listed deny patterns and, after each finding, a new rule about their shape: start-anchored literals (round 1, F1b: env-prefixed and endpoint-first forms escaped), `*gh api * -X POST*` (round 2, F4: the space before the inner `*` required a token, so flag-first forms escaped), then a validator refusal "no literal space between an inner `*` and its token" (round 3, F5: it refused the text's own allow, curl/wget and git patterns).
- Root cause: the requirement is behavioural (which commands a role may run) but the text specified the mechanism's surface (pattern strings) and reasoned about omp's matcher in prose instead of executing it; each round added a prose rule rather than a test.
- Mechanism: the text specifies a classification table and ships a reference matcher implementing the documented rule; patterns are data the worker shapes until the table passes; the validator carries no shape heuristics; the X pilot confirms the reference matcher against live omp. Generalised: a text never prescribes the surface form of a third-party rule language; it ships the oracle.
- Cost: three anchor rounds (about 50 minutes of the review seat) and the C-59 stop on the text.

classes: [pattern-shape, prose-specified-mechanism]
