# PLAN: Pi ワーカー統合(π1–π5)実装・検証計画

- 作成: 2026-08-16(オーケストレータ: Claude Code / Fable-5 xhigh)
- 根拠分析: `.orchestration/analysis/pi-harness-research.md`
- 体制: T45–T64b と同一運用(AGMSG-TASK 逐次委譲、5 成果物+ACCEPTANCE、
  `[memory:...]` マーカー+ワーカー `memory add`、受入時 decision 統合、effects 契約、
  裁定は本書「実装中の裁定記録」へ追記)。
- スコープ境界: 分析文書 π1–π5 のみ。不採用項目(オーケストレータ Pi 置換、π2 なしの
  実運用、MCP 的拡張)と記載外機能は禁止。曖昧点は AGMSG で質問。
- 大原則(本計画の安全不変条件):
  1. **π2(permgate 拡張)受入前に、Pi をスクラッチ以外のリポジトリで動かさない。**
  2. Pi は mise で**バージョンピン**(v0.84.2 起点)。拡張はピン版に対して検証し、
     昇格は staleness/doctor の管理下で行う。
  3. 配布する Pi 拡張(permgate.ts / contextdb.ts)は chezmoi 管理+
     validate-agent-assets の検証対象に加える(無サンドボックス実行のため、
     配布物の完全性が唯一の防御線)。
  4. 購読認証(`/login`)は operator の対話手順。ワーカー/CI はヘッドレス検証を
     API キー系プロバイダまたは faux/replay 系で行い、実モデル確認だけ operator に
     依頼する。

---

## フェーズ構成と依存関係

| フェーズ | 内容                                 | タスク                              | 依存                                    |
| -------- | ------------------------------------ | ----------------------------------- | --------------------------------------- |
| Phase 0  | 分析・計画のドキュメント化           | T65-0(本書+分析文書、PR)            | なし                                    |
| Phase 1  | Pi 導入基盤(ピン+配布骨格)           | T65                                 | Phase 0                                 |
| Phase 2  | permgate × Pi(π2)                    | T66                                 | T65                                     |
| Phase 3  | モデルアクセス実証(π1 前段)          | T67(operator 手順書+ヘッドレス検証) | T65                                     |
| Phase 4  | RPC ブリッジ+agmsg 統合(π1)          | T68                                 | T66・T67                                |
| Phase 5  | CompactionDB 拡張(π3)                | T69                                 | T66(T68 と独立可・逐次)                 |
| Phase 6  | セッション証跡抽出(π5)               | T70                                 | T68                                     |
| Phase 7  | コスト A/B 実験(π4・有界)            | T71(orchestrator 主導)              | T68・T69・T49(probe)                    |
| Phase 8  | 配布・ライブ E2E・オールグリーン・PR | T72                                 | Phase 1–6(Phase 7 は結果同梱・非ゲート) |

---

## Phase 0: ドキュメント化(T65-0、オーケストレータ直轄)

- 内容: 分析文書+本計画書(作成済み)を docs(orchestration) PR で main へ。
- 完了条件: 両文書のマージ(コミットメッセージに文書名)。

## Phase 1: Pi 導入基盤(T65)

- 担当: Codex ワーカー。
- 許可: `home/dot_mise/config.toml`(npm backend で
  `@earendil-works/pi-coding-agent` を **0.84.2 に固定ピン**)、
  `home/dot_pi/agent/`(新規 chezmoi ソースディレクトリ: `settings.json` 雛形 —
  `defaultProjectTrust` を非対話 deny 側に設定 — と `extensions/` 置き場)、
  `scripts/validate-agent-assets.py`(新カテゴリ: pi 拡張ソースの存在+後続タスクで
  内容ハッシュ)、tests/unit、成果物パス。
- 禁止: `make upgrade` 実行、実 HOME への chezmoi apply、既存 mise ピンの変更、
  Pi の実行を伴う検証(構文/レンダのみ。実行は T67 以降)。
- 手順: (1) mise npm backend でのピン記法を既存エントリに倣って追加(lock 更新は
  orchestrator の配布工程)。(2) `home/dot_pi/agent/settings.json`: 最小構成+
  `defaultProjectTrust` を「信頼しない」に。(3) validate 新カテゴリ(拡張ファイルの
  存在検査の骨格。ハッシュ検査は T66/T69 で拡張)。(4) テスト。
- 検証: make format / unit-test / validate-agent-assets 緑。git scope 検査。
- 完了: 5 成果物+memory add+受入。**effects=none**(配布は T72)。

## Phase 2: permgate × Pi(T66、π2 — 安全ゲート)

- 担当: Codex ワーカー。依存: T65。
- 許可: `home/dot_local/bin/common/executable_permgate`(`pi` プロバイダ引数の追加 —
  正規化 action メタデータの写像のみ、分類ポリシーは不変)、
  `home/dot_agents/permgate-policy.yaml`(pi 節: claude/codex と同一の決定論層を参照、
  LLM は shadow のまま)、`home/dot_pi/agent/extensions/permgate.ts`(新規)、
  validate-agent-assets(拡張の内容ハッシュ検査)、tests/unit、成果物パス。
