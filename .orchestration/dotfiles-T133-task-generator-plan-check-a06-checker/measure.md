# Complete final worker-round2 measurement

Fixed base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
Continuation/transport head: b8bf806655496b7a897aea25e1b43319095fac23
PR: https://github.com/mryfmo/dotfiles/pull/440
Branch: tools/task-generator-plan-check-a05-checker

Production: checker419 additions +27 deletions =446/450 changed lines.
ALL tests: new module652 additions +legacy35 additions +22 deletions +owner-authorized upstream test_regime_ci.py6 additions +5 deletions =720/720 changed lines. Worker-allowed test subtotal709 plus upstream11; all11 are counted, no exclusion or cap amendment.

The complete fixed-base diff below includes all 474 paths: retained a05 files, a06 artifacts, the three checker/test paths and25 owner-authorized upstream paths. D5 has161 committed files unchanged from06ffefbc633fe37bcef107385ea96810b2a9a0c5;25 imported paths remain byte-identical to762a2541f422b691199cb42fbbd1588604042ad2. No a01-a04 import/deletion, unrelated untracked path, cache or timestamp worklog is selected. No executable/helper is placed under artifacts; all a06 artifact modes0644.

Measured with git diff --cached --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e and git diff --cached --name-only 60a6fb2b324d0381c4a6e539b37c650105154a7e. After commit verify exact equality using git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...<full-head40> and git diff --name-only 60a6fb2b324d0381c4a6e539b37c650105154a7e...<full-head40>. Full head is sent in PONG, avoiding a self-referential commit hash. full-diff-inventory.json is the parsed complete inventory, including itself and this measure.

Task copy SHA256:b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af; byte-identical amended dispatch,240 author lines plus6 appended Checks, four allowed entries. Source/test hashes are revision1-final-bindings.json. Fixture consolidation preserves104 assertion-call AST multiplicities in the independent final review; no defense/assertion deleted.

## Complete numstat

