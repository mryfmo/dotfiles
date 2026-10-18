---
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a01
seat: claude-standard-dot-a011
code_commit: d3891c0b
---

# Validation: dotfiles-T129-audit-inherit-replan-json-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-d` on the branch `tools/audit-inherit-replan-json-followup-a01` at `d3891c0b` (the test commit `598ca1f9` and the fix `d3891c0b`, stacked on PR #390's head `741e242`, `BASE` below), inside the sandbox. `MAIN` names the main checkout, `T` the task id and `SCRATCH` the seat's scratchpad. The output is verbatim, with the main checkout's, the home directory's and the scratchpad's paths replaced by `$MAIN`, `$HOME` and `$SCRATCH`, and each block ends with the exit status of the command shown.

## 1. Task file (sha256 1f6b90f4…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
1f6b90f40470d02455fbd2424a01b1e9cb40a03c0b5f5f7f135d645295dbf3bb  $MAIN/.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a01.md
1f6b90f40470d02455fbd2424a01b1e9cb40a03c0b5f5f7f135d645295dbf3bb  .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-audit-inherit-replan-json-followup-a01.md: OK
[exit 0]
```
## 2. Premises
```console
$ /usr/bin/grep -c "\[P1\] Verify merge content before inheriting the parent audit" "$MAIN/.orchestration/validation/dotfiles-T129-audit-inherit-replan-json-a01-local-review-741e242.md"; git --version; git merge-tree --write-tree "$BASE^1" "$BASE^2"; git rev-parse "$BASE^{tree}"
3
git version 2.56.0
7a47cd7484696faf42121437239b0bc1bdba6ca0
7a47cd7484696faf42121437239b0bc1bdba6ca0
[exit 0]
```
## 3. The owned rows at dispatch (the lineage's acceptance record in the main checkout)
```console
$ awk '/^## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a01/{p=1} p&&/^- /{exit} p' "$MAIN/.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-a01.md"
## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a01 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:741e242:2	advisory-p2
local-finding: 741e242:2 not-applicable:advisory P2 owned by dotfiles-T129-audit-inherit-replan-json-followup-a01 (- [P2] Update the pre-audit ledger reader for inherited audit IDs — scripts/orchestrator/chain-integrate.sh:191-192); evidence=shasum -a 256 .orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a01.md (9ff8aa7877532495b6577271c25c3c000186a58fb1268954f9e67c3c9ffd1506)
[exit 0]
```
## 4. Branch
```console
$ git log --oneline "$BASE"..HEAD; git log --oneline -1 "$BASE"; git log --oneline -1 origin/main
d3891c0b fix(orchestrator): inherit an audit only when a clean merge reproduces the head's tree; the ledger check reads inherited ids from the marker (T129 audit-inherit-replan-json followup a01, R1 and R2)
598ca1f9 test(orchestrator): an inherited audit needs the merge-tree reproduction of the head's tree; the ledger check reads inherited ids from the marker (T129 audit-inherit-replan-json followup a01, R1 and R2, red)
741e2427 Merge branch 'main' into tools/audit-inherit-replan-json
99a4a80f feat(doctor): make doctor fails on a Mac that may sleep (T129 doctor-sleep-disabled a01) (#394)
[exit 0]
```
## 5. Red on the test commit 598ca1f9, green at the head: the re-plan's test command (scratch worktree removed afterwards)
```console
$ git worktree add --detach -q "$SCRATCH/vr-red" 598ca1f9 && uv run --directory "$SCRATCH/vr-red" python -m unittest tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reads_inherited_audit_ids_from_the_marker -v 2>&1 | /usr/bin/grep -E " \.\.\. (ok|FAIL|ERROR)$|AssertionError|^[-+] |^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//"; git worktree remove --force "$SCRATCH/vr-red"
test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree ... FAIL
test_ledger_check_reads_inherited_audit_ids_from_the_marker ... FAIL
AssertionError: Lists differ: ['dotfiles-T128-x-a01 /private/tmp/claude-[57 chars]w 7'] != []
+ []
- ['dotfiles-T128-x-a01 '
-  '$TMPDIR/tmp96g5m9kq/main/.claude/worktrees/orchestrator-review '
-  '7']
AssertionError: 1 != 0 : ledger rows 1; findings 1; gaps 0
Ran 2 tests in 7.018s
FAILED (failures=2)
[exit 0]
```
```console
$ uv run python -m unittest tests.unit.test_chain_glue tests.unit.test_task_checkers tests.unit.test_orchestrator_tools -v 2>&1 | /usr/bin/grep -E " \.\.\. (FAIL|ERROR)$|^Ran|^OK|^FAILED|inherit"
test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_the_merge_tree_reproduction_to_equal_the_head_tree) ... ok
test_integrate_inherits_the_audit_across_an_update_branch_only_head (tests.unit.test_chain_glue.ChainIntegrateTest.test_integrate_inherits_the_audit_across_an_update_branch_only_head) ... ok
test_ledger_check_reads_inherited_audit_ids_from_the_marker (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reads_inherited_audit_ids_from_the_marker) ... ok
test_dispatch_resolves_its_root_without_inherited_git_variables (tests.unit.test_orchestrator_tools.OrchestratorToolsTest.test_dispatch_resolves_its_root_without_inherited_git_variables) ... ok
Ran 80 tests in 123.636s
OK
[exit 0]
```
## 6. Lint
```console
$ shellcheck scripts/orchestrator/chain-integrate.sh && echo shellcheck-clean; shfmt -i 4 -sr -d scripts/orchestrator/chain-integrate.sh && echo shfmt-clean
shellcheck-clean
shfmt-clean
[exit 0]
```
```console
$ ruff format --config ruff.toml --check scripts/orchestrator/ledger-check.py tests/unit/test_chain_glue.py tests/unit/test_task_checkers.py; ruff check --config ruff.toml scripts/orchestrator/ledger-check.py tests/unit/test_chain_glue.py tests/unit/test_task_checkers.py
3 files already formatted
All checks passed!
[exit 0]
```
## 7. Caps (against 741e242: at most 60 changed lines outside tests/ and .orchestration/, 120 under tests/; origin/main pasted too)
```console
$ git diff --numstat "$BASE"...HEAD; git diff --numstat "$BASE"...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d\ntests/: %d\n", o, t }'
123	0	.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a01/task.md
6	1	scripts/orchestrator/chain-integrate.sh
7	3	scripts/orchestrator/ledger-check.py
46	0	tests/unit/test_chain_glue.py
12	0	tests/unit/test_task_checkers.py
outside tests/ and .orchestration/: 17
tests/: 58
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "origin/main...HEAD outside tests/ and .orchestration/: %d\ntests/: %d\n", o, t }'
origin/main...HEAD outside tests/ and .orchestration/: 113
tests/: 366
[exit 0]
```
## 8. Scope: the hunks of the two scripts
```console
$ git diff -U0 "$BASE"...HEAD -- scripts | /usr/bin/grep -E "^(\+\+\+|@@)"
+++ b/scripts/orchestrator/chain-integrate.sh
@@ -10 +10,2 @@
@@ -186,0 +188,4 @@ if [[ -n ${parent} && -f ${from}.md && -f ${from}.md.last.md ]] && "${git}" -C "
+++ b/scripts/orchestrator/ledger-check.py
@@ -5 +5,2 @@ a row is a record line `<id><TAB><class>`, the id a Codex Bot review comment or
@@ -29,2 +30,5 @@ def main(record, sweep, *audits):
[exit 0]
```
## 6a. The a01 Check command: inside the sandbox at the head and at 741e242, and with the global git config disabled
```console
$ uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py -v > "$SCRATCH/r1-check-head.txt" 2>&1; echo "head rc=$?"
head rc=1
$ git worktree add --detach -q "$SCRATCH/v-741" 741e24272fd64b6a36c0d6725c53265de1c94982 && uv run --directory "$SCRATCH/v-741" python -m unittest <the same four modules> -v > "$SCRATCH/r1-check-741.txt" 2>&1; echo "741e242 rc=$?"; git worktree remove --force "$SCRATCH/v-741"
741e242 rc=1
$ for f in r1-check-head r1-check-741; do echo "== $f"; grep -E "^Ran|^OK|^FAILED" "$SCRATCH/$f.txt"; grep -E "^(FAIL|ERROR): " "$SCRATCH/$f.txt" | grep -oE "test_[a-z_]+\.[A-Z][A-Za-z]+Test" | sort | uniq -c; done
== r1-check-head
Ran 201 tests in 213.806s
FAILED (failures=136)
 136 test_require_crit_review.ReviewGuardTest
