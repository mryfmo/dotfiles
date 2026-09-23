# refkit-P7: 報告

## 概要

ST／UAT の残存欠陥（G-17〜G-21）、UT／CT の残存欠陥（F-06・数値主張）、および P3 由来の ACT-006 対応（UAT の E151）を修正した。対象：`references/st/ST_SAMPLE.md`、`references/st/ST_GUIDE.md`（変更なし。理由は下記）、`references/uat/UAT_SAMPLE.md`、`references/uat/UAT_GUIDE.md`、`references/ct/CT_GUIDE.md`（§1 のみ）、`references/ct/CT_SAMPLE.md`（§8 のみ）、`references/ut/UT_SAMPLE.md`（§1・§4・§5 のみ）。

## 実施した変更

### 1. G-17: k6 の負荷モデル（ST_SAMPLE.md §9）

- 4 操作（一覧・詳細・提出・決裁）を反復ごとに 25%均等抽選する構成に変更。
- `warmup`（`ramping-arrival-rate`、0→20 件/秒・5 分）→ `nvt_001`（`constant-arrival-rate`、20 件/秒・30 分、`startTime: '5m'`）の 2 シナリオ構成にし、5 章の「20 件/秒、30 分、暖機 5 分」という記述と一致させた。
- 操作別の閾値 `http_req_duration{op:list|detail|submit|decide}: p(95)<800` を 4 本とも明示。`http_req_failed`・`dropped_iterations` は既存のまま維持。
- 決裁（decide）は `detail` 呼び出しで得た内容版（`revision`）を `seenRevision` として送り、要求識別子は `${__VU}-${__ITER}-${Date.now()}` で毎回新規に生成（同一要求の再送とは区別される）。
- 検証：`node --check` で構文確認（下記「検証」参照）。`k6 inspect` は k6 がインストールされていない（`which k6` は何も返さない）。導入には mise 等でワークツリー外に書き込みが必要になるため、本タスクでは実行せず「未実行」と明記する（task_file の条件「without writes outside the worktree」を満たせないため）。

### 2. G-18／G-19: 認証方針の一貫性と NVT ゲート（ST_SAMPLE.md §3・§6・§7・§8）

- §3・§6 の矛盾（§3「認証状態を主体ごとに保存して再利用する」対 §6「テストごとに新しい組織と認証状態を使う」）を解消。§6 を「テストごとに新しい組織を使う（認証状態は 3 章の通り主体ごとに再利用する）」に変更し、§3 の記述（Playwright の公式パターンに合致：ワーカーごとに認証を 1 回行い再利用、データはテストごとに新規）を正本として残した。
- §3 に新しい行「テスト専用の入口」を追加し、`clock`（時計操作）と `seed`（申請作成）を本番未配備の検証専用入口として明記。
- §3 テストデータ行に「申請の状態は作成後に提出などの操作を積み重ねて作る（テスト専用の入口で状態を直接指定しない）」を追記し、9 章の Playwright 例（下記）と整合させた。
- §7 G2 行に「NVT-001 は本番相当の規模での非暫定の結果を必要とする（3 章の暫定の注記）。それが無い場合は判定者が逸脱を明記して判断する」を追記（G-19：3 章の「暫定」注記がゲート条件に反映されていなかった問題）。
- §8 実行の契機行の NVT-004 に「（初回は G3 判定前に完了する）」を追記（四半期演習の初回実施を G3 の前提条件として明示）。
- Playwright 例（§9）：`state: 'SUBMITTED'` を直接指定する呼び出しを、`/api/test-support/seed` での作成 → `/api/applications/{id}/submit`（実物の提出操作）の 2 段階に変更。

### 3. G-20／G-21: PT 実施者と CT 用語（UAT_SAMPLE.md §5、UAT_GUIDE.md §6、CT_GUIDE.md §1）

