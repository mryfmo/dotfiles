# Validation: dotfiles-T128-v0-main-tests-a01

Revise round 1. Final head `32fe9a36a6ca67670e54bbcb1c506ca391d9dd32` on `feat/main-tests`, PR #317 (round 0 ended at `adcf783b`). Every block is the verbatim output of the command above it.

## §R Revise round 1: the checks fail on adcf783b's code and pass at the final head

On `adcf783b`'s harness, helper and workflow (written into the worktree from that commit and restored with `git checkout`), with the final head's tests:

```
$ git rev-parse HEAD; for f in scripts/main-tests.sh scripts/lib/contract_markers.py .github/workflows/test.yaml; do git show adcf783b:$f > $f; done; git diff --stat
32fe9a36a6ca67670e54bbcb1c506ca391d9dd32
 .github/workflows/test.yaml     | 34 +++++++++++-------------
 scripts/lib/contract_markers.py | 22 ++++++----------
 scripts/main-tests.sh           | 58 ++++++++++++-----------------------------
 3 files changed, 40 insertions(+), 74 deletions(-)
$ (cd tests/unit && uv run python -m unittest test_main_tests.MainTestsHarnessTest.test_nothing_from_the_pr_runs_before_mains_harness test_main_tests.MainTestsHarnessTest.test_a_planted_venv_is_not_used test_main_tests.MainTestsHarnessTest.test_a_zero_exit_without_a_summary_fails test_main_tests.MainTestsHarnessTest.test_a_short_contract_summary_fails test_main_tests.MainTestsHarnessTest.test_a_declared_module_without_its_script_stays_undeclared test_main_tests.MainTestsHarnessTest.test_a_renamed_script_still_triggers test_main_tests.MainTestsHarnessTest.test_an_empty_contract_class_is_no_contract) 2>&1 | grep -E '^(FAIL|ERROR):|^AssertionError|^Ran |^OK|^FAILED' | cut -c1-230
FAIL: test_nothing_from_the_pr_runs_before_mains_harness (test_main_tests.MainTestsHarnessTest.test_nothing_from_the_pr_runs_before_mains_harness) (line='source scripts/lib/github-release.sh')
AssertionError: False is not true : source scripts/lib/github-release.sh
FAIL: test_nothing_from_the_pr_runs_before_mains_harness (test_main_tests.MainTestsHarnessTest.test_nothing_from_the_pr_runs_before_mains_harness)
AssertionError: 'git show origin/main:scripts/lib/github-release.sh > "${RUNNER_TEMP}/scripts/lib/github-release.sh"' not found in '\n  main-tests:\n    # main\'s tests/unit judge this change (T128 INV-12, scripts/main-tests.sh).\
FAIL: test_a_planted_venv_is_not_used (test_main_tests.MainTestsHarnessTest.test_a_planted_venv_is_not_used)
AssertionError: True is not false : uv ran the PR's .venv interpreter
FAIL: test_a_zero_exit_without_a_summary_fails (test_main_tests.MainTestsHarnessTest.test_a_zero_exit_without_a_summary_fails)
AssertionError: 0 == 0 : main-tests: undeclared mode, main's modules as they are: test_bar test_baz test_foo
FAIL: test_a_short_contract_summary_fails (test_main_tests.MainTestsHarnessTest.test_a_short_contract_summary_fails)
AssertionError: 0 == 0 : main-tests: undeclared mode, main's modules as they are: test_bar test_foo
Ran 3 tests in 0.000s
OK (skipped=1)
Ran 1 test in 0.001s
OK
FAIL: test_a_declared_module_without_its_script_stays_undeclared (test_main_tests.MainTestsHarnessTest.test_a_declared_module_without_its_script_stays_undeclared)
AssertionError: 0 == 0 : main-tests: undeclared mode, main's modules as they are: test_bar
Ran 1 test in 0.000s
OK
Ran 1 test in 0.000s
OK
FAIL: test_a_renamed_script_still_triggers (test_main_tests.MainTestsHarnessTest.test_a_renamed_script_still_triggers)
AssertionError: 0 == 0 : main-tests: no script change
FAIL: test_an_empty_contract_class_is_no_contract (test_main_tests.MainTestsHarnessTest.test_an_empty_contract_class_is_no_contract)
AssertionError: 'main-tests: no contract on main for tests/unit/test_bar.py' not found in "main-tests: undeclared mode, main's modules as they are: test_foo\nmain-tests: declared mode, main's contracts with REGIME_CONTRACT=1: test
Ran 7 tests in 3.892s
FAILED (failures=8)
$ git checkout -- scripts/main-tests.sh scripts/lib/contract_markers.py .github/workflows/test.yaml; git status --short
```

At the final head:

