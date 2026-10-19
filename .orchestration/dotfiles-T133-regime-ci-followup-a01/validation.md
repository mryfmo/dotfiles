---
task_id: dotfiles-T133-regime-ci-followup-a01
seat: claude-standard-dot-a011
code_head: b65dd4c2
---

# Validation: dotfiles-T133-regime-ci-followup-a01

Every command below ran from the worktree `.claude/worktrees/worker-d` on the branch `tools/regime-ci-followup-a01`, created with `--no-track` from `origin/main` `0e496ce7` (PR #418's merge), inside the sandbox. `origin/main` has since moved to `86ea9884`, which is the base sha the regime job would use, so the bootstrap runs from there (§2 lists what moved). Two identities apply, by the rule of row `audit:7fad835:2`. The bootstrap target is the code head `b65dd4c2`: the task copy and `pr-body.md` (`e0565b47`), the red tests (`6c96e10a`), the workflow fix (`e6ea7c8d`) and the workflow review's test and comment fixes (`b65dd4c2`) of row `ci:39185982423:1`. The final head is the next commit, which adds this record and the other evidence. It touches only `.orchestration/dotfiles-T133-regime-ci-followup-a01/` (the RESULT lists its paths) and adds none of the three files regime-ci.py reads there (`task.md`, `precheck.json`, `result.txt`), so the bootstrap's verdict carries to the final head. The regime job's own run on the final head (`gh run view`) goes in the RESULT, because a record cannot hold its own commit's CI. `MAIN` names the main checkout, `T` the task id, `SCRATCH` the seat's scratchpad, `BASE` the base sha (current `origin/main`, not the merge base `0e496ce7`), `H` the bootstrapped code head and `TESTS` the five tests of §5. The output is verbatim, with the main checkout's, the home directory's and the scratchpad's paths replaced by `$MAIN`, `$HOME` and `$SCRATCH`, and each block ends with the exit status of the command shown. Every status line captures `rc=$?` before any command substitution.

## 1. Task file and task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
65d4b24a390674b303e7dcad6a305be7584ebf49e5f3776f2560dd9ffc14a0a1  $MAIN/.orchestration/tasks/dotfiles-T133-regime-ci-followup-a01.md
65d4b24a390674b303e7dcad6a305be7584ebf49e5f3776f2560dd9ffc14a0a1  .orchestration/dotfiles-T133-regime-ci-followup-a01/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-regime-ci-followup-a01.md: OK
[exit 0]
````

## 2. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git log --oneline 0e496ce7..origin/main; git merge-base origin/main HEAD; git diff --name-status origin/main...b65dd4c2
b65dd4c2 test(ci): the moved-base test models PR #420, the head guard keeps its strength, the comments state the observed lag (T133 regime-ci follow-up a01, ci:39185982423:1, workflow review P3s)
e6ea7c8d fix(ci): the regime job checks out the base branch's tip and verifies against it (T133 regime-ci follow-up a01, ci:39185982423:1)
6c96e10a test(ci): the regime job must take its base from the base branch's tip at run time (T133 regime-ci follow-up a01, ci:39185982423:1, red)
e0565b47 docs(orchestration): T133 regime-ci follow-up a01 task copy and PR #418's corrected title and body (audit:f7d2c48:3)
86ea9884 fix(herdr): isolate worker seat lock Python imports (#422)
0e496ce7449e9286aeac3b2770cbff374c7dc5cf
M	.github/workflows/regime.yml
A	.orchestration/dotfiles-T133-regime-ci-followup-a01/pr-body.md
A	.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md
M	tests/unit/test_regime_ci.py
M	tests/unit/test_workflow_security.py
[exit 0]
````

## 3. The Check's test modules: row ci:39185982423:1 red on 6c96e10a (the tests, the workflow unchanged), then green at the head

````console
$ git worktree add --detach -q "$SCRATCH/rc-red" 6c96e10a && uv run --directory "$SCRATCH/rc-red" python -m unittest tests.unit.test_workflow_security tests.unit.test_regime_ci > "$SCRATCH/rc-red.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/rc-red.out" /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | cut -c1-220; git worktree remove --force "$SCRATCH/rc-red"
unittest exit status: 1
FAIL: test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time
AssertionError: 'pull_request.base.sha' unexpectedly found in 'name: regime\n\n# The regime job (plan 024 P1-11, redesigned in T133 regime-ci a02): a pull request that carries a task copy is checked\n# by the base\'s scr
FAIL: test_the_regime_workflow_runs_base_code_only
AssertionError: {'fet[17 chars]f': 'refs/heads/${{ github.base_ref }}', 'pers[19 chars]alse} != {'fet[17 chars]f': '${{ github.event.pull_request.base.sha }}[27 chars]alse}
Ran 25 tests in 36.702s
FAILED (failures=2)
[exit 0]
````

````console
$ uv run python -m unittest tests.unit.test_regime_ci -v
test_regime_ci_accepts_a_base_that_moved_past_the_merge_base (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_accepts_a_base_that_moved_past_the_merge_base) ... ok
test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) ... ok
test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_checks_the_copy_against_result_txt_without_dispatched_text) ... ok
test_regime_ci_exempts_records_only_heads_by_content_not_branch_name (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_exempts_records_only_heads_by_content_not_branch_name) ... ok
test_regime_ci_keeps_an_authenticated_predecessor_a_head_only_successor_names (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_keeps_an_authenticated_predecessor_a_head_only_successor_names) ... ok
test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker) ... ok
test_regime_ci_passes_a_records_only_pr_with_no_target (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_passes_a_records_only_pr_with_no_target) ... ok
test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier) ... ok
test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list) ... ok
test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_a_copy_whose_task_id_is_not_its_directory) ... ok
test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr) ... ok
test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config) ... ok
test_regime_ci_supersedes_a_predecessor_only_when_both_copies_are_byte_equal_to_base (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_supersedes_a_predecessor_only_when_both_copies_are_byte_equal_to_base) ... ok
test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_unverifiable_copy_is_a_warning_until_the_flag) ... ok
test_regime_ci_warns_without_precheck_and_without_dispatched_text (tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_warns_without_precheck_and_without_dispatched_text) ... ok
test_the_regime_workflow_runs_base_code_only (tests.unit.test_regime_ci.RegimeCiTest.test_the_regime_workflow_runs_base_code_only) ... ok

