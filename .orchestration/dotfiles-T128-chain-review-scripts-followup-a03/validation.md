---
task_id: dotfiles-T128-chain-review-scripts-followup-a03
seat: claude-standard-dot-a002
code_commit: 9da0897a
---

# Validation: dotfiles-T128-chain-review-scripts-followup-a03

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. `UV_OFFLINE=1` was set for every uv call. The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's). Premise 1's `grep -c` prints `0` and exits 1 when it finds nothing, which is the premise's expected output. §4's block shows the mutant script and its output, and each mutant line carries its own `rc`. Captured at `9da0897a` (the code `a311781d`, the test round `a1ddb211`, the CI ShellCheck fix `9da0897a`).

## 1. Task file and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2  $MAIN/.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a03.md
e328a3fb8036d4b29b1ed798f42a967d66204bde810b62b84dd7048715c79ee2  .orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-review-scripts-followup-a03.md: OK
[exit 0]
```
## 2. Branch and the four premises
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
9da0897a fix(orchestrator): local-advisory.sh numbers each earlier finding with an if, not A && B || C (CI ShellCheck SC2015)
d2b33025 docs(orchestration): chain-review-scripts followup a03 task copy and evidence (a311781d, a1ddb211)
a1ddb211 test(orchestrator): the repeat test tells a line range from a wider one; the token reads a backticked path as itself (T128 chain-review-scripts followup a03)
a311781d fix(orchestrator): local-advisory.sh refuses an absent owner task, hashes the owner file as evidence, and classes a repeated finding by the earlier row (T128 chain-review-scripts followup a03)
f7847616970d6bd83739a75a65ad8f7c35e91462
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "write the owner task"
0
[exit 1]
```
```console
$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "git show origin/main"
1
[exit 0]
```
```console
$ git show origin/main:scripts/orchestrator/local-advisory.sh | /usr/bin/grep -c "advisory-p2"
2
[exit 0]
```
```console
$ git show origin/main:tests/unit/test_chain_review_scripts.py | /usr/bin/grep -c "def test_"
14
[exit 0]
```
## 2a. The diff outside tests and the evidence
```console
$ git diff origin/main...HEAD -- scripts/
diff --git a/scripts/orchestrator/local-advisory.sh b/scripts/orchestrator/local-advisory.sh
index 409035cc..5e67ace7 100755
--- a/scripts/orchestrator/local-advisory.sh
+++ b/scripts/orchestrator/local-advisory.sh
@@ -4,14 +4,19 @@
 # @description
 #   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
 #   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
-#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   other appends the row `local:<sha7>:<n><TAB><class>` under the heading `## Owned by <owner>` of
 #   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
-#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=shasum -a 256 .orchestration/tasks/<owner>.md
+#   (<sha256>)` line, each only when the record lacks it. A review with findings needs the owner task file. The
+#   class is `advisory-p2`, unless the finding's `path:line[-line]` token (backticks ignored) matches a finding of
+#   the task's earlier local review files whose `local:` row in the record has another class: then the last such
+#   row's class, and the line's parenthesis names it as `repeat of local:<sha7>:<n>` (C-50).
 # @arg $1 string Task id, letters, digits, `.`, `_` and `-`.
 # @arg $2 string The reviewed head, 40 hex characters.
 # @arg $3 string The task id that owns the advisory findings, in the task id's form.
 # @exitcode 0 No P0/P1 finding.
-# @exitcode 2 No local review file, or a malformed task id, head or owner task id.
+# @exitcode 2 No local review file, a malformed task id, head or owner task id, or (for a review with findings) no
+#   owner task file: `write the owner task <owner> first`.
 # @exitcode 3 A P0/P1 finding.
 # @example
 #   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
@@ -37,6 +42,26 @@ n=$(sed -n 's/^findings: //p' "$LR" | head -1)
     echo "local review of $h7: no findings"
     exit 0
 }
