---
task_id: dotfiles-T133-ci-efficiency-followup-a01
seat: claude-standard-dot-a011
code_commit: 5df527dd
---

# Validation: dotfiles-T133-ci-efficiency-followup-a01

Every command below ran from the worktree `.claude/worktrees/worker-d` on the branch `tools/ci-efficiency-followup-a01`, created with `--no-track` from `origin/main` `3e41e36a` (PR #409's merge), at `5df527dd`, inside the sandbox. The commits are, for row `audit:4fe2438:2`, the red test `11ca625b` and the fix `c3460269`, and for row `audit:4fe2438:1`, the red test `05714d84` and the fix `4da0c7be` (with amendment 1's `private-bootstrap.yaml`). `MAIN` names the main checkout, `T` the task id, `SCRATCH` the seat's scratchpad, `CHECK` the Check's three test modules and `M` the decision test class. The output is verbatim, with the main checkout's, the home directory's and the scratchpad's paths replaced by `$MAIN`, `$HOME` and `$SCRATCH`, and each block ends with the exit status of the command shown. Every status line captures `rc=$?` (or prints `$?`) before any command substitution.

## 1. Task file (amendment 1) and task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
b2088fe0b8ddd2e9edc0c8275ed179d073bcdcffaf408afcd9dd6d9fe40d02d9  $MAIN/.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a01.md
b2088fe0b8ddd2e9edc0c8275ed179d073bcdcffaf408afcd9dd6d9fe40d02d9  .orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-ci-efficiency-followup-a01.md: OK
[exit 0]
````

## 2. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git log --oneline -1 origin/main; git merge-base origin/main HEAD; git diff --stat 3e41e36a 11ca625b; git diff --stat c3460269 05714d84
5df527dd wip(orchestration): T133 ci-efficiency follow-up a01 task copy and draft records
4da0c7be fix(ci): both bootstrap path gates read NUL-delimited paths (T133 ci-efficiency follow-up a01, audit:4fe2438:1)
05714d84 test(ci): the bootstrap decision must read paths Git quotes (T133 ci-efficiency follow-up a01, audit:4fe2438:1, red)
c3460269 fix(ci): test.yaml's relevance filter counts .github/flakes.yaml (T133 ci-efficiency follow-up a01, audit:4fe2438:2)
11ca625b test(ci): a .github/flakes.yaml-only diff must run the unit tests (T133 ci-efficiency follow-up a01, audit:4fe2438:2, red)
3e41e36a feat(ci): one run per PR head, the private bootstrap off pull requests, in-job skips and a once-only flake rerun (T133 ci-efficiency a01) (#409)
3e41e36abc949acd7e6b4859c1a22df9e665c8d4
 tests/unit/test_workflow_orchestration_skip.py | 9 +++++++++
 1 file changed, 9 insertions(+)
 tests/unit/test_workflow_orchestration_skip.py | 23 ++++++++++++++++++-----
 1 file changed, 18 insertions(+), 5 deletions(-)
[exit 0]
````

## 3. Red, each row's test on its red commit (scratch worktrees), green at the head

````console
$ git worktree add --detach -q "$SCRATCH/fu-red2" 11ca625b && uv run --directory "$SCRATCH/fu-red2" python -m unittest "$M.test_the_unit_test_decision_runs_the_registry_test_for_a_flakes_only_diff" > "$SCRATCH/fu-red2.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/fu-red2.out" /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//"; git worktree remove --force "$SCRATCH/fu-red2"
unittest exit status: 1
FAIL: test_the_unit_test_decision_runs_the_registry_test_for_a_flakes_only_diff
AssertionError: 'should_test=true\n' not found in 'diff_range=origin/main...987a4d8144b9fde9c9080c2c0ccbfb33487b131c\nshould_test=false\nskip_reason=unrelated\n'
Ran 1 test in 0.521s
FAILED (failures=1)
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/fu-red1" 05714d84 && uv run --directory "$SCRATCH/fu-red1" python -m unittest "$M.test_the_bootstrap_decision_reads_paths_that_git_quotes" > "$SCRATCH/fu-red1.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/fu-red1.out" /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//"; git worktree remove --force "$SCRATCH/fu-red1"
unittest exit status: 1
FAIL: test_the_bootstrap_decision_reads_paths_that_git_quotes (case='double-quote')
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAIL: test_the_bootstrap_decision_reads_paths_that_git_quotes (case='backslash')
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAIL: test_the_bootstrap_decision_reads_paths_that_git_quotes (case='tab')
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAIL: test_the_bootstrap_decision_reads_paths_that_git_quotes (case='newline')
AssertionError: 'should_run=false\n' != 'should_run=true\n'
Ran 1 test in 1.411s
FAILED (failures=4)
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
test_the_bootstrap_decision_reads_paths_that_git_quotes (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_bootstrap_decision_reads_paths_that_git_quotes) ... ok
test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout) ... ok
test_the_unit_test_decision_ignores_renames (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_ignores_renames) ... ok
test_the_unit_test_decision_runs_the_registry_test_for_a_flakes_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_runs_the_registry_test_for_a_flakes_only_diff) ... ok
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
test_ci_rerun_refuses_a_superseded_pull_request_head (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_refuses_a_superseded_pull_request_head) ... ok
test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_requires_signatures_for_timed_out_and_cancelled_jobs) ... ok
test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reruns_once_only_when_every_failed_job_matches_a_signature) ... ok
test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reservations_are_per_run_and_do_not_block_other_runs) ... ok
test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice (tests.unit.test_ci_rerun.CiRerunTest.test_ci_rerun_reserves_the_run_before_rerunning_and_never_reruns_twice) ... ok
test_the_production_flake_registry_matches_its_samples_and_no_real_failure (tests.unit.test_ci_rerun.CiRerunTest.test_the_production_flake_registry_matches_its_samples_and_no_real_failure) ... ok

