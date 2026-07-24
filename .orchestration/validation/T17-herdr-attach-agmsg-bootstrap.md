# T17 validation evidence

## Test-first evidence

Before implementation, five focused tests produced three failures: start and
reuse emitted no `delivery set turn codex <repo>` call, and hook-present emitted
no identities verification. Silent absence and nonfatal behavior already
returned 0.

After implementation:

```text
test_attach_bootstraps_agmsg_after_codex_reuse ... ok
test_attach_bootstraps_agmsg_after_codex_start ... ok
test_attach_skips_delivery_when_turn_hook_exists ... ok
test_attach_skips_agmsg_silently_when_not_installed ... ok
test_attach_ignores_agmsg_bootstrap_failure ... ok
Ran 5 tests in 0.617s
OK
```

## Acceptance revision 2 red/green evidence

The hook-present fixture was first changed to the real schema:
`.hooks.Stop[].hooks[].command`. Before the jq fix, the focused regression
failed because delivery was still invoked:

```text
$ uv run python -m unittest tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists -v
test_attach_skips_delivery_when_turn_hook_exists ... FAIL
AssertionError: True is not false
Ran 1 test in 0.148s
FAILED (failures=1)
```

After changing the query to iterate `.hooks.Stop[]?.hooks[]?`:

```text
$ uv run python -m unittest tests.unit.test_herdr_agents.HerdrAgentsTest.test_attach_skips_delivery_when_turn_hook_exists -v
test_attach_skips_delivery_when_turn_hook_exists ... ok
Ran 1 test in 0.151s
OK
```

## Required validation

```text
$ uv run python -m unittest tests.unit.test_herdr_agents -v
Ran 42 tests in 3.576s
OK

$ make unit-test
uv run python -m unittest discover -s tests/unit -v
Ran 159 tests in 14.574s
OK

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ shellcheck home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ bash -n home/dot_local/bin/common/executable_herdr-agents
# exit 0, no output

$ git diff --check
# exit 0, no output
```

Task-owned status:

```text
 M home/dot_config/claude/rules/agmsg-orchestration.md
 M home/dot_local/bin/common/executable_herdr-agents
 M tests/unit/test_herdr_agents.py
?? .orchestration/autoskill/runs/T17-herdr-attach-agmsg-bootstrap.md
?? .orchestration/learning/T17-herdr-attach-agmsg-bootstrap.md
?? .orchestration/reports/T17-herdr-attach-agmsg-bootstrap.md
?? .orchestration/sandboxes/T17-herdr-attach-agmsg-bootstrap.md
?? .orchestration/validation/T17-herdr-attach-agmsg-bootstrap.md
```
