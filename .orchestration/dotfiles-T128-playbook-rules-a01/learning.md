# Learning triage: dotfiles-T128-playbook-rules-a01

These are candidates only; nothing is promoted.

1. [memory:decision] Before placing a token "beside" another in a SKILL command, grep every test module for the command's substring, not only the module the task names. `tests/unit/test_pr_feedback.py` pins `BASE=origin/main PR_FEEDBACK_EVIDENCE=<json> make require-crit-review` as one substring, so a new gate variable goes before `BASE=` unless the task lists that module.
2. [memory:decision] Generate a pinned-section fixture with the test's own `section` and `normalized` functions (import the test module from a scratch script) rather than transcribing it. Then compare the fixture's word diff with the prose's word diff to show the declared change is the only one.
3. [memory:failure] The repository masker reads a unittest subTest label (the keyword `token` followed by an equals sign and a quoted value) as a secret pattern, and so does the secret scan of `make validate-agent-assets`, even in prose that only spells the form out. When the label holds an apostrophe ("task's"), one match ran past the line end and swallowed the next line: 181 lines became 179, with no error. Print evidence without subTest labels (test name and FAIL count), and compare the line count before and after masking.
