# PLAN: ハーネス合成性知見統合(H1–H6)実装・検証計画

- 作成: 2026-08-16(オーケストレータ: Claude Code / Fable-5 xhigh)
- 根拠分析: `.orchestration/analysis/harness-composability-research.md`
- 体制: Claude Code(Fable-5 xhigh)=オーケストレータ(タスク発行・敵対的受入・crit・
  ライブ E2E 判定)。Codex(deep プロファイル、identity codex-deep-dot)=実装ワーカー
  (AGMSG-TASK 経由、単一 worktree・逐次)。モデル名は identity に含めない。
- 先行実績の踏襲: T45–T53(PLAN-compactiondb-research-integration)の運用をそのまま使う —
  vendor 改修はタスク内で CHANGELOG+MANIFEST まで完結し**タスク完了時点で vendor 単独
  オールグリーン**、5 成果物+ACCEPTANCE、`[memory:...]` マーカー契約、受入時
  `memory add` 統合(本 repo はオプトイン済みのため T45 契約が全面適用)、裁定は本書の
  「実装中の裁定記録」節へ追記。
- スコープ境界(勝手な解釈の禁止): 本計画は分析文書 H1–H6 のみを実装する。不採用と明記
  した項目(dsh 乗り換え/併用、Cordis 直接導入、実行時自己改変ツール)および記載外の
  機能追加は禁止。曖昧点はワーカーが実装で解釈せず AGMSG で質問する。

---

## フェーズ構成と依存関係

| フェーズ | 内容                                 | タスク                                  | 依存                                |
| -------- | ------------------------------------ | --------------------------------------- | ----------------------------------- |
| Phase 0  | 分析・計画のドキュメント化           | T54-0(本書+分析文書)                    | なし(作成済み、PR で完了)           |
| Phase 1  | リカバリ注入の台帳記録(H2)           | T54                                     | Phase 0                             |
| Phase 2  | フック合成の静的検証(H3)             | T55                                     | Phase 0                             |
| Phase 3  | 再起動必要性の検出(H4)               | T56                                     | Phase 0(T55 と独立)                 |
| Phase 4  | 資産マニフェスト+逆写像(H1)          | T57(マニフェスト記録)、T58(撤去+doctor) | Phase 0。T58 は T57 依存            |
| Phase 5  | 最小破壊 reconciliation(H5)          | T59                                     | T57(マニフェスト前提)、T58          |
| Phase 6  | AGMSG effects 契約(H6)               | T60                                     | Phase 4(逆写像確認の前提)。文書のみ |
| Phase 7  | 配布・ライブ E2E・オールグリーン・PR | T61                                     | Phase 1–6 全完了                    |

共通事項(全タスク): ワーカー禁止事項(git commit/push、chezmoi apply、ローカル bats、
依存追加、許可ファイル外編集)、成果物 5 点、敵対的受入、shdoc 英語コメント+shfmt 準拠、
Python は uv 方針。本 repo は CompactionDB オプトイン済みのため、**各ワーカーは完了前に
`python3 .claude/hooks/contextdb_cli.py memory add` で durable fact を記録し、実行コマンドを
RESULT に含める**(T45 契約)。受入時のオーケストレータ decision 統合も毎タスク実施。

---

## Phase 0: ドキュメント化

### T54-0(オーケストレータ直轄)

- 作業内容: 分析文書と本計画書の作成(済)。専用 worktree から PR(docs(orchestration))
  を作成し CI 全緑でマージ。
- 検証条件: H1–H6 の定義・不採用リスト・着手順が分析文書と本書で矛盾しない。
- 検証内容: オーケストレータが両文書を突合。
- 完了条件: 両文書がマージ済み(コミットメッセージに文書名明記)。

---

## Phase 1: リカバリ注入の台帳記録(H2)

### T54: `recovery_injected` イベント(vendor、2.0.0+dotfiles.5)

- 担当: Codex ワーカー。
- 許可ファイル: `vendor/compactiondb/.claude/contextdb/contextdb/recover_hook.py`、
  必要最小限の `hook.py`/`normalize.py` の event_type 許容追加(勝手に広げず、必要なら
  AGMSG で確認)、`vendor/compactiondb/tests/test_recovery.py` または新
  `tests/test_recover_hook.py`、docs(HOOKS.md の該当節)、CHANGELOG(新設
  `2.0.0+dotfiles.5` 節)、MANIFEST、成果物パス。
