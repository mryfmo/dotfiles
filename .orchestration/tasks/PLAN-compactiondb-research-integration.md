# PLAN: CompactionDB 研究知見統合(P1–P7)実装・検証計画

- 作成: 2026-08-16(オーケストレータ: Claude Code / Fable-5 xhigh)
- 根拠分析: `.orchestration/analysis/compactiondb-compaction-research.md`
- 体制: Claude Code(Fable-5 xhigh)=オーケストレータ(タスク発行・受入審査・crit 審査・
  ライブ E2E 判定)。Codex(標準ワーカープロファイル)=実装ワーカー(agmsg AGMSG-TASK 経由、
  単一 worktree・逐次割当)。モデル名は identity に含めない(`model_profiles` が唯一の出典)。
- スコープ境界(勝手な解釈の禁止): 本計画のタスクは分析文書 P1–P7 の記載内容のみを実装する。
  記載外の機能追加(spaCy/NER、PageRank、UserPromptSubmit 自動注入、グローバル自動有効化、
  JSON 形式のリカバリパケット等)は明示的に禁止。仕様が曖昧な点はワーカーが実装で解釈せず、
  AGMSG で質問を返す。

---

## フェーズ構成と依存関係

| フェーズ | 内容                                 | タスク                            | 依存                                                  |
| -------- | ------------------------------------ | --------------------------------- | ----------------------------------------------------- |
| Phase 0  | 分析・計画のドキュメント化           | T45-0(本書+分析文書)              | なし(完了済み扱い、コミットで完了)                    |
| Phase 1  | 規約整備(P6)                         | T45                               | Phase 0                                               |
| Phase 2  | recovery 改修(P1+P2+P7)              | T46(config)、T47(recovery packet) | Phase 0(Phase 1 と並行可だが同一 worktree のため逐次) |
| Phase 3  | Codex 捕捉パリティ(P5)               | T48                               | Phase 2(ingest 形式が recovery に載るため)            |
| Phase 4  | プローブ評価(P4)                     | T49                               | Phase 2(新パケットを評価対象とするため)               |
| Phase 5  | recall CLI(P3)                       | T50                               | Phase 2(config 基盤)。Phase 3/4 とは独立              |
| Phase 6  | 配布・ライブ E2E・オールグリーン・PR | T51                               | Phase 1–5 全完了                                      |

vendor 改修タスク(T46/T47/T49/T50)は各タスク内で CHANGELOG 追記+MANIFEST.sha256 再生成
まで行い、**各タスク完了時点で vendor が単独オールグリーン**であることを不変条件とする
(T44 の運用を踏襲)。

共通事項(全タスク):

- ワーカー禁止事項: `git commit` / `git push` / `chezmoi apply` / ローカル bats 実行 /
  依存追加 / 許可ファイル外の編集。
- ワーカー成果物(WP-K 形式): report `.orchestration/reports/<ID>.md`、
  validation `.orchestration/validation/<ID>.txt`、sandbox `.orchestration/sandboxes/<ID>.md`、
  learning `.orchestration/learning/<ID>.md`、autoskill `.orchestration/autoskill/runs/<ID>.md`。
- 受入: オーケストレータが RESULT を敵対的に審査(正しさ・回帰・セキュリティ・報告漏れ。
  再導出・反証を試み、サンプル確認を全数検証と見なさない)。
- Python 実行は uv 方針(リポジトリ側)/vendor 内は `make -C vendor/compactiondb` 経由。
- シェルスクリプトは shdoc 形式コメント(英語)+`shfmt --indent 4 --space-redirects` 準拠。

---

## Phase 0: ドキュメント化

### T45-0(オーケストレータ直轄・完了済み、コミットのみ残)

- 作業内容:
  1. `.orchestration/analysis/compactiondb-compaction-research.md` 作成(済)。
  2. 本計画書 `.orchestration/tasks/PLAN-compactiondb-research-integration.md` 作成(済)。
  3. 評価: 実装 PR とは分離し、`.orchestration` 証跡同期のバッチコミット規約で commit する。
