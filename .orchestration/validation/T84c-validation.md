# T84c Validation

## Rename sweep

Initial full `tests/` hit list:

```text
tests/install/common/lifecycle.bats:384:    grep -q 'model = ' home/dot_codex/modify_standard.config.toml
```

After the edit:

```sh
rg -n 'modify_(deep|express|review|security|standard)\.config\.toml' tests
# no output; zero misses
```

The renamed target exists, and line 384 now references `home/dot_codex/modify_private_standard.config.toml`.

The same literal-old-name regex returned no matches in `README.md`, `docs/`, `scripts/`, `home/`, `tests/`, or `Makefile`. The remaining repository-wide matches are intentionally unchanged:

- `.orchestration/`: immutable historical task, report, validation, and sandbox evidence (38 matches at inventory time, including the current task's problem statement).
- `.ua/`: generated knowledge-graph and fingerprint snapshots from before the accepted rename (35 matches); T84c does not own knowledge-graph regeneration.

## Syntax and gates

Direct `bash -n tests/install/common/lifecycle.bats` stops at line 9 because Bash does not parse Bats' existing `@test "..." {` syntax. Without running Bats, the test bodies were normalized to ordinary function declarations and checked:

```sh
awk '/^@test / { n++; print "test_" n "() {"; next } { print }' tests/install/common/lifecycle.bats | bash -n
# exit 0

make format
# exit 0

make validate-agent-assets
# agent asset validation ok

make unit-test
# Ran 342 tests in 35.046s — OK

git diff --check -- tests/install/common/lifecycle.bats
# exit 0
```

Local Bats execution was intentionally omitted per repository policy and task prohibition.
