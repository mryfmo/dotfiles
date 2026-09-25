# dot-ubuntu-parity-T8-a01 — zed.sh の fresh-HOME バグ修正(T7 発見のフォローアップ)

## Objective

`install/ubuntu/client/zed.sh::install_pinned_zed` は
`mv "${tmpdir}/zed.app" "${staging}"`(staging=~/.local/share/zed.app.tmp)を
`mkdir -p "$(dirname "${ZED_APP_DIR}")"` より**前**に実行する。~/.local/share が
未作成の fresh $HOME(初回ブートストラップ)では mv が失敗する。T5 の usage-timer と
同類の fresh-bootstrap バグ。

## Work item(1 コミット: `fix(ubuntu): create zed parent dir before staging move`)

- `install/ubuntu/client/zed.sh`: `mkdir -p "$(dirname "${ZED_APP_DIR}")"` を最初の `mv` より前に移動。
- `tests/install/ubuntu/client/zed.bats` の該当テストから T7 が入れた `.local/share` 事前作成の
  ワークアラウンドを**削除**し(スクリプト自身が保証するため)、`bats -f 'main downloads'` で
  ok を逐語確認(validation へ)。
- ブランチ: main から `fix/zed-fresh-home`(fetch してから)。
  `git -c commit.gpgsign=false commit`、Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>。

## Scope

allowed_files: `install/ubuntu/client/zed.sh`, `tests/install/ubuntu/client/zed.bats`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T8-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、
main への直コミット禁止、対象テスト以外の bats 実行禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=15。cost 行を report に。