- 検証条件: 両文書が存在し、P1–P7 の定義・不採用リスト・着手順が分析文書と本書で矛盾しない。
- 検証内容: オーケストレータが両文書を突合(diff 読み)。
- 完了条件: 両文書がコミットされている(コミットメッセージに文書名を明記)。

### Phase 0 完了条件

T45-0 完了。以降のタスク文面はすべて本書から切り出して発行する(口頭仕様の禁止)。

---

## Phase 1: 規約整備(P6 — コード変更なし)

### T45: 受入時記憶統合と AGMSG-TASK 契約の規約化

- 担当: Codex ワーカー(文書編集)/最終文言承認はオーケストレータ。
- 許可ファイル:
  - `home/dot_config/claude/rules/compactiondb.md`
  - `home/dot_config/claude/rules/agmsg-orchestration.md`
  - `home/dot_agents/skills/agmsg-orchestration/SKILL.md`(および同スキル内の TASK 雛形節)
  - `home/dot_claude/skills/agmsg-orchestration/` 配下の対応物(symlink/コピーの実態を
    確認し、単一ソースなら触らない)
  - 成果物パス
- 作業順序と内容:
  1. `home/dot_claude/skills/agmsg-orchestration` と `home/dot_agents/skills/agmsg-orchestration`
     の関係(symlink か重複実体か)を `ls -la` で確認し、編集すべき単一ソースを特定して
     report に記録する。
  2. `compactiondb.md` に追記(1–2 行): 「agmsg 並列 worktree 構成では DB を worktree 間で
     共有しない。受入(ACCEPTANCE)時にオーケストレータがメイン worktree の DB へ
     `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` で
     採択決定を統合記録する。ワーカー worktree の DB は worktree ごと破棄してよい」。
  3. `agmsg-orchestration.md` の受入・証跡同期の節に追記(1 行): 「`.orchestration` 同期
     バッチ時、accepted タスクの decision 記録漏れがないか確認する」。
  4. スキルの AGMSG-TASK 雛形に契約を追記: 「RESULT には永続化すべき事実を
     `[memory:decision]` / `[memory:failure]` マーカー(T44 の tag/bracket 形式・kind 別名
     規約)で明記する。CompactionDB 導入済みプロジェクトのワーカーは完了前に
     `contextdb_cli.py memory add` を実行し、実行コマンドを RESULT に含める」。
  5. 追記はいずれも既存文体(英語 rules は英語、日本語文書は日本語)に合わせる。
- 検証条件:
  - 追記が上記の意味論と一致し、既存規約(並列規約・identity 規約・store 規約)と矛盾しない。
  - 差分が許可ファイルのみ。マーカー規約の記述が vendor README(T44 後)と一致する。
- 検証内容:
  1. `git diff --stat` が許可ファイルのみであること。
  2. `git diff` 全文をオーケストレータが読み、compactiondb.md / agmsg-orchestration.md /
     SKILL.md / vendor README の 4 者間でマーカー形式・コマンド名・スコープ名を突合。
  3. `make validate-agent-assets` がグリーン(rules/skills はアセット検証対象)。
- 完了条件: 上記検証全通過+オーケストレータ受入(ACCEPTANCE 記録)+report/validation/
  sandbox/learning/autoskill の 5 成果物が揃う。

### Phase 1 完了条件

T45 受入完了。以降のタスク発行文に T45 で規約化した RESULT 契約を実際に適用する。

---

## Phase 2: recovery 改修(P1+P2+P7)

### T46: config スキーマ拡張(リカバリ予算とセクションサブ予算)

- 担当: Codex ワーカー。
- 許可ファイル: `vendor/compactiondb/.claude/contextdb/contextdb/config.py`、
  `vendor/compactiondb/.claude/contextdb/config.json`、
  `vendor/compactiondb/tests/test_recovery.py`(config 読込テストの置き場が別なら該当
  テストファイル)、`vendor/compactiondb/docs/DATA_MODEL.md` または該当 docs、
  `vendor/compactiondb/CHANGELOG.md`、`vendor/compactiondb/MANIFEST.sha256`、成果物パス。
