---
task_id: dotfiles-T133-result-precheck-a04
round: 1
code_head: 9f6ec7c95b271c8121fd25e5a42b34d4795a7351
merge_base: 740772efb9d7928e810a7d799f2bd32a88d9b8ff
---

# Validation

Every block is the command's own output, run in the seat's sandbox (sandbox.md), and names its tested revision. "Exact id" means `uv run python -m unittest <module>.<Class>.<name>`; no proof uses `-k`.

## Task copy and the reset bookkeeping

```
$ shasum -a 256 .orchestration/dotfiles-T133-result-precheck-a04/task.md
e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700  .orchestration/dotfiles-T133-result-precheck-a04/task.md
$ git show --stat --format=%H a495ec55
a495ec55e39da1a42139e4b65f6b080f1340a66f

 .../dotfiles-T133-result-precheck-a03/task.md      | 190 ----------------
 .../dotfiles-T133-result-precheck-a04/task.md      | 244 +++++++++++++++++++++
 2 files changed, 244 insertions(+), 190 deletions(-)
```

a495ec55 added the dispatched text (ce5f7d06…). bf1bce63 replaced it with amendment 1's text (e52afb63…), which is the copy above.

## Caps (`git diff --numstat` against the merge base, on the code head, outside `.orchestration/`)

```
13	0	.githooks/pre-commit
36	0	.githooks/pre-push
108	4	scripts/orchestrator/dispatch.sh
321	0	scripts/orchestrator/result-precheck.sh
5	2	tests/unit/test_orchestrator_tools.py
610	0	tests/unit/test_result_precheck.py
outside tests/ and .orchestration/: 482 (cap 500); under tests/: 617 (cap 640)
```

## Red: the eight hardening regressions against ddf262de (exact id, scratch worktree, removed)

```
production=ddf262dec0db404ffc4ba5e1095842f2f17c7e6d, test sources from the working tree of 7ccc8287:
  f2872b61834b791df39fbafd8536945c033941611b2b99797d2cb33617cab38f  tests/unit/test_result_precheck.py
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_fails_closed_when_masking_fails
exit=1
FAIL: test_precheck_fails_closed_when_masking_fails
AssertionError: Tuples differ: (1, True) != (1, False)
Ran 1 test in 4.662s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_refuses_symlinked_evidence
exit=1
FAIL: test_precheck_refuses_symlinked_evidence (link='precheck.json')
AssertionError: Tuples differ: (0, '{\n  "head": "b08a164606df96cce72a7c0[1115 chars], []) != (1, 'kept\n', [])
FAIL: test_precheck_refuses_symlinked_evidence (link='result.txt')
AssertionError: Tuples differ: (0, 'AGMSG-RESULT v1 task_id=dotfiles-T0-x[365 chars], []) != (1, 'kept\n', [])
FAIL: test_precheck_refuses_symlinked_evidence (link='precheck-unit-test.log')
AssertionError: Tuples differ: (0, 'kept\n', []) != (1, 'kept\n', [])
FAIL: test_precheck_refuses_symlinked_evidence (link='the task directory')
AssertionError: Tuples differ: (0, 'kept\n', [PosixPath('/private/tmp/cla[513 chars]g')]) != (1, 'kept\n', [])
Ran 1 test in 4.540s
FAILED (failures=4)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_ignores_messages_from_unregistered_identities
exit=1
FAIL: test_dispatch_ignores_messages_from_unregistered_identities
AssertionError: Tuples differ: (1, False, False) != (0, True, True)
Ran 1 test in 1.584s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_fixtures_isolate_home
exit=1
FAIL: test_precheck_fixtures_isolate_home
AssertionError: False is not true : /private/tmp/claude-501/tmpmw0ct7wq/sentinel-home
Ran 1 test in 0.760s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_blob_scan_rejects_paths_outside_scan_directory
exit=1
FAIL: test_blob_scan_rejects_paths_outside_scan_directory (path='../../victim')
AssertionError: Tuples differ: (True, '') != (True, 'kept\n')
FAIL: test_blob_scan_rejects_paths_outside_scan_directory (path='a/../../../victim')
AssertionError: Tuples differ: (True, '') != (True, 'kept\n')
FAIL: test_blob_scan_rejects_paths_outside_scan_directory
AssertionError: Tuples differ: (0, False) != (2, False)
Ran 1 test in 1.540s
FAILED (failures=3)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_masks_logs_when_proof_worktree_creation_fails
exit=1
FAIL: test_precheck_masks_logs_when_proof_worktree_creation_fails (masker_fails=False)
AssertionError: Tuples differ: (True, True, [True, True, True]) != (True, False, [False, False, True])
FAIL: test_precheck_masks_logs_when_proof_worktree_creation_fails (masker_fails=True)
AssertionError: Tuples differ: (True, True, [True, True, True]) != (True, False, [False, False, True])
Ran 1 test in 4.629s
FAILED (failures=2)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_binds_precheck_to_code_head_across_update_branch
exit=1
FAIL: test_dispatch_binds_precheck_to_code_head_across_update_branch
AssertionError: Tuples differ: (1, False) != (0, True)
Ran 1 test in 1.740s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings
exit=1
FAIL: test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings (task_sha256='b13ec3104320b0387f67791d4f660e922d3ed70f3ce7de9ba5ce9e0ba72e1119')
AssertionError: Tuples differ: (0, False, '') != (0, True, 'x')
FAIL: test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings (task_sha256='0000000000000000000000000000000000000000000000000000000000000000')
AssertionError: Tuples differ: (1, False, '') != (1, True, 'x')
FAIL: test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings
AssertionError: "'--premises-sha', 'b13ec3104320b0387f67791d4f660e922d3ed70f3ce7de9ba5ce9e0ba72e1119'" not found in "['--root', '/private/tmp/claude-501/tmp6z_f5j75/repo', '/private/tmp/claude-501/tmp6z_f5j75/repo/.orche
Ran 1 test in 1.527s
FAILED (failures=3)
removed=0
```

