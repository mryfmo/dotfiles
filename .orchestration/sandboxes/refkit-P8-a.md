# refkit-P8-a: サンドボックス状況

`references/` 配下の編集はすべて Bash から実行した Python の直接書き込みで行い、Claude Code の `Edit`／`Write`／`MultiEdit` ツールは経由していない（グローバル PostToolUse フォーマッタが cwd 次第で `.prettierignore` を無視する既知の不具合があるため）。

`kit_lint.py check` を 3 回実行した（読み取りのみ、ネットワークアクセスなし）：初回は基準確認、2 回目で新規の E014（`{{P9}}` プレースホルダ）を検出、`<P9>` へ変更後の 3 回目で E120/E121/E103(×2) のみに復帰したことを確認した。`extract`／`trace` は本タスクでは実行していない（E120/E121 の再生成は要求されておらず、生成物のコミットも forbidden_actions に含まれる）。

`grep` によるコードベース調査（`tools/kit_lint.py`・`kit.toml`）を多数回実行し、`[ids]`・`prefix`・`gherkin_source`・`mirror`・E122・E123・E159・W160 のいずれも本枝に存在しないことを確認した。`find`／`ls` でディレクトリ構成（`archive/`・`tools/`・`adr/`）を確認した。いずれもローカルの読み取りのみ。

`node`／`npx` のインストール状況確認は本タスクでは行っていない（前タスク refkit-P7 で確認済みの結果を再利用）。

4 件の並列サブエージェント（`Agent` ツール、`Explore` 型、読み取り専用）を用いて、91 件の指摘マッピング、02 の出典再分類、00/05/06/90 の骨格事実、PRD_GUIDE/PRD_SAMPLE の対象セルをそれぞれ調査した。いずれも読み取り専用で、編集は本セッションが直接行った。

OpenSandbox 等の隔離実行環境は不要と判断し、使用しなかった。
