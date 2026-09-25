# dot-ubuntu-parity-T12-a01 — CI 修正: T10 新設プロンプトの非対話フォールバック

## Objective(CI run 35808305772 / 35808305802 の失敗、c6fd552)

T10-1/T10-2 の新設プロンプト(`promptString "Full name"` / `promptBool "Use the private ..."`)が
非対話 CI を 2 経路で壊した:
- test.yaml:294-299 の fixture は data に email/system のみ供給 → name が hasKey false →
  promptString が `/dev/tty: no such device` で fail
- remote.yaml:62 の canned stdin(email, system の 2 行)がプロンプト増で行ズレ →
  既存 system プロンプトが EOF

## Work item(1 コミット: `fix(chezmoi): default the new identity prompts in CI`)

- `home/.chezmoi.yaml.tmpl`: 既存の encryption CI ガード(`CI=true` 判定)と同じ流儀で、
  **name と usePrivate の 2 キーのみ** `env "CI" == "true"`(既存判定の書き方に合わせる)かつ
  hasKey false のとき、プロンプトせずデフォルト(name=`"CI"`、usePrivate=`false`)を採用。
  email/system の既存プロンプト挙動は不変(canned stdin の 2 行整合が復元される)。
- 検証(逐語で validation へ):
  - `CI=true chezmoi init`(email/system のみの data を持つ一時 config)で
    プロンプトなしに成功し、rendered data に name="CI" / usePrivate=false が入ること
    (test.yaml fixture の再現手順をローカルの一時 HOME で模す。$HOME 実体は触らない —
    一時ディレクトリ HOME で)。
  - CI=true なし(対話)経路のテンプレート分岐が従来どおりプロンプトへ向かうこと
    (execute-template で分岐の見える形の確認で可)。
  - `printf 'ci@example.invalid\nclient\n' | CI=true chezmoi init ...` 相当で stdin 2 行整合が
    成立すること(remote.yaml 再現)。
- 可能なら unit テスト追加(config テンプレートの CI 分岐)。既存テスト追従。
- `make format` / `make validate-agent-assets` / `make unit-test` green。

## Scope

allowed_files: `home/.chezmoi.yaml.tmpl`, `tests/**`,
`.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ubuntu-parity-T12-a01.md`,
`.agents/worklog/codex/**`

forbidden_actions: push 禁止、PR 作成禁止、chezmoi apply 禁止、実 `$HOME` 配下の変更禁止
(検証は一時 HOME で)、main への直コミット禁止、.github/workflows の変更禁止
(テンプレート側で吸収する方針)、対象外 bats 実行禁止。
agmsg は自分の inbox 読みと最後の send.sh 1 通のみ。

## 手順

git fetch origin && git checkout -b fix/ci-prompt-defaults origin/main で開始
(T11 のブランチとは独立)。done_signal=AGMSG-RESULT。max_turns=25。cost 行を report に。
