---
task_id: dotfiles-T128-s1-replan-gate-a01
status: pre_push_checkpoint
---

The acceptance gate now refuses a non-advisory finding class at three or more ledger rows unless the record body has a matching re-plan line. The counters show re-plan=present or missing before source=record, and advisory-p2 has no S1 line. The exact prefix is re-plan: <class> -> followed on that same line by the words specification, design, implementation and verification. Both tools tokenize Unicode letters, numbers and underscore consistently; the existing S6 records-search checks still apply to every class, including advisory-p2. This changes the user-visible merge decision as requested; no policy bypass or threshold change.

Exactly six new tests:
- RegimeCountersTest.test_s1_reports_replan_present_for_the_class
- RegimeCountersTest.test_s1_reports_replan_missing_without_a_complete_matching_line
- RegimeCountersTest.test_s1_excludes_advisory_p2_at_three_rows
- ReviewGuardTest.test_s1_class_at_three_without_a_replan_line_is_refused
- ReviewGuardTest.test_s1_class_at_three_with_all_replan_words_is_accepted
- ReviewGuardTest.test_s1_class_at_three_with_a_missing_replan_word_is_refused

The negative cases and new counter token/advisory behavior fail before implementation; the gate's positive complete-line test passes baseline as expected. The first gate attempt failed earlier because global Git signing prevented temporary fixture commits; a test-process-only commit.gpgsign=false override exposed the intended S1 failures. No persistent Git configuration changed. All 126 tests in the requested modules pass after the final fix (88.427s), as do ShellCheck, shfmt, Ruff format, Prettier and source/test whitespace. The two old S1 assertions, shared fixture and write_record helper are the only other test changes. The fixture adds one re-plan line plus the blank line Prettier requires.

Independent local review found one P2, class replan-word-boundary: Python and jq native Unicode boundaries disagreed for design followed by U+0301. It was fixed before the first commit by exact token membership in both implementations; the existing new positive tests cover it. A new counter regression subcase failed before that fix. Independent rereview verified 12 actual-tool cases and approved the diff with no further finding. Both resolved records are in s1-worker-crit.json; s1-worker-review-receipt.md records addressed outcome. Parent read the evidence and the worker review gate passes. This is process evidence, not authentication or a task-level integration audit. This local finding is reported for the task's finding-class accounting; no class has reached three in this worker round.

Fresh branch fix/s1-replan-gate is based on f7847616970d6bd83739a75a65ad8f7c35e91462. Only the five allowed source/test/fixture paths change outside artifacts. Source changed: 29 <= 200; test additions: 105 <= 1000. Task copy SHA256:072564c75c137fffd42d54a6d7bcf86dcd7917e49cc3fa2ae6bf8a0b0ce8072e, byte-identical. The reader's public return shape and all callers remain unchanged; record body scanning is localized beside S6. No workflow, new production script, dependency, interpreter/configuration or unrelated behavior changes.

This checkpoint commits task.md plus report.md, validation.md, sandbox.md, learning.md and autoskill.md. Plan/todo and worker review JSON/receipt stay untracked. Final commit/PR identifiers and post-push CI/Bot outputs will be captured in report-final.md and validation-final.md without changing the final head; RESULT names those supplements and the five checkpoint records. No PR is claimed created at this checkpoint.

Prior PR375/PR379 branches and all untracked evidence are preserved. All commands ran inside the managed sandbox, with no escalation; UV cache is under /tmp and fixture signing disabled only in the test environment. The source graph was queried and found stale, so targeted rg covered callers; no graph-update hook fired or update ran. No Crit server, Plan Mode, AutoSkill, local Bats, live store mutation, memory promotion or merge. The tests use isolated temporary records/history and stub GitHub reads. Integration review/sweep/audit/dispositions/gate/merge remain orchestrator work; final-head CI and Bot will be awaited concurrently under Worker Playbook15. Third finding of one class stops further rounds pending the orchestrator's re-plan.

cost: n/a
