---
reviewed_at: 2026-10-10T22:06:21Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@6eedc15f74d9a150a601190e3fb839175be3799c2eadf37331f850430c930210
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 4
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round3.md
---

# Design review: dotfiles-T128-regime-v3-a01, round 4 (confirmation of the V1 split)

Diff check of v4 against the four edits the Round-4 section names. The hashed key implementing_tasks changed, so this is the review INV-7 requires.

1. V1 is validation only (line 163: schema, validator, tier module, legacy list, its test) and V1c is the CI check after V1 (line 164: regime-check.sh, regime.yml, its test, process_tiers, SKILL step 3, README); V1b follows V1c (line 165). Applied.
2. implementing_tasks gains dotfiles-T128-v1c-regime-ci-check-a01: [INV-1] (line 11), the second task on one invariant as V2 and V2b are on INV-5. Applied.
3. Order V1, V1c, V1b, V2, V2b, V3a, V3b, V3c, V3d, V4, V5a, V5b, V6 (line 177); V1 with V2 stays the concurrent pair. Applied.
4. Section 7 (line 181) now reads "15 changed files (the file count excludes .orchestration/ only) and 500 added lines outside tests/, .orchestration/ and the data list scripts/legacy-task-ids.txt", matching INV-2 and V1b. Applied. The receipt pointer names this round (line 7).

The four task files that follow carry INV-1, INV-2 and INV-5 byte-identical to this file's invariants (checked with PyYAML) and name this receipt.

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: accepted. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Note: INV-1's sentence names "V1's acceptance record" for the ruleset action; after the split that record is V1c's. The sentence is hashed, so leave it and let V1c's acceptance record say it carries the action.

Design verdict: accept
