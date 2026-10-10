---
reviewed_at: 2026-10-10T23:31:45Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@15daca85205c6ac50bc620965a3ee3a208bd0a2436454784dad4ba55e53d01d9
task: dotfiles-T128-task-review-v1-v2-a01
round: 16
previous: .orchestration/validation/dotfiles-T128-task-review-v1-v2-a01-round15.md
files:
  - dotfiles-T128-v0-main-tests-a01@89b101c155e7614e (prefix; full hash in the TASK line)
  - dotfiles-T128-v1-task-schema-a01@e5474a80d5e2fcbc
  - dotfiles-T128-v1b-pr-caps-a01@b30aa981aa05d856
verdicts:
  dotfiles-T128-v0-main-tests-a01: "revise: R16-1 the declared-module check (b0) as worded fails V1's own PR"
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
---

# Task-file review round 16: Bot findings on boundary head 3396d666 in V0, V1, V1b

Design unchanged at 15daca85; the three invariants byte-identical; pointers at round 13. Bot threads not read from this seat.

## V0: revise

- Applied and sound: the trigger list now covers every design-tier script path (scripts/**, home/dot_local/bin/**, install/**, home/.chezmoiscripts/**, setup.sh); the job runs main's copy of the harness through git show origin/main:… with a stated one-time fallback on this first PR; the harness files and the job join the operator-routed gate sources; tests (e) and (f) are added; scripts/lib/contract_markers.py is in allowed_files.
- R16-1: step (b0) says "every declared script path must map to a declared tests/unit/*.py module (the task lists both)" without saying what maps. Read by name, V1's own task declares scripts/validate-task.py, scripts/lib/high_risk_paths.py and scripts/legacy-task-ids.txt with the single module tests/unit/test_validate_task.py, so (b0) fails V1 on high_risk_paths.py and on a data file under scripts/; round 11 dropped the stem mapping for this reason. Right: (b0) requires that a design-tier task.md whose allowed_files contain at least one script path also lists at least one tests/unit/*.py module (the modules it lists are the contracts run in (b)), and a path is a script path only when it matches the trigger list and is not a data file (scripts/legacy-task-ids.txt is the one today; name it, or exclude .txt). Test (f)'s fixture then declares a script and no module.

## V1: ready

Wildcard entries are classified in both directions (install/foo* under install/**), with home/.chezmoiscripts/run_* among the test cases; the rest is unchanged since round 13.

## V1b: ready

A -contract-a01 id is looked up under its implementing id with the suffix stripped, consistent with the design's <task>-contract-a01 form (the task id followed by the suffix, which still matches the task-id pattern) and with V0's promotion check keyed on the same suffix; the fixture is added.
