# refkit-P0-05: exclude `references/` from prettier/ruff post-write formatters

## 概要

task_id=refkit-P0-05。担当: claude-standard-dot-a002（worker）。依頼元: claude-remediation-dot。目的: `~/.claude/hooks/format-edited-files.py`（グローバル PostToolUse フック）が編集済み `.md`/`.py` に `npx prettier@2 --write` / `uvx ruff format` + `ruff check --fix` を無条件で適用してしまい、`references/` 配下のドキュメンテーションキット（独自の書式規約を持つ）を意図せず全文再整形する問題（refkit-P3 round 1 で実際に発生）を、リポジトリルートの設定ファイルだけで防ぐ。

## 変更

1. `.prettierignore`（新規）: `references/` を除外。
2. `ruff.toml`（新規、他に ruff 設定ファイルが存在しないことを確認済み — `pyproject.toml`・`.ruff.toml`・`setup.cfg` はいずれも root に無い）: `extend-exclude = ["references"]` に加えて **`force-exclude = true` を追加した（task_file の指示にはない 1 行）**。

## task_file の指示からの変更点（重要、要確認）

task_file のステップ 3 は「`uvx ruff format --check references/tools/kit_lint.py` を実行し、除外されること（\"0 files\"）を期待する」としていたが、`extend-exclude` だけでは **この検証コマンドは失敗する**。実測（ruff 0.16.7）:

```
$ uvx ruff format --check references/tools/kit_lint.py   # extend-exclude のみの状態
unformatted: File would be reformatted
    --> references/tools/kit_lint.py:18:1
...
```

原因: Ruff はコマンドラインで明示的に渡されたパスに対しては、デフォルトで `exclude`/`extend-exclude` を適用しない（`--force-exclude` フラグ、または設定ファイルの `force-exclude = true` を指定したときだけ、明示パスにも除外を強制する）。フック（`~/.claude/hooks/format-edited-files.py`）は常に編集対象ファイルのパスを明示的に `ruff format`/`ruff check --fix` の引数として渡す（`command + file_args`）ため、`--force-exclude` 相当の設定が無ければ、`extend-exclude` を書いてもフックは `references/` 配下の `.py` を実際に再整形してしまう。これはこのタスクの目的（フックから守る）を達成できないため、`ruff.toml` に `force-exclude = true` を追加した。追加後、`uvx ruff format --check references/tools/kit_lint.py` は `warning: No Python files found under the given path(s)` を返し、期待どおり除外される（詳細は validation ファイル参照）。

フックそのもの（`~/.claude/hooks/format-edited-files.py`）は禁止事項（`changes-to-home-hooks`）のため編集していない。`force-exclude = true` はリポジトリ側の `ruff.toml` だけで完結する変更であり、この制約に抵触しない。

## 検証

- `npx prettier@2 --check references/00_README.md` → 除外され「All matched files use Prettier code style!」（`.prettierignore` は最初から機能した。ruff と異なり prettier の `--check` は ignore ファイルを明示パスにも適用する）。
- `uvx ruff format --check references/tools/kit_lint.py` → `force-exclude = true` 追加後、除外（`No Python files found under the given path(s)`）。
- `uvx ruff check --fix references/tools/kit_lint.py` （フックの 2 番目のコマンドと同一）→ 同様に除外。
- `make validate-agent-assets` → `agent asset validation ok`。
- `make unit-test` → `Ran 392 tests ... OK (skipped=1)`。ruff を参照するテストはリポジトリ内に存在しない（`grep -rl ruff tests/ scripts/` は 0 件）。

詳細な verbatim 出力は `.orchestration/validation/refkit-P0-05.md` を参照。

## コミット

`chore(references): exclude the documentation kit from prettier and ruff formatting`。push・PR 作成は行っていない。`references/` 配下・`~/.claude/hooks/*`・main への変更は無い。

## cost

cost: n/a
