---
task_id: dotfiles-T128-chain-review-scripts-followup-a07
seat: claude-standard-dot-a011
code_head: c82e10a8
---

# Validation: dotfiles-T128-chain-review-scripts-followup-a07

Every command below ran inside the sandbox from `.claude/worktrees/worker-d` on the branch `tools/chain-review-scripts-followup-a07`, created with `--no-track` from `origin/main` `60a6fb2b` after a single-command `git fetch origin main`.

The tested code head is `c82e10a8`. Its commits: the task copy (`f2ab71ff`), the tests written first (`6a4190f1`, red), the script change (`fb264487`), the amended task copy (`41379201`, amendment 1), the worker review's tests (`06cc0fe1`, red) and its fix (`c82e10a8`). The final head adds only records under `.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/`, so the RESULT carries its diff and CI.

Names used below: `MAIN` is the main checkout, `SCRATCH` the seat's scratchpad, `REC` the a06 acceptance record, `PY` an absolute Python 3.15 used only to apply the mutations. Each block ends with the exit status of the command shown.

## 1. Task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  $MAIN/.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-chain-review-scripts-followup-a07.md: OK
[exit 0]
````

## 2. Item 1: the owned rows, read at the start

Item 1 owns the rows recorded under `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` in the a06 acceptance record. This seat's first reading, a grep at the start that is not pasted here, found no such section in either copy. The orchestrator's working copy now has one, and its modification time below is after the dispatch at 04:13:45Z; the committed record on `origin/main` still lacks it. Below: the counts in both copies, the modification time, the section as it stands, and the working copy's advisory-P2 search.

````console
$ git show origin/main:"$REC" | /usr/bin/grep -c -F "## Owned by $T"; /usr/bin/grep -c -F "## Owned by $T" "$MAIN/$REC"; TZ=UTC stat -f "modified %Sm" -t "%Y-%m-%dT%H:%M:%SZ" "$MAIN/$REC"; sed -n "/^## Owned by $T\$/,\$p" "$MAIN/$REC"
0
1
modified 2026-10-20T04:22:05Z
## Owned by dotfiles-T128-chain-review-scripts-followup-a07

No advisory rows: the three task-level audits of PR #434 (b9f562e, af86233, 34cc889) found orchestration P2s fixed in this record, and the a05 lineage's advisory row (`## Owned by …-a06` in the a05 record, audit:c646472:1) was realised by a06 itself (#434). The a07 text's Item 1 is therefore vacuous and its Item 2 (local-review.sh takes its base from canonical main as design 5.14 item 8 reads it) carries the task. Written 2026-10-20T04:22Z after a009's identical question on the T129 a06 owner text (C-102).

[exit 0]
````

````console
$ "$PY" -I -c "import json, sys; t = open(sys.argv[1]).read(); d = json.loads(t.split(chr(10) + \"---\" + chr(10), 1)[0].removeprefix(\"---\" + chr(10))); print(\"searches:\", d[\"searches\"]); print(\"ledger rows naming a07:\", sum(\"a07\" in json.dumps(r) for r in d[\"ledger\"]))" "$MAIN/$REC"
searches: [{'class': 'advisory-p2', 'records': []}]
ledger rows naming a07: 0
[exit 0]
````

## 3. Premises: canonical main, read live

````console
$ gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha; git rev-parse origin/main; git cat-file -t "$(git rev-parse origin/main)"
60a6fb2b324d0381c4a6e539b37c650105154a7e
60a6fb2b324d0381c4a6e539b37c650105154a7e
commit
[exit 0]
````

