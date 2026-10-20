---
task: dotfiles-T133-result-precheck-a03
head: bccb2deabdf95bc558add6a5e56e4405a6a61b43
pr: 411
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T21:50:24Z
finished: 2026-10-18T21:57:37Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P2] Bind regression proofs to the requested previous head — scripts/orchestrator/dispatch.sh:177-177
- [P2] Match the requested regression method exactly — scripts/orchestrator/result-precheck.sh:241-242
- [P2] Stop when the clean-tree query fails — scripts/orchestrator/result-precheck.sh:187-187

```text
The clean-tree guard can fail open, and regression evidence can be accepted for the wrong baseline or test. Read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P2] Stop when the clean-tree query fails — scripts/orchestrator/result-precheck.sh:187-187
  If `git status` fails, its exit status is discarded by the process substitution, so the loop reads no entries and the precheck continues. For example, an invalid `status.relativePaths` configuration breaks this query while other Git commands still succeed. Checks can therefore run against uncommitted files while recording HEAD as the tested code. Capture and validate the query before processing its output, and cover this failure in the closed prerequisite-failure regression ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Bind regression proofs to the requested previous head — scripts/orchestrator/dispatch.sh:177-177
  When a later revision changes `previous_head=` but requests the same selectors, a new RESULT can reuse proofs from the old baseline: this block reads only `check=`, and `precheck.json` never records the baseline SHA. I confirmed that the gate accepts the existing proofs when the requested previous head is changed to the already-green code commit. Record the tested baseline in the evidence and require it to match the latest revision request.

- [P2] Match the requested regression method exactly — scripts/orchestrator/result-precheck.sh:241-242
  Unittest's `-k` performs substring matching, not exact method selection. If a module contains `test_a` and `test_a_regression`, requesting `::test_a` runs both; a failure only in `test_a_regression` supplies an accepted red proof even though `test_a` passes on both heads. It can likewise accept a nonexistent selector that matches another test's name. Use an exact test ID or an anchored method-name pattern.
The clean-tree guard can fail open, and regression evidence can be accepted for the wrong baseline or test. Read-only probes confirmed these issues; the full test suite was not run.

Full review comments:

- [P2] Stop when the clean-tree query fails — scripts/orchestrator/result-precheck.sh:187-187
  If `git status` fails, its exit status is discarded by the process substitution, so the loop reads no entries and the precheck continues. For example, an invalid `status.relativePaths` configuration breaks this query while other Git commands still succeed. Checks can therefore run against uncommitted files while recording HEAD as the tested code. Capture and validate the query before processing its output, and cover this failure in the closed prerequisite-failure regression ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Bind regression proofs to the requested previous head — scripts/orchestrator/dispatch.sh:177-177
  When a later revision changes `previous_head=` but requests the same selectors, a new RESULT can reuse proofs from the old baseline: this block reads only `check=`, and `precheck.json` never records the baseline SHA. I confirmed that the gate accepts the existing proofs when the requested previous head is changed to the already-green code commit. Record the tested baseline in the evidence and require it to match the latest revision request.

- [P2] Match the requested regression method exactly — scripts/orchestrator/result-precheck.sh:241-242
  Unittest's `-k` performs substring matching, not exact method selection. If a module contains `test_a` and `test_a_regression`, requesting `::test_a` runs both; a failure only in `test_a_regression` supplies an accepted red proof even though `test_a` passes on both heads. It can likewise accept a nonexistent selector that matches another test's name. Use an exact test ID or an anchored method-name pattern.
```
