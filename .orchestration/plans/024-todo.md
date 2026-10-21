# Plan 024 作業項目（ToDo）: 第 1 段階 P1-1〜P1-14 と第 2 段階の PR

> 読み方: 波表（plan 第 6 節）で自分の席に割り当たった項目の行だけを読み、詳細は `024-design.md` の目次から該当文書の節とタスク文へ。完了条件はこの表の列が唯一の定義。プログラムの仕様番号 (n) は `024-design-programs.md`。

## 第 1 段階のタスク（P1-1〜P1-14。各 1 PR、allowed_files は互いに素、担当は plan 第 6 節の波表）

| # | 目的（解消するボトルネック） | やること | 完了条件（機械的） |
| --- | --- | --- | --- |
| P1-1 マージ経路の復旧 | B2 strict の N²、B3 スレッド解決必須、B8 承認待ち、B11 live 不一致 | ユーザーの 2 トグル（D1/D2）→ #401（記録 PR は gate なし、plan 020 step 3。live の gh-merge-gate は merge 経路に受け入れ記録と監査を要求するので、ユーザーの承認 1 回で merge）→ 依存順の直列マージ（design-mechanism 5.1）→ glue `SKIP_RESOLVE=1` → #400 の P1 ラウンド（a010、タスク `dotfiles-T131-claude-pinned-merge-gate-fix-a01`。D3 の (a)、収まらなければ (d)）→ マージ → `make update` → `chezmoi verify` | plan 第 3 節の merge/close が完了、main の push CI 緑、DoD2、DoD9 |
| P1-2 再ラウンドの削減 | B4（update-branch で再監査、lint 不在） | F1 #390 マージ、F2 #387 の CI 赤と 6 スレッドを 1 ラウンドで直し 445c32dd を畳む | update-branch のみの head で監査が継承された記録 1 件以上、#387 が追加する lint ターゲット（名称は PR で確定）が CI で走る |
| P1-3 CI の効率化（F5） | C2 macOS 同時 5 の飽和、C3 旧 run の残留、C4/C5 不要な bootstrap、M9 flake | `concurrency` + `cancel-in-progress` を test/remote/agent-assets に、`private-bootstrap` を PR から外す、`public-bootstrap` の in-job skip を広げる、テスト並列化は item 0 で確認後、`.github/flakes.yaml` + `ci-rerun.sh`（(11)） | bootstrap パス非変更の PR で macOS ジョブ ≤ 1、3 workflow に concurrency、`gh run list` の PR 1 本の wall time 中央値を記録（目標 ≤ 7 分） |
| P1-4a verdict.sh と audit-pool.sh | B1 集中、A1 監査の直列、A3 散文所見、M1、M5 | (1) `verdict.sh`（9 条件、`--apply/--loop/--shadow`）、(2) `audit-pool.sh` と `orch-audit.sh --json`、(3) `.schemas/audit.json`・`.schemas/verdict.json`・`.orchestration/learning/classes.yaml`（class の制御語彙） | 実 PR 2 本で verdict が accept/revise を正しく出す fixture、監査 JSON が schema 緑、revise 後の head の監査が 5 分以内の記録、shadow 比較の運用開始 |
| P1-4 統合の席側実行（integrate-seat） | B1 集中、O2 直列、R2 Bot 待ち | 新タスク `integration-seat-a02`（#393 の 8 P1 を設計で disposition してから、ハーネス非依存で作り直す）: (17) `integrate-seat.sh`。Bot 待ちは chain から外し最終 head の sweep のみ。orchestrator に残すのは verdict と `gh pr merge --squash --match-head-commit` | 席が統合を完走した PR ≥ 2、統合ログに orchestrator の手作業 0、verdict.sh が席の証跡を受理 |
| P1-5 RESULT 前ゲート（result-precheck） | B4 revise 34/98、W4 文脈枯渇、M6、M7 | (4) `result-precheck.sh`（検査、赤→緑の証明、`precheck.json`、`result.txt`）、(9) の `.githooks/pre-commit`・`pre-push` と検出器（`herdr-agents` の hooksPath 設定は P1-7）。受け入れ側は `precheck=` の無い RESULT を拒否（`PRECHECK_REQUIRED` で段階強制） | 拒否の fixture 緑、以後 10 PR の revise 率 ≤ 20% を記録 |
| P1-6 記録の自動生成と次タスクの自動割当 | B1、B6 idle、W2 presend 戻り、M8、M10 | (8) `acceptance-front-matter.py --from-result`、(7) `dispatch.sh --next <seat>`（context% で拒否、`default_after=` の既定値消費） | 連続 2 波の bus 履歴で席の idle 間隔 ≤ 15 分（24 時間統計は第 2 段階中の監視）、記録 PR の手書き行 0 |
| P1-7 席数上限の数値化と launcher | B5/W7、(9) の hooksPath | manifest `worker_cap: 4`、`herdr-agents --add-worker` が超過を拒否し worktree に `core.hooksPath=.githooks` を設定、validator が SKILL の文言と一致を検査（#393 の該当部分を流用）。`herdr-agents` の変更系列は P1-7 → C-2 | テスト緑、`herdr-agents --add-worker` 5 席目が拒否される、着席した worktree で `git config core.hooksPath` が `.githooks` |
| P1-8 ルール文の縮小と契約の追記 | B1 の根（「委任しない」条項） | agmsg-orchestration の rules と SKILL: 「受け入れ・RESULT 審査・review・gate は委任しない」→「受け入れ判定と最終マージのみ orchestrator。統合・review・記録は席とスクリプト」。契約の追記: PONG の任意フィールド `context=<%>`、task.md の `requires_decision:` キー、`.orchestration/<task>/result.txt` の規約、RESULT の `precheck=`。文章は 1 段落、残りは P1-4〜P1-6 の仕組みが担保。共有ソースなので Codex 席 a010（plan 021 8.3） | `test_agmsg_orchestration_docs.py` 緑、`make check-regime-boundary` 緑 |
| P1-9 orchestrator の運用 | B7 文脈、O5 バス無応答、M12 | boundary 23 で handoff → 再起動、履歴読みに `timeout 60`、1 ターン 20 分・25 ツール。Monitor 不在は turn delivery。(10) `handoff.sh` が `.orchestration/handoff/<UTC>.md` を生成 | 再起動の記録、無応答が 3 回目なら defect 記録 |
| P1-10 所見 disposition の自動化 | R2/R4 の手書き disposition、A3、M2 | (5) `dispositions.py`（fixed 候補、refutation 3 形式の必須化）、(16) `audit-pool.sh --second-opinion`（P0/P1 の not-applicable に合議必須） | 実 PR 1 本で全スレッドの候補生成、空の not-applicable を拒否する fixture、合議の fixture |
| P1-11 CI の regime ジョブ | verdict の条件 (1)(5) を GitHub 側で、M3 | (6) `.github/workflows/regime.yml` と `regime-ci.py`。まず任意チェック | 違反 fixture で赤、正常で緑。必須化はユーザーの ruleset 操作 |
| P1-12 タスク文の生成とチェッカー拡張、plan の検査 | W2 presend 往復、タスク文 10〜20 分、M4、plan の形式・drift | (12) `task-from-plan.py`、`task-consistency-check.py` C11〜C15（3 つの形の規則、threat_table 単位規則、disposition 3 種、premises 実行、INV-2）、(15) `plan-check.py`（形式、`--drift`、`--invariants`） | 生成した task.md がチェッカー C1〜C15 を一発で通る fixture、形の規則の赤緑、plan 群で違反 0 |
| P1-13 hold の playbook | hold の扱いの機械化（design-quality 5.13） | (13) `hold-playbook.sh`、`.orchestration/learning/classes.yaml` の `remedy:` と `blast_radius:`。`dispatch.sh` の hold 中拒否は P1-6 マージ後に着手 | 既知 class 3 つの remedy 展開 fixture、範囲外で決定行が出る fixture、hold 中の送信拒否 |
| P1-14 permission guard と ruleset 補助 | 権限変更の検知と承認の機械化（design-quality 5.13） | (14) `permission-guard.py`（validate CI）、`ruleset-request.sh`、`ruleset-verify.sh`。validator 系列は #400 → P1-7 → P1-14 → B-1 → G | 権限 diff に決定行なしで赤、ありで緑；ruleset-verify が現在値と期待値の差を 1 行 1 件 |
| 品質の条件（design-quality 5.11、仕組みタスクに共通） | Q-A〜Q-F | P1-3、P1-4a、P1-4、P1-5、P1-6、P1-7、P1-10〜P1-14 は `security: true` と threat_table 必須、security review の 2 本目を受ける。fail-closed（欠落・不一致・schema 不合格は hold / 拒否）。verdict は shadow mode で手判定と並走し一致 4 件まで `--apply` 無効。証跡はファイル名に head を含め sha256 を記録。新規スクリプトは赤→緑 fixture 付き | 024-checklists.md P1-j、P1-k、P1-l |