== r1-check-741
Ran 200 tests in 177.659s
FAILED (failures=136)
 136 test_require_crit_review.ReviewGuardTest
$ diff <the sorted failing test names of the two runs> && echo "identical failing tests"
identical failing tests
$ grep -m1 -A6 "^FAIL: " "$SCRATCH/r1-check-head.txt" | tail -2
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_accepts_a_dispatch_list 2>&1 | tail -3; echo ---; uv run python -m unittest tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_accepts_a_dispatch_list 2>&1 | tail -2
Ran 1 test in 0.995s

OK
---

FAILED (failures=1)
$ GIT_CONFIG_GLOBAL=/dev/null uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py -v > "$SCRATCH/r1-check-head-noglobal.txt" 2>&1; echo "rc=$?"; grep -E "^Ran|^OK|^FAILED" "$SCRATCH/r1-check-head-noglobal.txt"
rc=0
Ran 201 tests in 214.329s
OK
```
The global config holds `commit.gpgsign=true` with `gpg.format=ssh`, and the sandbox denies `~/.ssh/id_ed25519*`, so fixture commits fail and `main` never exists in the fixture repositories (T133 validation §4a shows the signing error itself).
## 9. CompactionDB: one decision in this worktree's store before completion
```console
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T129 audit-inherit re-plan (supersedes PR 390's last round): chain-integrate.sh lets an update-branch-only head inherit its parent's audit only when the PR patch-id is unchanged AND git merge-tree --write-tree head^1 head^2 prints head^{tree} (patch-id ignores hunk positions, so a relocated edit kept it); ledger-check.py takes an inherited audit's ids from its first line inherited-from: <sha7>." 2>&1 | tail -1
707e4cfa-db8f-43aa-8a42-d32d32972aa6
```
