---
task_id: dotfiles-T133-hold-playbook-a01
seat: claude-standard-dot-a011
code_head: a6c073e5
---

# Validation: dotfiles-T133-hold-playbook-a01

Every command below ran from the worktree `.claude/worktrees/worker-d` on the branch `tools/hold-playbook-a01`, created with `--no-track` from `origin/main` `b22a5580`, inside the sandbox. Two identities apply. The tested code head is `a6c073e5`: the task copy (`5e719af3`), the tests written first (`6a72398c`, red), the script (`f76db928`) and the worker review's fixes (`a6c073e5`). The final head is the next commit, which adds this record and the other evidence and touches only `.orchestration/dotfiles-T133-hold-playbook-a01/`. The RESULT carries the final head's diff against `a6c073e5` and its CI, because a record cannot hold its own commit's CI. `MAIN` names the main checkout, `T` the task id, `SCRATCH` the seat's scratchpad, `BASE` the base sha (`origin/main`), `H` the tested code head, `RED` the test commit, and `UT` the Check's unittest command without `-v`. The output is verbatim, with the main checkout's, the home directory's and the scratchpad's paths replaced by `$MAIN`, `$HOME` and `$SCRATCH`. Each block ends with the exit status of the command shown, and every status line captures `rc=$?` before any command substitution.

## 1. Task file and task copy

````console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
e33f0aa1927956b7e5d17fe06987d611e8ed50ebb3f09f11bff7f9293b9e3d1c  $MAIN/.orchestration/tasks/dotfiles-T133-hold-playbook-a01.md
e33f0aa1927956b7e5d17fe06987d611e8ed50ebb3f09f11bff7f9293b9e3d1c  .orchestration/dotfiles-T133-hold-playbook-a01/task.md
byte-identical
[exit 0]
````

````console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T133-hold-playbook-a01.md: OK
[exit 0]
````

## 2. Branch and provenance

````console
$ git log --oneline origin/main..HEAD; git merge-base origin/main HEAD; git diff --name-status origin/main...a6c073e5
a6c073e5 fix(orchestrator): hold-playbook.sh refuses a multi-line remedy and a non-slug class, reports an unknown remedy's real globs; tests pin segment-bounded wildcards and the UTC time (T133 hold-playbook a01, worker review P3s)
f76db928 feat(orchestrator): hold-playbook.sh expands a class's remedy into a replan skeleton and records a pending decision for out-of-scope globs (T133 hold-playbook a01, plan 024 P1-13)
6a72398c test(orchestrator): hold-playbook.sh expands a class into a replan skeleton and records an out-of-scope decision (T133 hold-playbook a01, plan 024 P1-13, red)
5e719af3 docs(orchestration): T133 hold-playbook a01 task copy (plan 024 P1-13)
b22a5580d0778e57a66d3f75c76e3c55b88701e1
A	.orchestration/dotfiles-T133-hold-playbook-a01/task.md
A	scripts/orchestrator/hold-playbook.sh
A	tests/unit/test_hold_playbook.py
[exit 0]
````

## 3. Red before the script, green at the code head

The tests were committed in `6a72398c` before `scripts/orchestrator/hold-playbook.sh` existed. There every test fails in setUp, which copies the script into its fixture tree. That includes the vocabulary test, because the vocabulary check is a mode of the script (orchestrator note). The green runs are at `a6c073e5`.