```
$ git rev-parse HEAD
32fe9a36a6ca67670e54bbcb1c506ca391d9dd32
$ (cd tests/unit && uv run python -m unittest -v test_main_tests.MainTestsHarnessTest.test_nothing_from_the_pr_runs_before_mains_harness test_main_tests.MainTestsHarnessTest.test_a_planted_venv_is_not_used test_main_tests.MainTestsHarnessTest.test_a_zero_exit_without_a_summary_fails test_main_tests.MainTestsHarnessTest.test_a_short_contract_summary_fails test_main_tests.MainTestsHarnessTest.test_a_declared_module_without_its_script_stays_undeclared test_main_tests.MainTestsHarnessTest.test_a_renamed_script_still_triggers test_main_tests.MainTestsHarnessTest.test_an_empty_contract_class_is_no_contract)
test_nothing_from_the_pr_runs_before_mains_harness (test_main_tests.MainTestsHarnessTest.test_nothing_from_the_pr_runs_before_mains_harness) ... ok
test_a_planted_venv_is_not_used (test_main_tests.MainTestsHarnessTest.test_a_planted_venv_is_not_used) ... ok
test_a_zero_exit_without_a_summary_fails (test_main_tests.MainTestsHarnessTest.test_a_zero_exit_without_a_summary_fails) ... ok
test_a_short_contract_summary_fails (test_main_tests.MainTestsHarnessTest.test_a_short_contract_summary_fails) ... ok
test_a_declared_module_without_its_script_stays_undeclared (test_main_tests.MainTestsHarnessTest.test_a_declared_module_without_its_script_stays_undeclared) ... ok
test_a_renamed_script_still_triggers (test_main_tests.MainTestsHarnessTest.test_a_renamed_script_still_triggers) ... ok
test_an_empty_contract_class_is_no_contract (test_main_tests.MainTestsHarnessTest.test_an_empty_contract_class_is_no_contract) ... ok

----------------------------------------------------------------------
Ran 7 tests in 4.149s

OK
[exit 0]
```

Finding 2: which uv forms execute a planted `.venv` interpreter (`--isolated` does; an explicit `--python` does not):

```
$ # in a directory whose .venv/bin/python (and python3) appends to ./RAN and exits 0; each form below runs from that directory
$ uv run --no-config --no-project python -c pass  -> rc=0 planted-interpreter-ran=yes
$ uv run --no-config --no-project --quiet --with pyyaml python3 -c pass  -> rc=0 planted-interpreter-ran=yes
$ uv run --isolated --no-config --no-project python -c pass  -> rc=0 planted-interpreter-ran=yes
$ uv run --no-config --no-project --python $(cd / && uv python find --no-config) python -c pass  -> rc=0 planted-interpreter-ran=no
```

## §1 Local checks at the final head

