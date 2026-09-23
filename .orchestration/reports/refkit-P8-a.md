# refkit-P8-a: 報告

## 概要

共通文書（00・01 追補・02・05・06・90 骨格）と PRD の 2 セルを是正した。対象：`references/00_README.md`、`references/01_ADVERSARIAL_REVIEW.md`（append-only「v4 での追補」節）、`references/02_RESEARCH_AND_DECISIONS.md`、`references/05_AI_AGENT_INSTRUCTIONS.md`、`references/06_TEST_STRATEGY.md`、`references/90_VALIDATION_REPORT.md`、`references/prd/PRD_GUIDE.md`（3 章の 10 章行）、`references/prd/PRD_SAMPLE.md`（KPI-002 計測手段セルのみ）。`03_CONVENTIONS.md` は指示どおり触れていない（F-01 は P8-b）。

## 実施した変更

### 1. 00_README.md（F-07/F-08、版）

- 版番号を 3.0.0 → 4.0.0 に更新。
- ADR の記入例セルに ADR-0003・ADR-0004（proposed）を追加し、ADR-0001・0002 に（superseded）を付記。
- 共通表に `archive/` の行を追加（過去 zip の履歴保存、作業対象外）。`archive/` の実在をディレクトリ一覧で確認済み。
- 使い方 手順 3 に「対応する `[templates]` と `[vocab.*]` の該当水準の行も消す」を追記（テスト設計書を使わない場合の削除手順の抜けを補完）。
- **`tools/README.md` は追加していない**：task item 6 は構成表への追加を求めるが、このファイルは本枝（`feat/references-kit-v4-p3`）の `references/tools/` に実在しない（`kit_lint.py`・`portability_test.py`・`render_mermaid.py`・`run_examples.py` のみ）。refkit-P2-B が `feat/references-kit-v4` 枝（`dotfiles-w1`）で追加したものが、本枝にはまだ取り込まれていない。存在しないファイルへのリンクを構成表に書くのは「inventing results」に当たるため、追加を見送り、この報告に記載する。

### 2. 01_ADVERSARIAL_REVIEW.md（F-02/F-04、append-only）

本文（1〜5 章、F-01〜F-19）は一切変更せず、末尾に「## 6. v4 での追補」を追記した（`git diff` は追加のみ、149 行、削除 0 行）。

- (a) 第 1 部 91 件の指摘（`ai-references-vivid-sparrow.md`）を A〜G のカテゴリ別表にまとめ、対応する refkit タスクと状態（済／予定）を記載。集計行を付けた。設計判断による不採用の例は、現時点の受入記録に一件も無いことを確認した。
- (b) F-02・F-14 の是正状況を注記。本質的な是正（汎用リンター、`@FR-001` そのまま使用）は当時から成立しているが、複数 PRD 対応と `kit.toml [ids] prefix` は refkit-P2-B（`feat/references-kit-v4` 枝）で実装・受入済みであり、**本枝（`feat/references-kit-v4-p3`）の `tools/kit_lint.py`・`kit.toml` には未だ存在しない**ことを、`grep` で直接確認して明記した（`[ids]`・`prefix`・`gherkin_source`・`mirror`・E122・E123・E159 のいずれも本枝のコードに無い）。

### 3. 02_RESEARCH_AND_DECISIONS.md（F-05/E-02）