+# The rows name the owner task, so it must exist; its hash is evidence that replays before the boundary (C-51).
+O=".orchestration/tasks/$owner.md"
+[ -f "$O" ] || {
+    echo "write the owner task $owner first"
+    exit 2
+}
+sha=$(shasum -a 256 "$O" | cut -d' ' -f1)
+# C-50: a finding repeated from an earlier head takes the class the record gave it. Each earlier review's findings,
+# numbered as the loop below numbers them, as `<path:line[-line]> local:<sha7>:<n>` lines.
+# The class excludes the backtick, so `a.sh:1` in backticks reads as a.sh:1.
+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
+earlier=""
+for f in .orchestration/validation/"$task"-local-review-*.md; do
+    [[ -f $f && $f != "$LR" ]] || continue
+    e=${f%.md} && e=${e##*-local-review-} && k=0
+    while IFS= read -r l; do
+        k=$((k + 1))
+        if t=$(token "$l"); then earlier+="$t local:$e:$k"$'\n'; fi
+    done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$f" | sort -u)
+done
 # A literal heading match, ended by a space or the line's end: a . in the owner is no wildcard, a longer id no match.
 awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
 i=0 stop=0
@@ -48,8 +73,16 @@ while IFS= read -r line; do
         stop=1
         ;;
     *)
-        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\tadvisory-p2\n' "$h7" "$i" >> "$A"
-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s); evidence=git show origin/main:.orchestration/tasks/%s.md | grep -n '"'"'item 1'"'"'\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$owner" >> "$A"
+        # The last row in the record of an earlier finding with this token, other than advisory-p2, wins.
+        class=advisory-p2 repeat=""
+        t=$(token "$line") || t=""
+        ids=$(printf '%s' "$earlier" | awk -v t="$t" '$1 == t { print $2 }' | tr '\n' '|')
+        if [[ -n $t && -n $ids ]]; then
+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
+            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
+        fi
+        /usr/bin/grep -q "^local:$h7:$i	" "$A" || printf 'local:%s:%s\t%s\n' "$h7" "$i" "$class" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
         ;;
     esac
 done < <(/usr/bin/grep -E '^- \[P[0-3]\]' "$LR" | sort -u)
[exit 0]
```
## 3. The Check
```console
$ uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
test_local_advisory_classes_a_repeat_by_the_earlier_row (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_classes_a_repeat_by_the_earlier_row) ... ok
test_local_advisory_matches_the_owner_heading_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_matches_the_owner_heading_literally) ... ok
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_records_p2_rows_and_stops_on_p0_p1) ... ok
test_local_advisory_refuses_a_malformed_owner_id (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_a_malformed_owner_id) ... ok
test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file) ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory) ... ok
test_local_review_keeps_env_S_shebang_arguments (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_keeps_env_S_shebang_arguments) ... ok
test_local_review_pins_the_review_binary_interpreter (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_pins_the_review_binary_interpreter) ... ok
test_local_review_refuses_a_quoted_env_S_shebang (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_refuses_a_quoted_env_S_shebang) ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_codex_through_mise_and_refuses_a_shim) ... ok
test_local_review_resolves_the_review_binary_before_the_checkout (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_resolves_the_review_binary_before_the_checkout) ... ok
test_local_review_reuses_only_a_file_that_records_this_head (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_reuses_only_a_file_that_records_this_head) ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file) ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_strips_a_worktree_path_holding_sed_syntax_literally) ... ok
test_local_review_writes_no_file_when_the_review_binary_fails (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_writes_no_file_when_the_review_binary_fails) ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_sandbox_scan_prints_the_unsandboxed_mutation_calls) ... ok

----------------------------------------------------------------------
Ran 16 tests in 7.404s

