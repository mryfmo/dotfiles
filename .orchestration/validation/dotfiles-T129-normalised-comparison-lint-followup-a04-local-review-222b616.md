---
task: dotfiles-T129-normalised-comparison-lint-followup-a04
head: 222b61612d65ae47e7684ffa8505c5a6c288c60e
pr: 432
base: f7ed01427a43567b9c1857d2f62953add8b97c92
started: 2026-10-20T07:56:35Z
finished: 2026-10-20T08:03:25Z
findings: 5
engine: codex review --base main (profile review, read-only)
---

- [P2] Accept concatenations whose fragments are all escaped — scripts/lint-comparisons.py:306-310
- [P2] Identify jq from the current command rather than nested text — scripts/lint-comparisons.py:262-264
- [P2] Preserve expansions when distinguishing patterns from options — scripts/lint-comparisons.py:254-256
- [P2] Recognize command wrappers before bracket tests — scripts/lint-comparisons.py:240-243
- [P3] Emit R0 for reasonless comments inside jq programs — scripts/lint-comparisons.py:286-289

```text
Differential checks reproduced missed violations and false positives introduced by the patch. All 78 inherited fixture checks passed in memory; the full suite was not run in the read-only sandbox.

Full review comments:

- [P2] Preserve expansions when distinguishing patterns from options — scripts/lint-comparisons.py:254-256
  For `pgrep -f "$name-worker"` and `grep -E "$prefix-$name"`, `static()` removes the variables, leaving text beginning with `-`. This loop consumes the pattern as another option, so both violations go undetected instead of producing R5/R6 as they did before. Use the word's structure, not its expansion-stripped text, to distinguish options from patterns.

- [P2] Recognize command wrappers before bracket tests — scripts/lint-comparisons.py:240-243
  Valid comparisons such as `command [ "$path" = "$value" ]` now produce no R1 because the first argument is `command`, not `[`. The same regression affects `builtin [` and `env [`, all of which the base implementation detected. Unwrap statically known command prefixes before inspecting the test arguments.

- [P2] Identify jq from the current command rather than nested text — scripts/lint-comparisons.py:262-264
  For `printf '%s' "$(jq '.a' file)" 'select(.url == $p)'`, this search finds `jq` inside the substitution argument and treats the following printf argument as a jq program. The result is a new R3 false positive even though the actual jq program contains no comparison. Resolve the current command's executable separately and let AST traversal inspect nested commands.

- [P2] Accept concatenations whose fragments are all escaped — scripts/lint-comparisons.py:306-310
  `re.search(f"{re.escape(prefix) + re.escape(name)}", text)` now produces R6 even though every interpolated fragment is escaped and the base implementation accepted it. `escaped()` returns false for every concatenation, not just the partially escaped cases covered by the new tests. Recursively check both operands of string concatenations so safe expressions remain accepted.

- [P3] Emit R0 for reasonless comments inside jq programs — scripts/lint-comparisons.py:286-289
  A jq program containing `.foo # lint-comparisons: allow` now produces no R0. Marker handling is reached only for path-comparison hits, while the shell comment collection excludes the quoted jq program. The base implementation reported this reasonless marker. Collect jq comment markers independently of comparison hits so R0 remains enforced.
Differential checks reproduced missed violations and false positives introduced by the patch. All 78 inherited fixture checks passed in memory; the full suite was not run in the read-only sandbox.

Full review comments:

- [P2] Preserve expansions when distinguishing patterns from options — scripts/lint-comparisons.py:254-256
  For `pgrep -f "$name-worker"` and `grep -E "$prefix-$name"`, `static()` removes the variables, leaving text beginning with `-`. This loop consumes the pattern as another option, so both violations go undetected instead of producing R5/R6 as they did before. Use the word's structure, not its expansion-stripped text, to distinguish options from patterns.

- [P2] Recognize command wrappers before bracket tests — scripts/lint-comparisons.py:240-243
  Valid comparisons such as `command [ "$path" = "$value" ]` now produce no R1 because the first argument is `command`, not `[`. The same regression affects `builtin [` and `env [`, all of which the base implementation detected. Unwrap statically known command prefixes before inspecting the test arguments.

- [P2] Identify jq from the current command rather than nested text — scripts/lint-comparisons.py:262-264
  For `printf '%s' "$(jq '.a' file)" 'select(.url == $p)'`, this search finds `jq` inside the substitution argument and treats the following printf argument as a jq program. The result is a new R3 false positive even though the actual jq program contains no comparison. Resolve the current command's executable separately and let AST traversal inspect nested commands.

- [P2] Accept concatenations whose fragments are all escaped — scripts/lint-comparisons.py:306-310
  `re.search(f"{re.escape(prefix) + re.escape(name)}", text)` now produces R6 even though every interpolated fragment is escaped and the base implementation accepted it. `escaped()` returns false for every concatenation, not just the partially escaped cases covered by the new tests. Recursively check both operands of string concatenations so safe expressions remain accepted.

- [P3] Emit R0 for reasonless comments inside jq programs — scripts/lint-comparisons.py:286-289
  A jq program containing `.foo # lint-comparisons: allow` now produces no R0. Marker handling is reached only for path-comparison hits, while the shell comment collection excludes the quoted jq program. The base implementation reported this reasonless marker. Collect jq comment markers independently of comparison hits so R0 remains enforced.
```
