---
task: dotfiles-T129-normalised-comparison-lint-followup-a02
head: b24d3136b35e77efe647bdb6d487d9c76503d4c6
pr: 432
base: ba318e5369b14a79d6f515e87b685c9bcb30c12e
started: 2026-10-19T21:54:49Z
finished: 2026-10-19T22:00:35Z
findings: 5
engine: codex review --base main (profile review, read-only)
---

- [P2] Distinguish arithmetic shifts from heredoc redirections — scripts/lint-comparisons.py:98-100
- [P2] Exclude quoted heredoc data from shell-rule scanning — scripts/lint-comparisons.py:179-180
- [P2] Honor escaped quotes inside ANSI-C shell strings — scripts/lint-comparisons.py:88-94
- [P2] Recognize positional parameters in process patterns — scripts/lint-comparisons.py:74-75
- [P2] Scan every adjacent piece of a jq program word — scripts/lint-comparisons.py:125-129

```text
Base-versus-head reproductions confirm missed process and jq findings, broken comment recognition, and false positives on literal heredoc data. Existing fixture checks passed in memory; the full unittest suite was not run because the environment is read-only.

Full review comments:

- [P2] Recognize positional parameters in process patterns — scripts/lint-comparisons.py:74-75
  For `pgrep -f "$1"`, `${1}`, or `$*`, `expands()` returns false because it only recognizes names beginning with a letter or underscore. These are actual shell expansions, and the base version reported R5 for them. Include positional and special parameters so dynamic process patterns do not silently bypass the rule.

- [P2] Scan every adjacent piece of a jq program word — scripts/lint-comparisons.py:125-129
  For `jq -n --arg path /x "select("' .url == $path)'`, the shell concatenates the quoted pieces into one filter, but `programs()` yields only `select(`. Consequently, this raw path comparison no longer produces the R3 finding emitted by the base version. Collect adjacent quoted pieces belonging to the same shell word before analyzing the program.

- [P2] Distinguish arithmetic shifts from heredoc redirections — scripts/lint-comparisons.py:98-100
  Valid Bash arithmetic such as `mask=$((1 << n))` is treated as opening a heredoc with delimiter `n`. Unless a subsequent line is exactly `n`, all remaining comments disappear from the comment map: reasonless markers evade R0, while documented allow markers stop suppressing findings. Check the arithmetic context before recording a heredoc.

- [P2] Honor escaped quotes inside ANSI-C shell strings — scripts/lint-comparisons.py:88-94
  After a valid word such as `$'can\'t'`, the scanner mistakes the escaped apostrophe for the closing quote and the final apostrophe for a new opening quote. That incorrect state persists across later lines, hiding real comments and breaking both R0 detection and allow-marker handling. Track ANSI-C quoting separately and honor its escaped apostrophes.

- [P2] Exclude quoted heredoc data from shell-rule scanning — scripts/lint-comparisons.py:179-180
  A quoted heredoc containing the literal line `# [[ $path == /x ]]` now produces R1, although the base version accepted it. `comments()` correctly excludes heredoc bodies from its comment map, but this line then treats their absence as executable source and scans the entire body. Preserve literal-body spans and exclude them from shell-rule detection instead of interpreting them as commands.
Base-versus-head reproductions confirm missed process and jq findings, broken comment recognition, and false positives on literal heredoc data. Existing fixture checks passed in memory; the full unittest suite was not run because the environment is read-only.

Full review comments:

- [P2] Recognize positional parameters in process patterns — scripts/lint-comparisons.py:74-75
  For `pgrep -f "$1"`, `${1}`, or `$*`, `expands()` returns false because it only recognizes names beginning with a letter or underscore. These are actual shell expansions, and the base version reported R5 for them. Include positional and special parameters so dynamic process patterns do not silently bypass the rule.

- [P2] Scan every adjacent piece of a jq program word — scripts/lint-comparisons.py:125-129
  For `jq -n --arg path /x "select("' .url == $path)'`, the shell concatenates the quoted pieces into one filter, but `programs()` yields only `select(`. Consequently, this raw path comparison no longer produces the R3 finding emitted by the base version. Collect adjacent quoted pieces belonging to the same shell word before analyzing the program.

- [P2] Distinguish arithmetic shifts from heredoc redirections — scripts/lint-comparisons.py:98-100
  Valid Bash arithmetic such as `mask=$((1 << n))` is treated as opening a heredoc with delimiter `n`. Unless a subsequent line is exactly `n`, all remaining comments disappear from the comment map: reasonless markers evade R0, while documented allow markers stop suppressing findings. Check the arithmetic context before recording a heredoc.

- [P2] Honor escaped quotes inside ANSI-C shell strings — scripts/lint-comparisons.py:88-94
  After a valid word such as `$'can\'t'`, the scanner mistakes the escaped apostrophe for the closing quote and the final apostrophe for a new opening quote. That incorrect state persists across later lines, hiding real comments and breaking both R0 detection and allow-marker handling. Track ANSI-C quoting separately and honor its escaped apostrophes.

- [P2] Exclude quoted heredoc data from shell-rule scanning — scripts/lint-comparisons.py:179-180
  A quoted heredoc containing the literal line `# [[ $path == /x ]]` now produces R1, although the base version accepted it. `comments()` correctly excludes heredoc bodies from its comment map, but this line then treats their absence as executable source and scans the entire body. Preserve literal-body spans and exclude them from shell-rule detection instead of interpreting them as commands.
```
