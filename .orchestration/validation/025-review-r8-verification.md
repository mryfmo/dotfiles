# Plan 025 round 8 検証審査（perspective T: v8 と round-7 処分表の照合、W0c 書き換えと保護パス反転後の全体整合）

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v8（`shasum -a 256` prefix `e1f2e400`、`wc -l` 341、どちらも一致を確認してから読んだ）、`025-review-r7-dispositions.md`（26 行）、`025-review-r7-verification.md`（R-01〜R-13）、`025-review-r7-redteam.md`（S-01〜S-13）、handout `pilot/leg1.md`（111 行）/`leg2.md`（114 行）/`srt-{worker,audit,orchestrator}.json`/`events.ts`/`policy.yml`、`gh-actions-facts.md`（F1〜F4）、`decisions.tsv` D-024-115〜119、`.github/workflows/*`（8 本の `on:`/`permissions:`/job 名/`secrets.` 参照）、`Makefile` L189、`.gitignore`、`git ls-files` による除外一覧のパスの棚卸し。
- 方法: 読み取りのみ（Read/`sed -n`/`grep`/`jq`/`git ls-files`）。席・網・GitHub API・端末 pane には触れていない。書いたのは本ファイル 1 本。約 30 分の枠。届かなかった検査は §6 に 未確認 として挙げる。
- 様式: 手順は番号と名前で指す。資格情報を扱うコマンド行と settings の JSON 本文は貼らない。

## 1. 26 行の照合（欠落・部分・矛盾のみ）

26 行のうち 23 行は名指しの節・handout 手順に存在し、隣接する節と矛盾しなかった（§5 に列挙）。以下の 3 行だけが部分または矛盾。

| id | 処分 | 状態 | 何が足りないか |
| --- | --- | --- | --- |
| R-03 | fixed-in-v8 §3 W0c (2)、§2 Makefile 行、§7 W0c PR 行 | 部分 | 本文の 3 箇所は §3 W0c (2)・§2 L56・§7 L215 に揃って入った。完了条件 `grep -c -- '--no-project' Makefile` = 3 は成立しない: `grep -c` は一致**行**を数え、`UV_PYYAML` の `uv run` 3 箇所は `Makefile` L189 の 1 行にある（今日の値は 0、修正後は 1）。→ T-04 |
| S-12 | fixed-in-v8 §4 #7（設定 2 行、JSON は別文脈） | 矛盾 | 計画 §4 #7（L169）は「`seat-audit` は本番の `<seat dir>` と同じく denyRead の内側を `allowRead` で開けた形に置く（設定 2 行、S-12）」と書くが、`srt-audit.json`（mtime 03:11、v8 より前のまま）の `allowRead` は空で `denyRead` に `seat-audit` は無い。`leg2.md` #7 の期待文はむしろ「pilot が測るのは `$PILOT` 直下の `seat-audit` への create 拒否だけで、本番形での同じ canary は W5b の描画試験が持つ = S-12」と測定の先送りを明記する。計画と handout が逆を言う。→ T-03 |
| R-01 | handout-only `leg2.md` #8b + 計画 §4 #8b/§9 Q-08 行 | 部分（軽微） | #8b は handout・§4 ともにあり、`Q08-PASS-shim`/`Q08-FAIL-real-omp`、私設 store の `.tmp/launch`、pilot3 の kill まで一致。処分表が言う「§9 Q-08 行に launch dir `<HCOM_DIR>/.tmp/launch` を名指し」だけは §9 行（L256）に無く §4 #8b 行にだけある。実害は無い（§9 行は owner を #8b と指す） |

residual 2 行（R-05/S-04）は owner = 操作者、決定 (11)、測定 = boundary ごとの `gh secret list --app actions` が §9 L255・§11 #22・Status log v8 の 3 箇所で一致。

## 2. 全体整合

### 2.1 W0c 行 (0)〜(4) と workflow の実体

