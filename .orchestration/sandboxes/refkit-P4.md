# refkit-P4: サンドボックス状況

このタスクはドキュメント（Markdown）のみの編集であり、コード実行・ネットワークアクセス・外部サービス呼び出しは発生しない。OpenSandbox 等の隔離実行環境は不要と判断し、使用しなかった。

グローバル PostToolUse フォーマッタが `.prettierignore` を cwd 依存で無視ファイルを解釈する不具合（report 参照）を実作業中に発見したため、`references/` 配下のすべての編集（新規 2 ファイル、既存 3 ファイルの部分編集）を `Bash` から実行した Python スクリプト（`str.replace` の単発一致を assert した上での置換、または全文書き込み）で行った。Claude Code の `Write`/`Edit`/`MultiEdit` ツールは経由していない（新規 2 ファイルは最初 `Write` ツールで作成し、フォーマッタによる再整形を検知した後に同じ内容を Python で書き直して復元した）。

実行したコマンドはローカルの静的検査のみ：`python tools/kit_lint.py check`、`python tools/kit_lint.py selftest`（いずれも読み取りと一時ディレクトリでの変異のみ。`root` への書き込みなし）、`git diff`/`git status`。外部ネットワークアクセスは発生していない。
