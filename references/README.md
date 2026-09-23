# references/ について

このディレクトリは、PRD／ADR／BDD／UT／CT／ST／UAT のドキュメントキット（PRD_ADR_BDD_TEST
系列）の正本ツリーです。**正本は v3.0.0 を取り込んだこのツリー本体**であり、現在バージョン
**4.0.0** への是正作業を進めている途中版です（v3.0.0 をベースラインに、判明した不整合や
未実装機能を段階的に修正していきます）。

`archive/` は過去に配布された zip 一式（v2 kit、v3 kit、およびそれぞれを平坦化した配布用 zip）
の**履歴保存**であり、作業対象ではありません。詳細は `archive/README.md` を参照してください。

## チェックの実行方法

- `00_README.md` にキット自体の使い方（`kit.toml` の編集、`tools/kit_lint.py` の実行手順など）
  が書かれています。まずそちらを読んでください。
- 検査・生成ツールは `tools/` にあります（`kit_lint.py`、`portability_test.py`、
  `render_mermaid.py`、`run_examples.py`）。いずれも `tomllib`（標準ライブラリ、Python 3.11 以降）
  と PEP 723 のインラインスクリプトメタデータを使うため、**Python 3.11 以上が必須**です
  （`00_README.md` 自体は `gherkin-official`／`PyYAML` にしか触れていないため、この Python
  バージョン要件は個別に憶えておく必要があります）。
- 依存パッケージの追加はシステム Python に `pip install` せず、`uv run --with ...` や
  `uv venv` ＋ `uv pip install --python <venv>` のように `uv` 経由で行ってください。

## 完全性の検証

`references/` 直下の `SHA256SUMS.txt` は、この正本ツリー（キット本体）に対する完全性アンカー
です。`cd references && sha256sum -c SHA256SUMS.txt` で全ファイルが取り込み時点から改変されて
いないことを確認できます。`archive/SHA256SUMS.txt` は zip 配布物 4 点だけを対象にした別の
アンカーです。
