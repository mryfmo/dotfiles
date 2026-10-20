# Plan 024 設計 4/5: プログラム仕様（各仕組みのパス、呼び出し、入力、出力、終了コード、失敗時、テスト。17 項目）

> 読む時機: P1-3〜P1-14 の仕組みタスクのタスク文を書くとき、その 1 項目だけを読む。品質条件は `024-design-quality.md` 5.11、採否は 5.10、人の判断の細分化は 5.13。ディレクトリ規約: JSON Schema は `.schemas/`、flake 署名は `.github/flakes.yaml`、git hooks は `.githooks/`、学習記録と class 語彙は `.orchestration/learning/`。

5.12 **プログラム仕様（文章ではなくプログラムとして何を作るか）**

**(1) `scripts/orchestrator/verdict.sh <pr> [--apply] [--loop] [--shadow]`**（P1-4a）
- 入力: `gh pr view <pr> --json headRefOid,isDraft,baseRefName,state`、`gh pr checks <pr> --json name,state`（ruleset の必須 7 本）、受け入れ記録（JSON ブロックの `head`、`precheck`、`task_id`）、`.orchestration/validation/<task>-audit-<head>.json`、`scripts/pr-feedback.py <pr> --json <out>`（最終 head のスレッド。引数名はタスク文作成時に `--help` を貼って確定）、`.orchestration/validation/<task>-pr-feedback.json`（disposition）、`task.md` の `allowed_files`・`security`・caps、`scripts/regime-counters.sh <task> --history-only`（S1 クラス数、revise 数）、`git diff --name-only <base>..<head>`、`security: true` なら `<task>-security-<head>.md` の verdict、環境変数 `PRECHECK_REQUIRED`（0 のとき条件 (1) は警告扱い）。
- 判定条件（9。すべて真で accept）: (1) `precheck` の sha256 = `.orchestration/<task>/precheck.json` の sha256 かつ `head` 一致、(2) 必須チェック 7 本が head で success、(3) audit JSON が schema 合格かつ verdict=correct、または残る所見が `scope=records` のみ、(4) 全スレッドに最終 head の disposition があり、not-applicable には refutation、(5) 変更ファイル ⊆ allowed_files、caps 内、(6) S1 同一クラス < 3、INV-6 revise < 2、(7) P0/P1 の未対処 0、(8) `security: true` なら security review の verdict=correct、(9) 受け入れ記録に書かれた証跡 sha256 と実ファイルが一致。
- 出力: `.orchestration/validation/<task>-verdict-<head>.json`（schema `.schemas/verdict.json`: verdict、conditions[{id, ok, evidence}]、inputs_sha256、generated_at）。終了コード 0 = accept、10 = revise、20 = hold、2 = 内部エラー（= hold 扱い）。
- `--apply`: verdict=accept のときだけ、ACCEPTANCE 行（`status=accepted`）を `dispatch.sh` で送り、`gh pr merge <pr> --squash --match-head-commit <head>` を実行（`--admin`/`--auto` を含む引数は構文で拒否）。`--shadow`: 判定のみ書き、`.orchestration/validation/verdict-shadow.tsv`（列 pr、head、machine、human、agree、at）の machine 列に追記。human 列は orchestrator が受け入れ直後に書く。`--loop`: ready な PR（受け入れ記録が存在し、その head が PR の現在 head に一致する open・非 draft の PR）を順に処理、1 本終わるごとに `git fetch` して次へ。
- テスト `tests/unit/test_verdict.py`: 全緑 → accept；条件 (1)〜(9) を 1 つずつ崩す 9 fixture → revise か hold；schema 不合格 → hold；`--apply` が accept 以外で何も呼ばないこと（fake gh が argv を記録）；`--admin` 混入の拒否；`PRECHECK_REQUIRED=0` で (1) が警告になること。

