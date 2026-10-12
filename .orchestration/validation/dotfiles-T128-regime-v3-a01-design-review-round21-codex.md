reviewed_at: 2026-10-12T11:45:01Z (headless run 11:44Z; receipt saved by the orchestrator)
reviewed_at: 2026-10-12T11:45:01Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@dd5b7ff2f0c77bc1d8820bdbca413b36c25c2f39db3804126342e83b116a4dfa  
round: 21  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round20-codex.md

INV-6: rejected: the proposed clause is byte-equal and appears once, but it was appended to INV-4 at line 55, not INV-6 at line 57. Move that exact clause from INV-4 to the end of INV-6. The gate-evidence task truthfully specifies both refusals in `scripts/require-crit-review.py`, INV-6’s mandatory merge backstop, but its `[INV-6]` mapping remains unsupported until INV-6 itself states them.

## Findings

- P1 high — `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:55`: PyYAML comparison with the v18 front matter shows `changed_invariants ['INV-4']`; INV-6 is unchanged and contains no proposed clause. The other requested hashed keys—`threat_model`, `trust_anchors`, `implementing_tasks`, and `premises`—are equal. This contradicts the claimed sole INV-6 change and leaves `dotfiles-T128-gate-evidence-a01: [INV-6]` mapped to an invariant that does not state either refusal.
- P2 high — `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md:226`: the v19 history says INV-6 gained the clause, but the clause is actually in INV-4. Correct the placement; the historical claim then becomes true.
- Verification note — the independently computed whole-file SHA-256 is `dd5b7ff2f0c77bc1d8820bdbca413b36c25c2f39db3804126342e83b116a4dfa`. `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md:62-64` specifies both requested refusals and tests them at the mandatory gate.
- No files were modified and implementation tests were not run; this was a read-only design review.

Design verdict: revise