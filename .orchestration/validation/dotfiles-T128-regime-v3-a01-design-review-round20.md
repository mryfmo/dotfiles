---
reviewed_at: 2026-10-12T11:14:53Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@7f007ec41c9b0dedded66c964ba8e858d1d604e40b10a0ab278966f7eb2a2ae6
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 20
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md
premises:
  1-13: hold, as dispositioned in rounds 9 and 11; byte-equal to v18's (PyYAML)
---

# Design review: dotfiles-T128-regime-v3-a01, round 20 (plan 006 B0: INV-12 narrowed; INV-2's dead clause; two map entries)

Delta judged against v18 at 4520b8f0 (origin/main). PyYAML: threat_model, trust_anchors, premises, supersedes, reset_of and design_review are equal to v18's; the invariant id set is unchanged; INV-2 and INV-12 are the only changed sentences; implementing_tasks gains dotfiles-T128-v0-main-tests-a02: [INV-12] and dotfiles-T128-gate-evidence-a01: [INV-6], nothing removed or changed. Below the front matter, the INV-12 enforcement row, the V0 wave row, the wave order and the v18 history paragraph changed, as the brief says.

## (1) Changed invariants

INV-2: accepted. The -contract-a01 remap is gone and no contract task remains mappable (the three *-contract-a01 files under .orchestration/tasks/ carry superseded_by); the in-job sentence now states A5's form, and main's test.yaml and remote.yaml carry no needs and no job-level if (grep on origin/main, 0 and 0), so the sentence is true of main today.

INV-12: accepted. The narrowed sentence keeps the guard (main's module of every script outside allowed_files, run as it is, so an undeclared change fails), keeps the in-process oracle, its nonce and its stated residual, keeps the gaming-path list and the legacy list, and moves the judgement of a declared script to the PR's tests, the diff review and the trusted-root audit, with the deleted-or-weakened test still a conformance finding. Note, not a rejection: INV-5's sentence does not itself say the audit reads the test diff beside the code diff; AGENTS.md's Audit section (regressions in existing behavior and tests) is where that duty lives, so the reference holds through AGENTS.md rather than INV-5's text.

## (2) Sentences that still depend on dormant contracts, REGIME_CONTRACT or -contract-a01, with owners

- SKILL on main, "Review and integration invariants", the task-file-review bullet (line 69): "one invariant check (a -contract-a01 id maps to its implementing entry)". Owner: the next SKILL docs task (T703 or a B0 follow-up), together with tests/fixtures/regime/invariants.md line 6, which pins the bullet whole, and tests/unit/test_agmsg_orchestration_docs.py line 278, which pins that token; all three in one commit or the whole-section test fails.
- .orchestration/tasks/dotfiles-T128-v1b-pr-caps-a01.md: three mentions (the contract-id lookup case in item 3 and its test). Owner: V1b's re-specification under B0 (plan 006 line 87 says every Phase B task file is re-specified before dispatch).
- .orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md: six mentions. Owner: A301, the a02 successor; a01 is parked input and stays beside its map entry, as B0 says.
- The three *-contract-a01 task files (v1-task-schema, v2-audit-schema-and-runner, ci-skip-orchestration): each carries superseded_by, so INV-10's dispatchability excludes them; no action.
- .orchestration/plans/006-regime-v3-execution.md lines 71 and 87: history and the B0 row itself; owner: the plan, no change needed.
- AGENTS.md, the regime rule file, scripts/: no mention. The design body: only the round-2 history line and the v18 paragraph, both history.

## (3) Does the narrowed INV-12 still close its threat

Yes for the threat it maps to: an undeclared change to any script outside allowed_files fails main-tests, which runs main's module as it is in the PR's context, deciding inside its own job. An intentional change to a declared script is now judged by three things the design names: the PR's own tests (its own workflow), the orchestrator's diff review, and the trusted-root audit from main (INV-5) reading the test diff beside the code diff, with a deleted or weakened fails-when-removed test a conformance finding; the in-process forgery residual stays named in every design-tier acceptance record. What is lost is the pre-merged oracle for a declared script; the design says so by construction, and no wave used the dormant form (A302 withdrew it).

## (4) The two map entries

- dotfiles-T128-v0-main-tests-a02: [INV-12]: right. A301's successor implements main-tests, which is INV-12's required check.
- dotfiles-T128-gate-evidence-a01: [INV-6]: the task (plan 007 T702) adds two gate refusals, a not-applicable disposition without an evidence= clause and an acceptance record whose finding-class table has three rows of one class and no pasted search (S6). INV-6's sentence states neither; its gate clauses are the count thresholds, the reset record and the waiver. INV-5's not-applicable clause is about audit findings at P0-P2, not Bot dispositions. So a task.md carrying INV-6 byte for byte would implement two rules no hashed sentence states, the class M-2 records (a rule owned nowhere but the script). Rejected as the entry stands; right would be one clause appended to INV-6, so the entry is honest and INV-12's fails-when-removed rule reaches both refusals: "; the same gate refuses a merge whose acceptance record carries a not-applicable disposition without an evidence= clause, or a finding-class table with three rows of one class and no pasted search of the correction records (plan 007 S6)". A hashed change, so this pair's revision; V3a and the merged regime-counters a02 are the only tasks carrying INV-6 (a02 is merged; V3a is not dispatched).

INV-1: accepted. INV-2: accepted. INV-3: accepted. INV-4: accepted. INV-5: accepted. INV-6: rejected: the gate-evidence entry maps to a sentence that does not state the two refusals; append the clause above. INV-7: accepted. INV-8: accepted. INV-9: accepted. INV-10: accepted. INV-11: accepted. INV-12: accepted.

Design verdict: revise
