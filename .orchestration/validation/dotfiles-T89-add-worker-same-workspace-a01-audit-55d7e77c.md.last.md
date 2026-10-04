- [P2] high confidence `home/dot_local/bin/common/executable_herdr-agents:1784` Tab cleanup accepts unlabeled panes without checking `.agent`, allowing `--remove-worker` to close another running agent.
- [P2] high confidence `home/dot_local/bin/common/executable_herdr-agents:2009` Sharing the pair workspace makes `has_claude_pane` count an added Claude worker as the orchestrator, preventing repair when the orchestrator stops.
- [P2] high confidence `home/dot_local/bin/common/executable_herdr-agents:2009` Pair repair’s `empty_pane_id` can select an exited added worker’s pane, starting the pair worker in that worker’s tab.

All three were reproduced with read-only stubs using commit source. Syntax and whitespace checks passed. GitHub was unreachable; saved [PR #239](https://github.com/mryfmo/dotfiles/pull/239) CI evidence targets later commit `672f720e`.

📝 まとめ: `55d7e77c` の監査で3件の回帰を確認しました。修正が必要です。
Verdict: incorrect