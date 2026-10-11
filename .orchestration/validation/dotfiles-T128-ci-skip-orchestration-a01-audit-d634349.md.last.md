[P2] high implementation `.github/workflows/test.yaml:98` — The relocated classifier still permits rename detection: moving `home/a` to `.orchestration/a` leaves only the destination in `--name-only`, producing `should_test=false` despite deleting a relevant source file; add `--no-renames` and exercise renames in the unit-test decision test. [Git documentation](https://git-scm.com/docs/git-diff)

[P2] high implementation `tests/unit/test_workflow_orchestration_skip.py:67` — The handwritten parser ignores quoted YAML keys: inserting job-level `'if': false` or decision-step `'continue-on-error': true` leaves all seven structural tests passing, so the named tests do not close the skipped-job and failed-decision threats. A skipped required job can still permit merging. [GitHub documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions)

[P2] high orchestration `.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md:14` — The task’s INV-2 matches the modified main working-copy design, but differs from committed main at `b896d9bc`, whose implementing-task map also lacks this task; dispatch therefore used a design revision that had not crossed the required boundary PR.

[P2] high orchestration `.orchestration/acceptance/dotfiles-T128-ci-skip-orchestration-a01.md:7` — The claimed complete eight-item sweep predates the orchestrator’s reply `4240542203` and review `5482187594`; both lack dispositions in the supplied JSON, which also retains `resolved: false` for the now-resolved thread. Refresh the sweep before integration.

The threat-table assessment is:

| Row | Assessment |
|---|---|
| PR-controlled workflows | Acknowledged residual; V1c remains prospective. |
| Diff classification | Not closed: the unit-test rename case above is uncovered. |
| Required job skipped | Current jobs have no job-level `if` or `needs`; quoted-key mutations bypass the tests. |
| Decision failure | Current decision steps have no `if` or `continue-on-error`; fetch failures propagate, but the quoted-key mutation defeats the test. |
| Non-PR events | Bootstrap decision returns `true` before accessing Git. |

The table also omits the orchestrator-controlled design-version and feedback-freshness risks identified above.

Confirmed for [PR 320](https://github.com/mryfmo/dotfiles/pull/320): all seven required contexts succeeded; full-history fetching addresses the moved-base failure. Bootstrap classification handles renames, deletions, ordinary non-ASCII paths and empty diffs. Seven structural tests and eight existing workflow-security tests passed using head content in memory.

INV-2: violated `.orchestration/tasks/dotfiles-T128-ci-skip-orchestration-a01.md:14` — invariant text does not match committed main’s design.

Orchestration findings: 2

📝 まとめ: Read-only audit completed with four findings; no files changed.
Not rerun: scratch-repository/full-suite tests; the post-merge ≤10-minute boundary-PR measurement remains outstanding.
Verdict: incorrect