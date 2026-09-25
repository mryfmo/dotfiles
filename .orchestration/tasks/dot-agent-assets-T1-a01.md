# dot-agent-assets-T1-a01 — terminal-browser pin 更新 + Codex superpowers ガード修正

## Objective

新規 Ubuntu マシンの `make update` で観測された 2 問題を修正する
(実ログ: 操作者の spark-9e8d での実行結果)。

## Work items

F1 — `scripts/lib/installer-pins.sh` の terminal-browser pin 更新:

- `TERMINAL_BROWSER_PIN_VERSION="v0.7.4"` → `"v0.11.1"`、
  `TERMINAL_BROWSER_INSTALLER_SHA256` →
  `accb57252d6e7dde513db2a473c008d71897cf72feaaecd58c5042821d1d63f9`。
- この hash はオーケストレータが https://terminal-browser.sh/install の現行
  配布物から実測済み。worker 側でも独立に再ダウンロード・再計算して一致を
  validation に逐語で記録すること(不一致ならタスクを blocked で返す)。
- pin を参照する test(tests/ 配下、supply-chain 系)があれば追随。

F2 — `scripts/update-agent-assets.sh` `update_codex_superpowers` のガード:

- `codex_marketplace_is_configured_git_marketplace openai-curated` が偽の場合、
  marketplace upgrade だけでなく `codex plugin add` もスキップし、他セクションと
  同形式の `Skipping Codex Superpowers plugin: openai-curated is not a
configured Git marketplace.` を出す(生の `Error: plugin ... was not found`
  を出さない)。plugin が既に入っている場合の検出パスは現状維持。
- 可能なら該当関数の挙動を検証する既存 test 形式(python unit or bats)に
  1 ケース追加。bats はローカル実行禁止(CI で検証)。

## 検証

- shellcheck / shfmt / bash -n(変更スクリプト)。
- F1: installer 再取得と sha256 実測の逐語出力。
- F2: 未構成 marketplace を模擬した実行トレース(関数単体を mock で駆動)で
  「Error 行が出ずスキップ文言が出る」ことの逐語出力。
- `.orchestration/validation/dot-agent-assets-T1-a01.md` へ全て記録。

## Scope

allowed_files: `scripts/lib/installer-pins.sh`, `scripts/update-agent-assets.sh`,
`tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-agent-assets-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
インストーラの実行禁止(ダウンロードと hash 計算のみ)、VM 不使用、
他ファイル変更禁止、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=25。CompactionDB memory add + ID。
