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

- プロジェクト構成はプログラミング言語ごとに異なりますが、作業を開始する際、存在しない場合のみ以下の構成でセットアップしてください。
  - 作業中は plan と todo を常に更新し続けてください。
  - これらの plan/todo/learn ファイルはコミットしないでください。
  - `.agents/worklog/codex/plan/`: プロジェクトの計画や設計に関するドキュメントを格納するディレクトリ
    - `$(date +%Y%m%d_%H%M%S)_plan.md` のような形式でファイルを作成してください
    - 実装する前に計画を立て、必要であればユーザへの質問を行って計画用のドキュメントを更新してください。
  - `.agents/worklog/codex/todo/`: タスク管理用のディレクトリ
    - `$(date +%Y%m%d_%H%M%S)_todo.md` のような形式でファイルを作成してください
    - `.agents/worklog/codex/plan/` ディレクトリのドキュメントをもとに、実装するタスクを洗い出して記述してください。
    - タスクは完了したら完了済みのセクションに移動してください。todo 全体が完了したら、ファイル名を `$(date +%Y%m%d_%H%M%S)_done.md` のように変更してください。
    - タスクの完了に伴って計画が変更された場合は、`.agents/worklog/codex/plan/` ディレクトリのドキュメントを更新してください。
  - `.agents/worklog/codex/learn/`: 学習用のドキュメントを格納するディレクトリ
    - `$(date +%Y%m%d_%H%M%S)_learn.md` のような形式でファイルを作成してください
    - プロジェクトの実装に必要な知識や技術を学習した際に、学習内容をこのディレクトリに記録してください。
    - 学習内容はプロジェクトの実装に活かせるように、必要に応じて `.agents/worklog/codex/plan/` ディレクトリのドキュメントを更新してください。
    - learn は「次回の意思決定を速くする情報」が得られたときに更新してください。
    - learn には「何を学んだか」「どこに反映すべきか」を必ず書いてください。
    - learn を更新したら、必要に応じて plan の `Assumptions` / `Design` / `Tests` を更新してください。
    - `.agents/worklog/codex/learn/learn_index.md`: learn ファイルの要約インデックス。learn ファイルを新規作成・更新・削除した際は、必ずこのインデックスも更新してください。
    - インデックスの各エントリは 1 行で `- [タイトル](ファイル名) — 要約（150 文字以内）` の形式で記述してください。
  - 作成するファイルには以下の最低限の見出しを含めてください。
    - plan: `Goal`, `Scope`, `Assumptions`, `Design`, `Tests`, `Open Questions`
    - todo: `TODO`, `Done`
    - learn: `Date`, `Learnings`, `Plan Updates`

### plan/todo/learn の frontmatter ルール

- `.agents/worklog/codex/plan/*.md` `.agents/worklog/codex/todo/*.md` `.agents/worklog/codex/learn/*.md` の先頭に YAML frontmatter を必須とします。
- 並列実行を前提に、`active` 制約は「リポジトリ全体で 1 件」ではなく「`owner` ごとに 1 件」とします。

#### 共通必須キー

- `type`: `plan | todo | learn`
- `id`: `YYYYMMDD_HHMMSS`
- `owner`: 例 `codex-a`, `codex-b`
- `created_at`: ISO8601
- `updated_at`: ISO8601

#### type ごとの必須キー

- `todo`: `status`, `workstream`, `related_plan`
- `plan`: `status`
- `learn`: `validated`, `apply_to`

#### status 値

- `todo.status`: `active | blocked | done | superseded`
- `plan.status`: `draft | active | done | superseded`
- `learn.validated`: `true | false`

#### 推奨キー（任意）

- `depends_on`: 依存する `todo id` の配列
- `blocked_reason`: `status=blocked` の理由
- `evidence`: ログ/PR/実験結果のパス配列
- `tags`: 任意タグ

#### 運用ルール

- 新規 `todo` 作成時は `owner` を必ず設定してください。
- 各 `owner` は同時に `active` な `todo` を 1 件までにしてください。
- `# TODO` が空になったら `status: done` に更新し、`*_done.md` へリネームしてください。
- `learn` は「再利用可能」かつ「検証済み (`validated: true`)」のときのみ作成してください。
- `learn` 更新時は `apply_to` に反映先（plan/tests）を明記してください。

