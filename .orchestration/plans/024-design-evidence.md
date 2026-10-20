# Plan 024 設計 5/5: 根拠（実行可能性の検証 V1〜V15、役割別ボトルネック台帳 付録 A）

> 読む時機: 判断の根拠や公式ドキュメントの出典を確かめるとき、所見の disposition を書くとき。通常の作業では読まない。

## 9. 実行可能性の検証（後続を Claude Code + Codex + agmsg の現席で遂行できるか。2026-10-18 10:2x JST、この席の実測）

観点: (i) 権限と sandbox、(ii) 境界ルーティング規則、(iii) バス移行の順序、(iv) 品質装置の連続性、(v) 席の能力と文脈、(vi) ハーネス固有の障害、(vii) 文章（SKILL）の整合、(viii) 工程の実時間。結論: 遂行できる。ただし V1〜V4 は初版の順序欠陥で、修正を入れないと切替前の運用が止まる。修正は本文（C stage 1、5.1、B 完了条件、波表 W0）に反映済み。

| # | 観点 | 検証したこと（コマンドと結果） | 判定 | 修正 |
| --- | --- | --- | --- | --- |
| V1 | (iii) | `dispatch.sh` の履歴読みは `AGMSG_SCRIPTS` 1 本の seam（行 66・347）。C stage 1 原案は送信を hcom-dispatch に切り替えるが、席は agmsg のまま → マージした瞬間に orchestrator の TASK が誰にも届かない | 欠陥 | C stage 1 を追加型に。`bus: agmsg|hcom`（既定 agmsg）で経路選択。切替 X で hcom、E で seam ごと削除 |
| V2 | (i) | live `~/.claude/settings.json`: `agmsg-dispatch` は allow と excludedCommands にあるが `hcom` は 0 件、`~/.hcom` は allowWrite に無い。Claude 席（orchestrator 含む）は sandbox 内で `hcom send` できない | 欠陥 | Codex 席 a010 の 1 行タスク（Claude 境界）: `agent-config.yaml` に `hcom-dispatch` の excludedCommands/allow。C-1b 配線の前提。10:5x の 2 段階化で第 2 段階 D-W0 に移動（第 1 段階では `hcom-dispatch` を使わない） |
| V3 | (iv) | `.agents/worklog/orchestrator-glue/finish-pr.sh:17` が `resolve-threads.sh` を呼ぶ。D2 で ruleset の解決必須を外しても、glue が graphql 書込を発行して ask で止まる | 欠陥 | 5.1: `SKIP_RESOLVE=1`（既定）。sweep と disposition 記録は従来どおり。glue は orchestrator 管轄 |
| V4 | (vii) | agmsg-orchestration SKILL に worker 向け agmsg スクリプト言及 13 箇所。X（切替）が E2（SKILL 置換）より前なので、omp 席が読む文章が agmsg 手順のまま | 欠陥 | C stage 2 に hcom 版の最小 SKILL（送受信、PING/PONG、RESULT の形、停止ゲート）を含める。E2 は旧文の削除だけ |
| V5 | (iv) | `scripts/check-regime-boundary.sh` は agmsg/identities/team に 18 箇所依存し、C stage 1 の allowed_files に無い | 不足 | C stage 2 で hcom の member list 版に。それまで boundary check は agmsg 席の間だけ有効 |
| V6 | (ii) | B stage 1 は Claude 席 a009 が `agent-config.yaml` を編集。追加は omp キーで Claude 境界ではないが、generator/validator の変更は Claude/Codex 設定の描画に波及しうる | 条件付き可 | B stage 1 の完了条件に「Claude/Codex 向け生成物の差分 0」。監査が確認 |
| V7 | (ii) | #400 の P1 ラウンドは Claude 境界 → Codex 席 a010（可）。E1/E2 は両境界だが X の後に omp 席が実施するので規則の対象外 | 可 | なし |
| V8 | (iv) | gh-merge-gate hook は `mergeStateStatus` を見ない（PR open・非 draft・main 宛・head 一致・必須チェック緑・記録の head と最新 ACCEPTANCE=accepted、行 70〜80・147・190）。D1 で BEHIND でもマージが通る。gate は手作業適用で稼働中 | 可 | D3 のマージまで `make update` を走らせない（走らせると ask に戻る） |
| V9 | (i)(vi) | Claude 席の auto-mode classifier が今朝も `rm`、`cat >`、`grep` を拒否。omp の auth store 読みは以前「Credential Exploration」で拒否。B/C stage 2 の実測（hcom.db、agent.db、omp hook）で同種の拒否が出る | 障害 | 実測は (a) 固定版の上流ソース（WebFetch）、(b) Codex 席、(c) `$TMPDIR` の使い捨て store に限定。拒否は `AGMSG-PONG status=blocked` で返し、迂回しない |
| V10 | (v) | a008/a009/a011 は 02:05〜03:xx 起動で文脈に余裕、a010 は Codex。orchestrator（この席）は約 1M 文脈で圧縮 2 回 | 条件付き可 | orchestrator は W1 の終わり（boundary 23）で handoff → 再起動。5.5 の 20 分基準 |
| V11 | (iv) | task-level audit は `codex --profile audit exec`、security review は `--profile security`（Codex ログイン済み）。切替まで維持、B で omp 監査役に | 可 | なし |
| V12 | (viii) | W0〜W2: バックログ 10 本 2〜3 時間、C stage 1 は caps 260/700 行で 1 席 1 日以内、B stage 1 は push と記録のみ。W3 は B/C stage 2 完了後 1 日（plan 第 8 節の AI 基準では 3 時間） | 可 | plan 第 7 節 STOP で逸脱検知 |
| V13 | (i) | Claude 席は `hcom`・`omp` を実行できる（sandbox 内で `hcom 0.7.30`、`omp/18.11.3`）が `~/.hcom` に書けない → C stage 1 のテストは `$TMPDIR` の store のみ（タスク文どおり） | 可 | なし |
| V14 | (vi) | agmsg `history.sh`/`bus-read.sh` の無応答（今朝 2 回）。`dispatch.sh` の window 読みも history.sh | 障害 | 5.5 の `timeout 60`。C stage 1 の `bus-history.sh` で置換 |
| V15 | (iv) | glue `dispatch-direct.sh` も agmsg-dispatch 直呼び | 不足 | C stage 1 の seam を glue にも通す（orchestrator 管轄、同じ `BUS`） |

