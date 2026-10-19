---
task_id: dotfiles-T133-ci-efficiency-followup-a02
seat: claude-standard-dot-a011
code_commit: 02ff2e1c
---

# Validation: dotfiles-T133-ci-efficiency-followup-a02

Every command below ran from the worktree `.claude/worktrees/worker-d` on the branch `tools/ci-efficiency-followup-a02`, created with `--no-track` from `origin/main` `740772ef`, at `02ff2e1c`, inside the sandbox. The commits for row `security:4fe2438:1` are the red test `380f86d6` and the fix `0e42cb06`, then, from the worker review of 0e42cb06, the red tests `73e59b05` and the fix `02ff2e1c`. `MAIN` names the main checkout, `T` the task id, `SCRATCH` the seat's scratchpad, `CHECK` the Check's three test modules and `M` the test class. The output is verbatim, with the main checkout's, the home directory's and the scratchpad's paths replaced by `$MAIN`, `$HOME` and `$SCRATCH`, and each block ends with the exit status of the command shown. Every status line captures `rc=$?` (or prints `$?`) before any command substitution.

## 1. Task file and task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
50599bfdb250510004525e48155a53b954ba6c19af4a2be5d520c9352a3f2466  $MAIN/.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a02.md
50599bfdb250510004525e48155a53b954ba6c19af4a2be5d520c9352a3f2466  .orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-ci-efficiency-followup-a02.md: OK
[exit 0]
````

## 2. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git log --oneline -1 origin/main; git merge-base origin/main HEAD; git diff --quiet 740772ef 380f86d6 -- scripts && echo "the red commit changes no script"; git diff --stat 740772ef 380f86d6; git diff --stat 380f86d6 0e42cb06; git diff --quiet 0e42cb06 73e59b05 -- scripts && echo "73e59b05 changes no script of 0e42cb06"; git diff --stat 73e59b05 02ff2e1c
02ff2e1c fix(orchestrator): ci-rerun.sh starts python3 by its own path and runs no PATH tool before pinning (T133 ci-efficiency follow-up a02, worker review)
73e59b05 test(orchestrator): the pinned interpreter starts by its own path, and no checkout tool runs before pinning (T133 ci-efficiency follow-up a02, worker review, red)
0e42cb06 fix(orchestrator): ci-rerun.sh pins its tools and interpreter before reading a checkout (T133 ci-efficiency follow-up a02, security:4fe2438:1)
380f86d6 test(orchestrator): ci-rerun.sh must not take its interpreter from a checkout or the environment (T133 ci-efficiency follow-up a02, security:4fe2438:1, red)
740772ef fix(assets): uninstall hcom through uv, retry a failed hcom install, move an omp entry npm does not own aside (T129 assets-omp-hcom followup a02) (#416)
740772efb9d7928e810a7d799f2bd32a88d9b8ff
the red commit changes no script
 tests/unit/test_ci_rerun.py | 23 ++++++++++++++++++++++-
 1 file changed, 22 insertions(+), 1 deletion(-)
 scripts/orchestrator/ci-rerun.sh | 23 ++++++++++++++++++++---
 1 file changed, 20 insertions(+), 3 deletions(-)
73e59b05 changes no script of 0e42cb06
 scripts/orchestrator/ci-rerun.sh | 29 ++++++++++++++++++-----------
 1 file changed, 18 insertions(+), 11 deletions(-)
[exit 0]
````

## 3. Red on the red commit (a scratch worktree), green at the head

````console
$ git worktree add --detach -q "$SCRATCH/fu2-red" 380f86d6 && uv run --directory "$SCRATCH/fu2-red" python -m unittest "$M.test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment" -v > "$SCRATCH/fu2-red.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/fu2-red.out" /usr/bin/grep -E " \.\.\. (ok|FAIL|ERROR)$|^(FAIL|ERROR):|^AssertionError|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//"; git worktree remove --force "$SCRATCH/fu2-red"
unittest exit status: 1
test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment ... FAIL
FAIL: test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment
AssertionError: True is not false : a checkout or inherited selector ran the planted interpreter
Ran 1 test in 1.687s
FAILED (failures=1)
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/fu2-red2" 73e59b05 && uv run --directory "$SCRATCH/fu2-red2" python -m unittest "$M.test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment" "$M.test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path" -v > "$SCRATCH/fu2-red2.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/fu2-red2.out" /usr/bin/grep -E " \.\.\. (ok|FAIL|ERROR)$|^(FAIL|ERROR):|^AssertionError|^Items|^./|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//"; git worktree remove --force "$SCRATCH/fu2-red2"
unittest exit status: 1
test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment ... FAIL
test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path ... FAIL
FAIL: test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment
AssertionError: 0 != 1 : 
FAIL: test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path
AssertionError: Items in the first set but not the second:
'$TMPDIR/tmptk6n7shf/py/python3'
Items in the second set but not the first:
'$TMPDIR/ci-rerun-bin.8DoMYU/python3'
Ran 2 tests in 5.032s
FAILED (failures=2)
[exit 0]
````

````console
$ uv run python -m unittest $CHECK -v
test_a_main_tests_job_when_present_decides_in_itself (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_a_main_tests_job_when_present_decides_in_itself) ... ok
test_both_bootstrap_jobs_decide_with_the_same_script (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script) ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed) ... ok
test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff) ... ok
test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_unless_a_bootstrap_path_changed) ... ok
test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) ... ok
test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout) ... ok
test_the_unit_test_decision_ignores_renames (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_ignores_renames) ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff) ... ok
test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_macos_for_an_os_independent_diff_and_runs_it_otherwise) ... ok
test_no_job_is_left_for_a_required_job_to_need (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need) ... ok
test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs) ... ok
test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) ... ok
test_the_required_contexts_are_the_workflows_jobs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs) ... ok
test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script (tests.unit.test_workflow_orchestration_skip.WorkflowTriggerTest.test_private_bootstrap_runs_only_on_push_schedule_and_dispatch_and_decides_with_the_bootstrap_script) ... ok
test_the_matrices_do_not_fail_fast (tests.unit.test_workflow_orchestration_skip.WorkflowTriggerTest.test_the_matrices_do_not_fail_fast) ... ok
test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run (tests.unit.test_workflow_orchestration_skip.WorkflowTriggerTest.test_the_three_workflows_cancel_superseded_pull_request_runs_and_keep_every_main_run) ... ok
test_checkout_does_not_persist_credentials_without_explicit_exemption (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (tests.unit.test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (tests.unit.test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok
test_a_failing_gh_exits_1_never_with_the_scripts_own_codes (tests.unit.test_ci_rerun.CiRerunTest.test_a_failing_gh_exits_1_never_with_the_scripts_own_codes) ... ok
test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment) ... ok
test_ci_rerun_refuses_a_superseded_pull_request_head (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_refuses_a_superseded_pull_request_head) ... ok
test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs) ... ok
test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature) ... ok
test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs) ... ok
test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice) ... ok
test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path) ... ok
test_the_production_flake_registry_matches_its_samples_and_no_real_failure (tests.unit.test_ci_rerun.CiRerunTest.test_the_production_flake_registry_matches_its_samples_and_no_real_failure) ... ok

