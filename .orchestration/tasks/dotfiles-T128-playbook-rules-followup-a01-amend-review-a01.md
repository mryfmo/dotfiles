---
format: 2
task_id: dotfiles-T128-playbook-rules-followup-a01-amend-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-playbook-rules-followup-a01-amend-review-a01 — confirm amendment 1 of `dotfiles-T128-playbook-rules-followup-a01` (review seat half; Codex headless runs the same check)

Drafted 2026-10-14 by the orchestrator seat. The worker's question (bus 1108, 06:50:50Z): two sentences outside SKILL lines 171 to 178 (the task-level audit bullet, SKILL line 90, and AGENTS.md line 44) state the retired gate mechanism (`AUDIT_DISPOSITIONS`; the `audit-finding:` prose as what the gate reads), and item 2 forbids sentences outside the owned rows; the answer is a scope statement of the `procedure-migration` row, so it travels as this amendment, not as a PONG. Amended file: `.orchestration/tasks/dotfiles-T128-playbook-rules-followup-a01.md`, sha256 `ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b`; the pre-amendment copy is `.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-pre-amend1.md (the copy of `origin/main` at c15ba668, sha256 e22e0cc45de6fe70ac9be9b3e7b710055b7cd8b8c50767d7a832a9335f392c51)`.

## What changed (amendment 1)

- Item 1 (`## What to do`) gained one sentence after "the RESULT lists each row with `fixed:<sha>`": the `procedure-migration` row (`audit:71eb920:1`) covers every sentence in this task's allowed files that still states the retired gate input (`AUDIT_DISPOSITIONS`, or the `audit-finding:` prose as what the gate reads), since the gate on main reads the record's JSON `audit_findings`: the step 10 lines the audit named, the SKILL's task-level audit bullet, the AGENTS.md gate sentence and the pinned fixture `tests/fixtures/regime/invariants.md`, each changed sentence with its token test.
- A new `## Change (amendment 1, 2026-10-14)` section at the end: the why (bus 1108) and the pasted `git show origin/main:… | grep -n` lines the row now covers (SKILL 90, 171, 172, 178; AGENTS.md 44; the fixture's line 27).
- Nothing else: the front matter (allowed_files, threat table, premises), item 2, Validation and Completion are byte-identical to the pre-amendment copy.

## Stop condition

1. The diff of the task file against its copy on `main` contains only what the list above says.
2. For each behaviour the amendment adds or changes in a script or a procedure, name the threat row that covers it; a new effect on a gate input (an acceptance record, a sweep JSON, an audit receipt), on the bus or on the host has its own row with a closing test, added by this amendment (C-28, M-20261012-29). An amendment that adds behaviour without its row is `revise`.
3. Each closed row's named test closes its risk and the test names appear verbatim in the task's test item; the wording agrees with the rule sentences and the sibling tasks it cites.
4. The file passes C1 to C10 and C7b (the orchestrator pasted OK) (no superseded term: the amendment adds one sentence and one section, so `amend-sweep.sh` has nothing to sweep); the copy rows and the evidence directory are unchanged (the task has no `reset_of`).

## Output

`.orchestration/validation/dotfiles-T128-playbook-rules-followup-a01-amend-review-a01.md`: the usual header with the file's sha256, findings (`P0`–`P3`, confidence, `file:line`, one line), one line `Amendment verdict: dotfiles-T128-playbook-rules-followup-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-playbook-rules-followup-a01-amend-review-a01 verdict=confirm|revise amended_task_sha256=ec415eaf526937fd43907a59fccfc455de117850003ba3d48cd20b065fc5564b validation=<path>`.
