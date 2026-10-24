---
task_id: dotfiles-T128-chain-glue-finish-a01
seat: claude-standard-dot-a006
earlier_seat: claude-standard-dot-a002
code_commit: 6fba7690
---

# Validation: dotfiles-T128-chain-glue-finish-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's; §4's block shows the mutant script and its output, and each mutant line carries its own `rc`). §1 to §5 were captured by `claude-standard-dot-a002` at `14033382` (the code `af684dc2`, the Bot P1 fix `968d3439`, revise round 1 `60cdac47`, the orchestrator's update-branch merge `f4d86ee5`, revise round 2 `2171d927`, the macOS 14 jq fixture `14033382`). §6 was captured by `claude-standard-dot-a006` at `4d4e3b22` (revise round 3), and §7 at `6fba7690` (revise round 4, ACCEPTANCE round 5), each block run by a runner that prints the command, its output and `[exit <status>]`; the two unittest runs piped into `grep` carry `set -o pipefail`, so their status is unittest's.

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
14033382 test(orchestrator): link the test's jq into the stub directory, since macOS 14 has none in /usr/bin (CI on 27757afb)
27757afb docs(orchestration): chain-glue finish a01 revise round 2 evidence (2171d927)
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
Ran 21 tests in 60.287s

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
72	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/report.md
27	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/sandbox.md
121	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/task.md
238	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/validation.md
164	0	scripts/orchestrator/chain-finish.sh
227	1	tests/unit/test_chain_glue.py
[exit 0]
```

## 6. Revise round 3 (the local review of f20826e, local:f20826e:1), captured at 4d4e3b22

The task copy and the checker; the branch and its base; the new test against `f20826e2`'s script (red), restored; the Check on `4d4e3b22`; the linters; one mutant (the new refusal line deleted), restored; the caps.

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
```console
$ git log --oneline -2; git merge-base origin/main HEAD; git rev-parse origin/main
4d4e3b22 fix(orchestrator): chain-finish.sh refuses a sweep whose head is not the audited head before any GitHub write (T128 chain-glue finish a01 revise round 3)
f20826e2 Merge branch 'main' into tools/chain-glue-finish
af4f1e997f78119d5994d7d7b1966894d62bbc6a
af4f1e997f78119d5994d7d7b1966894d62bbc6a
[exit 0]
```
```console
$ git show f20826e2:scripts/orchestrator/chain-finish.sh > scripts/orchestrator/chain-finish.sh && git diff --stat
 scripts/orchestrator/chain-finish.sh | 6 ++----
 1 file changed, 2 insertions(+), 4 deletions(-)
[exit 0]
```
```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head 2>&1 | grep -E '^(FAIL|AssertionError|Ran|FAILED|OK)'
FAIL: test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head)
AssertionError: 10 != 0 : resolve-threads rc=0
Ran 1 test in 3.887s
FAILED (failures=1)
[exit 1]
```
```console
$ git checkout -- scripts/orchestrator/chain-finish.sh && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to 4d4e3b22
[exit 0]
```
```console
$ uv run python -m unittest tests/unit/test_chain_glue.py -v
test_finish_checks_each_audit_finding_line_in_full (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_checks_each_audit_finding_line_in_full) ... ok
test_finish_counts_the_trimmed_reason (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_counts_the_trimmed_reason) ... ok
test_finish_prints_the_acceptance_line_and_sends_nothing (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_prints_the_acceptance_line_and_sends_nothing) ... ok
test_finish_reads_the_last_nonblank_line_as_the_verdict (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_reads_the_last_nonblank_line_as_the_verdict) ... ok
test_finish_refuses_a_head_that_differs_from_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_head_that_differs_from_the_audit) ... ok
test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head) ... ok
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
Ran 22 tests in 101.699s

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
$ n=$(grep -n 'not the audited head' scripts/orchestrator/chain-finish.sh | cut -d: -f1) && sed -i '' "${n}d" scripts/orchestrator/chain-finish.sh && echo mutant: line $n deleted && git diff --stat
mutant: line 97 deleted
 scripts/orchestrator/chain-finish.sh | 1 -
 1 file changed, 1 deletion(-)
