# Plan 024（最初に読むもの）: 方向性、2 段階構成、決定、分類、作業順序、STOP、状態

> 読み方: この文書は orchestrator とユーザーが最初に読む。詳細設計は `024-design.md`（目次）、実行中の手引き（順序、`make update`、重ね方、本日の時刻表とトリップワイヤ）は `024-execution.md`、作業項目は `024-todo.md`、完了・退出の確認は `024-checklists.md`、進捗は `024-progress.tsv`。作業役はこの plan を読まず、自分のタスク文（`.orchestration/tasks/<task>.md`）と AGENTS.md だけを読む。

> オーケストレーター席（claude-deep-dot、Claude Fable 5.1 xhigh）が 2026-10-18 09:5x JST（00:5xZ）に起票。ユーザー指示 08:51 / 08:58 / 09:4x JST「dotfiles 改善計画を策定し、現在の問題箇所を整理して是正計画を策定すること。極限まで効率化するとともに品質を保つこと」に応える。**何も実行していない。** 決定パネルの既定値は、返答が無いときに適用する。本文は Plan 023 の方向性と PR A〜H、是正は `024-design-mechanism.md` 第 5 節に従属させた。材料は Grok Bot の全やり取り（`~/.local/state/grokbot/handoff/transcript-2026-10-18/`、精査ノートは席の scratchpad）、Plan 023、gh と agmsg の 09:3x JST 実測。

## 0. 方向性（ユーザー決定 2026-10-17 17:22〜17:38 JST、Plan 023 Decision 節。変更なし）

1. ハーネスは omp（oh-my-pi）一つ。Claude Code と Codex はやめる。
2. OpenAI は ChatGPT OAuth（`/login openai-codex`）、Anthropic は API キーのみ。omp での Anthropic OAuth は規約違反なので、その不在を機械的に検査する。
3. エージェント間通信は hcom 一本。agmsg は撤去。herdr は画面とペインの管理に残す。
4. 外部物（omp、hcom、herdr、pstack）は固定バージョンの取得物。コピーは置かない。
5. ルールは文章でなくコード・lint・テストで強制する。
6. spark-9e8d は hcom relay（SSH ポート転送の私設ブローカー）+ `herdr machine add`。
7. Cursor 専用スキル 9 系統を omp/hcom 向けに書き直す（H1〜H9）。

これに 10/17 夜〜10/18 朝のユーザー指示を加える: 人が介入しないと進まない作り方は欠陥（07:42）、人のレビューは不要だが問題のあるコードは通さない（07:17）、効率と確実さを最優先（19:24）、同種の問題はまとめて直す（20:52）、選択肢の羅列でなく意図に合う一案（21:21）、その場しのぎの例外を足さない（08:35）。10/18 10:5x 以降の指示（2 段階化、並列と直列の区分、AI 基準の見積もり、人の判断の細分化、仕組みの品質保証とプログラム化、文書の分割、精査）は Status log に時刻付きで記録する。

## 0b. 実行構成: 2 段階（ユーザー指示 2026-10-18 10:5x JST「2 つに分けるべき」）

**第 1 段階 = 現環境（Claude Code 3 席 + Codex 1 席 + agmsg）のボトルネック解消。** 方向転換の開発を高速・並列・品質維持で回せる状態を先に作る。live の運用を変える PR（C-1b の dispatch 経路切替、C-2 の hcom 着席、切替 X、撤去 E）はこの段階では merge しない。運用を変えない第 2 段階の PR（B-1、#404、G-a、H6）は `024-execution.md` 0e の 4 条件の下でだけ merge してよい。実装済みの B stage 1（a009 ローカル 41da91ce）と C stage 1 の item 0（a008 dfa9001b）は draft PR として push だけして退避し、席は第 1 段階のタスクに回る。是正はハーネス非依存の形（`scripts/orchestrator/*`、gh/git、CI、manifest）で作り、切替後もそのまま使う。Claude 専用の層（hook、settings）には #400 の暫定マージ以外に手を入れない。

**第 2 段階 = 方向転換（`024-design-prs.md` 第 4 節 PR A〜H と切替 X）。** 第 1 段階の退出条件（DoD-P1）を満たしてから始める。C stage 2 は第 1 段階で作った仕組みを hcom/omp へ移植するだけになる。

