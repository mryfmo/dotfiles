---
format: 2
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/chain-integrate.sh
  - scripts/require-crit-review.py
  - scripts/regime-counters.sh
  - scripts/orchestrator/acceptance-front-matter.py
  - tests/unit/test_chain_glue.py
  - tests/unit/test_require_crit_review.py
  - tests/unit/test_regime_counters.py
  - tests/unit/test_orchestrator_tools.py
  - scripts/orchestrator/ledger-check.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/**
after: []
threat_table:
  - control: "the PR edits scripts/orchestrator/chain-integrate.sh for the re-plan's item R1 (the inheritance of an update-branch-only head also requires git merge-tree --write-tree head^1 head^2 to equal head's tree, so a merge carrying any PR-side edit gets a fresh audit) and the owned rows (item 1)"
    disposition: "closed: tests/unit/test_chain_glue.py::test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree"
  - control: the PR edits scripts/require-crit-review.py only within the owned rows (item 1)
    disposition: "residual: the gate is a trust boundary; an owned row's fix never widens what the gate accepts without a test that refuses the wider form; the audit reads each case"
  - control: the PR edits scripts/regime-counters.sh only within the owned rows (item 1)
    disposition: "residual: as above; the audit reads each case"
  - control: the PR edits scripts/orchestrator/acceptance-front-matter.py only within the owned rows (item 1)
    disposition: "residual: as above; the writer's exact-key rule is never weakened"
  - control: the PR edits tests/unit/test_chain_glue.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_require_crit_review.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_regime_counters.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: the PR edits tests/unit/test_orchestrator_tools.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after"
  - control: "the PR edits scripts/orchestrator/ledger-check.py for the re-plan's item R2 (an audit summary whose first line is inherited-from: <sha7> yields ids audit:<that sha7>:<n>, never ids named for the file; nothing else changes)"
    disposition: "closed: tests/unit/test_task_checkers.py::test_ledger_check_reads_inherited_audit_ids_from_the_marker"
  - control: "tests/unit/test_task_checkers.py (the one fixture of item R2, red before and green after)"
    disposition: "residual: fixtures in a temporary directory; the audit reads the case"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the scripts as subprocesses on fixtures in a temporary directory with stub gh and real git in a temporary repository; nothing touches a live PR"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the scripts run under the repository's python and bash as today"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to the files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the local review of PR #390's head 741e242 recorded the P1 this re-plan fixes
    command: /usr/bin/grep -c '\[P1\] Verify merge content before inheriting the parent audit' .orchestration/validation/dotfiles-T129-audit-inherit-replan-json-a01-local-review-741e242.md
    output: |-
      3
  - claim: the installed git has merge-tree --write-tree (git 2.38 or later)
    command: git --version
    output: |-
      git version 2.56.0
  - claim: on the real update-branch head 741e242 the merge-tree reproduction equals the head's tree, so the new condition keeps inheriting the honest case
    command: git merge-tree --write-tree 741e24272fd64b6a36c0d6725c53265de1c94982^1 741e24272fd64b6a36c0d6725c53265de1c94982^2; git rev-parse '741e24272fd64b6a36c0d6725c53265de1c94982^{tree}'
    output: |-
      7a47cd7484696faf42121437239b0bc1bdba6ca0
      7a47cd7484696faf42121437239b0bc1bdba6ca0
---

# AGMSG-TASK dotfiles-T129-audit-inherit-replan-json-followup-a01 — the F1 lineage's owner task (advisory P2 of PR #390)

Written 2026-10-17 by the orchestrator seat before PR #390's integration chain (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a01` in `.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-a01.md` (plan 020 step 1.2); it is dispatched after PR #390 merges, to a seat the orchestrator names then, only if rows exist.

## Goal

Every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The owned rows at dispatch: none at the time of writing (PR #390's two Bot findings were fixed in its rounds); rows added by the audit or a later review are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row.

## Check

`uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py -v` green pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 200 changed lines outside `tests/` and `.orchestration/`, 1000 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main` after PR #390 merges. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-audit-inherit-replan-json-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md>` in the RESULT.

## Checks (pasted by the orchestrator before each send)

```
(pending: pasted at dispatch)
```

## Re-plan (2026-10-18T04:58Z): this task supersedes PR #390

PR #390 (F1, head 741e242, the update-branch merge of the accepted e0ed65d0) is held unmerged: its integration chain's local review found `[P1] Verify merge content before inheriting the parent audit` (chain-integrate.sh:181-188: `git patch-id --verbatim` discards hunk positions, so a merge that relocates an edit between repeated-context blocks keeps the parent's patch-id and inherits an audit of different behaviour; class `unbound-evidence`) and `[P2] Update the pre-audit ledger reader for inherited audit IDs` (the row above). The a01 task has used its one revise round (INV-6: revise < 2), so under plan 020 S1's spirit and the user's autonomy directive of 2026-10-18 13:5x JST the fix is this re-plan, not a third round. Seat: codex-standard-dot-a010 (worker-e), after its P1-7 RESULT. Routing: orchestrator scripts, not a seat's execution boundary.

- Branch: `git fetch origin tools/audit-inherit-replan-json && git switch -c tools/audit-inherit-replan-json-followup-a01 741e24272fd64b6a36c0d6725c53265de1c94982` (stacked on #390's head, so the PR's diff against main is the whole F1 change plus this re-plan, and the task-level audit covers F1 for the first time; #390 had none). PR base `main`; when it merges the orchestrator closes #390 as superseded.
- R1 (the P1): in `chain-integrate.sh`'s inheritance condition, in addition to the patch-id equality, require `"${git}" -C "${main}" merge-tree --write-tree "${head}^1" "${head}^2"` to print exactly `"${git}" -C "${main}" rev-parse "${head}^{tree}"` (a clean automatic merge reproduces the head's tree; any conflict resolution or extra PR-side edit does not, and the head gets a fresh audit). A merge-tree exit other than 0 (a conflict) is a fresh audit too. Test `test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree` in `tests/unit/test_chain_glue.py`: a temporary repository where (a) a clean `git merge main` into the audited head inherits, (b) a merge commit whose tree carries one extra PR-side line (same patch-id made by relocating a hunk, or any added line) does not inherit and the fresh audit path runs (asserted from the fake orch-audit.sh's recorded argv); red before the fix on case (b).
- R2 (the P2, the owned row `local:741e242:2`): `scripts/orchestrator/ledger-check.py` derives an audit summary's ids from its `inherited-from: <sha7>` first line when present (`audit:<that sha7>:<n>`), else from the file name as today; test `test_ledger_check_reads_inherited_audit_ids_from_the_marker` in `tests/unit/test_task_checkers.py`: an inherited summary with one `[P1]` line demands `audit:<parent sha7>:1` and accepts a record holding that row; red before.
- Item 1's other owned rows: none besides `local:741e242:2` at this writing (the record's `## Owned by` section); the owned-rows wording above stays for rows the orchestrator adds before dispatch.
- Check: the a01 task's Check applies plus `uv run python -m unittest tests.unit.test_chain_glue tests.unit.test_task_checkers tests.unit.test_orchestrator_tools -v` green and `git diff --numstat 741e24272fd64b6a36c0d6725c53265de1c94982...HEAD`: at most 60 changed lines outside `tests/` and `.orchestration/`, 120 under `tests/` (paste both this range and `origin/main...HEAD`).
- Completion: the Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-audit-inherit-replan-json-followup-a02` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md>` in the RESULT; a Codex seat writes its evidence at the same relative paths in its worktree and says so. `security: true`: the gate and the chain are trust boundaries; the orchestrator runs the task-level audit and the security-profile review on the final head.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-audit-inherit-replan-json-followup-a01.md: OK
premises 1 to 3: outputs pasted at write time (2026-10-18 14:0x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
```