----------------------------------------------------------------------
Ran 35 tests in 44.997s

OK
[exit 0]
````

## 4. Lint

````console
$ shellcheck scripts/orchestrator/ci-rerun.sh && echo shellcheck-clean; shfmt -i 4 -sr -d scripts/orchestrator/ci-rerun.sh && echo "shfmt -i 4 -sr -d ci-rerun.sh (the repository form): clean"; shfmt -d scripts/orchestrator/ci-rerun.sh > /dev/null; echo "plain shfmt -d ci-rerun.sh rc=$? (.editorconfig sets indent_size without indent_style, so bare shfmt asks for tabs on every tracked script)"; ruff format --config ruff.toml --check tests/unit/test_ci_rerun.py
shellcheck-clean
shfmt -i 4 -sr -d ci-rerun.sh (the repository form): clean
plain shfmt -d ci-rerun.sh rc=1 (.editorconfig sets indent_size without indent_style, so bare shfmt asks for tabs on every tracked script)
1 file already formatted
[exit 0]
````

## 5. make format

````console
$ make format > "$SCRATCH/fu2-format.out" 2>&1; rc=$?; echo "make format exit status: ${rc}"; base="$(git merge-base origin/main HEAD)"; sed -n "s/^diff \([^ ]*\)\.orig .*/\1/p" "$SCRATCH/fu2-format.out" > "$SCRATCH/fu2-flagged.txt"; echo "files the whole-tree shfmt step flags: $(wc -l < "$SCRATCH/fu2-flagged.txt" | tr -d " ")"; while read -r f; do git diff --quiet "$base" HEAD -- "$f" && echo "unchanged from ${base:0:8}: $f" || echo "CHANGED by this PR: $f"; done < "$SCRATCH/fu2-flagged.txt"
make format exit status: 2
files the whole-tree shfmt step flags: 12
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
unchanged from 740772ef: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
unchanged from 740772ef: home/dot_claude/hooks/executable_project-map-reload.sh
unchanged from 740772ef: tests/install/macos/common/brew.bats
[exit 0]
````