- §1 の凡例を「今回確認／継承」の 2 値から「取得して確認／概要のみ／継承」の 3 値に変更。
- S12・S19・S23・S24・S25 を「概要のみ」に再分類（いずれも備考欄が本文未取得・概要のみである旨を既に認めていた）。
- S16 は逆に「取得して確認」へ格上げした：P0-04 の調査で ISTQB CTFL v4.0.1 シラバス本文 PDF を実際に取得・`pdftotext` で確認できたため。この事実を出典セルに追記し、限界欄に「結合テスト」通称との対応が規格に定義が無いことを明記した（refkit-P7 が CT_GUIDE §1 の無出典文を削除した理由と対応）。これにより item 7（CT_GUIDE §1 の S-row 提案）を、未確認の推測行を追加するのではなく、既存 S16 の充実として解決した。
- 残り 20 件（S01〜S11・S13・S17・S18・S20〜S22・S26〜S28）を「取得して確認」に一括変更。
- 「Gherkin の置き場」判断行を、**本枝で実際に動く仕組み**（`extract` による Markdown→`.feature` の一方向生成、E121 で不一致検出）だけを「決定」欄に記述し、`mirror`／E122／E123 を含む双方向対応は refkit-P2-A の設計であって本枝には未反映と明記した。refkit-P2-A の報告書に「02 への反映案」という節は実在しなかった（task item 3 の前提が誤り。下記「逸脱」参照）ため、実装事実から文言を起こした。
- P0-04-sources.md から S30〜S36 を追加（mutmut・coverage.py・Hypothesis・pytest・k6・Playwright・Python tomllib/PEP 723）。いずれも URL と取得日（2026-09-23）付き。ruff の `force-exclude` と prettier の ignore 仕様は、P0-04-sources.md に該当節が無いため追加していない（下記「逸脱」参照）。MADR 4.0.0 は既存 S03 と内容が重複するため新規行を作らなかった。

### 4. 05_AI_AGENT_INSTRUCTIONS.md（F-07）

§2 の役割宣言行を「PRD・ADR・BDD 文書の作成と更新」→「PRD・ADR・BDD とテスト設計書・テストコードの作成と更新」に変更。§1 の表とファイル冒頭の説明文は既にテスト設計書・テストコードを含んでいたため、役割宣言だけが狭かった不整合を解消した。

### 5. 06_TEST_STRATEGY.md（F-04/F-06/F-05）

- §5「テスト名」行を、本枝の実装どおり「Python の関数名との文字列一致のみ。他言語は `[tests] code` に glob を追加すれば対象にできるが、名前抽出規則自体は言語別に設定できない」と明記（P2-B/P2-C はこの検査を言語非依存化していないことを、両タスクのファイル一覧・報告書で確認済み）。
- §5 に「逆方向の検査（予定）」行を新設：Must 要件・NFR にテスト条件・NVT が無い場合の警告（W160）を記述。**現状未実装**（`kit_lint.py` に W160 は存在しない。grep で確認）であることを明記し、実装は refkit-P4b の予定、文書側の理由付けは UT_SAMPLE §1（refkit-P7、FR-005・FR-009・FR-026）と明記した。
- §6 の道具の版を P0-04-sources.md §16（2026-09-23 確認）に合わせて更新（hypothesis・fast-check・Schemathesis・dependency-cruiser・Inspect AI・DeepEval）。日付の無い npm パッケージ（`@playwright/test`・Vitest・dependency-cruiser）は「公開日が確認できない」と注記し、日付を作らなかった。

### 6. 90_VALIDATION_REPORT.md（骨格化）

- 版を 3.0.0 → 4.0.0 に変更。
- §1 実行した検証と結果：全 14 行の「結果」列を、次回の検証実行（refkit-P9）まで埋めない旨のプレースホルダに置換。
- §3 環境：`gherkin-official` が `kit_lint.py check` 単独導入（環境 A、PyPI 最新版が解決）と `run_examples.py` の `pytest-bdd` 経由導入（環境 B、`pytest-bdd` の依存ピンで古い版が解決）で異なる版を報告する理由（refkit-P1 で根本原因を特定済み）を説明文として追加し、どの検査がどちらの環境で走るかを表にした。値自体は P9 まで空欄。
- §4 実施していないこと：ISTQB シラバス PDF は v4（02 の S16）で実際に取得したため、「取得していない」一覧から外した。他の項目（ST/UAT 未実行など）は v4 でも真実のまま変更していない。
- §5 再現手順：§3 の説明と整合するよう、`pip install` を環境 A（`kit_lint.py` 単独）と環境 B（`pytest-bdd` を含む参考実装実行）の 2 ブロックに分割した。

### 7. PRD_SAMPLE.md / PRD_GUIDE.md

- PRD_SAMPLE.md：KPI-002 計測手段セル「FR-003・FR-026」→「FR-026」。FR-026（常時型、提出・審査着手・決裁確定の時刻記録）だけで KPI-002 の分子・分母の時刻が揃う。FR-003 は提出時の表示要件であり、時刻記録そのものを義務付けていないため引用として不要と判断した。
- PRD_GUIDE.md：§3「3 目的と指標」行の良い例に「用語（『内容版』のような）は 10 章の用語集で定義する」を追記（10 章／用語集への言及がこれまで皆無だったため）。

