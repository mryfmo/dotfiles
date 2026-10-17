---
format: 2
task_id: dotfiles-T128-rules-s1-replan-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/fixtures/regime/worker-step-15.md
  - tests/fixtures/regime/message-contract.md
  - tests/fixtures/regime/invariants.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - .orchestration/dotfiles-T128-rules-s1-replan-a01/**
after: [dotfiles-T128-s1-replan-gate-a01]
threat_table:
  - control: the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md in three places (the counters bullet, the Message Contract, Worker Playbook step 15)
    disposition: "residual: prose read by both runtimes; the pinned fixtures follow the sections in the same commit (INV-12) and the docs tests pin each sentence; the orchestrator's diff review and the task-level audit compare the diff against this row"
  - control: the PR edits tests/fixtures/regime/worker-step-15.md only as the pinned copy of step 15
    disposition: "residual: a fixture; it changes with the section it pins in the same commit"
  - control: the PR edits tests/fixtures/regime/message-contract.md only as the pinned copy of the Message Contract
    disposition: "residual: a fixture; it changes with the section it pins in the same commit"
  - control: the PR edits tests/fixtures/regime/invariants.md only as the pinned copy of the counters bullets it holds
    disposition: "residual: a fixture; it pins the whole counters section, so the counters bullet's new sentence changes it in the same commit (INV-12)"
  - control: the PR edits tests/unit/test_agmsg_orchestration_docs.py only for the three pinned sentences
    disposition: "residual: new tests beside the existing ones, which stay; the module imports only the standard library and reads the rule files as text"
  - control: in-process effects
    disposition: "residual: the docs test module imports only the standard library and reads the rule files as text; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; prose and its tests; a PR checkout as cwd chooses nothing new"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-rules-s1-replan-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-rules-s1-replan-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'the SKILL on origin/main has no re-plan line yet'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "re-plan:"'
    output: |-
      0
  - claim: 'the template in the main checkout carries the S1 sentence (the orchestrator wrote it on 2026-10-17; it lands with the next boundary)'
    command: '/usr/bin/grep -c "third finding of one class" .orchestration/templates/task-short.md'
    output: |-
      1
  - claim: 'the gate task has merged, its S1 refusal being what the rule text describes as landed (the output read 0 until PR #382 merged as 8490047f at 07:57:51Z; it reads 1 now)'
    command: 'git show origin/main:scripts/require-crit-review.py | /usr/bin/grep -c "re-plan"'
    output: |-
      1
---

# AGMSG-TASK dotfiles-T128-rules-s1-replan-a01 — the three-repeat stop in the rule text: the re-plan line, the ACCEPTANCE tokens and the worker's stop (C-59; the operator's correction of 2026-10-17)

Written 2026-10-17 by the orchestrator seat. The gate task `dotfiles-T128-s1-replan-gate-a01` makes the stop mechanical in the counters and the merge gate; this task writes the rule the tools enforce, once, in the SKILL, so every seat reads it (the task template already carries its Completion sentence, the orchestrator's record). Premise 3 records today's value (0) and the dispatch waits until it reads 1 or more (the gate task merged).

## What to do

1. SKILL, the three-repeats bullet of the invariants section (the one beginning "When a finding class reaches three on one artifact"; the docs module calls the "Before every acceptance action" bullet the counters bullet): new sentences appended after its first sentence (the one ending "never text taken from a review title.", which `test_three_repeats_start_with_a_pasted_correction_search` asserts as one unbroken token; every existing sentence of the bullet stays byte-identical): after the `search:` line, the orchestrator writes one line `re-plan: <class> -> specification: … design: … implementation: … verification: …` (the four parts, one sentence each) before any further revise or amendment. The line is required for S1's count, which takes the ledger rows that are not advisory, as the counters bullet above excludes them (the class `advisory-p2` never triggers it), while S6's search threshold keeps every ledger class as today; the two counts are named apart in the sentence, and the sentence does not repeat the counters bullet's phrase "non-advisory rows only", which `test_advisory_rows_are_excluded_from_the_class_counts` counts exactly once in the section. The sentence names what enforces it and where: regime-counters.sh prints `re-plan=present|missing` on the S1 line and require-crit-review.py refuses a merge while a class at three rows has no such line (landed by `dotfiles-T128-s1-replan-gate-a01`); dispatch.sh refuses a revise or amendment line for a task whose record lacks the re-plan line (the tools a04 row C-59:1, pending until it lands, and the sentence says "when it lands"); the operator is asked once, with the re-plan, and a further finding of the class after the re-plan round is advisory. The fixture `tests/fixtures/regime/invariants.md` pins the invariants section and follows it in the same commit.
2. SKILL, Message Contract v1: an ACCEPTANCE of status revise for a task whose record holds an S1 class carries `s1=<class>` and `re-plan=<record line reference>`; the orchestrator writes both tokens (its standing procedure; no tool adds or checks them), and the only pending mechanism the sentence names is the one its row owns: dispatch.sh refusing a revise or amendment line for a task whose record lacks the re-plan line (the tools a04 row C-59:1, named as pending).
3. SKILL, Worker Playbook step 15: a worker whose ACCEPTANCE of status revise carries `s1=<class>` without `re-plan=` fixes nothing more and answers `AGMSG-PONG v1 … status=blocked note=S1:<class>`. Kept from PR #323's parked sentence (dc7edcc0, SKILL line 211): "fixes nothing more" and the blocked PONG; new: the trigger is the orchestrator's `s1=` token without `re-plan=` (the parked sentence triggered on the worker's own counts of heads and classes) and the note is `S1:<class>` (the parked note was `S1|INV-6;heads=<n>;classes=<class:count,…>;threads=<ids>`). The sentence names the worker's Stop gate check as pending (the task `dotfiles-T128-worker-s1-stop-a01`, which depends on this task's tokens).
4. The fixtures `worker-step-15.md`, `message-contract.md` and `invariants.md` follow their sections in the same commit; three docs tests in `tests/unit/test_agmsg_orchestration_docs.py`: `test_three_repeats_bullet_requires_a_re_plan_line_at_s1` (the bullet names the re-plan line's four parts and S1's count apart from S6's), `test_message_contract_names_the_s1_and_re_plan_tokens` (the two tokens on a revise ACCEPTANCE), `test_worker_step_15_stops_on_s1_without_re_plan` (the blocked PONG form `status=blocked note=S1:<class>`); each asserts the sentence's presence in the SKILL and in its fixture; the existing tests stay green, `test_advisory_rows_are_excluded_from_the_class_counts` and `test_three_repeats_start_with_a_pasted_correction_search` among them (item 1's two constraints). The task template's Completion sentence ("The third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59).") is the orchestrator's record, already in `.orchestration/templates/task-short.md`; the docs test may pin it from there. Nothing else changes.

## Validation

- `uv run python -m unittest tests/unit/test_agmsg_orchestration_docs.py -v` green in the validation file, with the three new tests named.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2); the rule text at most 450 words added.

## Completion

One PR from a fresh branch off `origin/main` (after the gate task dotfiles-T128-s1-replan-gate-a01 merges). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-rules-s1-replan-a01-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-rules-s1-replan-a01-followup-a01` in this task's acceptance record. The third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59). The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-rules-s1-replan-a01/task.md>` and the evidence paths.

## Change (round 1, 2026-10-17T02:29:34Z)

The Codex half's round 1 (P1, P2, P2, P2): `tests/fixtures/regime/invariants.md` pins the counters section and joins `allowed_files` with its row; S1's non-advisory count is named apart from S6's all-ledger search threshold; the dispatcher's and the Stop gate's enforcement are stated as pending with their owners (the tools a04 row, the worker task), not as landed; the three docs tests are named with their assertions. Nothing else changes from `dc88561d`.

## Change (round 4, 2026-10-17T03:02:04Z)

The review seat's round 1 (a005; P2 ×2, P3 ×4): item 1 names the two existing docs tests the new sentences must keep green (appended after the bullet's first sentence; the phrase "non-advisory rows only" not repeated) and calls the bullet by the module's name, the three-repeats bullet, with the test renamed; item 2 names only the mechanism the a04 row owns (the refusal) and keeps the tokens as the orchestrator's procedure; item 3 says what is kept from the parked sentence and what is new; the intro drops the template; premise 3's claim carries today's value. Nothing else changes from `cfb60308`.

## Change (premise 3, 2026-10-17T08:01:20Z)

PR #382 (the gate task) merged as 8490047f, so premise 3's recorded output moves from 0 to 1 and its claim says so; no other change from `bd0d8417`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-rules-s1-replan-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-rules-s1-replan-a01.md
```

## Change (round 2, 2026-10-17T02:33:34Z)

The Codex half's round 2 (P2): the brief's stop condition 4 reads the checker and mask outputs from this file; pasted above. Nothing else changes from `49623833`.
