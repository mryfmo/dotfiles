# refkit-P0-05: サンドボックス状況

コード実行はローカルの `npx prettier@2`・`uvx ruff`・`make` のみで、いずれも本リポジトリ内のファイルに対する読み取り専用の `--check` 呼び出し（`references/` に対しては何も書き込んでいない。`git status --short -- references/` で無変更を確認済み）。`make unit-test`・`make validate-agent-assets` はリポジトリ内の既存テスト・検証スクリプトを実行するのみ。外部ネットワークアクセスは prettier@2 パッケージの取得（npm 経由、既存の仕組み）のみで、新規の外部通信は発生していない。OpenSandbox 等の隔離実行環境は不要と判断し、使用しなかった。
