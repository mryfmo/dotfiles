---
task_id: dotfiles-T129-audit-inherit-replan-json-followup-a02
seat: claude-standard-dot-a008
code_head: 02b6eec1
test_commits: 495f51b3 f75c1137 02b6eec1
---

# Validation: dotfiles-T129-audit-inherit-replan-json-followup-a02

- Every command ran inside the sandbox through a generator that prints each command, its verbatim output and its exit status. A block's status is its last command's.
  - It ran from this worktree on `tools/audit-inherit-followup-a02` at the code head `02b6eec1`. The only later commit is the records commit that adds this directory.
- `MAIN` names the main checkout, `T` the task id, and `CODE` the code head. The scratch worktrees under `$TMPDIR` are removed after their block with `git worktree remove --force` (`git worktree prune` never ran).
- Red, in two steps:
  - §4 is the three owned rows, at `495f51b3`, whose scripts are the merge-base `3e41e36a`'s (origin/main when the branch was cut; main is now `740772ef`, #416, which touches none of these files).
  - §4b is the worker review's round-1 cases, at `f75c1137`, whose scripts are the first fix `9b59a3bc`'s.
  - §5 is green at the code head.
  - §5a is worker review round 2's surviving mutant (U+200B added to the text class). `02b6eec1` adds the test control that makes it fail.
- §6 and §6a: `test_require_crit_review` fails 136 subtests here and on origin/main alike. The cause is this seat's git environment, not the code:
  - the module's fixture commits fail because commit signing is on and the sandbox denies reading the signing key;
  - `init.defaultBranch` is unset.
  - §6b runs it at the code head with both set through git config environment variables: 98 of 98 pass.