## 0c〜0e. 実行手引き

並列と直列の区分、第 1 段階の順序の根拠、`make update` の時機（0d）、第 1 段階と第 2 段階の重ね方（0e）、本日の時刻表とトリップワイヤ（0c）、ユーザーの操作一覧は `024-execution.md` に分離。

## 1・4・5・9・付録 A の所在

第 1 節（完了の定義 DoD1〜12）は `024-checklists.md`。第 4 節（PR A〜H と切替 X）は `024-design-prs.md`。第 5 節（仕組みの設計と是正 5.0〜5.7）は `024-design-mechanism.md`、5.8〜5.13（天井、CI/Bot、追加の仕組み、品質保証、人の判断の細分化）は `024-design-quality.md`、5.12（プログラム仕様）は `024-design-programs.md`。第 9 節（実行可能性の検証 V1〜V15）と付録 A（役割別ボトルネック台帳）は `024-design-evidence.md`。この文書に残る節は 0、0b、2、3、6、7、8 と Status log。

## 2. 決定パネル（既定値はこの plan が合意された時点で適用。D-024-01〜D-024-12 = D1〜D12。合意の返答を受けた boundary 23 で orchestrator が decisions.tsv に 12 行を追記し（既定値採用の行は result=default）、消費するタスクの受け入れ記録が参照する）

| 決定 | 選択肢 | 既定値と理由 |
| --- | --- | --- |
| D1 strict up-to-date | (a) 今すぐ OFF（管理者操作、トグル 1 つ）。(b) train を作ってから OFF（08:12 の決定）。(c) ON のまま | **(a)**。train は新規コードで YAGNI。同等の安全は「必須チェックが各 head で緑 + 依存順に 1 本ずつマージし、main の push CI が緑になるまで次を入れない + allowed_files が互いに素」で得られる。バックログ 11 本（うち受理済み 9 本）が 9〜10 時間から 2〜3 時間になる（Bot 実測: CI 中央値 10 分、macOS runner 待ち最大 26 分、strict だと約 36 回の全再実行） |
| D2 レビュースレッド解決必須 | (a) OFF。(b) ON のまま、`resolve-threads.sh` の graphql 書込を hook で通す | **(a)**。全スレッドの disposition は `scripts/pr-feedback.py` の sweep と `PR_FEEDBACK_EVIDENCE` のゲートが最終 head で既に強制している。GitHub 上の「解決」は同じ情報の二重記録で、人の承認を要する唯一の書込だった。(b) は Claude 専用コードを増やす |
| D3 #400（gh-merge-gate hook、push の HTTPS 化を含む） | (a) a010 の T131 所見（8 P1 / 8 P2）のうち P1 を 1 ラウンドで直してマージし、E で削除する暫定物と明記（タスク `dotfiles-T131-claude-pinned-merge-gate-fix-a01`、Codex、security: true）。(b) 手作業適用のまま。(c) 閉じる。(d) 8 P1 に同一クラス 3 件があって S1 が発動するか、1 ラウンドで収まらないときは #400 を閉じ、live hook は手作業適用のまま維持し（`make update` は走らせない）、HTTPS push 設定と最小 gate を P1-14 と同じ Codex タスクで作り直す（期限 10/19 12:00） | **(a)**、収まらなければ **(d)**。(b) 単独は `make update` で ask ルールに戻る（DoD2 違反）。切替まで Claude 席でマージを回すのに必要 |
| D4 #393（F4: 統合専任席、pre-RESULT ゲート、席上限） | (a) stop。PR を閉じ、ブランチと記録を残し、要件を第 1 段階の P1-4 / P1-5 / P1-7 としてハーネス非依存に作り直す（S1 の再計画）。(b) 4 回目のラウンド | **(a)**。監査 incorrect 8 P1（同一クラス 5）、3 回目ラウンドが INV-6 超過（D-F4-round3 は誤り、M-20261018-02）。作り直しは #393 のブランチを材料に、8 P1 を設計段階で disposition してから |
| D5 #399（Codex local-review の sandbox 除外） | (a) 閉じる（ブランチ保持）。(b) 再設計 | **(a)**。Codex 専用、セキュリティ監査で同一クラス 6 件。omp では監査役・レビュー役が omp 実行になり要件が消える |
| D6 #383 と古い draft #315 #317 #323 | (a) 閉じる（ブランチ保持）。(b) 開いたまま | **(a)**。Plan 023 で #383 は保留済み、3 本は DIRTY で 1 週間以上更新なし |
| D7 #395（process substitution 禁止の portability guard）と #403（Claude sandbox README） | (a) #403 は閉じる。#395 は保留し E で閉じる。(b) 両方マージ | **(a)**。どちらも Claude sandbox の制約に対する対処で、方向性 1 で消える文脈 |
| D8 F3（orchestrator 負荷の仕組み化） | (a) ハーネス非依存の 2 点（RESULT からの記録自動生成、統合チェーンの席側実行）を第 1 段階の P1-6 / P1-4 として作り、Claude のターン上限フックは作らない。(b) Claude hook も作る | **(a)**。上限フックは第 2 段階の B stage 2 で omp の hook（`session_before_compact`）が担う。切替まで 5.5 の自己基準 |
| D9 切替後のオーケストレーターのモデル | (a) D-omp-model-mapping どおり Anthropic API キーで fable 5.1 xhigh。(b) OpenAI OAuth で gpt-6.1-sol xhigh | **(a)**（08:4x の記録済み決定）。ただし API 従量のため、1M トークン級の文脈は 1 ターン数十ドルになる。B で「文脈 600k 超で handoff を強制する omp hook」と「boundary ごとに omp の history.db から当日の使用量を記録」を必須にする。1 日の上限額はユーザーが決める（未設定なら記録のみ） |
| D10 席数上限 | (a) 4（現状）、spark の 2 席目が動いたら 6。(b) 今すぐ 6 | **(a)**。オーケストレーター待ちが解消するまで席を増やしても列が伸びるだけ（Bot 21:19 分析） |
| D11 spark のバス | (a) Plan 023 推奨: Mac の localhost に私設ブローカー、SSH 転送、`hcom relay`、`herdr machine add`。(b) 公開ブローカー | **(a)**。C stage 2 の後 |
| D12 Grok Bot の役割 | (a) 報告・伝達のみ。herdr への指示は送らない。ルーティンは報告の仕組み（H6/H7 と project-map）が入るまで pause のまま。(b) 元に戻す | **(a)**（ユーザー 08:51 の指示） |

