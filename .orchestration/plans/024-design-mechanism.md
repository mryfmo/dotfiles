# Plan 024 設計 1/5: 仕組み（指示役・監査役・CI/Bot の改善設計と是正の手段 5.0〜5.7）

> 読む時機: 第 1 段階のタスク文を書くとき、是正の手段を確かめるとき。節: 仕組みの設計（状態機械、役割別の変化、verdict の 9 条件）、5.0 台帳、5.1〜5.7 是正。5.8〜5.13 は `024-design-quality.md`、プログラム仕様は `024-design-programs.md`、PR A〜H は `024-design-prs.md`、根拠は `024-design-evidence.md`。

## 第 1 段階で作る仕組みの設計（指示役・監査役・CI/Bot を品質と速度でどう変えるか）

今の 1 PR の流れは、タスク文 → dispatch → 実装 → RESULT → **orchestrator が** review・sweep・判定 → revise 往復 → **orchestrator が** chain（update-branch、CI 待ち、Bot 待ち、sweep、local review）→ **orchestrator が** 監査（Codex headless、1 本ずつ 10〜15 分）→ disposition → gate → merge → 記録、で、太字の工程が全部 1 席の直列。席が増えても orchestrator の処理量が増えるだけで並列にならない。第 1 段階で次の形に変える（P1-4〜P1-8 の中身）。

**改善後の 1 PR の状態機械（席が進め、orchestrator は判定とマージだけ）**

```
TASK ─▶ 実装 ─▶ precheck（席: local review, unit, render-check, Bot 下書き）─▶ RESULT(precheck=sha)
  ─▶ integrate-seat（席: update-branch が要る時だけ, CI 待ち --interval 30, sweep 最終 head, audit-request）
  ─▶ audit-pool（同時 2 本, 構造化 JSON, 差分監査）─▶ verdict（スクリプトが機械判定: accept | revise | hold）
  ─▶ orchestrator: accept なら ACCEPTANCE 1 行 + gh pr merge --match-head-commit（約 2〜5 分）
      revise なら生成済みの revise 行を送るだけ（previous_head=, check=, counters 付き）
      hold（S1 / INV-6 / P0）だけが orchestrator の判断
  ─▶ records（RESULT と verdict から生成）─▶ dispatch --next（席に次のタスク）
```

| 役割 | 今（直列点） | 改善後 | 速度 | 品質 |
| --- | --- | --- | --- | --- |
| 指示役 | 全工程を自分で実行。1 PR に 60〜135 回のツール呼び出し、1 ターン 38〜75 分 | 計画とタスク文、`dispatch.sh --next` の実行、`verdict.sh` の結果に基づく ACCEPTANCE/revise 送信、最終マージ。review・sweep・chain・監査・記録は席とスクリプト | 1 PR あたり 2〜5 分（verdict 読み + 1 コマンド）。4〜6 席が同時に RESULT を出しても 1 時間に 12〜20 件捌ける | 判定材料が verdict JSON に固定され、読み落としが出ない。hold の判断に時間を使える |
| 監査役 | `orch-audit.sh` が head ごとに全差分を 1 本ずつ Codex headless で監査。所見は散文、記録への写しは手作業。update-branch だけでも再監査 | `audit-pool.sh`（orchestrator が boundary ごとに起動する常駐ループ）。席の `audit-request` を拾い、同時 2 本で `codex --profile audit exec --sandbox read-only`（切替後は omp 監査役）。出力は `audit-<head>.json`（verdict、findings[priority, confidence, file, line, class, rationale]、JSON Schema を `validate` CI が検査）。2 回目以降の head は前回の head との差分と前回の所見だけを渡す差分監査。update-branch のみの head は継承（#390） | 初回 10〜15 分、revise 後は 3〜5 分。並列 2 本で 1 時間に 8〜12 本 | 範囲は AGENTS.md Audit 節のまま（正当性、セキュリティ、回帰、規則、証跡、報告漏れ）。所見が構造化されるので S1 の同一クラス計数と disposition が機械化され、見逃しが減る。trust-boundary タスクは security profile の 2 本目を維持 |
| レビュー | review 席 a005 がタスク文と RESULT を往復レビュー。Bot を head ごとに最大 15 分待つ | タスク文レビューは 1 ラウンド固定（既定）。RESULT のレビューは席の precheck（local review スクリプト）と監査に吸収。Bot は待たず最終 head の sweep で全件 disposition | review 席の待ちが消える | Bot 所見は 1 件残らず disposition（gate で必須）。local review は RESULT 前に席が通す |
| CI | 13 チェック/push、macOS 3、concurrency なし、strict の N²、Bot 待ち | 5.9 の Q1〜Q9: PR は最新 head だけ、必須でない bootstrap は main と日次、必須ジョブは in-job skip、キャッシュは計測後、main の push で全マトリクス | PR 1 本の CI 10 分 → 5〜7 分、macOS 待ちほぼ 0、PR あたりの run 3 回以下 | 必須チェック 7 本は不変。飛ばした検証は main で必ず走る。赤なら凍結 |
| 作業役 | RESULT 後に revise 往復（34/98）、席が空く | precheck で RESULT 前に自分で止める。統合も自分の PR で完走。`--next` で次を受け取る | 往復と idle が減る | 証跡が揃った RESULT しか出ない |

