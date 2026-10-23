# plan 025 v11 review round 11（perspective Z1: round-10 処分表 31 行の v11 反映検証と、計画全体の整合）

- 対象: `.orchestration/plans/025-regime-cutover-plan.md` sha256 prefix `eb4e3192`、355 行（`shasum`/`wc -l` で確認済）
- 入力: `025-review-r10-dispositions.md`（31 行）、r10 の X/Y1/Y2 審査、`pilot/leg1.md`（111 行）、`pilot/leg2.md`（115 行）、`pilot/srt-{worker,orchestrator,audit}.json`、`gh-actions-facts.md` F5、`b2-c2-facts.md` 末尾の hcom regime 節、`decisions.tsv` D-024-123〜126
- 方式: 読み取りのみ（`sed -n`/`grep`/`jq`/`wc`/`shasum`）。25 分の上限。届かなかった検査は 未確認 と書く。

## (1) round-10 処分の v11 反映（欠落・部分・矛盾だけを列挙）

| r10 id | 処分 | v11 の状態 | 備考 |
|---|---|---|---|
| Y2-15 | fixed-in-v11 §1.7 (4)、§4 #8（handout は `leg2.md` #8） | 部分 | 計画 §4 #8 は `pgrep -fl -- '--profile pilot-'` を書くが、`leg2.md` #8（L101）は `pgrep -fl omp` を打つ。どちらの pattern も同じ `/bin/sh -c` の文字列（`hcom omp … --profile pilot-audit …` を含む）に自己一致するので、`pgrep_exit=0` は「他 sandbox の process が列挙できる」の証拠にならない（Z-01） |
| Y-09 | residual（owner = 操作者、測定 = boundary 記録の手 merge 数） | owner と測定は §9 Y-09 行にあり | 数え上げに「W0b の記録 PR」を含むが、その PR は PUT 後に merge されるので W0b 後の規則（操作者 approve → B merge）に当たり、手 merge の数とも §3 W0a/W0b 行の「操作者 merge」とも食い違う（Z-02） |
| Y2-20 | handout-only `leg2.md` #10 | 部分 | 計画 §4 #10 は「`pgrep` の前に `sleep 5`」、`leg2.md` #10（L110/L111）は `sleep 2`（2 秒の settle）。marker 注記と canary 一覧からの除外は反映済（Z-05） |

上記以外の 28 行（X-01〜X-08、Y-01〜Y-08、Y-10〜Y-12、Y2-11〜Y2-14、Y2-16〜Y2-19、Y2-21）は名指しの節に本文があり、隣接文と矛盾しない（第 5 節）。

## (2) 計画全体の整合

