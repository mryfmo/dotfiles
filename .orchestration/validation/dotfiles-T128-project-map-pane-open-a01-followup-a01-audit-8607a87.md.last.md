[P2] high implementation home/dot_claude/hooks/executable_project-map-reload.sh:18 — `~/repo/.project-map/index.html` is normalized beneath cwd, whereas terminal-browser expands `~/` to the home directory; reproducing this input yields an empty selection and opens a duplicate pane despite an existing matching map.

[P2] high evidence .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/report.md:30 — Fresh-session and persisted-session E2E verification is explicitly unperformed; agmsg-orchestration’s Live verification rule requires both before accepting pane-lifecycle changes, and stub tests cannot supply that evidence.

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:63 — “No count reaches 2” follows a snapshot containing `bot_p1_heads_after_result=unknown` and `audits=unknown`, without the source/interim command outputs required before authorizing the revise.

The task declares no invariant map; its explicitly cited constraints were checked:

INV-2: holds .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:70 — 14 source-line changes and 143 test additions satisfy the caps.

INV-6: holds .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:75 — History contains one TASK, two RESULTs and no questions: amendments=0, revises=1; supplied feedback and prior audit contain only P2 findings. The recording defect remains separate.

Both task premises hold at the dispatch base. Source hashes and committed evidence match; Bash syntax, ShellCheck and 129 direct URL comparisons passed.

Orchestration findings: 1

📝 まとめ: [PR 379](https://github.com/mryfmo/dotfiles/pull/379) audited without modifications; three findings remain. Unit/Bats/live E2E were not rerun; live CI could not be independently refreshed because both gh-first access and web fallback failed.
Verdict: incorrect