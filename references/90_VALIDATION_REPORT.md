# 検証報告

版 3.0.0（2026-09-19）。版 2.0.0 の PRD・ADR・BDD に、UT・CT・ST／E2E・UAT／PT を加えた全体について、何を実行して確かめ、何を確かめていないかを記録する。

## 1. 実行した検証と結果

| 検証 | 方法 | 結果 | 証跡 |
|---|---|---|---|
| 文書の全検査 | `python tools/kit_lint.py check` | 合格（エラー0・警告0）。文書 30、FR 28・NFR 9・ルール 23・シナリオ 41（展開後 68 ケース）・ADR 2・図 20。テスト項目は UT 18・CT 6・旅程 5・受入シナリオ 7・探索セッション 4、ペルソナ 6 | `evidence/kit_lint_check.json` |
| Gherkin の構文 | Cucumber 公式 parser（gherkin-official 42.0.1）で、記入例の8機能とテンプレートの1機能を解析し pickle に展開 | すべて成功 | 同上 |
| テンプレートと記入例の一致 | 必須節・節の順序・表の見出し・front matter のキーと語彙を機械照合 | PRD・ADR 2件・BDD・UT・CT・ST・UAT とも一致 | 同上 |
| 要件・ルール・ADR の整合 | 版 2.0.0 と同じ検査（EARS、根拠、受入、双方向照合、ADR の語彙と選択肢） | 適合 | 同上 |
| テスト設計書の整合 | 由来のIDの実在、1章の由来が本文で扱われているか、旅程が通るシナリオ・ペルソナの主体の実在、全 NVT がちょうど1つの水準に割当、BDD の全機能が CT か ST に割当、accepted の ADR を由来とするテスト項目の存在、全 GOAL に受入シナリオ、全主体の扱い | 適合。NVT は CT に3件・ST に8件 | 同上 |
| 設計書とテストコードの対応 | 設計書の「テスト名」22件が、テストコードに実在するか | すべて実在 | 同上 |
| **UT の実行** | 参考実装のドメイン規則に対し、pytest＋Hypothesis（状態機械のプロパティを含む） | 125件すべて合格。`domain.py` の分岐カバレッジ 100% | `evidence/example_tests.json` |
| **ミューテーションテスト** | mutmut で `domain.py` に68件の変異を注入 | 67件を検出（98.5%）。生き残り1件は例外メッセージの文言で、仕様でないため受容。**初回は5件が生き残り、弱いテスト2種を見つけて是正した**（UT_SAMPLE 6章） | 同上 |
| **CT の実行（BDD の実行を含む）** | BDD 文書から生成した `features/FEAT-004.feature`（`# language: ja`、`ルール`、シナリオアウトライン）を、pytest-bdd で無加工のまま決裁サービスに対して実行。同時実行・障害注入・認可の決定表のテストを追加 | 29件すべて合格（BDD 16ケース＋固有13ケース）。`service.py` の分岐カバレッジ 94.4% | 同上 |
| 実行証跡の鮮度と数値 | 証跡に記録した対象コード・テストコード・`.feature` の SHA-256 を現行と照合。設計書に書いた件数・カバレッジ・スコアを証跡と照合 | 一致。**この照合で、CT_SAMPLE のカバレッジの記載が再実行後の値とずれていたのを検出して直した** | `evidence/kit_lint_check.json` |
| ST 記入例のコード | Playwright の例を `@playwright/test` 1.63.0 の型定義で TypeScript の型検査（strict）。k6 の例を `node --check` で構文検査 | どちらも合格。**実行はしていない** | 証跡ファイルなし（5章の手順で再現） |
| Mermaid の描画 | 公式 npm 配布物の Mermaid 11.14.0 と 12.0.0 を Chromium で実行し、全20図を解析・描画。不正な図が拒否されることも確認 | 両方の版で 20/20 成功。全図に代替テキストあり | `evidence/mermaid_render.json` |
| リンターの変異試験 | 30種類の欠陥を1つずつ注入。版 2.0.0 の18種に、NVT の二重割当、存在しない由来、コードに無いテスト名、古い実行証跡、受入シナリオの無い目的、未割当の機能、front matter の語彙外、証跡の無い合格、存在しない主体とシナリオ、本文に出てこない由来、証跡と食い違う結果の12種を追加 | 30件とも検出 | `evidence/kit_lint_selftest.json` |
| 移植性 | 7種類のテンプレートだけから、別名・別ディレクトリ構成でテストコードの無い最小プロジェクトを作り、`trace`・`extract`・`check` を実行 | 合格（Mermaid 証跡が無い旨の警告のみ） | `evidence/portability_test.json` |

## 2. 作成物に対する敵対的レビューで見つけ、直したもの

