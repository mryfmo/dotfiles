# T3: agent-config.yaml + generator に herdr SessionStart フックを追加し再生成

依頼元: orchestrator-fable5(agmsg team: dotfiles-conformance)
repo: /Users/mryfmo/Workspace/dotfiles(branch 作成・commit 不要)

## 背景

`~/.claude/settings.json` は `home/dot_claude/private_settings.json` として chezmoi 全体管理されており、その実体は `scripts/generate-agent-configs.py` が `home/dot_agents/agent-config.yaml` から生成する成果物(直接手編集禁止。`--check` で鮮度検証あり)。

`herdr integration install claude` が実機 settings.json に追加するエントリを生成物にも含めることで、chezmoi apply と herdr install のどちらが先に走っても収束するようにする。

## オーケストレーターが実機で採取した追加エントリ(正確な形)

`~/.claude/settings.json` の `hooks` 配下に以下が追加された:

```json
"SessionStart": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "bash '/Users/mryfmo/.claude/hooks/herdr-agent-state.sh' session",
        "timeout": 10
      }
    ]
  }
]
```

注意:

- command のパスはシングルクォート付きの絶対パス。chezmoi テンプレート化する場合は `{{ .chezmoi.homeDir }}` 展開後にこの文字列と完全一致すること(herdr の ensure は文字列一致で no-op 判定するため、一致しないと重複エントリが増える)
- `timeout: 10` と `matcher: "*"` を正確に保持すること
- codex 側(~/.codex/hooks.json)は chezmoi 非管理のため repo 変更不要

## 変更ファイル

1. `home/dot_agents/agent-config.yaml` — claude セクションの hooks に herdr セッションフックの定義を追加(既存の hooks キーの記述スタイルに合わせる)
2. `scripts/generate-agent-configs.py` — claude settings のレンダリングに hooks.SessionStart エントリの出力を追加(既存の PermissionRequest / PreToolUse / PostToolUse レンダリングのパターンに従う)
3. `home/dot_claude/private_settings.json` — generator 実行で再生成(手編集しない)

## 手順

1. agent-config.yaml と generate-agent-configs.py の既存構造を読み、herdr フックの表現方法を既存パターンに合わせて設計
2. `uv run --with pyyaml scripts/generate-agent-configs.py` で再生成
3. `uv run --with pyyaml scripts/generate-agent-configs.py --check` が green
4. 生成された private_settings.json の SessionStart エントリが上記採取形(展開後)と一致することを確認
5. `make validate-agent-assets` が green
6. `make unit-test` が green(既存テストを壊していないこと)

## 受入条件

- 上記 3〜6 がすべて green
- 生成物の diff が SessionStart 追加(+既存生成差分があればそれも報告)に限定されている
- **`make require-crit-review` は実行しない・git commit しない**

## 完了報告

```
~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT T3: <サマリ>"
```
