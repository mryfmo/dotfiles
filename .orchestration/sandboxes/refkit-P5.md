# refkit-P5: サンドボックス状況

ドキュメント（Markdown）の編集に加え、`python tools/kit_lint.py extract` を 1 回実行した（`references/features/*.feature` を一時的に書き換えるが、リポジトリ内のローカル読み取り/生成のみで外部ネットワークアクセスは無い）。実行後、生成された `.feature` の内容を `git checkout --` で元に戻した（本タスクでは生成物をコミットしない方針のため）。`python tools/kit_lint.py check` と `selftest` 相当の追加実行は行っていない（P5 では明示的に要求されていない）。

`references/` 配下の編集はすべて `Bash` から実行した Python の直接書き込みで行い、Claude Code の `Edit`/`Write`/`MultiEdit` ツールは経由していない（グローバル PostToolUse フォーマッタがリポジトリルート以外の cwd では `.prettierignore` を無視する既知の不具合があるため）。

OpenSandbox 等の隔離実行環境は不要と判断し、使用しなかった。