**(2) `scripts/orchestrator/audit-pool.sh [--once|--loop] [--max 2]` と `orch-audit.sh --json`**（P1-4a。`--loop` は orchestrator が boundary ごとに起動し、次の boundary で止める）
- キュー: `.orchestration/validation/audit-queue/<task>-<head>.request`（integrate-seat か orchestrator が置く。中身: pr、head、base、task、previous_head）。`flock` でロック、同時 `--max` 本。
- 実行: `orch-audit.sh <pr> <head> --json --out audit-<head>.json [--previous-head <sha> --previous-findings audit-<prev>.json]`。差分モードでは監査プロンプトに `git diff <prev>..<head>` と前回所見を渡し、「前回所見の各項目が fixed / still-open か、新規 hunks の所見」を求める。初回は全差分。差分モードは shadow 比較（5.11 Q-C）で所見差 0 を 2 件確認するまで無効。
- 出力: `.schemas/audit.json` に合格した JSON のみ保存。不合格は `<request>.rejected` に理由を書き、request を blocked に。Codex の 429 は 60/120/240 秒で 3 回まで再試行、超えたら blocked。
- テスト `tests/unit/test_audit_pool.py`: fake codex が決め打ち JSON を返す；schema 合格で保存・不合格で rejected；`--max 2` で 3 本目が待つ；差分モードのプロンプトに前回所見が含まれる；429 の再試行回数。

**(3) `.schemas/audit.json`、`.schemas/verdict.json`、`.orchestration/learning/classes.yaml`**（P1-4a）

```json
{ "$schema": "https://json-schema.org/draft/2020-12/schema", "title": "audit", "type": "object",
  "required": ["head", "task_id", "auditor", "generated_at", "verdict", "findings"],
  "properties": {
    "head": {"type": "string", "pattern": "^[0-9a-f]{40}$"}, "task_id": {"type": "string"},
    "auditor": {"type": "string"}, "generated_at": {"type": "string", "format": "date-time"},
    "verdict": {"enum": ["correct", "incorrect", "blocked"]},
    "findings": {"type": "array", "items": {"type": "object",
      "required": ["id", "priority", "confidence", "file", "line", "class", "scope", "rationale"],
      "properties": {
        "id": {"type": "string"}, "priority": {"enum": ["P0", "P1", "P2", "P3"]},
        "confidence": {"enum": ["high", "medium", "low"]},
        "file": {"type": "string"}, "line": {"type": "integer", "minimum": 1},
        "class": {"enum": ["<.orchestration/learning/classes.yaml から生成>"]},
        "scope": {"enum": ["code", "records"]}, "rationale": {"type": "string", "maxLength": 400},
        "status": {"enum": ["new", "fixed", "still-open"]}
      }}}}}
```

`classes.yaml` は S1 の制御語彙（例: `string-form-comparison`、`ps-output-parsing`、`excluded-command-trusts-sandbox-context`、`records-form`、…）で、各 class に `remedy:` と `blast_radius:`（(13) が読む）を持つ。`validate` CI が schema と classes の整合を検査し、未知の class は schema 不合格。

**(4) `scripts/orchestrator/result-precheck.sh <task> [--previous-head <sha> --check <selector>...]`**（P1-5）
- 実行: `make unit-test`（または task の test 選択）、`make render-check`、`scripts/orchestrator/local-review.sh`（clean）、変更 `.sh` の shellcheck、`make format` の差分 0、秘密スキャン（`scripts/validate-agent-assets.py --mask-secrets` の検出器を diff に適用）。`--previous-head` と `--check` があれば、一時 worktree（`git worktree add` を `$TMPDIR` に）で previous_head のセレクタが fail、head で pass を確認。
- 出力: `.orchestration/<task>/precheck.json`（head、checks[{name, ok, output_sha256}]、selectors[{sel, prev, head}]）と `.orchestration/<task>/result.txt`（worker が送る RESULT 行の写し。(6) が読む）。precheck.json の sha256 を標準出力に出し、worker はそれを RESULT の `precheck=` に書く。1 検査でも ok=false なら exit 1。`dispatch.sh` は RESULT 行に `precheck=` が無い、または sha256 がファイルと一致しないと拒否（`PRECHECK_REQUIRED=0` の間は警告のみ）。
- テスト `tests/unit/test_result_precheck.py`: 各検査の fail で exit 1 と JSON の ok=false；赤→緑の確認が「prev で pass」のとき fail；sha256 の一致；`PRECHECK_REQUIRED` の 0/1。