----------------------------------------------------------------------
Ran 16 tests in 38.083s

OK
[exit 0]
````

````console
$ uv run python -m unittest tests.unit.test_workflow_security -v
test_checkout_does_not_persist_credentials_without_explicit_exemption (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_does_not_persist_credentials_without_explicit_exemption) ... ok
test_checkout_rejects_duplicate_or_non_false_credential_settings (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_rejects_duplicate_or_non_false_credential_settings) ... ok
test_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_external_actions_use_full_commit_shas (tests.unit.test_workflow_security.WorkflowSecurityTest.test_external_actions_use_full_commit_shas) ... ok
test_quoted_unnamed_checkout_is_detected (tests.unit.test_workflow_security.WorkflowSecurityTest.test_quoted_unnamed_checkout_is_detected) ... ok
test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time (tests.unit.test_workflow_security.WorkflowSecurityTest.test_the_regime_workflow_takes_its_base_from_the_base_branch_tip_at_run_time) ... ok
test_unnamed_checkout_setting_does_not_leak_from_the_next_step (tests.unit.test_workflow_security.WorkflowSecurityTest.test_unnamed_checkout_setting_does_not_leak_from_the_next_step) ... ok
test_workflows_have_exact_top_level_permissions (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_exact_top_level_permissions) ... ok
test_workflows_have_no_job_level_permission_overrides (tests.unit.test_workflow_security.WorkflowSecurityTest.test_workflows_have_no_job_level_permission_overrides) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.005s

OK
[exit 0]
````

The regime-ci test of this row passes on the unchanged verifier, so it cannot be red on `6c96e10a`. It is shown to guard the claim instead: in a scratch copy of the head, the verifier reads the dispatched text at the merge base rather than at `--base`, and the test goes red.

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    dispatched = show(root, base, f".orchestration/tasks/{t}.md")' '    dispatched = show(root, git(root, "merge-base", base, head).stdout.decode().strip(), f".orchestration/tasks/{t}.md")' && uv run --directory "$SCRATCH/rc-mut" python -m unittest tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_accepts_a_base_that_moved_past_the_merge_base > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "the dispatched text at the merge base: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: dispatched = show(root, base, f".orchestration/tasks/{t}.md") -> dispatched = show(root, git(root, "merge-base", base, head).stdout.decode().strip(), f".orchestration/tasks/{t}.md")
the dispatched text at the merge base: unittest exit status: 1
   1 FAIL: test_regime_ci_accepts_a_base_that_moved_past_the_merge_base
   1 FAILED (failures=1)
   1 Ran 1 test in 1.321s
[exit 0]
````

## 4. The local bootstrap: the regime job's command line from an isolated base checkout, the head as data

