---
format: 2
task_id: dotfiles-T128-gate-evidence-redesign-a02
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-gate-evidence-redesign-a02 — write the successor task file `dotfiles-T128-gate-evidence-a03` (plan 011 option F, the operator's choice)

Drafted 2026-10-12 by the orchestrator seat. On PR #329 the Codex Bot's four rounds all found edges of the gate's prose parsing of the acceptance record; round 4 on the merge head `4e2266aa` left 4249544748 (P1: a finding line that quotes `not-applicable:` is taken as its disposition), 4249544762 (P1: the record is not bound to the head) and 4249544794 (P2: quadratic regex). `acceptance-dispositions` reached three, the second class at three on T702 (after `search-command-scan`), so plan 007 S7 stopped the orchestrator; the operator chose plan 011 option F: the acceptance record's machine-read parts become a YAML front matter the gate loads with PyYAML and checks field by field (M-20261012-22, C-24). The change is task text, so a02 is withdrawn (INV-6 pre-empted) and the redesign is yours. The worker `claude-standard-dot-a002` holds at `61d90302` (merge head `4e2266aa`) and continues under a03 on PR #329.

## Inputs

- `.orchestration/tasks/dotfiles-T128-gate-evidence-a02.md` (amendment 1, sha `241aec12…`), the three threads (`gh api repos/mryfmo/dotfiles/pulls/329/comments --jq '.[]|select(.id==4249544748 or .id==4249544762 or .id==4249544794)|.body'`; quoted in M-20261012-22), C-24, plan 011, the design on `main` (INV-1 "jsonschema + PyYAML, no hand-written parser"; INV-6's clause; INV-12's enforcement row), the worker's report `.orchestration/reports/dotfiles-T128-gate-evidence-a02.md` (what the gate reads today), and an existing acceptance record for shape (`.orchestration/acceptance/dotfiles-T128-process-rules-a07.md`).

## What the successor says (everything else verbatim from a02 amendment 1)

1. Front matter: `task_id: dotfiles-T128-gate-evidence-a03`, `reset_of: [dotfiles-T128-gate-evidence-a01, dotfiles-T128-gate-evidence-a02]`, the a03 evidence directory in `allowed_files` (a02's no longer), copy rows for the a01 to a03 task copies (C3), `design_review.receipt` round 22, `invariants.INV-6` unchanged. Note for the design: `main` maps a01 and a02; a03 needs its own `implementing_tasks` entry (a design round after this redesign, as round 24 did for a02); say so in the intro.
2. Item 2 is replaced by the acceptance-record contract. The record the gate reads (`ACCEPTANCE_EVIDENCE`, required in PR mode, under `.orchestration/acceptance/<task id>.md`) starts with a YAML front matter the gate loads with `yaml.safe_load` and validates field by field (no regex over prose anywhere in the gate): `format: 1`; `task` equal to the task id the file name carries; `head` equal to the full `HEAD` sha the gate runs at (a stale record is refused with `acceptance record head <x> is not HEAD <y>`); `pr`; `ledger`: a list of `{id, class}` rows where `id` is a thread id or `audit:<sha7>:<n>` and `class` matches `^[a-z0-9-]+$`; `searches`: for every class with three or more ledger rows one `{class, records}` entry whose `records` list equals, as a set, the file basenames the gate itself finds with `grep -rl 'classes:.*<class>' .orchestration/learning/mistakes/` run without a shell from the repository root (`records: []` when none), otherwise refused with `S6: class <slug> at <n> without a matching records search`; `audit_findings`: when the audit verdict is `incorrect`, one `{n, reason, evidence}` entry per finding 1..N (each a non-empty string; a `fixed:` is not accepted here because a fix moves HEAD, as today). The prose after the front matter is for people and is not read. `AUDIT_DISPOSITIONS` is retired in favour of `audit_findings`; the Makefile and README name `ACCEPTANCE_EVIDENCE` in its place.
3. Item 1 (the sweep JSON's dispositions) stays, with its grammar implemented as one split on the first `; evidence=` and two non-empty parts (linear; no backtracking regex), a second delimiter refused.
4. Item 3's fixtures become YAML front matters: a record with a stale `head` (refused), a record missing a `searches` entry for a class at three (refused), a record whose `records` set matches (accepted), a finding entry whose `reason` quotes the grammar text (accepted, because it is a field, not a substring: the 4249544748 case), and the two disposition cases of a02.
5. Item 5 gains: "the three round-4 threads become `fixed:<sha>` through this contract: 4249544748 (fields, not substrings), 4249544762 (`head` equals `HEAD`), 4249544794 (one split, linear checks)".
6. The heading carries the reset; the intro names the two S1 cycles, plan 011 option F, the a02 heads `d5d6c9b1`, `61d90302`, `4e2266aa`, and the design-round note; the worker's commits stay; one Completion clause (PR #329 stays).
7. Nothing else changes: not item 4 (unchanged Makefile/README naming except `AUDIT_DISPOSITIONS` → `ACCEPTANCE_EVIDENCE`), not the premises (re-paste premise 3 from `/usr/bin/awk` at `origin/main` `e0e2fe62`, per C-18).

## Stop condition

`task-consistency-check.py` C1 to C9 pass on a03 (state what you re-derived: the three copy rows, C7, C8 for `ACCEPTANCE_EVIDENCE` and the retired `AUDIT_DISPOSITIONS`, C9); the differences from a02 amendment 1 are exactly items 1 to 6; the contract names every field the gate reads and no prose the gate reads; `invariants.INV-6` byte-equal to the design.

## Output

Write `.orchestration/tasks/dotfiles-T128-gate-evidence-a03.md` and the receipt `.orchestration/validation/dotfiles-T128-gate-evidence-redesign-a02.md` (header; diff summary; checks; the successor's sha256), then `AGMSG-RESULT v1 task_id=dotfiles-T128-gate-evidence-redesign-a02 status=ready_for_review verdict=accept design_sha256=<sha256 of the a03 file> receipt=<path> receipt_sha256=<sha256>` via `agmsg-dispatch dotfiles-conformance claude-review-dot-a001 claude-deep-dot w5:p1`. max_turns=3. Forbidden: editing any other tracked file; branches; PRs.
