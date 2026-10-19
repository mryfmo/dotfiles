## Summary

This PR supersedes #387 (task `dotfiles-T129-normalised-comparison-lint-followup-a01`, Amendment 1): it is #387's lint rebased onto `main` with the lineage's owned rows fixed on top, so its diff against `main` is the whole F2 change.

- `scripts/lint-comparisons.py` (200 lines, standard library only, `python3 -I`) refuses string-form comparisons of paths, URLs and processes (rules R0 to R6, `--list-rules`) over the shell and Python files `git ls-files` lists under `home/`, `scripts/` and `install/`; `scripts/lint-comparisons-baseline.tsv` holds one content-hashed row per existing hit; `tests/unit/test_lint_comparisons.py` holds one fixture per rule, normaliser and structural check, and the tracked-tree check.
- The three owned rows of the lineage's acceptance record, each with a refusal fixture red before its fix and green after:

| Row (Bot comment on #387) | Class | Change | Test |
|---|---|---|---|
| 4302629300 | jq-program-location | the base scan (the first single-quoted string after the `jq` word on its logical line) skips a `'` inside a `"…"` string and a single-quoted string that is an option's argument (`--arg`, `--argjson`, `--slurpfile`, `--rawfile`, `--indent`, `-L`, `--library-path`, from `jq --help` of jq 1.8.2) | `test_a_single_quoted_jq_option_value_is_not_read_as_the_program` |
| 4302629305 | presence-not-structure | R3 accepts a side only when it applies the def as a word outside string literals and jq comments | `test_a_jq_normaliser_name_inside_a_string_literal_is_no_application` |
| 4302629307 | presence-not-structure | Python R6 needs a `re.escape` reference in every formatted value of the f-string | `test_every_f_string_interpolation_in_a_regex_is_escaped` |

- The six Bot threads of #387, each closed by a fixture on this branch: 4302545078, 4302545082 and 4302545085 by 192c88d2 (the structural checks for the baseline count, the qualified normaliser names and the jq normaliser per operand), 4302629300 by f78e5dbf, 4302629305 and 4302629307 by 514969d1.
- The baseline follows `main`: the two rows of `home/dot_claude/hooks/executable_project-map-reload.sh`, which `main` changed, are replaced by its three current hits, and `scripts/update-agent-assets.sh:966` (the repeated `case "$(uname -s)/$(uname -m)"` line) gets a row; the lint exits 0 with no output on the tree.

## Evidence

`.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/` holds the task copy, the report (the per-thread dispositions and the baseline rows per rule and file), the validation output (§12 onward at the rebased head: the rebase map, the baseline, each thread's fixture red then green, the Check's tests and lint, ruff, the caps), the sandbox record and the learning triage; `.orchestration/dotfiles-T129-normalised-comparison-lint-a01/` holds #387's.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
