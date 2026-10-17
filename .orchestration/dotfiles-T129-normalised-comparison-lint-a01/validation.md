---
task_id: dotfiles-T129-normalised-comparison-lint-a01
seat: claude-review-dot-a005
code_commit: e88f8f05
---

# Validation: dotfiles-T129-normalised-comparison-lint-a01

Every command ran from the worktree `.claude/worktrees/worker-d` on the branch `lint/normalised-comparisons-a01` at `e88f8f05`, inside the sandbox; `MAIN` names the main checkout and `T` the task id. uv ran offline (`UV_OFFLINE=1` or `--offline`). The output is verbatim, with the main checkout's path replaced by `$MAIN`, and each block ends with the exit status of the command shown (a pipeline's is its last command's). Premise 1's `grep -c` prints `0` and exits 1, so its `|| true` makes the block's status 0 as in the task file.

## 1. Task file (Amendment 2's text, sha256 655e085b…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
655e085b88a2e93be12a8c7913a7aee3431f074673e3ac24d2ab34a6e305651f  $MAIN/.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md
655e085b88a2e93be12a8c7913a7aee3431f074673e3ac24d2ab34a6e305651f  .orchestration/dotfiles-T129-normalised-comparison-lint-a01/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-normalised-comparison-lint-a01.md: OK
[exit 0]
```
## 2. Branch and base
```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
e88f8f05 fix(lint): the R2 accepted forms keep a literal tail, Python R6 needs re as the receiver, one row per distinct line (T129 re-review)
26ed34bb fix(lint): find the test word anywhere on the line and anchor jq programs at the jq word (T129 worker review)
9fbd0de0 refactor(lint): bring lint-comparisons.py under the 200-line cap (T129 Amendment 2, D-cap-F2)
4663dc4d feat(lint): refuse string-form comparisons of paths, URLs and processes (T129 normalised-comparison lint a01)
35ab0e95a7fe27c501db3478d4f37e69a514d532
[exit 0]
```
## 2a. Premise 1 (no Makefile lint target on origin/main)
```console
$ git show origin/main:Makefile | /usr/bin/grep -cE "^lint:" || true
0
[exit 0]
```
## 2b. Premise 2 (the test workflow runs make unit-test for the lint's file set)
```console
$ git show origin/main:.github/workflows/test.yaml | /usr/bin/grep -cE "make unit-test|home/\|install/\|scripts/"
2
[exit 0]
```
## 2c. Premise 3 (the four known string-form comparisons)
```console
$ git grep -nE '\[\[ "\$file_path" == \*/|endswith\("/\.project-map|endswith\(\$suffix\)|grep -E "\^\(\$\{ids%\|\}\)' origin/main -- home/dot_claude/hooks/executable_project-map-reload.sh scripts/orchestrator/resolve-threads.sh scripts/orchestrator/local-advisory.sh | sed 's/^origin\/main://' | cut -d: -f1,2
home/dot_claude/hooks/executable_project-map-reload.sh:13
home/dot_claude/hooks/executable_project-map-reload.sh:21
scripts/orchestrator/local-advisory.sh:81
scripts/orchestrator/resolve-threads.sh:45
[exit 0]
```
## 3. The Check: the three tests
```console
$ UV_OFFLINE=1 uv run --no-project python -m unittest tests/unit/test_lint_comparisons.py -v
test_a_baseline_row_matching_no_hit_fails_as_stale (tests.unit.test_lint_comparisons.LintComparisonsTest.test_a_baseline_row_matching_no_hit_fails_as_stale) ... ok
test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted (tests.unit.test_lint_comparisons.LintComparisonsTest.test_each_rule_refuses_its_fixture_and_each_normaliser_and_the_marker_are_accepted) ... ok
test_the_tracked_tree_is_clean_against_the_baseline (tests.unit.test_lint_comparisons.LintComparisonsTest.test_the_tracked_tree_is_clean_against_the_baseline) ... ok

----------------------------------------------------------------------
Ran 3 tests in 2.969s

OK
[exit 0]
```
## 3a. The Check: the lint over the tracked tree against the committed baseline (exit 0, no output)
```console
$ uv run --offline --no-project python -I scripts/lint-comparisons.py
[exit 0]
```
## 3b. The rule table as the lint prints it
```console
$ uv run --offline --no-project python -I scripts/lint-comparisons.py --list-rules
R0 the allow marker carries no reason
R1 shell [[ ]] or [ ] compares a path or URL operand by its string form
R2 shell case matches a path or URL operand by its string form
R3 jq compares a URL or path by its string form
R4 Python compares a path or URL by its string form
R5 a process is read as text (ps piped to grep, awk, cut or sed; pgrep -f on a variable)
R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
shortcut: the lint is statement-local, so a variable normalised on an earlier line and compared later is a hit (mark it with the marker and its reason); upgrade to a cross-line data-flow when a second such marker is needed
[exit 0]
```
## 3c. ruff check
```console
$ ruff check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py
All checks passed!
[exit 0]
```
## 3d. ruff format --check (CI runs it over every tracked .py)
```console
$ ruff format --check scripts/lint-comparisons.py tests/unit/test_lint_comparisons.py
2 files already formatted
[exit 0]
```
## 3e. The same module through unittest discovery, as make unit-test runs it
```console
$ UV_OFFLINE=1 uv run --no-project python -m unittest discover -s tests/unit -p "test_lint_comparisons.py" 2>&1 | tail -3
Ran 3 tests in 2.974s

OK
[exit 0]
```
## 3f. The whole suite in this sandbox (the failures are the sandbox's: process visibility, network, home paths; CI's four test jobs passed on the pushed heads, §8)
```console
$ UV_OFFLINE=1 uv run --no-project python -m unittest discover -s tests/unit 2>&1 | tail -4
Ran 1162 tests in 636.217s