- `macos.yaml`/`ubuntu.yaml`: `on: push: branches: [main]` + `pull_request`（L3-27）、単一 job `build`（L32）、secret は `env:` の `HAS_*` 判定と `ssh-agent`/`EMAIL_ADDRESS`/`MY_DOTFILES_BENCHMARK` の step にだけ現れ、どの job にも `environment:` は無い【実測】。W0c (2) の「PR job（`environment:` 無し）と main-push job（`environment:` + `if: github.event_name == 'push'`）に分ける」は実体と整合する。`push` は `main` だけなので `if:` は PR run で job を skip させるだけで、統制が branch rule にあるという (2) の但し書きも正しい。
- `private-bootstrap.yaml`: `on: push: branches: [main]`、`workflow_dispatch`、`schedule`（L5-10）、job 1 本（matrix 3）。deployment branch rule `main` のみの environment を付けたとき: `schedule` の `GITHUB_REF` は default branch（= `refs/heads/main`）、`workflow_dispatch` は選んだ ref。よって週次と `main` への dispatch は通り、他 ref への dispatch は job が拒否される = S-03 の意図どおり。W0c の `threat_table` 行（`workflow_dispatch` = closed、`schedule` = closed）と整合。
- `docs.yml`: `workflow_dispatch` + `push: branches: [main]`、`permissions: contents: write`、job `deploy`（L3-27）。environment を付けると他 ref への dispatch で job 自体が拒否されるので S-03 の「攻撃者 ref の file が `contents: write` の token で走る」は閉じる。`GITHUB_TOKEN` は environment secret ではないが、拒否されるのは job なので関係しない。整合。
- `test.yaml`: `pull_request` の upload step に `CODECOV_TOKEN`（L425）、`agent-assets.yml`/`remote.yaml` は `contents: read` で `secrets.GITHUB_TOKEN` だけ【実測】。§2 L43、§9 L255、決定 (11)、W0c `threat_table` の `residual` 行と一致。
- 必須チェックの名: README の ruleset payload（L1176-1194）の 7 context は `validate`、`test (…)` ×3、`public-bootstrap (…)` ×3 で、`macos.yaml`/`ubuntu.yaml` の `build` は**入っていない**。計画 §3 W0c (0)「必須 2 チェックは PR でも main でも skip 経路だけを通る」、決定 (10)「必須 2 チェックが今日 PR でも main でも空」、D-024-117 の同文は、この記録と矛盾する。→ T-05。`build` が必須でなければ job 分割は ruleset に触れないので W0c には好都合だが、「品質項目」の根拠文が変わる。必須なら逆に「PR job は必須 context の名を保つ」が (2) に要る。第 1 脚 #0 の貼り付けで決着する。
- (4) の否定の測定: macos/ubuntu の PR run は `if: push` で environment job を評価しないので、素直な PR run からは「skipped」しか出ず拒否行は出ない。拒否行が出るのは `private-bootstrap.yaml`（または `docs.yml`）を使い捨て ref へ `workflow_dispatch` したとき、または使い捨て PR の file から `if:` を落としたとき。(4) は「`workflow_dispatch` または PR run」と書くだけで、どちらをどう起こすかを言わない。→ T-11。
- (1) の貼り付け欄（§7 L214）: `--jq .deployment_branch_policy` が返すのは `{protected_branches, custom_branch_policies}` の 2 真偽値で、`main` という pattern は `deployment-branch-policies` の副資源にある。→ T-07。
- `Makefile` L189: `uv run` は probe と 2 分岐の 3 箇所、全部 1 行【実測】。R-03 の本文は正しく、完了条件だけが誤り（§1、T-04）。

### 2.2 §1.6 の反転と各節

