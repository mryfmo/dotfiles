---
task_id: dotfiles-T128-chain-glue-finish-a01
seat: claude-standard-dot-a002
code_commit: 2171d927
---

# Validation: dotfiles-T128-chain-glue-finish-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's; §4's block shows the mutant script and its output, and each mutant line carries its own `rc`). Captured at `2171d927` (the code `af684dc2`, the Bot P1 fix `968d3439`, revise round 1 `60cdac47`, the orchestrator's update-branch merge `f4d86ee5`, revise round 2 `2171d927`).

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
2171d927 fix(orchestrator): chain-finish.sh runs pr-cost.sh with resolved tool links, reads the verdict and the reason as the gate does (T128 chain-glue finish a01 revise round 2)
f4d86ee5 Merge branch 'main' into tools/chain-glue-finish
9d5b9d29 docs(orchestration): chain-glue finish a01 revise round 1 evidence (60cdac47)
60cdac47 fix(orchestrator): chain-finish.sh checks each audit-finding line in the gate's grammar (PR #378 thread 4300359437)
72d0cd07 docs(orchestration): chain-glue finish a01 report: the test file's line count from numstat (169)
f13fed9f docs(orchestration): chain-glue finish a01 evidence update (the Bot's P1 thread 4300324931, fixed in 968d3439)
968d3439 fix(orchestrator): chain-finish.sh runs HEAD's pre-merge pr-cost.sh, not the merged head's (PR #378 thread 4300324931)
a8d975c6 docs(orchestration): chain-glue finish a01 task copy and evidence (af684dc2)
af684dc2 feat(orchestrator): chain-finish.sh finishes a PR after the audit's dispositions from the main checkout's scripts, logging every step (plan 022 T8, T128 chain-glue finish a01)
f7847616970d6bd83739a75a65ad8f7c35e91462
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
test_finish_checks_each_audit_finding_line_in_full (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_checks_each_audit_finding_line_in_full) ... ok
test_finish_counts_the_trimmed_reason (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_counts_the_trimmed_reason) ... ok
test_finish_prints_the_acceptance_line_and_sends_nothing (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_prints_the_acceptance_line_and_sends_nothing) ... ok
test_finish_reads_the_last_nonblank_line_as_the_verdict (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_reads_the_last_nonblank_line_as_the_verdict) ... ok
test_finish_refuses_a_head_that_differs_from_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_head_that_differs_from_the_audit) ... ok
test_finish_requires_an_audit_finding_line_per_incorrect_finding (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_requires_an_audit_finding_line_per_incorrect_finding) ... ok
test_finish_runs_gate_before_merge_and_cost_after (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_gate_before_merge_and_cost_after) ... ok
test_finish_runs_pr_cost_with_a_path_of_resolved_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_pr_cost_with_a_path_of_resolved_links) ... ok
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
Ran 21 tests in 65.709s

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
     164 scripts/orchestrator/chain-finish.sh
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
lrun() { # label old new test: as run, with a literal string replacement (python's str.replace, once)
    python3 -I -c 'import sys; p, a, b = sys.argv[1:]; t = open(p).read(); assert t.count(a) == 1, a; open(p, "w").write(t.replace(a, b))' "$S" "$2" "$3"
    git diff -U0 -- "$S" | /usr/bin/grep -v -E '^(---|\+\+\+|@@|diff|index)' || echo "(nothing changed)"
    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$4" > "$TMPDIR/cgf/m.log" 2>&1
    echo "mutant=$1 test=$4 rc=$? $(tail -1 "$TMPDIR/cgf/m.log")"
    git checkout -- "$S"
}
lrun grammar-off 'refuse 12 "audit finding ${n} of ${sha7}: the line is not not-applicable:<reason of 20 or more characters>; evidence=<command>"' 'true' test_finish_checks_each_audit_finding_line_in_full
lrun reason-length-off ' && ${#reason} -ge 20' '' test_finish_checks_each_audit_finding_line_in_full
lrun evidence-text-off ' && ${evidence} =~ [^[:space:]]' '' test_finish_checks_each_audit_finding_line_in_full
lrun second-delimiter-off ' && ${evidence} != *"; evidence="*' '' test_finish_checks_each_audit_finding_line_in_full
lrun tab-check-off ' && ${line} != *$'"'"'\t'"'"'*' '' test_finish_checks_each_audit_finding_line_in_full
lrun merged-pr-cost 'step pr-cost 0 cost_run "${pr}"' 'step pr-cost 0 "${main}/scripts/orchestrator/pr-cost.sh" "${pr}"' test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward
lrun tools-path-off 'env -i PATH="${tools}" HOME="${HOME}" "${BASH}"' '"${BASH}"' test_finish_runs_pr_cost_with_a_path_of_resolved_links
lrun tools-shims-off '[[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no ${name} for pr-cost.sh' 'true || refuse 10 "no ${name} for pr-cost.sh' test_finish_runs_pr_cost_with_a_path_of_resolved_links
lrun verdict-last-line "verdict=\$(/usr/bin/grep -v -E '^[[:space:]]*\$' \"\${summary}\" | tail -n 1 | sed -E 's/^[[:space:]]+|[[:space:]]+\$//g' || true)" 'verdict=$(tail -n 1 -- "${summary}")' test_finish_reads_the_last_nonblank_line_as_the_verdict
lrun reason-untrimmed "reason=\$(printf '%s' \"\${body%%; evidence=*}\" | sed -E 's/^[[:space:]]+|[[:space:]]+\$//g')" 'reason=${body%%; evidence=*}' test_finish_counts_the_trimmed_reason
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
-        refuse 12 "audit finding ${n} of ${sha7}: the line is not not-applicable:<reason of 20 or more characters>; evidence=<command>"
mutant=finding-line-off test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-[[ ${verdict} == "Verdict: correct" ]] || extra_args=(--audit-dispositions "${dispositions}")
+true || extra_args=(--audit-dispositions "${dispositions}")
mutant=dispositions-never test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-[[ ${verdict} == "Verdict: correct" || ${verdict} == "Verdict: incorrect" ]] || refuse 12 "unexpected audit verdict: ${verdict}"
mutant=verdict-check-off test=test_finish_requires_an_audit_finding_line_per_incorrect_finding rc=1 FAILED (failures=1)
-trap 'rm -f -- "${comments}" "${ledger}" "${dispositions}" "${cost}" && rm -rf -- "${tools}"' EXIT
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
-        refuse 12 "audit finding ${n} of ${sha7}: the line is not not-applicable:<reason of 20 or more characters>; evidence=<command>"
+        true
mutant=grammar-off test=test_finish_checks_each_audit_finding_line_in_full rc=1 FAILED (failures=6)
-    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${evidence} =~ [^[:space:]] && ${#reason} -ge 20 && ${line} != *$'\t'* ]] ||
+    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${evidence} =~ [^[:space:]] && ${line} != *$'\t'* ]] ||
mutant=reason-length-off test=test_finish_checks_each_audit_finding_line_in_full rc=1 FAILED (failures=3)
-    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${evidence} =~ [^[:space:]] && ${#reason} -ge 20 && ${line} != *$'\t'* ]] ||
+    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${#reason} -ge 20 && ${line} != *$'\t'* ]] ||
mutant=evidence-text-off test=test_finish_checks_each_audit_finding_line_in_full rc=1 FAILED (failures=4)
-    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${evidence} =~ [^[:space:]] && ${#reason} -ge 20 && ${line} != *$'\t'* ]] ||
+    [[ ${body} == *"; evidence="* && ${evidence} =~ [^[:space:]] && ${#reason} -ge 20 && ${line} != *$'\t'* ]] ||
mutant=second-delimiter-off test=test_finish_checks_each_audit_finding_line_in_full rc=1 FAILED (failures=5)
-    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${evidence} =~ [^[:space:]] && ${#reason} -ge 20 && ${line} != *$'\t'* ]] ||
+    [[ ${body} == *"; evidence="* && ${evidence} != *"; evidence="* && ${evidence} =~ [^[:space:]] && ${#reason} -ge 20 ]] ||
mutant=tab-check-off test=test_finish_checks_each_audit_finding_line_in_full rc=1 FAILED (failures=2)
-step pr-cost 0 cost_run "${pr}"
+step pr-cost 0 "${main}/scripts/orchestrator/pr-cost.sh" "${pr}"
mutant=merged-pr-cost test=test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward rc=1 FAILED (failures=1)
-cost_run() { env -i PATH="${tools}" HOME="${HOME}" "${BASH}" "${cost}" "$1"; } # HOME stays out of the log line
+cost_run() { "${BASH}" "${cost}" "$1"; } # HOME stays out of the log line
mutant=tools-path-off test=test_finish_runs_pr_cost_with_a_path_of_resolved_links rc=1 FAILED (failures=1)
-    [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no ${name} for pr-cost.sh outside a shims directory: ${found:-none}"
+    true || refuse 10 "no ${name} for pr-cost.sh outside a shims directory: ${found:-none}"
mutant=tools-shims-off test=test_finish_runs_pr_cost_with_a_path_of_resolved_links rc=1 FAILED (failures=1)
-verdict=$(/usr/bin/grep -v -E '^[[:space:]]*$' "${summary}" | tail -n 1 | sed -E 's/^[[:space:]]+|[[:space:]]+$//g' || true)
+verdict=$(tail -n 1 -- "${summary}")
mutant=verdict-last-line test=test_finish_reads_the_last_nonblank_line_as_the_verdict rc=1 FAILED (failures=1)
-    reason=$(printf '%s' "${body%%; evidence=*}" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g')
+    reason=${body%%; evidence=*}
mutant=reason-untrimmed test=test_finish_counts_the_trimmed_reason rc=1 FAILED (failures=1)
baseline rc=0 OK
[exit 0]
```
## 5. Caps
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/autoskill.md
6	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/learning.md
63	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/report.md
27	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/sandbox.md
121	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/task.md
216	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/validation.md
164	0	scripts/orchestrator/chain-finish.sh
225	1	tests/unit/test_chain_glue.py
[exit 0]
```
