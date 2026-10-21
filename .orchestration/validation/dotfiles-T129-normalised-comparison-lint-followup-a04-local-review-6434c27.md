---
task: dotfiles-T129-normalised-comparison-lint-followup-a04
head: 6434c27c762aecc134f075bd220a34c0d6e20037
pr: 432
base: b8213131f3818de6d14aae1ccb4b79a7ce7a99ba
started: 2026-10-20T08:51:23Z
finished: 2026-10-20T08:59:06Z
findings: 2
engine: codex review --base main (profile review, read-only)
---

- [P2] Keep fully escaped regex compositions accepted — scripts/lint-comparisons.py:310-314
- [P2] Preserve R5 detection through subshell producers — scripts/lint-comparisons.py:246-249

```text
Comparison against the base reproduced an R5 detection regression and R6 false positives. Existing in-memory fixture checks passed; the full test suite was not run in the read-only environment.

Full review comments:

- [P2] Preserve R5 detection through subshell producers — scripts/lint-comparisons.py:246-249
  For `(ps -axo pid,command) | grep claude`, the producer node is a `Subshell`, whose `Args` is absent, so this code never emits R5. The base version detects this input, and grouping the producer does not change the unsafe parsing of process output. Inspect grouped producers while retaining the existing `ps -o ... -p` exception, and add a regression test.

- [P2] Keep fully escaped regex compositions accepted — scripts/lint-comparisons.py:310-314
  Interpolations such as `f"{re.escape(a) + re.escape(b)}"` and `f"{re.escape(sep).join(map(re.escape, names))}"` now produce R6: concatenations fall through, and joins require a constant separator. Both were accepted before and contain no unescaped input, so valid changed files now fail lint. Recursively validate concatenation operands and permit escaped separators, with positive regression tests alongside the unsafe cases.
Comparison against the base reproduced an R5 detection regression and R6 false positives. Existing in-memory fixture checks passed; the full test suite was not run in the read-only environment.

Full review comments:

- [P2] Preserve R5 detection through subshell producers — scripts/lint-comparisons.py:246-249
  For `(ps -axo pid,command) | grep claude`, the producer node is a `Subshell`, whose `Args` is absent, so this code never emits R5. The base version detects this input, and grouping the producer does not change the unsafe parsing of process output. Inspect grouped producers while retaining the existing `ps -o ... -p` exception, and add a regression test.

- [P2] Keep fully escaped regex compositions accepted — scripts/lint-comparisons.py:310-314
  Interpolations such as `f"{re.escape(a) + re.escape(b)}"` and `f"{re.escape(sep).join(map(re.escape, names))}"` now produce R6: concatenations fall through, and joins require a constant separator. Both were accepted before and contain no unescaped input, so valid changed files now fail lint. Recursively validate concatenation operands and permit escaped separators, with positive regression tests alongside the unsafe cases.
```
