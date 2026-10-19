---
format: 2
task_id: dotfiles-T133-rule-text-reduction-a01
kind: code
security: false
allowed_files:
  - home/dot_config/claude/rules/agmsg-orchestration.md
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_agmsg_orchestration_docs.py
  - .orchestration/dotfiles-T133-rule-text-reduction-a01/**
after: []
threat_table:
  - control: home/dot_config/claude/rules/agmsg-orchestration.md
    disposition: "residual: only the Acceptance bullet and Delegation exemption list change; the doc tests verify the responsibility paragraph, interim exemption and retained word budgets, with no runtime executable change."
  - control: home/dot_agents/skills/agmsg-orchestration/SKILL.md
    disposition: "residual: edits stay within the named acceptance and contract sections; the doc tests verify the shared paragraph and four contract additions, with no runtime executable change."
  - control: tests/unit/test_agmsg_orchestration_docs.py
    disposition: "residual: tests read repository text and compare explicit expectations; unrelated section pins and word budgets remain enforced, and no runtime script changes."
  - control: .orchestration/dotfiles-T133-rule-text-reduction-a01/**
    disposition: "residual: this directory contains only the dispatched task copy and task evidence; the final-head audit compares their claims with the diff and CI."
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-rule-text-reduction-a01/task.md)
    disposition: "residual: the copy is byte-identical to the dispatched text; TASK and RESULT bind its own sha256 and the orchestrator compares it at acceptance."
  - control: the branch evidence records under .orchestration/dotfiles-T133-rule-text-reduction-a01/
    disposition: "residual: report, validation, sandbox, learning, result.txt, precheck evidence and worker review records contain task data; refused commands are recorded and claims are checked against the final head."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b before dispatch and at acceptance; the task-copy comparison covers the complete dispatched front matter."
  - control: metadata separators
    disposition: "residual: the first YAML front-matter document remains bounded by its separators; the byte-identical task-copy comparison covers those separators."
  - control: in-process effects
    disposition: "residual: the changed tests read documentation and fixture text; this task adds no production execution, dispatch or record-generation behavior."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: workflows, interpreter configuration and environment inputs remain unchanged; validation uses the existing unittest and formatting commands."
  - control: new or renamed scripts
    disposition: "residual: no script is added, renamed or edited; the changed-file inventory and final-head audit enforce this boundary."
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator merges only through gh pr merge --squash --match-head-commit <audited head> after the integration gate in Orchestrator Playbook step 10.5."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the feedback sweep and the task-level audit bind the new final head before the gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records the discarded uncommitted state in acceptance."
premises: []
---

# AGMSG-TASK dotfiles-T133-rule-text-reduction-a01 — plan 024 P1-8 rule-text reduction and contract additions

## Goal

Plan 024 P1-8 replaces the blanket prohibition on delegating acceptance work with one shared paragraph that reserves only the acceptance decision and final merge for the orchestrator, assigns integration, reviews and record generation to seats and scripts, and names the manual fallback until each P1-4 to P1-6 mechanism lands. Message Contract v1 gains the four specified contract additions. This task is `security: false` because it changes prose and documentation tests without changing runtime executables. A Codex seat on the `standard` profile edits the Claude-boundary rule source and shared SKILL source under plan 021 step 8.3.

## Files

1. `home/dot_config/claude/rules/agmsg-orchestration.md` changes only the Acceptance bullet and the Delegation bullet's exemption list.

   The Acceptance bullet contains one paragraph stating that only the acceptance decision and final merge stay with the orchestrator. Integration steps, adversarial RESULT review, review-profile work, the gate and record generation belong to seats and scripts. The paragraph names `verdict.sh`, `audit-pool.sh`, `result-precheck.sh`, `acceptance-front-matter.py` and `dispatch.sh --next`. Until each mechanism lands, the orchestrator performs that step by hand under the interim exemption named in Delegation.

   The paragraph retains one task-level audit of the final head for every code-changing RESULT and states that audit findings are input, never approval. Its pointer to the SKILL's "Task-level audit" bullet remains valid. Delegation's exemption list names the interim manual steps pending their mechanisms and retains the existing control-plane, evidence-sync, acceptance-decision, final-merge, repository-free hygiene and explicit operator opt-out exemptions.

   `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationRuleTest::test_acceptance_paragraph_names_the_seat_mechanisms`, `test_delegation_lists_the_interim_integration_exemption` and `test_word_budgets` verify these statements.

2. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the acceptance paragraph in "Review and integration invariants" and the four additions in "Message Contract v1".

   The sentence reserving acceptance review, adversarial RESULT review, review-profile work and the gate to the orchestrator is replaced by the same single paragraph as the rule's Acceptance bullet. The two paragraph bodies agree word for word after removing their Markdown list markers and the rule's bold Acceptance label. The obsolete never-delegated sentences and capability-based reconsideration sentence are absent.

   Message Contract v1 documents the optional PONG field `context=<percent>` as the seat's context usage. `dispatch.sh --next` reads that value and refuses a seat above its context threshold.

   Message Contract v1 documents the task.md front-matter key `requires_decision:` as a list of decision ids without which the task may not proceed. The task-consistency checker verifies that each listed id exists in `.orchestration/decisions.tsv` with a result other than `pending`.

   Message Contract v1 documents `.orchestration/<task>/result.txt` as the file where the worker writes the RESULT line's `key=value` pairs before sending. `result-precheck.sh` reads that file.

   Message Contract v1 documents the RESULT field `precheck=<sha256 of precheck.json>` as the digest of the precheck evidence already emitted by P1-5. These additions describe the contract; their executable enforcement remains with the mechanism tasks.

   `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationRuleTest::test_acceptance_paragraph_matches_skill` and `tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_contract_names_context_decisions_result_file_and_precheck` verify these statements.

3. `tests/unit/test_agmsg_orchestration_docs.py` uses the existing `unittest`, section-extraction and `subTest` style.

   The acceptance tests assert the new responsibility sentences and mechanism names in both paragraph bodies, their word-for-word equality, the interim exemption and the absence of the old never-delegated sentences. The contract test extracts "Message Contract v1" and checks all four additions and their meanings there.

   Existing assertions that pin the superseded acceptance text change with the new expectations. Existing word budgets remain enforced. The whole-section pin test retains every pinned section and verifies all unrelated text unchanged.

   The expected whole-section text comes from the existing fixtures plus explicit, narrowly anchored replacements for this task's acceptance paragraph and contract additions stored in this test module. Replacement anchors are checked, and expected text never comes from the live SKILL content being tested. No fixture file changes.

   `tests/unit/test_agmsg_orchestration_docs.py::AgmsgRegimePatternTest::test_regime_rule_sections_are_pinned_whole` and the complete module verify the retained pins and existing safeguards. New tests have red results before the documentation edits and green results afterward.

4. `.orchestration/dotfiles-T133-rule-text-reduction-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `result.txt`, applicable precheck artifacts and worker review evidence.

   The report maps the Files requirements to their test selectors and identifies the changed SKILL sections. Validation contains the red and green doc-test output, formatting output, cap totals and changed-file inventory. Worker review filenames carry the required `-worker-` infix. The task-copy comparison and the format-2 consistency check verify the dispatched copy and metadata.

## Out of scope

No script changes. The implementations of verdict, audit pooling, precheck, decision checking, acceptance-record generation and next-task dispatch remain with their mechanism tasks.

The Worker Playbook step 4 sentence remains unchanged; P1-15 owns that change. The Orchestrator Playbook, Worker Playbook and other SKILL sections remain unchanged.

Rules outside the Acceptance bullet and the Delegation bullet's exemption list remain unchanged. Routing rules, permission defaults, hooks, launchers, schemas, fixtures and generated or installed copies remain unchanged.

## Check

`make format`, `uv run --no-project python -m unittest tests.unit.test_agmsg_orchestration_docs -v` and `prettier --check home/dot_config/claude/rules/agmsg-orchestration.md home/dot_agents/skills/agmsg-orchestration/SKILL.md` have their commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-rule-text-reduction-a01/validation.md`. The doc-test module and the two Markdown formatting checks are green.

The new doc tests carry red-before-documentation-edit and green-final-head evidence. An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`. No local Bats tests run.

`git diff --numstat origin/main...HEAD` shows at most 120 changed lines outside `tests/` and `.orchestration/`, and at most 150 changed lines under `tests/`. Changed lines are additions plus deletions. Validation includes both totals and the complete changed-file inventory.

The orchestrator runs the format-2 task-consistency checker, including C1 to C10 and C7b, before dispatch and at acceptance. The task copy remains byte-identical to the dispatched file. The orchestrator records a green `make check-regime-boundary` result before completion.

## Completion

The Completion clause of `.orchestration/tasks/dotfiles-T133-hold-playbook-a01.md` applies with `dotfiles-T133-rule-text-reduction-followup-a01` as the owner of any advisory P2 and `task_copy=<sha256 of .orchestration/dotfiles-T133-rule-text-reduction-a01/task.md>` in the RESULT. This task's scope, Check, `security: false`, fresh-branch rule and prohibition on `@codex review` comments govern that reference.

One PR starts from a fresh branch off `origin/main`. The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The third finding of one class stops further rounds until the orchestrator's re-plan.

The report and RESULT identify the final head, base, branch, changed files, test selectors, caps, evidence paths, task-copy hash and every Bot finding's disposition. The worker writes the RESULT key-value pairs to this task's `result.txt` before sending and includes the applicable `precheck=<sha256 of precheck.json>` evidence.

The orchestrator runs the task-level audit on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh evidence.

No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and refusal.

## Amendment 1 (round 1, 2026-10-19T04:0xZ): the Delegation bullet may be shortened

a010's question PONG (03:59:46Z): the rule file holds 447 of its 450-word budget and the new Acceptance paragraph needs about 67 words. The whole Delegation bullet of `home/dot_config/claude/rules/agmsg-orchestration.md` may be shortened, with every invariant and every exemption it states retained word for word in meaning (the exemption list itself unchanged), so the file stays within 450 words and the SKILL within 1800; the doc test asserts the budgets and that each exemption name still appears. The caps stay 120/150. Everything else stands.

## Checks (pasted by the orchestrator before each send)

```
2026-10-19T03:5xZ dispatch 1
task=dotfiles-T133-rule-text-reduction-a01 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 source=live
C-78: home/dot_agents/skills/agmsg-orchestration/SKILL.md is also in dotfiles-T133-worker-write-boundary-a01 (not yet dispatched): disjoint sections (this task: Review and integration invariants, Message Contract v1; P1-15: the Worker Playbook step 4 sentence); the later PR takes the new base with gh pr update-branch
task-consistency-check: OK
2026-10-19T04:0xZ amendment 1: task=dotfiles-T133-rule-text-reduction-a01 tasks=1 amendments=0 questions=1 results=0 withdrawn=0 revises=0 source=live
```

Runtime mechanism changes and their behavioral verification remain with P1-4 to P1-6; the interim manual exemption applies until each mechanism lands.