- 作業順序と内容:
  1. `recover_hook.py` が additionalContext を返す**直前**に、注入内容を
     `recovery_injected` イベントとしてスプールする: summary=先頭 240 字、
     detail=パケット全文(既存の capture 上限に従う)、`detail_sha256` は既存機構で付与、
     session_id は当該セッション。スプール → 非ブロッキング drain は既存経路を使い、
     **リカバリ応答のレイテンシに同期 DB 書込を追加しない**(スプール書込のみ同期)。
  2. 記録失敗はリカバリ注入を阻害しない(record は best-effort、失敗時 health ログ 1 行)。
  3. 再帰防止: `recovery_injected` イベント自体は次回リカバリの Recent activity 集計から
     除外しない(通常イベントとして扱う)が、リカバリ構築が自身の記録を読む競合が
     ないことをテストで固定(記録は構築完了後)。
  4. テスト: (a) 注入時に台帳へ 1 行増え detail がパケット全文と一致、
     (b) sha256 が一致、(c) スプール書込失敗を注入結果に波及させない(モック)、
     (d) 既存リカバリテスト全緑。
  5. CHANGELOG `2.0.0+dotfiles.5` 節新設、MANIFEST 再生成(確立済み手順)。
- 検証条件: リカバリ応答の JSON エンベロープ不変。redaction 経路の迂回なし(パケットは
  既に redacted データのみから構成される — その旨をテストコメントで明記)。
- 検証内容: `make -C vendor/compactiondb clean && make test` / `clean && make validate`
  全緑(pycache 誤検知パターンに注意)。`git diff` 全文審査。
- 完了条件: 検証全通過+受入+5 成果物+memory add 実施記録。

### Phase 1 完了条件

T54 受入、vendor 単独オールグリーン。ライブ確認(実コンパクションで
`recovery_injected` 行が増える)は T61 の E2E-1' に含める。

---

## Phase 2: フック合成の静的検証(H3)

### T55: validate-agent-assets 新カテゴリ「hook composition」

- 担当: Codex ワーカー。
- 許可ファイル: `scripts/validate-agent-assets.py`、`tests/unit/`(該当ユニットテスト)、
  成果物パス。フック定義自体(settings テンプレート等)の変更は禁止 — 検証の追加のみ。
- 作業順序と内容:
  1. 検証対象の列挙: レンダリング済み Claude settings テンプレート
     (`home/.chezmoitemplates/claude-settings-managed.json`)と Codex config テンプレート、
     および CompactionDB の `settings.fragment.json`(vendor 側)を読み、イベント毎の
     フック登録リストを構築する。repo スコープの `.claude/settings.local.json` /
     `.codex/hooks.json` は**対象外**(実行時生成物のため。report に理由を記載)。
  2. 検証規則(各違反は独立の findings として報告):
     (a) 同一イベント内の同一 command 重複登録がない。
     (b) PermissionRequest イベントに permgate 以外の handler が先行しない
     (permgate が権限系の第一評価者)。
     (c) 同期フック(timeout 指定あり)のイベント毎タイムアウト合計を算出し、
     閾値(既定 30s、定数)超過を fail とする。
     (d) SessionStart 系で CompactionDB の recover(compact matcher)が logger より
     後に列挙されていないこと(注入は記録より先に完了している必要はないが、
     現行順序を「意図された順序」として**固定**し、無断変化を検出する)。
  3. 現行構成でグリーンになることを確認した上で、意図的に壊したフィクスチャで各規則の
     fail をユニットテストで固定。
  4. 規則 (b)(d) の「意図された順序」は本計画の裁定として validate 内の定数+コメントで
     文書化(出典: 本書 H3)。
- 検証条件: 既存 19 カテゴリの挙動不変。新カテゴリは現行ソースでグリーン。
- 検証内容: `make validate-agent-assets` 緑、`make unit-test` 全緑(新規テスト含む)、
  `git diff` 審査。
- 完了条件: 検証全通過+受入+5 成果物+memory add。

