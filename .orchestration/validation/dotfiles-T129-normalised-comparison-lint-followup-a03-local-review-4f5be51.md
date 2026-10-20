---
task: dotfiles-T129-normalised-comparison-lint-followup-a03
head: 4f5be516555fa55b48b98c26412d9937bd0bb9c1
pr: 415
base: b22a5580d0778e57a66d3f75c76e3c55b88701e1
started: 2026-10-19T04:49:26Z
finished: 2026-10-19T04:56:20Z
findings: 9
engine: codex review --base main (profile review, read-only)
---

- [P2] Bound jq operands at logical comparison boundaries — scripts/lint-comparisons.py:85-89
- [P2] Check every dynamic fragment within a regex interpolation — scripts/lint-comparisons.py:151-153
- [P2] Exclude literal dollar signs from shell interpolation checks — scripts/lint-comparisons.py:110-113
- [P2] Fold shell continuations before checking comparison tokens — scripts/lint-comparisons.py:98-101
- [P2] Ignore jq literals and comments when locating operators — scripts/lint-comparisons.py:117-121
- [P2] Inspect the complete quoted pattern passed to pgrep — scripts/lint-comparisons.py:49-49
- [P2] Preserve literal path suffixes after variable expansions — scripts/lint-comparisons.py:61-64
- [P2] Recognize allow markers only in actual comments — scripts/lint-comparisons.py:179-180
- [P2] Recognize double-quoted jq programs — scripts/lint-comparisons.py:78-82