遂行の前提は 3 つ: ユーザーの D1/D2 トグルと #401 の承認 1 回、T131-fix タスク（D3、#400 の 8 P1）、glue の `SKIP_RESOLVE`（V3）。V2 の 1 行タスクは第 2 段階 D-W0 に移動。V12 の工程見積もりは plan 第 8 節の AI 基準に訂正済み（履歴として残す）。

## 付録 A. ボトルネック台帳（役割別。現象 → 問題・課題 → 本質対処の手段・手法 → 公式根拠 → plan 内の位置）

根拠の取得日はすべて 2026-10-18（この席の WebFetch）か、Plan 023 の 2026-10-17 取得。「現象」は Grok Bot の実測（20:02 / 21:19 / 07:46 / 08:30）とこの席の 09:3x 実測。

### A-O 指示役（orchestrator）

| # | 現象（実測） | 問題・課題 | 本質対処（手段・手法） | 公式根拠 | 位置 |
| --- | --- | --- | --- | --- | --- |
| O1 | 65 分ターンでツール 135 回、約 6 割が受け入れ記録・台帳・タスク文・自前レビュー。rules「受け入れ・RESULT 審査・review・gate は委任しない」 | 1 席が全工程の直列点。席が結果を返しても判定待ちで止まる | 判定と最終マージ以外を席とスクリプトへ。統合チェーンは席側 `integrate-seat.sh`、記録は RESULT JSON から生成、review は H3 の両ベンダー review が verdict ファイルを返す。E2 で条項を縮小 | hcom README「Hooks record activity to a local SQLite database and deliver messages from it」（配送は hook で自動、orchestrator の手作業不要）。omp docs/hooks.md: `turn_end` / `agent_end` イベントで記録生成を自動化できる | 5.0 B1、P1-4a/P1-4/P1-6、H3、E2 |
| O2 | 統合が 1 本ずつ: update-branch → CI → Bot 待ち（最大 15 分）→ 監査。1 本/時間 | strict up-to-date が N² の再 CI を強いる。Bot 待ちは自前の規律 | strict OFF（D1）。Bot は repo rule どおり「optional、never gated」なので待ち上限を chain から外し、最終 head の sweep だけ残す。update-branch のみの head は監査継承（#390） | GitHub rulesets docs: strict は「The Require branches to be up to date before merging checkbox is checked」行の設定。`gh pr merge --match-head-commit`「Commit SHA that the pull request head must match to allow merge」（cli.github.com） | D1、5.1、F1 |
| O3 | 文脈 840k〜964k トークン、1 呼び出し 20〜35 秒、54 回の heredoc、10/14 から未リセット | 文脈肥大がすべての手作業を遅くし、圧縮で判断が欠ける | 600k で handoff を強制する hook（omp: `session_before_compact` / `context`）。切替まで 5.5 の自己基準。heredoc は `uv run … <file>` に（既に PreToolUse が拒否） | omp docs/hooks.md のイベント一覧（`session_before_compact`、`context`）。Claude Code hooks docs: Stop hook `decision: "block"` で終了を止められる（現行の agent-stop-gate の根拠） | B stage 2、5.5 |
| O4 | 01:05〜07:54 マージ 0（gh 書込 32 本の ask）。live 設定は手作業適用 | 「進めてよいか」を人の ask に委ねた。設定の手作業で main と不一致 | 判定を機械に: 現行は #400 hook（PR open・非 draft・main 宛・head 一致・必須チェック緑・記録 accepted）、切替後は omp `tool_call` の block。設定は manifest → `make update` → `chezmoi verify` のみ | Claude Code hooks docs: PreToolUse `permissionDecision` allow/deny/ask、「staying silent doesn't approve it」、硬い allow/deny は permission system で（hook は補助）。omp docs/hooks.md: `tool_call` が `{ block: true, reason }` を返すと止まる、throw は fail-closed | D3、B stage 2、5.3 |
| O5 | agmsg `history.sh` / `bus-read.sh` が 120 秒超で無応答（今朝 2 回）。再起動後 Monitor ツール消失 | バス読みがブロッキングで、配送がツール依存 | hcom の read command（`hcom events --type message --full --last n`、`--sql`）を `bus-history.sh` 1 本に。配送は hook で自動（Monitor 不要）。切替まで `timeout 60` | hcom README: 配送は hook、`hcom events --wait`「Block until match for scripting」。a008 item 0 の実測（events_v、user_version 18） | C stage 1、5.5 |
| O6 | 外部（Grok Bot）がターン中に 9 連発の指示、自己判断で方針変更 | 指示の入口が複数で、ターンが延び判断がぶれる | 入口を 1 つに（ユーザー → orchestrator）。Bot は報告のみ | — | D12 |