- 作業順序と内容:
  1. 現行 config スキーマの recovery 節(予算 8500 字、prompts 4 / events 12 / files 12 /
     failures 5)を読み、キー名の既存命名規則を report に記録する。
  2. 変更(P7): recovery 総予算デフォルトを 8500 → **12000** 字に引き上げる。
  3. 追加(P1): `recovery.files_budget_chars`(デフォルト **2000**)を新設。
     既存キーとの整合(命名・型・バリデーション)を保つ。
  4. 追加(P2): セクション見出しの有効/無効ではなく、**固定セクション順序はコード側定数**と
     し、config には予算値のみ置く(セクション構造の可変化はスコープ外)。
  5. 未知キー・型不正時の挙動が既存実装(無視 or エラー)と同一であることをテストで固定。
  6. ユニットテスト: (a) デフォルト値 12000/2000 の読込、(b) 明示指定の上書き、
     (c) 型不正時の既存例外系。
  7. CHANGELOG に `2.0.0+dotfiles.3` 節を起こし config 変更を記載。MANIFEST.sha256 再生成。
- 検証条件: 既存全テストが無改変で通る(後方互換)。新設キー未指定の旧 config.json でも
  動作する。インストール済みプロジェクトの既存 config を壊さない(install.py は既存
  config.json を上書きしない仕様の維持)。
- 検証内容:
  1. `make -C vendor/compactiondb test` 全緑(新規テスト含む)。
  2. `make -C vendor/compactiondb validate` 全 10 チェック緑(ruff lint・MANIFEST・install
     smoke 含む)。
  3. `git diff --stat` が許可ファイルのみ。
- 完了条件: 検証全通過+受入+5 成果物。

### T47: リカバリパケットの固定セクション化+決定論的アーティファクトトレイル

- 担当: Codex ワーカー。依存: T46。
- 許可ファイル: `vendor/compactiondb/.claude/contextdb/contextdb/recovery.py`、
  `vendor/compactiondb/tests/test_recovery.py`、`vendor/compactiondb/docs/ARCHITECTURE.md`、
  `vendor/compactiondb/README.md`(パケット例の節)、CHANGELOG、MANIFEST、成果物パス。
- 作業順序と内容(仕様 — 解釈余地を残さない):
  1. `build_recovery_context()` を次の**固定セクション順**に再構成する(P2)。空でも見出しを
     出力し `(none)` を置く(checklist 原理)。全体は現行どおりプレーンテキスト。
     1. **Header**(必須・現行踏襲): project/session ID+evidence 免責文。免責文に 1 文追加:
        「If the compact summary conflicts with the sections below, the ledger-derived
        sections are authoritative.」
     2. **Goal**: セッション最初の UserPromptSubmit の summary(240 字上限は既存 capture
        仕様に従う)+当該セッションで抽出された explicit `[memory:...]` 候補のうち
        kind=decision の最新 1 件(存在時)。
     3. **File modifications**(P1): 当該セッションの `event_files` から operation ∈
        {write, edit} の全ファイルを重複排除し、各ファイル 1 行
        `<path> (<最終 operation>, <当該 opの回数>x)` で列挙。並びは最終操作の新しい順。
        サブ予算 `files_budget_chars`(T46)内に収め、超過時は古いものから落とし
        `… and N more modified files (see contextdb files)` を末尾に置く。read/search は
        このセクションに入れず、既存の recent files(直近 12 件)相当は
        **Recent activity** として write/edit リストの後に置く。
     4. **Decisions**: project スコープ durable memories の階層レンダリング(現行実装を
        このセクションへ移設)+当該セッションの kind=decision session memories。
     5. **Open tasks**: kind=open_task の active memories+(TaskCreated − TaskCompleted)
        の未完了差分(イベント台帳から tool_use_id/タスク ID で突合)。
     6. **Failures**(現行踏襲: 5 件)。
     7. **Compact summary**(Claude 生成分・現行の 3000 字上限踏襲)を**最後**に「参考」と
        して置く(台帳優先の原則を配置でも表現)。
  2. 予算配分: Header と File modifications を必須先取りとし、残りを現行の
     truncate-middle 規則で配分。総予算は T46 の 12000 字。
  3. 決定論性の維持: 本タスクで LLM 呼び出し・外部プロセス起動を一切追加しない。
  4. ユニットテスト(最低限、各 1 ケース以上):
     (a) write/edit 混在+同一ファイル複数回編集 → 重複排除と最終 operation 表示、
     (b) files サブ予算超過 → 切詰めと "N more" 行、
     (c) 空セッション → 全セクション見出し+`(none)`、
     (d) compact summary との併存 → セクション順と免責文、
     (e) 旧テスト全緑(意図的に出力形式が変わるテストは新仕様値へ更新し、更新理由を
     テスト内コメントで 1 行説明)、
     (f) TaskCreated/TaskCompleted 差分の Open tasks 反映。
  5. docs(ARCHITECTURE.md のリカバリ経路図・README のパケット例)を新形式に更新。
  6. CHANGELOG `2.0.0+dotfiles.3` 節に追記。MANIFEST 再生成。
