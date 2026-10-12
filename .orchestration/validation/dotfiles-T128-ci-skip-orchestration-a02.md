# Validation: dotfiles-T128-ci-skip-orchestration-a02

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This main-checkout copy covers `a35a751e`, §7 the final head `fca44b4c`, §8 and §9 Amendment 1 and its head `a8c2bed9` (design INV-8).

## 1. Task file

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
2c3a5ee2439a4c8e0aa16e0013e9b8acfcbb82fc330b259f7748f34938d5d9bc
```

## 2. Checks at `a35a751e` (task validation: the YAML parse, the module; plus formatting and the security pins)

```
$ git log --oneline -3; git show --stat --format= a35a751e
a35a751e test(ci): the workflow reader fails closed on any key form it does not parse
406ca746 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a02
dc4e6c37 fix(ci): the unit-test decision lists both sides of a rename; the workflow reader sees quoted keys
 tests/unit/test_workflow_orchestration_skip.py | 109 ++++++++++++++++---------
 1 file changed, 70 insertions(+), 39 deletions(-)
$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3; ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py
Ran 21 tests in 4.718s

OK
1 file already formatted
All checks passed!
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml .github/workflows/agent-assets.yml
.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
.github/workflows/test.yaml ['test']
.github/workflows/agent-assets.yml ['validate']
```

## 3. The unsupported forms (`scratchpad/mutate-a5-a02.sh` at `a35a751e`, a `git archive HEAD` copy)

Each row inserts one form into a workflow. "YAML reads" is GitHub's view of it, from PyYAML on the mutated file: every form hides a real `if` or `continue-on-error`. The next lines run `RequiredContextsTest`, `DecisionStepTest` and `DecisionTest` (13 tests) and count the summary and `ValueError` lines. `errors=N` counts failing subTests, not tests. The task's four forms come first; the two positional rows (a shifted job body, a shifted step item) were found while checking the reader.

```
== unsupported form: spaced-job-key (remote.yaml): if : false
   YAML reads: False
   1 FAILED (errors=12)
   1 Ran 13 tests in 1.732s
  12 ValueError: unsupported key form inside jobs: '    if : false'
== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
   YAML reads: False
   1 FAILED (errors=12)
   1 Ran 13 tests in 2.220s
  12 ValueError: unsupported key form inside jobs: '    "\\x69f": false'
== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
   YAML reads: True
   1 FAILED (errors=9)
   1 Ran 13 tests in 2.040s
   9 ValueError: unsupported key form inside jobs: '        continue-on-error : true'
== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
   YAML reads: False
   1 FAILED (errors=3)
   1 Ran 13 tests in 3.463s
   3 ValueError: unsupported job body indentation inside jobs: '      if: false'
== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
   YAML reads: True
   1 FAILED (errors=12)
   1 Ran 13 tests in 1.583s
  12 ValueError: unsupported key form inside jobs: '      -   name: Decide whether the diff needs a bootstrap'
== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
   YAML reads: {'if': False}
   1 FAILED (errors=12)
   1 Ran 13 tests in 1.550s
  12 ValueError: unsupported key form inside jobs: '      - { if: false }'
