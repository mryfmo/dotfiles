# Validation of frozen final bytes

Source/test SHA256 bindings: frozen-final-binding.json. Full expanded commands: strict-final-commands.json; actual exits and per-mutant/group results: strict-final-results.json. Native tools are validated absolute non-shim bindings, isolated Python and offline private caches; no live API authority is inferred from fixtures.

| Proof | Python 3.15.0 | Python 3.12.15 |
| --- | --- | --- |
| Complete new checker module | 28 tests, OK, one native collision subtest skip, exit 0 | 28 tests, OK, one native collision subtest skip, exit 0 |
| Complete legacy checker module | 10 tests, OK, exit 0 | 10 tests, OK, exit 0 |
| Historical 7a201eab16 selectors | 16 tests, 18 assertion failures, 0 errors/skips | same |
| cedc7f5 three security selectors | 3 tests, 3 assertion failures, 0 errors/skips | same |
| 06ffefbc security/pipeline/collision selectors | 4 tests, 4 assertion failures, 0 errors/skips | same |
| Reviewed 5c09a95a directory/C10 selectors | 2 tests, 2 assertion failures, 0 errors/skips | same |
| Reviewed 1779440f backslash classifier selector | 1 test, 1 assertion failure, 0 errors/skips | same |
| Strict mutation controls | mutations=40 killed=40 survived=0 | mutations=40 killed=40 survived=0 |

All historical drivers actually exited 0 after requiring behavioral assertion failures for every named selector, with zero errors/skips. FAILED footers in red/mutation logs are expected child results, not passing suites or hidden infrastructure failures. Mutants were created only in TMP, are compiled individually, and each kill has an assertion failure with no error/skip. No runtime helper or mutation framework is committed.

Complete final outputs: strict-frozen-final-modules-{new,legacy}{315,312}.log, strict-frozen-final-historical-red{315,312}.log and strict-final-mutations{315,312}.log. JSON results include every mutant id, selector and mutant hash. required-selectors.json preserves all 16 required contract fixtures; historical group JSON maps additional security/review fixtures to exact checker hashes.

Initial failed attempts remain visible: seed-cache concurrency was isolated with private caches; final-mutations315/312 show the 39/40 trial in which a C6 warning satisfied an overly broad assertion. The final test requires the actual finding-line prefix and kills all 40. No product assertion was removed. The independent reviewer reconstructed the previous test hash by reversing that sole strengthening, and reran its selector on both runtimes.

The host's NFC/NFD spellings refer to the same native file. Only the genuine native two-file case skips with this observed reason; modeled distinct-entry and same-target collisions, single-file coverage, overlapping-scope deduplication and wrong-row identity controls run.

The exact dispatched task bytes passed the offline real CLI (exit 0), with the required C14 no-trusted-sha warning. A ./ hidden predecessor edit scope failed C2 (exit 1); removing copy mentions failed C3 (exit 1). See dispatched-copy-offline-copy-rows-command.json and .log. Fake canonical responses come from pinned local base files and are labeled fixtures only. The prior own-only-removal experiment remains in dispatched-copy-offline.log: it exits 0 through existing C3 -checker/task.md suffix compatibility, so that driver exits 1 and is not claimed as a passing negative. Owner disposition was requested; actual task metadata contains both explicit copy rows.

Production-only CI-style R4 lint: owner2809-ci-r4-lint.log exit 0; inherited warnings outside allowed scope remain. A supplemental explicit-tests scan in final-r4-lint.log exits 1 on intentional API protocol assertions; CI's default-files excludes tests. No baseline or assertion was weakened. Required full make formatting stopped at inherited shfmt differences on both snapshots (exit 2); byte-for-byte comparison of full-format-base.log and full-format-candidate.log exited 0. Changed Python formatting is checked separately.

Full make unit-test uses clean base/candidate snapshots in full-suite-snapshot-bindings.json and full-unit-commands.json. Candidate production is exact final 42183ecc; its new test is 55c31abd, preceding the single stronger finding-line assertion now 09db2fd0. This comparison therefore is not claimed as a full make run of the exact final test file. Complete final 09db modules, historical controls and mutations above were rerun after the strengthening; root CI must check the committed final head. Full unit statistics and exact failure multiplicity comparison are recorded separately after process completion.

Independent evidence: independent-final-verification.{md,json}, independent-test-strengthening-review.{md,json}, independent-finding-assertion-review.{md,json}; exact independent commands and complete outputs accompany each. worker-review-evidence.json and worker-review-receipt.md consolidate their resolved findings and final approval.

Pending external verification: root transport/CI/Bot, live canonical API check, final-head security/task audit, PR feedback dispositions, acceptance and integration gate. Worker gate and clean selected-tree asset validation are separate local checks and are recorded before local handoff. Local Bats are prohibited and were not run.

## Full-suite baseline comparison

Both full make processes actually exited 2. Base: 1267 tests in842.479s,150 failures,128 errors,3 skips. Candidate:1295 tests in871.916s,156 failures,128 errors,4 skips. Every inherited failure/error tuple retains its exact multiplicity; removed0. The six added FAIL subcases are exactly RegimeCiTest fixtures owned by dotfiles-T133-regime-ci-fixture-grammar-a01/#441. full-unit-comparison.json lists every inherited tuple and each delta; no unexpected failure or error delta exists. Candidate snapshot test55c31abd and final test09db distinction above remains explicit. Full format logs are byte-identical exit2 inherited shfmt differences. Changed Python format and production-only R4 both exit0, recorded in final-static-commands.json. Worker unreviewed gate exit2 requests review; with saved/read resolved JSON and receipt, reviewed gate exit0. These gates confer no PR integration approval.

## Final local gates

Clean selected-tree make validate-agent-assets: actual exit0; selected-tree-assets-result.json binds the selected tree and all three final code hashes. This snapshot precedes result/inventory documentation only. Canonical final privacy validation covers every newly committed evidence file after masking. Initial cache-copy preparation exited1 before any validator ran; new private cache copying preserved dangling symlinks. Worker reviewed gate exit0 is in worker-reviewed-gate.log and worker-gate-commands.json. Supplemental whole-evidence git diff --check exits2 on retained/raw log whitespace; code-only diff check exits0. No forensic output or retained predecessor data is changed to satisfy that diagnostic.

C3 exploratory limitation is preexisting: its complete three-line for-rid/regex/finding block is byte-identical at fixed base60a6fb2b and current source. The actual task contains both rows. Existing short-suffix compatibility was retained under the retain-C3 contract; owner disposition remains external and no patch is silently added. This does not convert the failed own-only-removal fixture to a passing negative.
