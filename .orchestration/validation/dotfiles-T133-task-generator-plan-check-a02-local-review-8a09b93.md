---
task: dotfiles-T133-task-generator-plan-check-a02
head: 8a09b9365932f23b09df8aa2385a93d0b3016a3e
pr: 417
base: b22a5580d0778e57a66d3f75c76e3c55b88701e1
started: 2026-10-19T04:09:13Z
finished: 2026-10-19T04:16:45Z
findings: 5
engine: codex review --base main (profile review, read-only)
---

- [P2] Classify agent instruction files as applied files — scripts/orchestrator/task-consistency-check.py:63-65
- [P2] Handle nested directory scopes before invoking C7b — scripts/orchestrator/task-from-plan.py:153-153
- [P2] Include repository-root files in the generated edit scope — scripts/orchestrator/task-from-plan.py:137-137
- [P2] Normalize extracted paths before emitting allowed_files — scripts/orchestrator/task-from-plan.py:138-143
- [P2] Use a threat-row selector accepted by C11 — .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md:37-37

```text
The generator can omit required files, emit incompatible paths, and reject nested scopes. Instruction-file coverage and the task's own disposition selector also have validation gaps. Read-only probes reproduced these issues; the write-requiring unit suite was not run.

Full review comments:

- [P2] Include repository-root files in the generated edit scope — scripts/orchestrator/task-from-plan.py:137-137
  When a program item names `Makefile` or `AGENTS.md`, the mandatory `/` filter silently drops those files from `allowed_files`. Neither can be recovered by the subsequent script/test grep. The generated task therefore omits explicitly requested edits, which regime CI later rejects as outside its scope. Accept existing root-level files and root-level filenames with extensions.

- [P2] Handle nested directory scopes before invoking C7b — scripts/orchestrator/task-from-plan.py:153-153
  An item naming both `scripts/demo.sh` and `scripts/**` generates separate rows, but C7b reduces the directory glob to `scripts` and counts both entries in the child-file row. Generation consequently fails with C7b despite having one row per entry. Make entry matching distinguish these nested scopes, preserving the row unit required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Normalize extracted paths before emitting allowed_files — scripts/orchestrator/task-from-plan.py:138-143
  When an item names `./scripts/demo.sh` and no other entry covers that script, the leading `./` is retained and the consistency checker passes. However, Git reports the changed path as `scripts/demo.sh`, and `regime-ci.py::allowed()` compares literal entries without normalization, rejecting the requested edit. Emit canonical repository-relative spellings rather than the original path text.

- [P2] Classify agent instruction files as applied files — scripts/orchestrator/task-consistency-check.py:63-65
  For an allowed scope of `*.md`, C12 passes without concrete rows for `AGENTS.md` or `CLAUDE.md` because this predicate classifies neither as applied. These files contain agent instructions, and the SKILL row-unit rule referenced by [AGENTS.md:78](AGENTS.md#L78) includes rules that seats follow. Recognize instruction files so both C12 and the generator require their concrete threat rows.

- [P2] Use a threat-row selector accepted by C11 — .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md:37-37
  This selector contains two `::` components, whereas the new C11 regex accepts only `tests/<path>::<identifier>`. Checking the a02 task content therefore produces a C11 finding, preventing its required consistency check from passing. Use the accepted selector shape, or update the validator and tests consistently; threat-row selector validation is required by [AGENTS.md:78](AGENTS.md#L78).
The generator can omit required files, emit incompatible paths, and reject nested scopes. Instruction-file coverage and the task's own disposition selector also have validation gaps. Read-only probes reproduced these issues; the write-requiring unit suite was not run.

Full review comments:

- [P2] Include repository-root files in the generated edit scope — scripts/orchestrator/task-from-plan.py:137-137
  When a program item names `Makefile` or `AGENTS.md`, the mandatory `/` filter silently drops those files from `allowed_files`. Neither can be recovered by the subsequent script/test grep. The generated task therefore omits explicitly requested edits, which regime CI later rejects as outside its scope. Accept existing root-level files and root-level filenames with extensions.

- [P2] Handle nested directory scopes before invoking C7b — scripts/orchestrator/task-from-plan.py:153-153
  An item naming both `scripts/demo.sh` and `scripts/**` generates separate rows, but C7b reduces the directory glob to `scripts` and counts both entries in the child-file row. Generation consequently fails with C7b despite having one row per entry. Make entry matching distinguish these nested scopes, preserving the row unit required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Normalize extracted paths before emitting allowed_files — scripts/orchestrator/task-from-plan.py:138-143
  When an item names `./scripts/demo.sh` and no other entry covers that script, the leading `./` is retained and the consistency checker passes. However, Git reports the changed path as `scripts/demo.sh`, and `regime-ci.py::allowed()` compares literal entries without normalization, rejecting the requested edit. Emit canonical repository-relative spellings rather than the original path text.

- [P2] Classify agent instruction files as applied files — scripts/orchestrator/task-consistency-check.py:63-65
  For an allowed scope of `*.md`, C12 passes without concrete rows for `AGENTS.md` or `CLAUDE.md` because this predicate classifies neither as applied. These files contain agent instructions, and the SKILL row-unit rule referenced by [AGENTS.md:78](AGENTS.md#L78) includes rules that seats follow. Recognize instruction files so both C12 and the generator require their concrete threat rows.

- [P2] Use a threat-row selector accepted by C11 — .orchestration/dotfiles-T133-task-generator-plan-check-a02/task.md:37-37
  This selector contains two `::` components, whereas the new C11 regex accepts only `tests/<path>::<identifier>`. Checking the a02 task content therefore produces a C11 finding, preventing its required consistency check from passing. Use the accepted selector shape, or update the validator and tests consistently; threat-row selector validation is required by [AGENTS.md:78](AGENTS.md#L78).
```
