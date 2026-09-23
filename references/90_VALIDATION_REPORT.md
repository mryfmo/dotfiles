# 検証報告

版 4.0.0（<P9>）。版3.0.0 の PRD・ADR・BDD・UT・CT・ST／E2E・UAT／PT について、敵対的レビュー（01_ADVERSARIAL_REVIEW.md の「v4 での追補」）で見つかった指摘を是正した全体について、何を実行して確かめ、何を確かめていないかを記録する。数値・結果は次回の検証実行（refkit-P9）まで `<P9>` とする。

## 1. 実行した検証と結果

| 検証 | 方法 | 結果 | 証跡 |
|---|---|---|---|
| 文書の全検査 | `python tools/kit_lint.py check` | <P9> | `evidence/kit_lint_check.json` |
| Gherkin の構文 | Cucumber 公式 parser（3章の環境の版）で、記入例の8機能とテンプレートの1機能を解析し pickle に展開 | <P9> | 同上 |
| テンプレートと記入例の一致 | 必須節・節の順序・表の見出し・front matter のキーと語彙を機械照合 | <P9> | 同上 |
| 要件・ルール・ADR の整合 | 版 2.0.0 と同じ検査（EARS、根拠、受入、双方向照合、ADR の語彙と選択肢） | <P9> | 同上 |
| テスト設計書の整合 | 由来のIDの実在、1章の由来が本文で扱われているか、旅程が通るシナリオ・ペルソナの主体の実在、全 NVT がちょうど1つの水準に割当、BDD の全機能が CT か ST に割当、accepted の ADR を由来とするテスト項目の存在、全 GOAL に受入シナリオ、全主体の扱い | <P9> | 同上 |
| 設計書とテストコードの対応 | 設計書の「テスト名」がテストコードに実在するか（Python の関数名一致。06_TEST_STRATEGY.md §5） | <P9> | 同上 |
| **UT の実行** | 参考実装のドメイン規則に対し、pytest＋Hypothesis（状態機械のプロパティを含む） | <P9> | `evidence/example_tests.json` |
| **ミューテーションテスト** | mutmut で `domain.py` に変異を注入 | <P9> | 同上 |
| **CT の実行（BDD の実行を含む）** | BDD 文書から生成した `features/FEAT-004.feature`（`# language: ja`、`ルール`、シナリオアウトライン）を、pytest-bdd で無加工のまま決裁サービスに対して実行。同時実行・障害注入・認可の決定表のテストを追加 | <P9> | 同上 |
| 実行証跡の鮮度と数値 | 証跡に記録した対象コード・テストコード・`.feature` の SHA-256 を現行と照合。設計書に書いた件数・カバレッジ・スコア（現状は `durations` 等の証跡キーへの参照に置換済み。refkit-P7）を証跡と照合 | <P9> | `evidence/kit_lint_check.json` |
| ST 記入例のコード | Playwright の例を `@playwright/test`（3章の環境の版）の型定義で TypeScript の型検査（strict）。k6 の例を `node --check` で構文検査 | <P9>（いずれも実行はしていない） | 証跡ファイルなし（5章の手順で再現） |
| Mermaid の描画 | 公式 npm 配布物の Mermaid（3章の環境の版）を Chromium で実行し、全図を解析・描画。不正な図が拒否されることも確認 | <P9> | `evidence/mermaid_render.json` |
| リンターの変異試験 | 欠陥を1つずつ注入する `selftest`。版 2.0.0 の18種に、テスト設計書関連の欠陥を追加 | <P9> | `evidence/kit_lint_selftest.json` |
| 移植性 | 7種類のテンプレートだけから、別名・別ディレクトリ構成でテストコードの無い最小プロジェクトを作り、`trace`・`extract`・`check` を実行 | <P9> | `evidence/portability_test.json` |

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

検査は最低2つの独立した Python 環境で行う。`gherkin-official` の解決結果がインストール経路で変わるため（`kit_lint.py check`・`trace`・`extract`・`selftest` は `gherkin-official`・`PyYAML` だけを直接インストールし PyPI の最新版が解決される。`run_examples.py` は同じ環境に `pytest-bdd` も入れるため、その依存ピンにより古い `gherkin-official` が解決される場合がある。これは証跡の破損ではなくインストール経路の違いによる。根本原因は refkit-P1 の報告に詳しい）。値は次回の検証実行（refkit-P9）で埋める。

