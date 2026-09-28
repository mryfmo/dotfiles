# T33i learning triage

## Candidates

1. A mask that must agree with a scanner has to reproduce the scanner's
   preprocessing at the same scope. The scan strips allowed placeholders
   from the whole text, while a regex match can start inside a placeholder
   name (at its trailing TOKEN part). So judge each line after stripping, not the match
   text alone, and finish with a whole-text rescan.
2. Tests for a secret scanner must build secret-shaped fixtures at runtime;
   otherwise the test file itself fails the repository scan. The same
   applies to validation artifacts that paste test output.
3. `bash -n` and shellcheck do not catch a call to a function that the
   script never defines. A missing `has_command` would have silently
   disabled a guarded step. Prefer the script's existing idiom
   (`command -v`) and cover the positive path with a test.

4. A trust guard based on `git diff --quiet HEAD -- <file>` misses
   **untracked** files. Pair it with `git ls-files --error-unmatch -- <file>`
   when the file's provenance matters.
5. Fail closed on every masking path: a refused, failed or impossible mask
   (for example, no python3) must end the audit as non-passing, never with
   a warning followed by a passing verdict.

6. Decide provenance exceptions from git state (index, `HEAD`, working tree),
   never from a filesystem test alone. A tracked file deleted from the tree
   passes `[[ -f ]]` as "absent" and silently takes the exception.

## Promotion

None. These are candidates only.