### A-W 作業役（worker）

| # | 現象 | 問題・課題 | 本質対処 | 公式根拠 | 位置 |
| --- | --- | --- | --- | --- | --- |
| W1 | sandbox 外での再実行 2,891 回（agmsg 1,324、gh 966、codex 609、git 497、uv 320、mise 251、ps 148）。classifier の拒否（rm、cat >、grep、auth store 読み） | Claude の sandbox と classifier が席の 1 ターンを消費し、迂回を誘発 | T130 で 12 原因は済み。残りは切替で消える（omp の実行層へ）。切替まで実測は上流ソース / Codex 席 / `$TMPDIR` に限定、拒否は blocked PONG | Claude Code sandboxing docs（`allowMachLookup`、`excludedCommands`、Plan 022 D）。Anthropic legal: 第三者ハーネスでの OAuth 不可（code.claude.com/docs/en/legal-and-compliance） | V9、X、E |
| W2 | presend チェックで落ちた 4 タスクを orchestrator が直し、席に届くまで 107 分 | タスク文の修正が orchestrator に戻る | `dispatch.sh` の拒否は維持し、落ちたタスク文の修正は task-author 役（席）へ。チェッカーは `task-consistency-check.py` のまま | — | P1-12（task-from-plan、チェッカー拡張）、5.5 |
| W3 | 空き席が 10〜60 分（a004/a007 21:19、3 席 01:22〜、4 席 03:29〜07:54） | 次の割当が orchestrator の判断待ち | `hcom events --idle <seat> --wait` で idle 検知 → `dispatch.sh --next` が前提充足のタスクを渡す。波表で全席に素なタスク | hcom README: `hcom events --idle luna --wait 600 && hcom send …` の例 | P1-6（C-2 で hcom に差し替え）、plan 第 6 節 |
| W4 | a005 96%、a006 95% で文脈枯渇、再起動 | 長い revise ループが席の文脈を使い切る | revise 上限 2（INV-6）、pre-RESULT ゲートで RESULT 前に local review と監査予行、H5 recall で再起動後の復元 | omp docs/session.md: session JSONL と history.db（H5 の読み元） | P1-5、H5、plan 第 7 節 |
| W5 | Codex 席 1 本に Claude 境界の作業が集中。1 worktree 1 席 | 境界ルーティングが単一点 | 切替で席が全部 omp になり規則が消滅。1 worktree 1 席は安全のため残す | — | E2、X |
| W6 | revise 34/98、同種所見の繰り返し（#379 #383 #382 #393 #399） | 文字列解析・ps 解析・二重パーサーの設計、P2 修正義務 | S1 ゲート（#382 済）、正規化 lint と ps 解析禁止（#387）、監査継承（#390）、revise 行の 4 拒否と計数（C stage 1）、pre-RESULT ゲート（P1-5） | — | F1、F2、P1-5、C |
| W7 | 席上限 SKILL 3 vs 実態 4 | 文章の上限と実態の乖離 | 数値上限を manifest に置き `herdr-agents` が強制、6 は spark 後 | — | D10、P1-7 |

