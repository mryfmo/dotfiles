## Codex

### ユーザーへの質問

- ユーザが提供した情報に基づいて、最適な解決策を提案するための質問を行ってください。

### セッション終了時のまとめ

- 対話セッションでは、会話の自然な区切りで直ちに次のアクションが想定されない場合に、以下の形式で 1 行のまとめを出力してください。`codex exec` などの非対話実行、監査、機械が読む出力には付けないでください。
- `📝 まとめ: <このセッションで完了した内容を 1〜2 文で要約してください。未完了のタスクや次のアクションがあれば末尾に追記してください。>`

### plan と todo

- リポジトリ作業では plan と todo を常に更新してください。
- スクラッチの plan/todo/learn はコミットせず、`active` な todo は `owner` ごとに 1 件までにしてください。plan をバージョン管理しているリポジトリ(dotfiles の `plans/` や `.orchestration/` など)では、そのリポジトリの規則に従ってください。

### コーディング

- 使い捨ての研究・プロトタイプのコードでは、エラーを恐れず、まず例外処理や後方互換性を気にせずに書いてください。
- リポジトリのコードでは、そのリポジトリの AGENTS.md の規則が優先です。trust boundary の入力検証、fail-closed のエラー処理、データ損失の防止は省かないでください。
- あらかじめテストを記述し、テストが通ることを確認してから、必要に応じてコードをリファクタリングしてください。

### レビューと Crit

- 計画、コード、diff、PR のレビューには Codex の `/diff`、`/review`、Codex app の Review pane を使ってください。レビュー証跡の形はリポジトリの AGENTS.md に従います。
- 自分からブラウザの Crit を開いたり、Crit で人間にレビューを依頼したりしないでください(2026-07-18 操作者指示)。ユーザが明示的に Crit web UI を求めた場合だけ `$crit`(`crit --no-open` または `crit`)を使い、`http://localhost` で始まるレビュー URL と「Finish Review をクリックする」旨をユーザ向けメッセージとして TUI 上に表示してください。
- Crit plugin の `Stop` hook による Plan Mode レビューが発火した場合は、`CRIT_PLAN_REVIEW=off` が明示されていない限り迂回しないでください。レビューが終わったら Crit セッションを閉じてください(ローカルの Crit web server を常駐させない)。
- `crit share` などの publish は、ユーザが明示的に求めた場合だけ実行してください。ユーザが明示的に Crit/review を無効化した場合のみ `CRIT_REVIEW=off` を使ってください。

### PR のフィードバック

- PR のフィードバック(issue comment、review、inline review comment、失敗・未完了の check run と全レベルの annotation、commit status)は最終 head に対して `gh` で取得し、push の後は取得し直してください。review thread の解決状態は読み取り専用の `pr-threads-check.sh` で読みます(`gh api graphql` は Codex の rules で禁止されています)。
- 指摘の処分と closure はリポジトリの AGENTS.md の規則に従ってください。Codex は merge しません(`gh pr merge` は Codex の rules で禁止されています)。

### モデル profile

- 通常の実装・デバッグは `codex --profile standard`、読み取り・検索・抽出だけの作業は `--profile express`、独立レビューは `--profile review`、`/security-review`、permgate policy、redaction/secret handling、trust-boundary code の監査は `--profile security`、監査以外の横断設計・未知の障害だけ `--profile deep` を使ってください。難所が終わったら standard へ戻してください。
- profile は `~/.codex/<profile>.config.toml` と `~/.agents/model-profiles.env` に生成されます。セッション途中でモデルを切り替えず、profile はセッション起動時に選んでください。

### CompactionDB の記録

- CompactionDB 導入済み project では、`model_profiles` の codex 側に `notify` を持つ profile(`~/.codex/<profile>.config.toml` に `notify` がある profile)の turn 完了が project DB へ自動記録されます。`--profile` なしの `codex` が記録するのは compaction と session 終了の hook だけです。
