---
task: dotfiles-T129-normalised-comparison-lint-followup-a04
head: 7eab146d20469e88b1c9012d5bcce6e12aace335
pr: 432
base: 230b36767eec123f90dcd79edca76993d9bb9de7
started: 2026-10-20T11:20:20Z
finished: 2026-10-20T11:25:09Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Accept concatenations whose operands are fully escaped — scripts/lint-comparisons.py:396-396
- [P2] Preserve R3 checks for jq launched through env — scripts/lint-comparisons.py:305-306

```text
Two reproducible regressions remain: env-wrapped jq filters evade R3, and fully escaped Python concatenations incorrectly trigger R6. Existing fixture-table checks pass but do not cover these cases.

Full review comments:

- [P2] Preserve R3 checks for jq launched through env — scripts/lint-comparisons.py:305-306
  For `env LC_ALL=C jq -r 'select(.url == "/x")'`, `command()` leaves `env` in `args[0]`, so this condition skips the jq filter entirely. The base version reports R3 for this input, but the patch returns no findings, allowing an unnormalized comparison in a changed file. Resolve the executable through supported launchers such as `env` before checking whether it runs jq.

- [P2] Accept concatenations whose operands are fully escaped — scripts/lint-comparisons.py:396-396
  `re.search(f"^{re.escape(prefix) + re.escape(name)}$", text)` was previously accepted, but now triggers R6 because its `ast.BinOp` falls through this check. Both dynamic fragments are escaped, so rejecting this expression incorrectly fails lint for safe code in changed files. Recursively validate concatenation operands while retaining rejection when either operand contains an unescaped value.
Two reproducible regressions remain: env-wrapped jq filters evade R3, and fully escaped Python concatenations incorrectly trigger R6. Existing fixture-table checks pass but do not cover these cases.

Full review comments:

- [P2] Preserve R3 checks for jq launched through env — scripts/lint-comparisons.py:305-306
  For `env LC_ALL=C jq -r 'select(.url == "/x")'`, `command()` leaves `env` in `args[0]`, so this condition skips the jq filter entirely. The base version reports R3 for this input, but the patch returns no findings, allowing an unnormalized comparison in a changed file. Resolve the executable through supported launchers such as `env` before checking whether it runs jq.

- [P2] Accept concatenations whose operands are fully escaped — scripts/lint-comparisons.py:396-396
  `re.search(f"^{re.escape(prefix) + re.escape(name)}$", text)` was previously accepted, but now triggers R6 because its `ast.BinOp` falls through this check. Both dynamic fragments are escaped, so rejecting this expression incorrectly fails lint for safe code in changed files. Recursively validate concatenation operands while retaining rejection when either operand contains an unescaped value.
```
