# CompactionDB × コンテキスト圧縮/メモリ研究 比較分析

- 作成: 2026-08-16(オーケストレータ: Claude Code / Fable-5 xhigh)
- 目的: 下記 3 ソースを精読し、vendored CompactionDB 2.0.0(+dotfiles patches)と比較、
  dotfiles の Claude Code(Fable-5 xhigh)+ Codex(gpt-5.6 Sol high)+ agmsg
  オーケストレーション体制への統合・改善方針を確定する。
- 対応する作業計画: `.orchestration/tasks/PLAN-compactiondb-research-integration.md`

## 0. ソースと比較対象の層の違い

| コンポーネント                                                                           | 層                                     | 一言で                                                                                 |
| ---------------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Factory.ai「Evaluating Context Compression for AI Agents」(2025-12-16, Factory Research) | 圧縮**戦略**+**評価方法論**            | セクション固定の anchored iterative 構造化要約と、プローブベース評価ハーネス           |
| Earendil「How Compaction Works in Pi」(2026-08-13, Earendil Engineering)                 | エージェント内蔵**コンパクション機構** | ターン境界での自動圧縮、直近 20k トークン保持、独立リクエストによる要約                |
| Zero-Mem(arXiv 2607.29377v1, 2026-07-31, Xiao et al.)                                    | **メモリシステム**(検索・想起層)       | LLM 呼び出しゼロ(zero-token)の決定論的メモリ操作。二重ビュー検索                       |
| CompactionDB 2.0.0(`vendor/compactiondb/`)                                               | **証拠台帳+リカバリ注入層**            | フックで全イベントを SQLite に記録し、コンパクション後に決定論的リカバリパケットを注入 |

CompactionDB はコンパクションを実行せず(それは Claude Code 本体の仕事)、要約も生成しない。
比較は「同機能の優劣」ではなく「各者の設計知見のうち、どれが CompactionDB の層に移植可能か」で行う。

## 1. 各ソースの内容(精読要約)

### 1.1 Factory.ai — 評価方法論と anchored iterative summarization

- 最適化目標は「リクエストあたりトークン数」ではなく「**タスク完了までの総トークン数**」。
  過剰圧縮は再取得・再探索でかえって高くつく。
- **プローブベース評価**: 圧縮後のエージェントに、切り捨てた履歴の具体的事実を問う 4 種の
  プローブ(recall=元のエラー、artifact=変更ファイル列挙、continuation=次の作業、
  decision=下した決定)を投げ、GPT-5.2 ブラインド LLM ジャッジが 6 次元
  (accuracy / context awareness / artifact trail / completeness / continuity /
  instruction following)を 0–5 ルーブリックで採点。本番 36,611 メッセージ・数百圧縮点で
  3 方式を同一プレフィクスに適用。
- 結果(総合): **Factory 3.70 > Anthropic 3.44 > OpenAI 3.35**。
  - Factory: intent / file modifications / decisions / next steps の固定セクションを持つ
    **永続要約を差分マージ**(anchored iterative)。「構造が保存を強制する」(checklist 原理)。
  - Anthropic(Claude SDK 組み込み): 構造化要約 7–12k 字だが**毎回フル再生成** → 反復圧縮で
    ドリフト。
  - OpenAI(`/responses/compact`): 圧縮率最高 99.3% だが不透明・検証不能・品質最下位。
- **最重要の負の知見**: artifact trail は全方式で最低次元(2.19–2.45/5)。Factory 自身が
  「要約では解けない。**別立てのアーティファクトインデックスかスキャフォールディング側の
  明示的ファイル状態追跡が必要**」と結論。
- 圧縮率の差はわずか(98.6% vs 99.3%)で品質差 0.35 点 → 「圧縮率は誤った指標」。

### 1.2 Pi(Earendil) — コンパクション機構の設計

- トリガー: (1) 上限接近時の自動(判定は**ターン終了時のみ** — ターン内はキャッシュ済み
  プレフィクスを維持)、(2) `/compact`、(3) ターン途中のオーバーフローエラー。
- 直近メッセージを**設定可能トークン予算(デフォルト 20k ≒ 5–20 ターン)分そのまま保持**、
  それ以前のみ要約対象。
