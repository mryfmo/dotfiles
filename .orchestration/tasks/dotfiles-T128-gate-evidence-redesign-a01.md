---
format: 2
task_id: dotfiles-T128-gate-evidence-redesign-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-gate-evidence-redesign-a01 — write the successor task file `dotfiles-T128-gate-evidence-a02` (INV-6 reset of T702: a missing threat row would be amendment 2)

Drafted 2026-10-12 by the orchestrator seat. The Codex Bot's round 1 on PR #329 (head `5971fffe`, review 5491066199) raised six findings; four are the worker's in-lane fixes (held uncommitted), one is a disposition (4248232955: SKILL step 10.4 lacks `ACCEPTANCE_EVIDENCE`; owned by `dotfiles-T128-playbook-rules-a02` item 6, PR #328 merges before #329), and one, 4248232976, is a missing threat row for the gate's new input `ACCEPTANCE_EVIDENCE`. A missing row is added once, counted as an amendment (SKILL threat-table bullet); amendment 1 was spent on the row split and the search grammar, so this amendment would be INV-6's count. `dotfiles-T128-gate-evidence-a01` is withdrawn (ACCEPTANCE 13:0xZ) and the redesign is yours. The worker `claude-standard-dot-a002` continues under the successor on the same branch and PR.

## Inputs

- `.orchestration/tasks/dotfiles-T128-gate-evidence-a01.md` (amendment 1, sha256 `d1b6fcf3…`), its acceptance record, the worker's question PONG (message 725, 13:00:25Z), the six Bot threads on PR #329 (4248232955, 4248232964, 4248232976, 4248232988, 4248232998, 4248233012), the sibling successor `.orchestration/tasks/dotfiles-T128-playbook-rules-a02.md` (its item 3 search form: `grep -rl 'classes:.*<slug>' .orchestration/learning/mistakes/`), plan 007 Phase 0, and the design v20 on `main` (INV-6's clause; `main` is `4cf1d4e2`).

## What the successor says (everything else verbatim from a01 amendment 1)

1. Front matter: `task_id: dotfiles-T128-gate-evidence-a02`, `reset_of: [dotfiles-T128-gate-evidence-a01]`, the a02 evidence directory in `allowed_files` (the a01 directory no longer), copy rows for the a01 and a02 task copies (C3), `design_review.receipt` round 22, the `invariants.INV-6` line unchanged (byte-equal to the design).
2. One new threat row (thread 4248232976): control `the ACCEPTANCE_EVIDENCE input: the acceptance record's path and content (ledger rows, search: lines, audit-finding: lines), written by the orchestrator and read by the gate`, disposition `closed: tests/unit/test_require_crit_review.py::test_base_requires_an_acceptance_record_under_acceptance` (the worker's proposed test name; the test asserts the path check under `.orchestration/acceptance/` and the refusal without it).
3. Item 2's `search:` line grammar (thread 4248233012): the line names the class slug, a `grep` with `classes:` over `.orchestration/learning/mistakes/` in either form (`grep -rl … .orchestration/learning/mistakes/` as the SKILL writes it in `dotfiles-T128-playbook-rules-a02` item 3, or `grep -l … .orchestration/learning/mistakes/*.md`), and `contextdb_cli.py memory search`; the fixtures use the SKILL's form.
4. Item 5 gains the disposition sentence for 4248232955: the SKILL step 10.4 sentence is `dotfiles-T128-playbook-rules-a02`'s (item 6); PR #328 merges before #329; the RESULT proposes `not-applicable: owned by dotfiles-T128-playbook-rules-a02 item 6; evidence=grep -n 'ACCEPTANCE_EVIDENCE' .orchestration/tasks/dotfiles-T128-playbook-rules-a02.md`.
5. The heading carries the reset; the intro names the question, the Bot round and the a01 head `5971fffe`; the worker's prepared fixes (4248232964, 4248232988, 4248232998, 4248233012) are kept as the worker made them.
6. Nothing else changes: not items 1, 3, 4, not the other premises (re-paste premise 3's awk output from `/usr/bin/awk` at `origin/main` `4cf1d4e2`, per C-18).

## Stop condition

`task-consistency-check.py` C1 to C7 pass on the successor (state what you re-derived: C3's two copy rows, C4 for every allowed path, C7's eight names, and the ninth row of item 2); the differences from a01 amendment 1 are exactly items 1 to 5; `invariants.INV-6` byte-equal to the design.

## Output

Write `.orchestration/tasks/dotfiles-T128-gate-evidence-a02.md` (through the permission gate, the main checkout) and the receipt `.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a01.md` (header; diff summary; checks; the successor's sha256), then `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-redesign-a01 status=ready_for_review verdict=accept design_sha256=<sha256 of the a02 file> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing any other tracked file; branches; PRs.
