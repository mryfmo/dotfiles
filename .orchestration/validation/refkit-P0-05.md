# refkit-P0-05: 検証記録

## 既存 ruff 設定の確認（変更前）

```
absent: pyproject.toml
absent: ruff.toml
absent: .ruff.toml
absent: setup.cfg
absent: .prettierignore
```

他に ruff 設定は存在しなかったため、`ruff.toml` を新規作成した（既存ファイルへの `extend-exclude` 追記は不要だった）。

## ステップ 3: 検証コマンド（verbatim）

### prettier（`.prettierignore` のみで成立）

```
$ npx prettier@2 --check references/00_README.md
npm warn exec The following package was not found and will be installed: prettier@2.8.8
Checking formatting...
All matched files use Prettier code style!
```

exit=0

### ruff format --check（`extend-exclude` のみの状態、修正前・参考として記録）

```
$ uvx ruff format --check references/tools/kit_lint.py
unformatted: File would be reformatted
    --> references/tools/kit_lint.py:18:1
     |
17   | """
18   +
19   | from __future__ import annotations
...
(以下省略。ファイル全体が再整形対象と判定された)
```

これは task_file の期待（除外される）に反した。原因と対応は report ファイル参照。`ruff.toml` に `force-exclude = true` を追加。

### ruff format --check（`force-exclude = true` 追加後、最終状態）

```
$ uvx ruff format --check references/tools/kit_lint.py
warning: No Python files found under the given path(s)
```

exit=0

### ruff check --fix（フックの 2 番目のコマンドと同一の呼び出し）

```
$ uvx ruff check --fix references/tools/kit_lint.py
warning: No Python files found under the given path(s)
All checks passed!
```

exit=0

### 変更が加わっていないことの確認

```
$ git status --short -- references/
(出力なし)
```

## ステップ 4: make ターゲット（verbatim、末尾）

### make validate-agent-assets

```
uv run --with pyyaml scripts/validate-agent-assets.py
Installed 1 package in 2ms
agent asset validation ok
```

### make unit-test

```
uv run python -m unittest discover -s tests/unit -v
...
----------------------------------------------------------------------
Ran 392 tests in 28.838s

OK (skipped=1)
```

`grep -rln ruff tests/ scripts/` は 0 件 — ruff 設定の発見に依存するテストは存在しない。root の `ruff.toml` 追加によるテスト結果への影響は無し。

## git show --stat HEAD（コミット後、verbatim）

```
commit 849a7706c2f90e318149f0c42fcc1318c67e334b
Author: Fumio Moriya <moriya.fumio@technopro.com>
Date:   Wed Sep 23 19:29:57 2026 +0900

    chore(references): exclude the documentation kit from prettier and ruff formatting
    
    Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

 .orchestration/autoskill/runs/refkit-P0-05.md |   3 +
 .orchestration/learning/refkit-P0-05.md       |  11 +++
 .orchestration/reports/refkit-P0-05.md        |  43 +++++++++++
 .orchestration/sandboxes/refkit-P0-05.md      |   3 +
 .orchestration/validation/refkit-P0-05.md     | 103 ++++++++++++++++++++++++++
 .prettierignore                               |   3 +
 ruff.toml                                     |   4 +
 7 files changed, 170 insertions(+)
```

## contextdb memory add

```
[memory:decision] references/ excluded from prettier/ruff via root .prettierignore and ruff.toml. Note: ruff needs force-exclude = true in addition to extend-exclude, because the format-edited-files.py hook always passes explicit file paths to ruff, and ruff's exclude/extend-exclude do not apply to explicit CLI paths by default (verified on ruff 0.16.7).
```

memory id: f6282ede-e155-4568-beeb-6b651e0d8535