````console
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check; git ls-files -z "*.md" | xargs -0 prettier --check
63 files already formatted
Checking formatting...
All matched files use Prettier code style!
[exit 0]
````

## 6. make unit-test with the sandbox limits neutralized, at the head and at the merge base

Inside the sandbox the global SSH commit signing cannot read `~/.ssh`, so most fixture commits fail in a plain run. These runs set `GIT_CONFIG_GLOBAL=/dev/null` and put the validation-only `mktemp` shim (`$SCRATCH/shim/mktemp`, which adds a `$TMPDIR` template because a bare macOS `mktemp -d` ignores `TMPDIR` and the sandbox denies the Darwin user temp directory) first on PATH, identically on both sides.

````console
$ GIT_CONFIG_GLOBAL=/dev/null PATH="$SCRATCH/shim:$PATH" make unit-test > "$SCRATCH/fu2-unit-head.out" 2>&1; rc=$?; echo "make unit-test at the head exit status: ${rc}"; < "$SCRATCH/fu2-unit-head.out" /usr/bin/grep -E "^(Ran|OK|FAILED)"; < "$SCRATCH/fu2-unit-head.out" /usr/bin/grep -E "^(FAIL|ERROR): test" | sed "s/.*(\([a-z_]*\)\..*/\1/" | sort | uniq -c
make unit-test at the head exit status: 2
Ran 1218 tests in 744.132s
FAILED (failures=44, errors=10, skipped=2)
   4 test_agent_stop_gate
   5 test_gh_auth
  37 test_herdr_agents
   8 test_runtime_health
[exit 0]
````

````console
$ base="$(git merge-base origin/main HEAD)"; git worktree add --detach -q "$SCRATCH/fu2-base" "$base" && GIT_CONFIG_GLOBAL=/dev/null PATH="$SCRATCH/shim:$PATH" make -C "$SCRATCH/fu2-base" unit-test > "$SCRATCH/fu2-unit-base.out" 2>&1; rc=$?; echo "make unit-test at ${base:0:8} exit status: ${rc}"; < "$SCRATCH/fu2-unit-base.out" /usr/bin/grep -E "^(Ran|OK|FAILED)"; < "$SCRATCH/fu2-unit-base.out" /usr/bin/grep -E "^(FAIL|ERROR): test" | sed "s/.*(\([a-z_]*\)\..*/\1/" | sort | uniq -c; git worktree remove --force "$SCRATCH/fu2-base"
make unit-test at 740772ef exit status: 2
Ran 1216 tests in 766.758s
FAILED (failures=44, errors=10, skipped=2)
   4 test_agent_stop_gate
   5 test_gh_auth
  37 test_herdr_agents
   8 test_runtime_health
[exit 0]
````

````console
$ comm -3 <(/usr/bin/grep -E "^(FAIL|ERROR): test" "$SCRATCH/fu2-unit-head.out" | sort) <(/usr/bin/grep -E "^(FAIL|ERROR): test" "$SCRATCH/fu2-unit-base.out" | sort) | sed "s/^/only on one side: /"; n="$(comm -23 <(/usr/bin/grep -E "^(FAIL|ERROR): test" "$SCRATCH/fu2-unit-head.out" | sort) <(/usr/bin/grep -E "^(FAIL|ERROR): test" "$SCRATCH/fu2-unit-base.out" | sort) | wc -l | tr -d " ")"; echo "failing at the head but not at the base: ${n}"
failing at the head but not at the base: 0
[exit 0]
````

## 7. Caps (at most 250 changed lines outside tests/ and .orchestration/; at most 350 under tests/)

````console
$ git diff --numstat origin/main...HEAD
29	5	scripts/orchestrator/ci-rerun.sh
39	1	tests/unit/test_ci_rerun.py
[exit 0]
````

````console
$ git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d of 250\ntests/: %d of 350\n", o, t }'
outside tests/ and .orchestration/: 34 of 250
tests/: 40 of 350
[exit 0]
````


## 8. Revise 1: no PATH-resolved command before the PATH pin

