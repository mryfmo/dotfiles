# ハーネス合成性研究(cordiverse/paper・cordis・deepseek-harness)× dotfiles 比較分析

- 作成: 2026-08-16(オーケストレータ: Claude Code / Fable-5 xhigh)
- 目的: 下記 3 リポジトリを精読し、dotfiles の現行エージェントハーネス(Claude Code +
  Codex + agmsg + herdr + permgate + CompactionDB + 資産ライフサイクル)と比較、
  統合・改善方針(H1–H6)を確定する。
- 対応する作業計画: `.orchestration/tasks/PLAN-harness-composability-integration.md`
- 先行プロジェクト: `.orchestration/analysis/compactiondb-compaction-research.md`(P1–P7、
  T45–T53 で実装完了)

## 0. 層の整理 — 3 リポジトリは「理論 → カーネル → 製品」の同一スタック

すべて 2026-08-13〜14 に同時公開/更新された一連の成果である。

| コンポーネント                     | 層           | 要点                                                                                                                                                                 |
| ---------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cordiverse/paper                   | 理論         | 88 頁プレプリント「A Programming Paradigm for Spatiotemporal Composability」(Shi/Zhang/Cui, PKU+DeepSeek-AI, 2026-08-13)。コード無し(README+PDF のみ、コミット 2 件) |
| cordiverse/cordis                  | カーネル     | 理論の TS 実装(v4.0.0-rc.8, MIT, ~4.1k stars)。Koishi で 4 年・4000+プラグインの実績。dsh のプラグインカーネル                                                       |
| deepseek-ai/deepseek-harness (dsh) | ハーネス     | Cordis 上の「Everything is a Plugin」エージェントハーネス。v0.1 Developer Preview(2026-08-13/14 公開、~11.7 万 stars、12,293 commits)                                |
| dotfiles ハーネス                  | 外付け運用層 | クローズドな既製ハーネス 2 つ(Claude Code / Codex)を外側から合成するメタハーネス                                                                                     |

## 1. 各コンポーネントの内容(精読要約)

### 1.1 cordiverse/paper — 動的合成の形式理論

- 中心命題(abstract 逐語訳): 「プラグインシステムから自己進化するエージェントハーネスまで、
  現代のソフトウェアは動的合成を要求するが、その形式的基盤は未発達」。
- 2 つの直交次元:
  - **時間的合成性**: 「コンポーネント撤去時にその副作用を完全に巻き戻せる能力」
    = **可逆エフェクト**(全ての文脈変換が明示的な逆写像を伴い、ランタイムが追跡)。
  - **空間的合成性**: 「コンポーネント間依存を宣言しリアクティブに管理する能力」
    = **リアクティブ・コエフェクト**(要求仕様を宣言し、文脈変化を
    activating/deactivating/neutral として通知)。
- 両者を単一の **context 型**に統一(「the context paradigm」)。計算体系(fiber、
  ライフサイクル遷移の操作的意味論)+メタ理論(保存・時間的/空間的合成性・進行・合流。
  reconciliation の健全性=静止状態が最終構成のみの関数で順序非依存・停止・残留状態ゼロ)。
- 動機付け実例: (1) VSCode 拡張(上位 100 中 87 が実行コードを持ち撤去に再起動が必要、
  `extensionDependencies` 宣言は 7 つのみ、exports は型無し)、(2) **自己進化エージェント
  ハーネス**(「不正な自己改変は回復に必要なプロセス自体を無効化しうる」)。
- 明示された限界: 逆写像が本当にエフェクトを回復することは「ランタイムが検証する性質では
  なく実装者の義務」。外部放出(ネットワーク送信・共有パスへの書込)は追跡文脈上は恒等で、
  withholding(出力コミット)か補償が必要(補償にはメタ理論が移らない)。定量評価は未了。
  リンクは名前的(キー)で、インターフェイスドリフトとキー衝突は未解決。
- Koishi は Cordis v3、本 paper は v4 を提示(effect/coeffect 意味論の精緻化+loader 再設計)。

### 1.2 cordis — 可逆プラグインカーネル(v4.0.0-rc.8)

