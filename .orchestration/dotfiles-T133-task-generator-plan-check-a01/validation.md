---
task_id: dotfiles-T133-task-generator-plan-check-a01
round: 1
code_head: d7332ebb9cef85a440a0d7c6a0b8a35136ad0690
base: de3b73cc4f8874a30be6adc47a0f07575869d0df
---

# Validation

Every block below is the command's own output, run on the code head named above in the seat's sandbox (sandbox.md). The task files and plan files exist only untracked in the main checkout, so the checker and plan-check runs read it with `--root <main checkout>`.

## Task copy

```
$ shasum -a 256 .orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md
e08bb0afe8d508f5327b0e199108ee1b74efdb5d4a2004faed93b1ca4d1f0c68  .orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md
```

## The four modules

```
head=d7332ebb9cef85a440a0d7c6a0b8a35136ad0690 origin/main=de3b73cc4f8874a30be6adc47a0f07575869d0df merge-base=de3b73cc4f8874a30be6adc47a0f07575869d0df
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers -v
test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs (tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs) ... ok
test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (tests.unit.test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan) ... ok
test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged (tests.unit.test_task_consistency_c11_c15.TaskConsistencyC11C15Test.test_each_new_check_is_red_on_its_fixture_and_the_existing_checks_are_unchanged) ... 
test_ledger_check_counts_what_the_gate_counts (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_counts_what_the_gate_counts) ... ok
test_ledger_check_passes_a_complete_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_passes_a_complete_record) ... ok
test_ledger_check_reads_inherited_audit_ids_from_the_marker (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reads_inherited_audit_ids_from_the_marker) ... ok
test_ledger_check_reports_the_gaps_of_the_pre_fix_record (tests.unit.test_task_checkers.TaskCheckersTest.test_ledger_check_reports_the_gaps_of_the_pre_fix_record) ... ok
test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c4_names_an_entry_only_at_a_path_boundary) ... ok
test_task_consistency_check_c9_probes_the_landed_checker_path (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_c9_probes_the_landed_checker_path) ... ok
test_task_consistency_check_detects_the_ten_historical_files (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_detects_the_ten_historical_files) ... ok
test_task_consistency_check_passes_a_complete_task_file (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_passes_a_complete_task_file) ... ok
test_task_consistency_check_reaches_every_other_check (tests.unit.test_task_checkers.TaskCheckersTest.test_task_consistency_check_reaches_every_other_check) ... ok
Ran 12 tests in 11.194s
OK (skipped=1)
exit=0
```

## make unit-test and make format, this head against a pristine origin/main worktree

```
head make unit-test exit=2
head make format exit=2
7 files already formatted
ruff format --check (changed .py) exit=0
Checking formatting...
All matched files use Prettier code style!
prettier --check (changed .md) exit=0
base=de3b73cc4f8874a30be6adc47a0f07575869d0df
base make unit-test exit=2
base make format exit=2
removed=0
head: Ran 1198 tests in 588.079s FAILED (failures=194, errors=111, skipped=3) 
base: Ran 1195 tests in 576.698s FAILED (failures=194, errors=111, skipped=2) 
failing names: head 305, base 305
cmp unit: identical failing sets
in this task's modules: 0
shfmt diff files: head 12, base 12
cmp format: identical file lists
$ git diff --numstat origin/main...HEAD
111	0	.orchestration/dotfiles-T133-task-generator-plan-check-a01/task.md
196	0	scripts/orchestrator/plan-check.py
81	2	scripts/orchestrator/task-consistency-check.py
224	0	scripts/orchestrator/task-from-plan.py
101	0	tests/unit/test_plan_check.py
15	5	tests/unit/test_task_checkers.py
143	0	tests/unit/test_task_consistency_c11_c15.py
109	0	tests/unit/test_task_from_plan.py
outside tests/ and .orchestration/: 503 (cap 600); tests/: 373 (cap 700)
```

The twelve files `shfmt --diff` lists on both sides (`make format` stops at shfmt, so ruff and prettier ran on the changed files above):

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

## The two edits of tests/unit/test_task_checkers.py

