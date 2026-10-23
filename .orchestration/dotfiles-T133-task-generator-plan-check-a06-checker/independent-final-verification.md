# Independent final verification

Review date: 2026-10-20. This is independent agent-side process evidence, not reviewer authentication or integration authority.

All three findings reported by this reviewer are resolved on the bytes below. No remaining substantive finding was identified. Previous reports and JSON records are preserved as historical evidence; their verdicts are bound to their own source hashes.

## Final binding

| File | SHA-256 |
| --- | --- |
| `scripts/orchestrator/task-consistency-check.py` | `42183ecc521ae501e705d23a36d3cdb3394298c33eb00b45205a7911092b2d9e` |
| `tests/unit/test_task_consistency_c11_c15.py` | `3d7b31c8782b65e73972e72c18d39f2ed5cf24e52c24eb7c8243fdf6bea0f56a` |
| `tests/unit/test_task_checkers.py` | `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f` |
| a06 `task.md` | `b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af` |

The test driver recorded these bindings before and after both test runs and exited 0 only when they agreed and both test processes succeeded.

## Resolution and inspection

- `a06-final-pipeline:1`: directory markers remain in comparison keys at checker lines 86–87, after original-path resolution. Trailing-slash scopes now reach descendant confinement checks. Their regression and the valid directory/child control passed again on both runtimes.
- `a06-final-pipeline:2`: C10 extracts the original non-delimited script spelling at line 389, preserving combining marks for confinement. NFC/NFD negative and confined controls passed again on both runtimes.
- `a06-lint-adjustment:1`: applied-directory classification at lines 474–476 uses `PurePosixPath` ancestry of the already-resolved comparison name. This retains real POSIX filename characters, including backslashes, without relaxing metadata operand validation or resolving a second pathname. Its new real-CLI regression requires an unnamed extensionless `scripts/evil\name` to fail, then removes that file and requires an ordinary named extensionless file to pass. Both cases passed on both runtimes.

Inspected the final repairs with their connected checker code and callers, using the complete-code review already performed in this thread. Original-path confinement, raw diagnostics, normalized comparison keys, literal scope binding, wildcard row target identity, collision refusal and C16 applicability remain intact. The `prior.parts != file.parts` comparison retains original spelling rather than deduplicating by resolved target. The modeled same-target collision, overlapping-scope deduplication and one-file controls ran successfully. The metadata grammar still rejects backslash operands; its explicit negative control also ran.

The parent reported owner 2809 authorization for this repair within the existing round. This review independently verifies the resulting code and regression; owner acceptance and final integration remain separate.

## Exact commands and observed results

`independent-final-verification-commands.json` records the exact expanded argv arrays, working directory, relevant environment, runtime executable SHA-256 values, before/after source/test/task bindings, output filenames and actual exits. Each process invokes a validated absolute native Python binary with `-I`, inserts only the absolute `tests/unit` root, loads the named selectors through `unittest`, and exits nonzero if any test fails. Its stdout and stderr are saved completely in the corresponding log. No runtime helper file was added.

| Runtime printed by the process | Tests | Actual exit | Complete output |
| --- | --- | --- | --- |
| Python 3.15.0 | 13; OK, one skipped subtest | 0 | `independent-final-verification-3.15.0.log` |
| Python 3.12.15 | 13; OK, one skipped subtest | 0 | `independent-final-verification-3.12.15.log` |

All selectors are methods of `TaskConsistencyC11C15Test`:

- `test_c12_classifies_backslash_filenames_from_resolved_ancestry`
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
- `test_retained_c11_c13_and_fixed_probe_controls`
- `test_path_grammar_distinguishes_globs_from_git_pathspecs`

Both runs observed `native-NFC-NFD-distinct=False`. Only the native two-distinct-file collision subtest skipped because the filesystem aliases those spellings. The deterministic distinct-file and same-target collision models ran; this establishes no native normalization-sensitive filesystem coverage.

The command `git diff --numstat 60a6fb2b -- scripts/orchestrator/task-consistency-check.py tests/unit/test_task_consistency_c11_c15.py tests/unit/test_task_checkers.py` exited 0:

```text
416 27 scripts/orchestrator/task-consistency-check.py
35  22 tests/unit/test_task_checkers.py
652 0  tests/unit/test_task_consistency_c11_c15.py
```

Production 443 and tests 709 fit the amended 450/720 caps.

Historical assertion-red claims, complete modules, mutation testing, lint and final-head CI remain the parent's separately recorded validation; this reviewer does not claim to have rerun them here. No source/test changes, network, browser, Bats, commit, merge or gate action was performed. Existing parent-execution, credentials and same-UID residual risks remain.

Verdict: correct
