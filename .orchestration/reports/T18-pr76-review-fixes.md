# T18 PR #76 review fixes

## Status

Ready for review.

## Findings addressed

1. Attach mode retains the unfiltered workspace pane list long enough to detect
   an existing Codex agent on another tab, warns, and skips a duplicate start.
   Order repair continues with an empty current-tab Codex pane and uses its
   existing refusal path.
2. A successful first-time `delivery.sh set turn` now tells the user that Codex
   loads the repo hook only after trusting the project `.codex` layer, with
   `/hooks` as the actionable command.
3. The fake `identities.sh` cats a fixture file verbatim, so tabs and multiple
   lines reach the shell helper. A two-identity test verifies the ambiguity
   warning while an existing turn hook prevents delivery reconfiguration.

The withdrawn direct-hook-schema finding remained unchanged because the
thread confirms Codex delivery uses the nested Stop-hook schema.

## Test-first evidence

Before implementation, the three focused regressions failed:

```text
test_attach_does_not_restart_codex_agent_from_another_tab ... FAIL
test_attach_bootstraps_agmsg_after_codex_start ... FAIL
test_attach_warns_when_multiple_agmsg_identities_exist ... FAIL
Ran 3 tests in 0.412s
FAILED (failures=3)
```

After implementation:

```text
Ran 3 tests in 0.440s
OK
```

## Validation

```text
$ uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 44 tests in 4.222s
OK

$ make unit-test
Ran 161 tests in 15.317s
OK

$ shellcheck home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ bash -n home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output
```

## Scope

Only `home/dot_local/bin/common/executable_herdr-agents` and
`tests/unit/test_herdr_agents.py` are intended for the fix commit. Existing
mise changes and orchestration history were not modified or staged. No GitHub
review thread was replied to or resolved by this worker.
