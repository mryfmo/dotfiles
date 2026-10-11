# Validation: dotfiles-T128-ci-skip-orchestration-a02

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This branch copy covers `a35a751e`; the main-checkout copy adds the final head (design INV-8).

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

## 8. Amendment 1: the task copy

```
$ shasum -a 256 ~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a02.md .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | cut -c1-64
4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
4de54fdec5db667e940365703ee5e16cd1d91f52794c79c75b48aad7eb0a8763
$ git diff --stat HEAD -- .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md
 .orchestration/dotfiles-T128-ci-skip-orchestration-a02/task.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```