```
$ git diff origin/main...HEAD -- tests/unit/test_task_checkers.py
diff --git a/tests/unit/test_task_checkers.py b/tests/unit/test_task_checkers.py
index f49a9ef9..73f09a51 100644
--- a/tests/unit/test_task_checkers.py
+++ b/tests/unit/test_task_checkers.py
@@ -79,10 +79,14 @@ class TaskCheckersTest(unittest.TestCase):
         for path, block in zip(files, blocks[2::2], strict=True):
             path.write_text(block)
         c2467, c467, c23467 = {"C2", "C4", "C6", "C7"}, {"C4", "C6", "C7"}, {"C2", "C3", "C4", "C6", "C7"}
-        expected = {"process-rules-a01": {"C2", "C6"}, "process-rules-a05": c467, "process-rules-a06": c467}
-        expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467)
-        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467)
+        expected = {
+            "process-rules-a01": {"C2", "C6"},
+            "process-rules-a05": c467 | {"C14"},
+            "process-rules-a06": c467 | {"C14"},
+        }
+        expected |= dict.fromkeys(["process-rules-a02", "process-rules-a03", "process-rules-a04"], c2467 | {"C14"})
+        expected |= dict.fromkeys(["regime-counters-a01", "ci-skip-orchestration-a01"], c2467 | {"C11", "C15"})
+        expected |= dict.fromkeys(["regime-counters-a02", "ci-skip-orchestration-a02"], c23467 | {"C11", "C15"})
         expected = {f"dotfiles-T128-{t}.md": ids for t, ids in expected.items()}
         self.assertEqual(expected, self.failing_checks(*files, root=ROOT))
 
@@ -186,7 +190,13 @@ class TaskCheckersTest(unittest.TestCase):
         for after in (".bak", "", " and its test", "/task.md", ") and more", '" and more', ", and more", "* and more"):
             with self.subTest(after=after):
                 path = self.task(
-                    uncovered=("scripts/foo.py",), rows=[{"control": f"the PR adds scripts/foo.py{after}"}]
+                    uncovered=("scripts/foo.py",),
+                    rows=[
+                        {
+                            "control": f"the PR adds scripts/foo.py{after}",
+                            "disposition": "residual: a compensating control",
+                        }
+                    ],
                 )
                 found = self.failing_checks(path, root=self.temp, code=1 if after == ".bak" else 0)[path.name]
                 self.assertEqual({"C4"} if after == ".bak" else set(), found)
```

The finding lines the extended checker prints on the ten historical files (stdout only, as the test reads them; `--root` this worktree):