- 検証条件:
  - パケット総文字数が予算内(境界値テストで固定)。
  - redaction 済みデータのみがパケットに載る(既存の redaction 経路を迂回しない —
    セクション追加は storage 読み出しのみで生データを再取得しない)。
  - session スコープ memories が他セッションへ漏れない(既存不変条件の維持)。
- 検証内容:
  1. `make -C vendor/compactiondb test` / `make -C vendor/compactiondb validate` 全緑。
  2. ワーカーがテスト用フィクスチャで生成した実パケット全文を validation 成果物に貼付し、
     オーケストレータがセクション順・免責文・切詰め表示を全数目視。
  3. `git diff` 全文審査(特に recovery.py の予算計算と SQL)。
- 完了条件: 検証全通過+受入+5 成果物。

### Phase 2 完了条件

T46・T47 受入完了、vendor 単独オールグリーン(`make -C vendor/compactiondb test && make -C
vendor/compactiondb validate`)、CHANGELOG/MANIFEST 更新済み。

---

## Phase 3: Codex 捕捉パリティ(P5)

### T48: Codex notify → contextdb ingest レシーバ

- 担当: Codex ワーカー。依存: T47。
- 許可ファイル: `home/dot_local/bin/common/executable_contextdb-codex-notify`(新規)、
  Codex プロファイル config 生成元(`home/dot_codex/modify_*.config.toml` または
  `home/dot_agents/agent-config.yaml` のレンダリング — 手順 1 で特定した単一注入点のみ)、
  `home/dot_config/codex/AGENTS.md`(Codex 向け使用手順の追記)、成果物パス。
  vendor 改変なし(既存 `ingest` サブコマンドと `ingested_from='codex'` を使う)。