```
30	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/dotfiles-T133-regime-ci-fixture-grammar-a01-worker-crit.json
21	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/dotfiles-T133-regime-ci-fixture-grammar-a01-worker-review-receipt.md
10	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/learning.md
67	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/report.md
31	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/sandbox.md
66	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md
258	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/validation.md
6	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/learning.md
31	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/report.md
23	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/sandbox.md
76	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md
70	0	.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/validation.md
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-markdown-format-final.log
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-markdown-format.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-python-format-final.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-python-format.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/autoskill.md
117	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-assets.log
443	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-format.log
5518	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-unit-final.log
5518	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-unit.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-assets-masked.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-assets.log
1969	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-format.log
5657	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-unit-final.log
130	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-clean-assets.log
128	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-evidence-mask.log
22	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-commands.json
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-lint.log
42	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-modules312.log
41	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-modules315.log
194	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations.json
552	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations.log
194	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations312.json
516	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations312.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-scope.log
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-lint-green.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-mask-launch-invalid.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-modules312.log
32	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-modules315.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-mutations.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-native312-binding.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-postcommit-push-blocker.md
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-red.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-bindings.json
109	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-blocker.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-rebuild.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-worker-gate.log
118	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/clean-candidate-assets.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/crit-status.json
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/diff-check.log
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dispatched-copy-checker.log
105	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dotfiles-T133-task-generator-plan-check-a05-checker-worker-crit.json
20	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dotfiles-T133-task-generator-plan-check-a05-checker-worker-review-receipt.md
699	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules.log
180	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules2.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules3.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules4.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules5.log
100	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/evidence-mask.log
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-dispatched-copy-checker.log
245	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-historical-red312.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-historical-red315.log
21	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-inventory-bindings.log
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-local-validation.md
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-modules-green312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-modules-green315.log
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-preimplementation-bindings.log
245	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-preimplementation-red312.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-preimplementation-red315.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-source-bindings.log
245	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/frozen-historical-red312.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/frozen-historical-red315.log
5069	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/graph-freshness.log
62	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-r4-review-transcript.md
42	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-review-transcript.md
63	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-revise1-review-transcript.md
29	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-security-review-transcript.md
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-red-bindings.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-sixteen-red.log
243	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-sixteen-red312.log
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/learning.md
349	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/measure.md
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/module-green-bindings.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/modules-green312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/modules-green315.log
186	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-final.json
535	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-final.log
194	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-round2.json
552	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-round2.log
194	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-scanner-fixed.json
552	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-scanner-fixed.log
162	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations.json
454	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/open-security-note.md
7	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/post-stage-blocker.md
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/postpublication-transport-2761.md
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/pr-body.md
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/precommit-assets.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-435.json
1130	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-design.base64
113	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-design.md
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-design.sha256
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-grep.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-main.sha
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/publication-bot-observations.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/publication-findings.md
62	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/publication-observations.json
32	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/regime-caller-probe.log
71	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/report.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/required-selectors.json
359	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/result-cedc7f5f.md
76	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red-valid.log
24	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red.log
58	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-red.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-check-commands.json
130	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-clean-assets.log
48	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-commands.json
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-final-bindings.log
60	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-final-security-red312.log
61	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-final-security-red315.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-format.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-green-commands.json
249	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-historical312.log
271	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-historical315.log
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-lint.log
157	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mask.log
45	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-modules312.log
44	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-modules315.log
226	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations312.json
602	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations312.log
226	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations315.json
640	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations315.log
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-red-commands.json
62	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-security-findings.json
59	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-security-red312.log
62	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-security-red315.log
7	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-source-bindings.json
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-source-diff-check.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-worker-gate.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round1-modules-green312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round1-modules-green315.log
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-diff-check.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-final-bindings.log
245	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-historical-red312.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-historical-red315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-modules-green312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-modules-green315.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-scoped-python-format.log
63	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/sandbox.md
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-assets.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-bindings.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-format.log
245	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-historical312.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-historical315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-modules312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-modules315.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scoped-python-format.log
469	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scoped-ruff-lint-initial.log
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/secret-scanner-diagnostic.log
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/source-diff-check-final.log
254	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task-dispatch-amendment1.md
251	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task-dispatch-initial.md
255	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/token-argv-red.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/unit-comparison.json
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/unit-comparison.log
432	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation-commands.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation-scope.md
39325	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation.md
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate-round2.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate-scanner-fixed.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/autoskill.md
7	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-evidence-integrity.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-batch-pong.md
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-pong.md
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-report.md
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/c3-compatibility-observation.json
28	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-initial-red312.log
28	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-initial-red315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-red-commands.json
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/crit-status.json
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/crit-status.stderr
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/current-measure.json
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-command.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-copy-rows-command.json
28	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-copy-rows.log
31	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline.log
24	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-grammar-red312.log
26	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-grammar-red315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-red-commands.json
177	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-all-mask.log
216	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-artifact-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-artifact-privacy.json
165	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-closed-mask.log
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-code-diff-check.json
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-code-diff-check.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-diff-check.json
654	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-diff-check.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-commands.json
78	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red312.json
432	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red312.log
78	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red315.json
466	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red315.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-module-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-legacy315.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-new312.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-new315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutation-commands.json
322	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations312.json
834	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations312.log
322	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations315.json
886	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations315.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-binding.json
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-module-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-legacy315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-new312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-new315.log
189	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-privacy-mask.log
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-production-r4.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-python-format.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-r4-lint.log
13	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-scope-integrity.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-source-binding.json
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-static-commands.json
23	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-task-table-validation.json
54	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-tool-bindings.json
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-module-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-legacy315.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-new312.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-new315.log
26	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/formatter-tool-bindings.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-binding.json
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-commands.json
78	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red312.json
432	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red312.log
78	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red315.json
466	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red315.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-module-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-legacy315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-new312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-new315.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-module-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-legacy315.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-new312.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-new315.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-source-binding.json
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-base-prepare.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-candidate-prepare.log
2897	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-diff-inventory.json
444	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-base.log
444	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-candidate.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-commands.json
111	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-suite-snapshot-bindings.json
6061	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-base.log
6297	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-candidate.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-commands.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-comparison-command.json
2857	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-comparison.json
31	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review-repro.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review.json
80	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review.md
23	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-3.12.15.log
23	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-3.15.0.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-commands.json
32	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification.json
67	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification.md
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-3.12.15.log
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-3.15.0.log
53	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-commands.json
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-review.json
31	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-review.md
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-lint-adjustment-review.json
53	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-lint-adjustment-review.md
19	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-3.12.15.log
19	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-3.15.0.log
46	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-commands.json
24	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification.json
62	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification.md
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-3.12.15.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-3.15.0.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-commands.json
32	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-review.json
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-review.md
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/learning.md
40	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-c12-diagnostic.log
72	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-initial-diagnostic.log
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocked-pong.md
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocker.md
88	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-before-new-P2-hold.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-current-evidence.log
973	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/measure.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/module-commands.json
26	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-legacy312.log
50	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-legacy315.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-new312.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-new315.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-measure.json
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-pong.md
7	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-stop.md
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red-commands.json
41	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red312.log
44	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red315.log
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-mask.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-red-commands.json
41	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-repair-red312.log
44	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-repair-red315.log
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-ci-r4-lint.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red-commands.json
26	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red312.log
27	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red315.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/post-repair-source-binding.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/pre-green-source-binding.json
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-format.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-module-commands.json
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-legacy315.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-new312.log
37	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-new315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-r4-lint.log
25	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report-before-final-revision.md
23	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/required-selectors.json
13	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/reset-provenance.json
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/result-before-final-revision.txt
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-command.json
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-reproduction.log
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise.yaml
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-blocked-report.md
58	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red312.log
61	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red315.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-mask.log
47	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-measure.json
7	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-pong.md
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-red-commands.json
22	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-replan.md
51	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-command.json
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-prepare.log
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-result.json
125	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets.log
270	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-closed-mask.log
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-code-diff-check.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-current-bindings.json
999	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-artifact-commands.json
19	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-artifact-privacy.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-bindings.json
21	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-format-command.json
444	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-format.log
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-prepare.log
55	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-suite-snapshot.json
6183	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-candidate.log
5043	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-comparison.json
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-exit.json
102	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical-red312.json
102	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical-red315.json
29	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312-command.json
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312-exit.json
581	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312.log
29	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315-command.json
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315-exit.json
619	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315.log
25	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-3.12.15.log
25	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-3.15.0.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-commands.json
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-consolidation.json
32	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-review.json
79	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-review.md
562	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mask.log
282	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mask2.log
22	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-module-commands.json
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-legacy312.log
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-legacy315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-new312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-new315.log
290	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutation-preflight.json
28	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312-command.json
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312-exit.json
386	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312.json
995	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312.log
28	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315-command.json
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315-exit.json
386	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315.json
1056	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315.log
271	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-observations.json
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-production-r4.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-python-format.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green-commands.json
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green312.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red-commands.json
34	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red312.log
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime-commands.json
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime312.log
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime315.log
80	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-fixture-consolidation.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-prepare.log
55	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-suite-snapshot.json
6184	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-unit-candidate.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-unit-exit.json
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green-commands.json
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green312.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green315.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-3.12.15.log
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-3.15.0.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-commands.json
24	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-review.json
57	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-review.md
266	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-mutation-preflight.json
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-pre-red-bindings.json
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-production-r4.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red-commands.json
26	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red312.log
27	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red-commands.json
36	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red315.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime-commands.json
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime312.log
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-gate-commands.json
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-reviewed-gate.log
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-unreviewed-gate.log
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/sandbox.md
51	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets-command.json
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets-result.json
119	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets.log
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-initial-preparation.json
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-prepare.log
34	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-commands.json
322	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations312.json
842	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations312.log
322	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations315.json
895	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations315.log
188	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-results.json
432	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-historical-red312.log
466	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-historical-red315.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-legacy312.log
17	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-legacy315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-new312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-new315.log
246	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task-initial-90ca0ae9.md
246	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md
11	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/transport-merge-hold.md
1976	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/transport-merge-verification.json
42	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation-before-final-revision.md
64	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-gate-commands.json
98	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-evidence.json
12	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-receipt.md
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-reviewed-gate.log
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-unreviewed-gate.log
6	6	.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
225	0	.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
1	3	.orchestration/tasks/dotfiles-T133-loop-limits-a01.md
99	0	.orchestration/tasks/dotfiles-T133-pre-send-check-a01.md
200	0	.orchestration/tasks/dotfiles-T133-python-pin-a01.md
183	0	.orchestration/tasks/dotfiles-T133-python-pin-a02.md
66	0	.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
76	0	.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a02.md
255	0	.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a05-checker.md
246	0	.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md
1	0	.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
655	0	.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
419	27	scripts/orchestrator/task-consistency-check.py
6	5	tests/unit/test_regime_ci.py
35	22	tests/unit/test_task_checkers.py
652	0	tests/unit/test_task_consistency_c11_c15.py
```