```
$ git rev-parse HEAD
32fe9a36a6ca67670e54bbcb1c506ca391d9dd32
[exit 0]

$ shasum -a 256 .orchestration/dotfiles-T128-v0-main-tests-a01/task.md
61554db0d12e73fabd3ba04d078fc29c42a93bbb3fdca3c2ddd129181ff8996f  .orchestration/dotfiles-T128-v0-main-tests-a01/task.md
[exit 0]

$ cat .orchestration/dotfiles-T128-v0-main-tests-a01/revise.yaml
round: 1
previous_head: adcf783b06d9081280991a3727f8a21c3c61ac85
checks:
  - tests/unit/test_main_tests.py::test_nothing_from_the_pr_runs_before_mains_harness
  - tests/unit/test_main_tests.py::test_a_planted_venv_is_not_used
  - tests/unit/test_main_tests.py::test_a_zero_exit_without_a_summary_fails
  - tests/unit/test_main_tests.py::test_a_declared_module_without_its_script_stays_undeclared
  - tests/unit/test_main_tests.py::test_a_renamed_script_still_triggers
  - tests/unit/test_main_tests.py::test_an_empty_contract_class_is_no_contract
[exit 0]

$ uv run python -m unittest discover -s tests/unit -v -p 'test_main_tests.py'
test_a_declared_module_without_its_script_stays_undeclared (test_main_tests.MainTestsHarnessTest.test_a_declared_module_without_its_script_stays_undeclared) ... ok
test_a_declared_script_meets_mains_contract_only (test_main_tests.MainTestsHarnessTest.test_a_declared_script_meets_mains_contract_only) ... ok
test_a_deleted_module_still_runs_from_main (test_main_tests.MainTestsHarnessTest.test_a_deleted_module_still_runs_from_main) ... ok
test_a_design_tier_module_needs_a_contract_on_main (test_main_tests.MainTestsHarnessTest.test_a_design_tier_module_needs_a_contract_on_main) ... ok
test_a_helper_failure_fails_the_run (test_main_tests.MainTestsHarnessTest.test_a_helper_failure_fails_the_run) ... ok
test_a_planted_venv_is_not_used (test_main_tests.MainTestsHarnessTest.test_a_planted_venv_is_not_used) ... ok
test_a_renamed_script_still_triggers (test_main_tests.MainTestsHarnessTest.test_a_renamed_script_still_triggers) ... ok
test_a_short_contract_summary_fails (test_main_tests.MainTestsHarnessTest.test_a_short_contract_summary_fails) ... ok
test_a_uv_config_the_pr_plants_is_ignored (test_main_tests.MainTestsHarnessTest.test_a_uv_config_the_pr_plants_is_ignored) ... ok
test_a_zero_exit_without_a_summary_fails (test_main_tests.MainTestsHarnessTest.test_a_zero_exit_without_a_summary_fails) ... ok
test_aliased_and_inline_contracts_are_still_dormant (test_main_tests.MainTestsHarnessTest.test_aliased_and_inline_contracts_are_still_dormant) ... ok
test_an_empty_contract_class_is_no_contract (test_main_tests.MainTestsHarnessTest.test_an_empty_contract_class_is_no_contract) ... ok
test_an_implementation_must_promote_its_contracts (test_main_tests.MainTestsHarnessTest.test_an_implementation_must_promote_its_contracts) ... ok
test_an_install_change_triggers_the_run (test_main_tests.MainTestsHarnessTest.test_an_install_change_triggers_the_run) ... ok
test_an_undeclared_script_change_meets_mains_ordinary_tests (test_main_tests.MainTestsHarnessTest.test_an_undeclared_script_change_meets_mains_ordinary_tests) ... ok
test_design_scripts_need_declared_modules_that_exist (test_main_tests.MainTestsHarnessTest.test_design_scripts_need_declared_modules_that_exist) ... ok
test_files_the_pr_plants_cannot_replace_mains_runner (test_main_tests.MainTestsHarnessTest.test_files_the_pr_plants_cannot_replace_mains_runner) ... ok
test_more_than_one_task_file_fails (test_main_tests.MainTestsHarnessTest.test_more_than_one_task_file_fails) ... ok
test_no_script_change_skips (test_main_tests.MainTestsHarnessTest.test_no_script_change_skips) ... ok
test_nothing_from_the_pr_runs_before_mains_harness (test_main_tests.MainTestsHarnessTest.test_nothing_from_the_pr_runs_before_mains_harness) ... ok

----------------------------------------------------------------------
Ran 20 tests in 24.166s

OK
[exit 0]

$ uv run python -m unittest discover -s tests/unit -v -p 'test_contract_markers.py'
test_a_decorated_class_contributes_its_test_methods_only (test_contract_markers.ContractMarkersTest.test_a_decorated_class_contributes_its_test_methods_only) ... ok
test_a_missing_or_unknown_tier_is_design (test_contract_markers.ContractMarkersTest.test_a_missing_or_unknown_tier_is_design) ... ok
test_a_nested_contract_still_counts_as_dormant (test_contract_markers.ContractMarkersTest.test_a_nested_contract_still_counts_as_dormant) ... ok
test_design_scripts_need_their_module (test_contract_markers.ContractMarkersTest.test_design_scripts_need_their_module) ... ok
test_every_form_is_found_on_its_method (test_contract_markers.ContractMarkersTest.test_every_form_is_found_on_its_method) ... ok
test_malformed_task_files_fail_closed (test_contract_markers.ContractMarkersTest.test_malformed_task_files_fail_closed) ... ok
test_only_a_module_whose_script_is_declared_is_exempt (test_contract_markers.ContractMarkersTest.test_only_a_module_whose_script_is_declared_is_exempt) ... ok
test_scripts_filters_script_paths (test_contract_markers.ContractMarkersTest.test_scripts_filters_script_paths) ... ok
test_task_lists_id_tier_and_declared_modules (test_contract_markers.ContractMarkersTest.test_task_lists_id_tier_and_declared_modules) ... ok
test_undecorated_and_unrelated_decorators_are_not_contracts (test_contract_markers.ContractMarkersTest.test_undecorated_and_unrelated_decorators_are_not_contracts) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.917s

OK
[exit 0]

$ uv run python -m unittest discover -s tests/unit -p 'test_workflow_security.py'
........
----------------------------------------------------------------------
Ran 8 tests in 0.003s

OK
[exit 0]

$ uv run python -m unittest discover -s tests/unit -p 'test_files_fixture.py'
...
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
[exit 0]

$ uv run python -m unittest discover -s tests/unit -p 'test_statusline_tools.py'
.....
----------------------------------------------------------------------
Ran 5 tests in 0.591s

OK
[exit 0]

$ uv run python -m unittest discover -s tests/unit -p 'test_agmsg_orchestration_docs.py'
.................
----------------------------------------------------------------------
Ran 17 tests in 0.009s

OK
[exit 0]

$ shellcheck -x scripts/main-tests.sh
[exit 0]

$ shfmt -i 4 -sr -d scripts/main-tests.sh
[exit 0]

$ ruff format --config ruff.toml --check scripts/lib/contract_markers.py tests/unit/regime_contract.py tests/unit/test_contract_markers.py tests/unit/test_main_tests.py
4 files already formatted
[exit 0]

$ prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md
Checking formatting...
All matched files use Prettier code style!
[exit 0]

$ uv run --no-project --quiet --with pyyaml python -c 'import yaml; d = yaml.safe_load(open(".github/workflows/test.yaml")); j = d["jobs"]["main-tests"]; print(list(d["jobs"]), j["needs"], j["runs-on"], "if" in j, [s["name"] for s in j["steps"]])'
['changes', 'main-tests', 'test'] changes ubuntu-24.04 False ['Configure Git defaults', 'Checkout repository', 'Setup uv', "Fetch main's harness and helpers", 'Install unit-test tools', "Run main's unit tests against this change"]
[exit 0]

$ git diff --numstat origin/main HEAD
65	0	.github/workflows/test.yaml
9	0	.orchestration/dotfiles-T128-v0-main-tests-a01/revise.yaml
67	0	.orchestration/dotfiles-T128-v0-main-tests-a01/task.md
2	1	home/dot_agents/skills/agmsg-orchestration/SKILL.md
118	0	scripts/lib/contract_markers.py
149	0	scripts/main-tests.sh
14	0	tests/unit/regime_contract.py
146	0	tests/unit/test_contract_markers.py
278	0	tests/unit/test_main_tests.py
[exit 0]

$ git ls-files -s scripts/main-tests.sh scripts/lib/contract_markers.py
100644 12746996dde9befe81b31a901314159dc53e2773 0	scripts/lib/contract_markers.py
100755 ca758d5b032f82c8726e5d3660f56e04af0b258a 0	scripts/main-tests.sh
[exit 0]

```