### Phase 2 完了条件

T55 受入。以後 CI がフック合成の前提条件を恒常的に守る。

---

## Phase 3: 再起動必要性の検出(H4)

### T56: セッション古さ(staleness)検出

- 担当: Codex ワーカー。
- 許可ファイル: 新規 `home/dot_local/bin/common/executable_agent-session-staleness`
  (bash または python — 実装言語は手順 1 の調査結果で選択し report に記載)、
  `scripts/check-agent-runtime.py`(doctor 統合)、`home/dot_agents/agent-config.yaml` の
  SessionStart フック節(追記 1 エントリのみ)、`scripts/generate-agent-configs.py`
  (フック追記が生成経路を通る場合のみ)、tests/unit、成果物パス。
- 作業順序と内容:
  1. 調査: 「セッションが読み込んだ資産のバージョン」を外部から知る手段を確定する。
     方針(この優先順で試し、採用理由を report へ): (a) Claude Code プラグイン
     キャッシュディレクトリ(`~/.claude/plugins/cache/...`)の現行バージョンと
     marketplace の最新インストール済みバージョンの比較、(b) `~/.agents/` 配下の
     rsync 済み資産の mtime とセッション開始時刻の比較。**ハーネス内部状態の推測や
     非公開ファイルのパースはしない**(得られる範囲での近似検出であることを明記)。
  2. 実装: `agent-session-staleness check --since <session-start-epoch>` が、
     セッション開始後に更新された管理資産(プラグイン、~/.agents 配下、rendered
     settings)を列挙し、あれば「restart recommended: <一覧>」を stdout 1〜5 行で返す。
     なければ無出力 exit 0。5 秒上限、失敗時も exit 0(セッション阻害禁止)。
  3. 配線: SessionStart フック(async)として追記。doctor にも同ロジックを
     `--session-staleness` として統合(引数なしなら現在時刻基準の資産更新履歴表示)。
  4. テスト: 資産 mtime を細工したフィクスチャで検出/非検出/失敗時 exit 0 を固定。
  5. shdoc+shfmt(bash の場合)/ uv 方針(python の場合)。
- 検証条件: フック追加が T55 の合成検証(タイムアウト合計等)に適合。既存フックの
  順序を変えない。
- 検証内容: `make validate-agent-assets` / `make unit-test` / `make format` 緑。
  ワーカーはスクラッチで mtime 細工の実挙動 3 ケースを validation に記録。
- 完了条件: 検証全通過+受入+5 成果物+memory add。ライブ確認(実セッションでの警告
  表示)は T61 E2E-2' に含める。

### Phase 3 完了条件

T56 受入。「古いコードで走り続けるセッション」が検出可能になる。

---

## Phase 4: 資産マニフェスト+逆写像(H1)

### T57: 導入マニフェストの記録

- 担当: Codex ワーカー。
- 許可ファイル: `scripts/update-agent-assets.sh`、新規
  `scripts/lib/asset-manifest.sh`(共有関数を置く場合)、tests/unit、成果物パス。
- 作業順序と内容:
  1. マニフェスト仕様(本計画で固定): `~/.agents/.installed-manifest.json` —
     `{ "version": 1, "steps": { "<step-name>": { "installed_at": iso8601,
"kind": "plugin|rsync|brew|installer|integration", "paths": [...],
"commands": [...], "source_version": "<ver|commit|sha>" } } }`。
     書込はアトミック(tmp+mv)。読み手が居なくても常に最新を保つ。
  2. update-agent-assets.sh の**全 11 導入ステップ**それぞれの末尾に、そのステップが
     作成/更新した主要パスと導入コマンド・バージョンを記録する呼び出しを追加。
     既存の導入挙動は一切変えない(記録のみ)。記録失敗は導入を fail させず
     stderr 警告 1 行。
  3. ステップ名は関数名と一致させ、勝手な粒度変更をしない。
  4. テスト: マニフェスト JSON スキーマの検証ユニットテスト(サンプル生成 → パース →
     必須キー)、アトミック書込(部分書込が残らない)の確認。
  5. shfmt/bash -n。`make update` のドライな検証はローカルで安全な範囲
     (該当関数の単体呼び出し+フェイク HOME)で行い、実 HOME への `make update` 実行は
     禁止(T61 でオーケストレータが実施)。
