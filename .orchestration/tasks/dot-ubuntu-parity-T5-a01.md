# dot-ubuntu-parity-T5-a01 — CI 修正: usage-snapshot timer スクリプトの実行順序

## Objective(2026-09-23、CI 失敗 run 35796642953 からの是正)

main への push で Snippet install ワークフローの public-bootstrap (ubuntu-latest, client) が失敗:

```
Failed to enable unit: Unit file usage-snapshot.timer does not exist.
chezmoi: .chezmoiscripts/ubuntu/60-enable-usage-snapshot-timer.sh: exit status 1
```

根本原因: chezmoi はスクリプトをターゲット名順で実行し、`.chezmoiscripts/...` は
`.config/...` より辞書順で先に来るため、fresh bootstrap では unit ファイル適用前に
enable スクリプトが走る。既適用マシンでは unit が既存のため再現しない。

## Work item(1 コミット: `fix(usage): run timer enablement after files are applied`)

- `home/.chezmoiscripts/ubuntu/run_onchange_60-enable-usage-snapshot-timer.sh.tmpl` を
  `run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl` へ **git mv で改名**
  (chezmoi の `after_` 属性でファイル適用後に実行される。リポジトリ既存の
  `run_once_after_*` と同じ規約)。内容は不変。
- 他の新規スクリプト(52-zed, 53-tailscale, 99-gnome-defaults, 50-server-timezone)は
  適用済みファイルに依存しないため対象外であることを確認し report に明記。
- `make format` / `make unit-test` green(逐語 or 末尾サマリを validation へ)。
  bats の files テストがスクリプト名を参照していれば追従。
- コミットは `git -c commit.gpgsign=false commit`、Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>。

## Scope

allowed_files: `home/.chezmoiscripts/ubuntu/**`, `tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T5-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、
main への直コミット禁止(feat/ubuntu-parity は main へマージ済みのため、
**新ブランチ `fix/usage-timer-ordering` を main から切って作業**)、allowed_files 外の変更禁止。

## 完了

done_signal=AGMSG-RESULT。max_turns=20。cost 行を report に。
