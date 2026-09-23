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
