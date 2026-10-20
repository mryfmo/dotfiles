[P2] high orchestration .orchestration/dotfiles-T128-chain-github-scripts-followup-a02/task.md:9 The added `scripts/lint-comparisons-baseline.tsv` exemption is absent from both `allowed_files` and `threat_table`. The report’s scope-extension prose does not update the committed specification; final-head CI explicitly rejects this undeclared path.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-chain-github-scripts-followup-a02.md:116 The missing threat-table coverage is assigned to followup-a03, whose allowed files exclude both the predecessor’s task specification and the baseline file. The cited owner-file hash proves existence, but that task cannot perform the required correction within its scope.

[P2] high orchestration .orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a02-pr-feedback.json:197 The `regime` failure disposition explains only the task-copy mismatch, omitting the independent `allowed-files` failure. The annotation’s evidence command at line 209 merely retrieves the latest workflow-run ID and cannot substantiate this disposition. [Final-head CI log](https://github.com/mryfmo/dotfiles/actions/runs/39317206083/job/118281668090).

INV-2: holds .orchestration/dotfiles-T128-chain-github-scripts-followup-a02/validation.md:2526 — independently confirmed 15 changed non-test/non-record lines and 47 added test lines, within the stated caps.

Orchestration findings: 3

The backtick checks passed read-only probes for both sources, empty IDs and comment rows. Existing tests and the posting/resolution code remain unchanged. Bash syntax and ShellCheck passed; final-head CI confirms the regression tests pass.

📝 まとめ: 指定 head の監査を完了しました。上記3件の orchestration findings は未解消です。

Not rerun locally: full unit/Bats suites; CI was inspected. Remaining risk: incomplete scope and failure-disposition records.
Verdict: incorrect