| 検査 | 結果 | 根拠 |
|---|---|---|
| 2 期の規則（W0b 前: 保護パス PR は chain 証跡の後に操作者が手 merge、除外だけの PR は B/orchestrator が merge; W0b 後: 全 PR に操作者 = code owner の approve、B が merge） | §1.6、§1.9、§1.10 (a)(f)、§3 前書き、§3 X 手順 0/2 (b)/5/5b、§7 の W0b 前・後の 2 行、§8 W0、§9 U-06/U-08 行、§11 #18/#19/#23 で同文 | 唯一の揺れは「W0b の記録 PR」の merge 者（Z-02） |
| 操作者が PR を author する文、B の approval が数に入る文 | 残っていない | `操作者 author`/`操作者が author` の出現（L36、L340、L354）は全部「author にならない」の否定形か v10 の履歴; `gh-reviewer` の出現は「置かない」と履歴だけ; `前後とも`/`2 account` の出現 0 |
| §7 5b 固定値一覧（10 項） | §1.10 (c)/(f)、§2 ruleset 行と `ruleset-main.json` 行、§3 W0a/W0b 行、§3 W6a、§8 W0 と一致 | enforcement active / include `refs/heads/main` のみ / bypass 空 / approval 1 / last push / code owner / dismiss stale / 必須 7 context / `allow_auto_merge: false` / `codeowners/errors` 空。§8 の「10 項と `codeowners/errors` 空」は二重に数える字面（Z-04） |
| `.github/CODEOWNERS` | §2 に行（新規、保護パス `.github/**`）、§3 W6a で新設、validate が `.github/` 外を拒む、§7 W6a 行で merge 後に `codeowners/errors`、§1.6/§1.10 (c)/§2/§11 #18 に【gh F5】 | F5 の 3 引用（base branch の file、owner の誰かの approval で足りる、`.github/` → root → `docs/` の探索順）と計画の帰結は一致 |
| auto-merge off | §1.10 (c)(f)、§2 ruleset 行、§3 W6a（README 反転）、§7 5b と W0b 後の行、§9 G-01 行と W-11 行、§11 #14/#24 | `autoMergeRequest` null は §1.10/§7/§9/§11 で同文 |
| `protected-paths.txt` の `exclude:` 4 項 / `protected:` 7 項 | §1.6、§3 W6a、§9 決定 (6)、§11 #21 で一致 | 7 項 = `AGENTS.md`・`CLAUDE.md`・`**/SKILL.md`・`.omp/**`・`tests/**`・`.orchestration/plans/**`・`scripts/orchestrator/ruleset-main.json` |
| `shell_env.json` | §1.3 の worker/orchestrator/audit の 3 行の denyWrite にあり; §1.7 (2) の taint 5 名（`config.toml`/`env`/`config.env`/`scripts`/`shell_env.json`）; `jq` で 3 JSON の denyWrite を平坦化 = worker 13 項・orchestrator 19 項・audit 9 項、各 1 項が `shell_env.json`（D-024-126 の数と一致） | `leg2.md` #7 の STORE-TAINTED loop（L88、L92）も同じ 5 名 |
| §1.7 (1) の【hcom regime】引用 | `b2-c2-facts.md` 末尾の節と一致: regime 判定は env だけ（`detect_tool` の marker 一覧、`HCOM_LAUNCHED=1`、`CI`/`GITHUB_ACTIONS`）、5 名の `env -i` は `HumanShell`、cache は `<hcom_dir>/shell_env.json`（0600、rc mtime、6 時間） | 計画が「parent process・file・`HERDR_*` は見ない」と書く点も facts の「No parent-process, file or HERDR_* inspection」と一致 |
| §1.7 (4) `lsof` 前提と `pgrep_exit` | §1.7 (4) は `lsof -t` 空を前提に足し、第 3 分岐を §4 #8 の srt 形で測ると書く; §4 #8 の期待欄に `pgrep_exit`; `leg2.md` #8 に `pgrep_exit` | pattern が自己一致（Z-01）。`lsof` は W6a の fixture にあり、§4 には無い（pilot で測る項目ではないので整合） |
| §1.9 `gh pr list` の field と `mergedBy` 規則 | §1.9 と §7 見出しが同じ `--json number,mergeCommit,mergedBy,files`、「W0a で B が存在してから有効」は §1.9/§9 U-06 行で同文 | — |
| §2 の行数 | data 行 52、`新規` 10 | `grep -c '^| '` = 54（header + 区切り + 52） |
| §9 の行数と決定 | data 行 41、決定 (1)〜(11)。決定 (5) に Y-09 の 1 句、(6) に X-01 の句、(10)(11) は v10 のまま | D-024-126 の「41 risk rows / decisions (1)-(11)」と一致 |
| §11 #1〜#24 | 24 行、#23（操作者は author にならない）と #24（auto-merge off）が新設 | D-024-126 と一致 |
| Status log v11 | fixed 27 id（X-01〜X-07、Y-01〜Y-08、Y-10〜Y-12、Y2-11〜Y2-17、Y2-19、Y2-21）、residual Y-09、handout-only X-08/Y2-18/Y2-20 を全部列挙 | 処分表の集計 27/1/3 と一致 |
| 用語の初出 | `<P>`・`audit-r2` は §1.1、A/B は §1.3 の初出で `machine account A/B（§1.10 (a)）` と gloss、`HumanShell` は §1.7 (1) の初出で【hcom regime】の引用内、code owner は L5 の用語行と §1.6 の同段落で定義 | 定義前の裸の使用は見つからない |
| 版の字面 | §7「今（採択）」行が「本計画 v10 の採択」（Z-03）、§4 前書きの handout 一覧が「v10 で更新」（Z-06） | handout の見出しは両脚とも v11 |

## (3) handout との一致（§4 #7/#8/#8b/#10 対 `leg2.md`）

