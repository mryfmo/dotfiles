---
reviewed_at: 2026-10-12T15:31:06Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@20d0937b9f7c6adebe6e4d5e6ad26ceb3578ae9b050bdce4f353b0a00ce9504a
task: dotfiles-T128-gate-evidence-redesign-a02
reset_of: dotfiles-T128-gate-evidence-a02
source: .orchestration/tasks/dotfiles-T128-gate-evidence-a02.md@241aec126fc58092f2ffabc59b142567f3b8f1a6f68d5798d511d1a511dd2f5c
successor: .orchestration/tasks/dotfiles-T128-gate-evidence-a03.md@686806a1b6cff143eef371f518098ac8b926fbe91462c1f8a5ac67d6e07c482e
consistency_check: "dotfiles-T128-gate-evidence-a03.md: OK (C1 to C9; the checker at the orchestrator's path carries no C8, see below)"
verdict: accept
---

# Redesign: the successor task file dotfiles-T128-gate-evidence-a03 (plan 011 option F: the acceptance record as YAML front matter)

Written by this seat into the main checkout, as the TASK's allowed_files permit, from a02 amendment 1 at 241aec12 (the copy on main at e0e2fe62, byte-equal) by a script that applied each edit exactly once and asserted it, then parsed the front matter with PyYAML. The successor is 100 lines; its sha256 is in the header.

## Diff summary, a02 amendment 1 to a03 (twelve hunks)

1. Front matter (item 1): task_id a03; reset_of [a01, a02]; allowed_files names .orchestration/dotfiles-T128-gate-evidence-a03/** in place of a02's; the a01 copy row stays, the a02 copy row becomes a history row (no hash binding, so C5 is silent) and a third row names the a03 copy with the residual that binds the a03 file's hash; the evidence-records row names the a03 directory; design_review.receipt stays round 22; invariants.INV-6 is untouched and byte-equal to the design on main (PyYAML).
2. Item 2 (item 2) is the acceptance-record contract: ACCEPTANCE_EVIDENCE required in PR mode under .orchestration/acceptance/<task id>.md; a YAML front matter loaded with yaml.safe_load and checked field by field, no regex over prose; format 1; task equal to the file name's id; head equal to HEAD with the refusal text; pr; ledger rows {id, class} with the id and class grammars; searches entries {class, records} for every class at three, the records set equal to the gate's own grep -rl run without a shell from the repository root, records: [] for none, the S6 refusal text otherwise; audit_findings entries {n, reason, evidence} when the audit is incorrect, no fixed: there; the prose is not read; AUDIT_DISPOSITIONS retired, the Makefile recipe and comment and the two README lines naming ACCEPTANCE_EVIDENCE in its place; the step 10.4 sentence is playbook-rules a04's; the existing PR-mode tests gain the variable; the passing shape of a record with nothing at three.
3. Item 1 (item 3): the grammar is one split on the first "; evidence=" into two non-empty parts, linear, a second delimiter refused; and, because item 2 retires AUDIT_DISPOSITIONS, the sentence that applied the grammar to audit-finding: lines read through that variable now says audit findings are dispositioned through the record's audit_findings entries (item 2). Without this the two items contradicted each other.
4. Item 3 (item 4): the fixtures are the two pr-feedback JSON files and four acceptance-record front matters (stale head refused; a class at three without its searches entry refused; a matching records set accepted; a reason that quotes "not-applicable:" accepted, the 4249544748 case); six fixtures under 90 lines together, the test count growing by at least six (a02 said four under 60).
5. Item 5 (item 5): the three round-4 threads become fixed:<sha> through the contract (4249544748 fields not substrings; 4249544762 head equals HEAD; 4249544794 one split, linear checks); the sibling id in item 5 and in the not-applicable proposal is playbook-rules a04, the sibling's current successor.
6. Heading, introduction and Completion (item 6): the heading names the reset under plan 011 option F after the second S1 cycle; the introduction names the two cycles with their thread ids, the round-4 threads, M-20261012-22 and C-24, the operator's choice at 15:25Z, the reset record, INV-1's form for the contract, the a02 heads d5d6c9b1 and 61d90302 and the merge head 4e2266aa, the worker's commits kept, and the design note (main maps a01 and a02; a03 needs its own implementing_tasks entry, a design round after this redesign as round 24 did for a02); "C1 to C7 pass" becomes "C1 to C9 pass"; Completion continues from the worker's head 61d90302 (merge head 4e2266aa) with the PR open.
7. Two bookkeeping lines beyond the brief, both consequences of item 2: the fixtures row names four acceptance-record front matters instead of two records, and the ACCEPTANCE_EVIDENCE row's control names the front-matter fields (task, head, pr, ledger, searches, audit_findings) instead of ledger rows, search: lines and audit-finding: lines.

Item 4, the premises, Validation and the other rows are byte for byte a02 amendment 1's (item 7); premises 1 to 3 replayed with /usr/bin/sed, /usr/bin/grep and /usr/bin/awk against origin/main at e0e2fe62 are byte-equal to their pasted outputs, so the premise blocks are unchanged.

## Checks

- Checker: OK (C1 to C9). The script at the orchestrator's path defines C1 to C7 and C9 and no C8; what the brief calls C8 was checked by hand: ACCEPTANCE_EVIDENCE appears in no double-quoted sentence (the task quotes no SKILL text, so nothing is stated as present), and AUDIT_DISPOSITIONS appears once in the body, in the sentence that retires it. Re-derived by hand: C3, rows name the a01, a02 and a03 task copies; C4, every allowed path has a row (the gate script, the test module, tests/fixtures/gate-evidence, Makefile, README.md, the a03 directory); C7, the eight names; C9, no quoted rule sentence.
- The contract names every field the gate reads (format, task, head, pr, ledger, searches, audit_findings) and names no prose the gate reads; it rests on INV-1's form, INV-6's clause (the records search present and true) and INV-12's enforcement row (no hand-written parser at a trust boundary).
- Design map: main (e0e2fe62) maps dotfiles-T128-gate-evidence-a01 and -a02 to [INV-6] and has no a03 entry; the introduction says so, and the entry is the design's, before a03's final audit and merge.

Verdict: accept, this RESULT being the reset anchor under the record's redesign_source.
