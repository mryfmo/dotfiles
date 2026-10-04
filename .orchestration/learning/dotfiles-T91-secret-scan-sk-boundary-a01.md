# Learning triage: dotfiles-T91-secret-scan-sk-boundary-a01

Candidates only; nothing is promoted.

1. **Anchor short key prefixes.** A secret regex with a short literal prefix (`sk-`) needs `\b` before it, or every long hyphenated identifier containing the prefix becomes a false positive.
2. **Key-shaped samples trip the scan too.** Task files and evidence that quote key-shaped samples are themselves scanned. Build samples at runtime in tests, and mask them in evidence with `--mask-secrets`, never as literals.
3. **zsh has no bash `PIPESTATUS`.** A pipeline's exit status must be captured from a separate command (`cmd > log; rc=$?`).
4. **zsh's built-in `echo` interprets backslash escapes.** `\uXXXX` followed by non-hex text can become a NUL byte, and a NUL makes `read_scannable_text()` skip the whole file, so the secret check is bypassed. Write evidence prose with Python, a quoted heredoc, or `printf '%s'`, never with `echo` when the text contains backslashes.
5. **Bound every lookahead that scans an unbounded class.** `(?=[…]*X)` after a repeatable prefix is O(n²) on a long run; `{0,N}` keeps it linear. Add a timing test with a generous bound.
6. **Know when to stop enumerating.** When a reviewer keeps finding the next spelling or the opposite trade-off, switch from enumerating forms to a general rule, then let the owner decide the trade-off.