- 要約は既存会話とキャッシュを共有しない**独立リクエスト** → 別システムプロンプト
  (「context summarization assistant」)+**別の安価なモデル**を追加コストなしで使える。
  要約構造は goal / progress / key decisions。
- 要約は**プレーンテキスト**で保存 → モデルを切り替えても継続利用可能(可搬性)。
- コンパクションはプロンプトキャッシュを一度破壊する(保持ターンも別プレフィクス後に来る
  ため再計算)。以後のリクエストは再びキャッシュが効く。

### 1.3 Zero-Mem — zero-token メモリ操作

- 主張: 最終 QA 以外の全メモリ操作(構築・整理・検索・校正)で LLM 呼び出し・トークン消費
  ゼロでも、生成型メモリ(Mem0 / A-Mem / MemoryOS / SimpleMem / GAM 等)を上回れる。
- 機構: 生トレース保存(provenance 保持)+二重ビュー:
  - 関係ビュー: spaCy NER のエンティティ–コンテキスト共起グラフ、活性伝播+
    Personalized PageRank(γ=0.6)。
  - 時系列ビュー: turn / window / episode / local の階層。
  - BM25+BGE-M3 はスコアリング専用。融合は min–max 正規化+重み **ρ=0.6**、
    隣接ユニット・ブリッジ文脈のクロージャ、決定論的フィルタ/校正。
- 結果: LoCoMo 平均 F1 59.15(最強ベースライン GAM +5.4)、HotpotQA 448K でも最良。
  メモリ操作トークン 0、0.22 秒/クエリ(最速ベースライン LightMem 比 57.6% 高速)。
- アブレーション: グラフのみ 62.5 / 階層のみ 54.9 / フル 72.1(HotpotQA 56K F1)
  → **二重ビューの相補性が本質**。
- 留意: zero-token ≠ zero computation(エンコーダ推論等は別勘定)。コードは査読後公開予定。
  ベンチは会話 QA 系でコーディングエージェント検証はない。

## 2. 比較表

| 観点               | Factory 方式                               | Pi コンパクション                                | Zero-Mem                                   | CompactionDB                                                             |
| ------------------ | ------------------------------------------ | ------------------------------------------------ | ------------------------------------------ | ------------------------------------------------------------------------ |
| 概要               | LLM による永続・構造化・差分更新型要約     | ハーネス内蔵の要約型コンパクション               | LLM 非依存の想起・検索システム             | フック駆動の証拠台帳+決定論的リカバリ                                    |
| 特徴               | 構造が保存を強制、差分マージでドリフト抑止 | ターン境界判定・保持予算・要約の独立リクエスト化 | 生トレース保持+二重ビュー検索、完全決定論  | 生イベント保持+redaction+明示マーカー永続記憶                            |
| 機能性             | ◎ 継続性(総合 3.70)                        | ○ 汎用要約                                       | ◎ クエリ条件付き高精度想起                 | ○ 記録・検索・リカバリ・昇格は揃うが想起は recency 基準                  |
| 長所               | 実測最良の圧縮品質、評価手法自体が資産     | キャッシュ配慮、安価モデル委譲、可搬な平文       | トークン 0、高速、出典追跡                 | ローカル・決定論・redaction・監査可能(sha256/lineage)・Claude/Codex 共有 |
| 短所               | LLM 依存、artifact 追跡未解決と自認        | 要約 1 個に全依存、artifact 特別扱いなし         | 重い依存、コード未公開、コーディング未検証 | 抽出的要約のみ、リカバリがクエリ非条件、Codex 手動、E2E 未検証(自認)     |
| 拡張性             | セクション追加は容易(概念)                 | Pi 拡張機構で置換可                              | 実装非公開                                 | ◎ config スキーマ・CLI・semantic.py アダプタあり                         |
| 保守性             | SaaS(手が出せない)                         | 同左                                             | 研究コード                                 | ◎ vendored+パッチ+MANIFEST+validate.py+regression tests                  |
| 効率性(トークン)   | 98.6% 圧縮+LLM 要約コスト                  | 要約 1 回分                                      | ◎ ゼロ                                     | ◎ ゼロ                                                                   |
| 高速性             | LLM 往復 1 回                              | 同左                                             | 0.22 s/query                               | ◎ 非同期フック+スプールで hot path ほぼゼロ                              |
| 可動性(運用可用性) | ベンダー依存                               | Pi 依存                                          | GPU/エンコーダ前提                         | ◎ sqlite3+Python 3.10、WAL+単一ライタ+quarantine+health                  |
| 移植性             | Factory 専用                               | Pi 専用(平文要約は可搬)                          | 理論のみ可搬                               | ◎ per-project 完結、平文、Claude hooks / Codex CLI 両対応                |