[exit 0]
```
```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head 2>&1 | grep -E '^(FAIL|AssertionError|Ran|FAILED|OK)'
FAIL: test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head)
AssertionError: 10 != 0 : resolve-threads rc=0
Ran 1 test in 4.089s
FAILED (failures=1)
[exit 1]
```
```console
$ git checkout -- scripts/orchestrator/chain-finish.sh && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to 4d4e3b22
[exit 0]
```
```console
$ wc -l scripts/orchestrator/chain-finish.sh
     166 scripts/orchestrator/chain-finish.sh
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/autoskill.md
6	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/learning.md
74	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/report.md
27	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/sandbox.md
121	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/task.md
240	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/validation.md
166	0	scripts/orchestrator/chain-finish.sh
242	1	tests/unit/test_chain_glue.py
[exit 0]
```

The CompactionDB entry, in the worktree's own database (the orchestrator consolidates at acceptance). The add ran as below; its exit status was not captured, since the seat's zsh has no `PIPESTATUS`, so the search that follows shows the entry.
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] chain-finish.sh binds the sweep JSON to the audited head (its head_sha must equal the review worktree's HEAD, exit 10) before resolve-threads.sh posts the sweep's dispositions to GitHub; a local evidence file that drives a GitHub write is checked against the head it was collected for before the write (T128 chain-glue finish a01 revise round 3, local:f20826e:1, fixed:4d4e3b22)" 2>&1 | tail -5
f7c752e6-7d04-48df-9cba-5eb6e9c13310
[exit not captured]
```
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory search head_sha
f7c752e6-7d04-48df-9cba-5eb6e9c13310 [project/decision] [memory:decision] chain-finish.sh binds the sweep JSON to the audited head (its head_sha must equal the review worktree's HEAD, exit 10) before resolve-threads.sh posts the sweep's dispositions to GitHub; a local evidence file that drives a GitHub write is checked against the head it was collected for before the write (T128 chain-glue finish a01 revise round 3, local:f20826e:1, fixed:4d4e3b22)
[exit 0]
```

## 7. Revise round 4 (ACCEPTANCE round 5, the Bot's P1 4301998951), captured at 6fba7690

The `gh` field check first, run outside the sandbox through the permission gate (`gh` fails TLS inside it): the round's `--json merged,mergeCommit` is refused by gh 2.102.0, and `state,mergeCommit` gives a merged and an open PR's answers. Then, as §6: the task copy and the checker; the branch and its base; the new test against `9a918f84`'s script (red), restored; the Check on `6fba7690`; the linters; two mutants (the not-landed refusal deleted, the break on a merged sha deleted), each restored; the caps.

```console
$ gh pr view 377 --repo mryfmo/dotfiles --json merged,mergeCommit 2>&1 | head -4   # [exit] is gh's status
Unknown JSON field: "merged"
Available fields:
  additions
  assignees
[exit 1]
```
```console
$ gh pr view 377 --repo mryfmo/dotfiles --json state,mergeCommit 2>&1 | head -4   # [exit] is gh's status
{"mergeCommit":{"oid":"7722704731b6cd6155fbca51c61ff5a710eaacbd"},"state":"MERGED"}
[exit 0]
```
```console
$ gh pr view 378 --repo mryfmo/dotfiles --json state,mergeCommit 2>&1 | head -4   # [exit] is gh's status
{"mergeCommit":null,"state":"OPEN"}
[exit 0]
```
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
```console
$ git log --oneline -3; git merge-base origin/main HEAD; git rev-parse origin/main
6fba7690 fix(orchestrator): chain-finish.sh waits for the merge to land and takes GitHub's merge commit (PR #378 thread 4301998951)
9a918f84 docs(orchestration): chain-glue finish a01 sandbox record names the push that landed (the documented HTTPS form, inside the sandbox)
d0d56c35 docs(orchestration): chain-glue finish a01 revise round 3 evidence (4d4e3b22)
af4f1e997f78119d5994d7d7b1966894d62bbc6a
a0e8b8ad54e90f685710f114b38d48105c3dc7e1
[exit 0]
```
```console
$ git show 9a918f84:scripts/orchestrator/chain-finish.sh > scripts/orchestrator/chain-finish.sh && git diff --stat
 scripts/orchestrator/chain-finish.sh | 22 +++++-----------------
 1 file changed, 5 insertions(+), 17 deletions(-)
[exit 0]
```
```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main 2>&1 | grep -E '^(FAIL|AssertionError|Ran|FAILED|OK)'
FAIL: test_finish_waits_for_the_merge_to_land_before_reading_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main)
AssertionError: 'reason=merged-as-cccccccccccccccccccccccccccccccccccccccc-pr-7-head-375979a ' not found in 'AGMSG-ACCEPTANCE v1 task_id=dotfiles-T128-x-a01 status=accepted reason=merged-as-f54572a8163dfdd1f48efba11790c34adefe519f-pr-7-head-375979a next_action=<the orchestrator fills this before sending>'
Ran 1 test in 4.690s
FAILED (failures=1)
[exit 1]
```
```console
$ git checkout -- scripts/orchestrator/chain-finish.sh && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to 6fba7690
[exit 0]
```
```console
$ uv run python -m unittest tests/unit/test_chain_glue.py -v
test_finish_checks_each_audit_finding_line_in_full (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_checks_each_audit_finding_line_in_full) ... ok
test_finish_counts_the_trimmed_reason (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_counts_the_trimmed_reason) ... ok
test_finish_prints_the_acceptance_line_and_sends_nothing (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_prints_the_acceptance_line_and_sends_nothing) ... ok
test_finish_reads_the_last_nonblank_line_as_the_verdict (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_reads_the_last_nonblank_line_as_the_verdict) ... ok
test_finish_refuses_a_head_that_differs_from_the_audit (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_head_that_differs_from_the_audit) ... ok
test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_refuses_a_sweep_whose_head_differs_from_the_audited_head) ... ok
test_finish_requires_an_audit_finding_line_per_incorrect_finding (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_requires_an_audit_finding_line_per_incorrect_finding) ... ok
test_finish_runs_gate_before_merge_and_cost_after (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_gate_before_merge_and_cost_after) ... ok
test_finish_runs_pr_cost_with_a_path_of_resolved_links (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_pr_cost_with_a_path_of_resolved_links) ... ok
test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_runs_the_pre_merge_pr_cost_after_the_fast_forward) ... ok
test_finish_waits_for_the_merge_to_land_before_reading_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main) ... ok
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
Ran 23 tests in 108.223s

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
$ n=$(grep -n -F 'merge enqueued, not landed' scripts/orchestrator/chain-finish.sh | cut -d: -f1) && sed -i '' "${n}d" scripts/orchestrator/chain-finish.sh && echo mutant: line $n deleted, the not-landed refusal && git diff --stat
mutant: line 170 deleted, the not-landed refusal
 scripts/orchestrator/chain-finish.sh | 1 -
 1 file changed, 1 deletion(-)
