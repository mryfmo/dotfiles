# dot-shell-sp-T1-a01 — Ubuntu client の zsh デフォルト化 + Codex superpowers provisioning

## Objective

操作者の指摘 2 件を解消する。いずれも fresh Ubuntu マシンで実確認された
恒久的未完了(スキップ表示や bash プロンプトのまま放置される)。

## Work items

F1 — Ubuntu client のログインシェルを zsh に収束:

- 現状: dependencies.sh が zsh を install し、setup.sh も client では
  `/bin/zsh --login` へ再起動する設計なのに、`chsh` がどこにもなく次回
  ログインから bash に戻る(macOS は OS デフォルトが zsh のため差異が出る)。
- 実装: `install/ubuntu/client/` に default shell 設定スクリプトを追加し
  chezmoiscripts の client run_once として配線(既存の命名規約に従う)。
  内容: 現在の login shell が zsh でない場合のみ
  `sudo chsh -s "$(command -v zsh)" "${USER}"`。zsh が /etc/shells に
  なければ追加してから。冪等(zsh 済みなら no-op メッセージ)。
  server は現行設計どおり bash のまま(変更しない)。
- README の Ubuntu 節に 1 行追記(client は次回ログインから zsh、即時反映は
  `exec zsh`)。
- bats: 冪等性(2 回実行で chsh 1 回)と zsh 済み no-op を mock で検証。

F2 — Codex superpowers の provisioning 欠落:

- 現状: `openai-curated` marketplace を構成する ensure 関数が存在せず、
  fresh マシンでは superpowers が永久にインストールされない
  (Mac は過去の手動構成の遺産で、そこでも root は local dir であり
  Git marketplace ではない)。
- 調査(先に事実確定、VM の scratch user + mise 導入の codex で):
  (a) fresh 環境の `codex plugin marketplace list` に openai-curated が
  bundled で存在するか、(b) `codex plugin add superpowers@openai-curated` が
  失敗する正確な機構(marketplace 未 fetch? 認証必要? Linux 版に superpowers
  が未収録?)、(c) refresh/fetch 手段(openai-curated-remote の意味)。
  逐語証拠を validation へ。
- 実装: 調査結果に基づき、可能なら `ensure_codex_superpowers_marketplace`
  相当(bundled marketplace の refresh or 正規の追加手順)を他 ensure 関数と
  同形式で追加し、fresh 環境で superpowers が入るところまで。
  **不可能な場合(認証必須・Linux 未提供等)は、偽装せず**: skip 文言を
  「理由 + 必要な手動手順(例: codex login 後に codex plugin add ...)」を
  示すものへ変え、README に記載し、UNRESOLVED として報告書に明記する。
- 単体 test: 新分岐を test_runtime_health の既存パターンで。

## 検証

- shellcheck / shfmt / bash -n。bats はローカル実行禁止(CI)。
- F1: VM の scratch user で実際に chsh が効くこと(getent passwd で shell 確認)
  → 逐語出力。user は削除して撤収。
- F2: VM での調査逐語 + (実装した場合)fresh user で superpowers 導入成功の
  逐語、または UNRESOLVED の機構説明。
- `.orchestration/validation/dot-shell-sp-T1-a01.md` へ全て記録。

## Scope

allowed_files: `install/ubuntu/**`, `home/.chezmoiscripts/**`,
`scripts/update-agent-assets.sh`, `README.md`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-shell-sp-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(scratch user 削除、credential 持込み禁止、
codex の認証 login 禁止 — 未認証で可能な範囲の調査に限る)、
mise config/lock 変更禁止、新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=35。CompactionDB memory add + ID。
