---
task_id: dotfiles-T128-chain-glue-integrate-a01
seat: claude-standard-dot-a002
code_commit: d8bc67d4
---

# Validation: dotfiles-T128-chain-glue-integrate-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (the capture script's `PIPESTATUS`; §4's block shows the mutant script and its output, and each mutant line carries its own `rc`). Captured at `d8bc67d4` (the code `24f8af19`, the Bot P1 fix `d8bc67d4`).

## 1. Task file and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
62706b88c365e1c21ef7c8b58e10647629f528b3a18b04048eb41a646a016b64  $MAIN/.orchestration/tasks/dotfiles-T128-chain-glue-integrate-a01.md
62706b88c365e1c21ef7c8b58e10647629f528b3a18b04048eb41a646a016b64  .orchestration/dotfiles-T128-chain-glue-integrate-a01/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-glue-integrate-a01.md: OK
[exit 0]
```
## 2. Branch and the five premises
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
d8bc67d4 fix(orchestrator): chain-integrate.sh runs only HEAD's copies of the main checkout's scripts (PR #372 thread 4291474880)
9f1cee1c docs(orchestration): chain-glue integrate a01 task copy and evidence (24f8af19)
24f8af19 feat(orchestrator): chain-integrate.sh runs a PR head's integration chain up to the audit from the main checkout's scripts, logging every step (plan 022 T7, T128 chain-glue integrate a01)
e2958f69ae560e665bd36ac1c2d823b5dfc934b7
[exit 0]
```
```console
$ git cat-file -e origin/main:scripts/orchestrator/chain-integrate.sh && echo present || echo absent
fatal: path 'scripts/orchestrator/chain-integrate.sh' exists on disk, but not in 'origin/main'
absent
[exit 0]
```
```console
$ git cat-file -e origin/main:tests/unit/test_chain_glue.py && echo present || echo absent
fatal: path 'tests/unit/test_chain_glue.py' exists on disk, but not in 'origin/main'
absent
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/acceptance-front-matter.py | /usr/bin/grep -c -e "--ledger" -e "--audit-dispositions"
6
[exit 0]
```
```console
$ for f in orch-audit.sh orch-gate.sh; do git show origin/main:scripts/orchestrator/$f | /usr/bin/grep -c "@arg [$]2 path The PR.s checkout"; done
1
1
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/local-review.sh | /usr/bin/grep -c -e "^# @arg" -e "ORCH_REVIEW_WORKTREE"
5
[exit 0]
```
## 3. The Check
```console
$ uv run python -m unittest tests/unit/test_chain_glue.py -v
test_integrate_refuses_a_main_checkout_script_that_is_not_heads (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_a_main_checkout_script_that_is_not_heads) ... ok
test_integrate_refuses_an_absent_owner_task_before_the_advisory_step (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_absent_owner_task_before_the_advisory_step) ... ok
test_integrate_refuses_when_main_is_not_on_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_when_main_is_not_on_main) ... ok
test_integrate_resolves_binaries_before_the_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_resolves_binaries_before_the_checkout) ... ok
test_integrate_restarts_after_update_branch (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_after_update_branch) ... ok
test_integrate_runs_the_steps_in_order_and_logs_each (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_the_steps_in_order_and_logs_each) ... ok
test_integrate_stops_on_a_sandbox_scan_hit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_stops_on_a_sandbox_scan_hit) ... ok

----------------------------------------------------------------------
Ran 7 tests in 11.359s

OK
[exit 0]
```
```console
$ shellcheck scripts/orchestrator/chain-integrate.sh && echo clean
clean
[exit 0]
```
```console
$ shfmt -i 4 -sr -d scripts/orchestrator/chain-integrate.sh && echo clean
clean
[exit 0]
```
```console
$ ruff check tests/unit/test_chain_glue.py && ruff format --check tests/unit/test_chain_glue.py
All checks passed!
1 file already formatted
[exit 0]
```
```console
$ wc -l scripts/orchestrator/chain-integrate.sh
     174 scripts/orchestrator/chain-integrate.sh
[exit 0]
```
## 4. Mutation check (each mutant applied alone with sed, its test run, the file restored with git checkout; then a baseline run)
```console
$ bash "$TMPDIR/cgi/mutate.sh" (the script, then its output)
S=scripts/orchestrator/chain-integrate.sh T=tests/unit/test_chain_glue.py
run() { # label sed-expression test
    sed -i '' "$2" "$S"
    git diff -U0 -- "$S" | /usr/bin/grep -v -E '^(---|\+\+\+|@@)' || echo "(sed changed nothing)"
    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$3" > "$TMPDIR/cgi/m.log" 2>&1
    echo "mutant=$1 test=$3 rc=$? $(tail -1 "$TMPDIR/cgi/m.log")"
    git checkout -- "$S"
}
run main-check-off 's|\] \|\| refuse 10 "main checkout is not on main"|] \|\| true|' test_integrate_refuses_when_main_is_not_on_main
run draft-check-off 's|\[ "${out}" = false \] \|\| refuse 10|true \|\| refuse 10|' test_integrate_refuses_when_main_is_not_on_main
run audited-check-off 's|\[ ! -e "${v}/${task}-audit-${sha7}.md.last.md" \] \|\||true \|\||' test_integrate_refuses_when_main_is_not_on_main
run checks-step-gone '/step checks any/d' test_integrate_runs_the_steps_in_order_and_logs_each
run ledger-six-digits 's|\[0-9\]{10,}|[0-9]{6,}|' test_integrate_runs_the_steps_in_order_and_logs_each
run comments-not-joined 's|printf .\[%s\]\\n. "${out//$.\\n./,}"|printf "%s\\n" "${out}"|' test_integrate_runs_the_steps_in_order_and_logs_each
run no-restart 's|((rc == 1)) \|\| break|break|' test_integrate_restarts_after_update_branch
run old-log-kept "/log='' # the next head/d" test_integrate_restarts_after_update_branch
run review-copy-runs 's|"${main}/scripts/orchestrator/local-review.sh"|"${review}/scripts/orchestrator/local-review.sh"|' test_integrate_resolves_binaries_before_the_checkout
run owner-check-off '/refuse 15/d' test_integrate_refuses_an_absent_owner_task_before_the_advisory_step
run scan-stop-off 's|\[ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" \] \|\||true \|\||' test_integrate_stops_on_a_sandbox_scan_hit
run script-diff-off '/diff --quiet HEAD -- scripts/d' test_integrate_refuses_a_main_checkout_script_that_is_not_heads
run script-tracked-off 's|ls-files --error-unmatch -- "${s}" > /dev/null 2>&1 \|\| refuse 10|ls-files -- "${s}" \|\| refuse 10|' test_integrate_refuses_a_main_checkout_script_that_is_not_heads
UV_OFFLINE=1 uv run python -m unittest "$T" > "$TMPDIR/cgi/m.log" 2>&1; echo "baseline rc=$? $(tail -1 "$TMPDIR/cgi/m.log")"
git status --short -- scripts/
--- output
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..c0df6e94 100755
-[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
+[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || true
mutant=main-check-off test=test_integrate_refuses_when_main_is_not_on_main rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..ceded8e8 100755
-[ "${out}" = false ] || refuse 10 "draft PR: the worker marks it ready"
+true || refuse 10 "draft PR: the worker marks it ready"
mutant=draft-check-off test=test_integrate_refuses_when_main_is_not_on_main rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..fb4ef581 100755
-    [ ! -e "${v}/${task}-audit-${sha7}.md.last.md" ] || refuse 10 "head already audited: one chain per head"
+    true || refuse 10 "head already audited: one chain per head"
mutant=audited-check-off test=test_integrate_refuses_when_main_is_not_on_main rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..0630a611 100755
-step checks any "${gh}" pr checks "${pr}" --required --watch
mutant=checks-step-gone test=test_integrate_runs_the_steps_in_order_and_logs_each rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..fcdc22ba 100755
-step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
+step record 0,1 /usr/bin/grep -o -E $'^([0-9]{6,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
mutant=ledger-six-digits test=test_integrate_runs_the_steps_in_order_and_logs_each rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..65ffff23 100755
-printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
+printf "%s\n" "${out}" > "${comments}"
mutant=comments-not-joined test=test_integrate_runs_the_steps_in_order_and_logs_each rc=1 FAILED (errors=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..5ca3597c 100755
-    ((rc == 1)) || break
+    break
mutant=no-restart test=test_integrate_restarts_after_update_branch rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..d53a54fc 100755
-    log='' # the next head's log takes every line; this one ends here
mutant=old-log-kept test=test_integrate_restarts_after_update_branch rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..79d77989 100755
-step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
+step local-review 0,3 "${review}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
mutant=review-copy-runs test=test_integrate_resolves_binaries_before_the_checkout rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..d465d3ce 100755
-    [ -f "${main}/.orchestration/tasks/${owner}.md" ] || refuse 15 "write the owner task ${owner} first"
mutant=owner-check-off test=test_integrate_refuses_an_absent_owner_task_before_the_advisory_step rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..ce310d92 100755
-    [ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" ] || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
+    true || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
mutant=scan-stop-off test=test_integrate_stops_on_a_sandbox_scan_hit rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..7820086d 100755
-"${git}" -C "${main}" diff --quiet HEAD -- scripts || refuse 10 "scripts/ in the main checkout differs from HEAD"
mutant=script-diff-off test=test_integrate_refuses_a_main_checkout_script_that_is_not_heads rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 662b7e2a..2035c272 100755
-    "${git}" -C "${main}" ls-files --error-unmatch -- "${s}" > /dev/null 2>&1 || refuse 10 "${s} is not tracked in the main checkout"
+    "${git}" -C "${main}" ls-files -- "${s}" || refuse 10 "${s} is not tracked in the main checkout"
mutant=script-tracked-off test=test_integrate_refuses_a_main_checkout_script_that_is_not_heads rc=1 FAILED (failures=1)
baseline rc=0 OK
[exit 0]
```
## 5. Caps
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-glue-integrate-a01/autoskill.md
6	0	.orchestration/dotfiles-T128-chain-glue-integrate-a01/learning.md
61	0	.orchestration/dotfiles-T128-chain-glue-integrate-a01/report.md
27	0	.orchestration/dotfiles-T128-chain-glue-integrate-a01/sandbox.md
142	0	.orchestration/dotfiles-T128-chain-glue-integrate-a01/task.md
182	0	.orchestration/dotfiles-T128-chain-glue-integrate-a01/validation.md
174	0	scripts/orchestrator/chain-integrate.sh
330	0	tests/unit/test_chain_glue.py
[exit 0]
```
