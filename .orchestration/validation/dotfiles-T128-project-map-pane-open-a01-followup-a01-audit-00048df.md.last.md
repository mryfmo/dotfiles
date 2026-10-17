[P2] confidence=0.99 implementation home/dot_claude/hooks/executable_project-map-reload.sh:40 — Checking the suffix after `realpath` rejects valid maps when `.project-map` or `index.html` points to a differently named symlink target; the hook exits before opening or reloading anything.

[P2] confidence=0.99 implementation home/dot_claude/hooks/executable_project-map-reload.sh:56 — `realpath` preserves case spelling on case-insensitive macOS filesystems, so aliases of the same repository compare unequal and repeatedly open duplicate panes; confirmed locally with directory aliases that `samefile` identifies as identical.

[P2] confidence=0.99 orchestration .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:111 — The S2 disposition incorrectly calls the third RESULT an update-branch head: history records `e234a05` at 07:44:35Z, containing canonicalizer, guard and separator changes since the second RESULT (`02fdf061`); the explanation dismissing `revises=2` therefore relies on false evidence.

The task has no invariant map; its cited constraints were checked:

INV-2: holds .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/task.md:70 — Two non-artifact files, 46 source changes and 279 test additions satisfy the caps.

INV-6: violated .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:111 — The threshold is reached, but its continuation rationale misclassifies the third RESULT.

Both amended-task premises hold at the dispatch base. Source hashes and the amended task hash match the evidence and dispatch history. After gh-first access failed, the GitHub connector confirmed the final head and passing workflows; [macOS CI](https://github.com/mryfmo/dotfiles/actions/runs/39035550385/job/117404501482) passed all 12 focused tests. Read-only syntax, ShellCheck and 15 guard checks passed.

Orchestration findings: 1

📝 まとめ: Audited [PR 379](https://github.com/mryfmo/dotfiles/pull/379) at `00048df` without modifications; two implementation defects and one orchestration record error remain.
Not checked: local full-suite/Bats or live pane E2E; the reload defects remain unresolved.
Verdict: incorrect