---
reviewed_at: 2026-10-12T13:07:02Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@7a067b19e88c6ad2546f6f0320821d2fd6e1bd5bb0b0a852d6db901312b31488
task: dotfiles-T128-gate-evidence-redesign-a01
reset_of: dotfiles-T128-gate-evidence-a01
source: .orchestration/tasks/dotfiles-T128-gate-evidence-a01.md@d1b6fcf3f1f7aada49c8a38e79fae57525d135d59d9c44a3ef5ebc87e79a8d26
successor: .orchestration/tasks/dotfiles-T128-gate-evidence-a02.md@930f570b9a44114ab68062575b212fdcbd959653cebb1f3f7c710d717f033ddf
consistency_check: "dotfiles-T128-gate-evidence-a02.md: OK (C1 to C7)"
verdict: accept
---

# Redesign: the successor task file dotfiles-T128-gate-evidence-a02 (INV-6 reset of T702: a missing threat row would be amendment 2)

Written by this seat into the main checkout, as the TASK's allowed_files permit, from a01 amendment 1 at d1b6fcf3 by a script that applied each edit exactly once and asserted it, then parsed the front matter with PyYAML. The successor is 98 lines; its sha256 is in the header.

## Diff summary, a01 amendment 1 to a02 (eleven hunks)

1. Front matter (item 1): task_id a02; reset_of [a01]; allowed_files names .orchestration/dotfiles-T128-gate-evidence-a02/** in place of the a01 directory; the a01 copy row stays as a history row and a second row names the a02 copy with the residual that binds the a02 file's hash; the evidence-records row names the a02 directory; design_review.receipt stays round 22; invariants.INV-6 is untouched and byte-equal to the design on main (PyYAML).
2. The new row (item 2), after the README row: control "the ACCEPTANCE_EVIDENCE input: the acceptance record's path and content (ledger rows, search: lines, audit-finding: lines), written by the orchestrator and read by the gate" (quoted, since it carries colon-spaces), disposition closed: tests/unit/test_require_crit_review.py::test_base_requires_an_acceptance_record_under_acceptance, the worker's proposed test name.
3. Item 2's search-line grammar (item 3): the line names the class slug, a grep carrying classes: over the mistake records in either form (grep -rl on the directory, the SKILL's form in playbook-rules a02 item 3, or grep -l on the *.md glob) and the memory search; the fixtures use the SKILL's form. Item 2's reference to the sibling now names dotfiles-T128-playbook-rules-a02.
4. Item 5 (item 4): the sibling id becomes a02 and the thread 4248232955 sentence is appended with the proposed not-applicable and its evidence= command.
5. Heading and introduction (item 5): the heading names the reset; the introduction names the Bot round on 5971fffe (review 5491066199), the question PONG of 13:00:25Z, the reset record, the worker, the same branch and PR #329, the four prepared fixes kept as made and the task copy recommitted under the a02 path; "C1 to C6 pass" becomes "C1 to C7 pass".
6. Completion, last sentence: PR #329 is open since a01, so "draft PR from origin/main" becomes "PR #329 (open since a01, continued from head 5971fffe)".

Items 1, 3 and 4, the premises, Validation and the other rows are byte for byte a01 amendment 1's. The amendment-1 sentence of the introduction keeps its historical reference to the sibling as a01, since that is what the sibling was at 12:3xZ.

## Checks

- Checker: OK (C1 to C7). Re-derived by hand: C3, rows name .orchestration/dotfiles-T128-gate-evidence-a01/task.md and .orchestration/dotfiles-T128-gate-evidence-a02/task.md; C4, every allowed path has a row (the gate script, the test module, tests/fixtures/gate-evidence, Makefile, README.md, the a02 directory); C7, the eight names task metadata, metadata separators, in-process effects, workflow and interpreter or environment inputs, new or renamed scripts, orchestrator effect merge, orchestrator effect update-branch, orchestrator effect forced worker removal; the ninth non-path row of item 2 is the ACCEPTANCE_EVIDENCE input with its closed selector in the tests/<file>::<name> form.
- Premises replayed per C-18 with the executor's binaries against origin/main at 4cf1d4e2 (git show origin/main:<file> piped to /usr/bin/sed, /usr/bin/grep and /usr/bin/awk): premise 1's two lines, premise 2's rows 26 and 33, and premise 3's rows 16 to 18 are byte-equal to the pasted outputs, so the premise blocks are unchanged.
- Map lookup (INV-2): the design on main (7a067b19) maps dotfiles-T128-gate-evidence-a01: [INV-6] and has no entry for a02; INV-2 compares a task id with its own entry, so the successor needs dotfiles-T128-gate-evidence-a02: [INV-6] on main before its final audit and merge, a hashed change with its review pair, as the ci-skip and regime-counters successors needed at round 18. The a02 file is correct as written; the entry is the design's.

Verdict: accept, this RESULT being the reset anchor under the record's redesign_source.