## 3. 進行中の作業の分類（09:3x JST 実測。continue = 続ける、merge = そのまま統合、stop = 止めてブランチ保持、close = PR を閉じる）

| 対象 | 状態（実測） | 方向性との関係 | 判定 | 理由 |
| --- | --- | --- | --- | --- |
| #401 記録 boundary 21+22 | CLEAN、CI 緑、スレッド 0 | 記録 | **merge 最初** | 記録が散らばったまま次に進まない |
| #390 F1 監査の patch-id 継承 | BLOCKED、CI 緑、スレッド 2、受け入れ済 | 5（F） | **merge**（D1/D2 の後） | 以後の全 PR の再監査を減らす。ハーネス非依存 |
| #389 D リポ側 Anthropic 認証チェック | BLOCKED、CI 緑、スレッド 8、既知の制限付きで受理済 | 2（D） | **merge**、直後に #396 | 平文の漏れを今日から止める。パーサー版 #396 が制限を埋める |
| #396 D パーサー版（base #389） | draft CLEAN | 2（D） | **continue → ready → merge**（#389 直後、担当 a010） | 正規表現の抜け道を構造解析で閉じる |
| #404 D 実行時 probe | draft BEHIND、head 1aa08902 | 2（D） | **continue**（a009。0e で ready まで前倒し可、マージは B-1 の後） | DoD4 の実体 |
| #378 chain-finish.sh、#375 lossless dispositions | BEHIND、CI 緑、スレッド 5 / 1、受け入れ済 | 統合チェーン（gh/git のみ） | **merge** | Plan 023 の分類どおり高価値、omp 後も残る |
| #398 A follow-up（hcom wheel receipt）、#405 T132（dangling omp link、uv upgrade skip） | BEHIND スレッド 3 / draft CLEAN | 1・4（A） | **merge** / **continue → merge**（a011） | A の仕上げ。make update の再現性 |
| #402 local-advisory.sh 修正 | draft BEHIND | 統合チェーン | **continue → merge**（a011） | gh/git のみ、小さい |
| #387 F2 正規化 lint + follow-up 445c32dd（PR 無し） | BEHIND、CI 失敗、スレッド 6 | 5（F） | **continue、後順**（a011、Wave 2） | lint はハーネス非依存。CI 赤を先に直す |
| #400 gate hook（+ push HTTPS 化） | BEHIND、スレッド 3、T131 レビュー 11 件、live に手作業適用 | 切替までの暫定 | **merge（D3）**、E で削除 | 上記 |
| #393 F4 | BLOCKED、監査 incorrect、D-393-hold | 5（F）→ 要件は P1-4/P1-5/P1-7（D4） | **stop + close（D4）** | 上記 |
| #399 Codex 除外 | BEHIND、D-399-A | Codex 専用 | **close（D5）** | 上記 |
| #383、#315、#317、#323 | BEHIND / DIRTY | 旧 | **close（D6）** | 上記 |
| #395、#403 | BEHIND / draft | Claude sandbox | **hold → E で close / close（D7）** | 上記 |
| B: worker-c `tools/omp-config-render` 41da91ce（未 push、item 0b と 1〜5 実装済、unit test 96 ok、report/validation 未作成） | a009 停止中 | 1・2（B） | **退避（draft push のみ）→ 第 2 段階で continue** | 第 2 段階の前提。実装はほぼ済みなので draft として push し、席は第 1 段階の P1-5 へ（0b） |
| C stage 1: worker-f `tools/hcom-dispatch-bus-a01` dfa9001b（item 0 の実測のみ、コード 0、タスク文に指摘 3〜7） | a008 停止中 | 3（C） | **退避（draft push のみ）→ 第 2 段階で continue**（amendment 1 を先に） | 切替の前提 |
| T131 #400 レビュー RESULT（status=hold 送信済） | a010 停止中 | 暫定 | **D3 のタスク `dotfiles-T131-claude-pinned-merge-gate-fix-a01` の ACCEPTANCE で閉じる**（P-W0 で orchestrator が書く 4 本のタスク文の 1 つ） | hold は契約外の暫定 status。閉じ方を記録に残す |
| T130 followup（#403）、`dotfiles-T129-audit-inherit-replan-json-followup-a01` など Claude 系 owner task | 未着手 | Claude 専用 | **stop** | E で消える |
| G pstack タスク文 `dotfiles-T129-pstack-asset-a01` | 未 dispatch | 4（G） | **continue、第 2 段階 D-W0**（a010。G-a の vendor 準備は 0e で前倒し可） | A は済み。manifest と updater（G-b）は validator 系列の後 |
| F3 タスク文 `dotfiles-T129-orchestrator-load-mechanisms-a01` | 未 dispatch | 5 | **stop、要件を第 1 段階の P1-4/P1-6 へ（D8）** | 上記 |
| Grok 残置物: 手編集 `~/.claude/settings.json`（バックアップ 4 本）、`~/.config/git/config` の pushInsteadOf 撤去、`~/.local/state/grokbot/*`、`dotfiles-operator`（削除済） | — | 環境の不整合 | **是正 5.3 で吸収** | DoD2 |

