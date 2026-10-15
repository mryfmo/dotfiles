---
task_id: dotfiles-T128-chain-github-scripts-followup-a01
seat: claude-standard-dot-a002
code_commit: 1650bfb9
---

# Validation: dotfiles-T128-chain-github-scripts-followup-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox. `MAIN` names the main checkout, and `S` a scratch directory under `/tmp/claude-501` that holds the mutation runner. `UV_OFFLINE=1` was set, since uv cannot reach pypi from the sandbox. The output is verbatim, with the main checkout's path removed, and each block ends with the command's exit status. Captured at `1650bfb9`, before the PR was marked ready.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
c89f6dc8cb5eeefcb7b8538b83dde533077d3b8e63ad919225066ffdd068597b  .orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a01.md
c89f6dc8cb5eeefcb7b8538b83dde533077d3b8e63ad919225066ffdd068597b  .orchestration/dotfiles-T128-chain-github-scripts-followup-a01/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-github-scripts-followup-a01.md: OK
[exit 0]
```

## 2. Branch and the two premises

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
1650bfb9 fix(orchestrator): resolve-threads.sh checks the resolve answer, passes the thread id as a variable and backticks the disposition (T128 chain-github-scripts followup a01)
727180dbc33f50b8934c2f2ed229d1c6a744ce0d
[exit 0]
```
```console
$ git cat-file -e origin/main:.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md && echo present || echo absent
present
[exit 0]
```
```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md 2>/dev/null | /usr/bin/grep -q "^## Owned by dotfiles-T128-chain-github-scripts-followup-a01" && echo present || echo absent
present
[exit 0]
```

## 3. The owned rows (item 1), read from origin/main

```console
$ git show origin/main:.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md | awk '/^## Owned by dotfiles-T128-chain-github-scripts-followup-a01/ {p = 1; next} /^## / {p = 0} p && /^[^ ]+\t[a-z0-9-]+$/'
4270684630	resolve-response-unchecked
local:d15fa87:1	advisory-p2
audit:d15fa87:1	resolve-response-unchecked
audit:d15fa87:2	graphql-id-interpolation
audit:d15fa87:3	reply-template-unparseable
[exit 0]
```

## 4. The script change

```console
$ git diff origin/main...HEAD -- scripts/orchestrator/resolve-threads.sh
diff --git a/scripts/orchestrator/resolve-threads.sh b/scripts/orchestrator/resolve-threads.sh
index 0b3ee519..dbf2aff4 100755
--- a/scripts/orchestrator/resolve-threads.sh
+++ b/scripts/orchestrator/resolve-threads.sh
@@ -6,16 +6,18 @@
 #   reads the first 100 review threads of the PR. Each unresolved thread is keyed on its first comment's database
 #   id, and its disposition is the row of the table whose first column is that id, else, when a sweep JSON is given,
 #   the `disposition` of the sweep item whose `url` ends with `_r<id>`. A `fixed:` or `not-applicable:` disposition
-#   gets one reply in its fixed sentence and one resolveReviewThread mutation. A thread without a disposition, or
-#   with another form, is reported and left open. `--dry-run` prints what would be done and writes nothing. gh runs
-#   with the orchestrator's credentials, so this runs outside the sandbox.
+#   gets one reply in its fixed sentence, the disposition in backticks as fill_sweep.py reads a reply back, and one
+#   resolveReviewThread mutation, the thread id passed as a GraphQL variable; the thread counts as resolved only when
+#   the mutation answers `isResolved` true. A thread without a disposition, with another form, or not answered true
+#   is reported and left open. `--dry-run` prints what would be done and writes nothing. gh runs with the
+#   orchestrator's credentials, so this runs outside the sandbox.
 # @arg $1 int PR number.
 # @arg $2 path The disposition table: TSV rows of a comment id and its disposition.
 # @arg $3 string `--dry-run`, or any placeholder such as `-`.
 # @arg $4 path The sweep JSON (optional).
 # @exitcode 0 Every unresolved thread was resolved (under `--dry-run`, would be).
 # @exitcode 2 Usage error.
-# @exitcode 3 A thread has no disposition, or one of another form; it is left open.
+# @exitcode 3 A thread has no disposition, one of another form, or a resolve answer other than true; it is left open.
 # @example
 #   scripts/orchestrator/resolve-threads.sh 355 extra.tsv - .orchestration/validation/t-a01-pr-feedback.json
 set -euo pipefail
@@ -30,6 +32,9 @@ pr=$1 tsv=$2 dry=${3:-} sweep=${4:-}
 query="query { repository(owner:\"mryfmo\", name:\"dotfiles\") { pullRequest(number:${pr}) { reviewThreads(first:100) \
 { nodes { id isResolved comments(first:1) { nodes { databaseId } } } } } } }"
 threads=$(gh api graphql -f query="${query}" --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved|not) | "\(.comments.nodes[0].databaseId) \(.id)"')
+# The thread id travels as a GraphQL variable, never inside the query text.
+# shellcheck disable=SC2016 # $threadId is GraphQL's variable, not the shell's
+resolve='mutation ($threadId: ID!) { resolveReviewThread(input: {threadId: $threadId}) { thread { isResolved } } }'
 missing=0 resolved=0
 # The threads come in on fd 3, so a command in the loop that reads stdin cannot swallow the rest of them.
 while read -r cid tid <&3; do
@@ -46,10 +51,10 @@ while read -r cid tid <&3; do
     fi
     case ${row} in
     fixed:*)
-        body="Disposition (orchestrator): ${row}. Fixed at root cause in that commit on this branch; verified by \
+        body="Disposition (orchestrator): \`${row}\`. Fixed at root cause in that commit on this branch; verified by \
 the task's tests and CI on the final head. Resolving."
         ;;
-    not-applicable:*) body="Disposition (orchestrator): ${row}. Resolving; the owning task on main carries it." ;;
+    not-applicable:*) body="Disposition (orchestrator): \`${row}\`. Resolving; the owning task on main carries it." ;;
     *)
         echo "row for ${cid} has an unknown form: ${row}"
         missing=1
@@ -61,8 +66,12 @@ the task's tests and CI on the final head. Resolving."
         continue
     fi
     gh api -X POST "repos/mryfmo/dotfiles/pulls/${pr}/comments/${cid}/replies" -f body="${body}" --jq '.id' > /dev/null
-    gh api graphql -f query="mutation { resolveReviewThread(input: {threadId: \"${tid}\"}) { thread { isResolved } } }" \
-        --jq '.data.resolveReviewThread.thread.isResolved' > /dev/null
+    state=$(gh api graphql -f query="${resolve}" -f threadId="${tid}" --jq '.data.resolveReviewThread.thread.isResolved')
+    if [[ ${state} != true ]]; then
+        echo "thread ${cid} not resolved (isResolved: ${state:-none}); left open"
+        missing=1
+        continue
+    fi
     resolved=$((resolved + 1))
     echo "resolved ${cid} (${row:0:60})"
 done 3<<< "${threads}"
[exit 0]
```