- 検証条件: update-agent-assets.sh の既存挙動がバイト同一の出力列(記録呼び出し以外の
  差分がない)。
- 検証内容: `make format` / `make unit-test` / `make validate-agent-assets` 緑、
  フェイク HOME での関数単体実行ログを validation へ。
- 完了条件: 検証全通過+受入+5 成果物+memory add。

### T58: `remove-agent-asset` と doctor の残留資産検出

- 担当: Codex ワーカー。依存: T57。
- 許可ファイル: 新規 `home/dot_local/bin/common/executable_remove-agent-asset`、
  `scripts/check-agent-runtime.py`(残留資産検出の追加)、`Makefile`
  (`doctor` 出力への組込みが必要な場合のみ最小変更)、tests/unit、成果物パス。
- 作業順序と内容:
  1. `remove-agent-asset <step-name> [--dry-run]`: T57 マニフェストの該当ステップを読み、
     kind 毎の逆操作を実行する — plugin: `claude plugin uninstall` /
     `codex plugin remove`(正確なサブコマンドは `--help` で確認し report へ)、
     rsync: 記録された配布先ディレクトリの削除、brew: `brew uninstall`、
     installer: 記録されたパスの削除、integration: `herdr integration uninstall`
     (存在するかを確認、なければ記録パス削除)。**--dry-run が既定**で、実削除は
     `--yes` 必須。マニフェスト外のパスには決して触れない(パスがマニフェストの
     記録と前方一致することを検証してから削除)。
  2. 逆操作後、マニフェストから該当ステップを除去(アトミック書込)。
  3. doctor(check-agent-runtime.py): `~/.agents` 配下でソース由来でもマニフェスト
     記載でもないディレクトリを「orphaned asset」として WARN 列挙し、
     `remove-agent-asset` の該当コマンドを提案表示(自動削除はしない)。
     既知の許容(understand-anything の symlink 群)は既存の許容リストを維持。
  4. テスト: フェイク HOME+フェイクマニフェストで dry-run/実削除/前方一致ガード/
     マニフェスト更新を固定。orphan 検出の許容リスト挙動。
  5. shdoc+shfmt。破壊的操作なので `--yes` なしでは一切削除しないことをテストで固定。
- 検証条件: いかなる場合もマニフェスト記録外のパスを削除しない(ガードのテスト必須)。
  doctor の既存 WARN/FAIL 挙動不変。
- 検証内容: `make format` / `make unit-test` / `make validate-agent-assets` 緑、
  フェイク HOME での 4 ケース実行ログ。
- 完了条件: 検証全通過+受入+5 成果物+memory add。

### Phase 4 完了条件

T57・T58 受入。「入れたものは列挙でき、巻き戻せる」状態(paper の時間的合成性の運用近似)。

---

## Phase 5: 最小破壊 reconciliation(H5)

### T59: `make doctor REPAIR=1`

- 担当: Codex ワーカー。依存: T57・T58。
- 許可ファイル: `scripts/check-agent-runtime.py`、`Makefile`(doctor 変数追加)、
  tests/unit、成果物パス。update-agent-assets.sh の変更は禁止(呼び出すだけ)。
- 作業順序と内容:
  1. check-agent-runtime.py の検出カテゴリに修復アクションを対応付ける:
     missing file → 該当ソースから chezmoi 単一ターゲット apply
     (`chezmoi apply <target>`)、content differs → 同前、exec-bit → `chmod +x`、
     orphaned asset(T58)→ 提案のみ(自動削除しない)、
     プラグイン欠落 → update-agent-assets.sh の該当ステップ関数のみ実行
     (ステップ単位実行の引数を T57 の関数分割に合わせて追加してよい — その場合
     update-agent-assets.sh への変更が必要になるため、**必要なら AGMSG で許可を
     求める**こと)。
  2. 既定は報告のみ(現行 doctor と同一)。`REPAIR=1` のときのみ修復を実行し、
     実行した修復を 1 行ずつ列挙。修復後に検出を再実行して収束を確認
     (1 回で収束しなければ fail — cordis reconciliation の停止性の運用版)。
  3. テスト: フェイク環境で各カテゴリの修復/収束/非修復(orphan)を固定。