## 4. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git diff --name-status origin/main...c82e10a8
c82e10a8 fix(orchestrator): local-review.sh reads no replace ref or graft, so a seat cannot rewrite canonical main's history in the shared .git (T128 chain-review-scripts follow-up a07 item 2, worker review P2)
06cc0fe1 test(unit): local-review.sh reviews canonical main's real history under a planted replace ref or graft, and refuses a sha printed by a failing gh (T128 chain-review-scripts follow-up a07 item 2, worker review, red)
41379201 docs(orchestration): T128 chain-review-scripts follow-up a07 task copy, amendment 1 (PR #402 -> #434)
fb264487 fix(orchestrator): local-review.sh reviews against canonical main as gh api reports it, never a local main or origin/main ref (T128 chain-review-scripts follow-up a07 item 2)
6a4190f1 test(unit): local-review.sh takes its review base from canonical main through gh api, never a local main or origin/main ref (T128 chain-review-scripts follow-up a07 item 2, red)
f2ab71ff docs(orchestration): T128 chain-review-scripts follow-up a07 task copy
A	.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md
M	scripts/orchestrator/local-review.sh
M	tests/unit/test_chain_review_scripts.py
[exit 0]
````

## 5. Red before the change

At the test commit the script still diffs against the local `main`: the new test fails in each refusal subtest and on the base, and the existing local-review tests fail where they now expect the sha after `--base`.

````console
$ git worktree add --detach -q "$SCRATCH/a07-red" "$RED" && (cd "$SCRATCH/a07-red" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-red.out" 2>&1; echo "unittest exit status: $?"; /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^FAILED" "$SCRATCH/a07-red.out" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-170; git worktree remove --force "$SCRATCH/a07-red"
unittest exit status: 1
FAIL: test_local_review_keeps_env_S_shebang_arguments
FAIL: test_local_review_pins_the_review_binary_interpreter [the interpreter mise answers runs the binary]
FAIL: test_local_review_resolves_codex_through_mise_and_refuses_a_shim
FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [CODEX_BIN unset: codex resolved in the root before the checkout]
FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [CODEX_BIN set: that binary runs, a relative path resolved in the root]
FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [one review per head: the file is reused]
FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='', status=1)
FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='main', status=0)
FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0000000000000000000000000000000000000000', status=0)
FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
Ran 19 tests in 9.491s
FAILED (failures=10)
[exit 0]
````

At the worker review's test commit `06cc0fe1` the script is `fb264487`'s: a planted replace ref or graft for canonical main leaves the stand-in review binary nothing to review.

