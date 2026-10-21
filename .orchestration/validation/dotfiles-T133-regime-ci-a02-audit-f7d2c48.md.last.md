[P2] high implementation scripts/orchestrator/regime-ci.py:260 Supersession checks only whether base-dispatched texts exist, not whether both head copies match them. A read-only probe with an altered predecessor copy returned `ok 1 task(s)` and exit 0, contrary to amendment 1’s authentication requirement; verify byte equality before excluding predecessors.

[P2] high evidence .orchestration/dotfiles-T133-regime-ci-a02/validation.md:221 The required bootstrap targets `1ee15af1`, not final head `f7d2c48d`; the latter adds six evidence files. Task lines 145 and 161 explicitly require the final-head command and output. The auditor’s in-memory final-head run passed, but the prescribed bootstrap evidence remains missing.

[P3] high orchestration .orchestration/dotfiles-T133-regime-ci-a02/sandbox.md:28 [PR #418](https://github.com/mryfmo/dotfiles/pull/418) still describes the withdrawn a01 design: `pull_request`, head execution and head-controlled policy binding. Update its title and description to reflect a02’s actual trust boundary.

INV-6: holds .orchestration/acceptance/dotfiles-T133-regime-ci-a02.md:42 — history confirms one amendment, one RESULT and no question/revise rounds.

Orchestration findings: 1

Final-head GitHub CI succeeded, including the 14 regime tests and eight workflow-security tests. The task declares no additional numbered invariants.

📝 まとめ: 指定 head の読み取り専用監査を完了し、3 件を報告しました。
No files changed; full suites and Bats were not rerun locally. The predecessor-copy authentication gap remains.
Verdict: incorrect