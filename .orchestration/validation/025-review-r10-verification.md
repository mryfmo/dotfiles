# Plan 025 round 10 検証レビュー（perspective X: v10 の round-9 処分照合と全体整合）

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` v10（`shasum -a 256` prefix `782f9024`、`wc -l` 349。どちらも一致を確認してから読んだ）。
- 入力: `025-review-r9-dispositions.md`（24 行）、`025-review-r9-verification.md`（V-01〜V-12）、`025-review-r9-redteam.md`（W-01〜W-12）、handout `pilot/leg1.md`（111 行）/`leg2.md`（115 行）/`srt-{worker,audit,orchestrator}.json`（鍵集合と denyRead の `~/.config/gh`・`__MAIN__` だけ `jq` で見た）/`events.ts`/`policy.yml`（v10 で不変、round 9 の一致を引き継ぐ）、`gh-actions-facts.md` F1〜F5、`decisions.tsv` D-024-120〜123、`.github/workflows/*`（trigger・`permissions`・`environment:`・`secrets.` 行の grep）、README の `main integration gate`（L1124/L1143/L1227）、`.gitignore` L1-40。
- 方法: 読み取りのみ（Read/`sed -n`/`grep`/`jq`/`awk`/`shasum`）。席・網・GitHub API・端末 pane には触れていない。書いたのは本ファイル 1 本。届かなかった検査は §6 に 未確認。
- 様式: 手順は番号と名前で指す。資格情報を扱うコマンド行と settings の JSON 本文は貼らない。
- D-024-123 の code-owner 規則（ruleset の「Require review from Code Owners」+ 保護 `.github/CODEOWNERS`）は v11 の予定として扱い、v10 に無いこと自体は欠陥としない。差し込み先は §2.4 に挙げる。

## 1. round-9 処分 24 行の照合（欠落・部分・矛盾のみ）

24 行のうち 23 行（fixed 22 + residual W-04）は名指しの節に在り、隣接する節と矛盾しない（§5 に列挙）。round-9 の P1 4 行（V-01/V-02/W-01/W-02）の修正はすべて名指しの場所にあり、欠落も逆向きの修正も無い。部分は次の 1 行。

| id | 処分 | 状態 | 何が足りないか |
| --- | --- | --- | --- |
| W-07 | fixed-in-v10 §1.6、§3 W6a、§11 #19 | 部分 | 規則の本体（A 作の PR は `.orchestration/` に自 task id の file だけ、`tasks/<自 id>.md` は不可、fixture 1 本）は 3 箇所に在る。ただし author の判定を「W0b 後は `gh pr view --json author`、W0b 前は head の committer」と 2 期に分けた部分が成り立たない: committer は席が自分の git 設定で書く値（worker の shim は `GIT_CONFIG_NOSYSTEM=1` で system を外すだけで user 設定は読み、`hcom-seat` は clone に committer 識別子を描かない = §1.1/§1.2）で、規則が狙う攻撃者 (1) がそのまま偽造できる。PR の author（token の identity）は W0b 前でも `gh pr view --json author` で取れ、A が存在する X 手順 5 以降は同じ検査で足りる; それより前（agmsg 席が操作者 token で PR を作る W2〜X）は A 作の PR が存在せず規則は空振りで、統制は orchestrator の読みだけ。→ X-02 |

residual W-04 は owner（W0a (3) の開いた測定）、測定（`.github/workflows/**` を触る PR の push と merge が B の token で通るか）、帰結の行（§1.10 (a)、§3 W0c 席欄/W9/経路外 D、§7「W0b 後の `.github/workflows/**` の変更」行、Status log）がそろう。D-024-123 はこの帰結を v11 で「B に Workflows write、操作者は author にならない」に置き換える予定で、v10 の行はその前の形として整合している。

## 2. 全体整合（3 識別子化後）

### 2.1 廃止語と再定義

- `reviewer store`: L278（「v9 の reviewer store は v10 で廃止」）、L344（Status log v5 の履歴）、L349（v10 の履歴）だけで、現行の規則文には無い。`gh-reviewer`: L36/L218/L349 の「置かない／作らない」だけ。
- 「操作者 account の merge token」: L32 と L3/L348 の「v9 では」の履歴だけ。「操作者 account の token」の現行の意味は全部「操作者自身の `~/.config/gh` にだけ置き全席 denyRead」（L25/L26/L36/L219/L236/L281/L297/L332）で一貫。
- 「web flow」: L36/L220 とも操作者自身の admin token の入れ方（操作者 store）の説明で、席には無い。
- A/B は L5（用語行）で定義され、§1.3（L25/L26）、§1.6、§1.10 (a)(b)(f)、§3 W0a、§7 W0a (1)(2)(3)/5b、§9、§11 #18 の役割が同じ: A = worker の PR author と push、B = boundary PR の author・push・merge、approve = 操作者。

### 2.2 §1.3 の merge store と §1.10 (a)/(b)

- worker 行: 席の gh dir = profile 配下（A）、orchestrator の merge store = `<main>/.agents/worklog/gh-orch`（B）は `<main>` の denyRead の内側; orchestrator 行: 同 store = B の fine-grained token; audit 行: `~/.config/gh` denyRead（gh を使わない）。§1.10 (a)（B の store と権限 6 項の無し）、(b)（A の store）、§9 L278（worker の gh dir は allow-list 外で読取専用、merge store は allowWrite の内側）と一致。X 手順 2 (f2)「`gh-orch/hosts.yml` の読取が拒否」は worker の `<main>` denyRead で成り立つ。
- pilot JSON: `srt-audit.json` だけ `~/.config/gh` を denyRead に持ち、worker/orchestrator は持たない = §4 前書き（V-08）と `leg2.md` L9 の注と一致。

### 2.3 merge 者と approver（§1.6 × §1.9 × §1.10 (f) × §3 X × §7）

PR 種別ごとに各節の字面を並べた。

| PR 種別 | W0b 前の merge 者 | W0b 後の approver → merge 者 | 一致 |
| --- | --- | --- | --- |
| 保護パス PR、author = A（W-step の code PR） | 操作者端末（§1.6、§1.9、§3 前書き、§7「W0b 前の保護パス PR の都度」） | 操作者 approve → B merge（§1.6、§1.10 (f)、§7「W0b 後の保護パス PR の都度」、§11 #19） | 一致 |
| 保護パス PR、author = B（plans/ruleset file を含む boundary PR） | 操作者端末（§1.9 の一般文「除外だけの PR 以外の全 merge」。ただし §3 前書き・§7 の列挙は W-step の code PR だけ → X-03） | 操作者 approve → B merge（§1.10 (f)、§7 5b 行「以後 boundary PR は操作者が approve してから orchestrator が merge」） | 一致（列挙の漏れだけ） |
| 除外だけの PR、author = A（W-07 の自 task id の記録 PR） | orchestrator（§1.6「W0b の前後とも orchestrator が merge」、§3 前書き） | **approver 未記載**: ruleset は approval 1 を全 PR に課す（path 条件は無い）ので B の approve が要るが、§1.6/§1.9 は「何もしない／orchestrator が merge」とだけ書き、§1.10 (f) は「worker の PR は … 操作者が最終 head を approve」と**全 worker PR**に操作者 approve を要求する | 矛盾 → X-01 |
| 除外だけの PR、author = B（記録 PR、X 手順 3 の handoff PR） | orchestrator（同上） | **approver 無し**: B は自作 PR を approve できず（§1.10 (f)）、§1.9 は W0b 後の操作者の手を「保護パス PR の approve、それ以外は何もしない」と限定する。§1.10 (f) の「boundary PR（author = B）も操作者が approve」とも食い違う。A に approve させる経路は §9 で「残余（早期 merge）」としか書かれず、手順としては無い | **merger/approver の無い PR 種別** → X-01 |
| 操作者 author の workflow PR（W-04 条件下） | — | B approve → 操作者 merge（§1.10 (a)、§7 行、§3 W9/D） | 一致。ただし §1.6/§1.10 (f) の「操作者は決して push しない」と字面が衝突 → X-04 |
| X 手順 0（C-1）/2 (b)/5（DoD11）/5b | 0 = 操作者 merge、2 (b) = records-only PR、5 = records-only か操作者 merge を DoD11 に数える、5b = boundary PR 1 本を操作者 approve → B merge（§3 X 行、§7 X 手順 0/2/5/5b 行） | — | 一致 |

B-approves-A の残余: §1.6（chain は approver の login を見る）、§1.10 (f)（残余の段落）、§9 U-06/U-08 行（「残る経路 = B が A 作の PR を approve + merge … 統制は chain の login 検査と `make update` の停止」）、§11 #19（login 検査）に在る。§11 #18 は「approve は操作者だけ」と platform 側の閉鎖として書き残余に触れず、§9 G-06 行は「2 account 化後の CODEOWNERS」と識別子の数が古い → X-05。

### 2.4 code-owner 規則（D-024-123、v11）の差し込み先

B の approve が ruleset で数えられる残余と「操作者 author の PR は B が approve」の規則を platform で閉じる変更。v10 の字面から見て書き換えが要る場所:

1. §1.10 (c) の payload 項目と正本 `scripts/orchestrator/ruleset-main.json`（`pull_request` 規則に code-owner review の要求を足す; W0b の受理 `diff` はこの file 基準なので file が先）。
2. §3 W6a（`.github/CODEOWNERS` の新設 = 操作者 login を `*` に 1 行; `.github/**` は反転で保護済み; validate に「`.github/` 以外（repo root、`docs/`）に `CODEOWNERS` が無い」1 本 — F5 の探索順は `.github/` → root → `docs/`、`docs/**` は除外なので敵対的 PR が置けるが、`.github/` にある限り無視される; fixture 1 本）。
3. §3 W0a/W0b 行と §7 X 手順 5b 行の「後」の値（`required_approving_review_count: 1`、`require_last_push_approval: true` に code-owner を足す）、§8 W0 の (f3)（「B の A 作 PR への approve が ruleset を満たさない」の否定 1 本）。
4. §1.6 の chain 規則（login 検査は platform 規則の二重化に格下げ、文はそのまま残せる）、§1.10 (a) の W-04 の帰結（B に Workflows write、操作者は author にならない）と §1.6/§1.10 (f) の push 文（X-04 が消える）、§7「W0b 後の `.github/workflows/**` の変更」行。
5. §9 U-06/U-08 行（残余の閉鎖、owner を W0b のまま測定に code-owner を足す）、§9 G-06 行（「長期は CODEOWNERS」→ W0b の一部）、§11 #18/#19、決定 (5)、§2 の ruleset 行 + 新規 file 行（`CODEOWNERS`）。
6. §1.9 の操作者の手: code-owner が要るのは全 PR なので「W0b 後は保護パス PR の approve、それ以外は何もしない」は「W0b 後は全 PR の approve」になる（X-01 と同じ文）。

### 2.5 §1.6 の除外 4 項 + 名指し保護 × W6a × §11 × boundary PR

- 除外 4 項（`.orchestration/**`、`docs/**`、`README.md`、`.ua/**`）と名指し保護（`AGENTS.md`・`CLAUDE.md`・`**/SKILL.md`・`.omp/**`・`tests/**`・`.orchestration/plans/**`・`scripts/orchestrator/ruleset-main.json`）、「二重一致は保護が勝つ」は §1.6、§3 W6a（refuse fixture に `.orchestration/plans/` 1 file と `ruleset-main.json`、通過 fixture は「`.orchestration/**`（`plans/**` 除く）+ 3 項」）、§9 決定 (6)、§11 #19/#21、§2 L91 で同じ。`.project-map/**` は落ち、validate が `git ls-files .agents/worklog` と `git ls-files .project-map` の空を固定（§1.6、W6a）。`.gitignore` L9/L26 と一致【実測】。
- 名指し保護の置き場が無い: §1.6 は `protected-paths.txt` に「書くのは除外だけ」と定め、chain は「除外 glob より先に保護の名指しを見る」と書くが、その名指し一覧がどこに在るか（chain の中か、同 file の別記法か）は書かれていない。W5a/W5b の render/テストは file の除外だけを読む → X-06（P3）。
- boundary PR と `.orchestration/plans/**`: 計画の改訂・処分表の同期・§7 の行の出所はすべて `plans/**` なので、それを運ぶ boundary PR は保護パス PR。W0b 前は §1.9 の一般文で操作者 merge、W0b 後は操作者 approve → B merge（§1.10 (f)）で手順は在る。ただし §3 前書き「除外だけの PR（記録 PR、X 手順 3 の handoff PR）だけ orchestrator が merge」と §7「W0b 前の保護パス PR の都度（W-step の code PR の全部 …）」は記録 PR を除外だけの PR と見なし、plans を含む記録 PR（今日の boundary PR のほぼ全部）が操作者 merge になることを書かない → X-03。

### 2.6 その他の節

- §1.7 (1) `env -i` の変数 5 名（`PATH=<seat dir>:<seat dir>/bin:<herdr binary の dir>:/usr/bin:/bin`、`HOME`、`HCOM_DIR`、`TMPDIR`、`HERDR_SOCKET_PATH`）= §4 #8b = §9 Q-08 行 = Status log v10 = `leg2.md` #8b の `envi` 形（PATH の 4 段の順も同じ）。
- §1.7 (4) の `pgrep -f` 2 本 + 3 分岐 = §3 W6a の fixture 文 = `leg2.md` L96 の注。`leg2.md` #7 の kill 後の列（`ps -p`、errno probe、`pgrep -fl 'sleep 600'`、`pgrep -lf pilot-audit`）は §4 #7 と同じで、計画も handout も「`ps_exit` は記録、条件は process 一覧」と書く。「canary は pane 閉鎖の経路だけ」は §1.7 (4) に在る。W-06 の処分が handout 側に置くとした「canary の pid を file に書かせる prompt」は `leg2.md` #7 にまだ無い（`canary.pid` の字面 0）→ X-08。`<results dir>/` の pattern が omp-run.sh 自身の process 木に当たりうる点は W6a の fixture 文に無い → X-07。
- §1.9 と §7 見出し: 名指しの出所（操作者自身の shell の `gh pr list --state merged --search`）と sha 突合（`.mergeCommit.oid`）は同文。§1.9 の「W0b 前は除外だけの PR 以外の全 merge、W0b 後は保護パス PR の approve、それ以外は何もしない」は V-11 どおりだが、W0b 後の「それ以外は何もしない」が X-01。
- §2: 表は 51 行（L42〜L92）、内訳 残す 10／残す・変える 2／変える 16／捨てる 13（書換 1・昇格 1 を含む）／新規 9／混合 1 = L94 の数と一致【実測 awk】。新規 file 行（`ruleset-main.json`、L91）在り。
- §8 STOP の base 文脈 trigger 3 つ + `uses: ./.github/workflows/` 1 段 = §3 W0c `threat_table` = W6a validate。今日の inventory【実測 grep】: `pull_request_target` は `regime.yml` だけ、`workflow_run`/`issue_comment`/`workflow_call`/`uses: ./`/`environment:` は 0、`contents: write` は `docs.yml` だけ、`CODECOV_TOKEN` は `test.yaml` L425 = 計画の記述どおり。
- §9 決定 (1)〜(11) と `decisions.tsv`: D-024-122（B の merge store、App の副選択、W0b 前の操作者 merge、plans/ruleset file の保護、W-07、除外 4 項、W-03、W-04、pgrep、STOP、`env -i`）が決定 (5)(6) と §1.6/§1.7/§1.10 の字面に一致; D-024-123（349 行、`782f9024`、23 fixed + residual W-04、handout 111/115、reviewer store 廃止、操作者 author の PR は B approve）は Status log v10 と一致。
- §11 1〜22: #14/#21（`ruleset-main.json` が正本、除外 4 項 + `plans/**` 保護）、#18（B、W-03 の限定）、#19（W0b 前後、W-07）が本文と一致。#18 の残余の省略は X-05。
- Status log v10: fixed 23 id（V-01〜V-12、W-01〜W-03、W-05〜W-12）= 処分表の fixed 集合、residual W-04、handout-only none（保留 4 件を名指し）、operator-decision W-01。一致。
- 用語の定義順: A/B（L5）、`<P>`（L9、表 L11 より前）、`audit-r2`（L3 は見出しの要約、L9 で説明、L20 に §1.7 (4) の指示）、正本 file（L32 で新設先と役割を定義）、`merge store`（L25、§1.10 (a) の指示付き）、`machine account`（L5）。先行使用は無い。L32 の「update-branch も machine account（§1.10 (b)）」は B の定義が (a) にあるので指示先が半分ずれるが、(b) にも A/B の両方の記述があり読める。

## 3. handout との一致

- `leg1.md`: 見出し L1 と末尾 L111 が「plan 025 v10 §4」、所要「60〜75 分」= 計画 L124/L216。v10 の第 1 脚の表は v9 から文言以外に変更が無く、round 9 で 19 手順の flag・順・期待が一致していた（#0 の 2 段と `RULESET-EMPTY`、#0b の keychain 2 種別と helper 2 段と `grep -c oauth_token`、`can_approve_pull_request_reviews` は L21-26 で再確認）。
- `leg2.md`: 115 行、見出し v10。前書き L9 に V-08 の注（worker/orchestrator JSON は `~/.config/gh` を denyRead に持たず、#5 (6)(10)(12) と #8 の `gh` は keychain で通る、W0a が足す）= 計画 §4 前書き/#2。#8b（L103-105）: `HERDR_BIN` を loop 前に 1 回取り空なら止まる、form ごとに `mark.<form>` を `touch`、`form=launched`（tag `pilot3`）と `form=envi`（`env -i` に `PATH`（`seat-audit` → `seat-audit/bin` → herdr の dir → `/usr/bin:/bin`）・`HOME`・`HCOM_DIR`・`TMPDIR`・`HERDR_SOCKET_PATH`、tag `pilot3u`）、起動 exit≠0 は `LAUNCH-FAIL` で次へ、marker より新しい runner が無ければ `NO-NEW-RUNNER`、`--hcom-tool-path` の値で `Q08-PASS-shim`/`Q08-FAIL-real-omp`、合格基準 `form=envi Q08-PASS-shim`、`launched` は参考、両 tag を kill = 計画 §4 #8b と §9 Q-08 行の全項目。#10（L110-112）: kill 4 本（`pilot2`、`pilot-audit`、`pilot3`、`pilot3u`）、`logstream.pid`、PR/branch の一覧、canary file 一覧に `mark.launched`/`mark.envi`、`pgrep` 2 本、`rm -rf` の 3 対象 = 計画 §4 #10。内部整合: `shimok`/`mkshim`/`wait_result` は L21/L53 で pane 単位に定義し直す注が前書き L6 にある; `srt-orch.json` は #8（L98）で `sed` が作り #8b が使う; `ANAME-EMPTY` の止まり方（L90-91）は leg1 #10 と同形。
- 差: W-06 の handout 側の項目（canary の pid を file に書かせ、操作者がその存在を見てから `pgrep` を読む）は `leg2.md` #7 に無い（X-08）。それ以外に計画と handout の flag・順・期待の差は見つからなかった。

## 4. 所見表

| id | priority | file and section | problem | evidence | fix |
| --- | --- | --- | --- | --- | --- |
| X-01 | P1 | plan §1.6 L32「除外だけの PR は W0b の前後とも orchestrator が merge」、§1.9 L35「W0b 後は保護パス PR の approve、それ以外は何もしない」、§1.10 (f) L36「worker の PR は … 操作者が最終 head を approve」「boundary PR（author = B）も操作者が approve」、§7 L236 | W0b 後の ruleset（approval 1 + `require_last_push_approval`）は path 条件を持たず全 PR に効く。除外だけの boundary PR（author = B: 記録 PR、X 手順 3 の handoff PR）は B が self-approve できず、§1.9 は操作者に approve させず、A に approve させる手順も無い = approver の無い PR 種別。除外だけの worker PR（author = A）は B の approve で通る設計に読めるが §1.6/§1.9 はそれを書かず、§1.10 (f) は全 worker PR に操作者 approve を要求して矛盾する | L32/L35/L36/L236 の字面; README L1143 の ruleset は `ref_name` 条件だけ（path 条件無し）; §1.10 (f)「B は自分の PR を approve できない」 | 1 文で決める: 「W0b 後は除外だけの PR にも approval 1 が要る: author = A の PR は orchestrator（B）が approve して merge（chain の login 検査は保護パス PR だけ）、author = B の記録 PR は操作者が approve」を §1.6/§1.9/§7 に、§1.10 (f) の「worker の PR は操作者が approve」を「保護パス PR は」に。v11 の code-owner 規則では全 PR が操作者 approve になるので、§1.9 を「W0b 後は全 PR の approve」と書く形に一本化できる |
| X-02 | P2 | plan §1.6 L32（W-07 の author 判定「W0b 前は head の committer」）、§3 W6a L112、§11 #19 L333 | committer は席の git 設定が書く値で、worker 席は user gitconfig を読み clone 側で上書きもできる（`hcom-seat` は clone に `commit.gpgsign false` しか描かない、§1.1）。規則が狙う攻撃者 (1) が判定を偽造できる。PR の author は token の identity で W0b 前でも `gh pr view --json author` が返す; A が存在するのは X 手順 5 以降で、それ以前の W-step の PR は agmsg 席が操作者 token で作るので規則は空振り | L32 の 2 期分け; §1.1 の clone 設定; §1.10 (b) の A の時期 | 判定を両期とも `gh pr view --json author` に 1 句で揃え、「X 手順 5 より前（agmsg 席の PR）は A 作の PR が無く、統制は orchestrator の読み」を 1 句 |
| X-03 | P2 | plan §3 前書き L98「除外だけの PR（記録 PR、X 手順 3 の handoff PR）だけ orchestrator が merge」、§7 L235 の列挙「W-step の code PR の全部」、§1.9 L35 | W-02 で `.orchestration/plans/**` が保護になった帰結が列挙に反映されていない: 計画改訂・処分表・決定行を運ぶ boundary PR は保護パス PR で、W0b 前は操作者 merge（§1.9 の一般文では正しい）。§3/§7 は記録 PR を除外だけの PR と見なし、今日の形（orchestrator が boundary PR を merge）が W0b 前にそのまま続くように読める | L98/L235 の字面 vs L32 の `plans/**` 保護 | §3 前書きと §7 行に「`plans/**` か `ruleset-main.json` を含む boundary PR も保護パス PR（W0b 前は操作者 merge、W0b 後は操作者 approve → B merge）」を 1 句 |
| X-04 | P3 | plan §1.6 L32、§1.10 (f) L36「操作者は決して push しない」 vs §1.10 (a) L36・§7 L237（W-04 条件下で操作者が branch を push して author になる） | 条件付きの行と絶対形の文が衝突する。approval の有効性は両立する（操作者 author の PR の approver は B） | 同一節内の 2 文 | 「決して」に「（W-04 の条件が立つ workflow PR を除く）」を添える。D-024-123 の v11（B に Workflows write、操作者は author にならない）で消える |
| X-05 | P3 | plan §11 #18 L332「approve は操作者だけ」、§9 G-06 行 L263「2 account 化後の CODEOWNERS」 | #18 は B が A 作の PR を approve でき ruleset が数える残余（§1.6/§9 U-06 行）を platform 側の閉鎖のように書く; G-06 行は識別子が 3 つになった後も「2 account」で、CODEOWNERS は D-024-123 で v11 の W0b の一部になる | L332/L263 vs L32/L265 | #18 に「B の A 作 PR への approve は chain の login 検査が弾く（§9 残余）」を 1 句; G-06 行を「3 identity + v11 の code-owner 規則」に |
| X-06 | P3 | plan §1.6 L32（`protected-paths.txt` は除外だけ、chain は名指し保護を先に見る）、§3 W5a L110/W5b L111/W6a L112 | 名指し保護 7 項の正本の置き場が書かれていない（chain の中か、同 file の別記法か）。W5a/W5b のテストは file の除外だけを読むので、名指し側の変更は検査されない | L32 と W5a/W5b/W6a の字面 | 「名指し保護は同じ file に `!` 行（または chain の定数）として持ち、W6a の fixture がその一覧を固定する」を 1 句 |
| X-07 | P3 | plan §1.7 (4) L33、§3 W6a L112 | `pgrep -f -- '<results dir>/'` は pgrep 自身を除くだけで、omp-run.sh を包む `sh -c` や `<results dir>` を引数に持つ親 process に当たれば常に exit 0 = 再試行が死ぬ（安全側だが W-05 (a) と同じ class）。W6a の fixture 文に自 process 木の不一致が無い | L33 の pattern; W6a の 3 分岐 fixture | W6a に「omp-run.sh 自身の process 木が 2 pattern のどちらにも当たらない」fixture 1 本、または pattern を audit 席の argv にだけ在る語（`--hcom-tool-path <seat dir>/omp` 等）に 1 句 |
| X-08 | P3 | handout `leg2.md` #7（L84 の prompt、L95 の読み）; plan §4 #7 L170 は要約のみ | W-06 の処分の handout 側（canary の pid を `out/canary.pid` に書かせ、操作者が file の存在を見てから `pgrep -fl 'sleep 600'` を読む）が未反映。席が canary を立てなければ `pgrep` の空を「生存無し」と読む | `grep canary.pid leg2.md` = 0 | #7 の prompt に pid file の 1 句、L95 の列に `cat out/canary.pid` を 1 句（別文脈の handout 作業） |

## 5. 確認済の行と一致した file

- 処分表 24 行のうち、名指しの節に在り隣接節と整合した 23 行: V-01（§1.6 W0b 前の規則、§1.9、§3 前書きの merge 者一覧、X 手順 0/2 (b)/5、§7 L235）、V-02（§1.6 chain 規則、§7 L236、§11 #19）、V-03（除外 4 項、`.project-map/**` の理由文、W6a の `git add -f` fixture と validate、決定 (6)、Status log）、V-04（役割表の注 L9、`<P>`、L27「自役割以外の profile」、§1.9/§7 B-3 行の `audit-r2`、L20 の `hcom-seat` 構文）、V-05（push 文 L32/L36）、V-06（検査の位置 = 証跡の後の最終 step、W6a の exit 10 の意味）、V-07（X 手順 2 (b) の records-only と `refuse 10` の注）、V-08（§4 前書き、#2、`leg2.md` L9）、V-09（L5 の A/B 定義、L32 の指示）、V-10（§3 W0b 欄）、V-11（§1.9）、V-12（L214 v10、L122 v10、60〜75 分 ×2、#10 の `tag:pilot3u`）、W-01（§1.3 両行、§1.6、§1.10 (a)(b)(f)、§3 W0a、§7 W0a (1)(2)(3)/5b、§8 W0、§9 U-06 行、§11 #18、決定 (5)、Status log）、W-02（`plans/**` と `ruleset-main.json`、§2 L91、W6a、§6 記録、§7 5b の `--input` と `diff`、§11 #14/#21、決定 (6)）、W-03（§1.10 (d) の srt 外の限定と手順 4 の順、§11 #18）、W-04（residual、上記）、W-05（§1.7 (4) の 2 pattern と 3 分岐、W6a）、W-06（§1.7 (4) の 1 句）、W-07 の本体（§1.6、W6a fixture、§11 #19）、W-08（§8、W0c `threat_table`、W6a validate、inventory の実測と一致）、W-09（§1.7 (1)、#8b、§9 Q-08、Status log）、W-10（V-01/V-06 と同文）、W-11（§1.10 (f) 末尾、§9 L284）、W-12（V-03 と同処分）。
- 一致した file: `leg1.md`（v10 見出し、60〜75 分、#0/#0b の行）; `leg2.md`（前書き L9、#7 の kill 後の列、#8 の `srt-orch.json`、#8b の全項目、#10 の kill と leftovers）; `srt-*.json` の鍵集合（5 配列 + `allowPty`、`network` 5 鍵）と denyRead の `~/.config/gh`（audit だけ）; `gh-actions-facts.md` F1〜F4（W0c、決定 (10) の引用元）と F5（code-owner、v11 の根拠）; `.github/workflows/*` の trigger/permission（§8 の inventory 文と一致）; README L1124/L1143/L1227（ruleset 名と payload の所在 = W6a が写す元）; `.gitignore` L9/L26（`.agents/worklog/`、`.project-map/`）; `decisions.tsv` D-024-120〜123。
- §2 の 51 行の内訳、§9 決定 (1)〜(11)、§11 1〜22、Status log v10 の id 集合は数え直して一致。

## 6. 報告（10 行）

1. 件数: P0 0、P1 1（X-01）、P2 2（X-02、X-03）、P3 5（X-04〜X-08、うち X-08 は handout 側）、計 8。round-9 の P1 4 行（V-01/V-02/W-01/W-02）の修正は全部名指しの場所に在り、逆向きの修正は無い。部分は W-07 の author 判定（X-02）だけ。
2. 最重要 = X-01: W0b 後の ruleset は全 PR に approval 1 を課すのに、除外だけの boundary PR（author = B）には approver が無く（B は self-approve 不可、§1.9 は操作者に approve させない）、除外だけの worker PR の approver も書かれていない。§1.10 (f) は全 worker PR に操作者 approve を書いて §1.6/§1.9 と食い違う。1 文で閉じるが、v11 の code-owner 規則は同じ文を「全 PR が操作者 approve」に変えるので、v11 でまとめて書き直すのが短い。
3. X-02: W-07 の「W0b 前は head の committer」は席が書ける値で、規則が狙う攻撃者が偽造できる。両期とも PR author（token の identity）に揃える 1 句。
4. X-03: `plans/**` の保護の帰結として、計画・処分表・決定行を運ぶ boundary PR は W0b 前に操作者 merge になる。§1.9 の一般文は正しいが §3/§7 の列挙が記録 PR を除外だけの PR と見なしている。1 句。
5. 3 識別子化の整合: `reviewer store`/`gh-reviewer`/操作者 account の merge token は履歴の言及だけに残り、A/B/操作者の役割は §1.3/§1.6/§1.10/§3/§7/§9/§11 で同じ。merge store の所在と denyRead の関係は 3 節で一致。
6. B-approves-A の残余は §1.6/§1.10 (f)/§9 U-06 行/§11 #19 に在る。§11 #18 と §9 G-06 行だけ字面が古い（X-05）。code-owner 規則の差し込み先は §2.4 の 6 箇所（payload file、W6a の `.github/CODEOWNERS` と validate、W0b/5b の値と (f3)、chain 規則と push 文と W-04 行、§9/§11/決定 (5)/§2、§1.9）。
7. 除外 4 項 + 名指し保護は §1.6/W6a/§11/決定 (6)/§2 で一致し、`.gitignore` と木の実体にも合う。名指し保護の正本の置き場だけ未指定（X-06）。
8. §1.7 (1) の `env -i` 5 名は §4 #8b・§9 Q-08・handout #8b と PATH の 4 段の順まで一致。§1.7 (4) の pgrep 3 分岐は W6a と handout の注に一致; 自 process 木への一致（X-07）と canary の pid file（X-08）が残る。§2 51 行、§8 STOP、§9 決定と `decisions.tsv`、§11、Status log v10 の id 集合は一致。
9. loop は規則上は止められない（P1 1 件）。ただし X-01 は設計（識別子 3 つ、token の権限、W0b の形）には触れず、§1.6/§1.9/§1.10 (f)/§7 の 1 文の決定で閉じ、v11 の code-owner 規則が同じ文を必ず書き換える。P2 2 件はどちらも 1 句〜2 句。P3 は字面と handout 1 件。v11 を書くなら round 10 の Y（red team）と合わせて 1 版で収まる量。
10. 未確認: fine-grained token の Workflows 権限と `.github/workflows/**` の push/merge の挙動（計画自身が開いた測定）; ruleset の code-owner 要求が `required_approving_review_count` と独立に数えられるか（F5 の引用に依拠、網無し）; omp policy overlay（B-2/B-3）が orchestrator の `gh pr review --approve` を deny 行に持つか（X-01 の「B が A 作の除外 PR を approve」が policy 層で通るか; overlay 本文は未読）; `events.ts`/`policy.yml` の v10 不変は Status log の記述に依拠（diff は取っていない）; `leg1.md` の #1〜#18 本文は round 9 の一致を引き継ぎ v10 で再読していない; GitHub docs の現在の文言。
