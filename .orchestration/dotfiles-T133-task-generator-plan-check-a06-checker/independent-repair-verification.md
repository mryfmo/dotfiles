# Independent repair verification

Review date: 2026-10-20. Reviewer: the same independent Codex subagent that reported `a06-final-pipeline:1` and `a06-final-pipeline:2`.
This is local process evidence, not reviewer authentication or integration approval.

The parent reported owner messages 2802 and 2805 authorizing the repairs and amended caps. Independently inspected the amended task copy and bound source/test bytes below. The previous review, reproduction log and unresolved JSON are preserved unchanged as historical evidence.

## Binding

| File | SHA-256 |
| --- | --- |
| `scripts/orchestrator/task-consistency-check.py` | `98c0904f4291b7d3971beb643321dff1c557c13d9b30f3af46760df1385b0f3c` |
| `tests/unit/test_task_consistency_c11_c15.py` | `7ba89c81cca29144d5702c056f45547cee8ce83d2ed7c4572f9fc8819de7ed61` |
| `tests/unit/test_task_checkers.py` | `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f` |
| a06 `task.md` | `b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af` |

## Resolved findings

- `a06-final-pipeline:1`, formerly P1 at line 440: `path_entry` now retains trailing-directory intent in its comparison key at lines 86–87, after resolving the original path. C12 therefore checks descendants under `scripts/` before granting coverage. The regression rejects escaping paths for `scripts/*.py`, `scripts/` and `scripts/**` on both runtimes. The directory/child valid-control test remains green.
- `a06-final-pipeline:2`, formerly P2 at line 387: C10 now extracts the original non-delimited script spelling at line 389, including combining marks, before calling `path_entry`. The new regression rejects NFD and NFC paths pointing outside and accepts confined files in both spellings on both runtimes.

Inspected the repairs in the connected checker previously reviewed in full, including the pipeline callers, original-path confinement, normalized row identity, collision refusal and C16 resolved-target classification. No new substantive finding. Collision keys still come from enumerated file paths; directory markers are scope metadata and do not replace original filesystem operands. Distinct enumerated names still collide even when their resolved target is identical, while repeat enumeration of the identical path is deduplicated.

## Independent validation

`independent-repair-verification-commands.json` contains the exact expanded argv arrays, working directory, relevant environment, runtime executable SHA-256 values, source/test/task bindings, log names and actual exits. Each command invokes the validated absolute Python binary with `-I`; its inline bootstrap inserts only the absolute test root and runs the named real-CLI fixture selectors. No helper file was created.

Both interpreter version probes used `<absolute-runtime> -I --version` and exited 0, printing `Python 3.15.0` and `Python 3.12.15`.

| Runtime | Tests | Result | Exit | Complete captured output |
| --- | --- | --- | --- | --- |
| Python 3.15.0 | 10 | OK, one native collision subtest skipped | 0 | `independent-repair-verification-3.15.0.log` |
| Python 3.12.15 | 10 | OK, one native collision subtest skipped | 0 | `independent-repair-verification-3.12.15.log` |

Selectors, all in `TaskConsistencyC11C15Test`:

- `test_path_grammar_rejects_escaping_scopes`
- `test_c10_confines_original_unicode_script_paths`
- `test_path_grammar_separates_directory_and_child_rows`
- `test_path_grammar_normalises_dot_spellings`
- `test_canonical_path_pipeline_preserves_identity`
- `test_canonical_path_pipeline_rejects_normalised_collisions`
- `test_security_c12_prunes_with_normalised_directory_names`
- `test_security_c12_resolves_original_unicode_path`
- `test_security_c12_rejects_internal_directory_alias`
- `test_security_c16_uses_resolved_literal_alias`

Both runs observed `native-NFC-NFD-distinct=False`. The native two-file collision subtest skipped with the explicit samefile-alias reason; the modeled distinct-file and same-target collisions, one-file coverage and overlap control ran. This does not establish native behavior on a normalization-sensitive filesystem.

The read-only measurement command `git diff --numstat 60a6fb2b -- scripts/orchestrator/task-consistency-check.py tests/unit/test_task_consistency_c11_c15.py tests/unit/test_task_checkers.py` exited 0:

```text
415 27 scripts/orchestrator/task-consistency-check.py
35  22 tests/unit/test_task_checkers.py
643 0  tests/unit/test_task_consistency_c11_c15.py
```

Production 442 and tests 700 fit the amended task's 450/720 caps.

The parent's historical-red claims were not independently rerun during this repair verification. Full modules, mutations, lint, CI, live API checks and the gate remain with the parent/orchestrator. No source/test edits, network, Bats, browser, deployment or integration actions were performed. Existing parent-execution, credentials and same-UID residual risks remain unchanged.

Verdict: correct
