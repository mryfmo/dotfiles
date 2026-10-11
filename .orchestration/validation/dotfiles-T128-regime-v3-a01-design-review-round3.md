---
reviewed_at: 2026-10-10T21:33:02Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b2bfad90d1e1d3b8210b40321f6d23cfdab7c4e5b27e8d644b02a8fea9d535d2
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 3
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round2.md
---

# Design review: dotfiles-T128-regime-v3-a01, round 3 (confirmation)

Same reviewer and seat; v3 read in full at the hash above and checked line by line against the five edits of the round-2 receipt's section 4. The hashed keys changed between v2 and v3 (implementing_tasks, INV-1, INV-2, INV-3, INV-6, INV-8, INV-12, one premise), so this round is the review INV-7 requires. No command was re-run and no page re-fetched: v3 adds no claim that round 1 or round 2 did not already verify.

## 1. The five edits

1. implementing_tasks is a map of task id to invariant ids inside the hashed keys (lines 9-21); INV-2 states the design-on-main precondition through a boundary PR and the fail-closed rule for a missing design (line 45); V1 repeats the precondition (line 162). Applied.
2. revise.yaml is a sibling file and task.md stays byte-identical (INV-3 line 46; INV-8 line 51; INV-12 gaming path line 55; enforcement row line 148; V3c line 168; the validation-file line assigned to V2b, line 165). Applied.
3. Question threshold 2 in INV-6 (line 49) and section 7 (line 179); audit JSONs count only when their sha256 matches their AGMSG-AUDIT record (line 49; map line 151). Applied.
4. V3a is an operator PR carrying all hook counting, with a Codex security-profile review before acceptance (line 166); V3b has no hook source (line 167); V3c has no gate source (line 168). Applied.
5. The legacy list is excluded from the line cap as data (INV-2 line 45; INV-12 line 55; V1 line 162); the workflow_dispatch premise is added with the page's sentence (lines 84-86); the stage-3 sentence names the orchestrator's make audit-head and what removes the queue (line 140); INV-1 names the latest TASK's token and the recommit after each amendment (line 44). Applied.

## 2. Invariants

INV-1: accepted.
INV-2: accepted. Note: section 7 (line 179) still words the cap as "outside tests/ and .orchestration/" without the data-list exclusion that INV-2 and INV-12 state; section 7 is outside the hash, so align it in the next edit without a new review.
INV-3: accepted.
INV-4: accepted.
INV-5: accepted.
INV-6: accepted.
INV-7: accepted.
INV-8: accepted.
INV-9: accepted.
INV-10: accepted.
INV-11: accepted.
INV-12: accepted.

## 3. New in v3

- scripts/regime-check.sh (lines 162, 168) now holds the regime job's logic, consistent with the residual that regime.yml itself is never exercised by its own PR (line 191). V1 is nine files; its added lines outside tests/, .orchestration/ and the data list (schema, validator, module, regime-check.sh, workflow, manifest, SKILL) are close to the 500 cap; V1b is the split if it goes over.
- V2b's map entry is [INV-5] (line 13) while its scope carries INV-3's validation-file line (line 165). The id comparison of INV-2 is between task.md and the map, not the diff, so this is not a mechanical conflict; V2b's acceptance record should say the line is INV-3 enforcement dispatched under V2b, or the map lists [INV-5, INV-3] at the next hashed-key change.

Nothing in v3 reopens a round-1 or round-2 finding.

Design verdict: accept
