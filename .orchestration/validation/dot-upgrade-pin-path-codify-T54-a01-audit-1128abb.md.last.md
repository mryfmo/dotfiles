[P2] High confidence `home/dot_local/bin/common/executable_herdr-agents:1668` — The revised body no longer matches an unmodified hook installed by `1128abb^`, so bootstrap classifies it as edited and leaves it unchanged. Those installations retain the unsafe launcher delegation and miss execute-bit repair: missing/stale launchers can still break feature pushes, and nonexecutable hooks remain disabled. Recognize and migrate the exact predecessor stub while preserving user edits.

Read-only probes confirmed this mismatch. [PR #225 CI](https://github.com/mryfmo/dotfiles/pull/225) passes on Linux and macOS, but the added tests cover newly generated stubs. No additional security, compliance, or evidence-integrity findings.

📝 まとめ: `1128abb` の監査を完了し、既存の管理済みフックに修正が適用されない問題を1件確認しました。

Verdict: incorrect