- §1.6（L32）→ §3 W5a（render テストが除外一覧を読み `home/dot_agents/**` が保護であることを固定）、W5b（`home/dot_local/bin/**` が除外に当たらない）、W6a（除外に無いパス 1 つで保護、語一致無し、fixture に git/ccstatusline/`.chezmoiroot`/既存 `*.tmpl` 1 行）、§7 保護パス行（L234: `*.tmpl`・`home/dot_config/git/**` を必読に）、§9 G-07 行（L261）、決定 (6)、§11 #19/#21 は同じ文で一致。「保護」の 2 つの意味（W0b 前 = 受け入れ記録の `operator_diff_read: <head40>`、W0b 後 = 操作者 account の `APPROVED`）は §1.6 で定義され、§3 W6a・§7・§11 #19・決定 (6) が同じ 2 分岐を使う。§1.5/§1.10 の W0a/W0b の時期（W0b = X 手順 5b）とも矛盾しない。
- 除外一覧の中身と「操作者側プロセスが実行・読込しないパス」という定義の照合【実測 `git ls-files`、`.gitignore`】:
  - `.orchestration/**`、`docs/**`（非 md は `docs/assets/stylesheets/extra.css` 1 本）、`.ua/**`、`.project-map/**`（`.gitignore` L26 で全体が無視）: 定義どおりデータと散文。
  - `tests/**`: `tests/unit/*.py` は `make unit-test` がどこで打たれても実行する（CI では確実）。AGENTS.md の Test Policy は bats を CI 限定にするが unittest には触れていない。定義に 1 文の前提（操作者端末で `make unit-test` を打たない、または打つなら差分を読む）が要る。→ T-12（P3）。
  - `.agents/worklog/**`: `.gitignore` L9 で木全体が無視され、追跡 file は 0 本。一方で計画自身が、ここに **席の sandbox 設定の描画先 `srt-seats/<name>/{settings.json,bin,omp}`**（§1.2）、**private hcom の実体 `uv-tools/hcom`**（§1.5、F-04）、`uv-cache`（§6 項目 9）、J-N2 で sandbox の外から実行する glue 2 本（§7 L217）、`omp-run/<results dir>` を置くと書く。つまり定義（どの操作者側プロセスも実行・読込しない）に最も反するパスが除外一覧に載っている。追跡 0 本なので除外しても何も「許可」していないが、`git add -f` で追跡に乗せた PR はこの一覧では保護にならず、gitignore という本当の理由は §1.6 に書かれていない。除外から外しても失うものは無い（fail-closed）。→ T-01（P1）。
  - `home/` の外の `*.md`【実測 43 本】: `README.md`、`plans/*.md`、`tests/fixtures/**/*.md`、`vendor/compactiondb/**/*.md` は散文。しかし `AGENTS.md`・`CLAUDE.md`（repo root）も一致し、これらは hold 中の Claude pane（sandbox の外）が instructions として読み、omp 席は `AGENTS.md` を cwd から祖先へ walk-up で読む（§1.7 L33【V-16】; §9 L279 自身が「local review/audit は PR の `AGENTS.md` を読む」と書く）。prompt を実行入力と見るなら定義に反する。さらに「例として … repo root の `.omp/` … は保護」と `*.md` 除外が `.omp/AGENTS.md` で衝突し、どちらが勝つかの規則が §1.6 に無い（chain の判定は「除外に無いパス 1 つで保護」の 1 文なので、`*.md` 一致 = 除外 = 非保護になる）。→ T-02（P1）。
