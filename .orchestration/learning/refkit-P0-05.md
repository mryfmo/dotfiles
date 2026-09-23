# refkit-P0-05: 学びの候補（トリアージ）

## 候補: Ruff の `exclude`/`extend-exclude` はコマンドラインで明示的に渡されたパスには既定で効かない

**観察**: `ruff.toml` に `extend-exclude = ["references"]` を書いても、`uvx ruff format --check references/tools/kit_lint.py`（パスを明示的に指定）は除外されず実際に再整形対象と判定された（ruff 0.16.7 で実測）。`--force-exclude` という CLI フラグが存在し、これは設定ファイル側にも `force-exclude = true` として書ける（`--no-force-exclude` という否定形フラグが存在することから設定可能と推測し、実測で確認した）。これを追加すると明示パスにも除外が強制され、期待どおり動作した。
**一般化できる点**: 「ある PostToolUse フックが特定ディレクトリを常に明示パスで linter/formatter に渡す」という構成を、その linter 側の exclude 設定だけで無効化したい場合、`exclude`/`extend-exclude` に加えて `force-exclude`（または同等の「明示パスにも除外を強制する」設定）が必要か、ツールのドキュメント／実測で確認する。config のキー名を推測せず、`--help` の CLI フラグ一覧（特に否定形フラグの有無）から config 側の対応キーを探すのが早い。
**昇格の判断**: 判定者に一任。ruff を使う他タスクにも直接有用なため、優先度は高いと考える。

## AutoSkill

使用していない。