- 自己記述: 「Meta-Framework of Spatiotemporal Composability」。README に「API is not yet
  stable and may change without notice」。core の依存は cosmokit+@standard-schema/spec のみ。
- **Context**: Proxy ベースの単一抽象(サービスコンテナ+イベントバス+スコープ)。
  `extend` / `isolate`(サブツリー毎のサービス分離)/ `intercept`。
- **Fiber**(v3 の scope/fork を置換): プラグインインスタンス毎の状態機械
  (PENDING/LOADING/ACTIVE/FAILED/DISPOSED/UNLOADING)。`ctx.effect(execute)` が唯一の
  変異プリミティブで、disposable を登録し **unload 時に逆順実行**。依存プロバイダ交換時は
  epoch 署名の変化で依存側が自動再起動。
- **DI**: `ctx.provide(name, value)`(現 fiber のエフェクトとして登録、unload で消滅)、
  `inject` 宣言、fiber 越しの変異は禁止。`Service` 基底クラス、callable service、tracker。
- **イベント**: emit / parallel / serial / bail / waterfall の 5 ディスパッチ+context filter。
- **loader**(`@cordisjs/plugin-loader` ほか group/include): エントリツリー
  (id/url/isolate/intercept/config/disabled)の宣言的構成と**最小破壊 reconciliation**
  (フィールド毎に rebuild / realm 再割当 / in-place / component-diff / unload-reload を
  使い分け)。依存未充足はロード順不要で単に待つ。
- **HMR**(`@cordisjs/plugin-hmr`): chokidar 監視 → 受理/拒否のモジュール分類 →
  **トランザクショナル・リロード**(キャッシュバックアップ+ロールバック、
  「半リロード状態には決してならない」)。fiber が全エフェクトを束ねているため
  **開発者による受理境界の注釈が不要**(Webpack/Vite HMR との明示的差別化)。
- 弱点: v4 は RC で API 不安定、v3 時代の文書との乖離、API リファレンス不足、
  Proxy/symbol 魔術の学習曲線、Node 前提。

### 1.3 deepseek-harness (dsh) — Cordis 上のエージェントハーネス

- 自己記述: 「DeepSeek Harness: Everything is a Plugin」「Agent = Model + Harness」。
  MIT、v0.1 Developer Preview(破壊的変更前提と作者が明言)。Node 22.19+/pnpm。
- **特権コアなし**: モデルアダプタ・ツールレジストリ・セッションログ・エージェントループ
  自体が差し替え可能なプラグイン。バンドル → プロファイル → ホーム →CLI の順序付き構成レイヤ。
- **実行モデル**: step(1 リクエスト+ツール実行)/ turn(入力 1 回の消化)。
  `agent/pre-step` waterfall(step の拒否/書換)→ prompt 組立 → ツール分類・実行
  (`tools/pre-execute` waterfall: フック・権限・サンドボックス。**monotonic guard は
  deny か abstain のみ、未応答 approval は fail-closed で拒否**)→ `tools/post-execute`
  → 凍結済み不変結果。
- **核心不変条件「model-visible = logged」**: モデルのリクエストに到達するものは全て追記
  専用セッションログから再構成可能でなければならない。これが **resume / fork / search /
  replay** を(コンテキストキャッシュを壊さず)可能にする。
- **コンテキスト管理**: `dsh-compaction-basic`(閾値デフォルト窓の 80%、直近 16%保持、
  要約モデルの分離指定可、`agent/pre-step` と `agent/request-error` の 2 箇所にフック)+
  `dsh-compaction-tool-result-pruner`(ツール結果の頭 4096/尾 1024 字保持)。