- §1.7 (4) の `-r2` 規則（`ps -p <pid>` exit 1 のときだけ、`<results dir>-r2`/`<name>-r2`/`<HCOM_DIR>-r2`）と §1.2 の `<name>`（= `<seat dir>`）の `-r2`、W6a の 2 fixture（旧 nonce の行しか無い = `blocked`、`ps -p` 0 なら `-r2` を作らず block）、§4 #7 の `ps_exit` は一致。
- §1.9 の sha 突合: squash merge では `gh pr view <n> --json mergeCommit` の `mergeCommit.oid` が main 上の squash commit を指すので、意味は正しい。字面は object を返すので `.mergeCommit.oid` と書くべき。→ T-08（P3）。
- §2 の数: 表は L42-91 の 50 行。残す 10（L43,45-52,54）、残す／変える 2（L42,44）、変える 16（L55-67,69-71）、捨てる 13（L68,72-81 の 11 + L82 書換 + L83 昇格）、新規 8（L84-91）、混合 1（L53）= 50。L93 の集計と一致。
- §7 採択行の順と §3 の鎖: 採択行「W1 ‖ W3 → W2、W0a は並走; W0c は W2 の後」は §3 前書きと一致（R-09）。ただし表の行順は W0c (1)/W0c の PR/W0c (3) が「今（W1）」「W0a」「A-2 merge 直後」より前に置かれ、見出しの「時期ごと」と合わない。→ T-09（P3）。
- §8 STOP「CI の secrets」と §9 決定 (10)/(11): 同じ 3 文（repository-level secret は足さない / secret は environment だけ / W0c merge 前に secret を設定しない）と `CODECOV_TOKEN` = 決定 (11) で一致。v7 の「W0c だけ例外」文は無い【`grep` 0 件】。
- §9 決定 (1)〜(11) と `decisions.tsv`: D-024-116 が (10) の番号訂正、D-024-117/118 が (11) の新設と既定 = 受容、D-024-119 が「(1)-(11)」と記す。一致。
- §11 1〜22 と決定: #19→(6)、#20→(7)、#21→(10)、#22→(11)、#18→(5)、#5→(4)。一致。
- 定義前の用語: `operator_diff_read`（§1.6 で定義、§3 W6a で使用）、`protected-paths.txt`（同）、`ps_exit`/`Q08-PASS-shim`（§4 #7/#8b で定義）、【gh Fn】（L5 で facts file を名指し）はいずれも定義が先。`private-dotfiles` は §2 L44 が §3 W0c より先に使うが同じ行で「deployment branch rule `main` のみ」と説明されている。
- Status log v8（L341）: fixed 18 id、residual 2、handout-only 6 = 処分表の 26 行と id 単位で一致。

## 3. handout の一致

- `leg1.md`: §4 第 1 脚 #0a〜#18 の各コマンドが同じ flag と順で存在。#0 の 2 段 + `can_approve_pull_request_reviews`、#0b の keychain 2 種別と helper 2 段、#4 の 7 鍵と 4 モデル、#5 の flag 行、#6 の `sed` 置換、#6b の import/login 分岐と `sk_ant_count`（import 直後、R-06）、#7 の probe と再実行規則、#10 の `NAME-EMPTY`、#11/#11b/#13/#14 の TASK 文、#15 の `PILOT_LOG empty`、#17 の transcript の exit 判定、#18 の残置一覧。`wait_result` の pattern は `task_id=$1 %`（R-12）。
- `leg2.md`: #0（`M=` 独立行、`__MAIN__` の `sed`、実体の種別）、#0f（`shimok`/`wait_result` = `task_id=$1 %`）、#1〜#3c、#4（`mkshim`: 9 tool + `omp` の link、HCOM_* 7 名、`GIT_CONFIG_NOSYSTEM=1`、`PILOT_LOG` と debug log は役割 tmp）、#4a〜#4c、#5（16 項目、helper 1 段の期待）、#6、#7（`N`/`launch_ts` は `{ … } | tee` の外の main shell の独立行 = R-04; store 4 file の検査を起動後と events/kill ブロック先頭で 2 回 = R-11; `ANAME` は私設 store から; `ps_exit` = S-09; JSONL は `-exec ls -t {} + | head -1` = R-07）、#8（`wpid` ガード、errno probe、pilot3 の起動と kill）、#8b（`export HCOM_LAUNCHED=1`、私設 store の `.tmp/launch` の最新 runner、`Q08-PASS-shim`/`Q08-FAIL-real-omp`、pilot3 の kill = R-01）、#9、#10（`hcom-audit/config.toml`、`out/cwd2`、`seat-audit/forbidden.txt`、`~/.agents/pilot-should-fail-15`、`sessions-renamed`、`should-fail`、全席 kill 後の `pgrep`）。§4 第 2 脚の表と flag・順・期待が一致。
- 内部整合: 変数と関数は使用前に定義（`M`→#0、`shimok`/`wait_result`→#0f、`mkshim`→#4、`ANAME`→#7 の独立行）。subshell 内の `exit 1`（#7 の再検査、#8 の `WPID-EMPTY`）は pipeline 左側の `{ … }` だけを抜ける。#0 の `sed -i` は再実行しても無害（置換済み）。
- 計画 §4 #7 と `srt-audit.json`/`leg2.md` #7 の不一致 = S-12（§1、T-03）。
- `srt-worker.json`/`srt-audit.json`/`srt-orchestrator.json` は `jq -S .` を通る（3 本とも valid）。orchestrator の `denyWrite` は 18 項（D-024-116 の記述と一致）、worker/audit の allow-list は `agent/{sessions,blobs,cache,history.db,agent.db}` + `run`、`cache/eval-js` は denyWrite、audit は `out/cwd` と私設 store 6 項を denyWrite、`allowLocalBinding: false`。`policy.yml` は §4 #8 の 3 要素、`events.ts` は §4 前書きの仕様（try/catch、`task_id=` の後方走査、`PILOT_STOP_N`、probe 語）に一致。
- handout の見出しと末尾は両脚とも「plan 025 v6 §4」のまま（計画 §4 前書きは「v8 で更新」）。R-08 が「見出しは別文脈」としたが直っていない。→ T-10（P3）。