- 作業順序と内容:
  1. Codex `notify` 設定の注入点を特定する: `agent-config.yaml` → プロファイル config の
     生成機構を読み、`notify = ["<command>"]` を worker 用プロファイルに入れる正規の場所を
     確定して report に記録(推測で複数箇所に書かない)。
  2. レシーバ実装(`executable_contextdb-codex-notify`、bash、shdoc コメント英語):
     - 引数: Codex が渡す JSON ペイロード(`agent-turn-complete` イベント)。
     - 動作: `cwd`(ペイロード内のプロジェクトパス)に `.claude/hooks/contextdb_cli.py` が
       存在する場合のみ、ペイロードを `python3 .claude/hooks/contextdb_cli.py ingest` へ
       渡す。存在しなければ **exit 0 で無音スキップ**(未導入プロジェクトで失敗させない)。
     - タイムアウト 5 秒、失敗時も exit 0(notify がワーカーターンを阻害しないこと)。
       失敗は stderr へ 1 行(Codex 側ログで追跡可能に)。
     - `AGMSG_STORAGE_PATH` 等の環境には一切触れない(contextdb は env 非依存)。
  3. `ingest` の入力スキーマ(vendor docs/HOOKS.md)にペイロードを正規化するのは
     レシーバ側の責務: event_type は turn 粒度(`codex_turn_complete` 相当の既存許容値)に
     マップし、`ingested_from='codex'` で記録されることを確認する。既存スキーマで受けられ
     ない場合は**実装せず**、スキーマ差分を AGMSG で報告して指示を仰ぐ(vendor 改変は本
     タスクの許可外)。
  4. Codex 向け AGENTS.md に、自動 ingest の存在と手動 `memory add` 契約(T45)の関係を
     3 行以内で追記。
  5. 静的検証: `bash -n`、`shfmt --indent 4 --space-redirects --diff`(対象は新規スクリプト)。
- 検証条件:
  - 未導入プロジェクトで exit 0・無出力。導入済みプロジェクトで events 行が
    `ingested_from='codex'` として増える。壊れた JSON でも exit 0+stderr 1 行。
  - notify 設定が対象プロファイルのみに入り、他プロファイルへ波及しない。
- 検証内容:
  1. ワーカー: スクラッチの一時ディレクトリ(`compactiondb-install` 済み/未導入の 2 面)で
     レシーバへ実ペイロード形式の JSON を渡し、`sqlite3` で events 増分と
     `ingested_from` 値を確認。壊れ JSON・タイムアウトの 3 ケースを validation に記録。
     (これはローカル実行可能な統合テスト。bats ではないので実行可)
  2. `make format`(shfmt diff)がリポジトリ全体でグリーン。
  3. `make validate-agent-assets` グリーン。
  4. `git diff --stat` が許可ファイルのみ。
- 完了条件: 検証全通過+受入+5 成果物。**ライブ検証(実 Codex ワーカーの notify 発火)は
  T51 の E2E に含める**(本タスク単体では合否にしない)。

### Phase 3 完了条件

T48 受入完了。レシーバと notify 設定が chezmoi ソースに存在し、静的検証グリーン。

---

## Phase 4: プローブ評価(P4)

### T49: `contextdb probe` サブコマンド(決定論的プローブ生成)

- 担当: Codex ワーカー。依存: T47。
- 許可ファイル: `vendor/compactiondb/.claude/contextdb/contextdb/cli.py`、必要なら同
  パッケージ内新モジュール `probe.py`、`vendor/compactiondb/tests/test_cli.py`(または
  新規 `tests/test_probe.py`)、`vendor/compactiondb/README.md`、docs、CHANGELOG、
  MANIFEST、成果物パス。
- 作業順序と内容:
  1. `probe --session <id> [--json]` を新設。**LLM 呼び出しなし**。出力は JSON:
     `{"probes": [{"type": ..., "question": ..., "ground_truth": ...}]}`。
  2. プローブ生成規則(Factory の 4 型の決定論版 — ground truth は台帳から機械抽出):
     - recall: 当該セッション最初の PostToolUseFailure(なければ最初の failure イベント)の
       summary を ground truth に、「What was the first error in this session?」を生成。
       failure が無ければこの型はスキップ(空配列要素を作らない)。
     - artifact: `event_files` の write/edit 集合(T47 と同一クエリを再利用)を ground truth
       に、「Which files were modified in this session?」を生成。
     - decision: 当該セッション+project スコープの kind=decision memories を ground truth
       に、「What decisions were made?」を生成。0 件ならスキップ。
     - continuation: T47 の Open tasks 導出(open_task memories+Task 差分)を ground truth
       に、「What remains to be done?」を生成。0 件ならスキップ。
  3. 採点はスコープ外(オーケストレータ側の運用: review プロファイル・低 effort・別
     コンテキストで、リカバリロジック変更 PR のときのみ実施 — この運用文を README の
     probe 節に 2 行で明記)。
  4. ユニットテスト: 4 型それぞれ (a) 正常生成、(b) 対象 0 件時スキップ、(c) JSON スキーマ
     (キー名・型)固定、(d) 他セッションのデータが ground truth に混入しない。
  5. CHANGELOG 追記(`2.0.0+dotfiles.3` 節)、MANIFEST 再生成、`--help` 文言追加。
