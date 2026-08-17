# PLAN: Pi 転換 — 第 3 エージェント削除と思想・機能の中核吸収

- 作成: 2026-08-17。根拠: `.orchestration/analysis/pi-pivot-decision.md`
  (削除・維持の棚卸しは git 履歴 #133/#134 の実差分から導出済み — 本計画の
  スコープはその 2a/2b/2c/2d 表に厳密に従い、hunk 単位の追加判断は AGMSG で質問)。
- 体制・運用は T45 以降と同一(逐次委譲、5 成果物、敵対的受入、memory add、
  effects 契約、PR 後の CI+bot 全文取得 → 本質対処)。

## フェーズ

| Phase | 内容                                                          | タスク                                            |
| ----- | ------------------------------------------------------------- | ------------------------------------------------- |
| 0     | 決定・計画のドキュメント化(PR)                                | T73-0(orchestrator)                               |
| 1     | ソースツリーの削除+外科的部分処理+`pi`→`cli` 改名             | T74(worker)                                       |
| 2     | ランタイム撤去 chore(mise ペア・配備物・identity・スクラッチ) | T75(orchestrator)                                 |
| 3     | 吸収: send.sh 識別子文法内蔵+ACCEPTANCE コスト欄規約          | T76(worker)                                       |
| 4     | 吸収: context diet 監査(注入文脈のトークン実測と削減提案)     | T77(orchestrator 分析 → 提案のみ。実削減は別裁定) |
| 5     | 最終 PR・CI/bot 本質対処・マージ・zero-tail                   | T78(orchestrator)                                 |

## T74(worker)要点

- 2a の純 Pi ファイルを削除。2b の混在ファイルは表の処置どおり(shdoc 化や
  SQL 安全化など共有資産 hunk は保持)。permgate は機構全維持でプロバイダ名
  `pi`→`cli` 改名(policy 節・テスト・ハッシュ/検証定数を追従。claude/codex
  golden はバイト同一のまま)。
- 削除後の全ゲート緑(format / unit-test / validate-agent-assets / shellcheck)。
  validate の pi-assets カテゴリ削除で総テスト数は減る — 削除されたテストの
  一覧を validation に列挙(黙殺禁止)。

## T75(orchestrator)要点

- mise ピン除去は config+lock ペア一体の独立 chore コミット。`mise uninstall`。
- 配備済み `~/.local/bin` 3 スクリプトと `~/.pi` 管理生成物の除去
  (auth.json 残置)。doctor で残滓ゼロ確認。`leave.sh` で `pi-standard-dot` 退役、
  `identities.sh` で確認。スクラッチ削除は権限で拒否されれば operator へ。

## T76(worker)要点

- send.sh: team/from/to を `^[a-z0-9][a-z0-9_-]{0,63}$` で検証(SQL 安全化に
  加えた入力文法の内蔵 — 旧 pi ツール境界防御の一般化)。既存呼び出し互換
  (現行の全 identity が適合することを確認してから固定)。
- agmsg-orchestration ルール/SKILL に ACCEPTANCE のコスト概算欄(worker 報告
  トークン等があれば記載、なければ n/a)を 1 項目追加。

## T77(orchestrator)要点

- 常時注入文脈(rules 10 本・CLAUDE.md 連鎖・スニペット)のトークン実測表を作成し
  削減候補を提案(実施は別裁定)。Databricks 知見の自前適用であり、計測なき削減は
  しない。

## オールグリーン・完了条件

T61/T72 と同一のゲート群(bats は CI)+「`grep -ri pi` 系の残存参照ゼロ確認
(文書の歴史的記述は除外)」+zero-tail+ACCEPTANCE/decision 統合。

## Phase 6(追補・operator 裁定 2026-08-17): 吸収プログラム本実行

T77 監査の提案を実施に移す(operator の再指示「pi の思想や機能を活かして
組み入れる方針に転換」を実施承認と解する)。

| タスク | 内容 |
|---|---|
| T79 | **agmsg-orchestration ルールの二層化**(progressive disclosure): 常時ルールを「体制起動トリガー+絶対不変条件+スキル参照」~300 tok に縮約し、詳細プロトコル全文を agmsg-orchestration スキルへ一本化(情報の削除は禁止 — 移設のみ。移設前後の全条項対応表を validation に必須) |
| T80 | **codex AGENTS.md の同型二層化**(2,773 tok): スキル/別文書へ移設可能節の特定と実施(同じく対応表必須) |
| T81 | **ワーカーのコスト報告**: RESULT 契約に「セッションのトークン/コスト実測が参照可能な場合は報告する」を追記(T76 のコスト欄の給源) |
| T82 | 効果再実測(トークン表の before/after)+最終 PR・CI/bot 本質対処・マージ |

見送り(理由付き): ドメイン rules(gpu/latex/python 計 ~750 tok)のスキル化は
絶対量が小さく優先度低。destructive ツールの cli ゲート経由化は既存 3 重ガードが
十分で YAGNI。セッションツリー/steer 等は CC/Codex 側に受け口がなく不可搬。

## 実装中の裁定記録

(開始後追記)
