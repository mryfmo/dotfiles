---
reviewed_at: 2026-10-10T21:44:02Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@b2bfad90d1e1d3b8210b40321f6d23cfdab7c4e5b27e8d644b02a8fea9d535d2
task: dotfiles-T128-task-review-v1-v2-a01
round: 2
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01.md
files:
  - dotfiles-T128-v1-task-schema-a01@49640e9008f7ae53f97930b408fdcb406698ec4e604cb2daec789a724e12431b
  - dotfiles-T128-v1b-pr-caps-a01@0488394c405ea0c5ef10faa904e0775f31538810dd4588367ddcbc699afd461e
  - dotfiles-T128-v2-audit-schema-and-runner-a01@377c67298f0dcb1138d92baad483ecca51efaa08bdbfd86240bfb57a2f434201
verdicts:
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
---

# Task-file review round 2: T128 V1, V1b, V2 (confirmation)

Diff check of the three files at the hashes above against the thirteen round-1 items. Mechanical check with PyYAML: each file's single invariant sentence equals the design's byte for byte (INV-1, INV-2, INV-5), its key equals the design's implementing_tasks entry, and design_review.receipt names the round-3 receipt in all three. Re-ran the premises that changed: V1b premise 2 prints 1; V1's fnmatch premise prints True; V2 premise 3's command prints four grep lines (28, 29, 32, 608) and the count 3.

## V1 (dotfiles-T128-v1-task-schema-a01): ready

- V1-1: premise added (lines 36-38) with the ModuleNotFoundError output; the test module drives the validator as a subprocess under uv run --no-project --with jsonschema --with pyyaml and imports only the stdlib module (line 65); Makefile stays forbidden.
- V1-2: implementing_tasks is an object of task id to arrays of INV ids (line 59); continuation_of and superseded_by are gone.
- V1-3: INV-1 verbatim (line 22); receipt round 3 (line 7).
- V1-4: DESIGN_TIER gains .github/workflows/**, scripts/regime-check.sh, scripts/pr-caps.sh, schemas/** (line 60).
- V1-5: precedence design, review, docs; README.md in REVIEW_TIER_FILES; kind: design is design; review or docs without allowed_files is docs; fnmatch premise (lines 39-41); the two new tier_of test cases (line 65).

## V1b (dotfiles-T128-v1b-pr-caps-a01): ready

- V1b-1: the file count excludes .orchestration/ and counts tests/; the added-line count excludes tests/, .orchestration/ and the data list (line 31). Note for the orchestrator: section 7 of the design still words the cap as "outside tests/ and .orchestration/"; align it with this reading (file count excludes .orchestration/ only) outside the hash.
- V1b-2: the premise command now prints 1 (line 21; re-run).
- V1b-3: receipt round 3; set equality without the one-invariant clause; fail-closed message when the design is absent from main; the thin-caller sentence (line 32).

## V2 (dotfiles-T128-v2-audit-schema-and-runner-a01): ready

- V2-1: three output files, transcript through tee, .last.md rendered from the JSON, the JSON beside them (line 50); premise lines 26-28.
- V2-2: join, send, leave inside one run (line 50); premise lines 29-31 match check-regime-boundary.sh:102; the fakes in the tests capture all three (line 54).
- V2-3: budget from process_tiers.<tier>.audit_budget_usd when present, else 5; clean means no tracked change (line 50).
- V2-4: INV-5 verbatim (line 18); receipt round 3 (line 7).
- V2-5: schema checks through the runner or a uv subprocess (line 54).
- The herdr-agents drift and the SKILL update-branch note are recorded (line 39).

Note, not a revise item: the pasted outputs of V2 premises 2 and 3 (lines 25, 28) are descriptions of what the commands show rather than the commands' verbatim output (premise 3's command prints four grep lines and the number 3); the claims hold as I re-ran them. INV-4 asks for pasted output, and the validator V1 builds cannot tell a paraphrase from output, so the habit is worth keeping exact.

Nothing new in the three files contradicts the design.