== reader made lenient again (plain_key returns instead of raising) -> test_the_reader_fails_closed_on_unsupported_key_forms
FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='spaced job key')
AssertionError: ValueError not raised
FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='escaped job key')
== restored: OK
== reader without the job-body indentation check -> test_the_reader_fails_closed_on_unsupported_key_forms
FAIL: test_the_reader_fails_closed_on_unsupported_key_forms (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_reader_fails_closed_on_unsupported_key_forms) (form='shifted job body')
AssertionError: ValueError not raised
FAILED (failures=1)
```

The tests that still pass under each form (the same harness with `-v`). Each is either the reader test itself (it rebuilds its own forms), or a test that never reads the mutated job's keys through `jobs()`: the context-name check reads job names by regex, and the rest read the other workflow file.

```
== unsupported form: spaced-job-key (remote.yaml): if : false
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
== unsupported form: escaped-job-key (remote.yaml): "\x69f": false
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
== unsupported form: spaced-step-key (test.yaml): continue-on-error : true
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
test_both_bootstrap_jobs_decide_with_the_same_script ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
test_every_event_but_pull_request_bootstraps ... ok
== unsupported form: shifted-job-body (agent-assets.yml): if: false|runs-on: ubuntu-24.04
test_no_job_is_left_for_a_required_job_to_need ... ok
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_both_bootstrap_jobs_decide_with_the_same_script ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
test_every_heavy_step_carries_its_jobs_decision ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
test_every_event_but_pull_request_bootstraps ... ok
test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
== unsupported form: shifted-step-item (remote.yaml): -   name: Decide whether the diff needs a bootstrap|continue-on-error: true
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
== unsupported form: flow-mapping-step (remote.yaml): - { if: false }
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
== restored: OK
```

## 4. The earlier proofs against the new reader (`scratchpad/mutate-a5.sh` and `scratchpad/mutate-a5-r1.sh` at `a35a751e`)

```
$ awk '/^== broken rule/{if(n!="")print n, f; n=$4; f="no"} /^(FAIL|ERROR):/{f="fails"} END{print n, f}' mutate-a5.log mutate-a5-r1.log; grep -E 'DID NOT APPLY|restored' mutate-a5.log mutate-a5-r1.log
public-bootstrap-step-ungated fails
private-deploy-key-ungated fails
unit-test-step-ungated fails
needs-on-a-required-job fails
job-level-if-on-a-required-job fails
changes-job-back fails
decision-continue-on-error fails
decision-before-checkout-history fails
private-script-drift fails
non-pr-events-judged fails
renames-collapsed fails
classification-inverted fails
unit-test-decision-ignores-orchestration fails
required-leg-dropped fails
shallow-base-fetch-remote fails
shallow-base-fetch-test fails
unit-test-diff-detects-renames fails
quoted-job-level-if fails
quoted-continue-on-error-on-decide fails
== reader-sees-bare-keys-only: MUTATION DID NOT APPLY
== restored: OK
== restored: OK
```

`reader-sees-bare-keys-only` targeted the quoted-key regex that this commit removes; the lenient-reader row of §3 replaces it.

## 5. The full suite locally, this head against `origin/main` (`git archive origin/main` copy; failing ids from the `FAIL:`/`ERROR:` lines)

```
$ UV_OFFLINE=1 make unit-test   # at this head; the same discover in the origin/main copy; then comm on the sorted ids
base (origin/main b896d9bc): FAILED (failures=114, errors=103, skipped=2)  failing ids: 188
head (a35a751e, make unit-test): FAILED (failures=114, errors=103, skipped=2) (make exits 2)  failing ids: 188
only at head:
only at base:
this module under make unit-test:
test_a_main_tests_job_when_present_decides_in_itself ... ok
test_both_bootstrap_jobs_decide_with_the_same_script ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed ... ok
test_every_heavy_step_carries_its_jobs_decision ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff ... ok
test_every_event_but_pull_request_bootstraps ... ok
test_the_decision_survives_a_base_that_moved_after_the_checkout ... ok
test_the_unit_test_decision_ignores_renames ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff ... ok
test_no_job_is_left_for_a_required_job_to_need ... ok
test_no_required_contexts_job_has_a_job_level_if_or_needs ... ok
test_the_reader_fails_closed_on_unsupported_key_forms ... ok
test_the_required_contexts_are_the_workflows_jobs ... ok
```

The local failures are the sandbox's, as on a01 (test commits that inherit the global signing setting, `mktemp` outside the writable paths, no pty devices, no local `main` ref). They are identical on `origin/main`. CI's `Run Python unit tests` step is the verdict.

## 6. CompactionDB (main checkout, outside the sandbox through the permission gate)

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128-ci-skip-orchestration-a02 …'
c62781a9-a65b-4484-925c-383fddb9a114
```

## 7. Final head `fca44b4c` (main-checkout copy)

