## Summary

The F1 lineage's owner task (`dotfiles-T129-audit-inherit-replan-json-followup-a02`) fixes the three advisory rows of PR #413's final-head audit and local review. Each row comes with one refusal fixture that is red before its fix and green after.

| Row | Change | Test |
|---|---|---|
| audit:274a536:1 (= local:274a536:1) | `scripts/regime-counters.sh`: S1's `re-plan=present` now follows the gate's exact schema (`require-crit-review.py` `record_field_errors()`, `acceptance-front-matter.py`). The whole `replans` object must be `{<class slug>: exactly the four keys, each a string with text after str.strip()}`. Text means any character outside the 29 that Python's `str.strip()` removes. A slug must end at the end of the key, as `fullmatch` requires, and `"replans": false` counts as malformed, not empty. | `test_s1_applies_the_gate_s_exact_replan_schema` |
| audit:274a536:2 (= local:274a536:2) | `scripts/orchestrator/chain-integrate.sh`: the audit is inherited only when the parent's verdict is one the gate accepts (`correct`, or `incorrect` with a `[P0-P3]` line). A blocked, empty or finding-less parent result takes the fresh-audit path. | `test_inheritance_requires_a_parent_verdict_the_gate_accepts` |
| audit:274a536:5 | `scripts/orchestrator/ledger-check.py`: the needed ids are deduplicated in order, so an audit and its inherited copy count each finding once. | `test_ledger_check_counts_an_audit_and_its_inherited_copy_once` |

## Evidence

`.orchestration/dotfiles-T129-audit-inherit-replan-json-followup-a02/` holds:

- the task copy;
- the report;
- the validation output:
  - each test red at its tests commit (`495f51b3` for the rows, `f75c1137` for the worker review's cases) and green at the code head `02b6eec1`;
  - the Check's modules;
  - `test_require_crit_review` passing 98 of 98 once the seat's git signing environment is fixed;
  - the linters;
  - the caps over merge-base...code head (26 of 200 and 69 of 1000);
- the sandbox record;
- the learning triage;
- the worker review record and its receipt.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