[exit 0]
```
```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main 2>&1 | grep -E '^(FAIL|AssertionError|Ran|FAILED|OK)'
FAIL: test_finish_waits_for_the_merge_to_land_before_reading_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main)
AssertionError: 10 != 0 : resolve-threads rc=0
Ran 1 test in 5.544s
FAILED (failures=1)
[exit 1]
```
```console
$ git checkout -- scripts/orchestrator/chain-finish.sh && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to 6fba7690
[exit 0]
```
```console
$ n=$(grep -n -F '|| break' scripts/orchestrator/chain-finish.sh | cut -d: -f1) && sed -i '' "${n}d" scripts/orchestrator/chain-finish.sh && echo mutant: line $n deleted, the break on a merged sha && git diff --stat
mutant: line 167 deleted, the break on a merged sha
 scripts/orchestrator/chain-finish.sh | 1 -
 1 file changed, 1 deletion(-)
[exit 0]
```
```console
$ set -o pipefail; uv run python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main 2>&1 | grep -E '^(FAIL|AssertionError|Ran|FAILED|OK)'
FAIL: test_finish_waits_for_the_merge_to_land_before_reading_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_finish_waits_for_the_merge_to_land_before_reading_main)
AssertionError: 3 != 40
Ran 1 test in 6.058s
FAILED (failures=1)
[exit 1]
```
```console
$ git checkout -- scripts/orchestrator/chain-finish.sh && git diff --quiet && echo restored to $(git rev-parse --short HEAD)
restored to 6fba7690
[exit 0]
```
```console
$ wc -l scripts/orchestrator/chain-finish.sh
     178 scripts/orchestrator/chain-finish.sh
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/autoskill.md
7	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/learning.md
83	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/report.md
17	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/revise.yaml
43	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/sandbox.md
121	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/task.md
381	0	.orchestration/dotfiles-T128-chain-glue-finish-a01/validation.md
178	0	scripts/orchestrator/chain-finish.sh
273	2	tests/unit/test_chain_glue.py
[exit 0]
```

The CompactionDB entry, in the worktree's own database; the add printed `3642bebd-53bd-4623-a099-89c5be68889f`, shown by this search.
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory search mergeCommit
3642bebd-53bd-4623-a099-89c5be68889f [project/decision] [memory:decision] chain-finish.sh waits for the merge to land after gh pr merge (a merge queue can enqueue only): it polls gh pr view <pr> --json state,mergeCommit until MERGED (CHAIN_MERGE_WAIT polls, default 40, CHAIN_POLL_SECONDS apart, default 15) and takes mergeCommit.oid as the merged sha; not landed is exit 10 with no fast-forward and no cost line. gh pr view has no merged JSON field (gh 2.102.0). (T128 chain-glue finish a01, PR #378 thread 4301998951, fixed:6fba7690)
[exit 0]
```