**総括**: CompactionDB は Zero-Mem 系(決定論・zero-token・provenance 保持)の思想をフック
基盤上で実装したものに相当し、効率・可搬・保守は既に押さえている。劣位は
(a) リカバリパケット品質(Factory の構造化・評価知見が未適用)、
(b) クエリ条件付き想起の不在(Zero-Mem の検索知見が未適用)。
Factory の負の知見(LLM 要約は artifact trail を保存できない)は、`event_files` を持つ
CompactionDB にとって最大の好機 — 決定論的ファイル台帳の注入で内蔵コンパクションの最弱
次元をゼロトークンで補完できる。

## 3. 統合・改善提案(P1–P7)

| ID  | 由来        | 内容                                                                                                                                                                                                                     | 実装先                      |
| --- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- |
| P1  | Factory     | セッション内 write/edit 全ファイルの決定論的リストをリカバリパケットへ(専用サブ予算、台帳優先の免責文)                                                                                                                   | `recovery.py`               |
| P2  | Factory     | パケットを固定セクション構造(Goal / File modifications / Decisions / Open tasks / Failures / Compact summary)へ。空セクションも見出しを出す(checklist 原理)。DB からの毎回決定論的再合成なのでドリフトは原理的に起きない | `recovery.py`               |
| P3  | Zero-Mem    | `contextdb recall <query>`: FTS5(BM25)+任意 semantic の min–max 正規化 ρ=0.6 融合+クロージャ(同 tool_use_id・隣接 id・同一ファイル共起)。spaCy NER / PageRank は規模不一致のため不採用                                   | `cli.py` ほか               |
| P4  | Factory     | `contextdb probe`: 台帳から ground truth 込みの 4 種プローブを決定論生成(zero-token)。採点は review プロファイル低 effort の別コンテキストで、リカバリ変更 PR 時のみ                                                     | `cli.py` ほか               |
| P5  | Pi/現状是正 | Codex `notify`(agent-turn-complete)→ `contextdb ingest` レシーバでターン粒度の自動証跡。AGMSG-TASK 雛形に `[memory:...]` マーカー/`memory add` の契約を明記                                                              | dotfiles 側スクリプト+skill |
| P6  | agmsg 整合  | ワークツリー分片化は DB 共有では解かず、**ACCEPTANCE 時にオーケストレータがメイン worktree DB へ `memory add --kind decision --scope project` で統合記録**(規約のみ)                                                     | rules / skill               |
| P7  | Pi          | recovery budget 8500 字 →12,000–16,000 字へ(注入はコンパクション毎に一度きり)。メモリ関連の LLM 使用(P4 採点等)は必ず別コンテキスト・下位プロファイルへ                                                                  | `config.json` / 運用規範    |

**不採用(根拠付き)**: OpenAI 型不透明圧縮(検証不能・非可搬)、Mem0/A-Mem 型 LLM 駆動
メモリ操作(Zero-Mem の実測が非 LLM 優位を裏付け)、Zero-Mem フル機構(スケール不一致・
依存過重 — 共起クロージャで測定可能な不足が出るまで導入しない)、CompactionDB のグローバル
自動有効化(追跡ファイル改変・シークレット台帳増殖のため従来判断を維持)。

**推奨着手順**: P6 → (P1+P2+P7 を一体の recovery 改修として) → P5 → P4 → P3 → 配布・E2E。

## 4. 参照

- https://factory.ai/news/evaluating-compression
- https://earendil.com/posts/compaction-in-pi/
- https://arxiv.org/html/2607.29377v1 (Zero-Mem)
- `vendor/compactiondb/`(docs/ARCHITECTURE.md, DATA_MODEL.md, SECURITY.md,
  KNOWN_LIMITATIONS.md)、`.orchestration/tasks/T43-*.md`, `T44-*.md`
