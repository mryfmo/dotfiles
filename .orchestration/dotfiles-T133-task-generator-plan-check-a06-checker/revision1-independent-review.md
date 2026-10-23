# Independent revision review

Reviewed the R1/R2 implementation against `b8bf806655496b7a897aea25e1b43319095fac23`, the connected checker code and test fixtures, and the current revision narrative in `report.md` and `validation.md`. No new code defect found. This review resolves the two implementation issues on the bound bytes below; it is not final-head task audit, full task acceptance, CI certification or merge approval.

The root security addendum and explicit CI green remain pending according to the supplied revision state. Any later source change needs a new binding and review.

## Bound bytes

| File | SHA-256 |
| --- | --- |
| `scripts/orchestrator/task-consistency-check.py` | `dd44ae3415ee7e6d6b0c3ca39782bdecac4fb0f9f44a69b69b601f4022e62187` |
| `tests/unit/test_task_consistency_c11_c15.py` | `57b3887a9d9d0854c838ea0e384a6228ea8855c0533bb3eedf524775598c0de3` |
| `tests/unit/test_task_checkers.py` | `20eff6f4cf0cbdb55da3f1265edaec6a3479f238a08a7ef36abfe03a8968e99f` |
| a06 `task.md` | `b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af` |

Before/after bindings remained identical during both independent test runs.

## Verified resolutions

- **R1, checker lines 37 and 138–143:** an unset cache no longer rejects module import. Launch rejects explicitly supplied relative or empty values, retains an absolute supplied cache, and uses its existing private temporary directory as the child cache when unset. The context manager cleans up the fallback directory. The independent real-CLI regression passed with cache unset, checked the fake-gh child's absolute cache path and its removal, and rejected a relative value. Existing controls also exercised the supplied absolute-cache launch path. Executable validation precedes the launch; token forwarding and sanitized Git child environment remain unchanged.
- **R2, checker line 479:** regular-file classification uses the already-confined resolved target. Collision registration still retains original enumerated names, independent of alternate spelling existence. The strengthened deterministic fixture forces the NFC alternate's `exists()` and `is_file()` to be false, yet requires the one-file wrong-target case to fail without a collision finding. It also retains distinct-target/same-target collision refusal, valid single-file coverage and overlapping-scope controls. These modeled controls passed independently on both runtimes.

The resolved-target change adds no pathname normalization before confinement and no second target selection. Raw-path diagnostics, directory-alias refusal and target-based exemptions remain. Prior Unicode, trailing-directory and backslash-filename protections passed again among the selected controls.

## Independent commands and results

`revision1-independent-commands.json` contains exact expanded argv arrays, cwd, relevant environment, executable hashes, before/after source/test/task bindings, actual exits and output filenames. Each subprocess uses the validated absolute native interpreter with `-I`, inserts only the absolute test root and runs the named real-CLI fixture selectors. The driver exited 0 after both test processes succeeded and all bindings stayed unchanged.

| Runtime | Observed result | Actual exit | Complete stdout/stderr |
| --- | --- | --- | --- |
| Python 3.15.0 | 8 tests, OK, one native collision subtest skipped | 0 | `revision1-independent-3.15.0.log` |
| Python 3.12.15 | 8 tests, OK, one native collision subtest skipped | 0 | `revision1-independent-3.12.15.log` |

Methods of `TaskConsistencyC11C15Test`:

- `test_private_cache_when_unset`
- `test_canonical_path_pipeline_rejects_normalised_collisions`
- `test_checker_rejects_untrusted_bindings_and_git_configuration`
- `test_gh_child_preserves_parent_tokens`
- `test_canonical_path_pipeline_preserves_identity`
- `test_path_grammar_rejects_escaping_scopes`
- `test_c10_confines_original_unicode_script_paths`
- `test_c12_classifies_backslash_filenames_from_resolved_ancestry`

The only skipped subtest is the native two-file NFC/NFD collision case: this filesystem reported the two names as aliases. The deterministic absent-alternate and wrong-target cases ran. This does not establish native Linux coverage.

## Acceptance limits and reporting integrity

Read the corrected R3 narrative: the six earlier candidate-only failures are now attributed to this task's R1, and the previous inherited/#441 attribution is withdrawn. The current report makes no CI-green claim. This review does not independently certify the historical runs, the five RegimeCi methods, mutation totals, the full candidate-minus-base comparison or actual GitHub CI.

Independently measured the relevant files with `git diff --numstat 60a6fb2b -- scripts/orchestrator/task-consistency-check.py tests/unit/test_task_consistency_c11_c15.py tests/unit/test_task_checkers.py` (exit 0): source 417 + 27 = 444; checker tests 35 + 22 + 663 = 720.

Also ran `git diff --numstat 60a6fb2b -- tests/` (exit 0). It additionally reports `tests/unit/test_regime_ci.py` at 6 additions + 5 deletions. Therefore the **complete fixed-base test diff is 731**, not 720. The worker-authored/inherited split does not itself establish compliance with the task's literal complete-diff cap. This existing acceptance limitation was reported to the parent and remains outside this scoped implementation approval.

No source/test changes, network, browser, Bats, commit, gate or integration action. Parent execution, credentials, supplied shared caches and same-UID interference remain residual risks; a private fallback child cache does not establish pre-start isolation. This is local review process evidence, not reviewer authentication.

Verdict: correct
