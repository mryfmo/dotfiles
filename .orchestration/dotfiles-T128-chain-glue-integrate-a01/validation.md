---
task_id: dotfiles-T128-chain-glue-integrate-a01
seat: claude-standard-dot-a002
code_commit: 24f8af19
---

# Validation: dotfiles-T128-chain-glue-integrate-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (the capture script's `PIPESTATUS`; §4's block shows the mutant script and its output, and each mutant line carries its own `rc`). Captured at `24f8af19`.

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
24f8af19 feat(orchestrator): chain-integrate.sh runs a PR head's integration chain up to the audit from the main checkout's scripts, logging every step (plan 022 T7, T128 chain-glue integrate a01)
fdef3cebd2c8f42d4ddcc15052c875bd01c6e31c
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
test_integrate_refuses_an_absent_owner_task_before_the_advisory_step (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_an_absent_owner_task_before_the_advisory_step) ... ok
test_integrate_refuses_when_main_is_not_on_main (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_refuses_when_main_is_not_on_main) ... ok
test_integrate_resolves_binaries_before_the_checkout (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_resolves_binaries_before_the_checkout) ... ok
test_integrate_restarts_after_update_branch (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_restarts_after_update_branch) ... ok
test_integrate_runs_the_steps_in_order_and_logs_each (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_runs_the_steps_in_order_and_logs_each) ... ok
test_integrate_stops_on_a_sandbox_scan_hit (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_stops_on_a_sandbox_scan_hit) ... ok

----------------------------------------------------------------------
Ran 6 tests in 9.162s

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
     180 scripts/orchestrator/chain-integrate.sh
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
UV_OFFLINE=1 uv run python -m unittest "$T" > "$TMPDIR/cgi/m.log" 2>&1; echo "baseline rc=$? $(tail -1 "$TMPDIR/cgi/m.log")"
git status --short -- scripts/
--- output
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..900873ec 100755
-[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || refuse 10 "main checkout is not on main"
+[ "$("${git}" -C "${main}" symbolic-ref -q --short HEAD || true)" = main ] || true
mutant=main-check-off test=test_integrate_refuses_when_main_is_not_on_main rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..f804dcbd 100755
-[ "${out}" = false ] || refuse 10 "draft PR: the worker marks it ready"
+true || refuse 10 "draft PR: the worker marks it ready"
mutant=draft-check-off test=test_integrate_refuses_when_main_is_not_on_main rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..248b780d 100755
-    [ ! -e "${v}/${task}-audit-${sha7}.md.last.md" ] || refuse 10 "head already audited: one chain per head"
+    true || refuse 10 "head already audited: one chain per head"
mutant=audited-check-off test=test_integrate_refuses_when_main_is_not_on_main rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..6aeb3977 100755
-step checks any "${gh}" pr checks "${pr}" --required --watch
mutant=checks-step-gone test=test_integrate_runs_the_steps_in_order_and_logs_each rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..2684aaea 100755
-step record 0,1 /usr/bin/grep -o -E $'^([0-9]{10,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
+step record 0,1 /usr/bin/grep -o -E $'^([0-9]{6,}|audit:[0-9a-f]{7}:[0-9]+)\t[a-z0-9-]+' "${record}"
mutant=ledger-six-digits test=test_integrate_runs_the_steps_in_order_and_logs_each rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..f1630ca4 100755
-printf '[%s]\n' "${out//$'\n'/,}" > "${comments}"
+printf "%s\n" "${out}" > "${comments}"
mutant=comments-not-joined test=test_integrate_runs_the_steps_in_order_and_logs_each rc=1 FAILED (errors=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..dc8a9cda 100755
-    ((rc == 1)) || break
+    break
mutant=no-restart test=test_integrate_restarts_after_update_branch rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..b5e260c2 100755
-    log='' # the next head's log takes every line; this one ends here
mutant=old-log-kept test=test_integrate_restarts_after_update_branch rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..d6097c15 100755
-step local-review 0,3 "${main}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
+step local-review 0,3 "${review}/scripts/orchestrator/local-review.sh" "${task}" "${head}" "${pr}"
mutant=review-copy-runs test=test_integrate_resolves_binaries_before_the_checkout rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..458b2159 100755
-    [ -f "${main}/.orchestration/tasks/${owner}.md" ] || refuse 15 "write the owner task ${owner} first"
mutant=owner-check-off test=test_integrate_refuses_an_absent_owner_task_before_the_advisory_step rc=1 FAILED (failures=1)
diff --git a/scripts/orchestrator/chain-integrate.sh b/scripts/orchestrator/chain-integrate.sh
index 6c5998d7..310c3a51 100755
-    [ "${CHAIN_SCAN_JUDGED:-}" = "${sha7}" ] || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
+    true || refuse 16 "sandbox scan hit: judge it, then re-run with CHAIN_SCAN_JUDGED=${sha7}"
mutant=scan-stop-off test=test_integrate_stops_on_a_sandbox_scan_hit rc=1 FAILED (failures=1)
baseline rc=0 OK
[exit 0]
```
## 5. Caps
```console
$ git diff --numstat origin/main...HEAD
180	0	scripts/orchestrator/chain-integrate.sh
317	0	tests/unit/test_chain_glue.py
[exit 0]
```
