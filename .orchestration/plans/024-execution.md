# Plan 024 実行手引き（実行中の orchestrator が読むもの）: 並列と直列、順序の根拠、`make update` の時機、第 1 段階と第 2 段階の重ね方、本日の時刻表とトリップワイヤ、ユーザーの操作

> 読む時機: 波を始めるとき（0d の順序と 0e の重ね方）、`make update` の前（0d の手順）、毎時のトリップワイヤ確認（0c）。plan 本体は `024-omp-cutover-and-corrective-order.md`。

## 0d. 並列と直列の区分、第 1 段階の順序の根拠、`make update` の時機（ユーザー問い 12:0x）

**並列にできるもの / 直列にしかできないもの**

| 並列（席ごと・PR ごとに同時） | 直列（1 本ずつ、または全体を止めて） | 理由 |
| --- | --- | --- |
| 席の実装（allowed_files が互いに素）、CI の run、draft PR の作成、監査（P1-4a 後、同時 2 本）、席側統合（P1-4 後） | main へのマージ（依存順に 1 本ずつ。素でない PR 間は main の push CI 緑を待つ） | main は 1 本の履歴。衝突と意味的衝突の検知は直列でしか確実にならない |
| — | ruleset の 2 トグル（ユーザー、最初に 1 回） | 権限の所在 |
| — | 共有ファイルを触るタスク: `agent-config.yaml` と validator（#400 → P1-7 → P1-14 → B-1 → G-b の順）、`dispatch.sh`（P1-5 → P1-6 → P1-13 → C-1b の順。P1-5 と P1-6 は同じ席 a009）、`herdr-agents`（P1-7 → C-2。P1-5 は `.githooks/*` だけで `herdr-agents` に触らない）、SKILL/rules の文（P1-8 → E2） | 互いに素の規則。同じファイルを 2 席が同時に変えない |
| — | `make update` と席の再着席（全席が波の境目で idle かつ worktree が clean のとき） | 設定と launcher が全席に効く操作。作業中の席を止めない |
| — | orchestrator の受け入れ（verdict 導入まで）と handoff（14:30） | 1 席の操作 |

**第 1 段階の順序とその根拠（先に入れるほど以降の全 PR が速く・確実になるものから）**

| 順 | 項目 | 以降の何を速く・確実にするか | 効く範囲 |
| --- | --- | --- | --- |
| 1 | D1/D2 の 2 トグル、#401（承認 1 回）、glue `SKIP_RESOLVE=1` | マージ凍結の解除。以後の全マージ | 即時、コスト 0 |
| 2 | #390（F1 監査継承） | update-branch だけの head で監査をやり直さない。以後の全 PR の監査回数 | 受理済み、マージのみ |
| 3 | F5 CI（P1-3） | 全 PR の CI 10 分 → 5〜7 分、macOS 待ち 0、旧 run の取り消し。4 席が同時に push しても詰まらない | a011 の最初のタスク（F2 より先） |
| 4 | P1-5 precheck | RESULT 前に席が自分で止めるので revise が減る。仕組み PR 自身（P1-4a 以降）の往復も減る | 強制は段階的（下記） |
| 5 | P1-4a verdict + 監査 pool（shadow） | orchestrator の 1 PR 2〜5 分、監査の並列化。以後の受け入れ全部 | shadow 一致 4 件で `--apply` |
| 6 | #400 の P1 ラウンド（T131-fix）とマージ → `make update` → 再着席 | live 設定と main の一致。HTTPS push、gate の恒久化。以後の `make update` を安全に | 波の境目で 1 回。収まらなければ D3 (d) |
| 7 | P1-6 記録自動生成と `--next`、P1-7 席上限と hooksPath、P1-8 ルール文 | idle の消滅、記録の手書き 0、上限の機械化 | — |
| 8 | P1-12 タスク文生成と plan-check、P1-10 disposition、P1-11 CI regime、P1-13 hold playbook、P1-14 permission guard | 第 2 段階の 14 本以上のタスク文を速く正確に。所見処理と権限変更の機械化 | 第 2 段階の前に |

**precheck の強制は段階的に。** P1-5 のマージ時点では `dispatch.sh` は `precheck=` 欠落を警告のみ（`PRECHECK_REQUIRED=0`）。理由: 進行中の席のブランチには `result-precheck.sh` がまだ無く、即時強制すると全 RESULT が拒否される。切替条件は 1 つ: 4 席すべてのブランチ head について `git merge-base --is-ancestor <P1-5 のマージ commit> <head>` が真になったことを確認してから、1 回だけ `PRECHECK_REQUIRED=1` にし、progress.tsv に時刻を書く（見込み P-W2 の終わり）。verdict の条件 (1) も同じ旗を見る。

