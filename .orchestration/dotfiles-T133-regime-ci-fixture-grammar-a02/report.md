---
task_id: dotfiles-T133-regime-ci-fixture-grammar-a02
seat: claude-standard-dot-a009
reset_of: dotfiles-T133-regime-ci-fixture-grammar-a01
branch: tools/regime-ci-fixture-grammar-a01
pr: https://github.com/mryfmo/dotfiles/pull/441
continued_from: cd47e1b0cf1f8d0b826d559858ad798ebf16f5d2
code_head: 15bc046ef0bc50476879e92cfaa42e5952f6878b
base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
task_sha256: fd9ff2123d96bebdabfea725bcc7c8412b3f1275bbaac2858da143d9a0ff1303
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T133-regime-ci-fixture-grammar-a02 (the reset of the fixture-grammar task)

- **Task:** the reset after INV-6 S2 on a01, from the AGMSG-TASK of message 2765. The a02 task copy is byte-identical to the dispatched file, sha256 `fd9ff212…`, and the task-consistency check passes (validation §1).
- **Branch and PR:** PR #441 continues on `tools/regime-ci-fixture-grammar-a01` from `cd47e1b0`. This task adds only the five a02 files: the task copy, this report, `validation.md`, `sandbox.md` and `learning.md`. The a01 files, its task copy included, are unchanged (§4).

## The inherited implementation (`15bc046e`, unchanged)

- **The five fixture rows** of `tests/unit/test_regime_ci.py`, originally at lines 27, 127, 276, 372 and 373, read the module constant `RESIDUAL = '"residual: the fixture row is test data for this control"'`.
- **Line 276's `no_row`** is an f-string and still removes exactly the `src/tool.sh` row that `ROWS` writes.
- **Nothing else:** no test logic, tests or test names changed.
- **Prior evidence, kept in the a01 records:** the module was 16/16 OK on the unmodified module at `60a6fb2b` and on `15bc046e`. The constant's PyYAML value passes the a05 checker's C13 and C11, with a 45-character payload. The a01 pre-push review found no code defect, nor did the task-level audit of `cd47e1b0`.

## Check

- **The final module run:** a02's measured command, with `uv`'s directory, `TMPDIR` and the three proxy variables, gives `Ran 16 tests` and `OK` (validation §2).
- **Caps (§3):** 0 changed lines outside `tests/` and `.orchestration/`, and 11 of 12 under `tests/`, measured from `60a6fb2b` to the final head.
- **Unchanged since `cd47e1b0`:** the implementation and the a01 records (§4).
- **Final-head CI:** read after the push and given in the RESULT.