- UAT_SAMPLE §5：PT-001「品質担当と新任の審査者の 2 人組」→「新任の審査者 2 名」、PT-003「品質担当」→「申請業務の利用者 2 名」に変更（品質担当が実施者を兼ねていた問題を解消。PT-002・PT-004 は既に実際の利用者・業務代表だったため変更なし）。
- §5 表の直後に「実施者は実際の利用者・業務代表とする。品質担当が同席する場合は進行役に限り、操作しない（UAT_GUIDE.md 6 章）」を追記。
- UAT_GUIDE §6 の運用表に新しい行「実施者」を追加し、上記方針の根拠を記載（§2・§9 は実質的な変更なし。§2 は進め方のフロー、§9 のレビュー観点はいずれも既に実施者と判定者の独立性を問う内容であり、本変更と矛盾する記述は見つからなかったため、そのまま維持）。
- CT_GUIDE §1：「日本の開発現場で『結合テスト』と呼ばれるものの前半（内部結合）に当たることが多い」という一文を削除。ISTQB CTFL v4.0.1 のシラバスは「結合テスト」という日本語通称や「前半＝内部結合」という区分を用いておらず、WebSearch で見つかった候補（AIQVEONE・Qbook・SHIFT・MagicPod 等の解説記事）はいずれも二次的な商用ブログで、JSTQB の一次資料（用語集・シラバスの原本ページ）を直接確認できなかった。task_file 自身が定める代替手段（一次資料が無ければ削除）に従った。
  - 参考として、02_RESEARCH_AND_DECISIONS.md に追加する場合の S-row 案（本タスクの scope 外のため実装はしていない）：
    `| S-XXX | JSTQB用語集は「結合テスト」を定義せず、統合テスト／コンポーネント統合テストを使う。日本現場の「結合テスト」との対応は組織依存 | 02_RESEARCH_AND_DECISIONS.md | JSTQB公式用語集（未確認：一次資料への直接アクセスができなかったため保留） |`

### 4. ACT-006／E151（UAT_SAMPLE.md）

- task_file は追加場所を「4 章（主体の扱い）」と指定しているが、UAT_SAMPLE.md に 4 章という見出しは存在せず、ACT-005 の同種の除外記述は §1「対象と正本」の「対象外の主体」行にある。task_file のこの参照は誤り（あるいは別文書の章番号との混同）と判断し、実在する §1 の同じ行に、task_file が指定した文言をそのまま追記した：
  「ACT-006（システムの予定処理）は人が操作しないため受入シナリオ・ペルソナの対象外。期限処理の確認は UT-017/UT-018・CT・NVT-009 で行う」
- `kit_lint.py check` で E151 が解消したことを確認（下記「検証」）。

### 5. 数値主張の是正（UT_SAMPLE.md §5、CT_SAMPLE.md §8）

- UT_SAMPLE §5「UT 全体で 10 秒以内」→「UT 全体の所要時間は証跡 `durations` を参照」。
- CT_SAMPLE §8「1 秒未満」→「所要時間は証跡 `durations` を参照」（E158 が検査する「29 件」「94.4%」は変更していない）。
- **既知の逸脱**：`evidence/example_tests.json` には現時点で `durations` キーが存在しない（grep で確認済み）。task_file が指定したこの文言は、将来（別フェーズ、P2-C 相当）で証跡にこのキーが追加されることを前提にした将来参照であり、現時点で機械検証可能な事実ではない。数値の目測（「10 秒以内」「1 秒未満」）という検証不能な主張を残すより、証跡キーへの参照という検証可能な形に置き換える方が適切と判断し、task_file の指示通り実施した。この逸脱は後続フェーズへの引継ぎとして下記「下流への波及」に記載する。

### 6. F-06（UT_SAMPLE.md §1・§4）

- §1 対象外行に、FR-005・FR-009・FR-026 の扱いを追記（由来行は変更していない。由来行を変更すると `check_cross` 相当の網羅チェックが新たな UT-\* 引用を要求し、存在しないテスト条件の追加を強制することになるため、由来行はそのままにして「対象外」の説明を拡張する形にした）：
  - FR-005（提出前後の編集拒否）：P6 で UT に追加予定。
  - FR-009（AI 応答のタイムアウト時の扱い）：CT で代役のタイムアウトを注入して確かめる（現時点で未実装。CT_SAMPLE.md に FR-009 の記述が無いことを grep で確認済み）。
  - FR-026（時刻の記録）：NVT-011（CT_SAMPLE.md §5 に既存の「未自動化（参考実装に FR-026 が無い）」と一致する記述）で確かめる。