## Red: the correction round's cases against bf1bce63, the reviewed head

```
production=bf1bce63bead0df3fcdd6c348cc44ea425f49dc4, test sources from the working tree of 7ccc8287:
  f2872b61834b791df39fbafd8536945c033941611b2b99797d2cb33617cab38f  tests/unit/test_result_precheck.py
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_binds_precheck_to_code_head_across_update_branch
exit=1
FAIL: test_dispatch_binds_precheck_to_code_head_across_update_branch (line='AGMSG-RESULT v1 task_id=t status=ready_for_review head=2cef0bd9387d9130dbaf09f45904b8a5ceb68f7c precheck_head=ab4091e074ecf77dcc80344bc925960b0b
AssertionError: Tuples differ: (0, True) != (1, False)
FAIL: test_dispatch_binds_precheck_to_code_head_across_update_branch (line='AGMSG-RESULT v1 task_id=t status=ready_for_review head=27cca53c2225fc4de2dae6ef6c68d29e98569839 precheck_head=ab4091e074ecf77dcc80344bc925960b0b
AssertionError: Tuples differ: (0, True) != (1, False)
Ran 1 test in 8.060s
FAILED (failures=2)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_precheck_masks_logs_when_proof_worktree_creation_fails
exit=1
FAIL: test_precheck_masks_logs_when_proof_worktree_creation_fails (masker_fails=False)
AssertionError: Tuples differ: (True, False, [True, True, True]) != (True, False, [False, False, True])
FAIL: test_precheck_masks_logs_when_proof_worktree_creation_fails (masker_fails=True)
AssertionError: Tuples differ: (True, False, [True, True, True]) != (True, False, [False, False, True])
Ran 1 test in 4.095s
FAILED (failures=2)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_blob_scan_rejects_paths_outside_scan_directory
exit=1
FAIL: test_blob_scan_rejects_paths_outside_scan_directory
AssertionError: Tuples differ: (0, False) != (2, False)
Ran 1 test in 2.808s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_ignores_messages_from_unregistered_identities
exit=1
FAIL: test_dispatch_ignores_messages_from_unregistered_identities
AssertionError: Tuples differ: (1, False, False) != (0, True, True)
Ran 1 test in 1.395s
FAILED (failures=1)
removed=0
```