| 項目 | 計画 | handout | 結果 |
|---|---|---|---|
| taint 5 名 | §1.7 (2)、§4 #7 | #7 L88/L92 の loop が同じ 5 名 | 一致 |
| canary.pid の書込と kill | §4 #7（pid を `out/canary.pid` に書かせ、file を見てから `pgrep`）、#10 | #7 L84 の prompt が `start_new_session` の子の pid を書く、L95 が `canary_pid=`/`CANARY-PID-EMPTY` の後に `pgrep -fl 'sleep 600'`; #10 L110 が pid を kill し `canary_kill_exit=` | 一致 |
| `pgrep_exit` | §4 #8: `pgrep -fl -- '--profile pilot-'` | #8 L101: `pgrep -fl omp >/dev/null; echo pgrep_exit=$?` | 不一致、かつ両方とも自己一致（Z-01） |
| `HERDR_BIN`/`HERDR-SOCK-EMPTY` ガード | §4 #8b（空ガード、`seat-audit/bin` の link） | #8b L104: `HERDR_BIN` 空で exit、`[ -n "$HERDR_SOCKET_PATH" ]` 空で `HERDR-SOCK-EMPTY` | 一致 |
| marker、first-match grep、full-path 等価、launch-only exit | §4 #8b | L104: `touch mark.<form>`、`find -newer`、`grep -o -m1 … \| head -1`、`case "$v" in "$PILOT/seat-audit/omp")`、`x=$?; sleep 25; hcom list; exit $x` | 一致 |
| pilot3/pilot3u の kill と settle | §4 #8b/#10（`sleep 5`） | L104 末尾と L110 で両 tag を kill; settle は `sleep 2` | kill は一致、settle の秒数が不一致（Z-05） |
| 見出しの版 | — | `leg1.md` L1・`leg2.md` L1 とも「plan 025 v11 §4」 | 一致 |
| 内部整合（変数の定義順、main shell の行） | — | `N`/`launch_ts`（L82）、`ANAME`（L90）、`wpid`（L98）、`HERDR_BIN`（L104）は使用より前; `N`/`launch_ts`/`ANAME` は pipeline の外の独立行。`wpid`/`HERDR_BIN` は同一ブロック内で定義→使用 | 一致 |
| handout の所見 id | — | `leg2.md` が引く `Y-12`（L103）は Y1 の Y-12（掃除一覧）と Y2 の Y2-12（`shell_env.json`）の両方に読める; `Y-15`/`Y-18`/`Y-19`/`Y-20` は Y1 に無い番号なので一意 | 字面（Z-07） |

## (4) 所見