````console
$ git worktree add --detach -q "$SCRATCH/hp-red" "$RED" && (cd "$SCRATCH/hp-red" && $UT) > "$SCRATCH/hp-red.out" 2>&1; rc=$?; echo "unittest exit status: ${rc}"; < "$SCRATCH/hp-red.out" /usr/bin/grep -E "^(FAIL|ERROR):|Error:|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c | cut -c1-220; git worktree remove --force "$SCRATCH/hp-red"
unittest exit status: 1
   1 ERROR: test_existing_replan_exits_4
   1 ERROR: test_invalid_task_id_is_refused
   1 ERROR: test_known_class_without_remedy_is_reported
   1 ERROR: test_record_text_is_never_executed
   1 ERROR: test_scope_comparison_covers_the_whole_glob
   1 ERROR: test_three_classes_expand_into_replans
   1 ERROR: test_uncovered_scope_appends_pending_decision
   1 ERROR: test_unknown_class_exits_2
   1 ERROR: test_vocabulary_covers_mistake_classes
   1 FAILED (errors=9)
   9 FileNotFoundError: [Errno 2] No such file or directory: '$SCRATCH/hp-red/scripts/orchestra
   1 Ran 9 tests in 0.006s
[exit 0]
````

````console
$ git rev-parse HEAD; uv run --no-project --with pyyaml python -m unittest tests.unit.test_hold_playbook -v
a6c073e5256e8335747aef710b519e93794d1d26
test_existing_replan_exits_4 (tests.unit.test_hold_playbook.HoldPlaybookTests.test_existing_replan_exits_4) ... ok
test_invalid_task_id_is_refused (tests.unit.test_hold_playbook.HoldPlaybookTests.test_invalid_task_id_is_refused) ... ok
test_known_class_without_remedy_is_reported (tests.unit.test_hold_playbook.HoldPlaybookTests.test_known_class_without_remedy_is_reported) ... ok
test_record_text_is_never_executed (tests.unit.test_hold_playbook.HoldPlaybookTests.test_record_text_is_never_executed) ... ok
test_scope_comparison_covers_the_whole_glob (tests.unit.test_hold_playbook.HoldPlaybookTests.test_scope_comparison_covers_the_whole_glob) ... ok
test_three_classes_expand_into_replans (tests.unit.test_hold_playbook.HoldPlaybookTests.test_three_classes_expand_into_replans) ... ok
test_uncovered_scope_appends_pending_decision (tests.unit.test_hold_playbook.HoldPlaybookTests.test_uncovered_scope_appends_pending_decision) ... ok
test_unknown_class_exits_2 (tests.unit.test_hold_playbook.HoldPlaybookTests.test_unknown_class_exits_2) ... ok
test_vocabulary_covers_mistake_classes (tests.unit.test_hold_playbook.HoldPlaybookTests.test_vocabulary_covers_mistake_classes) ... ok

----------------------------------------------------------------------
Ran 9 tests in 1.902s

OK
[exit 0]
````

## 4. The Check's lint commands

````console
$ shellcheck scripts/orchestrator/hold-playbook.sh
[exit 0]
````

The Check names `shfmt -d` without flags. The repository formats shell with `shfmt --indent 4 --space-redirects` (`make format`, Makefile line 180). Its `.editorconfig` sets `indent_size = 4` and `space_redirects = true` for `*.sh` but no `indent_style`, and shfmt v3.14.1 then indents with tabs. So the bare command flags every four-space script. The next two blocks show this on the unchanged base, then the script against the repository's flags.

````console
$ shfmt -d scripts/orchestrator/hold-playbook.sh > "$SCRATCH/hp-shfmt.out"; rc=$?; echo "shfmt -d exit status: ${rc}"; /usr/bin/grep -c "^-    " "$SCRATCH/hp-shfmt.out"; git worktree add --detach -q "$SCRATCH/hp-base" "$BASE" && (cd "$SCRATCH/hp-base" && for f in scripts/orchestrator/orch-audit.sh scripts/orchestrator/dispatch.sh scripts/orchestrator/ci-rerun.sh; do shfmt -d "$f" > /dev/null; echo "base ${BASE:0:8}: shfmt -d $f exit status: $?"; done); git worktree remove --force "$SCRATCH/hp-base"
shfmt -d exit status: 1
9
base b22a5580: shfmt -d scripts/orchestrator/orch-audit.sh exit status: 1
base b22a5580: shfmt -d scripts/orchestrator/dispatch.sh exit status: 1
base b22a5580: shfmt -d scripts/orchestrator/ci-rerun.sh exit status: 1
[exit 0]
````

