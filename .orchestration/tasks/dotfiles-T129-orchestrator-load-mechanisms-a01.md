---
format: 2
task_id: dotfiles-T129-orchestrator-load-mechanisms-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - home/dot_config/claude/rules/agmsg-orchestration.md
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - home/dot_agents/agent-config.yaml
  - home/dot_claude/hooks/executable_orchestrator-limits.py
  - scripts/orchestrator/record-from-result.py
  - scripts/orchestrator/integrate.sh
  - scripts/orchestrator/unsent-tasks.sh
  - tests/unit/test_orchestrator_load.py
  - .orchestration/dotfiles-T129-orchestrator-load-mechanisms-a01/**
after: [dotfiles-T129-assets-omp-hcom-a01]
threat_table:
  - control: "the PR edits home/dot_config/claude/rules/agmsg-orchestration.md in two bullets (Delegation: task authoring and pre-send fixes are the task-author worker role; Acceptance: the review seat runs reviews and returns a verdict file, the orchestrator approves verdict files and hashes; nothing else)"
    disposition: "residual: a Claude-boundary rule file edited by the Codex seat (the routing rule); the text is the minimum that names the roles, every procedure is the scripts below; the diff review and the audit compare against this row"
  - control: "the PR edits home/dot_agents/skills/agmsg-orchestration/SKILL.md in the sections the two bullets point to (the task-author role, the verdict-file review, the one integration script, the limit hook, the unsent-task warning), each as one short paragraph naming the script"
    disposition: "residual: shared prose read by every seat, edited by the Codex seat on the operator's instruction of 2026-10-17 20:0x JST; no procedure is written twice (the script is the procedure)"
  - control: "the PR edits home/dot_agents/agent-config.yaml in one place (the hook entry that registers executable_orchestrator-limits.py for the orchestrator's Claude session where the existing Claude hooks are declared; the generator renders it)"
    disposition: "residual: the hook table of the manifest, rendered into the Claude settings by scripts/generate-agent-configs.py; the validator checks the rendered hook tables against the manifest (agent-assets workflow)"
  - control: "the PR adds home/dot_claude/hooks/executable_orchestrator-limits.py (the limit hook of item 4: per-processing tool-call and minute counters, the 2k Bash and heredoc-program refusals, the 600k-token handoff)"
    disposition: "closed: tests/unit/test_orchestrator_load.py::test_limit_hook_stops_at_25_calls_or_20_minutes_refuses_long_bash_and_heredoc_programs_and_forces_a_handoff_at_600k_tokens"
  - control: "the PR adds scripts/orchestrator/record-from-result.py (item 2: acceptance-record entries, ledger rows and decisions.tsv rows generated from a RESULT JSON, the gate output and the regime-counters output)"
    disposition: "closed: tests/unit/test_orchestrator_load.py::test_record_from_result_writes_the_record_entries_ledger_rows_and_decision_rows_from_fixtures"
  - control: "the PR adds scripts/orchestrator/integrate.sh (item 3: sweep, audit, gate, merge, ff as one script run in the background, a completion file as the notification)"
    disposition: "closed: tests/unit/test_orchestrator_load.py::test_integrate_runs_the_steps_in_order_stops_at_the_first_failure_and_writes_the_completion_file"
  - control: "the PR adds scripts/orchestrator/unsent-tasks.sh (item 5: a warning for a prepared task unsent for 15 minutes while a seat is idle)"
    disposition: "closed: tests/unit/test_orchestrator_load.py::test_unsent_tasks_warns_after_15_minutes_only_when_a_seat_is_idle"
  - control: "the PR adds tests/unit/test_orchestrator_load.py (the five tests above, fixtures written by the test, stub gh, stub seats and stub scripts on PATH)"
    disposition: "residual: fixtures and stubs written by the test; the audit reads each case against items 1 to 5"
  - control: "the hook's inputs as a trust boundary (the hook-input JSON Claude Code passes, the transcript file it names, the Bash command text it inspects)"
    disposition: "residual: the hook reads the JSON from stdin and the transcript as text, decides by counts and lengths, writes one state file under the session's temporary directory and prints a JSON decision; it executes nothing from its inputs; a malformed input is a pass-through with a warning line (fail-open on the hook, fail-closed on the limits once read)"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-orchestrator-load-mechanisms-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-orchestrator-load-mechanisms-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run the hook, the two scripts and the generator as subprocesses on fixtures in a temporary directory with stub gh and stub scripts on PATH, and import only the standard library; nothing is imported into another process; no seat is contacted"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow file is in allowed_files; the hook runs under the repository's python as the format-edited-files hook does; integrate.sh runs the existing orchestrator scripts, gh and git as the glue runs them today; the generator renders the hook entry as it renders the others; a PR checkout as cwd chooses nothing new"
  - control: new or renamed scripts
    disposition: "residual: 3 new scripts under scripts/orchestrator and 1 new hook, each named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main; integrate.sh runs that same command and nothing else as the merge"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: the rule on origin/main keeps acceptance, adversarial RESULT review and review-profile work with the orchestrator (the lines naming it), the clause item 1 changes
    command: git show origin/main:home/dot_config/claude/rules/agmsg-orchestration.md | /usr/bin/grep -cE "never delegated|review-profile work"
    output: |-
      1
  - claim: none of the four new files exists on origin/main
    command: for f in home/dot_claude/hooks/executable_orchestrator-limits.py scripts/orchestrator/record-from-result.py scripts/orchestrator/integrate.sh scripts/orchestrator/unsent-tasks.sh; do git cat-file -e origin/main:$f 2>/dev/null && echo "$f present"; done; echo end
    output: |-
      end
  - claim: 'the orchestrator records are written by hand today: the acceptance records hold no generated marker (count of a record-from-result marker line on origin/main)'
    command: git grep -c "record-from-result" origin/main -- .orchestration/acceptance | wc -l | tr -d " "
    output: |-
      0
  - claim: the existing Claude hooks are declared in the manifest and rendered (the project-map-reload hook appears in the manifest and under home/dot_claude/hooks)
    command: a=$(git show origin/main:home/dot_agents/agent-config.yaml | /usr/bin/grep -c "project-map-reload"); b=$(git ls-tree --name-only origin/main home/dot_claude/hooks/ | /usr/bin/grep -c "project-map-reload"); echo "$a $b"
    output: |-
      1 1
---

# AGMSG-TASK dotfiles-T129-orchestrator-load-mechanisms-a01 — the orchestrator's load fixed in the structure: roles, generated records, one background integration, a limit hook, an unsent-task warning (plan 023 PR F3)

Written 2026-10-17 by the orchestrator seat on the operator's user-approved instruction of 20:0x JST. Cause found by the operator: the long processing is not CI waiting but the hand work the rules keep with the orchestrator (writing task texts, fixing pre-send failures, writing acceptance records and ledgers, running reviews), done one item at a time in a context near a million tokens. The five rows below are the fix, each a mechanism with a behaviour test; the text rules change by the minimum that names the roles. The orchestrator implements nothing of this.

## Goal

A task text is written and pre-send-fixed by a worker in the task-author role; a review is run by the review seat and returned as a verdict file the orchestrator approves by hash; acceptance-record entries, ledger rows and decision rows are generated from the RESULT JSON and the gate output; the integration runs as one background script with a completion notification; a hook ends a processing at 25 tool calls or 20 minutes, refuses a Bash command over 2000 characters and an inline heredoc program, and forces a handoff above 600k context tokens; a prepared task unsent for 15 minutes while a seat is idle raises a warning.

## Files

1. Roles (text, minimal). `home/dot_config/claude/rules/agmsg-orchestration.md`: the Delegation bullet gains the task-author role (a worker writes the task text from the orchestrator's one-paragraph brief, runs the pre-send checks and fixes what fails; the orchestrator approves the final hash); the Acceptance bullet changes from "stay with the orchestrator and are never delegated" to: the review seat runs the review and returns a verdict file (`.orchestration/validation/<task>-verdict-<sha7>.json`: task, hash, verdict, findings), the orchestrator approves the verdict file and the hash; acceptance of a RESULT stays the orchestrator's one-line approval of the generated record. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: one short paragraph per row of this task in the sections the bullets point to, each naming the script that is the procedure; no other text change.
2. `scripts/orchestrator/record-from-result.py <task> <result.json> [--gate <gate-output>] [--counters <regime-counters-output>]` (new; standard library): the RESULT line parsed into JSON by the existing bus reader or given as a file; writes to `.orchestration/acceptance/<task>.md` the round entry (head, PR, files, caps, test names, dispositions), the ledger tab rows for every finding id the RESULT and the gate output name with their classes, and appends a decisions.tsv row for each `decision:` field of the RESULT; attaches the regime-counters output verbatim under the entry; idempotent on the same inputs (a second run changes nothing); a line `<!-- record-from-result <sha256 of the inputs> -->` marks each generated entry (premise 3).
3. `scripts/orchestrator/integrate.sh <task> <pr> [--notify <file>]` (new): the chain as one script, each step one command under `set -e`: fast-forward the main checkout, the sweep (`scripts/pr-feedback.py`), the local review and its advisory rows, the record block, the audit (`orch-audit.sh`), the gate (`make require-crit-review` with the three evidence variables), `gh pr merge --squash --match-head-commit <audited head>`, the fast-forward after the merge; the log goes to `.orchestration/validation/<task>-integrate-<sha7>.log`; on completion or on the first failing step it writes the notify file (`step=<name> rc=<n> head=<sha>`), so the orchestrator starts it in the background and acts on the notification, never watching it.
4. `home/dot_claude/hooks/executable_orchestrator-limits.py` (new; the hook-input JSON on stdin, the decision JSON on stdout; registered in `home/dot_agents/agent-config.yaml` where the existing Claude hooks are declared, as PreToolUse and UserPromptSubmit for the orchestrator's session; the generator renders it): a state file per session under the session's temporary directory counts tool calls and the processing's start time since the last user prompt; the 26th tool call or the 21st minute returns a decision that ends the processing with the reason; a Bash command over 2000 characters, or one that feeds an interpreter a heredoc (`<<'PY'`, `<<EOF` followed by python, node, ruby, perl or bash), is refused with the reason (write the program to a file and run the file); when the transcript the input names shows more than 600000 context tokens in its last usage record, the decision forces a handoff (`.orchestration/handoff/<utc>.md` written by the orchestrator: in-flight PRs and tasks, seats, open decisions, next step, resume commands) and ends the processing.
5. `scripts/orchestrator/unsent-tasks.sh` (new): for every task file with a pasted `## Checks` block and no `AGMSG-TASK` line naming it in the bus, when the file is older than 15 minutes and `team.sh <team> --json` shows an idle seat, print `unsent task <id> for <n> minutes; idle seat <name>`; the limit hook calls it at each user prompt and surfaces its lines.
6. `tests/unit/test_orchestrator_load.py` (new): `test_record_from_result_writes_the_record_entries_ledger_rows_and_decision_rows_from_fixtures` (a RESULT fixture with two findings and one decision; the entry, the two tab rows and the decisions row appear once after two runs), `test_integrate_runs_the_steps_in_order_stops_at_the_first_failure_and_writes_the_completion_file` (stub scripts record their order; a failing gate stub stops before the merge stub and the notify file names the step), `test_limit_hook_stops_at_25_calls_or_20_minutes_refuses_long_bash_and_heredoc_programs_and_forces_a_handoff_at_600k_tokens` (hook-input fixtures: the 25th call passes and the 26th ends the processing; a start time 21 minutes old ends it; a 2001-character Bash and a `python3 - <<'PY'` command are refused with the reason, a 1999-character one passes; a transcript fixture whose last usage shows 600001 tokens forces the handoff, 599999 does not), `test_unsent_tasks_warns_after_15_minutes_only_when_a_seat_is_idle` (a prepared task 16 minutes old warns with an idle seat and is silent with every seat busy; a 14-minute-old one is silent), and `test_the_rule_and_skill_name_the_roles_and_the_scripts` (the two files contain the task-author role, the verdict file, and each script name once).

## Out of scope

Running any of this against live seats (the tests use stubs); moving the orchestrator to omp (plan 023 B and C: the hook is Claude Code's until then and the scripts are harness-independent); changing permgate or any permission policy; the acceptance-time checks that stay with the orchestrator (approving a verdict file's hash, approving a generated record).

## Check

`uv run python -m unittest tests/unit/test_orchestrator_load.py -v` green and `uv run --offline --with pyyaml scripts/validate-agent-assets.py` (exit 0) pasted in the validation file, with `shellcheck scripts/orchestrator/integrate.sh scripts/orchestrator/unsent-tasks.sh`, `ruff check` on the two Python files, and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/`, outside `.orchestration/` and outside the four new files (plan 021 step 7.2; the four new files are counted separately and reported, each at most 200 lines), and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` after dotfiles-T129-assets-omp-hcom-a01 merges (the manifest is shared). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round, before or after the first RESULT, counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T129-orchestrator-load-mechanisms-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T129-orchestrator-load-mechanisms-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T129-orchestrator-load-mechanisms-a01/task.md>` and the evidence paths.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-orchestrator-load-mechanisms-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-orchestrator-load-mechanisms-a01.md
```