```text
Reproducible detection gaps let forbidden comparisons pass, while literal handling rejects harmless code. In-memory fixture and CLI checks confirmed these issues; filesystem-creating unit tests were not run in the read-only sandbox.

Full review comments:

- [P2] Preserve literal path suffixes after variable expansions — scripts/lint-comparisons.py:61-64
  For `[[ "$left/bin" == "$right/bin" ]]`, the leading variables cause an immediate return before either `/bin` suffix is inspected, so the lint exits successfully without R1. This also misses the existing comparison in `scripts/check-regime-boundary.sh:125`. Check literal portions as well as variable names instead of treating them as mutually exclusive.

- [P2] Fold shell continuations before checking comparison tokens — scripts/lint-comparisons.py:98-101
  A valid comparison split after `==` using a backslash-newline produces no R1, and continuing `case "$path"` before `in` similarly bypasses R2. Each physical line is tokenized independently, so ordinary formatting lets forbidden comparisons pass the changed-file gate. Fold logical shell lines while retaining their source locations.

- [P2] Recognize double-quoted jq programs — scripts/lint-comparisons.py:78-82
  A changed script containing `jq -r "select(.url == \"/x\")"` passes without R3. The program locator only yields single-quoted strings and skips the entire double-quoted program, even though it is valid shell and jq syntax. Extract both quoting forms, including escaped quotes, before scanning the filter.

- [P2] Check every dynamic fragment within a regex interpolation — scripts/lint-comparisons.py:151-153
  `re.search(f"^{re.escape(prefix) + name}$", text)` passes R6 because its formatted value contains a `re.escape` descendant. Only `prefix` is escaped; metacharacters in `name` remain active. Check that every dynamic fragment is escaped rather than accepting an entire expression whenever an escape reference appears somewhere inside it.

- [P2] Recognize allow markers only in actual comments — scripts/lint-comparisons.py:179-180
  A comparison such as `path == "/tmp/# lint-comparisons: allow sample"` is silently accepted because the marker search examines raw source text. The marker is part of the compared string, not an intentional suppression comment; the same problem affects shell strings. Restrict suppression markers to actual comment tokens.

- [P2] Ignore jq literals and comments when locating operators — scripts/lint-comparisons.py:117-121
  The harmless filter `jq -n '{url: "https://host/?key=abc=="}'` produces R3 and fails for a changed file. Operator discovery scans string contents, so the URL's padding is mistaken for an equality operator; comparisons mentioned in jq comments also produce hits. Mask literals and comments before locating operators, preserving source offsets.

- [P2] Bound jq operands at logical comparison boundaries — scripts/lint-comparisons.py:85-89
  With `canonical_path` defined, `select((.url | canonical_path) == ($p | canonical_path) and .path == ($q | canonical_path))` passes despite comparing raw `.path`. The second operator's left span includes the preceding normalized comparison because scanning does not stop at `and`, so that earlier normalizer incorrectly satisfies the second comparison. Inspect each comparison's actual operands independently.

- [P2] Inspect the complete quoted pattern passed to pgrep — scripts/lint-comparisons.py:49-49
  `pgrep -f "python $proc"` passes without R5, whereas `pgrep -f "$proc"` is rejected. The `\S*` portion stops at the space inside the quoted argument, hiding the variable. Inspect the complete shell pattern argument so adding a command prefix cannot bypass the process-text rule.

- [P2] Exclude literal dollar signs from shell interpolation checks — scripts/lint-comparisons.py:110-113
  `grep -E '\$name' input` searches for the literal text `$name`, but the lint reports R6 and fails a changed script. The check ignores both single-quote semantics and backslash escaping, interpreting literal pattern text as variable expansion. Detect actual shell interpolations rather than every dollar-prefixed identifier in the captured pattern.
Reproducible detection gaps let forbidden comparisons pass, while literal handling rejects harmless code. In-memory fixture and CLI checks confirmed these issues; filesystem-creating unit tests were not run in the read-only sandbox.

Full review comments:

- [P2] Preserve literal path suffixes after variable expansions — scripts/lint-comparisons.py:61-64
  For `[[ "$left/bin" == "$right/bin" ]]`, the leading variables cause an immediate return before either `/bin` suffix is inspected, so the lint exits successfully without R1. This also misses the existing comparison in `scripts/check-regime-boundary.sh:125`. Check literal portions as well as variable names instead of treating them as mutually exclusive.

- [P2] Fold shell continuations before checking comparison tokens — scripts/lint-comparisons.py:98-101
  A valid comparison split after `==` using a backslash-newline produces no R1, and continuing `case "$path"` before `in` similarly bypasses R2. Each physical line is tokenized independently, so ordinary formatting lets forbidden comparisons pass the changed-file gate. Fold logical shell lines while retaining their source locations.

- [P2] Recognize double-quoted jq programs — scripts/lint-comparisons.py:78-82
  A changed script containing `jq -r "select(.url == \"/x\")"` passes without R3. The program locator only yields single-quoted strings and skips the entire double-quoted program, even though it is valid shell and jq syntax. Extract both quoting forms, including escaped quotes, before scanning the filter.

- [P2] Check every dynamic fragment within a regex interpolation — scripts/lint-comparisons.py:151-153
  `re.search(f"^{re.escape(prefix) + name}$", text)` passes R6 because its formatted value contains a `re.escape` descendant. Only `prefix` is escaped; metacharacters in `name` remain active. Check that every dynamic fragment is escaped rather than accepting an entire expression whenever an escape reference appears somewhere inside it.

- [P2] Recognize allow markers only in actual comments — scripts/lint-comparisons.py:179-180
  A comparison such as `path == "/tmp/# lint-comparisons: allow sample"` is silently accepted because the marker search examines raw source text. The marker is part of the compared string, not an intentional suppression comment; the same problem affects shell strings. Restrict suppression markers to actual comment tokens.

- [P2] Ignore jq literals and comments when locating operators — scripts/lint-comparisons.py:117-121
  The harmless filter `jq -n '{url: "https://host/?key=abc=="}'` produces R3 and fails for a changed file. Operator discovery scans string contents, so the URL's padding is mistaken for an equality operator; comparisons mentioned in jq comments also produce hits. Mask literals and comments before locating operators, preserving source offsets.

- [P2] Bound jq operands at logical comparison boundaries — scripts/lint-comparisons.py:85-89
  With `canonical_path` defined, `select((.url | canonical_path) == ($p | canonical_path) and .path == ($q | canonical_path))` passes despite comparing raw `.path`. The second operator's left span includes the preceding normalized comparison because scanning does not stop at `and`, so that earlier normalizer incorrectly satisfies the second comparison. Inspect each comparison's actual operands independently.

- [P2] Inspect the complete quoted pattern passed to pgrep — scripts/lint-comparisons.py:49-49
  `pgrep -f "python $proc"` passes without R5, whereas `pgrep -f "$proc"` is rejected. The `\S*` portion stops at the space inside the quoted argument, hiding the variable. Inspect the complete shell pattern argument so adding a command prefix cannot bypass the process-text rule.

- [P2] Exclude literal dollar signs from shell interpolation checks — scripts/lint-comparisons.py:110-113
  `grep -E '\$name' input` searches for the literal text `$name`, but the lint reports R6 and fails a changed script. The check ignores both single-quote semantics and backslash escaping, interpreting literal pattern text as variable expansion. Detect actual shell interpolations rather than every dollar-prefixed identifier in the captured pattern.
```