## 5. The Check: the test module

```console
$ uv run python -m unittest tests/unit/test_chain_github_scripts.py -v
test_pr_cost_appends_one_ledger_line_from_the_api (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_pr_cost_appends_one_ledger_line_from_the_api) ... ok
test_resolve_threads_counts_a_thread_resolved_only_when_the_mutation_answers_true (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_resolve_threads_counts_a_thread_resolved_only_when_the_mutation_answers_true) ... ok
test_resolve_threads_passes_the_thread_id_as_a_graphql_variable (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_resolve_threads_passes_the_thread_id_as_a_graphql_variable) ... ok
test_resolve_threads_replies_round_trip_through_fill_sweep (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_resolve_threads_replies_round_trip_through_fill_sweep) ... ok
test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows (tests.unit.test_chain_github_scripts.ChainGithubScriptsTest.test_resolve_threads_replies_with_the_table_row_and_resolves_only_threads_with_rows) ... ok

----------------------------------------------------------------------
Ran 5 tests in 3.033s

OK
[exit 0]
```

## 6. shellcheck, with bash -n, shfmt and ruff

```console
$ shellcheck scripts/orchestrator/resolve-threads.sh && echo shellcheck-clean; bash -n scripts/orchestrator/resolve-threads.sh && echo "bash -n: ok"; shfmt -i 4 -sr -d scripts/orchestrator/resolve-threads.sh && echo shfmt-clean; git ls-files -s scripts/orchestrator/resolve-threads.sh | cut -c1-6
shellcheck-clean
bash -n: ok
shfmt-clean
100755
[exit 0]
```
```console
$ ruff --version; ruff format --check tests/unit/test_chain_github_scripts.py && ruff check tests/unit/test_chain_github_scripts.py && ruff check --preview --select FURB,PLW,SIM,ISC tests/unit/test_chain_github_scripts.py
ruff 0.17.0
1 file already formatted
All checks passed!
All checks passed!
[exit 0]
```

## 7. Caps

```console
$ git diff --numstat origin/main...HEAD
17	8	scripts/orchestrator/resolve-threads.sh
89	7	tests/unit/test_chain_github_scripts.py
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests|\.orchestration)\// {o += $1 + $2; f++} $3 ~ /^tests\// {t += $1} END {printf "outside tests/ and .orchestration/: %d changed lines (cap 200), %d files; under tests/: %d added lines (cap 1000)\n", o, f, t}'
outside tests/ and .orchestration/: 25 changed lines (cap 200), 1 files; under tests/: 89 added lines (cap 1000)
[exit 0]
```

## 8. The neighbouring module that holds fill_sweep.py's tests

```console
$ uv run python -m unittest tests/unit/test_orchestrator_tools.py 2>&1 | tail -3
Ran 40 tests in 27.699s

OK
[exit 0]
```

## 9. Mutation pass

```console
$ shasum -a 256 scripts/orchestrator/resolve-threads.sh > "$S/before.sha"; uv run --no-project python -I "$S/mutate.py" "$PWD"; shasum -a 256 -c "$S/before.sha"
M1 response unchecked: caught
M2 id in the query text: caught
M3 fixed without backticks: caught
M4 not-applicable without backticks: caught
M5 no exit 3: caught
M6 counted anyway: caught
M7 empty answer unnamed: caught
M8 old operation name: caught
mutations: 8, caught 8, survived 0
scripts/orchestrator/resolve-threads.sh: OK
[exit 0]
```