**(5) `scripts/orchestrator/dispositions.py <pr> <head> --feedback <json> [--require-refutation]`**（P1-10）
- 入力: pr-feedback.py の JSON（thread_id、commit、path、line、body）。各スレッドの (path, line) を `git diff <thread.commit>..<head> -- <path>` に当て、該当 hunk があれば `fixed:<commit touching the hunk>` を候補に、無ければ `not-applicable:` を要求。
- refutation の 3 形式（5.13）: `test:<selector>`（実行して pass を貼る）、`source:{url, fetched_at, quote}`（quote の実在をページのハッシュで確認）、`diff:<range>`（静的に到達不能）。
- 出力: `<task>-pr-feedback.json` の候補行（人または (16) の合議が確定）。`--require-refutation` は not-applicable に 3 形式のどれも無い行があると exit 1。`orch-gate.sh` は `PR_FEEDBACK_EVIDENCE` をこのモードで再検証する。
- テスト: 変更あり → fixed 候補；変更なし → not-applicable 要求；refutation 無しで exit 1；3 形式それぞれの受理。

**(6) `.github/workflows/regime.yml`（P1-11。任意チェック → 安定後に必須）**

```yaml
on: { pull_request: {} }
concurrency: { group: regime-pr-${{ github.event.pull_request.number }}, cancel-in-progress: true }
jobs:
  regime:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@<pinned sha>
        with: { fetch-depth: 0 }
      - run: uv run --no-project python -I scripts/orchestrator/regime-ci.py --base ${{ github.base_ref }} --head ${{ github.sha }}
```

`regime-ci.py` は、PR に `.orchestration/<task>/task.md` があれば dispatched 文（`.orchestration/tasks/<task>.md`）と byte 一致、`precheck.json` の `head` = `github.sha` かつ sha256 が `.orchestration/<task>/result.txt`（(4)）の `precheck=` と一致、変更ファイル ⊆ allowed_files、caps、threat_table の単位規則、を検査。違反は 1 行 1 件で失敗。records-only の PR（`orchestration/*` ブランチ）は skip ではなく「対象なし」で success。

**(7) `dispatch.sh --next <seat>`**（P1-6。`dispatch.sh` の変更系列は P1-5 → P1-6 → P1-13 → C-1）
- ready の定義: `.orchestration/tasks/<task>.md` があり、受け入れ記録が無い（未 dispatch）、`after:` の全タスクが accepted、`allowed_files` が in-flight（dispatch 済みで未 accept）の全タスクと素、席の最新 PONG の `context=` が 80% 未満、決定パネルの前提（`requires_decision:`）が記録済み。優先度は todo の順。
- 実行: 該当 1 件を既存の dispatch 経路で送る（task_sha256、checker、premises の再実行はそのまま）。該当なしは exit 3 と理由（素でない相手、未充足の after、席の context）。期限付き決定（decisions.tsv の basis 列 `default_after=<分>`）は期限を過ぎていれば既定値を消費して記録してから進む。
- テスト: fixtures で各条件の有無、期限付き決定の消費。

**(8) `acceptance-front-matter.py --from-result <result-line> --verdict <verdict.json>`**（P1-6）: 受け入れ記録の JSON ブロック（task_id、head、precheck、evidence sha256、ledger 行の骨格）を生成。手書きは `## Decisions` の散文だけ。

**(9) git hooks**（`.githooks/*` と検出器は P1-5。worktree に `core.hooksPath=.githooks` を設定する `herdr-agents --add-worker` の変更は P1-7、hcom 着席経路への移植は C-2）: `.githooks/pre-commit` = `make format` の差分 0 と変更 `.sh` の shellcheck；`.githooks/pre-push` = 秘密スキャン（(4) と同じ検出器）を push 範囲の diff に。失敗は exit 1 で止める。テストは hook を一時リポジトリで実行。

**(10) `scripts/orchestrator/handoff.sh`**（P1-9）: progress.tsv、`bus-history.sh --limit 200`（C-1 まで `timeout 60 history.sh`）の未処理 RESULT/PONG、decisions.tsv の open 行、`herdr agent list` から `.orchestration/handoff/<UTC>.md` を生成。

**(11) `.github/flakes.yaml` + `scripts/orchestrator/ci-rerun.sh <run-id>`**（P1-3）: 失敗ジョブのログが署名（正規表現）に一致したときだけ `gh run rerun --failed` を 1 回、記録に残す。

**(12) `scripts/orchestrator/task-from-plan.py <todo-id>`**（P1-12）: todo 行から task.md 骨格、`git grep` による allowed_files 提案、premises の command 実行と output 貼り付け、threat_table 雛形。

