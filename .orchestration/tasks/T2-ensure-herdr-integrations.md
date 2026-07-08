# T2: update-agent-assets.sh に ensure_herdr_integrations を追加

依頼元: orchestrator-fable5(agmsg team: dotfiles-conformance)
repo: /Users/mryfmo/Workspace/dotfiles(branch 作成・commit 不要)

## 背景

`make update` は `chezmoi apply` 後に `./scripts/update-agent-assets.sh` を実行する。herdr の公式 integration(`herdr integration install claude` / `install codex`)は冪等(既存エントリがあれば no-op)で、herdr 更新時のフックスクリプト再配布も担う。chezmoi apply が `~/.claude/settings.json` を上書きしても、直後のこのスクリプトで自己修復されるようにする。

前提事実(オーケストレーターが実機で確認済み):

- `herdr integration install claude` → `~/.claude/hooks/herdr-agent-state.sh` 配置 + settings.json の hooks.SessionStart に自エントリを ensure
- `herdr integration install codex` → `~/.codex/herdr-agent-state.sh` 配置 + `~/.codex/hooks.json` に SessionStart エントリ追加 + config.toml の hooks 有効化 ensure
- 両方インストール済み(claude v7 / codex v6、`herdr integration status` で current)

## 変更ファイル

`scripts/update-agent-assets.sh` のみ。

## 仕様

既存の ensure\_\* 関数群(ensure_crit_cli / ensure_ccgate_cli 等)のスタイル・順序感に合わせて追加する:

```bash
# @description Install or refresh the Herdr agent integrations.
function ensure_herdr_integrations() {
    if ! has_command herdr; then
        return 0
    fi

    section "herdr integrations"
    herdr integration install claude
    herdr integration install codex
}
```

- main(または既存の呼び出し列)から適切な位置で呼ぶ(claude/codex 資産の ensure 群の近く)
- 関数コメント(@description)や section 見出しは既存の書式に合わせる
- herdr が無い環境(新規マシンの初期 apply 順序等)では静かにスキップ

## 受入条件

- `make format` で差分が出ない(shfmt)
- shellcheck がリポジトリで走る場合はそれも green
- `bash -n scripts/update-agent-assets.sh` が通る
- **`make require-crit-review` は実行しない・git commit しない**

## 完了報告

```
~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT T2: <サマリ>"
```
