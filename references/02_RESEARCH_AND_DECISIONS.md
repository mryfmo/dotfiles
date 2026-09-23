# 調査結果と採用判断

確認日：2026-09-19。「今回確認」は、この作業の中でページまたは配布物を実際に取得して内容を確かめたもの。「継承」は元キットが挙げていた出典で、今回は再確認していないもの（内容の主張には使わず、参照先としてだけ残す）。

## 1. 出典

| ID | 出典 | 確認 | 採用した点 | 限界 |
|---|---|---|---|---|
| <a id="S01"></a>S01 | Atlassian「Product requirements document」 https://www.atlassian.com/agile/product-management/requirements | 今回確認 | PRD は共有理解のための簡潔な文書。目標・背景・前提・ユーザーストーリー・設計へのリンク・未決の質問・やらないことを1ページ程度にまとめ、チームで更新する | 一企業の実務指針で、規格ではない |
| <a id="S02"></a>S02 | Alistair Mavin「EARS」公式解説 https://alistairmavin.com/ears/ | 今回確認 | 要求文の型：常時、状態（While）、イベント（When）、オプション（Where）、望ましくない振る舞い（If–Then）、およびそれらの複合 | 英語の構文。日本語への写像は本キットの定義 |
| <a id="S03"></a>S03 | MADR 4.0.0（2024-09-17公開）https://adr.github.io/madr/ とテンプレート原文 https://github.com/adr/madr/tree/4.0.0/template | 今回確認（npm でも 4.0.0 が最新） | 節構成（Context and Problem Statement／Decision Drivers／Considered Options／Decision Outcome〔Consequences・Confirmation〕／Pros and Cons of the Options／More Information）と front matter（status・date・decision-makers・consulted・informed） | 必須は背景・選択肢・決定のみ。他は任意 |
| <a id="S04"></a>S04 | Microsoft Azure Well-Architected Framework「Maintain an architecture decision record」 https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record | 今回確認 | ADR は追記専用。受理済みの記録は編集せず、新しい記録で置き換えて相互に結ぶ。確信度と状態を記録する。結果を隠さない。設計手引きにしない | Azure の文脈だが内容は製品非依存 |
| <a id="S05"></a>S05 | Cucumber「Gherkin Reference」 https://cucumber.io/docs/gherkin/reference/ | 今回確認 | Rule は1つの業務ルールを表し、それを例示するシナリオをまとめる（Gherkin 6 以降）。1つの例は3〜5ステップを推奨。説明文は自由記述で、レポートに出る | 実装によって対応状況が異なる |
| <a id="S06"></a>S06 | Cucumber「Anti-patterns」 https://cucumber.io/docs/guides/anti-patterns/ と「Step organization」 https://cucumber.io/docs/gherkin/step-organization/ | 今回確認 | 機能に結合したステップ定義と、複数の事柄を1ステップに詰める書き方は避ける。ステップは領域の概念ごとに整理し再利用する | — |
| <a id="S07"></a>S07 | Cucumber ブログ「Keep your scenarios BRIEF」 https://cucumber.io/blog/bdd/keep-your-scenarios-brief/ | 今回確認 | 業務の言葉・実データ・意図を示す・本質だけ・1つのルールに集中・短く | 2019年の記事。原則は現行の公式文書と整合 |
| <a id="S08"></a>S08 | Cucumber「Markdown with Gherkin」 https://github.com/cucumber/gherkin/blob/main/MARKDOWN_WITH_GHERKIN.md | 今回確認 | `.feature.md` という公式の Markdown 方言が存在する | 対応は JavaScript 実装（@cucumber/gherkin 19 以降）だけ |
| <a id="S09"></a>S09 | Gherkin の変更履歴 https://github.com/cucumber/gherkin/blob/main/CHANGELOG.md と PyPI `gherkin-official` | 今回確認・実行 | 最新は 42.0.1（2026-08-05）。本キットの全 Gherkin を実際に解析した | — |
| <a id="S10"></a>S10 | pytest-bdd 8.1.0 の文書 https://pytest-bdd.readthedocs.io/en/latest/ | 今回確認 | 8.0 から公式 parser を採用し Rule に対応 | 実行ツールは案件で選ぶ |
| <a id="S11"></a>S11 | Mermaid 12.0.0 リリースノート https://github.com/mermaid-js/mermaid/releases | 今回確認・実行 | 2026-09-10公開。既定のレイアウトが ELK になり、既定の見た目も変わる。フローチャート・状態図などは再配置される。旧来の見た目は設定で維持できる | 各ホスト（GitHub 等）が採用する版は別途確認が必要 |
| <a id="S12"></a>S12 | ISO/IEC 25010:2023 https://www.iso.org/standard/78176.html と arc42 による変更点の解説 https://quality.arc42.org/articles/iso-25010-update-2023 | 今回確認（規格本文は有償のため概要と解説のみ） | 製品品質は9特性。安全性が追加され、使用性はインタラクション能力に、移植性は柔軟性に改称 | 日本語の特性名は仮訳 |
| <a id="S13"></a>S13 | Kiro「Specs」 https://kiro.dev/docs/specs/ と GitHub Spec Kit https://github.com/github/spec-kit | 今回確認 | AI を使う仕様駆動開発では、要件（EARS の受入基準）→設計→タスクの順に成果物を分け、段階ごとに人が確認する。Spec Kit は原則（constitution）→仕様→計画→タスク→実装の順 | 特定製品の流儀。本キットは製品に依存しない |
| <a id="S14"></a>S14 | AWS Prescriptive Guidance「Transactional outbox」 https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html | 継承 | ADR-0002 の案Bの性質の説明 | 今回は再確認していない |
| <a id="S15"></a>S15 | 継承した参照先：AWS「ADR process」、Cucumber「BDD」「Example Mapping」、W3C WCAG 2.2、OWASP ASVS、NIST AI RMF、Google SRE Workbook「Implementing SLOs」、RFC 2119／8174、Michael Nygard「Documenting Architecture Decisions」（MADR のページから参照されている原典）、ISO/IEC/IEEE 29148:2018（書誌のみ） | 継承 | 参照先としてのみ | 今回は再確認していない。本キットの判断の根拠には使っていない |
| <a id="S16"></a>S16 | ISTQB「Certified Tester Foundation Level v4.0」 https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/ | 今回確認（公式ページと公開の解説。シラバス本文の PDF は取得していない） | 2023-04-21 公開（4.0.1 は 2024-09-15、内容の変更なし）。テスト水準は、コンポーネント（＝ユニット）・コンポーネント統合・システム・システム統合・受入の5つ。受入の形態は、利用者受入・運用受入・契約と規制・アルファとベータ。テストの種類は水準と直交する | 「コンポーネントテスト」の語が本キットの CT と違うものを指す |
| <a id="S17"></a>S17 | Martin Fowler の用語集「Component Test」 https://martinfowler.com/bliki/ComponentTest.html 、「Broad Stack Test」 https://martinfowler.com/bliki/BroadStackTest.html 、「Unit Test」 https://martinfowler.com/bliki/UnitTest.html 、「Integration Test」 https://martinfowler.com/bliki/IntegrationTest.html 、Toby Clemson「Testing Strategies in a Microservice Architecture」 https://martinfowler.com/articles/microservice-testing/fallback.html | 今回確認 | コンポーネントテストは範囲を意図的に限定したテストで、広い範囲を通すテストとの違いは程度の差。外部は代役にして契約テストで確かめる。広い範囲のテストは保守が難しく遅いので少なくする。単体・統合という語は人によって指すものが違う | 個人の用語の整理であり、規格ではない |
| <a id="S18"></a>S18 | 『Software Engineering at Google』11〜13章 https://abseil.io/resources/swe-book/html/ch11.html | 今回確認 | テストを大きさ（使う資源）と範囲（確かめるコード）の2軸で分ける。small は単一プロセスで入出力なし。できるだけ小さいテストで確かめる。振る舞いを公開の入口から、呼び出しではなく状態で確かめる。時計や外部は代役か、テストが寿命を管理する実物にする | 一企業の実践 |
| <a id="S19"></a>S19 | Google Testing Blog「Code Coverage Best Practices」 https://testing.googleblog.com/2020/08/code-coverage-best-practices.html | 今回確認（検索結果の抜粋と、同記事を引用する複数の解説） | カバレッジに理想の数値は無い。目安は 60%・75%・90%。一律の目標より、変更されるコードが覆われていることと、未実行の箇所を人が判断することが大事。実行と検証は別で、ミューテーションテストが補う | 記事本文の全文は取得していない |
| <a id="S20"></a>S20 | Playwright「Best Practices」 https://playwright.dev/docs/best-practices | 今回確認 | 利用者に見える振る舞いを確かめる、テストを独立させる、第三者の依存を直接テストしない、利用者に見える属性で要素を特定する、条件が満たされるまで待つ検証を使う | 特定の道具の文書だが、指針は道具に依存しない |
| <a id="S21"></a>S21 | Grafana k6「Open and closed models」 https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/ | 今回確認 | 同時接続数を固定するモデルでは、対象が遅くなると要求の到着も減る（coordinated omission）。到着率を固定するオープンモデルは、対象の応答時間と負荷を切り離す | — |
| <a id="S22"></a>S22 | Pact の文書 https://docs.pact.io/ 、「Contract Tests vs Functional Tests」 https://docs.pact.io/consumer/contract_tests_not_functional_tests | 今回確認 | 利用者側のテストが期待を契約として書き出し、提供者側がそれに対して検証する。契約テストは要求と応答の形を確かめ、提供者の業務ロジックや副作用は確かめない | — |
| <a id="S23"></a>S23 | ISO/IEC/IEEE 29119-3:2021「Test documentation」 https://www.iso.org/standard/79429.html | 今回確認（概要と公開されている冒頭部分。本文は有償） | テスト文書は紙でも電子でもよく、道具の記録や表計算でもよい。あらゆる開発の進め方に適用できる | 本文の雛形は確認していない。本キットの雛形は同規格への適合を主張しない |
| <a id="S24"></a>S24 | ISO/IEC 25019:2023「Quality-in-use model」 https://www.iso.org/standard/78177.html | 今回確認（概要と、同規格を用いた論文） | 利用時の品質を、有益さ・リスクからの解放・受容性の3特性で捉える。受入基準の特定に使える | 本文は有償。日本語の特性名は仮訳。有効さ・効率・満足度の定義（ISO 9241-11）は継承 |
| <a id="S25"></a>S25 | Jonathan Bach「Session-Based Test Management」（2000） https://www.satisfice.com/download/session-based-test-management | 今回確認（複数の解説による。原文の PDF は取得していない） | 探索的テストを、チャーター・中断されない時間枠・記録・振り返りで管理する | — |
| <a id="S26"></a>S26 | Lu ほか「UXAgent」（CHI 2025 Extended Abstracts） https://arxiv.org/abs/2504.09407 と、関連研究の一覧を含む「PerceptUI」 https://arxiv.org/html/2606.05697v1 | 今回確認 | ペルソナを与えた LLM エージェントに Web を操作させ、利用者調査を模擬する。著者らは、実際の人を対象にした調査の前に調査の設計を試して直す手段と位置付けている | 研究段階。製品の受入に使える根拠は示されていない |
| <a id="S27"></a>S27 | Nielsen Norman Group「Synthetic Users: If, When, and How to Use AI-Generated Research」 https://www.nngroup.com/articles/synthetic-users/ | 今回確認 | AI が生成した利用者の応答は、迎合的で、実際の人の行動（途中でやめる、使わない）を再現しない。利用者調査には実際の利用者が要る | 調査会社の見解だが、自社の過去の調査との比較に基づく |
| <a id="S28"></a>S28 | PyPI と npm のレジストリ（`pip index versions`・`npm view`） | 今回確認・実行 | 06_TEST_STRATEGY.md 6章の道具の版 | 版の確認であり、動作の確認ではない（実行したものは同表に明記） |
| <a id="S29"></a>S29 | 本キットでの実行：参考実装に対する pytest 9.1.1・Hypothesis 6.168.0・pytest-bdd 8.1.0・coverage.py 7.16.1・mutmut 3.8.0、TypeScript による Playwright 1.63.0 の型検査 | 今回実行 | pytest-bdd が `# language: ja`・`ルール`・シナリオアウトラインを含む `.feature` を無加工で実行できる。分岐カバレッジ100%でも、ミューテーションテストが弱いテストを見つける | 参考実装は最小で、保存先はメモリ上のフェイク |

