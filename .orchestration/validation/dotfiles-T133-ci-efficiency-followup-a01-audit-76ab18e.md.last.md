- [P2] high orchestration `.orchestration/dotfiles-T133-ci-efficiency-followup-a01/task.md:39` — The workflow/environment residual falsely claims no workflow is allowed, although lines 9–11 authorize three; file-specific tests do not make this separately required control statement true.
- [P2] high orchestration `.orchestration/acceptance/dotfiles-T133-ci-efficiency-followup-a01.md:41` — The disposition defers that correction to followup-a02, whose dispatched scope permits only ci-rerun, its tests, and its own records; it cannot repair a01’s task copy, so the stated follow-up does not resolve the finding.

INV-6: holds `.orchestration/acceptance/dotfiles-T133-ci-efficiency-followup-a01.md:40` — Recorded counts remain below reset thresholds.

Orchestration findings: 2

The implementation matches both owned fixes. Final-head Ubuntu and macOS CI logs confirm both regression tests passed within 1,234-test runs. Bootstrap scripts are identical and the task-copy hash matches. [PR #421](https://github.com/mryfmo/dotfiles/pull/421)

📝 まとめ: Completed the read-only audit; no files changed. Two orchestration findings remain.
Not rerun locally: full suites/Bats. Remaining risk: the documented disposition leaves the task-control defect uncorrected.
Verdict: incorrect