```
dotfiles-T128-process-rules-a01.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a01/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
dotfiles-T128-process-rules-a02.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a02/**
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C4 allowed path has no threat_table row naming it: tests/unit/test_agmsg_orchestration_docs.py
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a03.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a03/**
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a04.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-process-rules-a04/**
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a05.md: FAIL
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C4 allowed path has no threat_table row naming it: tests/fixtures/regime/*.md
  C4 allowed path has no threat_table row naming it: .orchestration/dotfiles-T128-process-rules-a05/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-process-rules-a06.md: FAIL
  C4 allowed path has no threat_table row naming it: home/dot_agents/skills/agmsg-orchestration/SKILL.md
  C4 allowed path has no threat_table row naming it: .orchestration/dotfiles-T128-process-rules-a06/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C14 premise output differs from its rerun: ~/.agents/skills/agmsg/scripts/history.sh dotfiles-conforman
dotfiles-T128-regime-counters-a01.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-regime-counters-a01/**
  C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
  C4 allowed path has no threat_table row naming it: tests/unit/test_regime_counters.py
  C4 allowed path has no threat_table row naming it: tests/unit/test_check_regime_boundary.py
  C4 allowed path has no threat_table row naming it: tests/fixtures/regime-counters/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: every count comes from agmsg history or GitHub only; .orches
  C11 closed: payload is not tests/<path>::<identifier>: a record silences the report only through INV-6's anchor for
  C11 closed: payload is not tests/<path>::<identifier>: the script reads the whole team history through lib/storage.
  C11 closed: payload is not tests/<path>::<identifier>: revises = RESULTs for the task_id minus one, exactly INV-6's
  C11 closed: payload is not tests/<path>::<identifier>: review_comment items carrying a P0 or P1 badge, grouped by o
  C11 closed: payload is not tests/<path>::<identifier>: an accepted acceptance record silences a PR-less task only w
  C11 closed: payload is not tests/<path>::<identifier>: the seams are flags, scripts/check-regime-boundary.sh never 
  C11 out-of-scope: V2 (INV-6 counts audit findings from .orchestration/validati is not a task under .orchestration/tasks/
  C15 invariant INV-6 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main
dotfiles-T128-regime-counters-a02.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-regime-counters-a02/**
  C3 no threat_table row names dotfiles-T128-regime-counters-a01 task.md
  C3 no threat_table row names dotfiles-T128-regime-counters-a02 task.md
  C4 allowed path has no threat_table row naming it: scripts/check-regime-boundary.sh
  C4 allowed path has no threat_table row naming it: tests/unit/test_regime_counters.py
  C4 allowed path has no threat_table row naming it: tests/unit/test_check_regime_boundary.py
  C4 allowed path has no threat_table row naming it: tests/fixtures/regime-counters/**
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: every count comes from agmsg history or GitHub only; .orches
  C11 closed: payload is not tests/<path>::<identifier>: a record silences the report only through INV-6's anchor for
  C11 closed: payload is not tests/<path>::<identifier>: the accepting AGMSG-RESULT must carry task_id equal to the r
  C11 closed: payload is not tests/<path>::<identifier>: the script reads the whole team history through lib/storage.
  C11 closed: payload is not tests/<path>::<identifier>: revises = RESULTs for the task_id minus one, exactly INV-6's
  C11 closed: payload is not tests/<path>::<identifier>: review_comment items carrying a P0 or P1 badge, grouped by o
  C11 closed: payload is not tests/<path>::<identifier>: an accepted acceptance record silences a PR-less task only w
  C11 closed: payload is not tests/<path>::<identifier>: the seams are flags, scripts/check-regime-boundary.sh never 
  C11 out-of-scope: V2 (INV-6 counts audit findings from .orchestration/validati is not a task under .orchestration/tasks/
  C11 closed: payload is not tests/<path>::<identifier>: tests/fixtures/regime-counters/* hold only the rows and fiel
  C15 invariant INV-6 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main
dotfiles-T128-ci-skip-orchestration-a01.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-ci-skip-orchestration-a01/**
  C4 allowed path has no threat_table row naming it: .github/workflows/remote.yaml
  C4 allowed path has no threat_table row naming it: .github/workflows/test.yaml
  C4 allowed path has no threat_table row naming it: tests/unit/test_workflow_orchestration_skip.py
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round16.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: the classification is one git diff --name-only over the merg
  C11 closed: payload is not tests/<path>::<identifier>: GitHub reports a skipped job as Success even for a required 
  C11 closed: payload is not tests/<path>::<identifier>: an in-job decision step that fails fails the required contex
  C11 closed: payload is not tests/<path>::<identifier>: should_run is true for every event but pull_request; test as
  C15 invariant INV-2 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main
dotfiles-T128-ci-skip-orchestration-a02.md: FAIL
  C2 allowed_files lacks .orchestration/dotfiles-T128-ci-skip-orchestration-a02/**
  C3 no threat_table row names dotfiles-T128-ci-skip-orchestration-a01 task.md
  C3 no threat_table row names dotfiles-T128-ci-skip-orchestration-a02 task.md
  C4 allowed path has no threat_table row naming it: .github/workflows/remote.yaml
  C4 allowed path has no threat_table row naming it: .github/workflows/test.yaml
  C4 allowed path has no threat_table row naming it: tests/unit/test_workflow_orchestration_skip.py
  C6 design_review.receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round18.md is not the design's current receipt .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  C7 threat_table has no row named for: task metadata
  C7 threat_table has no row named for: metadata separators
  C7 threat_table has no row named for: in-process effects
  C7 threat_table has no row named for: workflow and interpreter or environment inputs
  C7 threat_table has no row named for: new or renamed scripts
  C7 threat_table has no row named for: orchestrator effect merge
  C7 threat_table has no row named for: orchestrator effect update-branch
  C7 threat_table has no row named for: orchestrator effect forced worker removal
  C11 closed: payload is not tests/<path>::<identifier>: the classification is one git diff --name-only over the merg
  C11 closed: payload is not tests/<path>::<identifier>: GitHub reports a skipped job as Success even for a required 
  C11 closed: payload is not tests/<path>::<identifier>: an in-job decision step that fails fails the required contex
  C11 closed: payload is not tests/<path>::<identifier>: the reader fails closed: inside jobs:, a job name, a job key
  C11 closed: payload is not tests/<path>::<identifier>: INV-2 requires the design on main before the implementing TA
  C11 closed: payload is not tests/<path>::<identifier>: should_run is true for every event but pull_request; test as
  C15 invariant INV-2 is not byte-equal to .orchestration/tasks/dotfiles-T128-regime-v3-a01.md on origin/main

```

