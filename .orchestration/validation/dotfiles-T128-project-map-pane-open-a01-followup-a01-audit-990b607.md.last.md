[P2] confidence=0.99 implementation home/dot_claude/hooks/executable_project-map-reload.sh:17 — Relative paths use logical `$PWD`, while Node resolves them from the physical cwd. Reproduced with `/tmp` → `/private/tmp`: an existing map produces empty selection, so each write opens another pane. Follow-up ownership does not fix this head.

[P2] confidence=0.97 orchestration .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:42 — “INV-6 allows no second” incorrectly treats one pre-RESULT C-50 round as an exhausted counter. INV-6 counts RESULTs minus one, with threshold two; this record places the first RESULT afterward. The stated reason for refusing the small, in-scope fix contradicts the task’s count-based completion rule.

[P2] confidence=0.99 evidence .orchestration/reports/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:14 — Supplied report/validation are pre-push checkpoints: eight tests and 93 test additions. The final supplements and review JSON remain in the worker worktree, outside the supplied artifacts; they contain nine tests, 118 additions, the tilde fix and the remaining symlink defect. Collect those final records into the audit inputs.

Both task premises hold at the dispatch base. The task copy matches its dispatched hash. All nine focused tests passed in [final-head CI](https://github.com/mryfmo/dotfiles/actions/runs/38996670669/job/117290642721); Bash syntax, ShellCheck and 126 read-only URL probes also passed. GitHub investigation used `gh` first, then the connector after connection failure.

INV-2: holds .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:70 — Two non-artifact files, 14 source changes, 118 test additions; within caps.

INV-6: holds .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:43 — Recorded counts remain below reset thresholds; the unsupported exhaustion claim is the orchestration finding above.

Orchestration findings: 1

📝 まとめ: Read-only audit completed with three P2 findings; nothing modified. Live-pane behavior and bus counters were not independently replayed; duplicate-pane risk remains.
Verdict: incorrect