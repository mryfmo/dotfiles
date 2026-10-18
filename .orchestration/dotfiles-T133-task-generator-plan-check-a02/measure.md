---
task_id: dotfiles-T133-task-generator-plan-check-a02
round: 1
code_head: 6e07d29193e9a3b56b299dd9d55538788bc48b7b
merge_base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
---

# Measure

`git diff --numstat origin/main...HEAD` on the code head. The totals cover the whole PR, including the inherited a01 changes and the bundled template. Changed lines are additions plus deletions.

| Scope | Changed lines | Cap |
| --- | --- | --- |
| outside `tests/` and `.orchestration/` | 659 | 700 |
| under `tests/` | 657 | 800 |
| under `.orchestration/` (not capped) | 982 | — |

Changed files outside `.orchestration/`:

| Added | Deleted | File |
| --- | --- | --- |
| 232 | 0 | `scripts/orchestrator/plan-check.py` |
| 140 | 11 | `scripts/orchestrator/task-consistency-check.py` |
| 242 | 0 | `scripts/orchestrator/task-from-plan.py` |
| 34 | 0 | `scripts/orchestrator/task-template.md` |
| 166 | 0 | `tests/unit/test_plan_check.py` |
| 9 | 3 | `tests/unit/test_task_checkers.py` (amendment 1's two edits, from a01) |
| 265 | 0 | `tests/unit/test_task_consistency_c11_c15.py` |
| 214 | 0 | `tests/unit/test_task_from_plan.py` |

Under `.orchestration/`:
- the a01 evidence records, kept as history;
- the a02 task copy;
- this directory's records, added by the evidence commit.

The a01 task copy is deleted in 6da92853. Numstat against the merge base does not list it, because main never had it.

The review measured 651 and 647 on eb20d063. The correction round added 8 lines outside `tests/` and 10 under it.
