# Exact final worker-round2 validation

Source/test bindings: revision1-final-bindings.json. Final sourcef43de893ab5f7d3d68bac6be5cf8c04c6e33d4303bd38e6eab56dc2726880800, new testbe102aab7c88dc74f3be5019005992f53485b0a8ed3addcb8abb4decb338dbe1; legacy20eff6f4 remains unchanged. All results below are actual process exits, with full expanded commands and verbatim output in the named artifacts. Root security addendum was received; RESULT still requires explicit final-head ci=green.

## Complete checker and unchanged caller proofs

revision1-final-module-commands.json and revision1-final-modules-{new,legacy}{315,312}.log: each native3.15.0/3.12.15 passes29 new+10legacy tests, all four actual exits0. Only the native Unicode two-file subcase skips because this host observed NFC/NFD aliasing. Modeled absent-alternate, distinct/same-target collision, wrong-row, one-file and overlap cases execute; no native Linux claim.

revision1-final-regime-commands.json and revision1-final-regime315/312.log: unchanged5RegimeCi methods covering6 prior CI failure subcases pass on both runtimes, actual0,0failures/errors/skips. test_regime_ci.py is byte-identical to the imported upstream file.

## Red before repair and historical controls

Initial R1/R2 reds use frozen42183ecc: revision1-red-commands.json and logs show2tests/2assertfail/0error/0skip on each runtime, driver exits0. R4 reds use dd44ae34 with cache/type fixes only: revision1-final-r4-red-commands.json and logs show2tests/2assertfail/0error/0skip on each runtime, driver exits0. Final R4 greens use exactf43/be10: both2methods pass with0error/skip and exits0, including correct NFD receipt/hash/invariant and raw directory-child controls.

The final tests were also rerun against all historical source snapshots; every named method fails behaviorally with no import/error/skip. Complete executed argv/env/code is in revision1-final-historical315/312-command.json; full output in revision1-final-historical315/312.log; captured JSON in revision1-final-historical-red315/312.json. Drivers actually exit0. Their reused old JSON basename was copied to these revision files after completion, and the old historical basename was restored byte-identical fromb8; the command records disclose that capture step.

| Source group, each runtime | Tests | Assertion failures | Errors | Skips |
| --- | --- | --- | --- | --- |
| historical16 | 16 | 18 | 0 | 0 |
| security-cedc7f5 | 3 | 3 | 0 | 0 |
| security-06ffefb | 4 | 4 | 0 | 0 |
| review-5c09a95a | 2 | 2 | 0 | 0 |
| review-1779440f | 1 | 1 | 0 | 0 |
| revision1-R1-R2 | 2 | 2 | 0 | 0 |
| revision1-R4 | 2 | 2 | 0 | 0 |

## Mutation sensitivity

revision1-final-mutations315/312-command.json contains the exact48 cases and execution code; logs and JSON retain each id/selector/mutant SHA/outcome. Each runtime: mutations=48 killed=48 survived=0, actual driverexit0. Every kill is an assertion failure, one selected test, no error/skip. Controls retain the prior40 and add cache absence/private cleanup/relative refusal/supplied absolute honor, resolved classification, original design/request/child spelling. Mutants and runners exist only inTMP; command records are data.

Expected FAILED footers in red/mutation logs are negative child observations, never claimed as passing suites. revision1-final-observations.json consolidates actual exits/results.

## Corrected R3 historical delta

Owner2827 reported actual GitHub Unit-test run39402138504:7failures of1296 on all3Linux jobs. Macos14 skips unit tests for the Python-only diff, so its success is no unit-test evidence. Six are R1; the seventh is R2. No worker GitHub read is claimed.