### A-A 監査役（auditor）

| # | 現象 | 問題・課題 | 本質対処 | 公式根拠 | 位置 |
| --- | --- | --- | --- | --- | --- |
| A1 | 監査は 1 タブで直列（`codex --profile audit exec --sandbox read-only`） | 1 PR の監査が次を待たせる | 第 1 段階 P1-4a の監査 pool（同時 2 本、構造化 JSON、差分監査）。第 2 段階 B で監査役を omp 実行に。1 PR 1 回は維持 | Codex CLI: `codex exec`、`--sandbox read-only`、`--profile`（現行）。omp: headless 実行（Plan 023 facts） | P1-4a、第 2 段階 B、design-quality S4 |
| A2 | update-branch だけの head で全再監査 | 監査が head に紐づき、内容が同じでも再実行 | patch-id で継承（#390） | — | F1 |
| A3 | 監査 15 件中 9 件が記録の書き方、5 回とも `incorrect` | 記録指摘がコードのマージを止める | 判定をコード/記録に分離（AGENTS.md Audit 節は済み）。監査 JSON の `scope=records` で機械分離（P1-4a）。記録指摘は owner task へ | — | F、P1-4a |
| A4 | #393 で 3 回目ラウンドを決定行で許可 | 上限が文章・口頭で、機械で止まらない | verdict の条件 (6) と `dispatch.sh` の revise 拒否（P1-4a、C-1 の 4 拒否）が上限超過を機械で止める。決定行での waiver 禁止 | — | P1-4a、C-1、plan 第 7 節、C-66 |
| A5 | #399 のセキュリティレビューで同一クラス 6 件 | 境界設計（sandbox 文脈を信頼する除外） | #399 を閉じ、omp では監査・レビューを omp 実行にして除外自体を無くす | — | D5 |

