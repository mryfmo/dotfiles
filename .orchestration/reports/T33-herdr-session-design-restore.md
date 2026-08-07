# T33 herdr-session design restore

## Result

Restored `home/dot_local/bin/common/executable_herdr-session` exactly to
`57bcfde^`, returning to PR #75's lazy-attach design. Removed only #105's
workspace-focus assertions and reinstated the original plain-attach test.

Validation: `git diff --no-index` against a mode-preserving `57bcfde^` copy
exited 0 with no output; `git diff --check` exited 0; `make unit-test` passed
all 246 tests in 20.501 seconds.

## Review receipt

review_surface: crit-data
reviewer: codex
review_source: .orchestration/validation/T33-herdr-session-design-restore.md
review_outcome: approved

## Delivery

Branch: `fix/t33-herdr-session-restore`; commit `2d03705`.
PR: https://github.com/mryfmo/dotfiles/pull/107. The full unit-test matrix and
CodeRabbit are green; public-bootstrap jobs remain pending in GitHub Actions.
