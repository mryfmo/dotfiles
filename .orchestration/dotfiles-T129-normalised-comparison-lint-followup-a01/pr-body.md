## Summary

The owner task of the lint lineage's advisory P2 rows (`dotfiles-T129-normalised-comparison-lint-followup-a01`): the three rows recorded under `## Owned by dotfiles-T129-normalised-comparison-lint-followup-a01` in PR #387's acceptance record, each fixed in `scripts/lint-comparisons.py` with one refusal fixture in `tests/unit/test_lint_comparisons.py`, red before the fix and green after.

| Row (Bot comment on #387) | Class | Change | Test |
|---|---|---|---|
| 4302629300 | jq-program-location | the base scan (the first single-quoted string after the `jq` word on its logical line) now skips a `'` inside a `"…"` string and a single-quoted string that is an option's argument (`--arg`, `--argjson`, `--slurpfile`, `--rawfile` with an optional name; `--indent`, `-L`, `--library-path`, from `jq --help` of jq 1.8.2), so it reads every candidate the base read except a `'` inside a closed `"…"` string | `test_a_single_quoted_jq_option_value_is_not_read_as_the_program` |
| 4302629305 | presence-not-structure | R3 accepts a side only when it applies the def as a word outside string literals and jq comments, not a `.field` or `$variable` | `test_a_jq_normaliser_name_inside_a_string_literal_is_no_application` |
| 4302629307 | presence-not-structure | Python R6 needs a `re.escape` reference in every formatted value of the f-string (`map(re.escape, names)` counts) | `test_every_f_string_interpolation_in_a_regex_is_escaped` |

- The baseline gains one row: the sharper R6 finds `scripts/orchestrator/task-consistency-check.py:66`, where `rid.rsplit('-', 1)[-1]` is interpolated unescaped beside `re.escape(rid)`; the file is owned by no task in flight.
- `--list-rules` and the rule table are unchanged; the script stays at 200 lines (D-cap-F2).

## Evidence

`.orchestration/dotfiles-T129-normalised-comparison-lint-followup-a01/` holds the task copy, the report, the validation output (the RED run at the tests commit, the GREEN run at the head, ruff, the caps, the tree-hit and located-program diffs), the sandbox record and the learning triage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
