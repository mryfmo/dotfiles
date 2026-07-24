# T19 bootstrap HOME guard

## Status

Ready for review on `fix/herdr-bootstrap-home-guard`.

## Change

`bootstrap_agmsg` now compares canonical `workdir` and `$HOME` paths before
touching delivery or identity scripts. When they match, it prints one stderr
line and returns successfully, preventing user-level `.codex/hooks.json`
registration. The guard sits in the shared helper used by attach, reused, and
new workspace paths.

## Test-first evidence

Before implementation:

```text
test_full_mode_skips_agmsg_bootstrap_for_home ... FAIL
AssertionError: 'Skipping agmsg bootstrap for $HOME' not found
Ran 1 test in 0.430s
FAILED (failures=1)
```

After implementation:

```text
test_full_mode_skips_agmsg_bootstrap_for_home ... ok
Ran 1 test in 0.319s
OK
```

The regression sets the helper workdir to its fake `$HOME`, asserts the skip
note, and proves neither `delivery.sh` nor `identities.sh` is invoked.

## Validation

```text
$ uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 45 tests in 4.441s
OK

$ make unit-test
Ran 162 tests in 15.824s
OK

$ shellcheck home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ bash -n home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ git diff --check
# exit 0, no output
```

## Scope

Implementation used an isolated worktree based on main commit `0e33ebe`.
Only the Herdr helper and its unit test are intended for the commit; the
primary worktree and existing orchestration history were left untouched.