````console
$ git worktree add --detach -q "$SCRATCH/a07-red" "$RED2" && (cd "$SCRATCH/a07-red" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-red.out" 2>&1; echo "unittest exit status: $?"; /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^FAILED|^AssertionError" "$SCRATCH/a07-red.out" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-170; git worktree remove --force "$SCRATCH/a07-red"
unittest exit status: 1
FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref [replace]
AssertionError: 0 != 3 : 
FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref [graft]
AssertionError: 0 != 3 : 
Ran 19 tests in 11.207s
FAILED (failures=2)
[exit 0]
````

## 6. The Check

````console
$ git rev-parse HEAD; uv run python -c "import sys; print(sys.version.split()[0])"; uv run python -m unittest tests/unit/test_chain_review_scripts.py -v
c82e10a86d456f3534d26da6d4895bfc6e867693
3.10.22
test_local_advisory_classes_a_repeat_by_the_earlier_row (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_advisory_matches_an_earlier_review_id_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_advisory_matches_the_owner_heading_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_advisory_reads_the_whole_suffix_after_the_task_prefix (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_advisory_records_p2_rows_and_stops_on_p0_p1 (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_advisory_refuses_a_malformed_owner_id (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_advisory_refuses_an_absent_owner_task_and_hashes_the_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_and_local_advisory_refuse_a_task_or_head_that_leaves_their_directory (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_keeps_env_S_shebang_arguments (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_pins_the_review_binary_interpreter (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_refuses_a_quoted_env_S_shebang (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_resolves_codex_through_mise_and_refuses_a_shim (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_resolves_the_review_binary_before_the_checkout (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_reuses_only_a_file_that_records_this_head (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_strips_a_worktree_path_holding_sed_syntax_literally (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_local_review_writes_no_file_when_the_review_binary_fails (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok
test_sandbox_scan_prints_the_unsandboxed_mutation_calls (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest) ... ok

----------------------------------------------------------------------
Ran 19 tests in 14.180s

OK
[exit 0]
````

````console
$ shellcheck scripts/orchestrator/local-advisory.sh scripts/orchestrator/local-review.sh; echo "shellcheck exit $?"
shellcheck exit 0
[exit 0]
````

````console
$ git diff --numstat origin/main...HEAD -- . ":(exclude)tests" ":(exclude).orchestration"; git diff --numstat origin/main...HEAD -- tests; git diff --numstat origin/main...HEAD -- . ":(exclude)tests" ":(exclude).orchestration" | awk '{ c += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d changed lines (cap 200)\n", c }'; git diff --numstat origin/main...HEAD -- tests | awk '{ a += $1 } END { printf "added under tests/: %d lines (cap 1000)\n", a }'
21	5	scripts/orchestrator/local-review.sh
69	8	tests/unit/test_chain_review_scripts.py
outside tests/ and .orchestration/: 26 changed lines (cap 200)
added under tests/: 69 lines (cap 1000)
[exit 0]
````

## 7. Each claimed check against a wrong implementation

Each block truncates its output file, checks `c82e10a8` out into a scratch worktree, applies one replacement to `scripts/orchestrator/local-review.sh` (asserted to match exactly once; the block shows `mutated:` only when it applied) and only then runs the module. Each must turn a test red.

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'base=$("$found" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha < /dev/null) || base=' 'base=$(git -C "$R" rev-parse main) || base=' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "the local main as the base: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: base=$("$found" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha < /dev/null) || base= -> base=$(git -C "$R" rev-parse main) || base=
the local main as the base: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0000000000000000000000000000000000000000', status=0)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0d923eb8bd5e8e2b5c6d6ea08b7bb6a9147bbb3e', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='main', status=0)
   1 FAILED (failures=5)
   1 Ran 19 tests in 10.485s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'base=$("$found" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha < /dev/null) || base=' 'base=$(git -C "$R" rev-parse origin/main) || base=' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "origin/main as the base: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: base=$("$found" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha < /dev/null) || base= -> base=$(git -C "$R" rev-parse origin/main) || base=
origin/main as the base: unittest exit status: 1
   1 ERROR: test_local_review_pins_the_review_binary_interpreter
   1 FAIL: test_local_review_keeps_env_S_shebang_arguments
   1 FAIL: test_local_review_pins_the_review_binary_interpreter [the interpreter mise answers runs the binary]
   1 FAIL: test_local_review_resolves_codex_through_mise_and_refuses_a_shim
   1 FAIL: test_local_review_resolves_the_review_binary_before_the_checkout
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [a dirty review worktree or an unknown head exits 2 and runs 
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [CODEX_BIN set: that binary runs, a relative path resolved in
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [CODEX_BIN unset: codex resolved in the root before the check
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [no finding exits 0]
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [one review per head: the file is reused]
   1 FAIL: test_local_review_strips_a_worktree_path_holding_sed_syntax_literally
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0000000000000000000000000000000000000000', status=0)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='3f58c9466cc57132338677b331e74c4fc0090343', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='main', status=0)
   1 FAIL: test_local_review_writes_no_file_when_the_review_binary_fails
   1 FAILED (failures=16, errors=1)
   1 Ran 19 tests in 7.954s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'review --base "$base" < /dev/null' 'review --base main < /dev/null' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "the literal main passed to codex: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: review --base "$base" < /dev/null -> review --base main < /dev/null
the literal main passed to codex: unittest exit status: 1
   1 FAIL: test_local_review_keeps_env_S_shebang_arguments
   1 FAIL: test_local_review_pins_the_review_binary_interpreter [the interpreter mise answers runs the binary]
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [CODEX_BIN set: that binary runs, a relative path resolved in
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [CODEX_BIN unset: codex resolved in the root before the check
   1 FAIL: test_local_review_runs_the_review_binary_read_only_at_the_head_and_writes_one_file [one review per head: the file is reused]
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
   1 FAILED (failures=6)
   1 Ran 19 tests in 11.750s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" '[[ $base =~ ^[0-9a-f]{40}$ ]] || {' 'true || {' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "no 40-hex check: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: [[ $base =~ ^[0-9a-f]{40}$ ]] || { -> true || {
no 40-hex check: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0000000000000000000000000000000000000000', status=0)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='166d9bcdea8e645e126a5fa08b21418fb7b37772', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='main', status=0)
   1 FAILED (failures=5)
   1 Ran 19 tests in 11.668s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'git -C "$R" cat-file -e "$base^{commit}" 2> /dev/null || {' 'true || {' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "no local-commit check: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: git -C "$R" cat-file -e "$base^{commit}" 2> /dev/null || { -> true || {
no local-commit check: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0000000000000000000000000000000000000000', status=0)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='b080b50b18668da61f129df2580fbcc6cbeb6278', status=1)
   1 FAILED (failures=3)
   1 Ran 19 tests in 10.288s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'resolve gh "GitHub CLI"' 'resolve gh "GitHub CLI" yes' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "gh from PATH alone, never mise: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: resolve gh "GitHub CLI" -> resolve gh "GitHub CLI" yes
gh from PATH alone, never mise: unittest exit status: 1
   1 FAIL: test_local_review_resolves_codex_through_mise_and_refuses_a_shim
   1 FAILED (failures=1)
   1 Ran 19 tests in 11.506s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" '"$task" "$head" "$pr" "$base" "$t0"' '"$task" "$head" "$pr" "$(git -C "$W" merge-base main HEAD)" "$t0"' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "the recorded base from a local merge-base: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: "$task" "$head" "$pr" "$base" "$t0" -> "$task" "$head" "$pr" "$(git -C "$W" merge-base main HEAD)" "$t0"
the recorded base from a local merge-base: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref
   1 FAILED (failures=1)
   1 Ran 19 tests in 11.636s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'export GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null' 'export GIT_GRAFT_FILE=/dev/null' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "replace refs read: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: export GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null -> export GIT_GRAFT_FILE=/dev/null
replace refs read: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref [replace]
   1 FAILED (failures=1)
   1 Ran 19 tests in 12.923s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'export GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null' 'export GIT_NO_REPLACE_OBJECTS=1' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "grafts read: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: export GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null -> export GIT_NO_REPLACE_OBJECTS=1
grafts read: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref [graft]
   1 FAILED (failures=1)
   1 Ran 19 tests in 13.079s
[exit 0]
````

````console
$ : > "$SCRATCH/a07-mut.out"; git worktree add --detach -q "$SCRATCH/a07-mut" "$H" && "$PY" -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, (s.count(o), o); open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/a07-mut/scripts/orchestrator/local-review.sh" 'resolve gh "GitHub CLI"' 'git -C "$W" checkout -q --detach "$head"; resolve gh "GitHub CLI"' && { (cd "$SCRATCH/a07-mut" && uv run python -m unittest tests/unit/test_chain_review_scripts.py) > "$SCRATCH/a07-mut.out" 2>&1; echo "the review worktree checked out before canonical main is read: unittest exit status: $?"; < "$SCRATCH/a07-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests.unit.test_chain_review_scripts.ChainReviewScriptsTest)//" | cut -c1-150 | sort | uniq -c; }; git worktree remove --force "$SCRATCH/a07-mut"
mutated: resolve gh "GitHub CLI" -> git -C "$W" checkout -q --detach "$head"; resolve gh "GitHub CLI"
the review worktree checked out before canonical main is read: unittest exit status: 1
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='0000000000000000000000000000000000000000', status=0)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='3124a60a4193aa064c2e304026c4ef9deb84e900', status=1)
   1 FAIL: test_local_review_takes_its_base_from_canonical_main_never_a_local_ref (answer='main', status=0)
   1 FAILED (failures=4)
   1 Ran 19 tests in 13.215s
[exit 0]
````

## 8. Lint and formatting

````console
$ ruff format --config ruff.toml --check tests/unit/test_chain_review_scripts.py; ruff check --config ruff.toml tests/unit/test_chain_review_scripts.py; shfmt --indent 4 --space-redirects --diff scripts/orchestrator/local-review.sh && echo "shfmt: no diff"; "$PY" -I scripts/lint-comparisons.py --baseline scripts/lint-comparisons-baseline.tsv scripts/orchestrator/local-review.sh; echo "lint-comparisons exit $?"
1 file already formatted
All checks passed!
shfmt: no diff
lint-comparisons exit 0
[exit 0]
````

## 9. The review gate

Run with the records in place and uncommitted, before the evidence commit.

````console
$ make require-crit-review AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/$T/$T-worker-review-receipt.md
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
[exit 0]
````
