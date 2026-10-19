## Summary

The F2 lineage's owner task (`dotfiles-T129-normalised-comparison-lint-followup-a02`, with amendment 1) closes the lint's nine detection gaps. That is 13 owned row ids: the four Bot rows of #415 and `audit:4f5be51:1` to `:9`. The fix follows the record's re-plan: the comparison lint reads tokens, not physical-line regexes.

- **Shell:** shell words are read through shlex with continuation lines joined. A marker counts only in a real comment, on any line of a continued statement.
- **jq:** programs are read by a string-aware scanner that ignores string literals and comments, and keeps nested `\(…)` interpolations as code. `and`/`or`/`then`/`elif`/`else` bound an operand, `if…end` is one operand, and double-quoted programs are read too, across lines.
- **Python:** markers are read only from comment tokens. Every fragment of a formatted value must be escaped.
- **`pgrep -f` and `grep -E`:** they take their whole shell word, and a `$name` counts only where the shell expands it.
- **Operands:** a literal path piece beside an expansion counts.

`tests/unit/test_lint_comparisons.py::LintComparisonsTest::test_each_owned_row_is_refused_or_accepted_by_its_fixture` holds one entry per gap, naming its row ids. Each entry was red against main's lint, and each fix is shown load-bearing by a mutant.

The baseline follows the sharper rules:

- One false positive's row leaves.
- Three rows are added for hits newly found in files no open task names.
- Three true positives in files open tasks name stay as warnings, under the changed-file gate.

`--list-rules` is unchanged.

## Evidence

`.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a02/` holds:

- the task copy, byte-identical to the amended dispatched file;
- the report;
- the validation output:
  - red at main and at the first implementation;
  - green: 15 of 15;
  - 17 mutants killed;
  - the tree-wide `--all` comparison with main;
  - ruff;
  - the caps: 163 of 350 and 68 of 1000;
  - `make format`, verbatim with per-file exit statuses, the same at the merge-base;
- the sandbox record, including which Python runs used `-I`;
- the learning triage;
- the worker review record and its receipt.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
