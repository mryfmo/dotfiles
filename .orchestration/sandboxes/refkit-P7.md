# refkit-P7: サンドボックス状況

`references/` 配下の編集はすべて Bash から実行した Python の直接書き込みで行い、Claude Code の `Edit`／`Write`／`MultiEdit` ツールは経由していない（グローバル PostToolUse フォーマッタが cwd 次第で `.prettierignore` を無視する既知の不具合があるため）。

`kit_lint.py check` を 1 回実行した（読み取りのみ、ネットワークアクセスなし）。`tools/kit_lint.py extract`／`trace` は今回は実行していない（本タスクは E120／E121 の再生成を要求していないため）。

`node --check` を、§9 から抽出した k6 スクリプト（`/tmp/.../scratchpad/nvt_001.mjs`、スクラッチパッド配下）に対して実行した。ローカル Node（mise 管理、v26.9.0）のみを使用し、追加のインストールは行っていない。

`npx --no-install tsc --version` と `npx --no-install playwright --version` を試行し、いずれも未インストールで失敗することを確認した（ネットワーク経由の自動インストールは発生していない。`--no-install` により明示的に抑止）。typescript／@playwright/test のインストールは、task_file の「ワークツリー外への書き込みなしに導入できる場合のみ」という条件を満たせないため行っていない。

`which k6` で k6 が未インストールであることを確認したのみで、mise 等によるインストールは行っていない（同じ理由）。

OpenSandbox 等の隔離実行環境は不要と判断し、使用しなかった。