- 拡張仕様(固定): `tool_call` イベントで `bash`/`write`/`edit` を捕捉し、
  ツール名+主要引数を正規化して `permgate pi` を子プロセス実行(タイムアウト 7s)。
  戻り deny → ブロック(モデルへのエラー結果は「blocked by policy」1 行)、
  ask → 対話 UI があれば `ctx.ui.confirm`、**非対話(RPC/print)では fail-closed で
  deny**。permgate 呼出し自体の失敗も deny(fail-closed)。read/grep/find/ls は
  素通し(決定論 allow 相当)。
- テスト: 拡張は vitest 等を持ち込まず、**Pi の jiti ロードを模した Node 単体実行**で
  ハンドラ関数を直接呼ぶユニットテスト(repo の tests/unit から node 実行)。deny /
  ask 対話 / ask 非対話 / permgate 失敗の 4 経路+shellcheck 相当(biome は導入せず、
  tsc --noEmit があれば使用 — なければ node --check、選択を report)。
- ライブ検証は T72(E2E-π2)。完了: 5 成果物+memory add+受入。effects=none。

## Phase 3: モデルアクセス実証(T67、π1 前段)

- 担当: 分担 — ワーカー: ヘッドレス検証スクリプト+operator 手順書の作成。
  operator(ユーザー): 購読認証の実施と結果貼付。
- 許可: `docs/`(または `.orchestration/validation/T67-model-access.md` に手順+
  結果様式)、検証スクリプト(スクラッチで `pi -p`/`--mode json` を API キー系 or
  ローカル系で 1 往復)、成果物パス。
- 検証項目(様式化): (a) Anthropic 購読(`/login`)で Fable 系が列挙されるか、
  (b) thinking level と xhigh 相当の対応、(c) OpenAI 購読で gpt-5.6 系が使えるか、
  (d) 規約上の懸念の有無(operator 判断)、(e) API キー系での RPC 1 往復成功。
- ゲート判定(orchestrator): (e) 成功が T68 の前提。(a)–(d) は π4 の比較条件と
  model_profiles の pi 節の実値を決める(**不成立でも T68 は API キー系モデルで進行可**)。
- 完了: 手順書+検証様式の受入。operator 実施分は T72 までに回収。

## Phase 4: RPC ブリッジ+agmsg 統合(T68、π1 本体)

- 担当: Codex ワーカー。依存: T66(拡張は必ずロード)・T67(e)。
- 許可: `home/dot_local/bin/common/executable_agmsg-pi-worker`(新規ブリッジ)、
  `home/dot_agents/agent-config.yaml`(model_profiles に pi 実験節 —
  既存 claude/codex 節の変更禁止。検証器の profile 期待は「pi 節は任意・存在時は
  スキーマ検査」とする最小変更)、agmsg スキル文書(pi ワーカーの identity 規約
  `pi-<profile>-<project-suffix>` の 1 節)、tests/unit、成果物パス。
- ブリッジ仕様(固定): `pi --mode rpc` を子プロセスに保持し、
  (1) 起動時: agmsg join/identity 確認(既存 scripts 使用)、
  (2) inbox ポーリング(既存 check-inbox 系を再利用、ポーリングは agmsg 既存機構の
  範囲内 — 新規 ad-hoc sleep ループを作らず、Stop フック相当は `agent_end` イベントで
  代替)、AGMSG-TASK 受信 → `prompt` コマンド送出、
  (3) `agent_end` 検出 → `get_last_assistant_text` → ワーカー本文の RESULT 送出は
  **Pi 自身にさせる**(タスク文面の契約どおり send.sh を bash ツールで実行させる。
  ブリッジは配達と完了検出のみ — 判断を持たない)、
  (4) 異常系: 子プロセス死亡で exit 非 0+agmsg に AGMSG-PONG status=blocked 送出。
- スクラッチ限定: ブリッジの作業ディレクトリ検証(π2 受入済みでも、本計画中は
  cwd がスクラッチ/専用 worktree であることをブリッジが enforce — 恒久化の判断は
  T72 受入時の裁定)。
- テスト: フェイク pi(JSONL を喋るスタブスクリプト)で prompt/agent_end/異常系の
  3 経路+shellcheck/shfmt。
- ライブ検証は T72(E2E-π1: fresh+restore)。完了: 5 成果物+memory add+受入。

## Phase 5: CompactionDB 拡張(T69、π3)

- 担当: Codex ワーカー。依存: T66。
- 許可: `home/dot_pi/agent/extensions/contextdb.ts`(新規)、validate の内容ハッシュ
  対象追加、tests/unit、成果物パス。vendor 変更禁止(`--ingested-from pi` は既存
  検証 `^[a-z0-9][a-z0-9_-]{0,31}$` が受理)。