**verdict.sh の判定（機械。すべて揃って accept）**: (1) RESULT の `precheck=` が証跡の sha256 と一致、(2) head の必須チェック 7 本が緑（`gh pr checks`）、(3) `audit-<head>.json` の verdict が correct、または records-only の所見しか残らない、(4) sweep の全スレッドが最終 head の disposition を持つ、(5) 変更ファイル ⊆ allowed_files、caps 内、(6) S1 の同一クラス計数 < 3、INV-6 の revise < 2、(7) P0/P1 の未対処なし、(8) `security: true` のタスクは security review の verdict=correct、(9) 受け入れ記録の証跡 sha256 と実ファイルの一致（正本は 5.12 (1)）。1 つでも欠ければ `revise`（欠けた項目から revise 行を生成）か `hold`（S1 / INV-6 / P0 / 入力欠落）。verdict は `.orchestration/validation/<task>-verdict-<head>.json` に書き、ACCEPTANCE 行と記録が参照する。

**並列の見積もり（4〜6 席）**: 席側統合が並列、監査 2 本並列、CI は 3〜5 PR 分並列（S3）、orchestrator は 1 PR 2〜5 分。したがって定常で 1 時間に 6〜10 本のマージが天井で、律速は CI と監査枠。orchestrator は律速でなくなる。

## 5. 是正計画（従属。切替まで現環境を回す最小限）

5.0 **並列稼働と品質のボトルネック → 是正の対応表**（根拠は Grok Bot の 20:02 / 21:19 / 07:46 の調査と、この席の記録。各行の「是正」は本 plan 内の位置）