An earlier capture at `9b8a62a2` hit one 1-second timeout launching the host's `ccstatusline` in `test_statusline_tools` (`subprocess.TimeoutExpired: Command '['ccstatusline']' timed out after 1 seconds`); its rerun and every later run passed. The test does not read any file this PR changes.

## §2 Each rule removed in turn fails its test (final head)

```
$ uv run --no-project python <scratchpad>/mutate.py "$(pwd)"
mutation: remove 'undeclared mode' in scripts/main-tests.sh -> test_an_undeclared_script_change_meets_mains_ordinary_tests: FAILS (rule is load-bearing)
mutation: remove 'declared mode runs contracts only' in scripts/main-tests.sh -> test_a_declared_script_meets_mains_contract_only: FAILS (rule is load-bearing)
mutation: remove 'no contract on main' in scripts/main-tests.sh -> test_a_design_tier_module_needs_a_contract_on_main: FAILS (rule is load-bearing)
mutation: remove 'promotion check' in scripts/main-tests.sh -> test_an_implementation_must_promote_its_contracts: FAILS (rule is load-bearing)
mutation: remove 'alias forms' in scripts/lib/contract_markers.py -> test_aliased_and_inline_contracts_are_still_dormant: FAILS (rule is load-bearing)
mutation: remove 'inline skipUnless' in scripts/lib/contract_markers.py -> test_aliased_and_inline_contracts_are_still_dormant: FAILS (rule is load-bearing)
mutation: remove "main's copy of a deleted module" in scripts/main-tests.sh -> test_a_deleted_module_still_runs_from_main: FAILS (rule is load-bearing)
mutation: remove 'skip path' in scripts/main-tests.sh -> test_no_script_change_skips: FAILS (rule is load-bearing)
mutation: remove 'install/ triggers' in scripts/lib/contract_markers.py -> test_an_install_change_triggers_the_run: FAILS (rule is load-bearing)
mutation: remove 'uncovered design script' in scripts/main-tests.sh -> test_design_scripts_need_declared_modules_that_exist: FAILS (rule is load-bearing)
mutation: remove 'data is not a script' in scripts/lib/contract_markers.py -> test_design_scripts_need_declared_modules_that_exist: FAILS (rule is load-bearing)
mutation: remove 'declared module deleted' in scripts/main-tests.sh -> test_design_scripts_need_declared_modules_that_exist: FAILS (rule is load-bearing)
mutation: remove 'missing tier is design' in scripts/lib/contract_markers.py -> test_a_design_tier_module_needs_a_contract_on_main: FAILS (rule is load-bearing)
mutation: remove 'one task.md' in scripts/main-tests.sh -> test_more_than_one_task_file_fails: FAILS (rule is load-bearing)
mutation: remove "main's tests/unit only" in scripts/main-tests.sh -> test_files_the_pr_plants_cannot_replace_mains_runner: FAILS (rule is load-bearing)
mutation: remove '-P keeps the PR root off sys.path' in scripts/main-tests.sh -> test_files_the_pr_plants_cannot_replace_mains_runner: FAILS (rule is load-bearing)
mutation: remove 'uv --no-config' in scripts/main-tests.sh -> test_a_uv_config_the_pr_plants_is_ignored: FAILS (rule is load-bearing)
mutation: remove 'a failing helper stops the run' in scripts/main-tests.sh -> test_a_helper_failure_fails_the_run: FAILS (rule is load-bearing)
mutation: remove "the job sources main's github-release.sh" in .github/workflows/test.yaml -> test_nothing_from_the_pr_runs_before_mains_harness: FAILS (rule is load-bearing)
mutation: remove 'an interpreter found outside the tree' in scripts/main-tests.sh -> test_a_planted_venv_is_not_used: FAILS (rule is load-bearing)
mutation: remove 'a summary is required' in scripts/main-tests.sh -> test_a_zero_exit_without_a_summary_fails: FAILS (rule is load-bearing)
mutation: remove 'the declared count must match' in scripts/main-tests.sh -> test_a_short_contract_summary_fails: FAILS (rule is load-bearing)
mutation: remove 'exemption is keyed on the declared script' in scripts/lib/contract_markers.py -> test_a_declared_module_without_its_script_stays_undeclared: FAILS (rule is load-bearing)
mutation: remove '--no-renames' in scripts/main-tests.sh -> test_a_renamed_script_still_triggers: FAILS (rule is load-bearing)
mutation: remove 'contract ids are test methods' in scripts/lib/contract_markers.py -> test_an_empty_contract_class_is_no_contract: FAILS (rule is load-bearing)
tree restored: git diff clean
[exit 0]
```

