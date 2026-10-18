Audited [PR #398](https://github.com/mryfmo/dotfiles/pull/398) at `9842d91`. GitHub CI confirms 1,178 Python tests passed; task-copy hash and diff caps match.

[P2] high implementation `scripts/update-agent-assets.sh:980` A failed `uv tool install --force` can leave the old pinned binary and newly retained wheel together; subsequent runs return success without retrying, leaving uv’s receipt pointing to the deleted temporary source. The memory-only failure fixture confirmed this skipped retry.

[P2] high orchestration `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a01.md:39` The removal disposition incorrectly assumes the binary and wheel are deleted. Both paths fail `remove-agent-asset`’s safe-root guard before deletion. Correct the disposition and follow-up scope to cover this refusal; the worker report’s claim that the manifest makes the wheel removable is also unsupported.

The task declares no explicit invariant mapping; its inherited Completion clause references INV-6.

INV-6: holds `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a01.md:57` — two RESULTs, one revise, and no recorded reset threshold reached.

Orchestration findings: 1

📝 まとめ: 指定 head の監査を完了し、実装と orchestration に各1件の P2 を確認しました。ファイルは変更していません。

Not rerun locally: full tests or live installation/removal; CI and read-only checks support the findings, which remain unresolved.
Verdict: incorrect