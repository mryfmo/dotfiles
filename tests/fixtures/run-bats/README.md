# run-bats fixture

`timing-stream.txt` is the `--formatter cat --timing` stream Bats 1.14.0 (the `home/dot_mise/config.toml` pin) printed on 2026-10-31 for `two-tests.bats` (`bats --formatter cat --timing two-tests.bats`, exit 0), recorded for `tests/unit/test_run_bats.py` and `scripts/ci/run-bats.py` (regime-cutover U128). One edit: the `suite` line's absolute path became the repository-relative one; the wrapper drops `suite` lines unread.

The result line's form, which the test pins: `ok <n> <name> in <ms>ms`, the duration after the name, before any ` # skip <reason>` directive. A failing test prints `not ok <n> <name> in <ms>ms` in the same run session (observed, not recorded: the fixture's run passes so the wrapper test asserts exit 0). Without `--timing` the lines end at the name.