## The checker on the sixteen T133 task files (stdout and stderr)

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <main checkout>/.orchestration/tasks/dotfiles-T133-*.md
dotfiles-T133-ci-efficiency-a01.md: C14 skipped network premise: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules
dotfiles-T133-ci-efficiency-a02.md: C14 skipped network premise: gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '[.rules
dotfiles-T133-permission-guard-gate-a01.md: C14 skipped network premise: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/
dotfiles-T133-permission-guard-gate-a01.md: C14 skipped network premise: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agen
dotfiles-T133-permission-guard-gate-a02.md: C14 skipped network premise: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/
dotfiles-T133-permission-guard-gate-a02.md: C14 skipped network premise: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agen
dotfiles-T133-verdict-audit-pool-a01.md: C14: tool absent uv: uv run --no-project python scripts/pr-feedback.py --help | /
dotfiles-T133-verdict-audit-pool-a02.md: C14: tool absent uv: uv run --no-project python scripts/pr-feedback.py --help | /
dotfiles-T133-worker-hooks-path-a01.md: C14: tool absent codex: codex exec --help | /usr/bin/grep -c -- '--config'
dotfiles-T133-ci-efficiency-a01.md: OK
dotfiles-T133-ci-efficiency-a02.md: OK
dotfiles-T133-ci-efficiency-followup-a01.md: OK
dotfiles-T133-permission-guard-gate-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c 'scope=permission' .orchestration/decisions
dotfiles-T133-permission-guard-gate-a02.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c 'scope=permission' .orchestration/decisions
dotfiles-T133-result-precheck-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -n '^RECORD_KEYS = ' scripts/require-crit-revi
dotfiles-T133-result-precheck-a02.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -n '^RECORD_KEYS = ' scripts/require-crit-revi
dotfiles-T133-result-precheck-followup-a01.md: OK
dotfiles-T133-task-generator-plan-check-a01.md: OK
dotfiles-T133-verdict-audit-pool-a01.md: OK
dotfiles-T133-verdict-audit-pool-a02.md: OK
dotfiles-T133-verdict-audit-pool-followup-a01.md: OK
dotfiles-T133-worker-cap-hookspath-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c -E 'Keep at most three workers in total|Kee
  C14 premise output differs from its rerun: /usr/bin/grep -c '^worker_cap:' home/dot_agents/agent-config
dotfiles-T133-worker-cap-hookspath-a02.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -c -E 'Keep at most three workers in total|Kee
  C14 premise output differs from its rerun: /usr/bin/grep -c '^worker_cap:' home/dot_agents/agent-config
dotfiles-T133-worker-cap-hookspath-followup-a01.md: OK
dotfiles-T133-worker-hooks-path-a01.md: FAIL
  C14 premise output differs from its rerun: /usr/bin/grep -n 'shell_environment_policy\|settings.local.j
