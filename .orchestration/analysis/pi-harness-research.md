# Pi(earendil-works/pi)研究 × dotfiles ハーネス統合分析

- 作成: 2026-08-16(オーケストレータ: Claude Code / Fable-5 xhigh)
- 目的: earendil-works/pi を精読し、dotfiles の運用層(Claude Code + Codex + agmsg +
  permgate + CompactionDB + herdr + 資産ライフサイクル)および被運用エージェント群と
  比較、統合方針(π1–π5)を確定する。
- 対応する作業計画: `.orchestration/tasks/PLAN-pi-worker-integration.md`
- 先行分析: compactiondb-compaction-research.md(Pi のコンパクション記事は分析済み —
  本書はリポジトリ実体の分析)、harness-composability-research.md

## 0. 位置づけ

Pi は Claude Code / Codex と同格の**ハーネス**であり、dotfiles 運用層とは層が異なる。
比較軸は「被運用エージェントとしての Pi vs Claude Code vs Codex」+「Pi の設計が
運用層に提供しうるもの」。

## 1. Pi の実体(2 エージェント精読の要約)

- **出自/規模**: Mario Zechner(+Armin Ronacher)/ Earendil Inc.。MIT。TypeScript /
  Node >=22.19。npm workspaces モノレポ 10 パッケージ(`pi-ai` 統一プロバイダ API、
  `pi-agent-core` ループ、`coding-agent` CLI、`pi-tui`、CBOR `protocol`/`server`/
  `client`、`session-backends/sqlite-node`、`telemetry`、`evals`)。91,083★ /
  271 コントリビュータ / ~5,685 コミット / v0.84.2(2026-08-14)。週次リリース級の
  高速開発(API 変動リスク)。
- **哲学(逐語)**: 「Pi is a minimal terminal coding harness」「aggressively
  extensible so it doesn't have to dictate your workflow」。システムプロンプト+
  ツール定義 <1,000 トークン。MCP / サブエージェント / plan mode / todo /
  background bash を理由付きで排除(拡張領域へ)。
- **ツール**: 実装上 7(`read`/`bash`/`edit`/`write`/`grep`/`find`/`ls`)。
  file-mutation-queue で書込直列化。
- **セッション**: `~/.pi/agent/sessions/<cwd>/{ts}_{id}.jsonl` の**追記専用ツリー**
  (`id`/`parentId`、leaf ポインタ)。エントリ型: SessionHeader / Message /
  ModelChange / ThinkingLevelChange / **Compaction(summary, firstKeptEntryId,
  tokensBefore, details{readFiles, modifiedFiles}, usage)** / BranchSummary /
  Custom(拡張)/ Label / SessionInfo。`/fork` `/clone` `/tree` `/resume`。
  SQLite バックエンド選択可。モデル横断の可搬性が第一級。
- **コンパクション実装**(記事の実体を確認): `contextTokens > contextWindow -
reserveTokens` で発火、`reserveTokens=16384`、`keepRecentTokens=20000`。要約は
  独立リクエスト(`cacheRetention:"none"`)、システムプロンプト冒頭逐語 "You are a
  context summarization assistant..."。チェックポイント構造: Goal / Constraints &
  Preferences / Progress(Done・In Progress・Blocked)/ Key Decisions / Next Steps /
  Critical Context。**既存要約への差分マージ更新プロンプトあり**(Factory 型
  anchored の性質)。ツール結果は 2000 字で切詰めて要約入力へ。
- **拡張 API**: `~/.pi/agent/extensions/*.ts`(global)+ `.pi/extensions/*.ts`
  (project、trust ゲート)を jiti で実行時ロード。イベント約 30 種:
  `tool_call`(**実行前ブロック/改変可** — PermissionRequest 相当)、
  `session_before_compact` / `session_compact`、`turn_start/end`、
  `tool_execution_start/update/end`、`before_provider_request/headers`、
  `model_select`、`input`、`user_bash` 等。`registerTool` / `registerCommand` /
  `registerProvider` / UI(`confirm`/`select`/`notify`/widget)。
  **サンドボックスなし・in-process フル権限**(ゲートはプロジェクト信頼のみ。
  `defaultProjectTrust` で非対話時挙動を設定)。
- **外部駆動面(運用層として最重要)**:
  1. SDK: `createAgentSession()` → `session.prompt()` が**ターン完了で resolve**、
     `subscribe()` でイベント購読(`agent_end`, `agent_settled` 等)。
  2. **RPC モード**: stdin/stdout JSONL。コマンド 30+(`prompt`/`steer`/`follow_up`/
     `abort`/`fork`/`get_tree`/`get_last_assistant_text`/`set_model`/`compact`/
     `export_html` 等)、`id` 相関レスポンス+イベントストリームで完了検出。
  3. ヘッドレス: `pi -p` / `--mode json`(1 行 1 イベント)。
- **プロバイダ**: 25+(anthropic, openai, openai-codex, github-copilot, google,
  bedrock, deepseek, openrouter, llama.cpp ルータ等)。購読認証(`/login`:
  Claude Pro/Max、ChatGPT Plus/Pro、Copilot)+ API キー。**セッション途中の
  モデル切替が第一級**(ModelChangeEntry として記録)。
- **セキュリティ姿勢(逐語)**: 「Pi does not include a built-in permission system
  for restricting filesystem, process, network, or credential access.」—
  コンテナ化前提。公式想定ユースケースに「Permission gates(tool_call で確認)」。
- **実測効率**(Earendil の Databricks 評価): Pi+Opus 4.8 xhigh が最高パス率を
  Claude Code / Codex より大幅低コストで達成、「ターンあたり送信コンテキスト約 1/3」。
- **コスト可視化**: TUI フッターにトークン/セッション費、`/session` 統計、
  compaction・ツールまで使用量計上。