| id | prio | file and section | problem | evidence | fix |
|---|---|---|---|---|---|
| Z-01 | P1 | 計画 §4 #8（L172）と `leg2.md` #8（L101）、§1.7 (4) の第 3 分岐 | `pgrep_exit` の測定が自己一致で常に 0 になる: pattern（計画 `--profile pilot-`、handout `omp`）はどちらも、その `pgrep` を含む同一 sandbox の `/bin/sh -c "<全文>"` の argv（`hcom omp … --profile pilot-audit …` を含む）に当たる。pgrep は自分を除くが親 shell は除かない。他 sandbox の process が見えなくても 0 が出るので、§1.7 (4) の「それ以外 → block」の第 3 分岐が本番で到達不能だと誤って確定し、`-r2` 再試行が生存席の横で走る（S-09 の経路）。計画と handout の字面も食い違う | §4 #8「0 = 他 sandbox の process が列挙できる」; `leg2.md` L102「`pgrep_exit=0\|1` … 合格」; 同じ class を X-07/Y2-16 が `omp-run.sh` 側で閉じている | 親 shell に当たらない pattern を両方に書く: 例として `pgrep -f 'profile pilot-[w]orker'`（regex は `pilot-worker` = #4c の pilot2 席に当たり、`sh -c` の argv 中の文字列 `pilot-[w]orker` には当たらない）; 期待は「0 = pilot2 が列挙できた、1 = 見えない（第 3 分岐が実在）」に直し、`wpid` の `ps -p` と並べて読む |
| Z-02 | P2 | §1.10 の Y-09 の句、§9 Y-09 行、§3 W0a/W0b 行の完了条件末尾 | 「W0b の記録 PR」を W0b 前の手 merge（≒ 12 本）に数え、§3 W0a/W0b 行も「保護パス PR、操作者 merge」と書くが、D-024-22 の状態行と doctor の helper 検査を failure にする manifest 鍵（W3、P-02）を運ぶその PR は PUT と受理の後にしか書けず、W0b 後の規則では操作者 approve → B merge。節の間で merge 者が食い違う | §1.10「W0b の記録 PR; 各 merge 後に `make update` の停止確認」; §3 W3 行「W0b の記録 PR で failure に切り替える」; §7 W0b 後の行「以後全 PR は操作者が approve してから B が merge」 | 1 句: 「W0b の記録 PR は PUT 後なので操作者 approve → B merge（手 merge は ≒ 11 本: W-step 10 本 + `ruleset-main.json` の PR）」を §1.10・§9 Y-09 行・§3 W0a/W0b 行に |
| Z-03 | P3 | §7「今（採択）」行（L215） | 「本計画 v10 の採択」が残る | L215 | `v11` に |
| Z-04 | P3 | §8 W0（L250） | 「固定値一覧 10 項と `codeowners/errors` 空を含む」は、10 項の中に既に `codeowners/errors` と `allow_auto_merge` がある二重の字面 | §7 5b の一覧は 10 項目で末尾 2 項がそれ | 「固定値一覧 10 項（`allow_auto_merge: false` と `codeowners/errors` 空を含む）」に |
| Z-05 | P2 | §4 #10（L175）対 `leg2.md` #10（L110/L111） | settle の秒数が計画 `sleep 5`、handout `sleep 2`（処分表 Y2-20 は 5） | L175「`pgrep` の前に `sleep 5`」; L110「sleep 2」、L111「2 秒の settle」 | どちらかに揃える（handout を 5 に、または計画を 2 に） |
| Z-06 | P3 | §4 前書き（L123） | handout 一覧の「v10 で更新」が残る（Status log v11 と handout 見出しは v11） | L123 | 「v11 で更新」に |
| Z-07 | P3 | `leg2.md` #8b 注記（L103） | 所見 id `Y-12` が Y1 の Y-12 と Y2-12 の両方に読める（処分表は Y2 側を `Y2-12` と改番） | L103「…をそのまま拒む（Y-12）」 | `Y2-12` に（同様に L102 `Y-15`、L105 `Y-18`/`Y-19`、L111 `Y-20` も `Y2-` 前置に揃えると処分表と一致） |

## (5) 確認できた行

