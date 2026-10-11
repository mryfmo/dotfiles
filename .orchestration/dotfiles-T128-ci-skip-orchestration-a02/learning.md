# Learning triage: dotfiles-T128-ci-skip-orchestration-a02

These are candidates only; nothing is promoted.

1. [memory:failure] A hand-written YAML reader that accepts some forms and skips the rest is fail-open: each skipped form is a key the test cannot see while GitHub obeys it (spaced, escaped and quoted keys, flow mappings, a body shifted off its column). Make the reader raise on anything outside the one form it parses, check positions as well as forms, and show the hidden key with a real parser (`uv run --with pyyaml`) beside each mutation.
2. [memory:decision] A test that replaces a revise check under a reset is named in the report together with the selector it retires. The superseded task's `revise.yaml` stays as history, but its selector no longer resolves.
3. [memory:failure] `FAILED (errors=N)` counts failing subTests, not tests. When a proof shows "13 tests, 12 errors", paste the `-v` list of the tests that still pass, and say why each passes, so no structural test looks like it slipped through.
