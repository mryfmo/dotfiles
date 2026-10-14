---
task_id: dotfiles-T128-chain-review-scripts-a01
seat: claude-standard-dot-a002
code_commit: 1f307a6e
---

# Validation: dotfiles-T128-chain-review-scripts-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox. `MAIN` names the main checkout, `IN` the task's input directory there, and `S` a scratch directory under `/tmp/claude-501`. `UV_OFFLINE=1` was set, since uv cannot reach pypi from the sandbox. The output is verbatim, with the main checkout's path removed, and each block ends with the command's exit status. Captured at `1f307a6e`, before the PR was opened.

The whole unit suite, `make unit-test`'s `uv run python -m unittest discover -s tests/unit`, ran once in the sandbox and ended with `Ran 1082 tests in 471.510s` and `FAILED (failures=168, errors=103, skipped=2)`. No `origin/main` baseline was taken in the sandbox, so that run is evidence neither way; CI's `make unit-test` on the PR is. §7 runs the modules that exercise `scripts/orchestrator/`, and they all pass.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b  .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01.md
db9ff03a5eb720a4778fc357fb351926e7ecbb1d5af7a5f6cf11266232ba060b  .orchestration/dotfiles-T128-chain-review-scripts-a01/task.md
byte-identical
[exit 0]
```

## 2. Branch, the premise and the inputs

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
1f307a6e feat(orchestrator): local-review.sh, local-advisory.sh and sandbox-scan.sh land with their tests (T128 chain-review-scripts a01)
5ec860520075a2f0bbb551232de0f868e481a59c
[exit 0]
```
```console
$ git ls-tree --name-only origin/main scripts/orchestrator/ | /usr/bin/grep -c -E "local-review|local-advisory|sandbox-scan" || true
0
[exit 0]
```
```console
$ cd "$IN" && shasum -a 256 *.sh | sed -E "s/^([0-9a-f]{16})[0-9a-f]+/\1/"
2e44dabc23ea0397  local-advisory.sh
2258e370b9ff2575  local-review.sh
099f6c7534223cb4  sandbox-scan.sh
[exit 0]
```

## 3. Each port against its input

The input is formatted with the CI's shfmt first, so the diff shows the changes alone; `diff` exits 1 when the files differ.

```console
$ shfmt -i 4 -sr "$IN/local-review.sh" > "$S/input-local-review.sh" && diff -u --label input/local-review.sh --label scripts/orchestrator/local-review.sh "$S/input-local-review.sh" scripts/orchestrator/local-review.sh
--- input/local-review.sh
+++ scripts/orchestrator/local-review.sh
@@ -1,12 +1,29 @@
 #!/usr/bin/env bash
-# local-review.sh <task> <head> <pr>: C-32. Review a PR head's diff against main with the Bot's engine, locally, before the audit.
-# Run OUTSIDE the Bash sandbox (inside it codex exits 1: "failed to initialize in-process app-server client: Operation not permitted").
-# Writes .orchestration/validation/<task>-local-review-<sha7>.md (findings, then the transcript's final message with the worktree prefix stripped),
-# prints one line per unique finding and "local-review: <n> findings" last; exit 0 when n=0, 3 when n>0, 2 on a precondition.
+# @file local-review.sh
+# @brief Review a PR head's diff against main locally with the Bot's engine, once per head, before the audit (C-32).
+# @description
+#   Run outside the Bash sandbox: inside it codex exits 1 ("failed to initialize in-process app-server client:
+#   Operation not permitted"). An existing `.orchestration/validation/<task>-local-review-<sha7>.md` is reused and
+#   re-reported. Otherwise the clean review worktree (`$ORCH_REVIEW_WORKTREE`, else
+#   `.claude/worktrees/orchestrator-review`), a path with its own `.git` entry, is checked out detached at the head
+#   and left there, and the review binary (`$CODEX_BIN`, else codex) runs in it as `--profile review -s read-only
+#   review --base main`. The file gets the front matter, the unique `- [P0-3]` findings of the transcript's final
+#   message, and that message with the worktree prefix stripped; the findings are printed, then `local-review: <n>
+#   findings (<file>)`.
+# @arg $1 string Task id.
+# @arg $2 string The PR head commit, a local one.
+# @arg $3 int PR number.
+# @exitcode 0 No finding.
+# @exitcode 2 A precondition failed: the head is not a local commit, the review worktree is not a worktree root or not
+#   clean, or there is no review binary.
+# @exitcode 3 One or more findings.
+# @example
+#   scripts/orchestrator/local-review.sh dotfiles-T128-x-a01 "$(git rev-parse FETCH_HEAD)" 356
 set -euo pipefail
 task=$1 head=$2 pr=$3
 R="$(git rev-parse --show-toplevel)"
