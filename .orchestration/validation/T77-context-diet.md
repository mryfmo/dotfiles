# T77: Context diet 監査(提案のみ — 実削減は別裁定)

- 実施: 2026-08-17、オーケストレータ直轄(PLAN-pi-pivot Phase 4)
- 方法: 常時/高頻度注入ファイルの文字数実測+混合言語トークン推定
  (和文 1.7 字/tok・欧文 4 字/tok の粗い経験則。±20% 程度の誤差前提の
  序列比較用であり、絶対値の精密さは主張しない)

## 実測(降順)

|               推定 tok | ファイル                                                 | 注入面                              |
| ---------------------: | -------------------------------------------------------- | ----------------------------------- |
|                  2,773 | home/dot_config/codex/AGENTS.md                          | Codex 全セッション                  |
|                  2,172 | rules/agmsg-orchestration.md                             | Claude 全セッション・全プロジェクト |
|                    586 | rules/crit-review.md                                     | Claude 全セッション                 |
|                    565 | AGENTS.md(repo)                                          | 両者(CLAUDE.md @参照/Codex 連鎖)    |
|                    506 | rules/model-selection.md                                 | Claude 全セッション                 |
|                    418 | rules/understand-anything.md                             | Claude 全セッション                 |
|                    374 | CLAUDE.md(contextdb スニペット込み)                      | Claude(本 repo)                     |
| 349/272/202/167/127/68 | gpu/python/compactiondb/ponytail/latex/ask-user-question | Claude 全セッション                 |

**面別合計(概算)**: Claude ≈ 5,800 tok/セッション(rules 4,867+CLAUDE/AGENTS)、
Codex ≈ 3,300 tok/セッション。

## 分析

Pi の実証(固定部 <1k tok、Databricks でハーネス差が同品質のままコストを 2 倍超
動かす)を自前に適用すると、最大の的は **agmsg-orchestration.md(2,172 tok)** で
ある。この規約は「体制が非アクティブなプロジェクトの全 Claude セッション」にも
常時注入されているが、詳細プロトコル(並列規約・identity 規約・store 規約・
teardown 手順)は体制起動時にしか要らない。同内容は agmsg-orchestration スキル
(オンデマンドロード=progressive disclosure)と重複しつつある。

## 提案(実施は operator 裁定)

1. **agmsg-orchestration.md の二層化**: 常時ルールは「起動トリガー+スキル参照+
   絶対不変条件 3〜4 行」(~300 tok)へ縮約し、詳細プロトコル全文はスキル側へ
   一本化。削減 ~1,850 tok/セッション。情報は消えず、載る場所が変わるだけ。
2. **codex AGENTS.md の同型監査**(2,773 tok): スキル移設可能節の特定(別途)。
3. ドメイン条件付き rules(gpu/latex/python 計 ~750 tok)は「1 行トリガー+
   スキル化」で ~600 tok 削減可能だが、優先度は低い(絶対量が小さい)。
4. 見送り: crit-review/model-selection/compactiondb は毎セッションの判断に直結
   するため常時注入を維持。

**期待効果**: 提案 1 のみで Claude セッション固定部の約 32% 減。全採用で
~40–45% 減。probe(T49)でリカバリ品質の非劣化を検証してから確定する。