exit=1
```

## plan-check.py, run once

```
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/plan-check.py --root <main checkout>
F3 024-todo.md:22 P1-13 names no bottleneck id of 5.0 or 5.10
F3 024-todo.md:23 P1-14 names no bottleneck id of 5.0 or 5.10
F4 024-checklists.md:9 P1-a holds no backtick command or file path
F6 024-omp-cutover-and-corrective-order.md:39 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
F6 024-omp-cutover-and-corrective-order.md:70 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
F6 024-todo.md:9 cites dotfiles-T131-claude-pinned-merge-gate-fix-a01, which is not a task file
exit=1
```

## CI round 1: test (macos-14, client) on dfce34d7

Run 39124313375, job 117666117287 (`gh run view --log-failed`); the two ubuntu client jobs were cancelled by fail-fast, every other check passed.

```
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5523770Z FAIL: test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan)
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5524590Z ----------------------------------------------------------------------
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5525090Z Traceback (most recent call last):
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5550210Z   File "~/work/dotfiles/dotfiles/tests/unit/test_plan_check.py", line 78, in test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5556530Z     self.assertEqual(self.plan_check("--drift", "--invariants"), (0, []))
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5558150Z     ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5559240Z AssertionError: Tuples differ: (1, ['F6 024-omp-cutover-and-corrective-or[46 chars]st']) != (0, [])
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5559780Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5560060Z First differing element 0:
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5561350Z 1
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5561920Z 0
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5562350Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5562530Z + (0, [])
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5562780Z - (1,
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5563130Z -  ['F6 024-omp-cutover-and-corrective-order.md:11 cites #77, which is not a '
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5563540Z -   'pull request'])
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5563740Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5564050Z ----------------------------------------------------------------------
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5564540Z Ran 1198 tests in 380.499s
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5564810Z 
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.5565080Z FAILED (failures=1, skipped=3)
test (macos-14, client)	Run Python unit tests	2026-10-18T11:49:40.6147570Z make: *** [unit-test] Error 1
```

The stub `gh` lost to the real one: `uv run` puts its base interpreter's bin directory before PATH (on the macOS runner Homebrew's, which holds `gh`). The fix puts the stub first inside `uv run`, as `test_task_checkers.py` does. The four modules on the fix head:

```
head=562e77f4bfb1cf43738d857cda7b672acf302b02
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers
Ran 12 tests in 9.435s
OK (skipped=1)
exit=0
$ git diff --numstat origin/main...HEAD -- tests/unit/test_plan_check.py
104	0	tests/unit/test_plan_check.py
```

## Bot round 1 (review of 35c66022, 3 findings)

The two new cases (the generator refuses a checkout without its records; F2 reports a glob entry against the path it matches) against the code of 35c66022, then on the fix head b3c6b7ea:

```
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check   # code of 35c66022, new tests
FAIL: test_a_generated_task_passes_the_consistency_check_and_pastes_real_premise_outputs (tests.unit.test_task_from_plan.TaskFromPlanTest.test_a_generated_task_passes_the_consistency_check_and_pastes_
AssertionError: 'Traceback' unexpectedly found in 'Traceback (most recent call last):\n  File "~/Workspace/dotfiles/.claude/worktrees/worker-c/scripts/orchestrator/task-from-plan.py", li
FAIL: test_plan_check_reports_each_form_drift_and_invariant_violation_once_and_passes_a_clean_plan (tests.unit.test_plan_check.PlanCheckTest.test_plan_check_reports_each_form_drift_and_invariant_viola
AssertionError: Tuples differ: (0, []) != (1, ['F2 024-omp-cutover-and-corrective-or[45 chars]py'])
Ran 2 tests in 2.256s
FAILED (failures=2)
```

```
$ uv run python -m unittest tests.unit.test_task_from_plan tests.unit.test_plan_check tests.unit.test_task_consistency_c11_c15 tests.unit.test_task_checkers   # b3c6b7ea
Ran 12 tests in 9.443s
OK (skipped=1)
```

A read-only premise sandbox cannot nest inside a seat's sandbox (the probe for finding 4306960622):

```
$ sandbox-exec -p '(version 1)(allow default)(deny file-write*)(allow file-write* (literal "/dev/null"))' bash -c 'echo ran; touch ./nested-write-probe'
sandbox-exec: sandbox_apply: Operation not permitted
exit=71
```