## 4. 所見表

| id | priority | file and section | problem | evidence | fix |
| --- | --- | --- | --- | --- | --- |
| T-01 | P1 | plan §1.6（L32）除外一覧、決定 (6)（L291）、§11 #19 | `.agents/worklog/**` を除外に入れると、計画自身が置く実行入力（`srt-seats/<name>/{settings.json,bin,omp}` = 席の sandbox 設定と shim、`uv-tools/hcom` = private hcom の実体、`uv-cache`、J-N2 で sandbox 外から実行する glue 2 本）が「操作者側プロセスが実行・読込しないパス」という除外の定義と矛盾する。追跡 file は 0 本（`.gitignore` L9）なので除外は何も許していないが、その理由は書かれておらず、`git add -f` の PR には一覧が効かない | `.gitignore:9`、`git ls-files .agents/worklog` = 0、plan §1.2 L20（`<seat dir>` = `<main>/.agents/worklog/srt-seats/<name>/`）、§1.5 L31（`uv-tools/hcom/bin/hcom`）、§6 項目 9 L200、§7 L217 | `.agents/worklog/**` を除外一覧から外す（失うものは無い）。残すなら §1.6 に「gitignore で追跡 0 本が前提」と書き、`validate` job に `git ls-files .agents/worklog` が空である 1 検査を足す |
| T-02 | P1 | plan §1.6（L32）除外一覧「`home/` の外の `*.md`」、§9 L279、§1.7 L33 | `AGENTS.md`・`CLAUDE.md`（repo root）が除外に一致する。これらは hold 中の Claude pane と omp 席（walk-up【V-16】、§9 L279「local review/audit は PR の `AGENTS.md` を読む」）の instructions = 実行入力であり、除外の定義に反する。さらに同じ glob は `.omp/AGENTS.md` にも当たり、「repo root の `.omp/` は保護」の例文と衝突するが、優先規則が無い（判定は「除外に無いパス 1 つで保護」の 1 文） | `git ls-files '*.md'` の root 3 本（`AGENTS.md`、`CLAUDE.md`、`README.md`）、plan L32 の例文と除外文、L33、L279 | `*.md` の除外を名指しに絞る: `README.md`、`plans/**`、`vendor/**/*.md`（`tests/**`・`docs/**`・`.orchestration/**` は既に subtree で除外）。`AGENTS.md`/`CLAUDE.md`/`**/AGENTS.md` は保護と 1 文で書き、W6a の fixture に「`AGENTS.md` 1 行変更の PR → `refuse 10`」を足す。除外と例文が重なったときは保護が勝つと明記 |
| T-03 | P1 | plan §4 第 2 脚 #7（L169）vs `pilot/srt-audit.json`、`leg2.md` #7 期待文 | 計画は「`seat-audit` を denyRead の内側を `allowRead` で開けた形に置く（設定 2 行、S-12）」と fixed-in-v8 として書くが、`srt-audit.json`（mtime 03:11、`allowRead: []`、`denyRead` に `seat-audit` 無し）は変わっておらず、handout #7 は「本番形での同じ canary は W5b の描画試験が持つ = S-12」と先送りを明記する。計画と handout が逆 | `srt-audit.json` の `allowRead`/`denyRead`、`leg2.md` #7 期待文、処分表 S-12 行「JSON の変更は別文脈」 | どちらかに揃える: (a) `srt-audit.json` に `~/pilot-20261022/seat-audit` を denyRead と allowRead に 1 行ずつ足し #7 で測る、または (b) 計画 §4 #7 を handout の文に直し、処分表の S-12 を `residual（owner = W5b の描画試験）` に書き換える |
| T-04 | P2 | plan §3 W0c 完了条件（L102）、§2 L56 | `grep -c -- '--no-project' Makefile` = 3 は成立しない。`grep -c` は一致行数で、`UV_PYYAML` の `uv run` 3 箇所は L189 の 1 行（今日 0、修正後 1）。R-03 の本文は入っているが受理検査が誤り | `Makefile:189`【実測】、`grep -c` の今日の値 0 | `grep -o -- '--no-project' Makefile \| wc -l` = 3（または `sed -n 189p Makefile \| grep -o -- '--no-project' \| wc -l` = 3） |
| T-05 | P2 | plan §3 W0c (0)（L102）、決定 (10)（L291）、D-024-117 vs README ruleset payload | 「必須 2 チェック（macos/ubuntu）は PR でも main でも skip 経路だけ」と書くが、README の payload（L1176-1194）の 7 context は `validate`、`test` ×3、`public-bootstrap` ×3 で `build` は無い。必須でなければ「必須チェックが空」という根拠文が崩れ（品質項目の性格は残る）、必須なら W0c (2) に「PR job は必須 context `build` の名を保つ」が要る（job 名を変えると必須 context が永久 pending） | README L1176-1194、`macos.yaml:32`/`ubuntu.yaml:32`（job `build`）、plan L102/L291、D-024-117 | 第 1 脚 #0 の `required_status_checks` 貼り付けで決着し、文を実値に直す。必須なら W0c (2) に context 名の保持を 1 句 |
| T-06 | P3 | plan §7 W0c (1)（L214） | `gh api repos/<owner>/<repo>/environments/private-dotfiles --jq .deployment_branch_policy` は `{protected_branches, custom_branch_policies}` の 2 真偽値しか返さず、`main` という pattern は見えない | GitHub REST の environments 資源の形（`deployment_branch_policy` と `deployment-branch-policies` は別資源） | 貼る欄を `…/environments/private-dotfiles/deployment-branch-policies --jq '.branch_policies[].name'` = `main` の 1 行にする |
| T-07 | P3 | plan §1.9（L35）、§7 見出し | `gh pr view <n> --json mergeCommit` は object を返す。突合の対象は `.mergeCommit.oid` | `--json` の出力形 | 「`gh pr view <n> --json mergeCommit --jq .mergeCommit.oid`」に |
| T-08 | P3 | plan §3 W0c (4)（L102）、§7 W0c PR 行（L215） | 否定の測定「PR run を起こし拒否行を貼る」は、PR job の `if: push` が environment job を評価させないので skipped しか出ない。拒否行が出るのは `private-bootstrap.yaml`/`docs.yml` を使い捨て ref に `workflow_dispatch` したとき、または使い捨て PR の file から `if:` を落としたとき | `macos.yaml`/`ubuntu.yaml` の trigger（`workflow_dispatch` 無し）、W0c (2) の `if:` | (4) を「`private-bootstrap.yaml` を使い捨て branch へ `gh workflow run --ref` し、environment の拒否行を貼る」と 1 つに決める |
| T-09 | P3 | plan §7 表の行順（L213-218） | W0c (1)/W0c の PR/W0c (3) の 3 行が「今（W1）」「W0a」「A-2 merge 直後」より前にあり、見出し「時期ごと」と §3「W2 の後」に合わない | L213-218 | 3 行を「B-2 merge 直後」の後ろへ移す |
| T-10 | P3 | `leg1.md` L1/L111、`leg2.md` L1/L114 | 見出しと末尾が「plan 025 v6 §4」のまま（計画 §4 前書きは「v8 で更新」、R-08 は「別文脈」とした） | handout の当該行 | 「v8」に |
| T-11 | P3 | plan §1.6（L32）除外 `tests/**` | `tests/unit/*.py` は `make unit-test` が打たれた場所で実行される。AGENTS.md の Test Policy は bats だけを CI 限定にし unittest には触れない。除外の前提が書かれていない | `Makefile:186`、AGENTS.md Test Policy | §1.6 に 1 文「`tests/**` の実行は CI と sandbox 内の `make unit-test` だけ; 操作者端末では打たない」か、`tests/unit/**` を除外から外す |
| T-12 | P3 | plan §9 Q-08 行（L256） | 処分表 R-01 が約束した「launch dir `<HCOM_DIR>/.tmp/launch` の名指し」が §9 行に無い（§4 #8b 行にはある） | L256 vs L171 | §9 行の測定欄に `<HCOM_DIR>/.tmp/launch` を 1 句 |