## 1. Task file (sha256 5f33a507…) and task copy
```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
5f33a507b1ad6d6da09ed06f2a828dc1ae3fcdff39a4a6d000372ba04a684150  $MAIN/.orchestration/tasks/dotfiles-T129-audit-inherit-replan-json-followup-a02.md
5f33a507b1ad6d6da09ed06f2a828dc1ae3fcdff39a4a6d000372ba04a684150  .orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/task.md
byte-identical
[exit 0]
```
## 1a. The task-consistency check on the dispatched file
```console
$ uv run --offline --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T129-audit-inherit-replan-json-followup-a02.md: OK
[exit 0]
```
## 2. The owned rows as the record holds them
```console
$ awk "/^## Owned by $T/{f=1} f&&/^## Audit of/{exit} f" "$MAIN/.orchestration/acceptance/dotfiles-T129-audit-inherit-replan-json-followup-a01.md" | cut -c1-240
## Owned by dotfiles-T129-audit-inherit-replan-json-followup-a02 (advisory P2 of the final head; plan 020 step 1.2; rows id<TAB>class)

local:274a536:1	advisory-p2
local-finding: 274a536:1 not-applicable:advisory P2 owned by dotfiles-T129-audit-inherit-replan-json-followup-a02 (- [P2] Apply the gate's exact re-plan schema in the counters — scripts/regime-counters.sh:175-177); evidence=shasum -a 256 .o
local:274a536:2	advisory-p2
local-finding: 274a536:2 not-applicable:advisory P2 owned by dotfiles-T129-audit-inherit-replan-json-followup-a02 (- [P2] Re-audit instead of inheriting a blocked parent result — scripts/orchestrator/chain-integrate.sh:197-201); evidence=sh

- `audit:274a536:1	schema-drift` (P2 implementation, scripts/regime-counters.sh:175; = `local:274a536:1`)
- `audit:274a536:2	fail-open-on-error` (P2 implementation, scripts/orchestrator/chain-integrate.sh:197; = `local:274a536:2`)
- `audit:274a536:5	duplicate-count` (P3 implementation, scripts/orchestrator/ledger-check.py:35)
- records-form lessons for this owner: cap ranges in task texts are written as merge-base...code head, never `<base sha>...HEAD` (`audit:274a536:3`); a worker receipt's `reviewer:` field holds one allowlisted word (`audit:274a536:4`)

[exit 0]
```
## 3. Branch, base and commits
```console
$ git branch --show-current; git rev-parse HEAD origin/main; git log --oneline origin/main..HEAD
tools/audit-inherit-followup-a02
02b6eec1c5731096ade52614d35a28b970f976bb
740772efb9d7928e810a7d799f2bd32a88d9b8ff
02b6eec1 test(orchestrator): the present control also holds for format characters str.isspace() rejects, so a class widened past the 29 fails (T129 audit-inherit replan-json followup a02, worker review round 2)
cdfd3ee5 fix(orchestrator): the worker review's rows: a class slug ends at the end of the key, replans false is malformed, the headers name the gate's schema and the parent verdict (T129 audit-inherit replan-json followup a02)
f75c1137 test(orchestrator): the worker review's cases: a class key with a trailing newline, replans false, all 29 strip characters, a verdict that is not the last line, independent chain subtests (T129 audit-inherit replan-json followup a02)
9b59a3bc fix(orchestrator): the owned rows of the F1 lineage: the gate's re-plan schema in the counters, no inherited unusable audit, one count per audit id (T129 audit-inherit replan-json followup a02)
495f51b3 test(orchestrator): one refusal fixture per owned row of the F1 lineage's owner task (T129 audit-inherit replan-json followup a02)
[exit 0]
```
## 4. RED: the three regressions at the tests commit 495f51b3, whose scripts are the merge-base 3e41e36a's, in a scratch worktree
```console
$ git -C "$R" diff --quiet 3e41e36a -- scripts && echo "scripts identical to the merge-base 3e41e36a"; cd "$R" && uv run python -m unittest tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_an_audit_and_its_inherited_copy_once tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_a_parent_verdict_the_gate_accepts 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.[a-z_]+\\.[A-Za-z]+\\.[a-z_]+\\)//" | cut -c1-200
scripts identical to the merge-base 3e41e36a
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) [an extra key]
AssertionError: Lists differ: ['S1: class=bookkeeping count=3 re-plan=present source=record'] != ['S1: class=bookkeeping count=3 re-plan=missing source=record']
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) [a malformed entry under another class]
AssertionError: Lists differ: ['S1: class=bookkeeping count=3 re-plan=present source=record'] != ['S1: class=bookkeeping count=3 re-plan=missing source=record']
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) [a class that is no slug]
AssertionError: Lists differ: ['S1: class=bookkeeping count=3 re-plan=present source=record'] != ['S1: class=bookkeeping count=3 re-plan=missing source=record']
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) [a part only str.strip() empties]
AssertionError: Lists differ: ['S1: class=bookkeeping count=3 re-plan=present source=record'] != ['S1: class=bookkeeping count=3 re-plan=missing source=record']
FAIL: test_ledger_check_counts_an_audit_and_its_inherited_copy_once
AssertionError: Lists differ: ['led[15 chars]dings 1; gaps 1', 'GAP audit:abcdef0:1'] != ['led[15 chars]dings 2; gaps 2', 'GAP audit:abcdef0:1', 'GAP audit:abcdef0:1']
FAIL: test_inheritance_requires_a_parent_verdict_the_gate_accepts (summary='transcript\nVerdict: blocked\n')
AssertionError: 1 != 0
FAIL: test_inheritance_requires_a_parent_verdict_the_gate_accepts (summary='')
AssertionError: 2 != 0
FAIL: test_inheritance_requires_a_parent_verdict_the_gate_accepts (summary='no finding\nVerdict: incorrect\n')
AssertionError: 3 != 0
Ran 3 tests in 13.164s
FAILED (failures=8)
[exit 0]
```
## 4b. RED: the worker review's cases at the tests commit f75c1137, whose scripts are 9b59a3bc's, in a scratch worktree
```console
$ git -C "$R2" diff --quiet 9b59a3bc -- scripts && echo "scripts identical to 9b59a3bc"; cd "$R2" && uv run python -m unittest tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_a_parent_verdict_the_gate_accepts 2>&1 | /usr/bin/grep -E "^(FAIL|ERROR):|^AssertionError|^Ran|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.[a-z_]+\\.[A-Za-z]+\\.[a-z_]+\\)//" | cut -c1-200
scripts identical to 9b59a3bc
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) [a class key with a trailing newline]
AssertionError: Lists differ: ['S1: class=bookkeeping count=3 re-plan=present source=record'] != ['S1: class=bookkeeping count=3 re-plan=missing source=record']
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) [replans false]
AssertionError: 5 != 0 : jq: error (at <stdin>:1): Cannot index boolean with string ("bookkeeping")
Ran 2 tests in 15.803s
FAILED (failures=2)
[exit 0]
```
## 5. GREEN: the three regressions at HEAD
```console
$ git rev-parse --short=8 HEAD; uv run python -m unittest tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_an_audit_and_its_inherited_copy_once tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_a_parent_verdict_the_gate_accepts -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^(OK|FAILED)"
02b6eec1
test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) ... ok
test_ledger_check_counts_an_audit_and_its_inherited_copy_once (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_an_audit_and_its_inherited_copy_once) ... ok
test_inheritance_requires_a_parent_verdict_the_gate_accepts (tests.unit.test_chain_glue.ChainIntegrateTest.test_inheritance_requires_a_parent_verdict_the_gate_accepts) ... ok
Ran 3 tests in 13.434s
OK
[exit 0]
```
## 5a. The worker review round 2 mutant m13 (U+200B added to the text class) fails the S1 test at HEAD, in a scratch worktree
```console
$ cd "$Q" && sed -i "" "s/\\\\u3000\\]\")/\\\\u3000\\\\u200b]\")/" scripts/regime-counters.sh && git diff --numstat; uv run python -m unittest tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema 2>&1 | /usr/bin/grep -E "^FAIL:|^(OK|FAILED)" | sed -E "s/ \\(tests\\.unit\\.[a-z_]+\\.[A-Za-z]+\\.[a-z_]+\\)//"
1	1	scripts/regime-counters.sh
FAIL: test_s1_applies_the_gate_s_exact_replan_schema (tests.unit.test_regime_counters.RegimeCountersTest.test_s1_applies_the_gate_s_exact_replan_schema) (extra='\u200b')
FAILED (failures=1)
[exit 0]
```
## 6. The Check's unit modules at HEAD (and test_task_checkers, where ledger-check's tests live): every failure is test_require_crit_review's, the same 136 as on origin/main in this seat (§6a), and none with the seat's git environment fixed (§6b)
```console
$ uv run python -m unittest tests/unit/test_chain_glue.py tests/unit/test_require_crit_review.py tests/unit/test_regime_counters.py tests/unit/test_orchestrator_tools.py tests/unit/test_task_checkers.py > "$TMPDIR/f1-check.txt" 2>&1; echo "unittest exit $?"; /usr/bin/grep -E "^Ran|^(OK|FAILED)" "$TMPDIR/f1-check.txt"; /usr/bin/grep -oE "^(FAIL|ERROR): test[^ ]* \([a-z_.]+" "$TMPDIR/f1-check.txt" | sed -E "s/.*\(tests\.unit\.//; s/\..*//" | sort | uniq -c; /usr/bin/grep -m1 -A3 "^AssertionError" "$TMPDIR/f1-check.txt" | cut -c1-200
unittest exit 1
Ran 214 tests in 231.125s
FAILED (failures=136)
 136 test_require_crit_review
AssertionError: 1 != 0

======================================================================
FAIL: test_acceptance_record_accepts_a_dispatch_list (tests.unit.test_require_crit_review.ReviewGuardTest.test_acceptance_record_accepts_a_dispatch_list)
[exit 0]
```
## 6a. test_require_crit_review on a scratch worktree at origin/main, same sandbox
```console
$ cd "$M" && uv run python -m unittest tests/unit/test_require_crit_review.py 2>&1 | /usr/bin/grep -E "^Ran|^(OK|FAILED)"
Ran 98 tests in 52.422s
FAILED (failures=136)
[exit 0]
```
## 6b. test_require_crit_review at HEAD with commit signing off and init.defaultBranch=main (the sandbox denies the signing key read, and the module's fixture repos rely on a main default branch)
```console
$ GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false GIT_CONFIG_KEY_1=init.defaultBranch GIT_CONFIG_VALUE_1=main uv run python -m unittest tests/unit/test_require_crit_review.py 2>&1 | /usr/bin/grep -E "^Ran|^(OK|FAILED)"
Ran 98 tests in 111.410s
OK
[exit 0]
```
## 7. shellcheck -x and shfmt -d on the two shell scripts; ruff on ledger-check.py and the three tests
```console
$ shellcheck -x scripts/regime-counters.sh scripts/orchestrator/chain-integrate.sh && echo "shellcheck clean"; shfmt --indent 4 --space-redirects -d scripts/regime-counters.sh scripts/orchestrator/chain-integrate.sh && echo "shfmt clean"; ruff check --config ruff.toml scripts/orchestrator/ledger-check.py tests/unit/test_regime_counters.py tests/unit/test_chain_glue.py tests/unit/test_task_checkers.py; ruff format --config ruff.toml --check scripts/orchestrator/ledger-check.py tests/unit/test_regime_counters.py tests/unit/test_chain_glue.py tests/unit/test_task_checkers.py
shellcheck clean
shfmt clean
All checks passed!
4 files already formatted
[exit 0]
```
## 8. Caps over merge-base...code head (git diff --numstat), summed
```console
$ B=$(git merge-base origin/main "$CODE"); echo "merge-base ${B:0:8} code head $CODE"; git diff --numstat "$B...$CODE"; git diff --numstat "$B...$CODE" | awk -F "\t" "\$3 ~ /^\\.orchestration\\// {next} \$3 ~ /^tests\\// {t += \$1 + \$2; next} {o += \$1 + \$2} END {printf \"outside tests/ and .orchestration/: %d of 200\nunder tests/: %d of 1000\n\", o, t}"
merge-base 3e41e36a code head 02b6eec1
7	2	scripts/orchestrator/chain-integrate.sh
1	0	scripts/orchestrator/ledger-check.py
11	5	scripts/regime-counters.sh
31	0	tests/unit/test_chain_glue.py
26	0	tests/unit/test_regime_counters.py
12	0	tests/unit/test_task_checkers.py
outside tests/ and .orchestration/: 26 of 200
under tests/: 69 of 1000
[exit 0]
```