Each mutation replaces one rule's text in the committed file with a no-op (for example the undeclared-mode unittest call with `true`, `rm -rf "${tmp}/tests/unit"` with nothing, `python -P` with `python`, `else "design"` with `else "review"`), runs the named test method with `uv run python -m unittest` from `tests/unit`, and restores the file with `git checkout --`. The mutation table lives in the uncommitted scratch script.

## §3 `scripts/main-tests.sh origin/main` on this branch (final head)

```
$ git rev-parse HEAD > own-head.txt; start=$(date +%s); scripts/main-tests.sh origin/main > main-tests-own.log 2>&1; echo "rc=$? seconds=$(( $(date +%s) - start ))"
32fe9a36a6ca67670e54bbcb1c506ca391d9dd32
rc=1 seconds=418
$ grep -a '^main-tests:\|^Ran \|^OK\|^FAILED' main-tests-own.log
main-tests: no contract on main for tests/unit/test_main_tests.py
main-tests: no contract on main for tests/unit/test_contract_markers.py
main-tests: undeclared mode, main's modules as they are: test_agent_session_staleness test_agent_stop_gate test_agmsg_dispatch test_agmsg_orchestration_docs test_apparmor_userns test_asset_manifest test_aws_cli_acquisition test_check_agent_runtime test_chezmoiremove_agmsg test_claude_settings_merge test_codex_config_merge test_codex_execpolicy test_codex_orchestrate test_contextdb_codex_notify test_enforce_uv test_files_fixture test_format_edited_files_hook test_generate_agent_configs test_gh_auth test_github_release test_gitignore_sandbox_placeholders test_herdr_agents test_permgate test_pr_feedback test_remove_agent_asset test_require_crit_review test_runtime_health test_statusline_tools test_supply_chain_policy test_ua_symbol_coverage test_update_agent_assets_ua_core test_usage_review test_validate_agent_assets test_workflow_security
Ran 925 tests in 414.663s
FAILED (failures=114, errors=103, skipped=2)
```

The two `no contract on main` lines are the V0 bootstrap (report, "main-tests on this PR fails by design"). The undeclared-mode failures are this host's sandbox: §4 shows the identical set on main.

## §4 The same failures from main's tests without this PR's harness

`make unit-test` in this worktree at `efd8b66b` (`origin/main` `b896d9bc` plus the task file). I wrote this PR's new files while it ran, but discovery had already loaded its modules: it ran 925 tests, main's count and the count CI's `main-tests` runs (§5).

```
$ start=$(date +%s); make unit-test > baseline-unit.log 2>&1; rc=$?; echo "rc=$rc seconds=$(( $(date +%s) - start ))"
rc=2 seconds=397
$ grep -a '^Ran \|^FAILED' baseline-unit.log
Ran 925 tests in 397.281s
FAILED (failures=114, errors=103, skipped=2)
$ grep -a '^ERROR: \|^FAIL: ' baseline-unit.log | sort > base-fail.txt; grep -a '^ERROR: \|^FAIL: ' main-tests-own.log | sort > own-fail.txt; diff base-fail.txt own-fail.txt && echo "identical failing set: $(wc -l < own-fail.txt | tr -d ' ') lines"
identical failing set: 223 lines
```