## 5. 確認できた行と一致した file

- 処分表 26 行のうち、名指しの節・handout 手順に存在し隣接節と整合した 23 行: R-02、R-04、R-06、R-07、R-08、R-09、R-10、R-11、R-12、R-13、S-01、S-02、S-03、S-04、S-05、S-06、S-07、S-08、S-09、S-10、S-11、S-13、R-05（R-01 は軽微な部分、R-03/S-12 は §1）。
- S-01/S-02 は §3 W0c (0)〜(4)、§2 L44、§7 L213-216、§8 L244、§9 L254、決定 (10)、§11 #21、Status log v8 の全部で同じ environment 設計（`private-dotfiles`、branch rule `main` のみ、reviewers 無し、PR job は `environment:` 無し、main-push/private-bootstrap/docs の job は付き）を言い、D-024-117/118 と一致。v7 の「W0c だけ例外」文は消えている。
- S-03 は §1.10 (b)（`actions`/`workflow` 無し）、§7 W0a (2)（`Token scopes` に `workflow` 無し、permission 一覧に `actions` 無し）、§3 W0c (2)（docs の write job）、§9 GitHub 境界行で一致。
- S-05〜S-08/S-11 と R-02 は §1.6・§3 W5a/W5b/W6a・§7 L234・§9 L261・決定 (6)・§11 #19/#21 で同じ反転規則。template の語一致はどの節にも残っていない。
- S-09/R-10 は §1.2・§1.7 (4)・§3 W6a・§4 #7 で一致。S-10/S-11 は §1.9 に、S-13/R-13 は W0c `threat_table` と §9 L254 に、R-05/S-04 は §2 L43・§9 L255・§11 #22・決定 (11) に、R-08/R-09 は §4 前書き・Status log v7・§3 前書き・§7 採択行にある。
- 一致した file: `leg1.md` と §4 第 1 脚の全 19 手順、`leg2.md` と §4 第 2 脚の全 15 手順（#7 の S-12 の 1 句を除く）、`srt-worker.json`/`srt-orchestrator.json`（§1.3 の worker/orchestrator 行と鍵集合・allow-list・denyWrite 18 項が一致）、`policy.yml`（§4 #8）、`events.ts`（§4 前書き）、`gh-actions-facts.md` F1〜F4（§3 W0c と決定 (10) の引用元）、`.github/workflows/*` の trigger/permission/job 名、`Makefile` L189 の 3 箇所、`.gitignore` と `git ls-files` による除外パスの存在（6 path 全部存在）。
- §2 の 50 行の内訳、§9 決定 (1)〜(11)、§11 1〜22、Status log v8 の id 集合は数え直して一致。

