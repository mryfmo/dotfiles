[P1] high .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md:69 origin/main has neither a Makefile `lint` target nor a workflow invocation of `make lint` (premise replay prints `0`, exit 1), so item 2 must explicitly create and wire both.

[P1] high .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md:74 Existing hits in `home/dot_claude/hooks/executable_project-map-reload.sh:13,21`, `scripts/orchestrator/resolve-threads.sh:45`, and `scripts/orchestrator/local-advisory.sh:81` require markers in files excluded from allowed_files, making the promised green baseline impossible within scope.

[P2] high .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md:68 Item 1 provides prose rather than the required reviewable rule table, leaving no explicit mapping between individual rules, fixtures, and existing violations.

[P2] high .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md:68 Python comparisons such as `if path == "/x":` match none of the specified forbidden forms, so the lint cannot enforce its stated goal across the Python files it scans.

[P2] high .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md:70 Fixtures omit forbidden `[ = ]`, `case`, and jq `==`/`startswith`/`test` forms and allowed `cd -P`, `urllib.parse`, `canonical_path`, and `normalise_*` forms, leaving stop condition 2 unproven.

[P2] high .orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md:38 The environment threat row falsely states that no workflow is in allowed_files despite line 13 authorizing `.github/workflows/test.yaml`, so its residual assessment does not describe the proposed change.

Not checked: remote freshness because GitHub DNS failed, or implementation tests; hash, consistency checker, mask, and Completion comparison passed.
Task-file verdict: dotfiles-T129-normalised-comparison-lint-a01: revise