- §4「プロパティベーステストの乱数」行：現在の `conftest.py`（`examples/flowapprove_core/tests/.../conftest.py`）には Hypothesis の `derandomize` やデータベース設定が無い（直接確認済み）ため、再現性の主張を条件付きに変更：「再現性が保証されるのは `conftest.py` にプロファイル `kit`（乱数の固定とデータベース設定）を追加した後（6 章）で、本参考実装には未導入」。

## task_file からの意図的な逸脱（技術的根拠つき）

1. **ACT-006 の追加場所**：task_file は「4 章（主体の扱い）」を指定するが、実在するのは §1「対象と正本」の「対象外の主体」行。存在しない章を作らず、ACT-005 と同じ実在の行に追記した。E151 は文書内のどこかに ID が部分文字列として現れることだけを検査するため、機能上は等価。
2. **UT_SAMPLE §1 の F-06 回答場所**：`scope` は「§1 … prose only」（行の追加ではなくセル内テキストのみ）と明記されているため、新しい行を追加せず、既存の「対象外」セルにテキストを追記した。
3. **`durations` 証跡キーが未実装**：CT_SAMPLE §8／UT_SAMPLE §5 の新しい文言が参照する証跡キー `durations` は `evidence/example_tests.json` に現時点で存在しない。task_file の指示通りに文言を入れたが、これは将来のフェーズ（証跡生成）で実装されるまで検証不能な将来参照であることを明記する。
4. **CT_GUIDE §1 は削除、S-row は追加せず**：一次資料を直接確認できなかったため、task_file が示す 2 つの選択肢のうち「削除」を採用。S-row の追加は `02_RESEARCH_AND_DECISIONS.md` の編集を要し、本タスクの `allowed_files` に含まれないため、提案文言のみ本報告書に記載した。
5. **k6 inspect／tsc --noEmit を実行せず**：k6・typescript・@playwright/test はいずれもこの環境にインストールされていない。`npx --no-install` で確認済み。インストールには mise／npm のネットワーク取得が必要で、これは task_file が課す「installable … without writes outside the worktree」の条件を満たさない（mise はワークツリー外の共有ツールディレクトリに書き込む）ため、両方とも「未実行」とした。

## 下流への波及

- `durations` 証跡キーが `evidence/example_tests.json` に無い（UT_SAMPLE §5・CT_SAMPLE §8 が参照する）。証跡生成フェーズで追加が必要。
- CT_GUIDE §1 に一次資料（JSTQB 公式用語集）を追加する場合の S-row 案を「実施した変更」3 節に記載した。`02_RESEARCH_AND_DECISIONS.md` の編集が必要（本タスクの scope 外）。
- FR-005 の UT 追加は P6 に依存（すでに P6 スコープに含まれている前提）。
- k6・playwright・typescript のインストールは本タスクでは行っていない。`node --check` のみ実施。将来 CI 等でこれらのツールチェーンが使えるようになった際に `k6 inspect`／`npx tsc --noEmit` を追加で実施することを推奨する。

## 検証

- `kit_lint.py check`：E151 が解消し、残るエラーは `E120`／`E121`／`E103`(×2) のみ（いずれも P9 まで許容されている生成物の陳腐化）。新規エラーは 0 件。
- `node --check` on 抽出した k6 スクリプト：合格。
- `npx tsc --noEmit` on 抽出した Playwright TS：typescript／@playwright/test が未インストールのため未実行。
- `git diff --stat`：6 ファイル、64 行追加・15 行削除。意図した箇所のみの変更であることを diff で目視確認済み（Bash 経由の Python スクリプトで編集し、Claude Code の Edit/Write/MultiEdit は使用していない）。

## コミット

`docs(references/tests): fix ST/UAT samples (k6 model, auth policy, gates, PT actors) and record ACT-006 exclusion`

## cost

4 research subagents (parallel, read-only) + 1 primary session. 編集は Bash 実行の Python スクリプト 3 回（プロース、コードブロック、修正）。
