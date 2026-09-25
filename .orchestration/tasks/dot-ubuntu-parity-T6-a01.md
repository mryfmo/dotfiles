# dot-ubuntu-parity-T6-a01 — 無効な .chezmoiremove エントリの整理

## Objective(2026-09-23、実機検証からの是正)

T3/B7 で追加した `home/.chezmoiremove` の `.local/bin/server`(linux+client ガード)は
**無効**であることが実機で実証された: chezmoi は `.chezmoiignore` されたターゲットを
remove の対象にもしないため(ignore が remove に勝つ)、client の
`chezmoiignore.d/ubuntu/client` が `.local/bin/server` を ignore している限り
このエントリは永久に no-op。残骸はオーケストレーターが手動削除済み。
誤解を招く no-op を残さないため削除する。

## Work item(1 コミット: `fix(chezmoi): drop ineffective .chezmoiremove entry for ignored path`)

- `home/.chezmoiremove` から `{{ if and (eq .chezmoi.os "linux") (eq .system "client") }}.local/bin/server{{ end }}`
  ブロックを削除。コミットメッセージに「ignore されたターゲットは .chezmoiremove でも
  削除されない(chezmoi の仕様)」と根拠を明記。
- CompactionDB decision 登録: 「chezmoi では .chezmoiignore が .chezmoiremove に優先し、
  ignore されたパスは宣言的に削除できない。ignore 済み残骸の掃除は手動または
  ignore 解除が必要」— コマンドと ID を validation に逐語で。
- `make unit-test` green(末尾サマリを validation へ)。
- ブランチ: main から `fix/drop-ineffective-chezmoiremove` を切る(fetch してから)。
  コミットは `git -c commit.gpgsign=false commit`、Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>。

## Scope

allowed_files: `home/.chezmoiremove`, `tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T6-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、main への直コミット禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=15。cost 行を report に。