## 6. 波（並列。席: a008 Claude worker-f、a009 Claude worker-c、a010 Codex worker-e、a011 Claude worker-d。allowed_files は波の中で互いに素）

### 第 1 段階（現環境のボトルネック解消。見込み 10〜12 時間 = 5 波 P-W0〜P-W4、AI 基準、人の待ちは 2 トグルと #401 の承認のみ。第 8 節と design-quality 5.10）

| 波 | a009 | a008 | a010（Codex） | a011 | orchestrator / ユーザー |
| --- | --- | --- | --- | --- | --- |
| P-W0（合意直後、〜2 h） | B stage 1 を draft PR として push だけして退避。続けて P1-5 result-precheck（`scripts/orchestrator/result-precheck.sh`、受け入れ側の拒否、fixtures） | C stage 1 の item 0 を draft PR として push して退避。続けて P1-4a verdict.sh + audit-pool.sh + `.schemas/audit.json`（監査 JSON と機械判定。P1-4 の integrate-seat が依頼先として使う） | #400 の P1 のみ 1 ラウンド → V2 の 1 行（`hcom-dispatch` の excludedCommands/allow は第 2 段階で使うので今は不要。代わりに #396 ready） | #405 と #402 を ready → F5 CI 着手（F2 より先、0d の順序 3） | ユーザー: D1/D2 の 2 トグル、#401 の承認 1 回。orchestrator: タスク文 4 本（P1-5、P1-4a、F5、T131-fix）を書いて dispatch、#401 を承認後に merge、5.1 の順で直列マージ開始、glue `SKIP_RESOLVE=1`、5.2 の close |
| P-W1（〜1 日） | P1-6 記録自動生成と `dispatch.sh --next`（`acceptance-front-matter.py`、`dispatch.sh`。P1-5 と同じ席なので dispatch.sh の衝突なし） | P1-4a RESULT → P1-4 integrate-seat-a02（#393 の 8 P1 の disposition を設計メモに → 実装 → 自分の PR で統合を完走する初例） | #400 マージ後に P1-7 席上限（manifest、`herdr-agents`、validator）→ P1-8 ルール文の縮小 | F5 の RESULT → F2 #387 の CI 赤と 6 スレッド（1 ラウンド） | 受け入れ・監査・マージを 1 本ずつ。boundary 23 → handoff → 再起動（P1-9、14:30）。#400 マージ後、波の境目で `make update` → `chezmoi verify` → 席を 1 つずつ再着席（0d の手順、約 16:00） |
| P-W2（〜2 時間） | P1-5/P1-6 の revise 対応、DoD-P1 の計測スクリプト（idle 間隔、revise 率、CI 中央値を bus 履歴と `gh run list` から出す） | P1-4 の 2 本目の統合を実演（#387 か F5 を席側で完走） | P1-7/P1-8 の revise 対応、#396 マージ後の #389 follow-up 片付け | F5 の revise 対応、テスト並列化（item 0 で可なら） | 受け入れ・マージ |
| P-W3（〜2 時間、design 5.10 の追加分） | P1-12 タスク文生成とチェッカー拡張（plan-check を含む） | P1-10 所見 disposition の自動化（second-opinion を含む） | P1-11 CI regime ジョブ（workflows、threat_table） | P1-13 hold playbook（`.orchestration/learning/classes.yaml` の remedy、hold-playbook.sh。`dispatch.sh` の変更は P1-6 マージ後） | 受け入れ・マージ |
| P-W4（〜2 時間、design 5.13 の追加分） | P1-4 の revise 対応、計測。空きで B-2 item 0（omp hook の実測、0e） | P1-12/P1-10 の revise 対応。空きで C-1a（新規スクリプトのみ、0e） | P1-14 permission guard と ruleset 補助（validator、Claude 境界の権限面を扱うので Codex 席）。終わり次第 G-a | P1-13 の revise 対応。空きで H6 watch-pr（0e） | DoD-P1 の全項目（a〜l）を確認して記録。満たしたら第 2 段階へ。B-1 のマージは P1-14 の後（0e 条件 3） |

