# tools/ について

`kit_lint.py`・`portability_test.py`・`render_mermaid.py`・`run_examples.py` は、この
ドキュメントキット（PRD／ADR／BDD／UT・CT・ST・UAT）を検査・生成・検証するための道具である。
いずれも `kit.toml` を設定として読む。個別のツールの詳しい挙動はソース冒頭の docstring を見ること。

## 前提条件

- **Python 3.11 以上。** `tomllib`（TOML パーサ）が標準ライブラリに加わったのが 3.11 のため
  （[Python 3.11 what's new — tomllib](https://docs.python.org/3/library/tomllib.html)）。
  3.10 以下で `kit_lint.py` を実行すると、インポートを試みる前に一行メッセージを出して
  終了コード 2 で終わる。
- 必須の外部依存：`gherkin-official`・`PyYAML`（`kit_lint.py` が使う）。
- 任意の外部依存：
  - `render_mermaid.py` の実行には `playwright`（`python -m playwright install chromium`
    で Chromium も別途取得する）と、npm の `mermaid`（`npm install mermaid@<version>`）。
  - `run_examples.py` の実行には `pytest`・`hypothesis`・`pytest-bdd`・`coverage`・`mutmut`。

## 実行方法

システムの Python に直接 `pip install` せず、`uv` 経由で実行することを推奨する：

```bash
cd references
uv run --python 3.12 --with gherkin-official --with PyYAML python tools/kit_lint.py check
```

`render_mermaid.py`・`run_examples.py` を使う場合は、別途 `uv venv` で作った専用の venv に
`uv pip install --python <venv>` で依存を入れ、その venv の Python から実行する
（システム全体にインストールしない）。

## サブコマンドとエラー

| コマンド   | すること                                                                                                                                                      | 主なエラー                                                                                                                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `check`    | 全検査。終了コード 0=合格／1=不合格                                                                                                                           | 文書構造・ID・相互参照（E0xx〜E1xx 系）に加え、追跡表・`.feature`・Mermaid・テスト実行証跡が正本と一致しているか（E120〜E124、E100〜E103、E140〜E158 など）                                         |
| `trace`    | 追跡表（`04_TRACEABILITY.md` 等）を再生成して書き出す                                                                                                         | —                                                                                                                                                                                                   |
| `extract`  | `gherkin_source: markdown` の BDD 文書について、Markdown 内 Gherkin フェンスから `features/*.feature` を生成する（生成物には marker 行を付ける）              | `gherkin_source: feature` の文書には書き込まない（**E123**、`mirror` の実行を案内）。`features/` にマーカーのない `.feature` が残っている場合は削除せず **E122** を報告する                         |
| `mirror`   | `gherkin_source: feature` の BDD 文書について、`features/*.feature` の内容（marker 行を除く）で Markdown のフェンスを書き戻す。それ以外の記述は一切変更しない | 対象の `.feature` が存在しない場合 E121                                                                                                                                                             |
| `selftest` | リンター自身に既知の欠陥を注入し、対応するエラーが検出されるかを確認する変異試験                                                                              | 注入した正規表現がドキュメント中にちょうど 1 箇所しか一致しない場合のみ有効な試験とみなす。0 箇所なら `FIXTURE_MISSING`、2 箇所以上なら `FIXTURE_AMBIGUOUS`（いずれも selftest 全体を不合格にする） |

`check`・`extract`・`mirror` はいずれも `Lint` クラスの同じ検査ロジックを通るため、`check` を
単独で実行しても `gherkin_source` の不整合（**E124**：`markdown`／`feature` 以外の値）や
`.feature` とフェンスの不一致（**E121**）は検出できる。

## ID とプレフィックス（`[ids] prefix`）

ID の正規表現は、決まった種別の一覧（`FR｜NFR｜GOAL｜KPI｜GRD｜EVID｜ACT｜RISK｜NVT｜ADR｜FEAT｜RULE｜SCN｜Q｜UT｜CT｜E2E｜UAT｜PT｜PER`）
から組み立てる。`SHA-256`・`APP-001`・`SPEC-001` のような、たまたま「英字＋ハイフン＋数字」に
見える文字列は種別に無いので ID として誤検出しない。複数の製品を同じ場所で管理するときは
`kit.toml` の `[ids] prefix`（例：`PAY-`）で全 ID に接頭辞を要求できる。接頭辞を設定して
いないのに `PAY-FR-001` のように書いても、その ID は認識されず（`FR-001` として書いた場合と
違って）他所からの参照が軒並み「存在しない」扱いになるので、無視されて見過ごされることはない。

## 複数の PRD

`kit.toml` の `[docs] prd` は 1 件以上の PRD を指定できる。FR・NFR・GOAL・KPI・GRD・NVT の
ID は全 PRD をまたいで重複できない（重複は **E030**）。`trace` が生成する追跡表は、PRD が
2 件以上あるときだけ機能要件・非機能要件の節を PRD ごとに分ける（1 件のときは今までどおり）。

## 実行証跡が必須になる条件（E155）

`last_run` が `passed`／`failed` の文書は、`evidence` に実在するファイルへのパスを書かな
ければならない（BDD を含む全文書種別。前提として `evidence` キー自体が front matter に無い
場合も不合格にする）。

## 「実行結果」表と E158

UT・CT・ST・UAT のテンプレートは、証跡と数値で照合する専用の表を持つ：

```
| 項目 | 値 | 証跡のキー |
|---|---|---|
| UT件数 | 125 | ut.total |
```

「証跡のキー」は証跡 JSON（`evidence/example_tests.json` 等）内の値を指す。`<水準>.total` は
その水準のテスト件数、`<水準>.passed` は合格数、`<水準>.branch_coverage_percent` は真の
分岐カバレッジ、`<水準>.line_and_branch_percent` は行＋分岐の合成値（下記「`run_examples.py`
の証跡フィールド」参照）、`mutation.total`／`mutation.killed`／`mutation.score_percent` は
ミューテーション試験の対象数・検出数・スコアを指す。`check` はこの表だけを見る。文章中に
同じ数値が書いてあっても見ない。

文書自身の水準（`doc_type`）が証跡に存在するのに、その行の「証跡のキー」が解決できない場合
（誤記・存在しない節）は **E159** で不合格にする。キーを空欄にしてよいのは、文書自身の水準が
証跡に無い場合だけ（ST／UAT の `not_run` のように、そもそも証跡が無い水準）。

## `gherkin_source` の 2 モード

BDD 文書の front matter `gherkin_source` は、その文書中の Gherkin フェンスと対応する
`features/*.feature` の、どちらが正本かを宣言する：

- **`markdown`**（既定）：Markdown のフェンスが正本。`.feature` は `extract` の生成物。
  手で `.feature` を直接編集してはならない（`check` が **E121** で不合格にする）。
- **`feature`**：チームが Cucumber 系の実行ツールを導入し、`.feature` を直接編集するように
  なった後の状態。`.feature` が正本。Markdown 側のフェンスは `mirror` の生成物であり、
  Markdown を直接編集してはならない（`check` が **E121** で不合格にする）。`extract` はこの
  モードの文書には書き込まず、**E123** を報告して `mirror` の実行を案内する。

両方を手で直す運用（Markdown と `.feature` を独立に編集する）は、どちらのモードでもしない。

## marker 行

`extract` が生成する `.feature` ファイルは、1 行目の `# language: ...` の直後に、次の形式の
marker 行を付ける：

```
# generated-by: kit_lint extract — do not edit; source: bdd/BDD_SAMPLE.md
```

`check`・`mirror` はこの marker 行を除いて内容を比較する。そのため、marker 行の有無自体は
不一致の原因にならない（v3 でまだ marker のない既存の `.feature` も、フェンスの内容さえ
一致していれば `check` に合格する）。`features/` に marker のない `.feature` が
どのフェンスにも対応しない状態で残っている場合は、手で置いたものとみなして削除せず
**E122** を報告する。

## `selftest` の網羅性

`selftest` はリンター自身のソースを `self.err(`／`self.warn(` で正規表現走査し、実際に発行
され得る全 E／W コードの一覧を作る。変異の一覧（`MUTATIONS`）がこの一覧を1つでも欠くと
`selftest` 自体を不合格にする（`uncovered_codes` に列挙する）。変異は、この記入例に固有の
文章ではなく、テンプレートの見出し・表・front matter キー・Gherkin のタグのような**構造**で
対象を探す（例：`FR-001` という ID や `@SCN-001` というタグは規約上どの記入例にも存在する
契約なので対象にしてよいが、記入例だけの日本語文は対象にしない）。

## Mermaid（`render_mermaid.py`・`check_mermaid`）

`tools/mermaid_common.py` は両者が共有する、stdlib のみに依存する小さなモジュール
（`kit_lint.py` の `gherkin-official`／`PyYAML`、`render_mermaid.py` の `playwright` を
互いに引き込まないため）。フェンス抽出（`iter_fences`／`mermaid_blocks`）は
CommonMark のフェンスコードブロック定義に従う：列0から3文字までのインデント、
3個以上の ``` か ~~~（4個以上のバッククォートも同様）。対象文書集合
（`document_paths`）は `kit.toml` の `[docs]` にある全グロブの和集合（テンプレート・
PRD・ADR・BDD・UT/CT/ST/UAT・other・追跡表）で、`Lint.run()` が `all_docs` を組み立てる
手順と同じ順序・同じ重複排除規則を再現する。`kit.toml` の `[docs]` を変更したときは、
`tools/mermaid_common.py` の `document_paths()` も見直すこと（唯一の重複源）。

図の種類は `kit.toml` の `[mermaid] allowed_types`（既定 `flowchart`・`sequenceDiagram`・
`stateDiagram-v2`）に限り、フェンス本文の先頭の非空行・非ディレクティブ行（`%%` で
始まる行を除く）から取り出したキーワードで判定する。それ以外（`graph`・
`stateDiagram`（v1）・`classDiagram` 等）は **E104**。

`render_mermaid.py` は既定で Chromium のサンドボックスを有効のまま起動する
（Playwright 公式の既定）。動かない環境向けに `--allow-no-sandbox` を渡すと
`--no-sandbox` を付けて起動し、その旨を証跡の `no_sandbox` に記録する。

## `run_examples.py` の証跡フィールド

`coverage.py` は「行のみ」と「行＋分岐」を別の値として持つ（公式ドキュメント・
ソースの定義）。`percent_covered` は実行された行数＋分岐数の合計を、行数＋分岐数の
合計で割った値（行と分岐を合成した％）、`covered_branches`／`num_branches` の比が
真の分岐カバレッジ。旧版は前者を `branch_coverage_percent` と誤って呼んでいた
（表示名の誤り。E-13）。現在は：

- `branch_coverage_percent`：`covered_branches / num_branches * 100`（真の分岐カバレッジ。
  分岐が1つも無ければ 100.0）。
- `line_and_branch_percent`：`percent_covered`（行＋分岐の合成値。旧版の
  `branch_coverage_percent` はこの値だった）。

各テストケースの `duration_s` は pytest の JUnit XML（`--junitxml`）の `testcase` 要素
自身が持つ `time` 属性から転記する（setup／teardown を含む合計時間。pytest の既定
挙動）。`tools` には `pytest`・`hypothesis`・`pytest-bdd`・`coverage`・`mutmut` の各
バージョンを記録する。

ミューテーション対象（`mutation.target`）と対象テスト（`mutation.tests`）は
`examples/flowapprove_core/pyproject.toml` の `[tool.mutmut]` から読む
（`source_paths`／`pytest_add_cli_args_test_selection`。mutmut 3 系の現行キーで、
mutmut 2 系の `paths_to_mutate`／`tests_dir` はもう存在しない）。`mutmut run` の
タイムアウト（既定 1800 秒）を捕捉すると、証跡全体の `status` は `passed`／`failed`
ではなく `timeout` になる。`--out PATH` で証跡の出力先を変更できる（既定は `kit.toml`
の `[tests] evidence`）。

## `portability_test.py`

実物の `kit.toml` をコピーし、パスに関わる値だけを書き換える（`[vocab.*]`・`[ids]`・
`[adr]`・`[gherkin]`（`max_unique_step_ratio` 等の閾値を含む）・`[evidence]` はそのまま）。
そのため、記入例に固有の甘さで検査が通っているのではなく、実物と同じ閾値・語彙・ID規則で
全テンプレートを埋めたときに `check` が通ることを確かめる。`[tests]` 用に最小のテストコード
（`test_name` という関数1つ）も生成し、E152 まで実際に検査させる。`render_mermaid.py` は
`references/.mermaid/11/node_modules/mermaid` が無い場合、または実行している Python から
`playwright` を import できない場合はスキップし、その理由を結果の `mermaid` キーに記録する
（スキップも含めてどの分岐でも終了コードは 0）。
