---
task_id: dotfiles-T133-dispositions-a01
round: 1
code_head: 5c28ccf65d195ad574ae339de33b8ef789818234
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
---

# Validation

Every block is the command's own output, run in the seat's sandbox on the code head above (the real run outside it, for gh).

## Task copy

```
$ shasum -a 256 .orchestration/dotfiles-T133-dispositions-a01/task.md
5ed78fc9a916decddb3fd668e3fb5494b7a01f219e02a68e4c93b7794feeae48  .orchestration/dotfiles-T133-dispositions-a01/task.md
```

## The two modules

```
$ git log --oneline -1
5c28ccf6 feat(orchestrator): dispositions.py proposes fixed:<commit> per review thread and verifies the three refutation forms; orch-gate.sh re-validates them before the gate (T133 dispositions a01)
$ uv run python -m unittest tests.unit.test_dispositions tests.unit.test_orch_gate_path -v
test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit ... ok
test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise ... ok
test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three ... ok
test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory ... ok
test_orch_gate_removes_the_private_bin_on_exit ... ok
test_orch_gate_revalidates_the_dispositions_before_the_gate ... ok
test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries ... ok
Ran 7 tests in 34.612s
OK
```

## Red: the gate case against origin/main's orch-gate.sh

A detached worktree of 5c28ccf6 with `scripts/orchestrator/orch-gate.sh` restored from `origin/main` (`git show origin/main:scripts/orchestrator/orch-gate.sh`), removed afterwards with `git worktree remove --force`:

```
$ uv run python -m unittest tests.unit.test_orch_gate_path.OrchGatePathTest.test_orch_gate_revalidates_the_dispositions_before_the_gate
FAIL: test_orch_gate_revalidates_the_dispositions_before_the_gate (tests.unit.test_orch_gate_path.OrchGatePathTest.test_orch_gate_revalidates_the_dispositions_before_the_gate)
AssertionError: 2 != 0 : 
Ran 1 test in 6.631s
FAILED (failures=1)
```

## format, shellcheck, shfmt and the caps

```
$ make format; the shfmt file list against de3b73cc's; ruff on the changed files
head=5c28ccf65d195ad574ae339de33b8ef789818234 origin/main=3e41e36abc949acd7e6b4859c1a22df9e665c8d4
make format exit=2
shfmt diff files: head 12, base de3b73cc 12
cmp format: identical file lists
3 files already formatted
ruff format --check (changed .py) exit=0
$ shfmt -i 4 -sr -d scripts/orchestrator/orch-gate.sh
exit=0
$ shellcheck -x scripts/orchestrator/orch-gate.sh
exit=0
$ git diff --numstat origin/main...HEAD
217	0	scripts/orchestrator/dispositions.py
13	1	scripts/orchestrator/orch-gate.sh
144	0	tests/unit/test_dispositions.py
27	3	tests/unit/test_orch_gate_path.py
outside tests/ and .orchestration/: 231 (cap 350); tests/: 174 (cap 450)
```

The twelve files `shfmt --diff` lists on both sides:

```
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh.orig
--- .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh.orig
--- .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh.orig
--- home/dot_claude/hooks/executable_project-map-reload.sh.orig
--- tests/install/macos/common/brew.bats.orig
```

## The real run on PR #409's sweep (outside the sandbox: gh resolves the thread commits)

```
$ uv run --no-project python -I scripts/orchestrator/dispositions.py 409 4fe243803971bd5ba8ab45f8ede5cfb4dd37f719 --feedback <main checkout>/.orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json
dispositions: https://github.com/mryfmo/dotfiles/pull/409#discussion_r4305896433 proposal fixed:99b07d2b1b6b2643d8dcdcf7cfb22c0ca89641be
dispositions: https://github.com/mryfmo/dotfiles/pull/409#discussion_r4305896435 proposal fixed:492e7e28f5db46e84aa680f14f978ca57e5485f1
exit=0
$ the proposals of the written JSON, beside the hand dispositions
https://github.com/mryfmo/dotfiles/pull/409#discussion_r4305896433 .github/workflows/remote.yaml:75 disposition=fixed:99b07d2b proposal=fixed:99b07d2b1b6b2643d8dcdcf7cfb22c0ca89641be
https://github.com/mryfmo/dotfiles/pull/409#discussion_r4305896435 scripts/orchestrator/ci-rerun.sh:90 disposition=fixed:99b07d2b proposal=fixed:492e7e28f5db46e84aa680f14f978ca57e5485f1
```

