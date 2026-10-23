# Plan 025 round 10 処分表（v10 `782f9024` → v11）

- 対象: `025-review-r10-verification.md`（X-01〜X-08）、`025-review-r10-redteam-y1.md`（Y-01〜Y-12）、`025-review-r10-redteam-y2.md`（原文の id は Y-11〜Y-21 で Y1 と重複するため本表では `Y2-11`〜`Y2-21`）の 31 件。処分は D-024-123/124/125 の決定を転記したもので、本表で再決定はしていない。
- 反映先: `.orchestration/plans/025-regime-cutover-plan.md` v11（355 行、sha256 prefix `eb4e3192`）。handout `pilot/*` は別文脈が直す（handout 側の項目は「how」列に書く）。
- 処分の型: `fixed-in-v11 <節>` / `residual <owner, 測定>` / `handout-only <file 手順>` / `not-applicable <事実>`。
- 根拠の出所: 【gh F5】= `gh-actions-facts.md` F5（code owners）、【hcom regime】= `b2-c2-facts.md` 末尾の hcom v0.7.30 launch environment regime 節。

| id | priority | disposition | how |
| --- | --- | --- | --- |
| X-01 | P1 | fixed-in-v11 §1.6、§1.9、§1.10 (f)、§3 前書き、§7 W0b 後の行、§9 U-06/U-08 行、§11 #19 | code owner 規則で 1 文に一本化: W0b 後は全 PR（除外だけの PR、records-only の boundary PR を含む）に操作者 = code owner の approval が要り、orchestrator（B）が merge; 「除外だけの PR は W0b の前後とも orchestrator が merge」は「W0b 前だけ」に書き換え |
| X-02 | P2 | fixed-in-v11 §1.6、§3 W6a、§11 #19 | W-07 の author 判定を両期とも `gh pr view --json author`（token の identity）に; committer は席が書ける値なので見ない; X 手順 5 より前は A 作の PR が無く規則は空振りで統制は orchestrator の読み、と 1 句 |
| X-03 | P2 | fixed-in-v11 §3 前書き、§7 W0b 前の行 | `.orchestration/plans/**` か `ruleset-main.json` を運ぶ boundary PR（計画改訂・処分表・§7 の出所）は保護パス PR: W0b 前は操作者 merge、W0b 後は操作者 approve → B merge; §7 の列挙に X 手順 0 とこの boundary PR を足す |
| X-04 | P3 | fixed-in-v11 §1.10 (a)、§7 workflow 行 | Y-04 で操作者 author の経路が消え「操作者は決して push しない」と衝突する条件付き文が無くなった; Workflows 権限が要れば B に足す |
| X-05 | P3 | fixed-in-v11 §11 #18、§9 G-06 行 | #18 に「A・B の approval は code owner 規則を満たさず chain の login 検査は第 2 層」; G-06 行を「W0b の code owner 規則（3 identity + `.github/CODEOWNERS`）」に |
| X-06 | P3 | fixed-in-v11 §1.6、§3 W6a、§11 #21 | 名指し保護 7 項は `protected-paths.txt` の `protected:` 節、除外 4 項は `exclude:` 節; W6a の fixture が両節を固定し W5a/W5b のテストも同じ file を読む |
| X-07 | P3 | fixed-in-v11 §1.7 (4)、§3 W6a | `omp-run.sh` は背景子の argv に `<results dir>` を置かず pattern は字面どおり固定; W6a に「自身の process 木（`sh -c` 包み、背景子）が 2 pattern のどちらにも当たらない」fixture 1 本 |
| X-08 | P3 | handout-only `leg2.md` #7 | canary の pid を `out/canary.pid` に書かせ、操作者は file の存在を見てから `pgrep -fl 'sleep 600'` を読む; 計画 §4 #7 に注記だけ |
| Y-01 | P3 | fixed-in-v11 §1.6、§1.10 (c)(f)、§3 X 5b、§7 5b、§8、§9 先頭行 | ruleset payload に `require_code_owner_review: true`、`.github/CODEOWNERS` は `* @<操作者 login>`; A・B・`GITHUB_TOKEN` の approval は数に入らない【gh F5】; v10 の 2 残余（A の早期 merge、B の approve + merge）は閉じ、chain の login 検査は第 2 層; (f3) に「B の approve でも `BLOCKED`」 |
| Y-02 | P2 | fixed-in-v11 §1.10 (c)(f)、§2 ruleset 行、§3 W6a、§7 5b と W0b 後の行、§9 W-11 行、§11 #14/#24 | repository の auto-merge を W0b で off（受理の固定値 `allow_auto_merge: false`）、README の「auto-merge enabled」は W6a が反転; それまで chain は approve 依頼と merge の前に `gh pr view <n> --json autoMergeRequest` が null を見る |
| Y-03 | P3 | fixed-in-v11 §7 5b、§3 W0a/W0b | 受理の固定値一覧に `enforcement: active` と `conditions.ref_name.include` = `refs/heads/main` のみを含めた（Y-06 と同じ受理行） |
| Y-04 | P1 | fixed-in-v11 §1.6、§1.10 (a)、§3 前書き/W0c/W9/経路外、§7 W0a (3)・workflow 行・E1 前、§11 #8/#23 | 操作者は PR を author しない: 操作者決定の編集（W9/E1 の manifest・renderer・permgate 部分、shared source、permgate）は patch か指示として B に渡し、orchestrator が適用して B で push、操作者が approve、B が merge; 追跡 file が変わらない編集は PR 無しの local apply; Workflows 権限が要れば B に足す（D-024-123） |
| Y-05 | P3 | fixed-in-v11 §1.10 (a)、§3 W0a/W0c/W9、§7 W0a (3)・workflow 行 | W0a (3)・W9・§7 の 4 箇所を「B に Workflows write を足して W0a (3) をやり直す」に揃え、W-04 の分岐を書き換え; 後期に approver/merger を欠く PR class は無い |
| Y-06 | P1 | fixed-in-v11 §1.6、§1.10 (f)、§3 W0a/W0b、§7 5b、§8 | W0b の受理は §7 に書き下した固定値一覧（enforcement active、include `refs/heads/main` のみ、bypass 空、approval 1、last push、code owner、dismiss stale、必須 7 context、`allow_auto_merge: false`、`codeowners/errors` 空）との一致を操作者が自分の端末で見比べる; PUT 前に W6a 以降の `git log -p -- scripts/orchestrator/ruleset-main.json` を読む; 正本 file は PUT の入力のまま |
| Y-07 | P1 | fixed-in-v11 §1.9、§7 見出し、§9 U-06/U-08 行 | `make update` 停止の名指し一覧を `gh pr list … --json number,mergeCommit,mergedBy,files` で取り、除外に無いパスに触れた PR の `mergedBy.login` が操作者でなければ `CONFIRM=1` を打たず記録; W0a で B が存在してから有効、W0a 前は全 merge が操作者 login で停止は区別できないと明記 |
| Y-08 | P2 | fixed-in-v11 §1.6、§1.9、§7 W0b 前・後の行 | 操作者は差分を自分の端末の `gh pr diff <n>` と `gh pr view <n> --json files,author,mergedBy` でだけ読み、orchestrator の貼付は読まない; §7 の「orchestrator が差分本文を提示」を「証跡と PR 番号を提示」に |
| Y-09 | P2 | residual 操作者、測定 = boundary 記録の W0b 前の手 merge 数 | §1.10 と §9 +1 行に数を明記（≒ 12 本: W-step の code PR 10 本、`ruleset-main.json` の PR、W0b の記録 PR）し受容; 順序は変えない（W0b の依存は「push する全席が A/B の token を持つ」ことで、agmsg 席への A store 付与は agmsg 側の変更 = D-024-79/§10 #3 が禁じる）; 前倒しの代替は記録のみ; 決定 (5) に 1 句 |
| Y-10 | P2 | fixed-in-v11 §1.10 (f)、§9 W-11 行 | W-11 の文を「`--auto` を除きどれも main に届かない」に直し、`--auto` は Y-02（auto-merge off、`autoMergeRequest` null）で閉じる |
| Y-11 | P2 | fixed-in-v11 §1.10 (f)、§2 CODEOWNERS 行、§3 W6a、§7 W6a の PR 行と 5b、§8 | W6a の validate に `git ls-files CODEOWNERS docs/CODEOWNERS` 空（`.github/` 外を拒む【gh F5】）; W0b 受理に `GET repos/<owner>/<repo>/codeowners/errors` = `[]` と `require_code_owner_review: true`; §7 に W6a の PR の行（merge 後に `errors` を見る） |
| Y-12 | P3 | fixed-in-v11 §1.6、§1.10、§3 前書き/W0a/W0c/W9/経路外、§7 W0a (3)・5b・workflow 行、§9 G-06 行 | 掃除一覧を一括: 「前後とも orchestrator が merge」3 箇所、「B の approve を ruleset が数える … chain は login を見る」、Workflows 分岐 3 箇所、「2 account 化後の CODEOWNER」、§7 の列挙に X 手順 0 |
| Y2-11 | P3 | fixed-in-v11 §1.7 (1) | hcom/herdr が読む他の名（`LOGNAME`/`USER`、`XDG_*`、`HERDR_PANE_ID`/`HERDR_ENV`/`HERDR_HOME`）は要らない: 無ければ既定 workspace か `LAUNCH-FAIL` で、pane の置き場所は仕様ではない、と 1 句 |
| Y2-12 | P2 | fixed-in-v11 §1.3 3 行、§1.7 (1)(2)、§4 #7、§9 Q-08 行と store 行 | P1 → P2（source 事実）: §1.7 (1) を【hcom regime】の引用に書き換え（判定は環境だけ、5 名の `env -i` は `HumanShell`、`CI`/`GITHUB_ACTIONS` は unset、login shell の取り込みと cache は参照されない）; cache は file 状態でも引き金は環境なので 2 状態測定は不要と明記; `shell_env.json` を (2) の taint 検査（5 名）と worker/orchestrator/audit の denyWrite に追加 |
| Y2-13 | P2 | fixed-in-v11 §1.7 (1) | shim は `HOME` を描画時の絶対値として焼く（§1.2 の shim 式のとおり）; `~/.hcom/env` の passthrough は shim が転送する名だけが届き、`env` file は denyWrite と taint 検査の中、と 1 句 |
| Y2-14 | P3 | fixed-in-v11 §1.7 (1) | `env -i` が落として困るものは無い: 席の環境は shim が作り直し、起動側の `env -i` は launcher の `which_bin` と sidecar 転送だけに効く、と 1 文 |
| Y2-15 | P2 | fixed-in-v11 §1.7 (4)、§4 #8（handout 側は `leg2.md` #8） | 「#4b の `ps` の可否で確定」を削除し、#8 の srt 形の中で `pgrep -fl -- '--profile pilot-'; echo pgrep_exit=$?` を打って第 3 分岐（srt 下で他 sandbox の process が列挙できるか）を実測する; 計画側は期待欄に `pgrep_exit` |
| Y2-16 | P3 | fixed-in-v11 §1.7 (4)、§3 W6a | `omp-run.sh` は背景子の argv に `<results dir>` を置かず（poll は都度起動の `[ -f ]` と `tail -n1`）pattern は字面どおり固定するので自己一致しない、と 1 句（X-07 と同じ fixture） |
| Y2-17 | P2 | fixed-in-v11 §1.7 (4)、§3 W6a | 再試行の前提に「`lsof -t -- ~/.omp/profiles/audit/agent/agent.db` が空」を追加; `lsof` が無い・拒否された・非空 → 再試行せず block（fail-closed）; 検知の文言はそのまま; W6a に fixture |
| Y2-18 | P2 | handout-only `leg2.md` #8b | 偽 PASS の 3 閉鎖（`grep -o` の最初の 1 行だけを判定、shim への full path 等価、`LAUNCH-FAIL` は `hcom omp` 単独の exit）; 計画 §4 #8b に handout 側として注記 |
| Y2-19 | P2 | fixed-in-v11 §1.7 (1)、§4 #8b | `hcom-seat` が席の生成時に herdr binary の dir と `HERDR_SOCKET_PATH` を manifest から絶対値として `omp-run.sh` の `env -i` 前置に描画し、空なら拒否; pilot は操作者 shell から取り `[ -n "$HERDR_SOCKET_PATH" ]` の空ガードと `seat-audit/bin` の link で測る（handout 側） |
| Y2-20 | P3 | handout-only `leg2.md` #10 | `mark.launched`/`mark.envi` は #8b の設計上の file で残骸ではないと注記し canary 一覧から外す; `pgrep` の前に `sleep 5`; 計画 §4 #10 に注記 |
| Y2-21 | P3 | fixed-in-v11 §1.7 (1) | `env -i` 下で `SHELL`/`LOGNAME` が無ければ getpwuid 経路に落ち、失敗は `LAUNCH-FAIL`（安全側）、と Y2-11 の句に含めた |

集計: fixed-in-v11 27、residual 1（Y-09）、handout-only 3（X-08、Y2-18、Y2-20）、not-applicable 0。operator-decision: Y-04（操作者は author にならない、§11 #23）、Y-02（auto-merge off、§11 #24）、決定 (5) の既定の書き換え（code owner 規則、D-024-123）。