- X-01: §1.6「除外だけの PR を orchestrator 単独で merge するのは W0b 前だけ」、§1.9、§1.10 (f)、§3 前書き、§7 W0b 後の行、§9 U-06/U-08 行、§11 #19 が同文。
- X-02: §1.6 と §11 #19 の W-07 が `gh pr view --json author`（両期）、committer を見ない、X 手順 5 前は空振り、W6a に fixture。
- X-03: §3 前書きと §7 W0b 前の行に `plans/**`・`ruleset-main.json` を運ぶ boundary PR と X 手順 0。
- X-04/Y-05: §1.10 (a)、§3 W0a/W0b・W0c・W9・経路外、§7 W0a (3)・workflow 行が全部「B に Workflows write を足して W0a (3) をやり直す」。
- X-05: §11 #18 に「A・B の approval は code owner 規則を満たさず、chain の login 検査は第 2 層」、§9 G-06 行に「W0b の code owner 規則（3 identity + `.github/CODEOWNERS`）」。
- X-06: `protected:`/`exclude:` 節が §1.6・W6a・§11 #21 で一致。
- X-07/Y2-16: §1.7 (4) の「背景子の argv に `<results dir>` を置かず pattern は字面どおり固定」と W6a の process 木 fixture。
- X-08: §4 #7 の注記と `leg2.md` #7 の pid file 書込・存在確認・#10 の kill。
- Y-01: ruleset payload の `require_code_owner_review: true`、`.github/CODEOWNERS`、(f3) の「B の approve でも `BLOCKED`」が §1.10 (f)・§3 X 5b・§7 5b・§8 W0・§9 G-01 行にある。
- Y-02/Y-10: auto-merge off と `autoMergeRequest` null が §1.10 (c)(f)・§2・§3 W6a・§7 2 行・§9 W-11 行・§11 #14/#24; W-11 行は「`--auto` を除きどれも main に届かない」。
- Y-03/Y-06: §7 5b の固定値一覧 10 項、PUT 前の `git log -p`、「file との `diff` ではない」が §1.10 (f)・§3 W0a/W0b・§8 W0 と一致。
- Y-04: §1.6・§1.10 (a)・§3 前書き（a012 の Claude 描画部）・W0c-late・W9・経路外・§7 W0a (3)/workflow 行/E1 前・§11 #8/#23 が「操作者は PR を author しない、patch を B に、追跡 file が変わらなければ local apply」。
- Y-07: §1.9・§7 見出し・§9 U-06 行の `mergedBy.login` 規則と「W0a 後に有効」。
- Y-08: §1.6・§1.9・§7 2 行の「自分の端末の `gh pr diff` と `gh pr view --json files,author,mergedBy` でだけ読む」、§7 W0b 前の行が「証跡と PR 番号を提示」。
- Y-11: W6a validate の `git ls-files CODEOWNERS docs/CODEOWNERS` 空、§7 W6a 行の `codeowners/errors`、§2 CODEOWNERS 行、【gh F5】の引用内容。
- Y-12: 掃除一覧の 5 項（`前後とも` 0 件、`2 account` 0 件、Workflows 分岐の統一、§7 列挙の X 手順 0、B の approve の文）。
- Y2-11/Y2-13/Y2-14/Y2-21: §1.7 (1) の 4 句（他の名は不要、`HOME` は描画値で `env` file は denyWrite と taint の中、`env -i` が落として困るものは無い、getpwuid 経路と `LAUNCH-FAIL`）。
- Y2-12: §1.3 の 3 行、§1.7 (1)(2)、§4 #7、§9 Q-08 行と store 行、3 JSON の denyWrite（`jq` 出力）。
- Y2-17: §1.7 (4) の `lsof -t` 前提（無い・拒否・非空 → block）と W6a の fixture。
- Y2-18: `leg2.md` #8b の first-match・full-path 等価・launch-only exit（L104）と §4 #8b の注記。
- Y2-19: §1.7 (1) の「`hcom-seat` が manifest から絶対値で描画し空なら拒否」、§4 #8b の注記、`leg2.md` #8b の 2 ガード。
- decisions.tsv D-024-123〜126 の記述（code owner 規則、Y 分割、v11 の行数・sha・handout 行数・denyWrite 数）は計画と handout の現物と一致。

## (6) 報告

1. 所見 7 件: P0 0 / P1 1 / P2 2 / P3 4。
2. 最重要は Z-01: §4 #8 の `pgrep_exit` が計画と handout で pattern が違い、しかもどちらも自分を含む `/bin/sh -c` の argv に自己一致するため、§1.7 (4) の第 3 分岐（srt 下で他 sandbox の process が見えない）を測れない。X-07/Y2-16 が `omp-run.sh` 側で閉じた同じ class が pilot の測定に残っている。
3. Z-02 は「W0b の記録 PR」の merge 者が節ごとに違う（手 merge の数に入れつつ、W0b 後の規則では approve → B merge）。1 句で閉じる。
4. 2 期の規則、固定値一覧 10 項、`CODEOWNERS`、auto-merge off、`protected:`/`exclude:`、`shell_env.json`、【hcom regime】の引用、`gh pr list` の field、§2/§9/§11 の行数、Status log、用語の初出は全部一致した。
5. handout: `leg2.md` の #7/#8b/#10 は処分どおり（canary.pid、5 名、first-match、full-path、launch-only exit、2 ガード、marker、両 tag の kill）。残るのは #8 の pattern（Z-01）、settle 秒数（Z-05）、所見 id の前置（Z-07）。
6. ループ停止の可否: P1 が 1 件あるので止められない。Z-01 の修正は計画 §4 #8 の 1 句と `leg2.md` L101 の pattern 1 箇所で済み、P2 2 件はどちらも 1 句の編集。
7. 届かなかった検査: §5・§6・§10 の本文の全文読み（merge/approve の語は §5 の 1 箇所だけ grep で確認）、`leg1.md` の本文（見出しの版のみ確認）、§9 の 41 行のうち名指し以外の行の全文、`025-review-r10-{verification,redteam-y1,redteam-y2}.md` の原文（処分表の要約で代替）= 未確認。
8. 作業は読み取りのみ。書いた file は本 file 1 本。
