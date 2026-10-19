# Change measurement

Measured code head: 5a8820746b5129599ab78e6abb34b2da8e8e744b, base origin/main 212efe972a14d4d5f209bf739c1b8008471ba775, after the single authorized rebase. Later evidence-only updates do not change the code totals or path inventory below.

Command: git diff --numstat origin/main...HEAD

~~~~text
3	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/autoskill.md
7	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/learning.md
86	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/report.md
18	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/revise.yaml
24	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/sandbox.md
98	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md
2071	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/validation.md
7	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/autoskill.md
11	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/learning.md
13	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/report.md
5	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/revise.yaml
29	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/sandbox.md
83	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md
71	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/validation.md
6	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/a05-worker-receipt.md
18	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/a05-worker-review.json
4	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/autoskill.md
50	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/corpus-inventory.json
14	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/learning.md
10	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/measure.md
21	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/post-round-open.json
51	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/report.md
20	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/sandbox.md
186	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md
1607	0	.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/validation.md
216	0	scripts/validate-agent-assets.py
941	0	tests/unit/test_validate_agent_assets.py

~~~~

Outside tests/ and .orchestration/: 216 added + 0 deleted = 216/300. Tests: 941 added + 0 deleted = 941/1000, including every fixture line. No corpus input or validation is removed to meet the caps. All remaining paths are orchestration records; their counts can grow as command output is appended, and are excluded from the two code caps.

Complete changed-file inventory at that head:

~~~~text
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/autoskill.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/learning.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/report.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/revise.yaml
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/sandbox.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/task.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-a01/validation.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/autoskill.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/learning.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/report.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/revise.yaml
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/sandbox.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/validation.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/a05-worker-receipt.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/a05-worker-review.json
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/autoskill.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/corpus-inventory.json
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/learning.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/measure.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/post-round-open.json
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/report.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/sandbox.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/task.md
.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a05/validation.md
scripts/validate-agent-assets.py
tests/unit/test_validate_agent_assets.py

~~~~

Reset delta, compared with the rebased predecessor e1512cbc0d146360365caa43bab4ad175e66122a, deletes only the a04 task copy, adds this a05 directory and changes the two permitted code files. The earlier a01/followup-a01 records shown above are inherited and unchanged by this reset. The a05 task copy is byte-identical to the dispatched main-checkout file: sha256 5eb78325f3b09c2cd4a762305c25770f58d94cbc1d081dda6672d85c8ca8d925. No other predecessor artifact change, executable, dependency, workflow, home/ or install/ edit, baseline or waiver is introduced.

Implementation map after rebase: a99521b4 -> 726f92727e83929a8348a968e20fbb2f41ebfa75; sole correction e37be90d -> 5ed00db13a8c7daaaf0b9d95ae4a272210a4c16a. Range-diff equals for all four reset commits, and SHA256 of source/test/task matches pre-rebase. No second source correction or independent review.


## Revise-1 current measurement

Against the same PR base source paths, the authorized correction changes source by +13/-2 lines and tests by +26/-0 relative to eda0354b. The complete PR source total is 227 added +0 deleted =227/300; tests are 967 added +0 deleted =967/1000. The only new implementation helper is auth_diagnostic_key; one shared call replaces the final-only key redaction. No corpus row is removed and the inherited table remains425 rows; the new named method adds36 leaf/ancestor subcases. Task evidence and the two uncommitted timestamped worklogs remain task-local. Exact committed inventory and delivery head follow after commit.

## Amendment1 repair measurement

Current base205fe85c19c03750fe3551bb96e084e9f0a676b6. Full source changes:231 added/0deleted in scripts/validate-agent-assets.py plus1added/0deleted in scripts/lint-comparisons-baseline.tsv =232/300. Tests967 added/0deleted =967/1000. The baseline has exactly one new owned row; no existing row is removed or modified. The source repair changes the single authored template-directory condition (+5/-1 lines); the moved attribute loop is unchanged. Main's linter/test and its93-row baseline arrive from the incorporated base and are not new task-owned executable files. Amended task copy sha3158d7969b273ffd8499f6cc2dcb1dc56bd353c2e1796cf39700c33f8ceea6f1; older5eb78325 observations remain historical.

The corpus stays425 rows and tests stay123 methods. No original fixture is altered or removed; the new repair reuses the existing required lint test and both platform fixtures. Final committed inventory and CI/review observations are supplied after the single repair push.
