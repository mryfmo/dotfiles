---
reviewed_at: 2026-10-13T10:40Z
reviewer: claude-review-dot-a001 (review seat; the Codex half runs the same check on the same hashes)
profile: review
session: 2089b04f
task: dotfiles-T128-playbook-rules-a04-amend-review-a01
round: 2
task_file: .orchestration/tasks/dotfiles-T128-playbook-rules-a04-amend-review-a01.md@2b29a1510f01ebd5778d0f794d2e3be50562fb242ae89ca155b934e8e70fb525
amended_task: .orchestration/tasks/dotfiles-T128-playbook-rules-a04.md@c5dbc2c3d3514707870c2146ac4acfd6e96279d50f0f6bf04bd8921cd242a6fa
amended_task_main_copy: a03c1daa@e64ee6912c33d98305e70b4206f4d0f55bd4236730131a080f0fd81e7227f254
owner_task: .orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md@cb32794d2bb939456e747230e012729d47c327946fbe07fe97d644969dc4fa42 (untracked; not on main)
previous_round: a04@9c3c6b10 revise, followup@2958c5a2 revise (seat receipt 7ddc4f86a1ea9cb17a2aa6e42148a8f750f3e750b1826842e4aceaf2ad9928aa; Codex: a04 revise on line 74, followup confirm)
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main; INV-2 at line 56, INV-10 at line 64 (unchanged since round 1)
consistency_check: owner task C1 to C10 and C7b OK (checker sha256 fdab23e0, copy named by task_id); a04 FAIL on the same single C10 line as on main's copy e64ee691 (item 3, pre-existing, out of scope)
amend_sweep: `thirty minutes` hits lines 74 and 98, `complete bus read` hits line 98 only; line 74 carries the superseded parenthetical, line 98 is the Amendment 1 section (heading at 96), as the Round 2 stop condition 4 requires
---

# Amendment review: dotfiles-T128-playbook-rules-a04 amendment 1 and the owner task dotfiles-T128-playbook-rules-followup-a01 (round 2)

## Round 1 findings, re-checked on the new hashes

1. Finding 1 (P2, owner task premise 2 and item 1): closed. Premise 2 is `git cat-file -e origin/main:<a04 acceptance record> && echo present`, which replays as `present` today and keeps holding as the record grows; item 1 is defined by the `<id>\t<class>` rows under `## Owned by dotfiles-T128-playbook-rules-followup-a01` read from `origin/main`, with the dispatch condition (after the boundary that lands the section; the dispatch line names the record's hash) and the empty-section no-op; a04's Completion names the same heading and row form, so both files describe one source. The heading does not exist in the record yet (0 hits in the working tree), which is correct: it is appended at a04's acceptance.
2. Finding 2 (P3, a04 line 74): closed. The parenthetical "(superseded by amendment 1 of a04: INV-10's idle figure is 20 minutes)" sits beside the a02 wording; the sweep's line 74 hit is that line.
3. Finding 3 (P3, wildcard self-application): closed. Item 4 now scopes the per-file rows to wildcard entries whose files are executed or applied (scripts, workflows, hooks, settings, the rules seats follow) and keeps one row for a wildcard over fixtures or other data files; the Amendment 1 section says the same. Both tasks' `tests/fixtures/regime/*.md` rows stand under that wording. The design is silent on row granularity, so no conflict.

## Stop conditions

- Stop 1: `git diff -U0 origin/main` on a04 touches lines 74 (the parenthetical), 78 (item 1), 81-82 (items 4 and 5), 94 (Completion) and adds the Amendment 1 section; nothing else. Items 1 and 5 still follow design lines 64 and 56 word for word.
- Stop 2: unchanged from round 1 (scripts on `a03c1daa`; `bus-read.sh` refuses at `BUS_READ_LIMIT` and flags silence at 30; no invariant-sentence checker on main).
- Stop 3: checker OK; premise 1 replays as `1` (`Owned by` is case-distinct from `owned by`, and both sit on one line); premise 2 as `present`; item 1 closed to the named section.
- Stop 4: as the header says.

## Findings

1. P3, confidence high, `.orchestration/tasks/dotfiles-T128-playbook-rules-a04.md:98`. The Amendment 1 section ends "Nothing else changes: not items 2, 3, 6 and 8, not the threat table, not the premises" and does not name the line 74 parenthetical, which the review task's Round 2 section records instead. The a04 file's own audit trail is one clause short; no verdict weight (the review task is the record of this round), fold it in only if the file is edited again for another reason.

Out of scope, unchanged: item 3's stale "Once plan 007 T718 lands" clause.

Amendment verdict: dotfiles-T128-playbook-rules-a04: confirm
Task-file verdict: dotfiles-T128-playbook-rules-followup-a01: confirm
