# Learning triage: dotfiles-T129-normalised-comparison-lint-followup-a02

These are candidates only; nothing is promoted.

1. [memory:decision] Removing jq string interpolations with a `\([^)]*\)` regex breaks on a nested parenthesis (`\(if (…) …)`), and every later string-aware step inherits the desync.
   - A scanner that keeps a context stack works where the regex does not: string, interpolation code with its own parenthesis depth, comment.
   - The tree-wide `--all` diff against main's lint found the false positives that this desync caused. No fixture did.
2. [memory:decision] A sharper lint has to be measured on the whole tracked tree before and after.
   - Every new or vanished hit is judged true or false positive before any baseline row moves.
   - Here that judgment found two new false positives from my own change, which the keyword bound then fixed, and one false positive on main that the and/or bound fixed.
3. [memory:failure] An `operand` check that answers from a leading variable's name alone ignores the literal path the token goes on to carry (`"$x/path"`). Both pieces have to be checked.