**`make update` の時機と、何がそれを必要とするか。** `scripts/`・`.github/`・`.orchestration/`・`.schemas/`・`.githooks/` の変更はマージで即効く（席は `origin/main` から次のブランチを切る）。`home/` の変更（`herdr-agents`、settings、hook、omp 設定）はマージだけでは Mac に効かず、`make update` と席の再着席が要る。第 1 段階では #400 と P1-7（`herdr-agents` と hooksPath）がこれに当たる。手順: P-W2 の終わり（#400 マージ後、約 16:00）に、(0) `~/.claude/settings.json`・`~/.config/git/config`・`~/.local/bin/herdr-agents` を `$TMPDIR/pre-update-<UTC>/` に退避、(1) 全席が RESULT 済みか idle で、各 worktree の `git status --porcelain` が空であることを `team.sh` と `git -C` で確認、(2) `make update`、(3) `chezmoi verify` rc 0、(4) 席を 1 つずつ `--remove-worker` → `--add-worker`（新 launcher と hooks で着席）、(5) `herdr agent list` で 4 席の起動引数と、各 worktree の `git config core.hooksPath` を確認、(6) progress.tsv に記録、(7) 失敗時は (0) の退避を戻し、席は `--add-worker` をやり直す。D1/D2 を戻すときは同じトグル。第 2 段階では B-1 マージ後（omp 設定）と C-2 マージ後（hcom 着席）に同じ手順をもう 2 回、spark では X(6) で 1 回。

## 0e. 第 1 段階と第 2 段階の重ね方（並列にできる箇所と、その条件。ユーザー問い 12:1x）

**原則。** 第 2 段階の「準備」（実装、draft PR、CI、監査依頼）は第 1 段階の空き枠で並列に進めてよい。第 2 段階の「live の運用を変えるマージ」（C-1b の配線、C-2 の hcom 着席、切替 X、撤去 E）は DoD-P1 の後。重ねるときの 4 条件: (1) 第 1 段階のタスクが無い席の空き枠だけを使う、(2) 第 1 段階のファイルと素（`dispatch.sh`、`agent-config.yaml`、validator、workflows、SKILL/rules、`herdr-agents` に触らない）、(3) マージ枠は 1 波に第 2 段階 1 本まで、しかもその波の第 1 段階マージが終わってから、(4) CI 枠を食うので F5 のマージ後に push する（それまでは実装のみ）。

| 第 2 段階の項目 | 第 1 段階と重ねられるか | 理由と条件 | 空き枠（条件） |
| --- | --- | --- | --- |
| B-1 omp 設定生成の ready（rebase、report、PR、監査） | **可**（準備 15 分、マージは条件 3） | 実装済み。validator を触るので #400 → P1-7 → P1-14 の後にマージ | P-W2 で a009 が P1-5/P1-6 の revise を持たないとき |
| B-2 omp hooks（`home/dot_omp/agent/hooks/pre/*.ts`、item 0 の実測） | **可**（実装と draft） | 第 1 段階のファイルと素。omp は導入済み。`home/` なので 16:00 の `make update` に同乗でき、Claude 席には無害 | P-W4 で a010 が P1-14 の RESULT 後、または a009 が P1-4 の revise を持たないとき |
| C-1a 新規スクリプト（`bus-history.sh`、`hcom-dispatch`、そのテスト） | **可**（新規ファイルのみ） | 配線（C-1b）は P1-13 の後。新規ファイルだけなら素 | P-W4 で a008 が P1-12/P1-10 の revise を持たないとき |
| C-1b 配線（`bus: agmsg|hcom` の seam）、C-2 hcom 着席と移植 | 不可 | `dispatch.sh`、`herdr-agents`、counters が P1-5/P1-6/P1-7/P1-13 と重なる。live の運用を変える | DoD-P1 後 |
| D #404 実行時 probe の ready | **可** | `scripts/check-tools.sh` とテストのみ。#405 とは別ファイル | P-W2 で a009 の revise が無いとき（B-1 の後） |
| G-a pstack の vendor 準備（`vendor/pstack/*`、THIRD-PARTY-NOTICES、allowlist テスト） | **可** | manifest と updater に触らない部分。G-b（`assets.pstack`、`update-agent-assets.sh`）は validator 系列の後 | P-W4 で a010 の P1-14 RESULT 後 |
| H6 watch-pr（gh のみ） | **可** | omp にも hcom にも依存しない | P-W4 で a011 が P1-13 の revise を持たないとき |
| H1 show-me-your-work、H7 session-report | **可**（fixture 実装まで） | omp の session JSONL と history.db の形は docs で既知。実データでの確認は B-1 後 | P-W4 以降で、上の項目がすべて着手済みのとき |
| H3 interrogate/reflect（hcom 経由 review）、H4 architect/swarm、spark、X、E1〜E3 | 不可 | C-2 か X が前提 | 第 2 段階 |