## §5 CI

Final head `32fe9a36`:

```
$ gh pr checks 317 --repo mryfmo/dotfiles --watch --interval 30 > /dev/null 2>&1; gh pr checks 317 --repo mryfmo/dotfiles 2>&1 | awk -F'\t' '{print $1" | "$2" | "$3" | "$4}'
main-tests | fail | 3m39s | https://github.com/mryfmo/dotfiles/actions/runs/38103850834/job/114365133222
CodeRabbit | pass | 0 | 
GitGuardian Security Checks | pass | 1s | https://dashboard.gitguardian.com
changes | pass | 7s | https://github.com/mryfmo/dotfiles/actions/runs/38103850834/job/114365108162
private-bootstrap (macos-14, client) | pass | 14s | https://github.com/mryfmo/dotfiles/actions/runs/38103850757/job/114365107948
private-bootstrap (ubuntu-24.04, client) | pass | 11s | https://github.com/mryfmo/dotfiles/actions/runs/38103850757/job/114365107926
private-bootstrap (ubuntu-24.04, server) | pass | 9s | https://github.com/mryfmo/dotfiles/actions/runs/38103850757/job/114365107971
public-bootstrap (macos-14, client) | pass | 8m10s | https://github.com/mryfmo/dotfiles/actions/runs/38103850757/job/114365107883
public-bootstrap (ubuntu-24.04, client) | pass | 7m49s | https://github.com/mryfmo/dotfiles/actions/runs/38103850757/job/114365107987
public-bootstrap (ubuntu-24.04, server) | pass | 7m22s | https://github.com/mryfmo/dotfiles/actions/runs/38103850757/job/114365107959
test (macos-14, client) | pass | 6m7s | https://github.com/mryfmo/dotfiles/actions/runs/38103850834/job/114365133217
test (ubuntu-24.04, client) | pass | 8m8s | https://github.com/mryfmo/dotfiles/actions/runs/38103850834/job/114365133241
test (ubuntu-24.04, server) | pass | 5m34s | https://github.com/mryfmo/dotfiles/actions/runs/38103850834/job/114365133255
test (ubuntu-26.04, client) | pass | 8m26s | https://github.com/mryfmo/dotfiles/actions/runs/38103850834/job/114365133214
validate | pass | 1m33s | https://github.com/mryfmo/dotfiles/actions/runs/38103850777/job/114365107910
```

The `main-tests` job at the final head (job 114365133222):

```
$ gh api --allow-escape-sequences repos/mryfmo/dotfiles/actions/jobs/114365133222/logs | grep -a -E 'HEAD is now|chezmoi_[0-9.]+_linux_amd64.tar.gz: OK|main has no [a-z]|^[0-9TZ:.-]+ main-tests:|ERROR: test_|FAIL: test_|Ran [0-9]+ tests|^[0-9TZ:.-]+ OK$|FAILED \(|##\[error\]' | cut -c1-400
2026-10-11T02:02:59.6471572Z HEAD is now at cbe8da69 Merge 32fe9a36a6ca67670e54bbcb1c506ca391d9dd32 into b896d9bcb16f2288de3a259cabe06f7943e6749d
2026-10-11T02:03:01.0146451Z [36;1m    # Only this harness pair falls back, and only on the PR that adds it: main has no copy yet.[0m
2026-10-11T02:03:01.3482871Z main has no scripts/main-tests.sh; running this PR's copy
2026-10-11T02:03:01.3512657Z main has no scripts/lib/contract_markers.py; running this PR's copy
2026-10-11T02:03:19.8608669Z chezmoi_2.73.0_linux_amd64.tar.gz: OK
2026-10-11T02:03:25.2236593Z main-tests: no contract on main for tests/unit/test_main_tests.py
2026-10-11T02:03:25.2250233Z main-tests: no contract on main for tests/unit/test_contract_markers.py
2026-10-11T02:03:25.2256084Z main-tests: undeclared mode, main's modules as they are: test_agent_session_staleness test_agent_stop_gate test_agmsg_dispatch test_agmsg_orchestration_docs test_apparmor_userns test_asset_manifest test_aws_cli_acquisition test_check_agent_runtime test_chezmoiremove_agmsg test_claude_settings_merge test_codex_config_merge test_codex_execpolicy test_codex_orchestrate te
2026-10-11T02:06:27.8872478Z Ran 925 tests in 182.443s
2026-10-11T02:06:27.8872762Z OK
2026-10-11T02:06:28.4754598Z ##[error]Process completed with exit code 1.
```

The first `main-tests` run (head `3e715ef5`, job 114349176212) errored five of main's modules on a missing chezmoi, fixed in `9b8a62a2`:

```
$ gh run view 38098441693 --job 114349176212 --log | grep -a -E 'ERROR: test_|FileNotFoundError|Ran [0-9]+ tests|FAILED \(' | cut -c1-260
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9903734Z ERROR: test_chezmoi_wrapper_renders_shebang_and_source_root (test_asset_manifest.AssetManifestTest.test_chezmoi_wrapper_renders_shebang_and_source_root)
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9919137Z FileNotFoundError: [Errno 2] No such file or directory: 'chezmoi'
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9920254Z ERROR: test_external_checksum_failure_preserves_destination (test_supply_chain_policy.SupplyChainPolicyTest.test_external_checksum_failure_preserves_destination)
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9926256Z FileNotFoundError: [Errno 2] No such file or directory: 'chezmoi'
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9927581Z ERROR: test_externals_render_without_network_discovery (test_supply_chain_policy.SupplyChainPolicyTest.test_externals_render_without_network_discovery)
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9933833Z FileNotFoundError: [Errno 2] No such file or directory: 'chezmoi'
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9935175Z ERROR: test_mise_apply_replaces_live_symlinks_with_independent_copies (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_apply_replaces_live_symlinks_with_independent_copi
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9940769Z FileNotFoundError: [Errno 2] No such file or directory: 'chezmoi'
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9941846Z ERROR: test_mise_tools_track_latest_behind_the_cooldown (test_supply_chain_policy.SupplyChainPolicyTest.test_mise_tools_track_latest_behind_the_cooldown)
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9947386Z FileNotFoundError: [Errno 2] No such file or directory: 'chezmoi'
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9948122Z Ran 925 tests in 192.432s
main-tests	Run main's unit tests against this change	2026-10-11T00:30:20.9948363Z FAILED (errors=5, skipped=2)
```

`public-bootstrap (ubuntu-24.04, client)` on `9b8a62a2` (job 114351531912) failed on a snapcraft API timeout, and fail-fast cancelled the other two public-bootstrap jobs. I reran them with `gh run rerun 38099242529 --failed` (attempt 2). Every later head, the final one included, passed all three (above).

```
$ gh run view 38099242529 --job 114351531912 --log | sed -n 177463,177467p | cut -f3- | cut -c1-300
2026-10-11T00:43:06.8399353Z error: cannot perform the following tasks:
2026-10-11T00:43:06.8401043Z - Fetch and check assertions for snap "mesa-2404" (1839) (cannot fetch assertion: got unexpected HTTP status code 408 via GET to "https://api.snapcraft.io/v2/assertions/snap-revision/o_y3i90q5jFyl_bRaCoXe1F9ynTiH0Mf1f0cCu9I7iKEESmXq0-FOwcjqimGD0H6?max-format=0")
2026-10-11T00:43:06.8431823Z chezmoi: .chezmoiscripts/ubuntu/50-client-install-misc.sh: exit status 1
2026-10-11T00:43:06.8469289Z chezmoi apply failed; completed target operations may remain.
2026-10-11T00:43:06.8598482Z ##[error]Process completed with exit code 1.
```

## §6 CompactionDB

```
$ cd ~/Workspace/dotfiles && grep -c '\[memory:' .orchestration/tasks/dotfiles-T128-v0-main-tests-a01.md; uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 wave V0 (worker claude-standard-dot-a002, 2026-10-11, PR 317): scripts/main-tests.sh overlays main tests/unit on a git-archive copy of the PR tree when the diff touches scripts/**, home/dot_local/bin/**, install/**, home/.chezmoiscripts/** or setup.sh; main modules the task.md does not declare run as they are, declared tests/unit/test_*.py modules run only their @contract tests (tests/unit/regime_contract.py) with REGIME_CONTRACT=1; a design-tier task.md (missing tier stamp = design) must declare a module per non-data script, keep it, and find a contract on main; an implementation id (not -contract-a01) fails while its own copy keeps a contract decorator (ast, any alias or inline skipUnless). The main-tests job runs main copy of the harness and installs jq, zsh and a verified chezmoi; on PR 317 itself it fails by design on two no-contract-on-main lines (V0 bootstrap) while all 925 main tests pass.' 2>&1 | tail -3
0
c64e9528-04e1-4075-900a-34e53f044946
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 wave V0 revise round 1 (worker claude-standard-dot-a002, 2026-10-11, PR 317): uv executes a PR-planted .venv/bin/python while probing interpreters under uv run --no-project, --with and even --isolated; only an explicit --python <path> resolved from / (uv python find --no-config) avoids it, so scripts/main-tests.sh passes --python to every uv call. The harness also requires unittest own summary (Ran n > 0, n equal to the contract-id count in declared mode, then OK), exempts a main module only when the task.md declares its script too, diffs with --no-renames, lists contract ids as test methods, and the main-tests job sources main copy of scripts/lib/github-release.sh so nothing from the PR tree runs before the harness.' 2>&1 | tail -2
6f5e1dc2-27b4-4a10-8e09-5d0e7c0c12d7
```

