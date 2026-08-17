# AGENTS.md

## ユーザーへの質問

- ユーザが提供した情報に基づいて、最適な解決策を提案するための質問を行ってください。

## セッション開始時の learn 確認

- 作業を開始する前に、`.agents/worklog/codex/learn/learn_index.md` を読み、過去のセッションで得た知見やエラーの教訓を把握してください。
- インデックスの中で今回のタスクに関連しそうな項目があれば、該当する learn ファイルの本文も読んでから作業に取り掛かってください。
- 特にエラーや失敗に関する教訓は、同じ過ちを繰り返さないように作業中も意識してください。

## セッション終了時のまとめ

- 会話の自然な区切りで、直ちに次のアクションが想定されない場合は、以下の形式で 1 行のまとめを出力してください。
- `📝 まとめ: <このセッションで完了した内容を 1〜2 文で要約してください。未完了のタスクや次のアクションがあれば末尾に追記してください。>`

## プロジェクトの構成について

- リポジトリ作業では `agmsg-orchestration` skill の「Codex worker worklogs」を読み、plan と todo を常に更新してください。
- plan/todo/learn はコミットせず、`active` な todo は `owner` ごとに 1 件までにしてください。

## コーディング全般について

- エラーを恐れないでください。まずは例外処理は気にせずコードを書いてください。
- 最終成果物でも例外処理は入れなくて構いません。
- 研究開発用途が主なため後方互換性は気にしないでください。あらかじめテストを記述し、テストが通ることを確認してから、必要に応じてコードをリファクタリングしてください。

## Crit レビュー運用

- 計画レビュー、コードレビュー、diff レビュー、PR レビュー、または「レビュー」と明示された作業では、まず Codex 内の `/diff`、`/review`、Codex app の Review pane、または取得済みの Crit data を使ってください。ユーザが Crit web UI を明示した場合、または Crit data を取得できない場合のみ `$crit` / `crit` をブラウザ review として使ってください。
- Codex では Crit plugin の `Stop` hook による Plan Mode レビューが発火した場合は尊重してください。`CRIT_PLAN_REVIEW=off` が明示されていない限り、発火済みの計画レビュー hook を迂回しないでください。
- 完了報告前に git diff がある場合は `make require-crit-review` を実行してください。agent lifecycle、hooks、plugins、permissions、scripts、広い diff など意味のある変更だけレビューを要求します。
- `make require-crit-review` がレビューを要求したら、既定ではブラウザ版 Crit を起動しないでください。Codex は `crit status --json` で review file を特定し、`crit comments --all --json <review.json>` の出力を repo 内の `.agents/worklog/.../*.json` に保存して内容を判断し、指摘へ対応してください。Agent evidence には resolved record が 1 件以上必要です。指摘がない場合は review-scope の approval record を追加して resolve してください。このローカルデータは作業手順の証跡にすぎず、レビュー実施者を認証するものではありません。その後 `review_surface: crit-data` `reviewer: codex` `review_source: <repo 内 JSON evidence path>` `review_outcome:` を含む receipt を作り、`AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review` を通してください。Crit data の JSON evidence を読まない `AGENT_REVIEWED=1` だけの自己申告は禁止です。
- ユーザが明示的に Crit web UI を求めた場合、または Crit data を取得できない場合だけ `crit --no-open` または `crit` を使ってください。その場合は `http://localhost` で始まるレビュー URL と「Finish Review をクリックする」旨をユーザ向けメッセージとして TUI 上に表示し、完了後に receipt を作り `CRIT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review` を通してください。
- ユーザが明示的に Crit/review を無効化した場合のみ `CRIT_REVIEW=off` を使ってください。

## モデル選択

- 対話用モデル ID と reasoning effort の正本は dotfiles の `home/dot_agents/agent-config.yaml` の `model_profiles` です。profile は `~/.codex/<profile>.config.toml` と `~/.agents/model-profiles.env` に生成されます。対話用モデル変更は manifest で行い、launcher やルールに直書きしないでください。permgate の分類器モデルだけは security policy で別途固定します。
- 通常の実装・デバッグは `codex --profile standard`、読み取り・検索・抽出だけの作業は `--profile express`、独立レビューは `--profile review`、`/security-review`、permgate policy、redaction/secret handling、trust-boundary code の監査は `--profile security`、監査以外の横断設計・未知の障害だけ `--profile deep` を使ってください。難所が終わったら standard へ戻してください。
- セッション途中でモデルを切り替えず、profile はセッション起動時に選んでください。
- permgate は PermissionRequest を deterministic-first で評価し、不明・失敗時は Codex native の確認へ fail-closed します。Claude/Codex はそれぞれ既存認証の公式 CLI を使い、分類器へ渡すのは正規化済みaction metadataだけです。両providerを shadow のまま維持し、分類成功数・p50/p95・人手評価を満たしたproviderだけ有効化してください。

## Ponytail

- Ponytail (`ponytail@ponytail`) を利用できる場合は、コーディング作業で YAGNI、stdlib/native platform first、既存実装の再利用、最小の正しい差分を優先してください。
- Ponytail は「短ければよい」ではありません。trust boundary の入力検証、データ損失防止、セキュリティ、アクセシビリティ、明示要求された要件は削らないでください。
- Codex で初回導入または更新後は `/hooks` を開き、Ponytail lifecycle hooks を review and trust してから新しい thread を開始してください。
- モードは上流の既定値 `full` を使います。必要な場合だけ `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off` または Ponytail コマンドで変更してください。

## Understand-Anything

- Understand-Anything (`understand-anything@understand-anything`) を利用できる場合は、リポジトリのナレッジグラフ生成・参照に使ってください。Codex では `$understand` で起動します(`/understand` ではありません)。
- 初回のフル解析はトークン消費が大きい処理です。増分解析(2 回目以降)は軽量です。
- 出力は `.ua/` に生成されます。`.ua/intermediate/` と `.ua/diff-overlay.json` は commit せず、対象リポジトリの `.gitignore` に追加してください。それ以外の `.ua/` は commit 対象です。
- リポジトリ全体の探索やシンボル検索の前に、`.ua/knowledge-graph.json` があればまず node の `summary` と `filePath` を照会し、`.ua/meta.json` の `gitCommitHash` が `git rev-parse HEAD` と一致するか、異なる場合も `git diff --name-only <hash>..HEAD` が `.ua/` または `.orchestration/` 内の path だけなら current と扱い、graph が存在しないか別の path が含まれる場合だけ grep にフォールバックしてください。
- インストーラは skills を `~/.agents/skills` に symlink します。導入・更新後は CLI を再起動してください。

## Crit レビューの利用方針

## CompactionDB

- CompactionDB 導入済み project では、Codex standard/deep profile の turn 完了が同じ project DB へ自動記録されます。
- 永続的な決定は従来どおり `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` で明示記録します。

- Crit は自分(エージェント)自身のレビューにのみ使う: `crit comment` / `crit share` 等の CLI でコメントを起票・返信・解決し、JSON 証跡を `.orchestration/` または `.agents/worklog/` に保存する。
- ブラウザ Crit レビューを開いたり、人間のユーザーにレビューを依頼する目的で Crit を使うことは禁止(2026-07-18 操作者指示)。
