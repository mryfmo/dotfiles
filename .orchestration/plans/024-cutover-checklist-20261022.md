# Plan 024 切替チェックリスト（2026-10-22T08:58Z、D-024-87 の critical path を 1 枚にしたもの）

> 目的: ゴール（DoD3: 全席が `hcom omp` で起動、orchestrator も omp、agmsg を読まない。DoD11: hcom 越しに TASK→RESULT→ACCEPTANCE→merge が通る。E: agmsg と Claude/Codex 専用物の撤去）に対して「先に何が要るか」を全部ここに書く。以後の追加・変更はこの表の行の更新として記録し、後出しにしない。
> 根拠: `024-design-prs.md` 第 4 節 B/C/X/E、`024-omp-cutover-and-corrective-order.md` 第 6 節 D-W0/D-W1、`b2-c2-facts.md`（omp 18.11.3 / hcom 0.7.30 の公式記述、2026-10-22T08:0xZ）。

## 1. 作業の順序と状態

| # | 項目 | 依存 | 状態（2026-10-22T08:58Z） | 残り |
| --- | --- | --- | --- | --- |
| 0 | 審査が回る前提: codex を使う入口 3 本を sandbox 外で実行（J-N2） | なし | 操作者待ち | `excludedCommands` 3 行 |
| 1a | B-1 omp 設定生成（`dotfiles-T129-omp-config-render-a01`、a009） | なし | 本文 anchor 済（efc8c79b）。C-80 待ち（J-N2） | C-80 → dispatch → 実装（draft #406 継続）→ CI → local review/監査 → merge → `make update` |
| 1b | C-1 hcom dispatch bus（`dotfiles-T129-hcom-dispatch-bus-a02`、a008） | なし（gh-binding 依存は waiver 済） | 実装中（item 0 済、質問 5 件回答済） | RESULT → amendment 3（SQL 補間の脅威行、test 集合の文、`<checkout>` の語）→ 審査 → merge → `make update`（private hcom 導入） |
| 2a | B-2 omp 席の方針（`dotfiles-T129-omp-seat-policy-a01`、a009） | B-1 merge | 本文 round 2 審査中（a7180714）。C-80 待ち | anchor 完了 → C-80 → B-1 merge 後 dispatch → 実装 → 審査 → merge → `make update` |
| 2b | C-2 hcom で omp 席を着席（`dotfiles-T129-hcom-omp-seat-a01`） | C-1 merge（private hcom）、B-1/B-2 は名前で消費 | round 1 reject 3 件（返信先の定義、omp_args の制御、private hcom の使用）。amendment 1 を書く | amendment 1 → anchor → C-80 → dispatch（C-1 完了後の Claude 席）→ 実装 → 審査 → merge |
| 2d | 席の OS レベル隔離（J-X1 = A、D-024-92、2026-10-22T09:31Z）: worker/orchestrator/監査役の席プロセスを `@anthropic-ai/sandbox-runtime`（Claude Code の sandbox と同じエンジン）で包み、役割別設定を manifest から生成 | C-2 anchor 後 | 事実確認済（2026-10-22T09:54Z、srt-facts.md）: CLI と JSON 設定の形を確認、TTY は stdio 継承で可、hcom への差し込みは PATH 上の `omp` shim（hcom は解決した絶対パスを runner に固定、wrapper 設定キーは無い）、omp の書込先は `~/.omp/agent/**`・`~/.omp/run`・`~/.hcom` と loopback bind、監査席の read-only は allowWrite の限定で表現可。注意: srt は Beta Research Preview（npm 0.0.81、2026-10-20）で未導入、macOS の入れ子は未文書、Linux の入れ子は weakening が要る | C-2 amendment（wrapper 起動）、X-2 は omp 監査席を read-only で、X-1 は orchestrator も wrapper 下 |
| 2c | B-2 に畳む不足分: omp skills root への `skills.links` 行、generator の `WORKER_KINDS` に omp、`omp.model` の `:<level>`（役割ごとの effort、xhigh 指示） | B-2 anchor 後 | 未着手（本 checklist で確定） | B-2 amendment 2（本文 1 回の改訂で 3 点） |
| 3a | X-1 orchestrator 席を hcom omp で起動する本文（launch 形、orchestrator 方針 overlay、handoff、受信は hcom 配送、stop gate は `session_stop` hook + C-1 の bus-history） | B-2、C-1、C-2 | 未作成 | 本文作成 → anchor → C-80 → 実装 → 審査 → merge |
| 3b | X-2 監査役を omp で実行（`orch-audit.sh` の omp 版: audit profile = openai-codex/gpt-6-astra、read-only 方針 overlay） | B-2 | 未作成。E で codex が消える前に必須 | 本文作成 → 審査 → 実装 → merge |
| 3c | X 切替（手順は design-prs X(1)〜(5)） | 1a〜3b の merge | 未着手 | `make update` → login/環境変数 → パイロット 1 席 → 残り 3 席 → orchestrator 再起動（handoff から） |
| 4 | E1〜E3 撤去（Claude/Codex 描画と hooks、agmsg skill と rules、残り） | X 完了 | 未着手 | 3 PR 直列 |
| 経路外 | #456 gh-binding（J-L）、installer a02（hold）、G pstack、D 認証検査、H1〜H9、spark | — | hold / 待機 | X 後、または操作者の指示で |