## §7 Bot wait (Worker Playbook step 15, final head)

```
$ head=32fe9a36a6ca67670e54bbcb1c506ca391d9dd32; out=bot-wait.log; : > "$out"; deadline=$(( $(date +%s) + 900 )); echo "bot wait start $(date -u +%FT%TZ) head=${head}" >> "$out"; while [ "$(date +%s)" -lt "$deadline" ]; do r="$(gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq ".[]|select(.user.type==\"Bot\" and .commit_id==\"${head}\")|[.commit_id,.submitted_at,.user.login,.state]|@tsv" 2>&1)"; c="$(gh api --paginate repos/mryfmo/dotfiles/pulls/317/comments --jq ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"${head}\")|[.id,.original_commit_id,.path]|@tsv" 2>&1)"; if [ -n "$r$c" ]; then printf 'reviews:\n%s\ncomments:\n%s\n' "$r" "$c" >> "$out"; break; fi; sleep 30; done; echo "bot wait end $(date -u +%FT%TZ)" >> "$out"; cat "$out"
bot wait start 2026-10-11T02:03:04Z head=32fe9a36a6ca67670e54bbcb1c506ca391d9dd32
bot wait end 2026-10-11T02:18:05Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/317/reviews --jq '.[]|[.user.login,.user.type,.commit_id[0:8],.submitted_at]|@tsv'
$ gh api --paginate repos/mryfmo/dotfiles/pulls/317/comments --jq '.[]|[.user.login,.original_commit_id[0:8],.path]|@tsv'
$ gh api --paginate repos/mryfmo/dotfiles/issues/317/comments --jq '.[]|[.user.login,.user.type,.created_at,(.body|.[0:80])]|@tsv'
coderabbitai[bot]	Bot	2026-10-11T00:10:59Z	<!-- This is an auto-generated comment: summarize by coderabbit.ai -->\n<!-- This
$ gh api repos/mryfmo/dotfiles/issues/317/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
```

## §8 Invariant lines

invariant: INV-12 → tests/unit/test_main_tests.py::test_an_undeclared_script_change_meets_mains_ordinary_tests, scripts/main-tests.sh:143
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_declared_script_meets_mains_contract_only, scripts/main-tests.sh:147
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_design_tier_module_needs_a_contract_on_main, scripts/main-tests.sh:117
invariant: INV-12 → tests/unit/test_main_tests.py::test_an_implementation_must_promote_its_contracts, scripts/main-tests.sh:91
invariant: INV-12 → tests/unit/test_main_tests.py::test_aliased_and_inline_contracts_are_still_dormant, scripts/lib/contract_markers.py:56
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_deleted_module_still_runs_from_main, scripts/main-tests.sh:98
invariant: INV-12 → tests/unit/test_main_tests.py::test_files_the_pr_plants_cannot_replace_mains_runner, scripts/main-tests.sh:97
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_uv_config_the_pr_plants_is_ignored, scripts/main-tests.sh:36
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_helper_failure_fails_the_run, scripts/main-tests.sh:43
invariant: INV-12 → tests/unit/test_main_tests.py::test_design_scripts_need_declared_modules_that_exist, scripts/main-tests.sh:74
invariant: INV-12 → tests/unit/test_main_tests.py::test_an_install_change_triggers_the_run, scripts/lib/contract_markers.py:16
invariant: INV-12 → tests/unit/test_main_tests.py::test_no_script_change_skips, scripts/main-tests.sh:45
invariant: INV-12 → tests/unit/test_main_tests.py::test_more_than_one_task_file_fails, scripts/main-tests.sh:62
invariant: INV-12 → tests/unit/test_main_tests.py::test_nothing_from_the_pr_runs_before_mains_harness, .github/workflows/test.yaml:125
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_planted_venv_is_not_used, scripts/main-tests.sh:30
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_zero_exit_without_a_summary_fails, scripts/main-tests.sh:132
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_short_contract_summary_fails, scripts/main-tests.sh:133
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_declared_module_without_its_script_stays_undeclared, scripts/lib/contract_markers.py:46
invariant: INV-12 → tests/unit/test_main_tests.py::test_a_renamed_script_still_triggers, scripts/main-tests.sh:41
invariant: INV-12 → tests/unit/test_main_tests.py::test_an_empty_contract_class_is_no_contract, scripts/lib/contract_markers.py:95
invariant: INV-12 → tests/unit/test_contract_markers.py::test_every_form_is_found_on_its_method, scripts/lib/contract_markers.py:70
invariant: INV-12 → .github/workflows/test.yaml:79 (the main-tests job runs main's copy of the harness; validation §5)