- 検証条件: REPAIR なしの挙動がバイト同一。修復は検出済み項目のみに限定。
- 検証内容: `make unit-test` / `make validate-agent-assets` / `make format` 緑+
  フェイク環境ログ。
- 完了条件: 検証全通過+受入+5 成果物+memory add。

### Phase 5 完了条件

T59 受入。「全部 make update」から「壊れた箇所だけ直す」への移行。

---

## Phase 6: AGMSG effects 契約(H6)

### T60: RESULT 契約への `effects` 欄追加(文書のみ)

- 担当: Codex ワーカー。
- 許可ファイル: `home/dot_agents/skills/agmsg-orchestration/SKILL.md`、
  `home/dot_config/claude/rules/agmsg-orchestration.md`(1 bullet)、成果物パス。
- 作業順序と内容:
  1. SKILL.md の AGMSG-RESULT 契約に追記: リポジトリ外への永続的副作用(グローバル資産の
     導入、$HOME 配下への書込、外部サービスへの登録)を伴ったタスクの RESULT は
     `effects=<semicolon-list>` を記載し、各 effect について「逆写像の所在」
     (T57 マニフェスト掲載/撤去手順/不可逆である旨)を report に明記する。
     リポジトリ内のファイル編集(allowed_files 内)は effects に含めない。
  2. agmsg-orchestration.md に 1 bullet: オーケストレータは effects 付き RESULT の受入時に
     逆写像の存在を確認し、不可逆な effect は受入記録に明記する。
  3. 既存文体に合わせる(英語)。T45 のマーカー契約と矛盾しないこと。
- 検証条件: 差分が許可ファイルのみ。SKILL.md の既存契約(v1 フィールド)と後方互換
  (effects は任意欄)。
- 検証内容: `make validate-agent-assets` 緑+4 文書整合(SKILL/rules/本計画/分析文書)を
  オーケストレータが突合。
- 完了条件: 検証全通過+受入+5 成果物+memory add。

### Phase 6 完了条件

T60 受入。以後のタスク発行文に effects 契約を適用。

---

## Phase 7: 配布・ライブ E2E・オールグリーン・PR(T61、オーケストレータ主導)

- 作業順序と内容:
  1. 専用 worktree(main 起点)に本計画の全変更を集約し、論理コミット分割
     (feat(vendor) / feat(agents) / docs(orchestration))。
  2. 配布: `./scripts/update-agent-assets.sh`(CompactionDB dotfiles.5 の rsync 同期+
     T57 マニフェスト初回生成の確認)。必要な対象指定 `chezmoi apply`
     (新スクリプト 2 本、フック追記)。`.zprofile` 対話問題には対象指定 apply で対処。
  3. ライブ E2E(合否はオーケストレータ):
     - **E2E-1'(H2)**: オプトイン済みプロジェクト(本 repo または スクラッチ)で実
       コンパクション → 再開後、台帳に `recovery_injected` 行が増え detail sha256 が
       注入パケットと一致することを確認。
     - **E2E-2'(H4)**: 実セッション起動 → 資産を意図的に更新(touch)→SessionStart
       再発火相当(新セッション)で staleness 警告が出ることを fresh+restore 両面で確認。
     - **E2E-3'(H1/H5)**: 使い捨て資産(例: スクラッチ用ダミーステップ or 実在の
       小プラグイン)で install→manifest 記録 →`remove-agent-asset --dry-run`→`--yes`
       →doctor がクリーンに戻ることを一巡。`REPAIR=1` の収束確認(意図的に 1 ファイル
       削除 → 修復 → 再検出ゼロ)。
     - **E2E-4'(H6)**: T61 以前の effects 付きタスクが無ければ、T57/T58 の RESULT を
       遡及サンプルとして effects 欄の記載妥当性を受入記録で確認(新規タスク不要)。
  4. リポジトリ全体オールグリーン(下記)。crit 証跡(`make require-crit-review` →
     crit-data フロー、T51 と同一手順)。
  5. PR 作成(英語)→ CI 全緑まで反復 → squash マージ → main 追従 → worktree 撤去。
  6. 証跡同期: ACCEPTANCE 全件+`.orchestration` zero-tail+受入時 memory add 統合の
     漏れ確認(T45 規約)。
