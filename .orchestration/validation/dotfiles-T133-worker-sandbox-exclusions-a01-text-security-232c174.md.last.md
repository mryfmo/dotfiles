[P2] high .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a01.md:35 — The clean-environment control covers only line 100: generation and checks still invoke bare `uv`, `ruff` and Makefile recipes through this host’s mise-first PATH; subsequent Git commands retain inherited `GIT_*`. The sanitized test process does not bind those executions or their repository inputs.

[P2] high .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a01.md:94 — No specified CI step launches a Linux Claude sandbox and exercises the removed exclusions; existing CI and the proposed tests validate rendering, while the PONG runs from Codex on this host. Thus “Linux seats are measured in CI” is unsupported; require a named runtime probe or explicitly leave Linux runtime unmeasured. [Runtime verification guidance](https://code.claude.com/docs/en/sandboxing#confirm-commands-run-inside-the-sandbox).

[P2] high .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a01.md:10 — `tests/unit/test_claude_settings_merge.py:591` asserts the old exclusion lists for both platforms against the committed template, so the required change necessarily breaks CI; this test file needs an authorized update and its own threat row.

[P2] medium .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-a01.md:33 — The named validator test checks empty/non-empty input acceptance, but importing the PR-controlled validator can perform unrelated side effects while returning the expected results; that test cannot close the broad “in-process effects” row. Narrow the claim or classify those effects as residual under independent review.

Reviewed all 26 threat rows and the related acceptance/review records. Explicitly acknowledged same-UID substitution, symlink/case-alias risks and deferred live deployment are not treated as newly closed boundaries.

📝 まとめ: Completed the read-only pre-dispatch review; four findings remain for the orchestrator’s disposition.
Not checked: implementation, test execution or live enforcement; no files changed, and runtime confinement remains unverified.
Verdict: incorrect