# Validation: dotfiles-T128-ci-skip-orchestration-a01

Every block is the verbatim output of the command shown, run in `.claude/worktrees/worker-f` on `feat/ci-skip-orchestration` (PR #320). This branch copy covers heads through `e872f69f` (§1–§7 at `9fcd2b04`, §8 the Bot fix round); the main-checkout copy adds the final head (design INV-8).

## 1. Checks at `9fcd2b04` (task validation: the YAML parse, the module under `make unit-test`; plus formatting)

```
$ git log --oneline -4; git status --porcelain | wc -l
9fcd2b04 feat(ci): an .orchestration-only PR runs no bootstrap or test matrix
f7393ee1 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a01, Amendment 1
be935742 chore(orchestration): task file for dotfiles-T128-ci-skip-orchestration-a01
b896d9bc chore(orchestration): boundary commit 2026-10-11 (regime v3 design accepted) (#316)
       0
$ UV_OFFLINE=1 make unit-test 2>&1 | grep -E "test_workflow_orchestration_skip|^Ran|^OK|^FAILED" | sed -E "s/ \(tests[^)]*\)//"
test_a_main_tests_job_when_present_decides_in_itself (test_workflow_orchestration_skip.DecisionStepTest.test_a_main_tests_job_when_present_decides_in_itself) ... ok
test_both_bootstrap_jobs_decide_with_the_same_script (test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script) ... ok
test_each_deciding_job_decides_after_its_checkout_and_fails_closed (test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed) ... ok
test_every_heavy_step_carries_its_jobs_decision (test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) ... ok
test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff) ... ok
test_every_event_but_pull_request_bootstraps (test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) ... ok
test_the_unit_test_decision_skips_an_orchestration_only_diff (test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff) ... ok
test_no_job_is_left_for_a_required_job_to_need (test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need) ... ok
test_no_required_contexts_job_has_a_job_level_if_or_needs (test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs) ... ok
test_the_required_contexts_are_the_workflows_jobs (test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs) ... ok
Ran 935 tests in 407.246s
FAILED (failures=114, errors=103, skipped=2)
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml
.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
.github/workflows/test.yaml ['test']
$ ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py; prettier --check .github/workflows/remote.yaml .github/workflows/test.yaml
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ git diff --stat origin/main...HEAD; shasum -a 256 .orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
 .github/workflows/remote.yaml                      |  71 ++++-
 .github/workflows/test.yaml                        | 118 ++++-----
 .../task.md                                        |  73 ++++++
 tests/unit/test_workflow_orchestration_skip.py     | 285 +++++++++++++++++++++
 4 files changed, 478 insertions(+), 69 deletions(-)
8e9c23daf670ab73dc26603cfbc4001fd3bbbd560829a46fa3a163c21f6c76a7  .orchestration/dotfiles-T128-ci-skip-orchestration-a01/task.md
```

`tests.unit.test_workflow_security` passes at this head too: it is not among the failing modules of the full local run (§2). The full suite's local failures are the sandbox's, not this change's (§2); CI's `Run Python unit tests` step runs `make unit-test` and passed on all four legs (§5).

## 2. The full suite locally, this head against `origin/main` (`git archive origin/main` copy; failing ids from the `FAIL:`/`ERROR:` lines)

```
$ UV_OFFLINE=1 uv run python -m unittest discover -s tests/unit   # in each tree, then comm on the sorted ids
base (origin/main b896d9bc): FAILED (failures=114, errors=103, skipped=2)  failing ids:      188
head (9fcd2b04): FAILED (failures=114, errors=103, skipped=2)  failing ids:      188
only at head:
only at base:
failing modules:
  78 test_herdr_agents
  40 test_require_crit_review
  28 test_agent_stop_gate
  19 test_ua_symbol_coverage
   8 test_runtime_health
   5 test_gh_auth
   2 test_supply_chain_policy
   2 test_aws_cli_acquisition
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
   1 ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
   1 ERROR: model_profiles must define the express profile
   1 ERROR: model profile standard.claude.model must be a launcher-safe string
```

## 3. Removal proofs (`scratchpad/mutate-a5.sh` at `9fcd2b04`: each rule broken alone in a `git archive HEAD` copy, then its test run)

```
== broken rule: public-bootstrap-step-ungated (remote.yaml, diff lines: 1) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='public-bo
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in ''
FAILED (failures=1)
== broken rule: private-deploy-key-ungated (remote.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='private-b
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in "${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == '
FAILED (failures=1)
== broken rule: unit-test-step-ungated (test.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='test', st
AssertionError: "steps.decide.outputs.should_test == 'true'" not found in '${{ true }}'
FAILED (failures=1)
== broken rule: needs-on-a-required-job (remote.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'needs' unexpectedly found in {'needs': 'validate', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'env': '', 'steps': ''}
FAILED (failures=1)
== broken rule: job-level-if-on-a-required-job (test.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'if' unexpectedly found in {'if': '${{ always() }}', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'continue-on-error': "${{ matrix.os == 'ubuntu-26.04' }}", 'env'
FAILED (failures=1)
== broken rule: changes-job-back (test.yaml, diff lines: 5) -> RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need
FAIL: test_no_job_is_left_for_a_required_job_to_need (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need)
AssertionError: 'changes' unexpectedly found in {'changes': {'keys': {'runs-on': 'ubuntu-24.04', 'steps': ''}, 'steps': [{'run': 'true'}]}, 'test': {'keys': {'strategy': '', 'runs-
FAILED (failures=1)
== broken rule: decision-continue-on-error (remote.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'continue-on-error' unexpectedly found in {'name': 'Decide whether the diff needs a bootstrap', 'id': 'decide', 'continue-on-error': 'true', 'env': '', 'shell': 'ba
FAILED (failures=1)
== broken rule: decision-before-checkout-history (test.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'fetch-depth: 0' not found in "    # Run the same test suite on each target OS/system pair.\n    # We intentionally keep macOS as `client` only because this reposit
FAILED (failures=1)
== broken rule: private-script-drift (remote.yaml, diff lines: 2) -> DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script
FAIL: test_both_bootstrap_jobs_decide_with_the_same_script (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script)
AssertionError: 'set [728 chars]rep -qv \'^\\.orchestration/\' <<< "${changed}[114 chars]\n\n' != 'set [728 chars]rep -v -q \'^\\.orchestration/\' <<< "${change[116 chars]\n\n'
FAILED (failures=1)
== broken rule: non-pr-events-judged (remote.yaml, diff lines: 4) -> DecisionTest.test_every_event_but_pull_request_bootstraps
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='push')
AssertionError: bash: line 6: BASE_REF: unbound variable
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='schedule')
== broken rule: renames-collapsed (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAILED (failures=1)
== broken rule: classification-inverted (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=true\n' != 'should_run=false\n'
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
== broken rule: unit-test-decision-ignores-orchestration (test.yaml, diff lines: 3) -> DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff
FAIL: test_the_unit_test_decision_skips_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only
AssertionError: 'should_test=false\n' not found in 'diff_range=origin/main...c8e8527541576544c82f4aa19bfd28f95733a671\nshould_test=true\n'
FAILED (failures=1)
== broken rule: required-leg-dropped (remote.yaml, diff lines: 2) -> RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs
FAIL: test_the_required_contexts_are_the_workflows_jobs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs)
AssertionError: {'test (ubuntu-24.04, server)', 'public-b[141 chars]ate'} != frozenset({'test (ubuntu-24.04, server)',[191 chars]t)'})
FAILED (failures=1)
== restored: OK
```

## 4. Premises, re-run at this head

```
$ gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules[]|select(.type=="required_status_checks")|.parameters.required_status_checks[].context]|join("; ")'
validate; test (ubuntu-24.04, server); test (ubuntu-24.04, client); test (macos-14, client); public-bootstrap (ubuntu-24.04, server); public-bootstrap (ubuntu-24.04, client); public-bootstrap (macos-14, client)
$ gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith("public-bootstrap"))|[.name,.started_at,.completed_at]|@tsv'; gh api repos/mryfmo/dotfiles/pulls/316/commits --paginate --jq 'length'
public-bootstrap (macos-14, client)	2026-10-10T23:51:13Z	2026-10-10T23:58:20Z
public-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-11T00:00:07Z
public-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:09Z	2026-10-10T23:58:50Z
6
$ sed -n 1,12p .github/workflows/test.yaml   (this head)
name: Unit test

on:
  # Required checks must always report a final status for PRs into `main`.
  # Do not add workflow-level path or branch filters here: GitHub can leave
  # skipped required checks in a pending state and block merges.
  # Keep this workflow unconditional and decide inside jobs whether the full
  # test matrix is necessary for the current diff.
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

Both hold: the ruleset's seven contexts equal `REQUIRED_CONTEXTS`, and PR 316's legs ran 7–9 minutes on its sixth head.

## 5. CI at `9fcd2b04`

```
$ gh pr checks 320 --repo mryfmo/dotfiles --watch --interval 30   # final table; exit 0
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	3s	https://dashboard.gitguardian.com	
private-bootstrap (macos-14, client)	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144325	
private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144398	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144454	
public-bootstrap (macos-14, client)	pass	7m3s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144619	
public-bootstrap (ubuntu-24.04, client)	pass	10m10s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144233	
public-bootstrap (ubuntu-24.04, server)	pass	7m48s	https://github.com/mryfmo/dotfiles/actions/runs/38116087041/job/114401144511	
test (macos-14, client)	pass	6m40s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144677	
test (ubuntu-24.04, client)	pass	7m45s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144845	
test (ubuntu-24.04, server)	pass	4m24s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144852	
test (ubuntu-26.04, client)	pass	7m10s	https://github.com/mryfmo/dotfiles/actions/runs/38116087096/job/114401144840	
validate	pass	53s	https://github.com/mryfmo/dotfiles/actions/runs/38116087042/job/114401144188	
$ for j in 114401144511 114401144454 114401144852; do echo "== job $j"; gh api repos/mryfmo/dotfiles/actions/jobs/$j --jq '.name, (.steps[]|[.number,.name,.conclusion]|@tsv)'; done; gh api repos/mryfmo/dotfiles/commits/c264c7d1/check-runs --paginate --jq '.check_runs[]|select(.name|startswith("private-bootstrap"))|[.name,.started_at,.completed_at]|@tsv'
== job 114401144511
public-bootstrap (ubuntu-24.04, server)
1	Set up job	success
2	Configure isolated HOME	success
3	Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
4	Decide whether the diff needs a bootstrap	success
5	Skip the bootstrap for an .orchestration-only diff	skipped
6	Bootstrap the checked-out public source	success
12	Post Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
13	Complete job	success
== job 114401144454
private-bootstrap (ubuntu-24.04, server)
1	Set up job	success
2	Configure isolated HOME	success
3	Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
4	Decide whether the diff needs a bootstrap	success
5	Skip the bootstrap for an .orchestration-only diff	skipped
6	Explain skipped private bootstrap	success
7	Set up the private deploy key	skipped
8	Bootstrap with private restoration	skipped
16	Post Run actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1	success
17	Complete job	success
== job 114401144852
test (ubuntu-24.04, server)
1	Set up job	success
2	Configure Git defaults	success
3	Checkout repository	success
4	Decide whether the diff needs the unit tests	success
5	Skip full unit test run for unrelated changes	skipped
6	Install tools	success
7	Prepare statusline tool config	success
8	Setup mise for statusline smoke	success
9	Install statusline tools	success
10	Smoke-test statusline tools without network	success
11	Run `shfmt`	success
12	Check Python and Markdown formatting	success
13	Run `ShellCheck`	success
14	Setup uv	success
15	Run Python unit tests	success
16	Prepare public dotfiles fixture	success
17	Run unit test	success
18	Setup for Codecov	success
19	Upload coverage to Codecov	success
37	Post Setup uv	success
38	Post Checkout repository	success
39	Complete job	success
private-bootstrap (ubuntu-24.04, client)	2026-10-10T23:51:09Z	2026-10-10T23:51:21Z
private-bootstrap (ubuntu-24.04, server)	2026-10-10T23:51:10Z	2026-10-10T23:51:21Z
private-bootstrap (macos-14, client)	2026-10-10T23:51:12Z	2026-10-10T23:51:24Z
```

On this mixed diff every decision step succeeded and the heavy steps ran. `private-bootstrap`'s two deploy-key steps were skipped by their existing secret gate (`Explain skipped private bootstrap` ran), as on PR 316, whose private legs also took about 12 seconds.

## 6. CompactionDB

```
$ cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T128 plan 006 A5 …'
a48481dc-7c94-40a9-9300-b01cafb77a48
```

## 7. Bot round 1 on `9fcd2b04`

```
$ # Bot wait on 9fcd2b04 (Worker Playbook step 15 loop), last poll
poll 5 05:52:41Z head 9fcd2b0482bd9c3c27e39b687e3503271f49a154 asked=no
reviews: 
comments: 
code-review-completed: | 📝 **Code Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:52:35.399605Z">2026-10-11T05:52:35.399605Z</relative-time> | `9fcd2b0` | Draft marked ready |
+1: 
$ # wait for the connector security review row on 9fcd2b04, last poll
poll 7 05:55:53Z reactions=+1 reviews= comments=
  | 🔒 **Security Review** | ✅ **Completed** <relative-time datetime="2026-10-11T05:55:43.193970Z">2026-10-11T05:55:43.193970Z</relative-time> | `9fcd2b0` | Draft marked ready |
DONE
```

No review object and no comment: the connector's own rows record both reviews of this head as completed, and it reacts 👍 "once all reviews finish with no findings" (`reactions=+1` above, its 👀 gone). A 👍 alone is not evidence of a review (Worker Playbook step 15); here the summary rows are. No fix round ran.

## 8. Bot fix round 1 at `e872f69f` (thread 4240499289)

```
$ bash scratchpad/repro-shallow.sh   # main moves after the checkout; the base fetched shallow, then in full
== fetch --depth=1
fatal: origin/main...<head>: no merge base
rc=128 shallow=written
== fetch in full
.orchestration/y.md
rc=0 shallow=none
$ git log --oneline -1; git show --stat --format= HEAD
e872f69f fix(ci): fetch the PR base in full so a moved base keeps its merge base
 .github/workflows/remote.yaml                  |  8 ++++++--
 .github/workflows/test.yaml                    |  4 +++-
 tests/unit/test_workflow_orchestration_skip.py | 24 ++++++++++++++++++++++++
 3 files changed, 33 insertions(+), 3 deletions(-)
$ grep -nE "git fetch" .github/workflows/remote.yaml .github/workflows/test.yaml
.github/workflows/remote.yaml:63:          git fetch --no-tags origin "${BASE_REF}"
.github/workflows/remote.yaml:161:          git fetch --no-tags origin "${BASE_REF}"
.github/workflows/test.yaml:74:            git fetch --no-tags origin "${BASE_REF}"
$ UV_OFFLINE=1 uv run python -m unittest tests.unit.test_workflow_orchestration_skip tests.unit.test_workflow_security 2>&1 | tail -3
Ran 19 tests in 4.148s

OK
$ ruff format --config ruff.toml --check tests/unit/test_workflow_orchestration_skip.py; ruff check --config ruff.toml tests/unit/test_workflow_orchestration_skip.py; prettier --check .github/workflows/remote.yaml .github/workflows/test.yaml 2>&1 | tail -1
1 file already formatted
All checks passed!
All matched files use Prettier code style!
$ UV_OFFLINE=1 uv run --no-project --with pyyaml python -I -c "import sys, yaml; [print(p, sorted(yaml.safe_load(open(p))[\"jobs\"])) for p in sys.argv[1:]]" .github/workflows/remote.yaml .github/workflows/test.yaml
.github/workflows/remote.yaml ['private-bootstrap', 'public-bootstrap']
.github/workflows/test.yaml ['test']
```

Removal proofs at `e872f69f` (`scratchpad/mutate-a5.sh` with two new rules, `--depth=1` put back in each file; output cut to three lines per rule, so a rule with several failing subtests shows its `FAIL:` lines without the summary):

```
== broken rule: public-bootstrap-step-ungated (remote.yaml, diff lines: 1) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='public-bo
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in ''
FAILED (failures=1)
== broken rule: private-deploy-key-ungated (remote.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='private-b
AssertionError: "steps.decide.outputs.should_run == 'true'" not found in "${{ !contains(github.actor, '[bot]') && env.HAS_EMAIL_ADDRESS == 'true' && env.HAS_PRIVATE_DEPLOY_KEY == '
FAILED (failures=1)
== broken rule: unit-test-step-ungated (test.yaml, diff lines: 2) -> DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision
FAIL: test_every_heavy_step_carries_its_jobs_decision (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_every_heavy_step_carries_its_jobs_decision) (job='test', st
AssertionError: "steps.decide.outputs.should_test == 'true'" not found in '${{ true }}'
FAILED (failures=1)
== broken rule: needs-on-a-required-job (remote.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'needs' unexpectedly found in {'needs': 'validate', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'env': '', 'steps': ''}
FAILED (failures=1)
== broken rule: job-level-if-on-a-required-job (test.yaml, diff lines: 1) -> RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_or_needs
FAIL: test_no_required_contexts_job_has_a_job_level_if_or_needs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_required_contexts_job_has_a_job_level_if_o
AssertionError: 'if' unexpectedly found in {'if': '${{ always() }}', 'strategy': '', 'runs-on': '${{ matrix.os }}', 'continue-on-error': "${{ matrix.os == 'ubuntu-26.04' }}", 'env'
FAILED (failures=1)
== broken rule: changes-job-back (test.yaml, diff lines: 5) -> RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need
FAIL: test_no_job_is_left_for_a_required_job_to_need (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_no_job_is_left_for_a_required_job_to_need)
AssertionError: 'changes' unexpectedly found in {'changes': {'keys': {'runs-on': 'ubuntu-24.04', 'steps': ''}, 'steps': [{'run': 'true'}]}, 'test': {'keys': {'strategy': '', 'runs-
FAILED (failures=1)
== broken rule: decision-continue-on-error (remote.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'continue-on-error' unexpectedly found in {'name': 'Decide whether the diff needs a bootstrap', 'id': 'decide', 'continue-on-error': 'true', 'env': '', 'shell': 'ba
FAILED (failures=1)
== broken rule: decision-before-checkout-history (test.yaml, diff lines: 1) -> DecisionStepTest.test_each_deciding_job_decides_after_its_checkout_and_fails_closed
FAIL: test_each_deciding_job_decides_after_its_checkout_and_fails_closed (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_each_deciding_job_decides_after_its_chec
AssertionError: 'fetch-depth: 0' not found in "    # Run the same test suite on each target OS/system pair.\n    # We intentionally keep macOS as `client` only because this reposit
FAILED (failures=1)
== broken rule: private-script-drift (remote.yaml, diff lines: 2) -> DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script
FAIL: test_both_bootstrap_jobs_decide_with_the_same_script (tests.unit.test_workflow_orchestration_skip.DecisionStepTest.test_both_bootstrap_jobs_decide_with_the_same_script)
AssertionError: 'set [851 chars]rep -qv \'^\\.orchestration/\' <<< "${changed}[114 chars]\n\n' != 'set [851 chars]rep -v -q \'^\\.orchestration/\' <<< "${change[116 chars]\n\n'
FAILED (failures=1)
== broken rule: non-pr-events-judged (remote.yaml, diff lines: 4) -> DecisionTest.test_every_event_but_pull_request_bootstraps
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='push')
AssertionError: bash: line 8: BASE_REF: unbound variable
FAIL: test_every_event_but_pull_request_bootstraps (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_every_event_but_pull_request_bootstraps) (event='schedule')
== broken rule: renames-collapsed (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=false\n' != 'should_run=true\n'
FAILED (failures=1)
== broken rule: classification-inverted (remote.yaml, diff lines: 2) -> DecisionTest.test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
AssertionError: 'should_run=true\n' != 'should_run=false\n'
FAIL: test_a_pull_request_skips_the_bootstrap_only_for_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_a_pull_request_skips_the_bootstrap_
== broken rule: unit-test-decision-ignores-orchestration (test.yaml, diff lines: 3) -> DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only_diff
FAIL: test_the_unit_test_decision_skips_an_orchestration_only_diff (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_unit_test_decision_skips_an_orchestration_only
AssertionError: 'should_test=false\n' not found in 'diff_range=origin/main...e105c5c0fcb30f9f61c57c9f1442ba590fa8c2ce\nshould_test=true\n'
FAILED (failures=1)
== broken rule: required-leg-dropped (remote.yaml, diff lines: 2) -> RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs
FAIL: test_the_required_contexts_are_the_workflows_jobs (tests.unit.test_workflow_orchestration_skip.RequiredContextsTest.test_the_required_contexts_are_the_workflows_jobs)
AssertionError: {'test (ubuntu-24.04, client)', 'test (ma[141 chars]ate'} != frozenset({'test (ubuntu-24.04, client)',[191 chars]te'})
FAILED (failures=1)
== broken rule: shallow-base-fetch-remote (remote.yaml, diff lines: 4) -> DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout
FAIL: test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_t
AssertionError: From /tmp/claude-501/tmph268b2tq/origin
FAILED (failures=1)
== broken rule: shallow-base-fetch-test (test.yaml, diff lines: 2) -> DecisionTest.test_the_decision_survives_a_base_that_moved_after_the_checkout
FAIL: test_the_decision_survives_a_base_that_moved_after_the_checkout (tests.unit.test_workflow_orchestration_skip.DecisionTest.test_the_decision_survives_a_base_that_moved_after_t
AssertionError: From /tmp/claude-501/tmp92ypcmg1/origin
FAILED (failures=1)
== restored: OK
```