- 完了条件: 下記オールグリーン全項目+E2E 4 件の合格記録+PR マージ+zero-tail。

---

## オールグリーン定義(最終ゲート・全項目必須)

| #   | 区分             | コマンド/手段                                           | 合格基準                                                  |
| --- | ---------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| 1   | フォーマット     | `make format`                                           | 差分ゼロ                                                  |
| 2   | 構文             | `bash -n` 対象全シェル(新規 2 本含む)                   | エラーゼロ                                                |
| 3   | vendor 総合      | `make -C vendor/compactiondb clean && make validate`    | 全チェック緑・fail 0                                      |
| 4   | ユニット(vendor) | `make -C vendor/compactiondb clean && make test`        | 全緑(T54 新規含む)                                        |
| 5   | ユニット(repo)   | `make unit-test`                                        | 全緑(T55–T59 新規含む)                                    |
| 6   | アセット検証     | `make validate-agent-assets`                            | 全緑(T55 新カテゴリ含む)                                  |
| 7   | 統合(ローカル可) | T56/T57/T58/T59 のフェイク環境ケース                    | validation 記録どおり                                     |
| 8   | bats             | GitHub Actions(macos/ubuntu)— ローカル実行禁止          | CI 全緑                                                   |
| 9   | CI 全体          | push 後の全ワークフロー                                 | 全緑まで反復                                              |
| 10  | ライブ E2E       | E2E-1'〜4'                                              | 合格記録が `.orchestration/validation/T61-e2e.txt` に存在 |
| 11  | レビュー         | `make require-crit-review`(crit JSON 証跡+receipt)      | グリーン                                                  |
| 12  | 証跡             | zero-tail+ACCEPTANCE 全件+decision 統合(memory add)全件 | `git status --porcelain` 空+台帳確認                      |

## リスクと対処(実装時の判断固定)

- **T56 の資産バージョン検出が近似に留まる**: ハーネス内部状態の推測・非公開ファイルの
  パースは禁止。得られる範囲(mtime/キャッシュディレクトリ)での検出とし、限界を
  スクリプトの shdoc に明記。誤検知(警告過多)が運用で判明したら閾値調整の後続タスク。
- **T58 の削除ガード**: マニフェスト前方一致+`--yes` 必須+dry-run 既定の 3 重ガードを
  テストで固定。ガードを緩める変更は本計画では禁止。
- **T59 のステップ単位実行が update-agent-assets.sh の分割を要求**: 必要になったら
  AGMSG で許可を求める(T57 の記録呼び出しと衝突しない関数境界で)。
- **フック追加(T56)が同期タイムアウト予算を圧迫**: T55 の検証がゲートするため、
  T56 は async 登録とし同期予算を消費しない。
- **`make update` の実 HOME 実行はワーカー禁止**: フェイク HOME での単体検証に限定し、
  実配布は T61 でオーケストレータが行う(.zprofile 対話問題の回避も同時に処理)。

## 実装中の裁定記録(AGMSG-TASK-UPDATE の写し)

- T59: 修復可能なステップ drift は「マニフェストに記載済みかつ記録パスが(部分的にでも)
  欠けているステップ」のみ — 該当ステップの再実行で修復。マニフェスト不在ステップは
  drift ではない(導入は make update のオプトイン領分)。source_version 不一致も drift では
  ない(アップグレードは make update、staleness 報告は T56 の領分)。doctor REPAIR は
  「壊れたものを直す」だけで、導入も更新もしない。3除外をテスト固定。
- T58: doctor の検出は三分類に確定 — ACCOUNTED(ソース由来 or 許容リスト、
  先祖/子孫マッチ含む)は無出力、STALE(マニフェスト記載だがソース非由来 —
  Cognee 型のソース撤去済み資産)は `remove-agent-asset <step>` を提案する WARN、
  ORPHAN(ソース・マニフェスト・許容いずれにも無い)は manual review の WARN。
  当初仕様の2文はこの2クラスを混同していた(ワーカー指摘により裁定)。

(実装開始後に追記)
