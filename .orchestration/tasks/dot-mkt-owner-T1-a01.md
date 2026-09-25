# dot-mkt-owner-T1-a01 — marketplace.json をランタイム所有へ(drift の根治)

## Objective

#165 の chmod 後も操作者実機で drift(mode 664)が再発した。chmod の位置は
正しく前回ラン終了時は 644 のはずなので、**crit 以外の書き手**が
`~/.agents/plugins/marketplace.json` を再書込みしている疑いが濃厚
(有力候補: codex / claude セッション起動時の marketplace 再登録)。
もぐら叩きをやめ、ランタイムが書き換えるレジストリファイルの所有権を
ランタイムへ移す。

## Work items

F1 — 書き手の特定(VM で事実確定):

- adh-test の scratch user で marketplace.json を 644 に整えた後、
  (a) `codex exec --skip-git-repo-check 'echo hi'` 等の未認証セッション起動、
  (b) `claude --version` / claude の軽い起動、(c) `crit install codex-plugin`
  をそれぞれ単独実行し、各操作後の mode/mtime/内容 diff を逐語記録。
  どの操作が 664 化・再書込みするかを確定する。

F2 — 所有権の移行:

- `home/dot_agents/plugins/marketplace.json` を chezmoi の
  `create_` 属性へ変更(`create_marketplace.json` へ rename)し、
  「初回シードのみ・以後の内容/mode はランタイム所有・chezmoi は不変更」に
  する。既存マシンで chezmoi の entry 状態が旧属性のまま残る場合の挙動
  (rename 後の apply が旧 target を置換しないこと)も VM で確認。
- #165 の chmod は無害だが、F1 の結果 crit 以外も書くと確定したら
  コメントを実態に合わせて更新(削除はしない — フレッシュ直後の見た目安定用)。
- README の該当説明(あれば)を追随。

F3 — 検証(ユーザー同一経路):

- VM の bootstrap 済み scratch user で `make update` → codex 起動(F1 で
  664 化した操作)→ `make update` の順に実行し、**2 回目の make update が
  drift 警告ゼロで完走**することを逐語実証(これが受入ゲート。
  ランタイム書込みを挟んでも update が汚れないこと)。

## Scope

allowed_files: `home/dot_agents/plugins/**`(rename 含む), `home/.chezmoi*`
(属性変更に必要な範囲のみ), `scripts/update-agent-assets.sh`(コメントのみ),
`README.md`, `tests/**`,
`.orchestration/{tasks,reports,validation,sandboxes,learning,autoskill/runs}/dot-mkt-owner-T1-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: git commit 禁止、push 禁止、bats ローカル実行禁止、
VM は `limactl shell adh-test` のみ(scratch user 削除、credential 持込み禁止、
codex/claude の login 禁止)、mise config/lock 変更禁止、
新規トップレベルディレクトリ作成禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=30。CompactionDB memory add + ID。