### 第 2 段階（方向転換。DoD-P1 の後）

| 波 | a009 | a008 | a010（Codex） | a011 | orchestrator / ユーザー |
| --- | --- | --- | --- | --- | --- |
| D-W0 | B stage 1 の draft を ready（rebase、report/validation）→ マージ。次に #404 | C stage 1 を ready（追加型、`bus: agmsg` 既定）→ マージ | V2 の 1 行（`hcom-dispatch` の excludedCommands/allow）→ G pstack | H6 watch-pr（gh のみ） | ユーザー: `make update` 後に `/login openai-codex` と `ANTHROPIC_API_KEY` |
| D-W1 | B stage 2（omp hooks: gh 書込拒否、600k handoff、Stop 相当） | C stage 2（hcom omp 着席、launch.json、第 1 段階の仕組みの hcom 移植、最小 SKILL、member list） | G 仕上げ → E1 の棚卸し | H7 session-report | 受け入れ・マージ。omp の実測を plan に追記 |
| D-W2 切替 | — | — | — | — | X の (1)〜(5)。パイロット 1 席 → 全席 → orchestrator |
| D-W3 | H3 | H1、H5 | E1 → E2 → E3 | H2、H4、H8、H9 | spark relay + machine add + 2 席目（D10 で 6） |