## Complete changed-file list

```
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/dotfiles-T133-regime-ci-fixture-grammar-a01-worker-crit.json
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/dotfiles-T133-regime-ci-fixture-grammar-a01-worker-review-receipt.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/learning.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/report.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/sandbox.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/task.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a01/validation.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/learning.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/report.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/sandbox.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/task.md
.orchestration/dotfiles-T133-regime-ci-fixture-grammar-a02/validation.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-markdown-format-final.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-markdown-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-python-format-final.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/all-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/autoskill.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-unit-final.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/base-unit.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-assets-masked.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/candidate-unit-final.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-clean-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-evidence-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-modules312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-modules315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-final-scope.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-lint-green.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-mask-launch-invalid.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-modules312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-modules315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-mutations.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-native312-binding.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-postcommit-push-blocker.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-red.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-blocker.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-rebuild.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-worker-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/clean-candidate-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/crit-status.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dispatched-copy-checker.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dotfiles-T133-task-generator-plan-check-a05-checker-worker-crit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dotfiles-T133-task-generator-plan-check-a05-checker-worker-review-receipt.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules2.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules3.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/draft-two-modules5.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/evidence-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-dispatched-copy-checker.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-inventory-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-local-validation.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-modules-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-modules-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-preimplementation-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-preimplementation-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-preimplementation-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/final-source-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/frozen-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/frozen-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/graph-freshness.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-r4-review-transcript.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-review-transcript.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-revise1-review-transcript.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-security-review-transcript.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-red-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-sixteen-red.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-sixteen-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/learning.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/measure.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/module-green-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/modules-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/modules-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-final.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-final.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-round2.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-round2.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-scanner-fixed.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations-scanner-fixed.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/mutations.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/open-security-note.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/post-stage-blocker.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/postpublication-transport-2761.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/pr-body.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/precommit-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-435.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-design.base64
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-design.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-design.sha256
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-grep.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/prerequisite-main.sha
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/publication-bot-observations.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/publication-findings.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/publication-observations.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/regime-caller-probe.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/required-selectors.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/result-cedc7f5f.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red-valid.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-red.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-check-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-clean-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-final-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-final-security-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-final-security-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-green-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-historical312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-historical315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-modules312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-modules315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-security-findings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-security-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-security-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-source-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-source-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/revise1-worker-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round1-modules-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round1-modules-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-final-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-modules-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-modules-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-scoped-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/sandbox.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-bindings.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-historical312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-historical315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-modules312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scanner-fixed-modules315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scoped-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/scoped-ruff-lint-initial.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/secret-scanner-diagnostic.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/source-diff-check-final.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task-dispatch-amendment1.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task-dispatch-initial.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/token-argv-red.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/unit-comparison.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/unit-comparison.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation-scope.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation.md
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate-round2.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate-scanner-fixed.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/autoskill.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-evidence-integrity.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-batch-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/blocked-review-report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/c3-compatibility-observation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-initial-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-initial-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/collision-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/crit-status.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/crit-status.stderr
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/current-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-copy-rows-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline-copy-rows.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/dispatched-copy-offline.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-grammar-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-grammar-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/escape-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-all-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-artifact-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-artifact-privacy.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-closed-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-code-diff-check.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-code-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-diff-check.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutation-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-owner2809-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-privacy-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-production-r4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-r4-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-scope-integrity.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-static-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-task-table-validation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-tool-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/final-verified-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/formatter-tool-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/frozen-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-base-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-candidate-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-diff-inventory.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-base.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-format-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-suite-snapshot-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-base.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-comparison-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-unit-comparison.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review-repro.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-final-verification.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-finding-assertion-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-lint-adjustment-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-lint-adjustment-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-repair-verification.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/independent-test-strengthening-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/learning.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-c12-diagnostic.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-initial-diagnostic.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocked-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocker.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-before-new-P2-hold.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-current-evidence.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/measure.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-cap-stop.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-frozen-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-repair-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2802-repair-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-ci-r4-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/owner2809-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/post-repair-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/pre-green-source-binding.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/repaired-r4-lint.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report-before-final-revision.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/required-selectors.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/reset-provenance.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/result-before-final-revision.txt
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-reproduction.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise.yaml
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-blocked-report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-replan.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets-result.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-closed-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-code-diff-check.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-current-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-artifact-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-artifact-privacy.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-format-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-suite-snapshot.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-comparison.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-full-unit-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical-red312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical-red315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-historical315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-consolidation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-independent-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mask2.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-module-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutation-preflight.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-observations.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-production-r4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-python-format.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-r4-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-final-regime315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-fixture-consolidation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-suite-snapshot.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-unit-candidate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-full-unit-exit.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-green315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-3.12.15.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-3.15.0.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-review.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-independent-review.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-mutation-preflight.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-pre-red-bindings.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-production-r4.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-r4-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-regime315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-gate-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-reviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revision1-worker-unreviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/sandbox.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets-result.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-assets.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-initial-preparation.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/selected-tree-prepare.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations312.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations315.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-mutations315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-final-results.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-historical-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-historical-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-legacy312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-legacy315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-new312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/strict-frozen-final-modules-new315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task-initial-90ca0ae9.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/task.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/transport-merge-hold.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/transport-merge-verification.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation-before-final-revision.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-gate-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-evidence.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-receipt.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-reviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-unreviewed-gate.log
.orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a07.md
.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-followup-a04.md
.orchestration/tasks/dotfiles-T133-loop-limits-a01.md
.orchestration/tasks/dotfiles-T133-pre-send-check-a01.md
.orchestration/tasks/dotfiles-T133-python-pin-a01.md
.orchestration/tasks/dotfiles-T133-python-pin-a02.md
.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a01.md
.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a02.md
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a05-checker.md
.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md
.orchestration/tasks/dotfiles-T133-trusted-exec-contract-tests-a01.md
.orchestration/tasks/dotfiles-T133-worker-write-boundary-a03.md
scripts/orchestrator/task-consistency-check.py
tests/unit/test_regime_ci.py
tests/unit/test_task_checkers.py
tests/unit/test_task_consistency_c11_c15.py
```