**効果。** DoD-P1 の時点で B-1・B-2・C-1a・#404・G-a・H6 が ready なら、第 2 段階の壁時計 18〜24 時間は 12〜18 時間に縮む（B+C の 4〜6 時間の大半と G/H の 1 波が前倒し）。第 1 段階の完了時刻は変えない（条件 1〜4）。

## 0c. 本日 2026-10-18 の時刻表（11:30〜18:00 JST。ユーザー指示 11:1x「18 時までに全部を問題なく完了」への回答）

**結論（AI エージェント基準の見積もり、plan 第 8 節のモデル）: 第 1 段階は 11:30 開始で 18:00〜20:00 に完了しうる。第 2 段階は壁時計で 18〜24 時間かかるので、18:00 までに「全部」は終わらない。** 見積もりの根拠は人日ではなく、1 PR の臨界路（実装 15〜60 分 + precheck 10 分 + CI 10 分 + 監査 15 分 + 判定とマージ 5 分 = 1〜1.5 時間、revise 1 回なら +1 時間）と、並列の天井（CI 3〜5 PR 同時、監査 2 本同時、席 4）。人の待ちはあなたの 2 トグルと #401 の承認 1 回だけ。品質ゲートを外せば本数は増えるが「問題なく」に反するので提案しない。DoD-P1 の計測窓は 24 時間ではなく「連続 2 波」に改め、24 時間の統計は第 2 段階の間に監視として集める。

| 時刻 | orchestrator / ユーザー | a009（Claude） | a008（Claude） | a010（Codex） | a011（Claude） |
| --- | --- | --- | --- | --- | --- |
| 11:30〜12:15 | ユーザー: ruleset の 2 トグル（D1/D2）、#401 の承認 1 回。orchestrator: タスク文 4 本（P1-5、P1-4a、F5、T131-fix）を書いて dispatch、#401 を承認後に merge、glue `SKIP_RESOLVE=1` | B stage 1 を draft で push（15 分）→ P1-5 precheck 着手 | C stage 1 を draft で push → P1-4a（verdict.sh、audit-pool.sh、schema）着手 | T131-fix: #400 のレビュー所見 8 P1 / 8 P2（review.md）の disposition メモ（1 時間）→ P1 修正着手。同一クラス 3 件で S1 → D3 (d) | #405 と #402 を ready → F5 CI（P1-3、0d の順序 3。F2 より先） |
| 12:15〜13:30 | 直列マージ #390 → #389 → #378 → #375 → #398 → #405 → #402（accepted head の gate 確認、各 10〜15 分。#396 は #389 の後に a010 が ready）。5.2 の close | P1-5 実装 | P1-4a 実装 | #400 修正 | F5 実装（concurrency、private-bootstrap を PR から外す、in-job skip、threat_table） |
| 13:30〜15:00 | 受け入れと監査（manual `orch-audit.sh`、1 本 15 分）: P1-5、F5。14:30 boundary 23 → handoff → 再起動（20 分） | P1-5 RESULT → revise 対応 | P1-4a 実装 | #400 push → CI → 監査依頼 | F5 RESULT → F2 #387 の CI 赤と 6 スレッド（1 ラウンド） |
| 15:00〜16:30 | マージ: P1-5、F5。受け入れと監査: #387、#400（8 P1 の disposition を 1 件ずつ確認） | P1-6（記録自動生成、`--next`）着手 | P1-4a RESULT → revise 対応 | #400 revise 対応 → P1-7 席上限と hooksPath | F2 RESULT → revise 対応 |
| 16:30〜18:00 | マージ: #387、P1-4a、#400（1 ラウンドで収まったとき）→ 0d の手順で `make update` → `chezmoi verify` → 再着席。収まらなければ D3 (d): #400 を閉じ、live hook は手作業適用のまま、`make update` は走らせず、最小 gate の作り直しを P1-14 と同じ Codex タスクに積む（期限 10/19 12:00） | P1-6 実装続き | P1-4 integrate-seat の設計メモ（#393 の 8 P1 の disposition） | P1-7 RESULT → P1-8 着手 | F2 マージ待ち → P1-13 の `classes.yaml` と `hold-playbook.sh`（`dispatch.sh` の変更は P1-6 マージ後） |

