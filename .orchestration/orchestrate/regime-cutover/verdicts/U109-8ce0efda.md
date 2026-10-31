## Findings

- P2 (high) tests/unit/test_apt_mirror.py:1542: Only step.shell is checked: an inherited workflow/job defaults.run.shell can define a split-spelled /usr/bin/timeout function and source {0}, passing all 19 apt/budget tests while replacing the timeout and violating the promised bound.

## Reproduced

- Git status and HEAD checks confirmed a clean checkout at 8ce0efda3acd4fbf29c1ee3f9eff191b8fb50186.
- Unmodified test_apt_mirror run encountered host failures: unavailable offline PyYAML, unusable system Python, and denied shell temporary files.
- Unmodified four-module regression run encountered host tool and sandbox failures; it did not pass.
- Adapted in-memory harness using local PyYAML, host Python and direct shfmt pin verification: 56 apt-checker tests passed.
- Workflow- and job-level defaults.run.shell mutations produced no census, parser or tree violations.
- Inherited custom-shell mutation passed all 19 AptBoundRuleTest/BoundOrderTest tests; harmless execution printed BOUND_REMOVED after replacing timeout.
- Targeted parser-contract, capture, network-bound, pinned-install, fixture and orchestration checks: 45 tests passed.
- TypeScriptTestsStepTest: 4 tests passed.
- shfmt fixture formatting and git diff --check passed; final checkout remained clean.

## Notes

No network used; CI claims were not independently verified. The adapted harness excluded one subprocess-entrypoint test because of host shell restrictions.

Verdict: incorrect