## Red: the retained regressions against their historical heads

a03's four item 5 to 7 tests, against 4ed1b27a:

```
production=4ed1b27a666ba939db76051243143a7d7ed2aaa5, test sources from the working tree of 7ccc8287:
  f2872b61834b791df39fbafd8536945c033941611b2b99797d2cb33617cab38f  tests/unit/test_result_precheck.py
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding
exit=1
FAIL: test_pre_push_scans_each_blob_on_its_own_and_keeps_json_decoding
AssertionError: 0 != 1 : To /private/tmp/claude-501/tmpjyjfc19i/origin.git
Ran 1 test in 9.084s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_fails_closed_on_an_undecodable_blob
exit=1
FAIL: test_pre_push_fails_closed_on_an_undecodable_blob
AssertionError: 0 != 1 : To /private/tmp/claude-501/tmpdalem3h3/origin.git
Ran 1 test in 3.727s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise
exit=1
FAIL: test_dispatch_acceptance_check_requires_a_result_newer_than_the_latest_revise
AssertionError: Tuples differ: (0, True) != (1, False)
Ran 1 test in 0.941s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_reports_home_path_rewrites_only_under_orchestration
exit=1
FAIL: test_pre_push_reports_home_path_rewrites_only_under_orchestration
AssertionError: 1 != 0
Ran 1 test in 3.977s
FAILED (failures=1)
removed=0
```

The three revise-1 tests of the review of 9cd5514a:

```
production=9cd5514a790f6993136f5e74aaf3f3afa31b23d8, test sources from the working tree of 7ccc8287:
  f2872b61834b791df39fbafd8536945c033941611b2b99797d2cb33617cab38f  tests/unit/test_result_precheck.py
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_pre_push_scans_each_blob_on_its_own_boundary
exit=1
FAIL: test_pre_push_scans_each_blob_on_its_own_boundary
AssertionError: 0 != 1 : To /private/tmp/claude-501/tmpwdu0ac55/origin.git
Ran 1 test in 4.395s
FAILED (failures=1)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan
exit=1
FAIL: test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (encoding='utf-16')
AssertionError: 0 != 1 : secrets: 0 match(es)
FAIL: test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (encoding='utf-16-le')
AssertionError: 0 != 1 : secrets: 0 match(es)
FAIL: test_result_precheck_decodes_or_refuses_utf16_before_the_secret_scan (encoding='utf-16-be')
AssertionError: 0 != 1 : secrets: 0 match(es)
Ran 1 test in 4.447s
FAILED (failures=3)
$ uv run python -m unittest tests.unit.test_result_precheck.ResultPrecheckTest.test_previous_head_proof_requires_an_executed_failing_test
exit=1
FAIL: test_previous_head_proof_requires_an_executed_failing_test (name='test_always')
AssertionError: 0 != 1 : result-precheck: unit-test exit 0
FAIL: test_previous_head_proof_requires_an_executed_failing_test (name='test_helper')
AssertionError: 0 != 1 : result-precheck: unit-test exit 0
Ran 1 test in 4.887s
FAILED (failures=2)
removed=0
```

a03's revise-1 regressions keep their red evidence against bccb2dea in `.orchestration/dotfiles-T133-result-precheck-a03/validation.md`. All of them are green on the code head; the final proof below runs both modules.

## Shell checks and `make render-check` (9f6ec7c9)

```
$ shellcheck -x scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh
exit=0
$ shfmt -d -i 4 -sr scripts/orchestrator/result-precheck.sh .githooks/pre-commit .githooks/pre-push scripts/orchestrator/dispatch.sh
exit=0
$ make render-check
uv run --offline --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
exit=0
```