This is the command the fixed `.github/workflows/regime.yml` runs: `--base "$(git rev-parse HEAD)"` from a checkout of the base branch's tip. It runs from a scratch worktree checked out at the base `86ea9884` (current `origin/main`), so the verifier (as it landed in \`0e496ce7\`) and the base checker both come from the base. The head `b65dd4c2` sits in the shared object store and is read only through `git show`. This task's dispatched text is not on the base, so the copy is unverifiable and the checker is skipped. Both are expected warnings during that transition. precheck.json is absent, another documented warning.

````console
$ git worktree add --detach -q "$SCRATCH/rc-base" "$BASE" && git -C "$SCRATCH/rc-base" rev-parse HEAD && echo "head: $(git rev-parse "$H")" && git -C "$SCRATCH/rc-base" cat-file -t "$H" && (cd "$SCRATCH/rc-base" && HEAD_SHA="$(git rev-parse "$H")" && uv run --no-config --no-project --with pyyaml python -I scripts/orchestrator/regime-ci.py --base "$(git rev-parse HEAD)" --head "${HEAD_SHA}"); rc=$?; echo "regime-ci exit status: ${rc}"; git worktree remove --force "$SCRATCH/rc-base"
86ea98848b595f53e0afcf8f298ebda311a51dcf
head: b65dd4c2128619934eb733de9998ab54909268ca
commit
regime-ci: warning: the diff changes .github/workflows/regime.yml; this run executed the base's version, the audit reads the change
regime-ci: warning: dotfiles-T133-regime-ci-followup-a01: task copy unverifiable (no dispatched text at base)
regime-ci: warning: dotfiles-T133-regime-ci-followup-a01: checker skipped: the copy is unverifiable, and the base's checker reads only the base's text
regime-ci: warning: dotfiles-T133-regime-ci-followup-a01: precheck absent
regime-ci: warning: dotfiles-T133-regime-ci-followup-a01: no outside cap in the copy's ## Check section
regime-ci: warning: dotfiles-T133-regime-ci-followup-a01: no tests/ cap in the copy's ## Check section
regime-ci: ok 1 task(s)
regime-ci exit status: 0
[exit 0]
````

## 5. Row audit:7fad835:1: the five tests that close the regime-ci.py control, each red when a check it covers is disabled

Each block copies the head into a scratch worktree, replaces one line of `scripts/orchestrator/regime-ci.py` so that one claimed check stops reporting, and runs the five tests in `TESTS`: the base-verifier test, the violation table, the no-target exemption test, the test that no pull request text reaches the checker, and the test that refuses a checkout not at the base. The replacement is asserted to apply exactly once. The first block is the unmutated baseline. The last three mutations came from the worker review: the three-test selector missed them.
````console
$ printf "%s\n" $TESTS
tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier
tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr
tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_passes_a_records_only_pr_with_no_target
tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker
tests.unit.test_regime_ci.RegimeCiTest.test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list
[exit 0]
````


````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "baseline: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED"; git worktree remove --force "$SCRATCH/rc-mut"
baseline: unittest exit status: 0
Ran 5 tests in 23.169s
OK
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    found += checker(root, data) if dispatched else []' '    found += []' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "base checker: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: found += checker(root, data) if dispatched else [] -> found += []
base checker: unittest exit status: 1
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='checker crash')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='checker exit')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='checker')
   1 FAILED (failures=3)
   1 Ran 5 tests in 20.044s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '        if data != copy:' '        if False:' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "dispatched-text authentication: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: if data != copy: -> if False:
dispatched-text authentication: unittest exit status: 1
   1 FAIL: test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (dispatched=True)
   1 FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=1, phrase='task-copy: ')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='task-copy')
   1 FAILED (failures=3)
   1 Ran 5 tests in 22.265s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    found += [("precheck", detail) for detail in bound or []]' '    found += []' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "precheck binding: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: found += [("precheck", detail) for detail in bound or []] -> found += []
precheck binding: unittest exit status: 1
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck head')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck late')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck none')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck renamed')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck reverted')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck sha')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck side')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='precheck symbolic')
   1 FAILED (failures=8)
   1 Ran 5 tests in 25.819s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '        if not p.startswith(exempt) and not any(allowed(p, a) for a in entries)' '        if False' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "allowed files: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: if not p.startswith(exempt) and not any(allowed(p, a) for a in entries) -> if False
allowed files: unittest exit status: 1
   1 FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=1, phrase='allowed-files: stray.sh is outside allowed_files')
   1 FAIL: test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (expected=1, phrase='task-copy: ')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='allowed-files')
   1 FAILED (failures=3)
   1 Ran 5 tests in 22.518s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    found += [("caps", detail) for detail in exceeded]' '    found += []' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "caps: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: found += [("caps", detail) for detail in exceeded] -> found += []
