# T4: README の「Herdr and Ghostty agent workspace」節を更新

依頼元: orchestrator-fable5(agmsg team: dotfiles-conformance)
repo: /Users/mryfmo/Workspace/dotfiles(branch 作成・commit 不要)

## 背景

T1 で `herdr-agents` が冪等化され(既存 agents workspace の再利用・死んだエージェントの自己修復)、zshrc ラッパーが失敗時もアタッチするようになった。T2/T3 で herdr 公式 integration(claude/codex)が `update-agent-assets.sh` と agent-config.yaml で維持されるようになった。README の設計記述を実装に追随させる。

## 変更ファイル

`README.md` の「Herdr and Ghostty agent workspace」節のみ。

## 反映内容

1. **冪等動作**: bare `herdr` は毎回新規 workspace を作るのではなく、既存の agents workspace(label + pane cwd で識別)があれば focus し、claude/codex が死んでいればそのペインだけ再生成する
2. **失敗可視化**: `herdr-agents` が失敗しても stderr にエラーを出して `command herdr` にアタッチする(旧: `&&` 短絡で無言終了)
3. **公式 integration**: `herdr integration install claude` / `install codex` が `scripts/update-agent-assets.sh` の `ensure_herdr_integrations` で維持され、claude 側の SessionStart フックは `agent-config.yaml` → `generate-agent-configs.py` 経由で `private_settings.json` にも含まれる(chezmoi apply と herdr install のどちらが先でも収束)。integration により herdr サーバ再起動後にエージェントペインが会話セッションごと復元される(`[session] resume_agents_on_restore`、既定 true)
4. **表記修正**: 既存記述の agent 名 `codex-${workspace_id}` は実装と不一致 → `codex-worker-${workspace_id}` に修正
5. **運用ノート**: dotfiles 更新でラッパー関数が変わった場合、既に開いている ghostty シェルには反映されない — 一度 `exec zsh`(または新規ウィンドウ)が必要である旨を明記

実装の正は T1/T2/T3 適用後のコード(`home/dot_local/bin/common/executable_herdr-agents`、`home/dot_zshrc`、`scripts/update-agent-assets.sh`、`home/dot_agents/agent-config.yaml`)。記述はコードと矛盾しないよう実物を読んで書くこと。既存 README の文体(英語)・トーン・段落構成に合わせる。

## 受入条件

- README の当該節がコードと一致
- `make format` で差分なし(prettier / markdownlint 等が走る場合)
- tests/unit/test_herdr_agents.py に README 内容を検証するテストがある場合は green を維持
- **`make require-crit-review` は実行しない・git commit しない**

## 完了報告

```
~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT T4: <サマリ>"
```
