# dot-residuals-T1-a01 — Bot レビュー残存 3 件 + client bashrc の private ガード

## Objective

merge 済み PR に未対応で残っていた Codex review bot の指摘 3 件と、操作者実機で
再現した client bashrc のエラー 2 行を一括で解消する。

## Work items

F1 — client bashrc の private 配布物ガード(操作者実機で再現済み):

- `home/dot_bash/client/bashrc` の `source ~/.local/bin/server/prompt.sh` と
  `source ~/.local/bin/server/aliases.sh` を、同ブロックの secrets.sh と同じ
  `[ -r ... ] && source ...` ガードへ(この 2 ファイルは private chezmoi の
  配布物で、public のみのマシンでは対話 bash 起動ごとに 2 行のエラーが出る)。
  history.sh / cache.sh は public 配布のため現状維持。

F2 — (PR #160 P2)gh 拡張 run_once の再実行可能化:

- 現状: 未認証時に warning + return 0 で run_once が「成功」記録され、
  `setup-gh` 後の apply でも再実行されない → 拡張が永遠に入らない。
- 修正: gh 拡張の導入を run_once の一発性に依存させない。方針は
  `scripts/update-agent-assets.sh` に gh 拡張の ensure を追加し(認証済みなら
  install、未認証なら従来の警告)、`make update` 毎に収束させる。
  run_once 側 wrapper は薄いまま維持(初回導入の早道)。README の
  「setup-gh 後に再実行」の記述を実態(次の make update で入る)へ修正。

F3 — (PR #163 P2)crit の PATH 優先問題:

- `~/.local/bin/crit` へ pinned 版を入れても、mise shims 等の別 crit が PATH で
  優先されると古い実行体が使われ続け、毎回再ダウンロードも起こりうる。
- 修正: `ensure_crit_cli` の冒頭 version 判定と以後の呼出しを
  `command -v` 依存から「target パス優先」へ(pinned target が存在し version
  一致ならそれを明示使用。`hash -r` の追加と、以後の crit 呼出しを
  `"${HOME}/.local/bin/crit"` 明示 or PATH 先頭調整のどちらか一貫した方式で)。

F4 — (PR #163 P2)runtime repair への登録:

- `ensure_crit_cli` step を `ASSET_STEP_FUNCTIONS`(check-agent-runtime.py /
  asset_repair_action の許可リスト)へ登録し、`REPAIR=1 make doctor` が
  missing crit を修復できるように。既存の repair テスト形式で 1 ケース追加。

## 検証

- shellcheck / shfmt / bash -n(変更シェル)。bats ローカル禁止(CI)。
- F1: public のみ環境(VM scratch user、private なし)で `bash -i -c true` の
  stderr にエラー 0 行、private 相当ファイルを置いた場合は source されること。
- F2: 未認証 → make update 相当で警告、gh auth を mock した状態で同コマンドが
  extension install を呼ぶこと(mock trace)。
- F3: PATH 先頭に fake 旧 crit を置いた状態で ensure_crit_cli が pinned target を
  使う/再ダウンロードしないことの trace。
- F4: manifest finding → repair 呼出しの unit ケース green。
- 各 unit(test_runtime_health / test_asset_manifest ほか関連)green を逐語で。

## Scope

allowed_files: `home/dot_bash/client/bashrc`, `install/common/gh_extensions.sh`,
`home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl`,
`scripts/update-agent-assets.sh`, `scripts/check-agent-runtime.py`,
`README.md`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-residuals-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(scratch user 削除、login 禁止)、
mise config/lock 変更禁止、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=35。CompactionDB memory add + ID。