````console
$ shfmt --indent 4 --space-redirects --diff scripts/orchestrator/hold-playbook.sh
[exit 0]
````

## 5. Each test against a wrong implementation

Each block checks `a6c073e5` out into a scratch worktree, replaces one line of `scripts/orchestrator/hold-playbook.sh` with a plausible wrong implementation, and runs `UT`. The replacement is asserted to apply exactly once. The first block is the unmutated baseline.

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "baseline: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED"; git worktree remove --force "$SCRATCH/hp-mut"
baseline: unittest exit status: 0
Ran 9 tests in 1.345s
OK
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    a, g = tokens(entry), tokens(glob)' '    import fnmatch; return fnmatch.fnmatchcase(glob, entry)' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "coverage by the pattern string as a filename: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: a, g = tokens(entry), tokens(glob) -> import fnmatch; return fnmatch.fnmatchcase(glob, entry)
coverage by the pattern string as a filename: unittest exit status: 1
   1 FAIL: test_scope_comparison_covers_the_whole_glob
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.303s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    scope = [(glob, [a for a in allowed if covers(a, glob)]) for glob in radius]' '    scope = [(glob, [a for a in allowed if all(covers(a, str(p.relative_to(o.parent))) for p in o.parent.glob(glob))]) for glob in radius]' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "coverage by the existing files only: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: scope = [(glob, [a for a in allowed if covers(a, glob)]) for glob in radius] -> scope = [(glob, [a for a in allowed if all(covers(a, str(p.relative_to(o.parent))) for p in o.parent.glob(glob))]) for glob in radius]
coverage by the existing files only: unittest exit status: 1
   1 FAIL: test_existing_replan_exits_4
   1 FAIL: test_record_text_is_never_executed
   1 FAIL: test_scope_comparison_covers_the_whole_glob
   1 FAIL: test_three_classes_expand_into_replans (cls='colored-json-parse')
   1 FAIL: test_three_classes_expand_into_replans (cls='concurrent-ff-clobber')
   1 FAIL: test_three_classes_expand_into_replans (cls='records-form')
   1 FAIL: test_uncovered_scope_appends_pending_decision
   1 FAILED (failures=7)
   1 Ran 9 tests in 1.281s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" 'os.O_WRONLY | os.O_CREAT | os.O_EXCL' 'os.O_WRONLY | os.O_CREAT | os.O_TRUNC' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "an existing replan overwritten: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: os.O_WRONLY | os.O_CREAT | os.O_EXCL -> os.O_WRONLY | os.O_CREAT | os.O_TRUNC
an existing replan overwritten: unittest exit status: 1
   1 FAIL: test_existing_replan_exits_4
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.143s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '            csv.writer(out, delimiter="\t", lineterminator="\n").writerow(row)' '            pass' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "no decision row: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: csv.writer(out, delimiter="\t", lineterminator="\n").writerow(row) -> pass
no decision row: unittest exit status: 1
   1 ERROR: test_record_text_is_never_executed
   1 ERROR: test_scope_comparison_covers_the_whole_glob
   1 FAIL: test_existing_replan_exits_4
   1 FAIL: test_uncovered_scope_appends_pending_decision
   1 FAILED (failures=2, errors=2)
   1 Ran 9 tests in 1.091s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '        "pending",' '        "pending; default: proceed",' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "a default in the decision row: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: "pending", -> "pending; default: proceed",