Prior local base1267/150fail/128error/3skip and candidate1295/156fail/128error/4skip both exited2. The278 base failure/error tuples retain exact multiplicity, but the6 added tuples below are our checker R1. Prior attribution to #441 was wrong and is withdrawn:
- test_regime_ci_accepts_a_base_that_moved_past_the_merge_base (test_regime_ci.RegimeCiTest.test_regime_ci_accepts_a_base_that_moved_past_the_merge_base); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) (reset_of=True, predecessor_copy_kept=False); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage (test_regime_ci.RegimeCiTest.test_regime_ci_checks_only_the_latest_copy_of_a_reset_of_lineage) (reset_of=True, predecessor_copy_kept=True); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier (test_regime_ci.RegimeCiTest.test_regime_ci_reads_the_head_as_data_and_runs_the_base_verifier) (expected=0, phrase=None); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr (test_regime_ci.RegimeCiTest.test_regime_ci_reports_each_violation_once_and_passes_a_consistent_pr); multiplicity=1; cause=R1 import-time cache refusal.
- test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config (test_regime_ci.RegimeCiTest.test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config); multiplicity=1; cause=R1 import-time cache refusal.

The old report/validation remain explicitly historical. The dd44/test57b full candidate started before R4 was interrupted as obsolete; revision1-full-unit-exit.json marks it incomplete. It is not a final suite or comparison proof.

## Final candidate-minus-base comparison

COMPLETE with actual observed make exit2. revision1-final-full-suite-snapshot.json binds clean snapshot689cd97a61f002bb72f09f8e040039c5b7bd06b6 to finalf43/be10 bytes and exact argv/environment. revision1-final-full-unit-candidate.log/exits:1296 tests in1090.406s,150failures,128errors,4skips. Unchanged fixed60 baseline full-unit-base.log/full-unit-commands.json:1267 tests in842.479s,150failures,128errors,3skips, actual exit2. Same validated native315/offline environment, private cache paths differ. Additional skip is the disclosed native Unicode alias subcase.

Exact candidate-minus-base test-name/multiplicity tuples: `[]` (zero added occurrences).
Exact base-minus-candidate test-name/multiplicity tuples: `[]` (zero removed occurrences).

revision1-final-full-unit-comparison.json preserves all278 baseline and278 candidate failure/error tuple occurrences, unique tuple counts and both Counter differences. Parser uses only unittest70-equals/FAIL-or-ERROR/70-hyphens headers, retains repeated subcases, and asserts header counts match footer failure/error totals. It does not count bare fixture ERROR diagnostics. revision1-final-artifact-commands.json records the exact executed parser code/argv and actual exit0. This is an exact local baseline comparison, not a green full suite, native Linux run or final-head GitHub CI. The previous6 added failures were our R1 and are gone after the repair; the prior inherited attribution remains withdrawn.

## Format, lint, review and gate

Changed Python Ruff format check exits0. Production-only CI-style R4 lint exits0 in revision1-final-production-r4.log;5 inherited warnings in unchanged regime-ci.py remain outside scope. Full make format on the exact final snapshot exits2 at inherited shfmt differences; entire output is byte-identical to unchanged baseline, recorded in revision1-final-format-command.json/log. No lint baseline or assertion is weakened.

Read independent final MD/JSON, exact commands, both16-test runtime logs and consolidation proof. Each runtime exit0 with one disclosed native alias subtest skip; source/test/task hashes unchanged. All104 assertion-call AST multiplicities survive reversal of29 fixture-consolidation lines. Original intermediate consolidation record is not misrepresented as final-byte equivalence; later raw-API/cache controls are separately reviewed.

worker-review-evidence.json and worker-review-receipt.md bind the final resolved R1/R2/security:b8bf806:1 records. revision1-worker-gate-commands.json: unreviewed gate exits2 requesting review, saved/read Crit-data reviewed gate exits0. Independent process review is not final-head CI/task audit/acceptance.

Selected-tree make validate-agent-assets completed with actual exit0, log revision1-assets.log ending agent asset validation ok, metadata revision1-assets-command.json/result.json. It uses a clean selected tree with exact final source/test bytes; final data-only additions receive a canonical privacy scan. Final canonical privacy verification exits0:285 selected a06 artifacts,0secret matches,0home-path matches, all JSON parses and all artifact modes0644. revision1-final-artifact-privacy.json binds the final source/test/task and canonical validator hash. Initial newly written command metadata needed a further canonical mask; the attempt is disclosed in revision1-final-artifact-commands.json. Original task copies were scanned without rewriting. No local Bats, browser Crit, network, push or escalation. Task copy staysb9e; root owns canonical publication/recordsPR444 and applicable final-head CI/Bot/audits/feedback/acceptance/integration. RESULT requires explicit rootci=green.
