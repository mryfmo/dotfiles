[P2] high confidence orchestration .orchestration/acceptance/dotfiles-T128-playbook-rules-followup-a01.md:17 The referenced “dispatch list above” is absent: neither the JSON nor the prose contains the required bus lines. The initial and amended TASK payloads, hashes and read markers therefore cannot be checked against this record. Restore the bus-derived `dispatch` entries required by step 6 and task item 1.

The implementation matches the four owned rows. Both rule-gap rows share the step-6 fix; the migration covers all specified locations; disposition-range correctly requires no edit. No unrelated rule sentences changed, and the documented mechanisms exist on main. Both fixtures match. All 48 tests pass; reverting each of the six rule edits makes its token test fail. Final-head Actions succeeded for [PR #354](https://github.com/mryfmo/dotfiles/pull/354).

The task declares no `invariants` map; its directly applicable caps and test requirements were checked:

INV-2: holds .orchestration/dotfiles-T128-playbook-rules-followup-a01/validation.md:164 — verified 5 files, 6 added non-test lines and 50 added test lines.
INV-12: holds tests/unit/test_agmsg_orchestration_docs.py:519 — token regression checks and matching whole-section fixtures pass.

📝 まとめ: Read-only audit completed; the implementation passes, but the acceptance record lacks its cited dispatch evidence.

Orchestration findings: 1
Not checked: local Bats and the merge gate; dispatch evidence remains incomplete.
Verdict: incorrect