## 6. 報告（10 行）

1. 件数: P0 0、P1 3（T-01、T-02、T-03）、P2 2（T-04、T-05）、P3 7（T-06〜T-12）、計 12。round-7 の P0/P1（S-01/S-02/S-03/S-05/S-06/S-07/R-01/R-02）の修正はすべて名指しの場所にあり、欠落も逆向きの修正も無い。
2. 最重要 = T-01/T-02: 反転の設計は正しいが、除外一覧の初期値 2 項が §1.6 自身の定義に反する。`.agents/worklog/**` は席の sandbox 設定・shim・private hcom の置き場（gitignore で追跡 0 本という本当の理由が書かれていない）、`home/` の外の `*.md` は `AGENTS.md`/`CLAUDE.md` という instructions を除外し、`.omp/AGENTS.md` では例文と衝突する。どちらも一覧の 1 行と W6a fixture 1 本の修正で、設計には触れない。
3. T-03: S-12 は計画が「設定 2 行を置いた」と言い、`srt-audit.json` と `leg2.md` #7 が「W5b に先送り」と言う。どちらかに揃えるだけ。
4. T-04: R-03 の受理検査 `grep -c … = 3` は 1 行に 3 箇所ある `Makefile` L189 では 1 にしかならない。`grep -o | wc -l` に。
5. T-05: 「必須 2 チェック = macos/ubuntu」は README の ruleset payload（7 context に `build` は無い）と矛盾する。第 1 脚 #0 の貼り付けで決着し、必須なら W0c (2) に context 名の保持を足す。
6. W0c (0)〜(4) は workflow の実体（trigger、`environment:` の不在、secret の置き場、`workflow_dispatch`/`schedule` と `GITHUB_REF`、docs の write job）と整合する。残るのは測定の字面 2 点（T-06 の API field、T-08 の拒否行の起こし方）。
7. §1.7 retry と `-r2`、§1.9 の sha 突合、§2 の 50 行、§7 の採択順、§8 と決定 (10)/(11)、§9 の番号と `decisions.tsv`、§11 1〜22、用語の定義順、Status log v8 の id 集合は一致。
8. handout は両脚とも §4 と flag・順・期待が一致し、変数と関数は使用前に定義、main shell に要る行は pipeline の外、片付けは名指しの 5 項目を含み、JSON 3 本は valid。残りは見出しの「v6」（T-10）だけ。
9. loop は規則上は止められない（P1 3 件）。ただし 3 件とも除外一覧の 2 行・§4 #7 の 1 句（または JSON 2 行）の編集で、W0c の environment 設計、srt の役割表、W0、X の手順には変更が要らない。
10. 未確認: `hcom-seat` が `<seat dir>` を描画時に空にするか（T-01 の `git add -f` 経路の深さ）; ruleset の live な `required_status_checks`（README の payload が古い可能性、第 1 脚 #0 で決着）; chezmoi/mkdocs が `docs/**` を実行入力として読む経路の有無; `srt-*.json` と §1.3 の表の項目単位の完全照合（鍵集合・allow-list・denyWrite 18 項の数は確認、個々の denyRead 項の網羅は未確認）; GitHub docs の現在の文言（網を使っていないので `gh-actions-facts.md` の引用に依拠）。