各 PR に共通の審査: anchor（a011、数分）→ C-80（security: true の本文、codex）→ worker 実装 → CI（必須 9 本、約 10〜30 分）→ sweep → local review（codex）→ task-level audit（codex）→ gate → `--match-head-commit` merge。codex の 3 ステップはすべて J-N2 に依存。

## 2. 操作者にしかできないこと（全部）

| いつ | 何を | なぜ人間だけか |
| --- | --- | --- |
| 今 | J-N2: `.claude/settings.local.json` の `sandbox` に `excludedCommands` 3 行 | 自席の sandbox 設定は規程上も権限上も私が触れない |
| 今（任意） | J-L: #456 の A/B/C | INV-6 の閾値超過の免除は操作者の決定 |
| 今 | J10: ホストをスリープさせない | 電源管理 |
| B-1/C-1/B-2 の merge 後、各 1 回 | `make update`（omp を閉じた状態で。`~/.omp/agent/config.yml` と `policies/`、private hcom を配置） | 配置は利用者権限の apply |
| X の直前 | `omp login openai-codex`（OAuth）、`ANTHROPIC_API_KEY` を環境へ（`ANTHROPIC_OAUTH_TOKEN` は置かない）、D9 の費用上限 | 認証と課金 |
| X | パイロット 1 席の置換を承認、残り 3 席、orchestrator 再起動の pane 起動 | 席の生成・終了は操作者の端末操作 |
| X 後（spark） | `hcom relay connect <token>`（SSH 上で） | 秘密の入力 |

## 3. パイロット（X）で実測するまで未知のもの（b2-c2-facts.md の gaps）

1. `session_stop`/`turn_end` が print/rpc と hcom 配送下で発火するか。2. `tool_call` の bash 入力キー（docs は例のみ）。3. `ctx.getContextUsage()` の初回値と各モデルの `contextWindow`（gpt-6.1-sol は 500k/922k、fable-5-1 は未記載）。4. hcom の omp 通知サーバ（127.0.0.1:0）が sandbox 起動元から立つか。5. `hcom config omp_args` の既定（DB を開くコマンドは Claude sandbox では失敗）。6. `hcom list --json` が pid/launch_args を返すか。7. `.claude/hooks/*.ts` を omp が読むか。8. Post-Invoke hook と Error-Mode の挙動は installer 側（別件）。

## 4. 主なリスク

omp の権限・hook 層の実測前（B-2 と X-1 で閉じる）。Anthropic API 従量（D9）。herdr 0.9.5 との互換（`--kind omp` は help にある）。hcom 0.7.31 の存在（pin は 0.7.30、読む source も 0.7.30）。

## 5. 計画の弱点と判断（2026-10-22T09:03Z、操作者の「この計画で問題ないのか」への回答）

