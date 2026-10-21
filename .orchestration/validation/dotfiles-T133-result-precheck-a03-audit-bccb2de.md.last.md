Audited [PR #411](https://github.com/mryfmo/dotfiles/pull/411) at `bccb2dea`. Final-head CI is green; task-copy and log hashes match.

[P2] high orchestration .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md:50 The hash-only verification accepts stale precheck evidence. Its tested head is `1ac3a1a6`, but the final merge changes workflows, scripts and tests outside this task’s evidence directory. Running the pinned prechecker against these records rejects the final head. Regenerate the proof after the merge.

[P2] high implementation scripts/orchestrator/dispatch.sh:177 The gate extracts requested selectors but ignores `previous_head=`. I reproduced acceptance with an all-`f` requested baseline and the existing proof. Record the tested baseline and compare it with the latest revision request.

[P2] high specification .orchestration/tasks/dotfiles-T133-result-precheck-a03.md:101 The prescribed `unittest -k <name>` uses substring matching. A requested test can pass on both heads while a similarly named test supplies the previous-head failure; the writer then records a valid regression proof. I reproduced this with `test_requested` and `test_requested_extra`. Require exact method selection.

[P2] high implementation scripts/orchestrator/result-precheck.sh:187 The clean-tree query runs in process substitution, whose failure does not propagate to the loop. A `git status` failure therefore permits checks to continue without establishing that the tree is clean. Capture and check its exit status before consuming its output.

[P2] high orchestration .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md:39 The three local findings are deferred despite the record reporting zero a03 revise rounds. At least the clean-tree error-propagation fix is small and within `allowed_files`; Playbook step 10.1 requires such a P2 to receive a revise round with `check=` while counts permit it. The existing owner task does not justify this deferral.

INV-6: holds .orchestration/dotfiles-T133-result-precheck-a03/report.md:16 — the supplied a03 history shows one implementation round and preserves predecessor resets.

Orchestration findings: 2

📝 まとめ: 最終 head の読み取り専用監査を完了し、5 件の指摘を確認しました。ファイルは変更していません。

Not checked: full suites locally or live hook/bus deployment. Regression-proof acceptance gaps remain.
Verdict: incorrect