## コーディング全般について

- エラーを恐れないでください。まずは例外処理は気にせずコードを書いてください。
- 最終成果物でも例外処理は入れなくて構いません。
- 研究開発用途が主なため後方互換性は気にしないでください。あらかじめテストを記述し、テストが通ることを確認してから、必要に応じてコードをリファクタリングしてください。

## Crit レビュー運用

- 計画レビュー、コードレビュー、diff レビュー、PR レビュー、または「レビュー」と明示された作業では、まず Codex 内の `/diff`、`/review`、Codex app の Review pane、または Crit data（例: `crit comments --json`）を使ってください。ユーザが Crit web UI を明示した場合、または Crit data を取得できない場合のみ `$crit` / `crit` をブラウザ review として使ってください。
- Codex では Crit plugin の `Stop` hook による Plan Mode レビューが発火した場合は尊重してください。`CRIT_PLAN_REVIEW=off` が明示されていない限り、発火済みの計画レビュー hook を迂回しないでください。
- 完了報告前に git diff がある場合は `make require-crit-review` を実行してください。agent lifecycle、hooks、plugins、permissions、scripts、広い diff など意味のある変更だけレビューを要求します。
- `make require-crit-review` がレビューを要求したら、既定ではブラウザ版 Crit を起動せず、Codex が `crit comments --json` などで Crit data を取得し、repo 内の `.agents/worklog/.../*.json` に保存して内容を判断し、指摘へ対応してください。その後 `review_surface: crit-data` `reviewer: codex` `review_source: <repo 内 JSON evidence path>` `review_outcome:` を含む receipt を作り、`AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review` を通してください。Crit data の JSON evidence を読まない `AGENT_REVIEWED=1` だけの自己申告は禁止です。
- ユーザが明示的に Crit web UI を求めた場合、または Crit data を取得できない場合だけ `crit --no-open` または `crit` を使ってください。その場合は `http://localhost` で始まるレビュー URL と「Finish Review をクリックする」旨をユーザ向けメッセージとして TUI 上に表示し、完了後に receipt を作り `CRIT_REVIEWED=1 REVIEW_EVIDENCE=<receipt> make require-crit-review` を通してください。
- ユーザが明示的に Crit/review を無効化した場合のみ `CRIT_REVIEW=off` を使ってください。

## モデル選択と ccgate

- タスクに必要な最小限のモデルを選択してください。単純な読み取り、検索、整形、軽微な編集だけを続ける場合は gpt-5.5 や推論 tier の大型モデルを使い続けないでください。
- ccgate はモデルルータではなく PermissionRequest gate です。`provider.model` は ccgate の許可判定に使う小型分類器であり、Codex のタスク実行モデルではありません。
- Codex の PermissionRequest では ccgate が `HookInput.model` を参照できます。これは比例性の補助信号であり、必要な調査・検索・read 操作を大型モデルという理由だけで止めるためのものではありません。
- ccgate に過剰・危険・広すぎる操作を止められた場合は、小さいモデルへ切り替えるか、タスクを大型モデルが必要な範囲に絞ってから再実行してください。
- ccgate の判定傾向は `ccgate codex metrics --details 5` で確認し、fallthrough や deny が多い具体的な操作を見てルールを調整してください。

## Ponytail

- Ponytail (`ponytail@ponytail`) を利用できる場合は、コーディング作業で YAGNI、stdlib/native platform first、既存実装の再利用、最小の正しい差分を優先してください。
- Ponytail は「短ければよい」ではありません。trust boundary の入力検証、データ損失防止、セキュリティ、アクセシビリティ、明示要求された要件は削らないでください。
- Codex で初回導入または更新後は `/hooks` を開き、Ponytail lifecycle hooks を review and trust してから新しい thread を開始してください。
- モードは上流の既定値 `full` を使います。必要な場合だけ `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off` または Ponytail コマンドで変更してください。
