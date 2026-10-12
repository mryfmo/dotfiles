# Learning triage: dotfiles-T128-gate-evidence-a01

These are candidates only; nothing is promoted.

1. [memory:failure] Inside the Claude seat's sandbox, the global `commit.gpgsign` makes every `git commit` in a unit-test fixture repository fail (the signing key under `~/.ssh` is unreadable), so `tests/unit/test_require_crit_review.py` reports 73 failures on unmodified `origin/main`. Run test modules that create commits with `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`; establish the base's result before reading a failure as the change's. Applies to every worker validation run that builds git fixtures.
2. [memory:decision] A grammar change in the gate (`PR_FEEDBACK_DISPOSITION`) reaches every disposition literal in the gate's test module, not only the new tests: 17 existing `not-applicable:` literals needed the clause, or the short-reason cases would have hit the grammar error before the length rule they test. Grep the test module for the old form before writing new tests.
3. Candidate rule (not promoted): when a gate input or grammar changes, the README lines that state it to a reader are part of the change in the same section, even when the task names only the input lines; declare each such line in the report.