## 7. STOP 条件（plan 020 S1、INV-6、plan 022 の規律をそのまま）

- 同一クラスの所見が 1 artifact に 3 回 → その artifact を止め、`re-plan:` を書く（4 回目は走らせない）。
- revise 2 回で上限。決定行による上限超過は禁止（C-66）。
- マージ後に main の push CI が赤 → マージ凍結、fix-forward 1 本。
- B / C の item 0 で omp か hcom の前提が崩れる（hook API 無し、store 形式違い）→ パッチでなく plan 024 の該当 PR を再計画。
- Anthropic API の当日使用額が D9 の上限を超える → orchestrator の provider を (b) に切替。
- 切替パイロットが DoD11 を 2 回続けて満たさない → `bus: agmsg` に戻し、原因を記録してから再試行。
- 品質指標（design-quality 5.11 Q-D）: 連続 2 波で main の push CI 赤 > 1、escaped defect > 0、監査 P0/P1 のマージ後検出 > 0、not-applicable 比率 > 30% のいずれか → マージ凍結、根本原因を記録してから再開。
- 仕組み PR（P1-3〜P1-14）が 2 回目の revise に入ったら hold。追加ラウンドは禁止（決定行による延長も不可、C-66）。

## 8. 見込みとリスクの総括

**見積もりモデル（AI エージェント基準。人日では見積もらない）。** 時間を決めるのは席の作業時間ではなく、臨界路の待ちと並列の天井。入力はこの repo の実測: CI 1 run 中央値 10 分（07:46）、監査 1 本 10〜15 分、a009 は 6 項目のタスク（B stage 1、96 テスト）を dispatch から約 25 分で実装（08:4x → 09:09 PONG）、#392 は実装 20 分に対し修正 6 ラウンドで 3.5 時間、revise 率 34/98、6 時間の人待ち（01:05〜07:54）。

| 要素 | 1 PR あたり | 根拠 |
| --- | --- | --- |
| タスク文（orchestrator、並列可） | 10〜20 分 | 既存のテンプレートとチェッカー |
| 実装（席） | 15〜60 分 | a009 25 分、T130 20 分（12 原因） |
| precheck（席、P1-5 後） | 10 分 | unit + render-check + local review |
| CI | 10 分（F5 後 5〜7 分） | 実測中央値 |
| 監査 | 15 分（P1-4a 後は 2 本並列、差分監査 3〜5 分） | 実測 |
| 判定とマージ | 2〜5 分（verdict.sh）／今は 20〜60 分 | design-mechanism の設計 |
| **臨界路（revise 0 回）** | **1〜1.5 時間** | 合計 |
| revise 1 回の追加 | +1 時間（修正 20 分 + CI + 差分監査 + 判定） | — |
| 人の待ち | 0（ruleset の 2 トグルのみ） | D1/D2 |

並列の天井: 席 4（→ 6）、CI は同時 3〜5 PR（S3）、監査は同時 2 本（S4）。したがって 1 波（4 PR）は 1.5〜2.5 時間、1 時間あたりのマージは 6〜10 本が上限。

| 段階 | 作業の束 | 壁時計 | 前提 |
| --- | --- | --- | --- |
| 第 1 段階 | バックログ 11 本の消化（実装なし、gate とマージのみ: 1.5 時間）+ 新規 13 PR（P1-2〜P1-8、#400 ラウンド、P1-10〜P1-14。5 波 P-W0〜P-W4） | **10〜12 時間** | revise ≤ 1 回、人待ちは 2 トグルと #401 承認のみ、監査は今日前半は手動直列 |
| 第 2 段階 B + C | B-1 ready とマージ 1〜2 時間、B-2 3 時間、C-1 3 時間、C-2 3〜4 時間（B と C は並列） | 4〜6 時間 | omp hook の実測が docs どおり |
| 切替 X | make update 15 分、ログイン 5 分、パイロット 1 席 1 時間、全席 1 時間、orchestrator 再起動 30 分 | 3 時間 | B-2 と C-2 のマージ後 |
| E1〜E3 | 削除 3 PR（各 1 時間 + CI） | 4 時間 | X の後、直列 |
| G、H1〜H9 | 10 PR、4 席並列で 3 波 | 5〜6 時間 | B の後（E と並行可） |
| spark | relay、machine add、2 席目 | 1〜2 時間 | C-2、ユーザーの接続操作 |
| **第 2 段階 合計** | — | **18〜24 時間（連続稼働なら 1 日、日中のみなら 2〜3 日）。0e の重ね方で B-1・B-2・C-1a・#404・G-a・H6 が DoD-P1 時点で ready なら 12〜18 時間** | — |

