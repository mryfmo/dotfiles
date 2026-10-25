# AGENTS.md

## ユーザーへの質問

- ユーザが提供した情報に基づいて、最適な解決策を提案するための質問を行ってください。

## セッション終了時のまとめ

- 会話の自然な区切りで、直ちに次のアクションが想定されない場合は、以下の形式で 1 行のまとめを出力してください。
- `📝 まとめ: <このセッションで完了した内容を 1〜2 文で要約してください。未完了のタスクや次のアクションがあれば末尾に追記してください。>`

## プロジェクトの構成について

- リポジトリ作業では plan と todo を常に更新してください。
- plan/todo/learn はコミットせず、`active` な todo は `owner` ごとに 1 件までにしてください。

## コーディング全般について

- エラーを恐れないでください。まずは例外処理は気にせずコードを書いてください。
- 最終成果物でも例外処理は入れなくて構いません。
- 研究開発用途が主なため後方互換性は気にしないでください。あらかじめテストを記述し、テストが通ることを確認してから、必要に応じてコードをリファクタリングしてください。

## Crit レビュー運用

- 計画レビュー、コードレビュー、diff レビュー、PR レビュー、または「レビュー」と明示された作業では、Codex 内の `/diff`、`/review`、Codex app の Review pane を使ってください。ブラウザの Crit web UI を開いたり、人間のユーザーにレビューを依頼する目的で Crit を使ったりしないでください(2026-07-18 操作者指示)。
- Codex では Crit plugin の `Stop` hook による Plan Mode レビューが発火した場合は尊重してください。`CRIT_PLAN_REVIEW=off` が明示されていない限り、発火済みの計画レビュー hook を迂回しないでください。
- Plan Mode hook が開いた Crit セッションは、レビューが終わったら閉じてください(ローカルの Crit web server を常駐させない)。
- ユーザが明示的に Crit/review を無効化した場合のみ `CRIT_REVIEW=off` を使ってください。
- dotfiles リポジトリの変更のレビュー証跡は、プログラムの記録 `.orchestration/orchestrate/<program>/ledger.tsv` にある、その head sha の verdict 行です(`hcom-orchestration` skill)。Crit のコメントや保存した JSON はレビュー証跡になりません。

## PR 統合

- PR を merge する前に、最終 head commit に対する GitHub のフィードバックを `gh` で必ず全件確認してください。issue comment、review、thread の解決状態付き inline review comment、失敗・未完了の check run、全レベル(`notice`・`warning`・`failure`)の check-run annotation、commit status を含みます。
- 最終 head に `@coderabbitai full review` を依頼してもかまいません(任意)。プランは 1 時間に 1 review で、review event ごとに 1 回消費します(docs.coderabbit.ai/management/rate-limits)。依頼は最終 head で多くとも 1 回にしてください。CodeRabbit の review が存在する場合は他の item と同様に取得して disposition を付けます。ゲートは bot review を要求しません。
- 全 item に disposition を付けてください。`fixed:<commit>`(その commit で根本原因を修正)か `not-applicable:<理由>` のどちらかです。stopgap・抑制・「後で」は disposition として認めません。`failure` と `warning` の annotation を未処分のまま残さず、`failure` を `not-applicable` にする場合は 20 文字以上の具体的な理由が必要です。
- disposition の要約は PR のコメントに書いてください。merge は orchestrator が `hcom-orchestration` SKILL の手順(head sha の verdict 行、CI green)で行います。
- 新しい push の後は取得をやり直してください。disposition は記入した時点の head commit にだけ有効です。
- boundary PR(`.orchestration` のファイルだけを変更)も同じ `hcom-orchestration` SKILL の手順で merge します。CI の `regime` check は records-only の差分として通します。

## モデル選択