- 検証条件: probe 実行が DB を一切書き換えない(read-only。実行前後で
  `sqlite3 ... "PRAGMA data_version"` 相当またはファイル mtime/内容ハッシュ不変)。
  T47 のセクション導出と probe の ground truth が同一クエリ由来で一致する。
- 検証内容:
  1. `make -C vendor/compactiondb test` / `validate` 全緑。
  2. ワーカーはフィクスチャセッションで probe 出力全文を validation に貼付。
     オーケストレータが T47 のパケットと ground truth の整合を突合。
- 完了条件: 検証全通過+受入+5 成果物。

### Phase 4 完了条件

T49 受入完了、vendor 単独オールグリーン。

---

## Phase 5: recall CLI(P3)

### T50: `contextdb recall` — 二重ビュー融合検索

- 担当: Codex ワーカー。依存: T46。
- 許可ファイル: `vendor/compactiondb/.claude/contextdb/contextdb/cli.py`、新モジュール
  `recall.py`(推奨)、`config.json`/`config.py`(`recall.rho` デフォルト 0.6、
  `recall.k` デフォルト 5 の 2 キーのみ追加)、`tests/test_recall.py`(新規)、README、
  docs、CHANGELOG、MANIFEST、成果物パス。
- 作業順序と内容:
  1. `recall "<query>" [--session <id>] [--k N] [--json]` を新設。LLM 呼び出しなし。
  2. スコアリング(Zero-Mem §3.3–3.4 の縮約 — 分析文書 P3 の仕様に限定):
     - 語彙ビュー: `events_fts` と `memories_fts` の BM25 スコア(FTS5 rank)。
     - 意味ビュー: `semantic.py` の外部埋め込みが**設定済みの場合のみ** memories の
       埋め込み cos 類似。未設定なら語彙ビュー単独(決定論を保つ。エラーにしない)。
     - 各ビューを min–max 正規化(ビュー内 max=min のとき 1.0、不在 0.0 — Zero-Mem の
       正規化規則)し、`S = rho * lexical + (1 - rho) * semantic`(ρ=0.6、config 可変)。
     - クロージャ: 上位ヒットイベントに対し (a) 同一 `tool_use_id` のイベント、
       (b) id 隣接(±1)の同一セッションイベント、(c) 同一ファイルを触った他イベント
       (event_files 結合)を引き込み、event_uuid で重複排除。クロージャ追加分はスコア
       継承(親ヒットのスコア × 0.5、順位は親の直後)。
     - 出力: 上位 k 件を `<score> <ts> <type> <summary>`(--json 時は全カラム)で表示。
  3. PageRank・NER・埋め込みの新規生成は実装しない(明示的スコープ外)。
  4. ユニットテスト: (a) 語彙のみ環境での順位再現(固定フィクスチャで期待順序を固定)、
     (b) semantic 有効時の融合スコア計算(埋め込みはテスト用フェイクコマンドで注入 —
     test_semantic.py の既存手法を踏襲)、(c) min–max 縮退ケース(全同点・単一件)、
     (d) クロージャの 3 経路と重複排除、(e) `--session` フィルタの漏れなし、
     (f) read-only 保証(probe と同一の検証手法)。
  5. README に用途(ワーカーのタスク着手時 recall、受入時の過去失敗照合)を記載。
     CHANGELOG 追記、MANIFEST 再生成。
