---
format: 2
task_id: dotfiles-T128-worker-s1-stop-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/agent-stop-gate.sh
  - tests/unit/test_agent_stop_gate.py
  - .orchestration/dotfiles-T128-worker-s1-stop-a01/**
after: [dotfiles-T128-rules-s1-replan-a01]
threat_table:
  - control: "the PR edits scripts/agent-stop-gate.sh in one place (the S1 check on the status=revise ACCEPTANCE that set the seat's pending entry, cleared as the entry closes today)"
    disposition: "residual: the Stop hook of every seat; it can only refuse the seat's turn end (stderr and exit 2) and does so until the seat has answered, as it refuses an unanswered RESULT today; it reads the bus through agmsg's storage facade as today and reads two tokens by exact key (s1=, re-plan=) and no free text, the s1= value checked as a slug before it is printed (a non-slug prints `<not a slug>`); the orchestrator's diff review and the task-level audit compare the diff against this row"
  - control: the PR edits tests/unit/test_agent_stop_gate.py only for the S1 cases
    disposition: "residual: new tests beside the existing ones, which stay; the tests write bus fixtures to a temporary store and run the hook as a subprocess"
  - control: in-process effects
    disposition: "residual: the test module runs the hook as a subprocess with fixtures in a temporary directory and imports only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the hook runs jq and the agmsg scripts as today; a PR checkout as cwd chooses nothing new"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-worker-s1-stop-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-worker-s1-stop-a01/ (report.md, validation.md, sandbox.md, learning.md)
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
  - claim: 'the Stop gate on origin/main knows no s1 token'
    command: 'git show origin/main:scripts/agent-stop-gate.sh | /usr/bin/grep -c "s1="'
    output: |-
      0
  - claim: 'the Message Contract on origin/main does not name the s1 token yet (the output reads 0; the dispatch waits until it reads 1, the rules task merged)'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "s1=<class>"'
    output: |-
      0
---

# AGMSG-TASK dotfiles-T128-worker-s1-stop-a01 — the worker's Stop gate enforces the three-repeat stop (C-59; the operator's correction of 2026-10-17)

Written 2026-10-17 by the orchestrator seat. The rules task names the tokens; this task makes the worker's side mechanical within a Stop hook's power: a seat that received a status=revise ACCEPTANCE with `s1=<class>` and no `re-plan=` cannot end its turn while that entry remains pending (the hook refuses the turn end, as it refuses an unanswered RESULT today; the rule text, step 15, names the answer the worker gives, `status=blocked note=S1:<class>`, and that answer closes the entry as any blocked PONG does); the hook cannot stop a push or a RESULT send itself, and the rule text (step 15, the rules task this task depends on) tells the worker to fix nothing more; the dispatcher's refusal of a further revise line is pending (the tools a04 row C-59:1, not a precondition of this task). Premise 2 records today's value (0) and the dispatch waits until it reads 1 (the rules task merged).

## What to do

1. `scripts/agent-stop-gate.sh`: what a Stop hook can enforce is the seat's turn end, so the check is: for each of the seat's pending tasks (the `pending` map the gate already keeps today, lines 284 to 296), when the message that set the entry is an ACCEPTANCE of `status=revise` addressed to this seat carrying `s1=<class>` and no `re-plan=` token, the gate refuses the turn end with the reason `S1: <class> without a re-plan line; fix nothing more, answer status=blocked note=S1:<class> (C-59)`, printed through `block()` as `agent-stop-gate: S1: <class> …` beside the existing pending-task reason for the same id, and exit 2. What the tool enforces ends there: the entry closes as today (line 293: a RESULT or any `status=blocked` PONG from this seat to the peer, a later non-revise ACCEPTANCE from the peer; a further `status=revise` ACCEPTANCE sets the entry anew, lines 289 and 290, so its tokens decide), and a newer `AGMSG-TASK` for the same id (lines 289 and 290) sets the entry anew, so its setter is then the TASK line and the S1 check passes; the note form `S1:<class>` is step 15's rule text (the rules task), not a check of this gate. When the ACCEPTANCE carries `re-plan=`, or carries neither token, the S1 check passes and the existing checks decide as today. The tokens are read by exact key from the line's whitespace-split fields, as the gate reads `task_id=` and `status=` today, and the `s1=` value is bus text from whoever sent the ACCEPTANCE (line 289 lets any sender's revise ACCEPTANCE set the entry), so it is validated as a class slug, `[a-z0-9-]` of 1 to 64 characters, before it is printed: a value that is not a slug still refuses the turn end (fail closed) with the reason `S1: <not a slug> without a re-plan line; …`, the literal text `<not a slug>` in place of the value, so no bus text reaches stderr or the worker's PONG; a closed task is never blocked by it.
2. `tests/unit/test_agent_stop_gate.py`: `test_stop_gate_refuses_the_turn_on_s1_without_re_plan` (the `S1: <class>` reason on stderr as a substring, and exit 2), `test_stop_gate_clears_s1_after_the_blocked_pong` (the same bus plus the seat's blocked PONG newer than the ACCEPTANCE: the task is closed as today, no `S1:` line and no pending-task line), `test_stop_gate_resets_s1_on_a_newer_task_line` (the same bus plus a newer TASK for the same id: no `S1:` line; the pending-task reason as today), `test_stop_gate_ignores_s1_with_re_plan_or_without_tokens` (both tokens, and neither: no `S1:` line), `test_stop_gate_prints_no_bus_text_for_a_malformed_s1_value` (an `s1=` value with a space, a quote and `$(…)`: the reason carries `<not a slug>`, exit 2, and the value appears nowhere on stderr); the tests assert the diagnostic's presence or absence, not a bare pass, because the existing pending-task refusal still applies to a revise fixture; the existing tests stay. Nothing else changes.

## Validation

- `uv run python -m unittest tests/unit/test_agent_stop_gate.py -v` green in the validation file, with the five new tests named; `shellcheck scripts/agent-stop-gate.sh`.
- `git diff --numstat origin/main...HEAD` in the validation file: at most 200 changed lines outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Completion

One PR from a fresh branch off `origin/main` (after the rules task dotfiles-T128-rules-s1-replan-a01 merges). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-worker-s1-stop-a01-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-worker-s1-stop-a01-followup-a01` in this task's acceptance record. The third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59). The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-worker-s1-stop-a01/task.md>` and the evidence paths.

## Change (round 1, 2026-10-17T02:29:34Z)

The Codex half's round 1 (P1, P1, P2, P2): a Stop hook refuses only the seat's turn end, so item 1 states that power and nothing more; the check is scoped to the seat's pending task and its latest status=revise ACCEPTANCE and is cleared by the seat's blocked PONG, so a closed task is never blocked; the tests assert the S1 diagnostic's presence or absence rather than a bare pass; the orchestrator pastes the checker and mask results at dispatch (presend). Nothing else changes from `579d0a77`.

## Change (round 2, 2026-10-17T02:33:34Z)

The Codex half's round 2 (P2): the brief's stop condition 4 reads the checker and mask outputs from this file; pasted above. Nothing else changes from `232595f4`.

## Change (round 3, 2026-10-17T02:38:03Z)

The Codex half's round 3 (P1): the overview claimed the hook prevents pushes and RESULT sends; it now states the hook's actual power (refusing the turn end until the blocked PONG) and names the rule text and the dispatcher's refusal for the rest. Nothing else changes from `be279225`.

## Change (round 4, 2026-10-17T02:41:09Z)

The Codex half's round 4 (P1): the overview presented the dispatcher's refusal as active; it is pending (the tools a04 row) and not an `after:` precondition, and the overview now says so. Nothing else changes from `3d486010`.

## Change (round 5, 2026-10-17T03:02:05Z)

The review seat's round 1 (a003; P2, P3 ×3): item 1 states what the tool enforces apart from what the rule states (the entry closes as today on a RESULT, any blocked PONG or a later ACCEPTANCE; a newer TASK line resets it; the note form is step 15's text), quotes the reason with the `agent-stop-gate: ` prefix, and item 2 adds the newer-TASK case (four tests, the Validation line following); premise 2's claim carries today's value. Nothing else changes from `133faede`.

## Change (round 6, 2026-10-17T03:06:57Z)

The Codex half's round 6 (P2 ×2): the overview describes the block as lasting while the S1 entry remains pending and leaves the answer's form to the rule; item 1 qualifies the closing ACCEPTANCE as non-revise, a revise ACCEPTANCE setting the entry anew. Nothing else changes from `b3900362`.

## Change (round 7, 2026-10-17T03:22:42Z)

The review seat's round 2 (a005; P2, P3): the `s1=` value is bus text from any sender, so item 1 and row 1 now check it as a slug before printing it (a non-slug refuses with `<not a slug>`, nothing from the bus on stderr), with a fifth test; row 1's control names the closure as item 1 states it; the Change sections are in time order. Nothing else changes from `6164ab23`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-worker-s1-stop-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-worker-s1-stop-a01.md
```