OK
[exit 0]
```
```console
$ shellcheck scripts/orchestrator/local-advisory.sh && echo clean
clean
[exit 0]
```
```console
$ shfmt -i 4 -sr -d scripts/orchestrator/local-advisory.sh && echo clean
clean
[exit 0]
```
```console
$ ruff check --config ruff.toml tests/unit/test_chain_review_scripts.py && ruff format --config ruff.toml --check tests/unit/test_chain_review_scripts.py
All checks passed!
1 file already formatted
[exit 0]
```
## 4. Mutation check (each mutant a literal string replacement applied alone, its test run, the file restored with git checkout; then a baseline run)
```console
$ bash "$TMPDIR/crs3/mutate.sh" (the script, then its output)
S=scripts/orchestrator/local-advisory.sh T=tests/unit/test_chain_review_scripts.py
lrun() { # label old new test: a literal string replacement (python's str.replace, once), the test, the restore
    python3 -I -c 'import sys; p, a, b = sys.argv[1:]; t = open(p).read(); assert t.count(a) == 1, a; open(p, "w").write(t.replace(a, b))' "$S" "$2" "$3"
    git diff -U0 -- "$S" | /usr/bin/grep -v -E '^(---|\+\+\+|@@|diff|index)' || echo "(nothing changed)"
    UV_OFFLINE=1 uv run python -m unittest "$T" -k "$4" > "$TMPDIR/crs3/m.log" 2>&1
    echo "mutant=$1 test=$4 rc=$? $(tail -1 "$TMPDIR/crs3/m.log")"
    git checkout -- "$S"
}
A=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file R=test_local_advisory_classes_a_repeat_by_the_earlier_row H=test_local_advisory_matches_the_owner_heading_literally
lrun owner-check-off '[ -f "$O" ] ||' 'true ||' $A
lrun old-evidence 'evidence=shasum -a 256 %s (%s)\n'"'"' "$h7" "$i" "$owner" "$(printf '"'"'%s'"'"' "$line" | cut -c1-120 | tr -d '"'"'`'"'"')" "$repeat" "$O" "$sha"' 'evidence=git show origin/main:%s | grep -n item\n'"'"' "$h7" "$i" "$owner" "$(printf '"'"'%s'"'"' "$line" | cut -c1-120 | tr -d '"'"'`'"'"')" "$repeat" "$O"' $A
lrun repeat-off '[ -z "$row" ] || class=' 'true || class=' $R
lrun first-row-wins '| tail -1 || true)' '| head -1 || true)' $R
lrun range-token-off ':[0-9]+(-[0-9]+)?)' ':[0-9]+)' $R
lrun heading-as-regex 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/' '$0 ~ "^" h' $H
UV_OFFLINE=1 uv run python -m unittest "$T" > "$TMPDIR/crs3/m.log" 2>&1; echo "baseline rc=$? $(tail -1 "$TMPDIR/crs3/m.log")"
git status --short -- scripts/
--- output
-[ -f "$O" ] || {
+true || {
mutant=owner-check-off test=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file rc=1 FAILED (failures=1)
-        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=shasum -a 256 %s (%s)\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" "$sha" >> "$A"
+        /usr/bin/grep -q "^local-finding: $h7:$i " "$A" || printf 'local-finding: %s:%s not-applicable:advisory P2 owned by %s (%s%s); evidence=git show origin/main:%s | grep -n item\n' "$h7" "$i" "$owner" "$(printf '%s' "$line" | cut -c1-120 | tr -d '`')" "$repeat" "$O" >> "$A"
mutant=old-evidence test=test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file rc=1 FAILED (failures=1)
-            [ -z "$row" ] || class=${row#*	} repeat="; repeat of ${row%%	*}"
+            true || class=${row#*	} repeat="; repeat of ${row%%	*}"
mutant=repeat-off test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
-            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
+            row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | head -1 || true)
mutant=first-row-wins test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
-token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+(-[0-9]+)?) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
+token() { [[ $1 =~ ([A-Za-z0-9._/-]+:[0-9]+) ]] && printf '%s\n' "${BASH_REMATCH[1]}"; }
mutant=range-token-off test=test_local_advisory_classes_a_repeat_by_the_earlier_row rc=1 FAILED (failures=1)
-awk -v h="## Owned by $owner" 'substr($0, 1, length(h)) == h && substr($0, length(h) + 1, 1) ~ /^ ?$/ { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
+awk -v h="## Owned by $owner" '$0 ~ "^" h { f = 1 } END { exit !f }' "$A" 2> /dev/null || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
mutant=heading-as-regex test=test_local_advisory_matches_the_owner_heading_literally rc=1 FAILED (failures=1)
baseline rc=0 OK
[exit 0]
```
## 5. Caps
```console
$ git diff --numstat origin/main...HEAD
3	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/autoskill.md
6	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/learning.md
72	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/report.md
27	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/sandbox.md
106	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/task.md
219	0	.orchestration/dotfiles-T128-chain-review-scripts-followup-a03/validation.md
38	5	scripts/orchestrator/local-advisory.sh
60	2	tests/unit/test_chain_review_scripts.py
[exit 0]
```
