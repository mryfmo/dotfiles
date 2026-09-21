# dot-residuals-T1-a01 validation

## Test-first RED

Command:

```text
uv run python -m unittest -v tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable
```

Verbatim result before implementation:

```text
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... FAIL
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... FAIL
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... FAIL
test_missing_crit_asset_is_repairable (tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable) ... ERROR

Ran 4 tests in 0.180s

FAILED (failures=3, errors=1)
```

The failures were the expected missing guards, missing recurring call, shadow-triggered download, and absent repair mapping.

## Focused final tests

Command: same four-test command as above.

```text
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_missing_crit_asset_is_repairable (tests.unit.test_check_agent_runtime.CheckAgentRuntimeTest.test_missing_crit_asset_is_repairable) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.105s

OK
```

## Related unit suites

Command:

```text
uv run python -m unittest tests.unit.test_runtime_health tests.unit.test_asset_manifest tests.unit.test_check_agent_runtime
```

Verbatim output:

```text
...........................................................................
----------------------------------------------------------------------
Ran 75 tests in 9.010s

OK
```

`make unit-test` and a quiet full discovery were also run and exited 0. The full discovery emitted existing ResourceWarnings for unclosed test SQLite connections plus expected fixture diagnostics for deliberately invalid model profiles.

## Shell and diff validation

Commands, each exit 0 with no output:

```text
bash -n home/dot_bash/client/bashrc install/common/gh_extensions.sh scripts/update-agent-assets.sh
shfmt --indent 4 --space-redirects --diff home/dot_bash/client/bashrc install/common/gh_extensions.sh scripts/update-agent-assets.sh tests/install/common/gh_extensions.bats
shellcheck -x -e SC1090,SC1091,SC2015 home/dot_bash/client/bashrc && shellcheck -x install/common/gh_extensions.sh scripts/update-agent-assets.sh
git diff --check
```

The three ShellCheck exclusions are existing findings in the Ubuntu-derived client bashrc; the changed private-source lines add no new finding.

## Agent-asset validation

Command:

```text
make validate-agent-assets
```

Verbatim output:

```text
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```

## GitHub extension convergence traces

Unauthenticated followed by authenticated retry through `ensure_gh_extensions`:

```text
Warning: GitHub CLI is not authenticated. Run setup-gh, then make update to install extensions.
gh extension install seachicken/gh-poi
```

Installed extension preservation fixture:

```text
installed-extension-preserved
```

The initial preservation check returned 99 and printed `unexpected: extension install seachicken/gh-poi`; this exposed whitespace parsing of the display name. Changing the list parser to tab-delimited fields fixed the root cause.

## `adh-test` public/private bashrc E2E

The final credential-free scratch-user run used only `limactl shell adh-test` and the mounted worktree. Verbatim output:

```text
public-only stderr: 0 private-source errors
private-prompt
private-aliases
scratch cleanup: OK
```

An earlier scratch run also cleaned up successfully but rendered both marker names on one line because its temporary stand-in scripts used an over-escaped newline; the final run above corrected only the fixture and verified exact lines.

## CompactionDB

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-residuals-T1-a01: make update reuses install/common/gh_extensions.sh to install only missing authenticated gh extensions; Linux Crit resolution treats ~/.local/bin/crit as authoritative and make doctor may repair the ensure_crit_cli manifest step.'
```

Verbatim output:

```text
efc9f127-c02a-40a4-b4b6-bc335c7d90ba
```

## Agent Crit data review gate

Initial gate output:

```text
Native agent review required before completion.
- agent lifecycle path changed: scripts/check-agent-runtime.py
- broad diff touches 9 files
- broad diff changes 238 lines
make: *** [require-crit-review] Error 1
```

`crit status --json` initially reported no review file. Browser Crit is prohibited by repository instructions, so Codex used headless `crit comment`, resolved review-scope approval `r_1c1148`, and saved the JSON under `.agents/worklog/codex/review/`.

Final command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-residuals-T1-a01-receipt.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Deliberately not run

```text
bats: NOT RUN locally (task and repository policy require CI)
git commit: NOT RUN
git push: NOT RUN
```