| 判断 | 内容 | 既定案 |
| --- | --- | --- |
| J-X1 worker の封じ込め | 決定: A（D-024-92）。OS レベル隔離を新体制の要件にする | sandbox-runtime で席を包む。C-2/X-1/X-2 に反映 |
| J-X2 監査役の read-only | A の帰結として omp 監査席を sandbox-runtime の read-only で動かす（OS 強制、codex 不要、入れ子なし）。事実確認で不可なら codex CLI を残す案に戻す | 事実確認待ち |
| 範囲の固定（2026-10-22T09:26Z、D-024-91） | 弱点 J-X1/J-X2 は既定で確定し、新しい隔離基盤の調査・設計は行わない（調査コンテキストは停止）。X のパイロットで実測した事実だけが X-1/X-2 本文に入る | 既定どおり |
| 順序の確認 | X-1（orchestrator の omp 化）は最大の未知 | C-2 merge 直後に worker 1 席で小タスクを通し、第 3 節の未知を実測してから X-1 本文を確定する |

## 6. plan 025 の後に検討（2026-10-22T11:55Z、操作者の提案）

| 項目 | 内容 | 時期 |
| --- | --- | --- |
| ハーネス工学の適用 | 引き継ぎ書を START-HERE（読む順）／STATUS（今の状態・終わりの条件・次の一手、区切りごとに書き換え）／CHECKPOINT（経過の追記）の 3 本に一本化し、読むのは主担当 1 体だけ。サブエージェントには仕事に要る分だけの指示書と返り値の形を渡し、冒頭に「基準コミットを確かめ、違えば止まる」を置いて読了を行動で確かめる。終わりの条件は始める前に書き、後から変えない。試験は回帰／現在の限界として固定（golden）／正解が割れる例（変化数のみ）に分け、検査器（regime-ci、pre-send、matcher）にはミューテーションテストで賢さを測る。既存の CompactionDB・M/C 記録・受入記録との統合先を決める | X と E の後、記録の棚卸しと同時 |
| 参照する配置（操作者提供の図、2026-10-22T11:55Z） | リポジトリ側は `CLAUDE.local.md` 1 行（「作業の前と compaction の後は START-HERE.md を読む」）。引き継ぎ書ディレクトリ（主担当だけが読む）: `START-HERE.md`（入口、読む順）、`STATUS.md`（今の状態・終わりの条件・次の一手、区切りごとに上書き）、`CHECKPOINT.md`（経過の追記）、`USER-DECISIONS.md`（人の決断）、`GOALS-<version>.md`（目標と合格条件）、`understand/`（サブエージェントの返り値を主担当が保存）。作業置き場（コミットしない）に `design/` などサブエージェント向けの指示書（その仕事に要る分だけ）。dotfiles への対応候補: 引き継ぎ書 = `.orchestration/handoff/`、USER-DECISIONS = `decisions.tsv`、GOALS = DoD、understand = `.orchestration/validation/`、作業置き場 = `.agents/worklog/` | 同上 |
| 状態遷移図と形式検証（操作者の提案、2026-10-22T12:00Z） | エージェントに対象（席のライフサイクル、TASK→RESULT→ACCEPTANCE の契約、merge 経路、stop gate、rollback）のステートチャートを描かせ、pstack の `/create-formal-verification-skill` で TLA+ 相当のモデルを作って不変条件（例: 席は常に 1 つの task を持つか idle、RESULT 無しに merge されない、hold 中に push されない、INV-6 の計数が RESULT 数−1 と一致）を検査する。利点: コードとユーザーフローの理解、利用者が先に踏む不具合の事前発見。前提: G pstack（固定資産化）が済んでいること | X と E の後、G の後 |
| 参照する図の形（操作者提供、2026-10-22T12:01Z） | 利用者から見える流れを 1 枚のステートチャートにし、各状態を「Works／Bug TLA+ found／Fixed」の 3 色で示す（例: メッセージ受信後の表示: 既読扱いになる未読の返信、開いた後の通知、Do Not Disturb 中の通知、復帰後の未読表示の 4 件が TLA+ で見つかり、各修正後の状態を緑で併記）。dotfiles での対象候補: hcom 配送後に席が見るもの（配送・listening・blocked・hold・compaction／handoff の各状態と、RESULT が処理されないまま「読了」になる、blocked なのに listening になる、hold を後から読んで作業を続ける、といった不変条件違反） | 同上 |