## 2. 比較表(被運用エージェント軸+運用層)

| 観点   | Pi                                                                       | Claude Code                                | Codex CLI                   | dotfiles 運用層                   |
| ------ | ------------------------------------------------------------------------ | ------------------------------------------ | --------------------------- | --------------------------------- |
| 概要   | 極小・可鍛性最優先のハーネス                                             | フル機能ハーネス(本体制)                   | OpenAI 公式ハーネス         | ハーネス合成・統制層              |
| 特徴   | <1k 固定部、ツリーセッション、拡張で全て                                 | フック 15 種・スキル・権限系               | notify・profile・最小 hooks | 宣言 → 生成 → 検証 →drift→ 逆写像 |
| 機能性 | ○(コア 7 ツール+拡張)                                                    | ◎                                          | ○                           | ◎(統制)                           |
| 長所   | **外部駆動面が最良**(RPC/SDK/JSON)、効率 1/3、プロバイダ非依存、後処理性 | Fable-5 xhigh 供給、フック可観測性、権限系 | gpt-5.6 系供給、軽量        | fail-closed、証跡、可逆性         |
| 短所   | **権限システム不在(YOLO)**、拡張無サンドボックス、API 変動               | 固定部が重い、内部不透明                   | フック貧弱(turn 粒度)       | ハーネス内部に介入不能            |
| 拡張性 | ◎(30 イベント+登録系)                                                    | ○                                          | △                           | ○                                 |
| 保守性 | ○(依存小、但し高速開発追随)                                              | △                                          | △                           | ◎                                 |
| 効率性 | ◎(実測 1/3)                                                              | △                                          | ○                           | —                                 |
| 可動性 | ○(trust の非対話設定要)                                                  | ◎                                          | ◎                           | ◎                                 |
| 移植性 | ◎(mac/Linux/Win/Termux、モデル可搬)                                      | ○                                          | ○                           | ◎                                 |
| 高速性 | ◎(差分描画、Bun バイナリ)                                                | ○                                          | ○                           | —                                 |
| 成熟度 | 1 年・91k★・週次(変動リスク)                                             | 成熟                                       | 成熟                        | 実証済み                          |

## 3. 体制にとっての本質

Pi は現行体制の最大ペイン 2 つを構造的に解く:

1. **ワーカー駆動の脆さ**: pane run 注入(bracketed-paste 事故多発)+Stop フック+
   notify の現行 Codex 駆動に対し、Pi は **RPC 直結**(`prompt` 送信・`agent_end`
   完了検出)でペーン駆動を不要化できる。
2. **捕捉粒度の非対称**: CompactionDB は Claude=15 フック vs Codex=turn 粒度。Pi は
   `tool_execution_end` 購読で **Claude 並みのツール粒度捕捉が拡張 1 ファイル**。

決定的欠落は権限システム。ただし `tool_call` ブロックという受け皿があり、permgate を
Pi 拡張として接続できる(公式想定ユースケース)。

## 4. 統合提案(π1–π5)

| ID  | 内容                                                                                                                                                                                                                                           | 実装先                                                                      |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| π2  | **permgate × Pi(前提条件)**: `tool_call` で bash/write/edit を捕捉し `permgate pi` を呼ぶ拡張。非対話(RPC)時は fail-closed で deny                                                                                                             | permgate(provider 追加)+ `~/.pi/agent/extensions/permgate.ts`(chezmoi 配布) |
| π1  | **Pi ワーカー PoC(RPC 直結 agmsg ブリッジ)**: `pi --mode rpc` を子に持つブリッジが inbox→`prompt`、`agent_end`→RESULT 検出。identity `pi-<profile>-dot`。第一手順は**モデルアクセス実証**(購読認証での Fable 系/effort 対応・規約適合は未確認) | 新ブリッジスクリプト+model_profiles pi 節+agmsg                             |
| π3  | **CompactionDB × Pi**: 拡張が `tool_execution_end`/`turn_end`/`session_compact` を `contextdb ingest --ingested-from pi` へ(T48b トークン検証は `pi` を受理)。`session_before_compact` で台帳由来トレイルの要約入力注入は将来拡張              | `~/.pi/agent/extensions/contextdb.ts`                                       |
| π4  | **コスト A/B**: express/standard 級タスクを Pi+同モデルで走らせ probe(T49)で採点、ワーカーハーネス配置をデータで決定                                                                                                                           | 実験手順(orchestrator 主導・有界)                                           |
| π5  | **セッションツリー証跡連携**: CompactionEntry.details 等を受入記録へ機械抽出                                                                                                                                                                   | 小スクリプト or 受入手順                                                    |

**不採用**: オーケストレータの Pi 置換(Fable-5 xhigh 供給と permgate/CompactionDB/
スキル統合深度は Claude Code 側)/π2 なしの Pi 実運用(YOLO のまま実リポジトリ禁止)/
MCP 的拡張。

**リスク**: v0.8x の API 変動(→ mise で**バージョンピン**、拡張はピン版に対して
regression test)、拡張の無サンドボックス(→ 配布拡張は chezmoi 管理+検証対象)、
購読認証の対話性(→ 導入は operator 手順、ヘッドレスは API キー系で検証)。

**推奨順序**: π2 → π1(スクラッチ+worktree 限定 PoC)→ π3 → π5 → π4。

## 5. 参照

- https://github.com/earendil-works/pi(README、packages/*、core/extensions、
  core/compaction、core/session-manager、modes/rpc)
- https://pi.dev/docs/latest(extensions / sessions / security / RPC / SDK)
- https://earendil.com/posts/compaction-in-pi/ ・ /pi-autoresearch-and-databricks/
- founder essay: mariozechner.at/posts/2025-11-30-pi-coding-agent/