| # | ボトルネック・問題 | 根拠 | 是正（plan 内の位置） | 切替後に残るか |
| --- | --- | --- | --- | --- |
| B1 | orchestrator 1 席に受け入れ・RESULT 審査・review・gate・タスク文・記録が集中（rules「委任しない」）。65 分ターンでツール 135 回、約 6 割が手作業 | 20:02 診断、rules/agmsg-orchestration.md:7 | P1-4a/P1-4/P1-6（verdict、統合チェーンの席側実行 `integrate-seat.sh`、records 補助）、H3（review を hcom 経由の両ベンダー review に置換、verdict ファイルを返す）、E2 で「委任しない」条項を「受け入れ判定と最終マージのみ」に縮小、D8 | 消える（orchestrator は判定と最終マージだけ） |
| B2 | 統合が直列: 1 本ごとに update-branch → CI → Bot 待ち → audit。strict up-to-date で 1 本マージするたび全 PR が再 CI（N²、1 本/時間） | 07:46 調査（CI 中央値 10 分、macOS runner 待ち 26 分、約 36 回の全再実行） | D1（strict OFF 今すぐ）、5.1（依存順に 1 本ずつ、main の push CI 緑で次へ）、D-parallel-chains（chain は並列、マージのみ直列、既に運用中）、P1-4 の席側統合 | 消える |
| B3 | ruleset のスレッド解決必須。解決は gh api 書込で人の承認待ち。#389 8 / #387 6 / #393 5 / #378 5 など | 08:30 監査、09:3x 実測 | D2（OFF。disposition は sweep ゲートが最終 head で既に強制） | 消える |
| B4 | revise 率 34/98、同種所見の繰り返し（#379 #383 #382 #393 #399）、RESULT 前ラウンド非計数、update-branch だけで再監査 | 16:59 分析、21:19 調査、D-393-hold、D-399-A | main 済: S1 ゲート #382。F1 #390（監査継承）、F2 #387（正規化 lint、ps 解析禁止）、C stage 1（RESULT−1 と revise 行の大きい方、revise 行の 4 拒否）、P1-5（pre-RESULT ゲート）、plan 第 7 節 STOP（決定行での上限超過禁止 C-66） | 残る（ハーネス非依存の品質装置） |
| B5 | 席上限が SKILL で 3、実態 4。Codex 席が 1 本で「Claude 境界は Codex 席」のルーティングが単一点 | 21:19 調査（SKILL.md:38、rules:13） | D10（4 → spark 稼働後 6、P1-7 で herdr-agents が数値上限を強制）、切替で席が全部 omp になり境界ルーティング自体が消滅（E2 で規則削除） | 上限だけ残る |
| B6 | 手の空いた席が orchestrator の返事待ちで 10〜60 分空く（a004/a007 21:19、3 席 01:22〜、4 席 03:29〜07:54） | 21:19、01:45、03:12 の見回り | P1-6（idle PONG → `dispatch.sh --next` が前提充足のタスクを自動で渡す。第 2 段階 C-2 で `hcom events --idle` に差し替え）、plan 第 6 節の波表（各波で 4 席すべてに素なタスク）、D1/D2 で承認待ちの停止を無くす | 消える |
| B7 | 長ターン（38 / 75 / 65 分）、約 1M トークンの文脈、1 呼び出し 20〜35 秒、54 回の heredoc、10/14 から未リセット | 20:02 診断 | B stage 2（omp hook で文脈 600k 超の handoff 強制）、5.5（切替まで 20 分・25 ツールの自己基準、超える処理は席へ）、D9（使用量の記録） | 仕組みとして残る |
| B8 | gh 書込が人の承認待ち（T130 の 32 ルールで 01:05〜07:54 マージ 0） | 01:16、07:35 | D3（#400 を暫定でマージ、E で削除）、B stage 2（omp 側 hook: 統合スクリプト経由以外の gh 書込を拒否） | omp hook に置き換わる |
| B9 | Mac のスリープで処理が 4 回中断 | 21:33 調査 | 済み（20:30 `disablesleep 1`、#394 の doctor チェックが 07:54 マージ） | 済み |
| B10 | 再起動後の Monitor ツール消失、agmsg `history.sh` / `bus-read.sh` が 120 秒超で無応答（今朝 2 回） | 01:45、この席 | 5.5（`timeout 60`、3 回目で defect 記録）、C（hcom 配送は hook 経由で Monitor 不要） | 消える |
| B11 | live 設定の手作業適用（settings.json、git config）と main の不一致 | 08:30 監査 | 5.3（#400 マージ → `make update` → `chezmoi verify`、DoD2）、boundary 時に `chezmoi verify` を確認項目に | 消える |
| B12 | 監査が 1 タブで直列、Codex の headless 実行 | SKILL:43 | B（監査役を omp 実行に。headless で PR ごとに並列可。task-level audit は 1 PR 1 回のまま） | 残る（並列化される） |
| B13 | 報告が人に把握できる形でない（チャット文の積み重ね） | 08:20〜08:36 | 5.7（boundary 記録の 2 部定型 + project-map）、H6（停滞の機械検知）、H7（omp ログの HTML） | H6/H7 が担う |
| B14 | 外部（Grok Bot）が orchestrator のターン中に指示を連投し、ターンを延ばし自己判断で方針を変えた | 20:02 診断、08:33 B 表 | D12（Bot は報告のみ、herdr への指示なし） | 消える |