- 検証条件: FTS トークナイザ(trigram/unicode61)双方で動作(既存のトークナイザ選択
  ロジックに従う)。1 万イベント規模のフィクスチャで 1 秒以内(決定論・非 LLM の確認を
  兼ねた性能スモーク。値は validation に記録)。
- 検証内容: `make -C vendor/compactiondb test` / `validate` 全緑+ワーカーの実行例
  (クエリ 3 種: ファイルパス完全一致・日本語語句・英語語句)を validation に貼付し、
  オーケストレータが期待ヒットを台帳と突合。
- 完了条件: 検証全通過+受入+5 成果物。

### Phase 5 完了条件

T50 受入完了、vendor 単独オールグリーン。

---

## Phase 6: 配布・ライブ E2E・オールグリーン・PR(T51)

### T51: 統合・配布・E2E(オーケストレータ主導。ライブ操作以外の修正はワーカーへ差し戻し)

- 作業順序と内容:
  1. **ブランチ/worktree**: 現 worktree には無関係の変更(mise config/lock)があるため、
     AGENTS.md の規約どおりデフォルトブランチから専用 `git worktree` を作成し、本計画の
     変更のみを載せる(mise ペアは別 chore コミット規約の対象で本 PR に混ぜない)。
  2. **配布**: `make update`(update-agent-assets.sh)で `~/.agents/compactiondb/` へ同期
     (state/spool/health 除外の rsync 仕様が維持されることを確認)。導入済みプロジェクト
     を洗い出し(`find` で `.claude/contextdb` を持つ管理下プロジェクト)、各プロジェクトで
     `compactiondb-install <path>` を再実行してフック/ランタイムを更新(既存 config.json は
     上書きされない仕様のため、T46 の新キーはデフォルト値で有効化されることを確認)。
  3. **ライブ E2E(合否判定はオーケストレータ)**:
     - E2E-1(リカバリ): スクラッチプロジェクトに `compactiondb-install` → 実 Claude Code
       セッションで write/edit を伴う作業 →`/compact`(または自動コンパクション)→
       再開時 additionalContext に T47 の固定セクション(特に File modifications の実
       ファイル一致・免責文・予算内サイズ)が現れることを確認し、パケット全文を
       `.orchestration/validation/T51-e2e.txt` に保存。
     - E2E-2(Codex notify): 実 Codex ワーカー(herdr ペーン、worker プロファイル)で
       1 ターン実行 →`sqlite3` で `ingested_from='codex'` 行の増分を確認。
     - E2E-3(契約): T45 契約に従う AGMSG-TASK を 1 件発行し、RESULT の `[memory:...]`
       マーカーと `memory add` 実行、受入時のオーケストレータ `memory add` 統合記録までの
       一巡を実施(このタスク自体を T48〜T50 のいずれかの受入で兼ねてよい)。
     - E2E は「ライブのデスクトップ挙動を変えるタスクはライブ E2E なしに受け入れない」
       規約(fresh session+persisted restore の両面)に従い、E2E-2 は新規セッションと
       再アタッチの両方で確認する。
  4. **リポジトリ全体オールグリーン**(下記定義)をローカルで満たす。
  5. **crit 審査**: `make require-crit-review` → crit JSON 証跡を `.agents/worklog/` 配下に
     保存し、receipt(`review_surface: crit-data`, `reviewer: claude-code`,
     `review_source`, `review_outcome`)を作成、`AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt>`
     で再実行してグリーン。
  6. **PR**: 英語タイトル/本文で作成(コミットは規約トレーラ付き)。push 後 GitHub Actions
     (test.yaml のユニット+スモーク、macos/ubuntu の bats、agent-assets, docs)を確認し、
     赤があれば修正タスクをワーカーへ発行して再 push、全緑まで反復。
  7. **証跡同期**: ACCEPTANCE 記録を書き切り、`.orchestration` の全ファイルを対象タスク ID
     列挙のメッセージでバッチコミット(untracked の残り = zero-tail を確認)。