## 第 2 段階の作業項目（DoD-P1 の後。詳細は `024-design-prs.md` 第 4 節、順序は plan 第 6 節 D-W0〜D-W3。0e の 4 条件を満たす準備は第 1 段階の空き枠で前倒し可）

| # | 項目 | 一行の中身 | 完了条件（design-prs 第 4 節の該当項） |
| --- | --- | --- | --- |
| A | 資産固定の仕上げ | #398、#405 をマージ。spark は X で `make update` | DoD1、`make update` 2 回で差分 0 |
| B-1 | omp 設定生成 stage 1 | a009 の 41da91ce を ready → マージ（P1-14 の後、0e 条件 3） | `make render-check` 緑、Claude/Codex 生成物の差分 0、config.yml の 6 役割の provider |
| B-2 | omp hooks / permission | gh 書込拒否、600k handoff、Stop 相当（docs/hooks.md の `tool_call`、`session_before_compact`、`turn_end`） | 拒否と handoff のテスト |
| C-1 | hcom-dispatch とバス読み（追加型、`bus: agmsg` 既定） | C-1a 新規スクリプト（`bus-history.sh`、`hcom-dispatch`、テスト。前倒し可）、C-1b 配線（dispatch/bus-read/counters の経路選択。P1-13 の後） | 5 ファイルの `grep -c agmsg` が説明行のみ、fixture 緑 |
| C-2 | hcom 着席と第 1 段階の仕組みの移植 | `herdr-agents` が `hcom omp`、launch.json、precheck/`--next`/cap/hooks の移植、最小 SKILL、member list | PING/PONG が hcom 越しに `bus-history.sh` に出る |
| D | 認証検査 | #389 → #396 → #404 | DoD4 |
| X | 切替 | `make update` → ログインと API キー → パイロット 1 席 → 全席 → orchestrator | DoD3、DoD11 |
| E1〜E3 | 撤去 | hooks/settings → skill/rules/Makefile/launcher → 本体とテスト | DoD5、DoD6、DoD8 |
| G | pstack | G-a vendor 準備（前倒し可）、G-b 固定 sha と manifest（validator 系列の後） | DoD7 |
| H1〜H9 | スキル書き直し | 優先順 H3、H6（前倒し可）、H7 → H1、H5 → H2、H4、H8、H9 | DoD8 |
| spark | relay + machine add + 2 席目 | 私設ブローカー、SSH 転送、D10 で 6 | X(6) |
