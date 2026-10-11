reviewed_at: 2026-10-11T07:35:58Z  
reviewer: codex-review-dot-h001 (headless)  
profile: review  
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@1d5f4c07e8a23d0bc5185931fe1037c16b76ae48441b62ffb05bd3ffde2ac0a5  
round: 18  
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round17-codex.md

INV-1: accepted

INV-2: accepted

INV-3: accepted

INV-4: accepted

INV-5: accepted

INV-6: accepted

INV-7: accepted

INV-8: accepted

INV-9: accepted

INV-10: accepted

INV-11: accepted

INV-12: accepted

## Findings

The two entries name exactly the invariant sets carried by their reset successors: `dotfiles-T128-ci-skip-orchestration-a02` carries only INV-2, and `dotfiles-T128-regime-counters-a02` carries only INV-6.

The per-task entries are necessary under INV-2’s current lookup: reset successors retain distinct task ids, while only `-contract-a01` ids are remapped. No additional hashed-key change is needed. INV-6’s `reset_of` binding authenticates the reset relationship; it does not provide implementing-task map inheritance. Adding a general successor-to-predecessor mapping rule would be a separate semantic change, not required for these two successors.

Removing exactly these two lines reproduces whole-file sha256 `15957fbc6b47ff8f2424072ca5b5849911b7be90582e1d850f5d315563494cd4`. Therefore INV-1 through INV-12, the premises, and all other hashed content are unchanged from round 17.

## Residual

The round-17 residual remains unchanged: the PR-authored counter implementation, tests, fixtures, and `source=` label depend on the trusted-root audit and live acceptance replay until V0’s main-tests protection lands. V3a remains responsible for the mandatory merge backstop and protected waiver path. Implementation and tests were not executed; no files were modified.

Design verdict: accept