**18:00 時点の到達目標（確認できるもの）**: (1) バックログ 11 本（うち受理済み 9 本）の merge / close が完了し main の push CI が緑、(2) P1-5（precheck）、F5（CI）、P1-4a（verdict と監査 pool）、#387（lint）がマージ済み、(3) #400 がマージ済みで `chezmoi verify` 一致、または D3 (d) に分岐済み、(4) P1-7 が RESULT 済み、P1-6 が実装中、(5) 4 席が同時に互いに素なタスクで稼働した初回の記録（P1-h の計測開始）、(6) boundary 23 の記録 PR とこの時刻表の実績欄。

**18:00 に到達しないもの（理由）**: P1-4 integrate-seat の実装完了（#393 の 8 P1 を設計で潰してから作るため、設計メモは 17:00、実装 RESULT は 19:00〜20:00 の見込み）、P1-6 のマージ（17:30 以降の RESULT、マージ 19:00 前後）、P1-10〜P1-14（P-W3/P-W4、19:00 以降）、DoD-P1 の確認（連続 2 波の計測は 20:00 前後に揃う）、第 2 段階の全部（plan 第 8 節: 18〜24 時間）。第 1 段階の完了は 18:00〜22:00 の幅で見る（P-W3/P-W4 を含むため）。

**停滞と品質低下の早期検知（トリップワイヤ。昨夜の「6 時間気づかない」を繰り返さないための規則。1 つでも引っかかったら作業を足さず、原因を 1 行で記録してユーザーに報告する）**

| 時刻 | 進捗の条件（満たさなければ停止して報告） | 品質の条件（満たさなければマージ凍結） |
| --- | --- | --- |
| 12:15 | D1/D2 が反映（`gh api rulesets/24397953` で確認）、#401 マージ済み、タスク文 4 本 dispatch 済み | main の push CI 緑 |
| 13:30 | バックログのマージ ≥ 7、4 席すべてが RESULT 済みか作業中（blocked PONG は 15 分以内に処理）、席の idle > 20 分なし | 各マージが gate（記録 accepted、監査、sweep）を通っている（gate ログ） |
| 15:00 | P1-5 と F5 が受け入れ済み、#400 の CI 緑、P1-4a が実装中 | 仕組み PR の security review verdict が correct。revise 2 回目に入った仕組み PR は hold（追加ラウンド禁止） |
| 17:00 | P1-5 と F5 がマージ済み、P1-4a が RESULT 済み、#400 の判定（マージか D3 (d)）が出ている、P1-7 が実装中 | shadow の不一致 0。main 赤 0 |
| 毎時 | `024-progress.tsv` を実測で更新（PR 番号、head、時刻）。orchestrator の 1 ターン ≤ 20 分（超えたら handoff） | not-applicable 比率 ≤ 30%、監査 P0 の未対処 0 |

**時刻表を崩す要因と手当**: 監査が今日はまだ手動で直列（新規 head 約 8 本 × 15 分 = 2 時間。マージ待ちの間に回す）、4 席が同時に push したときの macOS CI の待ち（F5 が入るまで最大 26 分）、S1 の発動（同一クラス 3 回で止める。止めたら時刻表の次項へ）、classifier の拒否（blocked PONG で可視化、迂回しない）、orchestrator の文脈（14:30 の handoff）。

## ユーザーの操作（時機順。これ以外に人の操作は無い）

| 時機 | 操作 | 根拠 |
| --- | --- | --- |
| 合意直後（11:30） | ruleset 24397953 で「Require branches to be up to date before merging」と「Require conversation resolution」の 2 トグルを OFF | D1、D2。トークンに admin が無い |
| 直後 | #401（記録 PR）の merge を承認 1 回 | live の gh-merge-gate は merge に受け入れ記録と監査を要求し、記録 PR にはどちらも無い（R07）。plan 020 step 3 で記録 PR は gate なし |
| D3 (d) に分岐したとき | 無し（orchestrator が報告するだけ） | — |
| E1 の前 | `~/.claude/settings.json` の管理分削除でよいか 1 行で確認 | 個人用途の Claude Code への影響 |
| B-1 マージと `make update` の後 | omp で `/login openai-codex`（ブラウザで ChatGPT OAuth） | 方向性 2 |
| 同上 | `ANTHROPIC_API_KEY` を自分のシークレット置場から環境へ。`ANTHROPIC_OAUTH_TOKEN` は置かない | 方向性 2、PR D が検査 |
| D9 | 切替後の Anthropic API の 1 日上限額を決める（未設定なら記録のみ） | 費用 |
| X(6) | spark で `hcom relay connect <token>`（SSH 上で入力）と `herdr machine add spark-9e8d` | D11 |
| 任意 | Grok 残置物（settings.json のバックアップ 4 本、`~/.local/state/grokbot/*`）の削除 | 席は触らない |
| 第 1 段階の退出後 | （任意）P1-11 の regime チェックを必須チェックに加える | ruleset の管理者操作 |
