[P1] High — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:106` — `acceptance-front-matter.py` has no defined source or preservation rule for `searches`, nor an input for `{n, reason, evidence}` audit dispositions, so S6-triggering or incorrect-audit records cannot reliably satisfy amendment 1’s required JSON contract.

[P2] High — `.orchestration/tasks/dotfiles-T128-orchestrator-tools-a02.md:111` — Numeric and missing `id` rows must be ignored, but none of the only permitted reason slugs (`ledger-row-not-object`, `class-not-slug`, `block-not-json`) accurately represents an object whose `id` is absent or non-string.

Task-file verdict: dotfiles-T128-orchestrator-tools-a02: revise