**順序の原則（0b の 2 段階に合わせて改訂）。** 第 1 段階で B1〜B8・B10〜B12・B14 を現環境で解消する（P1-1〜P1-14）。慢性のボトルネック（B1 集中、B4 revise、B6 idle、B5 上限）もここで、ハーネス非依存の `scripts/orchestrator/*`・CI・manifest として作る。Claude 専用の層に新しい仕組みは作らない（#400 の暫定マージだけが例外）。第 2 段階は DoD-P1 を満たした後に始め、C stage 2 は第 1 段階の仕組みを hcom/omp へ移植する。波の割り当ては plan 第 6 節（第 1 段階 P-W0〜P-W4、第 2 段階 D-W0〜D-W3）。


5.1 **マージ経路（今日）**: ユーザーが ruleset 24397953 で D1/D2 を切る → ユーザーの承認 1 回で #401 をマージ（記録 PR は gate なし、live の gh-merge-gate は merge 経路に受け入れ記録と監査を要求するため）→ 依存順に 1 本ずつ: #390 → #389 → #396 → #378 → #375 → #398 → #405 → #402 → #387 → #400（D3 のラウンド後）。B-1 のマージは 0e 条件 3（P1-14 の後）、C-1b は DoD-P1 の後。各マージの後、main の push CI が緑になるまで次を入れない（赤なら凍結、fix-forward PR）。各 PR は受け入れ済み head を `gh pr merge --squash --match-head-commit` で、ゲート（`make require-crit-review` + sweep + audit evidence）を通してから。D2 の後は chain glue `finish-pr.sh` の `resolve-threads.sh` 呼び出し（行 17）を `SKIP_RESOLVE=1`（既定）で飛ばす。disposition の sweep と記録はそのまま（evidence V3）。見込み: 1 本 10〜15 分、全体 2〜3 時間（audit 未実施の head は +15 分）。
5.2 **閉じる**: #393、#399、#383、#315、#317、#323、#403（D4〜D7）。ブランチは残す。
5.3 **環境の整合**: #400 マージ → `make update` → `chezmoi verify` rc 0（DoD2）。これで手編集の `settings.json` と `git config` が main 由来に揃う。バックアップ 4 本と `~/.local/state/grokbot/*` はユーザーが不要と判断したら削除（席からは触らない）。spark は X で `make update`。
5.4 **記録**: 今朝の未コミット（D-399-A、D-393-hold、M-20261018-01/02、C-65/C-66、T129/T131/T132 タスク文、この plan、decisions の D-024-*）を boundary 23 として #401 の次の記録 PR に。Plan 023 の Status log に 024 への参照を 1 行。
5.5 **orchestrator の運用（切替まで）**: 1 ターン 20 分・ツール 25 回を自己基準に、超える処理は席へ。agmsg の `history.sh` / `bus-read.sh` が 120 秒超で止まる事象（今朝 2 回）は `timeout 60` を付けて使い、3 回目で defect 記録。Monitor 不在のため turn delivery と `inbox.sh` を節目ごとに。handoff は `scripts/orchestrator/handoff.sh`（P1-9、programs (10)）が `.orchestration/handoff/<UTC>.md` に生成する。
5.6 **品質で残すもの / 外すもの**: 残す = 必須チェック 7 本、最終 head の task-level audit（切替後は omp 監査役）、S1 と INV-6（決定行での上限超過は C-66 で禁止）、allowed_files の互いに素、PR 経由 main と `--match-head-commit`、sweep と disposition、秘密マスク、trust-boundary タスクの脅威表。外す = strict up-to-date、GitHub 上のスレッド解決必須、gh 書込への人の ask（今は #400 の hook、切替後は B stage 2 の omp hook）。
5.8〜5.13（多重並列の天井 S1〜S10、PR 多重時の CI/Bot Q1〜Q9、追加の仕組み M1〜M12、品質保証 Q-A〜Q-F、プログラム仕様の所在、人の判断の細分化）は `024-design-quality.md` に分離。

5.7 **報告（人が把握できる形）**: 切替まで = 各 boundary の記録 PR 本文に「全体（PR A〜H の状態）/ 今の問題」の 2 部を定型で書き、project-map を更新。切替後 = H6（停滞検知）と H7（HTML）。Grok Bot は D12 のとおり pause。

