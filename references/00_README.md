# PRD・ADR・BDD・テスト 文書キット（版 4.0.0）

確認日：2026-09-19。受領した `PRD_ADR_BDD_Kit_20260919.zip`（版1.0.0）を敵対的にレビューして作り直した版2.0.0に、PRD・ADR・BDD の後に続く4つのテスト水準（UT・CT・ST／E2E・UAT／PT）を加えたもの。形式は UTF-8 の Markdown と Mermaid。特定のベンダー・言語・AI 製品に依存しない。

## 構成

| 分類 | テンプレート | 記入例 | 記載指示書 |
|---|---|---|---|
| PRD | [prd/PRD_TEMPLATE.md](prd/PRD_TEMPLATE.md) | [prd/PRD_SAMPLE.md](prd/PRD_SAMPLE.md) | [prd/PRD_GUIDE.md](prd/PRD_GUIDE.md) |
| ADR | [adr/ADR_TEMPLATE.md](adr/ADR_TEMPLATE.md) | [ADR-0001](adr/ADR-0001-ai-authority-boundary.md)・[ADR-0002](adr/ADR-0002-decision-consistency.md)（superseded）／[ADR-0003](adr/ADR-0003-ai-authority-boundary.md)・[ADR-0004](adr/ADR-0004-decision-consistency.md)（proposed） | [adr/ADR_GUIDE.md](adr/ADR_GUIDE.md) |
| BDD | [bdd/BDD_TEMPLATE.md](bdd/BDD_TEMPLATE.md) | [bdd/BDD_SAMPLE.md](bdd/BDD_SAMPLE.md) | [bdd/BDD_GUIDE.md](bdd/BDD_GUIDE.md) |
| UT（単体テスト） | [ut/UT_TEMPLATE.md](ut/UT_TEMPLATE.md) | [ut/UT_SAMPLE.md](ut/UT_SAMPLE.md)（実行済み） | [ut/UT_GUIDE.md](ut/UT_GUIDE.md) |
| CT（コンポーネントテスト） | [ct/CT_TEMPLATE.md](ct/CT_TEMPLATE.md) | [ct/CT_SAMPLE.md](ct/CT_SAMPLE.md)（一部実行済み） | [ct/CT_GUIDE.md](ct/CT_GUIDE.md) |
| ST／E2E（システムテスト） | [st/ST_TEMPLATE.md](st/ST_TEMPLATE.md) | [st/ST_SAMPLE.md](st/ST_SAMPLE.md)（未実行） | [st/ST_GUIDE.md](st/ST_GUIDE.md) |
| UAT／PT（利用者受入・ペルソナ駆動テスト） | [uat/UAT_TEMPLATE.md](uat/UAT_TEMPLATE.md) | [uat/UAT_SAMPLE.md](uat/UAT_SAMPLE.md)（未実施） | [uat/UAT_GUIDE.md](uat/UAT_GUIDE.md) |

| 共通 | 内容 |
|---|---|
| [01_ADVERSARIAL_REVIEW.md](01_ADVERSARIAL_REVIEW.md) | 元キットへの指摘19件（証拠・根本原因・是正・再発を止める検査） |
| [02_RESEARCH_AND_DECISIONS.md](02_RESEARCH_AND_DECISIONS.md) | 出典（今回確認したものと継承したものを区別）と採用判断 |
| [03_CONVENTIONS.md](03_CONVENTIONS.md) | 正本・ID・関係・状態・ゲート・Markdown と Mermaid の規約 |
| [04_TRACEABILITY.md](04_TRACEABILITY.md) | 追跡表（**自動生成**。手で編集しない） |
| [05_AI_AGENT_INSTRUCTIONS.md](05_AI_AGENT_INSTRUCTIONS.md) | AI エージェントと人への作業指示、レビュー指示、実装への引き継ぎ |
| [06_TEST_STRATEGY.md](06_TEST_STRATEGY.md) | テスト水準の定義（ISTQB との対応）、分担の原則、共通規約、道具の候補と確認した版 |
| [90_VALIDATION_REPORT.md](90_VALIDATION_REPORT.md) | 実際に行った検証と結果、未実施の範囲 |
| `features/` | BDD 記入例から生成した `.feature`（**自動生成**） |
| `examples/flowapprove_core/` | UT・CT の記入例を実際に実行するための最小の参考実装（ドメイン規則と決裁サービス）とテストコード。製品ではない |
| `tools/`・`kit.toml`・`evidence/` | リンター、Mermaid 描画検証、参考実装のテスト実行、移植性試験、設定、検証の証跡 |
| `archive/` | 過去に配布された zip 一式（v1〜v3、および平坦化した配布用 zip）の履歴保存。作業対象ではない（詳細は archive/README.md） |

## 使い方

1. テンプレートを自分のリポジトリにコピーし、`kit.toml` の `[docs]` を自分の文書のパスに書き換える。
2. 記載指示書に沿って記入する。見出しに「（任意）」が付く節は、不要なら節ごと削除する。
3. `python tools/kit_lint.py trace`、`extract`、`check` の順に実行する。依存は `pip install gherkin-official PyYAML`。テスト設計書を使わない場合は、`kit.toml` の `ut`・`ct`・`st`・`uat` の行と `[tests]` を消す。対応する `[templates]` と `[vocab.*]` の該当水準の行も消す。
4. 図を変えたら `python tools/render_mermaid.py --mermaid-dir <npm の mermaid>` を実行する。

## 記入例について

FlowApprove（社内ソフトウェア利用申請とAI審査補助）は架空の題材で、組織・数値・期間・承認はすべて説明用である。UT と CT の記入例だけは、同梱の参考実装に対して実際に実行した結果を書いている（`evidence/example_tests.json`）。ST／E2E と UAT／PT は、対象のシステムが無いため未実行・未実施と明記している。記入例は「利用者が書く値の例」になるよう、正規の状態（draft・accepted など）を書き、架空であることは front matter の `sample: true` で示している。製品全体の実装・試験・実在の承認は存在しない。

## このキットが保証しないこと

リンターの合格は、構造・参照・構文の整合を示すだけである。要件が妥当か、具体例が業務上足りているか、設計判断が正しいかは、人が確かめる。規制のある領域（医療・金融・安全など）では、適用される制度の要求を別に定める必要がある。
