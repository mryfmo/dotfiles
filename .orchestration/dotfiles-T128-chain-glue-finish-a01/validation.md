---
task_id: dotfiles-T128-chain-glue-finish-a01
seat: claude-standard-dot-a002
code_commit: 968d3439
---

# Validation: dotfiles-T128-chain-glue-finish-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's; §4's block shows the mutant script and its output, and each mutant line carries its own `rc`). Captured at `968d3439` (the code `af684dc2`, the Bot P1 fix `968d3439`).

## 1. Task file and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
8eb760cc25b1e44050b85366ac8baadafedb863eec6dcfa98e3839a512db7272  $MAIN/.orchestration/tasks/dotfiles-T128-chain-glue-finish-a01.md
8eb760cc25b1e44050b85366ac8baadafedb863eec6dcfa98e3839a512db7272  .orchestration/dotfiles-T128-chain-glue-finish-a01/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-glue-finish-a01.md: OK
[exit 0]
```
## 2. Branch and the five premises
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
968d3439 fix(orchestrator): chain-finish.sh runs HEAD's pre-merge pr-cost.sh, not the merged head's (PR #378 thread 4300324931)
a8d975c6 docs(orchestration): chain-glue finish a01 task copy and evidence (af684dc2)
af684dc2 feat(orchestrator): chain-finish.sh finishes a PR after the audit's dispositions from the main checkout's scripts, logging every step (plan 022 T8, T128 chain-glue finish a01)
5fd4fe0c32846f8e5ecbbbd027cb67f0a5be0398
[exit 0]
```
```console
$ git cat-file -e origin/main:scripts/orchestrator/chain-finish.sh && echo present || echo absent
fatal: path 'scripts/orchestrator/chain-finish.sh' exists on disk, but not in 'origin/main'
absent
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/resolve-threads.sh | /usr/bin/grep -c "^# @arg"
4
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/orch-gate.sh | /usr/bin/grep -c -e "@arg [$]2 path The PR.s checkout" -e "the review receipt, the crit JSON and the"
2
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/acceptance-front-matter.py | /usr/bin/grep -c "required. if incorrect else .refused"
1
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/pr-cost.sh | /usr/bin/grep -c -e "^# @arg \$1 int PR number" -e "metrics/pr-cost.tsv"
4
[exit 0]
```
## 3. The Check
```console
$ uv run python -m unittest tests/unit/test_chain_glue.py -v
test_finish_prints_the_acceptance_line_and_sends_nothing (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_prints_the_acceptance_line_and_sends_nothing) ... ok
test_finish_refuses_a_head_that_differs_from_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_head_that_differs_from_the_audit) ... ok
test_finish_requires_an_audit_finding_line_per_incorrect_finding (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_requires_an_audit_finding_line_per_incorrect_finding) ... ok
test_finish_runs_gate_before_merge_and_cost_after (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_gate_before_merge_and_cost_after) ... ok
test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward) ... ok
test_integrate_refuses_a_main_checkout_script_that_is_not_heads (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_main_checkout_script_that_is_not_heads) ... ok
test_integrate_refuses_a_stale_main_checkout_after_the_restart (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_stale_main_checkout_after_the_restart) ... ok
test_integrate_refuses_an_absent_owner_task_before_the_advisory_step (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_absent_owner_task_before_the_advisory_step) ... ok
test_integrate_refuses_an_extra_tsv_outside_the_main_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_extra_tsv_outside_the_main_checkout) ... ok
test_integrate_refuses_when_main_is_not_on_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_when_main_is_not_on_main) ... ok
test_integrate_resolves_binaries_before_the_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_resolves_binaries_before_the_checkout) ... ok
test_integrate_restarts_after_update_branch (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_after_update_branch) ... ok
test_integrate_restarts_when_the_base_moves_during_the_waits (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_when_the_base_moves_during_the_waits) ... ok
test_integrate_restores_the_review_worktree_after_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restores_the_review_worktree_after_the_audit) ... ok
test_integrate_runs_gh_without_forced_colour (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_gh_without_forced_colour) ... ok
test_integrate_runs_the_steps_in_order_and_logs_each (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_the_steps_in_order_and_logs_each) ... ok
test_integrate_stops_on_a_sandbox_scan_hit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_stops_on_a_sandbox_scan_hit) ... ok

----------------------------------------------------------------------
Ran 17 tests in 33.574s

OK
[exit 0]
```
```console
$ shellcheck scripts/orchestrator/chain-finish.sh && echo clean
clean
[exit 0]
```
```console
$ shfmt -i 4 -sr -d scripts/orchestrator/chain-finish.sh && echo clean
clean
[exit 0]
```
```console
$ ruff check --config ruff.toml tests/unit/test_chain_glue.py && ruff format --config ruff.toml --check tests/unit/test_chain_glue.py
All checks passed!
1 file already formatted
[exit 0]
```
```console
$ wc -l scripts/orchestrator/chain-finish.sh
     148 scripts/orchestrator/chain-finish.sh
[exit 0]
```
## 4. Mutation check (each mutant applied alone with sed, its test run, the file restored with git checkout; then a baseline run)
```console
$ bash "$TMPDIR/cgf/mutate.sh" (the script, then its output)
S=scripts/orchestrator/chain-finish.sh T=tests/unit/test_chain_glue.py
run() { # label sed-expression test
    sed -i '' "$2" "$S"
    git diff -U0 -- "$S" | /usr/bin/grep -v -E '^(---|\+\+\+|@@|diff|index)' || echo "(sed changed nothing)"
    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$3" > "$TMPDIR/cgf/m.log" 2>&1
    echo "mutant=$1 test=$3 rc=$? $(tail -1 "$TMPDIR/cgf/m.log")"
    git checkout -- "$S"
}
H=test_finish_refuses_a_head_that_differs_from_the_audit F=test_finish_requires_an_audit_finding_line_per_incorrect_finding
O=test_finish_runs_gate_before_merge_and_cost_after A=test_finish_prints_the_acceptance_line_and_sends_nothing
run head-check-off 's|\[\[ ${out} == "${head}" \&\& -f ${summary} \]\] \|\||true \|\||' $H
run gate-input-off '/refuse 10 "gate input missing/d' $H
run canonical-off 's|\[ "${review}" = "${canonical}" \] \|\||true \|\||' $H
run finding-line-off '/refuse 12 "audit finding/d' $F
run dispositions-never 's|\[\[ ${verdict} == "Verdict: correct" \]\] \|\| extra_args=|true \|\| extra_args=|' $F
run verdict-check-off '/refuse 12 "unexpected audit verdict/d' $F
run trap-off '/^trap /d' $F
run gate-gone '/^step gate 0/d' $O
run unbound-merge 's|--match-head-commit "${head}" ||' $O
run ff-gone '/^step ff-main 0/d' $O
run sends 's|^echo "${accept}"|agmsg-dispatch x; echo "${accept}"|' $A
run line-form 's|status=accepted reason=merged-as-|status=accepted reason=merged-|' $A
run merged-pr-cost 's|^step pr-cost 0 "${BASH}" "${cost}" "${pr}"|step pr-cost 0 "${main}/scripts/orchestrator/pr-cost.sh" "${pr}"|' test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward
UV_OFFLINE=1 uv run python -m unittest "$T" > "$TMPDIR/cgf/m.log" 2>&1; echo "baseline rc=$? $(tail -1 "$TMPDIR/cgf/m.log")"
git status --short -- scripts/
--- output
-[[ ${out} == "${head}" && -f ${summary} ]] || refuse 10 "head differs from the audit: ${head} (PR ${out}, summary ${summary#"${main}"/})"
+true || refuse 10 "head differs from the audit: ${head} (PR ${out}, summary ${summary#"${main}"/})"
mutant=head-check-off test=test_finish_refuses_a_head_that_differs_from_the_audit rc=1 FAILED (failures=1)
-    [ -f "${f}" ] || refuse 10 "gate input missing: ${f#"${main}"/}"
mutant=gate-input-off test=test_finish_refuses_a_head_that_differs_from_the_audit rc=1 FAILED (failures=1)
-[ "${review}" = "${canonical}" ] || refuse 10 "review worktree is not the canonical one: ${canonical}"
+true || refuse 10 "review worktree is not the canonical one: ${canonical}"
mutant=canonical-off test=test_finish_refuses_a_head_that_differs_from_the_audit rc=1 FAILED (failures=1)
-    [ -n "${line}" ] || refuse 12 "audit finding ${n} of ${sha7} has no audit-finding line"
mutant=finding-line-off test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-[[ ${verdict} == "Verdict: correct" ]] || extra_args=(--audit-dispositions "${dispositions}")
+true || extra_args=(--audit-dispositions "${dispositions}")
mutant=dispositions-never test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-[[ ${verdict} == "Verdict: correct" || ${verdict} == "Verdict: incorrect" ]] || refuse 12 "unexpected audit verdict: ${verdict}"
mutant=verdict-check-off test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-trap 'rm -f -- "${comments}" "${ledger}" "${dispositions}" "${cost}"' EXIT
mutant=trap-off test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-step gate 0 "${main}/scripts/orchestrator/orch-gate.sh" "${task}" "${review}" "${pr}"
mutant=gate-gone test=test_finish_runs_gate_before_merge_and_cost_after rc=1 FAILED (failures=1)
-step merge 0 "${gh}" pr merge --squash --match-head-commit "${head}" "${pr}"
+step merge 0 "${gh}" pr merge --squash "${pr}"
mutant=unbound-merge test=test_finish_runs_gate_before_merge_and_cost_after rc=1 FAILED (failures=1)
-step ff-main 0 "${main}/scripts/orchestrator/ff-main.sh"
mutant=ff-gone test=test_finish_runs_gate_before_merge_and_cost_after rc=1 FAILED (failures=1)
-echo "${accept}"
+agmsg-dispatch x; echo "${accept}"
mutant=sends test=test_finish_prints_the_acceptance_line_and_sends_nothing rc=1 FAILED (failures=1)
-accept="AGMSG-ACCEPTANCE v1 task_id=${task} status=accepted reason=merged-as-${merged}-pr-${pr}-head-${sha7} next_action=<the orchestrator fills this before sending>"
+accept="AGMSG-ACCEPTANCE v1 task_id=${task} status=accepted reason=merged-${merged}-pr-${pr}-head-${sha7} next_action=<the orchestrator fills this before sending>"
mutant=line-form test=test_finish_prints_the_acceptance_line_and_sends_nothing rc=1 FAILED (failures=1)
-step pr-cost 0 "${BASH}" "${cost}" "${pr}"
+step pr-cost 0 "${main}/scripts/orchestrator/pr-cost.sh" "${pr}"
mutant=merged-pr-cost test=test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward rc=1 FAILED (failures=1)
baseline rc=0 OK
[exit 0]
```
## 5. Caps
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/autoskill.md
6	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/learning.md
55	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/report.md
27	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/sandbox.md
121	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/task.md
171	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/validation.md
148	0	scripts/orchestrator/chain-finish.sh
169	0	tests/unit/test_chain_glue.py
[exit 0]
```
