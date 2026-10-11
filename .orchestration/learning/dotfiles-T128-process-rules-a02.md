# Learning triage: dotfiles-T128-process-rules-a02 (with the a01 items)

These are candidates only; nothing is promoted.

1. [memory:failure] Two in-flight PRs that edit the same SKILL paragraph, or the line next to the other's insertion, conflict on merge. Compare the other PR's hunk headers (`gh pr diff <n> | awk` on the file) before editing a shared prose file, and keep a separating unchanged line (here: Orchestrator Playbook step 3 and the line before PR 317's step 16).
2. [memory:failure] The Codex connector's summary comment carries one `status` for the whole comment: `"status":"completed"` appears as soon as the security review finishes while the code review is still running. A Bot wait has to read the Code Review row, a review object or the 👍 reaction, not the comment's status marker.
3. [memory:decision] Docs tests scoped to the section that owns the rule (split on the section heading) make the "fails when its sentence is removed" proof real: the same token elsewhere in the file cannot satisfy them.

## a02 (reset continuation)

4. [memory:decision] A prose rule that states a value grammar (a regex, a placeholder list) draws the same review finding class head after head; put the shape in the schema (`schemas/task.json`) and leave the prose to substance. Plan 006 S1 reset PR 318 on exactly this class.
5. [memory:failure] Replacing a rule sentence verbatim breaks every test that pinned the old sentence; grep the test file for the replaced text before committing (here `test_code_review_rules_cover_orchestration_records_and_threat_tables`).