前版の「第 1 段階 2〜3 日、第 2 段階 4〜6 日」は、今の regime（revise 34%、監査直列、orchestrator の 40〜70 分ターン、人待ち）を前提にした数字で、第 1 段階の仕組みが入った後の AI のペースではない。訂正する。見積もりの検証: 各 PR の RESULT 時刻・マージ時刻・ラウンド数を `024-progress.tsv` に記録し、1 波ごとに上の表の数字と比べて plan を直す。
- 品質: 必須チェック・監査・S1・disposition は全部残る。外すのは二重記録（GitHub スレッド解決）と N² の再 CI だけ。
- 最大リスク: omp の権限・hook 層の未知（B stage 2 で最初に実測）、Anthropic API 費用（D9 の記録と上限）、hcom 0.7 の変化（固定版 + 全 store 読み）。

## Status log

- 2026-10-18 09:5x JST plan 起票。何も実行していない。決定 D1〜D12 の既定値、分類表、波表はユーザーの合意待ち。合意後の最初の操作は 5.1 の順（ユーザーの D1/D2 トグル → #401 マージ）。
- 2026-10-18 10:2x JST 第 9 節（実行可能性の検証 V1〜V15）を追加し、C stage 1 を追加型に、5.1 に `SKIP_RESOLVE`、B の完了条件に描画差分 0 を反映。
- 2026-10-18 10:4x JST 付録 A（役割別ボトルネック台帳、公式根拠付き）と F5（CI 効率化）を追加。omp hooks と hcom idle 検知の手段を docs で確定。
- 2026-10-18 10:5x JST ユーザー指示「2 つに分けるべき」により 0b（第 1 段階 = 現環境のボトルネック解消 P1-1〜P1-9 と退出条件 DoD-P1、第 2 段階 = 方向転換）を新設。D4/D8 を第 1 段階へ、第 6 節の波表を 2 段階に、C stage 2 を移植のみに、B/C stage 1 の実装は draft で退避に変更。
- 2026-10-18 11:0x JST ユーザー指摘「一枚に詰め込むと LLM に不利」により、読む時機で 5 文書に分割: この plan（最初に読む）、`024-design.md`（必要に応じて）、`024-todo.md`（作業項目と完了条件）、`024-checklists.md`（終了時: DoD-P1 と DoD）、`024-progress.tsv`（進捗、boundary ごとに更新）。本文は節単位で移しただけで文言は変えていない。分割前の全文は席の scratchpad に `024-full-backup.md` として保持。
- 2026-10-18 12:5x JST 網羅精査（独立の読み手 fork の所見 49 件: P0 2、P1 12、P2 22、P3 13、と機械照合で見つけた旧参照 31 箇所）を反映。主な修正: 0b の「merge しない」を live 運用を変える PR に限定し 0e と整合、5.1 のマージ順から B/C を外す、#401 はユーザーの承認 1 回（live gate は記録 PR を merge 経路で ask）、D3 に (d) の分岐と T131-fix タスク、`herdr-agents`（P1-5 → P1-7）と `dispatch.sh`（P1-6 → P1-13）の衝突を直列化、`security: true` の列挙を P1-3/P1-4/P1-7/P1-13/P1-14 に拡大、Q-D の凍結条件を第 7 節に追加、見積もりを 13 PR・5 波・10〜12 時間に統一、verdict の出力パスと `.orchestration/learning/classes.yaml`・`.schemas/`・`.github/flakes.yaml`・`.githooks/` の規約を統一、progress.tsv に P1-10〜P1-14 と暫定項目、checklists に P1-m〜P1-p、programs に (17) integrate-seat、execution にユーザー操作の時機順一覧と `make update` の退避と rollback、旧波表 2 つを削除。