## `make format`: 9f6ec7c9, and the merge base 740772ef

```
$ make format   (9f6ec7c9)
make: *** [format] Error 1
shfmt --diff files: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh, .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh, home/dot_claude/hooks/executable_project-map-reload.sh, tests/install/macos/common/brew.bats
$ make format   (a detached scratch worktree of 740772ef)
make: *** [format] Error 1
shfmt --diff files: .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/pr-cost.sh, .orchestration/tasks/dotfiles-T128-chain-github-scripts-a01-input/resolve-threads.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-advisory.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/local-review.sh, .orchestration/tasks/dotfiles-T128-chain-review-scripts-a01-input/sandbox-scan.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/boundary.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/ff-main.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-audit.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/orch-gate.sh, .orchestration/tasks/dotfiles-T128-orchestrator-tools-a01-input/t717-prep.sh, home/dot_claude/hooks/executable_project-map-reload.sh, tests/install/macos/common/brew.bats
identical: True
```

`make format` stops at its first command, `shfmt --diff .`, on the same twelve pre-existing files on both sides. CI's three formatting commands in their CI scopes, the precheck's `format` check, pass (below).

## The default precheck run (9f6ec7c9), then the comparison with a pristine merge base in the same sandbox

```
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a04
result-precheck: unit-test exit 2
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
precheck=ae9a75d5bd447798af3ba0cd82b52431210e6b05c689214569e227d57ab01022
exit=1
$ make unit-test   (a detached scratch worktree of 740772ef, removed)
Ran 1216 tests in 2218.423s
FAILED (failures=205, errors=112, skipped=2)
$ the unit-test log of the default run
Ran 1242 tests in 784.030s
FAILED (failures=205, errors=112, skipped=2)
failing names: 322 on 9f6ec7c9, 322 on 740772ef
only on 9f6ec7c9: ['FAIL: test_timeout_is_one_shared_budget (test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget)']
only on 740772ef: ['FAIL: test_session_start_attach_bounds_a_trickling_hook_payload (test_herdr_agents.HerdrAgentsTest.test_session_start_attach_bounds_a_trickling_hook_payload)']
$ uv run python -m unittest tests.unit.test_agmsg_dispatch.AgmsgDispatchTest.test_timeout_is_one_shared_budget   (9f6ec7c9, alone)
Ran 1 test in 2.590s
OK
```

The default run exits 1 on `unit-test` alone: render-check, format, shellcheck and secrets pass. Its 322 failing names are sandbox-denied operations and match the merge base's but for two timing tests. One fails only on the branch and passes alone; the other fails only on the base. Neither is in this task's modules or touched by it. CI's `make unit-test` decides the full suite.

## The final proof