| 見つけた問題 | 原因 | 是正 |
|---|---|---|
| 提出前（DRAFT）・差戻し中（RETURNED）の申請への決裁要求の扱いが、PRD のどこにも無かった | 版 2.0.0 の FR-020 は終端状態だけを対象にしていた。UT で状態×出来事の全36通りを書いて初めて空白が見えた | PRD 0.4.0 で FR-020 を「SUBMITTED 以外」に一般化。BDD 0.4.0 で RULE-017 と SCN-031 に DRAFT・RETURNED の例を追加 |
| 拒否理由の優先順位（FR-028）に自己決裁が無かった | 版 2.0.0 で優先順位を足したとき、4条件しか検討していなかった。UT で決定表の全32通りを書いて発覚 | FR-028 を5条件の順序に改訂 |
| 分岐カバレッジ100%のテストが、実装の誤りを5種類見逃していた | `valid_url` 単体は確かめていたが `violations` がそれを呼ぶことを確かめていなかった。情報分類のテストが項目名を確かめていなかった | UT-008 を追加、UT-009 を強化。指示書に「カバレッジは実行を示すだけ」の実例として記載 |
| pytest-bdd が Gherkin のタグを未登録の pytest マーカーに変換し、警告が出て、IDでテストを選べなかった | 道具の既定の振る舞い | `conftest.py` でタグを `req` マーカーに写し、`--req <ID>` での選択と、JUnit XML へのIDの書き出しを実装。`--strict-markers` で再発を検出 |
| UAT と PRD のゲートがつながっていなかった（G3 に利用者受入が無い） | 版 2.0.0 は UAT を範囲外にしていた | PRD のテンプレートと記入例の G3 に UAT の受入判定を追加 |
| テスト戦略のゲート表が、PRD のゲート条件と別の条件を定義していた（正本が2つ） | 戦略文書を独立に書いた | 「正本は PRD 9章」と明記し、各ゲートで使われる水準の対応表に変更 |
| ST 記入例の1章の由来に挙げた FEAT と NFR の大半が、本文のどこでも扱われていなかった | 由来を「関係しそうなもの」で書いた | 由来を実際に扱うIDだけに直し、この種の漏れを検出する検査（E157、範囲記法の展開つき）をリンターに追加 |
| 探索セッション（PT）にだけ由来が無く、共通規約「すべてのテスト項目に由来」と矛盾していた | チャーターを台本でないものとして別扱いした | PT の表に由来の列を追加（リスク・ガードレール・要件） |
| BDD 文書の `last_run: not_run` が、FEAT-004 を実行した事実と合わなくなった | 実行の状態を BDD 文書に持たせる設計と、水準ごとの設計書の追加が衝突 | 語彙に `partial` を追加し、`last_run` を「自動化済みの範囲の最新結果」と定義。証跡の場所は実行した水準の設計書に書く。`passed` と書いて証跡が無い文書は不合格（E155） |
| 移植性試験が、指示書のコピー漏れと 03→06 のリンクで失敗した | 試験の準備が版 2.0.0 の3種類のままだった | 7種類のテンプレートと指示書、06 を準備に追加 |
| 参考実装とテストコードに、1行に複数の文、副作用のための内包表記があった | 短く書こうとした | 通常の書き方に直して再実行 |

## 3. 環境

| 項目 | 値 |
|---|---|
| Python | 3.12.3 |
| gherkin-official・PyYAML | 42.0.1、6.0.3 |
| pytest・Hypothesis・pytest-bdd・coverage.py・mutmut | 9.1.1、6.168.0、8.1.0、7.16.1、3.8.0 |
| Node.js・TypeScript・@playwright/test | 22.22.2、7.0.2、1.63.0（型検査のみ） |
| Mermaid | 11.14.0、12.0.0。いずれも npm の公式配布物 `dist/mermaid.min.js` |
| ブラウザ | Playwright 同梱の Chromium（版は `evidence/mermaid_render.json` に記録） |

## 4. 実施していないこと

| 項目 | 理由・扱い |
|---|---|
| ST／E2E の実行、NVT-001・NVT-003〜NVT-009 の実行 | FlowApprove のシステム全体（画面・永続化・認証・AI 連携）が存在しない。ST_SAMPLE は `last_run: not_run` |
| UAT・PT の実施、ペルソナの根拠となる利用者調査 | 同上。ペルソナは全件「仮説」と明記。受入の判定は「未判定」 |
| 実物の DB に対する CT | 参考実装の保存先はメモリ上のフェイク。トランザクションと同時更新の確認は、フェイクに対してだけ成立している。CT-005（フェイクと実物の契約テスト）は未実装で、CT_SAMPLE 7章に「未達」と明記 |
| 契約テスト（CT-006 ほか）、FEAT-004 以外の BDD の自動化、NVT-011、NVT-002 の決裁以外の分岐 | 未実装。CT_SAMPLE に「未自動化」「未実行」と明記 |
| Playwright・k6・評価基盤・Testcontainers・Pact・Schemathesis などの動作確認 | 版をレジストリで確認しただけ。06_TEST_STRATEGY.md 6章で「実行」と書いたもの以外は動かしていない。JVM の道具は版も確認していない |
| 一次資料の本文の確認 | ISTQB シラバスの PDF、ISO/IEC/IEEE 29119-3・ISO/IEC 25019 の本文（有償）、SBTM の原文、Google Testing Blog の記事全文は取得していない。公式の概要ページと複数の解説で確認した範囲を 02_RESEARCH_AND_DECISIONS.md に明記 |
| GitHub・GitLab・VS Code などでの表示確認 | 各環境が採用する Mermaid の版と Markdown の方言は環境ごとに異なる |
| 業務責任者による内容の妥当性確認、独立した第三者によるレビュー | 未実施。テスト条件が業務上足りているかは機械検査の対象外 |

## 5. 再現手順

```text
pip install gherkin-official PyYAML playwright pytest hypothesis pytest-bdd coverage mutmut
playwright install chromium
npm install mermaid@11.14.0          # 任意のディレクトリで。12.0.0 も同様
python tools/kit_lint.py trace
python tools/kit_lint.py extract
python tools/render_mermaid.py --mermaid-dir <node_modules/mermaid のパス>
python tools/run_examples.py --mutation
python tools/kit_lint.py check --json evidence/kit_lint_check.json
python tools/kit_lint.py selftest --json evidence/kit_lint_selftest.json
python tools/portability_test.py

# ST 記入例のコードの検査（任意）
npm install @playwright/test typescript @types/node
npx tsc --noEmit --strict --target es2022 --module nodenext --moduleResolution nodenext --skipLibCheck <Playwright の例を保存した .ts>
node --check <k6 の例を保存した .mjs>
```