----------------------------------------------------------------------
Ran 35 tests in 41.690s

OK
[exit 0]
````

## 4. The two bootstrap decide scripts stay equal, and the edit is the same in both files

````console
$ git show HEAD:.github/workflows/remote.yaml | sed -n "/id: decide/,/should_run=false/p" > "$SCRATCH/fu-remote.txt"; git show HEAD:.github/workflows/private-bootstrap.yaml | sed -n "/id: decide/,/should_run=false/p" > "$SCRATCH/fu-private.txt"; cmp "$SCRATCH/fu-remote.txt" "$SCRATCH/fu-private.txt" && echo "decide steps byte-identical"; git diff 3e41e36a HEAD -- .github/workflows/remote.yaml | sed 1,4d > "$SCRATCH/fu-dr.txt"; git diff 3e41e36a HEAD -- .github/workflows/private-bootstrap.yaml | sed 1,4d | sed "s/^@@ -[0-9,]* +[0-9,]* @@/@@/" > "$SCRATCH/fu-dp.txt"; sed "s/^@@ -[0-9,]* +[0-9,]* @@/@@/" "$SCRATCH/fu-dr.txt" | cmp - "$SCRATCH/fu-dp.txt" && echo "the two workflow diffs are the same hunk"
decide steps byte-identical
the two workflow diffs are the same hunk
[exit 0]
````

## 5. Lint

````console
$ shellcheck scripts/orchestrator/ci-rerun.sh && echo shellcheck-clean; shfmt -i 4 -sr -d scripts/orchestrator/ci-rerun.sh && echo "shfmt -i 4 -sr -d ci-rerun.sh (the repository form): clean"; shfmt -d scripts/orchestrator/ci-rerun.sh > /dev/null; echo "plain shfmt -d ci-rerun.sh rc=$? (.editorconfig sets indent_size without indent_style, so bare shfmt asks for tabs on every tracked script)"; git diff --quiet 3e41e36a HEAD -- scripts/orchestrator/ci-rerun.sh && echo "ci-rerun.sh is unchanged by this PR"
shellcheck-clean
shfmt -i 4 -sr -d ci-rerun.sh (the repository form): clean
plain shfmt -d ci-rerun.sh rc=1 (.editorconfig sets indent_size without indent_style, so bare shfmt asks for tabs on every tracked script)
ci-rerun.sh is unchanged by this PR
[exit 0]
````

````console
$ ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; command -v actionlint > /dev/null && actionlint .github/workflows/remote.yaml .github/workflows/private-bootstrap.yaml .github/workflows/test.yaml && echo actionlint-clean || echo "actionlint: not installed or failed (rc above)"
1 file already formatted
actionlint: not installed or failed (rc above)
[exit 0]
````

## 6. make format

````console
$ make format > "$SCRATCH/fu-format.out" 2>&1; rc=$?; echo "make format exit status: ${rc}"; base="$(git merge-base origin/main HEAD)"; sed -n "s/^diff \([^ ]*\)\.orig .*/\1/p" "$SCRATCH/fu-format.out" > "$SCRATCH/fu-flagged.txt"; echo "files the whole-tree shfmt step flags: $(wc -l < "$SCRATCH/fu-flagged.txt" | tr -d " ")"; while read -r f; do git diff --quiet "$base" HEAD -- "$f" && echo "unchanged from ${base:0:8}: $f" || echo "CHANGED by this PR: $f"; done < "$SCRATCH/fu-flagged.txt"; tail -2 "$SCRATCH/fu-format.out"
make format exit status: 2
files the whole-tree shfmt step flags: 12
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
unchanged from 3e41e36a: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
unchanged from 3e41e36a: home/dot_claude/hooks/executable_project-map-reload.sh
unchanged from 3e41e36a: tests/install/macos/common/brew.bats
 
make: *** [format] Error 1
[exit 0]
````

