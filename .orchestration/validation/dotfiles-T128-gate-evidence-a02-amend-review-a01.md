---
reviewed_at: 2026-10-12T14:27:14Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@9c9d42cb00c52457e8e7df37bf5276d42978d3466768286cd30b326fb8fdc0e2
task: dotfiles-T128-gate-evidence-a02-amend-review-a01
round: 1
files:
  - dotfiles-T128-gate-evidence-a02@241aec126fc58092f2ffabc59b142567f3b8f1a6f68d5798d511d1a511dd2f5c
verdicts:
  dotfiles-T128-gate-evidence-a02: confirm
---

# Amendment confirmation: dotfiles-T128-gate-evidence-a02 amendment 1 (the recomputed records search; the first-delimiter split)

1. Diff against main (7cbe5405, the a02 as this seat wrote it at 930f570b): the heading gains the amendment note with the four thread ids; the introduction gains the amendment paragraph (M-20261012-20, C-22, the S1 record, the worker's head d5d6c9b1 and its two fix rounds kept); item 1 splits the disposition at the first "; evidence=" and refuses a second delimiter; item 2 replaces the scan of the pasted search line with a recomputation (grep -rl 'classes:.*<slug>' over the mistake records from the repository root) compared as a set with the fixed-template line "search: <slug> -> <sorted basenames or none>", leaves the CompactionDB half an unvalidated paste, reads no pasted command text, and refuses with "S6: class <slug> at <n> without a matching records search". Nothing else: the invariants block, the seventeen rows, the premises, items 3 to 5, Validation and Completion are byte for byte main's.
2. The check cannot be satisfied by text that is not the recomputed set: the gate compares two sets, one it computed and one it parsed from a fixed template, and consults no command text, so the three bypasses of 2026-10-12 (a bare-directory grep, a class token in a prefix, xgrep and echo grep) have nothing to act on; the disposition grammar has one shape, reason then one "; evidence=" then command, with a second delimiter refused, which closes the greedy-split bypass (4248934816). Both read INV-6's clause as the records search being present and true, and C-22 states the same two rules; INV-12's enforcement row (no new hand-written parser at a trust boundary) is what the recomputation satisfies, since the only parsing left is two fixed templates.
3. Checker OK (C1 to C9). By hand: C7, the eight names are in the rows, unchanged; C9, the items quote no SKILL sentence, so nothing is stated as present; invariants.INV-6 is byte-equal to the design on main; reset_of, the copy rows and the a02 directory are unchanged.

Note, implementation-level, not a defect of the task text: the slug enters the grep pattern, so the implementation refuses a slug outside [a-z0-9-] (every ledger slug today is in that alphabet; A7 reduces class names to it), invokes grep without a shell, and treats grep exit 2 as a refusal (exit 1 is "none"); item 2's "the gate recomputes the records search itself" leaves the invocation to the implementation, and INV-12's rule and the audit cover it, so no task-text change is needed.

Amendment verdict: dotfiles-T128-gate-evidence-a02: confirm