| 項目 | 値 | どの検査で使うか |
|---|---|---|
| Python | <P9> | 共通 |
| gherkin-official（環境A：`kit_lint.py` 単独導入） | <P9> | `kit_lint.py check`・`trace`・`extract`・`selftest` |
| gherkin-official（環境B：`pytest-bdd` 経由の解決） | <P9> | `run_examples.py`（UT・CT の実行） |
| PyYAML | <P9> | `kit_lint.py` 全般（環境A） |
| pytest・Hypothesis・pytest-bdd・coverage.py・mutmut | <P9> | `run_examples.py`（環境B） |
| Node.js・TypeScript・@playwright/test | <P9> | ST 記入例のコードの型検査 |
| Mermaid | <P9> | `render_mermaid.py` |
| ブラウザ | <P9> | `render_mermaid.py`（Chromium） |

## 4. 実施していないこと

| 項目 | 理由・扱い |
|---|---|
| ST／E2E の実行、NVT-001・NVT-003〜NVT-009 の実行 | FlowApprove のシステム全体（画面・永続化・認証・AI 連携）が存在しない。ST_SAMPLE は `last_run: not_run` |
| UAT・PT の実施、ペルソナの根拠となる利用者調査 | 同上。ペルソナは全件「仮説」と明記。受入の判定は「未判定」 |
| 実物の DB に対する CT | 参考実装の保存先はメモリ上のフェイク。トランザクションと同時更新の確認は、フェイクに対してだけ成立している。CT-005（フェイクと実物の契約テスト）は未実装で、CT_SAMPLE 7章に「未達」と明記 |
| 契約テスト（CT-006 ほか）、FEAT-004 以外の BDD の自動化、NVT-011、NVT-002 の決裁以外の分岐 | 未実装。CT_SAMPLE に「未自動化」「未実行」と明記 |
| Playwright・k6・評価基盤・Testcontainers・Pact・Schemathesis などの動作確認 | 版をレジストリで確認しただけ。06_TEST_STRATEGY.md 6章で「実行」と書いたもの以外は動かしていない。JVM の道具は版も確認していない |
| 一次資料の本文の確認 | ISO/IEC/IEEE 29119-3・ISO/IEC 25019 の本文（有償）、SBTM の原文、Google Testing Blog の記事全文は取得していない（ISTQB シラバスは v4 で PDF 本文を取得。02_RESEARCH_AND_DECISIONS.md S16）。公式の概要ページと複数の解説で確認した範囲を 02_RESEARCH_AND_DECISIONS.md に明記 |
| GitHub・GitLab・VS Code などでの表示確認 | 各環境が採用する Mermaid の版と Markdown の方言は環境ごとに異なる |
| 業務責任者による内容の妥当性確認、独立した第三者によるレビュー | 未実施。テスト条件が業務上足りているかは機械検査の対象外 |

## 5. 再現手順

```text
# 環境A：kit_lint.py 単独（gherkin-official は PyPI の最新版が解決される）
pip install gherkin-official PyYAML
python tools/kit_lint.py trace
python tools/kit_lint.py extract
python tools/kit_lint.py check --json evidence/kit_lint_check.json
python tools/kit_lint.py selftest --json evidence/kit_lint_selftest.json
python tools/portability_test.py

# 環境B：参考実装の実行（pytest-bdd の依存ピンにより、環境Aと異なる gherkin-official の版が解決される場合がある。3章）
pip install playwright pytest hypothesis pytest-bdd coverage mutmut
playwright install chromium
python tools/run_examples.py --mutation

npm install mermaid@11.14.0          # 任意のディレクトリで。12.0.0 も同様
python tools/render_mermaid.py --mermaid-dir <node_modules/mermaid のパス>

# ST 記入例のコードの検査（任意）
npm install @playwright/test typescript @types/node
npx tsc --noEmit --strict --target es2022 --module nodenext --moduleResolution nodenext --skipLibCheck <Playwright の例を保存した .ts>
node --check <k6 の例を保存した .mjs>
```