**(13) `scripts/orchestrator/hold-playbook.sh <task> <class>`**（P1-13）: `.orchestration/learning/classes.yaml` の `remedy:`（是正手順の文）と `blast_radius:`（glob の列）を読み、`.orchestration/tasks/<task>-replan.md` の骨格（原因 class、remedy、変更範囲、新しい完了条件、`re-plan:` 行）を書く。変更範囲が task の allowed_files に含まれれば exit 0（AI が中身を書いて再 dispatch）、含まれなければ decisions.tsv に `D-<task>-replan` 行（既定値なし）を追記して exit 3。`dispatch.sh` は hold 中（verdict=hold の最新記録）の task への TASK/revise を拒否（この `dispatch.sh` 変更は P1-6 マージ後）。テスト: 3 class の展開、範囲外で決定行、hold 中の拒否。

**(14) `scripts/permission-guard.py --base <ref> --head <ref>`（validate CI）と `scripts/orchestrator/ruleset-request.sh` / `ruleset-verify.sh`**（P1-14）: guard は `home/dot_agents/agent-config.yaml` と生成物の権限面（`permissions.*`、`excludedCommands`、`allowMachLookup`、`allowWrite`、`allowedDomains`、gh 書込を決める hook のパス）の diff を抽出し、その sha256 と一致する `D-… scope=permission approved_by=user diff_sha256=<sha>` 行が decisions.tsv に無ければ違反 1 行 1 件で exit 1。request は望む ruleset（strict、thread resolution、必須チェック）を JSON で出し `gh api rulesets/<id>` の現在値との diff を表示（書込はしない）。verify は適用後に一致を確認し progress.tsv に書く。テスト: 権限 diff に決定行なしで赤・ありで緑、request の diff 表示、verify の不一致検出。

**(15) `scripts/orchestrator/plan-check.py [--drift] [--invariants]`**（P1-12）: plan 群（024-* の 11 文書）を読み、形式（各 todo 行の完了条件、同時行の allowed_files 互いに素、P1 行 ↔ ボトルネック id、DoD のコマンド形式、決定の既定値と期限、相互参照の実在）、drift（PR/ブランチ/head/状態 vs gh・git、progress.tsv vs 受け入れ記録）、不変条件（禁止パターン）を検査。違反 1 行 1 件、exit 1。`validate` CI と boundary で実行。

**(16) `audit-pool.sh --second-opinion <finding-id> --refutation <file>`**（P1-10）: 所見と refutation を audit profile と security profile（別ベンダーがあればそちら）に渡し、両方が「所見は成立しない」なら `accepted-by-consensus`、不一致なら hold を `dispositions` の結果に書く。P0/P1 の not-applicable はこの合議を必須にする。

**(17) `scripts/orchestrator/integrate-seat.sh <pr>`**（P1-4。席が自分の PR に対して実行）
- 入力: PR 番号。`gh pr view` で head、base、state。task は受け入れ記録か `.orchestration/<task>/task.md` から。
- 手順: (a) BEHIND かつ衝突があるときだけ `gh pr update-branch <pr>`（strict OFF 後は通常不要）、(b) `gh pr checks <pr> --watch --interval 30`（必須 7 本の success か failure まで）、(c) 最終 head の sweep `scripts/pr-feedback.py <pr> --json .orchestration/validation/<task>-pr-feedback.json`、(d) `dispositions.py` の候補生成、(e) `local-review.sh` と `local-advisory.sh` を実行して validation に保存、(f) `.orchestration/validation/audit-queue/<task>-<head>.request` を置く、(g) `audit-<head>.json` が現れるまで待つ（上限 30 分、超えたら exit 4）、(h) 各 step の command・exit code・時刻を `.orchestration/validation/<task>-integrate-<head>.log` に書く。
- 出力と終了コード: 全 step 完了で exit 0（orchestrator が verdict.sh を実行できる状態）。CI 失敗は exit 3（step 名を stderr に）、監査待ち超過は exit 4、それ以外の失敗は exit 1。Bot は待たない。`gh pr merge` は呼ばない。
- テスト `tests/unit/test_integrate_seat.py`: fake gh と fake audit-pool で全 step の順序と証跡ファイル名；CI 失敗で exit 3；監査タイムアウトで exit 4；merge を呼ばないこと。