```
$ git log -1 --format='%h %s' 99b07d2b; git diff -U0 99b07d2b^ 99b07d2b -- scripts/orchestrator/ci-rerun.sh | grep '^@@'
99b07d2b fix(ci): the bootstrap gate runs on .chezmoiroot and vendor/; ci-rerun.sh reserves the run under a lock before rerunning it (T133 c
@@ -9,5 +9,8 @@
@@ -15,2 +18,2 @@
@@ -31,0 +35,8 @@ ledger="${root}/.orchestration/validation/ci-reruns.tsv"
@@ -86,2 +97 @@ done <<< "${failed}"
@@ -91,0 +102,4 @@ done
$ git log -1 --format='%h %s' 492e7e28; git diff -U0 492e7e28^ 492e7e28 -- scripts/orchestrator/ci-rerun.sh | grep '^@@'
492e7e28 fix(ci): ci-rerun.sh refuses a run not completed yet and reports a reservation it cannot create as an error; the flake file's heade
@@ -22 +22 @@
@@ -89,0 +90,6 @@ event="$(jq -r '.event // empty' <<< "${run}")" || exit 1
@@ -127,0 +134,4 @@ if ! mkdir "${reservation}" 2> /dev/null; then
```

## The legacy-evidence count

```
$ grep -l "evidence=" .orchestration/validation/*-pr-feedback.json | wc -l   # this branch
37
$ ls .orchestration/validation/*-pr-feedback.json | wc -l
131
$ the same two in the main checkout
47
141
```

## CompactionDB memory

```
$ uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T133 P1-10 part 1: dispositions.py proposes fixed:… refuses only under DISPOSITIONS_REQUIRE_REFUTATION=1.'
948b228f-b574-462e-99fc-c712602f8b98
exit=0
```

## CI round 1 on 74baf481: the four test jobs

Run 39133431120, job 117693061093 (`test (ubuntu-24.04, server)`, `gh run view --log-failed`); the other three test jobs failed the same way, validate and public-bootstrap passed.

```
FAIL: test_orch_gate_restores_the_review_worktree_when_setup_fails (test_orchestrator_tools.OrchestratorToolsTest.test_orch_gate_restores_the_review_worktree_when_setup_fails)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "~/work/dotfiles/dotfiles/tests/unit/test_orchestrator_tools.py", line 1621, in test_orch_gate_restores_the_review_worktree_when_setup_fails
    self.assertIsNone(self.call("gate-python"))
AssertionError: ['-I', '/tmp/tmp6ldsrudh/repo/scripts/orchestrator/dispositions.py', '9', '8c2fef6ff7279dd94903a7f4f1ec6d540de8c3df', '--feedback', '.orchestration/validation/t-a01-pr-feedback.json', '--out', '/dev/null'

----------------------------------------------------------------------
Ran 1211 tests in 280.833s

FAILED (failures=1)
make: *** [Makefile:186: unit-test] Error 1
##[error]Process completed with exit code 2.
```

## Bot round 1 on 74baf481 (review 5563269439, 13:55:07Z)

```
4307288053 scripts/orchestrator/dispositions.py:162 [P1] Include badged review-body findings in validation
4307288056 scripts/orchestrator/dispositions.py:51 [P2] Pass feedback paths as literal pathspecs
```

## The fix round: red, then green on dd567d77

The new cases against the code of 74baf481 (both Bot cases red):

```
$ uv run python -m unittest tests.unit.test_dispositions
ERROR: test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three (tests.unit.test_dispositions.DispositionsTest.test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three)
KeyError: 'refutation'
FAIL: test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise (tests.unit.test_dispositions.DispositionsTest.test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise
AssertionError: Lists differ: ['fix[63 chars], None, None, None] != ['fix[63 chars], None, 'fixed:8edd6d42424838ec04b4f1174de6d120919c4516', None]
Ran 3 tests in 1.903s
FAILED (failures=1, errors=1)
```

After the review-location fix alone, the literal-pathspec case is still red: the diff: evidence on the file `:b.py` is accepted (the ninth entry True), because git read the name as magic for b.py:

```
FAIL: test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three (tests.unit.test_dispositions.DispositionsTest.test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three)
AssertionError: Lists differ: [False, False, True, False, True, False, True, False, True, False] != [False, False, True, False, True, False, True, False, False, False]
Ran 3 tests in 2.944s
FAILED (failures=1)
```

```
$ git log --oneline -1
dd567d77 fix(orchestrator): the dispositions step runs right before the gate; badged review-body findings are threads located by their blob link; git reads thread paths as literal pathspecs (T133 disp
$ uv run python -m unittest tests.unit.test_dispositions tests.unit.test_orch_gate_path tests.unit.test_orchestrator_tools
Ran 64 tests in 53.279s
OK
$ shfmt -i 4 -sr -d scripts/orchestrator/orch-gate.sh; shellcheck -x scripts/orchestrator/orch-gate.sh
shfmt=0
shellcheck=0
$ git diff --numstat origin/main...HEAD
12	0	.orchestration/dotfiles-T133-dispositions-a01/learning.md
85	0	.orchestration/dotfiles-T133-dispositions-a01/report.md
30	0	.orchestration/dotfiles-T133-dispositions-a01/sandbox.md
103	0	.orchestration/dotfiles-T133-dispositions-a01/task.md
132	0	.orchestration/dotfiles-T133-dispositions-a01/validation.md
228	0	scripts/orchestrator/dispositions.py
14	1	scripts/orchestrator/orch-gate.sh
161	0	tests/unit/test_dispositions.py
32	3	tests/unit/test_orch_gate_path.py
```