## 2. 判断

| 論点 | 選択肢 | 決定 | 理由 |
|---|---|---|---|
| PRD の重さ | ①全節必須の詳細版 ②1ページの簡易版 ③必須節＋任意節 | ③ | S01 は簡潔さを勧めるが、権限・品質・検証の欠落は後工程で高くつく。必須11節を短く保ち、状態図・データ・AI・運用の4節は該当時だけ使う |
| 要求文の形式 | ①自由記述 ②ユーザーストーリー＋受入基準 ③EARS | ③（背景の説明にストーリーを併用してよい） | 1文で契機と応答が決まり、機械的に検査でき、BDD の「もし／ならば」に写しやすい。AI に渡す仕様としても広く使われている（S02・S13） |
| 要件と受入の結び方 | ①シナリオに要件タグを付けるだけ ②PRD の受入列とルールIDを双方向に照合 | ② | 片方向のタグは貼り忘れや貼り過ぎを検出できない |
| 非機能要件の書き方 | ①形容詞 ②数値のみ ③品質シナリオ（刺激・環境・合格基準・検証） | ③ | 数値だけでは測り方が決まらない。特性の棚卸しは S12 の9特性で行う |
| ADR の形式 | ①Nygard 形式 ②MADR 4.0.0 ③独自形式 | ②に確信度・再検討のきっかけ・要件IDを追加 | 選択肢の比較を構造として持ち、道具や事例が多い。追加項目は S04 に基づく |
| ADR の変更 | ①本文を更新し続ける ②追記専用 | ② | 判断当時の文脈が残る（S04）。accepted 後に変えてよいのは status と superseded-by だけ |
| Gherkin の置き場 | ①.feature が正本 ②Markdown のフェンスが正本で .feature を生成 ③Markdown with Gherkin | 文書先行の段階は②、実行ツールを導入したら①へ一度だけ移管 | ③は JavaScript 実装だけで可搬性が無い（S08）。どちらの段階でも編集は片方向に限り、リンターが不一致を検出する |
| Gherkin のキーワード言語 | ①英語キーワード＋日本語本文 ②日本語キーワード | ②を既定、①は実行ツールや編集環境の制約があるとき | BDD の目的は業務側との共通理解であり、読み手が日本語話者なら全文が日本語の方が読める。公式 parser で `ルール` を含め有効（S09で実行確認）。1ファイル1言語で `# language:` を必ず書く |
| Rule の粒度 | ①機能ごとに1つ ②業務ルール1つにつき1つ | ② | 公式の定義（S05）と Example Mapping の構造に合う |
| タグの形式 | ①`@req_FR_001` のように変換 ②`@FR-001` | ② | 変換は不要で、IDが1種類になり検索しやすい（公式 parser で確認） |
| 追跡表 | ①手書き ②正本から生成 | ② | 手書きは必ずずれる（元キットで実際にずれていた） |
| Mermaid の検証 | ①特定アプリ同梱のバンドル ②公式 npm 配布物を複数版で | ② | 再現でき、版の違い（S11）も確かめられる。図は flowchart・sequenceDiagram・stateDiagram-v2 に限り、位置に意味を持たせない |
| サンプルの状態表記 | ①status に「例示」と書く ②正規の status＋`sample: true` | ② | サンプルは利用者が書く値の例であるべき |
| テスト文書の位置付け | ①全テストの手順と期待値を書く仕様書 ②設計書（何をなぜどの技法で）＋テストコードが正本 ③文書なし | ②。UAT だけは人が読んで実施するため文書が正本 | 手順と期待値を文書とコードの両方に書くと必ずずれる。S23 は文書の形を問わない。設計書のテスト名がコードに実在することをリンターが検査する |
| 水準の切り方 | ①ISTQB の5水準 ②UT・CT・ST／E2E・UAT／PT の4水準 | ②。ISTQB との対応を表で固定 | 依頼された工程に合わせる。語の食い違い（ISTQB のコンポーネントテスト＝UT）は S16・S17 に基づいて明示 |
| BDD のシナリオを実行する水準 | ①全部を画面経由 ②CT を既定にし、代表的な経路だけ E2E | ② | 業務ルールは画面に依存しない。広い範囲を通すテストは遅く壊れやすい（S17・S18・S20） |
| UT の十分性 | ①カバレッジの数値目標 ②カバレッジで穴を探し、ミューテーションテストで強さを測る | ② | 実行と検証は別（S19）。参考実装で、分岐カバレッジ100%のまま5件の見逃しを確認した（S29） |
| CT での依存の扱い | ①全部を代役 ②所有する依存は実物、他は代役＋契約テスト | ② | 代役は本物との食い違いに気付けない。契約テストは形だけを確かめ、業務ロジックは確かめない（S17・S22） |
| 負荷のモデル | ①同時接続数を固定 ②到着率を固定 | ② | ①は対象が遅くなるほど測定が甘くなる（S21）。PRD の NFR-001 の定義とも一致 |
| UAT の書き方 | ①操作手順と期待結果 ②業務の依頼と成功の判断 | ② | ①は E2E の再実行で、利用者が自力でできるかが分からない。受入は業務の必要を確かめる水準（S16） |
| PT の位置付け | ①自由に触る ②ペルソナの立場での探索を、セッション単位で管理 ③AI エージェントに任せる | ②。③は事前の試行に限る | ①は何を確かめたか残らない（S25）。③は迎合的で実際の行動を再現せず、受入の根拠にならない（S26・S27） |
| 記入例の検証 | ①コード片を載せるだけ ②最小の参考実装を同梱し実際に実行 | UT・CT は②、ST／E2E は型検査と構文検査まで、UAT は未実施と明記 | 実行していないコードは誤りを含み得る。実行の過程で PRD の欠落が2件見つかった |
| テストと要件の追跡 | ①手書きの対応表 ②設計書の由来＋コードの印＋実行証跡のハッシュ | ② | 手書きはずれる。証跡のある合格だけが検証済みの関係を作る |

## 3. 見送ったもの

| 見送ったもの | 理由 |
|---|---|
| 全要件の Gherkin 化 | 負荷・復旧・アクセシビリティ・AI の統計的品質は専用の検証（NVT）の方が適切 |
| 点数表による ADR の比較を必須にすること | 必須の決め手で除外した後は、少数の比較基準の文章で足りることが多い。使う場合の注意は ADR_GUIDE に記載 |
| 承認ワークフローや電子署名の規定 | 組織ごとに異なる。承認は「誰が・いつ・どの版を・どの条件で」を記録する欄だけを定めた |
| 規制領域（医療・金融・安全）向けの拡張 | 適用される制度の要求を専門家と別に定める必要がある |