a default in the decision row: unittest exit status: 1
   1 FAIL: test_uncovered_scope_appends_pending_decision
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.312s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    if cls not in classes:' '    if False:' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "an unknown class not refused: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: if cls not in classes: -> if False:
an unknown class not refused: unittest exit status: 1
   1 FAIL: test_unknown_class_exits_2 (cls='no-such-class')
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.334s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    [[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || {' '    [[ -n $1 ]] || {' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "the task id not checked: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: [[ $1 =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || { -> [[ -n $1 ]] || {
the task id not checked: unittest exit status: 1
   1 FAIL: test_invalid_task_id_is_refused (task='-x')
   1 FAIL: test_invalid_task_id_is_refused (task='../x')
   1 FAIL: test_invalid_task_id_is_refused (task='.x')
   1 FAIL: test_invalid_task_id_is_refused (task='a b')
   1 FAIL: test_invalid_task_id_is_refused (task='a/b')
   1 FAIL: test_invalid_task_id_is_refused (task='dotfiles-T999-fixture-a01;true')
   1 FAIL: test_invalid_task_id_is_refused (task='x\n')
   1 FAILED (failures=7)
   1 Ran 9 tests in 1.681s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    unknown = remedy == "unknown"' '    unknown = False' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "an unknown remedy not reported: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: unknown = remedy == "unknown" -> unknown = False
an unknown remedy not reported: unittest exit status: 1
   1 FAIL: test_known_class_without_remedy_is_reported
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.214s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")' '    os.system("echo " + remedy + " " + " ".join(radius)); now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "record text run by a shell: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") -> os.system("echo " + remedy + " " + " ".join(radius)); now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
record text run by a shell: unittest exit status: 1
   1 FAIL: test_record_text_is_never_executed
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.484s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '        return 2' '        return 0' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "missing classes not reported: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: return 2 -> return 0
missing classes not reported: unittest exit status: 1
   1 FAIL: test_vocabulary_covers_mistake_classes
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.287s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" 'g[j] is not ANY and g[j] != "/" and absorbs(i, j + 1)' 'g[j] is not ANY and absorbs(i, j + 1)' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "an entry * taking a /: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: g[j] is not ANY and g[j] != "/" and absorbs(i, j + 1) -> g[j] is not ANY and absorbs(i, j + 1)
an entry * taking a /: unittest exit status: 1
   1 FAIL: test_scope_comparison_covers_the_whole_glob
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.293s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" 'isinstance(g[j], str) and g[j] != "/") and absorbs(i + 1, j + 1)' 'isinstance(g[j], str)) and absorbs(i + 1, j + 1)' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "an entry ? taking a /: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: isinstance(g[j], str) and g[j] != "/") and absorbs(i + 1, j + 1) -> isinstance(g[j], str)) and absorbs(i + 1, j + 1)
an entry ? taking a /: unittest exit status: 1
   1 FAIL: test_scope_comparison_covers_the_whole_glob
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.362s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" 'now = datetime.datetime.now(datetime.timezone.utc)' 'now = datetime.datetime.now()' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "local time in the decision row (red where the local zone is not UTC; this seat runs in JST): unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: now = datetime.datetime.now(datetime.timezone.utc) -> now = datetime.datetime.now()
local time in the decision row (red where the local zone is not UTC; this seat runs in JST): unittest exit status: 1
   1 FAIL: test_uncovered_scope_appends_pending_decision
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.292s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    if not paths([remedy]) or not remedy.strip()' '    if not isinstance(remedy, str) or not remedy.strip()' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "a multi-line remedy accepted: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: if not paths([remedy]) or not remedy.strip() -> if not isinstance(remedy, str) or not remedy.strip()
a multi-line remedy accepted: unittest exit status: 1
   1 FAIL: test_record_text_is_never_executed
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.199s
[exit 0]
````

````console
$ git worktree add --detach -q "$SCRATCH/hp-mut" "$H" && uv run --no-project python -I -c 'import sys; p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1, o; open(p, "w").write(s.replace(o, n)); print("mutated:", o.strip(), "->", n.strip())' "$SCRATCH/hp-mut/scripts/orchestrator/hold-playbook.sh" '    if not paths([cls]):' '    if False:' && (cd "$SCRATCH/hp-mut" && $UT) > "$SCRATCH/hp-mut.out" 2>&1; rc=$?; echo "a class with a tab accepted: unittest exit status: ${rc}"; < "$SCRATCH/hp-mut.out" /usr/bin/grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | sed "s/ (tests\.unit[^)]*)//" | sort | uniq -c; git worktree remove --force "$SCRATCH/hp-mut"
mutated: if not paths([cls]): -> if False:
a class with a tab accepted: unittest exit status: 1
   1 FAIL: test_unknown_class_exits_2 (cls='a\tb')
   1 FAILED (failures=1)
   1 Ran 9 tests in 1.253s
[exit 0]
````

## 6. Caps and changed files

````console
$ git diff --numstat origin/main...HEAD; git diff --numstat origin/main...HEAD | awk '$3 ~ /^tests\// { t += $1 + $2; next } $3 ~ /^\.orchestration\// { next } { o += $1 + $2 } END { printf "outside tests/ and .orchestration/: %d of 350\ntests/: %d of 400\n", o, t }'
135	0	.orchestration/dotfiles-T133-hold-playbook-a01/task.md
231	0	scripts/orchestrator/hold-playbook.sh
243	0	tests/unit/test_hold_playbook.py
outside tests/ and .orchestration/: 231 of 350
tests/: 243 of 400
[exit 0]
````

This record is part of the final head, so it cannot list that commit's own paths. The RESULT carries `git diff --name-only a6c073e5 <final head>`, which lists only `.orchestration/dotfiles-T133-hold-playbook-a01/` paths.

## 7. make format

An inherited failure is reproduced on the unchanged base: every file the whole-tree shfmt step flags is checked against the merge base.

````console
$ make format > "$SCRATCH/hp-format.out" 2>&1; rc=$?; echo "make format exit status: ${rc}"; base="$(git merge-base origin/main HEAD)"; sed -n "s/^diff \([^ ]*\)\.orig .*/\1/p" "$SCRATCH/hp-format.out" > "$SCRATCH/hp-flagged.txt"; echo "files the whole-tree shfmt step flags: $(wc -l < "$SCRATCH/hp-flagged.txt" | tr -d " ")"; while read -r f; do git diff --quiet "$base" HEAD -- "$f" && echo "unchanged from ${base:0:8}: $f" || echo "CHANGED by this PR: $f"; done < "$SCRATCH/hp-flagged.txt"
make format exit status: 2
files the whole-tree shfmt step flags: 12
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh
unchanged from b22a5580: .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh
unchanged from b22a5580: home/dot_claude/hooks/executable_project-map-reload.sh
unchanged from b22a5580: tests/install/macos/common/brew.bats
[exit 0]
````

````console
$ git ls-files -z "*.py" | xargs -0 ruff format --config ruff.toml --check; ruff check --config ruff.toml tests/unit/test_hold_playbook.py; git ls-files -z "*.md" | xargs -0 prettier --check
66 files already formatted
All checks passed!
Checking formatting...
All matched files use Prettier code style!
[exit 0]
````

## 8. The vocabulary check against the real records (read-only, informative)

No test reads the real `.orchestration/learning/` tree (orchestrator note). The orchestrator runs this command at acceptance. Here it ran once, read-only, against the main checkout's seeded class file and records, as a smoke run of the completed script.

````console
$ git -C "$MAIN" status --short -- .orchestration/learning/classes.yaml; /bin/ls "$MAIN"/.orchestration/learning/mistakes/M-*.md | wc -l | tr -d " "; bash scripts/orchestrator/hold-playbook.sh --check-vocabulary "$MAIN/.orchestration/learning/classes.yaml" "$MAIN/.orchestration/learning/mistakes"
?? .orchestration/learning/classes.yaml
80
hold-playbook: $MAIN/.orchestration/learning/classes.yaml holds the 97 classes of 80 mistake records
[exit 0]
````

