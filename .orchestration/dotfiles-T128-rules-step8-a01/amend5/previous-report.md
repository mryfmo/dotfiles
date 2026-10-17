# RESULT: dotfiles-T128-rules-step8-a01 amendment 1

status: blocked-on-Bot-P2-task-direction; implementation committed and all CI green, not merge-ready.
Head: becba33c616247057f2f75cf30ec5aefcbf00592
Base / GitHub base: 8b25f9ca6d6bc25c21b30f2a67cb462a6dd4a95e
Branch: fix/regime-rules-step8
PR: https://github.com/mryfmo/dotfiles/pull/371 (OPEN, ready, MERGEABLE)
Task-copy SHA256: 95185488d062644c2adba7a30e502d7e364e80db96b5a545551ca2f9f6221919

## Implementation

[memory:decision] Standing prose states the advisory-P2 owner and small in-scope revise policy once in step10, the one worker-side P0/P1 fix round and surviving-item operator decision, final-head audit authority, landed shape/invariant hand checks and S6 searches, and platform-conditional Claude sandbox facts. Codex in-sandbox execution and existing merge/feedback guards remain. The exact amendment1 Boundaries bullet adds the daily limit while shortening its own second sentence; unchanged450-word test passes. No mechanism or permission configuration changed.

Four prose files: AGENTS.md, home/dot_agents/skills/agmsg-orchestration/SKILL.md, home/dot_config/claude/rules/pr-integration.md, home/dot_config/claude/rules/agmsg-orchestration.md. Test module: tests/unit/test_agmsg_orchestration_docs.py. Four declared fixtures: invariants.md, worker-step-15.md, message-contract.md, code-review-orchestration.md under tests/fixtures/regime. Other two pinned fixtures untouched. Task and worker-review JSON/receipt committed; reports/logs/worklogs untracked for orchestrator sync. Source45 changed lines of200; tests61 added lines of1000.

Four new tests: test_skill_names_no_unlanded_mechanism, test_skill_sandbox_text_names_both_platforms, test_step_10_states_the_advisory_p2_policy, test_advisory_rows_are_excluded_from_the_class_counts. They failed red first. Existing48 tests retained, renamed where old rule wording required. All52 pass; render-check, native Ruff format, source/test whitespace and D6 counts0and0 pass. Independent read-only review and amendment delta review had no findings; local review gate passes with saved resolved JSON/receipt. The later Bot finding below is not erased by that earlier review. Local pre-commit config absent; none added outside task scope. No local bats.

## Publication and CI

Normal in-sandbox HTTPS push succeeded without -u/shared config edits. Commit signing disabled for sandbox key access. Nonfatal packed-refs.lock read-only warning occurred on switch and commit; correct branch/head confirmed. gh used first for GitHub; no browser/web fallback. PR created draft then ready at2026-10-15T23:21:52Z. All checks pass, including all four unit-test environments, public/private bootstraps, Agent assets and secret checks. CodeRabbit status success means automatic review skipped. Initial gh checks watcher exited1 on API transport error, not a check failure; restarted watcher exited0 with all checks green. Full watcher output in ci-watch.txt; final API snapshot in validation.md.

## Bot finding and required next action

bot_rounds=1, fix_rounds=0. Final-head review5541108807 (https://github.com/mryfmo/dotfiles/pull/371#pullrequestreview-5541108807) completed with one P2 inline finding4289271574 at home/dot_config/claude/rules/agmsg-orchestration.md:13 (https://github.com/mryfmo/dotfiles/pull/371#discussion_r4289271574). No P0/P1 or review-body finding. Security review completed with no findings (final structured summary in bot-final-summary.json).

The P2 is substantive: exact mandated Boundaries text reads as if make check-regime-boundary enforces the new once-a-day limit, but the checker has no date/history check, and existing SKILL permits a date-2 boundary and another auto-merge. Local rg over the named checker confirms no daily/history enforcement path. Mechanism code is explicitly out of scope; changing the exact mandated clause requires task direction. Sent PONG status=question requesting a C-50 check-scoped revise/amendment for the small doc correction, or an orchestrator-owned advisory task/disposition. No reply yet at handoff. No worker reply/resolve, code edit or fabricated disposition.

Proposed handling: a C-50 revise with a check for the doc wording, since this is the PR's own small allowed-file change. If the orchestrator judges it advisory instead, candidate owner is dotfiles-T128-rules-step8-followup-a01 and candidate disposition is not-applicable:advisory P2 owned by dotfiles-T128-rules-step8-followup-a01, valid only after that owner task file exists and the owned row is written. This is a conditional proposal, not an applied disposition or a claim that owner exists. P2 remains unresolved; gate/merge must wait for proper handling.

## Evidence and limits

report.md, validation.md, sandbox.md, learning.md, autoskill.md, ci-watch.txt, bot-reviews.json, bot-comments.json, bot-issue-comments.json, bot-final-summary.json and bot-status.txt under this task directory are untracked in worker-e at the same relative paths; orchestrator must sync by absolute path before review/audit. task.md and the -worker-crit.json/-worker-review-receipt.md files are committed. Worklogs uncommitted; plan active, todo waiting task direction. Current tracked tree is clean. Prior T15 branch and artifacts preserved.

Platform faults were supplied task facts, not live reproduced. No installed apply/restart, dependency manifest edit, sandbox-policy edit, graph update, Plan Mode, Crit server, outside-sandbox execution or merge. Graph summaries read and graph found stale; no auto-update hook fired. Main-checkout CompactionDB consolidation remains orchestrator-owned. After integration, operator applies dotfiles and restarts Claude Code.

cost: n/a