- 検証条件・検証内容: 下記「オールグリーン定義」の全項目+E2E-1/2/3 の合格記録。
- 完了条件: PR がレビュー証跡付きで作成され CI 全緑、E2E 記録と ACCEPTANCE が
  `.orchestration` にコミット済み、導入済みプロジェクトの実機更新完了。

### Phase 6 完了条件 = プロジェクト完了条件

T51 の完了条件に同じ。

---

## オールグリーン定義(最終ゲート・全項目必須)

| #   | 区分                            | コマンド/手段                                                                                                                                                      | 合格基準                                               |
| --- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ |
| 1   | フォーマット(shell)             | `make format`(shfmt --indent 4 --space-redirects --diff)                                                                                                           | 差分ゼロ                                               |
| 2   | 構文(shell)                     | `bash -n` 対象全シェル(新規: contextdb-codex-notify)                                                                                                               | エラーゼロ                                             |
| 3   | リント/静的解析(Python, vendor) | `make -C vendor/compactiondb validate` 内 ruff check(E,F,I,UP,B / py310 / line-length 120)                                                                         | 指摘ゼロ                                               |
| 4   | vendor 総合検証                 | `make -C vendor/compactiondb validate`(schema / redaction / marker / hook JSON / install smoke / release tree clean / ruff / MANIFEST.sha256 / permissions / E2E※) | 10 チェック全緑(※E2E は claude 実行体があれば実施)     |
| 5   | ユニット(vendor)                | `make -C vendor/compactiondb test`(unittest, `-W error::ResourceWarning`)                                                                                          | 全緑(T46/T47/T49/T50 の新規テスト含む)                 |
| 6   | ユニット(repo)                  | `make unit-test`                                                                                                                                                   | 全緑                                                   |
| 7   | アセット検証                    | `make validate-agent-assets`                                                                                                                                       | 全緑                                                   |
| 8   | 統合(ローカル可)                | T48 レシーバ 3 ケース(導入済/未導入/壊れ JSON)                                                                                                                     | validation 記録どおり                                  |
| 9   | bats                            | GitHub Actions(macos.yaml / ubuntu.yaml)— ローカル実行禁止                                                                                                         | CI 全緑                                                |
| 10  | CI 全体                         | push 後の全ワークフロー(test / agent-assets / docs / macos / ubuntu)                                                                                               | 全緑(赤 → 修正 → 再 push を全緑まで反復)               |
| 11  | ライブ E2E                      | E2E-1(リカバリ注入)/ E2E-2(notify ingest, fresh+restore)/ E2E-3(AGMSG 契約一巡)                                                                                    | 3 件とも合格記録が `.orchestration/validation/` に存在 |
| 12  | レビュー                        | `make require-crit-review`(crit JSON 証跡+receipt)                                                                                                                 | グリーン                                               |
| 13  | 証跡                            | `.orchestration` zero-tail(untracked なし)+ACCEPTANCE 全件                                                                                                         | `git status --porcelain` で確認                        |

## リスクと対処(実装時の判断固定)

- **Codex notify ペイロードが ingest スキーマに載らない**(T48 手順 3): vendor を勝手に
  広げず AGMSG で差し戻し。必要なら T48b として ingest スキーマ拡張を別タスク化。
- **T47 で既存テストの期待値変更が広範に及ぶ**: 出力形式変更は仕様(P2)であり、期待値
  更新はテストごとに理由コメント必須。理由を書けない変更はスコープ逸脱のシグナルとして
  差し戻し。
- **プロンプトキャッシュへの影響**: 注入はコンパクション毎に一度きりで、破壊は
  コンパクション自体が既に起こしている(Pi の分析)。パケット肥大のみが実コストのため
  予算上限をテストで固定(T47)。
- **導入済みプロジェクトの config 据え置き**: 新キーはデフォルトで効く設計(T46)のため
  再インストールのみで有効。config を書き換える一括マイグレーションは行わない。
