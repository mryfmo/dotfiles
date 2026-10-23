---
format: 2
task_id: dotfiles-T128-chain-glue-finish-a02
reset_of: [dotfiles-T128-chain-glue-finish-a01]
retained_predecessor_directories: [.orchestration/dotfiles-T128-chain-glue-finish-a01/]
kind: code
security: false
allowed_files:
  - scripts/orchestrator/chain-finish.sh
  - tests/unit/test_chain_glue.py
  - .orchestration/dotfiles-T128-chain-glue-finish-a02/**
after: []
threat_table:
  - {control: "scripts/orchestrator/chain-finish.sh", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_shim_exclusion_compares_the_resolved_path"}
  - {control: "tests/unit/test_chain_glue.py", disposition: "residual: the fixture plants a symlinked shim and a real binary in temporary directories; final-head CI and the task-level audit verify the assertion; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "the task-file copy (.orchestration/dotfiles-T128-chain-glue-finish-a02/task.md); predecessor .orchestration/dotfiles-T128-chain-glue-finish-a01/task.md is inherited read-only", disposition: "residual: byte-identical to the dispatched text; the orchestrator compares its SHA256 with the TASK line at acceptance; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "task metadata (kind, security, allowed_files, after, reset_of, threat_table, premises)", disposition: "residual: the consistency checker parses the mapping before dispatch and at acceptance; byte comparison of the task copy covers changes; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "metadata separators (the --- boundaries in the task copy and evidence records)", disposition: "residual: front matter stays YAML; the checker parses the task and byte comparison covers the whole dispatched file; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "in-process effects (the two rewritten tests run no new command beyond the normaliser)", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_shim_exclusion_compares_the_resolved_path"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow, interpreter, launcher or dependency change; the normaliser is the system realpath on the fixed PATH the script already uses; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "new or renamed scripts", disposition: "residual: none; only chain-finish.sh changes in place; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "orchestrator effect merge", disposition: "residual: only the orchestrator merges the audited head with --match-head-commit after sweep, audit and gate; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "orchestrator effect update-branch", disposition: "residual: a moved head gets fresh CI, sweep, audit and gate before the merge; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; any discarded state is recorded at acceptance; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "orchestrator effect task copy", disposition: "residual: the a02 copy is compared byte-for-byte and by SHA256 with the dispatched text at acceptance; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "orchestrator effect records", disposition: "residual: the orchestrator owns acceptance, feedback dispositions and the reset record; the worker supplies evidence only; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "the evidence records under .orchestration/dotfiles-T128-chain-glue-finish-a02/**", disposition: "residual: command output and learning triage; sandbox.md lists refused commands; the audit checks claims against the final head; owner: dotfiles-T128-chain-glue-finish-followup-a01"}
  - {control: "path comparison form (the two [[ ]] tests at chain-finish.sh:67 and :111)", disposition: "closed: tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline"}
premises: []
---

# AGMSG-TASK dotfiles-T128-chain-glue-finish-a02 — chain-finish.sh compares paths in the lint's normalised form (reset of a01)

Written 2026-10-21T09:57Z by the orchestrator seat. PR #378 (`dotfiles-T128-chain-glue-finish-a01`, five worker rounds, last round 2026-10-17) was update-branched to `b09c88c6deaed78ca7c06bfb314cd52bff1123e8` after records boundary 27 and the pins merge; its required unit-test jobs now fail on `tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_the_changed_files_are_clean_against_the_baseline`, because the comparison lint merged on main after round 5 flags two lines of the PR's own file (R1: a path operand compared by its string form): `scripts/orchestrator/chain-finish.sh:67` and `:111`, both `[[ ${found} == /* && ${found} != */shims/* ]]`. The mechanism-PR two-round limit forbids a sixth worker round (D-024-63), so this reset text, by another context than a002/a006, carries exactly that conformance fix. The PR's own module `tests.unit.test_chain_glue` passes at `b09c88c6deaed78ca7c06bfb314cd52bff1123e8` (27 tests, orchestrator run). Design: `.orchestration/tasks/dotfiles-T128-regime-v3-a01.md` by reference, unchanged.

## Item 1

Continue PR #378 on branch `tools/chain-glue-finish` from `b09c88c6deaed78ca7c06bfb314cd52bff1123e8`; keep every a01 commit and artifact; add no file outside the three allowed entries.

Rewrite the two tests at `chain-finish.sh:67` and `:111` so the statement normalises the operand it compares, in the form the lint accepts (a normaliser such as `realpath --` inside the same statement, never the `# lint-comparisons: allow` marker): the refusal "no binary outside a shims directory" compares the resolved path of `${found}` (a symlinked shim resolves to its target directory, which is the intent of the exclusion) and keeps refusing a relative or empty `${found}`. The two refusal messages, exit codes and every other line stay byte-identical.

## Item 2

Add `ChainIntegrateTest::test_shim_exclusion_compares_the_resolved_path` to `tests/unit/test_chain_glue.py`: with temporary directories, a symlink under a `shims/` directory that resolves outside it is refused with exit 10, and a real binary outside any `shims/` directory is accepted; red at `b09c88c6deaed78ca7c06bfb314cd52bff1123e8` on the behavioural assertion, green at the fix commit. The lint test is the second red-then-green: `python -I scripts/lint-comparisons.py --changed scripts/orchestrator/chain-finish.sh` exits 1 at `b09c88c6deaed78ca7c06bfb314cd52bff1123e8` and 0 after the fix; paste both outputs.

## Check

Run `bash -n scripts/orchestrator/chain-finish.sh`, `shellcheck scripts/orchestrator/chain-finish.sh`, `python -m unittest tests.unit.test_chain_glue tests.unit.test_lint_comparisons -v` and `ruff check tests/unit/test_chain_glue.py`; English shdoc comments; never run Bats locally.
Caps: at most 200 changed lines outside `tests/` and `.orchestration/` and at most 320 under `tests/`, measured as additions plus deletions with `git diff --numstat <merge-base> <head>` over the whole PR (C-123; the regime verifier measures the same way; the inherited a01 lines were 178/275 at dispatch); this reset's own commits add at most 40 outside `tests/` and 120 under `tests/` of those.
Worker Playbook step 4: every command sandboxed; push without `-u`: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git tools/chain-glue-finish`; on any denial send `AGMSG-PONG v1 task_id=dotfiles-T128-chain-glue-finish-a02 status=blocked` with the exact command and boundary.
Each evidence item names its producer (worker, Claude seat, or orchestrator, Claude seat, sandboxed Bash). Keep this text at or under 110 lines including the Checks block below; the orchestrator pastes Checks before the anchor review and dispatches the anchored bytes unchanged.

## Completion

Write `.orchestration/dotfiles-T128-chain-glue-finish-a02/`: task.md byte-identical to the dispatched text, report.md, validation.md (every command, status and verbatim redacted output, both red-then-green pairs with commit shas), sandbox.md, learning.md, autoskill.md, result.txt (`task_copy=<sha256 of task.md>`, `head=<40-hex>` literal). Rewrite PR #378's English description to the final design and counts. After the push wait for required CI; at most one worker Bot fix-round. Then send `AGMSG-RESULT v1 task_id=dotfiles-T128-chain-glue-finish-a02 status=ready_for_review` with pr, head, merge_base, changed_non_tests, changed_tests, the two red/green sha pairs, task_copy and the artifact paths. No merge, no thread resolution, no acceptance.

## Amendment 1 (2026-10-21T21:17Z)

The test module's class is `ChainIntegrateTest`, not `ChainGlueTest`; the three selector references above now name `ChainIntegrateTest::test_shim_exclusion_compares_the_resolved_path` (the worker's RESULT 2999 note). Nothing else changes; the records-only round updates `task.md` and `result.txt`'s `task_copy=` to these bytes.

## Amendment 2 (2026-10-21T21:40Z)

The cap sentence now states the PR-wide caps the regime verifier measures from the merge-base (200/320; the a01 lineage's cap was 200 outside), with this reset's own 40/120 as a sub-limit; amendment 1's 40/120 "for this reset's own commits" was refused by the verifier at 111cbe61 as 178/290 exceeding 40/120. Records-only round: task.md and result.txt's task_copy= to these bytes.

## Checks

```text
canonical main (gh api repos/mryfmo/dotfiles/branches/main --hostname github.com --jq .commit.sha): 4eafd890454e495fdb1d429734c5835e46c87652; PR #378 head at dispatch: b09c88c6deaed78ca7c06bfb314cd52bff1123e8; merge-base: 4eafd890454e495fdb1d429734c5835e46c87652
inherited lines of the whole PR from the merge-base (git diff --numstat, additions plus deletions, outside tests/ and .orchestration/ / under tests/): 178/275; the PR's own module tests.unit.test_chain_glue: 27 tests OK at that head (orchestrator, sandboxed, 92 s)
CI job 119152960907 (ubuntu-24.04 client) at that head: FAILED (failures=1) on test_the_changed_files_are_clean_against_the_baseline with stdout "scripts/orchestrator/chain-finish.sh:67: R1 shell [[ ]] or [ ] compares a path or URL operand by its string form" and the same for :111
observed 2026-10-21T09:57Z by the orchestrator (Claude seat, sandboxed Bash); every value is pasted command output
```