## task_file からの意図的な逸脱（技術的根拠つき）

1. **`tools/README.md` を追加しなかった**：本枝に実在しないファイルへの参照を作ることは「inventing results」に当たるため。
2. **02 の「Gherkin の置き場」記述を、P2-A 報告書の「02 への反映案」からの引用ではなく実装事実から起こした**：該当節は refkit-P2-A の報告書に実在しなかった（`grep` で確認）。task_file 自身が引用元として指定したものが存在しないため、代わりに実装済みの挙動（本枝の `extract`／E121）と、未反映の設計（`mirror`／E122・E123）を正確に書き分けた。
3. **E-01・E-04・E-08〜E-12・E-14・E-15・E-17 を「本枝には未反映」として明記**：91 件マッピングの初期分類ではこれらは「済」（プログラム全体としては refkit-P2-A／P2-B で受入済み）だが、本枝の `tools/kit_lint.py`・`kit.toml` を直接 grep して、該当機能（`gherkin_source`・`mirror`・`[ids]`・`prefix`・E122・E123・E159）が一つも存在しないことを確認した。ドキュメントとコードの不一致を新たに生まないよう、01 の追補表・02 の判断行・06 の§5 ともに「本枝の現状」を優先して記述し、プログラム全体の状態（済）と本枝の状態（未反映）を区別して書いた。
4. **`{{P9}}` ではなく `<P9>` をプレースホルダに使った**：task item 8 の文言は literal `{{P9}}` を指示するが、`kit_lint.py` の E014 が `is_template` でない文書中の `\{\{.*?\}\}` を「未置換のプレースホルダ」としてエラーにする（90_VALIDATION_REPORT.md はテンプレート文書ではない）。E014 は task_file の許容リスト（E120/E121/E103/E153）に無いため、意味を保ったまま `<P9>` に変更した。
5. **ruff `force-exclude`／prettier ignore 仕様の S-row を追加しなかった**：P0-04-sources.md にこれらの URL・取得日が記載された節が存在しない（grep で確認）。task item 4 は「with URL + retrieval date from P0-04」を要求しており、無い情報から URL・日付を作ることは forbidden_actions の「inventing … dates」に当たるため、追加を見送った。
6. **MADR 4.0.0・ISTQB PDF の重複行を作らなかった**：MADR は既存 S03 と内容が重複、ISTQB PDF は既存 S16 の格上げで対応した方が、同じ主題の出典が 2 行に分裂するのを避けられる。

## 下流への波及

- `tools/README.md`、`kit.toml [ids] prefix`、`gherkin_source`／`mirror`、E122・E123・E159、W160 は、いずれも `feat/references-kit-v4`（`dotfiles-w1`）側で実装済み（またはこれから refkit-P4b で実装予定）だが、`feat/references-kit-v4-p3`（本枝）にはまだ取り込まれていない。両枝の統合（マージ）が行われた時点で、01・02・06・00 の該当記述を「済」に更新する後続タスクが必要。
- W160（逆方向検査）の実装は refkit-P4b が担当。実装後、06 §5 の「予定」を「実装済み」に更新する必要がある。
- ruff force-exclude／prettier ignore の一次資料引用は、P0-04-sources.md に該当節が無いため、必要であれば別途ソース調査タスクを起票する必要がある。
- 90_VALIDATION_REPORT.md の全数値（§1・§3）は refkit-P9 が実際の検証を実行して埋める。

## 検証

- `kit_lint.py check`：E120／E121／E103(×2) のみ（task_file の許容リストどおり）。新規エラー 0 件（E014 は `<P9>` への変更で解消）。
- `git diff --stat`：8 ファイル、236 行追加・69 行削除。
- `01_ADVERSARIAL_REVIEW.md` は append-only（追加 149 行・削除 0 行）を `git diff` で確認済み。

## コミット

`docs(references): update sources, strategy, README and validation skeleton for kit v4 (part 1)`

## cost

4 research subagents（並列、読み取り専用）＋ 1 メインセッション。編集は Bash 実行の Python スクリプト 5 回（00/05/PRD、02、06、90、01 追補）＋ プレースホルダ修正 1 回。