````console
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check
63 files already formatted
[exit 0]
````

````console
$ git ls-files -z "*.md" | xargs -0 prettier --check
Checking formatting...
All matched files use Prettier code style!
[exit 0]
````

## 7. make unit-test at the head (plain, then with the sandbox limits neutralized) and at the merge base (neutralized)

Inside the sandbox the global SSH commit signing cannot read `~/.ssh`, so most fixture commits fail in a plain run. The neutralized runs set `GIT_CONFIG_GLOBAL=/dev/null` and put the validation-only `mktemp` shim (`$SCRATCH/shim/mktemp`, which adds a `$TMPDIR` template because a bare macOS `mktemp -d` ignores `TMPDIR` and the sandbox denies the Darwin user temp directory) first on PATH, identically on both sides.

````console
$ make unit-test > "$SCRATCH/fu-unit-plain.out" 2>&1; rc=$?; echo "plain make unit-test exit status: ${rc}"; < "$SCRATCH/fu-unit-plain.out" /usr/bin/grep -E "^(Ran|OK|FAILED)"
plain make unit-test exit status: 2
Ran 1209 tests in 1149.386s
FAILED (failures=194, errors=111, skipped=2)
[exit 0]
````

````console
$ GIT_CONFIG_GLOBAL=/dev/null PATH="$SCRATCH/shim:$PATH" make unit-test > "$SCRATCH/fu-unit-head.out" 2>&1; rc=$?; echo "make unit-test at the head exit status: ${rc}"; < "$SCRATCH/fu-unit-head.out" /usr/bin/grep -E "^(Ran|OK|FAILED)"; < "$SCRATCH/fu-unit-head.out" /usr/bin/grep -E "^(FAIL|ERROR): " | sed "s/.*(\([a-z_]*\)\..*/\1/" | sort | uniq -c
make unit-test at the head exit status: 2
Ran 1209 tests in 972.020s
FAILED (failures=44, errors=10, skipped=2)
   1 ERROR: model profile standard.claude.model must be a launcher-safe string
   1 ERROR: model_profiles must define the express profile
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
   4 test_agent_stop_gate
   5 test_gh_auth
  37 test_herdr_agents
   8 test_runtime_health
[exit 0]
````

````console
$ base="$(git merge-base origin/main HEAD)"; git worktree add --detach -q "$SCRATCH/fu-base" "$base" && GIT_CONFIG_GLOBAL=/dev/null PATH="$SCRATCH/shim:$PATH" make -C "$SCRATCH/fu-base" unit-test > "$SCRATCH/fu-unit-base.out" 2>&1; rc=$?; echo "make unit-test at ${base:0:8} exit status: ${rc}"; < "$SCRATCH/fu-unit-base.out" /usr/bin/grep -E "^(Ran|OK|FAILED)"; < "$SCRATCH/fu-unit-base.out" /usr/bin/grep -E "^(FAIL|ERROR): " | sed "s/.*(\([a-z_]*\)\..*/\1/" | sort | uniq -c; git worktree remove --force "$SCRATCH/fu-base"
make unit-test at 3e41e36a exit status: 2
Ran 1207 tests in 1091.469s
FAILED (failures=44, errors=10, skipped=2)
   1 ERROR: model profile standard.claude.model must be a launcher-safe string
   1 ERROR: model_profiles must define the express profile
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
   4 test_agent_stop_gate
   5 test_gh_auth
  37 test_herdr_agents
   8 test_runtime_health
[exit 0]
````

````console
$ comm -3 <(/usr/bin/grep -E "^(FAIL|ERROR): " "$SCRATCH/fu-unit-head.out" | sort) <(/usr/bin/grep -E "^(FAIL|ERROR): " "$SCRATCH/fu-unit-base.out" | sort) | sed "s/^/only on one side: /"; n="$(comm -23 <(/usr/bin/grep -E "^(FAIL|ERROR): " "$SCRATCH/fu-unit-head.out" | sort) <(/usr/bin/grep -E "^(FAIL|ERROR): " "$SCRATCH/fu-unit-base.out" | sort) | wc -l | tr -d " ")"; echo "failing at the head but not at the base: ${n}"
failing at the head but not at the base: 0
[exit 0]
````

## 8. Caps (at most 250 changed lines outside tests/ and .orchestration/; at most 350 under tests/)

````console
$ git diff --numstat origin/main...HEAD
8	5	.github/workflows/private-bootstrap.yaml
8	5	.github/workflows/remote.yaml
3	2	.github/workflows/test.yaml
10	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a01/learning.md
52	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a01/report.md
15	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a01/sandbox.md
67	0	.orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md
27	5	tests/unit/test_workflow_orchestration_skip.py
[exit 0]
````

````console
$ git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d of 250\ntests/: %d of 350\n", o, t }'
outside tests/ and .orchestration/: 31 of 250
tests/: 32 of 350
[exit 0]
````

