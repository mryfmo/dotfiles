---
threat_table:
  - control: "the task-file copy on the branch (.orchestration/<task_id>/task.md)"
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/<task_id>/ (report.md, validation.md, sandbox.md, learning.md)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: "metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)"
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: "in-process effects"
    disposition: "residual: draft from the generator; the tests run the task's scripts as subprocesses in temporary repositories, and nothing writes outside the worktree, the evidence directory and $TMPDIR"
  - control: "workflow and interpreter or environment inputs"
    disposition: "residual: draft from the generator; no workflow or interpreter file is in allowed_files unless the rows above name it, and Python runs under python -I through uv"
  - control: "new or renamed scripts"
    disposition: "residual: draft from the generator; every new or renamed script is named in allowed_files and listed in the RESULT, and any other is an undeclared change the audit fails"
  - control: "orchestrator effect merge"
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: "orchestrator effect update-branch"
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: "orchestrator effect forced worker removal"
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
check:
  - make unit-test
  - make format
---

# The task template of scripts/orchestrator/task-from-plan.py

The generator reads this bundled file, never a sibling task record: the control rows above (`<task_id>` replaced), the unverified common Check commands and the Completion section below. Generation executes none of these commands; the orchestrator separately verifies trusted commands and records observations before dispatch.

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2`, stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (every fix round, before or after the first RESULT, counts toward INV-6's cap of two); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line; a later review's P2 and every P3 are advisory, as is any other P2, owned by `<task_id>-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions, and recorded under `## Owned by <task_id>-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/<task_id>/task.md>` and the evidence paths.
