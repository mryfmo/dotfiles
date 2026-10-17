---
format: 2
task_id: dotfiles-T128-process-hardening-a02
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - home/dot_config/claude/rules/pr-integration.md
  - home/dot_config/claude/rules/agmsg-orchestration.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/fixtures/regime/invariants.md
  - tests/fixtures/regime/worker-step-15.md
  - .orchestration/dotfiles-T128-process-hardening-a02/**
after: [dotfiles-T128-rules-s1-replan-a01, dotfiles-T128-process-hardening-a01]
threat_table:
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md in five places (the counters bullet's INV-6 count and the second-row check, the task-level audit bullet's split verdict, Orchestrator Playbook step 10's first-review P2 clause and P3 routing and its update-branch sentence, the Worker Playbook's comparison constraint)
    disposition: "residual: the rule text seats read; the docs tests pin each new sentence and the fixtures follow the sections in the same commit; the orchestrator's diff review and the task-level audit compare the diff against this row; an edit outside these places is an undeclared change the audit fails"
  - control: "the PR edits home/dot_config/claude/rules/pr-integration.md in one place (the disposition bullet with the first review's P2 and the P3 routing, and the audit's code verdict as the merge authority)"
    disposition: "residual: an always-loaded Claude rule within its word budget (test_word_budgets); the sentence pinned by the docs test"
  - control: "the PR edits home/dot_config/claude/rules/agmsg-orchestration.md in one place (the Acceptance invariant, where the audit's code verdict decides the merge and its record findings are dispositioned beside it)"
    disposition: "residual: an always-loaded Claude rule within its word budget; the sentence pinned by the docs test"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py only for the new sentence tests
    disposition: "residual: new tests beside the existing ones, which stay (`test_three_repeats_start_with_a_pasted_correction_search` and `test_advisory_rows_are_excluded_from_the_class_counts` among them: the new sentences are appended after the sentences those tests pin and repeat none of their phrases)"
  - control: the PR edits tests/fixtures/regime/invariants.md only as its pinned section changes
    disposition: "residual: the pinned copy of the invariants section, compared whole by test_regime_rule_sections_are_pinned_whole"
  - control: the PR edits tests/fixtures/regime/worker-step-15.md only as its pinned section changes
    disposition: "residual: the pinned copy of Worker Playbook step 15, compared whole by test_regime_rule_sections_are_pinned_whole"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-process-hardening-a02/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-process-hardening-a02/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the docs tests read the rule files and fixtures as text and import only the standard library; nothing is run"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; prose only; a PR checkout as cwd chooses nothing"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the SKILL on origin/main still says a new push including an update-branch merge needs a new audit'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "including a .gh pr update-branch. merge, needs a new audit"'
    output: |-
      1
  - claim: 'the SKILL on origin/main knows no code and record verdict split'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "Verdict (code)"'
    output: |-
      0
  - claim: 'the rules S1 task has merged (the Message Contract names the s1 token; absent today: this task dispatches after it)'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "s1=<class>"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-process-hardening-a02 — the six process rules in the rule text: counted rounds, inherited audits, the code verdict, first-review P2, the second-row check, the comparison constraint (C-61, the operator's decision of 2026-10-17)

Written 2026-10-17 by the orchestrator seat after the operator's root-cause analysis (M-20261017-06, C-61). This is the rules half of the lineage `dotfiles-T128-process-hardening`; the tools half (a01) lands the same rules in regime-counters.sh, chain-integrate.sh and chain-finish.sh, and the audit task `dotfiles-T128-audit-s1-report-a01` writes the split verdict the auditor emits. The SKILL is a shared prose source read by every seat and the two rules files are Claude-boundary, so a Codex seat implements (Orchestrator Playbook step 3). The new rules apply to this PR itself.

## Goal

Every seat reads, in one sentence each, which mechanism enforces the six rules (the orchestrator's counters, chain and audit; the template; the lints of a03) where it reads its procedure: the counters bullet, the task-level audit bullet, Orchestrator Playbook step 10 and the Worker Playbook of the SKILL, and the two always-loaded rules files; each new sentence is pinned by a docs test and its fixture.

## Files

1. SKILL, the counters bullet (the one beginning "Before every acceptance action"): INV-6's revise count is the larger of RESULTs minus one and the `status=revise` ACCEPTANCE lines for the task, each fix round before or after the first RESULT, cap two (C-61 rule 2; the counters print it, landed by the tools half a01, an `after:` task); and at a class's second row (`S1-watch` line) the orchestrator checks whether a string parse is involved and whether there is one data source and one parser, and opens a design task when not (rule 5). The sentences are appended after the bullet's existing sentences and repeat none of the phrases the existing docs tests pin.
2. SKILL, the task-level audit bullet: the audit ends with two verdict lines, `Verdict (record): correct|incorrect` over the records and then the final `Verdict: correct|incorrect` over the diff (the code verdict, the line every consumer reads today; the audit task's amendment 1 writes them), each finding tagged `code` or `record`; the merge reads the final line, and a record finding is dispositioned in the record beside the merge, never a stop (rule 4). The sentence "A new push, including a `gh pr update-branch` merge, needs a new audit of the new head." becomes: a new push needs a new audit, except an update-branch merge whose PR diff is unchanged (the chain compares patch-ids, landed by a01), which inherits the previous head's audit with its source named in the receipt (rule 3).
3. SKILL, Orchestrator Playbook step 10: the small in-PR P2 fix covers only the Bot's first review of the PR; a P2 of a later review and every P3 go to the follow-up owner, never to a round (rule 1); the update-branch sentence of the step follows item 2's reading.
4. SKILL, Worker Playbook (a new sentence in the step that states the worker's implementation duties): comparisons of paths, URLs, processes and text use one normalising function or structured data, never a string form compared by text (rule 6; the task template's Constraints section says the same).
5. `home/dot_config/claude/rules/pr-integration.md`: the disposition bullet's exception reads "an advisory P2 with an existing owner task file, or a P2 of a later review or a P3, which the follow-up owns"; the audit sentence reads "its code verdict is the merge authority, its record findings are dispositioned beside it". `home/dot_config/claude/rules/agmsg-orchestration.md`, the Acceptance invariant: "the audit's code verdict decides the merge; its record findings are input dispositioned in the record" (within the file's word budget, `test_word_budgets`).
6. `tests/unit/test_agmsg_orchestration_docs.py`: `test_counters_bullet_counts_every_revise_line_and_checks_the_second_row`, `test_audit_bullet_splits_the_verdict_and_inherits_across_update_branch`, `test_step_10_limits_the_in_pr_fix_to_the_first_review`, `test_worker_playbook_requires_normalised_comparisons`, `test_rules_files_name_the_code_verdict_and_the_follow_up_routing`; each asserts its sentence in the SKILL or rule file directly, and also in the fixture for the two sections that have one (`invariants.md` for the counters and task-level audit bullets, `worker-step-15.md` for the Worker Playbook sentence when it lands in step 15; step 10 and the two rules files have no fixture and are asserted in place); the fixtures follow their sections in the same commit; the existing tests stay green.

## Out of scope

The tools (a01); AGENTS.md's Audit section and orch-audit.sh (the audit task); the task template (the orchestrator's record, already carrying the Constraints section and the first-review clause).


## Check

`uv run python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` green in the validation file, with the five new tests named; `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2); the rules files within their word budgets.

## Completion

One PR from a fresh branch off `origin/main` (after the rules S1 task and the tools half a01 merge). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; the counters count every fix round, before or after the first RESULT); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `<lineage>-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by <lineage>-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-process-hardening-a02/task.md>` and the evidence paths.

## Change (round 1, 2026-10-17T08:20:04Z)

The Codex half's round 1 (P2 ×4) and the operator's policy of 08:1xZ (mechanisms, not text): the tools the sentences name are a01's, now an `after:` task; the verdict split keeps the final `Verdict:` line as the code verdict; the fixture coverage is stated per section; the generic update-branch row is verbatim; the task copy path is this task's; the Constraints section is withdrawn and each rule sentence names the mechanism that enforces it, no more. Nothing else changes from `944925fd`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-process-hardening-a02.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-process-hardening-a02.md
```
