# T1: herdr-agents 冪等化 + zshrc ラッパー失敗可視化 + テスト更新

依頼元: orchestrator-fable5(agmsg team: dotfiles-conformance)
repo: /Users/mryfmo/Workspace/dotfiles(このまま作業。branch 作成・commit は不要 — コミットはオーケストレーターが統合時に行う)

## 背景

ghostty の zsh で素の `herdr` を打つと `home/dot_zshrc` の `herdr()` 関数が `herdr-agents "$PWD" && command herdr` を実行し、`home/dot_local/bin/common/executable_herdr-agents` が「上段 claude / 下段 codex」の 2 ペイン workspace を組む設計。現状の問題:

1. `herdr-agents` は非冪等 — 毎回 `herdr workspace create` するだけで、既存 agents workspace の再利用も死んだエージェントの自己修復もしない
2. ラッパーの `&&` 短絡により bootstrap 失敗時に無言でプロンプトに戻る

## 変更ファイル

1. `home/dot_local/bin/common/executable_herdr-agents`
2. `home/dot_zshrc`
3. `tests/unit/test_herdr_agents.py`

## 仕様 1: herdr-agents 冪等化

`workspace create` の前に検出フェーズを追加する。herdr 0.7.1 の実測 JSON 形状(`--json` フラグは無く出力自体が JSON):

```
herdr workspace list
→ {"id":"cli:workspace:list","result":{"type":"workspace_list","workspaces":[
    {"active_tab_id":"wJ:t1","agent_status":"working","focused":true,"label":"~",
     "number":1,"pane_count":1,"tab_count":1,"workspace_id":"wJ"}]}}
   ※ cwd は含まれない → label 一致だけでは不十分

herdr pane list --workspace <id>
→ {"result":{"panes":[{"agent":"claude","agent_status":"working","cwd":"/Users/mryfmo",
    "foreground_cwd":"...","pane_id":"wJ:p1","tab_id":"wJ:t1","terminal_id":"...","workspace_id":"wJ"}]}}
   ※ cwd と agent フィールド(検出エージェント名 "claude"/"codex" 等、無ければ null/欠落)あり。
     pane rename した label は出力に含まれないため、判定を pane label に依存させない

herdr agent get <name>
→ {"result":{"agent":{"pane_id":"...",...},"type":"agent_info"}}(未登録ならエラー終了)

herdr workspace focus <id> / herdr pane split <pane> --direction down [--no-focus] /
herdr pane swap --direction up 等が利用可能(herdr pane --help / workspace --help で確認可)
```

検出・修復ロジック:

- 検出: `workspace list` から label == `"$(basename "$workdir") agents"` の workspace を列挙し、各候補の `pane list --workspace` に `cwd == $workdir` のペインがあるものを既存 agents workspace と判定(同名 basename の別ディレクトリを排除)
- 既存 workspace あり:
  - claude 健在判定: panes に `agent == "claude"` のペインがある
  - codex 健在判定: `herdr agent get "codex-worker-${wid}"` が返す pane_id が pane list に実在する(agent get が成功しても pane list に無ければ stale 登録として不在扱い)
  - 両方健在 → `herdr workspace focus "$wid"` のみで exit 0
  - codex 不在 → 既存と同じ `herdr agent start "codex-worker-${wid}" --cwd ... --workspace "$wid" --split down --env CLICOLOR_FORCE=1 --env FORCE_COLOR=1 --no-focus -- codex --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=high` を再実行(start が agent_name_taken 等で失敗した場合はエラーメッセージを stderr に出して exit 非 0 — 無言にしない)
  - claude 不在 → agent フィールドが空のペインがあればそこへ `herdr pane rename <pane> claude-orchestrator` + `herdr pane run <pane> "CLICOLOR_FORCE=1 FORCE_COLOR=1 claude --model 'claude-fable-5[1m]' --effort high"` で再起動。無ければ codex ペインを `pane split --direction down` して新ペインに claude を起動し、`herdr pane swap --direction up` で claude を上段に配置
  - 修復後も `workspace focus` して exit 0
- 既存 workspace なし → 現行の新規作成ロジックをそのまま実行
- claude / codex の起動コマンドと agent start 引数は関数または変数に一元化し、新規作成パスと修復パスで重複させない
- 既存のコーディング規約(set -euo pipefail、@file/@brief ヘッダ、function 構文、jq 利用パターン)を維持

## 仕様 2: home/dot_zshrc のラッパー

現行:

```zsh
function herdr() {
    if [[ $# -eq 0 && -n "${GHOSTTY_RESOURCES_DIR:-}" ]]; then
        herdr-agents "${PWD}" && command herdr
        return
    fi
    command herdr "$@"
}
```

変更後(短絡廃止・失敗可視化。失敗してもアタッチする):

```zsh
function herdr() {
    if [[ $# -eq 0 && -n "${GHOSTTY_RESOURCES_DIR:-}" ]]; then
        if ! herdr-agents "${PWD}"; then
            print -u2 "herdr-agents failed; attaching to herdr anyway"
        fi
        command herdr
        return
    fi
    command herdr "$@"
}
```

## 仕様 3: tests/unit/test_herdr_agents.py

現構造: fake `herdr` スクリプトが呼び出しを記録ファイルに書き、`workspace create` / `agent start` に固定 JSON を返す。既存テストは呼び出し列を断言している。

- fake herdr に `workspace list` / `pane list --workspace` / `agent get` / `workspace focus`(必要なら `pane split` / `pane swap`)ハンドラを追加。既定の `workspace list` は空リストを返し、テストごとに応答を差し替えられる構造にする。JSON は上記実測形状に合わせる
- 既存アサーション更新(シーケンス先頭に `workspace list` が入る等)
- 新規テスト(最低限):
  1. 既存 agents workspace(claude+codex 健在)→ `workspace focus` のみで `workspace create` / `agent start` が呼ばれない
  2. codex 死亡(pane list に codex ペイン不在)→ `agent start codex-worker-<wid>` のみ再実行される
  3. claude 死亡(agent 無しペインあり)→ 当該ペインへの `pane run` 再実行
  4. zshrc ラッパー: `herdr-agents` が exit 非 0 でも `command herdr` が呼ばれ、stderr にエラーが出る
- E2E テスト(`test_ghostty_herdr_starts_stacked_agents_with_working_agmsg`)の fake herdr にも `workspace list`(空)ハンドラを追加して壊れないようにする

## 受入条件

- `make unit-test` が green(全テスト。herdr 関連の新規テスト含む)
- `make format` で差分が出ない(shfmt / ruff 等リポジトリのフォーマッタに準拠)
- **`make require-crit-review` は実行しないこと**(オーケストレーターの最終統合工程)
- git commit しないこと

## 完了報告

完了したら以下を実行して報告(1 行サマリ + 変更ファイル + テスト結果):

```
~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT T1: <サマリ。変更ファイル、make unit-test の結果、注意点>"
```

問題・仕様疑義があれば AGMSG-RESULT の代わりに AGMSG-QUESTION で送ること。