caps: unittest exit status: 1
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='caps outside')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='caps tests')
   1 FAIL: test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (case='caps worded')
   1 FAILED (failures=3)
   1 Ran 5 tests in 24.111s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '        if not stray:' '        if True:' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "content-based exemption: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: if not stray: -> if True:
content-based exemption: unittest exit status: 1
   1 FAIL: test_regime_ci_passes_a_records_only_pr_with_no_target
   1 FAILED (failures=1)
   1 Ran 5 tests in 21.739s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    found += checker(root, data) if dispatched else []' '    found += checker(root, copy) if dispatched else []' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "the pull request text to the checker: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: found += checker(root, data) if dispatched else [] -> found += checker(root, copy) if dispatched else []
the pull request text to the checker: unittest exit status: 1
   1 FAIL: test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (dispatched=True)
   1 FAILED (failures=1)
   1 Ran 5 tests in 23.224s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    found += checker(root, data) if dispatched else []' '    found += checker(root, data) if dispatched else checker(root, copy)' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "the checker on an unverifiable copy: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: found += checker(root, data) if dispatched else [] -> found += checker(root, data) if dispatched else checker(root, copy)
the checker on an unverifiable copy: unittest exit status: 1
   1 FAIL: test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (dispatched=False)
   1 FAIL: test_regime_ci_never_feeds_a_pull_request_s_text_to_the_base_checker (dispatched=True)
   1 FAILED (failures=2)
   1 Ran 5 tests in 25.068s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/rc-mut" HEAD && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/rc-mut/scripts/orchestrator/regime-ci.py" '    if at != base:' '    if False:' && uv run --directory "$SCRATCH/rc-mut" python -m unittest $TESTS > "$SCRATCH/rc-mut.out" 2>&1; rc=$?; echo "the checkout-at-base refusal: unittest exit status: ${rc}"; < "$SCRATCH/rc-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/rc-mut"
mutated: if at != base: -> if False:
the checkout-at-base refusal: unittest exit status: 1
   1 FAIL: test_regime_ci_refuses_a_checkout_not_at_the_base_and_a_diff_git_cannot_list
   1 FAILED (failures=1)
   1 Ran 5 tests in 25.564s
[exit 0]
````

## 6. Caps and the evidence commit's paths

````console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD -- . ; git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d of 330\ntests/: %d of 480\n", o, t }'
4	3	.github/workflows/regime.yml
48	0	.orchestration/dotfiles-T133-regime-ci-followup-a01/pr-body.md
62	0	.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md
15	4	tests/unit/test_regime_ci.py
9	0	tests/unit/test_workflow_security.py
4	3	.github/workflows/regime.yml
48	0	.orchestration/dotfiles-T133-regime-ci-followup-a01/pr-body.md
62	0	.orchestration/dotfiles-T133-regime-ci-followup-a01/task.md
15	4	tests/unit/test_regime_ci.py
9	0	tests/unit/test_workflow_security.py
outside tests/ and .orchestration/: 7 of 330
tests/: 28 of 480
[exit 0]
````

This record is part of the final head, so it cannot list that commit's own paths. The RESULT carries `git diff --name-only b65dd4c2 <final head>`, which lists only `.orchestration/dotfiles-T133-regime-ci-followup-a01/` paths.

## 7. make format

````console
$ make format > "$SCRATCH/rc-format.out" 2>&1; rc=$?; echo "make format exit status: ${rc}"; base="$(git merge-base origin/main HEAD)"; sed -n "s/^diff \([^ ]*\)\.orig .*/\1/p" "$SCRATCH/rc-format.out" > "$SCRATCH/rc-flagged.txt"; echo "files the whole-tree shfmt step flags: $(wc -l < "$SCRATCH/rc-flagged.txt" | tr -d " ")"; while read -r f; do git diff --quiet "$base" HEAD -- "$f" && echo "unchanged from ${base:0:8}: $f" || echo "CHANGED by this PR: $f"; done < "$SCRATCH/rc-flagged.txt"
make format exit status: 2
files the whole-tree shfmt step flags: 12
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
unchanged from 0e496ce7: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
unchanged from 0e496ce7: home/dot_claude/hooks/executable_project-map-reload.sh
unchanged from 0e496ce7: tests/install/macos/common/brew.bats
[exit 0]
````

````console
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check; git ls-files -z "*.md" | xargs -0 prettier --check
65 files already formatted
Checking formatting...
All matched files use Prettier code style!
[exit 0]
````