- 拡張仕様(固定): `tool_execution_end`(ツール名・成否・主要引数を正規化)、
  `turn_end`(last assistant text の要約 240 字)、`session_compact`(summary)を、
  cwd に `.claude/hooks/contextdb_cli.py` が存在する場合のみ
  `ingest --ingested-from pi` へ(stdin、5s、失敗 silent — T48 レシーバと同じ契約)。
  未導入 cwd では完全無音。`session_before_compact` への台帳注入は本計画スコープ外
  (将来拡張として report に記載のみ)。
- テスト: ハンドラ直接呼びで導入済み/未導入/失敗の 3 経路。
- 完了: 5 成果物+memory add+受入。ライブは T72(E2E-π3)。

## Phase 6: セッション証跡抽出(T70、π5)

- 担当: Codex ワーカー。依存: T68。
- 許可: `home/dot_local/bin/common/executable_pi-session-evidence`(新規小スクリプト:
  セッション JSONL パスを引数に、CompactionEntry.details(readFiles/modifiedFiles)、
  ModelChange、コスト統計を抽出して受入記録用の要約を stdout へ)、tests/unit
  (フィクスチャ JSONL)、成果物パス。
- 完了: 5 成果物+memory add+受入。

## Phase 7: コスト A/B 実験(T71、π4 — orchestrator 主導・有界・非ゲート)

- 手順: T49 probe を評価器に、express/standard 級の同一タスク 3 件を
  (a) Codex 現行 (b) Pi+同等モデル で実行し、コスト(Pi は `/session` 統計、Codex は
  概算)と probe 採点(review プロファイル低 effort)を比較表に。
- 有界性: タスク 3 件・各 1 回・追試なし。結果は配置変更の提案材料であり、本計画では
  プロファイル変更を行わない(変更は別途 operator 裁定)。
- 完了: 比較表が `.orchestration/validation/T71-ab.md` に存在。

## Phase 8: 配布・ライブ E2E・オールグリーン・PR(T72、オーケストレータ主導)

- 配布: mise ピンの install(lock 更新は独立 chore コミット規約に従う)、chezmoi
  対象指定 apply(dot_pi 一式・ブリッジ・evidence スクリプト)、manifest への記録
  (mise 管理分は mise.lock が逆写像、chezmoi 分は chezmoi が逆写像 — その旨を
  effects 記録に明記)。
- ライブ E2E(合否はオーケストレータ):
  - **E2E-π2**: スクラッチで `rm -rf` 相当を Pi に指示 → permgate 拡張が deny、
    RPC(非対話)でも fail-closed deny をログで確認。
  - **E2E-π1**: ブリッジ経由で AGMSG-TASK→Pi 実行 →RESULT 一巡を fresh+
    restore(`/resume` 経由)の両面。
  - **E2E-π3**: 導入済みスクラッチで `ingested_from='pi'` 行(ツール粒度)を確認。
  - **E2E-π5**: 実セッション JSONL から evidence スクリプトの抽出結果を受入記録へ。
- オールグリーン定義: T61 と同一の 12 項目(format / bash -n+tsc・node --check /
  vendor 総合+テスト / repo テスト / アセット検証(pi 新カテゴリ込み)/
  フェイク pi 統合 / CI(bats 含む)全緑 / ライブ E2E 4 件 / crit 証跡 /
  zero-tail+ACCEPTANCE+decision 統合)。
- PR(英語)→ CI 全緑 → squash マージ → main 追従 → 後片付け。

## リスクと対処(判断固定)

- **Pi の API 変動**(v0.8x 週次): mise ピン+拡張はピン版に対する回帰テスト。
  昇格時は T56 系 staleness が検知し、拡張テスト再実行を昇格手順に含める。
- **拡張の無サンドボックス**: 配布拡張 2 本は chezmoi 管理+内容ハッシュ検査を
  validate に追加。手元改変は drift として検出。
- **購読認証の対話性**: operator 手順として分離(T67)。ヘッドレスは API キー系。
- **RPC イベント形の不確定部**(print/JSON との封筒一致は未検証): T68 の最初の
  実装ステップで実プロセスに対し封筒を確認し、report に記録してから本実装。
- **ブリッジの越権禁止**: ブリッジは配達と完了検出のみ。本文生成・判断・RESULT 組立を
  ブリッジに置かない(Pi 自身が契約に従う)。

## 実装中の裁定記録(AGMSG-TASK-UPDATE の写し)

- 運用条件(operator 指示 2026-08-16、全 PR に適用): PR 作成後は CI 結果と bot
  コメントを**全文取得**し、その場しのぎの手段(抑止ディレクティブの濫用、テスト緩和、
  症状パッチ)ではなく**本質対処**ですべて是正してからマージする。bot 指摘は根本原因
  まで広げて監査し、対処内容をコメントへ返信する。

(実装開始後に追記)
