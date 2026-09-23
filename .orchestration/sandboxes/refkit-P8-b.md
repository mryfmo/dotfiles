# refkit-P8-b: サンドボックス状況

`references/` 配下の編集はすべて Bash から実行した Python の直接書き込みで行い、Claude Code の `Edit`／`Write`／`MultiEdit` ツールは経由していない。

`kit_lint.py check` を 1 回実行した（読み取りのみ、ネットワークアクセスなし）。`git log`・`grep` によるコード・設定の直接確認（`kit.toml` の `[ids]`／`[mermaid]`、`tools/kit_lint.py` の `gherkin_source`／E086、`tools/README.md`／`tools/mermaid_common.py` の実在）を多数回実行した。`extract`／`mirror`／`trace` は本タスクでは実行していない（E120／E121 の再生成は本タスクの対象外で、生成物のコミットも forbidden_actions に含まれる）。

OpenSandbox 等の隔離実行環境は不要と判断し、使用しなかった。並列サブエージェントは使用しなかった（対象ファイルが少なく、統合後の事実確認は直接の `grep`／ファイル読み取りで足りたため）。