-W=$R/.claude/worktrees/orchestrator-review
+cd -- "$R"
+W=${ORCH_REVIEW_WORKTREE:-$R/.claude/worktrees/orchestrator-review}
 out=$R/.orchestration/validation/$task-local-review-${head:0:7}.md
 if [ -s "$out" ]; then
     # one sample per head (C-32): a review of this head exists; reuse it instead of sampling again
@@ -21,15 +38,27 @@
     echo "local-review: $head is not a local commit (fetch pull/$pr/head first)"
     exit 2
 }
+# Without its own .git entry, git -C would act on an enclosing checkout and move that one to the head.
+[ -e "$W/.git" ] || {
+    echo "local-review: $W is not a worktree root"
+    exit 2
+}
 [ -z "$(git -C "$W" status --porcelain)" ] || {
     echo "local-review: $W is not clean"
     exit 2
 }
+# Resolved in the root before the checkout and run by its absolute path, so no relative PATH entry (./bin) picks a
+# binary from the PR head.
+codex=$(command -v "${CODEX_BIN:-codex}") || {
+    echo "local-review: no review binary ${CODEX_BIN:-codex}"
+    exit 2
+}
+[[ $codex == /* ]] || codex=$R/$codex
 git -C "$W" checkout -q --detach "$head"
 base=$(git -C "$W" merge-base main HEAD)
 t0=$(date -u +%FT%TZ)
-tmp=$(mktemp)
-(cd "$W" && codex --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
+tmp=$(mktemp "${TMPDIR:-/tmp}/local-review.XXXXXX")
+(cd "$W" && "$codex" --profile review -s read-only review --base main < /dev/null > "$tmp" 2>&1) || echo "local-review: codex exited $? (see $out)"
 final=$(awk '/^codex$/{f=1; buf=""; next} f{buf=buf $0 "\n"} END{printf "%s", buf}' "$tmp" | sed "s#$W/##g")
 findings=$(printf '%s\n' "$final" | /usr/bin/grep -E '^- \[P[0-3]\]' | sort -u || true)
 n=$(printf '%s' "$findings" | /usr/bin/grep -c . || true)
[exit 1]
```
```console
$ shfmt -i 4 -sr "$IN/local-advisory.sh" > "$S/input-local-advisory.sh" && diff -u --label input/local-advisory.sh --label scripts/orchestrator/local-advisory.sh "$S/input-local-advisory.sh" scripts/orchestrator/local-advisory.sh
--- input/local-advisory.sh
+++ scripts/orchestrator/local-advisory.sh
@@ -1,9 +1,22 @@
 #!/usr/bin/env bash
-# local-advisory.sh <task> <head40> <owner-task-id>: plan 020 step 1.2 for the local review. Reads .orchestration/validation/<task>-local-review-<head7>.md; for each finding: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2), a P2/P3 appends a row `local:<head7>:<n>\tadvisory-p2` under the heading `## Owned by <owner>` of the acceptance record (created when missing) and a `local-finding: <head7>:<n> not-applicable:advisory P2 owned by <owner>; evidence=…` line. Exit 3 on a P0/P1, 0 otherwise.
+# @file local-advisory.sh
+# @brief Record a local review's P2/P3 findings as advisory rows of the acceptance record; stop on a P0/P1.
+# @description
+#   Plan 020 step 1.2 for the local review. Reads `.orchestration/validation/<task>-local-review-<sha7>.md`. Each
+#   unique finding, numbered from 1: a P0/P1 prints STOP (the PR's one round is over: the plan's step 4.2); any
+#   other appends the row `local:<sha7>:<n><TAB>advisory-p2` under the heading `## Owned by <owner>` of
+#   `.orchestration/acceptance/<task>.md` (created when missing) and a `local-finding: <sha7>:<n>
+#   not-applicable:advisory P2 owned by <owner> (…); evidence=…` line, each only when the record lacks it.
+# @arg $1 string Task id.
+# @arg $2 string The reviewed head, 40 hex characters.
+# @arg $3 string The task id that owns the advisory findings.
+# @exitcode 0 No P0/P1 finding.
+# @exitcode 2 No local review file.
+# @exitcode 3 A P0/P1 finding.
+# @example
+#   scripts/orchestrator/local-advisory.sh dotfiles-T128-x-a01 "$head" dotfiles-T128-x-followup-a01
 set -euo pipefail
-task=$1
-head=$2
-owner=$3
+task=$1 head=$2 owner=$3
 cd "$(git rev-parse --show-toplevel)"
 h7=${head:0:7}
 LR=".orchestration/validation/$task-local-review-$h7.md"
@@ -18,8 +31,7 @@
     exit 0
 }
 /usr/bin/grep -q "^## Owned by $owner" "$A" || printf '\n## Owned by %s (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)\n\n' "$owner" >> "$A"
-i=0
-stop=0
+i=0 stop=0
 while IFS= read -r line; do
     i=$((i + 1))
     case "$line" in
[exit 1]
```
```console
$ shfmt -i 4 -sr "$IN/sandbox-scan.sh" > "$S/input-sandbox-scan.sh" && diff -u --label input/sandbox-scan.sh --label scripts/orchestrator/sandbox-scan.sh "$S/input-sandbox-scan.sh" scripts/orchestrator/sandbox-scan.sh
--- input/sandbox-scan.sh
+++ scripts/orchestrator/sandbox-scan.sh
@@ -1,9 +1,24 @@
 #!/usr/bin/env bash
-# sandbox-scan.sh <task>: C-29 interim, extracted from the scratchpad integrate-prep.sh (lines 34 to 38). Prints the unsandboxed mutation calls found in the worker sandbox record .orchestration/sandboxes/<task>.md, or one line saying none; a hit is judged before the audit.
+# @file sandbox-scan.sh
+# @brief Print the unsandboxed mutation calls of a worker's sandbox record, so a hit is judged before the audit (C-29).
+# @description
+#   Reads `.orchestration/sandboxes/<task>.md`, a trailing `-fixtures` of the task id stripped. A line that names
+#   `dangerouslyDisableSandbox`, `outside the sandbox` or `unsandboxed` and a mutation (`git commit`, `git switch -c`,
+#   `git checkout`, `git add`, `git mv`, `git rm`, `cp `, `mv `, `> `, `tee `) but none of `counts`, `reads`, `lists`,
+#   matched case-insensitively, is printed with its line number, then the judge line; with no such line, one line says
+#   none. A missing record prints nothing.
+# @arg $1 string Task id.
+# @exitcode 0 Always.
+# @example
+#   scripts/orchestrator/sandbox-scan.sh dotfiles-T128-x-a01
 set -euo pipefail
 task=$1
 cd "$(git rev-parse --show-toplevel)"
 sb=".orchestration/sandboxes/${task%-fixtures}.md"
 if [ -f "$sb" ]; then
-    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"; else echo "sandbox scan: no unsandboxed mutation call in $sb"; fi
+    if /usr/bin/grep -n -i -E 'dangerouslyDisableSandbox|outside the sandbox|unsandboxed' "$sb" | /usr/bin/grep -i -E 'git (commit|switch -c|checkout|add|mv|rm)|cp |mv |> |tee ' | /usr/bin/grep -v -i 'counts\|reads\|lists'; then
+        echo "sandbox scan: unsandboxed mutation calls above (C-29); judge before the audit"
+    else
+        echo "sandbox scan: no unsandboxed mutation call in $sb"
+    fi
 fi
[exit 1]
```

## 4. The Check: the test module

```console
$ uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_advisory_records_p2_rows_and_stops_on_p0_p1) ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file) ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest.test_sandbox_scan_prints_the_unsandboxed_mutation_calls) ... ok

----------------------------------------------------------------------
Ran 3 tests in 3.359s

OK
[exit 0]
```

## 5. The Check: shellcheck, with bash -n, shfmt and ruff

```console
$ shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh && echo shellcheck-clean
shellcheck-clean
[exit 0]
```
```console
$ for f in scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh; do bash -n "$f" && echo "bash -n $f: ok"; done; shfmt -i 4 -sr -d scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh && echo shfmt-clean; git ls-files -s scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/sandbox-scan.sh | cut -c1-6
bash -n scripts/orchestrator/local-review.sh: ok
bash -n scripts/orchestrator/local-advisory.sh: ok
bash -n scripts/orchestrator/sandbox-scan.sh: ok
shfmt-clean
100755
100755
100755
[exit 0]
```
```console
$ ruff --version; ruff format --check tests/unit/test_chain_review_scripts.py && ruff check tests/unit/test_chain_review_scripts.py && ruff check --preview --select FURB,PLW,SIM,ISC tests/unit/test_chain_review_scripts.py
ruff 0.17.0
1 file already formatted
All checks passed!
All checks passed!
[exit 0]
```

## 6. The Check: caps

```console
$ git diff --numstat origin/main...HEAD
49	0	scripts/orchestrator/local-advisory.sh
75	0	scripts/orchestrator/local-review.sh
24	0	scripts/orchestrator/sandbox-scan.sh
230	0	tests/unit/test_chain_review_scripts.py
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests|\.orchestration)\// {o += $1 + $2; f++} $3 ~ /^tests\// {t += $1} END {printf "outside tests/ and .orchestration/: %d changed lines (cap 200), %d files; under tests/: %d added lines (cap 1000)\n", o, f, t}'
outside tests/ and .orchestration/: 148 changed lines (cap 200), 3 files; under tests/: 230 added lines (cap 1000)
[exit 0]
```

## 7. The neighbouring test modules

These modules exercise `scripts/orchestrator/` (test_orchestrator_tools.py copies the whole directory into its temporary repository).

```console
$ uv run python -m unittest tests/unit/test_orchestrator_tools.py tests/unit/test_task_checkers.py tests/unit/test_orch_gate_path.py tests/unit/test_chain_review_scripts.py 2>&1 | tail -3
Ran 53 tests in 35.788s

OK
[exit 0]
```

## 8. Mutation pass

`$S/mutate.py` applies one textual mutation at a time to one of the three scripts, runs the test module, and restores the script. A mutation counts as caught when the module fails. It skips any pattern that does not occur exactly once. The first full run (before amendment 1) caught 53 of 54, with S8 alive and R12/R13 skipped, since their patterns also matched the shdoc header. The fixture fix is in `1f307a6e`, and the narrowed patterns are in the runner. Below is the full run on the content `1f307a6e` commits (the scripts' hashes equal its blobs), G1, amendment 1's refusal, included:

```console
$ uv run --no-project python -I "$S/mutate.py" "$PWD"; shasum -a 256 -c "$S/before.sha"
R1 reuse off: caught
R2 reuse exit: caught
R3 reuse msg: caught
R4 local commit: caught
R5 dirty: caught
R6 no cd: caught
R7 no absolutize: caught
R8 lookup in W: caught
R9 CODEX_BIN ignored: caught
R10 ORCH_REVIEW_WORKTREE ignored: caught
R11 no checkout: caught
R12 profile: caught
R13 sandbox: caught
R14 stdin: caught
R15 final message: caught
R16 prefix: caught
R17 unique: caught
R18 codex exited: caught
R19 base: caught
R20 findings field: caught
R21 rm tmp: caught
R22 exit 3: caught
R23 no binary exit: caught
R24 file name: caught
R25 merge-base: caught
R26 cut 2000: caught
G1 worktree root: caught
A1 no file: caught
A2 no findings: caught
A3 heading guard: caught
A4 row guard: caught
A5 line guard: caught
A6 P0: caught
A7 P1: caught
A8 stop exit: caught
A9 unique: caught
A10 cut 120: caught
A11 backticks: caught
A12 numbering: caught
A13 evidence: caught
A14 last line: caught
A15 stop line: caught
S1 fixtures: caught
S2 grep1 -i: caught
S3 grep2 -i: caught
S4 grep3 -i: caught
S5 grep3 off: caught
S6 counts: caught
S7 reads: caught
S8 lists: caught
S9 -n: caught
S10 missing: caught
S11 exit hit: caught
S12 exit none: caught
S13 git add: caught
S14 outside: caught
S15 judge line: caught
mutations: 57, caught 57, survived 0
scripts/orchestrator/local-advisory.sh: OK
scripts/orchestrator/local-review.sh: OK
scripts/orchestrator/sandbox-scan.sh: OK
[exit 0]
```