```
$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200472	
private-bootstrap (ubuntu-24.04, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200388	
private-bootstrap (ubuntu-24.04, server)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200263	
public-bootstrap (macos-14, client)	pass	6m51s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200408	
public-bootstrap (ubuntu-24.04, client)	pass	9m57s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200432	
public-bootstrap (ubuntu-24.04, server)	pass	6m46s	https://github.com/mryfmo/dotfiles/actions/runs/38122927319/job/114421200378	
test (macos-14, client)	pass	5m52s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199766	
test (ubuntu-24.04, client)	pass	8m0s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199949	
test (ubuntu-24.04, server)	pass	5m8s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199892	
test (ubuntu-26.04, client)	pass	8m22s	https://github.com/mryfmo/dotfiles/actions/runs/38122927273/job/114421199888	
validate	pass	51s	https://github.com/mryfmo/dotfiles/actions/runs/38122927329/job/114421200195	
$ bash scratchpad/bot-wait.sh 320 fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf 2026-10-11T07:53:53Z   # last poll
poll 5 07:56:08Z head fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf asked=no
reviews: 
comments: 
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:56:00.911325Z">2026-10-11T07:56:00.911325Z</relative-time> | `fca44b4` | New commits |
DONE
$ # final recheck right before the RESULT
2026-10-11T08:04:16Z
$ gh pr view 320 --json headRefOid,state,isDraft
fca44b4c25d4b20d0b029dc5d8dd16f9c37a7dbf	OPEN	false
$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/reviews --jq '.[]|select(.user.type=="Bot")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
5482144676	b3f88beb	2026-10-11T06:15:10Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
4240499289	b3f88beb	.github/workflows/remote.yaml	61
$ gh api repos/mryfmo/dotfiles/issues/comments/6105983720 --jq .body | grep -E 'Code Review|Security Review'
| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T07:56:00.911325Z">2026-10-11T07:56:00.911325Z</relative-time> | `fca44b4` | New commits |
| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
$ gh api repos/mryfmo/dotfiles/issues/320/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-11T07:56:03Z
```
## 8. Amendment 1: the task copy

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
$ git diff --stat HEAD -- .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
 .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```

## 9. Final head `a8c2bed9` (main-checkout copy, Amendment 1)

```
$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	0	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329188	
private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329081	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329196	
public-bootstrap (macos-14, client)	pass	8m7s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329125	
public-bootstrap (ubuntu-24.04, client)	pass	9m42s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329150	
public-bootstrap (ubuntu-24.04, server)	pass	7m17s	https://github.com/mryfmo/dotfiles/actions/runs/38129377997/job/114440329256	
test (macos-14, client)	pass	6m15s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329292	
test (ubuntu-24.04, client)	pass	7m49s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329219	
test (ubuntu-24.04, server)	pass	5m2s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329374	
test (ubuntu-26.04, client)	pass	8m13s	https://github.com/mryfmo/dotfiles/actions/runs/38129378007/job/114440329357	
validate	pass	1m36s	https://github.com/mryfmo/dotfiles/actions/runs/38129377998/job/114440328928	
$ bash scratchpad/bot-wait.sh 320 a8c2bed92559e2d9855f78154a4181363893c3f5 2026-10-11T09:43:15Z   # last poll
poll 4 09:44:58Z head a8c2bed92559e2d9855f78154a4181363893c3f5 asked=no
reviews: 
comments: 
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T09:44:38.538540Z">2026-10-11T09:44:38.538540Z</relative-time> | `a8c2bed` | New commits |
DONE
$ # final recheck right before the RESULT
2026-10-11T09:53:40Z
$ gh pr view 320 --json headRefOid,state,isDraft
a8c2bed92559e2d9855f78154a4181363893c3f5	OPEN	false
$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/reviews --jq '.[]|select(.user.type=="Bot")|[.id,.commit_id[0:8],.submitted_at]|@tsv'
5482144676	b3f88beb	2026-10-11T06:15:10Z
$ gh api --paginate repos/mryfmo/dotfiles/pulls/320/comments --jq '.[]|select(.in_reply_to_id == null and .user.type=="Bot")|[.id,.original_commit_id[0:8],.path,(.original_line|tostring)]|@tsv'
4240499289	b3f88beb	.github/workflows/remote.yaml	61
$ gh api repos/mryfmo/dotfiles/issues/comments/6105983720 --jq .body | grep -E 'Code Review|Security Review'
| 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T09:44:38.538540Z">2026-10-11T09:44:38.538540Z</relative-time> | `a8c2bed` | New commits |
| 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
$ gh api repos/mryfmo/dotfiles/issues/320/reactions --jq '.[]|[.user.login,.content,.created_at]|@tsv'
chatgpt-codex-connector[bot]	+1	2026-10-11T09:44:41Z
```