- 対話用モデル ID と reasoning effort の正本は dotfiles の `home/dot_agents/agent-config.yaml` の `model_profiles` です。profile は `~/.codex/<profile>.config.toml` と `~/.agents/model-profiles.env` に生成されます。対話用モデル変更は manifest で行い、launcher やルールに直書きしないでください。
- 通常の実装・デバッグは `codex --profile standard`、読み取り・検索・抽出だけの作業は `--profile express`、独立レビューは `--profile review`、`/security-review`、permgate policy、redaction/secret handling、trust-boundary code の監査は `--profile security`、監査以外の横断設計・未知の障害だけ `--profile deep` を使ってください。難所が終わったら standard へ戻してください。
- セッション途中でモデルを切り替えず、profile はセッション起動時に選んでください。
- permgate は deterministic-only です。PermissionRequest は policy の deny/allow パターンだけで判定し、それ以外と失敗時は Codex native の確認へ fail-closed します。分類器モデルは使いません。

## Ponytail

- Ponytail (`ponytail@ponytail`) を利用できる場合は、コーディング作業で YAGNI、stdlib/native platform first、既存実装の再利用、最小の正しい差分を優先してください。
- Ponytail は「短ければよい」ではありません。trust boundary の入力検証、データ損失防止、セキュリティ、アクセシビリティ、明示要求された要件は削らないでください。
- Codex で初回導入または更新後は `/hooks` を開き、Ponytail lifecycle hooks を review and trust してから新しい thread を開始してください。
- モードは上流の既定値 `full` を使います。必要な場合だけ `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off` または Ponytail コマンドで変更してください。

## Understand-Anything

- Understand-Anything (`understand-anything@understand-anything`) を利用できる場合は、リポジトリのナレッジグラフ生成・参照に使ってください。Codex では `$understand` で起動します(`/understand` ではありません)。
- 初回のフル解析はトークン消費が大きい処理です。
- dotfiles リポジトリでは、graph の更新は operator が regime boundary で依頼したときだけ、worker task が `$understand --full` で行います。増分更新はこのリポジトリでは公開できません。Understand-Anything 2.9.7 の `validate-incremental-symbols.mjs` は、決定的な parser がないファイル(拡張子のない shell script `executable_hcom-dispatch`、Python の chezmoi script `modify_private_settings.json`)の class に属さない関数をすべて `unknown` と判定し、path ごとの言語指定もないためです(T51)。`.ua/config.json` は `autoUpdate: false` で、plugin の SessionStart と PostToolUse の更新指示を止めます。更新と更新の間 graph は意図的に stale であり、下の鮮度確認によって検索は grep にフォールバックします。
- 出力は `.ua/` に生成されます。`.ua/intermediate/` と `.ua/diff-overlay.json` は commit せず、対象リポジトリの `.gitignore` に追加してください。それ以外の `.ua/` は commit 対象です。
- リポジトリ全体の探索やシンボル検索の前に、`.ua/knowledge-graph.json` があればまず node の `summary` と `filePath` を照会し、`.ua/meta.json` の `gitCommitHash` が `git rev-parse HEAD` と一致するか、異なる場合も `git diff --name-only <hash>..HEAD` が `.ua/` または `.orchestration/` 内の path だけなら current と扱い、graph が存在しないか別の path が含まれる場合だけ grep にフォールバックしてください。
- インストーラは skills を `~/.agents/skills` に symlink します。導入・更新後は CLI を再起動してください。
- `.ua/` graph の RESULT は、`ua-symbol-coverage <前回 graph> <新 graph> --old-ref <前回 graph の rev> --repo-ref <新 graph の rev>`(`~/.local/bin/common` から PATH 上にあります。各 rev はその graph の `.ua/meta.json` の `gitCommitHash` で、フル再構築では `--old-ref` が前回の `meta.gitCommitHash` です。新 graph 側は通常 `HEAD`、変更前の base ではありません。`--old-ref` で rename と削除を区別します) の表を validation file に貼り、regression が 0 件(または減少ごとに原因となるソース変更を明記)の場合だけ accept します。`validateGraph` の成功は抽出の完全性を保証しません。
- worker seat は、unit の SCOPE に `.ua/**` が含まれない限り、Understand-Anything の auto-update hook の指示(「knowledge graph is stale, you MUST update it」)を対象外として扱い、report に「hook fired; not acted on」と記録して作業を続けてください。orchestrator は自身のセッションで graph を更新せず、graph の更新は別の worker seat の unit にします。

## CompactionDB

- CompactionDB 導入済み project では、Codex standard/deep profile の turn 完了が同じ project DB へ自動記録されます。
- 永続的な決定は従来どおり `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` で明示記録します。
