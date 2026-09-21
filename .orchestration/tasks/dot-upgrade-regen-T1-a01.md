# dot-upgrade-regen-T1-a01 — make upgrade を Mac 側で実行し pin 差分を chore PR 用に生成

## Objective(操作者決定 2026-09-21)

spark 側の `make upgrade` が生んだ未コミット mise config/lock 差分は破棄し、
**Mac 側でこの worktree から `make upgrade` を実行して最新 pin を再生成**、
レビュー可能な chore 差分として提出する。これが main へ merge されたのち、
spark と Mac の古い dirty pair は破棄されて全マシンが同一 pin に収束する。

## Work items

1. この worktree で `make upgrade` を実行(SYSTEM なし。Mac のユーザーレベル
   ツールが最新 pin へ上がる — 操作者承認済み)。長時間コマンドのため出力は
   逐語で validation へ(mise の provenance ダウンロード行は要約可、
   Upgraded 行と WARN 行は全て逐語)。
2. 生成された差分を確認: `home/dot_mise/config.toml`、`home/dot_mise/mise.lock`、
   `scripts/lib/installer-pins.sh`(値が同じなら差分なしで可)。
   **これ以外のファイルに差分が出た場合は内容を報告し、タスク外なら revert**。
3. 差分レビュー用の要約を report に: ツールごとの旧 → 新 pin 一覧、
   minimum_release_age(7d)で ignore された newer 版の一覧、
   スキップ(fd の macOS x64 asset 欠如等)の一覧。
4. `uv run python -m unittest tests.unit.test_supply_chain_policy` green
   (MISE_VERSION 等の期待が壊れていないこと)。lock と config の整合は
   同 test が検証する。
5. upgrade 中に herdr server の reload が走る場合、失敗したら報告のみ
   (このセッションの herdr は稼働中のため)。

## Scope

allowed_files: `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`,
`scripts/lib/installer-pins.sh`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-upgrade-regen-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
上記以外のファイル変更禁止(出たら revert して報告)、VM 不使用、
`make upgrade SYSTEM=1` 禁止(OS パッケージは対象外)。

## 完了

done_signal=AGMSG-RESULT。max_turns=25。CompactionDB memory add + ID。