The chain's local review of the update-branch head `7329f0ee` found a P1 at `scripts/orchestrator/ci-rerun.sh:42`: the EXIT trap ran `rm` through the caller's PATH, and the refusal path exits before PATH is pinned. The same holds for the `env` around `mise which`, which runs in every pass of the tool loop. `RED` is the test commit `4dacbd60` (the test on `7329f0ee`'s script), `FIX` is `67180e37` and `TEST` is the new test. The test puts an `rm` and an `env` that log their names first on PATH, then runs the script on the refusal path (a `jq` under a `shims/` directory) and as a full run. `mise` stays the stub from setUp: it is the resolver the design names, the one program found through PATH.

````console
$ git log --oneline -3; git diff --stat "$PREV" "$FIX"
67180e37 fix(orchestrator): ci-rerun.sh runs the EXIT trap's rm and the env around mise by their system paths before its PATH pin (T133 ci-efficiency follow-up a02, revise 1)
4dacbd60 test(orchestrator): ci-rerun.sh runs no PATH-resolved command before its PATH pin (T133 ci-efficiency follow-up a02, revise 1, red)
7329f0ee Merge branch 'main' into tools/ci-efficiency-followup-a02
 scripts/orchestrator/ci-rerun.sh |  7 ++++---
 tests/unit/test_ci_rerun.py      | 20 ++++++++++++++++++++
 2 files changed, 24 insertions(+), 3 deletions(-)
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/fu2r-red" "$RED" && (cd "$SCRATCH/fu2r-red" && uv run python -m unittest "$TEST") > "$SCRATCH/fu2r-red.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/fu2r-red.out" /usr/bin/grep -E -A11 "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | /usr/bin/grep -v "^--$" | cut -c1-200; git worktree remove --force "$SCRATCH/fu2r-red"
unittest exit status: 1
FAIL: test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin [refused before the pin]
----------------------------------------------------------------------
Traceback (most recent call last):
  File "$SCRATCH/fu2r-red/tests/unit/test_ci_rerun.py", line 324, in test_c
    self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false : env
env
env
env
rm

FAIL: test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin [a full run]
----------------------------------------------------------------------
Traceback (most recent call last):
  File "$SCRATCH/fu2r-red/tests/unit/test_ci_rerun.py", line 324, in test_c
    self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false : env
env
env
env
env
env
Ran 1 test in 1.221s

FAILED (failures=2)
[exit 0]
````

````console
$ git rev-parse HEAD; uv run python -m unittest tests.unit.test_ci_rerun -v
67180e37d30c58a276eef6816ad1ee4479c43d20
test_a_failing_gh_exits_1_never_with_the_scripts_own_codes (tests.unit.test_ci_rerun.CiRerunTest.test_a_failing_gh_exits_1_never_with_the_scripts_own_codes) ... ok
test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_never_runs_a_path_resolved_command_before_the_pin) ... ok
test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_pins_its_interpreter_against_a_checkout_and_the_environment) ... ok
test_ci_rerun_refuses_a_superseded_pull_request_head (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_refuses_a_superseded_pull_request_head) ... ok
test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs) ... ok
test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature) ... ok
test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs) ... ok
test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice) ... ok
test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_starts_the_pinned_interpreter_by_its_own_path) ... ok
test_the_production_flake_registry_matches_its_samples_and_no_real_failure (tests.unit.test_ci_rerun.CiRerunTest.test_the_production_flake_registry_matches_its_samples_and_no_real_failure) ... ok

----------------------------------------------------------------------
Ran 10 tests in 22.095s

OK
[exit 0]
````

````console
$ shellcheck scripts/orchestrator/ci-rerun.sh; shfmt --indent 4 --space-redirects --diff scripts/orchestrator/ci-rerun.sh; ruff format --config ruff.toml --check tests/unit/test_ci_rerun.py; ruff check --config ruff.toml tests/unit/test_ci_rerun.py
1 file already formatted
All checks passed!
[exit 0]
````

````console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d of 250\ntests/: %d of 350\n", o, t }'
44	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/dotfiles-T133-ci-efficiency-followup-a02-worker-crit.json
13	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/dotfiles-T133-ci-efficiency-followup-a02-worker-review-receipt.md
10	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/learning.md
61	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/report.md
14	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/sandbox.md
51	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md
212	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a02/validation.md
30	5	scripts/orchestrator/ci-rerun.sh
59	1	tests/unit/test_ci_rerun.py
outside tests/ and .orchestration/: 35 of 250
tests/: 60 of 350
[exit 0]
````