FAILED (failures=177, errors=107, skipped=2)
done rc=0
```
## 4. The baseline's shape (rows, rows per rule, malformed rows, distinct rows)
```console
$ wc -l scripts/lint-comparisons-baseline.tsv; cut -f2 scripts/lint-comparisons-baseline.tsv | sort | uniq -c; awk -F'\t' 'NF != 3 || $3 !~ /^[0-9a-f]{64}$/' scripts/lint-comparisons-baseline.tsv | wc -l; sort -u scripts/lint-comparisons-baseline.tsv | wc -l
      85 scripts/lint-comparisons-baseline.tsv
  32 R1
   2 R2
   6 R3
  41 R4
   4 R6
       0
      85
[exit 0]
```
## 5. Caps: git diff --numstat origin/main...HEAD
```console
$ git diff --numstat origin/main...HEAD
85	0	scripts/lint-comparisons-baseline.tsv
200	0	scripts/lint-comparisons.py
160	0	tests/unit/test_lint_comparisons.py
[exit 0]
```
## 5a. Caps summed as Amendment 2's Check reads them (the baseline excluded; the script alone at most 200 lines)
```console
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^tests\// && $3 !~ /^\.orchestration\// && $3 != "scripts/lint-comparisons-baseline.tsv" {o += $1 + $2} $3 ~ /^tests\// {t += $1} END {print "outside tests/ and .orchestration/, the baseline excluded (D-cap-F2): " o " changed lines (cap 200); under tests/: " t " added lines (cap 1000)"}'; wc -l scripts/lint-comparisons.py
outside tests/ and .orchestration/, the baseline excluded (D-cap-F2): 200 changed lines (cap 200); under tests/: 160 added lines (cap 1000)
     200 scripts/lint-comparisons.py
[exit 0]
```
## 6. CompactionDB memory add (Message Contract: before completion)
```console
$ UV_OFFLINE=1 uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "[memory:decision] T129 lint-comparisons: the baseline … never a substring."
53f1d551-ba19-4a5d-817c-984f1a801a4a
[exit 0]
```
## 7. Push and the draft PR (outside the sandbox through the permission gate; the push in the boundary script's form, the global config skipped so the SSH rewrite does not apply)
```console
$ GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin lint/normalised-comparisons-a01
remote: Create a pull request for 'lint/normalised-comparisons-a01' on GitHub by visiting:
remote:      https://github.com/mryfmo/dotfiles/pull/new/lint/normalised-comparisons-a01
remote:
To https://github.com/mryfmo/dotfiles
 * [new branch]        lint/normalised-comparisons-a01 -> lint/normalised-comparisons-a01
[exit 0]
```
```console
$ gh pr create --draft --repo mryfmo/dotfiles --base main --head lint/normalised-comparisons-a01 --title "feat(lint): refuse string-form comparisons of paths, URLs and processes (T129 PR F2)" --body-file <pr body>
https://github.com/mryfmo/dotfiles/pull/387
[exit 0]
```
## 8. CI on the pushed heads (gh pr checks, outside the sandbox)
```console
$ gh pr checks 387 --repo mryfmo/dotfiles --watch --interval 30   # head 9fbd0de0, 11:11Z to 11:20Z
(the 13 checks: all pass; the listing of 11:20:26Z is in the session, pasted below for head 26ed34bb)
```
```console
$ gh pr checks 387 --repo mryfmo/dotfiles --watch --interval 30; gh pr view 387 --json headRefOid,isDraft   # head 26ed34bb
validate  pass  2m6s  https://github.com/mryfmo/dotfiles/actions/runs/39028743728/job/117384800424  
CodeRabbit  pass  0    Review skipped: automatic reviews are disabled
GitGuardian Security Checks  pass  0  https://dashboard.gitguardian.com  
private-bootstrap (macos-14, client)  pass  11s  https://github.com/mryfmo/dotfiles/actions/runs/390287
private-bootstrap (ubuntu-24.04, client)  pass  7s  https://github.com/mryfmo/dotfiles/actions/runs/390
private-bootstrap (ubuntu-24.04, server)  pass  11s  https://github.com/mryfmo/dotfiles/actions/runs/39
public-bootstrap (macos-14, client)  pass  7m43s  https://github.com/mryfmo/dotfiles/actions/runs/39028
public-bootstrap (ubuntu-24.04, client)  pass  9m27s  https://github.com/mryfmo/dotfiles/actions/runs/3
public-bootstrap (ubuntu-24.04, server)  pass  6m21s  https://github.com/mryfmo/dotfiles/actions/runs/3
test (macos-14, client)  pass  7m32s  https://github.com/mryfmo/dotfiles/actions/runs/39028743765/job/1
test (ubuntu-24.04, client)  pass  8m30s  https://github.com/mryfmo/dotfiles/actions/runs/39028743765/j
test (ubuntu-24.04, server)  pass  4m59s  https://github.com/mryfmo/dotfiles/actions/runs/39028743765/j
test (ubuntu-26.04, client)  pass  8m38s  https://github.com/mryfmo/dotfiles/actions/runs/39028743765/j
validate  pass  2m6s  https://github.com/mryfmo/dotfiles/actions/runs/39028743728/job/117384800424  
watch rc=
26ed34bb  true
11:38:52Z
```
The code head `e88f8f05` had 5 checks passed and 8 pending when this record was committed (11:41:48Z); its results and the final head's (this evidence commit, `.orchestration/` only) are read by the orchestrator on GitHub and named in the RESULT.
