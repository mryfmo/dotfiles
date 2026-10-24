# Learning triage: dotfiles-T129-normalised-comparison-lint-followup-a04

These are candidates only; nothing is promoted.

1. [memory:decision] When a hand-written parser has failed audits more than once, the fix is to take the syntax from the language's own parser and keep only rule logic in the lint.
   - Here, shfmt's `--tojson` AST answered all seven audit findings and the three Bot threads without a single quote, continuation or heredoc rule of our own.
   - The tree-wide `--all` output stayed byte-identical to the hand-parser's (validation §3), so the reader changed without moving the baseline.
2. [memory:decision] An AST is only the reader for the files it can parse. Before adopting one, run it over every tracked target.
   - That probe found 14 refusals under `-ln bash`: 4 zsh files, 5 non-shell `.tmpl` files and 5 chezmoi shell templates. Those findings became amendment 1's dialect, targeting and blanking rules.
   - Two of the templates still refused after blanking: a subshell holding only `{{ include }}` lines became empty. An include alone on its line therefore became the no-op `:`.
3. [memory:failure] A mutant guarding a defensive branch survives unless some fixture reaches the branch.
   - The `Hdoc` skip mattered only for a command substitution, or a comment, inside an unquoted heredoc body, and no fixture had either.
   - Another fixture never reached its branch because of a short-circuit: `[[ $path == '' ]]` decides on `$path` before reading `''`.
   - The fix was to plan the mutants against the fixtures before calling the fixtures done.
4. [memory:failure] Swapping the reader also swaps the unit of "a statement". The first AST version used the innermost statement, which narrowed marker and normaliser scope against the old physical-line reading, and only the review caught it.
   - Behavior preservation needs fixtures for the old unit's edges (a `&&` chain, a continued `case … in`, a `;` on one line). The tree comparison alone cannot show this, because no tracked file sits on those edges.
5. [memory:decision] shfmt's JSON omits empty fields (`''` has no `Value`). A split double-quoted backslash-newline leaves its backslash inside one `Lit`'s span and the newline outside it. An unquoted `Lit`'s `Value` drops the continuation that its span keeps.
   - Read positions from the source span and every optional field with `.get`.
   - The tracked-tree test found the empty-`Value` crash that no fixture had.
6. [memory:failure] `uv run python` silently resolved to Python 3.10 in this worktree, which cannot compile the possessive `*+` the old lint used. Name the trusted interpreter by its absolute path in every evidence command.
