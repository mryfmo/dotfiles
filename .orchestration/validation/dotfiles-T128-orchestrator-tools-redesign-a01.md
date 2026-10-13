---
reviewed_at: 2026-10-13T04:18:43Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@fa2c5157e6b962d10076a505788cb9d074e366acc73a8fa5e83877b77c5a863a
task: dotfiles-T128-orchestrator-tools-redesign-a01
task_file: dotfiles-T128-orchestrator-tools-redesign-a01@e4b70c9752cb9320d0bd956164943365539a891c982395c399907b35d6e9d655
reset_of: dotfiles-T128-orchestrator-tools-a01
source: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01.md@91eb1ebe246f76e138ce8f3bf108adff844f5acf303bcfecc2b7bc62eb0130ee
successor: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a03.md@b7348b8a2c08f1102eb4357249256a0790075c1a9b36de408a598daf86e19952
consistency_check: "dotfiles-T128-orchestrator-tools-a03.md: OK (C1 to C10, C7b)"
verdict: accept
---

# Redesign: the successor task file dotfiles-T128-orchestrator-tools-a03 (the INV-6 reset of T718's first slice: the record read-and-rewrite row)

Written by this seat into the main checkout, as the TASK's allowed_files permit, from a01 amendment 1 at 91eb1ebe (the copy on main 4470b0c8, byte-equal) by a script that applied each edit exactly once and asserted it, then parsed the front matter with PyYAML. Both hashes of the 04:15:04Z TASK line recomputed and equal. The successor is 110 lines; its sha256 is in the header. dotfiles-T128-orchestrator-tools-a02 is T718's second slice and is not touched.

## Diff summary, a01 amendment 1 to a03 (the brief's items 1 to 4, then the bookkeeping)

1. Front matter (item 1): task_id a03; reset_of [a01]; allowed_files names .orchestration/dotfiles-T128-orchestrator-tools-a03/** in place of a01's; the a01 copy row becomes a history row (as dispatched at amendment 1; not edited under a03; no hash phrase, so C5 is silent) and a second row names the a03 copy with the residual that binds the a03 file's hash; the evidence-records row names the a03 directory; design_review.receipt stays round 22; after: [] stays.
2. Threat table (item 2): one new row after the two dispatch.sh rows, quoted because it carries a colon: dispatch.sh, given an acceptance record path, reads the record's JSON block, reads the bus marker through history.sh and rewrites the record's dispatch list after the send (a gate input mutated by the orchestrator's tooling; thread 4254494999), with the controls it keeps (the path is the orchestrator's argument, object_pairs_hook on read, only the dispatch list changes, the file written whole with sort_keys and indent=2, the a04 gate re-validates the block); closed by test_dispatch_records_the_sent_line_with_its_read_marker, which exists in the head 5ec05d8d (git show 5ec05d8d:tests/unit/test_orchestrator_tools.py, line 166).
3. Item 2 (item 3) names that test beside the happy-path sentence it describes (the name appears three times in the file: the row, the introduction's reset paragraph and item 2).
4. Heading, introduction and Completion (item 4): the heading names the reset and says -a02 is the second slice, not a predecessor; a new first paragraph names thread 4254494999 and what it found, the amendment-1 head 5ec05d8d, the INV-6 trigger with the counters of 04:14Z, what a03 adds, the a02 note, the six worker commits kept and the same worker on PR #336; the a01 paragraph follows under "History (a01)"; Completion continues PR #336 from 5ec05d8d with the a03 task copy and evidence as the expected change; the "Amendment 1" section is kept under the heading "History: a01 amendment 1 (…; a03's base)". The reset record is named in the gate-evidence lineage's form (dotfiles-T128-orchestrator-tools-a01-design-reset.md); if the orchestrator names it otherwise, that one path is the orchestrator's to align.
5. Bookkeeping beyond the brief, one phrase in two places: the task-metadata row and the introduction say the checker range "C1 to C10 and C7b" (was "C1 to C6"), the phrase the checker and the stop condition name, and the one the a04 lineage corrected the same way (its brief item 7).

Items 1, 3 and 4 of the task, the premises, Validation and the environment row are byte for byte a01 amendment 1's (item 5); premises 1 to 3 replayed at origin/main 4470b0c8 with /usr/bin/grep -h, git grep against origin/main and /bin/ls are byte-equal to their pasted outputs, so the premise blocks are unchanged.

## Checks

- Checker: OK (C1 to C10, C7b). Re-derived by hand: C3, rows name the a01 and a03 task copies; C4, every allowed path has a row (scripts/orchestrator/* through the dispatch.sh, three-repeat.sh and bus-read.sh rows, the two test modules, regime-counters.sh, the a03 directory; the new row names no path and adds none); C7, the eight names; C7b, one row per allowed_files entry; C8, no new *_EVIDENCE input; C9, no quoted rule sentence; C10, no sentence states an output a script on main lacks.
- amend-sweep for orchestrator-tools-a01/: the one hit is the a01 history copy row; the premise's -a01-input/ directory is a different path and stays (the inputs are evidence).
- The new row's test name exists in 5ec05d8d (line 166) and nowhere else is required; the worker's RESULT of 04:13:13Z names the record write as implemented, so a03 asks for no new code beyond the task copy and evidence.
- Design map: main maps no T718 slice and a03 declares no invariants (kind code, review tier by INV-1), so INV-2's set comparison holds with empty sets; no design round is needed for this reset.

Verdict: accept, this RESULT being the reset anchor under the record's redesign_source.
