# Complete selected-change measurement

Fixed base: 60a6fb2b324d0381c4a6e539b37c650105154a7e
Continuation head: 06ffefbc633fe37bcef107385ea96810b2a9a0c5
PR: https://github.com/mryfmo/dotfiles/pull/440
Branch: tools/task-generator-plan-check-a05-checker

Production: checker416 additions +27 deletions =443/450 changed lines.
Tests: new module655 additions +legacy35 additions +22 deletions =712/720 changed lines.
Artifacts are counted in the complete inventory below, separately from the production/test caps. No executable/helper is placed under artifacts. All new artifact modes are0644. Timestamped worklogs, foreign untracked directories and caches are excluded.

Measured the selected staged tree with git diff --cached --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e and git diff --cached --name-only 60a6fb2b324d0381c4a6e539b37c650105154a7e. The base is an ancestor of HEAD. After commit, verify the exact same results with git diff --numstat 60a6fb2b324d0381c4a6e539b37c650105154a7e...<full-head40> and git diff --name-only 60a6fb2b324d0381c4a6e539b37c650105154a7e...<full-head40>; the validated full head is sent in PONG, avoiding a self-referential commit hash in its own artifact. full-diff-inventory.json contains the parsed complete inventory.

Retained .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/ (161 committed files) unchanged from 06ffefbc633fe37bcef107385ea96810b2a9a0c5; no a01-a04 import/deletion. Source attribution:396 at06ff +24 held pipeline +18 identity/collision +4 directory/C10 +2 R4 -1 PurePosixPath ancestry =443. The task text's attribution is retained verbatim; this measured worker breakdown distinguishes the separately observed identity/collision contribution. No further cap increase or defense removal.

Task SHA256:b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af, 240 author lines plus6 appended Checks lines, four allowed entries. Full numstat entries:356. Source/test hashes: frozen-final-binding.json.

## Complete numstat

```
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
39	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/current-measure.json
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
2150	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/full-diff-inventory.json
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
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/learning.md
40	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-c12-diagnostic.log
72	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/legacy-initial-diagnostic.log
9	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocked-pong.md
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/lint-adjustment-blocker.md
88	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-before-new-P2-hold.log
52	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/mask-current-evidence.log
738	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/measure.md
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
25	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
18	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/required-selectors.json
13	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/reset-provenance.json
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-command.json
6	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-reproduction.log
4	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-blocked-report.md
58	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red312.log
61	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red315.log
3	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-mask.log
47	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-measure.json
7	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-pong.md
10	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-red-commands.json
22	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-replan.md
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
42	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
38	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-gate-commands.json
68	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-evidence.json
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-receipt.md
2	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-reviewed-gate.log
16	0	.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-unreviewed-gate.log
416	27	scripts/orchestrator/task-consistency-check.py
35	22	tests/unit/test_task_checkers.py
655	0	tests/unit/test_task_consistency_c11_c15.py
```

## Complete changed-file list

```
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
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/required-selectors.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/reset-provenance.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-command.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/review-directory-scope-reproduction.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-blocked-report.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red312.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-initial-red315.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-mask.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-measure.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-overcap-pong.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-red-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/revise2-replan.md
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
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/validation.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-gate-commands.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-evidence.json
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-review-receipt.md
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-reviewed-gate.log
.orchestration/dotfiles-T133-task-generator-plan-check-a06-checker/worker-unreviewed-gate.log
scripts/orchestrator/task-consistency-check.py
tests/unit/test_task_checkers.py
tests/unit/test_task_consistency_c11_c15.py
```
