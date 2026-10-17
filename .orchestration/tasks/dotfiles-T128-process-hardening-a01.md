---
format: 2
task_id: dotfiles-T128-process-hardening-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/regime-counters.sh
  - scripts/orchestrator/chain-integrate.sh
  - tests/unit/test_regime_counters.py
  - tests/unit/test_chain_glue.py
  - .orchestration/dotfiles-T128-process-hardening-a01/**
after: []
threat_table:
  - control: the PR edits scripts/regime-counters.sh in two places (the revise count becomes the count of status=revise ACCEPTANCE lines, so a round before the first RESULT counts; an S1 watch line at a class's second row)
    disposition: "closed: tests/unit/test_regime_counters.py::RegimeCountersTest::test_revises_count_every_revise_acceptance_line_and_a_class_at_two_rows_prints_the_watch"
  - control: the PR edits scripts/orchestrator/chain-integrate.sh in one place (the audit step inherits the previous head's receipt when the head is an update-branch merge whose PR diff is unchanged by patch-id)
    disposition: "closed: tests/unit/test_chain_glue.py::test_integrate_inherits_the_audit_across_an_update_branch_only_head"
  - control: the PR edits tests/unit/test_regime_counters.py only for the new case beside the existing ones
    disposition: "residual: one new test beside the existing ones, which stay with their values: revises is the larger of RESULTs minus one and the revise ACCEPTANCE lines, so a fixture without revise lines keeps RESULTs minus one, and T118's authored fixture (20 revise lines, 9 RESULTs) now asserts 20, which item 4 names"
  - control: the PR edits tests/unit/test_chain_glue.py only for the new case beside the existing ones
    disposition: "residual: one new test beside the existing ones, which stay; the module's stub scripts (its stub orch-audit.sh records its calls) and real git in a temporary repository as today"
  - control: "the audit receipt as an input of chain-integrate.sh's inheritance (the previous head's .last.md copied to the new head's names)"
    disposition: "residual: the copy happens only when git says the head's first parent is the audited head, its second parent is on origin/main and the two patch-ids are equal, all computed by git in the main checkout; the copied receipt gets a first line naming its source, so the record and the gate read where the verdict came from; a forged receipt file is the main checkout's own file, outside the PR's control"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-process-hardening-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-process-hardening-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the three scripts as subprocesses with the modules' fixture storage facade, stub gh, stub scripts, stub codex and real git in a temporary repository, and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; regime-counters.sh runs jq, git and gh as today; chain-integrate.sh runs git (rev-parse, merge-base, diff-tree, patch-id) and the main checkout's scripts as today, never the PR head's copies; chain-finish.sh runs the same binaries as today; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the counters on origin/main define revises as RESULTs minus one'
    command: 'git show origin/main:scripts/regime-counters.sh | /usr/bin/grep -c "revises = AGMSG-RESULTs - 1"'
    output: |-
      1
  - claim: 'the chain on origin/main refuses an already audited head and knows no inherited audit'
    command: 'git show origin/main:scripts/orchestrator/chain-integrate.sh | /usr/bin/grep -c "inherited"'
    output: |-
      0
  - claim: 'the audit receipts on origin/main end with one Verdict line (the record verdict line is the audit task''s amendment, pending)'
    command: 'git show origin/main:scripts/orchestrator/orch-audit.sh | /usr/bin/grep -c "Verdict (record)"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-process-hardening-a01 — the six process rules in the orchestrator's tools: counted rounds, inherited audits, the code verdict (C-61, the operator's decision of 2026-10-17)

Written 2026-10-17 by the orchestrator seat after the operator's root-cause analysis of the day's integrations (M-20261017-06, C-61: rounds of one class answered one instance at a time, update-branch heads re-audited in full, record findings stopping merges, fix rounds before the first RESULT uncounted). This is the tools half of the lineage `dotfiles-T128-process-hardening`; the rules half (a02) writes the same rules into the SKILL and the rules files. The new rules apply to this PR itself.

## Goal

`scripts/regime-counters.sh` counts every fix round toward INV-6's cap and warns at a class's second row; `scripts/orchestrator/chain-integrate.sh` inherits an audit across an update-branch-only head.

## Files

1. `scripts/regime-counters.sh`: (a) `revises` becomes the larger of RESULTs minus one (today's value) and the number of `AGMSG-ACCEPTANCE` lines with `status=revise` for the task from the TASK senders (each one a fix round, before or after the first RESULT), read from the same bus facade as the other counts; the header comment states the new definition (C-61 rule 2) and the S2 line keeps its form (`S2: revises <n> >= 2 source=live`); `results` and the other counts are unchanged; the existing tests keep their values except T118's authored fixture (20 revise lines, 9 RESULTs), whose assertion moves to 20. (b) For every non-advisory ledger class at exactly two rows the script prints `S1-watch: class=<slug> count=2 check=string-parse,one-source-one-parser source=record` after the S2 lines and before any S1 line (C-61 rule 5: the orchestrator's cue to check for a string parse and for one data source and one parser); the S1 line at three or more rows is unchanged.
2. `scripts/orchestrator/chain-integrate.sh`: before the audit step, when the head is a merge commit whose first parent is a head with a receipt `.orchestration/validation/<task>-audit-<parent sha7>.md.last.md`, whose second parent is an ancestor of `origin/main`, and whose PR diff is unchanged (`git diff-tree -p <merge-base(origin/main, parent)> <parent> | git patch-id --stable` equals the same for the head), the audit is inherited: both receipt files of the parent are copied to the head's names with a first line `inherited-from: <parent sha7> (update-branch only, C-61 rule 3)` and the step logs `audit inherited from <parent sha7>`; otherwise the audit runs as today. The existing refusal of an already audited head (line 105) stays for a head that already has its own receipt.
3. The split verdict (C-61 rule 4) is produced by the audit task `dotfiles-T128-audit-s1-report-a01` through its amendment 1 (pending): the receipt's final line stays `Verdict: correct|incorrect` and means the code verdict, so `acceptance-front-matter.py`, `require-crit-review.py` and chain-finish.sh (PR #378) read it unchanged, and a line `Verdict (record): correct|incorrect` precedes it; nothing in this task touches those consumers.
4. `tests/unit/test_regime_counters.py`: `test_revises_count_every_revise_acceptance_line_and_a_class_at_two_rows_prints_the_watch`: a bus with one TASK, two `status=revise` ACCEPTANCE lines before the first RESULT and one RESULT gives `revises=2` and the S2 line, a bus with three RESULTs and no revise line keeps `revises=2`, and T118's fixture assertion moves from 9 to 20; a record with a class at two rows prints the S1-watch line and no S1 line, at three rows the S1 line and no watch; advisory-p2 at two rows prints neither. The existing tests stay and keep their values (their fixtures hold no revise line, or the test states the new count).
5. `tests/unit/test_chain_glue.py`: `test_integrate_inherits_the_audit_across_an_update_branch_only_head`: a repository where the audited head is merged with a moved main: the chain copies the receipt with the inherited-from line and the module's stub orch-audit.sh records no call; the same with one extra commit on the PR side records one orch-audit call.

## Out of scope

The SKILL and the rules files (the rules half, a02); AGENTS.md's Audit section and orch-audit.sh's prompt (the audit task `dotfiles-T128-audit-s1-report-a01`, whose amendment 1 writes the split verdict, the final line kept as the code verdict); chain-finish.sh (PR #378), the gate `scripts/require-crit-review.py` and `acceptance-front-matter.py`, which read the final Verdict line unchanged; local-advisory.sh (it already records P3 findings as advisory rows); the lints of the lineage's a03.


## Check

`uv run python -m unittest tests/unit/test_regime_counters.py tests/unit/test_chain_glue.py -v` green, pasted in the validation file with `shellcheck scripts/regime-counters.sh scripts/orchestrator/chain-integrate.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; the counters count every fix round, before or after the first RESULT); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `<lineage>-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by <lineage>-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-process-hardening-a01/task.md>` and the evidence paths.

## Change (round 1, 2026-10-17T08:20:04Z)

The Codex half's round 1 (P1, P2 ×7, P3): chain-finish.sh and the split-verdict read leave this task (the receipt's final line stays `Verdict:` as the code verdict, written by the audit task's amendment, so no consumer changes); revises is the larger of RESULTs minus one and the revise lines, with T118's fixture value named; the inheritance test asserts the stub orch-audit's calls; the generic update-branch row is verbatim; `after:` is empty and the Completion says so; the task copy path is this task's; the checks are pasted; the Constraints section is withdrawn with the template's (the operator, 2026-10-17: mechanisms, not text). Nothing else changes from `16675d7e`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-process-hardening-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-process-hardening-a01.md
```