### A-R レビュー（review 席、Codex Bot、local review）

| # | 現象 | 問題・課題 | 本質対処 | 公式根拠 | 位置 |
| --- | --- | --- | --- | --- | --- |
| R1 | review 席 1（a005）、タスク文レビューが往復 | 人的 review の直列点 | H3: interrogate/reflect を hcom 経由で OpenAI と Anthropic の両モデルに回し verdict ファイル。タスク文レビューは 1 ラウンド固定（SKILL 既定） | hcom README（席間送受信） | H3 |
| R2 | Codex Bot の review を head ごとに最大 15 分待ち、update-branch だけでも新所見 | Bot を gate 扱いにしていた | repo rule「A bot review is optional and never gated」を chain に反映: 待ち上限を外し、最終 head の sweep と disposition のみ。自動 review は Codex 側設定「Automatic review」（P0/P1 のみ）で、必要時は `@codex review` | learn.chatgpt.com/docs/third-party/github:「In a pull request comment, mention `@codex review`」「turn on Automatic review under Personal preferences」、所見は「only P0 and P1 issues」 | 5.1、pr-integration rule |
| R3 | local-review / local-advisory が head ごとに走り、ファイル形式の所見で止まる | スクリプトが記録の形まで審査 | #402（local-advisory の suffix 読み）、#386 済。記録所見は advisory（owner task） | — | #402、F |
| R4 | ruleset のスレッド解決必須で緑の PR が BLOCKED（#389 8、#387 6、#393 5 …）。解決は graphql 書込で ask | 同じ情報の二重記録を人の操作で要求 | D2 で OFF。disposition は sweep ゲートが最終 head で強制 | GitHub rulesets docs:「Optionally, you can require all comments on the pull request to be resolved before it can be merged to a branch」（任意設定） | D2、V3 |
| R5 | Bot の review が付いた直後は comments が 0 件に見える（race） | sweep が早すぎる | 数秒後に再取得（memory の規律）。sweep は最終 head のみ | — | pr-integration rule |

### A-C GitHub Actions / CI

| # | 現象 | 問題・課題 | 本質対処（手段） | 公式根拠 | 位置 |
| --- | --- | --- | --- | --- | --- |
| C1 | 1 本マージごとに残り全部が update-branch + 13 チェック再実行（約 36 回の全再実行、CI 中央値 10 分） | strict up-to-date | OFF（D1）。代替の安全: 各 head で必須チェック緑 + 依存順の直列マージ + main の push CI 緑で次へ | rulesets docs（strict の定義、上記） | D1、5.1 |
| C2 | macOS runner の待ち最大 26 分 | プランの macOS 同時実行上限 5。PR 1 本で macOS 3 ジョブ（test、public-bootstrap、private-bootstrap）なので PR 2 本で枠が埋まる | PR あたりの macOS ジョブを減らす: `private-bootstrap` を `pull_request` から外す、`public-bootstrap` macOS を in-job skip（下記 C5）、`concurrency` で旧 head の run を止める | GitHub Actions limits: 「Free 20 / 5、Pro 40 / 5、Team 60 / 5、Enterprise 500 / 50」（Total concurrent jobs / Maximum concurrent macOS jobs）、「The maximum concurrent macOS jobs is shared across standard GitHub-hosted runners and GitHub-hosted larger runners」 | F5 |
| C3 | 新しい head を push しても旧 head の run が走り続ける（`test.yaml`、`remote.yaml`、`agent-assets.yml` に `concurrency` なし。`docs.yml` だけ設定済み） | 枠を無駄に使う | `concurrency: group: <workflow>-${{ github.event.pull_request.number \|\| github.ref }}`、`cancel-in-progress: true` | Actions docs:「To also cancel any currently running job or workflow in the same concurrency group, specify `cancel-in-progress: true`」「at most one running job or workflow in a concurrency group at any time」 | F5 |
| C4 | `private-bootstrap`（必須でない）が PR ごとに ubuntu 2 + macOS 1 で走る | 必須でないジョブが枠を食う | `on.pull_request` から外し `push`（main）と `schedule` のみ | — | F5 |
| C5 | `public-bootstrap`（必須、ubuntu 2 + macOS 1）が設定ファイルに触れない PR でも走る | 必須チェックなので path filter で skip すると「Waiting for status to be reported」で merge が塞がる | 既存の decide step（`.orchestration` のみの差分は skip）を広げ、bootstrap 関連パスに触れない PR では後続 step を `if:` で飛ばし job は success | GitHub docs（required status checks の troubleshooting）: path filter で skip された必須チェックは「stay in a "Pending" state and block merging」、「Avoid requiring workflows that can be skipped」 | F5 |
| C6 | `test` が約 9 分（3 OS） | bats と unit test が直列か未確認 | `bats --jobs` と unit の並列 runner を item 0 で確認してから導入 | — | F5（条件付き） |
| C7 | merge queue が使えない | 個人リポジトリ | ローカル直列マージ + main の push CI（D1 の代替）。org 移管は保留 | Plan 022 の決定（merge queue は組織リポジトリ向け） | D1 |
| C8 | GitGuardian と `validate` は緑（問題なし） | — | 維持 | — | — |