- ツール~50(fs/shell/PTY/lsp/web/planning/セッション検索/ジョブ制御/**実行時自己改変**
  `cordis_define` 等はオプトイン)。マルチエージェント: subagent / ralph(不変目標への
  fresh-agent 反復)/ workflow(JS スクリプト編成)。MCP(stdio+HTTP/SSE)、skills、
  settings ホットリロード。サンドボックス: bubblewrap(Linux)/E2B/worker-thread 予算。
  セッション永続化: JSONL(+zstd)or SQLite(WAL+FTS)。OTLP テレメトリ。
- 留意: DeepSeek モデル最適化(first-party アダプタ、V4 thinking/effort 制御)だが
  プロバイダ非依存設計。公開数日で実績は浅い。リポジトリ自体は他ハーネスとの比較を
  一切書いていない(比較は報道と HN 由来)。

### 1.4 dotfiles ハーネス(現行)の要約

- **宣言 → 生成 → 配布 → 検証 →drift 検出の閉ループ**: `agent-config.yaml`(4 プロファイル:
  express/standard/review/deep)→ `generate-agent-configs.py`(8 種の出力: Claude settings、
  Codex config、per-profile modify スクリプト、model-profiles.env、express-explorer、
  marketplace、plugin manifest、skill symlink)→ chezmoi 配布(ルール 10・スキル 8)→
  `validate-agent-assets.py`(19 カテゴリ)→ `check-agent-runtime.py`(drift 検出)。
- **資産ライフサイクル**: `update-agent-assets.sh`(664 行、11 導入ステップ: プラグイン 4 種
  ×2 ハーネス、CompactionDB rsync、herdr 統合等)。
- **permgate**: PermissionRequest フック(両ハーネス)。deny→allow→LLM 分類(shadow、
  閾値 0.9、7s)→ ask フォールスルー。分類器モデルは別途ピン。fail-closed。
- **agmsg + herdr**: SQLite バス+メッセージ契約(T45 以降 [memory:...] マーカー契約込み)、
  herdr ペーン編成(3 モードランチャー)、repo スコープ配達フック。
- **CompactionDB**(T45–T53 で強化済み): 証拠台帳+固定セクション・リカバリ+probe/recall
  +Codex notify 取り込み+体制起動時オプトイン契機。
- CI: agent-assets / test(unit+bats)/ docs / macos / ubuntu。

## 2. 12 観点比較表

| 観点   | paper                                      | cordis                                 | dsh                                                  | dotfiles ハーネス                                                  |
| ------ | ------------------------------------------ | -------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------ |
| 概要   | 動的合成の形式理論                         | 可逆プラグインカーネル                 | フルスタック・エージェントハーネス                   | 既製ハーネス 2 種の外付け合成層                                    |
| 特徴   | 可逆エフェクト+コエフェクトの統一          | Fiber・effect 追跡・宣言的 DI・HMR     | 特権コアなし・全ログ不変条件・自己改変ツール         | 宣言 → 生成 → 配布 → 検証 →drift の閉ループ                        |
| 機能性 | ◎ 理論的完備(保存/進行/合流)               | ◎ カーネルとして必要十分               | ◎ ツール~50・複数モード・マルチエージェント          | ○ 合成運用には十分、ハーネス内部には介入不能                       |
| 長所   | 自己進化ハーネスの数学的基礎               | 依存極小・4 年実績・部分ホットリロード | 完全追跡可能性・resume/fork/replay・プロバイダ非依存 | モデルの質(Fable-5/gpt-5.6)・permgate 等の独自安全層・完全自己所有 |
| 短所   | 逆写像の正しさは実装者の義務・定量評価なし | v4 RC 不安定・Proxy 魔術・文書不足     | v0.1 preview・DeepSeek 最適化・実績数日              | ハーネス本体ブラックボックス(再起動必要・フック合成契約なし)       |
| 拡張性 | —                                          | ◎ 全て後付け・撤去可能                 | ◎ ループまで差し替え可                               | ○ 資産追加は容易、ハーネス挙動は上流依存                           |
| 保守性 | —                                          | ○ 小さいが RC                          | △ 巨大+preview                                       | ◎ マニフェスト+19 カテゴリ検証+CI(T45–T53 で実証)                  |
| 効率性 | —                                          | ◎ 依存極小                             | ○ Node22+/pnpm/2 プログラム                          | ◎ bash/python/sqlite、生成物は静的                                 |
| 可動性 | —                                          | ○                                      | △ preview 品質                                       | ◎ 各層が独立劣化・fail-closed                                      |
| 移植性 | ◎ 言語非依存                               | △ Node/TS 前提                         | △ Node22+・bwrap は Linux                            | ◎ chezmoi で全マシン再現                                           |
| 高速性 | —                                          | ◎ HMR 数百 ms                          | ○                                                    | △ 資産更新は make update+再起動(分オーダー)— 最大の負け筋          |
| 成熟度 | 改訂中プレプリント                         | RC(v3 系は 4 年)                       | 公開数日                                             | 継続的実証済み                                                     |

## 3. 本質的対比

**dotfiles が既に独立到達している dsh 的設計**: fail-closed 権限パイプライン(permgate ≒
dsh monotonic guards)、セッション証跡と検索(CompactionDB 台帳+recall/probe ≒
session*event*\*)、宣言的構成の閉ループ(≒ cordis loader の外付け版)。

**構造的に欠けているもの(paper の語彙で)**:

1. **時間的合成性の欠如**: update-agent-assets.sh は apply のみで逆写像がない。撤去は
   手作業(Cognee 削除 #115 が実例)。
2. **再起動不要性の欠如**: Claude Code のプラグイン更新は再起動必須。外付けでは HMR は
   原理的に不可能 — できるのは「再起動が必要な状態」の検出と警告まで。
3. **フック合成契約の不在**: 同一イベントに permgate/CompactionDB/herdr/agmsg のフックが
   並ぶが、順序・タイムアウト合計・重複の検証がない。
4. **model-visible=logged の不完全性**: リカバリパケット注入自体が台帳に残らない
   (モデルが見たものの記録が欠ける)。

## 4. 統合・改善提案(H1–H6)

| ID  | 由来                            | 内容                                                                                                                                   | 実装先                                         |
| --- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| H1  | paper(時間的合成性)             | 資産ライフサイクルへの逆写像: 導入マニフェスト記録(`~/.agents/.installed-manifest.json`)+`remove-agent-asset.sh`+doctor の残留資産検出 | update-agent-assets.sh / 新スクリプト / doctor |
| H2  | dsh(model-visible=logged)       | リカバリパケット注入自体を `recovery_injected` イベントとして台帳記録(ハッシュ+全文)                                                   | vendor recover_hook.py(dotfiles.5)             |
| H3  | dsh(waterfall 契約)             | フック合成の静的検証: 同一イベントの登録順・同期タイムアウト合計・重複を validate-agent-assets の新カテゴリで固定                      | validate-agent-assets.py                       |
| H4  | cordis(HMR 不在の次善)          | 再起動必要性の検出: インストール済み資産バージョン vs セッション読込済みキャッシュの drift を SessionStart/doctor で警告               | 新フックまたは doctor                          |
| H5  | cordis(最小破壊 reconciliation) | `make doctor --repair`: missing→ 該当ステップのみ再実行、content→ 該当ファイルのみ再 render、extra→H1 撤去提案                         | check-agent-runtime.py / Makefile              |
| H6  | paper(コエフェクト運用)         | AGMSG RESULT 契約に `effects` 欄(永続副作用の宣言)を追加し、受入時に逆写像存在(H1 マニフェスト掲載)を確認                              | rules / agmsg-orchestration skill              |

**不採用(根拠付き)**: dsh への乗り換え/併用(Fable-5・gpt-5.6 は各公式ハーネス限定供給
であり、モデル品質>ハーネス設計美。dsh は preview+DeepSeek 最適化。将来 DeepSeek 系
第 3 ワーカーを導入する日が来たら agmsg ワーカー化の第一候補として再評価)、Cordis の直接
導入(bash/python 基盤と言語不一致 — 理論のみ移植)、実行時自己改変ツールの導入(paper
自身が警告する領域。permgate と規約で守る現行方針を維持)。

**推奨着手順**: H2 → H3 → H4 → H1 → H5(H1 依存)→ H6 → 配布・E2E・PR。

## 5. 参照

- https://github.com/cordiverse/paper(paper.pdf 全文抽出済み)
- https://github.com/cordiverse/cordis(core/loader/hmr ソース+npm メタデータ)
- https://github.com/deepseek-ai/deepseek-harness(README+docs 7 本+報道)
- dotfiles ハーネス構成マップ(本セッション調査: permgate / herdr / 資産ライフサイクル /
  モデルプロファイルパイプライン / ルール・スキル配布 / CI / フック台帳)
