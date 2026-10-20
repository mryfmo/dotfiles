# Final measurements

Base/merge-base: 60a6fb2b324d0381c4a6e539b37c650105154a7e. Branch tools/task-generator-plan-check-a05-checker. This full prospective staged inventory is checked against Git now and against actual origin/main...HEAD after commit; authoritative full head/PR is supplied in RESULT without embedding an unknown self hash. Source b91d8d3ae978d394a91ff669db34e2cfafd728c7a2ce4f559dabc48686e2add0; tests unchanged1efd2ebf/20eff6f4.

Command: git diff --numstat origin/main...HEAD

````text
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
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-red.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-bindings.json
109	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-blocker.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-runtime-rebuild.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ci-r4-worker-gate.log
118	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/clean-candidate-assets.log
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/crit-status.json
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/diff-check.log
8	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dispatched-copy-checker.log
87	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dotfiles-T133-task-generator-plan-check-a05-checker-worker-crit.json
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/dotfiles-T133-task-generator-plan-check-a05-checker-worker-review-receipt.md
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
29	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/independent-security-review-transcript.md
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-red-bindings.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-sixteen-red.log
243	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/initial-sixteen-red312.log
14	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/learning.md
293	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/measure.md
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
47	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/report.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/required-selectors.json
76	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red-valid.log
24	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red.log
58	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-red.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round1-modules-green312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round1-modules-green315.log
0	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-diff-check.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-final-bindings.log
245	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-historical-red312.log
268	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-historical-red315.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-modules-green312.log
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-modules-green315.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/round2-scoped-python-format.log
51	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/sandbox.md
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
352	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation-commands.json
5	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation-scope.md
36493	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation.md
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate-round2.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate-scanner-fixed.log
1	0	.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/worker-gate.log
373	24	scripts/orchestrator/task-consistency-check.py
35	22	tests/unit/test_task_checkers.py
527	0	tests/unit/test_task_consistency_c11_c15.py
````

Command: git diff --name-only origin/main...HEAD

````text
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
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red-valid.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-four-red.log
.orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/review-round1-red.log
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
scripts/orchestrator/task-consistency-check.py
tests/unit/test_task_checkers.py
tests/unit/test_task_consistency_c11_c15.py
````

Production: only scripts/orchestrator/task-consistency-check.py373 additions+24 deletions=397<=400. Tests: test_task_checkers.py35add22del plus test_task_consistency_c11_c15.py527add0del;562add<=700,22del. Artifacts contain no executable helper and count toward neither cap. Timestamped plan/todo/learn worklogs are excluded. retained_predecessor_directories: [].

Task copyd0ad49f43aae4be0360cb88339b5d9f23e92e5588d38e3a93a3fbc58a6fe5faa;245 lines before exact Checks heading;four allowed_files. Final397-source complete29 modules exit0 on31531.689s/31241.585s. Tests unchanged: historical16 methods18 assertion failures0errors/skips at7a201eab remain recorded. Final mutants24/24/0 on each runtime, actual exits0. Real R4 lint6findings/exit1 before repair, CI-named regression exit0 afterward. Fresh independent six-edit review approved, equivalence self-check16146/2394/95760/6 exit0. Worker gate exit0.

Two post-review repair rounds remain historical; owner2750 classifies R4 as in-scope CI correction and2754/2757 classify/recover temporary environment loss, no added repair round. First-head8fd3ae7e Linux CI7fail/job had6separate RegimeCiTest fixtures owned by#441 and1in-scope lint test fixed by this revision. GitGuardian's synthetic digest false positive and Bot quota failures are disclosed, no red check is called green. Applicable new-head CI/Bot observations follow in RESULT. Worker never merges or update-branches.

Current sourceb91 clean selected-tree asset validation actually exited0 on tree b9680ba922744b61d58b6b1054e59f03dfebd35e; complete log in ci-r4-clean-assets.log. Later evidence-only edits record this observation; prior source/base scans and failed dirty-worktree scans remain historical. External new-head CI/Bot observations follow after push.

cost: n/a