### A-M その他（機械、ネットワーク、バス、記録、費用、人）

| # | 現象 | 問題・課題 | 本質対処 | 公式根拠 | 位置 |
| --- | --- | --- | --- | --- | --- |
| M1 | Mac の蓋閉じスリープで 4 回中断 | — | 済（`disablesleep 1`、#394 の doctor チェック） | — | 済 |
| M2 | push が SSH に書き換えられ失敗 | git config の `pushInsteadOf` | #400 に HTTPS 化と validator が入っている | — | D3 |
| M3 | live 設定が手作業適用で main と不一致、chezmoi ソースが main 以外 | 再現性の喪失 | #400 マージ → `make update` → `chezmoi verify` を boundary の確認項目に | — | 5.3、DoD2 |
| M4 | 未コミット記録 57 → boundary PR が遅れる | 記録の塊が大きくなる | boundary を半日ごと、記録 PR は gate なし（plan 020 step 3） | — | 5.4 |
| M5 | agmsg のマシン間同期が mktemp 失敗（spark 連携不可） | agmsg の sync 設計 | hcom relay に置換。私設ブローカー + SSH 転送 | hcom SECURITY.md:「Relay payloads are end-to-end encrypted. Brokers do not see data」「shared PSK with XChaCha20-Poly1305」「The PSK cannot be revoked」「Use a private/custom/self-hosted broker with `--broker` and `--password`」 | D11、X(6) |
| M6 | Claude Code セッション費用 $745、omp では Anthropic が API 従量 | 費用の見えなさ | boundary ごとに omp history.db から当日使用量を記録、600k handoff、上限はユーザー | omp docs/session.md（history.db） | D9、B stage 2 |
| M7 | 報告が人に把握できる形でない | — | boundary 記録の 2 部定型 + project-map → H6/H7 | — | 5.7、H6、H7 |
| M8 | 人の承認が工程に残る | 自律環境の欠陥 | 残すのは ruleset の管理者操作、OAuth ログイン、API キー、relay 接続、権限拡張の承認だけ | — | 3-6、各 PR の「ユーザー」欄 |
| M9 | Grok Bot の残置物（settings.json バックアップ、`~/.local/state/grokbot/*`） | 環境のノイズ | ユーザー判断で削除。席は触らない | — | 5.3 |

結論: 初版の plan は B1〜B14 の主題別分類と plan 内の位置しか持たず、役割別の分類、CI の具体手段（concurrency、private-bootstrap の除外、in-job skip、macOS 同時 5 の制約）、公式根拠の引用を欠いていた。本付録と F5 でそれを補った。未確認のまま残るのは C6（テストの並列化）と、omp hook の導入版での実測（B stage 2 item 0）。

