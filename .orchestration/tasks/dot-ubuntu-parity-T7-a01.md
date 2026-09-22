# dot-ubuntu-parity-T7-a01 — CI 修正: T4 新規 bats テスト 4 件の exit 127

## Objective(2026-09-23、CI run 35798238740 = Unit test / ubuntu-latest client の失敗)

失敗 4 件(すべて T4 で新設したモックベーステスト):
- tests/install/ubuntu/client/gnome_settings.bats:11「main is a no-op without gsettings on PATH」
- 同 :21「main is a no-op headless even when gsettings exists」
- tests/install/ubuntu/client/misc.bats:52「install_chromium is a no-op when snap is unavailable」
- tests/install/ubuntu/client/zed.bats:51「main downloads, verifies, and links zed…」

根本原因(CI の BW01 警告が証拠): `run env PATH=<モックdirのみ> … bash ./install/...` の形は
**env が bash 自体を PATH 解決できず exit 127**。モックだけの PATH では bash/coreutils
(tar, awk, sha256sum, mktemp 等)が見えない。

## Work item(1 コミット: `fix(tests): resolve interpreters and core tools under stripped PATH in T4 bats`)

- 4 テストを修正。方針: インタープリタは絶対パス(`/usr/bin/env` を避け `run env PATH=… /bin/bash script`)
  で起動し、スクリプト内部が必要とする coreutils は PATH に `/usr/bin:/bin` を含めて解決させる。
  「gsettings が PATH にない」ケースは、gsettings **stub を置かない**モック dir を先頭にしつつ
  /usr/bin に実物 gsettings が存在しても発動しないよう、モック dir に `exit 127` する gsettings を
  置かない設計ではなく **PATH から /usr/bin を外しつつ必要コマンドのみ symlink したミニ bin を組む**か、
  いずれか確実な方を選び、選択根拠を report へ。既存 repo の他 bats のモック流儀を必ず参照して合わせる。
- **検証は実際に bats を実行する**(今回の教訓)。ただしシステム変異テストを避けるため、
  対象 4 テストのみを `bats -f '<テスト名の正規表現>' <file>` で個別実行し、逐語出力を validation へ。
  4 件 ok になること。他のテストは実行しない(apt/snap を実際に叩くため)。
- ブランチ: main から `fix/t4-bats-stripped-path`(fetch してから)。
  `git -c commit.gpgsign=false commit`、Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>。
- CompactionDB decision: 「この repo の bats install テストはローカル実行禁止(実システムを変異)だが、
  新設するモックベーステストは `bats -f` で個別実行してから出荷する。`env PATH=<mock only> bash …` は
  127 で死ぬ」を登録、コマンドと ID を逐語で。

## Scope

allowed_files: `tests/install/ubuntu/client/{gnome_settings,misc,zed}.bats`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T7-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、`$HOME` 配下の変更禁止、
main への直コミット禁止、install スクリプト本体の変更禁止(テストのみ)、
対象 4 件以外の bats 実行禁止(システム変異防止)。

## 完了

done_signal=AGMSG-RESULT。max_turns=25。cost 行を report に。