```
$ scripts/orchestrator/result-precheck.sh dotfiles-T133-result-precheck-a04 --tests tests.unit.test_result_precheck tests.unit.test_orchestrator_tools --previous-head ddf262dec0db404ffc4ba5e1095842f2f17c7e6d --check tests/unit/test_result_precheck.py::<each of the eight revise.yaml selectors>
result-precheck: unit-test exit 0
result-precheck: render-check exit 0
result-precheck: format exit 0
result-precheck: shellcheck exit 0
result-precheck: secrets exit 0
result-precheck: tests/unit/test_result_precheck.py::test_precheck_fails_closed_when_masking_fails previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_precheck_refuses_symlinked_evidence previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_dispatch_ignores_messages_from_unregistered_identities previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_precheck_fixtures_isolate_home previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_blob_scan_rejects_paths_outside_scan_directory previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_precheck_masks_logs_when_proof_worktree_creation_fails previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_dispatch_binds_precheck_to_code_head_across_update_branch previous head exit 1, this head exit 0
result-precheck: tests/unit/test_result_precheck.py::test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings previous head exit 1, this head exit 0
precheck=2b921eb17de04c8232f83210a13a278b0147aba13b0a7aedd2d09363638db2cd
exit=0
$ the unit-test log's summary (both modules)
Ran 83 tests in 168.420s
OK
$ the record: head, code_head and tree, the checks, each selector's exact id, baseline, test counts and exits, then each previous-head summary
head 9f6ec7c95b271c8121fd25e5a42b34d4795a7351 code_head 9f6ec7c95b271c8121fd25e5a42b34d4795a7351 tree d7a9e10685c52a77d100f9acee440d605fac2602
unit-test True
render-check True
format True
shellcheck True
secrets True
local-review None
test_precheck_fails_closed_when_masking_fails ok=True id=test_precheck_fails_closed_when_masking_fails previous_head=ddf262dec0db tests=1/1 exits=1/0
test_precheck_refuses_symlinked_evidence ok=True id=test_precheck_refuses_symlinked_evidence previous_head=ddf262dec0db tests=1/1 exits=1/0
test_dispatch_ignores_messages_from_unregistered_identities ok=True id=test_dispatch_ignores_messages_from_unregistered_identities previous_head=ddf262dec0db tests=1/1 exits=1/0
test_precheck_fixtures_isolate_home ok=True id=test_precheck_fixtures_isolate_home previous_head=ddf262dec0db tests=1/1 exits=1/0
test_blob_scan_rejects_paths_outside_scan_directory ok=True id=test_blob_scan_rejects_paths_outside_scan_directory previous_head=ddf262dec0db tests=1/1 exits=1/0
test_precheck_masks_logs_when_proof_worktree_creation_fails ok=True id=test_precheck_masks_logs_when_proof_worktree_creation_fails previous_head=ddf262dec0db tests=1/1 exits=1/0
test_dispatch_binds_precheck_to_code_head_across_update_branch ok=True id=test_dispatch_binds_precheck_to_code_head_across_update_branch previous_head=ddf262dec0db tests=1/1 exits=1/0
test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings ok=True id=test_dispatch_passes_the_task_sha_to_c14_and_forwards_warnings previous_head=ddf262dec0db tests=1/1 exits=1/0
precheck-selector-1-previous.log: Ran 1 test in 2.818s FAILED (failures=1)
precheck-selector-2-previous.log: Ran 1 test in 3.263s FAILED (failures=4)
precheck-selector-3-previous.log: Ran 1 test in 0.691s FAILED (failures=1)
precheck-selector-4-previous.log: Ran 1 test in 0.571s FAILED (failures=1)
precheck-selector-5-previous.log: Ran 1 test in 1.100s FAILED (failures=3)
precheck-selector-6-previous.log: Ran 1 test in 2.666s FAILED (failures=2)
precheck-selector-7-previous.log: Ran 1 test in 1.465s FAILED (failures=1)
precheck-selector-8-previous.log: Ran 1 test in 0.871s FAILED (failures=3)
$ shasum -a 256 .orchestration/dotfiles-T133-result-precheck-a04/precheck.json
2b921eb17de04c8232f83210a13a278b0147aba13b0a7aedd2d09363638db2cd  .orchestration/dotfiles-T133-result-precheck-a04/precheck.json
$ cat .orchestration/dotfiles-T133-result-precheck-a04/result.txt
AGMSG-RESULT v1 task_id=dotfiles-T133-result-precheck-a04 status=ready_for_review head=9f6ec7c95b271c8121fd25e5a42b34d4795a7351 precheck_head=9f6ec7c95b271c8121fd25e5a42b34d4795a7351 precheck=2b921eb17de04c8232f83210a13a278b0147aba13b0a7aedd2d09363638db2cd task_copy=e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700 report=.orchestration/dotfiles-T133-result-precheck-a04/report.md validation=.orchestration/dotfiles-T133-result-precheck-a04/validation.md sandbox=.orchestration/dotfiles-T133-result-precheck-a04/sandbox.md learning=.orchestration/dotfiles-T133-result-precheck-a04/learning.md
```

## CompactionDB memory

```
d0df4572-a49b-4385-97cf-79e43f7ee164
exit=0
```
