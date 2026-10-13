P1 (high confidence) `.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md:87-88` — The amendment requires `parse_constant` to reject NaN/Infinity but mandates no corresponding test; this violates INV-12’s “every rule … exercised by a unit test” requirement, so add a rejecting fixture/test for non-finite JSON constants.

Amendment verdict: dotfiles-T128-gate-evidence-a03: revise